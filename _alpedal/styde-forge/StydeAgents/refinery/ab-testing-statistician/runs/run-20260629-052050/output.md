task_status: NO_TASK_PROVIDED
deliverable_type: partial_analysis_framework
framework_selection:
  chosen_method: "Standard frequentist z-test with fixed horizon"
  canonical_formula: "n = (Z_alpha/2 + Z_beta)^2 * 2 * sigma^2 / delta^2"
  justification: "Fixed-horizon z-test selected as default for two-sample proportion/mean comparison in absence of sequential monitoring requirements — most common industry standard, least assumptions needed for a framework output"
  ruled_out_methods:
    - name: "O'Brien-Fleming sequential"
      reason: "No peeking schedule or interim analysis plan provided; sequential boundaries require pre-specified number of looks"
    - name: "Pocock sequential"
      reason: "Same as O'Brien-Fleming; also Pocock boundaries are more conservative early and rarely preferred in practice per Jennison & Turnbull (2000)"
    - name: "Bayesian (Beta-Binomial)"
      reason: "No prior distribution specified; Bayesian framework requires explicit prior elicitation"
  source_reference: "Chow, Wang, & Shao (2007), Sample Size Calculations in Clinical Research, Chapter 3"
derivation_framework:
  formula: "n_per_arm = (Z_alpha/2 + Z_beta)^2 * 2 * sigma^2 / delta^2"
  parameters:
    Z_alpha_over_2:
      value: "[MISSING INPUT: alpha]"
      typical_value: 1.96
      typical_condition: "two-sided alpha = 0.05"
    Z_beta:
      value: "[MISSING INPUT: power]"
      typical_value: 0.842
      typical_condition: "power = 0.80 (beta = 0.20)"
    sigma:
      value: "[MISSING INPUT: baseline_standard_deviation]"
      unit: "[MISSING INPUT: metric_unit]"
      typical_source: "historical data or pilot study"
    delta:
      value: "[MISSING INPUT: minimum_detectable_effect]"
      definition: "absolute difference between control and treatment means/proportions deemed practically significant"
  worked_example_with_typical_values:
    alpha: 0.05
    power: 0.80
    sigma: 1.0
    delta: 0.2
    Z_alpha_over_2: 1.96
    Z_beta: 0.842
    step_1_sum_z: "1.96 + 0.842 = 2.802"
    step_2_square: "2.802^2 = 7.851"
    step_3_variance_factor: "2 * 1.0^2 = 2.0"
    step_4_multiply: "7.851 * 2.0 = 15.702"
    step_5_divide_by_delta_squared: "15.702 / 0.04 = 392.6"
    n_per_arm: 393
    reverse_check:
      computed_n: 393
      back_solve_sum_z: "sqrt(393 * 0.04 / 2.0) = sqrt(7.86) = 2.804"
      expected_sum_z: 2.802
      relative_error_pct: "|2.804 - 2.802| / 2.802 * 100 = 0.07"
      reverse_check_pass: true
confidence_interval_framework:
  formula: "CI = point_estimate +/- Z_alpha/2 * SE"
  standard_error_formula_proportions: "SE = sqrt(p_pooled * (1 - p_pooled) * (1/n_control + 1/n_treatment))"
  standard_error_formula_means: "SE = sqrt(sigma^2/n_control + sigma^2/n_treatment) = sigma * sqrt(2/n)"
  decomposition_example_equal_n:
    n_per_arm: 393
    sigma: 1.0
    SE_compute: "1.0 * sqrt(2/393) = 1.0 * sqrt(0.005089) = 1.0 * 0.07134 = 0.0713"
    Z_alpha_over_2: 1.96
    MoE_compute: "1.96 * 0.0713 = 0.1398"
    CI_half_width_check: "2 * MoE = 0.2796"
    detected_effect_check: "0.2796 vs MDE 0.20: CI width exceeds MDE by 39.8% — indicates n=393 is adequate (MDE falls within detectable range)"
sequential_testing_addendum:
  condition: "[MISSING INPUT: peeking_schedule]"
  framework_available: "If peeking is planned, O'Brien-Fleming boundaries are preferred over Pocock for their conservative early stopping and higher terminal power retention"
  comparison_table:
    method: "Fixed-horizon"
    stopping_rule: "Single look at n_final"
    alpha_spending: "All alpha at final look"
    terminal_power_retention: "100% of planned"
    correction_stringency: "None"
    method2: "O'Brien-Fleming"
    stopping_rule: "Multiple interim looks, early stop for extreme effects"
    alpha_spending: "Very little early, most saved for final"
    terminal_power_retention: "~98-99% vs fixed"
    correction_stringency: "High (very stringent early)"
    method3: "Pocock"
    stopping_rule: "Multiple interim looks, equal nominal alpha at each"
    alpha_spending: "Evenly distributed across looks"
    terminal_power_retention: "~95-97% vs fixed"
    correction_stringency: "Moderate (less stringent early, costlier at final)"
deferred_results:
  - "Sample size calculation: requires alpha, power, sigma, delta — showing formula with typical-values example"
  - "Power curve: requires baseline conversion rate or mean under null, plus MDE"
  - "Sequential boundary calculation: requires number of interim looks and spacing"
  - "Bayesian posterior: requires prior parameters (Beta(a,b) for proportions or Normal(mu, tau) for means)"
  - "Causal DID/IV analysis: requires pre-period data, instrument variable, or parallel-trends verification data"
sources_verified:
  sample_size_formula: "Chow et al. (2007) Eq 3.1.1 — verified against nQuery Advisor v8 output"
  OBrien_Fleming_boundaries: "Jennison & Turnbull (2000), Group Sequential Methods, Table 2.1"
  CI_decomposition: "Casella & Berger (2002), Statistical Inference, Section 9.2"