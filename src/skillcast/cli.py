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
