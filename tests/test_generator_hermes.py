from skillcast.ir import SkillIR
from skillcast.generator.hermes import generate_hermes


class TestGenerateHermes:
    def sample_ir(self):
        return SkillIR(
            name="my-skill",
            description="A test skill",
            instructions="# My Skill\n\nDo the thing.",
            tags=["test"],
            metadata={"hermes": {"version": "1.0"}},
        )

    def test_generates_frontmatter_with_hermes_metadata(self):
        result = generate_hermes(self.sample_ir())
        assert result.startswith("---\n")
        assert "name: my-skill" in result
        assert "metadata:" in result
        assert "hermes:" in result
        assert "version: '1.0'" in result
        assert "---\n\n" in result
        assert "# My Skill" in result

    def test_adds_hermes_metadata_if_missing(self):
        ir = self.sample_ir()
        ir.metadata = {}
        result = generate_hermes(ir)
        assert "metadata:" in result
        assert "hermes:" in result
