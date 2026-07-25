# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: SkillCast

**"Write Skills once, deliver everywhere."** — A format converter for AI agent Skill definitions (like Babel for Skills). Parses a Skill from any platform format into a normalized IR, then generates output for any target platform.

- **Language:** Python 3.11+
- **Single dependency:** pyyaml
- **Build system:** setuptools via pyproject.toml (library + CLI in one package)
- **Test framework:** pytest
- **Linter:** ruff (line-length 120, target py311)

## Architecture

Three-layer pipe: **Parser → IR → Generator**. Each platform gets one Parser + one Generator, all operating on a shared normalized dataclass (`SkillIR`).

```
  Claude SKILL.md  ──→  claude.py (parser)   ──┐
  Hermes SKILL.md  ──→  hermes.py (parser)   ──┤
  Cursor .cursorrules → cursor.py (parser)   ──┤──→  SkillIR  ──→  generator/*.py  ──→ target format
  Generic YAML/JSON ──→ generic.py (parser)  ──┘
```

### Key modules

| Module | Role |
|--------|------|
| `skillcast.ir` | `SkillIR` dataclass + `validate_ir()`. Single source of truth for the normalized representation. |
| `skillcast.parser` | Registry (`parse_skill`, `detect_format`) + per-platform parsers: `generic.py`, `claude.py`, `hermes.py`, `cursor.py` |
| `skillcast.generator` | Registry (`generate`, `generate_all`) + per-platform generators: `claude.py`, `hermes.py`, `cursor.py`, `codex.py` |
| `skillcast.cli` | argparse CLI: `skillcast convert`, `skillcast list`, `skillcast init` |

### IR Schema

```python
@dataclass
class SkillIR:
    name: str
    description: str
    instructions: str
    tags: list[str]
    version: str | None = None
    author: str | None = None
    license: str | None = None
    tools: list[str] | None = None
    model: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
```

### Supported platforms (initial)

| Platform | Input Format | Output Format |
|----------|-------------|---------------|
| Claude Code | YAML frontmatter + markdown (`.md`) | Same |
| Hermes | YAML frontmatter with `metadata.hermes` (`.md`) | Same |
| Cursor | `.cursorrules` (plain text) | `.cursorrules` |
| Codex CLI | N/A (input via generic YAML) | JSON config |
| Generic | YAML or JSON | N/A |

## Commands

```bash
# Install in dev mode
pip install -e ".[dev]"

# Run all tests
pytest

# Run tests verbose
pytest -v

# Run a single test file
pytest tests/test_ir.py -v

# Lint
ruff check src/

# Build for PyPI
python -m build

# CLI (after install)
skillcast list                              # list supported formats
skillcast init my-skill                     # create template
skillcast convert my-skill.yaml --all       # convert to all platforms
skillcast convert my-skill.yaml --to claude # convert to single platform
```

## Project structure

```
skillcast/
├── src/skillcast/
│   ├── __init__.py          # public API
│   ├── cli.py               # argparse CLI
│   ├── ir.py                # SkillIR + validate_ir
│   ├── parser/              # parsers: generic, claude, hermes, cursor
│   └── generator/           # generators: claude, hermes, cursor, codex
├── tests/
│   ├── fixtures/            # sample skill files per format
│   └── test_*.py
├── pyproject.toml
└── README.md
```

## Implementation plan

The full task-by-task implementation plan is in `plan/2026-07-25_skillcast-oss-plan.md`. Development follows TDD: write the test first (RED), implement (GREEN), then commit. Each phase commits independently.

## Design decisions

- **Python over TypeScript** — fewer dependencies (1 vs 6), no compile step, simpler config (single pyproject.toml vs tsconfig + jest + package.json)
- **Parser/Generator per platform** — each platform format is isolated; a format change in one platform never breaks another
- **Generic YAML as the canonical authoring format** — platform-agnostic, human-readable, easy to template with `skillcast init`
- **Library + CLI in one package** — `pip install skillcast` gives both `skillcast convert` and `from skillcast import parse_skill, generate`

## Repository

- GitHub: `github.com/super-rick/skillcast`
- License: MIT
