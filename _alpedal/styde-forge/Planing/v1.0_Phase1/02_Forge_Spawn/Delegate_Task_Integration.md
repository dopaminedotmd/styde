# Delegate Task Integration

**Styde Forge v3.0**
**Section:** 02_Forge_Spawn
**References:** `Skill_Loading_Mechanism.md`, `Component_Interfaces.md` §3.2, `Core_Loop_Detail.md` §2
**Resolves:** GAP-F01, GAP-F02, GAP-F03

---

## 1. Purpose

This is the exact specification for how Styde Forge spawns agents via Hermes `delegate_task()`. It resolves the three critical gaps identified in Phase 0 gap analysis:

- **GAP-F01:** Exact `delegate_task` parameter contract
- **GAP-F02:** Agent output capture method
- **GAP-F03:** Self-eval mechanism

---

## 2. `delegate_task()` Contract

### 2.1 Hermes Tool Signature

Based on Hermes Agent v0.17.0+ tool definition:

```python
delegate_task(
    goal: str,              # The task description
    context: str,           # System context (persona + skills + rules)
    toolsets: list[str]     # Tools available: ["terminal", "file", "web"]
) -> dict
```

### 2.2 Return Value

```python
# Successful spawn:
{
    "status": "success",
    "agent_id": "subagent-20260625-123000",
    "summary": "Agent completed the code review task...",
    "output": "...",         # Full agent output (may be truncated)
    "tokens": {"input": 1200, "output": 800},
    "duration_ms": 2340
}

# Failed spawn:
{
    "status": "error",
    "reason": "API rate limit exceeded",
    "retry_after_seconds": 5
}

# Timeout:
{
    "status": "timeout",
    "reason": "Agent exceeded 300s timeout"
}
```

### 2.3 Key Behaviors

| Behavior | Detail |
|----------|--------|
| **Context isolation** | Subagent has NO access to parent conversation or memory |
| **Tool access** | Only tools listed in `toolsets` parameter |
| **Timeout** | Default 300s. Configurable per blueprint in config.yaml |
| **Concurrency** | Max 1 on Machine-B, max 3 on Machine-A |
| **Cost** | Counts against parent's API key |
| **Retry** | Parent handles retry logic (not built into delegate_task) |

---

## 3. Agent Output Capture (GAP-F02)

### Decision: Hybrid Approach

The agent writes its output to a known file path AND returns it in the response. This gives us two capture methods with different trade-offs.

### Method A: File-Based Output (Primary)

Agent writes output to a predetermined path using the `write_file` tool:

```python
# In the subagent context, we instruct:
output_path = f"StydeAgents/refinery/{agent_name}/runs/{run_id}/output.md"

# Agent uses write_file tool to save its result
# Parent reads the file after agent completes
```

**Pros:** Full output preserved, no truncation, audit trail
**Cons:** Requires agent to use write_file (cooperative)

### Method B: Return Value (Fallback)

Parse `delegate_task` return value's `output` field:

```python
result = delegate_task(goal=task, context=context, toolsets=toolsets)
if result["status"] == "success":
    output = result.get("output", result.get("summary", ""))
```

**Pros:** Always available
**Cons:** May be truncated, less structured

### Implementation: File-Based with Fallback

```python
def capture_agent_output(agent_dir: Path, run_id: str, delegate_result: dict) -> tuple[str, str]:
    """
    Capture agent output from file or delegate_task return.
    Returns (output_text, source) where source is 'file' or 'return'.
    """
    output_path = agent_dir / "runs" / run_id / "output.md"
    
    # Primary: read from file
    if output_path.exists():
        output = output_path.read_text(encoding="utf-8")
        return output, "file"
    
    # Fallback: use delegate_task return value
    output = delegate_result.get("output", "")
    if output:
        # Save to file for audit trail
        from persistence import atomic_write
        atomic_write(output_path, output)
        return output, "return_saved"
    
    # Last resort: use summary
    return delegate_result.get("summary", ""), "summary_only"
```

---

## 4. Self-Eval Mechanism (GAP-F03)

### Decision: Inline Self-Eval

Self-eval is included in the agent's prompt — it evaluates its own output as part of the task. This avoids a second API call.

### Prompt Injection

After the agent's task description, we append self-eval instructions:

```python
SELF_EVAL_INSTRUCTION = """
## AFTER COMPLETING YOUR TASK

You MUST self-evaluate your output against the rubric below.

**SELF_EVAL format (append to end of output, after a --- separator):**
---
SELF_EVAL:
  score: <0-100 integer>
  correctness: <0-100>
  robustness: <0-100>
  code_quality: <0-100>
  efficiency: <0-100>
  innovation: <0-100>
  documentation: <0-100>
  notes: "<one line explaining your score>"
"""
```

### Parsing Self-Eval from Output

```python
import re, yaml

def extract_self_eval(output: str) -> dict:
    """
    Extract self-evaluation from agent output.
    Agent appends YAML block after '---' separator.
    """
    # Find SELF_EVAL block
    match = re.search(r'---\s*\nSELF_EVAL:(.*?)(?:\n---|\n\Z|\Z)', output, re.DOTALL)
    
    if not match:
        return {"score": 0, "error": "no_self_eval_found"}
    
    try:
        # The captured text may need the 'SELF_EVAL:' prefix stripped
        yaml_text = match.group(1).strip()
        eval_data = yaml.safe_load(yaml_text)
        
        # Validate required fields
        if not isinstance(eval_data, dict) or "score" not in eval_data:
            return {"score": 0, "error": "invalid_self_eval_format"}
        
        # Clamp scores to 0-100
        for key in eval_data:
            if isinstance(eval_data[key], (int, float)):
                eval_data[key] = max(0, min(100, int(eval_data[key])))
        
        return eval_data
        
    except yaml.YAMLError:
        return {"score": 0, "error": "unparseable_self_eval"}
```

### Clean Output (without self-eval)

For judge evaluation, we need the agent's actual output without the self-eval block:

```python
def strip_self_eval(output: str) -> str:
    """Remove self-eval block from output for judge evaluation."""
    match = re.search(r'\n---\s*\nSELF_EVAL:', output)
    if match:
        return output[:match.start()].strip()
    return output
```

---

## 5. Complete Spawn Function

### `scripts/spawn.py`

```python
"""
Agent spawn system for Styde Forge.
Wraps Hermes delegate_task with blueprint context, Caveman Ultra,
RAG context, and output capture.
"""
import time
import yaml
from pathlib import Path
from datetime import datetime

from persistence import atomic_write, atomic_write_json, read_yaml
from blueprint_loader import load_blueprint_context
from blueprint_valid import validate_blueprint

# --- Configuration ---
FORGE_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = FORGE_ROOT / "StydeAgents"
REFINERY_DIR = AGENTS_DIR / "refinery"
MAX_RETRIES = 3
RETRY_DELAYS = [5, 10, 20]  # seconds, exponential-ish

# --- Caveman Ultra Rules ---
CAVEMAN_ULTRA_RULES = """
CAVEMAN ULTRA MODE ACTIVE:
- No markdown. Plain text or YAML only.
- No greetings, no sign-offs, no pleasantries.
- One line per finding. One word if one word is enough.
- Skip explanations unless confidence < 80%.
- If output is code: just the code. No "Here is the code:".
"""

# --- Self-Eval Instructions ---
SELF_EVAL_INSTRUCTION = """
## AFTER COMPLETING YOUR TASK

You MUST self-evaluate your output against the rubric below.

Self-eval format (append to end of output after --- separator):
---
SELF_EVAL:
  score: <0-100>
  correctness: <0-100>
  robustness: <0-100>
  code_quality: <0-100>
  efficiency: <0-100>
  innovation: <0-100>
  documentation: <0-100>
  notes: "<one line>"
"""


def spawn_agent(
    blueprint_name: str,
    task: str,
    rubric: dict,
    context: dict,
    toolsets: list[str] = None,
    timeout: int = 300
) -> dict:
    """
    Spawn a subagent via delegate_task.
    
    Args:
        blueprint_name: Name of the blueprint (e.g., 'code-reviewer')
        task: The benchmark task content
        rubric: The evaluation rubric (dict from rubric.yaml)
        context: Loaded blueprint context (from blueprint_loader)
        toolsets: Tools available to agent (default: ["terminal", "file", "web"])
        timeout: Max seconds for agent to complete
    
    Returns:
        dict with keys: status, agent_id, output_path, duration_ms, tokens, error
    """
    if toolsets is None:
        toolsets = context.get("toolsets", ["terminal", "file", "web"])
    
    # Validate blueprint
    errors = validate_blueprint(blueprint_name)
    if errors:
        return {"status": "validation_failed", "errors": errors}
    
    # Generate agent ID and directory
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    agent_name = f"agent-{blueprint_name}-{timestamp}"
    agent_dir = REFINERY_DIR / agent_name
    run_id = f"run-{timestamp}"
    run_dir = agent_dir / "runs" / run_id
    evals_dir = agent_dir / "evals"
    
    # Create directories
    for d in [run_dir, evals_dir]:
        d.mkdir(parents=True, exist_ok=True)
    
    # Build spawn context
    spawn_context = build_spawn_context(
        blueprint_name=blueprint_name,
        context=context,
        task=task,
        rubric=rubric,
        output_path=str(run_dir / "output.md"),
        caveman_ultra=True  # Always on for Forge agents
    )
    
    # Spawn with retry
    for attempt in range(MAX_RETRIES):
        try:
            result = _call_delegate_task(
                goal=task,
                context=spawn_context,
                toolsets=toolsets,
                timeout=timeout
            )
            
            if result["status"] == "success":
                # Capture output
                output, capture_source = capture_agent_output(
                    agent_dir, run_id, result
                )
                
                # Extract self-eval
                self_eval = extract_self_eval(output)
                clean_output = strip_self_eval(output)
                
                # Extract token usage
                tokens = result.get("tokens", {"input": 0, "output": 0})
                
                # Save agent metadata
                agent_meta = {
                    "name": agent_name,
                    "blueprint": blueprint_name,
                    "run_id": run_id,
                    "status": "eval_pending",
                    "output_path": str(run_dir / "output.md"),
                    "output_size": len(output),
                    "capture_source": capture_source,
                    "self_eval": self_eval,
                    "tokens": tokens,
                    "duration_ms": result.get("duration_ms", 0),
                    "spawned": datetime.now().isoformat(),
                    "model": context.get("config", {}).get("agent", {}).get("model", "unknown"),
                    "attempt": attempt + 1
                }
                
                # Save clean output for judge eval
                atomic_write(run_dir / "output.md", clean_output)
                atomic_write(run_dir / "raw_output.md", output)  # With self-eval
                
                # Save self-eval
                import json
                atomic_write_json(evals_dir / "self_eval.json", self_eval)
                
                # Save agent metadata
                atomic_write_json(agent_dir / "AGENT.json", agent_meta)
                
                # Update state.yaml
                _register_agent_in_state(agent_meta)
                
                return {
                    "status": "success",
                    "agent_id": agent_name,
                    "run_id": run_id,
                    "output_path": str(run_dir / "output.md"),
                    "output_size": len(output),
                    "self_eval_score": self_eval.get("score", 0),
                    "tokens": tokens,
                    "duration_ms": result.get("duration_ms", 0),
                    "attempts": attempt + 1
                }
            
            elif result["status"] == "timeout":
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAYS[min(attempt, len(RETRY_DELAYS) - 1)]
                    print(f"  Timeout (attempt {attempt+1}/{MAX_RETRIES}). Retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                else:
                    return {
                        "status": "timeout",
                        "agent_id": agent_name,
                        "reason": f"Agent timed out after {MAX_RETRIES} attempts",
                        "attempts": MAX_RETRIES
                    }
            
            elif result["status"] == "error":
                reason = result.get("reason", "unknown")
                
                # Rate limit → always retry
                if "rate limit" in reason.lower() or "429" in reason:
                    if attempt < MAX_RETRIES - 1:
                        delay = result.get("retry_after_seconds", RETRY_DELAYS[0])
                        print(f"  Rate limited. Retrying in {delay}s...")
                        time.sleep(delay)
                        continue
                
                # Server error → retry with backoff
                if "5" in reason[:3] or "server error" in reason.lower():
                    if attempt < MAX_RETRIES - 1:
                        delay = RETRY_DELAYS[min(attempt, len(RETRY_DELAYS) - 1)]
                        print(f"  Server error. Retrying in {delay}s...")
                        time.sleep(delay)
                        continue
                
                return {
                    "status": "failed",
                    "agent_id": agent_name,
                    "reason": reason,
                    "attempts": attempt + 1
                }
        
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                delay = RETRY_DELAYS[min(attempt, len(RETRY_DELAYS) - 1)]
                print(f"  Exception: {e}. Retrying in {delay}s...")
                time.sleep(delay)
                continue
            else:
                return {
                    "status": "failed",
                    "agent_id": agent_name,
                    "reason": str(e),
                    "attempts": MAX_RETRIES
                }
    
    return {"status": "failed", "reason": "max_retries_exceeded"}


def build_spawn_context(
    blueprint_name: str,
    context: dict,
    task: str,
    rubric: dict,
    output_path: str,
    caveman_ultra: bool = True
) -> str:
    """
    Build the full context string for delegate_task.
    
    Structure:
    1. Persona (from blueprint)
    2. Blueprint purpose
    3. Skills (from blueprint)
    4. Caveman Ultra rules (if enabled)
    5. Task instructions
    6. Output path instruction
    7. Rubric
    8. Self-eval instruction
    9. Historical context (if available)
    """
    parts = []
    
    # 1. Persona
    parts.append(f"You are a {blueprint_name} agent in the Styde Forge ecosystem.")
    parts.append(f"\n## Your Purpose\n{context.get('blueprint_md', '')}")
    parts.append(f"\n## Your Persona\n{context.get('persona', '')}")
    
    # 2. Skills
    skills = context.get("skills", "")
    if skills:
        parts.append(f"\n## Your Skills\n{skills}")
    
    # 3. Caveman Ultra
    if caveman_ultra:
        parts.append(f"\n{CAVEMAN_ULTRA_RULES}")
    
    # 4. Task
    parts.append(f"\n## Your Task\n{task}")
    
    # 5. Output path
    parts.append(f"\n## Output Instructions")
    parts.append(f"Write your final output to: {output_path}")
    parts.append(f"Use the write_file tool to save your result.")
    
    # 6. Rubric (for self-eval)
    rubric_yaml = yaml.dump(rubric, default_flow_style=False, allow_unicode=True)
    parts.append(f"\n## Evaluation Rubric\n{rubric_yaml}")
    
    # 7. Self-eval instruction
    parts.append(SELF_EVAL_INSTRUCTION)
    
    # 8. Historical context
    history = context.get("history", "")
    if history:
        parts.append(f"\n## Historical Context\n{history}")
    
    return "\n".join(parts)


def _call_delegate_task(goal: str, context: str, toolsets: list[str], timeout: int) -> dict:
    """
    Wrapper around Hermes delegate_task.
    
    In production, this calls the Hermes tool API.
    For now, the parent Hermes agent calls delegate_task() directly.
    The Forge scripts are run BY Hermes, so delegate_task is available.
    
    When running forge.py as a standalone script (not inside Hermes),
    this function is a stub that logs the call. The actual spawn happens
    when the parent Hermes agent reads the forge output and makes the call.
    """
    # NOTE: This function is called FROM INSIDE the Hermes agent context.
    # It uses the agent's built-in delegate_task tool.
    # When forge.py is run standalone (for testing), we mock this.
    
    try:
        # In Hermes context, delegate_task is available as a tool
        # The agent calling this script has delegate_task in its toolset
        result = delegate_task(  # noqa: F821 — Hermes built-in
            goal=goal,
            context=context,
            toolsets=toolsets
        )
        return result
    except NameError:
        # Standalone mode: log the call and return mock
        import json
        log_path = FORGE_ROOT / "logs/spawn_calls.jsonl"
        call = {
            "timestamp": datetime.now().isoformat(),
            "goal": goal[:200],
            "toolsets": toolsets,
            "timeout": timeout,
            "mode": "standalone_stub"
        }
        with open(log_path, "a") as f:
            f.write(json.dumps(call) + "\n")
        
        return {
            "status": "stub",
            "reason": "Not running inside Hermes. deploy_task call logged.",
            "log_path": str(log_path)
        }


# --- Output Capture ---

def capture_agent_output(agent_dir: Path, run_id: str, delegate_result: dict) -> tuple[str, str]:
    """Capture agent output. Returns (output_text, source)."""
    output_path = agent_dir / "runs" / run_id / "output.md"
    
    if output_path.exists():
        return output_path.read_text(encoding="utf-8"), "file"
    
    output = delegate_result.get("output", "")
    if output:
        atomic_write(output_path, output)
        return output, "return_saved"
    
    return delegate_result.get("summary", ""), "summary_only"


# --- Self-Eval ---

import re

def extract_self_eval(output: str) -> dict:
    """Extract self-evaluation YAML from agent output."""
    match = re.search(r'---\s*\nSELF_EVAL:(.*?)(?:\n---|\n\Z|\Z)', output, re.DOTALL)
    
    if not match:
        return {"score": 0, "error": "no_self_eval"}
    
    try:
        eval_data = yaml.safe_load(match.group(1).strip())
        if not isinstance(eval_data, dict) or "score" not in eval_data:
            return {"score": 0, "error": "invalid_format"}
        
        for key in list(eval_data.keys()):
            if isinstance(eval_data[key], (int, float)):
                eval_data[key] = max(0, min(100, int(eval_data[key])))
        
        return eval_data
    except yaml.YAMLError:
        return {"score": 0, "error": "unparseable"}


def strip_self_eval(output: str) -> str:
    """Remove self-eval block for judge evaluation."""
    match = re.search(r'\n---\s*\nSELF_EVAL:', output)
    if match:
        return output[:match.start()].strip()
    return output


# --- State Management ---

def _register_agent_in_state(agent_meta: dict):
    """Add agent to state.yaml."""
    from forge import load_state, save_state
    
    state = load_state()
    
    agent_entry = {
        "name": agent_meta["name"],
        "blueprint": agent_meta["blueprint"],
        "version": 1,
        "stage": "refinery",
        "status": "eval_pending",
        "path": str(REFINERY_DIR / agent_meta["name"]),
        "composite_score": None,
        "evals_passed": 0,
        "spawned": agent_meta["spawned"],
        "run_id": agent_meta["run_id"],
        "tokens": agent_meta["tokens"],
        "model": agent_meta.get("model", "unknown")
    }
    
    state.setdefault("agents", []).append(agent_entry)
    state["total_agents_spawned"] = len(state["agents"])
    
    # Add blueprint if new
    bp_names = [b["name"] for b in state.get("blueprints", [])]
    if agent_meta["blueprint"] not in bp_names:
        state.setdefault("blueprints", []).append({
            "name": agent_meta["blueprint"],
            "version": 1,
            "status": "testing",
            "domain": agent_meta.get("domain", "unknown"),
            "last_eval_score": None,
            "created": agent_meta["spawned"]
        })
    
    save_state(state)
```

---

## 6. Test Scenarios

### Test 1: Successful Spawn
```bash
python forge.py spawn code-reviewer code-review-basic
# Expect: agent-<name> created in refinery/
# Expect: output.md written with review content
# Expect: self_eval.json with score > 0
# Expect: agent registered in state.yaml
```

### Test 2: Self-Eval Extraction
```python
output = """
L14: SQL injection. Fix: parameterized queries.
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
eval = extract_self_eval(output)
assert eval["score"] == 85
assert eval["correctness"] == 90
```

### Test 3: Missing Self-Eval
```python
output = "Just some code review output."
eval = extract_self_eval(output)
assert eval["score"] == 0
assert eval["error"] == "no_self_eval"
```

### Test 4: Rate Limit Retry
```python
# Simulate 429 response
# Expect: 3 retries with 5s/10s/20s delays
# Expect: eventual success or final failure
```

---

## 7. Operational Notes

### Running forge.py standalone vs inside Hermes

| Mode | delegate_task | Use case |
|------|--------------|----------|
| **Inside Hermes** | Real call via Hermes tool API | Production |
| **Standalone** | Stub that logs the call | Testing, debugging |

To run forge.py standalone (testing spawn logic without actual API calls):
```bash
python forge.py spawn code-reviewer code-review-basic
# Logs: logs/spawn_calls.jsonl
# Creates: agent directory structure
# No API cost
```

To run forge.py inside Hermes (actual agent spawn):
```
Hermes prompt: "Run forge.py spawn code-reviewer code-review-basic"
→ Hermes executes the Python script
→ delegate_task is available as a Hermes tool
→ Real agent is spawned with API call
```

---

**Status:** Specification complete. This resolves GAP-F01, F02, F03.
