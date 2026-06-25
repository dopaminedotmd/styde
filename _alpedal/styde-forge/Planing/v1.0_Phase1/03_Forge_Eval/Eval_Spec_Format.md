# Eval Spec Format — Binary Checks + Golden Cases + Rollout

**Styde Forge v3.0**
**Section:** 03_Forge_Eval
**Source:** Adapted from agent-skill-creator v6.0.0 eval system
**Replaces:** Rubric-only eval (rubric.yaml)

---

## 1. Purpose

Replace dimension-based rubrics with concrete, automatable eval specs. Every agent benchmark is a regression test suite: binary checks (pass/fail assertions) + golden cases (known input → expected output pairs) + rollout (run agent on golden inputs, score real output).

This is the **loss function** for Forge agents. The eval loop optimizes against it.

---

## 2. Format: `eval/<benchmark>/eval.yaml`

```yaml
name: "code-review-basic"
domain: "coding"
version: 1
created: "2026-06-25"

# Binary checks are pass/fail assertions.
# command: shell command returning 0=pass, non-zero=fail
# llm_judge: true = LLM evaluates this check (slower, for qualitative checks)
binary_checks:
  - id: "sql-injection"
    description: "Detects SQL injection in f-string queries"
    command: null
    llm_judge: true
    severity: "critical"
    
  - id: "hardcoded-credentials"
    description: "Flags hardcoded passwords and API keys"
    command: null
    llm_judge: true
    severity: "critical"
    
  - id: "edge-case-null"
    description: "Handles null/empty input without crashing"
    command: null
    llm_judge: true
    severity: "major"
    
  - id: "output-is-yaml"
    description: "Output is valid YAML"
    command: "python -c \"import yaml, sys; yaml.safe_load(open(sys.argv[1])); print('OK')\" {output_path}"
    llm_judge: false
    severity: "minor"
    
  - id: "no-markdown"
    description: "Output contains no markdown formatting (Caveman Ultra)"
    command: "grep -q '```' {output_path}; test $? -eq 1"
    llm_judge: false
    severity: "minor"

# Golden cases: known inputs with expected outputs.
# status: active (enforced) | pending-first-green (baseline not yet captured)
golden_cases:
  - id: "case-1-simple"
    description: "Simple function with SQL injection and hardcoded password"
    input: "golden/case-1/input.py"
    expected: "golden/case-1/expected.yaml"
    status: "active"
    
  - id: "case-2-edge-cases"
    description: "Code with null handling and edge cases"
    input: "golden/case-2/input.py"
    expected: "golden/case-2/expected.yaml"
    status: "active"
    
  - id: "case-3-empty-input"
    description: "Empty file — agent should report no issues"
    input: "golden/case-3/input.py"
    expected: "golden/case-3/expected.yaml"
    status: "active"

# Scoring
min_pass_score: 70
min_binary_checks_passed: 4    # At least 4 of 5 binary checks must pass
min_golden_cases_passed: 2     # At least 2 of 3 golden cases must match

# Rollout scoring weights
rollout_weights:
  binary_checks: 0.5           # Binary checks contribute 50% of score
  golden_cases: 0.3            # Golden case matches contribute 30%
  llm_judge: 0.2               # LLM judge score contributes 20%
```

---

## 3. Rollout Runner

### `run_evals.py --rollout`

```python
"""
Run agent on golden inputs and score real output.
Exit code 0 = all checks pass, non-zero = failure.
"""
import sys
import yaml
import subprocess
from pathlib import Path
import json

def run_binary_check(check: dict, output_path: Path) -> bool:
    """Run a binary check. Returns True if passed."""
    if check.get("command"):
        cmd = check["command"].format(output_path=str(output_path))
        result = subprocess.run(cmd, shell=True, capture_output=True)
        return result.returncode == 0
    return True  # LLM-judge checks handled separately

def run_golden_case(case: dict, agent_output: str) -> bool:
    """Compare agent output against expected golden output."""
    expected_path = Path(case["expected"])
    if not expected_path.exists():
        return False
    
    expected = yaml.safe_load(expected_path.read_text())
    
    # Try parsing agent output as YAML
    try:
        actual = yaml.safe_load(agent_output)
    except yaml.YAMLError:
        return False
    
    # Fuzzy match (not exact — allows minor differences)
    return _fuzzy_match(expected, actual)

def _fuzzy_match(expected: dict, actual: dict, threshold: float = 0.8) -> bool:
    """Compare two dicts with tolerance for minor differences."""
    if not isinstance(actual, dict):
        return False
    
    matches = 0
    total = len(expected)
    
    for key, exp_val in expected.items():
        if key in actual:
            act_val = actual[key]
            if isinstance(exp_val, list) and isinstance(act_val, list):
                if len(act_val) >= len(exp_val) * threshold:
                    matches += 1
            elif isinstance(exp_val, str) and isinstance(act_val, str):
                if exp_val.lower() in act_val.lower():
                    matches += 1
            else:
                if exp_val == act_val:
                    matches += 1
    
    return matches / max(total, 1) >= threshold

def run_rollout(benchmark_name: str, agent_output_path: str) -> dict:
    """
    Run full rollout evaluation.
    
    1. Load eval spec
    2. Run all binary checks (except llm_judge)
    3. Run all golden cases
    4. Calculate composite score
    5. Return results
    
    Returns dict with: passed, score, binary_results, golden_results, details
    """
    benchmark_dir = Path(f"eval/benchmarks/{benchmark_name}")
    eval_spec = yaml.safe_load((benchmark_dir / "eval.yaml").read_text())
    output_path = Path(agent_output_path)
    agent_output = output_path.read_text(encoding="utf-8")
    
    results = {
        "binary_checks": [],
        "golden_cases": [],
        "passed": True,
        "score": 0,
        "details": {}
    }
    
    # Binary checks (non-LLM)
    binary_passed = 0
    binary_total = 0
    for check in eval_spec["binary_checks"]:
        if check.get("llm_judge"):
            continue  # LLM-judge checks handled in evaluate.py
        
        binary_total += 1
        passed = run_binary_check(check, output_path)
        if passed:
            binary_passed += 1
        results["binary_checks"].append({
            "id": check["id"],
            "passed": passed,
            "severity": check.get("severity", "minor")
        })
    
    # Golden cases
    golden_passed = 0
    golden_total = 0
    for case in eval_spec.get("golden_cases", []):
        if case.get("status") != "active":
            continue
        
        golden_total += 1
        passed = run_golden_case(case, agent_output)
        if passed:
            golden_passed += 1
        results["golden_cases"].append({
            "id": case["id"],
            "passed": passed
        })
    
    # Composite (rollout portion only — llm_judge added by evaluate.py)
    weights = eval_spec.get("rollout_weights", {
        "binary_checks": 0.5,
        "golden_cases": 0.3,
        "llm_judge": 0.2
    })
    
    binary_score = (binary_passed / max(binary_total, 1)) * 100 if binary_total > 0 else 100
    golden_score = (golden_passed / max(golden_total, 1)) * 100 if golden_total > 0 else 100
    
    rollout_score = int(
        binary_score * weights["binary_checks"] +
        golden_score * weights["golden_cases"]
    )
    
    results["score"] = rollout_score
    results["details"] = {
        "binary_checks_passed": f"{binary_passed}/{binary_total}",
        "golden_cases_passed": f"{golden_passed}/{golden_total}",
        "binary_score": binary_score,
        "golden_score": golden_score,
        "rollout_score": rollout_score
    }
    
    # Check minimum thresholds
    min_binary = eval_spec.get("min_binary_checks_passed", 0)
    min_golden = eval_spec.get("min_golden_cases_passed", 0)
    
    if binary_total > 0 and binary_passed < min_binary:
        results["passed"] = False
    if golden_total > 0 and golden_passed < min_golden:
        results["passed"] = False
    
    return results


def run_rollout_promote(benchmark_name: str, agent_output_path: str):
    """
    Run rollout and capture the first passing baseline.
    If golden cases are 'pending-first-green', promote them to 'active'
    and save the agent's output as the expected.
    """
    benchmark_dir = Path(f"eval/benchmarks/{benchmark_name}")
    eval_spec = yaml.safe_load((benchmark_dir / "eval.yaml").read_text())
    
    for case in eval_spec.get("golden_cases", []):
        if case.get("status") == "pending-first-green":
            output_path = Path(agent_output_path)
            expected_path = benchmark_dir / case["expected"]
            
            # Copy agent output as golden expected
            expected_path.parent.mkdir(parents=True, exist_ok=True)
            expected_path.write_text(output_path.read_text(encoding="utf-8"))
            
            case["status"] = "active"
    
    # Update eval spec
    (benchmark_dir / "eval.yaml").write_text(
        yaml.dump(eval_spec, default_flow_style=False, allow_unicode=True)
    )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: run_evals.py <benchmark> <agent_output_path> [--promote] [--rollout]")
        sys.exit(1)
    
    benchmark = sys.argv[1]
    output_path = sys.argv[2]
    promote = "--promote" in sys.argv
    
    if promote:
        run_rollout_promote(benchmark, output_path)
        print("PROMOTED: pending-first-green cases now active")
    else:
        result = run_rollout(benchmark, output_path)
        print(f"Score: {result['score']} ({'PASS' if result['passed'] else 'FAIL'})")
        print(f"  Binary: {result['details']['binary_checks_passed']}")
        print(f"  Golden: {result['details']['golden_cases_passed']}")
        sys.exit(0 if result["passed"] else 1)
```

---

## 4. Golden Case Directory Structure

```
eval/benchmarks/<name>/
├── eval.yaml                    # Eval spec (binary checks + golden cases)
├── task.md                      # Task description for the agent
│
└── golden/                      # Golden case data
    ├── case-1/
    │   ├── input.py             # Input file for the agent
    │   └── expected.yaml        # Expected output
    ├── case-2/
    │   ├── input.py
    │   └── expected.yaml
    └── case-3/
        ├── input.py
        └── expected.yaml
```

---

## 5. Integration with Forge Eval Loop

```
OLD (rubric only):
  spawn → self-eval → judge-eval → composite

NEW (binary + golden + judge):
  spawn → self-eval → ROLLOUT (binary + golden) → judge-eval → composite
             ↓                                         ↓
       parsed from output                    LLM scores remaining checks
             ↓                                         ↓
       self_score (40%)             rollout_score (30%) + judge_score (30%)
                                              ↓
                                     COMPOSITE = weighted sum
                                              ↓
                                     PASS if ≥ min_pass_score
```

### Updated Composite Formula

```python
composite = (
    self_eval.score * 0.3 +       # Agent's own assessment
    rollout_result.score * 0.3 +  # Binary checks + golden cases (deterministic)
    judge_eval.score * 0.4         # LLM judge on remaining checks
)
```

---

## 6. Comparison: Old vs New

| Aspect | Old (Rubric) | New (Binary + Golden) |
|--------|-------------|----------------------|
| Determinism | Subjective (LLM) | Partially deterministic (binary checks) |
| Regression | None | Golden cases catch regressions |
| CI-ready | No | `run_evals.py` exits non-zero on failure |
| Auto-optimizable | No | Consumable by optimization tools |
| Edge cases | Implicit in rubric | Explicit in golden cases |
| Baseline capture | Manual | `--promote` flag auto-captures |
| Security checks | None | Built-in: SQL injection, credentials |

---

**Status:** Defined. Replaces rubric.yaml with eval.yaml. Adopted from agent-skill-creator v6.0.0.
