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
