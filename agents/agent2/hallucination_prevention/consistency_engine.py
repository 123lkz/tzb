"""ConsistencyEngine -- ???????????????"""
from loguru import logger
from agents.agent2.nlp_profile.schemas import SkillProfile, PositionProfile
from agents.agent2.nlp_profile.profile_store import ProfileStore
from agents.agent2.llm.client import LLMClient
from agents.agent2.llm.prompt_templates import RELATIONSHIP_CHECK_SYSTEM_PROMPT, RELATIONSHIP_CHECK_USER_PROMPT_TEMPLATE

class ConsistencyEngine:
    def __init__(self, llm: LLMClient, store: ProfileStore):
        self.llm = llm; self.store = store

    def check_relationship(self, skill: SkillProfile, position: PositionProfile) -> dict:
        logger.info(f"Checking: Skill[{skill.name}] <-> Position[{position.name}]")
        prompt = RELATIONSHIP_CHECK_USER_PROMPT_TEMPLATE.format(
            skill_name=skill.name, skill_category=skill.category, skill_summary=skill.summary,
            skill_applications=", ".join(skill.typical_applications[:5]),
            skill_prerequisites=", ".join(skill.prerequisites[:5]),
            position_name=position.name, position_summary=position.summary,
            position_responsibilities="\n".join(f"- {r}" for r in position.core_responsibilities[:8]),
            position_required_skills=", ".join(position.required_skills[:10]),
            position_optional_skills=", ".join(position.optional_skills[:10]),
            position_domain=position.industry_domain,
        )
        messages = [{"role": "system", "content": RELATIONSHIP_CHECK_SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
        result = self.llm.chat_with_json(messages, temperature=0.1)
        if "error" in result:
            logger.warning(f"LLM check failed: {result[chr(34)+chr(34)+chr(34)]}")
            return {"valid": False, "confidence": 0.0, "explanation": "LLM check failed", "evidence": [], "counter_evidence": [], "recommendation": "exclude"}
        return {
            "valid": result.get("valid", False),
            "confidence": float(result.get("confidence", 0.5)),
            "explanation": result.get("explanation", ""),
            "evidence": result.get("evidence", []),
            "counter_evidence": result.get("counter_evidence", []),
            "recommendation": result.get("recommendation", "weakly_include"),
        }

    def check_relationship_by_ids(self, skill_id: str, position_id: str) -> dict:
        skill = self.store.get_skill_profile(skill_id)
        position = self.store.get_position_profile(position_id)
        if not skill or not position: return {"valid": False, "confidence": 0.0, "explanation": "profile not found", "evidence": [], "counter_evidence": [], "recommendation": "exclude"}
        return self.check_relationship(skill, position)

    def check_relationship_by_names(self, skill_name: str, position_name: str) -> dict:
        skill = self.store.get_skill_profile_by_name(skill_name)
        position = self.store.get_position_profile_by_name(position_name)
        if not skill or not position: return {"valid": False, "confidence": 0.0, "explanation": "profile not found", "evidence": [], "counter_evidence": [], "recommendation": "exclude"}
        return self.check_relationship(skill, position)

__all__ = ["ConsistencyEngine"]
