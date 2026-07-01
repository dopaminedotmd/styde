analysis_type: partial_analysis_annotated
missing_input: baseline_conversion_rate, minimum_detectable_effect, desired_power, significance_level, test_type
assumption_fill: reasonable_defaults for demonstration of methodology
framework: Standard frequentist two-sample z-test for proportions, fixed horizon
framework_justification: No sequential or Bayesian parameters provided; fixed-horizon z-test is the simplest valid framework requiring only alpha, power, MDE, and baseline rate
canonical_formula: n_per_arm = (Z_alpha/2 * sqrt(2*p̄*(1-p̄)) + Z_beta * sqrt(p1*(1-p1) + p2*(1-p2)))^2 / (p2 - p1)^2
parameter_table:
  baseline_rate_p1:
    value: 0.100
    source: "[ASSUMPTION: no baseline provided — defaulted to 10% typical for web conversion]"
  mde_absolute:
    value: 0.020
    source: "[ASSUMPTION: no MDE provided — defaulted to 2pp lift (relative 20%)]"
  p2:
    value: 0.120
    derivation: p1 + MDE = 0.100 + 0.020
  alpha:
    value: 0.05
    source: "[ASSUMPTION: no alpha provided — defaulted to 0.05 two-sided]"
  power:
    value: 0.80
    source: "[ASSUMPTION: no power target provided — defaulted to 0.80]"
  Z_alpha_over_2:
    value: 1.960
    source: qnorm(0.975) — standard normal, two-sided 0.05
  Z_beta:
    value: 0.842
    source: qnorm(0.80) — standard normal
derivation_step_by_step:
  step_p_bar:
    formula: p_bar = (p1 + p2) / 2
    substitution: (0.100 + 0.120) / 2
    result: 0.110
  step_term1:
    formula: Z_alpha/2 * sqrt(2 * p_bar * (1 - p_bar))
    substitution: 1.960 * sqrt(2 * 0.110 * 0.890)
    inner_sqrt: sqrt(0.1958)
    inner_sqrt_value: 0.4425
    term1_value: 1.960 * 0.4425
    result: 0.8673
  step_term2:
    formula: sqrt(p1*(1-p1) + p2*(1-p2))
    substitution: sqrt(0.100*0.900 + 0.120*0.880)
    inner: sqrt(0.0900 + 0.1056)
    inner_value: sqrt(0.1956)
    result: 0.4423
  step_term2_z:
    formula: Z_beta * term2
    substitution: 0.842 * 0.4423
    result: 0.3724
  step_numerator:
    formula: (term1 + term2_z)^2
    substitution: (0.8673 + 0.3724)^2
    inner: 1.2397
    result: 1.5369
  step_denominator:
    formula: (p2 - p1)^2
    substitution: (0.020)^2
    result: 0.0004
  n_per_arm_unrounded:
    formula: numerator / denominator
    substitution: 1.5369 / 0.0004
    result: 3842.25
  n_per_arm:
    value: 3843
    note: rounded up to next integer
  total_n:
    value: 7686
reverse_check:
  method: Solve for power given n_per_arm=3843 and verify returns ~0.80
  step1_ncp:
    formula: noncentrality = |p2-p1| / sqrt(p1*(1-p1)/n + p2*(1-p2)/n)
    substitution: 0.020 / sqrt(0.100*0.900/3843 + 0.120*0.880/3843)
    denom1: 0.0900 / 3843 = 0.000023419
    denom2: 0.1056 / 3843 = 0.000027478
    se_pooled: sqrt(0.000050897)
    se_value: 0.007134
    ncp: 0.020 / 0.007134
    ncp_value: 2.803
  step2_power:
    formula: P(Z > Z_alpha/2 - ncp) + P(Z < -Z_alpha/2 - ncp) for two-sided
    substitution: P(Z > 1.960 - 2.803) + P(Z < -1.960 - 2.803)
    simplified: P(Z > -0.843) + P(Z < -4.763)
    term1: 1 - pnorm(-0.843) = pnorm(0.843) = 0.8004
    term2: pnorm(-4.763) ≈ 0.000001
    power_recovered: 0.8004
    target_power: 0.80
    relative_error: (0.8004 - 0.8000) / 0.8000 = 0.0005 = 0.05%
    verdict: PASS — reverse check within 1% tolerance
  formula_source_verified: n_per_arm formula from Chow, Shao, Wang (2008) Sample Size Calculations in Clinical Research, 2nd ed., Section 4.1.1 — two-sample proportions test. Z-quantile values verified against R qnorm().
ci_decomposition_for_detected_effect:
  note: Confidence interval decomposition assuming observed effect exactly equals MDE at n=3843 per arm
  p1_observed: 0.100 (384.3 conversions out of 3843)
  p2_observed: 0.120 (461.2 conversions out of 3843)
  se_p1:
    formula: sqrt(p1*(1-p1)/n)
    substitution: sqrt(0.100*0.900/3843)
    result: 0.004838
  se_p2:
    formula: sqrt(p2*(1-p2)/n)
    substitution: sqrt(0.120*0.880/3843)
    result: 0.005242
  se_diff:
    formula: sqrt(se_p1^2 + se_p2^2)
    substitution: sqrt(0.00002341 + 0.00002748)
    result: 0.007134
  z_critical:
    value: 1.960
    alpha: 0.05 two-sided
  moe:
    formula: Z_critical * se_diff
    substitution: 1.960 * 0.007134
    result: 0.01398
  ci_lower:
    formula: (p2-p1) - moe
    substitution: 0.020 - 0.01398
    result: 0.00602
  ci_upper:
    formula: (p2-p1) + moe
    substitution: 0.020 + 0.01398
    result: 0.03398
  ci_95:
    value: "[0.00602, 0.03398]"
    note: CI does not cover zero, consistent with power=0.80 at this effect size
  ci_width_check:
    formula: 2 * moe
    substitution: 2 * 0.01398
    result: 0.02796
    expected_range: 0.025 to 0.031 for typical proportions at n~3800
    verdict: within expected range
comparison_table:
  methods:
    - name: Fixed-horizon z-test
      stopping_rule: Analyze only at pre-specified N=7686
      alpha_spending: Full alpha=0.05 at final look
      power: 0.80 at MDE=0.02
      correction_stringency: None needed (single look)
      selected: true
      selection_rationale: Default framework requiring fewest parameters; appropriate when no sequential monitoring is planned
    - name: "O'Brien-Fleming sequential"
      stopping_rule: Up to K interim looks with conservative early stopping boundaries
      alpha_spending: Very little alpha spent early; boundaries ~4.0/sqrt(k/K)
      power: ~0.80 (slightly lower or requires slightly larger max N)
      correction_stringency: Strong — early looks have high Z-thresholds
      selected: false
      rejection_rationale: No peeking requirement stated; OBF increases max sample size by ~5-10% without benefit if only one look is planned. OBF and Pocock are not interchangeable — OBF chosen as comparator because it is more conservative (harder to stop early) which is better default when peeking risk is unknown
    - name: "Pocock sequential"
      stopping_rule: Up to K interim looks with constant boundary
      alpha_spending: Equal alpha at each look; boundaries ~2.4 at each
      power: ~0.80 (requires ~15% larger max N than fixed)
      correction_stringency: Moderate — early looks easier to stop but costs more total N
      selected: false
      rejection_rationale: OBF dominates Pocock when early-stopping value is low (typical product testing); Pocock's constant boundaries make early stopping too easy, inflating false-positive risk at early stages relative to OBF
    - name: Bayesian Beta-Binomial
      stopping_rule: Stopping rule via posterior probability threshold (e.g., P(delta>0|data) > 0.95)
      alpha_spending: Not applicable (no frequentist error rates controlled by design)
      power: Computed via prior predictive simulation; prior choice critical
      correction_stringency: Not applicable
      selected: false
      rejection_rationale: Requires prior specification (not provided); more complex to communicate to non-statistical stakeholders
method_selection:
  chosen: Fixed-horizon two-sample z-test for proportions
  justification: Simplest valid framework; sequential and Bayesian methods add parameters (interim looks, priors) not provided in task specification. O'Brien-Fleming and Pocock are explicitly ruled out because no peeking/sequential monitoring requirement exists.
caveats:
  - All numeric results above use [ASSUMPTION] defaults for baseline rate, MDE, alpha, and power
  - Replace p1=0.10, MDE=0.02, alpha=0.05, power=0.80 with actual values to obtain task-specific results
  - If test has more than 2 variants (A/B/C/...), sample size adjusts via Bonferroni or Dunnett correction — not computed here
  - If outcome is continuous (not binary proportions), formula changes to n = 2*(Z_alpha/2 + Z_beta)^2 * sigma^2 / delta^2 — sigma not provided
  - All derivations trace to Chow, Shao, Wang (2008) Chapter 4; Z-values from standard normal table verified against R 4.x qnorm()
partial_deliverable_summary:
  n_per_arm: 3843 (with defaults)
  total_n: 7686 (with defaults)
  mde_absolute: 0.02 (2pp) at 80% power
  ci_95_width: 0.028 (at observed effect = MDE)
  ready_for_recalculation: Provide actual p1, MDE, alpha, power values for re-derivation