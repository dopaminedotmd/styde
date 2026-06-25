# Automatic Validation

**Styde Forge v3.0 — Phase 0**
**Section:** 03_Eval_Pipeline

---

## 1. Purpose

The last line of defense before anything reaches the USB. A multi-layer
validation pipeline combining automated tests, benchmarks, self-evaluation,
and teacher review.

---

## 2. Validation Pipeline

### Stage 1: Pre-Validation (Lightweight)
- Syntax check
- Basic functionality (smoke tests)
- File format validation

### Stage 2: Automated Technical Validation
- Code execution in sandbox
- Static analysis (ruff, pylint, mypy, eslint)
- Security scan (basic vulnerability detection)
- Benchmarks (standard + custom)
- Resource usage measurement (VRAM/RAM/CPU)

### Stage 3: Quality & Intelligence Validation
- Self-Evaluation from agent
- LLM-as-Judge (Parent + secondary model)
- Historical Consistency Check (vs. previous generations)
- Edge Case Coverage (≥ 85% must pass)

### Stage 4: Teacher Final Review
- Parent makes final judgment
- Approves or sends back for iteration (max 3 attempts)

---

## 3. Decision Rules

```json
{
  "total_score": 83,
  "required": 80,
  "status": "APPROVED",
  "blocking_issues": [],
  "warnings": ["Slight token overconsumption"],
  "decision_reason": "All technical tests passed. Self-eval and teacher agree. Delta +0.12 vs previous generation."
}
```

| Score | Action |
|-------|--------|
| ≥ 80 | Approved → atomic write to USB |
| 70-79 | Iteration required (max 3) |
| < 70 | Rejected → lessons saved to Historical Learning |

---

## 4. Integration

- Dynamic Model Selector: Validates that model choice delivered expected performance
- Historical Learning: All validation results feed into learning
- Self-Evaluation: Consistency check between self-score and automated results
- Teacher Loop: Detailed report for feedback generation

---

**Status:** Implemented. Final quality gate.
