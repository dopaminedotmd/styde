refined-blueprint:
  source: desktop-mockup-artist v5
  changes-from-feedback:
    - add pre-submission style-lint step
    - inject lint constraints into config.yaml
    - add sub-label clarity note under usefulness
    - add postverify stage for compact diff summary
    - add verification section specifying single-line-per-file PASS/FAIL
    - wrap grep/sed commands in safe-shell format for Git-Bash
  blueprint-updates:
    code-quality-constraints:
      - css-dry: define custom properties before component styles; no hardcoded values
      - js-modern: const/let only; arrow functions (no function keyword); template literals (no + concatenation); spread/rest operators
      - sub-label-clarity: all sub-labels and units must be unambiguous (e.g., "12% of 10 Gbps link" not "12%")
    verification-protocol:
      - html-wellformedness: all tags closed, DOCTYPE present
      - css-syntax: no unclosed rules, selectors reference known classes
      - js-completeness: all event handlers bound, all functions closed, no trailing commas
      - content-rendering: non-empty SVG, chart canvases with data, populated tables
      - json-state: inline JSON must be parseable
      - structural-presence: all expected UI zones from catalog exist
      - postverify: compact diff-on-changes-only check with structured summary table
      - style-lint: grep for function keyword, grep for + concatenation, grep for var
    platform-safety:
      - escape single quotes in grep/sed patterns
      - prefer double-quotes around pattern files
      - verify grep/sed commands work on Git-Bash
  verification-checklist:
    - structural zones present and correct
    - all widgets render real content not lorem-ipsum
    - css at-rules complete and closed
    - event listeners reference defined functions
    - chart canvases have at minimum border/background
    - svg elements have viewBox width height and content
    - no hardcoded 404 URLs use data: URIs instead
    - pre-submission style-lint passed
suggested-score-after-fixes: 95
structural-catalog-zones-for-next-mockup:
  - titlebar
  - navigation-sidebar
  - header-with-actions
  - content-workspace
  - status-bar
  - floating-panels
  - modal-dialogs
widget-types-ready:
  - agent-status-card
  - gpu-monitor
  - activity-feed
  - system-overview-card
  - data-table
  - metric-gauge
  - chart-container
spacing-grid:
  titlebar-height: 32px
  sidebar-width-collapsed: 48px
  sidebar-width-expanded: 220px
  statusbar-height: 28px
  content-padding: 16px
  card-gap-grid: 12px
  card-gap-stacked: 8px
  widget-radius: 6px
  icon-sizes: [16, 20, 24]