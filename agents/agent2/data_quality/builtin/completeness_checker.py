"""??????"""
from agents.agent2.data_quality.base_checker import AbstractDataQualityChecker, CheckResult, CheckerType

class CompletenessChecker(AbstractDataQualityChecker):
    REQUIRED_FIELDS = ["title", "company", "salary", "skills", "city"]
    IMPORTANT_FIELDS = ["description", "experience", "education"]

    @property
    def name(self) -> str:
        return "completeness"

    @property
    def check_type(self) -> CheckerType:
        return CheckerType.COMPLETENESS

    def check(self, record: dict) -> CheckResult:
        missing_required = [f for f in self.REQUIRED_FIELDS if not record.get(f) or (isinstance(record.get(f), str) and record[f].strip() == "")]
        missing_important = [f for f in self.IMPORTANT_FIELDS if not record.get(f) or (isinstance(record.get(f), str) and record[f].strip() == "")]
        total = len(self.REQUIRED_FIELDS) + len(self.IMPORTANT_FIELDS)
        present = total - len(missing_required) - len(missing_important)
        score = round(present / total, 3) if total > 0 else 0.0
        flagged = missing_required + missing_important
        if missing_required:
            return CheckResult(checker_name=self.name, passed=False, score=score, details=f"missing: {missing_required}", flagged_items=flagged)
        elif missing_important:
            return CheckResult(checker_name=self.name, passed=True, score=score, details=f"missing optional: {missing_important}", flagged_items=flagged)
        else:
            return CheckResult(checker_name=self.name, passed=True, score=1.0, details="OK", flagged_items=[])
__all__ = ["CompletenessChecker"]
