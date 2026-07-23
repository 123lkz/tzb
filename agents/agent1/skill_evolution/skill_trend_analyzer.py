"""SkillTrendAnalyzer — 技能趋势分析

职责：按岗位分组，分析技能在时间序列上的出现频次变化。
"""
from collections import defaultdict
from datetime import datetime, timedelta
from loguru import logger

from agents.agent1.config import TREND_WINDOW_MONTHS, TREND_MIN_RECORDS
from agents.agent1.skill_evolution.schemas import PositionSkillTrend, TrendPoint


class SkillTrendAnalyzer:
    """分析技能在特定岗位中的出现频次趋势"""

    def __init__(self, window_months: int = TREND_WINDOW_MONTHS,
                 min_records: int = TREND_MIN_RECORDS):
        self.window_months = window_months
        self.min_records = min_records
        logger.info(f"SkillTrendAnalyzer: window_months={window_months}, min_records={min_records}")

    def _normalize_position_name(self, title: str) -> str:
        """归一化岗位名称"""
        import re
        cleaned = re.sub(r"[（\(].*?[\)）]", "", title)
        cleaned = re.sub(r"实习|初级|高级|资深|专家|助理", "", cleaned)
        return cleaned.strip()

    def _extract_period(self, pub_date: str, granularity: str = "quarter") -> str:
        """从发布日期提取时间窗口标识

        Args:
            pub_date: 发布日期字符串（多种格式兼容）
            granularity: "month" 或 "quarter"

        Returns:
            时间窗口标识，如 "2026-Q1" 或 "2026-07"
        """
        dt = self._parse_date(pub_date)
        if dt is None:
            return "unknown"
        if granularity == "month":
            return dt.strftime("%Y-%m")
        # quarter
        quarter = (dt.month - 1) // 3 + 1
        return f"{dt.year}-Q{quarter}"

    def _parse_date(self, date_str: str):
        """尝试多种格式解析日期"""
        if not date_str:
            return None
        formats = [
            "%Y-%m-%d", "%Y/%m/%d", "%Y-%m", "%Y/%m",
            "%Y.%m.%d", "%Y.%m", "%Y年%m月%d日",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except (ValueError, TypeError):
                continue
        return None

    def _collect_skills(self, record: dict) -> list[str]:
        """从记录中提取技能列表（多种格式兼容）"""
        skills = record.get("skills", [])
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",")]
        elif not isinstance(skills, list):
            skills = []
        return [s for s in skills if s]

    def analyze(self, records: list[dict]) -> list[PositionSkillTrend]:
        """分析所有记录，返回按岗位分组的趋势数据

        Args:
            records: jobs_clean 格式的记录列表

        Returns:
            list[PositionSkillTrend]: 每个岗位的趋势分析结果
        """
        # 1. 按岗位分组
        grouped = defaultdict(list)
        for r in records:
            title = r.get("title", "")
            pos_name = self._normalize_position_name(title)
            if pos_name:
                grouped[pos_name].append(r)

        logger.info(f"岗位分组完成: {len(grouped)} 个归一化岗位, 共 {len(records)} 条记录")

        # 2. 对每个岗位进行趋势分析
        results = []
        for pos_name, pos_records in grouped.items():
            if len(pos_records) < self.min_records:
                continue  # 样本太少，不分析

            trend = self._analyze_single_position(pos_name, pos_records)
            results.append(trend)

        logger.info(f"趋势分析完成: {len(results)} 个岗位满足最低记录数要求")
        return results

    def _analyze_single_position(self, pos_name: str,
                                  records: list[dict]) -> PositionSkillTrend:
        """分析单个岗位的技能趋势"""
        # 提取所有时间窗口
        periods = set()
        for r in records:
            period = self._extract_period(r.get("pub_date", ""))
            if period != "unknown":
                periods.add(period)

        sorted_periods = sorted(periods)
        if not sorted_periods:
            sorted_periods = ["unknown"]
            for r in records:
                r["_period"] = "unknown"
        else:
            for r in records:
                period = self._extract_period(r.get("pub_date", ""))
                r["_period"] = period if period != "unknown" else sorted_periods[0]

        # 统计每个时间窗口内各技能的出现频次
        skill_freq = defaultdict(lambda: defaultdict(int))
        period_counts = defaultdict(int)

        for r in records:
            period = r["_period"]
            period_counts[period] += 1
            for skill in self._collect_skills(r):
                skill_freq[skill][period] += 1

        # 构建 skill_frequencies 字典和 sample_jds
        skill_frequencies = {}
        sample_jds = {}
        for skill, period_data in skill_freq.items():
            freq_list = []
            for p in sorted_periods:
                count = period_data.get(p, 0)
                total = max(period_counts.get(p, 1), 1)
                freq_list.append(count / total)
            skill_frequencies[skill] = freq_list

            # 收集出现该技能的 JD 片段
            skill_samples = []
            for r in records:
                if skill in self._collect_skills(r):
                    desc = r.get("description", "")[:150]
                    if desc:
                        skill_samples.append(desc)
            sample_jds[skill] = skill_samples[:3]

        # 构建趋势点列表
        trend_points = []
        for p in sorted_periods:
            trend_points.append(TrendPoint(
                period=p,
                frequency=0.0,
                record_count=period_counts.get(p, 0),
            ))

        return PositionSkillTrend(
            position_name=pos_name,
            total_records=len(records),
            time_windows=sorted_periods,
            skill_frequencies=skill_frequencies,
            sample_jds=sample_jds,
        )
