"""Tests for spawn.py."""
import pytest
import yaml
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from Core.spawn import (
    extract_self_eval,
    strip_self_eval,
    build_spawn_context,
    capture_agent_output,
    CAVEMAN_ULTRA_RULES,
    SELF_EVAL_INSTRUCTION,
)


class TestExtractSelfEval:
    """Self-eval extraction from agent output."""

    def test_extracts_valid_self_eval(self):
        output = """L14: SQL injection. Fix: parameterized queries.
L28: Hardcoded password.
Score: 85
---
SELF_EVAL:
  score: 85
  correctness: 90
  robustness: 75
  code_quality: 88
  efficiency: 82
  innovation: 80
  documentation: 95
  notes: "Missed one edge case"
"""
        result = extract_self_eval(output)
        assert result["score"] == 85
        assert result["correctness"] == 90
        assert result["robustness"] == 75
        assert result["notes"] == "Missed one edge case"

    def test_no_self_eval_returns_error(self):
        output = "Just some code review output. No self-eval here."
        result = extract_self_eval(output)
        assert result["score"] == 0
        assert result["error"] == "no_self_eval"

    def test_invalid_yaml_returns_error(self):
        output = """Some output
---
SELF_EVAL:
  - item1
  - item2
    - bad indent: sub: item
"""
        result = extract_self_eval(output)
        assert result["score"] == 0
        assert result["error"] == "unparseable"

    def test_missing_score_field(self):
        output = """Some output
---
SELF_EVAL:
  correctness: 90
  notes: "no score field"
"""
        result = extract_self_eval(output)
        assert result["score"] == 0
        assert result["error"] == "invalid_format"

    def test_clamps_scores_to_0_100(self):
        output = """---
SELF_EVAL:
  score: 150
  correctness: -10
  robustness: 75
"""
        result = extract_self_eval(output)
        assert result["score"] == 100
        assert result["correctness"] == 0
        assert result["robustness"] == 75

    def test_self_eval_at_end_of_output(self):
        output = """Task completed.

---
SELF_EVAL:
  score: 92
  notes: "done"
"""
        result = extract_self_eval(output)
        assert result["score"] == 92

    def test_no_separator_returns_error(self):
        output = "SELF_EVAL:\n  score: 50"
        result = extract_self_eval(output)
        assert result["score"] == 0
        assert result["error"] == "no_self_eval"


class TestStripSelfEval:
    """Strip self-eval from agent output."""

    def test_removes_self_eval_block(self):
        output = """Code review output here.

---
SELF_EVAL:
  score: 85
"""
        result = strip_self_eval(output)
        assert result == "Code review output here."

    def test_no_self_eval_returns_unchanged(self):
        output = "Just some output. No self-eval."
        assert strip_self_eval(output) == output

    def test_preserves_separators_before_self_eval(self):
        output = """Section 1
---
Section 2
---
SELF_EVAL:
  score: 90
"""
        result = strip_self_eval(output)
        assert "Section 1" in result
        assert "Section 2" in result
        assert "SELF_EVAL" not in result


class TestBuildSpawnContext:
    """Context builder for spawn."""

    def test_includes_persona(self):
        context = {
            "persona": "You are a code reviewer.",
            "blueprint_md": "## Purpose\nReview code.",
            "config": {},
            "skills": "",
            "history": "",
        }
        result = build_spawn_context(
            blueprint_name="code-reviewer",
            context=context,
            task="Review this code",
            rubric={"score": {"weight": 1.0}},
            output_path="/tmp/output.md",
            caveman_ultra=False,
        )
        assert "You are a code-reviewer agent" in result
        assert "code reviewer" in result.lower()
        assert "Review this code" in result
        assert "/tmp/output.md" in result

    def test_includes_caveman_ultra_when_enabled(self):
        context = {
            "persona": "Test",
            "blueprint_md": "Test",
            "config": {},
            "skills": "",
            "history": "",
        }
        result = build_spawn_context(
            "test", context, "task", {"score": {"weight": 1.0}}, "/out", caveman_ultra=True
        )
        assert "CAVEMAN ULTRA MODE" in result

    def test_excludes_caveman_ultra_when_disabled(self):
        context = {
            "persona": "Test",
            "blueprint_md": "Test",
            "config": {},
            "skills": "",
            "history": "",
        }
        result = build_spawn_context(
            "test", context, "task", {"score": {"weight": 1.0}}, "/out", caveman_ultra=False
        )
        assert "CAVEMAN ULTRA MODE" not in result

    def test_includes_self_eval_instruction(self):
        context = {
            "persona": "Test",
            "blueprint_md": "Test",
            "config": {},
            "skills": "",
            "history": "",
        }
        result = build_spawn_context(
            "test", context, "task", {"score": {"weight": 1.0}}, "/out"
        )
        assert "SELF_EVAL:" in result
        assert "score: <0-100>" in result

    def test_includes_skills_when_present(self):
        context = {
            "persona": "Test",
            "blueprint_md": "Test",
            "config": {},
            "skills": "SKILL: code-review-v2",
            "history": "",
        }
        result = build_spawn_context(
            "test", context, "task", {"score": {"weight": 1.0}}, "/out"
        )
        assert "code-review-v2" in result

    def test_includes_rubric(self):
        context = {
            "persona": "Test",
            "blueprint_md": "Test",
            "config": {},
            "skills": "",
            "history": "",
        }
        rubric = {"correctness": {"weight": 0.4}, "robustness": {"weight": 0.3}}
        result = build_spawn_context(
            "test", context, "task", rubric, "/out"
        )
        assert "correctness" in result
        assert "robustness" in result

    def test_includes_history_when_present(self):
        context = {
            "persona": "Test",
            "blueprint_md": "Test",
            "config": {},
            "skills": "",
            "history": "Previous: Score 75 — FAILED",
        }
        result = build_spawn_context(
            "test", context, "task", {"score": {"weight": 1.0}}, "/out"
        )
        assert "Historical Context" in result
        assert "Score 75" in result

    def test_skips_history_when_empty(self):
        context = {
            "persona": "Test",
            "blueprint_md": "Test",
            "config": {},
            "skills": "",
            "history": "",
        }
        result = build_spawn_context(
            "test", context, "task", {"score": {"weight": 1.0}}, "/out"
        )
        assert "Historical Context" not in result


class TestCaptureAgentOutput:
    """Output capture from file or delegate_task return."""

    def test_reads_from_file_when_exists(self, tmp_path):
        agent_dir = tmp_path / "agent-1"
        run_id = "run-001"
        run_dir = agent_dir / "runs" / run_id
        run_dir.mkdir(parents=True)
        output_path = run_dir / "output.md"
        output_path.write_text("Agent output from file.")

        result = {"output": "Agent output from return.", "summary": "summary"}
        text, source = capture_agent_output(agent_dir, run_id, result)
        assert text == "Agent output from file."
        assert source == "file"

    def test_falls_back_to_return_value(self, tmp_path):
        agent_dir = tmp_path / "agent-2"
        run_id = "run-002"
        result = {"output": "Agent output from return.", "summary": "summary"}

        text, source = capture_agent_output(agent_dir, run_id, result)
        assert text == "Agent output from return."
        assert source == "return_saved"

        # Verify file was saved
        output_path = agent_dir / "runs" / run_id / "output.md"
        assert output_path.exists()
        assert output_path.read_text() == "Agent output from return."

    def test_falls_back_to_summary(self, tmp_path):
        agent_dir = tmp_path / "agent-3"
        run_id = "run-003"
        result = {"output": "", "summary": "Summary only."}

        text, source = capture_agent_output(agent_dir, run_id, result)
        assert text == "Summary only."
        assert source == "summary_only"


class TestSpawnAgent:
    """Integration tests for spawn_agent."""

    def test_validation_fails_for_missing_blueprint(self):
        from Core.spawn import spawn_agent

        with patch("Core.spawn.validate_blueprint") as mock_validate:
            mock_validate.return_value = ["Blueprint not found"]
            result = spawn_agent(
                "nonexistent", "task", {"score": {"weight": 1.0}},
                {"config": {}}, timeout=5
            )
            assert result["status"] == "validation_failed"
            assert len(result["errors"]) == 1

    def test_successful_spawn(self, tmp_path):
        from Core.spawn import spawn_agent, REFINERY_DIR

        with patch("Core.spawn.validate_blueprint", return_value=[]), \
             patch("Core.spawn.REFINERY_DIR", tmp_path / "refinery"), \
             patch("Core.spawn._call_delegate_task") as mock_call, \
             patch("Core.spawn._register_agent_in_state"):
            mock_call.return_value = {
                "status": "success",
                "output": "Task output\n---\nSELF_EVAL:\n  score: 88\n  correctness: 90\n  notes: ok",
                "tokens": {"input": 100, "output": 50},
                "duration_ms": 1500,
            }

            result = spawn_agent(
                "code-reviewer",
                "Review this file",
                {"score": {"weight": 1.0}},
                {"persona": "CR", "blueprint_md": "review", "config": {}},
                timeout=5,
            )

            assert result["status"] == "success"
            assert result["agent_id"].startswith("agent-code-reviewer-")
            assert result["self_eval_score"] == 88
            assert result["attempts"] == 1

    def test_timeout_with_retry(self, tmp_path):
        from Core.spawn import spawn_agent

        with patch("Core.spawn.validate_blueprint", return_value=[]), \
             patch("Core.spawn.REFINERY_DIR", tmp_path / "refinery"), \
             patch("Core.spawn._call_delegate_task") as mock_call, \
             patch("Core.spawn.MAX_RETRIES", 2), \
             patch("Core.spawn.RETRY_DELAYS", [0, 0]):  # Fast retries
            mock_call.return_value = {"status": "timeout", "reason": "timeout"}

            result = spawn_agent(
                "code-reviewer", "task", {"score": {"weight": 1.0}},
                {"config": {}}, timeout=1,
            )
            assert result["status"] == "timeout"
            assert result["attempts"] == 2

    def test_rate_limit_with_retry(self, tmp_path):
        from Core.spawn import spawn_agent

        with patch("Core.spawn.validate_blueprint", return_value=[]), \
             patch("Core.spawn.REFINERY_DIR", tmp_path / "refinery"), \
             patch("Core.spawn._call_delegate_task") as mock_call, \
             patch("Core.spawn._register_agent_in_state"), \
             patch("Core.spawn.MAX_RETRIES", 2), \
             patch("Core.spawn.RETRY_DELAYS", [0, 0]):
            mock_call.side_effect = [
                {"status": "error", "reason": "rate limit exceeded"},
                {
                    "status": "success",
                    "output": "done\n---\nSELF_EVAL:\n  score: 75\n  notes: ok",
                    "tokens": {"input": 50, "output": 20},
                    "duration_ms": 500,
                },
            ]

            result = spawn_agent(
                "code-reviewer", "task", {"score": {"weight": 1.0}},
                {"persona": "x", "blueprint_md": "x", "config": {}},
                timeout=5,
            )
            assert result["status"] == "success"
            assert result["attempts"] == 2
