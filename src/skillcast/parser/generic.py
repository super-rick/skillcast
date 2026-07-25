import json
from pathlib import Path

import yaml

from skillcast.ir import SkillIR, validate_ir


def parse_generic(filepath: Path) -> SkillIR:
    """Parse a generic YAML or JSON Skill file into SkillIR."""
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    content = filepath.read_text(encoding="utf-8")
    ext = filepath.suffix.lower()

    if ext == ".json":
        data = json.loads(content)
    elif ext in (".yaml", ".yml"):
        data = yaml.safe_load(content)
    else:
        raise ValueError(f"Unsupported format: {ext}. Use .yaml, .yml, or .json")

    ir = SkillIR(
        name=data.get("name", ""),
        description=data.get("description", ""),
        instructions=data.get("instructions", ""),
        tags=data.get("tags", []),
        version=data.get("version"),
        author=data.get("author"),
        license=data.get("license"),
        tools=data.get("tools"),
        model=data.get("model"),
        metadata=data.get("metadata", {}),
    )
    validate_ir(ir)
    return ir
