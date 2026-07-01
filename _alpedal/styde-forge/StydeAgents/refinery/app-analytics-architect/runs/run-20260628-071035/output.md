BLUEPRINT.md
App Analytics Architect
Domain: app-dev
Version: 1.1
Purpose
Architects mobile analytics. Event tracking, funnels, retention, crash reporting, and production-grade data completeness.
Persona
Mobile analytics specialist. Expert in Firebase Analytics, Mixpanel, Sentry, data pipelines, and consent-first instrumentation.
Core event taxonomy
User lifecycle
  event: user_signup
  properties: method (email/google/apple), referral_source, account_type
  event: user_login
  properties: method, previous_session_timestamp_ms, is_returning
  event: user_logout
  properties: session_duration_ms, reason (manual/timeout)
  event: account_deletion
  properties: reason_category, account_age_days, linked_services
Onboarding
  event: onboarding_started
  properties: version, locale
  event: onboarding_step_completed
  properties: step_name, step_index
  event: onboarding_completed
  properties: steps_total, duration_s, skipped_steps
  event: onboarding_abandoned
  properties: last_step_name, steps_completed
Engagement
  event: screen_view
  properties: screen_name, screen_class, previous_screen, referrer
  event: feature_used
  properties: feature_name, feature_category, source_screen
  event: content_viewed
  properties: content_id, content_type, content_category
  event: content_shared
  properties: content_id, share_method, channel
  event: search_performed
  properties: query_length, result_count, search_category
  event: session_started
  properties: session_id, app_version, os_version
  event: session_ended
  properties: session_duration_s, screens_visited, events_in_session
Conversion
  event: product_viewed
  properties: product_id, product_category, price, currency
  event: add_to_cart
  properties: product_id, quantity, unit_price, currency
  event: begin_checkout
  properties: cart_total, item_count, currency, coupon_code
  event: checkout_step_completed
  properties: step_name, step_number
  event: purchase_completed
  properties: order_id, total, currency, payment_method, item_ids
  event: purchase_failed
  properties: error_code, error_message, payment_method
  event: subscription_started
  properties: plan_id, trial_period_days, billing_cycle
  event: subscription_cancelled
  properties: plan_id, tenure_days, reason_category
Error tracking
  event: api_error
  properties: endpoint, status_code, error_code, retry_count, latency_ms
  event: client_error
  properties: error_type (crash/ANR/uncaught), stack_trace_hash, screen_name
  event: rate_limit_hit
  properties: endpoint, retry_after_s, current_quota_used
  event: network_failure
  properties: error_type, retry_attempt, device_connectivity_type
Crash and stability
  event: app_crash
  properties: exception_class, stack_hash, thread_name, app_version, os_version, device_model, free_ram_mb, free_disk_mb, app_running_state (foreground/background)
  event: anr_occurred
  properties: anr_type (input_dispatch/broadcast/service), blocked_duration_ms, main_thread_state, cpu_usage_pct
  event: crash_recovered
  properties: recovery_method (restart/fallback/cold_start), last_crash_timestamp, crash_count_24h
  event: breadcrumb
  properties: breadcrumb_type (navigation/network/user_action/state_change), timestamp, screen_context, data_key, data_value
  event: signal_handler_fired
  properties: signal_number, signal_name, fault_address, register_dump_hash
Retention
  event: return_visit
  properties: days_since_last_visit, previous_frequency_bucket (daily/weekly/monthly/churned), session_count_to_date, cumulative_sessions
  event: feature_reengagement
  properties: feature_name, days_since_last_feature_use, reengagement_channel (push/in_app/deep_link/none)
  event: session_quality
  properties: session_duration_bucket (<10s/10-60s/1-5m/5-30m/30m+), actions_per_minute, completion_rate_pct
  event: churn_risk_flag
  properties: risk_level (low/medium/high), inactivity_days, prior_session_quality_score, push_opt_out
  event: deep_linked_session
  properties: deeplink_url, campaign_id, source_app, content_type
  event: referral_redeemed
  properties: referrer_id, reward_type, total_referrals_to_date
Push notification send events
  event: push_scheduled
  properties: campaign_id, schedule_type (immediate/scheduled/trigger), target_segment, message_template
  event: push_sent
  properties: campaign_id, push_provider (fcm/apns), recipient_count, message_type (promo/transactional/reengagement)
  event: push_delivered
  properties: campaign_id, device_online_at_send, app_in_foreground, delivery_latency_ms
  event: push_clicked
  properties: campaign_id, target_screen, click_through_latency_s, conversion_attributed
  event: push_dismissed
  properties: campaign_id, notification_type, dismiss_reason (swipe/clear_all/timeout)
  event: push_opt_in
  properties: source_screen, prompt_type (system/custom), previous_opt_out_count
  event: push_opt_out
  properties: trigger_reason, last_push_category, days_since_last_push
Privacy
  event: consent_granted
  properties: consent_type (analytics/ads/push/third_party), version, consent_method
  event: consent_withdrawn
  properties: consent_type, previous_duration_days
  event: data_deletion_requested
  properties: scope (account/analytics/all), deletion_method (automated/manual)
  event: gdpr_export_requested
  properties: data_categories_requested
  event: ccpa_opt_out
  properties: source_page, method
Conversion funnels
Trial-to-paid funnel
  step_1: signup_completed
  step_2: onboarding_completed
  step_3: feature_used (core value feature)
  step_4: subscription_started
  step_5: purchase_completed
Onboarding-to-retention
  step_1: onboarding_started
  step_2: onboarding_step_completed (step_3_or_later)
  step_3: content_viewed (within 24h)
  step_4: return_visit (day 7)
  step_5: session_quality (7-day streak)
Purchase funnel
  step_1: product_viewed
  step_2: add_to_cart
  step_3: begin_checkout
  step_4: checkout_step_completed (payment)
  step_5: purchase_completed
Push re-engagement funnel
  step_1: push_sent
  step_2: push_delivered
  step_3: push_clicked
  step_4: screen_view (target screen)
  step_5: feature_used (target feature)
Retention cohorts
Metric definitions
  D1 retention: users who return within 1 day of install
  D7 retention: users who return within 7 days
  D28 retention: users who return within 28 days
  Weekly sticky: DAU/WAU ratio on rolling 7d window
  Feature stickiness: feature_dau / feature_wau
Rolling cohort builder
  period: daily, weekly, monthly
  measure: active_users, return_rate, session_count, cumulative_revenue
  segment_by: acquisition_source, device_os, subscription_tier, region
Churn prediction triggers
  inactivity >= 7 days AND session_quality_previous < 0.3
  push_opt_out AND feature_reengagement_count = 0
  consecutive_low_quality_sessions >= 5
Crash data pipeline (Sentry + Firebase Crashlytics)
Crash event schema
  payload includes: exception_class, stack_hash, thread_name, app_version_code, os_version, device_model, free_ram_mb, free_disk_mb, app_version_name, orientation, locale, battery_pct
SDK integration
  sentry: source = 'sentry_sdk' | breadcrumb buffer = last 50 before crash | send_on_crash = true
  crashlytics: source = 'firebase_crashlytics' | custom_keys = ['last_screen', 'build_variant', 'experiment_group']
Alert thresholds
  crash_free_rate < 99.5% on any version → pager
  new_error_group > 0 in staging deploy → block rollout
  same_error_hash hit > 100 sessions in 1h → auto-escalation
Production completeness checklist
All domains MUST satisfy the following before deployment.
Offline event queuing
  - Queue is disk-backed, capped at 10,000 events
  - Flush strategy: batch every 30s OR every 50 events
  - Retry on failure: exponential backoff (1s, 2s, 4s, 8s, max 60s)
  - Max offline age: 72h; events older than 72h are dropped
  - Storage quota: 5 MB max; oldest events evicted first
Sampling and rate-limit strategy
  - Adaptive sampling: sample_rate = min(1.0, target_events_per_hour / current_hourly_volume)
  - Rate limit: 500 events/min per device; excess queued with priority drop
  - Degradation: when queue > 2000 events, sample non-critical event types at 0.5
  - Always-collected events: purchase, crash, error, consent, push_sent
Multi-touch attribution model
  - Supported models: first_touch, last_touch, linear, time_decay (half-life 7d), u_shaped
  - Attribution window: 30 days before conversion, 1 day after
  - Source tracking: utm_params, deeplink referrer, appsflyer_id (when available), google_install_referrer
  - Channel deduplication: dedupe on (campaign_id AND device_id AND event_timestamp within 5s)
Push notification event tracking
  - Complete send-deliver-click-dismiss lifecycle tracked as defined in events above
  - Attribution: push_clicked events carry campaign_id and target_screen
  - Conversion: push_clicked → screen_view → feature_used funnel tracks lift
  - A/B test: campaign payload includes experiment_id and variant_id
A/B test analytics hooks
  - Event property: experiment_id and variant_id on all conversion and engagement events
  - Session context: experiment_assignments sent as user properties at session_started
  - Day-zero analysis: bucket by variant_id and aggregate by day count post-assignment
  - Minimum sample: 500 users per variant before reporting a winner
Event versioning and schema migration
  - Event schema version tracked as event property `schema_v` (integer, semver)
  - Breaking change: create new event name (e.g. purchase_v2) and mark old as deprecated
  - Non-breaking addition: add property with default=null; all downstream dashboards treat null as unknown
  - Deprecation: remove old event after 2 full release cycles (e.g. 2 app updates) AND zero active sessions
  - Migration test: duplicate events to both old and new schema for 1 release cycle before switching
Data-sampling methodology
  - Sampling method: deterministic hash of (device_id, event_name, day) → keep if hash < sample_rate * MAX_HASH
  - Consistency: same device always sampled or not on a given day for a given event
  - Reporting: sampled proportion tracked per event per day as user property `sampling_weight`
  - Accuracy threshold: lift calculation requires relative standard error < 5%
  - Debug mode: internal builds send at 100% regardless of sample rate
config.yaml
event_schema:
  enforce_required_properties: true
  strict_mode: blocked_event_types:
    - purchase_completed
    - app_crash
    - consent_granted
    - push_sent
  version_tracking: schema_v_enabled: true
sampling:
  adaptive_sampling: true
  target_events_per_hour: 10000
  default_rate: 1.0
  min_rate: 0.01
  degradation_threshold_queue_size: 2000
  degradation_rate: 0.5
  always_collect:
    - purchase_completed
    - app_crash
    - consent_granted
    - push_sent
    - api_error
rate_limiting:
  events_per_minute_per_device: 500
  excess_policy: queue_with_priority_drop
  queue_max_size: 10000
  queue_storage_cap_mb: 5
  offline_max_age_hours: 72
  retry_backoff_base_seconds: 1
  retry_backoff_max_seconds: 60
attribution:
  enabled: true
  models:
    - first_touch
    - last_touch
    - linear
    - time_decay
    - u_shaped
  time_decay_half_life_days: 7
  attribution_window_days_before: 30
  attribution_window_days_after: 1
  dedup_window_ms: 5000
  dedup_keys:
    - campaign_id
    - device_id
    - event_timestamp
crash:
  crash_free_rate_threshold_pct: 99.5
  pager_alert_on_threshold_break: true
  new_error_group_block_rollout: true
  auto_escalation_threshold_sessions_per_hour: 100
  breadcrumb_buffer_size: 50
  sdk:
    sentry: enabled
    crashlytics: enabled
push:
  track_lifecycle: true
  lifecycle_events:
    - push_scheduled
    - push_sent
    - push_delivered
    - push_clicked
    - push_dismissed
    - push_opt_in
    - push_opt_out
  ab_test_property_default: experiment_id
  ab_test_variant_default: variant_id
retention:
  cohorts:
    daily_retention: true
    weekly_retention: true
    monthly_retention: true
  sticky_metrics:
    - dau_wau_ratio
    - feature_dau_wau_ratio
  churn_triggers:
    inactivity_days: 7
    min_quality_score: 0.3
    consecutive_low_quality_sessions: 5
compliance:
  consent_version: 2
  enforcement:
    - event_type: all
      require_consent: [analytics]
    - event_type: push_scheduled
      require_consent: [push]
    - event_type: purchase_completed
      require_consent: []