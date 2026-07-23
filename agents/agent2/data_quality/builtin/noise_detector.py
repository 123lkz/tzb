"""Noise detector"""
import re
from agents.agent2.data_quality.base_checker import AbstractDataQualityChecker, CheckResult, CheckerType
MM=[(["\u4f1a\u8ba1","\u51fa\u7eb3"],["pytorch","tensorflow","kubernetes"]),(["\u524d\u53f0"],["spring boot","\u5fae\u670d\u52a1"]),(["\u4fdd\u5b89"],["transformer","\u5927\u6a21\u578b"])]
class NoiseDetector(AbstractDataQualityChecker):
    @property
    def name(self):return"noise_detector"
    @property
    def check_type(self):return CheckerType.NOISE
    def check(self,record):
        flagged=[]
        title=record.get("title","")
        salary=str(record.get("salary",""))
        company=record.get("company","")
        skills=record.get("skills",[])or[]
        if isinstance(skills,str):skills=[s.strip().lower()for s in re.split(r"[,|/]",skills)]
        elif isinstance(skills,list):skills=[s.lower()if isinstance(s,str)else str(s)for s in skills]
        nums=re.findall(r"(\d+\.?\d*)",salary.replace(",",""))
        if nums:
            avg=sum(float(n)for n in nums)/len(nums)
            if"\u4e07"in salary or"w"in salary.lower():avg=avg*10
            if 0<avg<3:flagged.append("low salary:"+salary)
            elif avg>500:flagged.append("high salary:"+salary)
        if not company or len(company.strip())<2:flagged.append("bad company")
        for pk,bs in MM:
            if any(kw in title.lower()for kw in pk):
                for b in bs:
                    if any(b in s for s in skills):flagged.append("mismatch:"+b);break
        score=max(0.0,1.0-len(flagged)*0.25)
        details="; ".join(flagged)if flagged else"OK"
        return CheckResult(checker_name=self.name,passed=len(flagged)==0,score=score,details=details,flagged_items=flagged)
__all__=["NoiseDetector"]
