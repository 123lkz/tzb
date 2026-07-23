"""OutputAdapter 单元测试"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import pytest
from datetime import datetime
from agents.agent1.output_adapter.change_record_builder import ChangeRecordBuilder
from agents.agent1.output_adapter.graph_interface import GraphInterface
from agents.agent1.output_adapter.schemas import Agent1Output
from agents.agent1.job_discovery.schemas import NewPositionSuggestion
from agents.agent1.skill_evolution.schemas import SkillChangeSuggestion


class TestChangeRecordBuilder:
    def test_build_from_new_position(self):
        builder = ChangeRecordBuilder(batch_id="TEST001")
        suggestion = NewPositionSuggestion(
            suggested_name="新岗位", description="测试描述", cluster_size=10
        )
        output = builder.build_from_new_position(suggestion)
        assert output.output_type == "new_position"
        assert output.batch_id == "TEST001"
        assert output.status == "pending"
        assert "new_position" in output.tags

    def test_build_from_skill_change(self):
        builder = ChangeRecordBuilder(batch_id="TEST002")
        suggestion = SkillChangeSuggestion(
            position_name="算法", skill_name="RAG", change_type="rising"
        )
        output = builder.build_from_skill_change(suggestion)
        assert output.output_type == "skill_change"
        assert output.batch_id == "TEST002"
        assert "change_type:rising" in output.tags

    def test_build_batch(self):
        builder = ChangeRecordBuilder()
        new_pos = NewPositionSuggestion(suggested_name="A", description="desc")
        skill_ch = SkillChangeSuggestion(position_name="X", skill_name="Y", change_type="new")
        outputs = builder.build_batch([new_pos], [skill_ch])
        assert len(outputs) == 2
        assert outputs[0].output_type == "new_position"
        assert outputs[1].output_type == "skill_change"

    def test_batch_empty(self):
        builder = ChangeRecordBuilder()
        outputs = builder.build_batch([], [])
        assert outputs == []

    def test_output_id_unique(self):
        builder = ChangeRecordBuilder()
        s1 = NewPositionSuggestion(suggested_name="A", description="d")
        s2 = NewPositionSuggestion(suggested_name="B", description="d")
        o1 = builder.build_from_new_position(s1)
        o2 = builder.build_from_new_position(s2)
        assert o1.output_id != o2.output_id

    def test_output_has_created_at(self):
        builder = ChangeRecordBuilder()
        s = NewPositionSuggestion(suggested_name="A", description="d")
        output = builder.build_from_new_position(s)
        assert output.created_at is not None
        assert len(output.created_at) > 0


class TestGraphInterface:
    def test_save_and_query(self):
        iface = GraphInterface()
        output = Agent1Output(
            output_id="TEST_SAVE_001",
            created_at=datetime.now().isoformat(),
            batch_id="TEST_BATCH",
            output_type="new_position",
            payload={"name": "test"},
        )
        saved = iface.save(output)
        assert saved is True

        try:
            pending = iface.get_pending(output_type="new_position", limit=10)
            found = any(p["output_id"] == "TEST_SAVE_001" for p in pending)
            assert found is True

            iface.update_status("TEST_SAVE_001", "verified", verified_by="test_agent")
            verified = iface.get_verified(output_type="new_position", limit=10)
            found_verified = any(p["output_id"] == "TEST_SAVE_001" for p in verified)
            assert found_verified is True
        finally:
            from agents.agent1.config import MONGODB_URI, MONGODB_DB, AGENT1_OUTPUT_COLLECTION
            import pymongo
            client = pymongo.MongoClient(MONGODB_URI)
            client[MONGODB_DB][AGENT1_OUTPUT_COLLECTION].delete_one({"output_id": "TEST_SAVE_001"})
            client.close()
            iface.close()

    def test_save_batch(self):
        iface = GraphInterface()
        outputs = [
            Agent1Output(
                output_id=f"TEST_BATCH_{i}",
                created_at=datetime.now().isoformat(),
                batch_id="TEST_BATCH",
                output_type="new_position",
                payload={"name": f"test_{i}"},
            )
            for i in range(3)
        ]
        saved_cnt = iface.save_batch(outputs)
        assert saved_cnt == 3

        try:
            pending = iface.get_pending(limit=10)
            found = sum(1 for p in pending if p["output_id"].startswith("TEST_BATCH_"))
            assert found == 3
        finally:
            from agents.agent1.config import MONGODB_URI, MONGODB_DB, AGENT1_OUTPUT_COLLECTION
            import pymongo
            client = pymongo.MongoClient(MONGODB_URI)
            for o in outputs:
                client[MONGODB_DB][AGENT1_OUTPUT_COLLECTION].delete_one({"output_id": o.output_id})
            client.close()
            iface.close()

    def test_count_by_status(self):
        iface = GraphInterface()
        output = Agent1Output(
            output_id="TEST_COUNT_001",
            created_at=datetime.now().isoformat(),
            batch_id="TEST",
            output_type="new_position",
            payload={},
        )
        iface.save(output)
        try:
            counts = iface.count_by_status()
            assert "pending" in counts
            assert counts["pending"] >= 1
        finally:
            from agents.agent1.config import MONGODB_URI, MONGODB_DB, AGENT1_OUTPUT_COLLECTION
            import pymongo
            client = pymongo.MongoClient(MONGODB_URI)
            client[MONGODB_DB][AGENT1_OUTPUT_COLLECTION].delete_one({"output_id": "TEST_COUNT_001"})
            client.close()
            iface.close()

    def test_close_multiple(self):
        iface = GraphInterface()
        iface.close()
        iface.close()
