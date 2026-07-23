"""NoveltyDetector — 新兴性检测

职责：将聚类得到的新簇与已有岗位画像（PositionProfile）对比，
判断该簇是否代表新兴岗位，还是已有岗位的变体/子类。
"""
import numpy as np
from loguru import logger

from agents.agent1.config import NOVELTY_THRESHOLD, NOVELTY_VARIANT_THRESHOLD
from agents.agent1.job_discovery.schemas import ClusterInfo


class NoveltyDetector:
    """检测新簇的新兴程度"""

    def __init__(self, threshold: float = NOVELTY_THRESHOLD,
                 variant_threshold: float = NOVELTY_VARIANT_THRESHOLD):
        self.threshold = threshold
        self.variant_threshold = variant_threshold
        logger.info(f"NoveltyDetector: threshold={threshold}, variant_threshold={variant_threshold}")

    def detect(self, cluster: ClusterInfo,
               existing_embeddings: dict[str, list[float]]) -> dict:
        """检测簇的新兴性

        Args:
            cluster: 聚类得到的簇信息
            existing_embeddings: 已有岗位画像的 {position_name: embedding}

        Returns:
            dict: {
                "novelty_score": float,    # 0~1 新兴度
                "most_similar": str,        # 最相似的已有岗位名
                "similarity": float,        # 与最相似岗位的相似度
                "is_novel": bool,           # 是否为新岗位
                "is_variant": bool,         # 是否为已有岗位的变体
                "all_similarities": dict,   # {position_name: similarity}
            }
        """
        if not existing_embeddings:
            # 没有已有岗位画像，默认标记为新兴
            return {
                "novelty_score": 1.0,
                "most_similar": "",
                "similarity": 0.0,
                "is_novel": True,
                "is_variant": False,
                "all_similarities": {},
            }

        centroid = np.array(cluster.centroid)
        similarities = {}

        for pos_name, pos_emb in existing_embeddings.items():
            pos_vec = np.array(pos_emb)
            if len(centroid) != len(pos_vec):
                continue
            sim = float(np.dot(centroid, pos_vec))  # 已归一化，点积即余弦相似度
            similarities[pos_name] = sim

        if not similarities:
            return {
                "novelty_score": 1.0,
                "most_similar": "",
                "similarity": 0.0,
                "is_novel": True,
                "is_variant": False,
                "all_similarities": {},
            }

        # 找最相似和次相似的岗位
        sorted_sims = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        top_name, top_sim = sorted_sims[0]

        # 计算新兴度: 1 - 最高相似度
        novelty_score = 1.0 - top_sim
        novelty_score = max(0.0, min(1.0, novelty_score))

        is_novel = novelty_score >= (1.0 - self.threshold)
        is_variant = (not is_novel) and (novelty_score < (1.0 - self.variant_threshold))

        return {
            "novelty_score": round(novelty_score, 4),
            "most_similar": top_name,
            "similarity": round(top_sim, 4),
            "is_novel": bool(is_novel),
            "is_variant": bool(is_variant),
            "all_similarities": {k: round(v, 4) for k, v in sorted_sims[:5]},
        }
