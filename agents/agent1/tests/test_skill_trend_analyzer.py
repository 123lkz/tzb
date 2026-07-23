"""SkillTrendAnalyzer 单元测试"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import pytest
from agents.agent1.skill_evolution.skill_trend_analyzer import SkillTrendAnalyzer
from agents.agent1.skill_evolution.schemas import PositionSkillTrend


class TestSkillTrendAnalyzer:
    def test_analyze_empty(self):
        analyzer = SkillTrendAnalyzer(min_records=1)
        results = analyzer.analyze([])
        assert results == []

    def test_normalize_position(self):
        analyzer = SkillTrendAnalyzer()
        name = analyzer._normalize_position_name("高级Python开发工程师")
        assert "高级" not in name
        assert "Python" in name

    def test_parse_date_y_m_d(self):
        analyzer = SkillTrendAnalyzer()
        dt = analyzer._parse_date("2026-06-15")
        assert dt is not None
        assert dt.year == 2026
        assert dt.month == 6

    def test_parse_date_y_m(self):
        analyzer = SkillTrendAnalyzer()
        dt = analyzer._parse_date("2026-06")
        assert dt is not None
        assert dt.year == 2026

    def test_parse_date_chinese(self):
        analyzer = SkillTrendAnalyzer()
        dt = analyzer._parse_date("2026年06月15日")
        assert dt is not None

    def test_parse_date_invalid(self):
        analyzer = SkillTrendAnalyzer()
        dt = analyzer._parse_date("not_a_date")
        assert dt is None

    def test_extract_period_quarter(self):
        analyzer = SkillTrendAnalyzer()
        p = analyzer._extract_period("2026-06-15", "quarter")
        assert p == "2026-Q2"

    def test_extract_period_month(self):
        analyzer = SkillTrendAnalyzer()
        p = analyzer._extract_period("2026-06-15", "month")
        assert p == "2026-06"

    def test_extract_period_unknown(self):
        analyzer = SkillTrendAnalyzer()
        p = analyzer._extract_period("", "quarter")
        assert p == "unknown"

    def test_collect_skills_list(self):
        analyzer = SkillTrendAnalyzer()
        skills = analyzer._collect_skills({"skills": ["Python", "Go"]})
        assert skills == ["Python", "Go"]

    def test_collect_skills_str(self):
        analyzer = SkillTrendAnalyzer()
        skills = analyzer._collect_skills({"skills": "Python, Go, Rust"})
        assert "Python" in skills
        assert len(skills) == 3

    def test_analyze_single_position(self):
        analyzer = SkillTrendAnalyzer(min_records=1)
        records = [
            {"title": "Python开发", "pub_date": "2026-01-15", "skills": ["Python", "Django"], "description": "Web dev"},
            {"title": "Python开发", "pub_date": "2026-04-15", "skills": ["Python", "FastAPI"], "description": "API dev"},
        ]
        results = analyzer.analyze(records)
        assert len(results) > 0
        trend = results[0]
        assert isinstance(trend, PositionSkillTrend)
        assert trend.total_records == 2

    def test_analyze_below_min_records(self):
        analyzer = SkillTrendAnalyzer(min_records=10)
        records = [{"title": "测试", "pub_date": "2026-01-01", "skills": ["A"]}]
        results = analyzer.analyze(records)
        assert len(results) == 0

    def test_skill_frequency_calculation(self):
        analyzer = SkillTrendAnalyzer(min_records=1)
        records = [
            {"title": "开发", "pub_date": "2026-01-01", "skills": ["Python"], "description": "dev"},
            {"title": "开发", "pub_date": "2026-04-01", "skills": ["Python", "Go"], "description": "dev"},
        ]
        results = analyzer.analyze(records)
        if results:
            trend = results[0]
            skill_python = trend.skill_frequencies.get("Python", [])
            assert len(skill_python) > 0
