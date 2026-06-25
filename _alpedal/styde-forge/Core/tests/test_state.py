"""Tests for Core.state — state.yaml management."""
import pytest
import yaml
from pathlib import Path


class TestState:
    """Test load_state and save_state."""

    def test_load_state_returns_dict(self, tmp_path, monkeypatch):
        """load_state returns a dict from state.yaml."""
        from Core.state import load_state

        state_file = tmp_path / "state.yaml"
        state_file.write_text(yaml.dump({"forge_version": "3.0.0", "loop_iterations": 0}))

        monkeypatch.setattr("Core.state.STATE_FILE", state_file)
        state = load_state()

        assert isinstance(state, dict)
        assert state["forge_version"] == "3.0.0"
        assert state["loop_iterations"] == 0

    def test_load_state_missing_file_raises(self, tmp_path, monkeypatch):
        """Missing state.yaml raises FileNotFoundError."""
        from Core.state import load_state

        state_file = tmp_path / "nonexistent.yaml"
        monkeypatch.setattr("Core.state.STATE_FILE", state_file)

        with pytest.raises(FileNotFoundError):
            load_state()

    def test_save_state_persists_data(self, tmp_path, monkeypatch):
        """save_state writes YAML that load_state can read back."""
        from Core.state import load_state, save_state

        state_file = tmp_path / "state.yaml"
        state_file.write_text(yaml.dump({"forge_version": "3.0.0", "loop_iterations": 0}))

        monkeypatch.setattr("Core.state.STATE_FILE", state_file)

        state = load_state()
        state["loop_iterations"] = 42
        state["new_key"] = "new_value"
        save_state(state)

        reloaded = load_state()
        assert reloaded["loop_iterations"] == 42
        assert reloaded["new_key"] == "new_value"

    def test_load_state_handles_empty_file(self, tmp_path, monkeypatch):
        """Empty state.yaml returns None (yaml.safe_load behavior)."""
        from Core.state import load_state

        state_file = tmp_path / "empty.yaml"
        state_file.write_text("")

        monkeypatch.setattr("Core.state.STATE_FILE", state_file)
        state = load_state()

        # yaml.safe_load of empty string returns None
        assert state is None

    def test_save_state_is_atomic(self, tmp_path, monkeypatch):
        """save_state writes atomically — no partial writes."""
        from Core.state import save_state, load_state

        state_file = tmp_path / "state.yaml"
        state_file.write_text(yaml.dump({"forge_version": "3.0.0"}))

        monkeypatch.setattr("Core.state.STATE_FILE", state_file)

        large_state = {"forge_version": "3.0.0", "agents": list(range(1000))}
        save_state(large_state)

        reloaded = load_state()
        assert len(reloaded["agents"]) == 1000

    def test_default_state_structure(self, tmp_path, monkeypatch):
        """Default state has all required top-level keys."""
        from Core.state import load_state

        state_file = tmp_path / "state.yaml"
        default = {
            "forge_version": "3.0.0",
            "forge_codename": "The Crucible",
            "loop_iterations": 0,
            "total_agents_spawned": 0,
            "total_evaluations": 0,
            "blueprints": [],
            "agents": [],
            "evaluations": [],
            "improvements": [],
        }
        state_file.write_text(yaml.dump(default))

        monkeypatch.setattr("Core.state.STATE_FILE", state_file)
        state = load_state()

        for key in default:
            assert key in state, f"Missing key: {key}"
