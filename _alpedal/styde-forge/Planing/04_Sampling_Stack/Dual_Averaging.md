# Dual Averaging

**Styde Forge v3.0 — Phase 0**
**Section:** 04_Sampling_Stack

---

## 1. Purpose

Automatically adapt step_size in HMC/NUTS to reach target acceptance ratio
(~0.8). Uses exponentially weighted averaging for stable convergence.

---

## 2. Algorithm

```
η_{t+1} = η_t + α_t · (target_accept − accept_rate_t)
step_size_{t+1} = exp(η_{t+1} − γ · avg_accept)
```

With adaptive α_t = γ / (t + t₀).

---

## 3. Implementation

```python
class DualAveraging:
    def __init__(self, target_accept=0.8, gamma=0.05, t0=10, kappa=0.75):
        self.mu = 0.0
        self.log_step_size = math.log(0.1)
        self.avg_accept = target_accept
        self.iter = 0

    def update(self, accept_rate: float) -> float:
        self.iter += 1
        eta = 1.0 / (self.iter + self.t0)
        self.avg_accept = (1 - eta) * self.avg_accept + eta * accept_rate
        self.mu -= (self.gamma / (self.iter + self.t0)) * (self.avg_accept - self.target_accept)
        self.log_step_size = self.mu - self.gamma * self.avg_accept * self.kappa
        self.step_size = max(math.exp(self.log_step_size), 1e-5)
        return self.step_size
```

---

## 4. Integration

- Called after every accept/reject in NUTS/HMC
- Stabilizes quickly during burn-in
- Diagnostics fed to Historical Learning

---

**Status:** Final. Embedded in NUTS and HMC.
