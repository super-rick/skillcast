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
    """Generate platform-specific output from a SkillIR."""
    gen = _GENERATORS.get(fmt)
    if not gen:
        raise ValueError(f"Unsupported format: {fmt}. Supported: {', '.join(OUTPUT_FORMATS)}")
    return gen(ir)


def generate_all(ir: SkillIR) -> dict[str, str]:
    """Generate output for all supported target platforms."""
    return {fmt: generate(ir, fmt) for fmt in OUTPUT_FORMATS}


def file_extension(fmt: str) -> str:
    """Return the file extension for a given output format."""
    return EXTENSIONS.get(fmt, ".txt")
