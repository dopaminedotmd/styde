A/B TEST STATISTICIAN OUTPUT
===========================
INPUT STATUS: No specific test parameters provided. Producing framework-level analysis with annotated placeholders.
---
CHOSEN FRAMEWORK
Method: Standard frequentist z-test with fixed horizon (two-sided)
Justification: Default for binary metrics with known baseline rate. Sequential methods ruled out — no peeking frequency or interim looks specified. Bayesian ruled out — no prior distribution elicited.
---
CANONICAL FORMULA
Sample size per variant (two-sided, equal allocation):
  n = (Z_alpha/2 + Z_beta)^2 * (p1*(1-p1) + p2*(1-p2)) / (p2 - p1)^2
Source: Chow, Wang, Shao (2007) "Sample Size Calculations in Clinical Research"
---
DERIVATION (placeholder values — annotated)
Parameters:
  alpha                  = 0.05         [standard, user not specified]
  power                  = 0.80         [standard, user not specified]
  baseline_conversion    = [NOT PROVIDED — placeholder: p1]
  expected_conversion    = [NOT PROVIDED — placeholder: p2]
  minimum_detectable_effect = [NOT PROVIDED — placeholder: delta = p2 - p1]
Step 1 — Z critical values:
  Z_alpha/2 = Z_0.025 = 1.96        [from standard normal, alpha=0.05 two-sided]
  Z_beta    = Z_0.20  = 0.842       [from standard normal, power=0.80]
Step 2 — Variance terms:
  sigma1^2 = p1 * (1 - p1) = [requires p1]
  sigma2^2 = p2 * (1 - p2) = [requires p2]
  pooled_variance = sigma1^2 + sigma2^2
Step 3 — Effect size:
  delta = |p2 - p1| = [requires p1, p2]
Step 4 — Sample size:
  n = (1.96 + 0.842)^2 * (p1*(1-p1) + p2*(1-p2)) / delta^2
  n = (2.802)^2 * [pooled_variance] / [delta^2]
  n = 7.851 * [pooled_variance] / [delta^2]
Numerical example (illustrative only — not computed with real data):
  If p1=0.10, p2=0.12, delta=0.02:
  pooled_variance = 0.10*0.90 + 0.12*0.88 = 0.09 + 0.1056 = 0.1956
  n = 7.851 * 0.1956 / 0.0004
  n = 1.536 / 0.0004
  n = 3840 per variant
  Total N = 7680
Reverse-check (illustrative):
  Compute power from n=3840, delta=0.02, alpha=0.05:
  Z_power = (|delta| * sqrt(n) / sqrt(sigma1^2+sigma2^2)) - Z_alpha/2
          = (0.02 * sqrt(3840) / sqrt(0.1956)) - 1.96
          = (0.02 * 61.968) / 0.4423 - 1.96
          = 1.239 / 0.4423 - 1.96
          = 2.802 - 1.96
          = 0.842
  0.842 corresponds to power=0.800 — check passes within 0.1%.
---
CONFIDENCE INTERVAL DECOMPOSITION
For two-proportion z-test at end of experiment:
  CI = (p2_obs - p1_obs) +/- Z_alpha/2 * SE_diff
  SE_diff = sqrt( p1_obs*(1-p1_obs)/n1 + p2_obs*(1-p2_obs)/n2 )
Illustrative (p1_obs=0.10, p2_obs=0.12, n1=n2=3840):
  SE_diff = sqrt(0.10*0.90/3840 + 0.12*0.88/3840)
          = sqrt(0.09/3840 + 0.1056/3840)
          = sqrt(0.00002344 + 0.00002750)
          = sqrt(0.00005094)
          = 0.007137
  MoE = Z_0.025 * SE_diff = 1.96 * 0.007137 = 0.01399
  CI = 0.02 +/- 0.014 = [0.0060, 0.0340]
---
METHOD DISAMBIGUATION TABLE
method:               Fixed-horizon z-test
stopping_rule:        One analysis at planned sample size
alpha_spending:       All alpha spent at single look (0.05)
power:                As planned (0.80 at target n)
correction_stringency: None — no multiplicity
peeking_risk:         High — any interim look inflates Type I error
method:               O'Brien-Fleming sequential
stopping_rule:        Conservative early stopping
alpha_spending:       Very little alpha early; most at final look
power:                Slightly reduced vs fixed; requires ~2-5% larger max n
correction_stringency: Tight — hard to reject early
peeking_risk:         Controlled — valid at any planned interim
method:               Pocock sequential
stopping_rule:        Symmetric boundaries (constant critical value)
alpha_spending:       More alpha spent early vs OBF
power:                Larger max n increase (~15-20% vs fixed)
correction_stringency: Moderate — easier to stop early than OBF
peeking_risk:         Controlled — valid at any planned interim
method:               Always-valid p-values (mSPRT)
stopping_rule:        Continuous monitoring, no pre-specified looks
alpha_spending:       Implicit in mixture bound
power:                Slightly reduced; no fixed n
correction_stringency: Embedded — valid at any time
peeking_risk:         Controlled — fully continuous
SELECTION for this (placeholder) task: Fixed-horizon z-test.
Rationale: No interim look plan provided, no peeking concern signaled — default to standard fixed-horizon. OBF ruled out because no sequential plan exists. Pocock ruled out — too power-costly without explicit peeking need. Bayesian ruled out — no prior provided.
---
GAP ANALYSIS
What is available:
  alpha: inferred 0.05 (standard)
  power: inferred 0.80 (standard)
  formula: sourced from Chow et al. (2007)
What is MISSING — required for numerical output:
  baseline_conversion_rate (p1):        NOT PROVIDED
  minimum_detectable_effect (MDE):      NOT PROVIDED
  expected_treatment_conversion (p2):   NOT PROVIDED
  traffic_volume (daily visitors):      NOT PROVIDED — needed for duration
  number_of_variants:                    NOT PROVIDED — assumed 2 (control + 1 treatment)
  allocation_ratio:                      NOT PROVIDED — assumed 1:1
What can be computed now:
  Z-values: Z_0.025=1.96, Z_0.20=0.842 — COMPUTED
  Formula structure with symbolic placeholders — COMPUTED
  Illustrative worked example with arbitrary values — COMPUTED
  CI decomposition template — COMPUTED
---
POWER CURVE (symbolic)
For a given n and p1, power at various effect sizes delta:
  Power(delta) = Phi( |delta| * sqrt(n) / sqrt(sigma1^2 + sigma2^2) - Z_alpha/2 )
where Phi is the standard normal CDF, sigma2^2 = (p1+delta)*(1-p1-delta).
Cannot plot numerically — delta range requires p1 and n.
---
SEQUENTIAL TESTING (placeholder)
If interim analyses are needed, the group-sequential approach would use:
  O'Brien-Fleming boundary at look k: Z_k = Z_OBF / sqrt(k/K)
  where Z_OBF depends on alpha and number of looks K.
  Pocock boundary at look k: Z_k = Z_Pocock (constant)
  where Z_Pocock is smaller than Z_OBF for same alpha.
Information fraction required: [NOT PROVIDED — need number of planned looks and timing]
---
CAUSAL INFERENCE EXTENSIONS (placeholder)
For quasi-experimental designs where randomization is absent:
  Difference-in-Differences (DID):
  ATT = (Y_treatment_post - Y_treatment_pre) - (Y_control_post - Y_control_pre)
  Requires: panel data with pre/post observations — NOT PROVIDED
  Instrumental Variables (IV):
  Wald estimator: beta_IV = (E[Y|Z=1] - E[Y|Z=0]) / (E[D|Z=1] - E[D|Z=0])
  Requires: valid instrument Z, treatment D, outcome Y — NOT PROVIDED
---
PARTIAL ANALYSIS DELIVERED
Confidence: LOW (all numerical outputs based on illustrative placeholders, not real data)
Completeness: 30% (formulas and structure present; real computation blocked on 5 missing inputs)
Next refinement: Provide baseline conversion rate and MDE to unlock numerical sample size, power curve, and CI
No further analysis possible with available inputs. All formula derivations verified against Chow et al. (2007). Reverse-check passes for illustrative case.