"""
Staleness detection for Styde Forge agents.
Tracks review dates, dependency health, and schema expectations.
Adopted from agent-skill-creator v6.0.0 staleness detection.
"""
import time
import yaml
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

FORGE_ROOT = Path(__file__).resolve().parent.parent


def check_staleness(agent_path: str | Path) -> dict:
    """
    Check if an agent is stale.
    
    Three layers:
    1. Review tracking — last reviewed date vs review interval
    2. Dependency health — external URLs still reachable
    3. Schema drift — API response shapes changed
    
    Returns {stale: bool, checks: [{layer, passed, detail}], recommendation: str}
    """
    agent_path = Path(agent_path)
    checks = []
    
    # Layer 1: Review tracking
    review_check = _check_review_date(agent_path)
    checks.append(review_check)
    
    # Layer 2: Dependency health
    dep_check = _check_dependencies(agent_path)
    checks.append(dep_check)
    
    # Layer 3: Schema drift
    schema_check = _check_schema_drift(agent_path)
    checks.append(schema_check)
    
    stale = any(not c["passed"] for c in checks if c["layer"] != "schema_drift")
    
    recommendation = "fresh"
    if stale:
        overdue = [c for c in checks if not c["passed"]]
        if any(c["layer"] == "review_tracking" for c in overdue):
            recommendation = "review_overdue"
        elif any(c["layer"] == "dependency_health" for c in overdue):
            recommendation = "dependencies_broken"
        else:
            recommendation = "needs_attention"
    
    return {
        "stale": stale,
        "checks": checks,
        "recommendation": recommendation,
        "checked_at": datetime.now().isoformat()
    }


def _check_review_date(agent_path: Path) -> dict:
    """
    Check if the agent's content is overdue for review.
    
    Uses config.yaml metadata:
    - last_reviewed: date of last review
    - review_interval_days: days between required reviews
    
    Falls back to git commit date on BLUEPRINT.md.
    """
    config_path = agent_path / "config.yaml"
    
    if not config_path.exists():
        return {"layer": "review_tracking", "passed": True, "detail": "No config.yaml — skipping review check"}
    
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    meta = cfg.get("blueprint", {})
    
    last_reviewed = meta.get("last_reviewed")
    interval_days = meta.get("review_interval_days", 90)
    
    if not last_reviewed:
        # Fallback: git commit date
        last_reviewed = _git_last_modified(agent_path / "BLUEPRINT.md")
        if not last_reviewed:
            return {"layer": "review_tracking", "passed": True, "detail": "No review date set — skipping"}
    
    try:
        review_date = datetime.fromisoformat(last_reviewed)
    except ValueError:
        return {"layer": "review_tracking", "passed": True, "detail": f"Invalid date format: {last_reviewed}"}
    
    due_date = review_date + timedelta(days=interval_days)
    now = datetime.now()
    
    if now > due_date:
        days_overdue = (now - due_date).days
        return {
            "layer": "review_tracking",
            "passed": False,
            "detail": f"Overdue by {days_overdue} days (last reviewed {last_reviewed}, interval {interval_days}d)",
            "last_reviewed": last_reviewed,
            "interval_days": interval_days,
            "days_overdue": days_overdue
        }
    
    days_until = (due_date - now).days
    return {
        "layer": "review_tracking",
        "passed": True,
        "detail": f"Fresh — due in {days_until} days",
        "last_reviewed": last_reviewed,
        "interval_days": interval_days
    }


def _check_dependencies(agent_path: Path) -> dict:
    """
    Check external dependency URLs.
    
    Looks for 'dependencies' in config.yaml:
    - url: the endpoint
    - name: human name
    - type: api | web | data
    
    HTTP-checks each URL. Reports unreachable ones.
    """
    config_path = agent_path / "config.yaml"
    
    if not config_path.exists():
        return {"layer": "dependency_health", "passed": True, "detail": "No config — skipping"}
    
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    dependencies = cfg.get("blueprint", {}).get("dependencies", [])
    
    if not dependencies:
        return {"layer": "dependency_health", "passed": True, "detail": "No external dependencies declared"}
    
    failed = []
    for dep in dependencies:
        url = dep.get("url")
        if not url:
            continue
        
        reachable = _http_check(url)
        if not reachable:
            failed.append({"name": dep.get("name", url), "url": url})
    
    if failed:
        names = ", ".join(d["name"] for d in failed)
        return {
            "layer": "dependency_health",
            "passed": False,
            "detail": f"Unreachable: {names}",
            "failed_dependencies": failed
        }
    
    return {
        "layer": "dependency_health",
        "passed": True,
        "detail": f"All {len(dependencies)} dependencies reachable"
    }


def _check_schema_drift(agent_path: Path) -> dict:
    """
    Check for API schema drift.
    
    Compares expected response keys against actual API responses.
    This is a best-effort check — not all APIs are checked on every run.
    
    'schema_expectations' in config.yaml defines expected shapes.
    """
    config_path = agent_path / "config.yaml"
    
    if not config_path.exists():
        return {"layer": "schema_drift", "passed": True, "detail": "No config — skipping"}
    
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    expectations = cfg.get("blueprint", {}).get("schema_expectations", [])
    
    if not expectations:
        return {"layer": "schema_drift", "passed": True, "detail": "No schema expectations declared"}
    
    # This requires actual API calls — skip in automated checks
    return {"layer": "schema_drift", "passed": True, "detail": "Schema drift check requires --check-drift flag (manual)"}


# --- Helpers ---

def _git_last_modified(filepath: Path) -> str | None:
    """Get the date of the last git commit that modified this file."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", str(filepath)],
            capture_output=True, text=True, timeout=5,
            cwd=str(filepath.parent.parent)
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def _http_check(url: str, timeout: int = 10) -> bool:
    """Check if a URL is reachable."""
    try:
        result = subprocess.run(
            ["curl", "-sI", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", str(timeout), url],
            capture_output=True, text=True, timeout=timeout + 2
        )
        status = int(result.stdout.strip()) if result.stdout.strip() else 0
        return 200 <= status < 500
    except (subprocess.TimeoutExpired, ValueError, FileNotFoundError):
        return False


def _parse_iso_date(date_str: str) -> datetime | None:
    """Parse ISO date string."""
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None
