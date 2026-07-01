event_taxonomy:
  schema_version: 1.0
  naming_convention: snake_case, prefixed by domain
  standard_properties:
    - app_version
    - platform
    - os_version
    - device_model
    - session_id
    - timestamp_utc
    - user_id (hashed)
    - consent_level
  domains:
    onboarding:
      events:
        - onboarding_start {method: email|google|apple}
        - onboarding_step_view {step_name, step_number}
        - onboarding_complete {time_to_complete_s}
        - permission_grant {permission_type, granted: boolean}
      funnel: [onboarding_start, onboarding_step_view, onboarding_complete]
    engagement:
      events:
        - screen_view {screen_name, referrer, duration_ms}
        - feature_used {feature_name, feature_group}
        - content_shared {target_platform, content_type}
        - search_performed {query_hash, result_count}
      funnel: [screen_view, feature_used, content_shared]
    conversion:
      events:
        - product_view {product_id, category, price}
        - add_to_cart {product_id, quantity, price}
        - checkout_start {cart_total, item_count}
        - purchase_complete {order_id, revenue, currency, payment_method}
      funnel: [product_view, add_to_cart, checkout_start, purchase_complete]
    retention:
      metric: day_N_retention
      cohort_period: daily
      windows: [1, 3, 7, 14, 28, 60]
      trigger_event: session_start
      return_event: any_screen_view
    crash:
      tool: sentry + firebase_crashlytics_dual
      breadcrumbs: all analytics events
      context: device_info, network_state, memory_pressure
      grouping: error_class + stack_hash
      alert_threshold: 0.1% crash_free_rate_drop_per_hour
    privacy:
      consent_model: tcf_2.0_gdpr_ccpa_dual
      analytics_start: after_consent_given
      data_retention: 13_months_rolling
      anonymization: user_id_hmac_sha256_before_transmission
      opt_out: stop_all_event_fire + delete_backend_data
production_checklist:
  offline_queuing: true
  max_queue_size: 500_events
  flush_on_reconnect: true
  sampling:
    method: adaptive
    base_rate: 1.0
    max_load_reduction: 0.1
    config_endpoint: /analytics/sampling
  multi_touch_attribution:
    model: time_decay_linear
    window: 7_days
    touch_points: [push_open, search, product_view, checkout_start]
  push_analytics:
    events: [notification_received, notification_opened, notification_dismissed]
    enrich: campaign_id, message_type, a_b_variant
  ab_test_hooks:
    event: experiment_exposure {experiment_id, variant, timestamp}
    metric_events: all_conversion_funnel_events
  schema_migration:
    version_field: event_version
    backward_compatible_aliases: true
    deprecated_events: keep_30_days_then_drop
  data_sampling_methodology:
    production: deterministic_hash_sampling_mod_100
    debug: full_fidelity_with_user_id_log
    replay: event_sequencer_with_original_timestamps