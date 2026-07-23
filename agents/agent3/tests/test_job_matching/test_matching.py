"""
测试：人岗匹配模块
覆盖：匹配引擎、差距分析、报告生成
"""
import pytest
from agents.agent3.job_matching.schemas import (
    SkillMatchResult, DimensionScore, GapItem, MatchReport,
)
from agents.agent3.job_matching.match_engine import MatchEngine
from agents.agent3.job_matching.gap_analyzer import GapAnalyzer
from agents.agent3.job_matching.match_report_builder import MatchReportBuilder
from agents.agent3.resume_parser.schemas import ResumeProfile, PersonalInfo
from agents.agent2.nlp_profile.schemas import PositionProfile, SkillProfile


# ========== 匹配引擎测试 ==========

class TestMatchEngine:
    """"""

    @pytest.fixture
    def engine(self):
        return MatchEngine(llm_client=None)

    def test_skill_exact_match(self, engine):
        candidate = ["Python", "Java", "SQL"]
        required = ["Python", "Go"]
        optional = ["Docker"]
        results, req_rate, opt_rate = engine._match_skills(candidate, required, optional)
        assert req_rate == 0.5  # Python matches, Go doesn"t
        assert opt_rate == 0.0  # Docker not in candidate
        assert len(results) == 3
        assert results[0].matched is True   # Python matched
        assert results[1].matched is False  # Go not matched

    def test_skill_case_insensitive(self, engine):
        candidate = ["python", "java", "sql"]
        required = ["Python", "Java"]
        results, _, _ = engine._match_skills(candidate, required, [])
        assert results[0].matched is True
        assert results[1].matched is True

    def test_skill_version_normalization(self, engine):
        candidate = ["Python3", "PyTorch2.0"]
        required = ["Python", "PyTorch"]
        results, req_rate, _ = engine._match_skills(candidate, required, [])
        assert req_rate >= 0.5

    def test_skill_no_match(self, engine):
        candidate = ["Rust", "C++"]
        required = ["Python", "Java"]
        results, req_rate, _ = engine._match_skills(candidate, required, [])
        assert req_rate == 0.0
        assert all(not r.matched for r in results)

    def test_skill_empty_candidate(self, engine):
        results, req_rate, _ = engine._match_skills([], ["Python"], [])
        assert req_rate == 0.0
        assert results[0].matched is False

    def test_skill_empty_required(self, engine):
        results, req_rate, opt_rate = engine._match_skills(["Python"], [], ["Docker"])
        assert req_rate == 0.0
        assert opt_rate == 0.0
        assert len(results) == 1


# ========== 差距分析测试 ==========

class TestGapAnalyzer:
    """测试 GapAnalyzer"""

    @pytest.fixture
    def analyzer(self):
        return GapAnalyzer(skill_profiles={})

    def test_gap_from_unmatched_required(self, analyzer):
        matches = [
            SkillMatchResult(skill_name="Python", is_required=True, matched=True),
            SkillMatchResult(skill_name="Go", is_required=True, matched=False),
            SkillMatchResult(skill_name="Docker", is_required=False, matched=True),
        ]
        gaps = analyzer.analyze(matches)
        assert len(gaps) == 1
        assert gaps[0].skill_name == "Go"
        assert gaps[0].importance == "high"

    def test_gap_with_skill_profile(self, analyzer):
        sp = SkillProfile(
            skill_id="SK001", name="Go", category="编程语言",
            summary="Go 是 Google 开发的编译型语言",
            prerequisites=["编程基础"],
            related_technologies=["gRPC", "Kubernetes"],
            typical_applications=["微服务"],
        )
        analyzer.skill_profiles = {"Go": sp}
        matches = [
            SkillMatchResult(skill_name="Go", is_required=True, matched=False),
        ]
        gaps = analyzer.analyze(matches)
        assert len(gaps) == 1
        assert "Go" in gaps[0].reason

    def test_gap_no_gaps_when_all_matched(self, analyzer):
        matches = [
            SkillMatchResult(skill_name="Python", is_required=True, matched=True),
        ]
        gaps = analyzer.analyze(matches)
        assert len(gaps) == 0

    def test_gap_optional_skill_not_analyzed(self, analyzer):
        matches = [
            SkillMatchResult(skill_name="Docker", is_required=False, matched=False),
        ]
        gaps = analyzer.analyze(matches)
        assert len(gaps) == 0


# ========== 报告生成测试 ==========

class TestMatchReportBuilder:
    """测试 MatchReportBuilder"""

    @pytest.fixture
    def builder(self):
        return MatchReportBuilder()

    def test_build_report(self, builder):
        resume = ResumeProfile(resume_id="RES-001", candidate_name="张三")
        position = PositionProfile(position_id="POS-001", name="算法工程师", summary="")
        dim_scores = [
            DimensionScore(dimension="skill", score=0.8, weight=0.45, details=""),
            DimensionScore(dimension="experience", score=0.6, weight=0.30, details=""),
            DimensionScore(dimension="responsibility", score=0.7, weight=0.25, details=""),
        ]
        skill_matches = [
            SkillMatchResult(skill_name="Python", is_required=True, matched=True),
            SkillMatchResult(skill_name="Go", is_required=True, matched=False),
        ]

        report = builder.build(
            resume=resume, position=position,
            dimension_scores=dim_scores, skill_matches=skill_matches,
            req_rate=0.5, opt_rate=0.0, gaps=[],
            llm_model="",
        )
        assert report.report_id.startswith("MR-")
        assert report.candidate_name == "张三"
        assert report.position_name == "算法工程师"
        assert 0.0 <= report.overall_match_score <= 1.0
        assert report.confidence > 0.0

    def test_build_high_recommendation(self, builder):
        resume = ResumeProfile(resume_id="RES-001", candidate_name="张三")
        position = PositionProfile(position_id="POS-001", name="算法工程师", summary="")
        dim_scores = [
            DimensionScore(dimension="skill", score=0.95, weight=0.45, details=""),
            DimensionScore(dimension="experience", score=0.9, weight=0.30, details=""),
            DimensionScore(dimension="responsibility", score=0.9, weight=0.25, details=""),
        ]
        report = builder.build(
            resume=resume, position=position,
            dimension_scores=dim_scores, skill_matches=[],
            req_rate=0.9, opt_rate=0.8, gaps=[],
        )
        assert report.recommendation == "highly_recommend"

    def test_build_low_recommendation(self, builder):
        resume = ResumeProfile(resume_id="RES-001", candidate_name="张三")
        position = PositionProfile(position_id="POS-001", name="算法工程师", summary="")
        dim_scores = [
            DimensionScore(dimension="skill", score=0.2, weight=0.45, details=""),
            DimensionScore(dimension="experience", score=0.2, weight=0.30, details=""),
            DimensionScore(dimension="responsibility", score=0.2, weight=0.25, details=""),
        ]
        report = builder.build(
            resume=resume, position=position,
            dimension_scores=dim_scores, skill_matches=[],
            req_rate=0.0, opt_rate=0.0, gaps=[],
        )
        assert report.recommendation == "not_recommend"

    def test_report_serialization(self, builder):
        resume = ResumeProfile(resume_id="RES-001", candidate_name="张三")
        position = PositionProfile(position_id="POS-001", name="算法工程师", summary="")
        dim_scores = [DimensionScore(dimension="skill", score=0.7, weight=0.45, details="")]
        report = builder.build(
            resume=resume, position=position,
            dimension_scores=dim_scores, skill_matches=[],
            req_rate=0.5, opt_rate=0.0, gaps=[],
        )
        data = report.model_dump(mode="json")
        assert data["report_id"] == report.report_id
        assert data["candidate_name"] == "张三"
        assert data["overall_match_score"] == report.overall_match_score

    def test_strength_extraction(self, builder):
        matches = [
            SkillMatchResult(skill_name="Python", is_required=True, matched=True),
            SkillMatchResult(skill_name="Go", is_required=True, matched=True),
            SkillMatchResult(skill_name="Java", is_required=True, matched=False),
        ]
        strengths = builder._extract_strengths(matches)
        assert len(strengths) > 0
        assert "Python" in strengths[0]

    def test_compute_confidence(self, builder):
        resume = ResumeProfile(
            resume_id="RES-001", parsing_method="llm", confidence=0.9,
            skills=["Python", "Java", "SQL", "Docker", "K8s", "Go"],
        )
        dim_scores = [DimensionScore(dimension="skill", score=0.8, weight=0.45, details="")]
        confidence = builder._compute_confidence(resume, dim_scores, llm_model="spark-4.0")
        assert confidence >= 0.8
        assert confidence <= 1.0
