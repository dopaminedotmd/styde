"""
Hermes CLI bridge for Styde Forge.

Wraps `hermes -z` for non-interactive agent execution.
Used by spawn, eval, and teacher commands.
"""
import subprocess
import os
import shutil
from pathlib import Path
from typing import Optional


def find_hermes() -> str:
    """Find hermes executable."""
    if shutil.which("hermes"):
        return "hermes"
    home = Path.home()
    for subdir in ["AppData/Local/hermes", ".local/bin"]:
        p = home / subdir / "hermes"
        if p.exists():
            return str(p)
    return "hermes"


def _run_hermes(
    prompt: str,
    model: str = "deepseek/deepseek-chat",
    toolsets: list[str] = None,
    skills: list[str] = None,
    timeout: int = 300,
    yolo: bool = True,
) -> dict:
    """
    Run hermes -z (inline mode). Core execution engine.
    """
    cmd = [find_hermes(), "-z", prompt, "-m", model]

    if toolsets:
        cmd.extend(["-t", ",".join(toolsets)])
    if skills:
        cmd.extend(["--skills", ",".join(skills)])
    if yolo:
        cmd.append("--yolo")

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
            env=env,
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "exit_code": result.returncode,
            "stderr": result.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "exit_code": -1,
            "stderr": f"Timeout after {timeout}s",
        }
    except FileNotFoundError:
        return {
            "success": False,
            "output": "",
            "exit_code": -1,
            "stderr": "Hermes not found.",
        }


def spawn_agent(
    goal: str,
    context: str = "",
    model: str = "deepseek/deepseek-chat",
    toolsets: list[str] = None,
    skills: list[str] = None,
    timeout: int = 300,
) -> dict:
    """
    Spawn agent via Hermes -z inline mode.

    Returns {success, output, exit_code, stderr}
    """
    if toolsets is None:
        toolsets = ["terminal", "file", "web"]

    full_prompt = goal
    if context:
        full_prompt = f"{context}\n\n---\n\n{goal}"

    return _run_hermes(
        prompt=full_prompt,
        model=model,
        toolsets=toolsets,
        skills=skills,
        timeout=timeout,
    )


def run_eval(
    prompt: str,
    model: str = "deepseek/deepseek-chat",
    timeout: int = 60,
) -> dict:
    """Run evaluation via Hermes (self-eval or judge-eval). No tools needed."""
    full_prompt = f"Use temperature=0.1. Be precise.\n\n{prompt}"
    return _run_hermes(
        prompt=full_prompt,
        model=model,
        toolsets=None,  # No tools for pure eval
        timeout=timeout,
    )


def run_teacher(
    prompt: str,
    model: str = "deepseek/deepseek-chat",
    timeout: int = 90,
) -> dict:
    """Run teacher analysis via Hermes."""
    return run_eval(prompt, model=model, timeout=timeout)


def is_available() -> bool:
    """Check if Hermes CLI is available."""
    try:
        result = subprocess.run(
            [find_hermes(), "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
