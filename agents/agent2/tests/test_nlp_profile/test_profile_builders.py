"""自然语言画像系统单元测试"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest
from agents.agent2.nlp_profile.schemas import (
    SkillProfile, PositionProfile, RelationProfile,
    EvidenceItem, RelationProvenance, ProficiencyLevels,
    CheckResult, QualityReport,
)


class TestSkillProfile:
    def test_create_skill_profile(self):
        skill = SkillProfile(
            skill_id="SK_TEST01",
            name="PyTorch",
            category="深度学习框架",
            summary="PyTorch is a deep learning framework.",
            prerequisites=["Python", "线性代数"],
            related_technologies=["TensorFlow", "CUDA"],
            typical_applications=["CV", "NLP"],
            proficiency_levels=ProficiencyLevels(
                beginner="能搭建简单网络",
                intermediate="能自定义训练流程",
                advanced="能优化CUDA kernel",
            ),
            industry_trend="需求持续增长",
            sources=["bosszhipin"],
            last_updated="2025-07-15T10:00:00",
        )
        assert skill.skill_id == "SK_TEST01"
        assert skill.name == "PyTorch"
        assert len(skill.prerequisites) == 2
        assert skill.proficiency_levels.beginner == "能搭建简单网络"

    def test_skill_profile_defaults(self):
        skill = SkillProfile(
            skill_id="SK_TEST02",
            name="Python",
            summary="A programming language.",
        )
        assert skill.category == ""
        assert skill.prerequisites == []
        assert skill.typical_applications == []

    def test_skill_profile_to_dict(self):
        skill = SkillProfile(
            skill_id="SK_TEST03",
            name="Docker",
            summary="Container platform.",
        )
        data = skill.model_dump()
        assert data["skill_id"] == "SK_TEST03"
        assert "summary" in data


class TestPositionProfile:
    def test_create_position_profile(self):
        pos = PositionProfile(
            position_id="POS_TEST01",
            name="大模型算法工程师",
            summary="负责LLM的训练和优化。",
            core_responsibilities=["模型训练", "推理优化"],
            required_skills=["Python", "PyTorch"],
            optional_skills=["Kubernetes", "vLLM"],
            industry_domain="人工智能",
            typical_salary_range="40K-80K",
            experience_level="3-5年",
            sources=["bosszhipin", "zhilian"],
            last_updated="2025-07-15",
        )
        assert pos.position_id == "POS_TEST01"
        assert "模型训练" in pos.core_responsibilities
        assert pos.typical_salary_range == "40K-80K"

    def test_position_profile_with_minimal_data(self):
        pos = PositionProfile(
            position_id="POS_TEST02",
            name="后端工程师",
            summary="负责后端开发。",
        )
        assert pos.required_skills == []


class TestRelationProfile:
    def test_create_relation_profile(self):
        relation = RelationProfile(
            relation_id="REL_TEST01",
            source_type="skill",
            source_id="SK_TEST01",
            source_name="PyTorch",
            target_type="position",
            target_id="POS_TEST01",
            target_name="大模型算法工程师",
            relation_type="requires",
            valid=True,
            confidence=0.92,
            explanation="大模型训练必须使用深度学习框架，PyTorch是主流选择。",
            evidence=[
                EvidenceItem(type="职责匹配", detail="模型训练需要PyTorch", source="bosszhipin")
            ],
            counter_evidence=[
                EvidenceItem(type="可选替代", detail="也可使用TensorFlow", source="zhilian")
            ],
            recommendation="strongly_include",
            provenance=RelationProvenance(
                created_by="agent2",
                created_at="2025-07-15T10:00:00",
                llm_model="spark-4.0",
                consensus_rounds=3,
            ),
        )
        assert relation.valid is True
        assert relation.confidence == 0.92
        assert len(relation.evidence) == 1
        assert relation.provenance.consensus_rounds == 3


class TestQualityReport:
    def test_create_quality_report(self):
        report = QualityReport(
            report_id="QR_20250715_001",
            record_id="REC_001",
            overall_score=0.85,
            check_results={
                "completeness": CheckResult(
                    checker_name="completeness",
                    passed=True, score=1.0,
                    details="所有字段完整",
                    flagged_items=[],
                ),
            },
            passed=True,
            created_at="2025-07-15T10:00:00",
        )
        assert report.overall_score == 0.85
        assert report.passed is True
        assert "completeness" in report.check_results


class TestProficiencyLevels:
    def test_create_proficiency_levels(self):
        pl = ProficiencyLevels(
            beginner="基础水平",
            intermediate="中级水平",
            advanced="高级水平",
        )
        assert pl.beginner == "基础水平"
        assert pl.advanced == "高级水平"

    def test_proficiency_levels_required_fields(self):
        with pytest.raises(Exception):
            ProficiencyLevels()
