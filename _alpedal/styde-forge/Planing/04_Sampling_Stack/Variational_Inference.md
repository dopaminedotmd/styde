# Variational Inference

**Styde Forge v3.0 — Phase 0**
**Section:** 04_Sampling_Stack

---

## 1. Purpose

Fast approximate Bayesian inference optimized for Machine-B. VI trades some
precision for speed — ideal for the high-volume evaluation cycles when
VRAM/RAM is limited.

---

## 2. Algorithm

```python
class VariationalInference:
    def __init__(self, num_iterations=400, learning_rate=0.01):
        self.num_iterations = num_iterations
        self.learning_rate = learning_rate

    def fit(self, alpha_prior: list) -> dict:
        alpha_q = [a + 1.0 for a in alpha_prior]

        for _ in range(self.num_iterations):
            samples = np.random.dirichlet(alpha_q, size=100)
            grad = self._compute_elbo_gradient(alpha_q, alpha_prior, samples)
            alpha_q = [max(a + self.learning_rate * g, 0.01)
                      for a, g in zip(alpha_q, grad)]

        total = sum(alpha_q)
        return {
            "weights": [a / total for a in alpha_q],
            "method": "VI",
            "iterations": self.num_iterations
        }
```

---

## 3. VI vs NUTS Comparison

| Aspect | VI | NUTS |
|--------|-----|------|
| Speed | Seconds | Minutes |
| Precision | Approximate | Exact asymptotically |
| VRAM | Low | Medium-High |
| Default on | Machine-B | Machine-A |
| Uncertainty estimates | No | Yes |

---

## 4. Integration

- Chosen automatically by Hardware Adaptation Layer for Machine-B
- Periodically verified against NUTS when on Machine-A
- Performance comparison stored in Historical Learning

---

**Status:** Primary sampler for Machine-B.
