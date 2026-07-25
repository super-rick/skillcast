# SkillCast: Write AI agent Skills once, deliver everywhere

**TL;DR:** A Python CLI/library that converts Skill definitions between Claude Code, Cursor, Hermes, and Codex CLI. `pip install skillcast`. Open source, MIT.

## The Problem

Every AI coding agent has its own Skill format:

- **Claude Code** uses YAML frontmatter in `SKILL.md`
- **Cursor** uses plain text `.cursorrules`
- **Hermes** uses `SKILL.md` with a metadata block
- **Codex CLI** uses a JSON config

If you maintain skills for multiple tools, you're copy-pasting the same instructions into different formats. It's the Babel problem — but for AI agent Skills.

## What SkillCast Does

```
1 Skill definition → skillcast → 4 platform-native files
```

```bash
pip install skillcast

# Write once
skillcast init java-interview
vim java-interview.yaml  # your instructions here

# Deliver everywhere
skillcast convert java-interview.yaml --all
# → java-interview.claude.md
# → java-interview.hermes.md
# → java-interview.cursor.cursorrules
# → java-interview.codex.json
```

## Architecture

```
Parser → IR (normalized) → Generator
```

4 input formats, 4 output formats. Each platform is isolated — a format change in one never breaks another. Also works as a library:

```python
from skillcast import parse_skill, generate
ir = parse_skill("my-skill.yaml")
print(generate(ir, "cursor"))  # → .cursorrules output
```

## Why Python?

Unlike the TS/JS alternatives, SkillCast has **one dependency** (pyyaml), **zero compile step**, and works via `uvx skillcast` without install.

- **GitHub:** https://github.com/super-rick/skillcast
- **PyPI:** https://pypi.org/project/skillcast/
- **License:** MIT

Would love feedback — what platforms should I add next? (Windsurf? Aider? Cline?)

---

*For r/CursorAI and r/ClaudeAI:*

**Title:** Tool to convert Cursor rules ↔ Claude Skills ↔ Hermes

I got tired of maintaining the same AI instructions in 4 different formats, so I built SkillCast — a Python tool that converts between all of them.

```bash
pip install skillcast  # or uvx skillcast
skillcast convert my-rules.cursorrules --to claude
skillcast convert my-skill.md --to cursor
skillcast convert my-skill.yaml --all  # output all 4 platforms
```

Also works if you just want to share your `.cursorrules` with Claude users (and vice versa). Free, MIT, 1 dependency.

https://github.com/super-rick/skillcast

---
*For Hacker News:*

**Title:** Show HN: SkillCast — one Skill file → all AI coding agent formats

---

*For Twitter/X:*

🔥 Just shipped SkillCast — write AI agent skills once, convert to Claude / Cursor / Hermes / Codex automatically.

`pip install skillcast` → `skillcast convert my-skill.yaml --all` → done.

Python, MIT, 1 dep. GitHub: https://github.com/super-rick/skillcast
