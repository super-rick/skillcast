import re
from pathlib import Path

import yaml

from skillcast.ir import SkillIR, validate_ir

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)", re.DOTALL)


def _parse_frontmatter(content: str) -> tuple[dict, str]:
    m = _FRONTMATTER_RE.match(content)
    if not m:
        raise ValueError("No YAML frontmatter found. Expected: ---\\n...\\n---")
    fm = yaml.safe_load(m.group(1)) or {}
    body = m.group(2).strip()
    return fm, body


def parse_claude(filepath: Path) -> SkillIR:
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
