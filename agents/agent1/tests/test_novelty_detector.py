"""NoveltyDetector 单元测试"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import pytest
import numpy as np
from agents.agent1.job_discovery.novelty_detector import NoveltyDetector
from agents.agent1.job_discovery.schemas import ClusterInfo


def _make_cluster(cid, centroid):
    return ClusterInfo(cluster_id=cid, size=5, centroid=centroid)


def _norm(vec):
    arr = np.array(vec, dtype=float)
    return (arr / np.linalg.norm(arr)).tolist()


class TestNoveltyDetector:
    def test_empty_existing(self):
        detector = NoveltyDetector(threshold=0.75, variant_threshold=0.60)
        cluster = _make_cluster(0, [0.1, 0.2, 0.3])
        result = detector.detect(cluster, {})
        assert result["is_novel"] is True
        assert result["novelty_score"] == 1.0

    def test_novel_cluster(self):
        detector = NoveltyDetector(threshold=0.75)
        cluster = _make_cluster(0, _norm([1.0, 0.0, 0.0]))
        existing = {"后端开发": _norm([0.1, 0.2, 0.3]), "前端开发": _norm([0.0, 0.1, 0.9])}
        result = detector.detect(cluster, existing)
        assert result["is_novel"] is True
        assert result["novelty_score"] > 0.5

    def test_variant_detection(self):
        detector = NoveltyDetector(threshold=0.75, variant_threshold=0.60)
        cluster = _make_cluster(0, _norm([0.85, 0.10, 0.05]))
        existing = {"大模型算法工程师": _norm([0.82, 0.12, 0.06])}
        result = detector.detect(cluster, existing)
        assert "all_similarities" in result

    def test_most_similar_found(self):
        detector = NoveltyDetector(threshold=0.75)
        c = _norm([1.0, 0.0])
        e1 = _norm([0.99, 0.01])
        cluster = _make_cluster(0, c)
        existing = {"同岗位": e1, "其他": _norm([0.0, 1.0])}
        result = detector.detect(cluster, existing)
        assert result["most_similar"] == "同岗位"

    def test_all_similarities_format(self):
        detector = NoveltyDetector(threshold=0.75)
        cluster = _make_cluster(0, _norm([1.0, 0.0]))
        existing = {"A": _norm([1.0, 0.0]), "B": _norm([0.0, 1.0])}
        result = detector.detect(cluster, existing)
        assert len(result["all_similarities"]) <= 5

    def test_novelty_score_range(self):
        detector = NoveltyDetector(threshold=0.75)
        cluster = _make_cluster(0, _norm([0.5, 0.5]))
        existing = {"X": _norm([0.5, 0.5])}
        result = detector.detect(cluster, existing)
        assert 0.0 <= result["novelty_score"] <= 1.0
