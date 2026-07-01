App Analytics Architect
Domain: app-dev Version: 1
Purpose
Architects mobile analytics — event taxonomy, conversion funnels, cohort retention, crash reporting, all under consent-first privacy.
Persona
Mobile analytics specialist. Expert in Firebase Analytics, Mixpanel, Sentry, and data pipelines.
Skills
  Event: design event taxonomy for mobile
  Funnel: build conversion funnels
  Retention: track cohort retention metrics (D1/D7/D30)
  Crash: integrate Sentry / Firebase Crashlytics with fatal vs non-fatal
  Privacy: implement consent-first analytics with granular opt-in
---
config.yaml
analytics:
  project_id: firebase-project-1234        # REQUIRED: Firebase project. Override per env.
  app_id: com.example.app                  # REQUIRED: Bundle ID / package name. Override per env.
  api_key: AIzaSy...                       # REQUIRED: Firebase API key. Override per env. DO NOT COMMIT.
  sentry_dsn: https://key@o0.ingest.sentry.io/0  # REQUIRED: Sentry project DSN. Override per env.
  event_prefix: app_                       # Prefix applied to all custom events. Default: app_
  autocapture_enabled: false               # Set true to capture screen_views, app_installs automatically
  consent:
    mode: explicit                         # explicit | implicit. explicit requires user action before tracking
    default_denied: true                    # If true, no events fire until consent granted
    storage_key: app_analytics_consent      # Key used in SharedPreferences / NSUserDefaults
  funnels:
    max_funnel_steps: 10                   # Hard cap. Exceeding triggers warning in pipeline validation
    default_timeout_seconds: 1800          # 30 min default. Override per funnel below.
  retention:
    cohort_periods: [1, 7, 30]             # D1 / D7 / D30 cohort windows
    lookback_days: 90                      # How far back to compute cohort rollups
    metric: retention_rate                 # Calculated as users_active_in_period / users_in_cohort
  crash:
    fatal_priority: high                   # Tag for sentry alerts
    nonfatal_priority: medium              # Tag for sentry alerts
    stacktrace_capture: true               # Always capture full stack on crash events
    breadcrumbs_enabled: true              # Attach user-action breadcrumbs to crash payload
---
BLUEPRINT.md
Event Taxonomy
1. App Lifecycle Events
  app_open            - Application launched. Properties: source(deeplink|icon|notification), timestamp
  app_close           - Application backgrounded / terminated. Properties: session_duration_seconds
  app_crash           - Unhandled exception captured by crash reporter. Properties: see crash section
  screen_view         - Screen entered. Properties: screen_name, screen_class, referrer
2. User Engagement Events
  user_signup         - Account created. Properties: method(email|google|apple|phone), tenant_id
  user_login          - Authentication completed. Properties: method, is_returning(bool)
  user_logout         - Session ended. Properties: session_length_seconds
  feature_used        - Feature accessed. Properties: feature_name, feature_group, trigger(button|swipe|voice)
3. Conversion Events
  trial_started       - Free trial begins. Properties: plan_tier, source(campaign|organic|referral)
  subscription_started - Paid subscription activated. Properties: plan_tier, price, currency, promo_code
  purchase_completed  - One-time in-app purchase. Properties: product_id, price, currency, quantity
  trial_cancelled     - Trial ended before conversion. Properties: reason, days_in_trial
  subscription_renewed - Auto-renewal succeeded. Properties: plan_tier, renewal_cycle(monthly|yearly)
4. Consent Gate Events
  consent_prompt_shown - Consent dialog displayed. Properties: prompt_version, region(gdpr|ccpa|lgpd)
  consent_granted      - User gave explicit consent. Properties: consent_type(all|analytics|crash|marketing), consent_version, userid
  consent_denied       - User denied consent. Properties: consent_type, consent_version, userid
  consent_revoked      - User revoked previously granted consent. Properties: consent_type, userid, days_active
  consent_updated      - User changed consent preferences. Properties: old_consent_types, new_consent_types
5. Error Events
  error_api            - API call failed. Properties: endpoint, status_code, error_message, retry_count
  error_validation     - Client-side validation failed. Properties: field_name, error_type, input_fragment
  error_permission     - Required permission denied by OS. Properties: permission_name, grant_result
All events carry standard properties: userid(string), timestamp(unix_ms), session_id(uuid), app_version(string), platform(ios|android).
---
Funnels & Funnel Analysis
Funnel definitions specify ordered steps, fallback paths, and timeout windows.
Standard Funnels
1. Onboarding Funnel
  Steps: app_open -> screen_view(welcome) -> user_signup -> screen_view(plan_picker) -> trial_started
  Timeout between steps: 1800s (30 min)
  Fallback: If user_signup fails, emit error_validation with field_name and continue tracking next open
  Drop-off points: screen_view(plan_picker) -> trial_started typically drops 40-60%
2. Subscription Funnel
  Steps: trial_started -> feature_used(count > 3 sessions) -> screen_view(payment) -> purchase_completed
  Timeout: 604800s (7 days) between trial_started and purchase_completed
  Fallback: trial_cancelled with reason captured as exit event
  Drop-off points: feature_used -> screen_view(payment) drops 30-50%
3. Deep-Link Activation Funnel
  Steps: app_open(source=deeplink) -> screen_view(linked_content) -> feature_used(feature_name=linked_feature)
  Timeout: 300s (5 min) — deep-link flows must convert fast
  Fallback: If screen_view(linked_content) does not match the deeplink target, emit error_deeplink with mismatch_reason
Funnel Validation Rules
  Each event in step must share a session_id
  Steps must be consecutive — no intervening events of other types break the funnel (re-ordered: intervening events of the same user but different session reset the step counter)
  Timeout resets partial progress — user must restart from step 1 after timeout expiry
  Report conversion_rate = users_reaching_last_step / users_entering_step_1
---
Retention Analysis
Cohort periods: D1 (1 day), D7 (7 days), D30 (30 days) post-acquisition.
Retention metric: retention_rate = users_active_in_cohort_period / users_in_cohort
Cohort assignment: user's first tracked event (app_open or user_signup whichever comes first) sets day 0.
Calculation rules:
  D1 retention: users who triggered at least one event on day 1 (24h after day 0)
  D7 retention: users who triggered at least one event on any of days 7-8 (168h-192h after day 0)
  D30 retention: users who triggered at least one event on any of days 30-35 (720h-840h after day 0)
  Lookback grace: +5 day window on D30 to account for weekly-active users
Computed fields per cohort:
  cohort_date, acquisition_source, platform, total_users, d1_active, d1_rate, d7_active, d7_rate, d30_active, d30_rate
Visualization: bar chart with cohort_date on x-axis, stacked rates per period. Use Mixpanel's built-in retention report or BigQuery rollup.
---
Crash & Error Reporting
Crash schema (event: app_crash):
  userid              string     - Affected user
  timestamp           unix_ms    - Crash time
  crash_type          string     - fatal | nonfatal
  error_class         string     - NullPointerException, SIGSEGV, NSException
  error_message       string     - Human-readable crash reason
  stacktrace          string     - Full stack trace. Base64 encoded for transport
  thread_name         string     - Thread where crash occurred
  app_version         string     - Build version at crash time
  os_version          string     - OS version at crash time
  device_model        string     - Device model identifier
  orientation         string     - portrait | landscape at time of crash
  memory_used_mb      float      - App memory footprint at crash
  breadcrumbs         array      - Last 50 user-action events before crash, with timestamps
Crash classification:
  Fatal: SIGSEGV, SIGABRT, NSException (unhandled), ANR, OOM
  Nonfatal: NSError (handled), caught exception, network timeout, background crash
Processing pipeline:
  1. Crashlytics/Sentry captures app_crash event
  2. Breadcrumbs attached from local logged event buffer (max 50, FIFO)
  3. Server side: deduplicate by (userid, error_class, stacktrace hash) within 24h window
  4. Alert rules: >5 fatal crashes per minute on any version -> pagerduty critical
  >50 nonfatal crashes per minute on any version -> slack notification medium
Crash rate reporting: crashes_per_session = count(app_crash) / count(app_open) per day.
---
Privacy & Consent Framework
Consent gate flow:
  1. app_open -> check consent storage (storage_key from config)
  2. If no consent stored: show consent_prompt_shown with prompt_version
  3. User action -> consent_granted | consent_denied | consent_revoked
  4. If consent_granted: set tracking enabled for allowed consent_types
  5. If consent_denied: suppress ALL analytics event emission for duration of session
  6. If consent_revoked: purge PII from event queue (userid replaced with hash), stop further emission
  7. consent_updated emitted on any change to existing consent preferences
Consent types:
  analytics - Standard event and funnel tracking. Default behavior when granted.
  crash     - Crash report collection. Requires separate opt-in per GDPR/CCPA guidance.
  marketing - Advertising ID, attribution, push notification targeting.
Data retention: if consent revoked, batch-delete all rows with matching userid from analytics tables within 72h. Emit consent_revoked before deletion for audit trail.
GDPR regions (EU/EEA): force explicit mode. Default denied. Consent storage must persist across app reinstalls (keychain / credential manager).
CCPA regions (California): allow opt-out at any time. Default denied for minors under 16.
LGPD regions (Brazil): same rule as GDPR — explicit consent with full audit trail.
---
Quality Gate Criteria
Blueprint passes quality gate when all 5 criteria score >= 80/100.
1. Event completeness (weight: 25%)
  Minimum 20 event types across lifecycle, engagement, conversion, consent, and error categories
  Each event must have at least 3 defined properties + userid + timestamp
  Consent events must match consent types from privacy section (granted, denied, revoked)
2. Funnel completeness (weight: 20%)
  At least 3 defined funnels with ordered step lists
  Each funnel must specify timeout window and fallback path
  Funnel drop-off points must be documented
3. Retention completeness (weight: 15%)
  At least 3 cohort periods defined
  Retention metric formula explicitly stated
  Lookback window and cohort assignment rules documented
4. Crash reporting (weight: 20%)
  Fatal and nonfatal classification criteria defined
  Crash schema with minimum 12 properties (per spec above)
  Alert rules and deduplication logic specified
5. Privacy integration (weight: 20%)
  Consent gate flow documented end-to-end
  Consent type taxonomy matches event taxonomy (consent_granted / consent_denied / consent_revoked use same consent_type values)
  Regional compliance notes (GDPR / CCPA / LGPD) present
  Revocation data-purging policy stated
Score function: score = sum of (criterion_score * weight) where criterion_score is 0-100 based on checklist completion.
---
person.md
This document is retired. All persona guidance lives in the blueprint opening section (Persona + Skills block above). If you need persona context — role, expertise, tools — refer to the opening block at the top of BLUEPRINT.md. Do not read this file. If you find yourself here during an automated run, skip it and proceed to config.yaml for integration parameters.