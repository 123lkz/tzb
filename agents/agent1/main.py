"""Agent 1 主入口 —— 新岗位发现 + 能力更新

数据流：
  MongoDB jobs_clean
    → job_discovery/ → 聚类 → 新兴检测 → LLM 标注 → NewPositionSuggestion[]
    → skill_evolution/ → 趋势分析 → 演化检测 → SkillChangeSuggestion[]
    → output_adapter/ → 统一包装 → MongoDB agent1_output
    → (后续由 Agent2 校验后入 jobs_kg → Neo4j)

使用方式：
  python -m agents.agent1.main                          # 完整流水线
  python -m agents.agent1.main --discovery-only          # 仅新岗位发现
  python -m agents.agent1.main --evolution-only          # 仅能力演化检测
  python -m agents.agent1.main --batch 200               # 指定批次大小
  python -m agents.agent1.main --industry "人工智能"      # 指定行业范围
"""
import argparse
import sys
from datetime import datetime
from loguru import logger

from agents.agent1.config import (
    LOG_LEVEL, LOG_FILE, DEFAULT_BATCH_SIZE,
    NOVELTY_THRESHOLD, MONGODB_URI, MONGODB_DB,
    JOBS_CLEAN_COLLECTION, PROFILES_COLLECTION,
)


class Agent1Orchestrator:
    """Agent 1 主调度器"""

    def __init__(self):
        logger.remove()
        logger.add(sys.stderr, level=LOG_LEVEL)
        logger.add(LOG_FILE, rotation="10 MB", level="INFO")

        logger.info("=== Agent 1 初始化开始 ===")

        # 复用 Agent2 的 LLM 客户端
        try:
            from agents.agent2.llm.client import LLMClient
            self.llm = LLMClient()
            logger.info("LLM 客户端已加载（复用 Agent2）")
        except ImportError:
            logger.warning("Agent2 LLM 客户端不可用，使用 None（降级统计模式）")
            self.llm = None

        # 复用 Agent2 的 ProfileStore（读取已有岗位画像）
        try:
            from agents.agent2.nlp_profile.profile_store import ProfileStore
            self.profile_store = ProfileStore()
            logger.info("ProfileStore 已加载（复用 Agent2）")
        except ImportError:
            logger.warning("Agent2 ProfileStore 不可用，将无法对比已有岗位画像")
            self.profile_store = None

        # 初始化模块
        from agents.agent1.job_discovery import JobClusterer, NoveltyDetector, LabelGenerator
        from agents.agent1.skill_evolution import SkillTrendAnalyzer, EvolutionDetector
        from agents.agent1.output_adapter import ChangeRecordBuilder, GraphInterface

        self.clusterer = JobClusterer()
        self.novelty_detector = NoveltyDetector(threshold=NOVELTY_THRESHOLD)
        self.label_generator = LabelGenerator(llm_client=self.llm)

        self.trend_analyzer = SkillTrendAnalyzer()
        self.evolution_detector = EvolutionDetector()

        self.record_builder = ChangeRecordBuilder()
        self.graph_iface = GraphInterface()

        logger.info("=== Agent 1 初始化完成 ===")

    def _load_records(self, batch_size: int = DEFAULT_BATCH_SIZE,
                       industry: str = None) -> list[dict]:
        """从 MongoDB jobs_clean 加载数据"""
        if self.profile_store is None:
            logger.warning("ProfileStore 不可用，无法加载数据")
            return []

        db = self.profile_store.client[self.profile_store.db.name]
        collection = db[JOBS_CLEAN_COLLECTION]

        query = {}
        if industry:
            query["industry"] = {"$regex": industry, "$options": "i"}

        records = list(collection.find(query).limit(batch_size))
        logger.info(f"从 jobs_clean 加载 {len(records)} 条记录" +
                     (f" (industry={industry})" if industry else ""))
        return records

    def _load_existing_profiles(self) -> dict[str, list[float]]:
        """加载已有岗位画像的 embedding，用于新兴性对比"""
        if self.profile_store is None:
            return {}

        positions = self.profile_store.get_all_position_profiles()
        if not positions:
            logger.info("无已有岗位画像，跳过新兴性对比")
            return {}

        # 对已有岗位进行向量化
        pos_names = [p.name for p in positions]
        pos_texts = [f"{p.name} {p.summary}" for p in positions]

        if not self.clusterer._model:
            self.clusterer._load_model()
        try:
            embeddings = self.clusterer.embed_texts(pos_texts)
            result = {}
            for name, emb in zip(pos_names, embeddings):
                result[name] = emb
            logger.info(f"已加载 {len(result)} 个已有岗位画像")
            return result
        except Exception as e:
            logger.warning(f"加载已有岗位画像失败: {e}")
            return {}

    def run_discovery(self, batch_size: int = DEFAULT_BATCH_SIZE,
                       industry: str = None) -> list:
        """运行新岗位发现流水线

        Returns:
            发现的 NewPositionSuggestion 列表
        """
        logger.info("=" * 50)
        logger.info("开始新岗位发现")
        logger.info("=" * 50)

        # 1. 加载数据
        records = self._load_records(batch_size, industry)
        if not records:
            logger.warning("未加载到数据，跳过新岗位发现")
            return []

        # 2. 聚类
        cluster_result = self.clusterer.cluster(records)
        if not cluster_result.clusters:
            logger.info("未发现有效簇，跳过")
            return []

        # 3. 加载已有岗位画像
        existing_embeddings = self._load_existing_profiles()

        # 4. 新兴性检测
        suggestions = []
        for cluster in cluster_result.clusters:
            novelty_result = self.novelty_detector.detect(
                cluster, existing_embeddings
            )
            if novelty_result["is_novel"]:
                # 取簇内记录用于 LLM 标注
                cluster_records = [
                    records[i] for i in cluster.sample_indices
                    if i < len(records)
                ]
                suggestion = self.label_generator.generate(cluster, cluster_records)
                suggestion.novelty_score = novelty_result["novelty_score"]
                suggestion.provenance["batch_id"] = f"B{datetime.now().strftime('%Y%m%d%H%M%S')}"
                suggestions.append(suggestion)

        logger.info(f"新岗位发现完成: 共发现 {len(suggestions)} 个潜在新岗位")
        return suggestions

    def run_evolution(self, batch_size: int = DEFAULT_BATCH_SIZE,
                       industry: str = None) -> list:
        """运行能力演化检测流水线

        Returns:
            检测到的 SkillChangeSuggestion 列表
        """
        logger.info("=" * 50)
        logger.info("开始能力演化检测")
        logger.info("=" * 50)

        # 1. 加载数据
        records = self._load_records(batch_size, industry)
        if not records:
            logger.warning("未加载到数据，跳过能力演化检测")
            return []

        # 2. 趋势分析
        trends = self.trend_analyzer.analyze(records)
        if not trends:
            logger.info("未满足趋势分析的最低记录要求")
            return []

        # 3. 演化检测
        suggestions = self.evolution_detector.detect(trends)
        for s in suggestions:
            s.provenance["batch_id"] = f"B{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # 统计
        type_counts = {}
        for s in suggestions:
            type_counts[s.change_type] = type_counts.get(s.change_type, 0) + 1
        logger.info(f"能力演化检测完成: {type_counts}")
        return suggestions

    def run_pipeline(self, batch_size: int = DEFAULT_BATCH_SIZE,
                      industry: str = None) -> dict:
        """运行完整流水线"""
        logger.info("=" * 50)
        logger.info("Agent 1 完整流水线启动")
        logger.info("=" * 50)

        # Step 1: 新岗位发现
        new_positions = self.run_discovery(batch_size, industry)

        # Step 2: 能力演化检测
        skill_changes = self.run_evolution(batch_size, industry)

        # Step 3: 统一输出到 agent1_output
        if new_positions or skill_changes:
            outputs = self.record_builder.build_batch(new_positions, skill_changes)
            saved = self.graph_iface.save_batch(outputs)

            summary = {
                "new_positions_found": len(new_positions),
                "skill_changes_detected": len(skill_changes),
                "outputs_saved": saved,
            }
        else:
            summary = {
                "new_positions_found": 0,
                "skill_changes_detected": 0,
                "outputs_saved": 0,
            }

        logger.info("=" * 50)
        logger.info("Agent 1 流水线完成")
        logger.info(f"摘要: {summary}")
        logger.info("=" * 50)

        return summary

    def close(self):
        """关闭资源"""
        if self.profile_store:
            self.profile_store.close()
        self.graph_iface.close()
        logger.info("Agent 1 资源已释放")


def main():
    parser = argparse.ArgumentParser(
        description="Agent 1 - 新岗位发现 + 能力更新"
    )
    parser.add_argument(
        "--discovery-only", action="store_true",
        help="仅运行新岗位发现"
    )
    parser.add_argument(
        "--evolution-only", action="store_true",
        help="仅运行能力演化检测"
    )
    parser.add_argument(
        "--batch", type=int, default=DEFAULT_BATCH_SIZE,
        help=f"批次大小（默认 {DEFAULT_BATCH_SIZE}）"
    )
    parser.add_argument(
        "--industry", type=str, default=None,
        help="按行业筛选（如 '人工智能'）"
    )
    args = parser.parse_args()

    orchestrator = Agent1Orchestrator()

    try:
        if args.discovery_only:
            orchestrator.run_discovery(args.batch, args.industry)
        elif args.evolution_only:
            orchestrator.run_evolution(args.batch, args.industry)
        else:
            orchestrator.run_pipeline(args.batch, args.industry)
    finally:
        orchestrator.close()


if __name__ == "__main__":
    main()
