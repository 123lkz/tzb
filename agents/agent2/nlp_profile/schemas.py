"""
Pydantic 数据模型 —— 定义三种自然语言画像的结构
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ============================================================
# 1. 技能画像
# ============================================================
class ProficiencyLevels(BaseModel):
    """技能熟练度分级描述"""
    beginner: str = Field(..., description="初级水平：能完成基础任务")
    intermediate: str = Field(..., description="中级水平：能独立完成复杂任务")
    advanced: str = Field(..., description="高级水平：能优化和创新")


class SkillProfile(BaseModel):
    """技能的自然语言画像"""
    skill_id: str = Field(..., description="技能唯一标识")
    name: str = Field(..., description="技能名称，如 PyTorch")
    category: str = Field(default="", description="技能分类，如深度学习框架")
    summary: str = Field(..., description="自然语言概述（LLM生成）")
    prerequisites: list[str] = Field(default_factory=list, description="前置知识列表")
    related_technologies: list[str] = Field(default_factory=list, description="相关技术栈")
    typical_applications: list[str] = Field(default_factory=list, description="典型应用场景")
    proficiency_levels: Optional[ProficiencyLevels] = Field(default=None, description="熟练度分级")
    industry_trend: str = Field(default="", description="行业趋势")
    sources: list[str] = Field(default_factory=list, description="数据来源列表")
    last_updated: str = Field(default="", description="最后更新时间")

    model_config = {"json_schema_extra": {
        "example": {
            "skill_id": "SK001",
            "name": "PyTorch",
            "category": "深度学习框架",
            "summary": "PyTorch是Meta AI开发的开源深度学习框架，以动态计算图和易用性著称...",
            "prerequisites": ["Python", "线性代数", "机器学习基础"],
            "related_technologies": ["TensorFlow", "CUDA", "ONNX"],
            "typical_applications": ["计算机视觉", "自然语言处理", "生成式AI"],
            "industry_trend": "2025年仍是深度学习研究和工业部署的主流框架之一"
        }
    }}


# ============================================================
# 2. 岗位画像
# ============================================================
class PositionProfile(BaseModel):
    """岗位的自然语言画像"""
    position_id: str = Field(..., description="岗位唯一标识")
    name: str = Field(..., description="岗位名称，如大模型算法工程师")
    summary: str = Field(..., description="自然语言概述（LLM生成）")
    core_responsibilities: list[str] = Field(default_factory=list, description="核心职责清单")
    required_skills: list[str] = Field(default_factory=list, description="必需技能列表")
    optional_skills: list[str] = Field(default_factory=list, description="加分技能列表")
    industry_domain: str = Field(default="", description="所属行业领域")
    typical_salary_range: str = Field(default="", description="典型薪资范围")
    experience_level: str = Field(default="", description="典型经验要求")
    sources: list[str] = Field(default_factory=list, description="数据来源")
    last_updated: str = Field(default="", description="最后更新时间")

    model_config = {"json_schema_extra": {
        "example": {
            "position_id": "POS001",
            "name": "大模型算法工程师",
            "summary": "负责大规模语言模型的训练、微调和部署优化...",
            "core_responsibilities": ["模型训练与微调", "推理加速", "数据处理"],
            "required_skills": ["Python", "PyTorch", "分布式训练"],
            "optional_skills": ["Kubernetes", "vLLM", "TensorRT"],
            "industry_domain": "人工智能",
            "typical_salary_range": "40K-80K",
            "experience_level": "3-5年"
        }
    }}


# ============================================================
# 3. 关系画像（幻觉防控的输出）
# ============================================================
class EvidenceItem(BaseModel):
    """证据项"""
    type: str = Field(..., description="证据类型")
    detail: str = Field(..., description="证据详情")
    source: Optional[str] = Field(default=None, description="来源引用")


class RelationProvenance(BaseModel):
    """数据溯源信息"""
    created_by: str = Field(..., description="创建者标识")
    created_at: str = Field(..., description="创建时间")
    llm_model: str = Field(default="", description="使用的LLM模型")
    consensus_rounds: int = Field(default=1, description="共识轮次")


class RelationProfile(BaseModel):
    """技能-岗位关系的自然语言画像（幻觉防控的直接输出）"""
    relation_id: str = Field(..., description="关系唯一标识")
    source_type: str = Field(..., description="起点类型: skill / position")
    source_id: str = Field(..., description="起点标识")
    source_name: str = Field(default="", description="起点名称")
    target_type: str = Field(..., description="终点类型: skill / position")
    target_id: str = Field(..., description="终点标识")
    target_name: str = Field(default="", description="终点名称")
    relation_type: str = Field(..., description="关系类型: requires / depends_on / belongs_to")
    valid: bool = Field(..., description="关系是否有效")
    confidence: float = Field(..., ge=0.0, le=1.0, description="置信度评分")
    explanation: str = Field(..., description="自然语言推理过程")
    evidence: list[EvidenceItem] = Field(default_factory=list, description="支持证据")
    counter_evidence: list[EvidenceItem] = Field(default_factory=list, description="反面证据")
    recommendation: str = Field(default="", description="建议操作")
    provenance: RelationProvenance = Field(..., description="数据溯源")


# ============================================================
# 4. 数据质量检查结果
# ============================================================
class CheckResult(BaseModel):
    """单个数据质量检查的结果"""
    checker_name: str = Field(..., description="检查器名称")
    passed: bool = Field(..., description="是否通过检查")
    score: float = Field(..., ge=0.0, le=1.0, description="质量评分")
    details: str = Field(..., description="自然语言说明")
    flagged_items: list[str] = Field(default_factory=list, description="被标记的问题项")


class QualityReport(BaseModel):
    """数据质量报告"""
    report_id: str = Field(..., description="报告唯一标识")
    record_id: str = Field(..., description="被检查的记录ID")
    overall_score: float = Field(..., ge=0.0, le=1.0, description="综合评分")
    check_results: dict[str, CheckResult] = Field(default_factory=dict, description="各检查器的结果")
    passed: bool = Field(..., description="是否通过质量检查")
    created_at: str = Field(..., description="创建时间")


__all__ = [
    "SkillProfile", "PositionProfile", "RelationProfile",
    "ProficiencyLevels", "EvidenceItem", "RelationProvenance",
    "CheckResult", "QualityReport",
]
