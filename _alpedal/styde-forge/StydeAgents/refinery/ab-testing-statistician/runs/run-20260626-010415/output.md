power_analysis:
  sample_size_formula:
    two_sample_z_test:
      n_per_group: ( (Z_alpha_2 + Z_beta)^2 * (p1*(1-p1) + p2*(1-p2)) ) / (p2 - p1)^2
      inputs:
        baseline_conversion: p1
        expected_effect: p2 - p1
        alpha: 0.05 (default)
        power: 0.80 (default)
      notes: Use for binary outcomes. For continuous outcomes replace with mean/variance formula.
    continuous:
      n_per_group: (2 * (Z_alpha_2 + Z_beta)^2 * sigma^2) / delta^2
      inputs:
        sigma: pooled_standard_deviation
        delta: minimum_effect_size
minimum_detectable_effect:
  formula:
    mde: Z_alpha_2 + Z_beta * sqrt( p*(1-p) * (1/n1 + 1/n2) )
  notes: Relative MDE = absolute_MDE / baseline_rate. For fixed n, higher baseline rates yield smaller relative MDE.
sequential_testing:
  methods:
    - name: peeking_correction
      approach: o_brien_fleming
      description: Conservative stopping boundaries. Spend most alpha at final analysis.
      alpha_spending:
        interim_1: 0.0005
        interim_2: 0.004
        interim_3: 0.018
        final: 0.045  # total alpha ~0.05
    - name: always_valid_inference
      approach: johndoh_sequential_testing
      description: Martingale-based confidence sequences. Continuously valid.
      formula: Reject H0 when |Z_t| > sqrt( (t*log(1+2*t)) * 2 )
      notes: No peeking penalty. More conservative than fixed-horizon.
bayesian_ab_testing:
  model:
    likelihood: Binomial(y | n, theta)
    prior: Beta(alpha, beta)
    posterior: Beta(alpha + y, beta + n - y)
    default_prior: Beta(1,1) for uniform, Beta(0.5,0.5) for Jeffreys
  metrics:
    - probability_that_B_is_better:
        method: Monte Carlo samples from posterior_A and posterior_B
        formula: mean(theta_B_samples > theta_A_samples)
    - expected_loss:
        formula: integral( loss_function(delta) * p(delta | data) d_delta )
    - credible_interval:
        formula: highest_posterior_density_interval(posterior, 0.95)
  decision_rules:
    - threshold: P(B > A) >= 0.95
    - threshold: expected_loss < 0.01 * baseline
    - threshold: credible_interval excludes zero
causal_inference:
  diff_in_diff:
    model: Y = beta_0 + beta_1 * treatment + beta_2 * post + beta_3 * (treatment * post) + epsilon
    estimand: beta_3
    assumption: parallel_trends
    diagnostics: placebo_test on pre-treatment periods, leads_and_lags plot
  instrumental_variables:
    conditions:
      - relevance: Z correlates with treatment (F-stat > 10)
      - exclusion: Z affects Y only through treatment
      - exchangeability: Z is as-if randomly assigned
    estimator: two_stage_least_squares
    diagnostics: weak_instrument_test (F-stat), overidentification_test (Sargan/Hansen)
  regression_discontinuity:
    design: cutoff assigns treatment
    bandwidth_selection: cross_validation or IK_method
    polynomial_order: 1 or 2
    robustness: placebo cutoff tests, bandwidth sensitivity
t_tests:
  two_sample:
    assumption: normality within groups, independence between groups
    variance_assumption: equal (pooled) or unequal (Welch)
    formula_t_stat: (mean_A - mean_B) / sqrt( s_p^2 * (1/n_A + 1/n_B) )
    welch_df: ( (s_A^2/n_A + s_B^2/n_B)^2 ) / ( (s_A^2/n_A)^2/(n_A-1) + (s_B^2/n_B)^2/(n_B-1) )
  nonparametric_alternative:
    mann_whitney_u: ordinal, no normality required
    permutation_test: exact distribution under null, any test statistic
multiple_testing_correction:
  bonferroni: alpha / m (m = number of comparisons)
  holm_bonferroni: sequentially reject smallest p-values
  benjamini_hochberg: controls false_discovery_rate
    formula: rank p-values, reject if p_(k) <= (k/m) * q
effect_size_metrics:
  cohens_d: (mean_A - mean_B) / s_pooled
  hedges_g: cohens_d * (1 - 3/(4*(n_A+n_B) - 9))
  risk_ratio: p_A / p_B
  odds_ratio: (p_A/(1-p_A)) / (p_B/(1-p_B))
  lift: (p_A - p_B) / p_B
python_implementation:
  libraries:
    - statsmodels (power, ztest, ttest, diff_in_diff)
    - scipy (distributions, tests)
    - pymc (bayesian models)
    - causalnex, dowhy (causal inference)
    - sequential_tests (pip install)