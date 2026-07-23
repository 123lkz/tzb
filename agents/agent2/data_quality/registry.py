"""CheckerRegistry -- ???????????????"""
from typing import Optional
from loguru import logger
from agents.agent2.data_quality.base_checker import (
    AbstractDataQualityChecker, CheckResult, CheckerType,
)

class CheckerRegistry:
    _checkers: dict[str, AbstractDataQualityChecker] = {}

    @classmethod
    def register(cls, checker: AbstractDataQualityChecker) -> None:
        name = checker.name
        if name in cls._checkers:
            logger.warning(f"Checker {name} already registered, overwriting")
        cls._checkers[name] = checker

    @classmethod
    def get_checker(cls, name: str) -> Optional[AbstractDataQualityChecker]:
        return cls._checkers.get(name)

    @classmethod
    def get_checkers(cls, check_type: Optional[CheckerType] = None) -> list[AbstractDataQualityChecker]:
        if check_type is None:
            return list(cls._checkers.values())
        return [c for c in cls._checkers.values() if c.check_type == check_type]

    @classmethod
    def get_all_checker_names(cls) -> list[str]:
        return list(cls._checkers.keys())

    @classmethod
    def run_all(cls, record: dict) -> dict[str, CheckResult]:
        results = {}
        for name, checker in cls._checkers.items():
            try:
                result = checker.check(record)
                results[name] = result
            except Exception as e:
                logger.error(f"Checker {name} failed: {e}")
                results[name] = CheckResult(checker_name=name, passed=False, score=0.0, details=str(e), flagged_items=["__error__"])
        return results

    @classmethod
    def run_all_batch(cls, records: list[dict]) -> list[dict[str, CheckResult]]:
        return [cls.run_all(record) for record in records]

    @classmethod
    def compute_overall_score(cls, results: dict[str, CheckResult]) -> tuple[float, bool]:
        if not results:
            return 0.0, False
        total = sum(r.score for r in results.values())
        avg_score = total / len(results)
        all_passed = all(r.passed for r in results.values())
        return round(avg_score, 3), all_passed

    @classmethod
    def clear(cls) -> None:
        cls._checkers.clear()
        logger.info("Checker registry cleared")

__all__ = ["CheckerRegistry"]
