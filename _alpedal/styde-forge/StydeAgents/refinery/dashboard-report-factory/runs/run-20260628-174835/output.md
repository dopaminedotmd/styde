BLUEPRINT.md
Dashboard Report Factory
Domain: dashboard
Version: 1
Purpose: Export and report generation engine for dashboards. Export current dashboard view as PDF (preserving layout), PNG (screenshot), HTML snapshot (interactive standalone), or CSV data dump. Scheduled auto-reports: Send me a PDF of this dashboard every Monday at 9am. Branded report templates with custom header/logo/footer. Auto-generated narrative summary prepended to reports. Compare mode: export baseline vs current with delta annotations.
PERSONA
Report generation specialist and export format engineer. Expert in HTML-to-PDF conversion, print CSS, chart rasterization, and building scheduled report delivery systems.
SKILLS
  PDF: render current dashboard to PDF with preserved layout, colors, and chart fidelity
  PNG: capture dashboard screenshot via html2canvas with device-pixel-ratio awareness
  HTML: export full interactive standalone HTML snapshot with embedded data
  CSV: dump all visible data tables as downloadable CSV with headers and timestamps
  Schedule: configurable cron-based auto-export with email delivery (PDF/PNG/HTML)
  Brand: apply custom header, logo, colors, and footer to all exports and reports
  Output: interactive HTML dashboard with export button menu, schedule config, and preview
ARCHITECTURE
Component-Interaction Diagram
+--------------------+       trigger       +------------------+
| Dashboard UI       | ------------------> | ExportController |
| (React frontend)   | <------------------ | (orchestrator)   |
| - export button    |   status/progress   |                  |
| - schedule config  |                     |                  |
| - preview pane     |                     |                  |
+--------------------+                     +--------+---------+
                                                   |
                    +------------------------------+------------------------------+
                    |                              |                              |
                    v                              v                              v
          +-------------------+          +-------------------+          +-------------------+
          | PDFRenderer       |          | PNGRenderer       |          | HTMLRenderer      |
          | (puppeteer/       |          | (html2canvas      |          | (data embedder    |
          |  wkhtmltopdf)     |          |  puppeteer        |          |  + inline assets) |
          | output: .pdf      |          | output: .png      |          | output: .html     |
          +-------------------+          +-------------------+          +-------------------+
                   |                              |                              |
                   +------------------------------+------------------------------+
                                                  |
                                                  v
                                        +-------------------+
                                        | CSVExporter       |
                                        | (data tables      |
                                        |  query + format)  |
                                        | output: .csv      |
                                        +-------------------+
Lifecycle State Machine (per export job)
IDLE -> PENDING (user clicks export) -> RENDERING (renderer active) -> COMPLETED (file ready)
     -> FAILED (error, retry up to 3x) -> IDLE
     -> CANCELLED (user aborts) -> IDLE
Scheduled delivery:
IDLE -> PENDING (cron fires) -> RENDERING -> COMPLETED -> DELIVERY_QUEUED (email queued)
     -> DELIVERY_SENT (confirmed) -> IDLE
     -> DELIVERY_FAILED (retry up to 3, exponential backoff: 5min, 15min, 1hr) -> IDLE
Data Flow
1. User clicks Export -> ExportController receives format, filters, schedule flag
2. ExportController validates permissions (user has export access on this dashboard)
3. Controller snapshots current viewport state (filters, time range, visible widgets)
4. For PDF/PNG/HTML: controller renders dashboard headless via renderer pool
5. For CSV: controller queries underlying data tables, applies filters, formats rows
6. File written to temp storage with TTL (24h), signed URL generated
7. UI receives download URL, starts progress bar, shows preview if applicable
8. If scheduled: cron entry persisted to schedule store, triggered on next cron tick
9. Delivery service picks up completed file, wraps in brand template, sends via SMTP
10. Delivery receipt logged; on failure, retry queue with backoff
FAILURE MODES & EDGE CASES
Error Handling Per Endpoint
  Export POST /api/export
    400: invalid format (not pdf/png/html/csv), missing dashboard_id, malformed filter JSON
    401: missing or expired auth token
    403: user lacks export permission on this dashboard or org
    409: export already in progress for same dashboard (concurrent limit 1 per user per dashboard)
    413: export payload too large (dashboard has >50 widgets, reduce scope)
    429: rate limit exceeded (max 10 exports per minute per user)
    500: renderer unavailable, storage write failure, unknown error
    502: upstream data source unreachable during CSV export
    504: renderer timeout (dashboard exceeds 30s render window)
  Schedule POST /api/schedule
    400: invalid cron expression, missing format, missing email recipient
    403: user lacks schedule-admin permission
    409: duplicate schedule (identical dashboard+format+cron already exists)
    422: email format invalid, cron interval too short (min 1hr enforced)
    429: max schedules per user exceeded (limit 20)
  Download GET /api/export/{id}/download
    404: job id not found or expired (TTL 24h)
    410: file deleted by admin or storage purge
    500: storage backend unreachable
Loading, Empty, Error States Per Component
  Export Button Menu
    Loading: disabled, spinner, text "Preparing export..."
    Empty: N/A (always has options; if no formats available, show "No export formats configured" message)
    Error: disabled, error icon, text "Export unavailable — contact admin"
  Export Progress Indicator
    Loading: progress bar % animated, estimated time, cancel button
    Empty: N/A (only visible when export active)
    Error: red bar, "Export failed: [reason]", retry button, cancel button
    Upload progress (for CSV large dumps): separate sub-progress bar
  Schedule Config Panel
    Loading: skeleton rows for cron input, format dropdown, email field
    Empty: "No schedules configured. Create your first scheduled report below."
    Error: inline validation errors per field, submission failure toast "Could not save schedule — [reason]"
  Dashboard Preview (in export dialog)
    Loading: full-widget skeleton grid matching dashboard layout
    Empty: "Dashboard has no visible widgets — nothing to export"
    Error: "Preview render failed. The dashboard contains unsupported widget types. Export anyway?"
  CSV Data Preview (CSV export mode)
    Loading: skeleton table with 5 placeholder rows
    Empty: "No data matches the current filters — CSV will contain headers only"
    Error: "Data source query failed — CSV export may be incomplete. Continue?"
    Truncation: "Showing first 100 of 12,450 rows. Full CSV will contain all rows."
  Schedule List
    Loading: skeleton cards (5 rows)
    Empty: "No scheduled reports. Click 'Schedule Report' to create one."
    Error: "Could not load schedules — [reason]. Retry or refresh."
  Email Delivery Status
    Success: green badge "Delivered Mon 12:03"
    Pending: yellow spinner "Queued for delivery"
    Failed: red badge "Delivery failed — will retry in 5 min"
    Permanent failure: red badge with exclamation "Delivery failed after 3 attempts. Manual intervention needed."
Permission Deny Paths
  Viewer role: export button disabled, tooltip "Viewers cannot export. Ask your admin for export access."
  Editor role: can export PDF/PNG/HTML/CSV for dashboards they can view. Cannot schedule.
  Admin role: full access including schedule, brand template config, delete any export.
  Org-scoped deny: dashboard belongs to locked org, export disabled for all. Toast: "Exports are disabled for this organization."
Large Dataset Limits (>10K rows)
  CSV export: max 100,000 rows per export. Above 100K: user prompted "This export will generate ~850K rows and may take several minutes. Continue?"
  PDF/PNG: max 50 widgets. Dashboard with >50 widgets exports as summary report with paginated full-data appendix.
  HTML: all data embedded, max file size 50MB. Above 50MB: truncate data series, link to CSV for full data.
  Pagination tokens: API returns cursor for CSV export of >25K rows. Server streams rows in batches of 5K.
Rate Limiting
  Per user: 10 exports/min, 50 exports/hr, 200 exports/day
  Per org: 100 exports/min
  Schedule executions: max 1/hr per schedule, 10 concurrent deliveries per org
  Burst: up to 5 exports queued per user; beyond queued = 429
  Headers on all responses: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset (epoch)
Scheduled Delivery Failure Fallback with Retry Semantics
  Attempt 1: immediate retry after failure
  Attempt 2: wait 5 minutes, retry
  Attempt 3: wait 15 minutes, retry
  Attempt 4: wait 60 minutes, retry
  After 4 attempts: mark schedule as FAILED, disable it, notify admin via alert channel
  Delivery failure types and retry eligibility:
    SMTP temp failure (5xx transient): retry eligible
    SMTP permanent failure (550 user unknown): NOT retry eligible, mark as PERMANENT_FAILURE
    Attachment size exceeded (>25MB email limit): retry with compressed PDF option, then permanent failure
    Renderer failed (dashboard changed/deleted): retry eligible, then permanent failure
  On success after retry: update delivery log, reset failure count, next delivery scheduled normally
  Notifications: email to schedule creator on permanent failure, webhook to admin channel
TESTING & VERIFICATION PLAN
Unit Test Coverage Targets
  ExportController: >= 90%
  PDFRenderer: >= 85%
  PNGRenderer: >= 85%
  HTMLRenderer: >= 85%
  CSVExporter: >= 90%
  ScheduleManager: >= 90%
  DeliveryService: >= 90%
  BrandTemplateEngine: >= 85%
  Overall project target: >= 85%
Integration Test Requirements
  Each critical path must have at least 1 integration test:
    Export PDF happy path: mock dashboard -> POST export -> poll status -> download -> verify PDF header
    Export CSV >10K rows: mock large dataset -> verify streaming and pagination
    Schedule creation -> cron tick -> delivery queued -> SMTP mock receipt
    Permission deny: export POST as viewer role -> assert 403
    Rate limit: 11 exports in 1 min -> assert 429 on 11th
    Retry delivery failure: 3 consecutive SMTP failures -> assert schedule disabled after 4th attempt
    Brand template: custom header/logo applied to PDF -> assert header string in PDF metadata
    Concurrent export: same user, same dashboard, 2 exports -> assert 409
    Corrupted dashboard: renderer receives invalid widget config -> assert graceful error state
Edge Case to Test Scenario Mapping Table
  Edge Case from Failure Modes Section | Test Scenario File | Type
  Invalid export format | test_export_controller.py::test_invalid_format -> 400 | Unit
  Missing auth token | test_export_controller.py::test_missing_auth -> 401 | Unit
  Insufficient export permission | test_permissions.py::test_viewer_export_403 | Integration
  Duplicate schedule | test_schedule_manager.py::test_duplicate_schedule_409 | Unit
  Dashboard with 0 widgets | test_renderers.py::test_empty_dashboard | Integration
  Dashboard with >50 widgets | test_renderers.py::test_oversized_dashboard_truncation | Integration
  CSV with 0 matching rows | test_csv_exporter.py::test_empty_dataset | Unit
  CSV with >100K rows | test_csv_exporter.py::test_large_dataset_truncation | Integration
  CSV with >25K rows pagination | test_csv_exporter.py::test_cursor_pagination | Unit
  Renderer timeout >30s | test_renderers.py::test_timeout_504 | Integration
  Preview render failure | test_export_controller.py::test_preview_fallback | Integration
  Concurrent export (same user + dashboard) | test_export_controller.py::test_concurrent_export_409 | Integration
  Rate limit exceeded | test_rate_limit.py::test_10_per_min_429 | Integration
  SMTP transient failure (retry eligible) | test_delivery.py::test_smtp_temp_failure_retry | Integration
  SMTP permanent failure (not retry eligible) | test_delivery.py::test_smtp_permanent_failure_disabled | Integration
  Attachment exceeds 25MB | test_delivery.py::test_attachment_size_threshold | Integration
  File expired (TTL 24h) | test_storage.py::test_expired_download_410 | Integration
  Storage backend unreachable | test_storage.py::test_backend_failure_500 | Unit
  Schedule cron interval too short | test_schedule_manager.py::test_min_interval_enforced | Unit
  Max schedules per user exceeded | test_schedule_manager.py::test_schedule_limit_429 | Unit
  Brand header applied to PDF | test_brand_template.py::test_header_embedded | Integration
  Delivery success after 2 retries | test_delivery.py::test_retry_eventually_succeeds | Integration
  Dashboard deleted before delivery | test_delivery.py::test_renderer_failure_permanent | Integration
  Cancel export in progress | test_export_controller.py::test_cancel_during_rendering | Integration
persona.md
Report generation specialist and export format engineer. Expert in HTML-to-PDF conversion, print CSS, chart rasterization, and building scheduled report delivery systems. Before finalizing the blueprint, scan each component for at least 3 states: loading, empty, and error. List them explicitly with UI representation and user-facing message for each state per component. Cover: export button menu, progress indicator, schedule config panel, dashboard preview, CSV data preview, schedule list, and delivery status badge. For loading states, specify skeleton type or spinner variant. For empty states, specify placeholder message. For error states, specify error message text, retry strategy, and fallback behavior. Annotate each permission level (viewer, editor, admin) with its deny-state rendering. Tag each state with its automated test identifier from the test coverage mapping table.