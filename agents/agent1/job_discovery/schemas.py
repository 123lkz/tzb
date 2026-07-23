"""job_discovery 模块的数据模型"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NewPositionSuggestion(BaseModel):
    """新岗位建议——由新岗位发现模块输出"""
    suggested_name: str  = Field(..., description="LLM 建议的岗位名称")
    description: str = Field(..., description="岗位自然语言描述")
    core_responsibilities: list[str] = Field(default_factory=list, description="核心职责列表")
    typical_applications: list[str] = Field(default_factory=list, description="典型行业应用场景")
    cluster_size: int = Field(default=0, description="簇内记录数（需求热度）")
    novelty_score: float = Field(default=0.0, ge=0.0, le=1.0, description="0~1 新兴度")
    evidence_samples: list[str] = Field(default_factory=list, description="代表性原始 JD 片段")
    related_skills: list[str] = Field(default_factory=list, description="簇内高频技能列表")
    suggested_required_skills: list[str] = Field(default_factory=list, description="建议归入必需技能")
    suggested_optional_skills: list[str] = Field(default_factory=list, description="建议归入加分技能")
    typical_salary_range: dict = Field(default_factory=dict, description="薪资范围 {min, max, avg}")
    typical_experience: str = Field(default="", description="经验要求")
    data_sources: list[str] = Field(default_factory=list, description="数据来源平台列表")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="LLM 标注置信度")
    provenance: dict = Field(default_factory=dict, description="溯源信息")


class ClusterInfo(BaseModel):
    """聚类中间结果"""
    cluster_id: int = Field(..., description="簇编号（-1 表示噪声）")
    size: int = Field(0, description="簇内记录数")
    centroid: list[float] = Field(default_factory=list, description="簇质心向量")
    sample_indices: list[int] = Field(default_factory=list, description="代表性样本索引")
    titles_sample: list[str] = Field(default_factory=list, description="样本岗位名")
    text_sample: list[str] = Field(default_factory=list, description="样本文本片段")


class ClusteringResult(BaseModel):
    """聚类完整结果"""
    n_records: int = Field(0, description="输入记录数")
    n_clusters: int = Field(0, description="有效簇数（不含噪声）")
    n_noise: int = Field(0, description="噪声点数")
    clusters: list[ClusterInfo] = Field(default_factory=list, description="各簇信息")
    method: str = Field("hdbscan", description="使用的聚类方法")
    typical_applications: list[str] = Field(default_factory=list, description="典型行业应用场景")
