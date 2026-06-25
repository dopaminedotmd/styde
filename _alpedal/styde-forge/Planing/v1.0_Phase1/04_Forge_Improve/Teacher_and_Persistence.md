# Teacher Integration + Persistence Layer

**Styde Forge v3.0**
**Sections:** 04_Forge_Improve + 05_Forge_Persistence
**References:** `Teacher_Agent.md`, `Core_Loop_Detail.md` §4-5, `Filesystem_Transactions.md`, `Atomic_Checkpoint_Writes.md`, `Automatic_Recovery.md`

---

## Part A: Teacher Agent (`scripts/teacher.py`)

```python
"""
Teacher Agent for Styde Forge.
Analyzes eval results, proposes blueprint improvements, extracts skills.
"""
import yaml
from pathlib import Path
from datetime import datetime

from persistence import atomic_write

FORGE_ROOT = Path(__file__).resolve().parent.parent
BLUEPRINTS_DIR = FORGE_ROOT / "blueprints"
TEACHER_LOGS_DIR = FORGE_ROOT / "08_TEACHER_LOGS"

TEACHER_PROMPT = """
You are the Teacher Agent in Styde Forge.
Analyze agent performance and generate concrete improvements.

## Current Evaluation
- Agent: {agent_id}
- Blueprint: {blueprint_name}
- Benchmark: {benchmark}
- Self-Eval: {self_score}
- Judge Score: {judge_score}
- Composite: {composite_score}
- Passed: {passed}

## Weaknesses (from judge)
{judge_notes}

## Previous Scores (last 3)
{history_scores}

## Task
1. Identify ROOT CAUSE of each weakness (not symptoms)
2. Propose CONCRETE changes (persona, skills, or config)
3. Rate each by expected impact: high/medium/low
4. If composite ≥ 85, extract successful patterns as new skill
5. Output ONLY valid YAML:

teacher_review:
  diagnosis:
    primary_weakness: "<one line>"
    root_cause: "<one line>"
  improvements:
    - target: "persona.md"
      change: "<specific change>"
      impact: "high|medium|low"
      rationale: "<why>"
  extracted_skills: []
  anti_patterns: []
  recommendation: "retry|promote|archive"
"""


def analyze_eval(agent_id: str, blueprint_name: str, eval_data: dict) -> dict:
    """
    Teacher analyzes evaluation and generates improvements.
    
    Returns teacher_review dict with diagnosis, improvements, skills.
    """
    from spawn import _call_delegate_task
    
    composite = eval_data.get("composite", {})
    self_eval = eval_data.get("self_eval", {})
    judge_eval = eval_data.get("judge_eval", {})
    
    # Load history
    history = _get_score_history(blueprint_name)
    
    prompt = TEACHER_PROMPT.format(
        agent_id=agent_id,
        blueprint_name=blueprint_name,
        benchmark=eval_data.get("benchmark", "unknown"),
        self_score=self_eval.get("score", "?"),
        judge_score=judge_eval.get("score", "?"),
        composite_score=composite.get("score", "?"),
        passed="YES" if composite.get("passed") else "NO",
        judge_notes=judge_eval.get("notes", "No notes"),
        history_scores="\n".join(f"- {s}" for s in history) if history else "No history"
    )
    
    result = _call_delegate_task(
        goal="Analyze eval results and propose blueprint improvements. Return YAML.",
        context=prompt,
        toolsets=[],  # Teacher only analyzes
        timeout=120
    )
    
    if result.get("status") != "success":
        return _fallback_teacher_review(composite.get("score", 0))
    
    teacher_output = result.get("output", "")
    review = _parse_teacher_yaml(teacher_output)
    
    if not review:
        return _fallback_teacher_review(composite.get("score", 0))
    
    # Save teacher log
    cycle_dir = TEACHER_LOGS_DIR / f"cycle-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    cycle_dir.mkdir(parents=True, exist_ok=True)
    atomic_write(cycle_dir / "teacher_review.yaml", yaml.dump(review, allow_unicode=True))
    atomic_write(cycle_dir / "eval_input.yaml", yaml.dump(eval_data, allow_unicode=True))
    
    return review


def _get_score_history(blueprint_name: str) -> list[str]:
    """Get last 3 scores for this blueprint."""
    from forge import load_state
    state = load_state()
    evals = [
        e for e in state.get("evaluations", [])
        if e.get("blueprint") == blueprint_name
    ]
    return [
        f"Score: {e['composite_score']} — {'PASS' if e.get('passed') else 'FAIL'}"
        for e in evals[-3:]
    ]


def _parse_teacher_yaml(output: str) -> dict | None:
    """Parse teacher YAML output."""
    import re
    match = re.search(r'teacher_review:(.*?)(?:\n\Z|\Z)', output, re.DOTALL)
    if match:
        try:
            return yaml.safe_load("teacher_review:" + match.group(1))["teacher_review"]
        except yaml.YAMLError:
            pass
    
    # Try entire output
    try:
        data = yaml.safe_load(output)
        if isinstance(data, dict) and "teacher_review" in data:
            return data["teacher_review"]
    except yaml.YAMLError:
        pass
    
    return None


def _fallback_teacher_review(score: int) -> dict:
    """Generate basic review when teacher API fails."""
    if score >= 85:
        rec = "promote"
    elif score >= 70:
        rec = "retry"
    else:
        rec = "archive"
    
    return {
        "diagnosis": {
            "primary_weakness": "Teacher API unavailable — auto-review",
            "root_cause": "N/A"
        },
        "improvements": [],
        "extracted_skills": [],
        "anti_patterns": [],
        "recommendation": rec,
        "fallback": True
    }


def apply_improvements(
    blueprint_name: str,
    teacher_review: dict,
    promote: bool = False,
    archive: bool = False,
    retry: bool = False
):
    """
    Apply teacher's recommended improvements to blueprint and agents.
    
    Actions:
    - promote: Move agent refinery/ → production/
    - retry: Update blueprint, increment retry counter, re-spawn
    - archive: Move agent refinery/ → archive/
    """
    from forge import AGENTS_DIR, load_state, save_state
    from persistence import atomic_write
    
    state = load_state()
    
    # Find agent
    agents = [a for a in state["agents"] if a["blueprint"] == blueprint_name]
    if not agents:
        return
    
    agent = agents[-1]
    agent_name = agent["name"]
    
    if promote:
        # Move to production
        src = AGENTS_DIR / "refinery" / agent_name
        dst = AGENTS_DIR / "production" / agent_name
        if src.exists():
            import shutil
            if dst.exists():
                shutil.rmtree(dst)
            shutil.move(str(src), str(dst))
        
        agent["stage"] = "production"
        agent["status"] = "deployed"
        
        # Update blueprint status
        for bp in state["blueprints"]:
            if bp["name"] == blueprint_name:
                bp["status"] = "stable"
                bp["last_eval_score"] = agent.get("composite_score")
        
        print(f"  ✓ Promoted {agent_name} to production/")
    
    elif archive:
        # Move to archive
        src = AGENTS_DIR / "refinery" / agent_name
        dst = AGENTS_DIR / "archive" / agent_name
        if src.exists():
            import shutil
            if dst.exists():
                shutil.rmtree(dst)
            shutil.move(str(src), str(dst))
        
        agent["stage"] = "archive"
        agent["status"] = "archived"
        
        print(f"  ✗ Archived {agent_name}")
    
    elif retry:
        # Apply blueprint improvements from teacher
        for imp in teacher_review.get("improvements", []):
            target = imp["target"]
            change = imp["change"]
            
            if target.endswith(".md"):
                # Append improvement notes to the file
                target_path = BLUEPRINTS_DIR / blueprint_name / target
                if target_path.exists():
                    current = target_path.read_text(encoding="utf-8")
                    new_section = f"\n\n## Teacher Improvement ({datetime.now().strftime('%Y-%m-%d')})\n{change}\n"
                    atomic_write(target_path, current + new_section)
            
            print(f"  → Updated {target}: {change[:60]}...")
        
        agent["status"] = "retrying"
        agent["retries"] = agent.get("retries", 0) + 1
        
        # Increment blueprint version
        for bp in state["blueprints"]:
            if bp["name"] == blueprint_name:
                bp["version"] += 1
                bp["status"] = "testing"
                bp["last_eval_score"] = agent.get("composite_score")
        
        # Record improvement
        state.setdefault("improvements", []).append({
            "blueprint": blueprint_name,
            "from_version": agent.get("version", 1),
            "to_version": agent.get("version", 1) + 1,
            "eval_delta": 0,
            "changes": "; ".join(
                imp["change"][:80] for imp in teacher_review.get("improvements", [])
            ),
            "timestamp": datetime.now().isoformat()
        })
    
    save_state(state)


def extract_skill_from_success(agent_output: str, eval_result: dict) -> str | None:
    """
    Extract reusable skill from successful agent run (≥85).
    Returns skill markdown content or None.
    """
    composite = eval_result.get("composite", {})
    if composite.get("score", 0) < 85:
        return None
    
    skill = f"""# Extracted Skill: {eval_result.get('blueprint', 'unknown')}

**Source Agent:** {eval_result.get('agent_id', 'unknown')}
**Score:** {composite.get('score', 0)}
**Date:** {datetime.now().strftime('%Y-%m-%d')}

## Successful Pattern
[Extracted from agent output — requires human review]

## When to Use
[Conditions where this pattern applies]

## Anti-Patterns to Avoid
[What didn't work, learned from evals]
"""
    return skill
```

---

## Part B: Persistence Layer (`scripts/checkpoint.py`)

```python
"""
Checkpoint system for Styde Forge.
Atomic state snapshots with integrity verification.
"""
import hashlib
import shutil
import time
from pathlib import Path
from datetime import datetime

from persistence import atomic_write, atomic_write_json, transactional_save

FORGE_ROOT = Path(__file__).resolve().parent.parent
CHECKPOINTS_DIR = FORGE_ROOT / "09_CHECKPOINTS"
STATE_FILE = FORGE_ROOT / "state.yaml"
LOCK_FILE = FORGE_ROOT / ".checkpoint.lock"

CHECKPOINT_PATHS = [
    "state.yaml",
    "00_MANIFEST.json",
    "99_INDEXES/hardware_profile.json",
    "99_INDEXES/cost_summary.json",
    "StydeAgents/refinery/",
    "StydeAgents/production/",
    "StydeAgents/archive/",
    "blueprints/",
    "eval/results/",
    "08_TEACHER_LOGS/",
]

CHECKPOINT_EXCLUDE = [
    "09_CHECKPOINTS/",
    "01_KNOWLEDGE/",
    "logs/",
    ".checkpoint.lock",
]


def create_checkpoint() -> dict:
    """Create atomic checkpoint of forge state."""
    t0 = time.time()
    
    # Acquire lock
    if LOCK_FILE.exists():
        return {"success": False, "reason": "Checkpoint already in progress"}
    
    LOCK_FILE.touch()
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        checkpoint_id = f"checkpoint-{timestamp}"
        staging = CHECKPOINTS_DIR / f".{checkpoint_id}.staging"
        final = CHECKPOINTS_DIR / checkpoint_id
        
        # Clean any leftover staging
        if staging.exists():
            shutil.rmtree(staging)
        
        staging.mkdir(parents=True, exist_ok=True)
        
        # Copy files
        files_copied = 0
        total_size = 0
        
        for pattern in CHECKPOINT_PATHS:
            src = FORGE_ROOT / pattern
            if not src.exists():
                continue
            
            dst = staging / pattern
            
            if src.is_file():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                files_copied += 1
                total_size += src.stat().st_size
            
            elif src.is_dir():
                for f in src.rglob("*"):
                    if f.is_file():
                        rel = f.relative_to(FORGE_ROOT)
                        # Skip excluded paths
                        if any(str(rel).startswith(ex) for ex in CHECKPOINT_EXCLUDE):
                            continue
                        target = staging / rel
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(f, target)
                        files_copied += 1
                        total_size += f.stat().st_size
        
        # Write manifest
        manifest = {
            "checkpoint_id": checkpoint_id,
            "created": datetime.now().isoformat(),
            "files": files_copied,
            "size_bytes": total_size,
            "sha256": _compute_checkpoint_hash(staging)
        }
        atomic_write_json(staging / "CHECKPOINT_MANIFEST.json", manifest)
        
        # Atomic rename
        if final.exists():
            shutil.rmtree(final)
        staging.rename(final)
        
        # Update state
        from forge import load_state, save_state
        state = load_state()
        state["last_checkpoint"] = checkpoint_id
        save_state(state)
        
        duration_ms = int((time.time() - t0) * 1000)
        
        return {
            "success": True,
            "checkpoint_id": checkpoint_id,
            "files": files_copied,
            "size_mb": round(total_size / (1024 * 1024), 1),
            "duration_ms": duration_ms
        }
    
    finally:
        # Release lock
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()


def _compute_checkpoint_hash(dir_path: Path) -> str:
    """Compute SHA256 of all files in checkpoint."""
    hasher = hashlib.sha256()
    for f in sorted(dir_path.rglob("*")):
        if f.is_file():
            hasher.update(f.read_bytes())
    return hasher.hexdigest()


def verify_checkpoint(checkpoint_id: str) -> bool:
    """Verify checkpoint integrity."""
    cp_dir = CHECKPOINTS_DIR / checkpoint_id
    manifest_path = cp_dir / "CHECKPOINT_MANIFEST.json"
    
    if not manifest_path.exists():
        return False
    
    import json
    manifest = json.loads(manifest_path.read_text())
    stored_hash = manifest["sha256"]
    actual_hash = _compute_checkpoint_hash(cp_dir)
    
    return stored_hash == actual_hash


def list_checkpoints() -> list[dict]:
    """List all checkpoints."""
    if not CHECKPOINTS_DIR.exists():
        return []
    
    checkpoints = []
    for cp_dir in sorted(CHECKPOINTS_DIR.glob("checkpoint-*")):
        manifest_path = cp_dir / "CHECKPOINT_MANIFEST.json"
        if manifest_path.exists():
            import json
            manifest = json.loads(manifest_path.read_text())
            manifest["directory"] = str(cp_dir)
            checkpoints.append(manifest)
    
    return checkpoints


def restore_from_checkpoint(checkpoint_id: str = None) -> dict:
    """
    Restore forge state from a checkpoint.
    If no checkpoint_id given, restores the latest valid one.
    """
    if checkpoint_id is None:
        checkpoints = list_checkpoints()
        if not checkpoints:
            return {"success": False, "reason": "No checkpoints found"}
        checkpoint_id = checkpoints[-1]["checkpoint_id"]
    
    cp_dir = CHECKPOINTS_DIR / checkpoint_id
    if not cp_dir.exists():
        # Try with "checkpoint-" prefix
        cp_dir = CHECKPOINTS_DIR / f"checkpoint-{checkpoint_id}"
        if not cp_dir.exists():
            return {"success": False, "reason": f"Checkpoint not found: {checkpoint_id}"}
    
    # Verify integrity
    if not verify_checkpoint(checkpoint_id.replace("checkpoint-", "")):
        return {"success": False, "reason": "Checkpoint integrity check failed"}
    
    # Restore files
    restored = 0
    for f in cp_dir.rglob("*"):
        if f.is_file() and f.name != "CHECKPOINT_MANIFEST.json":
            rel = f.relative_to(cp_dir)
            target = FORGE_ROOT / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)
            restored += 1
    
    return {
        "success": True,
        "checkpoint_id": checkpoint_id,
        "files_restored": restored
    }
```

---

## Part C: Recovery (`scripts/recovery.py`)

```python
"""
Crash recovery for Styde Forge.
Detects crashes and restores from latest valid checkpoint.
"""
from pathlib import Path
from datetime import datetime

FORGE_ROOT = Path(__file__).resolve().parent.parent
LOCK_FILE = FORGE_ROOT / ".checkpoint.lock"


def detect_crash() -> bool:
    """
    Detect if a crash occurred.
    
    Indicators:
    - Lock file exists but no active checkpoint process
    - state.yaml missing or corrupted
    - Inconsistent file state
    """
    # Check for stale lock file
    if LOCK_FILE.exists():
        # Lock exists → was there a crash during checkpoint?
        staging_dirs = list(FORGE_ROOT.glob("09_CHECKPOINTS/.*.staging"))
        if staging_dirs:
            return True
        # Lock is stale (> 10 min old)
        lock_age = datetime.now().timestamp() - LOCK_FILE.stat().st_mtime
        if lock_age > 600:
            return True
    
    # Check state.yaml exists and is valid
    state_file = FORGE_ROOT / "state.yaml"
    if not state_file.exists():
        return True
    
    try:
        import yaml
        yaml.safe_load(state_file.read_text(encoding="utf-8"))
    except Exception:
        return True
    
    return False


def recover() -> dict:
    """
    Attempt recovery from crash.
    1. Clean stale staging directories
    2. Remove stale lock file
    3. Restore from latest valid checkpoint
    """
    from checkpoint import restore_from_checkpoint
    
    result = {"actions": [], "success": False}
    
    # Clean staging
    for staging in FORGE_ROOT.glob("09_CHECKPOINTS/.*.staging"):
        import shutil
        shutil.rmtree(staging)
        result["actions"].append(f"Cleaned stale staging: {staging.name}")
    
    # Clean lock
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
        result["actions"].append("Removed stale lock file")
    
    # Restore from checkpoint
    recovery = restore_from_checkpoint()
    if recovery["success"]:
        result["success"] = True
        result["actions"].append(f"Restored from checkpoint: {recovery['checkpoint_id']}")
        result["files_restored"] = recovery.get("files_restored", 0)
    else:
        result["actions"].append(f"Recovery failed: {recovery['reason']}")
    
    # Log recovery event
    log_path = FORGE_ROOT / "logs/recovery/recovery.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    import json
    with open(log_path, "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "event": "recovery_attempt",
            "result": result
        }) + "\n")
    
    return result
```

---

## Part D: Circuit Breaker (`scripts/circuit_breaker.py`)

```python
"""
Circuit breaker for Styde Forge.
Prevents cascade failures and wasted API costs.
"""
import time

class CircuitBreaker:
    def __init__(self, name: str, failure_threshold: int = 5, reset_timeout_min: int = 30):
        self.name = name
        self.threshold = failure_threshold
        self.reset_timeout = reset_timeout_min * 60
        self.failures = 0
        self.last_failure = None
        self.state = "closed"  # closed → open → half_open → closed

    def record_failure(self):
        self.failures += 1
        self.last_failure = time.time()
        if self.failures >= self.threshold:
            self.state = "open"
            print(f"CIRCUIT BREAKER OPEN ({self.name}): {self.failures} failures")

    def record_success(self):
        if self.state == "half_open":
            self.state = "closed"
            self.failures = 0
            print(f"CIRCUIT BREAKER CLOSED ({self.name})")
        elif self.state == "closed":
            self.failures = max(0, self.failures - 1)

    def allow_request(self) -> bool:
        if self.state == "closed":
            return True
        if self.state == "open":
            if self.last_failure and (time.time() - self.last_failure > self.reset_timeout):
                self.state = "half_open"
                return True
            return False
        return True  # half_open: allow one probe


# Global breaker registry
_breakers: dict[str, CircuitBreaker] = {}

def get_breaker(name: str, threshold: int = 5) -> CircuitBreaker:
    if name not in _breakers:
        _breakers[name] = CircuitBreaker(name, threshold)
    return _breakers[name]

# Pre-configured breakers
def get_blueprint_breaker(blueprint: str) -> CircuitBreaker:
    return get_breaker(f"blueprint:{blueprint}", threshold=3)

def get_global_breaker() -> CircuitBreaker:
    return get_breaker("global", threshold=5)
```

---

**Status:** All core Forge components specified.
- Teacher agent with fallback behavior
- Atomic checkpoint system with integrity verification
- Crash recovery with automatic restore
- Circuit breaker with per-blueprint + global protection
