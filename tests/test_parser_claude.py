from pathlib import Path
import pytest
from skillcast.parser.claude import parse_claude

FIXTURES = Path(__file__).parent / "fixtures"


class TestParseClaude:
    def test_parses_frontmatter_and_body(self):
        result = parse_claude(FIXTURES / "claude-skill.md")
        assert result.name == "java-interview"
        assert "Java technical interviews" in result.description
        assert result.tags == ["java", "interview", "career"]
        assert result.tools == ["terminal", "web_search"]
        assert result.model == "claude-sonnet-4"
        assert "# Java Interview Coach" in result.instructions
        assert "expert Java interviewer" in result.instructions

    def test_no_frontmatter_raises(self):
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# No frontmatter here\nJust body.")
            tmp = f.name
        try:
            with pytest.raises(ValueError, match="frontmatter"):
                parse_claude(Path(tmp))
        finally:
            os.unlink(tmp)

    def test_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            parse_claude(Path("/nonexistent.md"))
