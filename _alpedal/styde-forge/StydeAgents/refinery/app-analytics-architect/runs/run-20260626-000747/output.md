EVENT TAXONOMY
Mobile event schema: snake_case, prefix by screen/feature.
Standard properties: session_id, app_version, os_version, device_model, timestamp_utc, locale, connection_type.
Critical events:
auth_signup_completed { method: email|google|apple }
auth_login_succeeded { method, mfa_used: bool }
main_feed_impression { item_count, scroll_depth_px }
content_shared { platform: whatsapp|twitter|clipboard }
payment_checkout_started { currency, item_count }
payment_checkout_succeeded { amount, payment_method }
payment_checkout_failed { reason_code, amount }
onboarding_step_viewed { step_name, step_number }
onboarding_completed { total_steps, time_seconds }
deep_link_opened { link_source, destination_screen }
push_notification_tapped { campaign_id, message_type }
search_performed { query_length, result_count }
search_no_results { query_text_hashed }
subscription_trial_started { product_id, trial_duration_days }
subscription_converted { trial_days_used, promo_applied: bool }
FUNNEL DESIGN
Funnel 1: Sign-up to First Action
Sign-up impression -> sign-up started -> email verified -> onboarding step_1 -> onboarding completed -> main_feed_impression
Funnel 2: Discovery to Conversion
search_performed -> product_detail_viewed -> add_to_cart -> checkout_started -> checkout_succeeded
Funnel 3: Push to Retention
push_received -> push_tapped -> app_opened_from_push -> session_active_30s -> session_active_5m
Funnel 4: Subscription
paywall_impressed -> trial_started -> trial_day_3_active -> trial_day_6_active -> subscription_converted -> subscription_renewed
RETENTION
Cohort definition: signup_date (D0).
Measurements: D1, D3, D7, D14, D28, D60, D90.
Core action for retention: session with >=2 screen views OR any content_shared.
Rolling retention (not rigid): user qualifies if they performed the action ANY day since last qualifying day, not only exact D+N.
Power-user threshold: >=3 sessions in a calendar week AND >=1 content_shared.
Track weekly active users (WAU) / monthly active users (MAU) ratio. Target >0.4 for healthy stickiness.
CRASH REPORTING
Sentry integration: init in AppDelegate/Application.onCreate, before any other SDK.
Attach user context: anonymous_id (not PII), app_version, os.
Breadcrumbs: add on every navigation event + network request.
Crash-free session rate target: >99.5%.
Symbolication: upload dSYM (iOS) / mapping files (Android) on every CI build.
Fatal vs non-fatal: tag ANR (Android) / app freeze (iOS) as non-fatal but alert at >1% per version.
Alert thresholds:
Critical: crash-free rate drop >1% in 1h.
Warning: new error group >100 sessions in 24h.
Info: single-user crash count >5 in 1h.
PRIVACY CONSENT FIRST FLOW
Step 1: on first launch, show consent dialog with 3 toggles:
- Essential (always on): crash reporting, session count
- Analytics (opt-in): event tracking, funnel analysis, A/B test membership
- Personalization (opt-in): user properties, attribution, ad targeting
Step 2: store consent in UserDefaults/SharedPreferences + keychain hash.
Step 3: Firebase Analytics: setAnalyticsCollectionEnabled(analyticsConsented).
Step 4: Sentry: configure beforeSend callback that drops events if essential-only.
Step 5: Mixpanel: optOutTracking() / optInTracking() based on consent.
Data retention: delete user-level properties after 90d of inactivity.
GDPR/CCPA: expose /api/analytics/export and /api/analytics/delete endpoints from backend. Trigger from app -> firebase delete + sentry delete + mixpanel delete via their REST APIs.
Audit log: store consent_change events locally with ISO timestamp. Send to backend analytics_consent_audit topic. Never backfill events before consent was granted.