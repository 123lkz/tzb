"""ConsensusManager -- ??????"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
from agents.agent2.nlp_profile.schemas import SkillProfile, PositionProfile
from agents.agent2.hallucination_prevention.consistency_engine import ConsistencyEngine
from agents.agent2.hallucination_prevention.confidence_scorer import ConfidenceScorer
from agents.agent2.config import CONSENSUS_MIN_ROUNDS

class ConsensusManager:
    def __init__(self, engine: ConsistencyEngine, scorer: ConfidenceScorer, min_rounds: int = CONSENSUS_MIN_ROUNDS):
        self.engine = engine; self.scorer = scorer; self.min_rounds = min_rounds

    def reach_consensus(self, skill: SkillProfile, position: PositionProfile, rounds: int = None, parallel: bool = True) -> dict:
        rounds = rounds or self.min_rounds
        logger.info(f"Consensus for {skill.name} <-> {position.name} ({rounds} rounds)")
        if parallel and rounds > 1:
            round_results = self._run_parallel(skill, position, rounds)
        else:
            round_results = self._run_sequential(skill, position, rounds)
        return self._aggregate_results(round_results)

    def _run_sequential(self, skill, position, rounds):
        return [self._single_round(skill, position, i+1) for i in range(rounds)]

    def _run_parallel(self, skill, position, rounds):
        results = []
        with ThreadPoolExecutor(max_workers=min(rounds, 4)) as ex:
            futs = {ex.submit(self._single_round, skill, position, i+1): i+1 for i in range(rounds)}
            for f in as_completed(futs):
                try: results.append(f.result())
                except Exception as e: logger.error(f"Round failed: {e}")
        results.sort(key=lambda x: x["round"])
        return results

    def _single_round(self, skill, position, round_num):
        result = self.engine.check_relationship(skill, position)
        conf, breakdown = self.scorer.score(
            llm_confidence=result.get("confidence", 0.5),
            evidence_items=result.get("evidence", []),
            counter_evidence_items=result.get("counter_evidence", []),
            explanation_length=len(result.get("explanation", "")),
            source_diversity=self._count_sources(skill, position),
        )
        return {"round": round_num, "valid": result["valid"], "raw_confidence": result["confidence"], "final_score": conf, "explanation": result["explanation"], "evidence": result["evidence"], "counter_evidence": result["counter_evidence"], "recommendation": result["recommendation"], "breakdown": breakdown}

    def _aggregate_results(self, round_results):
        if not round_results:
            return {"valid": False, "confidence": 0.0, "explanation": "no results", "evidence": [], "counter_evidence": [], "recommendation": "exclude", "consensus": {"error": "no_results"}}
        valid_count = sum(1 for r in round_results if r["valid"])
        agreement = valid_count / len(round_results)
        majority = valid_count > len(round_results) / 2
        best = max(round_results, key=lambda r: r["final_score"])
        adjusted, consensus_record = self.scorer.adjust_for_consensus([r for r in round_results if "final_score" in r])
        all_ev, seen_ev = [], set()
        for r in round_results:
            for e in r.get("evidence", []):
                k = e.get("detail","")[:50]
                if k not in seen_ev: all_ev.append(e); seen_ev.add(k)
        all_ce, seen_ce = [], set()
        for r in round_results:
            for e in r.get("counter_evidence", []):
                k = e.get("detail","")[:50]
                if k not in seen_ce: all_ce.append(e); seen_ce.add(k)
        return {"valid": majority and adjusted >= 0.5, "confidence": adjusted, "explanation": best["explanation"], "evidence": all_ev, "counter_evidence": all_ce, "recommendation": best["recommendation"], "consensus": {"rounds": len(round_results), "agreement_rate": round(agreement,3), "valid_count": valid_count, "total": len(round_results), "breakdown": consensus_record}}

    @staticmethod
    def _count_sources(skill: SkillProfile, position: PositionProfile) -> int:
        return len(set(skill.sources) | set(position.sources))

__all__ = ["ConsensusManager"]
