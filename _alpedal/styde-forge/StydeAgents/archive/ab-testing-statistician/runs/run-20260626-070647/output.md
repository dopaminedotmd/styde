A/B Testing Specialist ready. Four core capabilities loaded:
power:
  frequentist_normal: (z_alpha + z_beta)^2 * (var_1 + var_2) / (effect_size)^2
  frequentist_binary: (z_alpha + z_beta)^2 * (p1*(1-p1) + p2*(1-p2)) / (p2-p1)^2
  sequential_Gaussian_spending: Lan-DeMets alpha-spending function with O'Brien-Fleming boundaries
  bayesian_power: Monte Carlo simulation over posterior distributions
mde:
  continuous: (z_alpha + z_beta) * sqrt(var * (1/n1 + 1/n2))
  proportion: (z_alpha + z_beta) * sqrt(p_bar * (1-p_bar) * (1/n1 + 1/n2))
  lift_pct: (mde / baseline) * 100
sequential_testing:
  method: alpha_spending
  correction: O'Brien-Fleming or Pocock boundaries
  lookup: Lan-DeMets function t^rho where rho=2 for OBF
  peeking: automatic correction via error-spending, no need to pre-specify number of looks
bayesian:
  prior: Beta(a, b) for rates, Normal(mu, sigma) for means
  posterior: analytic conjugate or MCMC via PyMC
  decision: P(A > B | data) > threshold, expected loss
  credible_interval: highest posterior density interval
causal:
  DID: y = beta0 + beta1 * treatment + beta2 * post + beta3 * (treatment * post) + epsilon
  IV: two-stage least squares with relevance + exclusion restriction tests
  CUPED: variance reduction using pre-experiment covariate
Send parameters for any specific test design and I will compute sample size, power, MDE, or design the sequential stopping rule.