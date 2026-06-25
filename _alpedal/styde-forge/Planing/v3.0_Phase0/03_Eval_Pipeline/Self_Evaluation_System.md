# Self-Evaluation System

**Styde Forge v3.0 — Phase 0**
**Section:** 03_Eval_Pipeline

---

## 1. Purpose

A two-layer reflective system: agents evaluate their own output before
submission, and the Parent evaluates the entire meta-process.

---

## 2. Agent-Level Self-Eval

Every subagent must complete a self-evaluation before returning results:

```markdown
### Self-Evaluation (Agent X)

**Task:** [original task]
**Model:** [model used]

**Self-Assessment (0-100):**
- Functional Correctness: __/100
- Robustness & Edge Cases: __/100
- Code Quality / Maintainability: __/100
- Efficiency: __/100
- Innovation & Elegance: __/100
- Documentation: __/100

**Total Self-Score:** __/100

**Strengths:** ...
**Weaknesses:** ...
**Alternative approaches considered:** ...
**Lessons for future agents:** ...
```

---

## 3. Meta-Level Self-Eval (Parent)

Parent evaluates after each major cycle:

- How accurate was the model selection?
- How effective was the teacher feedback?
- Which Historical Learning patterns led to the most improvement?
- What is the current meta-score for the entire reactor?

```json
{
  "cycle": 47,
  "meta_score": 87,
  "model_selection_accuracy": 0.91,
  "strongest_improvement_area": "real_time_architecture",
  "recommended_meta_skills": ["better_prompt_framing_v5"],
  "system_health": "strong"
}
```

---

## 4. Integration

- Self-eval data feeds Dynamic Model Selector
- Historical Learning stores all self-evaluations
- Teacher Loop uses agent self-eval as feedback signal
- Consistency between self-eval and judge-eval tracked as metric

---

**Status:** Implemented.
