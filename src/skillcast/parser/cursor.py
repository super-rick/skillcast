from pathlib import Path

from skillcast.ir import SkillIR, validate_ir


def parse_cursor(filepath: Path) -> SkillIR:
    """Parse a Cursor .cursorrules file (plain text instructions) into SkillIR."""
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    content = filepath.read_text(encoding="utf-8").strip()

    # Derive name from filename, description from first meaningful line
    name = filepath.stem or "cursor-skill"
    first_line = content.split("\n")[0].strip()
    description = first_line[:100] if first_line else "Cursor rules"

    ir = SkillIR(
        name=name,
        description=description,
        instructions=content,
        tags=[],
        metadata={"source": "cursor", "filename": filepath.name},
    )
    validate_ir(ir)
    return ir
