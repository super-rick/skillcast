# SkillCast 开源项目实现计划

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 构建 SkillCast CLI/库——一份 Skill 定义 → 多平台输出的格式转换器（Skill 格式的 Babel），PyPI 发布，GitHub 开源。

**Architecture:** Parser → IR（中间表示）→ Generator 三层。每个平台一个 Parser + Generator，IR 做归一化。Python 单项目，`pyyaml` 唯一依赖，`pyproject.toml` 同时提供 CLI + 库。

**Tech Stack:** Python 3.11+, pyyaml, pytest, pyproject.toml (setuptools)

**Initial Platforms:** Claude Code, Hermes, Cursor, Codex CLI

**Repository:** github.com/super-rick/skillcast

---

## 项目定位

```
SkillCast = 一份 Skill，投送到所有平台
pip install skillcast
skillcast convert my-skill.yaml --all
```

**叙事：** "I write Skills once. SkillCast delivers them everywhere."

---

## 架构总览

```
                  ┌──────────────┐
  Claude SKILL.md →│              │
  Hermes SKILL.md →│   PARSER     │→ IR (dataclass)
  Generic YAML   →│              │
                  └──────────────┘
                          │
                          ▼
                  ┌──────────────┐
                  │      IR      │
                  │ (normalized) │
                  └──────────────┘
                          │
                          ▼
                  ┌──────────────┐
        IR →      │  GENERATOR   │→ Claude SKILL.md
                  │              │→ Hermes SKILL.md
                  │              │→ Cursor .cursorrules
                  │              │→ Codex config
                  └──────────────┘
```

### IR Schema

```python
@dataclass
class SkillIR:
    name: str
    description: str
    instructions: str
    tags: list[str] = field(default_factory=list)
    version: str | None = None
    author: str | None = None
    license: str | None = None
    tools: list[str] | None = None
    model: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
```

---

## 文件结构

```
skillcast/
├── src/
│   └── skillcast/
│       ├── __init__.py          # 暴露公共 API
│       ├── cli.py               # CLI 入口 (argparse)
│       ├── ir.py                # IR dataclass + validate
│       ├── parser/
│       │   ├── __init__.py      # Parser 注册表 + detect()
│       │   ├── generic.py       # Generic YAML/JSON → IR
│       │   ├── claude.py        # Claude SKILL.md → IR
│       │   ├── hermes.py        # Hermes SKILL.md → IR
│       │   └── cursor.py        # Cursor .cursorrules → IR
│       └── generator/
│           ├── __init__.py      # Generator 注册表
│           ├── claude.py        # IR → Claude SKILL.md
│           ├── hermes.py        # IR → Hermes SKILL.md
│           ├── cursor.py        # IR → Cursor .cursorrules
│           └── codex.py         # IR → Codex config
├── tests/
│   ├── test_ir.py
│   ├── test_parser_generic.py
│   ├── test_parser_claude.py
│   ├── test_parser_hermes.py
│   ├── test_generator_claude.py
│   ├── test_generator_hermes.py
│   ├── test_generator_cursor.py
│   ├── test_generator_codex.py
│   ├── test_cli.py
│   └── fixtures/
│       ├── generic-skill.yaml
│       ├── claude-skill.md
│       ├── hermes-skill.md
│       └── cursor-rules.txt
├── pyproject.toml
├── .gitignore
├── LICENSE
└── README.md
```

---

## Phase 1: 项目骨架（15 min）

### Task 1: 初始化项目 + pyproject.toml

**Objective:** 创建项目结构，一个 pyproject.toml 同时定义库 + CLI

**Files:**
- Create: `skillcast/pyproject.toml`
- Create: `skillcast/.gitignore`

**Step 1: 创建目录**

```bash
mkdir -p ~/projects/skillcast/src/skillcast/parser
mkdir -p ~/projects/skillcast/src/skillcast/generator
mkdir -p ~/projects/skillcast/tests/fixtures
cd ~/projects/skillcast
git init
```

**Step 2: 创建 pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=75", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "skillcast"
version = "0.1.0"
description = "Write Skills once, deliver everywhere. Universal Skill format converter."
requires-python = ">=3.11"
dependencies = ["pyyaml"]
license = {text = "MIT"}
authors = [{name = "Rick", email = "super-rick@github"}]
keywords = ["skill", "claude", "cursor", "hermes", "codex", "agent", "ai", "converter"]
readme = "README.md"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]

[project.urls]
Homepage = "https://github.com/super-rick/skillcast"
Repository = "https://github.com/super-rick/skillcast"

[project.scripts]
skillcast = "skillcast.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 120
target-version = "py311"
```

**Step 3: 创建 .gitignore**

```
__pycache__/
*.pyc
*.egg-info/
dist/
build/
.coverage
.pytest_cache/
.ruff_cache/
```

**Step 4: 创建占位文件 + 安装开发模式**

```bash
touch src/skillcast/__init__.py
touch src/skillcast/parser/__init__.py
touch src/skillcast/generator/__init__.py
pip install -e ".[dev]"
skillcast --help  # Should show CLI
```

**Step 5: Commit**

```bash
git add .
git commit -m "chore: init Python project with pyproject.toml"
```

---

### Task 2: 安装开发依赖 + 验证

**Objective:** pytest 可运行

```bash
pip install pytest ruff
pytest  # Should show "no tests ran" (not error)
```

---

## Phase 2: 核心 IR + Parser（TDD，~2h）

### Task 3: 实现 IR dataclass + validate

**Objective:** SkillIR dataclass + 校验函数

**Files:**
- Create: `skillcast/src/skillcast/ir.py`
- Create: `skillcast/tests/test_ir.py`

**Step 1: 写测试（RED）**

```python
# tests/test_ir.py
import pytest
from skillcast.ir import SkillIR, validate_ir, SkillIRValidationError


class TestValidateIR:
    def valid_ir(self):
        return SkillIR(
            name="my-skill",
            description="A test skill",
            instructions="Do the thing",
            tags=["test"],
        )

    def test_passes_valid_ir(self):
        validate_ir(self.valid_ir())  # no exception

    def test_raises_on_empty_name(self):
        ir = self.valid_ir()
        ir.name = ""
        with pytest.raises(SkillIRValidationError, match="name"):
            validate_ir(ir)

    def test_raises_on_empty_description(self):
        ir = self.valid_ir()
        ir.description = ""
        with pytest.raises(SkillIRValidationError, match="description"):
            validate_ir(ir)

    def test_raises_on_empty_instructions(self):
        ir = self.valid_ir()
        ir.instructions = ""
        with pytest.raises(SkillIRValidationError, match="instructions"):
            validate_ir(ir)

    def test_raises_on_non_list_tags(self):
        ir = self.valid_ir()
        ir.tags = "not-a-list"  # type: ignore
        with pytest.raises(SkillIRValidationError, match="tags"):
            validate_ir(ir)
```

**Step 2: 验证失败**

```bash
pytest tests/test_ir.py -v
# Expected: 5 failed (module not found)
```

**Step 3: 实现（GREEN）**

```python
# src/skillcast/ir.py
from dataclasses import dataclass, field
from typing import Any


class SkillIRValidationError(ValueError):
    """Raised when a SkillIR fails validation."""


@dataclass
class SkillIR:
    name: str
    description: str
    instructions: str
    tags: list[str] = field(default_factory=list)
    version: str | None = None
    author: str | None = None
    license: str | None = None
    tools: list[str] | None = None
    model: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


def validate_ir(ir: SkillIR) -> None:
    """Validate a SkillIR object. Raises SkillIRValidationError on failure."""
    if not ir.name or not ir.name.strip():
        raise SkillIRValidationError("name is required and must not be empty")
    if not ir.description or not ir.description.strip():
        raise SkillIRValidationError("description is required and must not be empty")
    if not ir.instructions or not ir.instructions.strip():
        raise SkillIRValidationError("instructions is required and must not be empty")
    if not isinstance(ir.tags, list):
        raise SkillIRValidationError("tags must be a list")
    if not isinstance(ir.metadata, dict):
        raise SkillIRValidationError("metadata must be a dict")
```

**Step 4: 验证通过**

```bash
pytest tests/test_ir.py -v
# Expected: 5 passed
```

**Step 5: Commit**

```bash
git add src/skillcast/ir.py tests/test_ir.py
git commit -m "feat: add SkillIR dataclass + validate_ir"
```

---

### Task 4: 实现 Generic YAML Parser

**Objective:** 解析通用 YAML/JSON → IR。这是 SkillCast 推荐的 Skill 编写格式。

**Files:**
- Create: `skillcast/src/skillcast/parser/generic.py`
- Create: `skillcast/tests/test_parser_generic.py`
- Create: `skillcast/tests/fixtures/generic-skill.yaml`

**Step 1: 创建 fixture**

```yaml
# tests/fixtures/generic-skill.yaml
name: java-interview
description: Helps prepare for Java technical interviews
version: "1.0.0"
author: Rick
tags:
  - java
  - interview
  - career
instructions: |
  You are an expert Java interviewer. Follow these steps:
  1. Ask about the candidate's experience level
  2. Pick questions from the pool based on level
  3. Provide detailed feedback after each answer
tools:
  - terminal
  - web_search
model: claude-sonnet-4
```

**Step 2: 写测试（RED）**

```python
# tests/test_parser_generic.py
from pathlib import Path
import pytest
from skillcast.parser.generic import parse_generic

FIXTURES = Path(__file__).parent / "fixtures"


class TestParseGeneric:
    def test_parses_yaml_fixture(self):
        result = parse_generic(FIXTURES / "generic-skill.yaml")
        assert result.name == "java-interview"
        assert result.description == "Helps prepare for Java technical interviews"
        assert result.version == "1.0.0"
        assert result.author == "Rick"
        assert result.tags == ["java", "interview", "career"]
        assert result.tools == ["terminal", "web_search"]
        assert result.model == "claude-sonnet-4"
        assert "expert Java interviewer" in result.instructions

    def test_raises_on_missing_file(self):
        with pytest.raises(FileNotFoundError):
            parse_generic(Path("/nonexistent.yaml"))

    def test_raises_on_missing_required_field(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("name: test\n")  # missing description & instructions
            tmp = f.name
        try:
            with pytest.raises(Exception):
                parse_generic(Path(tmp))
        finally:
            os.unlink(tmp)
```

**Step 3: 实现（GREEN）**

```python
# src/skillcast/parser/generic.py
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
```

**Step 4: 验证 → Commit**

```bash
pytest tests/test_parser_generic.py -v
git add src/skillcast/parser/generic.py tests/test_parser_generic.py tests/fixtures/generic-skill.yaml
git commit -m "feat: add generic YAML/JSON parser"
```

---

### Task 5: 实现 Claude SKILL.md Parser

**Objective:** 解析 Claude Code 的 YAML frontmatter + markdown body 格式

**Files:**
- Create: `skillcast/src/skillcast/parser/claude.py`
- Create: `skillcast/tests/test_parser_claude.py`
- Create: `skillcast/tests/fixtures/claude-skill.md`

**Step 1: 创建 fixture**

```markdown
---
name: java-interview
description: Helps prepare for Java technical interviews
tags: [java, interview, career]
tools: [terminal, web_search]
model: claude-sonnet-4
---

# Java Interview Coach

You are an expert Java interviewer. Follow these steps:
1. Ask about the candidate's experience level
2. Pick questions from the pool based on level
3. Provide detailed feedback after each answer
```

**Step 2: 测试**

```python
# tests/test_parser_claude.py
from pathlib import Path
from skillcast.parser.claude import parse_claude

FIXTURES = Path(__file__).parent / "fixtures"


class TestParseClaude:
    def test_parses_frontmatter_and_body(self):
        result = parse_claude(FIXTURES / "claude-skill.md")
        assert result.name == "java-interview"
        assert "Java technical interviews" in result.description
        assert result.tags == ["java", "interview", "career"]
        assert result.tools == ["terminal", "web_search"]
        assert result.model == "claude-sonnet-4"
        assert "# Java Interview Coach" in result.instructions
        assert "expert Java interviewer" in result.instructions

    def test_no_frontmatter_raises(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# No frontmatter here\nJust body.")
            tmp = f.name
        try:
            from skillcast.parser.claude import parse_claude
            with pytest.raises(ValueError, match="frontmatter"):
                parse_claude(Path(tmp))
        finally:
            os.unlink(tmp)
```

**Step 3: 实现**

```python
# src/skillcast/parser/claude.py
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
```

**Step 4: 验证 → Commit**

---

### Task 6: 实现 Hermes + Cursor Parser

**Objective:** Hermes（类似 Claude + metadata.hermes）、Cursor（纯文本 → IR 包装）

两个 parser 结构几乎相同，一起实现。

**Step: 实现 → 测试 → Commit（每个一个 task）**

---

### Task 7: 实现 Parser 注册表

**Objective:** 统一入口 `parse_skill(path, format=None)` + `detect_format(path)`

```python
# src/skillcast/parser/__init__.py
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
    ext = filepath.suffix.lower()
    if ext in (".yaml", ".yml", ".json"):
        return "generic"
    if ext == ".md":
        content = filepath.read_text(encoding="utf-8")
        if "metadata:" in content[:500] and "hermes:" in content[:500]:
            return "hermes"
        return "claude"  # default for .md
    if ext == ".cursorrules":
        return "cursor"
    raise ValueError(f"Cannot detect format for: {filepath}. Use --from to specify.")


def parse_skill(filepath: Path, fmt: str | None = None) -> SkillIR:
    fmt = fmt or detect_format(filepath)
    parser = _PARSERS.get(fmt)
    if not parser:
        raise ValueError(f"Unsupported format: {fmt}. Supported: {', '.join(INPUT_FORMATS)}")
    return parser(filepath)
```

---

## Phase 3: Generator（TDD，~1.5h）

### Task 8-12: 逐个实现 Generator

每个 Generator：`IR → platform-specific string`，~30 行代码。

```python
# src/skillcast/generator/claude.py
import yaml
from skillcast.ir import SkillIR


def generate_claude(ir: SkillIR) -> str:
    fm = {
        "name": ir.name,
        "description": ir.description,
        "tags": ir.tags,
    }
    if ir.version: fm["version"] = ir.version
    if ir.author: fm["author"] = ir.author
    if ir.tools: fm["tools"] = ir.tools
    if ir.model: fm["model"] = ir.model

    yaml_str = yaml.dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False).strip()
    return f"---\n{yaml_str}\n---\n\n{ir.instructions}\n"
```

### Task 13: Generator 注册表

```python
# src/skillcast/generator/__init__.py
from skillcast.ir import SkillIR
from skillcast.generator.claude import generate_claude
from skillcast.generator.hermes import generate_hermes
from skillcast.generator.cursor import generate_cursor
from skillcast.generator.codex import generate_codex

OUTPUT_FORMATS = ("claude", "hermes", "cursor", "codex")

_GENERATORS = {
    "claude": generate_claude,
    "hermes": generate_hermes,
    "cursor": generate_cursor,
    "codex": generate_codex,
}

EXTENSIONS = {
    "claude": ".md",
    "hermes": ".md",
    "cursor": ".cursorrules",
    "codex": ".json",
}


def generate(ir: SkillIR, fmt: str) -> str:
    gen = _GENERATORS.get(fmt)
    if not gen:
        raise ValueError(f"Unsupported format: {fmt}. Supported: {', '.join(OUTPUT_FORMATS)}")
    return gen(ir)


def generate_all(ir: SkillIR) -> dict[str, str]:
    return {fmt: generate(ir, fmt) for fmt in OUTPUT_FORMATS}


def file_extension(fmt: str) -> str:
    return EXTENSIONS.get(fmt, ".txt")
```

---

## Phase 4: CLI（~30 min）

### Task 14: 实现 CLI

**Objective:** `skillcast convert`, `skillcast list`, `skillcast init`

**Files:**
- Create: `skillcast/src/skillcast/cli.py`

```python
"""SkillCast CLI — Write Skills once, deliver everywhere."""
import argparse
import sys
from pathlib import Path
from skillcast.parser import parse_skill, INPUT_FORMATS
from skillcast.generator import generate, generate_all, OUTPUT_FORMATS, file_extension


def cmd_convert(args):
    src = Path(args.input)
    ir = parse_skill(src, args.from_)
    print(f"✅ Parsed: {ir.name} — {ir.description}")

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.all:
        results = generate_all(ir)
        for fmt, content in results.items():
            ext = file_extension(fmt)
            out_path = out_dir / f"{ir.name}.{fmt}{ext}"
            out_path.write_text(content, encoding="utf-8")
            print(f"  📄 {out_path}")
    elif args.to:
        content = generate(ir, args.to)
        ext = file_extension(args.to)
        out_path = out_dir / f"{ir.name}{ext}"
        out_path.write_text(content, encoding="utf-8")
        print(f"  📄 {out_path}")
    else:
        print("❌ Specify --to <format> or --all", file=sys.stderr)
        sys.exit(1)

    print(f"\n🎉 Done! Output in: {out_dir}")


def cmd_list(_args):
    print("📥 Input formats:")
    for f in INPUT_FORMATS:
        print(f"  - {f}")
    print("\n📤 Output formats:")
    for f in OUTPUT_FORMATS:
        print(f"  - {f}")


def cmd_init(args):
    name = args.name or "my-skill"
    template = f"""# SkillCast Skill Template
# Convert to any platform: skillcast convert {name}.yaml --all

name: {name}
description: What this Skill does (one sentence)
version: "0.1.0"
author: Your Name
tags:
  - example
instructions: |
  # {name}

  You are a helpful assistant specialized in...
  Follow these steps:
  1. First step
  2. Second step
  3. Third step
"""
    out_path = Path(args.output)
    out_path.write_text(template, encoding="utf-8")
    print(f"✅ Created: {out_path}")
    print(f"\nNext: skillcast convert {out_path} --all")


def main():
    parser = argparse.ArgumentParser(
        prog="skillcast",
        description="Write Skills once, deliver everywhere.",
    )
    sub = parser.add_subparsers(dest="command")

    # convert
    p = sub.add_parser("convert", help="Convert a Skill file to target platforms")
    p.add_argument("input", help="Input Skill file path")
    p.add_argument("--from", dest="from_", choices=INPUT_FORMATS, help="Input format (auto-detect if omitted)")
    p.add_argument("--to", choices=OUTPUT_FORMATS, help="Output format")
    p.add_argument("--all", action="store_true", help="Generate for all output formats")
    p.add_argument("-o", "--output", default="output", help="Output directory (default: ./output)")

    # list
    sub.add_parser("list", help="List supported formats")

    # init
    p = sub.add_parser("init", help="Create a new Skill template")
    p.add_argument("name", nargs="?", default="my-skill", help="Skill name")
    p.add_argument("-o", "--output", default="skill.yaml", help="Output file path")

    args = parser.parse_args()

    if args.command == "convert":
        cmd_convert(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "init":
        cmd_init(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

**Step: 测试 CLI**

```bash
skillcast list
skillcast init java-interview
skillcast convert java-interview.yaml --all
```

---

## Phase 5: 发布（~30 min）

### Task 15: README + LICENSE

```bash
# MIT License
curl -o LICENSE https://raw.githubusercontent.com/licenses/license-templates/master/templates/mit.txt
```

README 内容：Badge + 一句话 + 安装 + Quick Start + 平台表 + CLI 参考 + Roadmap。

### Task 16: 构建 + 发布到 PyPI

```bash
pip install build twine
python -m build
twine upload dist/*
```

### Task 17: GitHub 仓库 + CI

```yaml
# .github/workflows/test.yml
name: test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: pytest -v
```

---

## 时间预估

| Phase | 内容 | 预估 |
|:------|:-----|:-----|
| Phase 1 | 项目骨架 | 15 min |
| Phase 2 | IR + 4 Parsers + 注册表 | 2 h |
| Phase 3 | 4 Generators + 注册表 | 1.5 h |
| Phase 4 | CLI (3 commands) | 30 min |
| Phase 5 | README + 发布 | 30 min |
| **Total** | **~17 tasks** | **~4.5 h** |

比 TypeScript 方案少了一半——没有 tsc 编译、没有 jest 配置、依赖从 6 个降到 1 个。

---

## 与 TypeScript 方案对比

| | TypeScript（旧） | Python（新） |
|:--|:--|:--|
| 依赖 | 6 个 npm 包 | **1 个**（pyyaml） |
| 配置文件 | tsconfig + jest.config + package.json | **1 个**（pyproject.toml） |
| 编译步骤 | tsc → dist/ | **无** |
| 代码量 | ~500 行 + 配置样板 | **~400 行**全业务 |
| 零安装体验 | `npx skillcast` | `pipx run skillcast` 或 `uvx skillcast` |
| 开发体验 | `tsx src/cli.ts` | 直接 `python -m skillcast.cli` |
| 你的熟练度 | 中等 | **主语言** |
| 预估时间 | ~8 h | **~4.5 h** |

---

## 后续路线

```
v0.1 CLI + 库 → v0.2 Web 在线转换器 (skillcast.dev) → v0.3 社区索引 → v1.0 MCP Skill Registry 联动
```

### 关键里程碑

- **开源发布帖子标题**："SkillCast: Write AI agent Skills once, deliver to Claude / Cursor / Hermes / Codex"
- **差异化**：唯一用 Python 实现的跨平台 Skill 转换器（竞品几乎全是 TS/JS）
- **引流品定位**：免费开源 → 用户 → 后续 MCP Skill Registry 的内容来源

---

## 风险

| 风险 | 缓解 |
|:-----|:-----|
| 平台格式变化 | 每个格式独立的 Parser/Generator，改一个不影响其他的；fixture 驱动测试 |
| pyyaml 不够用 | 就一个 YAML 解析需求，pyyaml 是 Python 生态最稳的库 |
| 社区不感兴趣 | 先在 agentcrew-mcn 用起来，写实战博客，发 HN/Reddit/r/Python |
| 竞品 `skillport` (405⭐) | 他们用 TS，我们用 Python——差异化。而且概念不完全一样 |

---

## 验证清单

- [ ] `pip install skillcast` 安装成功
- [ ] `skillcast list` 列出 4 个输入格式 + 4 个输出格式
- [ ] `skillcast init test-skill` 生成模板
- [ ] `skillcast convert test-skill.yaml --all` 生成 4 个平台文件
- [ ] 生成的 Claude SKILL.md 可被 Claude Code 正确加载
- [ ] 生成的 Hermes SKILL.md 可被 Hermes 正确加载
- [ ] `pytest` 全部通过，覆盖率 > 80%
- [ ] `from skillcast import parse_skill, generate` 可作为库使用
