"""Agent 2 config"""
import os
from dotenv import load_dotenv
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "recruitment")
JOBS_CLEAN_COLLECTION = "jobs_clean"
JOBS_KG_COLLECTION = "jobs_kg"
QUALITY_REPORTS_COLLECTION = "quality_reports"
PROFILES_COLLECTION = "nlp_profiles"
RELATION_PROFILES_COLLECTION = "relation_profiles"
AUDIT_QUEUE_COLLECTION = "audit_queue"
JOBS_DEDUPLICATED_COLLECTION = "jobs_deduplicated"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
XF_API_KEY = os.getenv("XF_API_KEY", "")
XF_API_SECRET = os.getenv("XF_API_SECRET", "")
XF_APP_ID = os.getenv("XF_APP_ID", "")
XF_API_BASE = os.getenv("XF_API_BASE", "wss://spark-api.xf-yun.com/v4.0/chat")
XF_MODEL = os.getenv("XF_MODEL", "spark-4.0")
HALLUCINATION_CHECK_PROMPT_VERSION = "v1.0"
CONSENSUS_MIN_ROUNDS = 3
CONFIDENCE_HIGH_THRESHOLD = 0.85
CONFIDENCE_MEDIUM_THRESHOLD = 0.60
CONFIDENCE_LOW_THRESHOLD = 0.30
DEFAULT_BATCH_SIZE = 50
MAX_WORKERS = 4
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "agent2.log")
