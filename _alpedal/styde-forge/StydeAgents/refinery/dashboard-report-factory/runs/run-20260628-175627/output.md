Blueprint: Dashboard Report Factory
Version: 2
Domain: dashboard
Purpose
Export and report generation engine for dashboards. Export current dashboard view as PDF (preserving layout), PNG (screenshot), HTML snapshot (interactive standalone), or CSV data dump. Scheduled auto-reports with email delivery. Branded report templates with custom header/logo/footer. Auto-generated narrative summary prepended to reports. Compare mode: export baseline vs current with delta annotations.
Persona
Report generation specialist and export format engineer. Expert in HTML-to-PDF conversion, print CSS, chart rasterization, and building scheduled report delivery systems.
Skills
  PDF: render current dashboard to PDF with preserved layout, colors, and chart fidelity
  PNG: capture dashboard screenshot via html2canvas with device-pixel-ratio awareness
  HTML: export full interactive standalone HTML snapshot with embedded data
  CSV: dump all visible data tables as downloadable CSV with headers and timestamps
  Schedule: configurable cron-based auto-export with email delivery (PDF/PNG/HTML)
  Brand: apply custom header, logo, colors, and footer to all exports and reports
  Output: interactive HTML dashboard with export button menu, schedule config, and preview
Architecture (structural)
mermaid
graph TD
    subgraph Frontend
        DB[Dashboard UI]
        EB[Export Button Menu]
        SB[Schedule Config Panel]
        PB[Brand Settings Panel]
    end
    subgraph Export Engine
        PDF_R[PDF Renderer - puppeteer + print CSS]
        PNG_R[PNG Capturer - html2canvas, DPR 2x]
        HTML_R[HTML Snapshot Builder - inline data + Chart.js]
        CSV_R[CSV Dumper - column headers + timestamped rows]
    end
    subgraph Report Pipeline
        RP[Report Builder - merge header/footer/narrative]
        RN[Narrative Generator - chart summary + trend text]
        CD[Compare Diff Engine - baseline vs current, delta annotations]
    end
    subgraph Scheduler
        CR[Cron Runner - node-cron, configurable]
        Q[Export Queue - FIFO, max 10 pending]
        EM[Email Dispatcher - SMTP, attachment MIME]
    end
    DB -->|select format| EB
    EB -->|format + data| PDF_R
    EB -->|format + data| PNG_R
    EB -->|format + data| HTML_R
    EB -->|format + data| CSV_R
    PDF_R --> RP
    PNG_R --> RP
    HTML_R --> RP
    CSV_R --> RP
    RP -->|assembled report| DB
    SB -->|schedule + format + recipients| CR
    CR -->|trigger export| Q
    Q -->|dequeue| PDF_R
    Q -->|dequeue| PNG_R
    Q -->|dequeue| HTML_R
    Q -->|dequeue| CSV_R
    RP -->|final report| EM
    PB -->|brand config| RP
    CD -->|delta overlay| RP
    RN -->|summary text| RP
end
Data flow
  Dashboard data moves from DB to Export Engine through format-specific renderers.
  Each renderer returns raw export bytes to Report Builder.
  Report Builder applies brand config (header, logo, footer, colors) and prepends narrative.
  Compare mode: baseline snapshot stored in memory, diff computed at render time, delta annotations rendered as red/green overlays on charts and tables.
  Finished report bytes delivered to download handler (interactive) or Email Dispatcher (scheduled).
Lifecycle state machine
  IDLE -> EXPORT_REQUESTED: user clicks export button or cron triggers
  EXPORT_REQUESTED -> RENDERING: format renderer started
  RENDERING -> BUILDING: raw export bytes returned to Report Builder
  BUILDING -> NARRATING: brand and narrative applied (unless skipped)
  NARRATING -> DELIVERING: final bytes sent to download or email queue
  DELIVERING -> COMPLETED: delivery acknowledged or file saved
  COMPLETED -> IDLE: after delivery timeout (30s) or user dismissal of download dialog
  Any state -> IDLE: on unrecoverable error or user abort
Testing and Verification Plan
  Unit test coverage targets: >= 80% across all modules
  Integration tests:
    PDF: render 3-series chart dashboard, verify page count >= 1 and no crash
    PNG: capture at DPR 2x, verify image dimensions >= canvas * 2
    HTML: export with embedded data, re-import and verify chart renders same values
    CSV: dump 50-row table, verify row count == 50 and headers match columns
    Schedule: cron fires at correct hour, triggers export, email sent with attachment
    Brand: custom logo replaces default, footer text present in PDF
    Narrative: generated summary contains at least 2 trend references
  Edge case to test scenario mapping
    edge: empty data table
    test: CSV dump of empty table produces only headers, no crash
    edge: chart with zero values
    test: PNG capture renders empty chart without error, axes still labeled
    edge: browser print CSS overflow
    test: PDF render of 30-chart dashboard does not clip last chart
    edge: html2canvas timeout on large DOM
    test: PNG capture on 5000-element dashboard completes within 15s or returns error
    edge: cron schedule with invalid expression
    test: Schedule config rejects * * * * * *  and shows validation error
    edge: SMTP server unreachable
    test: Email Dispatcher returns failure status, does not crash scheduler
    edge: baseline missing in compare mode
    test: Compare mode falls back to current-only export, logs warning
    edge: brand image not found
    test: Report Builder logs missing logo warning, renders without logo
    edge: concurrent export queue overflow
    test: Queue rejects 11th pending job, returns 429 status
    edge: report narrative generation on single data point
    test: Narrative produces 'stable' text instead of trend comparison, no crash