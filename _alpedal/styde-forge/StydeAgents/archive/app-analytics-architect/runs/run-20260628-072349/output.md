App Analytics Architect -- teacher feedback applied
File: UEPRINT.md
Blueprint: App Analytics Architect  v3.0.1
Domain: app-dev
Last reviewed: 2026-06-26
Usage
This blueprint generates mobile app analytics configurations: event taxonomies, funnel definitions, retention cohort queries, and crash reporting setup for Firebase Analytics, Mixpanel, and Sentry.
Invocation:
  forge run --blueprint app-analytics-architect --input event_list.yaml
Evaluation
Quality gate criteria (min pass: 70/100):
- Event schema completeness: every event has name, properties, type classification
- Funnel logic: step ordering, fallback paths, timeout windows defined
- Retention: cohort period, metric, lookback window
- Crash: symbolication config, breadcrumb capture, user context
- Privacy: consent gate placement, data retention policy, PII scrub filter
Scoring history:
  v3.0.1  score=57.0  PATCH: minor regression
  v3.0.0  score=89.6  MAJOR: quality gate passed
  v2.0.0  score=91.2  MAJOR: quality gate passed
Production readiness
Version alignment:
  BLUEPRINT.md v3  config.yaml v3.0.1  persona.md v3
Pre-deploy checklist:
  1. Run eval suite: forge eval --blueprint app-analytics-architect
  2. Confirm score >= 70
  3. Verify all REQUIRED markers in config.yaml are replaced
  4. Run syntax validation on generated Firebase configs
  5. Validate event names against platform character limits (Firebase: 40 chars, Mixpanel: no limit)
Real integration configs
WARNING: The values below are valid defaults for local/staging.
REQUIRED: Replace every marked field with production values before deployment.
Sentry:
  dsn: https://examplePublicKey@o0.ingest.sentry.io/0  # REQUIRED: replace before deploy
  environment: production                                # REQUIRED: set to 'production' in CI
  traces_sample_rate: 1.0                                # REQUIRED: reduce to 0.2 for production
  profiles_sample_rate: 0.5                              # REQUIRED: reduce to 0.1 for production
Mixpanel:
  token: YOUR_PROJECT_TOKEN                              # REQUIRED: replace before deploy
  api_host: https://api.mixpanel.com                      # Override if using EU data residency -> https://api-eu.mixpanel.com
  disable_geoip: false                                    # REQUIRED: switch to true for GDPR compliance
  test_token: YOUR_TEST_TOKEN                             # REQUIRED: replace before deploy (used in dev/staging)
Firebase:
  project_id: your-firebase-project-id                    # REQUIRED: replace before deploy
  app_id: 1:123456789:android:abc123def456                # REQUIRED: replace before deploy
  ga_tracking_id: UA-XXXXX-Y                              # REQUIRED: replace with GA4 measurement ID (G-XXXXXXXX)
  crashlytics:
    enabled: true
    symbol_upload_auth_token: YOUR_AUTH_TOKEN              # REQUIRED: replace before deploy
PostHog:
  api_key: phc_YOUR_POSTHOG_KEY                           # REQUIRED: replace before deploy
  host: https://app.posthog.com                           # Override for self-hosted deployments
  capture_uncaught_errors: true
Amplitude:
  api_key: YOUR_AMPLITUDE_KEY                             # REQUIRED: replace before deploy
  secret_key: YOUR_AMPLITUDE_SECRET                       # REQUIRED: replace before deploy
  server_zone: US                                         # REQUIRED: switch to EU for GDPR
Data pipeline endpoints:
  kafka_broker: localhost:9092                            # REQUIRED: replace with production broker
  s3_bucket: your-analytics-bucket                        # REQUIRED: replace before deploy
  redshift_host: your-cluster.redshift.amazonaws.com      # REQUIRED: replace before deploy
  bigquery_dataset: your_project.analytics_events         # REQUIRED: replace before deploy
---
File: persona.md
You are Mobile analytics specialist. Expert in Firebase Analytics, Mixpanel, Sentry, and data pipelines.
Delivery rule: ALL output files SHALL be written to disk — never delivered as response text. If the user asks for file output, use writefile, not a chat message.
Tone and style:
- Use precise technical language. No marketing fluff.
- When recommending an event name, include the exact platform convention (snake_case for Firebase, camelCase for Mixpanel).
- Always pair a recommendation with a rationale. Never say "just do X" — say "use screen_view instead of page_view because Firebase auto-collects screen_view with screen_class and screen_instance parameters, giving you free breakdowns by screen class."
- When diagnosing a crash, lead with the stack trace line, not the summary.
Error-recovery heuristics:
1. Missing API keys at generation time
   If the target platform API key is absent from config, skip the integration block entirely and output a WARNING comment at the top of the generated file listing exactly which integrations were omitted and why.
   DO NOT generate placeholder code that will fail at runtime.
   DO NOT abort the full generation — proceed with available integrations.
2. Schema conflict between platforms
   If an event property name exceeds Firebase's 40-character limit but works in Mixpanel, generate a PlatformEventMap section that documents the mapping.
   If types conflict (e.g. string vs int for the same property), emit a CONFLICT comment at the definition site with both types and a recommended resolution.
3. Rate limit indication
   If the generated output would exceed 500 distinct event names, split into a core taxonomy (first 500) and an extended taxonomy appendix.
   Log a WARNING at the top: "Extended taxonomy has 47 events that exceed the 500-event limit. These are appended as optional — deploy only if needed."
4. Consent framework missing
   If no consent management platform (CMP) is specified in the input, insert a CONSENT_GATE block before every event that has a privacy impact classification of PII or SENSITIVE.
   Each CONSENT_GATE block must include: the required consent category (analytics, marketing, personalization), the fallback behavior when denied, and a reference anchor for the CMP integration.
Decision trees for common forks:
  Question: Should I use an auto-tracked event or a custom event?
  Condition: Does the user need a property that Firebase/Mixpanel does not auto-capture?
  |-- YES -> custom event. Prefix with 'custom_' for Firebase, omit prefix for Mixpanel.
  |-- NO  -> use auto-tracked event (e.g. screen_view, session_start).
  Exit: Document the choice in the taxonomy with a comment: // auto-tracked: screen_view or // custom: custom_profile_complete.
  Question: Should I track in Firebase, Mixpanel, or both?
  Condition: Is the metric a North Star (retention, revenue, engagement)?
  |-- YES -> both platforms. Firebase for realtime + crash correlation, Mixpanel for behavioral analysis.
  |-- NO  -> Firebase only (lower cost, simpler pipelines).
  Exit: Generate dual-platform output with // COMPAT comment on diverging property names.
  Question: How to classify an event for privacy?
  Condition: Does the property contain user-identifiable data (email, device ID, exact location)?
  |-- YES -> classification = SENSITIVE. Apply hashing before sending. Inline: // SENSITIVE: hashed with SHA-256(client_salt)
  |-- NO but contains coarse location (city, region) -> classification = PII.
  |-- NO  -> classification = ANONYMOUS.
  Exit: Emit a classification metadata block above the event definition.
Worked example: User wants to track "user started free trial" in a fitness app.
1. Event name: free_trial_started (Firebase), freeTrialStarted (Mixpanel)
2. Properties:
   - trial_duration_days (int, required, range 3-30)
   - source_channel (string, required, enum: email_push_invite_organic)
   - has_credit_card (bool, optional, default false)
   - app_version (string, auto-captured by both platforms)
3. Funnel placement: step 1 of "Free trial -> Active use -> Subscription purchase"
4. Privacy: has_credit_card is SENSITIVE. Replace with has_payment_method (bool, anonymous). Source channel may contain UTM params that encode user IDs in some campaigns — flag for manual review.
5. Output: Write to disk as events/free_trial_started.yaml with full schema definition.
---
File: BLUEPRINT.md
# App Analytics Architect
Domain: app-dev  Version: 3
Purpose
Architects mobile analytics infrastructure. Designs event taxonomies, conversion funnels, retention cohort queries, crash reporting pipelines, and consent-first privacy frameworks across Firebase Analytics, Mixpanel, and Sentry.
Persona
Mobile analytics specialist with expertise in Firebase Analytics, Mixpanel, Sentry, Crashlytics, and data pipeline orchestration.
Skills
  Event: design event taxonomy for mobile across multiple platforms
  Funnel: build conversion funnels with step timing and fallback paths
  Retention: track cohort retention metrics with configurable lookback windows
  Crash: integrate Sentry and Firebase Crashlytics with symbolication and breadcrumb context
  Privacy: implement consent-first analytics with CMP gate placement and PII scrubbing
Events Reference
Event definitions must include: name, description, schema, classification, and example payload.
Standard events (auto-captured by Firebase / Mixpanel):
  Event: session_start
  Description: User opens app and a new session begins. Fired automatically by SDK.
  Platform: Firebase (auto), Mixpanel (auto)
  Properties:
    - session_id (string, required, range: UUID v4 format)
    - device_category (string, auto, enum: mobile_tablet_desktop)
    - app_version (string, auto)
    - previous_session_timestamp (int, optional, Unix ms, range: >0)
  Classification: ANONYMOUS
  Example:
    event: session_start
    properties:
      session_id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
      device_category: mobile
      app_version: 3.4.1
      previous_session_timestamp: 1719523200000
  Event: screen_view
  Description: User views a screen. Firebase auto-captures with screen_class and screen_instance.
  Platform: Firebase (auto), Mixpanel (auto)
  Properties:
    - screen_class (string, required, max 40 chars, Firebase only)
    - screen_name (string, optional, max 40 chars)
    - screen_instance (string, auto, Firebase only)
    - previous_screen_class (string, optional)
  Classification: ANONYMOUS
  Example:
    event: screen_view
    properties:
      screen_class: OnboardingWelcomeScreen
      screen_name: welcome
      screen_instance: 3
      previous_screen_class: SplashScreen
  Event: app_remove
  Description: User uninstalls the app. Fired via silent push notification pingback.
  Platform: Firebase (via app_indexing), Mixpanel (via push_campaign)
  Properties:
    - last_session_timestamp (int, required, Unix ms)
    - lifetime_days (int, auto, range: 0-3650)
    - campaign_id (string, optional, max 40 chars)
  Classification: ANONYMOUS
  Example:
    event: app_remove
    properties:
      last_session_timestamp: 1719523200000
      lifetime_days: 187
      campaign_id: summer_2026_retargeting
Custom events (user-defined, follow naming conventions below):
  Event: custom_trial_started
  Description: User initiates a free trial of a premium feature.
  Platform: Firebase (custom), Mixpanel (custom)
  Properties:
    - trial_duration_days (int, required, range: 3-30)
    - source_channel (string, required, enum: email_push_invite_organic_social_ad)
    - has_payment_method (bool, optional, default: false)
    - trial_tier (string, optional, enum: basic_premium_enterprise, default: basic)
  Classification: PII (source_channel may encode user identifiers)
  Example:
    event: custom_trial_started
    properties:
      trial_duration_days: 14
      source_channel: email
      has_payment_method: true
      trial_tier: premium
  Event: custom_checkout_started
  Description: User enters checkout flow with at least one item in cart.
  Platform: Firebase (custom), Mixpanel (custom)
  Properties:
    - cart_total_cents (int, required, range: 0-999999)
    - currency (string, required, enum: ISO 4217, max 3 chars)
    - item_count (int, required, range: 1-100)
    - promo_code (string, optional, max 20 chars)
    - is_guest_checkout (bool, optional, default: true)
  Classification: ANONYMOUS
  Example:
    event: custom_checkout_started
    properties:
      cart_total_cents: 2999
      currency: USD
      item_count: 2
      promo_code: SUMMER20
      is_guest_checkout: false
  Event: custom_payment_failed
  Description: Payment processing returned an error code.
  Platform: Firebase (custom), Mixpanel (custom)
  Properties:
    - error_code (string, required, enum: insufficient_funds_expired_card_declined_processing_error_3ds_required)
    - payment_provider (string, required, enum: stripe_braintree_apple_pay_google_pay)
    - amount_cents (int, required, range: 1-999999)
    - retry_count (int, optional, range: 0-5, default: 0)
  Classification: SENSITIVE (amount_cents + payment_provider correlation can identify user)
  Example:
    event: custom_payment_failed
    properties:
      error_code: insufficient_funds
      payment_provider: stripe
      amount_cents: 2999
      retry_count: 1
  Event: custom_subscription_cancelled
  Description: User cancels an active subscription.
  Platform: Firebase (custom), Mixpanel (custom)
  Properties:
    - subscription_tier (string, required, enum: monthly_yearly_lifetime)
    - months_active (int, required, range: 0-120)
    - reason (string, optional, enum: too_expensive_not_used_bugs_switching_other)
    - is_voluntary (bool, required, default: true)
  Classification: PII
  Example:
    event: custom_subscription_cancelled
    properties:
      subscription_tier: monthly
      months_active: 14
      reason: too_expensive
      is_voluntary: true
Naming conventions:
  Firebase: snake_case, max 40 chars, no spaces, no leading digits. Prefix custom events with custom_.
  Mixpanel: camelCase, no length limit, no prefix requirement.
  When dual-platform: Firebase name is primary, Mixpanel name is derived via automated name_transform function.
Platform-specific notes:
  Firebase limits: 500 distinct event types per app, 256 properties per event, property names max 40 chars, property values max 1024 chars (strings).
  Mixpanel limits: no hard event limit, 1000 properties per event, property names max 200 chars, property values max 65535 chars (strings).
  Sentry breadcrumbs: max 100 breadcrumbs per event, each breadcrumb message max 1024 chars.
  Event classification uses three tiers: ANONYMOUS (no user-identifiable data), PII (may contain identifiable data — hash before sending), SENSITIVE (definitely identifiable — require explicit consent and hashing).
---
File: config.yaml
agent:
  max_iterations: 10
  retry_on_failure: true
  timeout_seconds: 300
  toolsets:
  - terminal
  - file
  - web
blueprint:
  dependencies: []
  domain: app-dev
  last_reviewed: '2026-06-26'
  name: app-analytics-architect
  version: 3.0.1
  version_history:
  - from: 1.0.0
    to: 2.0.0
    reason: 'MAJOR: quality gate passed (score=91.2)'
    score: 91.2
    previous_score: null
    timestamp: '2026-06-26T00:46:01Z'
  - from: 2.0.0
    to: 3.0.0
    reason: 'MAJOR: quality gate passed (score=89.6)'
    score: 89.6
    previous_score: 91.2
    timestamp: '2026-06-26T00:46:26Z'
  - from: 3.0.0
    to: 3.0.1
    reason: 'PATCH: minor change (score=57.0, delta=-32.6)'
    score: 57.0
    previous_score: 89.6
    timestamp: '2026-06-26T06:56:28Z'
eval:
  benchmarks: []
  judge_model: deepseek-v4-pro
  min_pass_score: 70
hardware_profiles:
  pontus-main:
    eval_model: deepseek-v4-pro
    max_tokens: 8192
    model: deepseek-v4-flash
    provider: deepseek
    temperature: 0.3
# Integration-specific overrides
# REQUIRED: Override every value below per deployment environment.
# Copy this section, rename the key for each environment (staging, production),
# and fill in the real values.
integrations:
  sentry:
    dsn: https://examplePublicKey@o0.ingest.sentry.io/0
    # REQUIRED: replace before deploying to production
    environment: production
    # REQUIRED: set to 'production' in CI pipeline
    traces_sample_rate: 1.0
    # REQUIRED: reduce to 0.2 for production to manage quota
    profiles_sample_rate: 0.5
    # REQUIRED: reduce to 0.1 for production
    release: app-analytics-architect@3.0.1
  mixpanel:
    token: YOUR_PROJECT_TOKEN
    # REQUIRED: replace with actual Mixpanel project token before deploy
    api_host: https://api.mixpanel.com
    # Override to https://api-eu.mixpanel.com for EU data residency
    disable_geoip: false
    # REQUIRED: switch to true for GDPR compliance in EU deployments
    test_token: YOUR_TEST_TOKEN
    # REQUIRED: replace with Mixpanel test project token for dev/staging
  firebase:
    project_id: your-firebase-project-id
    # REQUIRED: replace with actual Firebase project ID before deploy
    app_id: 1:123456789:android:abc123def456
    # REQUIRED: replace with actual Firebase app ID
    ga_tracking_id: UA-XXXXX-Y
    # REQUIRED: replace with actual GA4 measurement ID (format: G-XXXXXXXX)
    crashlytics:
      enabled: true
      symbol_upload_auth_token: YOUR_AUTH_TOKEN
      # REQUIRED: replace with Crashlytics symbol upload token before deploy
  posthog:
    api_key: phc_YOUR_POSTHOG_KEY
    # REQUIRED: replace with PostHog project API key before deploy
    host: https://app.posthog.com
    # Override to self-hosted URL if applicable
    capture_uncaught_errors: true
  amplitude:
    api_key: YOUR_AMPLITUDE_KEY
    # REQUIRED: replace with Amplitude API key before deploy
    secret_key: YOUR_AMPLITUDE_SECRET
    # REQUIRED: replace with Amplitude secret key before deploy
    server_zone: US
    # REQUIRED: switch to EU deployments for GDPR compliance
  pipeline:
    kafka_broker: localhost:9092
    # REQUIRED: replace with production Kafka broker address
    s3_bucket: your-analytics-bucket
    # REQUIRED: replace with your analytics S3 bucket name
    redshift_host: your-cluster.redshift.amazonaws.com
    # REQUIRED: replace with Redshift cluster endpoint
    bigquery_dataset: your_project.analytics_events
    # REQUIRED: replace with BigQuery dataset ID (format: project_id.dataset_name)