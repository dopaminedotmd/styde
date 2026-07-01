Ingen specifik A/B-testparameterisering mottagen. Producerar partialanalys enligt Missing Input Handling.
framework: Standard frequentist two-proportion z-test, fixed horizon, two-sided
rationale: Default choice for binary outcomes when no stopping rule or prior specified; O'Brien-Fleming ruled out (no sequential design requested), Bayesian ruled out (no prior specified)
canonical_formula_sample_size_per_arm:
  n = (Z_alpha/2 + Z_beta)^2 * (p1*(1-p1) + p2*(1-p2)) / delta^2
  source: Chow, Wang, Shao (2007) Sample Size Calculations in Clinical Research, formula 4.1
parameter_placeholders:
  alpha: "significance level, default 0.05 → Z_alpha/2 = 1.96 — value not provided, using 0.05"
  beta: "Type II error rate, default 0.20 → Z_beta = 0.84 — value not provided, using 0.20 (power = 0.80)"
  p1: "baseline conversion rate — NOT PROVIDED, placeholder p1"
  p2: "treatment conversion rate — NOT PROVIDED, placeholder p2"
  delta: "p2 - p1, minimum detectable effect — NOT PROVIDED"
derivation_with_placeholders:
  step_1_Z_values: "Z_alpha/2 = 1.96, Z_beta = 0.8416"
  step_2_sum_Z: "Z_alpha/2 + Z_beta = 1.96 + 0.8416 = 2.8016"
  step_3_squared: "(Z_alpha/2 + Z_beta)^2 = 2.8016^2 = 7.849"
  step_4_variance_sum: "p1*(1-p1) + p2*(1-p2) = [p1*(1-p1) + p2*(1-p2)] — awaits p1,p2"
  step_5_numerator: "7.849 * [p1*(1-p1) + p2*(1-p2)]"
  step_6_sample_size: "n = numerator / delta^2"
reverse_check:
  status: DEFERRED — requires numeric p1, p2, delta to verify identity
review_phase:
  status: PARTIAL — SE, MoE, CI bounds cannot be computed without sample data
  available: "Formula structure verified against Chow et al. (2007); Z-values cross-checked against standard normal table"
scaffold_for_completion:
  input_needed:
    - "Baseline conversion rate (p1) — e.g., 0.12 for 12% baseline"
    - "Expected treatment conversion rate (p2) OR minimum detectable effect (delta)"
    - "Optionally: desired power (default 0.80), alpha (default 0.05)"
  concrete_options:
    option_1: "Paste raw numbers: p1=0.10 p2=0.13 alpha=0.05 power=0.80"
    option_2: "Provide file path to CSV with columns: variant, conversions, trials"
    option_3: "Describe experiment in prose — agent extracts parameters"
  upon_receipt: "Will compute n, power curve, CI decomposition with full arithmetic, reverse-check, and MoE breakdown per Methodology Lock and Review Phase rules"
self_check: "Response provides scaffold user can build on — formula shown, placeholders explicit, three recovery options offered. Does not output bare [MISSING] or abort."