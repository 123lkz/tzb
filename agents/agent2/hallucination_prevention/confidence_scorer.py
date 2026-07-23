"""ConfidenceScorer -- ????????"""
from loguru import logger

class ConfidenceScorer:
    def __init__(self):
        logger.info("ConfidenceScorer initialized")

    def score(self, llm_confidence: float, evidence_items: list, counter_evidence_items: list, explanation_length: int, source_diversity: int, relation_type: str = "requires", existing_relations: list = None) -> tuple:
        llm_score = llm_confidence * 0.40
        ev_score = self._score_evidence(evidence_items, counter_evidence_items) * 0.30
        ex_score = self._score_explanation(explanation_length) * 0.15
        src_score = self._score_source_diversity(source_diversity) * 0.15
        final = round(llm_score + ev_score + ex_score + src_score, 3)
        return final, {"llm": llm_confidence, "evidence": round(ev_score/0.30,3) if 0.30 else 0, "explanation": round(ex_score/0.15,3) if 0.15 else 0, "source": round(src_score/0.15,3) if 0.15 else 0, "final_score": final}

    def adjust_for_consensus(self, round_results: list[dict]) -> tuple:
        if not round_results: return 0.0, {"error": "no_rounds"}
        scores = [r.get("final_score", 0) for r in round_results]
        mean = sum(scores)/len(scores)
        var = sum((s-mean)**2 for s in scores)/len(scores)
        bonus = max(0, 0.05*(1-var*4))
        adjusted = min(1.0, mean+bonus)
        return round(adjusted, 3), {"round_scores": scores, "mean": round(mean,3), "variance": round(var,3), "bonus": round(bonus,3), "adjusted": round(adjusted,3)}

    @staticmethod
    def _score_evidence(evidence: list, counter: list) -> float:
        if not evidence: return 0.3
        detailed = sum(1 for e in evidence if len(e.get("detail","")) > 20)
        s = min(1.0, 0.3 + detailed*0.15)
        if counter: s = max(0.0, s - len(counter)*0.1)
        return round(s, 3)

    @staticmethod
    def _score_explanation(length: int) -> float:
        if length >= 200: return 0.9
        if length >= 100: return 0.7
        if length >= 50: return 0.5
        if length >= 20: return 0.3
        return 0.1

    @staticmethod
    def _score_source_diversity(n: int) -> float:
        if n >= 5: return 1.0
        if n >= 3: return 0.85
        if n >= 2: return 0.65
        if n >= 1: return 0.4
        return 0.2

__all__ = ["ConfidenceScorer"]
