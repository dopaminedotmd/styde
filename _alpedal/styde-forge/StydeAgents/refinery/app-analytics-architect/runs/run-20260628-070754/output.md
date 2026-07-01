MOBILE ANALYTICS ARCHITECTURE — E-COMMERCE APP
EVENT TAXONOMY
event_taxonomy:
  standard:
    app_launch: { params: [source, campaign_id], trigger: on_first_activity }
    app_close: { params: [session_duration_s, foreground], trigger: on_background }
    screen_view: { params: [screen_name, referrer], trigger: LifecycleObserver }
    login: { params: [method, user_id_hash], trigger: AuthSuccess }
    signup: { params: [method, tenant_id], trigger: RegistrationComplete }
  commerce:
    product_view: { params: [sku, category, price], trigger: RecyclerView.onItemVisible }
    add_to_cart: { params: [sku, qty, variant], trigger: CartButton.tap }
    begin_checkout: { params: [cart_total, item_count], trigger: CheckoutStep.enter }
    purchase_complete: { params: [order_id, revenue, currency, items], trigger: PaymentGateway.confirm }
    refund: { params: [order_id, amount, reason], trigger: AdminAction  }
SCHEMA ENFORCEMENT — run at CI + PR merge, reject if unknown param or missing required param
    source_of_truth: events_v2.json in monorepo root
    linter: analytics_lint.py checks all firebase_analytics.logEvent calls
CONVERSION FUNNEL — Onboarding -> Purchase
funnel_steps:
  - step: signup_complete
    expected: 100%
    drop_threshold: 10%
  - step: add_first_product
    expected: 60%
    drop_threshold: 15%
  - step: begin_checkout
    expected: 30%
    drop_threshold: 10%
  - step: purchase_complete
    expected: 20%
    drop_threshold: 8%
  reporting:
    tool: BigQuery + Looker
    refresh: hourly
    alert_on_drop: >20% week-over-week in any step
RETENTION COHORTS
cohort_definition:
  granularity: daily
  window: D7 D14 D30
  metric: day_active (any tracked event within calendar day)
  query: BigQuery cohort_table auto-generated from app_launch event
  dashboard: Looker tile showing W-shaped retention curve by install_week
CRASH REPORTING — Sentry + Firebase Crashlytics
crash_pipeline:
  capture: UncaughtExceptionHandler + ANR watchdog
  transport: Sentry SDK 7.x — breadcrumbs buffer 100 events before send
  grouping: fingerprint by stack_frame[0].function + exception_type
  severity: fatal | non_fatal | ANR
  alerts: Slack webhook on fatal rate > 0.5% per version per hour
  source_map: auto-upload on release build — dsyms to Sentry via fastlane
PRIVACY — GDPR / CCPA consent-first
consent_flow:
  step1: gdpr_dialog on first launch — reject_button, accept_all, customize
  step2: if reject, fire only app_launch with event_policy=minimal
  step3: if customize, toggle per event_category (commerce, crash, analytics)
  enforcement:
    - FirebaseAnalytics.setConsent before any logEvent
    - Mixpanel.optOutTracking(true) on reject until consent granted
    - Sentry.setUser(nil) on reject
  data_retention:
    user_deletion: API endpoint triggers BigQuery DELETE on user_id_hash within 48h
    event_ttl: 13 months, enforced by BigQuery table partition expiration
IMPLEMENTATION ORDER — execute immediately
1. add analytics_lint.py to CI pipeline PR gate
2. add Firebase + Sentry init to Application.onCreate
3. wire GDPR consent dialog as splash screen
4. log screen_view from all fragments via base class
5. BigQuery view: create funnel_weekly, cohort_daily
6. Looker dashboard: funnel + retention + crash_rate + consent_rate