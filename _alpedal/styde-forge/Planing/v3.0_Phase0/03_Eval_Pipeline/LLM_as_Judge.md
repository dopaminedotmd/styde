# LLM-as-Judge

**Styde Forge v3.0 — Phase 0**
**Section:** 03_Eval_Pipeline

---

## 1. Purpose

Use a separate, powerful model to evaluate subagent output against a defined
rubric on multiple dimensions. The judge is independent of the agent being
evaluated — eliminating self-evaluation bias.

The judge uses `deepseek-v4-pro` for maximum evaluation quality.
Judge model selection is NOT dynamic — eval quality must never be compromised.

All eval output follows Caveman Ultra format: minimal text, YAML where possible,
no markdown, no fluff. Judge receives raw agent output, returns structured scores.

---

## 2. Weighted Eval Template (100 points)

| Criterion | Weight | Method |
|-----------|--------|--------|
| Functional Correctness | 25% | Test cases + execution |
| Robustness & Edge Cases | 20% | Automated edge-case suite |
| Code Quality / Maintainability | 20% | Static analysis + LLM-judge |
| Efficiency & Scalability | 15% | Benchmarks + resource usage |
| Innovation & Elegance | 10% | Teacher + LLM-judge |
| Documentation & Traceability | 10% | Manual + automated review |

---

## 3. Judge Invocation

```python
def llm_as_judge(agent_output: str, task: str, rubric: dict,
                 judge_model: str = "deepseek-v4-pro") -> dict:
    prompt = f"""
    You are an impartial judge evaluating AI agent output.

    TASK: {task}
    OUTPUT: {agent_output}
    RUBRIC: {rubric}

    Score each dimension (0-100) with justification.
    Return structured JSON.
    """
    result = call_model(model=judge_model, prompt=prompt, temperature=0.1)
    return parse_judge_response(result)
```

---

## 4. Example Output

```json
{
  "judge_model": "deepseek-v4-pro",
  "composite_score": 83,
  "passed": true,
  "dimensions": {
    "correctness": {"score": 90, "notes": "All tests pass"},
    "robustness": {"score": 75, "notes": "Misses empty input edge case"},
    "code_quality": {"score": 85, "notes": "Clean, well-structured"},
    "efficiency": {"score": 80, "notes": "Acceptable"},
    "innovation": {"score": 82, "notes": "Solid approach"},
    "documentation": {"score": 88, "notes": "Well-documented"}
  }
}
```

---

## 5. Quality Gates

| Score | Action |
|-------|--------|
| ≥85×3 | Promoted → production |
| ≥80 | Approved → stays in refinery |
| 70-79 | Iterate (max 3) |
| <70 | Rejected → archive |

---

**Status:** Implemented. Primary evaluation layer.

---

## Related Documents

- `Cross_Judge_Consensus.md` — Multi-judge validation
- `Bias_Calibration.md` — Judge bias detection and correction
- `Bayesian_Weight_Optimization.md` — Weight updates from judge scores
- `Self_Evaluation_System.md` — Agent self-assessment (paired with judge)
- `Automatic_Validation.md` — Technical validation layer
