"""Tests for Core.blueprint — load and validate blueprints."""
import pytest
import yaml
from pathlib import Path


@pytest.fixture
def blueprint_dir(tmp_path):
    """Create a minimal valid blueprint directory."""
    bp = tmp_path / "blueprints" / "code-reviewer"
    bp.mkdir(parents=True)

    (bp / "persona.md").write_text("You are a code reviewer. Find bugs. Be direct. " * 3)
    (bp / "BLUEPRINT.md").write_text("## Purpose\nReview code for bugs and security issues.")
    (bp / "config.yaml").write_text(yaml.dump({
        "blueprint": {"name": "code-reviewer", "domain": "coding"},
        "hardware_profiles": {"pontus-main": {"model": "deepseek-v4-flash"}},
        "agent": {"max_iterations": 10, "timeout_seconds": 300},
        "eval": {"min_pass_score": 70}
    }))

    skills = bp / "skills"
    skills.mkdir()
    (skills / "security.md").write_text("# Security Review\nCheck for SQL injection and XSS.")

    return tmp_path


class TestValidateBlueprint:
    """Test validate_blueprint."""

    def test_valid_blueprint_passes(self, blueprint_dir, monkeypatch):
        """Valid blueprint returns empty error list."""
        from Core.blueprint import validate_blueprint

        monkeypatch.setattr("Core.blueprint.BLUEPRINTS_DIR", blueprint_dir / "blueprints")
        errors = validate_blueprint("code-reviewer")
        assert errors == []

    def test_missing_directory(self, monkeypatch):
        """Non-existent blueprint returns error."""
        from Core.blueprint import validate_blueprint

        monkeypatch.setattr("Core.blueprint.BLUEPRINTS_DIR", Path("/nonexistent"))
        errors = validate_blueprint("nonexistent")
        assert len(errors) > 0
        assert "not found" in errors[0].lower()

    def test_missing_persona(self, blueprint_dir, monkeypatch):
        """Missing persona.md returns error."""
        from Core.blueprint import validate_blueprint
        import os

        (blueprint_dir / "blueprints" / "code-reviewer" / "persona.md").unlink()

        monkeypatch.setattr("Core.blueprint.BLUEPRINTS_DIR", blueprint_dir / "blueprints")
        errors = validate_blueprint("code-reviewer")
        assert any("persona.md" in e.lower() for e in errors)

    def test_persona_too_short(self, blueprint_dir, monkeypatch):
        """Persona under 50 chars returns error."""
        from Core.blueprint import validate_blueprint

        (blueprint_dir / "blueprints" / "code-reviewer" / "persona.md").write_text("Too short.")

        monkeypatch.setattr("Core.blueprint.BLUEPRINTS_DIR", blueprint_dir / "blueprints")
        errors = validate_blueprint("code-reviewer")
        assert any("short" in e.lower() for e in errors)

    def test_missing_blueprint_md(self, blueprint_dir, monkeypatch):
        """Missing BLUEPRINT.md returns error."""
        from Core.blueprint import validate_blueprint

        (blueprint_dir / "blueprints" / "code-reviewer" / "BLUEPRINT.md").unlink()

        monkeypatch.setattr("Core.blueprint.BLUEPRINTS_DIR", blueprint_dir / "blueprints")
        errors = validate_blueprint("code-reviewer")
        assert any("BLUEPRINT.md" in e for e in errors)

    def test_missing_config(self, blueprint_dir, monkeypatch):
        """Missing config.yaml returns error."""
        from Core.blueprint import validate_blueprint

        (blueprint_dir / "blueprints" / "code-reviewer" / "config.yaml").unlink()

        monkeypatch.setattr("Core.blueprint.BLUEPRINTS_DIR", blueprint_dir / "blueprints")
        errors = validate_blueprint("code-reviewer")
        assert any("config.yaml" in e.lower() for e in errors)


class TestLoadBlueprintContext:
    """Test load_blueprint_context."""

    def test_loads_all_context_keys(self, blueprint_dir, monkeypatch):
        """Returns dict with all required keys."""
        from Core.blueprint import load_blueprint_context

        monkeypatch.setattr("Core.blueprint.BLUEPRINTS_DIR", blueprint_dir / "blueprints")
        ctx = load_blueprint_context("code-reviewer")

        assert "persona" in ctx
        assert "blueprint_md" in ctx
        assert "config" in ctx
        assert "skills" in ctx
        assert "toolsets" in ctx

    def test_loads_persona_content(self, blueprint_dir, monkeypatch):
        """Persona content matches file."""
        from Core.blueprint import load_blueprint_context

        monkeypatch.setattr("Core.blueprint.BLUEPRINTS_DIR", blueprint_dir / "blueprints")
        ctx = load_blueprint_context("code-reviewer")

        assert "code reviewer" in ctx["persona"].lower()

    def test_loads_skills_content(self, blueprint_dir, monkeypatch):
        """Skills from skills/ directory are loaded."""
        from Core.blueprint import load_blueprint_context

        monkeypatch.setattr("Core.blueprint.BLUEPRINTS_DIR", blueprint_dir / "blueprints")
        ctx = load_blueprint_context("code-reviewer")

        assert "SQL injection" in ctx["skills"]
        assert "Security Review" in ctx["skills"]

    def test_handles_missing_skills_dir(self, blueprint_dir, monkeypatch):
        """Missing skills/ directory doesn't crash."""
        from Core.blueprint import load_blueprint_context
        import shutil

        shutil.rmtree(blueprint_dir / "blueprints" / "code-reviewer" / "skills")

        monkeypatch.setattr("Core.blueprint.BLUEPRINTS_DIR", blueprint_dir / "blueprints")
        ctx = load_blueprint_context("code-reviewer")

        assert ctx["skills"] == ""

    def test_config_parsed_correctly(self, blueprint_dir, monkeypatch):
        """Config YAML is parsed into dict."""
        from Core.blueprint import load_blueprint_context

        monkeypatch.setattr("Core.blueprint.BLUEPRINTS_DIR", blueprint_dir / "blueprints")
        ctx = load_blueprint_context("code-reviewer")

        assert ctx["config"]["blueprint"]["name"] == "code-reviewer"
        assert ctx["config"]["blueprint"]["domain"] == "coding"

    def test_toolsets_from_config(self, blueprint_dir, monkeypatch):
        """Toolsets default to [terminal, file, web]."""
        from Core.blueprint import load_blueprint_context

        monkeypatch.setattr("Core.blueprint.BLUEPRINTS_DIR", blueprint_dir / "blueprints")
        ctx = load_blueprint_context("code-reviewer")

        assert isinstance(ctx["toolsets"], list)
        assert "terminal" in ctx["toolsets"]
        assert "file" in ctx["toolsets"]
        assert "web" in ctx["toolsets"]
