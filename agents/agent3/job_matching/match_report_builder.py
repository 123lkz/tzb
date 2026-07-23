"""
MatchReportBuilder —— 匹配报告组装器

将匹配计算结果组装为完整的 MatchReport。
"""
import uuid
from datetime import datetime
from loguru import logger
from agents.agent3.config import (
    RECOMMEND_HIGH, RECOMMEND_MEDIUM, RECOMMEND_LOW,
)
from agents.agent3.resume_parser.schemas import ResumeProfile
from agents.agent3.job_matching.schemas import (
    MatchReport, MatchProvenance, DimensionScore, GapItem,
)
from agents.agent2.nlp_profile.schemas import PositionProfile


class MatchReportBuilder:
    """匹配报告生成器"""

    def build(
        self,
        resume: ResumeProfile,
        position: PositionProfile,
        dimension_scores: list[DimensionScore],
        skill_matches: list,
        req_rate: float,
        opt_rate: float,
        gaps: list[GapItem],
        llm_model: str = "",
    ) -> MatchReport:
        """构建完整的匹配诊断报告"""
        report_id = f"MR-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
        overall = sum(ds.score * ds.weight for ds in dimension_scores)
        confidence = self._compute_confidence(resume, dimension_scores, llm_model)
        recommendation = self._determine_recommendation(overall, req_rate, confidence)
        strengths = self._extract_strengths(skill_matches)
        summary = self._generate_summary(
            resume.candidate_name, position.name, overall, recommendation
        )

        report = MatchReport(
            report_id=report_id,
            candidate_name=resume.candidate_name,
            position_id=position.position_id or "",
            position_name=position.name,
            overall_match_score=round(overall, 4),
            dimension_scores=dimension_scores,
            skill_matches=skill_matches,
            required_skills_match_rate=round(req_rate, 4),
            optional_skills_match_rate=round(opt_rate, 4),
            gaps=gaps,
            strengths=strengths,
            summary=summary,
            recommendation=recommendation,
            confidence=round(confidence, 4),
            provenance=MatchProvenance(
                created_by="agent3",
                created_at=datetime.now().isoformat(),
                llm_model=llm_model,
                resume_profile_ref=resume.resume_id,
                position_profile_ref=position.position_id,
            ),
            created_at=datetime.now().isoformat(),
        )

        logger.info(f"匹配报告生成完成: {report.report_id}")
        logger.info(f"  {resume.candidate_name} <-> {position.name}: "
                     f"overall={overall:.2f}, confidence={confidence:.2f}, "
                     f"recommendation={recommendation}")

        return report

    @staticmethod
    def _compute_confidence(resume: ResumeProfile, dim_scores: list[DimensionScore],
                            llm_model: str) -> float:
        score = 0.7
        if llm_model:
            score += 0.1
        if resume.parsing_method == "llm":
            score += 0.1
        elif resume.parsing_method == "hybrid":
            score += 0.05
        if resume.confidence > 0.8:
            score += 0.05
        if len(resume.skills) > 5:
            score += 0.05
        if len(dim_scores) == 3:
            score += 0.05
        return min(score, 1.0)

    @staticmethod
    def _determine_recommendation(overall: float, req_rate: float, confidence: float) -> str:
        effective_score = overall * (0.8 + 0.2 * confidence)
        if effective_score >= RECOMMEND_HIGH and req_rate >= 0.8:
            return "highly_recommend"
        elif effective_score >= RECOMMEND_MEDIUM:
            return "recommend"
        elif effective_score >= RECOMMEND_LOW:
            return "consider"
        else:
            return "not_recommend"

    @staticmethod
    def _extract_strengths(skill_matches: list) -> list[str]:
        strengths = []
        matched_required = [m for m in skill_matches if m.is_required and m.matched]
        if matched_required:
            names = [m.skill_name for m in matched_required[:3]]
            strengths.append(f"具备核心必需技能: {', '.join(names)}")
        return strengths[:5]

    @staticmethod
    def _generate_summary(candidate: str, position: str, overall: float,
                          recommendation: str) -> str:
        rec_labels = {
            "highly_recommend": "高度推荐",
            "recommend": "推荐",
            "consider": "可以考虑",
            "not_recommend": "暂不推荐",
        }
        rec_label = rec_labels.get(recommendation, "未知")
        return (f"候选人{ candidate }与岗位{ position }的综合匹配度为 "
                f"{overall:.0%}，评估结论为{ rec_label }。")


__all__ = ["MatchReportBuilder"]
