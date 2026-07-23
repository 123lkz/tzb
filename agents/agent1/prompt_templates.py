"""Agent 1 — LLM Prompt 模板"""
from typing import Optional

# 新岗位标注 Prompt
NEW_POSITION_LABEL_PROMPT = """你是一个招聘数据分析专家。以下是一组已聚类的招聘岗位样本，请分析这些岗位的共同特征。

样本岗位名称：
{titles}

样本 JD 片段：
{descriptions}

请以 JSON 格式输出：
{{
    "suggested_name": "建议的标准化中文岗位名称",
    "description": "50-100字自然语言描述，涵盖核心职责和技能要求",
    "core_responsibilities": ["核心职责1", "核心职责2", ...],
    "required_skills": ["必需技能1", "必需技能2", ...],
    "optional_skills": ["加分技能1", ...],
    "typical_applications": ["典型应用场景1", "典型应用场景2", ...],
    "confidence": 0.xx
}}
"""

# 技能趋势摘要 Prompt（备选方案）
SKILL_TREND_SUMMARY_PROMPT = """请分析以下岗位的技能需求趋势数据。

岗位名称：{position_name}
技能趋势数据（各时间窗口频次）：
{trend_data}

请输出该岗位技能需求的演化分析，重点关注：
1. 哪些技能正在快速升温？
2. 哪些技能正在被淘汰？
3. 有哪些值得关注的跨领域技能迁移？

以 JSON 格式输出分析结果。
"""


def format_new_position_prompt(
    titles: list[str],
    descriptions: list[str],
    max_samples: int = 5,
) -> str:
    """格式化新岗位标注 Prompt"""
    titles_text = "\n".join(f"- {t}" for t in titles[:max_samples])
    descs_text = "\n".join(f"- {d[:300]}" for d in descriptions[:3])
    return NEW_POSITION_LABEL_PROMPT.format(
        titles=titles_text,
        descriptions=descs_text,
    )
