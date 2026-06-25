# Bias Calibration

**Styde Forge v3.0 — Phase 0**
**Section:** 03_Eval_Pipeline

---

## 1. Purpose

Periodically calibrate the evaluation system against known benchmarks to
detect and correct systematic bias in judge models. All LLM judges have
inherent biases — towards verbosity, certain styles, or specific patterns.

---

## 2. Calibration Process

```python
class BiasCalibrator:
    def __init__(self, calibration_benchmarks: list):
        """benchmarks: List of (output, known_score) with ground truth."""
        self.benchmarks = calibration_benchmarks
        self.bias_factors = {}

    def calibrate(self, judge_model: str) -> float:
        differences = []
        for output, known_score in self.benchmarks:
            judge_score = llm_as_judge(output, "", {}, model=judge_model)
            diff = judge_score["composite_score"] - known_score
            differences.append(diff)

        avg_bias = sum(differences) / len(differences)
        bias_factor = 1.0 - (avg_bias / 100.0)
        # > 1.0 = judge is generous, < 1.0 = judge is strict
        self.bias_factors[judge_model] = bias_factor
        return bias_factor

    def get_calibrated_score(self, raw_score: float, judge_model: str) -> float:
        factor = self.bias_factors.get(judge_model, 1.0)
        return max(0, min(100, raw_score * factor))
```

---

## 3. Calibration Schedule

| Trigger | Frequency |
|---------|-----------|
| System startup | Every time |
| Periodic | Every 50 loop iterations |
| Model change | Immediately |
| Low consensus | Triggered automatically |

---

## 4. Judge Replacement Policy

Judges with persistent bias > 15% across 3+ calibrations are flagged for
replacement. Historical Learning tracks judge reliability over time.

---

**Status:** Implemented.
