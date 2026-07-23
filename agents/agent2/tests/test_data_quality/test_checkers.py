"""数据质量检查器单元测试"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest
from agents.agent2.data_quality.builtin.completeness_checker import CompletenessChecker
from agents.agent2.data_quality.builtin.consistency_checker import ConsistencyChecker
from agents.agent2.data_quality.builtin.timeliness_checker import TimelinessChecker
from agents.agent2.data_quality.builtin.plagiarism_checker import PlagiarismChecker
from agents.agent2.data_quality.builtin.noise_detector import NoiseDetector


class TestCompletenessChecker:
    def setup_method(self):
        self.checker = CompletenessChecker()

    def test_name(self):
        assert self.checker.name == "completeness"

    def test_complete_record(self):
        record = {
            "title": "算法工程师",
            "company": "某科技公司",
            "salary": "30K-50K",
            "skills": ["Python", "PyTorch"],
            "city": "北京",
            "description": "负责算法研发",
            "experience": "3-5年",
            "education": "硕士",
        }
        result = self.checker.check(record)
        assert result.passed is True
        assert result.score == 1.0

    def test_missing_required_fields(self):
        record = {"title": "算法工程师"}
        result = self.checker.check(record)
        assert result.passed is False
        assert "company" in result.flagged_items
        assert result.score < 1.0

    def test_empty_record(self):
        result = self.checker.check({})
        assert result.passed is False


class TestConsistencyChecker:
    def setup_method(self):
        self.checker = ConsistencyChecker()

    def test_normal_record(self):
        record = {
            "title": "高级算法工程师",
            "salary": "30K-50K",
            "experience": "3-5年",
            "education": "硕士",
            "skills": ["Python", "PyTorch"],
        }
        result = self.checker.check(record)
        assert result.passed is True

    def test_entry_level_high_salary(self):
        record = {
            "title": "实习生",
            "salary": "100K-200K",
            "experience": "应届",
            "skills": ["Python"],
        }
        result = self.checker.check(record)
        assert result.passed is False
        assert len(result.flagged_items) > 0

    def test_empty_skills(self):
        record = {
            "title": "算法工程师",
            "salary": "30K",
            "experience": "3-5年",
            "skills": [],
        }
        result = self.checker.check(record)
        assert result.passed is False
        assert "no skills listed" in str(result.flagged_items)


class TestTimelinessChecker:
    def setup_method(self):
        self.checker = TimelinessChecker()

    def test_recent_record(self):
        from datetime import datetime, timedelta
        record = {
            "pub_date": (datetime.now() - timedelta(days=7)).isoformat(),
            "skills": ["Python", "PyTorch"],
        }
        result = self.checker.check(record)
        assert result.passed is True

    def test_obsolete_tech(self):
        record = {
            "pub_date": "2025-01-01",
            "skills": ["jQuery", "Flash", "Python"],
        }
        result = self.checker.check(record)
        assert result.passed is False
        assert any("flash" in item.lower() or "jquery" in item.lower() for item in result.flagged_items)


class TestPlagiarismChecker:
    def setup_method(self):
        self.checker = PlagiarismChecker()

    def test_normal_jd(self):
        record = {
            "description": "我们正在招聘一名高级Python后端工程师，负责设计和实现高并发分布式系统。"
                           "需要使用FastAPI和PostgreSQL构建RESTful API，并优化数据库查询性能。"
        }
        result = self.checker.check(record)
        assert result.passed is True
        assert result.score > 0.5

    def test_template_jd(self):
        record = {
            "description": (
                "岗位职责：负责相关产品的研发工作。"
                "任职要求：具有良好的团队合作精神，有较强的责任心。"
                "具有良好的沟通协调能力，具备一定的相关领域经验。"
                "有经验者优先，优秀者可适当放宽条件。"
                "职责描述：负责日常开发工作。岗位要求：熟悉相关领域。"
            )
        }
        result = self.checker.check(record)
        assert result.passed is False

    def test_short_description(self):
        record = {"description": "简短的描述"}
        result = self.checker.check(record)
        assert result.passed is False


class TestNoiseDetector:
    def setup_method(self):
        self.checker = NoiseDetector()

    def test_normal_record(self):
        record = {
            "title": "算法工程师",
            "salary": "30K-50K",
            "company": "北京某科技有限公司",
            "skills": ["Python", "PyTorch"],
        }
        result = self.checker.check(record)
        assert result.passed is True

    def test_abnormal_salary(self):
        record = {
            "title": "算法工程师",
            "salary": "1K-2K",
            "company": "某科技公司",
            "skills": ["Python"],
        }
        result = self.checker.check(record)
        assert result.passed is False

    def test_skill_position_mismatch(self):
        record = {
            "title": "会计",
            "salary": "8K-15K",
            "company": "某财务公司",
            "skills": ["PyTorch", "TensorFlow", "Excel"],
        }
        result = self.checker.check(record)
        assert result.passed is False

    def test_garbage_company_name(self):
        record = {
            "title": "工程师",
            "salary": "20K",
            "company": "a",
            "skills": ["Python"],
        }
        result = self.checker.check(record)
        assert result.passed is False
