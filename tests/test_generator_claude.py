from skillcast.ir import SkillIR
from skillcast.generator.claude import generate_claude


class TestGenerateClaude:
    def sample_ir(self):
        return SkillIR(
            name="my-skill",
            description="A test skill",
            instructions="# My Skill\n\nDo the thing.",
            tags=["test"],
            tools=["terminal"],
            model="claude-sonnet-4",
        )

    def test_generates_frontmatter_and_body(self):
        result = generate_claude(self.sample_ir())
        assert result.startswith("---\n")
        assert "name: my-skill" in result
        assert "description: A test skill" in result
        assert "---\n\n" in result
        assert "# My Skill" in result
        assert "Do the thing." in result

    def test_includes_optional_fields(self):
        ir = self.sample_ir()
        ir.version = "1.0.0"
        ir.author = "Test Author"
        result = generate_claude(ir)
        assert "version: 1.0.0" in result
        assert "author: Test Author" in result

    def test_does_not_include_null_fields(self):
        ir = self.sample_ir()
        ir.version = None
        ir.author = None
        ir.tools = None
        result = generate_claude(ir)
        assert "version:" not in result
        assert "author:" not in result
        assert "tools:" not in result
