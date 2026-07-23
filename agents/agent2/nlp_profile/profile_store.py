"""ProfileStore -- MongoDB ????"""
from datetime import datetime
from typing import Optional
import pymongo
from loguru import logger
from agents.agent2.config import MONGODB_URI, MONGODB_DB, PROFILES_COLLECTION, RELATION_PROFILES_COLLECTION, QUALITY_REPORTS_COLLECTION, AUDIT_QUEUE_COLLECTION
from agents.agent2.nlp_profile.schemas import SkillProfile, PositionProfile, RelationProfile, CheckResult, QualityReport

class ProfileStore:
    def __init__(self, uri: str = MONGODB_URI, db_name: str = MONGODB_DB):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        self.profiles = self.db[PROFILES_COLLECTION]
        self.relation_profiles = self.db[RELATION_PROFILES_COLLECTION]
        self.quality_reports = self.db[QUALITY_REPORTS_COLLECTION]
        self.audit_queue = self.db[AUDIT_QUEUE_COLLECTION]
        self.profiles.create_index([("skill_id", pymongo.ASCENDING)], unique=True, sparse=True)
        self.profiles.create_index([("position_id", pymongo.ASCENDING)], unique=True, sparse=True)
        self.profiles.create_index([("name", pymongo.ASCENDING)])
        self.relation_profiles.create_index([("relation_id", pymongo.ASCENDING)], unique=True)
        self.quality_reports.create_index([("record_id", pymongo.ASCENDING)])

    def save_skill_profile(self, profile: SkillProfile) -> bool:
        try:
            data = profile.model_dump(mode="json"); data["type"] = "skill"; data["last_updated"] = datetime.now().isoformat()
            self.profiles.update_one({"skill_id": profile.skill_id}, {"$set": data}, upsert=True)
            return True
        except Exception as e: logger.error(f"save skill failed: {e}"); return False

    def get_skill_profile(self, skill_id: str) -> Optional[SkillProfile]:
        doc = self.profiles.find_one({"skill_id": skill_id, "type": "skill"})
        if doc: doc.pop("_id", None); return SkillProfile(**doc)
        return None

    def get_skill_profile_by_name(self, name: str) -> Optional[SkillProfile]:
        doc = self.profiles.find_one({"name": name, "type": "skill"})
        if doc: doc.pop("_id", None); return SkillProfile(**doc)
        return None

    def get_all_skill_profiles(self) -> list[SkillProfile]:
        result = []
        for doc in self.profiles.find({"type": "skill"}):
            doc.pop("_id", None); result.append(SkillProfile(**doc))
        return result

    def save_position_profile(self, profile: PositionProfile) -> bool:
        try:
            data = profile.model_dump(mode="json"); data["type"] = "position"; data["last_updated"] = datetime.now().isoformat()
            self.profiles.update_one({"position_id": profile.position_id}, {"$set": data}, upsert=True)
            return True
        except Exception as e: logger.error(f"save position failed: {e}"); return False

    def get_position_profile(self, position_id: str) -> Optional[PositionProfile]:
        doc = self.profiles.find_one({"position_id": position_id, "type": "position"})
        if doc: doc.pop("_id", None); return PositionProfile(**doc)
        return None

    def get_position_profile_by_name(self, name: str) -> Optional[PositionProfile]:
        doc = self.profiles.find_one({"name": name, "type": "position"})
        if doc: doc.pop("_id", None); return PositionProfile(**doc)
        return None

    def get_all_position_profiles(self) -> list[PositionProfile]:
        result = []
        for doc in self.profiles.find({"type": "position"}):
            doc.pop("_id", None); result.append(PositionProfile(**doc))
        return result

    def save_relation_profile(self, profile: RelationProfile) -> bool:
        try:
            data = profile.model_dump()
            import json as _j
            data = _j.loads(_j.dumps(data))
            r = self.relation_profiles.replace_one({"relation_id": profile.relation_id}, data, upsert=True)
            logger.info(f"Relation profile saved: {profile.relation_id} upserted={r.upserted_id is not None}")
            return True
        except Exception as e:
            logger.error(f"save relation FAILED: {e}")
            return False

    def save_quality_report(self, report: QualityReport) -> bool:
        try: self.quality_reports.insert_one(report.model_dump()); return True
        except Exception as e: logger.error(f"save quality report failed: {e}"); return False

    def save_to_jobs_kg(self, relation: RelationProfile):
        try:
            doc = {"relation_id": relation.relation_id, "source_type": relation.source_type, "source_id": relation.source_id, "source_name": relation.source_name, "target_type": relation.target_type, "target_id": relation.target_id, "target_name": relation.target_name, "relation_type": relation.relation_type, "confidence": relation.confidence, "explanation": relation.explanation, "source": "agent2", "created_at": datetime.now().isoformat()}
            self.db["jobs_kg"].update_one({"relation_id": relation.relation_id}, {"$set": doc}, upsert=True)
        except Exception as e: logger.error(f"save to jobs_kg failed: {e}")

    def add_to_audit_queue(self, item: dict) -> bool:
        try: item["status"] = "pending"; item["created_at"] = datetime.now().isoformat(); self.audit_queue.insert_one(item); return True
        except Exception as e: logger.error(f"add to audit queue failed: {e}"); return False

    def close(self):
        self.client.close()

__all__ = ["ProfileStore"]
