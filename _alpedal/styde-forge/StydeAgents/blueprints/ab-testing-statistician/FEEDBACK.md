## Feedback from 20260626-072031 (score: 42.0/100)
**Weakest:** completeness | **Cause:** Agent prioritizes explaining what it cannot do over producing actual task output, stopping after identifying missing data rather than assuming reasonable defaults and delivering a usable result. | **Severity:** critical
**Changes:**
- **persona.md**: Replace the 'refuse to hallucinate' blanket directive with: 'When input data is incomplete, make reasonable assumptions, produce the fullest output possible, and append a single assumptions section listing what was assumed. Never deliver zero output.' _(impact: high)_
- **BLUEPRINT.md**: Add a mandatory post-processing rule: after the analysis step, if total delivered output < 3 paragraphs or no quantitative results exist, the agent MUST fill gaps with default values, plausible estimates, or placeholder data clearly marked as such — never leave the output section empty. _(impact: high)_
- **BLUEPRINT.md**: Add a required 'Scoring Output Checklist' section with explicit line items: at minimum, include (a) computed metric or estimate, (b) sample size used, (c) confidence interval or error margin, (d) one-sentence interpretation. Check that each item is present before outputting the final response. _(impact: medium)_
**Summary:** Completeness at 5/100 — the agent explains missing data instead of assuming defaults and producing output; fix is to invert the 'refuse to hallucinate' heuristic and add a fallback-output requirement to the blueprint.

---

---
## Feedback from 20260626-072103 (score: 72.8/100)
**Weakest:** accuracy | **Cause:** Blueprint permits the agent to conflate incompatible statistical frameworks (always-valid p-values vs O'Brien-Fleming sequential testing) and does not enforce deriving sample-size figures from first-principles calculations using the stated parameters. | **Severity:** high
**Changes:**
- **BLUEPRINT.md**: Add a 'methodology lock' rule: the agent must explicitly name ONE chosen framework before any analysis, cite the canonical formula used, and show the complete derivation step-by-step from stated inputs to numerical output. _(impact: high)_
- **persona.md**: Add a directive: 'When calculating sample sizes, power, or any numeric artifact, first emit the formula with the substituted values, then evaluate it — never output the final number without showing the arithmetic.' _(impact: medium)_
**Summary:** Accuracy is the bottleneck (avg 69) driven by conflating two sequential-testing frameworks and an unreproducible sample size — locking methodology choice in the blueprint and requiring derived-arithmetic visibility in the persona should push accuracy into the 75-80 range.

---

---
## Feedback from 20260626-072155 (score: 86.2/100)
**Weakest:** accuracy | **Cause:** Agent correctly applied Z-values and arithmetic but miscalculated post-hoc confidence interval width (stated ±1.4pp vs correct ~±0.79pp for two-sided 95%), indicating a gap in statistical interpretation or formula application for CI width from reported SE/σ. | **Severity:** medium
**Changes:**
- **BLUEPRINT.md**: Add a 'Statistical & Numerical Verification' subsection under the Review phase requiring the agent to explicitly show each step of statistical calculations (σ_known, SE, Z-value, MoE, CI bounds) and cross-check against known reference values before finalizing. _(impact: high)_
- **persona.md**: Add a directive: 'When computing confidence intervals, margin of error, or any derived statistic, decompose into atomic steps and state the formula before plugging values. Do not skip the intermediate MoE calculation.' _(impact: medium)_
**Summary:** Solid performance (86.2) with correct formula selection and arithmetic, but a preventable CI width miscalculation brought accuracy to 80 — add step-by-step numerical verification to the blueprint's review phase to catch these errors before submission.

---

---
## Feedback from 20260626-072443 (score: 32.0/100)
**Weakest:** accuracy | **Cause:** Agent inverted a core statistical formula (dividing instead of multiplying by sqrt(k/K)) and conflated O'Brien-Fleming with Pocock boundaries as if they were the same method. | **Severity:** critical
**Changes:**
- **BLUEPRINT.md**: Add a mandatory 'Formula Verification' step: before outputting any derivation, the agent must trace every term back to its published source, write the canonical form, and annotate each substitution. No derivation may be emitted without a post-hoc reverse-check (plug in sample numbers, compute both sides numerically, verify identity). _(impact: high)_
- **BLUEPRINT.md**: Add a 'Method Disambiguation' rule: when multiple statistical methods are discussed, the agent must first produce a comparison table showing how they differ, then pick exactly one and defend the choice. O'Brien-Fleming and Pocock must never be conflated. _(impact: high)_
- **persona.md**: Add a constraint line: 'Before submitting any technical output, verify all formulas against authoritative sources (textbook, peer-reviewed paper, or known statistical software implementation). If uncertain about a formula, state the uncertainty rather than guessing.' _(impact: high)_
- **config.yaml**: Add a pre-deployment validation hook that runs a compliance check: (1) formula sanity (numeric cross-check), (2) method disambiguation, (3) no 'TODO' or 'future work' promises in core deliverables. _(impact: medium)_
**Summary:** Critical accuracy failure (32/100) driven by inverted formula and conflated methods; blueprint needs formula verification, method disambiguation rules, and a pre-deployment quality gate.
