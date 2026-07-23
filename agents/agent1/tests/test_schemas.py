"""Agent 1 测试套件 —— 数据模型"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import pytest
from pydantic import ValidationError

from agents.agent1.job_discovery.schemas import NewPositionSuggestion, ClusterInfo, ClusteringResult
from agents.agent1.skill_evolution.schemas import SkillChangeSuggestion, TrendPoint, PositionSkillTrend
from agents.agent1.output_adapter.schemas import InputRecord, Agent1Output


class TestNewPositionSuggestion:
    def test_create_full(self):
        s = NewPositionSuggestion(
            suggested_name="AI训练数据标注师",
            description="负责大规模AI训练数据的标注与质量审核",
            cluster_size=47, novelty_score=0.88,
            evidence_samples=["负责文本标注", "负责质控"],
            related_skills=["数据标注", "Python"],
            suggested_required_skills=["数据标注工具"],
            suggested_optional_skills=["Python"],
            typical_salary_range={"min": 8000, "max": 25000},
            typical_experience="1-3年",
            data_sources=["bosszhipin"],
            confidence=0.85,
            provenance={"batch_id": "B001"},
        )
        assert s.suggested_name == "AI训练数据标注师"
        assert s.novelty_score == 0.88
        assert len(s.evidence_samples) == 2

    def test_create_minimal(self):
        s = NewPositionSuggestion(suggested_name="测试岗", description="测试描述")
        assert s.suggested_name == "测试岗"
        assert s.cluster_size == 0
        assert s.novelty_score == 0.0
        assert s.related_skills == []
        assert s.typical_salary_range == {}

    def test_novelty_score_bounds(self):
        with pytest.raises(ValidationError):
            NewPositionSuggestion(suggested_name="x", description="x", novelty_score=1.5)
        with pytest.raises(ValidationError):
            NewPositionSuggestion(suggested_name="x", description="x", novelty_score=-0.1)

    def test_serialize(self):
        s = NewPositionSuggestion(suggested_name="测试", description="描述")
        data = s.model_dump()
        assert data["suggested_name"] == "测试"
        assert "novelty_score" in data

    def test_confidence_bounds(self):
        with pytest.raises(ValidationError):
            NewPositionSuggestion(suggested_name="x", description="x", confidence=1.1)

    def test_empty_skills_defaults(self):
        s = NewPositionSuggestion(suggested_name="x", description="x")
        assert s.related_skills == []
        assert s.suggested_required_skills == []

    def test_salary_range_dict(self):
        s = NewPositionSuggestion(
            suggested_name="x", description="x",
            typical_salary_range={"min": 10000, "max": 30000, "avg": 20000},
        )
        assert s.typical_salary_range["avg"] == 20000

    def test_provenance(self):
        s = NewPositionSuggestion(
            suggested_name="x", description="x",
            provenance={"batch_id": "B001", "model": "deepseek"},
        )
        assert s.provenance["batch_id"] == "B001"

    def test_data_sources(self):
        s = NewPositionSuggestion(
            suggested_name="x", description="x",
            data_sources=["bosszhipin", "zhilian"],
        )
        assert len(s.data_sources) == 2


class TestClusterInfo:
    def test_create(self):
        c = ClusterInfo(cluster_id=0, size=10)
        assert c.cluster_id == 0
        assert c.size == 10
        assert c.centroid == []
        assert c.sample_indices == []

    def test_noise_cluster(self):
        c = ClusterInfo(cluster_id=-1, size=5)
        assert c.cluster_id == -1

    def test_with_samples(self):
        c = ClusterInfo(
            cluster_id=1, size=3,
            centroid=[0.1, 0.2, 0.3],
            sample_indices=[0, 1, 2],
            titles_sample=["后端", "前端"],
            text_sample=["desc1", "desc2"],
        )
        assert len(c.centroid) == 3
        assert c.titles_sample[0] == "后端"


class TestClusteringResult:
    def test_create(self):
        r = ClusteringResult()
        assert r.n_records == 0
        assert r.n_clusters == 0
        assert r.clusters == []

    def test_with_clusters(self):
        c1 = ClusterInfo(cluster_id=0, size=5)
        c2 = ClusterInfo(cluster_id=1, size=3)
        r = ClusteringResult(
            n_records=20, n_clusters=2, n_noise=2,
            clusters=[c1, c2], method="hdbscan",
        )
        assert r.n_records == 20
        assert len(r.clusters) == 2

    def test_method_default(self):
        r = ClusteringResult()
        assert r.method == "hdbscan"
class TestSkillChangeSuggestion:
    def test_create_full(self):
        s = SkillChangeSuggestion(
            position_name="大模型算法工程师", skill_name="RAG",
            change_type="rising", trend_score=0.75,
            frequency_before=0.1, frequency_after=0.65,
            time_window={"start": "2026-01", "end": "2026-06"},
            suggestion="建议加入必需技能",
            cross_domain_flag=False, confidence=0.82,
        )
        assert s.position_name == "大模型算法工程师"
        assert s.change_type == "rising"
        assert s.trend_score == 0.75

    def test_create_minimal(self):
        s = SkillChangeSuggestion(position_name="测试", skill_name="测试技能", change_type="new")
        assert s.trend_score == 0.0
        assert s.cross_domain_flag is False

    def test_change_type_enum(self):
        for ct in ["new", "dying", "rising", "declining"]:
            s = SkillChangeSuggestion(position_name="x", skill_name="y", change_type=ct)
            assert s.change_type == ct

    def test_trend_score_bounds(self):
        with pytest.raises(ValidationError):
            SkillChangeSuggestion(position_name="x", skill_name="y", change_type="new", trend_score=1.5)

    def test_with_trend_points(self):
        tp = TrendPoint(period="2026-Q1", frequency=0.2, record_count=50)
        s = SkillChangeSuggestion(position_name="x", skill_name="y", change_type="rising", trend_points=[tp])
        assert len(s.trend_points) == 1
        assert s.trend_points[0].period == "2026-Q1"

    def test_sample_jds(self):
        s = SkillChangeSuggestion(position_name="x", skill_name="y", change_type="new", sample_jds=["JD1", "JD2"])
        assert len(s.sample_jds) == 2

    def test_cross_domain_flag(self):
        s = SkillChangeSuggestion(position_name="x", skill_name="y", change_type="rising", cross_domain_flag=True)
        assert s.cross_domain_flag is True

    def test_serialize(self):
        s = SkillChangeSuggestion(position_name="x", skill_name="y", change_type="declining")
        data = s.model_dump()
        assert data["change_type"] == "declining"
        assert "trend_score" in data


class TestTrendPoint:
    def test_create(self):
        tp = TrendPoint(period="2026-Q1", frequency=0.5, record_count=100)
        assert tp.period == "2026-Q1"
        assert tp.frequency == 0.5

    def test_minimal(self):
        tp = TrendPoint(period="未知")
        assert tp.frequency == 0.0


class TestPositionSkillTrend:
    def test_create(self):
        t = PositionSkillTrend(position_name="算法工程师", total_records=50)
        assert t.position_name == "算法工程师"
        assert t.skill_frequencies == {}

    def test_with_frequencies(self):
        t = PositionSkillTrend(
            position_name="测试", total_records=10,
            time_windows=["2026-Q1", "2026-Q2"],
            skill_frequencies={"Python": [0.8, 0.9]},
        )
        assert t.skill_frequencies["Python"] == [0.8, 0.9]


class TestInputRecord:
    def test_create_full(self):
        r = InputRecord(
            title="算法工程师", description="负责算法研发",
            skills=["Python", "PyTorch"], company="某公司", industry="AI",
            city="北京", salary="30K-50K", experience="3-5年", pub_date="2026-06-01",
            extras={"source": "test"},
        )
        assert r.title == "算法工程师"
        assert r.extras["source"] == "test"

    def test_create_minimal(self):
        r = InputRecord(title="测试岗", description="测试描述")
        assert r.skills == []
        assert r.company is None
        assert r.extras == {}

    def test_all_optionals_none(self):
        r = InputRecord(title="t", description="d")
        assert r.industry is None
        assert r.city is None

    def test_serialize(self):
        r = InputRecord(title="t", description="d")
        d = r.model_dump()
        assert d["title"] == "t"
        assert "extras" in d


class TestAgent1Output:
    def test_create_new_position(self):
        o = Agent1Output(
            output_id="OUT001", created_at="2026-07-17T10:00:00",
            batch_id="B001", output_type="new_position",
            payload={"suggested_name": "新岗位", "description": "xxx"},
        )
        assert o.output_type == "new_position"
        assert o.status == "pending"

    def test_create_skill_change(self):
        o = Agent1Output(
            output_id="OUT002", created_at="2026-07-17T10:00:00",
            batch_id="B001", output_type="skill_change",
            payload={"skill_name": "RAG", "change_type": "rising"},
            status="verified", verified_by="agent2",
            tags=["test"], metadata={"position": "工程师"},
        )
        assert o.status == "verified"
        assert o.verified_by == "agent2"

    def test_status_flow(self):
        o = Agent1Output(
            output_id="OUT003", created_at="2026-07-17T10:00:00",
            batch_id="B001", output_type="new_position", payload={},
        )
        assert o.status == "pending"
        o.status = "verified"
        assert o.status == "verified"

    def test_metadata_extensible(self):
        o = Agent1Output(
            output_id="OUT004", created_at="2026-07-17T10:00:00",
            batch_id="B001", output_type="skill_change", payload={},
            metadata={"future_field": "any_value"},
        )
        assert o.metadata["future_field"] == "any_value"

    def test_serialize(self):
        o = Agent1Output(
            output_id="OUT005", created_at="2026-07-17T10:00:00",
            batch_id="B001", output_type="new_position",
            payload={"name": "test"},
        )
        d = o.model_dump()
        assert d["status"] == "pending"
        assert d["output_type"] == "new_position"
