BLUEPRINT:
Dashboard Report Factory
Domain: dashboard Version: 2
Purpose
Export and report generation engine for dashboards. Export current dashboard view as PDF (preserving layout), PNG (screenshot), HTML snapshot (interactive standalone), or CSV data dump. Scheduled auto-reports: 'Send me a PDF of this dashboard every Monday at 9am'. Branded report templates with custom header/logo/footer. Auto-generated narrative summary prepended to reports. Compare mode: export baseline vs current with delta annotations.
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
  PreviewPane: floating detail panel toggled on row click in any data table
  CompareMode: diff overlay rendered only on a dedicated comparison panel, not full dashboard
  DataModel: single normalized dataset layer shared across script and table-render components
  FormatCurrency: batched via single Intl.NumberFormat instance, not per-cell calls
UI elements
  PreviewPane: absolute-positioned panel slides in from right on row click. Shows row detail, inline chart snapshot, and export-to-csv for that row. Close via X button or click-outside. Panel state managed by a single boolean ref to avoid re-rendering parent dashboard.
  CompareMode toggle: switches a comparison panel (not dashboard body) between baseline and current. Panel holds two side-by-side frames + delta annotation layer. Toggle only swaps the panel's data bindings; dashboard layout and other panels remain mounted.
Architecture
  DataModel layer: fetches raw data once into a shared store (zustand). Script components read from store via selector. Table-render components read from same store via identical selector. Writes (filter, sort, drill-down) mutate store and both consumers re-render from single source. Eliminates duplicate fetch/build paths.
  CompareMode rendering: toggling compare mode never unmounts or re-renders the full dashboard. It sets a compareActive flag in store. A dedicated ComparePanel component watches this flag and renders/clears its two side-by-side views. Other panels are isolated via React.memo and receive no compare-related props.
  formatCurrency optimization: on data load, all numeric values are pre-formatted through a single Intl.NumberFormat('en-US', {style:'currency', currency:'USD'}) instance. Formatted values stored alongside raw values in DataModel. Components read pre-formatted string directly, skipping per-cell formatCurrency calls. Reduces format calls from O(n) to O(1).
State overview
  DataModel state: rawData, formattedData, filters, sortKey, sortDir, selectedRowId, compareActive, compareBaselineId. Single atomic update path.
  PreviewPane state: isOpen, rowId, position. Managed in DataModel store, not local component state, so table and preview always agree on selection.
  ComparePanel state: baselineData, currentData, diffAnnotations. Hydrated from DataModel on flag toggle. Cleared on toggle off to free memory.
Data flow
  API fetch -> DataModel.fetch() -> rawData stored -> formatCurrency batch runs -> formattedData stored -> all consumers react. Row click -> DataModel.selectRow(id) -> tables highlight, PreviewPane opens. Compare toggle -> DataModel.setCompare(true) -> ComparePanel hydrates from rawData -> renders diff. Export/Schedule buttons read from store directly, no second fetch.