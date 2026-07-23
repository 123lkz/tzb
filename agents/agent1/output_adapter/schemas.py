"""output_adapter 模块的数据模型 —— 统一输入输出"""
from datetime import datetime
from typing import Optional, Union, Literal
from pydantic import BaseModel, Field


class InputRecord(BaseModel):
    """
    Agent1 的输入数据模型。从 jobs_clean 读取。
    核心字段明确，扩展字段用 extras dict 兜底。
    """
    # === 核心字段（所有场景必需）===
    title: str = Field(..., description="岗位名称")
    description: str = Field(..., description="JD 完整描述文本")
    skills: list[str] = Field(default_factory=list, description="技能标签列表")

    # === 重要字段（增强分析精度）===
    company: Optional[str] = Field(default=None, description="公司名称")
    industry: Optional[str] = Field(default=None, description="行业分类")
    city: Optional[str] = Field(default=None, description="工作城市")
    salary: Optional[str] = Field(default=None, description="薪资范围，如 '20K-40K'")
    experience: Optional[str] = Field(default=None, description="经验要求，如 '3-5年'")
    education: Optional[str] = Field(default=None, description="学历要求")
    pub_date: Optional[str] = Field(default=None, description="发布日期")

    # === 扩展字段（为未来格式变化预留）===
    extras: dict = Field(default_factory=dict, description="兜底字段：任何未知字段")
    raw: dict = Field(default_factory=dict, description="原始记录全文，仅用于溯源")


class Agent1Output(BaseModel):
    """Agent1 的统一输出包装，写入 MongoDB agent1_output 集合"""
    output_id: str = Field(..., description="UUID")
    created_at: str = Field(..., description="创建时间 ISO 格式")
    batch_id: str = Field(..., description="批次标识")
    output_type: str = Field(..., description="输出类型: new_position / skill_change")

    # 输出负载
    payload: dict = Field(..., description="根据 output_type 装载对应的负载数据")

    # 状态管理
    status: str = Field(default="pending", description="pending / verified / rejected / merged")
    verified_by: Optional[str] = Field(default=None, description="Agent2 验证后将更新此字段")
    verification_report_id: Optional[str] = Field(default=None, description="验证报告 ID")

    # 扩展字段（为未来预留）
    tags: list[str] = Field(default_factory=list, description="标签")
    metadata: dict = Field(default_factory=dict, description="扩展元信息")

