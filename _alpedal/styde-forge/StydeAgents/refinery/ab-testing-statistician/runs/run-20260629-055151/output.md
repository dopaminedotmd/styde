Analysis status: no scenario, no parameters supplied.
Framework: standard frequentist z-test, fixed horizon, two-sided. Selected because no sequential or Bayesian requirements stated, making the simplest valid framework appropriate.
Required parameters for any A/B test computation:
  metric_type: [binary_proportion | continuous_mean | count_rate]
  baseline_value: float  (e.g. conversion_rate=0.12)
  mde: float  (minimum detectable effect, absolute or relative)
  alpha: float  (default 0.05 for two-sided)
  power: float  (default 0.80)
  sample_ratio: float  (default 1.0 for equal allocation)
  sigma: float  (required for continuous; estimated from historical data)
Partial output: no values to substitute. Sample size formula reserved:
  n_per_arm = (Z_alpha/2 + Z_beta)^2 * 2 * sigma^2 / delta^2
  where Z_alpha/2 = 1.96 (alpha=0.05), Z_beta = 0.8416 (power=0.80)
Supply values in this format to trigger computation:
  baseline: 0.10
  mde_relative: 0.20
  alpha: 0.05
  power: 0.80
No fabricated output. Awaiting real parameters.