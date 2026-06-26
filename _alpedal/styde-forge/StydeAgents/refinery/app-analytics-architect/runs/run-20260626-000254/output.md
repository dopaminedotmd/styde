EVENT TAXONOMY — Mobile App Analytics v1
Track 3 event categories:
- user_engagement: app_open, screen_view, feature_interact, session_duration
- conversion: signup_start, signup_complete, add_to_cart, purchase_initiated, purchase_success, purchase_failed
- error: crash_occurred, api_error, network_timeout, permission_denied
Each event carries properties: event_name, timestamp, screen_name, user_id (hashed), device_os, app_version, session_id.
FIRST FUNNEL — Activation to First Purchase
1. app_open (entry)
2. signup_complete (drop-off 1)
3. feature_interact (drop-off 2)
4. add_to_cart (drop-off 3)
5. purchase_success (goal)
Expected baseline conversion: 40% app_open to signup, 25% to first purchase.
COHORT RETENTION — Day-1/7/30
Track: D0 install, D1 return, D7 return, D30 return.
Metric: % of cohort active on each day.
Target: D1 > 40%, D7 > 20%, D30 > 10%.
CRASH — Firebase Crashlytics + Sentry dual pipeline
- Crashlytics: realtime alerts, non-fatals, breadcrumbs
- Sentry: full stack traces, user context, release tracking
- Keys: app_version, os_version, device_model, breadcrumb trail (last 20 actions before crash)
PRIVACY — Consent-first setup
- Block all tracking until user accepts consent via CMP.
- Events queued in memory (max 200), flushed on consent grant.
- On consent deny: fire only anonymous session ping (no user_id, no device_id).
- GDPR compliance: data_retention=13 months, auto-delete opt-out users every 30 days.
- Firebase: enable Analytics, disable Ads Personalization by default.
- Mixpanel: EU data residency, IP anonymization on.