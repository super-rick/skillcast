# SkillCast

**Write Skills once, deliver everywhere.** — A universal Skill format converter for AI agent platforms.

[![PyPI](https://img.shields.io/pypi/v/skillcast)](https://pypi.org/project/skillcast/)
[![Python](https://img.shields.io/pypi/pyversions/skillcast)](https://pypi.org/project/skillcast/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Installation

```bash
pip install skillcast
```

## Quick Start

```bash
# Create a new Skill template
skillcast init my-skill

# Edit the generated YAML file with your instructions...
vim my-skill.yaml

# Convert to all supported platforms
skillcast convert my-skill.yaml --all

# Or convert to a specific target
skillcast convert my-skill.yaml --to claude
```

## Supported Platforms

| Platform | Input | Output |
|----------|-------|--------|
| Claude Code | `SKILL.md` (YAML frontmatter) | `SKILL.md` |
| Hermes | `SKILL.md` (with hermes metadata) | `SKILL.md` |
| Cursor | `.cursorrules` (plain text) | `.cursorrules` |
| Codex CLI | — (via generic YAML) | JSON config |
| Generic | YAML / JSON | — |

## CLI Reference

```
skillcast list                    List supported input/output formats
skillcast init <name>             Create a new Skill template
skillcast convert <file> --all    Convert to all target platforms
skillcast convert <file> --to <fmt>  Convert to a single platform
```

## Library Usage

```python
from skillcast import parse_skill, generate, generate_all

# Parse any Skill file
ir = parse_skill("my-skill.yaml")

# Generate for a specific platform
claude_output = generate(ir, "claude")

# Generate for all platforms
outputs = generate_all(ir)
```

## Architecture

```
Parser → IR (SkillIR dataclass) → Generator
```

Each platform has an isolated Parser and Generator, operating on a shared normalized intermediate representation.

## License

MIT — see [LICENSE](LICENSE)
