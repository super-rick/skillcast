from pathlib import Path

from skillcast.ir import SkillIR, validate_ir
from skillcast.parser.claude import _parse_frontmatter


def parse_hermes(filepath: Path) -> SkillIR:
    """Parse a Hermes SKILL.md (frontmatter with metadata.hermes) into SkillIR."""
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    content = filepath.read_text(encoding="utf-8")
    fm, body = _parse_frontmatter(content)

    ir = SkillIR(
        name=fm.get("name", ""),
        description=fm.get("description", ""),
        instructions=body,
        tags=fm.get("tags", []),
        version=fm.get("version"),
        author=fm.get("author"),
        license=fm.get("license"),
        tools=fm.get("tools"),
        model=fm.get("model"),
        metadata=fm.get("metadata", {}),
    )
    validate_ir(ir)
    return ir
