
"""SkillProfileBuilder"""
import json
from datetime import datetime
from collections import defaultdict
from loguru import logger
from agents.agent2.nlp_profile.schemas import SkillProfile, ProficiencyLevels
from agents.agent2.nlp_profile.profile_store import ProfileStore
from agents.agent2.llm.client import LLMClient
from agents.agent2.llm.prompt_templates import SKILL_PROFILE_SYSTEM_PROMPT


class SkillProfileBuilder:
    def __init__(self, llm: LLMClient, store: ProfileStore):
        self.llm = llm
        self.store = store

    def build_from_jd_data(self, skill_name: str, jd_records: list[dict]) -> SkillProfile:
        import hashlib
        skill_id = "SK_" + hashlib.md5(skill_name.encode("utf-8")).hexdigest()[:8].upper()
        from collections import Counter
        categories = Counter()
        for r in jd_records:
            cat = r.get("skill_category", "")
            if cat:
                categories[cat] += 1
        category = categories.most_common(1)[0][0] if categories else ""

        parts = []
        for i, r in enumerate(jd_records[:20]):
            title = r.get("title", "?")
            company = r.get("company", "?")
            desc = r.get("description", "") or r.get("job_desc", "") or ""
            if isinstance(desc, str) and len(desc) > 300:
                desc = desc[:300] + "..."
            parts.append(f"[{i+1}] {title} @ {company}\n{desc}")
        context = "\n\n".join(parts)

        messages = [
            {"role": "system", "content": SKILL_PROFILE_SYSTEM_PROMPT},
            {"role": "user", "content": f"Skill: {skill_name}\nCategory: {category}\n\nJD context:\n{context}"},
        ]
        logger.info(f"Generating skill profile: {skill_name}")
        result = self.llm.chat_with_json(messages, temperature=0.2)
        profile_data = result

        sources = list(set(r.get("source", "unknown") for r in jd_records))
        proficiency = None
        pl = profile_data.get("proficiency_levels", {})
        if pl:
            proficiency = ProficiencyLevels(
                beginner=pl.get("beginner", ""),
                intermediate=pl.get("intermediate", ""),
                advanced=pl.get("advanced", ""),
            )
        profile = SkillProfile(
            skill_id=skill_id, name=skill_name, category=category,
            summary=profile_data.get("summary", ""),
            prerequisites=profile_data.get("prerequisites", []),
            related_technologies=profile_data.get("related_technologies", []),
            typical_applications=profile_data.get("typical_applications", []),
            proficiency_levels=proficiency,
            industry_trend=profile_data.get("industry_trend", ""),
            sources=sources,
            last_updated=datetime.now().isoformat(),
        )
        self.store.save_skill_profile(profile)
        return profile

    def build_all_from_jobs_clean(self, batch_size: int = 50) -> list[SkillProfile]:
        from agents.agent2.config import JOBS_CLEAN_COLLECTION
        db = self.store.client[self.store.db.name]
        skill_records = defaultdict(list)
        for record in db[JOBS_CLEAN_COLLECTION].find().limit(batch_size):
            skills = record.get("skills", [])
            if isinstance(skills, str):
                skills = [s.strip() for s in skills.split(",")]
            for skill in skills:
                skill_records[skill].append(record)
        profiles = []
        for name, records in skill_records.items():
            try:
                profiles.append(self.build_from_jd_data(name, records))
            except Exception as e:
                logger.error(f"Failed: {name}: {e}")
        return profiles

__all__ = ["SkillProfileBuilder"]
