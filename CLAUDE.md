# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: SkillCast

**"Write Skills once, deliver everywhere."** — A format converter for AI agent Skill definitions (like Babel for Skills). Parses a Skill from any platform format into a normalized IR, then generates output for any target platform.

- **Language:** Python 3.11+
- **Single dependency:** pyyaml
- **Build system:** setuptools via pyproject.toml (library + CLI in one package)
- **Test framework:** pytest
- **Linter:** ruff (line-length 120, target py311)
- **Repository:** https://github.com/super-rick/skillcast
- **PyPI:** https://pypi.org/project/skillcast/ (published v0.1.0)
- **CI:** GitHub Actions — test on 3.11, 3.12, 3.13 (push + PR)
- **SSH:** `~/.ssh/skillcast_github` (Host `github.com-skillcast` in ~/.ssh/config)

## Current Status (v0.1.0)

- **30 tests passing** (5 IR, 9 parser, 9 generator, 5 CLI, 1 version + 1 package)
- **4 input formats:** generic YAML/JSON, Claude SKILL.md, Hermes SKILL.md, Cursor .cursorrules
- **4 output formats:** Claude, Hermes, Cursor, Codex CLI
- **CLI:** `skillcast convert`, `skillcast list`, `skillcast init`
- **Library:** `from skillcast import parse_skill, generate, generate_all`
- **Zero-install:** `uvx skillcast --help` works
- **`skillcast.__version__`** exported via `importlib.metadata`

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

### Supported platforms

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
│   ├── __init__.py              # public API + __version__
│   ├── cli.py                   # argparse CLI (convert, list, init)
│   ├── ir.py                    # SkillIR + validate_ir
│   ├── parser/                  # parsers: generic, claude, hermes, cursor
│   └── generator/               # generators: claude, hermes, cursor, codex
├── tests/
│   ├── fixtures/                # sample skill files per format
│   └── test_*.py                # 30 tests total
├── demo/
│   ├── demo.sh                  # live terminal demo script
│   ├── terminalizer.yml         # config for GIF recording
│   ├── skillcast.tape           # vhs tape for GIF recording
│   └── launch-post.md           # draft posts for HN, Reddit, X
├── .github/workflows/test.yml   # CI: pytest on 3.11/3.12/3.13
├── pyproject.toml               # single config: build + CLI + pytest + ruff
├── LICENSE                      # MIT
├── README.md
└── plan/2026-07-25_skillcast-oss-plan.md
```

## Roadmap

```
v0.1 ✅ CLI + 库 (done)
  ├── Published to PyPI: pip install skillcast
  ├── 30 tests, 4 input × 4 output formats
  ├── CI: GitHub Actions
  └── zero-install: uvx skillcast

v0.2 Web converter (skillcast.dev)
  └── Browser-based: paste YAML → download platform files
       (might replace with a simple Streamlit/Gradio app first)

v0.3 Community Skill index
  └── Searchable catalog of community-contributed Skills

v1.0 MCP Skill Registry integration
  └── Connect to the emerging MCP Skill Registry ecosystem
```

## Launch Plan

Target channels and hooks:

| Channel | Hook | Post |
|---------|------|------|
| **r/ClaudeAI** | "Convert Claude Skills ↔ Cursor rules" | `demo/launch-post.md` |
| **r/CursorAI** | "Export .cursorrules to Claude/Hermes format" | `demo/launch-post.md` |
| **HN Show HN** | Tech angle: Parser→IR→Generator, 1 dep, Python | `demo/launch-post.md` |
| **X/Twitter** | One-liner + demo code block | `demo/launch-post.md` |

## Demo GIF

Recording tools were installing too slowly. To generate a GIF later:

```bash
# Option A: vhs (charmbracelet)
brew install vhs
vhs demo/skillcast.tape    # → demo/skillcast-demo.gif

# Option B: terminalizer
npm install -g terminalizer
terminalizer record demo/skillcast -c demo/terminalizer.yml
terminalizer render demo/skillcast
```

Once GIF is generated, add to README: `![demo](demo/skillcast-demo.gif)`

## Design decisions

- **Python over TypeScript** — fewer dependencies (1 vs 6), no compile step, simpler config (single pyproject.toml vs tsconfig + jest + package.json)
- **Parser/Generator per platform** — each platform format is isolated; a format change in one platform never breaks another
- **Generic YAML as the canonical authoring format** — platform-agnostic, human-readable, easy to template with `skillcast init`
- **Library + CLI in one package** — `pip install skillcast` gives both `skillcast convert` and `from skillcast import parse_skill, generate`
- **TDD workflow** — write test first (RED), implement (GREEN), commit. Each commit is self-contained.
