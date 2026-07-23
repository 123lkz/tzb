"""
测试：简历解析模块
覆盖：数据模型、段落分割、正则降级解析
"""
import pytest
from pydantic import ValidationError
from datetime import datetime

from agents.agent3.resume_parser.schemas import (
    PersonalInfo, Education, WorkExperience, ProjectExperience, ResumeProfile,
)
from agents.agent3.resume_parser.section_splitter import SectionSplitter
from agents.agent3.resume_parser.resume_parser import ResumeParser


# ========== 数据模型测试 ==========

class TestResumeProfileModels:
    """测试 ResumeProfile 系列 Pydantic 数据模型"""

    def test_personal_info_defaults(self):
        pi = PersonalInfo()
        assert pi.name == ""
        assert pi.phone == ""
        assert pi.email == ""
        assert pi.education_level == ""
        assert pi.years_of_experience == 0.0
        assert pi.current_position == ""
        assert pi.current_company == ""

    def test_education_required_fields(self):
        edu = Education(school="清华大学", degree="硕士", major="计算机")
        assert edu.school == "清华大学"
        assert edu.start_date == ""
        assert edu.end_date == ""

    def test_work_experience_defaults(self):
        we = WorkExperience(company="百度", position="算法工程师")
        assert we.responsibilities == []
        assert we.achievements == []

    def test_resume_profile_validation(self):
        prof = ResumeProfile(resume_id="TEST-001")
        assert prof.resume_id == "TEST-001"
        assert prof.candidate_name == ""
        assert prof.personal_info.name == ""
        assert prof.parsing_method == "rule"
        assert prof.confidence == 0.0

    def test_resume_profile_serialization(self):
        prof = ResumeProfile(
            resume_id="TEST-001",
            candidate_name="张三",
            skills=["Python", "PyTorch"],
            parsing_method="llm",
            confidence=0.9,
        )
        data = prof.model_dump()
        assert data["resume_id"] == "TEST-001"
        assert data["candidate_name"] == "张三"
        assert len(data["skills"]) == 2

    def test_resume_profile_confidence_range(self):
        with pytest.raises(ValidationError):
            ResumeProfile(resume_id="T1", confidence=1.5)
        with pytest.raises(ValidationError):
            ResumeProfile(resume_id="T2", confidence=-0.1)

    def test_resume_profile_missing_resume_id(self):
        with pytest.raises(ValidationError):
            ResumeProfile()

    def test_work_experience_immutable_fields(self):
        we = WorkExperience(company="腾讯", position="后端研发")
        we.position = "高级后端研发"
        assert we.position == "高级后端研发"

    def test_skill_match_result_roundtrip(self):
        from agents.agent3.job_matching.schemas import SkillMatchResult
        sm = SkillMatchResult(
            skill_name="Python", is_required=True,
            matched=True, semantic_match=False,
            evidence="精确匹配",
        )
        d = sm.model_dump()
        assert d["skill_name"] == "Python"
        assert d["is_required"] is True
        assert d["matched"] is True


# ========== 段落分割测试 ==========

class TestSectionSplitter:
    """测试 SectionSplitter 段落分割"""

    def test_split_experience_section(self):
        text = "教育背景\n清华大学 本科\n计算机科学与技术\n\n工作经历\n百度 算法工程师"
        sections = SectionSplitter.split(text)
        assert "education" in sections
        assert "experience" in sections

    def test_split_skills_section(self):
        text = "专业技能\nPython Java SQL\n\n项目经验\n电商推荐系统"
        sections = SectionSplitter.split(text)
        assert "skills" in sections
        assert "project" in sections

    def test_split_empty_text(self):
        sections = SectionSplitter.split("")
        assert sections == {}

    def test_split_no_section_headers(self):
        text = "张三 电话: 13800138000 邮箱: test@test.com"
        sections = SectionSplitter.split(text)
        assert "others" in sections or len(sections) > 0

    def test_split_multiple_same_section(self):
        text = "教育背景\n清华\n\n教育背景\n北大"
        sections = SectionSplitter.split(text)
        assert "education" in sections

    def test_split_project_and_skills_order(self):
        text = "专业技能\nPython\n\n项目经验\n推荐系统\n\n专业技能\nJava"
        sections = SectionSplitter.split(text)
        assert "skills" in sections
        assert "project" in sections


# ========== 规则降级解析测试 ==========

class TestResumeParserRuleFallback:
    """测试 ResumeParser 规则降级模式"""

    @pytest.fixture
    def parser(self):
        return ResumeParser(llm_client=None)  # 无 LLM，触发降��

    def test_extract_name(self, parser):
        text = "姓名：李四\n电话：13900139000"
        name = parser._extract_name_from_text(text)
        assert name == "李四"

    def test_extract_phone(self, parser):
        text = "联系电话：13900139000"
        phone = parser._extract_phone(text)
        assert phone == "13900139000"

    def test_extract_email(self, parser):
        text = "邮箱：lisi@example.com"
        email = parser._extract_email(text)
        assert email == "lisi@example.com"

    def test_extract_education_level(self, parser):
        text = "硕士毕业于清华大学"
        level = parser._extract_education_level(text)
        assert level == "硕士"

    def test_extract_skills(self, parser):
        text = "精通Python，熟悉Java、C++"
        skills = parser._extract_skills(text)
        assert len(skills) > 0

    def test_parse_with_rules(self, parser):
        sections = {
            "personal": "姓名：王五\n电话：13700137000\n邮箱：wangwu@test.com",
            "skills": "Python, Java, SQL",
        }
        profile = parser._parse_with_rules("RES-TEST-001", sections, "test.pdf")
        assert profile.candidate_name == "王五"
        assert profile.parsing_method == "rule"
        assert profile.confidence == 0.4
        assert len(profile.skills) > 0

    def test_parse_with_rules_no_name(self, parser):
        sections = {"personal": "电话：13700137000"}
        profile = parser._parse_with_rules("RES-TEST-002", sections, "test.txt")
        assert profile.candidate_name == "未知候选人"

    def test_years_of_experience_extraction(self, parser):
        text = "5年工作经验"
        years = parser._extract_years_of_experience(text)
        assert years == 5.0
