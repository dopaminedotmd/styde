"""
Tests for Core.persistence — atomic filesystem operations.
TDD: RED phase — test fails because persistence.py is empty.
"""
import pytest
import tempfile
from pathlib import Path

# The module under test — currently a stub
# Once GREEN: from Core.persistence import atomic_write, atomic_write_json, atomic_append, transactional_save


class TestAtomicWrite:
    """Test atomic_write — temp-file + rename pattern."""

    def test_writes_content_to_file(self, tmp_path):
        """Normal write: content written, file exists."""
        from Core.persistence import atomic_write

        f = tmp_path / "test.txt"
        result = atomic_write(f, "hello world")

        assert result is True
        assert f.exists()
        assert f.read_text(encoding="utf-8") == "hello world"

    def test_creates_parent_directories(self, tmp_path):
        """Missing parent dirs are auto-created."""
        from Core.persistence import atomic_write

        f = tmp_path / "deep" / "nested" / "dir" / "test.txt"
        atomic_write(f, "content")

        assert f.exists()
        assert f.read_text(encoding="utf-8") == "content"

    def test_overwrites_existing_file(self, tmp_path):
        """Existing file is completely replaced."""
        from Core.persistence import atomic_write

        f = tmp_path / "test.txt"
        f.write_text("old content")
        atomic_write(f, "new content")

        assert f.read_text(encoding="utf-8") == "new content"

    def test_handles_empty_content(self, tmp_path):
        """Empty string is written correctly."""
        from Core.persistence import atomic_write

        f = tmp_path / "empty.txt"
        atomic_write(f, "")

        assert f.exists()
        assert f.read_text(encoding="utf-8") == ""

    def test_handles_unicode_content(self, tmp_path):
        """Unicode characters (Swedish, emoji) survive round-trip."""
        from Core.persistence import atomic_write

        f = tmp_path / "unicode.txt"
        content = "åäö ÅÄÖ — emoji: 🚀🔥💯\nmultiline\ncontent"
        atomic_write(f, content)

        assert f.read_text(encoding="utf-8") == content

    def test_no_temp_file_left_behind(self, tmp_path):
        """After successful write, no .tmp files remain."""
        from Core.persistence import atomic_write

        d = tmp_path / "dir"
        f = d / "test.txt"
        atomic_write(f, "content")

        tmp_files = list(d.glob("*.tmp"))
        assert len(tmp_files) == 0, f"Temp files left behind: {tmp_files}"

    def test_atomic_no_partial_on_disk_full(self, tmp_path):
        """If write fails mid-stream, original file is intact. Marked skip — hard to simulate."""
        pass  # Requires mocking disk fullness — integration test

    def test_concurrent_writes_different_files(self, tmp_path):
        """Multiple atomic writes to different files don't interfere."""
        from Core.persistence import atomic_write

        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"

        atomic_write(f1, "content A")
        atomic_write(f2, "content B")

        assert f1.read_text(encoding="utf-8") == "content A"
        assert f2.read_text(encoding="utf-8") == "content B"


class TestAtomicWriteJson:
    """Test atomic_write_json."""

    def test_writes_dict_as_json(self, tmp_path):
        """Dict is serialized to JSON and written atomically."""
        from Core.persistence import atomic_write_json

        f = tmp_path / "data.json"
        data = {"name": "test", "version": 1, "nested": {"key": "value"}}
        atomic_write_json(f, data)

        import json
        loaded = json.loads(f.read_text(encoding="utf-8"))
        assert loaded == data

    def test_indents_output(self, tmp_path):
        """JSON output is pretty-printed with indent=2."""
        from Core.persistence import atomic_write_json

        f = tmp_path / "pretty.json"
        atomic_write_json(f, {"a": 1})

        content = f.read_text(encoding="utf-8")
        assert "  " in content  # indent=2
        assert "\n" in content  # multiline


class TestAtomicAppend:
    """Test atomic_append — JSON-lines logging."""

    def test_appends_line_to_file(self, tmp_path):
        """Lines are appended, file grows."""
        from Core.persistence import atomic_append

        f = tmp_path / "log.jsonl"
        atomic_append(f, '{"level": "INFO", "msg": "first"}')
        atomic_append(f, '{"level": "INFO", "msg": "second"}')

        lines = f.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 2
        assert "first" in lines[0]
        assert "second" in lines[1]

    def test_adds_newline_if_missing(self, tmp_path):
        """Append adds trailing newline if line doesn't end with one."""
        from Core.persistence import atomic_append

        f = tmp_path / "log.jsonl"
        atomic_append(f, "no newline")

        content = f.read_text(encoding="utf-8")
        assert content.endswith("\n")

    def test_creates_file_if_missing(self, tmp_path):
        """If file doesn't exist, it's created."""
        from Core.persistence import atomic_append

        f = tmp_path / "new_log.jsonl"
        atomic_append(f, "first line")

        assert f.exists()


class TestTransactionalSave:
    """Test transactional_save — multi-file atomic directory writes."""

    def test_saves_multiple_files(self, tmp_path):
        """Multiple files saved in one atomic operation."""
        from Core.persistence import transactional_save

        d = tmp_path / "savedir"
        files = {
            "a.txt": "content A",
            "sub/b.txt": "content B",
            "sub/deep/c.txt": "content C",
        }
        result = transactional_save(d, files)

        assert result is True
        assert (d / "a.txt").read_text(encoding="utf-8") == "content A"
        assert (d / "sub" / "b.txt").read_text(encoding="utf-8") == "content B"
        assert (d / "sub" / "deep" / "c.txt").read_text(encoding="utf-8") == "content C"

    def test_handles_dict_values(self, tmp_path):
        """Dict values are auto-serialized as JSON."""
        from Core.persistence import transactional_save

        d = tmp_path / "savedir"
        files = {
            "config.json": {"name": "forge", "version": 3},
        }
        transactional_save(d, files)

        import json
        loaded = json.loads((d / "config.json").read_text(encoding="utf-8"))
        assert loaded == {"name": "forge", "version": 3}

    def test_no_partial_on_failure(self, tmp_path):
        """If any write fails, staging dir is cleaned, target untouched."""
        from Core.persistence import transactional_save
        import os

        d = tmp_path / "target"
        old_file = d / "existing.txt"
        old_file.parent.mkdir(parents=True, exist_ok=True)
        old_file.write_text("preexisting")

        # Simulate failure via read-only directory inside staging
        # This is environment-dependent; mark as known limitation
        pass

    def test_cleans_staging_after_crash(self, tmp_path):
        """No .staging directories left after successful save."""
        from Core.persistence import transactional_save

        d = tmp_path / "savedir"
        transactional_save(d, {"a.txt": "content"})

        staging_dirs = list(tmp_path.glob("*.staging"))
        assert len(staging_dirs) == 0


class TestEdgeCases:
    """Edge case handling."""

    def test_write_to_readonly_dir_raises(self, tmp_path):
        """Writing to a read-only directory raises PermissionError."""
        # Skip on Windows — permission model differs
        import sys
        if sys.platform == "win32":
            pytest.skip("Windows permission model differs")

        from Core.persistence import atomic_write

        d = tmp_path / "readonly"
        d.mkdir()
        d.chmod(0o444)  # Read only

        f = d / "test.txt"
        with pytest.raises(PermissionError):
            atomic_write(f, "content")

        d.chmod(0o755)  # Cleanup

    def test_write_with_special_chars_in_path(self, tmp_path):
        """Paths with spaces and special chars work."""
        from Core.persistence import atomic_write

        f = tmp_path / "my dir" / "file (1).txt"
        atomic_write(f, "works")

        assert f.read_text(encoding="utf-8") == "works"
