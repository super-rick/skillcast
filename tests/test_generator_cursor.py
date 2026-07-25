from skillcast.ir import SkillIR
from skillcast.generator.cursor import generate_cursor


class TestGenerateCursor:
    def sample_ir(self):
        return SkillIR(
            name="my-skill",
            description="A test skill for cursor",
            instructions="You are an expert Java interviewer. Follow these steps:\n1. Ask about experience\n2. Pick questions",
            tags=["java"],
        )

    def test_generates_plain_text_instructions(self):
        result = generate_cursor(self.sample_ir())
        assert "You are an expert Java interviewer" in result
        assert "# Skill: my-skill" in result
        assert "A test skill for cursor" in result

    def test_output_is_plain_text_no_yaml(self):
        result = generate_cursor(self.sample_ir())
        assert not result.startswith("---")
