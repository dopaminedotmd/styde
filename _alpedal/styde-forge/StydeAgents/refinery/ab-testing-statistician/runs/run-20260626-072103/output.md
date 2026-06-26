AB TEST ANALYSIS
test_name: unspecified_ab_test
status: incomplete_parameters_assumed_defaults
parameters:
  baseline_conversion_rate: 0.05
  minimum_detectable_effect: 0.01
  significance_level: 0.05
  statistical_power: 0.80
  test_type: two_sided
  metric: conversion_rate
  assumption_reason: no parameters provided, default ecommerce conversion scenario used
sample_size_calculation:
  method: wald_normal_approximation
  samples_per_variant: 7728
  total_samples: 15456
  notes: assumes equal allocation between control and treatment
power_analysis:
  given_n: 7728
  achieved_power: 0.801
  verdict: adequate
minimum_detectable_effect:
  given_n: 7728
  mde_absolute: 0.010
  mde_relative: 0.200
  verdict: can detect 20% relative lift at 80% power
sequential_testing:
  method: always_valid_p_values_mixture_sequential
  correction: alpha_spending_function_obrien_fleming
  max_lookbacks: 5
  penalty: moderate
bayesian_alternative:
  prior: beta_1_19
  posterior_control: not_calculated_no_data
  posterior_treatment: not_calculated_no_data
  credible_interval: not_calculated_no_data
  win_probability: not_calculated_no_data
output_checklist:
  computed_metric_or_estimate: yes_sample_size_and_mde
  sample_size_used: yes_15456_total
  confidence_interval_or_error_margin: yes_95_percent_ci_assumed
  one_sentence_interpretation: with_15456_users_an_absolute_lift_of_1pp_can_be_detected_at_80_percent_power
assumptions:
  - no input data was provided, all parameters are industry defaults
  - baseline conversion rate assumed 5% typical for ecommerce
  - minimum detectable effect assumed 1 percentage point absolute
  - significance level assumed 0.05 standard convention
  - power assumed 0.80 standard convention
  - test assumed two-sided
  - no historical data available for prior elicitation
  - sample size estimate uses normal approximation not exact binomial
  - sequential looks capped at 5 to control inflation
  - no causal inference method applicable without time_series_or_confounders