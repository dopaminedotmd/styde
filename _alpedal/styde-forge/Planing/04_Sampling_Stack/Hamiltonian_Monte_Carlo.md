# Hamiltonian Monte Carlo

**Styde Forge v3.0 — Phase 0**
**Section:** 04_Sampling_Stack

---

## 1. Purpose

High-quality MCMC sampling using Hamiltonian dynamics and gradient information.
Used as a verification sampler alongside NUTS, and for special calibration runs.

---

## 2. When to Use

| Situation | Method |
|-----------|--------|
| Normal operation | NUTS (automatic) |
| Diagnostic check | HMC (fixed steps, comparable) |
| NUTS divergences detected | HMC verification run |
| Simple posterior | HMC (less overhead than NUTS) |
| Calibration benchmarks | HMC for ground truth |

---

## 3. Core Mechanism

HMC uses physics-inspired dynamics:
1. Sample momentum from N(0, I)
2. Simulate Hamiltonian trajectory via leapfrog integration
3. Accept/reject via Metropolis-Hastings

```python
def hmc_step(position, step_size, num_steps, target_log_prob):
    momentum = np.random.normal(0, 1, len(position))
    current_h = hamiltonian(position, momentum, target_log_prob)

    proposed_pos, proposed_mom = position.copy(), momentum.copy()
    for _ in range(num_steps):
        proposed_pos, proposed_mom = leapfrog(proposed_pos, proposed_mom, step_size)

    proposed_h = hamiltonian(proposed_pos, proposed_mom, target_log_prob)

    if np.random.random() < np.exp(current_h - proposed_h):
        return proposed_pos  # Accept
    return position  # Reject
```

---

## 4. Integration

- **Dual Averaging**: Step size adaptation
- **NUTS**: Primary sampler; HMC is verification
- **Bayesian Weight Optimization**: Used for calibration
- **Historical Learning**: Comparison metrics HMC vs NUTS

---

**Status:** Implemented as verification sampler.
