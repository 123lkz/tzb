"""EvolutionDetector 单元测试"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import pytest
from agents.agent1.skill_evolution.evolution_detector import EvolutionDetector
from agents.agent1.skill_evolution.schemas import PositionSkillTrend, SkillChangeSuggestion


class TestEvolutionDetector:
    def test_detect_empty(self):
        detector = EvolutionDetector()
        results = detector.detect([])
        assert results == []

    def test_detect_rising_skill(self):
        detector = EvolutionDetector(rising_threshold=0.3, declining_threshold=-0.3)
        trend = PositionSkillTrend(
            position_name="算法工程师", total_records=100,
            time_windows=["2026-Q1", "2026-Q2"],
            skill_frequencies={"RAG": [0.1, 0.6]},
            sample_jds={"RAG": ["需要RAG经验"]},
        )
        results = detector.detect([trend])
        assert len(results) == 1
        assert results[0].change_type == "rising"
        assert results[0].trend_score == 0.5

    def test_detect_declining(self):
        detector = EvolutionDetector(rising_threshold=0.3, declining_threshold=-0.3)
        trend = PositionSkillTrend(
            position_name="前端开发", total_records=50,
            time_windows=["2026-Q1", "2026-Q2"],
            skill_frequencies={"jQuery": [0.8, 0.2]},
        )
        results = detector.detect([trend])
        declining = [r for r in results if r.change_type == "declining"]
        assert len(declining) > 0

    def test_detect_new_skill(self):
        detector = EvolutionDetector()
        trend = PositionSkillTrend(
            position_name="ML工程师", total_records=50,
            time_windows=["2026-Q1", "2026-Q2"],
            skill_frequencies={"RAG": [0.0, 0.5]},
            sample_jds={"RAG": ["构建RAG系统"]},
        )
        results = detector.detect([trend])
        new_skills = [r for r in results if r.change_type == "new"]
        assert len(new_skills) > 0

    def test_detect_dying_skill(self):
        detector = EvolutionDetector()
        trend = PositionSkillTrend(
            position_name="前端", total_records=30,
            time_windows=["2026-Q1", "2026-Q2"],
            skill_frequencies={"Flash": [0.3, 0.0]},
        )
        results = detector.detect([trend])
        dying = [r for r in results if r.change_type == "dying"]
        assert len(dying) > 0

    def test_no_change_returns_empty(self):
        detector = EvolutionDetector(rising_threshold=0.3, declining_threshold=-0.3)
        trend = PositionSkillTrend(
            position_name="稳定岗", total_records=50,
            time_windows=["2026-Q1", "2026-Q2"],
            skill_frequencies={"Python": [0.5, 0.5]},
        )
        results = detector.detect([trend])
        stable = [r for r in results if r.change_type not in ("rising", "declining", "new", "dying")]
        assert len(stable) == 0

    def test_cross_domain_detection(self):
        detector = EvolutionDetector()
        t1 = PositionSkillTrend(
            position_name="AI工程师", total_records=30,
            time_windows=["2026-Q1", "2026-Q2"],
            skill_frequencies={"大模型": [0.1, 0.5]},
        )
        t2 = PositionSkillTrend(
            position_name="后端开发", total_records=30,
            time_windows=["2026-Q1", "2026-Q2"],
            skill_frequencies={"大模型": [0.0, 0.4]},
        )
        results = detector.detect([t1, t2])
        cross_domain = [r for r in results if r.cross_domain_flag]
        assert len(cross_domain) > 0

    def test_insufficient_windows(self):
        detector = EvolutionDetector()
        trend = PositionSkillTrend(
            position_name="测试", total_records=10,
            time_windows=["2026-Q1"],
            skill_frequencies={"Python": [0.5]},
        )
        results = detector.detect([trend])
        assert len(results) == 0

    def test_confidence_calculation(self):
        detector = EvolutionDetector()
        confidence = detector._compute_confidence(0.8, 200)
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.5

    def test_suggestion_for_type(self):
        detector = EvolutionDetector()
        assert "必需" in detector._suggestion_for_type("new")
        assert "移除" in detector._suggestion_for_type("dying")
        assert "关注" in detector._suggestion_for_type("rising")
        assert "关注" in detector._suggestion_for_type("declining")

