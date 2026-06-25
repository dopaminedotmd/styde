# Core Loop — Detailed Specification

**Styde Forge v3.0 — Phase 0**
**Section:** 00_Overview

---

## 1. Purpose

Exact step-by-step specification of one complete forge loop iteration.
Every tool call, every prompt, every file written. This is the blueprint
Phase 1 implements.

---

## 2. Prerequisites

- Active hardware profile detected
- Blueprint validated (`validate_blueprint()` passed)
- Benchmark selected with task.md and rubric.yaml
- USB mounted and writable
- Styde Forge running on Hermes Agent v0.17.0+
- DeepSeek API key configured and reachable

---

## 3. Loop Steps

### Step 1: DEFINE

**Input:** Blueprint name (e.g., `code-reviewer`)
**Action:** Load blueprint, validate, prepare spawn context

```
1. Load state.yaml → get forge_version, loop_iterations
2. Load blueprints/<name>/persona.md
3. Load blueprints/<name>/BLUEPRINT.md
4. Load blueprints/<name>/config.yaml
5. Load blueprints/<name>/skills/ (all SKILL.md files)
6. Load eval/benchmarks/<benchmark>/task.md
- Load eval/benchmarks/<benchmark>/rubric.yaml
8. Run RAG retrieval: embed task → search vector store → get top-3 chunks
9. Run validate_blueprint(name) → must pass
10. Get historical context from Historical Learning System
11. Build spawn_context string
```

**Output:** `spawn_context.md`, `spawn_task.md` written to agent directory

---

### Step 2: SPAWN

**Action:** Spawn subagent via `delegate_task`

Caveman Ultra mode is injected into agent context:

```python
# Hermes tool call:
caveman_rules = """
CAVEMAN ULTRA MODE ACTIVE:
- No markdown. Plain text or YAML only.
- No greetings, no sign-offs.
- One line per finding. One word if enough.
- Skip explanations unless confidence < 80%.
- If output is code: just the code.
"""

delegate_task(
    goal=task_content,
    context=caveman_rules + "\n" + spawn_context,
    toolsets=["terminal", "file", "web"]
)
```

**Expected behavior:**
- Subagent runs in isolated context
- Subagent has access to its blueprint skills only
- Subagent produces output following its persona format
- Timeout: 300 seconds (configurable)

**Output:** Agent output saved to `agents/<agent-id>/runs/<run-id>/output.md`

---

### Step 3: EVALUATE

Three sub-steps that run sequentially:

#### 3a: Self-Evaluation

```
Prompt to subagent (or parent simulates):
"Utvärdera din egen output mot följande rubric:
<rubric.yaml content>

Ge poäng 0-100 per dimension med motivering.
Returnera som YAML."
```

**Output:** `self_eval.yaml`

#### 3b: LLM-as-Judge

```python
delegate_task(
    goal="Bedöm följande agent-output mot rubric.",
    context=f"""
## Agent Output
{agent_output}

## Rubric
{rubric_content}

Return scores 0-100 per dimension with justification.
Return as YAML.
""",
    toolsets=["file"]
)
```

**Output:** `judge_eval.yaml`

#### 3c: Cross-Judge Consensus (if variance > 100)

```python
# Run additional judges
for judge_model in ["claude-sonnet-4", "grok-3"]:
    score = llm_as_judge(agent_output, task, rubric, model=judge_model)

# Calculate consensus
consensus = cross_judge_consensus(all_judge_results)
```

**Output:** Updated `judge_eval.yaml` with consensus data

#### 3d: Automatic Validation

```
1. Run automated tests (if applicable)
2. Static analysis (ruff, pylint, mypy)
3. Security scan (basic vulnerability check)
4. Edge case coverage check (≥85%)
5. Resource usage measurement
```

**Output:** Validation report appended to eval

#### 3e: Composite Score

```python
composite_score = (
    self_eval.score * 0.3 +
    judge_eval.score * 0.5 +
    consensus_adjustment * 0.2
)

passed = composite_score >= min_pass_score
```

**Output:** `eval.yaml` with composite score and pass/fail

---

### Step 4: IMPROVE

Conditional on eval results:

#### If PASSED (≥80):
```
1. Extract successful patterns → new skill candidate
2. Run Automatic Version Increment
3. Update blueprint with new version
4. Save to Historical Learning database
5. Log success
```

#### If NEEDS WORK (70-79):
```
1. Teacher analyzes weaknesses from eval
2. Generate concrete improvement suggestions
3. Update blueprint (patch version)
4. Schedule re-spawn with improvements
5. Max 3 retry attempts
```

#### If FAILED (<70):
```
1. Log detailed failure analysis
2. Save lessons to Historical Learning (anti-patterns)
3. Do NOT save agent to USB
4. Agent directory archived or deleted
```

---

### Step 5: CHECKPOINT

```
1. Lock state.yaml
2. Copy all state to checkpoints/checkpoint-YYYYMMDD-HHMMSS/
3. Verify integrity (size + hash + structure)
4. Atomic rename staging → checkpoint
5. Unlock
6. Update state.yaml → last_checkpoint
7. Increment loop_iterations
```

**Output:** New checkpoint directory + updated state.yaml

---

## 4. Loop Execution Modes

### Manual (Phase 1)
```
Human runs each step:
  python scripts/forge.py agent spawn <blueprint> <benchmark>
  → Copy delegate_task to Hermes
  → Wait for agent output
  → python scripts/eval_runner.py run <agent> <benchmark>
  → Copy eval prompts to Hermes
  → python scripts/forge.py checkpoint
```

### Semi-Automated (Phase 2)
```
Single command triggers full loop:
  python scripts/forge.py loop <blueprint> <benchmark>
  → Forge orchestrates all steps via Hermes tool calls
```

### Fully Autonomous (Phase 3)
```
Cron job triggers loop every N minutes:
  hermes cron create "30m" --prompt "Kör forge loop för code-reviewer mot code-review-basic"
```

---

## 5. Loop Metrics (per iteration)

```yaml
loop_id: "loop-20260625-124500"
blueprint: "code-reviewer"
benchmark: "code-review-basic"
iteration: 47

timing:
  define_ms: 120
  spawn_ms: 2340
  self_eval_ms: 850
  judge_eval_ms: 3200
  validation_ms: 450
  improve_ms: 560
  checkpoint_ms: 210
  total_ms: 7730

scores:
  self_eval: 85
  judge_eval: 83
  composite: 83
  delta_vs_previous: 0.12

cost:
  tokens_input: 8400
  tokens_output: 2100
  cost_usd: 0.0032

status: "passed"
```

---

**Status:** Defined. Exact specification for Phase 1 implementation.

---

## 6. Error Handling

Every loop step must handle failures gracefully:

| Step | Failure Mode | Response |
|------|-------------|----------|
| DEFINE | Blueprint not found | Log error, skip to next blueprint |
| DEFINE | Blueprint validation failed | Log validation errors, skip |
| SPAWN | delegate_task timeout (300s) | Retry once. If still timeout: mark agent failed, log |
| SPAWN | API error (429 rate limit) | Wait 5s, retry. Max 3 retries |
| SPAWN | API error (5xx server error) | Wait 10s, retry. Max 2 retries |
| SPAWN | Garbage output (unparseable) | Mark as self_eval=0, send to judge anyway |
| SELF-EVAL | Agent didn't include self-eval | Score=0, flag for teacher review |
| JUDGE-EVAL | Judge API error | Fallback: use self-eval score only |
| JUDGE-EVAL | Judge + self-eval diverge >20pts | Trigger Cross-Judge Consensus |
| IMPROVE | Teacher API error | Skip improvement, use last known good blueprint |
| CHECKPOINT | Disk full | Trigger maintenance. If critical: pause loop |
| CHECKPOINT | USB disconnected | Emergency: save to local temp, alert human |

```python
def loop_with_errors(blueprint: str, benchmark: str) -> dict:
    try:
        # DEFINE
        context = load_blueprint_context(blueprint)
    except BlueprintError as e:
        return {"status": "skipped", "reason": str(e)}

    try:
        # SPAWN (with retry)
        output = spawn_with_retry(context, max_retries=3)
    except SpawnError as e:
        return {"status": "failed", "step": "spawn", "reason": str(e)}

    try:
        # EVALUATE
        self_eval = run_self_eval(output)
    except Exception:
        self_eval = {"score": 0, "error": "self_eval_failed"}

    try:
        judge_eval = run_judge_eval(output)
    except JudgeError:
        judge_eval = {"score": self_eval["score"], "fallback": True}

    composite = calculate_composite(self_eval, judge_eval)

    if composite >= 80:
        try:
            improve(blueprint, composite, judge_eval)
            checkpoint()
        except Exception as e:
            log_error("improve_or_checkpoint_failed", e)

    return {"status": "completed", "score": composite}
```

---

## 7. Circuit Breaker

Prevents cascade failures. If the loop keeps failing, stop — don't waste API money.

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout_min=30):
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
            log_critical(f"Circuit breaker OPEN after {self.failures} failures")

    def record_success(self):
        if self.state == "half_open":
            self.state = "closed"
            self.failures = 0
        elif self.state == "closed":
            self.failures = max(0, self.failures - 1)

    def allow_request(self) -> bool:
        if self.state == "closed":
            return True
        if self.state == "open":
            if time.time() - self.last_failure > self.reset_timeout:
                self.state = "half_open"
                return True
            return False
        return True  # half_open: allow one probe request
```

### Circuit States

| State | Meaning | Action |
|-------|---------|--------|
| **closed** | Normal operation | Allow all requests |
| **open** | Too many failures | Block all requests |
| **half_open** | Testing recovery | Allow one probe request |

### Triggers

| Event | Circuit breaker | Threshold |
|-------|----------------|-----------|
| 3 consecutive eval < 70 | Per-blueprint breaker | 3 failures → open |
| 5 API errors in 10 min | Global breaker | 5 failures → open |
| delegate_task timeout 3× | Per-blueprint breaker | 3 failures → open |
| Disk full | Global breaker | 1 failure → open |

---

## Related Documents

- `Component_Interfaces.md` — How spawn/eval/checkpoint components communicate
- `03_Eval_Pipeline/Self_Evaluation_System.md` — Self-eval step details
- `03_Eval_Pipeline/LLM_as_Judge.md` — Judge eval step details
- `06_Persistence_Safety/Atomic_Checkpoint_Writes.md` — Checkpoint step details
- `10_Operations/Skill_Loading_Mechanism.md` — How skills are loaded at spawn
- `12_Teacher_Agent/Teacher_Agent.md` — Teacher feedback loop
