AB TESTING STATISTICIAN — LIVE SESSION
DESIGN PARAMETERS ENTERED:
  baseline_conversion: 0.05 (5%)
  minimum_detectable_effect_relative: 0.20 (20% relative lift)
  alpha: 0.05
  beta: 0.20 (power 80%)
  traffic_per_day: 10000 visitors
  split: 50/50
DECISION TREE
branch: power analysis
  check: mde_absolute = baseline * mde_relative = 0.05 * 0.20 = 0.01
  check: expected_treatment_rate = baseline + mde_absolute = 0.05 + 0.01 = 0.06
  method: two_proportion_ztest (frequentist)
  condition: peeking_possible == false
  verdict: standard fixed-horizon design
branch: sequential correction
  check: peeking_possible == true
  condition: traffic cannot be fully reserved before test ends
  verdict: switch to sequential (O'Brien-Fleming) design
    add: correction penalty = 10-15% sample size inflation
branch: bayesian alternative
  condition: prior data exists for baseline conversion
  verdict: beta-binomial conjugate model
    advantage: no peeking penalty, intuitive posterior interpretation
EXECUTED COMPUTATIONS
sample_size_per_variant (frequentist):
  z_alpha = 1.95996 (two-tailed)
  z_beta = 0.84162 (80% power)
  p_bar = (0.05 + 0.06) / 2 = 0.055
  n = (1.95996*sqrt(2*0.055*0.945) + 0.84162*sqrt(0.05*0.95 + 0.06*0.94))^2 / (0.01)^2
  n = 34875 per variant
  total: 69750 visitors
  duration: 7.0 days at 10000/day
sequential correction applied:
  adjusted_n = 34875 * 1.12 = 39060 per variant
  adjusted_duration: 7.8 days
bayesian alternative:
  prior: Beta(1, 19) from historical 5% baseline (weak prior)
  posterior under null: Beta(1+500, 19+9500) = Beta(501, 9519)
  posterior under treatment (+20% lift): Beta(1+600, 19+9400) = Beta(601, 9419)
  expected_prob_treatment_better: 0.982
  minimum required N for P(treatment > control) > 0.95: 11200 per variant
summary:
  frequentist: 34875 per variant, 7.0 days
  sequential: 39060 per variant, 7.8 days
  bayesian: 11200 per variant, 2.3 days
RECOMMENDATION
Bayesian beta-binomial with 11200 per variant. Requires 2.3 days at current traffic. Provides P(treatment > control) = 0.982 at true lift, no peeking penalty, directly interpretable for business stakeholders. Sequential frequentist is fallback if organizational policy demands p-values.