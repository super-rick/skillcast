from pathlib import Path
import pytest
from skillcast.parser.cursor import parse_cursor

FIXTURES = Path(__file__).parent / "fixtures"


class TestParseCursor:
    def test_parses_cursor_rules(self):
        result = parse_cursor(FIXTURES / "cursor-rules.cursorrules")
        assert result.name  # name is derived from filename or content
        assert "expert Java interviewer" in result.instructions
        assert "Ask about the candidate" in result.instructions

    def test_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            parse_cursor(Path("/nonexistent.txt"))
