"""Agent 1 - New position discovery + skill evolution"""

# 使用懒加载避免 -m 运行时的 RuntimeWarning
def get_orchestrator():
    from .main import Agent1Orchestrator
    return Agent1Orchestrator

from .config import *

