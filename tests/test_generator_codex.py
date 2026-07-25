import json
from skillcast.ir import SkillIR
from skillcast.generator.codex import generate_codex


class TestGenerateCodex:
    def sample_ir(self):
        return SkillIR(
            name="my-skill",
            description="A test skill",
            instructions="Do the thing.",
            tags=["test"],
            tools=["terminal"],
            model="claude-sonnet-4",
        )

    def test_generates_json_config(self):
        result = generate_codex(self.sample_ir())
        data = json.loads(result)
        assert data["name"] == "my-skill"
        assert data["description"] == "A test skill"
        assert "Do the thing." in data["instructions"]
        assert data["tags"] == ["test"]
        assert data["tools"] == ["terminal"]

    def test_output_is_valid_json(self):
        result = generate_codex(self.sample_ir())
        parsed = json.loads(result)
        assert isinstance(parsed, dict)
