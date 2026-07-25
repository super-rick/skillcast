import json

from skillcast.ir import SkillIR


def generate_codex(ir: SkillIR) -> str:
    config: dict = {
        "name": ir.name,
        "description": ir.description,
        "instructions": ir.instructions,
        "tags": ir.tags,
    }
    if ir.version:
        config["version"] = ir.version
    if ir.author:
        config["author"] = ir.author
    if ir.tools:
        config["tools"] = ir.tools
    if ir.model:
        config["model"] = ir.model
    if ir.metadata:
        config["metadata"] = ir.metadata

    return json.dumps(config, indent=2, ensure_ascii=False) + "\n"
