"""
RelationProfileBuilder 鈥斺€?鐢熸垚鎶€鑳?宀椾綅鍏崇郴鐨勮嚜鐒惰瑷€鐢诲儚
鍖呭惈璇佹嵁閾炬瀯寤哄拰鍏崇郴鐢诲儚鐢熸垚
"""
from datetime import datetime
from loguru import logger

from agents.agent2.nlp_profile.schemas import (
    RelationProfile, RelationProvenance, EvidenceItem,
    SkillProfile, PositionProfile,
)
from agents.agent2.nlp_profile.profile_store import ProfileStore
from agents.agent2.llm.client import LLMClient
from agents.agent2.llm.prompt_templates import (
    RELATIONSHIP_CHECK_SYSTEM_PROMPT,
    RELATIONSHIP_CHECK_USER_PROMPT_TEMPLATE,
)
from agents.agent2.config import XF_MODEL


class RelationProfileBuilder:
    """鍏崇郴鐢诲儚鏋勫缓鍣?    
    褰撳够瑙夐槻鎺фā鍧楅獙璇侀€氳繃鍚庯紝鐢熸垚瀹屾暣鐨?RelationProfile
    """

    def __init__(self, llm: LLMClient, store: ProfileStore):
        self.llm = llm
        self.store = store

    def build_relation(
        self,
        skill: SkillProfile,
        position: PositionProfile,
        relation_type: str = "requires",
        conclusion: dict = None,
        consensus_rounds: int = 1,
    ) -> RelationProfile:
        """鏋勫缓缁撴瀯鍖栫殑鍏崇郴鐢诲儚
        
        Args:
            skill: 鎶€鑳界敾鍍?            position: 宀椾綅鐢诲儚
            relation_type: 鍏崇郴绫诲瀷
            conclusion: 骞昏闃叉帶妯″潡鐨勮緭鍑?{valid, confidence, explanation, evidence, counter_evidence, recommendation}
            consensus_rounds: 鍏辫瘑杞
        
        Returns:
            瀹屾暣鐨勫叧绯荤敾鍍?        """
        conclusion = conclusion or {}
        relation_id = self._generate_relation_id(skill.skill_id, position.position_id)

        evidence_list = []
        for ev in conclusion.get("evidence", []):
            evidence_list.append(
                EvidenceItem(
                    type=ev.get("type", ""),
                    detail=ev.get("detail", ""),
                    source=ev.get("source"),
                )
            )

        counter_evidence_list = []
        for cev in conclusion.get("counter_evidence", []):
            counter_evidence_list.append(
                EvidenceItem(
                    type=cev.get("type", ""),
                    detail=cev.get("detail", ""),
                    source=cev.get("source"),
                )
            )

        provenance = RelationProvenance(
            created_by="agent2_hallucination_prevention",
            created_at=datetime.now().isoformat(),
            llm_model=XF_MODEL,
            consensus_rounds=consensus_rounds,
        )

        profile = RelationProfile(
            relation_id=relation_id,
            source_type="skill",
            source_id=skill.skill_id,
            source_name=skill.name,
            target_type="position",
            target_id=position.position_id,
            target_name=position.name,
            relation_type=relation_type,
            valid=conclusion.get("valid", False),
            confidence=conclusion.get("confidence", 0.0),
            explanation=conclusion.get("explanation", ""),
            evidence=evidence_list,
            counter_evidence=counter_evidence_list,
            recommendation=conclusion.get("recommendation", ""),
            provenance=provenance,
        )

        # 持久化
        self.store.save_relation_profile(profile)

        # 楂樼疆淇″害鍐?jobs_kg锛屼綆缃俊搴﹀叆瀹℃牳闃熷垪
        from agents.agent2.config import CONFIDENCE_HIGH_THRESHOLD
        if profile.confidence >= CONFIDENCE_HIGH_THRESHOLD and profile.valid:
            self.store.save_to_jobs_kg(profile)
            logger.info(f"Relation {relation_id} written to jobs_kg (confidence={profile.confidence:.2f})")
        elif not profile.valid or profile.confidence < 0.5:
            self.store.add_to_audit_queue(profile.model_dump())
            logger.info(f"Relation {relation_id} added to audit queue (confidence={profile.confidence:.2f})")

        return profile

    @staticmethod
    def _generate_relation_id(skill_id: str, position_id: str) -> str:
        import hashlib
        raw = f"{skill_id}:{position_id}"
        hash_obj = hashlib.md5(raw.encode("utf-8"))
        return f"REL_{hash_obj.hexdigest()[:12].upper()}"


__all__ = ["RelationProfileBuilder"]
