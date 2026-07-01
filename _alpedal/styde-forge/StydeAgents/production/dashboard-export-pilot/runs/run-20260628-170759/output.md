```
task: dashboard-export-pilot
domain: frontend
version: 1
status: complete
findings:
  - Export button with submenu (PDF/PNG/HTML) found in top-strip toolbar at lines 509-516
  - @media print CSS (lines 373-426) with page-break-inside:avoid on forge-blocks, white background, grayscale bars, hidden interactive elements (fc-btn, skill-nodes, particle-canvas)
  - html2canvas@1.4.1 loaded via CDN (line 7) for PNG capture of #workshop element at 2x scale with useCORS:true, backgroundColor:#020208
  - HTML export (lines 1142-1151) clones #page-mission, strips fc-btn/fc-input/fc-toggle/skill-nodes, inlines all style tags, produces self-contained static snapshot
  - Footer rendered via .export-footer and .export-sub (display:none by default, display:block in @media print and before PNG/HTML capture) with format: 'StydeForge Mission Control — exported YYYY-MM-DD HH:MM — v3.0'
  - JS handlers at lines 1127-1151: toggleExportMenu(), fmtNow(), exportPDF(), exportPNG(), exportHTML()
edge-cases-and-error-handling:
  async:
    - exportPNG wraps html2canvas in .then/.catch, shows alert('PNG export failed') on error, restores display of footer elements in finally-equivalent pattern
    - exportHTML no error handling on Blob/URL.createObjectURL but these are synchronous and unlikely to fail
  missing-dom:
    - exportPDF references #export-date and #export-ts — these exist at lines 600-601 inside .export-footer and .export-sub
    - exportPNG checks for #workshop existence with guard clause: if(!t) alert('Dashboard not found'); return
    - exportHTML reads all style/link elements — if none exist, ss is empty string, output degrades gracefully
  event-driven:
    - exportPDF uses window.print() which blocks — no afterprint listener registered. This is a known limitation: afterprint is not consistently supported cross-browser
    - toggleExportMenu() has a document click listener (line 1128) to close menu on outside click — proper event delegation pattern
  cross-browser:
    - @media print contains ::before/::after on body and .forge-block — pseudo-elements in print rendering vary across browsers; the body::before/after atmosphere effects are hidden via display:none in print, so this is safe
    - html2canvas does not render CSS ::before/::after pseudo-elements — this is a documented limitation; the export-footer and export-sub are real DOM elements so they render correctly
recommendations:
  - Add window.onafterprint = function(){...} as complement to fixed timeout for cleanup after PDF/print to handle both event-driven and timeout teardown
  - exportHTML should wrap Blob/URL.createObjectURL/link.click in try/catch with fallback to document.write for browsers blocking blob downloads
  - For html2canvas on very tall grids, add a scroll-based capture loop (capture viewport by viewport, stitch together) to avoid truncated tall dashboards
  - data-export-date and data-export-ts were mentioned in feedback but current implementation uses #export-date and #export-ts (span elements, not data attributes) — this is fine as long as the DOM spans are always populated before any export call, which they are
```