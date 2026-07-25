# SkillCast

**Write Skills once, deliver everywhere.** — A universal Skill format converter for AI agent platforms.

[![PyPI](https://img.shields.io/pypi/v/skillcast)](https://pypi.org/project/skillcast/)
[![Python](https://img.shields.io/pypi/pyversions/skillcast)](https://pypi.org/project/skillcast/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/super-rick/skillcast/actions/workflows/test.yml/badge.svg)](https://github.com/super-rick/skillcast/actions/workflows/test.yml)

## Quick Demo

```console
$ pip install skillcast

$ skillcast list
📥 Input formats:
  - generic   - claude   - hermes   - cursor
📤 Output formats:
  - claude    - hermes   - cursor   - codex

$ skillcast init java-interview
✅ Created: java-interview.yaml

$ skillcast convert java-interview.yaml --all -o output
✅ Parsed: java-interview — Helps prepare for Java technical interviews
  📄 output/java-interview.claude.md
  📄 output/java-interview.hermes.md
  📄 output/java-interview.cursor.cursorrules
  📄 output/java-interview.codex.json
🎉 Done! Output in: output/

$ ls -1 output/
java-interview.claude.md
java-interview.codex.json
java-interview.cursor.cursorrules
java-interview.hermes.md
```

> 💡 Run `bash demo/demo.sh` to see the full workflow live in your terminal.

## Installation

```bash
pip install skillcast
# or zero-install:
uvx skillcast --help
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
skillcast list                          List supported input/output formats
skillcast init <name>                   Create a new Skill template
skillcast convert <file> --all          Convert to all target platforms
skillcast convert <file> --to <fmt>     Convert to a single platform
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
