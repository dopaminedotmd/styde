BLUEPRINT.md
Dashboard Report Factory
Domain: dashboard Version: 2
Purpose
Export and report generation engine for dashboards. Export current dashboard view as PDF (preserved layout), PNG (screenshot), HTML snapshot (interactive standalone), or CSV data dump. Scheduled auto-reports with cron, configurable frequency, and email delivery. Branded report templates with custom header, logo, colors, and footer. Auto-generated narrative summary prepended to reports. Compare mode: export baseline vs current with delta annotations, using concrete diff storage and narrative generation.
Skills
Agent competencies:
  PDF rendering: headless Chromium via puppeteer, preserves layout and chart fidelity, page-break-aware print CSS
  PNG capture: html2canvas with device-pixel-ratio awareness, clips viewport to chart area
  HTML export: inline all JS/CSS/data as single self-contained file, reproduce dashboard state at export moment
  CSV dump: extract visible table data, emit headers + timestamped rows, escape commas and quotes
  Narrative generation: LLM-summarize key deltas (trend direction, top-3 movers, anomaly flags), fallback to templated sentence if LLM unavailable
Architectural features:
  Schedule engine: cron expression parser with timezone support, configurable via UI modal
  Email delivery: SMTP or SendGrid transport, attach exported file, plain-text fallback when HTML rejected
  Brand template: header/footer/logo injected via print CSS @page margin boxes, color palette from dashboard theme
  Compare mode: store baseline snapshot as JSON blob (chart-point arrays, table rows, timestamps), diff on export via array subtraction and statistical z-score comparison, annotated as green/red/neutral labels
  Preview window: render export result in an iframe before download
Render pipeline decision tree
1. Output format
   - PDF: headless Chrome print-to-PDF via puppeteer. Recommended default. Consumes ~150 MB memory per render. Falls back to html2canvas + jsPDF when puppeteer unavailable (lower fidelity).
   - PNG: html2canvas with DPR scaling. Faster than PDF (~50 ms), no text selection.
   - HTML: inline all assets. Zero runtime cost, full interactivity in output.
   - CSV: synchronous data extraction from in-memory store. Instantaneous regardless of dataset size.
2. Render concurrency
   - Synchronous: block UI until export completes. Use for CSV and small PNG only. Avoid for PDF.
   - Async worker pool: offload to Web Worker or child process (pool size=2). Recommended default for PDF and large PNG. Backpressure at pool saturation — queue renders.
3. Node isolation
   - Single-threaded: serial render on main thread. Acceptable for CSV, risky for PDF/HTML.
   - Web Worker: isolate per export type in separate thread. Recommended default for PNG/HTML. No DOM access, pass serialized chart config instead of live DOM reference.
   - Dedicated browser context: puppeteer incognito context per render. Recommended default for PDF. Isolates cookies and auth tokens.
Compare-mode storage
Data structure per snapshot:
  type Snapshot = {
    id: string
    timestamp: string (ISO 8601)
    charts: Record<chartId, {
      datapoints: { label: string; value: number }[]
      derivedStats: { mean: number; stddev: number; min: number; max: number }
    }>
    tables: Record<tableId, {
      headers: string[]
      rows: string[][]
    }>
    kpis: Record<kpiId, { value: number; label: string }>
  }
Diff algorithm:
  1. Align two snapshots by chartId/tableId/kpiId key
  2. For each aligned metric, compute delta = current - baseline
  3. Normalize delta: z = delta / baseline.stddev  (or delta / baseline.mean if stddev=0)
  4. Classify: |z| < 0.5 -> neutral (gray), |z| >= 0.5 -> notable, |z| >= 2.0 -> significant (red/green)
  5. Table rows: cell-level diff with Levenshtein distance; highlight changed cells
Fallback: if only one snapshot exists, produce non-compare export without annotations. Log warning, no error.
Narrative generation logic
Pipeline:
  1. Collect all classified deltas with |z| >= 0.5
  2. Sort by absolute z-score descending
  3. Top-3 movers -> noun phrase for each: "{metric} {direction} {delta%}"  e.g. "Revenue down 12.4%"
  4. If LLM available: pass structured diff JSON + top-3 list to LLM prompt, request 2-3 sentence summary. Temperature=0.3, max_tokens=150.
  5. If LLM unavailable: concatenate top-3 mover phrases into a single sentence. "Revenue down 12.4%. Active users up 8.1%. Bounce rate up 3.2pp."
  6. Prepend narrative to report: positioned between title block and first chart/table.
CMYK-safe sRGB color space handling
Remove the qualifier. sRGB is RGB-only and cannot represent CMYK gamut. Export color pipeline treats all chart colors as sRGB hex. If a future requirement demands CMYK-aware output, introduce a separate color-profile option that converts sRGB to FOGRA39 (ISO 12647-2) via color-math library (e.g. colorcet or d3-color with icc profile). No CMYK claim on sRGB pipeline.
Edge cases
  Dashboard empty: export empty PDF with notice "No data" centered on page. PNG returns 1x1 transparent pixel. CSV returns headers only. HTML returns skeleton.
  Large data (>10K rows): CSV streaming mode (chunked write). PDF paginates at 50 rows per page. PNG samples down by showing summary table. HTML truncates to 1000 rows with "Show all" toggle.
  Auth token expired: prompt re-auth before render, do not attempt export with stale token.
  Export in progress: disable export button, show progress bar. Queue duplicate request for after completion.
  Scheduled report fails: retry 3 times with 5-minute backoff. On final failure, send error alert to configured email.
  Brand assets missing (logo not found): fall back to text-only header. Log warning, do not abort.
persona.md
You are Report generation specialist and export format engineer. Expert in HTML-to-PDF conversion, print CSS, chart rasterization, and building scheduled report delivery systems.
Rules:
  PDF: render current dashboard to PDF with preserved layout, colors, and chart fidelity
  PNG: capture dashboard screenshot via html2canvas with device-pixel-ratio awareness
  HTML: export full interactive standalone HTML snapshot with embedded data
  CSV: dump all visible data tables as downloadable CSV with headers and timestamps
  Schedule: configurable cron-based auto-export with email delivery (PDF/PNG/HTML)
  Brand: apply custom header, logo, colors, and footer to all exports and reports
  Output: interactive HTML dashboard with export button menu, schedule config, and preview
  Precision: prefer explicit specification over hand-waving. When a section is underspecified, fill the gap with concrete algorithms, data structures, and fallback behavior rather than glossing over it. Default values and error paths are part of the design, not optional additions.