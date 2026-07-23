"""
GapAnalyzer —— 差距分析器

对每项不匹配的必需技能，从 SkillProfile 中提取为什么需要的解释，
并给出改进建议。
"""
from loguru import logger
from agents.agent3.job_matching.schemas import SkillMatchResult, GapItem
from agents.agent2.nlp_profile.schemas import SkillProfile


class GapAnalyzer:
    """差距分析器"""

    def __init__(self, skill_profiles: dict[str, SkillProfile] = None):
        self.skill_profiles = skill_profiles or {}

    def analyze(self, skill_matches: list[SkillMatchResult]) -> list[GapItem]:
        """分析差距：从未匹配的必需技能生成差距项

        Args:
            skill_matches: 技能匹配结果列表

        Returns:
            list[GapItem]: 差距清单，按 importance 降序排列
        """
        gaps = []

        for match in skill_matches:
            if not match.is_required:
                continue
            if match.matched:
                continue

            skill_name = match.skill_name
            sp = self.skill_profiles.get(skill_name)

            if sp:
                reason = sp.summary[:200] if sp.summary else f"{skill_name} 是该岗位的必需技能"
                suggestion = self._generate_suggestion(sp)
                importance = "high"
            else:
                reason = f"{skill_name} 是该岗位的必需技能，但缺少详细画像"
                suggestion = f"建议系统学习 {skill_name}"
                importance = "high"

            gaps.append(GapItem(
                skill_name=skill_name,
                importance=importance,
                reason=reason,
                suggestion=suggestion,
            ))

        importance_order = {"high": 0, "medium": 1, "low": 2}
        gaps.sort(key=lambda g: importance_order.get(g.importance, 99))

        logger.info(f"差距分析完成: 共 {len(gaps)} 项差距")
        return gaps

    @staticmethod
    def _generate_suggestion(skill_profile: SkillProfile) -> str:
        """根据 SkillProfile 生成学习建议"""
        parts = []
        if skill_profile.prerequisites:
            parts.append(f"前置知识: {''.join(skill_profile.prerequisites[:3])}")
        if skill_profile.related_technologies:
            parts.append(f"配套学习: {', '.join(skill_profile.related_technologies[:3])}")
        if skill_profile.typical_applications:
            parts.append(f"实践方向: {', '.join(skill_profile.typical_applications[:2])}")
        if parts:
            return "; ".join(parts)
        return f"建议系统学习 {skill_profile.name}"


__all__ = ["GapAnalyzer"]
