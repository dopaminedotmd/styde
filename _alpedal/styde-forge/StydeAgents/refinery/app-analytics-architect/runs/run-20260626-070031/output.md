Event Taxonomy: Fitness Tracking App v1.0
Event Name: app_launch
Properties: source(icon|notification|deep_link), is_cold_start(bool), app_version(string)
Event Name: user_signup
Properties: method(email|google|apple), referral_source(organic|invite|ad), campaign_id(string|null)
Event Name: workout_started
Properties: workout_type(run|cycle|swim|walk|strength), target_minutes(int), plan_id(string|null), is_guided(bool), start_ts(iso8601)
Event Name: workout_paused
Properties: elapsed_seconds(int), reason(manual|call|notification)
Event Name: workout_resumed
Properties: paused_seconds(int)
Event Name: workout_completed
Properties: elapsed_minutes(float), calories_burned(int), distance_meters(float), avg_heart_rate(int), streak_extended(bool)
Event Name: workout_abandoned
Properties: elapsed_minutes(float), last_milestone_completed(string|null), reason(too_hard|interrupted|error|other)
Event Name: goal_set
Properties: goal_type(daily_distance|weekly_frequency|monthly_duration), target_value(float), unit(km|sessions|minutes)
Event Name: goal_achieved
Properties: goal_type(string), target_value(float), days_to_achieve(int)
Event Name: social_share
Properties: share_type(workout|achievement|leaderboard), platform(whatsapp|instagram|twitter|share_sheet), audience(public|friends|private)
Event Name: subscription_event
Properties: event_type(purchase|renewal|cancellation|expiry), product_id(string), price_usd(float), trial_converted(bool)
Event Name: crash_occurred
Properties: error_class(string), error_message(truncated_128), thread_name(string), os_version(string), device_model(string), app_version(string), memory_mb(int)
Event Name: permission_denied
Properties: permission_type(location|healthkit|notifications|camera), prompt_count(int), permanently_denied(bool)
---
Funnel: Signup-to-First-Workout
Step 1: app_launch (filter: new_user=true)
Step 2: user_signup (method=any)
Step 3: onboarding_complete
Step 4: workout_started (filter: is first workout ever)
Step 5: workout_completed (filter: elapsed_minutes >= 10)
Expected conversion floor: 22% step 1 to step 5 (industry baseline)
---
Retention Cohorts
Day-0 stickiness: users who launch app again within 24h
Week-1 retention: users with >= 2 workouts in calendar week 1
Month-1 retention: users with >= 4 workouts in month 1
Month-3 premium retention: subscription_event(purchase) followed by monthly logins
---
Crash Integration
Sentry project: com.alpedal.fitnessapp
On beforeSend: redact user.email, user.phone from breadcrumbs before crash event is submitted
Breadcrumb auto-capture: network requests, view transitions, user taps
Breadcrumb manual: "data_write_complete" and "data_read_failed" for core model sync
Alert threshold: >0.15% crash-free rate = pager duty notify
---
Privacy Pipeline
Consent gate checks before ALL analytics writes:
if not AnalyticsKit.hasConsent(.tracking):
    drop event entirely (do not send firebase/mixpanel)
    log to local console only
if not AnalyticsKit.hasConsent(.analytics):
    send event stripped of user_id, device_id, ad_id
    keep only session_id, event_name, platform, os_version
if not AnalyticsKit.hasConsent(.crashReporting):
    do NOT attach breadcrumbs to crash reports
    send only raw exception: class, message, memory stats
    strip thread traces containing file paths
GDPR data export endpoint returns all stored events for user_id within 14d, formatted as ndjson.