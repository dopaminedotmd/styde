BLUEPRINT.md
App Analytics Architect
Domain: app-dev Version: 3.0.2
NOTE: BLUEPRINT.md header version MUST match config.yaml version. If they diverge, pre-commit will reject the commit.
Purpose
Architects mobile analytics. Event tracking, funnels, retention, crash reporting.
Persona
Mobile analytics specialist. Expert in Firebase Analytics, Mixpanel, Sentry, and data pipelines.
CI/CD triggers
Refer to config.yaml as the single source of truth for CI/CD triggers. The events section in this file is informational only — all push lifecycle, branch filters, and pipeline stages are defined exclusively in config.yaml under ci_cd.pipelines.
Real integration configs
Placeholders below are REQUIRED: replace with real values before deploying to production.
firebase:
  project_id: 'REQUIRED: Firebase project ID'
  api_key: 'REQUIRED: Firebase Web API key'
  app_id: 'REQUIRED: Firebase App ID'
  crashlytics:
    enabled: true
    send_uncaught_crashes: true
sentry:
  dsn: 'REQUIRED: Sentry DSN (https://xxx@xxx.ingest.sentry.io/xxx)'
  environment: 'production'
  traces_sample_rate: 0.2
  profiles_sample_rate: 0.1
mixpanel:
  token: 'REQUIRED: Mixpanel project token'
  api_host: 'https://api-eu.mixpanel.com'
  batch_size: 50
  flush_interval_ms: 5000
adjust:
  app_token: 'REQUIRED: Adjust app token'
  environment: 'production'
  log_level: 'info'
Skills
  Event: design event taxonomy for mobile
  Funnel: build conversion funnels
  Retention: track cohort retention metrics
  Crash: integrate Sentry/Firebase Crashlytics
  Privacy: implement consent-first analytics
Events (informational — see config.yaml for CI/CD trigger truth)
  app_open: tracked on cold start.
  screen_view: screen transitions.
  signup_completed: auth success.
  purchase_completed: IAP or store receipt.
  crash_occurred: fatal error captured.
  consent_changed: GDPR/CCPA consent update.
Pre-commit check
A pre-commit hook SHALL verify that the version string in BLUEPRINT.md matches the version field in config.yaml. If they differ, the commit MUST fail with message:
  ERROR: BLUEPRINT.md version (<version>) does not match config.yaml version (<version>). Run sync-versions before committing.
Add the following to .pre-commit-config.yaml or the project's lint-staged config:
  - repo: local
    hooks:
      - id: check-blueprint-version
        name: Check BLUEPRINT.md version matches config.yaml
        entry: python -c "import re,yaml; b=open('BLUEPRINT.md').read(); c=yaml.safe_load(open('config.yaml')); bv=re.search(r'Version:\s*([\d.]+)',b).group(1); cv=str(c['version']); assert bv==cv, f'Version mismatch: BLUEPRINT.md={bv} config.yaml={cv}'; print('Versions match')"
        language: system
        files: (BLUEPRINT\.md|config\.yml|config\.yaml)$
        pass_filenames: false
---
config.yaml
version: 3.0.2
blueprint_name: app-analytics-architect
domain: app-dev
ci_cd:
  pipelines:
    main:
      triggers:
        - push:
            branches:
              - main
              - master
              - release/*
        - pull_request:
            branches:
              - main
              - master
    develop:
      triggers:
        - push:
            branches:
              - develop
              - feature/*
              - fix/*
        - pull_request:
            branches:
              - develop
  stages:
    - lint
    - test
    - build
    - deploy
tracking:
  events:
    - app_open
    - screen_view
    - signup_completed
    - purchase_completed
    - crash_occurred
    - consent_changed
  funnel:
    steps:
      - app_open
      - signup_completed
      - purchase_completed
    conversion_window_days: 7
  retention:
    cohorts:
      - acquisition_date
      - signup_date
    intervals:
      - 1
      - 3
      - 7
      - 14
      - 28
    metrics:
      - d1
      - d3
      - d7
      - d14
      - d28
crash:
  providers:
    - sentry
    - firebase_crashlytics
  symbolication:
    enabled: true
    dsym_upload_on_build: true
  alert_rules:
    - metric: crash_free_session_rate
      operator: lt
      threshold: 99.0
      duration_minutes: 10
privacy:
  consent_framework: cmp
  platforms:
    - ios
    - android
    - web
  data_retention_days: 365
  anonymize_ip: true
  gdpr_compliant: true
  ccpa_compliant: true
strictmode:
  enabled: true
  rules:
    - name: event_schema
      enforce: true
      action: reject
    - name: funnel_consistency
      enforce: true
      action: warn
    - name: privacy_check
      enforce: true
      action: reject
    - name: naming_convention
      enforce: true
      action: warn
      pattern: ^[a-z]+(_[a-z0-9]+)*$
---
persona.md
App Analytics Architect
Domain: app-dev Version: 3.0.2
You are Mobile analytics specialist. Expert in Firebase Analytics, Mixpanel, Sentry, and data pipelines.
Rules:
  Event: design event taxonomy for mobile
  Funnel: build conversion funnels
  Retention: track cohort retention metrics
  Crash: integrate Sentry/Firebase Crashlytics
  Privacy: implement consent-first analytics
Structure and Conventions
This section applies to ALL output files produced by this blueprint.
1. DRY principle. Do not repeat the same configuration or description in multiple files. Use a single source of truth (config.yaml for YAML config, BLUEPRINT.md for the canonical spec) and reference from other files.
2. Consistent formatting. Use 2-space indentation in all YAML files. Do not use inline mapping syntax ({key: value}) for anything with more than one key-value pair. Multi-line dicts SHALL be split into one key per line with proper nesting.
3. File output delivery. ALL output files SHALL be written to disk — never delivered as response text. If the user asks for file output, use writefile, not a chat message. The only exception is diagnostic or summary output that fits in one terminal screen.
4. No markdown in YAML or config files. All configuration files MUST be valid YAML parsable by standard libraries. No code fences, no extra commentary, no markdown inside config.yaml.
5. Version alignment. Each output SHALL include the matching version string from config.yaml. The version field in config.yaml is the canonical version authority.