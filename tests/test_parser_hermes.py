from pathlib import Path
import pytest
from skillcast.parser.hermes import parse_hermes

FIXTURES = Path(__file__).parent / "fixtures"


class TestParseHermes:
    def test_parses_hermes_skill(self):
        result = parse_hermes(FIXTURES / "hermes-skill.md")
        assert result.name == "java-interview"
        assert "Java technical interviews" in result.description
        assert result.tags == ["java", "interview", "career"]
        assert result.tools == ["terminal", "web_search"]
        assert result.model == "claude-sonnet-4"
        assert result.metadata == {"hermes": {"version": "1.0"}}
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
                parse_hermes(Path(tmp))
        finally:
            os.unlink(tmp)
