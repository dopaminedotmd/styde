# NUTS Algorithm (No-U-Turn Sampler)

**Styde Forge v3.0 — Phase 0**
**Section:** 04_Sampling_Stack

---

## 1. Purpose

Deliver the most efficient, adaptive MCMC sampling for Bayesian Weight
Optimization on Machine-A. NUTS automatically determines optimal trajectory
length and step size — no manual tuning needed.

---

## 2. Core Algorithm

```python
class NUTS:
    def __init__(self, target_log_prob_fn, target_accept=0.8, max_tree_depth=10):
        self.target_log_prob = target_log_prob_fn
        self.dual_averaging = DualAveraging(target_accept)
        self.max_tree_depth = max_tree_depth

    def build_tree(self, position, momentum, step_size, direction, depth):
        if depth == 0:
            new_pos, new_mom = leapfrog_step(position, momentum, step_size)
            return new_pos, new_mom, hamiltonian(new_pos, new_mom)
        # Recursive tree building with U-turn detection
        left = self.build_tree(position, momentum, step_size, direction, depth-1)
        right = self.build_tree(left.pos, left.mom, step_size, direction, depth-1)
        if is_u_turn(left.pos, right.pos, left.mom, right.mom):
            return None
        return right
```

---

## 3. Usage

| Context | Settings |
|---------|----------|
| Machine-A | NUTS, depth 10-12, 2800 samples |
| High uncertainty | NUTS, depth 11 |
| Critical domains | NUTS, depth 12 |
| Calibration | NUTS, depth 12, 3500 samples |

---

## 4. Diagnostics

- **ESS** (Effective Sample Size): Target > 0.7 per sample
- **Divergences**: 0 is ideal, < 3 acceptable
- **Accept rate**: Target 0.75-0.85
- **Tree depth**: Auto-optimized by Dynamic Tree Depth Adjustment

---

**Status:** Refined & final. Primary sampler for Machine-A.
