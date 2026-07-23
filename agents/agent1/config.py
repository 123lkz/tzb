"""Agent 1 配置模块"""
import os
from dotenv import load_dotenv

load_dotenv()

# ===== MongoDB =====
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "recruitment")

JOBS_CLEAN_COLLECTION = "jobs_clean"
AGENT1_OUTPUT_COLLECTION = "agent1_output"
PROFILES_COLLECTION = "nlp_profiles"

# ===== 文本向量化 =====
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
EMBEDDING_DIMENSION = 384

# ===== 聚类参数 =====
CLUSTER_MIN_SAMPLES = int(os.getenv("CLUSTER_MIN_SAMPLES", "5"))
CLUSTER_MIN_CLUSTER_SIZE = int(os.getenv("CLUSTER_MIN_CLUSTER_SIZE", "5"))
CLUSTERING_METHOD = os.getenv("CLUSTERING_METHOD", "hdbscan")

# ===== 新兴性判定 =====
NOVELTY_THRESHOLD = float(os.getenv("NOVELTY_THRESHOLD", "0.75"))
NOVELTY_VARIANT_THRESHOLD = float(os.getenv("NOVELTY_VARIANT_THRESHOLD", "0.60"))

# ===== 趋势分析 =====
TREND_WINDOW_MONTHS = int(os.getenv("TREND_WINDOW_MONTHS", "3"))
TREND_MIN_RECORDS = int(os.getenv("TREND_MIN_RECORDS", "10"))
TREND_RISING_THRESHOLD = float(os.getenv("TREND_RISING_THRESHOLD", "0.30"))
TREND_DECLINING_THRESHOLD = float(os.getenv("TREND_DECLINING_THRESHOLD", "-0.30"))

# ===== 批处理 =====
DEFAULT_BATCH_SIZE = int(os.getenv("DEFAULT_BATCH_SIZE", "500"))
MAX_TEXT_LENGTH = 2000

# ===== 日志 =====
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "agent1.log")
