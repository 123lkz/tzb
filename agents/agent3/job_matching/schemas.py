"""
人岗匹配数据模型 —— MatchReport 及相关嵌套模型
"""
from typing import Optional
from pydantic import BaseModel, Field


class SkillMatchResult(BaseModel):
    """逐技能匹配结果"""
    skill_name: str = Field(..., description="技能名称")
    is_required: bool = Field(default=False, description="是否为岗位必需技能")
    matched: bool = Field(default=False, description="候选人是否具备该技能")
    semantic_match: bool = Field(default=False, description="是否为语义等价匹配(如 Python3=python)")
    skill_profile_ref: str = Field(default="", description="引用 SkillProfile.skill_id")
    evidence: str = Field(default="", description="匹配证据，如候选人在项目中使用过该技术")


class DimensionScore(BaseModel):
    """维度评分"""
    dimension: str = Field(..., description="维度标识: skill / experience / responsibility")
    score: float = Field(..., ge=0.0, le=1.0, description="该维度得分")
    weight: float = Field(..., ge=0.0, le=1.0, description="该维度权重")
    details: str = Field(default="", description="自然语言说明")



class LearningStep(BaseModel):
    stage: str = Field(..., description="stage name")
    description: str = Field(..., description="learning content")
    duration: str = Field(default="", description="estimated time")
    resources: list[str] = Field(default_factory=list, description="recommended resources")

class LearningPath(BaseModel):
    skill_name: str = Field(..., description="skill name")
    steps: list[LearningStep] = Field(default_factory=list, description="learning steps")

class GapItem(BaseModel):
    """差距项"""
    skill_name: str = Field(..., description="缺失的技能/经验名称")
    importance: str = Field(default="medium", description="重要性: high / medium / low")
    reason: str = Field(default="", description="为什么需要该技能/经验")
    suggestion: str = Field(default="", description="改进建议")
    learning_path: Optional[LearningPath] = Field(default=None, description="structured learning path")


class MatchProvenance(BaseModel):
    """匹配溯源信息"""
    created_by: str = Field(default="agent3", description="创建者标识")
    created_at: str = Field(default="", description="创建时间")
    llm_model: str = Field(default="", description="使用的 LLM 模型")
    resume_profile_ref: str = Field(default="", description="引用 ResumeProfile.resume_id")
    position_profile_ref: str = Field(default="", description="引用 PositionProfile.position_id")


class MatchReport(BaseModel):
    """人岗匹配诊断报告"""
    report_id: str = Field(..., description="报告唯一标识")
    candidate_name: str = Field(default="", description="候选人姓名")
    position_id: str = Field(default="", description="岗位标识")
    position_name: str = Field(default="", description="岗位名称")
    overall_match_score: float = Field(..., ge=0.0, le=1.0, description="综合匹配度")
    dimension_scores: list[DimensionScore] = Field(default_factory=list, description="三维评分明细")
    skill_matches: list[SkillMatchResult] = Field(default_factory=list, description="逐技能匹配结果")
    required_skills_match_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="必需技能匹配率")
    optional_skills_match_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="加分技能匹配率")
    gaps: list[GapItem] = Field(default_factory=list, description="差距清单")
    strengths: list[str] = Field(default_factory=list, description="候选人优势总结")
    summary: str = Field(default="", description="匹配诊断总评")
    recommendation: str = Field(default="", description="推荐建议: highly_recommend / recommend / consider / not_recommend")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="诊断置信度")
    provenance: Optional[MatchProvenance] = Field(default=None, description="数据溯源")
    created_at: str = Field(default="", description="创建时间")


__all__ = [
    "SkillMatchResult", "DimensionScore", "LearningStep", "LearningPath", "GapItem",
    "MatchProvenance", "MatchReport",
]
