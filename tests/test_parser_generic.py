from pathlib import Path
import pytest
from skillcast.parser.generic import parse_generic

FIXTURES = Path(__file__).parent / "fixtures"


class TestParseGeneric:
    def test_parses_yaml_fixture(self):
        result = parse_generic(FIXTURES / "generic-skill.yaml")
        assert result.name == "java-interview"
        assert result.description == "Helps prepare for Java technical interviews"
        assert result.version == "1.0.0"
        assert result.author == "Rick"
        assert result.tags == ["java", "interview", "career"]
        assert result.tools == ["terminal", "web_search"]
        assert result.model == "claude-sonnet-4"
        assert "expert Java interviewer" in result.instructions

    def test_raises_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            parse_generic(Path("/nonexistent.yaml"))

    def test_raises_on_missing_required_field(self):
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("name: test\n")  # missing description & instructions
            tmp = f.name
        try:
            with pytest.raises(Exception):
                parse_generic(Path(tmp))
        finally:
            os.unlink(tmp)
