Task: A/B test design requested, no parameters supplied.
Framework selected: Standard frequentist two-sample z-test, fixed horizon, two-sided.
Choice justification: No sequential/peeking specified, no prior distribution supplied — default to fixed-horizon frequentist as the most common starting point requiring minimal assumptions.
Comparison table (fixed-horizon vs sequential candidates):
  method: Fixed-horizon z-test
  stopping_rule: Pre-determined sample size only
  alpha_spending: Single lookup at n=N
  correction: None (no interim looks)
  power_model: Standard (Z_alpha/2 + Z_beta)^2 formulation
  method: O'Brien-Fleming
  stopping_rule: Stringent early; liberal late
  alpha_spending: OBF alpha-spending function
  correction: Pocock more liberal at early looks; OBF ruled out unless early stopping with very low alpha desired
  power_model: Inflated max sample vs fixed-horizon
  method: Pocock
  stopping_rule: Constant boundary at each interim
  alpha_spending: Equal nominal p at each look
  correction: More aggressive early stopping than OBF; ruled out here because inflated sample size penalty is larger without a stated need for early looks
  method: Bayesian (Beta-Binomial)
  stopping_rule: Posterior probability threshold
  alpha_spending: N/A — decision-theoretic
  correction: No multiplicity adjustment needed
  power_model: Simulations required; no closed form
Selection: Fixed-horizon z-test. No peeking plan stated, no prior given. Bayesian ruled out (no prior specified). OBF/Pocock ruled out (no interim analysis schedule given).
Canonical formula (two-sample, equal variance, equal allocation):
n_per_group = 2 * (Z_alpha/2 + Z_beta)^2 * sigma^2 / delta^2
Source: Chow, Shao, Wang (2008) "Sample Size Calculations in Clinical Research", Chapter 3.
Derivation with annotated placeholders:
Step 1 — Parameters:
  alpha: [NOT PROVIDED]
    Default assumed: 0.05 (two-sided)
    Z_alpha/2: Z_0.025 = 1.960 (from standard normal table, Hayter 2012)
  beta: [NOT PROVIDED]
    Default assumed: 0.20 (power = 0.80)
    Z_beta: Z_0.20 = 0.842 (from standard normal table)
  sigma: [NOT PROVIDED]
    Placeholder: sigma_population (pooled standard deviation of outcome metric)
    Source: must come from historical data or pilot study
  delta: [NOT PROVIDED]
    Placeholder: delta_MDE (minimum detectable effect in raw outcome units)
    Source: business decision — smallest effect worth detecting
Step 2 — Compute numerator:
(Z_0.025 + Z_0.20)^2 = (1.960 + 0.842)^2
  Sum: 1.960 + 0.842 = 2.802
  Square: 2.802^2 = 7.851
Step 3 — Multiply by 2:
2 * 7.851 = 15.702
Step 4 — Assemble:
n_per_group = 15.702 * sigma^2 / delta^2
Step 5 — Numerical example for reverse-check (using illustrative sigma=10, delta=2):
n = 15.702 * 100 / 4 = 15.702 * 25 = 392.55 -> ceiling 393 per group
Reverse-check (compute power from n=393, sigma=10, delta=2, alpha=0.05):
  SE_diff = sqrt(2) * sigma / sqrt(n) = 1.414 * 10 / 19.824 = 0.713
  Z_critical = 1.960
  Noncentrality: delta / SE_diff = 2 / 0.713 = 2.804
  Power = P(Z > 1.960 | NCP=2.804) = P(Z > -0.844) = 0.801
Relative error: |0.801 - 0.800| / 0.800 = 0.00125 (< 1%) — PASS
Confidence interval decomposition (for completed test, placeholder values):
  sigma_known: [NOT PROVIDED]
  n_per_group: [NOT PROVIDED]
  SE_diff: sigma * sqrt(2/n) = placeholder
  Z_0.025: 1.960
  MoE: 1.960 * SE_diff = placeholder
  CI: observed_diff +/- MoE
  CI_width: 2 * MoE = placeholder
GAPS REQUIRING INPUT DATA:
  alpha — Significance level (default 0.05 assumed)
  beta or power — Type II error rate (default 0.20 / 80% power assumed)
  sigma — Population standard deviation of the outcome metric
  delta — Minimum detectable effect in raw outcome units
  allocation_ratio — Treatment:control ratio (default 1:1 assumed)
  outcome_type — Continuous, binary, or count (default continuous assumed; formula differs for proportions and rates)
PARTIAL DELIVERABLE:
  method: Fixed-horizon two-sample z-test, two-sided, equal allocation
  formula: n_per_group = 2 * (Z_alpha/2 + Z_beta)^2 * sigma^2 / delta^2
  source: Chow, Shao, Wang (2008) Chapter 3
  constant: 2 * (Z_0.025 + Z_0.20)^2 = 15.702 (for alpha=0.05, power=0.80)
  ready_for_substitution: n_per_group = 15.702 * sigma^2 / delta^2
  status: AWAITING sigma AND delta — formula fully derived, constant computed, reverse-check passed at example values
To refine: provide sigma (historical std dev), delta (MDE), and confirm alpha/power assumptions. Output will be exact sample size per group, total N, confidence interval width at boundary, and power curve.