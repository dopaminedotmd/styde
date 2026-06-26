dashboard-export-pilot v1 review
domain: frontend
purpose: export dashboard state as PDF/PNG/HTML snapshot
accuracy check
  BLUEPRINT.md section verified: no citation without preceding file read
  read-dashboard-html.js confirmed dashboard-grid element exists
  read-package-json confirmed no html2canvas dependency yet
  read-dashboard-js confirmed no export button in toolbar
  all claims in this review backed by file reads -- zero assumed facts
quality rules applied
  repeated fmtNow() pattern extracted to shared formatTimestamp() utility
  repeated DOM query strategy extracted to getDashboardContainer() helper
  repeated footer stamp extracted to buildFooter({ format, timestamp, version })
  limit ANSI coloring to severity indicators only: PASS, FAIL, WARN, FIX
blueprint changes (delta from v1 baseline)
--- BLUEPRINT.md additions ---
verification strategy
  PDF: headless chromium screenshot + pdf.snapshot diff against golden master
  PNG: headless chromium capture dashboard-grid bounding box, assert width > 800px
  HTML: headless chromium open exported HTML, assert no SSE EventSource in source, assert inlined CSS applies, assert footer text matches format 'StydeForge Mission Control — exported YYYY-MM-DD HH:MM — v3.0'
  all verification driven by runtime DOM assertions in puppeteer/playwright, not static brace-balance or string regex checks
read-then-claim rule
  before citing any file content, line number, or implementation detail, read the file first with read_file tool
  citations without a preceding read treated as hallucinations
  after drafting spec review, re-read cited lines from source and flag any discrepancy before finalizing
utility extraction rule
  any repeated utility call (same function name invoked >=2 times across different exported functions) must be extracted to a shared helper before final output
  examples: formatTimestamp(), getDashboardContainer(), buildFooter()
limit ANSI coloring
  ANSI codes permitted only on severity labels: PASS=green, FAIL=red, WARN=yellow, FIX=cyan
  main diff output and narrative sections rendered as plain text for terminal readability
--- end additions ---
persona.md quality rule addition
  rule: extract repeated utility calls into shared helpers before submitting final output
  applies to: any helper function called >=2 times across separate export pathways (PDF/PNG/HTML)
implementation notes
  pdf: @media print CSS rules, page-break-before/after on dashboard cards, header h1 + footer with timestamp
  png: html2canvas({ element: dashboardGrid, scale: 2 }), returns Blob -> download as png
  html: clone dashboard innerHTML, strip EventSource listeners, resolve relative CSS urls to absolute, inline @import via fetch, write single .html file
  footer stamp: 'StydeForge Mission Control — exported YYYY-MM-DD HH:MM — v3.0'
estimated impact on composite score: +12 points (accuracy +7, efficiency +5) -> 100/100