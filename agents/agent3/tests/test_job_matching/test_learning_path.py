
from agents.agent3.job_matching.schemas import LearningStep, LearningPath
from agents.agent3.job_matching.learning_path_generator import LearningPathGenerator
from agents.agent2.nlp_profile.schemas import SkillProfile

class TestLearningPathGenerator:
    def test_generate_with_rules_no_profile(self):
        gen = LearningPathGenerator(llm_client=None)
        path = gen._generate_with_rules("Python")
        assert path.skill_name == "Python"
        assert len(path.steps) == 4
        assert "Foundation" in path.steps[0].stage
        assert "Beginner" in path.steps[1].stage
        assert "Practice" in path.steps[2].stage
        assert "Project" in path.steps[3].stage

    def test_generate_with_rules_with_profile(self):
        sp = SkillProfile(
            skill_id="SK001", name="Python", category="Language",
            summary="Python is a versatile programming language",
            prerequisites=["Basic computer knowledge"],
            related_technologies=["Django", "FastAPI", "NumPy"],
            typical_applications=["Web development", "Data science"],
        )
        gen = LearningPathGenerator(llm_client=None)
        path = gen._generate_with_rules("Python", sp)
        assert "Basic computer knowledge" in path.steps[0].description
        assert len(path.steps[2].resources) > 0

    def test_generate_with_rules_empty_profile(self):
        sp = SkillProfile(skill_id="SK002", name="Go", summary="")
        gen = LearningPathGenerator(llm_client=None)
        path = gen._generate_with_rules("Go", sp)
        assert len(path.steps) == 4

    def test_learning_step_model(self):
        step = LearningStep(stage="Foundation", description="Learn basics", duration="2 weeks", resources=["Book A"])
        assert step.stage == "Foundation"
        assert step.duration == "2 weeks"

    def test_learning_path_model(self):
        steps = [LearningStep(stage="Foundation", description="Basics", duration="2w"), LearningStep(stage="Beginner", description="Tutorials", duration="2w")]
        path = LearningPath(skill_name="Python", steps=steps)
        assert path.skill_name == "Python"
        assert len(path.steps) == 2

    def test_learning_path_serialization(self):
        steps = [LearningStep(stage="Practice", description="Build projects")]
        path = LearningPath(skill_name="PyTorch", steps=steps)
        data = path.model_dump()
        assert data["skill_name"] == "PyTorch"
        assert len(data["steps"]) == 1

    def test_gap_item_with_learning_path(self):
        from agents.agent3.job_matching.schemas import GapItem
        path = LearningPath(skill_name="Docker", steps=[LearningStep(stage="Foundation", description="Container basics")])
        gap = GapItem(skill_name="Docker", importance="high", reason="Required", suggestion="Learn it", learning_path=path)
        assert gap.learning_path is not None
        assert gap.learning_path.skill_name == "Docker"

    def test_format_skill_profile(self):
        sp = SkillProfile(skill_id="SK003", name="FastAPI", category="Web", summary="Modern web framework", prerequisites=["Python"])
        gen = LearningPathGenerator(llm_client=None)
        text = gen._format_skill_profile("FastAPI", sp)
        assert "FastAPI" in text
        assert "Python" in text
