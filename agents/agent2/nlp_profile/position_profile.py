"""PositionProfileBuilder"""
from datetime import datetime
from collections import defaultdict
from loguru import logger
from agents.agent2.nlp_profile.schemas import PositionProfile
from agents.agent2.nlp_profile.profile_store import ProfileStore
from agents.agent2.llm.client import LLMClient
from agents.agent2.llm.prompt_templates import POSITION_PROFILE_SYSTEM_PROMPT

class PositionProfileBuilder:
    def __init__(self, llm: LLMClient, store: ProfileStore):
        self.llm = llm; self.store = store

    def build_from_jd_data(self, position_name: str, jd_records: list[dict]) -> PositionProfile:
        import hashlib
        pos_id = f"POS_{hashlib.md5(position_name.encode(chr(117)+chr(116)+chr(102)+chr(45)+chr(56))).hexdigest()[:8].upper()}"
        from collections import Counter
        salaries = [r.get("salary","") for r in jd_records if r.get("salary")]
        salary_range = Counter(salaries).most_common(1)[0][0] if salaries else ""
        exps = [r.get("experience","") for r in jd_records if r.get("experience")]
        exp_level = Counter(exps).most_common(1)[0][0] if exps else ""
        parts = []
        for i, r in enumerate(jd_records[:15]):
            desc = r.get("description","") or r.get("job_desc","") or ""
            if isinstance(desc, str) and len(desc) > 400: desc = desc[:400] + "..."
            parts.append(f"[{i+1}] {r.get(chr(99)+chr(111)+chr(109)+chr(112)+chr(97)+chr(110)+chr(121),chr(117)+chr(110)+chr(107)+chr(110)+chr(111)+chr(119)+chr(110))} | {r.get(chr(115)+chr(97)+chr(108)+chr(97)+chr(114)+chr(121),chr(109)+chr(105)+chr(115)+chr(99))}\n{desc}")
        context = "\n\n".join(parts)
        messages = [{"role": "system", "content": POSITION_PROFILE_SYSTEM_PROMPT}, {"role": "user", "content": f"position: {position_name}\n{context}"}]
        result = self.llm.chat_with_json(messages, temperature=0.2)
        if "error" in result:
            return PositionProfile(position_id=pos_id, name=position_name, summary="", sources=[r.get("source","unknown") for r in jd_records], last_updated=datetime.now().isoformat())
        profile = PositionProfile(position_id=pos_id, name=position_name, summary=result.get("summary",""), core_responsibilities=result.get("core_responsibilities",[]), required_skills=result.get("required_skills",[]), optional_skills=result.get("optional_skills",[]), industry_domain=result.get("industry_domain",""), typical_salary_range=result.get("typical_salary_range",salary_range), experience_level=result.get("experience_level",exp_level), sources=list(set(r.get("source","unknown") for r in jd_records)), last_updated=datetime.now().isoformat())
        self.store.save_position_profile(profile)
        return profile

    def build_all_from_jobs_clean(self, batch_size: int = 50) -> list[PositionProfile]:
        from agents.agent2.config import JOBS_CLEAN_COLLECTION
        db = self.store.client[self.store.db.name]
        records = defaultdict(list)
        for r in db[JOBS_CLEAN_COLLECTION].find().limit(batch_size):
            title = r.get("title","").strip()
            if title: records[title].append(r)
        profiles = []
        for name, recs in records.items():
            try: profiles.append(self.build_from_jd_data(name, recs))
            except Exception as e: logger.error(f"Failed: {name}: {e}")
        return profiles

__all__ = ["PositionProfileBuilder"]
