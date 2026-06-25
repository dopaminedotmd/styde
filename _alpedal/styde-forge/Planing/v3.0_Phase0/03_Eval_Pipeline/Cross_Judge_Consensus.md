# Cross-Judge Consensus

**Styde Forge v3.0 — Phase 0**
**Section:** 03_Eval_Pipeline

---

## 1. Purpose

Use multiple independent judge models to build consensus, reduce individual
model bias, and increase evaluation reliability. When judges disagree
significantly, a deeper review is triggered.

---

## 2. Consensus Algorithm

```python
def cross_judge_consensus(agent_output, task, rubric,
                          judges=["deepseek-v4-pro", "claude-sonnet-4", "grok-3"]):
    results = []
    for judge_model in judges:
        score = llm_as_judge(agent_output, task, rubric, model=judge_model)
        results.append(score)

    scores = [r["composite_score"] for r in results]
    mean_score = sum(scores) / len(scores)
    variance = sum((s - mean_score)**2 for s in scores) / len(scores)

    return {
        "consensus_score": mean_score,
        "variance": variance,
        "consensus_strength": "high" if variance < 25 else "medium" if variance < 100 else "low",
        "per_judge": results,
        "needs_review": variance > 100
    }
```

---

## 3. Decision Rules

| Variance | Consensus | Action |
|----------|-----------|--------|
| < 25 | High | Use mean score directly |
| 25-100 | Medium | Flag for Teacher review |
| > 100 | Low | Full re-evaluation with more judges |

---

## 4. Integration

- Automatically invoked for all critical evaluations
- Results feed into Bayesian Weight Optimization
- Consensus strength affects weight adjustment magnitude
- Low consensus triggers additional judges

---

**Status:** Implemented.
