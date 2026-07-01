BLUEPRINT.md
Dashboard Report Factory
Domain: dashboard Version: 2
Purpose
Export and report generation engine for dashboards. Export current dashboard view as PDF preserving layout and chart fidelity. PNG screenshot via html2canvas with device-pixel-ratio awareness. HTML snapshot full interactive standalone with embedded data. CSV dump all visible data tables with headers and timestamps. Scheduled auto-reports configurable via cron with email delivery. Branded report templates with custom header logo colors and footer. Compare mode baseline versus current with delta annotations. Auto-generated narrative summary prepended to all reports.
Persona
Report generation specialist and export format engineer. Expert in HTML-to-PDF conversion, print CSS, chart rasterization, and building scheduled report delivery systems.
Skills
Agent competencies                        Architectural features
---------------------------------------   --------------------------------------------
Render PDF from DOM with print CSS        Export button menu with file picker
Capture PNG screenshot with html2canvas   Schedule config panel with cron builder
Generate standalone HTML snapshot         Brand template editor (header/logo/footer)
Serialize visible data tables to CSV      Narrative summary auto-generator
Configure cron schedule with timezone     Compare mode diff view with delta badges
Apply brand template to all exports       Delivery: email + download + webhook
State Machine Delivery Lifecycle
IDLE -> EXPORTING (on user trigger or schedule fire)
EXPORTING -> READY (on successful render) | EXPORTING -> FAILED (on error)
READY -> DELIVERING (on download/email send action)
DELIVERING -> COMPLETED (on delivery success) | DELIVERING -> FAILED (on delivery error)
COMPLETED -> IDLE (after delivery timeout or user dismissal of notification)
FAILED -> IDLE (on dismiss) | FAILED -> EXPORTING (on retry)
READY -> IDLE (on cancel)
Retry semantics
Up to 4 retry attempts total. Exponential backoff: 2s 4s 8s 16s. Retry applies on EXPORTING->FAILED and DELIVERING->FAILED transitions. After 4th failure transition to FAILED terminal state require manual dismiss to IDLE.
Render Pipeline Decision Tree
Step 1 Rendering backend
  Option A SVG-only in-memory renderer (default)
    Trade-off highest fidelity no disk I/O but larger memory footprint for complex dashboards >50 widgets
  Option B Raster cache with canvas snapshot
    Trade-off lower memory but loses vector sharpness in PDF output
  Decision default Option A. Switch to B when dashboard exceeds 50 widgets or memory budget is under 256MB
Step 2 Execution model
  Option A Synchronous render on main thread (default for single-export)
    Trade-off simple implementation blocks UI during export. Acceptable under 2s render time
  Option B Async worker pool with 4 workers
    Trade-off non-blocking UI but adds complexity with worker lifecycle and transferables
  Decision default Option A. Switch to B when average render time exceeds 2s or user has queue of 3+ scheduled exports
Step 3 Node isolation
  Option A Single-threaded in-process (default)
    Trade-off simplest integration. Risk of chart library crashes taking down the whole export
  Option B Web Worker or child process per export
    Trade-off crash isolation and true parallelism. Adds serialization overhead for transferring render state
  Decision default Option A for development and low-volume deployments. Switch to B when handling 10+ concurrent exports or when chart library errors are detected in production
Export Format Specifications
PDF
  Page size letter or A4 configurable. Print CSS with @page margin 15mm. Chart rasterization at 300 DPI. Colors preserved in CMYK-safe sRGB. Text selectable. File size target under 10MB.
PNG
  Screenshot at device-pixel-ratio 2x (Retina). Full-page capture for scrollable dashboards. Max dimension 8000px wide. Compression level 8. Background always white.
HTML
  Self-contained single file. All data embedded as JSON in script tag. All CSS inlined. All SVGs embedded. No external dependencies. Opens in any modern browser offline. File size warning at 50MB.
CSV
  One file per visible table. Filename dashboard-name_timestamp.csv. UTF-8 BOM. ISO 8601 timestamps. Numbers unformatted machine-readable. Null values empty cell.
Schedule Configuration
cron expression with timezone selector. Supported frequencies: hourly daily weekly monthly. Delivery targets: email SMTP optional attachment list. Retention delete after N days default 30. One-time or recurring. Named presets Monday 9am First-of-month PDF Weekly summary PNG.
Brand Template
Configurable fields header logo URL primary color hex accent color hex footer text. Applied to PDF header and footer. Applied to PNG watermark. Applied to HTML snapshot theme. Inherited from dashboard theme by default.
Compare Mode
Baseline export stored as snapshot. Current export rendered alongside. Delta annotations red green badges for changed values. Side-by-side or overlaid layout. Baseline timestamp always visible.
Edge Cases
Export of empty dashboard emits placeholder PDF with Minimal data available notice
Export timeout after 60s transitions to FAILED with timeout reason in error log
Browser tab hidden during render html2canvas uses requestAnimationFrame may produce blank frames on tab switch fallback to document.body render
Schedule fires while previous export still running queue depth 1 excess dropped logged
Memory pressure during large dashboard export triggers incremental render 10 widgets per batch yield to event loop between batches
File name collisions appends timestamp microseconds to guarantee uniqueness
Unicode in chart labels rendered correctly in all formats tested against CJK and RTL
Dependencies
  html2canvas 1.4.x for PNG capture
  jsPDF 2.5.x for PDF generation
  FileSaver.js for download triggering
  cron-parser for schedule validation
  nodemailer for email delivery server-side
  Print CSS standard no polyfill needed