"""JobClusterer — 文本聚类引擎

职责：从 jobs_clean 读取岗位数据，进行文本向量化和聚类分析。
支持 SentenceTransformer 和降级 TF-IDF 两种向量化方式。
"""
import re
import numpy as np
from loguru import logger

from agents.agent1.config import (
    EMBEDDING_MODEL_NAME, MAX_TEXT_LENGTH,
    CLUSTER_MIN_SAMPLES, CLUSTER_MIN_CLUSTER_SIZE, CLUSTERING_METHOD,
)


class JobClusterer:
    """对岗位数据进行文本聚类"""

    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model_name = model_name
        self._model = None
        self._vectorizer = None
        self._embedding_fallback = False
        logger.info(f"JobClusterer 初始化: model={model_name}")

    def _load_model(self):
        """加载向量化模型，失败时降级到 TF-IDF"""
        if self._model is not None:
            return
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
            self._embedding_fallback = False
            logger.info(f"SentenceTransformer 模型已加载: {self.model_name}")
        except Exception as e:
            logger.warning(f"SentenceTransformer 加载失败 ({e})，降级至 TF-IDF")
            from sklearn.feature_extraction.text import TfidfVectorizer
            self._vectorizer = TfidfVectorizer(max_features=1000, stop_words="english")
            self._embedding_fallback = True

    def _build_text(self, record: dict) -> str:
        """将单条记录拼接为用于聚类的文本"""
        parts = []
        title = record.get("title", "")
        if title:
            parts.append(title)
        desc = record.get("description", "")
        if desc:
            parts.append(desc[:MAX_TEXT_LENGTH])
        skills = record.get("skills", [])
        if skills:
            parts.append(" ".join(skills) if isinstance(skills, list) else skills)
        text = " ".join(parts)
        return text[:MAX_TEXT_LENGTH]

    def _normalize_embedding(self, embedding) -> list[float]:
        """归一化向量"""
        arr = np.array(embedding, dtype=np.float32)
        norm = np.linalg.norm(arr)
        if norm > 0:
            arr = arr / norm
        return arr.tolist()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """将文本列表转换为向量列表"""
        self._load_model()
        if not self._embedding_fallback and self._model is not None:
            embeddings = self._model.encode(texts, show_progress_bar=False)
            return [self._normalize_embedding(e) for e in embeddings]
        else:
            if not texts:
                return []
            matrices = self._vectorizer.fit_transform(texts)
            return [m.tolist() for m in matrices.toarray()]

    def embed_one(self, text: str) -> list[float]:
        """将单条文本转换为向量"""
        return self.embed_texts([text])[0]

    def cluster(self, records: list[dict]) -> "ClusteringResult":
        """对记录列表执行聚类

        返回 ClusteringResult 对象，包含簇信息和噪声信息。
        """
        from agents.agent1.job_discovery.schemas import ClusteringResult, ClusterInfo

        if not records:
            logger.warning("聚类输入为空")
            return ClusteringResult(n_records=0)

        # 构建文本并向量化
        texts = [self._build_text(r) for r in records]
        embeddings = self.embed_texts(texts)
        logger.info(f"向量化完成: {len(texts)} 条, 维度={len(embeddings[0]) if embeddings else 0}")

        # 执行聚类
        try:
            result = self._run_hdbscan(embeddings)
        except Exception as e:
            logger.warning(f"HDBSCAN 聚类失败 ({e})，降级到 KMeans")
            result = self._run_kmeans_fallback(embeddings)

        # 构建 ClusteringResult
        clusters = []
        for cluster_id in sorted(set(result.get("labels", []))):
            if cluster_id < 0:
                continue  # 跳过噪声点
            mask = np.array(result["labels"]) == cluster_id
            indices = np.where(mask)[0].tolist()

            # 找到距离质心最近的样本作为代表性样本
            cluster_embeddings = np.array([embeddings[i] for i in indices])
            centroid = cluster_embeddings.mean(axis=0).tolist()

            # 代表性样本：取前3条距质心最近的
            dists = np.linalg.norm(cluster_embeddings - np.array(centroid), axis=1)
            nearest = np.argsort(dists)[:3].tolist()
            sample_idx = [indices[i] for i in nearest]

            cluster_info = ClusterInfo(
                cluster_id=int(cluster_id),
                size=len(indices),
                centroid=centroid,
                sample_indices=sample_idx,
                titles_sample=[records[i].get("title", "") for i in sample_idx],
                text_sample=[texts[i][:200] for i in sample_idx],
            )
            clusters.append(cluster_info)

        # 按簇大小降序排列
        clusters.sort(key=lambda c: c.size, reverse=True)

        n_noise = result.get("n_noise", 0)
        logger.info(f"聚类完成: {len(clusters)} 个有效簇, {n_noise} 个噪声点")

        return ClusteringResult(
            n_records=len(records),
            n_clusters=len(clusters),
            n_noise=n_noise,
            clusters=clusters,
            method=result.get("method", CLUSTERING_METHOD),
        )

    def _run_hdbscan(self, embeddings: list[list[float]]) -> dict:
        """使用 HDBSCAN 进行聚类"""
        import hdbscan
        arr = np.array(embeddings, dtype=np.float64)
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=CLUSTER_MIN_CLUSTER_SIZE,
            min_samples=CLUSTER_MIN_SAMPLES,
            metric="euclidean",
            prediction_data=True,
        )
        labels = clusterer.fit_predict(arr)
        n_noise = int((labels == -1).sum())
        return {
            "labels": labels.tolist(),
            "n_noise": n_noise,
            "method": "hdbscan",
        }

    def _run_kmeans_fallback(self, embeddings: list[list[float]]) -> dict:
        """KMeans 降级方案"""
        from sklearn.cluster import KMeans
        arr = np.array(embeddings, dtype=np.float64)
        n_clusters = max(2, min(len(embeddings) // CLUSTER_MIN_CLUSTER_SIZE, 20))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
        labels = kmeans.fit_predict(arr)
        return {
            "labels": labels.tolist(),
            "n_noise": 0,
            "method": "kmeans",
        }

