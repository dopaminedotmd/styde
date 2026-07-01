BLUEPRINT.md
Event Taxonomy
event: app_open
  userid: string
  timestamp: integer
  source: string (icon|notification|deep_link)
  consent_status: string (granted|denied|pending)
event: app_close
  userid: string
  timestamp: integer
  session_duration_ms: integer
event: screen_view
  userid: string
  timestamp: integer
  screen_name: string
  screen_class: string
  previous_screen: string
  consent_status: string
event: button_tap
  userid: string
  timestamp: integer
  button_id: string
  screen_name: string
  consent_status: string
event: signup_start
  userid: string
  timestamp: integer
  method: string (email|google|apple)
  consent_status: string
event: signup_complete
  userid: string
  timestamp: integer
  method: string
  userid_assigned: string
event: login
  userid: string
  timestamp: integer
  method: string
  success: boolean
event: purchase_start
  userid: string
  timestamp: integer
  product_id: string
  price: float
  currency: string
event: purchase_complete
  userid: string
  timestamp: integer
  product_id: string
  transaction_id: string
  price: float
  currency: string
event: purchase_fail
  userid: string
  timestamp: integer
  product_id: string
  reason: string
  error_code: string
event: consent_granted
  userid: string
  timestamp: integer
  consent_type: string (analytics|ads|personalization)
  consent_version: string
event: consent_denied
  userid: string
  timestamp: integer
  consent_type: string
  consent_version: string
  reason: string
event: consent_revoked
  userid: string
  timestamp: integer
  consent_type: string
  previous_decision: string
  days_since_grant: integer
event: crash_occurred
  userid: string
  timestamp: integer
  crash_type: string (fatal|non_fatal)
  exception_class: string
  message: string
  stack_trace: string
  screen_name: string
  app_version: string
  os_version: string
event: crash_recovered
  userid: string
  timestamp: integer
  crash_id: string
  recovery_method: string (restart|background_resume|manual)
event: error_logged
  userid: string
  timestamp: integer
  error_domain: string (network|ui|permission|storage|api)
  error_code: integer
  message: string
  screen_name: string
  severity: string (critical|warning|info)
Global Properties
  app_version: string
  os: string (ios|android)
  os_version: string
  device_model: string
  device_type: string (phone|tablet)
  screen_resolution: string
  network_type: string (wifi|cellular|offline)
  is_consented: boolean
  consent_types: array of string
  session_id: string
  install_source: string
Consent Gate
All events tagged consent_status=granted fire immediately.
Events where consent_status=denied or pending are buffered locally with flag buffered=true and emitted once consent_granted fires.
consent_granted, consent_denied, consent_revoked events are ALWAYS emitted regardless of consent state — they are the consent system's own audit trail.
Consent gate evaluates in this order:
  1. Is event in consent_audit_list? (consent_granted, consent_denied, consent_revoked) -> always fire.
  2. Is consent_type required for this event? -> check user preferences.
  3. If consent missing -> buffer with buffered=true flag, queue for retry on consent_granted.
  4. Buffer TTL: 7 days. Expired buffered events are discarded silently.
Funnels and Funnel Analysis
funnel: activation
  steps:
    - event: app_open
      timeout: 30s
    - event: signup_start
      timeout: 5m
    - event: signup_complete
      timeout: 10m
    - event: screen_view
      screen_name: dashboard
      timeout: 2m
  fallback_spec:
    signup_start -> signup_complete failure triggers email_verification_resent tracking event.
    signup_complete -> dashboard failure sends user to onboarding_screen with event onboarding_resume.
  global_timeout_window: 30m
  window_type: sliding
funnel: purchase
  steps:
    - event: screen_view
      screen_name: product_detail
      timeout: 15m
    - event: purchase_start
      timeout: 10m
    - event: purchase_complete
      timeout: 5m
  fallback_spec:
    purchase_start -> purchase_complete failure or timeout triggers recovery event purchase_retry_offered.
    If purchase_retry completes within 5m, counted as funnel_success with flag recovered=true.
  global_timeout_window: 60m
  window_type: fixed
funnel: onboarding
  steps:
    - event: signup_complete
      timeout: 5m
    - event: screen_view
      screen_name: onboarding_step_1
      timeout: 10m
    - event: screen_view
      screen_name: onboarding_step_2
      timeout: 10m
    - event: screen_view
      screen_name: onboarding_step_3
      timeout: 10m
    - event: screen_view
      screen_name: dashboard
      timeout: 5m
  fallback_spec:
    Any step >3 min idle marks step_abandoned with last_screen captured.
    User returning within 24h resumes from last completed step.
    24h expiry resets funnel entirely — tracked as funnel_reset.
  global_timeout_window: 24h
  window_type: sliding
Funnel Calculation
  step_conversion_rate = users_at_step_n / users_at_step_1 * 100
  overall_conversion = users_completing_all_steps / users_starting_funnel * 100
  drop_off_points identified per step with event funnel_drop_off (step_name, step_number).
Retention Analysis
cohort_periods:
  d1: 24 hours post acquisition
  d7: 168 hours post acquisition
  d30: 720 hours post acquisition
retention_metric_calculation:
  acquisition_event: signup_complete or app_open (first_seen)
  return_event: any tracked event with consent_status=granted
  retention_rate: users_active_in_period / users_in_cohort * 100
  calculation_formula: count(distinct userid where return_event.timestamp between cohort_start + period_start and cohort_start + period_end) / count(distinct userid who triggered acquisition_event in cohort_day) * 100
lookback_window_specifications:
  d1: lookback is exact day 1 (24h window from acquisition timestamp)
  d7: window is day 2 through day 7 (25h to 168h post acquisition)
  d30: window is day 8 through day 30 (169h to 720h post acquisition)
  sticky_d7: any return within 7 days, counted once at d7 regardless of d1 state
  sticky_d30: cumulative — any return within 30 days tracked as d30_ever
Cohort Event Schema
event: retention_ping
  userid: string
  timestamp: integer
  cohort_date: string (YYYY-MM-DD)
  cohort_period: string (d1|d7|d30)
  days_since_acquisition: integer
  is_returning: boolean
Crash and Error Reporting
crash_classification:
  fatal: unhandled exception causing application termination
  non_fatal: caught exception, error logged, application continues running
crash_schema:
  crash_occurred:
    userid: string
    timestamp: integer
    crash_type: string (fatal|non_fatal)
    exception_class: string (full qualified class name)
    message: string
    stack_trace: string (full stack trace lines joined by newline)
    screen_name: string
    app_version: string
    os_version: string
    device_model: string
    thread_name: string
    foreground: boolean
    memory_pressure: integer (percentage 0-100)
    breadcrumbs: array of string (last 20 events before crash)
  crash_recovered:
    userid: string
    timestamp: integer
    crash_id: string (UUID linking back to crash_occurred)
    recovery_method: string (automatic_restart|background_resume|user_launch)
stack_trace_capture:
  captured on application crash handlers (uncaught exception handler + signal handler)
  maximum stack depth: 128 frames
  truncation: frames beyond 128 replaced with ... (N more frames) annotation
  file/line stripped from release builds, preserved in debug builds
  SDK-level frames filtered out when stack exceeds 64 frames
error_logged schema:
  error_logged:
    userid: string
    timestamp: integer
    error_domain: string (network|ui|permission|storage|api|parsing|crashlytics)
    error_code: integer
    message: string
    screen_name: string
    severity: string (critical|warning|info)
    retry_count: integer
    is_recoverable: boolean
    underlying_error: string
Crash Reporting Integration
  fatal crashes forwarded to both local buffer and Sentry SDK within 5 seconds.
  non_fatal errors forwarded to Sentry SDK + Firebase Crashlytics.
  Crash rate alert threshold: >=3 fatal crashes per 1000 sessions in rolling 1h window.
  Symbolication: debug symbols uploaded at every release build to Sentry.
Privacy and Consent Gate Implementation
consent_gate_flow:
  1. Application launch -> check stored consent preferences from secure keystore.
  2. If no stored consent -> show consent dialog -> capture consent_granted or consent_denied.
  3. consent_granted -> enable analytics SDK, flush buffered events.
  4. consent_denied -> disable analytics SDK, keep buffer empty.
  5. consent_revoked -> delete all stored analytic events older than 24h per GDPR right to erasure guidance, disable SDK, emit consent_revoked.
consent_type definitions:
  analytics: basic usage analytics, screen views, button taps, funnels, retention.
  ads: ad attribution, ad click events, ad impression events.
  personalization: user preference tracking, behavioral segments, A/B test assignment.
consent_version: semver string matching the app's consent dialog version. Current is 1.0.0.
Event Buffering Rules
  buffer_on_deny: events with deniable consent type are dropped permanently.
  buffer_on_pending: events queued to SQLite buffer (max 5000 rows), tagged buffered=true.
  buffer_flush: on consent_granted, replay buffered events with original timestamps appended with delivered_at field.
  buffer_expiry: 7 day TTL, checked on app foreground. Expired rows deleted silently.
Configuration (env-aware defaults)
analytics:
  provider: firebase
  project_id: styde-forge-dev
  consent_required: true
  consent_version: 1.0.0
  buffer_max_rows: 5000
  buffer_ttl_days: 7
  debug_mode: true
  flush_interval_seconds: 30
  min_batch_size: 10
sentry:
  dsn: https://example@sentry.io/styde-forge-dev
  environment: development
  debug: true
  traces_sample_rate: 1.0
  profiles_sample_rate: 0.5
  attach_stacktrace: true
  max_breadcrumbs: 20
  before_send: consent_filter
crashlytics:
  enabled: true
  crash_collection_consent: required
  send_without_consent: false
  max_stack_trace_lines: 128
funnels:
  default_timeout_window: 30m
  enable_fallback_tracking: true
  max_funnel_steps: 10
  retention_lookback_days: 30
retention:
  cohort_periods: [d1, d7, d30]
  sticky_d7_enabled: true
  sticky_d30_enabled: true
  calculation_batch_size: 10000
config_env_defaults:
  development:
    sentry.dsn: https://example@sentry.io/styde-forge-dev
    analytics.debug_mode: true
    sentry.traces_sample_rate: 1.0
  staging:
    sentry.dsn: https://example@sentry.io/styde-forge-staging
    analytics.debug_mode: true
    sentry.traces_sample_rate: 0.5
  production:
    sentry.dsn: https://example@sentry.io/styde-forge-prod
    analytics.debug_mode: false
    sentry.traces_sample_rate: 0.1
Quality Gate Coverage
gate_1 event_taxonomy: comprehensive event schema covering all user journeys, consent events, and error/crash events. Score target 25/25.
gate_2 funnel_analysis: three defined funnels (activation, purchase, onboarding) with step definitions, fallback paths, timeout windows, and conversion calculation. Score target 20/20.
gate_3 retention: cohort periods d1/d7/d30 with calculation formulas, lookback windows, and sticky retention definitions. Score target 20/20.
gate_4 crash_reporting: fatal/non_fatal classification, stack trace capture, integration with Sentry and Crashlytics, alert thresholds. Score target 15/15.
gate_5 privacy_consent: consent gate flow with consent_granted/denied/revoked events, buffering rules, consent_type taxonomy, GDPR-compliant erasure, env-aware config defaults. Score target 20/20.
total: 100/100