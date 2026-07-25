import skillcast
import pytest
from skillcast.ir import SkillIR, validate_ir, SkillIRValidationError


class TestPackage:
    def test_version_is_set(self):
        assert skillcast.__version__
        assert isinstance(skillcast.__version__, str)
        major, minor, patch = skillcast.__version__.split(".")
        assert int(major) >= 0
        assert int(minor) >= 0
        assert int(patch) >= 0


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
