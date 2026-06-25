# Bayesian Weight Optimization

**Styde Forge v3.0 — Phase 0**
**Section:** 03_Eval_Pipeline

---

## 1. Purpose

Optimize evaluation criterion weights using Bayesian inference.
Static weights are a starting point — real data reveals which criteria
actually predict agent quality.

---

## 2. Weight Model

Six eval criteria with weights summing to 1.0, modeled as Dirichlet:

```
w ~ Dirichlet(α)
α = [25, 20, 20, 15, 10, 10]  (initial concentrations)
```

---

## 3. Sampler Selection

| Hardware | Method | Reason |
|----------|--------|--------|
| Machine-A | NUTS | High precision, enough VRAM |
| Machine-B | VI | Speed over precision, limited VRAM |
| Calibration | HMC | Verification against NUTS |

---

## 4. Weight Evolution Example

```
Cycle   0: [.25, .20, .20, .15, .10, .10]  Default
Cycle  50: [.28, .22, .18, .14, .08, .10]  Robustness↑
Cycle 100: [.30, .24, .17, .12, .07, .10]  Correctness dominates
```

---

## 5. Integration

- Receives data from LLM-as-Judge + Cross-Judge Consensus
- Updated weights used in all subsequent evaluations
- Weight history stored in Historical Learning
- Sampler chosen automatically by Hardware Adaptation Layer

---

**Status:** Implemented.
