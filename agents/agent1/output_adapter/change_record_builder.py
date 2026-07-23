"""ChangeRecordBuilder — 变更记录组装器

职责：接收 job_discovery 和 skill_evolution 的输出，
统一包装为 Agent1Output 格式。
"""
import uuid
from datetime import datetime
from loguru import logger

from agents.agent1.job_discovery.schemas import NewPositionSuggestion
from agents.agent1.skill_evolution.schemas import SkillChangeSuggestion
from agents.agent1.output_adapter.schemas import Agent1Output


class ChangeRecordBuilder:
    """将各类建议转换为统一的 Agent1Output"""

    def __init__(self, batch_id: str = None):
        self.batch_id = batch_id or f"B{datetime.now().strftime('%Y%m%d%H%M%S')}"
        logger.info(f"ChangeRecordBuilder: batch_id={self.batch_id}")

    def build_from_new_position(self, suggestion: NewPositionSuggestion) -> Agent1Output:
        """将新岗位建议包装为 Agent1Output"""
        return Agent1Output(
            output_id=str(uuid.uuid4()),
            created_at=datetime.now().isoformat(),
            batch_id=self.batch_id,
            output_type="new_position",
            payload=suggestion.model_dump(),
            status="pending",
            tags=["new_position"],
            metadata={"cluster_size": suggestion.cluster_size},
        )

    def build_from_skill_change(self, suggestion: SkillChangeSuggestion) -> Agent1Output:
        """将技能变更建议包装为 Agent1Output"""
        return Agent1Output(
            output_id=str(uuid.uuid4()),
            created_at=datetime.now().isoformat(),
            batch_id=self.batch_id,
            output_type="skill_change",
            payload=suggestion.model_dump(),
            status="pending",
            tags=[f"change_type:{suggestion.change_type}"],
            metadata={"position_name": suggestion.position_name},
        )

    def build_batch(self,
                    new_positions: list[NewPositionSuggestion],
                    skill_changes: list[SkillChangeSuggestion]) -> list[Agent1Output]:
        """批量构建输出记录"""
        outputs = []

        for np_sug in new_positions:
            outputs.append(self.build_from_new_position(np_sug))

        for sc_sug in skill_changes:
            outputs.append(self.build_from_skill_change(sc_sug))

        logger.info(f"批量构建完成: {len(outputs)} 条输出记录 "
                     f"({len(new_positions)} 新岗位 + {len(skill_changes)} 技能变更)")
        return outputs
