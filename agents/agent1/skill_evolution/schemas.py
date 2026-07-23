"""skill_evolution 模块的数据模型"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TrendPoint(BaseModel):
    """单个时间点的技能频次"""
    period: str = Field(..., description="时间窗口标识（如 '2026-Q1'）")
    frequency: float = Field(0.0, description="该时间点技能出现频率")
    record_count: int = Field(0, description="该时间点的记录数")


class SkillChangeSuggestion(BaseModel):
    """技能变更建议——由能力演化检测模块输出"""
    position_name: str = Field(..., description="所属岗位")
    skill_name: str = Field(..., description="技能名称")
    change_type: str = Field(..., description="变更类型: new/dying/rising/declining")
    trend_score: float = Field(0.0, ge=-1.0, le=1.0, description="-1~1 趋势强度")
    frequency_before: float = Field(0.0, ge=0.0, le=1.0, description="上一周期出现频率")
    frequency_after: float = Field(0.0, ge=0.0, le=1.0, description="当前周期出现频率")
    time_window: dict = Field(default_factory=dict, description="{start, end} 分析时间范围")
    trend_points: list[TrendPoint] = Field(default_factory=list, description="各时间点频次明细")
    sample_jds: list[str] = Field(default_factory=list, description="出现该技能的原始 JD 片段")
    suggestion: str = Field(default="", description="建议操作（加入必须/移出/关注）")
    cross_domain_flag: bool = Field(default=False, description="是否为跨领域迁移")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="检测置信度")
    provenance: dict = Field(default_factory=dict, description="溯源信息")


class PositionSkillTrend(BaseModel):
    """单个岗位的技能趋势汇总（分析中间结果）"""
    position_name: str = Field(..., description="归一化后的岗位名称")
    total_records: int = Field(0, description="该岗位的总记录数")
    time_windows: list[str] = Field(default_factory=list, description="时间窗口列表")
    skill_frequencies: dict[str, list[float]] = Field(
        default_factory=dict,
        description="{skill_name: [freq_window1, freq_window2, ...]}",
    )
    sample_jds: dict[str, list[str]] = Field(
        default_factory=dict,
        description="{skill_name: [sample_jd_fragments]}",
    )
