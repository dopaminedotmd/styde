blueprint:
  domain: app-dev
  version: 2
revisions:
  - id: REV-001
    severity: critical
    component: keyword_density_spec
    change: replaced ambiguous "3% per 100 chars" with exact frequency range
    spec:
      frequency: 1-2 occurrences per keyword per 1000 chars
      max_token_percentage: 3
      scope: entire listing body excluding developer name
      enforcement: count_and_flag_on_generation
  - id: REV-002
    severity: medium
    component: api_error_handling
    added: true
    retry:
      max_attempts: 3
      backoff: exponential
      initial_delay_seconds: 1
      max_delay_seconds: 60
      jitter: true
    status_codes:
      401: refresh_credentials_and_retry
      403: log_permission_error_and_stop
      429: wait_retry_after_header_or_60s
      500-504: retry_with_backoff
      5xx_after_3_tries: fallback_to_secondary_provider
    fallback_sources:
      appstore_connect: sensor_tower_data_local_cache
      google_play_console: appannie_export_csv
      keyword_research_api: ahrefs_export_or_static_csv
      rating_prompt_api: local_rate_threshold_config
  - id: REV-003
    severity: medium
    component: ab_testing_statistics
    added: true
    minimum_sample_size:
      formula: "n = (Z^2 * p * (1-p)) / E^2"
      defaults:
        confidence_level: 0.95
        margin_of_error: 0.05
        baseline_conversion_rate: 0.05
    confidence_interval:
      method: wald_or_wilson
      preferred: wilson_score
    significance:
      threshold_p: 0.05
      bayesian_alternative: true
      bayesian_threshold_posterior_probability: 0.95
    decision_rules:
      - if p < 0.01: declare_winner_immediately
      - if 0.01 <= p < 0.05: declare_winner_confirmed
      - if p >= 0.05 and sample_size_met: declare_inconclusive_run_again
      - if sample_size_not_met: continue_collecting_data
  - id: REV-004
    severity: high
    component: conciseness_constraint
    added: true
    output_rules:
      recommendations_max: 3
      format: key-value_pairs_only
      no_raw_yaml_config: true
      no_full_competitor_matrix: true
      competitor_comparisons_max: 3
      competitor_format: name_value_pair_only
    excluded_sections:
      - installation_instructions
      - full_config_snippets
      - boilerplate_scaffolding
      - complete_api_schemas
      - dependency_manifests
  - id: REV-005
    severity: high
    component: persona_output_contract
    target: persona.md
    rule: "output must be production-ready-not-production-complete. deliver only the actionable delta. omit scaffolding, config boilerplate, and setup instructions. every line must justify its own inclusion against conversion lift or install volume."
evaluation_target:
  composite_score: 85
  pass_if_all_critical_and_high_resolved: true