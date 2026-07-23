"""
Agent 3 主入口 —— 简历解析 + 人岗匹配

数据流：
  简历文件 (PDF/Word/TXT)
    -> resume_parser/ -> ResumeProfile
    -> job_matching/ -> MatchReport
    -> MongoDB resume_profiles + match_reports

使用方式：
  python -m agents.agent3.main parse ./resume.pdf
  python -m agents.agent3.main match ./resume.pdf --position "大模型算法工程师"
  python -m agents.agent3.main match ./resume.pdf --match-all
"""
import argparse
import sys
from datetime import datetime
from loguru import logger

from agents.agent3.config import (
    LOG_LEVEL, LOG_FILE, GLOBAL_MATCH_TOP_K,
)
from agents.agent2.config import DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, DEEPSEEK_MODEL
from agents.agent3.resume_parser import ResumeParser
from agents.agent3.job_matching import MatchEngine, GapAnalyzer, MatchReportBuilder, LearningPathGenerator
from agents.agent2.llm.deepseek_client import DeepSeekClient
from agents.agent2.nlp_profile.profile_store import ProfileStore


class Agent3Orchestrator:
    """Agent 3 主调度器"""

    def __init__(self):
        logger.remove()
        logger.add(sys.stderr, level=LOG_LEVEL)
        logger.add(LOG_FILE, rotation="10 MB", level="INFO")

        logger.info("=== Agent 3 初始化开始 ===")

        # LLM
        self.llm = DeepSeekClient(api_key=DEEPSEEK_API_KEY, api_base=DEEPSEEK_API_BASE, model=DEEPSEEK_MODEL)
        self.llm_model = DEEPSEEK_MODEL if DEEPSEEK_API_KEY else ""

        # MongoDB Store
        self.store = ProfileStore()

        # 简历解析
        self.parser = ResumeParser(llm_client=self.llm if self.llm_model else None)

        # 人岗匹配
        self.match_engine = MatchEngine(llm_client=self.llm if self.llm_model else None)
        self.gap_analyzer = GapAnalyzer()
        self.report_builder = MatchReportBuilder()

        logger.info("=== Agent 3 初始化完成 ===")

    def parse_resume(self, file_path: str) -> dict:
        """解析一份简历

        Args:
            file_path: 简历文件路径

        Returns:
            dict: 解析结果摘要
        """
        logger.info(f"开始解析简历: {file_path}")
        profile = self.parser.parse(file_path)

        # 存 MongoDB
        self._save_resume_profile(profile)

        summary = {
            "resume_id": profile.resume_id,
            "candidate_name": profile.candidate_name,
            "skills_count": len(profile.skills),
            "education_count": len(profile.education),
            "work_count": len(profile.work_experiences),
            "project_count": len(profile.project_experiences),
            "parsing_method": profile.parsing_method,
            "confidence": profile.confidence,
        }

        logger.info(f"简历解析完成: {summary}")
        return summary

    def match_position(self, file_path: str, position_name: str = None,
                       match_all: bool = False) -> list[dict]:
        """人岗匹配

        Args:
            file_path: 简历文件路径
            position_name: 指定岗位名称（与 match_all 互斥）
            match_all: 是否全局匹配所有岗位

        Returns:
            list[dict]: 匹配报告摘要列表
        """
        # 1. 解析简历
        logger.info(f"Step 1/3: 解析简历 {file_path}")
        resume = self.parser.parse(file_path)
        self._save_resume_profile(resume)

        # 2. 加载岗位画像
        logger.info("Step 2/3: 加载岗位画像")
        if match_all:
            positions = self.store.get_all_position_profiles()
            logger.info(f"加载全部岗位画像: {len(positions)} 个")
        elif position_name:
            pos = self.store.get_position_profile_by_name(position_name)
            if pos is None:
                raise ValueError(f"未找到岗位: {position_name}")
            positions = [pos]
            logger.info(f"加载指定岗位画像: {position_name}")
        else:
            raise ValueError("请指定 --position 或 --match-all")

        # 3. 加载技能画像（供差距分析使用）
        skill_profiles_raw = self.store.get_all_skill_profiles()
        skill_profiles = {sp.name: sp for sp in skill_profiles_raw}
        self.gap_analyzer = GapAnalyzer(skill_profiles)

        # 4. 执行匹���
        logger.info(f"Step 3/3: 执行匹配")
        results = []
        all_match_data = []

        for position in positions:
            try:
                match_data = self.match_engine.match(resume, position, skill_profiles)
                gaps = self.gap_analyzer.analyze(match_data["skill_matches"])

                # Generate learning paths for each gap
                lp_gen = LearningPathGenerator(llm_client=self.llm if self.llm_model else None)
                for gap in gaps:
                    sp = skill_profiles.get(gap.skill_name)
                    gap.learning_path = lp_gen.generate(gap.skill_name, sp)

                report = self.report_builder.build(
                    resume=resume,
                    position=position,
                    dimension_scores=match_data["dimension_scores"],
                    skill_matches=match_data["skill_matches"],
                    req_rate=match_data["required_match_rate"],
                    opt_rate=match_data["optional_match_rate"],
                    gaps=gaps,
                    llm_model=self.llm_model,
                )

                # 存 MongoDB
                self._save_match_report(report)

                all_match_data.append((report.overall_match_score, report))
            except Exception as e:
                logger.error(f"匹配失败: {position.name} - {e}")

        # 5. 排序（全局匹配取 Top-K，指定岗位取全部）
        all_match_data.sort(key=lambda x: -x[0])

        if match_all:
            top_k = all_match_data[:GLOBAL_MATCH_TOP_K]
        else:
            top_k = all_match_data

        results = []
        for score, report in top_k:
            results.append({
                "position_name": report.position_name,
                "overall_match_score": score,
                "recommendation": report.recommendation,
                "required_skills_match_rate": report.required_skills_match_rate,
                "gap_count": len(report.gaps),
            })

        # 打印摘要
        self._print_results_table(results, match_all)

        return results

    def _save_resume_profile(self, profile):
        """存简历画像到 MongoDB"""
        try:
            data = profile.model_dump(mode="json")
            data["last_updated"] = datetime.now().isoformat()
            self.store.db["resume_profiles"].update_one(
                {"resume_id": profile.resume_id},
                {"$set": data},
                upsert=True,
            )
            logger.info(f"简历已存入 MongoDB: {profile.resume_id}")
        except Exception as e:
            logger.warning(f"简历存储失败: {e}")

    def _save_match_report(self, report):
        """存匹配报告到 MongoDB"""
        try:
            data = report.model_dump(mode="json")
            self.store.db["match_reports"].insert_one(data)
            logger.info(f"匹配报告已存入 MongoDB: {report.report_id}")
        except Exception as e:
            logger.warning(f"匹配报告存储失败: {e}")

    @staticmethod
    def _print_results_table(results: list[dict], is_global: bool):
        """打印匹配结果到控制台"""
        print()
        print("=" * 80)
        if is_global:
            print(f"  全局匹配结果 Top-{len(results)}:")
        else:
            print(f"  指定岗位匹配结果:")
        print("=" * 80)

        for i, r in enumerate(results, 1):
            rec_label = {
                "highly_recommend": "高度推荐",
                "recommend": "推荐",
                "consider": "可以考虑",
                "not_recommend": "暂不推荐",
            }.get(r["recommendation"], r["recommendation"])

            print(f"\n  #{i}  {r['position_name']}")
            print(f"      匹配度: {r['overall_match_score']:.1%}")
            print(f"      建议:   {rec_label}")
            print(f"      必需技能匹配: {r['required_skills_match_rate']:.0%}")
            print(f"      差距项: {r['gap_count']} 项")

        print()
        print("=" * 80)

    def close(self):
        """关闭资源"""
        self.store.close()
        logger.info("Agent 3 资源已释放")


def main():
    parser = argparse.ArgumentParser(description="Agent 3 - 简历解析 + 人岗匹配")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # parse 命令
    parse_parser = subparsers.add_parser("parse", help="仅解析简历")
    parse_parser.add_argument("resume", type=str, help="简历文件路径")

    # match 命令
    match_parser = subparsers.add_parser("match", help="解析并匹配")
    match_parser.add_argument("resume", type=str, help="简历文件路径")
    match_group = match_parser.add_mutually_exclusive_group(required=True)
    match_group.add_argument("--position", type=str, help="指定岗位名称")
    match_group.add_argument("--match-all", action="store_true", help="全局匹配所有岗位")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    orchestrator = Agent3Orchestrator()

    try:
        if args.command == "parse":
            result = orchestrator.parse_resume(args.resume)
            print(f"\n解析完成: {result['candidate_name']}")
            print(f"  方式: {result['parsing_method']}, 置信度: {result['confidence']:.2f}")
            print(f"  技能: {result['skills_count']} 项, 教育: {result['education_count']} 段")
            print(f"  工作经历: {result['work_count']} 段, 项目: {result['project_count']} 段")

        elif args.command == "match":
            if args.position:
                orchestrator.match_position(args.resume, position_name=args.position)
            elif args.match_all:
                orchestrator.match_position(args.resume, match_all=True)

    finally:
        orchestrator.close()


if __name__ == "__main__":
    main()
