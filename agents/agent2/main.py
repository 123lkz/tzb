"""
Agent 2 主入口 —— 数据质量治理 + 基于自然语言画像的幻觉防控

数据流：
  MongoDB jobs_clean
    → data_quality/registry.run_all() → quality_report
    → nlp_profile/ → 生成/更新 SkillProfile + PositionProfile
    → hallucination_prevention/consensus_manager → 关系验证
    → MongoDB profiles + relation_profiles + jobs_kg + audit_queue

使用方式：
  python -m agents.agent2.main              # 默认模式：处理一批数据
  python -m agents.agent2.main --check-only # 仅做数据质量检查
  python -m agents.agent2.main --batch 100  # 指定处理批次大小
"""
import argparse
import sys
from datetime import datetime
from loguru import logger

from agents.agent2.config import (
    LOG_LEVEL, LOG_FILE, DEFAULT_BATCH_SIZE,
    CONFIDENCE_HIGH_THRESHOLD, CONFIDENCE_MEDIUM_THRESHOLD,
)
from agents.agent2.llm.client import LLMClient
from agents.agent2.dedup.deduper import DedupOrchestrator
from agents.agent2.nlp_profile.profile_store import ProfileStore
from agents.agent2.nlp_profile.skill_profile import SkillProfileBuilder
from agents.agent2.nlp_profile.position_profile import PositionProfileBuilder
from agents.agent2.nlp_profile.relation_profile import RelationProfileBuilder
from agents.agent2.hallucination_prevention.consistency_engine import ConsistencyEngine
from agents.agent2.hallucination_prevention.confidence_scorer import ConfidenceScorer
from agents.agent2.hallucination_prevention.consensus_manager import ConsensusManager
from agents.agent2.data_quality.registry import CheckerRegistry
from agents.agent2.nlp_profile.schemas import QualityReport
# 确保内置检查器被注册（通过 __init_subclass__ 自动注册）
from agents.agent2.data_quality.builtin import (
    CompletenessChecker, ConsistencyChecker,
    TimelinessChecker, PlagiarismChecker, NoiseDetector,
)


class Agent2Orchestrator:
    """Agent 2 主调度器"""

    def __init__(self):
        logger.remove()
        logger.add(sys.stderr, level=LOG_LEVEL)
        logger.add(LOG_FILE, rotation="10 MB", level="INFO")

        logger.info("=== Agent 2 初始化开始 ===")
        self.llm = LLMClient()
        self.store = ProfileStore()
        self.skill_builder = SkillProfileBuilder(self.llm, self.store)
        self.position_builder = PositionProfileBuilder(self.llm, self.store)
        self.relation_builder = RelationProfileBuilder(self.llm, self.store)
        self.engine = ConsistencyEngine(self.llm, self.store)
        self.scorer = ConfidenceScorer()
        self.consensus = ConsensusManager(self.engine, self.scorer)
        logger.info("=== Agent 2 初始化完成 ===")

    def run_data_quality_check(self, batch_size: int = DEFAULT_BATCH_SIZE) -> list[dict]:
        """运行数据质量检查
        
        对 jobs_clean 中的记录，运行所有已注册的数据质量检查器。
        """
        logger.info(f"开始数据质量检查（batch_size={batch_size}）")
        db = self.store.client[self.store.db.name]
        jobs_clean = db["jobs_clean"]
        
        reports = []
        for record in jobs_clean.find().limit(batch_size):
            try:
                results = CheckerRegistry.run_all(record)
                overall_score, all_passed = CheckerRegistry.compute_overall_score(results)
                
                report = QualityReport(
                    report_id=f"QR_{datetime.now().strftime('%Y%m%d%H%M%S')}_{record.get('_id', 'unknown')}",
                    record_id=str(record.get("_id", "")),
                    overall_score=overall_score,
                    check_results={k: v.model_dump() for k, v in results.items()},
                    passed=all_passed,
                    created_at=datetime.now().isoformat(),
                )
                self.store.save_quality_report(report)
                reports.append({
                    "record_id": report.record_id,
                    "overall_score": overall_score,
                    "passed": all_passed,
                    "detail_count": len(report.check_results),
                })
            except Exception as e:
                logger.error(f"Quality check failed for record: {e}")

        passed_count = sum(1 for r in reports if r["passed"])
        logger.info(
            f"数据质量检查完成：共检查 {len(reports)} 条，"
            f"通过 {passed_count} 条，通过率 {passed_count/len(reports)*100:.1f}%"
        )
        return reports

    def build_profiles(self, batch_size: int = DEFAULT_BATCH_SIZE) -> dict:
        """构建/更新自然语言画像"""
        logger.info("开始构建自然语言画像")
        
        skill_profiles = self.skill_builder.build_all_from_jobs_clean(batch_size)
        logger.info(f"技能画像构建完成：{len(skill_profiles)} 个")

        position_profiles = self.position_builder.build_all_from_jobs_clean(batch_size)
        logger.info(f"岗位画像构建完成：{len(position_profiles)} 个")

        return {
            "skill_count": len(skill_profiles),
            "position_count": len(position_profiles),
        }

    def run_hallucination_prevention(self, batch_size: int = None) -> list[dict]:
        """运行幻觉防控
        
        对技能和岗位画像之间的候选关系执行白盒推理验证。
        """
        logger.info("开始幻觉防控关系验证")
        
        skills = self.store.get_all_skill_profiles()
        positions = self.store.get_all_position_profiles()
        logger.info(f"加载 {len(skills)} 个技能画像，{len(positions)} 个岗位画像")

        if not skills or not positions:
            logger.warning("画像不足，跳过幻觉防控")
            return []

        # 对每个技能-岗位对执行共识验证
        results = []
        for skill in skills[:10]:  # 防止一次调用过多
            for position in positions[:10]:
                try:
                    consensus_result = self.consensus.reach_consensus(
                        skill, position, rounds=3, parallel=True
                    )

                    # 构建关系画像
                    relation = self.relation_builder.build_relation(
                        skill=skill,
                        position=position,
                        conclusion=consensus_result,
                        consensus_rounds=consensus_result.get("consensus", {}).get("rounds", 3),
                    )

                    results.append({
                        "skill": skill.name,
                        "position": position.name,
                        "valid": relation.valid,
                        "confidence": relation.confidence,
                        "recommendation": relation.recommendation,
                    })

                    logger.info(
                        f"关系验证：{skill.name} <-> {position.name} | "
                        f"valid={relation.valid}, conf={relation.confidence:.2f}"
                    )
                except Exception as e:
                    logger.error(
                        f"关系验证失败：{skill.name} <-> {position.name} | {e}"
                    )

        valid_count = sum(1 for r in results if r["valid"])
        logger.info(
            f"幻觉防控完成：共检查 {len(results)} 个候选关系，"
            f"有效 {valid_count} 个"
        )
        return results

    def run_pipeline(self, batch_size: int = DEFAULT_BATCH_SIZE) -> dict:
        """运行完整数据流水线"""
        logger.info("=" * 50)
        logger.info("Agent 2 完整流水线启动")
        logger.info("=" * 50)

        step1 = self.run_data_quality_check(batch_size)
        step2 = self.build_profiles(batch_size)
        step3 = self.run_hallucination_prevention()

        summary = {
            "data_quality": {
                "records_checked": len(step1),
                "passed_count": sum(1 for r in step1 if r["passed"]),
            },
            "nlp_profiles": step2,
            "hallucination_prevention": {
                "relationships_checked": len(step3),
                "valid_count": sum(1 for r in step3 if r["valid"]),
            },
        }

        logger.info("=" * 50)
        logger.info("Agent 2 流水线完成")
        logger.info(f"摘要：{summary}")
        logger.info("=" * 50)

        return summary

    def close(self):
        """关闭资源"""
        self.store.close()
        logger.info("Agent 2 资源已释放")


def main():
    parser = argparse.ArgumentParser(description="Agent 2 - 数据质量治理 + 幻觉防控")
    parser.add_argument("--check-only", action="store_true", help="仅运行数据质量检查")
    parser.add_argument("--profile-only", action="store_true", help="仅构建自然语言画像")
    parser.add_argument("--hallucination-only", action="store_true", help="仅运行幻觉防控")
    parser.add_argument("--batch", type=int, default=DEFAULT_BATCH_SIZE, help="批次大小")
    args = parser.parse_args()

    orchestrator = Agent2Orchestrator()

    try:
        if args.dedup:
            o = DedupOrchestrator()
            r = o.run()
            print("Dedup result:", r)
            o.close()
        elif args.check_only:
            orchestrator.run_data_quality_check(args.batch)
        elif args.profile_only:
            orchestrator.build_profiles(args.batch)
        elif args.hallucination_only:
            orchestrator.build_profiles(args.batch)
            orchestrator.run_hallucination_prevention()
        else:
            orchestrator.run_pipeline(args.batch)
    finally:
        orchestrator.close()


if __name__ == "__main__":
    main()
