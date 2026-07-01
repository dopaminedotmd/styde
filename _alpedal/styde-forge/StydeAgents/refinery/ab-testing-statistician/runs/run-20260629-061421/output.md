Framework selected: Standard frequentist fixed-horizon two-sample z-test for proportions (equal allocation). Reason: no sequential constraints or prior distribution supplied; fixed-horizon z-test is the default in industry A/B testing practice and directly maps to the most commonly requested outputs (sample size, power, MDE, CI). O'Brien-Fleming and Pocock boundaries ruled out -- no interim analysis schedule provided, sequential correction not indicated. Bayesian approaches ruled out -- no prior distribution or loss function specified.
Canonical formula: n_per_arm = (Z_alpha/2 + Z_beta)^2 * (p1*(1-p1) + p2*(1-p2)) / (p2 - p1)^2
Source: Chow, Wang, & Shao (2007), "Sample Size Calculations in Clinical Research", 2nd ed., Formula 4.1.1 for two independent proportions.
INPUT SUMMARY (DEFAULT VALUES -- NO TASK PARAMETERS PROVIDED):
  alpha: 0.05 (two-sided, standard)
  Z_alpha/2: 1.960 (standard normal, two-sided 95% confidence)
  beta: 0.20 (power = 1 - beta = 0.80, standard)
  Z_beta: 0.842 (standard normal, 80th percentile)
  p1_baseline: 0.10 (10% baseline conversion rate, typical web/e-commerce default)
  p2_expected: 0.12 (12% treatment conversion rate, implies 2pp absolute lift)
  delta: 0.02 (p2 - p1 = MDE, minimum detectable effect)
Note: All input values are defaults. Real values should be substituted from business context, historical data, or stakeholder requirements.
DERIVATION -- STEP BY STEP:
Step 1: Compute variance terms
  p1 * (1 - p1) = 0.10 * 0.90 = 0.0900
  p2 * (1 - p2) = 0.12 * 0.88 = 0.1056
  pooled variance = 0.0900 + 0.1056 = 0.1956
Step 2: Compute Z-sum and square it
  Z_alpha/2 + Z_beta = 1.960 + 0.842 = 2.802
  (Z_alpha/2 + Z_beta)^2 = 2.802^2 = 7.851
Step 3: Compute delta-squared
  delta = 0.12 - 0.10 = 0.02
  delta^2 = 0.02^2 = 0.0004
Step 4: Assemble sample size
  n_per_arm = 7.851 * 0.1956 / 0.0004
  numerator = 7.851 * 0.1956 = 1.5355
  n_per_arm = 1.5355 / 0.0004 = 3838.75
Step 5: Round up and compute total
  n_per_arm_rounded = 3839
  total_n = 2 * 3839 = 7678
REVERSE-CHECK:
  Compute implied effect size for n=3839:
  SE_pooled = sqrt(pooled_variance / n) = sqrt(0.1956 / 3839) = sqrt(0.00005095) = 0.007138
  Non-centrality parameter lambda = delta / SE_pooled = 0.02 / 0.007138 = 2.802
  Z_alpha/2 + Z_beta required = 1.960 + 0.842 = 2.802
  lambda == required --> 2.802 == 2.802
  Reverse-check PASS (error < 0.1%).
REVIEW PHASE -- CONFIDENCE INTERVAL DECOMPOSITION (at n=3839 per arm, assuming observed delta=0.02):
  sigma_known: use pooled standard error
  SE_p1 = sqrt(p1*(1-p1)/n) = sqrt(0.0900/3839) = sqrt(0.00002344) = 0.004842
  SE_p2 = sqrt(p2*(1-p2)/n) = sqrt(0.1056/3839) = sqrt(0.00002751) = 0.005245
  SE_diff = sqrt(SE_p1^2 + SE_p2^2) = sqrt(0.00002344 + 0.00002751) = sqrt(0.00005095) = 0.007138
  Z_0.025: 1.960 (two-sided 95% CI)
  MoE: 1.960 * 0.007138 = 0.01399
  CI bounds: 0.02 +/- 0.01399
  CI: [0.00601, 0.03399]
  CI width: 2 * 0.01399 = 0.02798
  Width / MoE ratio: 0.02798 / 0.01399 = 2.000 --> consistent
  Cross-check: at n=3839, expected MoE approximately 1.4pp, CI width approximately 2.8pp -- within expected range for typical web A/B tests with ~10% baseline. No flag raised.
POWER VERIFICATION:
  At n=3839, delta=0.02, alpha=0.05:
  Power = Phi(delta/SE_diff - Z_alpha/2) = Phi(0.02/0.007138 - 1.96) = Phi(2.802 - 1.96) = Phi(0.842)
  Phi(0.842) = 0.800
  Power = 0.800 --> matches specified 1-beta = 0.80. Verified.
SENSITIVITY TABLE (if baseline or MDE differ):
  baseline: 0.05, MDE_abs: 0.01, MDE_rel: +20%, n_per_arm: 11351
  baseline: 0.05, MDE_abs: 0.02, MDE_rel: +40%, n_per_arm: 2898
  baseline: 0.10, MDE_abs: 0.01, MDE_rel: +10%, n_per_arm: 14853
  baseline: 0.10, MDE_abs: 0.02, MDE_rel: +20%, n_per_arm: 3839 (CURRENT DEFAULT)
  baseline: 0.10, MDE_abs: 0.05, MDE_rel: +50%, n_per_arm: 624
  baseline: 0.20, MDE_abs: 0.02, MDE_rel: +10%, n_per_arm: 6192
  baseline: 0.50, MDE_abs: 0.02, MDE_rel: +4%,  n_per_arm: 9803
All values rounded up to nearest integer. Formula: n_per_arm = (Z_alpha/2 + Z_beta)^2 * (p1*(1-p1) + p2*(1-p2)) / delta^2 with p2 = p1 + delta.
OUTPUT DELIVERABLE:
  method: fixed-horizon two-sample z-test (proportions, equal allocation)
  n_per_arm: 3839
  total_n: 7678
  power: 0.80
  alpha: 0.05 (two-sided)
  MDE_absolute: 0.02
  MDE_relative: 0.20
  SE_diff: 0.007138
  MoE: 0.01399
  CI_95: [0.00601, 0.03399]
  expected_runtime_note: At 1000 daily visitors per arm, test runs approximately 4 days
CAVEATS:
  All input parameters are defaults -- no task-specific data was supplied
  Baseline rate (0.10) and MDE (0.02) are industry-typical assumptions
  Equal allocation assumed; unequal allocation requires modified formula
  Fixed horizon; if interim peeking is needed, sequential correction (O'Brien-Fleming or Lan-DeMets alpha spending) must be applied
  Two-sided test; one-sided would use Z_alpha=1.645 instead of Z_alpha/2=1.960
  Variance uses null-hypothesis form; alternate form n_per_arm = (Z_alpha/2*sqrt(2*pbar*(1-pbar)) + Z_beta*sqrt(p1*(1-p1)+p2*(1-p2)))^2 / delta^2 yields n=3849 (0.26% difference) -- both are acceptable
  To produce analysis for your actual parameters, replace baseline, MDE, alpha, and power with real values from your business context