"""CheckerRegistry 单元测试"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest
from agents.agent2.data_quality.registry import CheckerRegistry
from agents.agent2.data_quality.base_checker import (
    AbstractDataQualityChecker, CheckResult, CheckerType,
)


class TestCheckerRegistry:
    def setup_method(self):
        CheckerRegistry.clear()

    def test_register_and_get(self):
        checker = DummyChecker()
        CheckerRegistry.register(checker)
        retrieved = CheckerRegistry.get_checker("dummy")
        assert retrieved is not None
        assert retrieved.name == "dummy"

    def test_run_all(self):
        CheckerRegistry.register(DummyChecker())
        CheckerRegistry.register(AnotherDummyChecker())

        record = {"test": "data"}
        results = CheckerRegistry.run_all(record)
        assert "dummy" in results
        assert "another_dummy" in results

    def test_compute_overall_score(self):
        CheckerRegistry.register(DummyChecker())
        results = CheckerRegistry.run_all({"test": "data"})
        score, all_passed = CheckerRegistry.compute_overall_score(results)
        assert 0.0 <= score <= 1.0
        assert isinstance(all_passed, bool)

    def test_clear(self):
        CheckerRegistry.register(DummyChecker())
        CheckerRegistry.clear()
        assert len(CheckerRegistry.get_all_checker_names()) == 0

    def test_get_checkers_by_type(self):
        CheckerRegistry.clear()
        CheckerRegistry.register(DummyChecker())
        custom_checkers = CheckerRegistry.get_checkers(CheckerType.CUSTOM)
        assert len(custom_checkers) > 0


class DummyChecker(AbstractDataQualityChecker):
    @property
    def name(self) -> str:
        return "dummy"

    def check(self, record: dict) -> CheckResult:
        return CheckResult(
            checker_name=self.name,
            passed=True,
            score=0.85,
            details="Dummy check passed",
            flagged_items=[],
        )


class AnotherDummyChecker(AbstractDataQualityChecker):
    @property
    def name(self) -> str:
        return "another_dummy"

    def check(self, record: dict) -> CheckResult:
        return CheckResult(
            checker_name=self.name,
            passed=False,
            score=0.5,
            details="Flagged some fields",
            flagged_items=["field_x"],
        )
