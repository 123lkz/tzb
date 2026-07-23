"""?????"""
from datetime import datetime
from agents.agent2.data_quality.base_checker import AbstractDataQualityChecker, CheckResult, CheckerType

OBSOLETE_TECH = ["jquery", "flash", "flex", "silverlight", "extjs", "angularjs", "cobol", "vb6", "delphi"]
class TimelinessChecker(AbstractDataQualityChecker):
    @property
    def name(self) -> str:
        return "timeliness"
    @property
    def check_type(self) -> CheckerType:
        return CheckerType.TIMELINESS

    def check(self, record: dict) -> CheckResult:
        flagged = []
        pub_date = record.get("pub_date") or record.get("publish_date") or record.get("created_at")
        if pub_date:
            try:
                if isinstance(pub_date, datetime): pub_dt = pub_date
                elif isinstance(pub_date, str):
                    pub_dt = datetime.fromisoformat(pub_date.replace("Z", "+00:00"))
                else: pub_dt = None
                if pub_dt:
                    age = (datetime.now() - pub_dt).days
                    if age > 180:
                        flagged.append(f"published {age} days ago")
            except: pass
        skills = record.get("skills", []) or []
        if isinstance(skills, str): skills = [s.strip().lower() for s in skills.split(",")]
        elif isinstance(skills, list): skills = [s.lower() if isinstance(s, str) else str(s) for s in skills]
        for obs in OBSOLETE_TECH:
            if any(obs in s.lower() for s in skills if isinstance(s, str)):
                flagged.append(f"obsolete tech: {obs}")
                break
        score = max(0.3, 1.0 - len(flagged) * 0.2)
        return CheckResult(checker_name=self.name, passed=len(flagged)==0, score=score, details="; ".join(flagged) if flagged else "OK", flagged_items=flagged)
__all__ = ["TimelinessChecker"]
