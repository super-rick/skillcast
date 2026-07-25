import tempfile
import os
from pathlib import Path
import pytest
from skillcast.cli import main


class TestCLIList:
    def test_list_outputs_formats(self, capsys):
        import sys
        sys.argv = ["skillcast", "list"]
        try:
            main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        assert "Input formats" in captured.out
        assert "generic" in captured.out
        assert "claude" in captured.out
        assert "Output formats" in captured.out
        assert "codex" in captured.out


class TestCLIInit:
    def test_init_creates_template(self, tmp_path):
        out_file = tmp_path / "test-skill.yaml"
        import sys
        sys.argv = ["skillcast", "init", "test-skill", "-o", str(out_file)]
        try:
            main()
        except SystemExit:
            pass
        assert out_file.exists()
        content = out_file.read_text()
        assert "name: test-skill" in content
        assert "instructions:" in content

    def test_init_default_name(self, tmp_path):
        out_file = tmp_path / "skill.yaml"
        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            import sys
            sys.argv = ["skillcast", "init"]
            try:
                main()
            except SystemExit:
                pass
            assert out_file.exists()
            assert "name: my-skill" in out_file.read_text()
        finally:
            os.chdir(old_cwd)


class TestCLIConvert:
    def test_convert_to_single_format(self, tmp_path):
        fixture = Path(__file__).parent / "fixtures" / "generic-skill.yaml"
        out_dir = tmp_path / "output"
        import sys
        sys.argv = [
            "skillcast", "convert", str(fixture),
            "--to", "claude",
            "-o", str(out_dir),
        ]
        try:
            main()
        except SystemExit:
            pass
        # Check output file exists
        files = list(out_dir.glob("*.md"))
        assert len(files) == 1
        content = files[0].read_text()
        assert "java-interview" in content
        assert "# Java Interview Coach" not in content  # claude output has frontmatter, not original body — but wait, Claude output has instructions

    def test_convert_all_formats(self, tmp_path):
        fixture = Path(__file__).parent / "fixtures" / "generic-skill.yaml"
        out_dir = tmp_path / "output"
        import sys
        sys.argv = [
            "skillcast", "convert", str(fixture),
            "--all",
            "-o", str(out_dir),
        ]
        try:
            main()
        except SystemExit:
            pass
        files = sorted(out_dir.glob("*"))
        assert len(files) == 4  # claude.md, hermes.md, cursor.cursorrules, codex.json
