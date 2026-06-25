# Tree Depth Optimization

**Styde Forge v3.0 — Phase 0**
**Section:** 04_Sampling_Stack

---

## 1. Purpose

Dynamically adjust NUTS tree depth in real-time based on current performance,
hardware, uncertainty, and domain — balancing sampling quality with
computational cost.

---

## 2. Adjustment Rules

| Factor | Depth Change | Reason |
|--------|-------------|--------|
| High ESS / good mixing | +1 or +2 | Can explore more |
| Many divergences | -2 | Trajectory too long |
| High computation time | -1 | Reduce cost |
| High posterior variance | +1 | Need better exploration |
| Machine-B | Cap at 8-9 | Hardware limit |
| Stable domain with lots of data | -1 | Already converged |

---

## 3. Implementation

```python
class DynamicTreeDepthAdjuster:
    def __init__(self, initial_depth=8, min_depth=5, max_depth=12):
        self.current_depth = initial_depth

    def adjust(self, metrics: dict) -> int:
        score = 0.0

        if metrics["ess"] > 0.75:      score += 1.5
        if metrics["accept_rate"] > 0.78: score += 0.8
        if metrics["divergences"] > 2:  score -= 2.5
        if metrics["time_per_sample"] > 0.7: score -= 1.8
        if metrics.get("posterior_variance", 0) > 0.25: score += 1.2

        if metrics["hardware"] == "B":
            self.max_depth = min(self.max_depth, 9)

        if score > 1.2 and self.current_depth < self.max_depth:
            self.current_depth += 1
        elif score < -1.2 and self.current_depth > self.min_depth:
            self.current_depth -= 1

        return self.current_depth
```

---

## 4. Default Depths

| Hardware | Default | Range |
|----------|---------|-------|
| Machine-A | 10-11 | 7-12 |
| Machine-B | 8 | 5-9 |

---

**Status:** Implemented. Self-calibrating NUTS depth.
