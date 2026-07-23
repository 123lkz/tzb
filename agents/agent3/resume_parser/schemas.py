"""
简历解析数据模型 —— ResumeProfile 及相关嵌套模型
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    """个人信息"""
    name: str = Field(default="", description="姓名")
    phone: str = Field(default="", description="电话")
    email: str = Field(default="", description="邮箱")
    education_level: str = Field(default="", description="最高学历：博士/硕士/本科/大专")
    years_of_experience: float = Field(default=0.0, description="工作经验年数")
    current_position: str = Field(default="", description="当前职位")
    current_company: str = Field(default="", description="当前公司")


class Education(BaseModel):
    """教育经历"""
    school: str = Field(default="", description="学校名称")
    degree: str = Field(default="", description="学位")
    major: str = Field(default="", description="专业")
    start_date: str = Field(default="", description="开始时间 YYYY-MM")
    end_date: str = Field(default="", description="结束时间 YYYY-MM")


class WorkExperience(BaseModel):
    """工作经历"""
    company: str = Field(default="", description="公司名称")
    position: str = Field(default="", description="职位名称")
    start_date: str = Field(default="", description="开始时间 YYYY-MM")
    end_date: str = Field(default="", description="结束时间 YYYY-MM")
    responsibilities: list[str] = Field(default_factory=list, description="工作职责")
    achievements: list[str] = Field(default_factory=list, description="工作成就")


class ProjectExperience(BaseModel):
    """项目经验"""
    name: str = Field(default="", description="项目名称")
    role: str = Field(default="", description="担任角色")
    description: str = Field(default="", description="项目描述")
    technologies: list[str] = Field(default_factory=list, description="使用技术栈")
    highlights: list[str] = Field(default_factory=list, description="项目亮点")


class ResumeProfile(BaseModel):
    """简历的自然语言画像"""
    resume_id: str = Field(..., description="简历唯一标识（UUID）")
    candidate_name: str = Field(default="", description="候选人姓名")
    personal_info: PersonalInfo = Field(default_factory=PersonalInfo, description="个人信息")
    education: list[Education] = Field(default_factory=list, description="教育经历列表")
    work_experiences: list[WorkExperience] = Field(default_factory=list, description="工作经历列表")
    project_experiences: list[ProjectExperience] = Field(default_factory=list, description="项目经验列表")
    skills: list[str] = Field(default_factory=list, description="全部技能清单（扁平化，经过语义归一）")
    raw_sections: dict[str, str] = Field(default_factory=dict, description="原始分段文本，用于溯源")
    parsing_method: str = Field(default="rule", description="解析方式: llm / rule / hybrid")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="整体解析置信度")
    source_file: str = Field(default="", description="简历源文件名")
    created_at: str = Field(default="", description="创建时间")

    model_config = {"json_schema_extra": {
        "example": {
            "resume_id": "RES-20260715-001",
            "candidate_name": "张三",
            "skills": ["Python", "PyTorch", "SQL"],
            "parsing_method": "llm",
            "confidence": 0.92,
            "source_file": "zhang_san_resume.pdf",
        }
    }}


__all__ = [
    "PersonalInfo", "Education", "WorkExperience",
    "ProjectExperience", "ResumeProfile",
]
