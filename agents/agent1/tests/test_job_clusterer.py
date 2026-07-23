"""JobClusterer 单元测试"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import pytest
import numpy as np
from agents.agent1.job_discovery.job_clusterer import JobClusterer
from agents.agent1.job_discovery.schemas import ClusteringResult


class TestJobClustererBasic:
    def test_embed_texts_empty(self):
        clusterer = JobClusterer()
        clusterer._model = None
        clusterer._embedding_fallback = True
        from sklearn.feature_extraction.text import TfidfVectorizer
        clusterer._vectorizer = TfidfVectorizer(max_features=100)
        result = clusterer.embed_texts([])
        assert result == []

    def test_embed_texts_single(self):
        clusterer = JobClusterer()
        clusterer._model = None
        clusterer._embedding_fallback = True
        from sklearn.feature_extraction.text import TfidfVectorizer
        clusterer._vectorizer = TfidfVectorizer(max_features=100)
        result = clusterer.embed_texts(["test job posting"])
        assert len(result) == 1
        assert len(result[0]) > 0

    def test_embed_texts_multiple(self):
        clusterer = JobClusterer()
        clusterer._model = None
        clusterer._embedding_fallback = True
        from sklearn.feature_extraction.text import TfidfVectorizer
        clusterer._vectorizer = TfidfVectorizer(max_features=100)
        texts = ["data scientist job", "software engineer role", "product manager position"]
        result = clusterer.embed_texts(texts)
        assert len(result) == 3

    def test_build_text_full(self):
        clusterer = JobClusterer()
        record = {"title": "算法工程师", "description": "负责推荐系统算法研发", "skills": ["Python", "TensorFlow"]}
        text = clusterer._build_text(record)
        assert "算法工程师" in text
        assert "Python" in text
        assert len(text) <= 2000

    def test_build_text_minimal(self):
        clusterer = JobClusterer()
        text = clusterer._build_text({"title": "工程师"})
        assert "工程师" in text

    def test_build_text_empty(self):
        clusterer = JobClusterer()
        text = clusterer._build_text({})
        assert text == ""

    def test_cluster_empty(self):
        clusterer = JobClusterer()
        result = clusterer.cluster([])
        assert isinstance(result, ClusteringResult)
        assert result.n_records == 0

    def test_normalize_embedding(self):
        clusterer = JobClusterer()
        emb = clusterer._normalize_embedding([1.0, 2.0, 3.0])
        norm = np.linalg.norm(emb)
        assert abs(norm - 1.0) < 0.001

    def test_normalize_embedding_zero(self):
        clusterer = JobClusterer()
        emb = clusterer._normalize_embedding([0.0, 0.0, 0.0])
        assert emb == [0.0, 0.0, 0.0]

