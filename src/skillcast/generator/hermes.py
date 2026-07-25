import yaml

from skillcast.ir import SkillIR


def generate_hermes(ir: SkillIR) -> str:
    fm: dict = {
        "name": ir.name,
        "description": ir.description,
        "tags": ir.tags,
    }
    if ir.version:
        fm["version"] = ir.version
    if ir.author:
        fm["author"] = ir.author
    if ir.tools:
        fm["tools"] = ir.tools
    if ir.model:
        fm["model"] = ir.model

    # Ensure hermes metadata is present
    metadata = ir.metadata.copy() if ir.metadata else {}
    if "hermes" not in metadata:
        metadata["hermes"] = {"version": "1.0"}
    fm["metadata"] = metadata

    yaml_str = yaml.dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=False).strip()
    return f"---\n{yaml_str}\n---\n\n{ir.instructions}\n"
