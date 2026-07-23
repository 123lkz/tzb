"""Consistency checker (fixed)"""
import re
from agents.agent2.data_quality.base_checker import AbstractDataQualityChecker, CheckResult, CheckerType
E="\u5e94\u5c4a"
U="\u5728\u6821"
S="\u5b9e\u4e60"
Y="\u5e74"
W="\u65e0\u7ecf\u9a8c"
X="\u4ee5\u4e0b"
wan="\u4e07"
class ConsistencyChecker(AbstractDataQualityChecker):
    @property
    def name(self):return"consistency"
    @property
    def check_type(self):return CheckerType.CONSISTENCY
    def check(self,record):
        flagged=[]
        salary=str(record.get("salary",""))
        experience=str(record.get("experience",""))
        skills=record.get("skills",[])or[]
        if any(kw in experience for kw in [E,U,S,"1"+Y+X,W,"1"+Y]):
            nums=re.findall(r"(\d+\.?\d*)",salary.replace(",",""))
            if nums:
                mx=max(float(n) for n in nums)
                if wan in salary or"w"in salary.lower():mx=mx*10
                if mx>30:flagged.append("high salary: "+salary)
        if not skills or len(skills)==0:flagged.append("no skills listed")
        score=max(0.0,1.0-len(flagged)*0.3)
        details="; ".join(flagged)if flagged else"OK"
        return CheckResult(checker_name=self.name,passed=len(flagged)==0,score=score,details=details,flagged_items=flagged)
__all__=["ConsistencyChecker"]
