# Eval Pipeline Implementation

**Styde Forge v3.0**
**Section:** 03_Forge_Eval
**References:** `Core_Loop_Detail.md` §3, `LLM_as_Judge.md`, `Self_Evaluation_System.md`, `Cross_Judge_Consensus.md`, `Automatic_Validation.md`
**Resolves:** GAP-F04

---

## 1. `scripts/eval_runner.py`

```python
"""
Evaluation pipeline for Styde Forge.
Phase 1: Self-eval + Judge-eval + Composite scoring.
Phase 2+: Cross-judge consensus, bias calibration, Bayesian weights.
"""
import yaml
import time
from pathlib import Path
from datetime import datetime

from persistence import atomic_write, read_yaml

FORGE_ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = FORGE_ROOT / "eval"
BENCHMARKS_DIR = EVAL_DIR / "benchmarks"
RESULTS_DIR = EVAL_DIR / "results"

# --- Self-Evaluation ---

def run_self_eval(agent_id: str, output: str, rubric: dict) -> dict:
    """
    Run self-evaluation.
    
    Phase 1: Parse the self-eval block that the agent appended to its output.
    This is the inline self-eval from Delegate_Task_Integration.md §4.
    
    Returns: {score, dimensions: {...}, notes, parse_status}
    """
    from spawn import extract_self_eval
    
    self_eval = extract_self_eval(output)
    
    # Validate dimensions against rubric
    rubric_dims = set(rubric.get("dimensions", {}).keys())
    eval_dims = set(k for k in self_eval.keys() if k not in ("score", "notes", "error"))
    
    if "error" in self_eval:
        return {
            "score": 0,
            "dimensions": {},
            "notes": f"Self-eval parse error: {self_eval['error']}",
            "parse_status": "failed",
            "source": "parsed_from_output"
        }
    
    # Check dimension coverage
    missing_dims = rubric_dims - eval_dims
    if missing_dims:
        self_eval["notes"] = self_eval.get("notes", "") + f" (missing dims: {missing_dims})"
    
    return {
        "score": self_eval.get("score", 0),
        "dimensions": {k: v for k, v in self_eval.items() if k not in ("score", "notes", "error")},
        "notes": self_eval.get("notes", ""),
        "parse_status": "ok",
        "source": "parsed_from_output"
    }


# --- Judge Evaluation ---

def run_judge_eval(agent_id: str, output: str, rubric: dict, blueprint_name: str = None) -> dict:
    """
    Run independent judge evaluation using deepseek-v4-pro.
    
    The judge is a FRESH subagent with ONLY:
    - Agent output (cleaned, no self-eval block)
    - Rubric
    - Scoring instructions
    
    No blueprint context. No persona. No skills. Clean slate.
    
    Phase 1: Single judge (deepseek-v4-pro, temperature=0.1)
    Phase 2: Multi-judge with cross-consensus
    """
    from spawn import strip_self_eval, _call_delegate_task
    
    # Strip self-eval block so judge evaluates pure output
    clean_output = strip_self_eval(output)
    
    rubric_yaml = yaml.dump(rubric, default_flow_style=False, allow_unicode=True)
    
    judge_prompt = f"""
You are an impartial evaluator. Judge the following agent output against the rubric.

## Agent Output
{clean_output}

## Evaluation Rubric
{rubric_yaml}

## Instructions
1. Score each dimension 0-100.
2. Calculate an overall score 0-100.
3. Provide brief justification for each score.
4. Return ONLY valid YAML in this exact format:

judge_eval:
  score: <0-100>
  correctness: <0-100>
  robustness: <0-100>
  code_quality: <0-100>
  efficiency: <0-100>
  innovation: <0-100>
  documentation: <0-100>
  notes: "<one-line justification>"
"""
    
    result = _call_delegate_task(
        goal="Evaluate agent output against rubric and return YAML scores.",
        context=judge_prompt,
        toolsets=[],  # No tools — judge only evaluates
        timeout=120
    )
    
    if result.get("status") != "success":
        return {
            "score": 0,
            "dimensions": {},
            "notes": f"Judge failed: {result.get('reason', 'unknown')}",
            "model": "deepseek-v4-pro",
            "status": "failed"
        }
    
    # Parse judge output
    judge_output = result.get("output", "")
    judge_eval = _parse_judge_yaml(judge_output)
    judge_eval["model"] = "deepseek-v4-pro"
    judge_eval["status"] = "success"
    judge_eval["tokens"] = result.get("tokens", {})
    judge_eval["duration_ms"] = result.get("duration_ms", 0)
    
    return judge_eval


def _parse_judge_yaml(output: str) -> dict:
    """Parse judge's YAML output."""
    import re
    
    # Try to find YAML block
    yaml_match = re.search(r'judge_eval:(.*?)(?:\n\Z|\Z)', output, re.DOTALL)
    if yaml_match:
        yaml_text = "judge_eval:" + yaml_match.group(1)
    else:
        # Try parsing the whole output
        yaml_text = output
    
    try:
        data = yaml.safe_load(yaml_text)
        if isinstance(data, dict) and "judge_eval" in data:
            je = data["judge_eval"]
            # Clamp scores
            for key in list(je.keys()):
                if isinstance(je[key], (int, float)) and key != "notes":
                    je[key] = max(0, min(100, int(je[key])))
            return {
                "score": je.get("score", 0),
                "correctness": je.get("correctness", 0),
                "robustness": je.get("robustness", 0),
                "code_quality": je.get("code_quality", 0),
                "efficiency": je.get("efficiency", 0),
                "innovation": je.get("innovation", 0),
                "documentation": je.get("documentation", 0),
                "notes": je.get("notes", ""),
            }
    except yaml.YAMLError:
        pass
    
    return {"score": 0, "notes": "unparseable_judge_output", "status": "parse_failed"}


# --- Composite Scoring ---

def calculate_composite(self_eval: dict, judge_eval: dict) -> dict:
    """
    Calculate weighted composite score.
    
    Phase 1 weights:
    - Self-eval: 0.4
    - Judge-eval: 0.6
    
    Phase 2 adds cross-judge consensus and Bayesian weights.
    """
    self_score = self_eval.get("score", 0)
    judge_score = judge_eval.get("score", 0)
    
    composite = (self_score * 0.4) + (judge_score * 0.6)
    composite = round(composite)
    
    # Calculate agreement
    agreement = 1.0 - abs(self_score - judge_score) / 100.0
    
    # Check divergence (triggers cross-judge in Phase 2)
    divergence = abs(self_score - judge_score) > 20
    
    # Get min_pass_score from blueprint config
    min_pass = 70  # Default
    
    return {
        "score": composite,
        "self_score": self_score,
        "judge_score": judge_score,
        "weights": {"self_eval": 0.4, "judge_eval": 0.6},
        "agreement": round(agreement, 2),
        "divergence_detected": divergence,
        "passed": composite >= 70,
        "min_pass_score": 70
    }


# --- Full Eval Runner ---

def run_full_eval(agent_id: str, benchmark_name: str, blueprint_name: str = None) -> dict:
    """
    Run complete evaluation: self-eval + judge-eval + composite.
    Saves results to agent's evals/ directory and eval/results/.
    """
    from forge import AGENTS_DIR, load_state, save_state
    
    # Load rubric
    rubric_path = BENCHMARKS_DIR / benchmark_name / "rubric.yaml"
    if not rubric_path.exists():
        return {"status": "error", "reason": f"Benchmark not found: {benchmark_name}"}
    rubric = read_yaml(rubric_path)
    
    # Load agent output
    agent_dir = AGENTS_DIR / "refinery" / agent_id
    run_dirs = sorted((agent_dir / "runs").glob("run-*"))
    if not run_dirs:
        return {"status": "error", "reason": f"No runs found for agent {agent_id}"}
    
    latest_run = run_dirs[-1]
    output_path = latest_run / "output.md"
    if not output_path.exists():
        return {"status": "error", "reason": f"No output found: {output_path}"}
    
    output = output_path.read_text(encoding="utf-8")
    
    # Self-eval
    print(f"  Self-eval...")
    t0 = time.time()
    self_eval = run_self_eval(agent_id, output, rubric)
    self_duration = int((time.time() - t0) * 1000)
    print(f"    Score: {self_eval['score']} ({self_eval.get('parse_status', '?')}) [{self_duration}ms]")
    
    # Judge-eval
    print(f"  Judge-eval (deepseek-v4-pro, temp=0.1)...")
    t0 = time.time()
    judge_eval = run_judge_eval(agent_id, output, rubric, blueprint_name)
    judge_duration = int((time.time() - t0) * 1000)
    print(f"    Score: {judge_eval['score']} ({judge_eval.get('status', '?')}) [{judge_duration}ms]")
    
    # Composite
    composite = calculate_composite(self_eval, judge_eval)
    status_icon = "PASSED" if composite["passed"] else "FAILED"
    print(f"  Composite: {composite['score']} → {status_icon} (agreement: {composite['agreement']:.0%})")
    
    if composite["divergence_detected"]:
        print(f"  ⚠ High divergence ({abs(self_eval['score'] - judge_eval['score'])}pts). Cross-judge needed in Phase 2.")
    
    # Build eval result
    eval_result = {
        "run_id": latest_run.name,
        "agent_id": agent_id,
        "blueprint": blueprint_name or "unknown",
        "benchmark": benchmark_name,
        "timestamp": datetime.now().isoformat(),
        "self_eval": self_eval,
        "judge_eval": judge_eval,
        "composite": composite,
        "timing": {
            "self_eval_ms": self_duration,
            "judge_eval_ms": judge_duration,
            "total_ms": self_duration + judge_duration
        }
    }
    
    # Save to agent directory
    evals_dir = agent_dir / "evals"
    evals_dir.mkdir(parents=True, exist_ok=True)
    atomic_write(evals_dir / "latest.yaml", yaml.dump(eval_result, default_flow_style=False, allow_unicode=True))
    
    # Save to global results
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    result_path = RESULTS_DIR / f"{agent_id}.yaml"
    atomic_write(result_path, yaml.dump(eval_result, default_flow_style=False, allow_unicode=True))
    
    # Update state
    state = load_state()
    for agent in state.get("agents", []):
        if agent["name"] == agent_id:
            agent["composite_score"] = composite["score"]
            agent["status"] = "eval_pending"
            if composite["passed"]:
                agent["evals_passed"] = agent.get("evals_passed", 0) + 1
            else:
                agent["retries"] = agent.get("retries", 0) + 1
            break
    
    state.setdefault("evaluations", []).append({
        "agent_id": agent_id,
        "blueprint": blueprint_name or "unknown",
        "benchmark": benchmark_name,
        "run_id": latest_run.name,
        "composite_score": composite["score"],
        "passed": composite["passed"],
        "timestamp": datetime.now().isoformat()
    })
    state["total_evaluations"] = len(state["evaluations"])
    save_state(state)
    
    return {"status": "success", "result": eval_result}
```

---

## 2. Benchmark Structure

```
eval/
├── benchmarks/
│   └── <benchmark-name>/
│       ├── task.md          # Task description for the agent
│       └── rubric.yaml      # Scoring rubric
└── results/
    └── <agent-id>.yaml      # Per-agent eval results
```

### Example `rubric.yaml`

```yaml
name: "code-review-basic"
domain: "coding"
description: "Code review benchmark for bug and security detection"

dimensions:
  correctness:
    weight: 0.30
    description: "Correctly identifies all bugs in the code"
    scoring:
      90-100: "All bugs found with correct fixes"
      70-89: "Most bugs found, minor misses"
      50-69: "Some bugs found, significant misses"
      0-49: "Few or no bugs found"
  
  robustness:
    weight: 0.25
    description: "Handles edge cases and error conditions"
    scoring:
      90-100: "All edge cases covered"
      70-89: "Most edge cases covered"
      50-69: "Some edge cases missed"
      0-49: "Edge cases not addressed"
  
  code_quality:
    weight: 0.20
    description: "Quality and clarity of suggested fixes"
    scoring:
      90-100: "Production-quality fixes"
      70-89: "Good fixes, minor improvements possible"
      50-69: "Adequate fixes, needs work"
      0-49: "Poor quality fixes"
  
  efficiency:
    weight: 0.10
    description: "Performance-aware suggestions"
  
  innovation:
    weight: 0.05
    description: "Creative or unexpected improvements"
  
  documentation:
    weight: 0.10
    description: "Clarity of explanations"

min_pass_score: 70
```

---

**Status:** Specification complete. Self-eval, judge-eval, composite scoring.
