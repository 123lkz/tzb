"""幻觉防控模块单元测试"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest
from agents.agent2.hallucination_prevention.confidence_scorer import ConfidenceScorer
from agents.agent2.hallucination_prevention.consensus_manager import ConsensusManager
from agents.agent2.hallucination_prevention.consistency_engine import ConsistencyEngine


class TestConfidenceScorer:
    def setup_method(self):
        self.scorer = ConfidenceScorer()

    def test_basic_scoring(self):
        score, breakdown = self.scorer.score(
            llm_confidence=0.9,
            evidence_items=[{"type": "A", "detail": "非常详细的证据说明" * 10}],
            counter_evidence_items=[],
            explanation_length=250,
            source_diversity=3,
        )
        assert 0.0 <= score <= 1.0
        assert score > 0.7
        assert "final_score" in breakdown

    def test_low_confidence_scoring(self):
        score, breakdown = self.scorer.score(
            llm_confidence=0.3,
            evidence_items=[],
            counter_evidence_items=[{"type": "B", "detail": "反面证据"}],
            explanation_length=10,
            source_diversity=0,
        )
        assert score < 0.5

    def test_source_diversity_scoring(self):
        score_1, _ = self.scorer.score(
            llm_confidence=0.8, evidence_items=[{"detail": "x" * 30}],
            counter_evidence_items=[], explanation_length=100, source_diversity=1,
        )
        score_5, _ = self.scorer.score(
            llm_confidence=0.8, evidence_items=[{"detail": "x" * 30}],
            counter_evidence_items=[], explanation_length=100, source_diversity=5,
        )
        assert score_5 >= score_1

    def test_adjust_for_consensus(self):
        round_results = [
            {"final_score": 0.85},
            {"final_score": 0.82},
            {"final_score": 0.88},
        ]
        adjusted, record = self.scorer.adjust_for_consensus(round_results)
        assert 0.0 <= adjusted <= 1.0
        assert adjusted >= 0.8
        assert "bonus" in record
        assert "variance" in record

    def test_high_variance_consensus(self):
        round_results = [
            {"final_score": 0.95},
            {"final_score": 0.30},
            {"final_score": 0.88},
        ]
        adjusted, record = self.scorer.adjust_for_consensus(round_results)
        assert record["variance"] > 0.01
        assert record["bonus"] < 0.05

    def test_empty_round_results(self):
        score, record = self.scorer.adjust_for_consensus([])
        assert score == 0.0
        assert record.get("error") == "no_rounds"


class TestConsensusManager:
    def setup_method(self):
        """使用 mock 初始化 ConsensusManager"""
        from unittest.mock import MagicMock
        self.mock_engine = MagicMock(spec=ConsistencyEngine)
        self.mock_scorer = MagicMock(spec=ConfidenceScorer)
        # 默认 mock 返回值
        self.mock_engine.check_relationship.return_value = {
            "valid": True, "confidence": 0.85, "explanation": "Good",
            "evidence": [{"type": "A", "detail": "Ev1"}],
            "counter_evidence": [], "recommendation": "include",
        }
        self.mock_scorer.score.return_value = (0.85, {"final_score": 0.85})
        self.mock_scorer.adjust_for_consensus.return_value = (0.86, {
            "round_scores": [0.85, 0.82, 0.88],
            "mean_before_adjustment": 0.85,
            "variance": 0.0006,
            "bonus": 0.015,
            "final_adjusted": 0.865,
        })

    def test_count_sources(self):
        from agents.agent2.nlp_profile.schemas import SkillProfile, PositionProfile
        skill = SkillProfile(
            skill_id="SK_T", name="Python", summary="test",
            sources=["bosszhipin", "zhilian", "lagou"],
        )
        position = PositionProfile(
            position_id="POS_T", name="Engineer", summary="test",
            sources=["bosszhipin", "liepin"],
        )
        count = ConsensusManager._count_sources(skill, position)
        assert count == 4

    def test_aggregate_results_all_valid(self):
        cm = ConsensusManager.__new__(ConsensusManager)
        cm.scorer = self.mock_scorer
        round_results = [
            {"round": 1, "valid": True, "final_score": 0.85,
             "explanation": "Good", "recommendation": "include",
             "evidence": [{"type": "A", "detail": "Ev1"}],
             "counter_evidence": [], "breakdown": {}},
            {"round": 2, "valid": True, "final_score": 0.82,
             "explanation": "Also good", "recommendation": "include",
             "evidence": [{"type": "B", "detail": "Ev2"}],
             "counter_evidence": [], "breakdown": {}},
            {"round": 3, "valid": True, "final_score": 0.88,
             "explanation": "Consistent", "recommendation": "strongly_include",
             "evidence": [{"type": "C", "detail": "Ev3"}],
             "counter_evidence": [], "breakdown": {}},
        ]
        result = cm._aggregate_results(round_results)
        assert result["valid"] is True
        assert result["confidence"] > 0.8
        assert result["consensus"]["agreement_rate"] == 1.0
        assert result["consensus"]["rounds"] == 3

    def test_aggregate_results_split(self):
        cm = ConsensusManager.__new__(ConsensusManager)
        cm.scorer = self.mock_scorer
        round_results = [
            {"round": 1, "valid": True, "final_score": 0.9,
             "explanation": "Good", "recommendation": "include",
             "evidence": [], "counter_evidence": [], "breakdown": {}},
            {"round": 2, "valid": False, "final_score": 0.3,
             "explanation": "Bad", "recommendation": "exclude",
             "evidence": [], "counter_evidence": [], "breakdown": {}},
            {"round": 3, "valid": True, "final_score": 0.85,
             "explanation": "Good", "recommendation": "include",
             "evidence": [], "counter_evidence": [], "breakdown": {}},
        ]
        result = cm._aggregate_results(round_results)
        assert result["consensus"]["agreement_rate"] == pytest.approx(2/3, abs=0.01)
        assert result["valid"] is True

    def test_aggregate_results_empty(self):
        cm = ConsensusManager.__new__(ConsensusManager)
        result = cm._aggregate_results([])
        assert result["valid"] is False
        assert result["confidence"] == 0.0
        assert result["consensus"]["error"] == "no_results"
