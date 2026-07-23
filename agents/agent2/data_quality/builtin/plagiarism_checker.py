"""Plagiarism checker"""
import re
from agents.agent2.data_quality.base_checker import AbstractDataQualityChecker, CheckResult, CheckerType
T=["\u804c\u8d23\u63cf\u8ff0","\u4efb\u804c\u8981\u6c42","\u5c97\u4f4d\u804c\u8d23","\u5c97\u4f4d\u8981\u6c42","\u56e2\u961f\u5408\u4f5c\u7cbe\u795e","\u826f\u597d\u7684\u6c9f\u901a\u80fd\u529b","\u8d23\u4efb\u5fc3\u5f3a","\u6709\u8f83\u5f3a\u7684\u8d23\u4efb\u5fc3","\u6709\u7ecf\u9a8c\u8005\u4f18\u5148","\u4f18\u79c0\u8005\u53ef\u9002\u5f53\u653e\u5bbd"]
class PlagiarismChecker(AbstractDataQualityChecker):
    @property
    def name(self):return"plagiarism"
    @property
    def check_type(self):return CheckerType.PLAGIARISM
    def check(self,record):
        desc=record.get("description","")or record.get("job_desc","")or""
        if not desc or len(desc.strip())<50:
            return CheckResult(checker_name=self.name,passed=False,score=0.3,details="short",flagged_items=["short"])
        count=sum(len(re.findall(re.escape(p),desc))for p in T)
        ur=len(set(desc))/max(len(desc),1)
        score=max(0.0,min(1.0,ur*2-count*0.03))
        flagged=[]
        if count>3:flagged.append(str(count)+"templates")
        if ur<0.25:flagged.append("low density")
        details="; ".join(flagged)if flagged else"OK"
        return CheckResult(checker_name=self.name,passed=len(flagged)==0,score=round(score,3),details=details,flagged_items=flagged)
__all__=["PlagiarismChecker"]
