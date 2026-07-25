from pathlib import Path

from skillcast.ir import SkillIR
from skillcast.parser.generic import parse_generic
from skillcast.parser.claude import parse_claude
from skillcast.parser.hermes import parse_hermes
from skillcast.parser.cursor import parse_cursor

INPUT_FORMATS = ("generic", "claude", "hermes", "cursor")

_PARSERS = {
    "generic": parse_generic,
    "claude": parse_claude,
    "hermes": parse_hermes,
    "cursor": parse_cursor,
}


def detect_format(filepath: Path) -> str:
    """Detect the input format of a Skill file based on extension and content."""
    ext = filepath.suffix.lower()
    if ext in (".yaml", ".yml", ".json"):
        return "generic"
    if ext == ".md":
        content = filepath.read_text(encoding="utf-8")
        if "metadata:" in content[:500] and "hermes:" in content[:500]:
            return "hermes"
        return "claude"  # default for .md
    if ext in (".cursorrules",):
        return "cursor"
    raise ValueError(f"Cannot detect format for: {filepath}. Use --from to specify.")


def parse_skill(filepath: Path, fmt: str | None = None) -> SkillIR:
    """Parse a Skill file into SkillIR. Auto-detects format if fmt is None."""
    fmt = fmt or detect_format(filepath)
    parser = _PARSERS.get(fmt)
    if not parser:
        raise ValueError(f"Unsupported format: {fmt}. Supported: {', '.join(INPUT_FORMATS)}")
    return parser(filepath)
