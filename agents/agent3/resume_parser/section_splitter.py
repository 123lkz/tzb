"""
SectionSplitter —— 规则/正则段落分割
将简历全文分割为：personal / education / experience / project / skills 等段落
不调用 LLM，确保离线可用。
"""
import re
from loguru import logger


class SectionSplitter:
    """简历段落分割器（纯规则）"""

    # 段落标题关键词映射
    SECTION_PATTERNS = {
        "personal": [
            r"(?:基本信息|个人信息|个人资料|姓\s*名|联系方式)",
        ],
        "education": [
            r"(?:教育背景|教育经历|教\s*育|学\s*历|学校|毕业院校|求学经历)",
        ],
        "experience": [
            r"(?:工作经历|工作背景|工作履历|职业经历|从业经历|实习经历|工作经验)",
        ],
        "project": [
            r"(?:项目经验|项目经历|项\s*目\s*经\s*历|项目实践|项目案例|参与项目|主要项目)",
        ],
        "skills": [
            r"(?:专业技能|技术技能|技能清单|技术栈|职业技术|掌握技能|技能概览|编程技能)",
        ],
    }

    # 汇总的正则表达式
    _combined_pattern = None

    @classmethod
    def _get_combined_pattern(cls) -> re.Pattern:
        """构建统一的段落标题匹配正则"""
        if cls._combined_pattern is None:
            all_patterns = []
            for section_type, patterns in cls.SECTION_PATTERNS.items():
                for pat in patterns:
                    all_patterns.append(f"(?P<{section_type}>{pat})")
            combined = "|".join(all_patterns)
            cls._combined_pattern = re.compile(combined, re.IGNORECASE)
        return cls._combined_pattern

    @classmethod
    def split(cls, full_text: str) -> dict[str, str]:
        """将全文分割为段落

        Args:
            full_text: 简历全文文本

        Returns:
            dict[str, str]: {段落类型: 段落文本}，包含一个 "others" 段落用于未被匹配的内容
        """
        if not full_text.strip():
            logger.warning("输入文本为空，返回空段落")
            return {}

        lines = full_text.split("\n")
        sections: dict[str, list[str]] = {}
        current_section = "others"
        sections[current_section] = []
        pattern = cls._get_combined_pattern()

        for line in lines:
            stripped = line.strip()
            if not stripped:
                if current_section != "others":
                    sections[current_section].append("")
                continue

            match = pattern.search(stripped)
            if match:
                # 找到匹配的段落类型
                for section_type in cls.SECTION_PATTERNS:
                    if match.group(section_type):
                        current_section = section_type
                        if current_section not in sections:
                            sections[current_section] = []
                        # 保留标题行
                        sections[current_section].append(stripped)
                        break
            else:
                sections.setdefault(current_section, []).append(stripped)

        # 合并为字符串
        result = {}
        for key, lines_list in sections.items():
            text = "\n".join(line for line in lines_list if line.strip())
            if text.strip():
                result[key] = text.strip()

        logger.debug(f"段落分割完成: {list(result.keys())}")
        return result


__all__ = ["SectionSplitter"]
