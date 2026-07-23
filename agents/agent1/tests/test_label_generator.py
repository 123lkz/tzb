"""LabelGenerator 单元测试"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import pytest
from agents.agent1.job_discovery.label_generator import LabelGenerator
from agents.agent1.job_discovery.schemas import ClusterInfo, NewPositionSuggestion


class MockLLM:
    def __init__(self, response=None):
        self.response = response or '{"suggested_name":"测试新岗位","description":"测试描述","core_responsibilities":["职责A","职责B"],"required_skills":["技能A"],"optional_skills":["技能B"],"typical_applications":["互联网","AI"],"confidence":0.85}'

    def chat_with_json(self, messages, temperature=0.3):
        import json
        return json.loads(self.response)


class TestLabelGeneratorStatistical:
    def test_generate_statistical_no_records(self):
        gen = LabelGenerator(llm_client=None)
        cluster = ClusterInfo(cluster_id=0, size=3, titles_sample=["测试工程师", "测试开发"])
        sug = gen.generate(cluster, None)
        assert isinstance(sug, NewPositionSuggestion)
        assert sug.confidence == 0.5
        assert "测试" in sug.suggested_name

    def test_generate_statistical_with_skills(self):
        gen = LabelGenerator(llm_client=None)
        cluster = ClusterInfo(cluster_id=0, size=2, sample_indices=[0, 1])
        records = [{"skills": ["Python", "PyTorch"]}, {"skills": ["Python", "TensorFlow"]}]
        sug = gen.generate(cluster, records)
        assert "Python" in sug.related_skills

    def test_common_name_extraction(self):
        gen = LabelGenerator(llm_client=None)
        cluster = ClusterInfo(cluster_id=0, size=3, titles_sample=["高级AI算法工程师", "AI算法工程师", "资深AI算法工程师"])
        sug = gen.generate(cluster, None)
        assert "AI" in sug.suggested_name or "算法" in sug.suggested_name

    def test_batch_generate(self):
        gen = LabelGenerator(llm_client=None)
        clusters = [
            ClusterInfo(cluster_id=0, size=2, titles_sample=["A岗"]),
            ClusterInfo(cluster_id=1, size=3, titles_sample=["B岗"]),
        ]
        records = [{"skills": ["Python"]}, {"skills": ["Java"]}, {"skills": ["Go"]}]
        results = gen.generate_batch(clusters, records)
        assert len(results) == 2
        assert all(isinstance(r, NewPositionSuggestion) for r in results)

    def test_empty_titles(self):
        gen = LabelGenerator(llm_client=None)
        cluster = ClusterInfo(cluster_id=5, size=1, titles_sample=[])
        sug = gen.generate(cluster, None)
        assert sug.suggested_name == "新兴岗位_簇5"

    def test_extract_skills_empty(self):
        gen = LabelGenerator(llm_client=None)
        skills = gen._extract_skills_from_records([])
        assert skills == []

    def test_extract_skills(self):
        gen = LabelGenerator(llm_client=None)
        records = [{"skills": ["A", "B"]}, {"skills": ["B", "C"]}]
        skills = gen._extract_skills_from_records(records)
        assert "A" in skills
        assert "B" in skills
        assert len(skills) == 3


class TestLabelGeneratorLLM:
    def test_generate_with_llm(self):
        mock = MockLLM()
        gen = LabelGenerator(llm_client=mock)
        cluster = ClusterInfo(cluster_id=0, size=5, titles_sample=["AI岗"], text_sample=["desc"])
        sug = gen._generate_with_llm(cluster, None)
        assert sug.suggested_name == "测试新岗位"
        assert sug.confidence == 0.85
        assert "技能A" in sug.suggested_required_skills

    def test_llm_fallback_on_error(self):
        class FailingMock:
            def chat_with_json(self, messages, temperature=0.3):
                raise Exception("API error")
        gen = LabelGenerator(llm_client=FailingMock())
        cluster = ClusterInfo(cluster_id=0, size=3, titles_sample=["岗"], text_sample=["d"])
        sug = gen._generate_with_llm(cluster, None)
        assert sug.confidence == 0.5
        assert sug.provenance["generation_method"] == "statistical"

    def test_llm_parse_invalid_json(self):
        class BadJSONMock:
            def chat_with_json(self, messages, temperature=0.3):
                return {"error": "parse_failed", "raw": "something"}
        gen = LabelGenerator(llm_client=BadJSONMock())
        cluster = ClusterInfo(cluster_id=0, size=3, titles_sample=["岗"], text_sample=["d"])
        sug = gen._generate_with_llm(cluster, None)
        assert sug.provenance["generation_method"] == "statistical"
