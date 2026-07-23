"""
ResumeParser —— LLM + 规则混合解析器

优先策略：SectionSplitter 分段 → 对每段调用 LLM 做 NER 抽取
降级策略：LLM 不可用时，用正则抽取基础信息，输出低置信度标记
"""
import re
import uuid
from datetime import datetime
from loguru import logger

from agents.agent3.resume_parser.schemas import (
    ResumeProfile, PersonalInfo, Education, WorkExperience, ProjectExperience,
)
from agents.agent3.resume_parser.section_splitter import SectionSplitter
from agents.agent3.resume_parser.file_extractor import FileExtractor
from agents.agent3.prompt_templates import (
    RESUME_PARSE_SYSTEM_PROMPT, RESUME_PARSE_USER_PROMPT_TEMPLATE,
)


class ResumeParser:
    """简历解析器（LLM + 规则混合）"""

    def __init__(self, llm_client=None):
        self.llm = llm_client
        self.splitter = SectionSplitter()

    def parse(self, file_path: str) -> ResumeProfile:
        """解析一份简历文件

        Args:
            file_path: 简历文件路径

        Returns:
            ResumeProfile: 结构化简历画像
        """
        logger.info(f"开始解析简历: {file_path}")

        # 1. 文件提取
        raw = FileExtractor.extract(file_path)
        full_text = raw.get("full_text", "")

        # 2. 段落分割
        sections = self.splitter.split(full_text)
        logger.info(f"段落分割完成: {list(sections.keys())}")

        resume_id = f"RES-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
        source_file = file_path.split("\\")[-1] or file_path

        # 3. 基于 LLM 的解析（优先）
        if self.llm is not None:
            logger.info("使用 LLM 模式解析简历")
            profile = self._parse_with_llm(resume_id, sections, source_file)
        else:
            logger.info("LLM 未配置，使用规则降级模式解析简历")
            profile = self._parse_with_rules(resume_id, sections, source_file)

        profile.created_at = datetime.now().isoformat()
        profile.raw_sections = sections

        logger.info(f"简历解析完成: {profile.candidate_name}, 方式={profile.parsing_method}, conf={profile.confidence:.2f}")
        return profile

    def _parse_with_llm(self, resume_id: str, sections: dict[str, str], source_file: str) -> ResumeProfile:
        """使用 LLM 逐段解析"""
        profile = ResumeProfile(
            resume_id=resume_id,
            source_file=source_file,
            parsing_method="llm",
            confidence=0.0,
        )

        # 先构建几个容器的累加器
        all_skills = []
        work_experiences = []
        project_experiences = []
        education_list = []
        personal_info = PersonalInfo()

        for section_type, section_text in sections.items():
            try:
                user_prompt = RESUME_PARSE_USER_PROMPT_TEMPLATE.format(section_text=section_text)
                messages = [
                    {"role": "system", "content": RESUME_PARSE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ]
                result = self.llm.chat_with_json(messages, temperature=0.1)
            except Exception as e:
                logger.warning(f"LLM 解析段落 [{section_type}] 失败: {e}")
                continue

            if not isinstance(result, dict) or "error" in result:
                continue

            extracted = result.get("extracted", {})
            section_conf = result.get("confidence", 0.0)

            # 个人信息
            pi = extracted.get("personal_info", {})
            if isinstance(pi, dict):
                if pi.get("name"): personal_info.name = pi["name"]
                if pi.get("phone"): personal_info.phone = pi["phone"]
                if pi.get("email"): personal_info.email = pi["email"]
                if pi.get("education_level"): personal_info.education_level = pi["education_level"]
                if pi.get("years_of_experience"): personal_info.years_of_experience = float(pi["years_of_experience"])

            # 教育经历
            for edu in extracted.get("education", []):
                if isinstance(edu, dict) and edu.get("school"):
                    education_list.append(Education(**edu))

            # 工作经历
            we = extracted.get("work_experience", {})
            if isinstance(we, dict) and we.get("company"):
                work_experiences.append(WorkExperience(**we))

            # 项目经验
            proj = extracted.get("project", {})
            if isinstance(proj, dict) and proj.get("name"):
                project_experiences.append(ProjectExperience(**proj))

            # 技能
            sk = extracted.get("skills", {})
            if isinstance(sk, dict):
                skills_list = sk.get("skills_list", [])
                if isinstance(skills_list, list):
                    all_skills.extend(skills_list)

            profile.confidence = max(profile.confidence, section_conf)

        # 姓名：如果 LLM 没抽到，尝试从 sections 中规则提取
        if not personal_info.name:
            personal_info.name = self._extract_name_from_text(
                sections.get("personal", sections.get("others", ""))
            )

        profile.personal_info = personal_info
        profile.education = education_list
        profile.work_experiences = work_experiences
        profile.project_experiences = project_experiences
        profile.skills = list(dict.fromkeys(all_skills))  # 去重保持顺序
        profile.candidate_name = personal_info.name

        has_meaningful = bool(education_list or work_experiences or project_experiences or all_skills)
        if profile.confidence == 0.0 or not has_meaningful:
            profile.parsing_method = "rule"
            profile = self._parse_with_rules(resume_id, sections, source_file)

        return profile

    def _parse_with_rules(self, resume_id: str, sections: dict[str, str], source_file: str) -> ResumeProfile:
        """纯规则降级解析"""
        all_text = "\n".join(sections.values())
        personal_text = sections.get("personal", all_text)
        skills_text = sections.get("skills", "")

        # 个人信息规则提取
        name = self._extract_name_from_text(personal_text)
        phone = self._extract_phone(personal_text)
        email = self._extract_email(personal_text)
        education_level = self._extract_education_level(all_text)
        years_exp = self._extract_years_of_experience(all_text)

        # 技能列表规则提取
        skills = self._extract_skills(skills_text) if skills_text else []

        personal_info = PersonalInfo(
            name=name, phone=phone, email=email,
            education_level=education_level, years_of_experience=years_exp,
        )

        profile = ResumeProfile(
            resume_id=resume_id,
            candidate_name=name or "未知候选人",
            personal_info=personal_info,
            skills=skills,
            parsing_method="rule",
            confidence=0.4,
            source_file=source_file,
        )

        return profile

    # ============= 正则提取方法 =============

    @staticmethod
    def _extract_name_from_text(text: str) -> str:
        """从文本中提取姓名"""
        # 常见模式：姓名：XXX / 姓 名：XXX / 姓名 XXX
        patterns = [
            r"(?:姓名|姓\s*名)[：:\s]*(\S{2,4})",
            r"(?:名字?)[：:\s]*(\S{2,4})",
            r"(?:候选人)[：:\s]*(\S{2,4})",
        ]
        for pat in patterns:
            m = re.search(pat, text)
            if m:
                return m.group(1).strip()

        # 无关键词时，取第一行前2-4个汉字
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if lines:
            first_line = lines[0].strip()
            # 如果第一行是标准简历标题行，跳过
            if not any(kw in first_line for kw in ["简历", "个人", "基本信息"]):
                name_match = re.search(r"^(\S{2,4})$", first_line)
                if name_match:
                    return name_match.group(1)
        return ""

    @staticmethod
    def _extract_phone(text: str) -> str:
        m = re.search(r"(?:手机|电话|联系方式)[：:\s]*(\d{11})", text)
        if m: return m.group(1)
        m = re.search(r"1[3-9]\d{9}", text)
        return m.group(0) if m else ""

    @staticmethod
    def _extract_email(text: str) -> str:
        m = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        return m.group(0) if m else ""

    @staticmethod
    def _extract_education_level(text: str) -> str:
        levels = ["博士", "硕士", "研究生", "本科", "大专", "专科", "高中"]
        for level in levels:
            if level in text:
                return level
        return ""

    @staticmethod
    def _extract_years_of_experience(text: str) -> float:
        m = re.search(r"(\d+)[\s]*(?:年工作经验|年经验|年工作经历)", text)
        if m: return float(m.group(1))
        # 尝试从毕业时间推算（简单版本）
        m = re.search(r"(?:毕业|入学)[\s\S]*?(\d{4})", text)
        return 0.0

    @staticmethod
    def _extract_skills(text: str) -> list[str]:
        """从技能段落提取技能列表"""
        skills = []
        # 分割符号：中文逗号/英文逗号/顿号/空格/换行/分号
        parts = re.split(r"[，,、；;|\n\r\s]+", text)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            # 过滤掉看起来不像技能的文本（过短/包含非技能关键词）
            if len(part) < 2:
                continue
            if any(kw in part for kw in ["技能", "精通", "熟练", "了解", "熟悉", "掌握"]):
                # 尝试提取具体的技能名称: "熟悉Python" -> "Python"
                skill_match = re.search(r"(?:精通|熟练|了解|熟悉|掌握)\s*(\S+)", part)
                if skill_match:
                    skills.append(skill_match.group(1))
                    continue
            skills.append(part)
        return skills

    # ============= 批量解析接口（预留） =============

    def parse_batch(self, file_paths: list[str]) -> list[ResumeProfile]:
        """批量解析简历（当前为简单串行，后续可升级为并行）

        Args:
            file_paths: 简历文件路径列表

        Returns:
            list[ResumeProfile]: 结构化简历画像列表
        """
        logger.info(f"批量解析 {len(file_paths)} 份简历")
        results = []
        for fp in file_paths:
            try:
                profile = self.parse(fp)
                results.append(profile)
            except Exception as e:
                logger.error(f"批量解析失败: {fp} - {e}")
        return results


__all__ = ["ResumeParser"]
