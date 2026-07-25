"""SkillCast — Write Skills once, deliver everywhere."""

from importlib.metadata import version as _version

from skillcast.ir import SkillIR, SkillIRValidationError, validate_ir
from skillcast.parser import detect_format, parse_skill, INPUT_FORMATS
from skillcast.generator import generate, generate_all, file_extension, OUTPUT_FORMATS

__version__ = _version("skillcast")

__all__ = [
    "SkillIR",
    "SkillIRValidationError",
    "validate_ir",
    "parse_skill",
    "detect_format",
    "generate",
    "generate_all",
    "file_extension",
    "INPUT_FORMATS",
    "OUTPUT_FORMATS",
    "__version__",
]
