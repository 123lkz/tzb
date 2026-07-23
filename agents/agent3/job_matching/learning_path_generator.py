from agents.agent3.job_matching.schemas import LearningStep, LearningPath
from agents.agent3.prompt_templates import LEARNING_PATH_SYSTEM_PROMPT, LEARNING_PATH_USER_PROMPT_TEMPLATE
from agents.agent2.nlp_profile.schemas import SkillProfile
from loguru import logger


class LearningPathGenerator:
    """学习路径生成器：为缺失技能生成结构化学习路径"""

    def __init__(self, llm_client=None):
        self.llm = llm_client

    def generate(self, skill_name: str, skill_profile: SkillProfile = None) -> LearningPath:
        """为缺失技能生成学习路径

        Args:
            skill_name: 技能名称
            skill_profile: 技能画像（可选，用于生成更精准的路径）

        Returns:
            LearningPath: 结构化学习路径
        """
        if self.llm is not None:
            return self._generate_with_llm(skill_name, skill_profile)
        return self._generate_with_rules(skill_name, skill_profile)

    def _generate_with_llm(self, skill_name: str, sp: SkillProfile = None) -> LearningPath:
        """使用 LLM 生成结构化学习路径"""
        try:
            sp_text = self._format_skill_profile(skill_name, sp)
            messages = [
                {"role": "system", "content": LEARNING_PATH_SYSTEM_PROMPT},
                {"role": "user", "content": LEARNING_PATH_USER_PROMPT_TEMPLATE.format(
                    skill_name=skill_name, skill_profile=sp_text
                )},
            ]
            result = self.llm.chat_with_json(messages, temperature=0.3)
            if isinstance(result, dict) and "steps" in result:
                steps = []
                for s in result["steps"]:
                    if isinstance(s, dict) and "stage" in s and "description" in s:
                        steps.append(LearningStep(
                            stage=s.get("stage", ""),
                            description=s.get("description", ""),
                            duration=s.get("duration", ""),
                            resources=s.get("resources", []),
                        ))
                if steps:
                    return LearningPath(skill_name=skill_name, steps=steps)
        except Exception as e:
            logger.warning(f"LLM learning path generation failed for {skill_name}: {e}")

        # LLM 失败时降级到规则模式
        return self._generate_with_rules(skill_name, sp)

    @staticmethod
    def _generate_with_rules(skill_name: str, sp: SkillProfile = None) -> LearningPath:
        """基于规则的兜底学习路径生成"""
        steps = []

        # Foundation阶段
        if sp and sp.prerequisites:
            preq = " -> ".join(sp.prerequisites[:3])
            steps.append(LearningStep(
                stage="Foundation",
                description=f"掌握前置知识: {preq}",
                duration="2-4 weeks",
                resources=sp.prerequisites[:3],
            ))
        else:
            steps.append(LearningStep(
                stage="Foundation",
                description=f"学习 {skill_name} 的Foundation概念和原理",
                duration="2-3 weeks",
                resources=[],
            ))

        # Beginner阶段
        if sp and sp.typical_applications:
            apps = ", ".join(sp.typical_applications[:2])
            steps.append(LearningStep(
                stage="Beginner",
                description=f"完成官方教程，了解典型应用场景: {apps}",
                duration="2-3 weeks",
                resources=[],
            ))
        else:
            steps.append(LearningStep(
                stage="Beginner",
                description=f"完成 {skill_name} 的官方Beginner教程",
                duration="2-3 weeks",
                resources=[],
            ))

        # Practice阶段
        if sp and sp.related_technologies:
            techs = ", ".join(sp.related_technologies[:3])
            steps.append(LearningStep(
                stage="Practice",
                description=f"结合相关技术栈进行Practice: {techs}",
                duration="3-4 weeks",
                resources=sp.related_technologies[:3],
            ))
        else:
            steps.append(LearningStep(
                stage="Practice",
                description=f"通过实际Project练习 {skill_name} 的使用",
                duration="3-4 weeks",
                resources=[],
            ))

        # Project阶段
        steps.append(LearningStep(
            stage="Project",
            description=f"构建一个完整的Project，展示 {skill_name} 的实际应用能力",
            duration="4-6 weeks",
            resources=[],
        ))

        return LearningPath(skill_name=skill_name, steps=steps)

    @staticmethod
    def _format_skill_profile(skill_name: str, sp: SkillProfile = None) -> str:
        """格式化技能画像为文本"""
        if sp is None:
            return f"技能: {skill_name}（无详细画像）"
        parts = [f"技能: {skill_name}"]
        if sp.summary:
            parts.append(f"概述: {sp.summary}")
        if sp.prerequisites:
            parts.append(f"前置知识: {', '.join(sp.prerequisites)}")
        if sp.related_technologies:
            parts.append(f"相关技术: {', '.join(sp.related_technologies)}")
        if sp.typical_applications:
            parts.append(f"典型场景: {', '.join(sp.typical_applications)}")
        return "\n".join(parts)
