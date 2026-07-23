"""AbstractDataQualityChecker -- checker abstract base class"""
from abc import ABC, abstractmethod
from enum import Enum
from pydantic import BaseModel, Field

class CheckerType(str, Enum):
    COMPLETENESS = "completeness"
    CONSISTENCY = "consistency"
    TIMELINESS = "timeliness"
    PLAGIARISM = "plagiarism"
    NOISE = "noise"
    CUSTOM = "custom"

class CheckResult(BaseModel):
    checker_name: str = Field(..., description="checker name")
    passed: bool = Field(..., description="whether passed")
    score: float = Field(..., ge=0.0, le=1.0, description="score 0-1")
    details: str = Field(..., description="details")
    flagged_items: list[str] = Field(default_factory=list, description="flagged items")

    model_config = {"json_schema_extra": {"example": {"checker_name": "test", "passed": True, "score": 1.0, "details": "ok", "flagged_items": []}}}

class AbstractDataQualityChecker(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    def check_type(self) -> CheckerType: return CheckerType.CUSTOM

    @abstractmethod
    def check(self, record: dict) -> CheckResult: ...

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        from agents.agent2.data_quality.registry import CheckerRegistry
        CheckerRegistry.register(cls())

__all__ = ["AbstractDataQualityChecker", "CheckResult", "CheckerType"]
