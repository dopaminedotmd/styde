Dashboard Report Factory
Domain: dashboard
Version: 2
Purpose
Export and report generation engine for dashboards. Export current dashboard view as PDF (preserving layout), PNG (screenshot), HTML snapshot (interactive standalone), or CSV data dump. Scheduled auto-reports with cron-based delivery. Branded report templates with custom header/logo/footer. Auto-generated narrative summary prepended to reports. Compare mode: export baseline vs current with delta annotations.
Architecture
- Data model layer: single normalized dataset shared between script and table-render. No data duplication.
- Preview pane: floating detail panel toggled on row click. Renders selected row data without re-fetching.
- Compare mode: toggles only re-render the comparison-specific delta panel, not the full dashboard.
- Formatting: batch all formatCurrency calls into a single Intl.NumberFormat pass. Memoize with WeakMap keyed on raw value plus locale.
Components
  ExportBar
    - Contains: export button menu (PDF/PNG/HTML/CSV), schedule config trigger, preview toggle
    - States: loading, ready, error, disabled (when dashboard has no data)
  PreviewPane
    - Floating detail panel, toggled on row click
    - States: closed, loading (fetching row detail), populated, error (failed to load detail), empty (row has no detail data)
  ReportBuilder
    - Assembles branded report: header, narrative summary, exported dashboard content, footer
    - States: idle, building, ready, error (template render failure)
  SchedulerConfig
    - Cron expression builder with visual preset pickers (every Monday 9am, Daily at 8am, etc)
    - Delivery destinations: email, slack, webhook
    - States: idle, saving, scheduled, error (invalid cron, delivery failed), rate-limited
  NarrativeSummary
    - AI-generated prose summary of dashboard insights
    - States: generating, complete, empty (no insights to summarize), error (LLM call failed)
Failure Modes and Edge Cases
  Endpoint errors
  - Export API returns 4xx/5xx: surface toast with retry button, fall back to last-known-good export
  - html2canvas failure (CORS, canvas taint): fall back to server-side PDF render
  - CSV export on empty dataset: emit file with headers only, no rows
  Large datasets
  - Table >10,000 rows: paginate server-side, show row count warning on export
  - PDF render with >50 pages: paginate into chaptered PDF or warn user
  - CSV export unlimited but warn at 100K rows for browser memory
  Permission paths
  - User lacks export permission: hide export buttons entirely, show locked icon with tooltip
  - User lacks schedule permission: show schedule config as read-only, allow viewing existing schedules only
  - User lacks view-detail permission: preview pane shows redacted placeholder, logs audit event
  Loading and empty states
  - Every table: skeleton rows (6 shimmer lines), empty state illustration with call-to-action
  - Every chart: skeleton circle/bar placeholders, empty state "no data for this period"
  - Dashboard as a whole: full-page skeleton, then empty state if all components empty
  Rate limiting
  - Export API: 5 requests per minute per user. On limit breach: show cooldown timer, disable button
  - Schedule API: 20 schedules per user max. Warn at 15.
  Delivery failure
  - Email delivery fail: retry 3 times with exponential backoff (30s, 2min, 5min), then surface alert
  - Webhook delivery fail: same retry, log to delivery audit trail
  - Fallback delivery: if primary channel fails after retries, attempt secondary channel (e.g. Slack then email)
  Security
  - Export data must respect row-level security filters applied in dashboard
  - Schedule tokens stored encrypted, never exposed in client-side JS
  - PDF/HTML export must not embed raw database identifiers in markup
Testing and Verification Plan
  Unit test coverage target: >=80%
  Integration test for each critical path:
    - ExportBar: click each format button, verify correct export triggers
    - PreviewPane: click row, verify panel opens with correct data; click close, verify panel closes
    - SchedulerConfig: create schedule, verify cron saved; create duplicate, verify error
    - NarrativeSummary: verify generated text appears in final report
  Edge case to test scenario mapping:
    - Empty dataset CSV: headers-only output verified byte-for-byte against fixture
    - 10,001 row pagination: confirm export warns and paginates
    - Export permission denied: confirm ExportBar shows locked state, API returns 403
    - Rate limit exceeded: confirm button disabled, cooldown visible, next request blocked
    - Email delivery retry: mock 3 consecutive SMTP failures, verify alert surface after third
    - Preview pane row detail fetch failure: verify error state renders, retry button works
    - Large PDF >50 pages: verify chaptered output or user warning
Performance and rendering notes
- Compare mode toggles only re-render the comparison-specific delta panel, not the full dashboard
- formatCurrency calls: single Intl.NumberFormat pass across all formatted values in one batch, memoized with WeakMap
- Chart rasterization for PNG export: use OffscreenCanvas in worker thread, avoid blocking main thread
- HTML snapshot: inline critical CSS, defer non-critical, embed data as JSON in script tag (not inline HTML to avoid injection)
Revision history
2026-06-28 v2: added preview pane component, normalized data model layer, compare-mode render isolation, memoization strategy, failure modes and edge cases section, testing and verification plan, performance notes