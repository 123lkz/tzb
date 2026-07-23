"""EvolutionDetector — 演化检测

职责：基于 SkillTrendAnalyzer 的输出，判定每个技能的演化状态：
新增/淘汰/升温/降温，以及跨领域迁移检测。
"""
import numpy as np
from collections import defaultdict
from loguru import logger

from agents.agent1.config import (
    TREND_RISING_THRESHOLD, TREND_DECLINING_THRESHOLD,
)
from agents.agent1.skill_evolution.schemas import (
    SkillChangeSuggestion, PositionSkillTrend,
)


class EvolutionDetector:
    """检测技能的演化状态"""

    def __init__(self, rising_threshold: float = TREND_RISING_THRESHOLD,
                 declining_threshold: float = TREND_DECLINING_THRESHOLD):
        self.rising_threshold = rising_threshold
        self.declining_threshold = declining_threshold
        logger.info(f"EvolutionDetector: rising={rising_threshold}, declining={declining_threshold}")

    def detect(self, trends: list[PositionSkillTrend]) -> list[SkillChangeSuggestion]:
        """对所有岗位的技能执行演化检测

        Args:
            trends: SkillTrendAnalyzer 的分析结果

        Returns:
            list[SkillChangeSuggestion]: 检测到的技能变更
        """
        all_suggestions = []

        for trend in trends:
            suggestions = self._detect_single_position(trend)
            all_suggestions.extend(suggestions)

        # 跨领域迁移检测
        cross_domain = self._detect_cross_domain(all_suggestions)
        for cd in cross_domain:
            for s in all_suggestions:
                if s.skill_name == cd["skill_name"] and s.position_name != cd["position_name"]:
                    s.cross_domain_flag = True

        logger.info(f"演化检测完成: 共 {len(all_suggestions)} 项技能变更")
        return all_suggestions

    def _detect_single_position(self, trend: PositionSkillTrend) -> list[SkillChangeSuggestion]:
        """检测单个岗位的技能演化"""
        suggestions = []
        windows = trend.time_windows
        n_windows = len(windows)

        if n_windows < 2:
            return []  # 至少需要两个时间窗口才能做演化检测

        for skill_name, freq_list in trend.skill_frequencies.items():
            if len(freq_list) < 2:
                continue

            freq_before = freq_list[0]
            freq_after = freq_list[-1]

            # 计算趋势得分：使用最后一个窗口和第一个窗口的差值
            trend_score = freq_after - freq_before

            # 判断变化类型
            change_type = self._classify_change(
                trend_score, freq_before, freq_after, n_windows
            )
            if change_type is None:
                continue

            # 取最后两个时间窗口作为分析范围
            time_window = {}
            if n_windows >= 2:
                time_window = {"start": windows[0], "end": windows[-1]}

            # 构建趋势点列表
            trend_points = []
            for i, w in enumerate(windows):
                from agents.agent1.skill_evolution.schemas import TrendPoint
                trend_points.append(TrendPoint(
                    period=w,
                    frequency=freq_list[i] if i < len(freq_list) else 0.0,
                    record_count=0,
                ))

            suggestion = SkillChangeSuggestion(
                position_name=trend.position_name,
                skill_name=skill_name,
                change_type=change_type,
                trend_score=round(trend_score, 4),
                frequency_before=round(freq_before, 4),
                frequency_after=round(freq_after, 4),
                time_window=time_window,
                trend_points=trend_points,
                sample_jds=trend.sample_jds.get(skill_name, []),
                suggestion=self._suggestion_for_type(change_type),
                cross_domain_flag=False,
                confidence=self._compute_confidence(trend_score, trend.total_records),
                provenance={"total_records": trend.total_records, "windows": len(windows)},
            )
            suggestions.append(suggestion)

        return suggestions

    def _classify_change(self, trend_score: float,
                          freq_before: float,
                          freq_after: float,
                          n_windows: int) -> str | None:
        """分类技能变化类型"""
        if freq_before <= 0.01 and freq_after >= 0.05:
            return "new"
        if freq_before >= 0.05 and freq_after <= 0.01:
            return "dying"
        if trend_score >= self.rising_threshold:
            return "rising"
        if trend_score <= self.declining_threshold:
            return "declining"
        return None

    def _suggestion_for_type(self, change_type: str) -> str:
        """根据变化类型输出建议"""
        suggestions = {
            "new": "新出现的热门技能，建议加入岗位必需技能列表",
            "dying": "技能需求显著下降，建议从必需技能中移除或降级为加分技能",
            "rising": "技能需求持续上升，建议关注并考虑升级为必需技能",
            "declining": "技能需求持续下降，建议关注趋势并预备调整",
        }
        return suggestions.get(change_type, "请关注趋势变化")

    def _compute_confidence(self, trend_score: float,
                             total_records: int) -> float:
        """计算演化检测的置信度"""
        # 基于趋势幅度和数据量
        magnitude = min(abs(trend_score) * 2, 1.0)
        size_factor = min(total_records / 100, 1.0)
        confidence = 0.3 + 0.4 * magnitude + 0.3 * size_factor
        return round(min(confidence, 1.0), 4)

    def _detect_cross_domain(self, suggestions: list[SkillChangeSuggestion]) -> list[dict]:
        """检测跨领域迁移：一项技能在多个不同岗位中同时升温"""
        skill_positions = defaultdict(list)
        for s in suggestions:
            if s.change_type in ("new", "rising"):
                skill_positions[s.skill_name].append(s.position_name)

        cross_domain = []
        for skill_name, positions in skill_positions.items():
            if len(set(positions)) >= 2:
                for pos in positions:
                    cross_domain.append({
                        "skill_name": skill_name,
                        "position_name": pos,
                        "domains": positions,
                    })
        return cross_domain
