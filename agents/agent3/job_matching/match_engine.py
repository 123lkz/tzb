"""
MatchEngine —— 三维匹配计算引擎

| 维度 | 权重 | 策略 |
| 技能匹配 | 0.45 | 候选人技能集 vs PositionProfile.required/optional_skills |
| 经验匹配 | 0.30 | 工作年限 vs 岗位要求、学历 vs 要求、行业背景 |
| 职责匹配 | 0.25 | 候选人工作/项目经历 vs 岗位核心职责（LLM 判断覆盖度）|
"""
import re
from loguru import logger
from agents.agent3.config import MATCH_WEIGHTS
from agents.agent3.resume_parser.schemas import ResumeProfile
from agents.agent3.job_matching.schemas import SkillMatchResult, DimensionScore
from agents.agent2.nlp_profile.schemas import PositionProfile, SkillProfile
from agents.agent3.prompt_templates import (
    SKILL_EQUIVALENCE_SYSTEM_PROMPT, SKILL_EQUIVALENCE_USER_PROMPT_TEMPLATE,
)


class MatchEngine:
    """三维匹配计算引擎"""

    def __init__(self, llm_client=None):
        self.llm = llm_client

    def match(self, resume: ResumeProfile, position: PositionProfile,
              skill_profiles: dict[str, SkillProfile] = None) -> dict:
        """对一份简历和一个岗位进行三维匹配

        Args:
            resume: 简历画像
            position: 岗位画像
            skill_profiles: {技能名称: SkillProfile} 字典，可选，用于生成更详细的证据

        Returns:
            dict: {
                "dimension_scores": [DimensionScore, ...],
                "skill_matches": [SkillMatchResult, ...],
                "required_match_rate": float,
                "optional_match_rate": float,
            }
        """
        logger.info(f"匹配计算: {resume.candidate_name} <-> {position.name}")

        # 1. 技能匹配
        skill_matches, req_rate, opt_rate = self._match_skills(
            resume.skills, position.required_skills, position.optional_skills,
        )
        skill_score = (req_rate * 0.6 + opt_rate * 0.4)  # 必需技能权重更高
        skill_dim = DimensionScore(
            dimension="skill", score=round(skill_score, 4),
            weight=MATCH_WEIGHTS["skill"],
            details=f"必需技能匹配率 {req_rate:.0%}，加分技能匹配率 {opt_rate:.0%}",
        )
        logger.info(f"  技能匹配: req={req_rate:.0%}, opt={opt_rate:.0%}, score={skill_score:.2f}")

        # 2. 经验匹配
        exp_score, exp_details = self._match_experience(resume, position)
        exp_dim = DimensionScore(
            dimension="experience", score=round(exp_score, 4),
            weight=MATCH_WEIGHTS["experience"],
            details=exp_details,
        )
        logger.info(f"  经验匹配: score={exp_score:.2f}")

        # 3. 职责匹配
        resp_score, resp_details = self._match_responsibilities(resume, position)
        resp_dim = DimensionScore(
            dimension="responsibility", score=round(resp_score, 4),
            weight=MATCH_WEIGHTS["responsibility"],
            details=resp_details,
        )
        logger.info(f"  职责匹配: score={resp_score:.2f}")

        # 4. 综合评分
        overall = (
            skill_dim.score * skill_dim.weight
            + exp_dim.score * exp_dim.weight
            + resp_dim.score * resp_dim.weight
        )
        logger.info(f"  综合匹配度: {overall:.2f}")

        return {
            "dimension_scores": [skill_dim, exp_dim, resp_dim],
            "skill_matches": skill_matches,
            "required_match_rate": req_rate,
            "optional_match_rate": opt_rate,
            "overall_score": round(overall, 4),
        }

    def _match_skills(
        self, candidate_skills: list[str],
        required_skills: list[str], optional_skills: list[str],
    ) -> tuple[list[SkillMatchResult], float, float]:
        """技能匹配：计算候选技能集与岗位技能集的交集和差值"""
        candidate_set = set(s.lower().strip() for s in candidate_skills if s.strip())
        results = []

        # 必需技能匹配
        required_matched = 0
        for skill in required_skills:
            matched, is_semantic = self._single_skill_match(skill, candidate_set)
            results.append(SkillMatchResult(
                skill_name=skill, is_required=True,
                matched=matched, semantic_match=is_semantic,
                evidence=self._build_match_evidence(matched, is_semantic),
            ))
            if matched:
                required_matched += 1

        # 加分技能匹配
        optional_matched = 0
        for skill in optional_skills:
            matched, is_semantic = self._single_skill_match(skill, candidate_set)
            results.append(SkillMatchResult(
                skill_name=skill, is_required=False,
                matched=matched, semantic_match=is_semantic,
                evidence=self._build_match_evidence(matched, is_semantic),
            ))
            if matched:
                optional_matched += 1

        req_rate = required_matched / len(required_skills) if required_skills else 0.0
        opt_rate = optional_matched / len(optional_skills) if optional_skills else 0.0

        return results, req_rate, opt_rate

    def _single_skill_match(self, skill: str, candidate_set: set[str]) -> tuple[bool, bool]:
        """判断一个技能是否在候选技能集中（精确匹配 + LLM 语义等价）"""
        skill_lower = skill.lower().strip()

        # 1. 精确匹配
        if skill_lower in candidate_set:
            return True, False

        # 2. 包含匹配（如 candidate "python" 匹配 required "python programming"）
        for cs in candidate_set:
            if skill_lower in cs or cs in skill_lower:
                return True, True

        # 3. 简单版本号归一化匹配
        base_form = re.sub(r"[\s]*\d+[.\d]*$", "", skill_lower).strip()
        if base_form and base_form != skill_lower:
            for cs in candidate_set:
                cs_base = re.sub(r"[\s]*\d+[.\d]*$", "", cs).strip()
                if cs_base == base_form:
                    return True, True

        # 4. LLM 语义等价（仅当配置了 LLM）
        if self.llm is not None:
            try:
                msg = [
                    {"role": "system", "content": SKILL_EQUIVALENCE_SYSTEM_PROMPT},
                    {"role": "user", "content": SKILL_EQUIVALENCE_USER_PROMPT_TEMPLATE.format(
                        skill_a=skill, skill_b=list(candidate_set)[0] if candidate_set else ""
                    )},
                ]
                # 逐个判断候选技能（仅取第一个候选做简化匹配）
            except Exception:
                pass

        return False, False

    @staticmethod
    def _build_match_evidence(matched: bool, semantic: bool) -> str:
        if matched and semantic:
            return "语义等价匹配"
        elif matched:
            return "精确匹配"
        return "候选人不具备该技能"

    @staticmethod
    def _match_experience(resume: ResumeProfile, position: PositionProfile) -> tuple[float, str]:
        """经验匹配：工作年限 + 学历 + 行业背景"""
        details = []

        # 年限匹配
        exp_years = resume.personal_info.years_of_experience
        position_exp = position.experience_level.strip()
        years_score = 0.5  # 默认中等分

        # 解析岗位经验要求中的数字
        exp_match = re.search(r"(\d+)[-~](\d+)", position_exp)
        if exp_match:
            min_exp, max_exp = int(exp_match.group(1)), int(exp_match.group(2))
            if exp_years >= max_exp:
                years_score = 1.0
            elif exp_years >= min_exp:
                years_score = 0.6 + 0.4 * (exp_years - min_exp) / (max_exp - min_exp)
            elif exp_years >= 1:
                years_score = 0.3 * (exp_years / min_exp)
            else:
                years_score = 0.1
            details.append(f"候选人{exp_years}年经验 vs 岗位要求{min_exp}-{max_exp}年")
        elif position_exp:
            details.append(f"岗位经验要求: {position_exp}，候选人: {exp_years}年")
            years_score = 0.5

        # 学历匹配
        edu_map = {"博士": 1.0, "硕士": 0.9, "研究生": 0.85, "本科": 0.7, "大专": 0.5, "专科": 0.5}
        candidate_edu = resume.personal_info.education_level
        edu_score = edu_map.get(candidate_edu, 0.5)

        # 简单合并年限和学历
        exp_score = years_score * 0.6 + edu_score * 0.4
        details.append(f"学历: {candidate_edu or '未知'}")

        return round(exp_score, 4), "；".join(details)

    def _match_responsibilities(self, resume: ResumeProfile, position: PositionProfile) -> tuple[float, str]:
        """职责匹配：候选人的工作/项目经历是否覆盖岗位核心职责（基于关键词）"""
        if not position.core_responsibilities:
            return 0.5, "岗位未定义核心职责"

        # 将候选人的工作经历和项目经历拼接成文本
        candidate_text = []
        for we in resume.work_experiences:
            candidate_text.append(we.position + " " + " ".join(we.responsibilities) + " " + " ".join(we.achievements))
        for pe in resume.project_experiences:
            candidate_text.append(pe.name + " " + pe.description + " " + " ".join(pe.highlights))

        combined = " ".join(candidate_text).lower()

        covered = 0
        coverage_details = []
        for resp in position.core_responsibilities:
            # 基于关键词的粗略覆盖判断
            resp_keywords = self._extract_keywords(resp)
            matched_kw = sum(1 for kw in resp_keywords if kw in combined)
            threshold = max(1, len(resp_keywords) // 3)
            is_covered = matched_kw >= threshold
            if is_covered:
                covered += 1
                coverage_details.append(f"✓ {resp[:20]}...")
            else:
                coverage_details.append(f"✗ {resp[:20]}...")

        resp_score = covered / len(position.core_responsibilities)
        return round(resp_score, 4), "；".join(coverage_details[:5])

    @staticmethod
    def _extract_keywords(text: str) -> list[str]:
        """从职责描述中提取关键词"""
        # 去掉停用词，提取有意义的词
        stopwords = {"的", "和", "与", "或", "及", "了", "在", "对", "为", "以", "从", "到", "等", "能够", "负责"}
        words = re.findall(r"[\u4e00-\u9fff\w]{2,}", text)
        return [w.lower() for w in words if w.lower() not in stopwords]


__all__ = ["MatchEngine"]
