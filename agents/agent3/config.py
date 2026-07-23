"""Agent 3 配置模块"""
from agents.agent2.config import MONGODB_URI, MONGODB_DB

RESUME_PROFILES_COLLECTION = "resume_profiles"
MATCH_REPORTS_COLLECTION = "match_reports"
RESUME_CONFIDENCE_THRESHOLD = 0.6
SUPPORTED_FILE_TYPES = [".pdf", ".docx", ".txt"]

MATCH_WEIGHTS = {"skill": 0.45, "experience": 0.30, "responsibility": 0.25}
RECOMMEND_HIGH = 0.80
RECOMMEND_MEDIUM = 0.60
RECOMMEND_LOW = 0.40
GLOBAL_MATCH_TOP_K = 5
LOG_LEVEL = "INFO"
LOG_FILE = "agent3.log"
