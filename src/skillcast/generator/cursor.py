from skillcast.ir import SkillIR


def generate_cursor(ir: SkillIR) -> str:
    header = f"# Skill: {ir.name}\n# {ir.description}\n\n"
    return header + ir.instructions + "\n"
