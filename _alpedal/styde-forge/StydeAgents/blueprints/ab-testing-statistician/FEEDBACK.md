
---

---
## Feedback from 20260626-063439 (score: 63.2/100)
**Weakest:** usefulness | **Cause:** Agent produced a static API reference instead of an executable, decision-guiding interaction — spec sheet, not a tool. | **Severity:** critical
**Changes:**
- **BLUEPRINT.md**: Add an execution requirement: every method MUST include an inline working implementation (e.g. print actual sample sizes, compute SE, output formatted result), not just parameter docs. _(impact: high)_
- **persona.md**: Insert rule: 'Before calling a math/stats method, ALWAYS include a worked example that prints the computed output in context.' _(impact: high)_
- **BLUEPRINT.md**: Add a 'decision tree' section: given input parameters (sample sizes, baseline rate, MDE), show which AB-testing method is appropriate and why. _(impact: medium)_
**Summary:** Blueprint produces correct descriptions but zero executable value — fix the persona and blueprint to demand runnable code and decision logic, not static documentation.

---

---
## Feedback from 20260626-063917 (score: 86.2/100)
**Weakest:** completeness | **Cause:** Bayesian sample size derivation was circular (used posterior N instead of power-based N) and frequentist intermediate rounding was premature — both are gaps in completing the full methodological chain. | **Severity:** medium
**Changes:**
- **BLUEPRINT.md**: Add a 'sample size derivation' stage that forces explicit power calculation (alpha, beta, MDE) before any Bayesian posterior computation, with a validation cross-check between frequentist and Bayesian approaches. _(impact: high)_
**Summary:** Strong multi-method reasoning held back by a circular Bayesian sample-size shortcut — fix the derivation chain and this crosses production threshold comfortably.
