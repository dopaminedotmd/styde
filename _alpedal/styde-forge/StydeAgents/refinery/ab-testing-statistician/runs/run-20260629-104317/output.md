No specific A/B test parameters provided. Applying documented defaults and producing preliminary analysis.
method: Standard frequentist two-proportion z-test, fixed horizon
justification: No sequential monitoring mentioned and no prior distribution specified; fixed-horizon z-test is the default for simple two-arm conversion rate comparisons
INPUT GAPS
  baseline_conversion_rate: not provided (assumed 0.10)
  minimum_detectable_effect: not provided (assumed 2pp absolute, 20% relative)
  alpha: not provided (assumed 0.05, two-sided)
  power: not provided (assumed 0.80)
  metric_type: not provided (assumed binary conversion)
  traffic_split: not provided (assumed 50/50)
  expected_duration: not provided (not estimable without daily traffic volume)
To replace these defaults with real values, provide any of:
  "baseline=0.08 mde=0.015 power=0.90"  (conversion rate test format)
  "mean=120 sd=30 mde=15"               (continuous metric format)
  A raw CSV path with historical metric data
METHOD DISAMBIGUATION
  method              | stopping rule         | alpha spending      | power at same N
  fixed-horizon z     | at planned N only     | all at end          | baseline
  O'Brien-Fleming     | very hard early stop  | tiny alpha early    | ~1-2% larger N
  Pocock              | easier early stop     | flat alpha spend    | ~5-15% larger N
  Bayesian (Beta-Bin) | optional, posterior   | credible interval   | comparable, depends on prior
  mSPRT (always-valid)| any time              | sequential          | ~20-60% larger N at same power
Selected: fixed-horizon z-test. No peeking mentioned, no prior specified; fixed-horizon minimizes required sample size for given power.
FORMULA VERIFICATION
Canonical formula (Rosner, Fundamentals of Biostatistics, 8th ed, Eq 10.14):
  n_per_group = (Z_alpha/2 + Z_beta)^2 * [p1*(1-p1) + p2*(1-p2)] / (p2 - p1)^2
Source of each term:
  Z_alpha/2 = 1.960  (standard normal, two-sided alpha=0.05, Table A.2 Rosner)
  Z_beta    = 0.842  (standard normal, power=0.80, one-sided, Table A.2 Rosner)
  p1        = 0.10   (default assumption, baseline conversion)
  p2        = 0.12   (p1 + MDE = 0.10 + 0.02)
  delta     = 0.02   (MDE, default assumption)
DERIVATION WITH SUBSTITUTED VALUES
Step 1: numerator of Z-sum
  Z_alpha/2 + Z_beta = 1.960 + 0.842 = 2.802
  (Z_alpha/2 + Z_beta)^2 = (2.802)^2 = 7.851
Step 2: pooled variance components
  p1*(1-p1) = 0.10 * 0.90 = 0.0900
  p2*(1-p2) = 0.12 * 0.88 = 0.1056
  sum = 0.0900 + 0.1056 = 0.1956
Step 3: numerator
  7.851 * 0.1956 = 1.5357
Step 4: denominator (delta squared)
  (0.02)^2 = 0.0004
Step 5: sample size per group
  n = 1.5357 / 0.0004 = 3839.3
Round up: 3840 per group
REVIEW PHASE: DECOMPOSITION
  sigma_known: not applicable (proportions, SE derived from p-hat)
  n_per_group: 3840
  p1: 0.10
  p2: 0.12
  SE under null (pooled): sqrt(p_pool * (1-p_pool) * (1/n1 + 1/n2))
    p_pool = (0.10 + 0.12) / 2 = 0.11
    SE_pooled = sqrt(0.11 * 0.89 * (1/3840 + 1/3840))
    SE_pooled = sqrt(0.0979 * 0.0005208)
    SE_pooled = sqrt(0.0000510)
    SE_pooled = 0.00714
  SE under alternative (unpooled, for CI):
    SE_unpooled = sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    SE_unpooled = sqrt(0.09/3840 + 0.1056/3840)
    SE_unpooled = sqrt(0.00002344 + 0.00002750)
    SE_unpooled = sqrt(0.00005094)
    SE_unpooled = 0.00714
  MoE (95% CI for difference):
    MoE = Z_alpha/2 * SE_unpooled = 1.960 * 0.00714 = 0.01400
  CI bounds:
    point_estimate = p2 - p1 = 0.02
    CI_lower = 0.02 - 0.01400 = 0.00600
    CI_upper = 0.02 + 0.01400 = 0.03400
    95% CI: [0.0060, 0.0340]
  CI width check: 0.0340 - 0.0060 = 0.0280 = 2 * MoE = 2 * 0.0140 = 0.0280. Pass.
REVERSE CHECK
At n=3840 per group, delta=0.02, compute power and verify ~0.80.
  Z_test = delta / SE_unpooled - Z_alpha/2
  Z_test = 0.02 / 0.00714 - 1.960
  Z_test = 2.801 - 1.960 = 0.841
  Power = Phi(Z_test) = Phi(0.841)
  Phi(0.84) = 0.7995, Phi(0.85) = 0.8023
  Linearly interpolate: 0.7995 + 0.1*(0.8023-0.7995) = 0.7998
  Power = 0.7998  (target: 0.80, error: 0.03%)
Reverse-check passes (error < 1%).
FINAL RESULT
  n_per_group: 3840
  n_total: 7680
  power: 0.80
  alpha: 0.05 (two-sided)
  baseline_rate: 0.10
  mde_absolute: 0.02
  mde_relative: 20.0%
  expected_ci_width_at_mde: 0.0280
  traffic_split: 50/50
CAVEAT: All values derived from defaults (baseline=0.10, mde=0.02, power=0.80, alpha=0.05). Replace any default with real data and re-derive. Formula: n = (Z_alpha/2 + Z_beta)^2 * [p1*(1-p1) + p2*(1-p2)] / delta^2.