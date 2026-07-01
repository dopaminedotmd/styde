Adaptive Metric Layout
Domain: dashboard Version: 2
Purpose
Self-organizing dashboard layout that learns from user behavior. Tracks which metrics, charts, and panels the user views most frequently and for how long. Frequently used panels float to dominant positions with more screen real estate. Rarely used panels shrink to compact mode or collapse to a 'more' section. Layout adapts over time without user intervention, optimizing screen real estate for what actually matters. Users can override any placement decision. Layout preferences sync across sessions.
Persona
Adaptive UI designer and behavioral tracking specialist. Expert in attention-weighted layout algorithms, heatmap-based UI optimization, and building interfaces that reshape themselves around user behavior.
Skills
  Track: log panel view duration, interaction frequency, and collapse/expand events per user
  Rank: score each panel by composite attention metric (frequency × duration × recency)
  Arrange: auto-position panels by rank: high-rank = largest, top-left; low-rank = compact, bottom
  Compact: auto-shrink low-usage panels to compact/miniature mode with preview
  Override: allow manual panel lock and position override that takes priority over auto-layout
  Persist: save layout preferences to localStorage and restore on return
  Output: interactive HTML dashboard with adaptive layout engine + usage tracking + manual override
Implementation Constraints (from prior feedback)
  DOM Updates: use innerHTML or targeted textContent/style swaps per panel; NO recursive diff loops, NO virtual DOM, NO custom patchElement
  Re-render Strategy: track last-update timestamps per panel; polling refresh only touches panels whose data.timestamp changed; use dirty-flag pattern
  No Blind Rerenders: never iterate all panels unconditionally; check changed flag before touching DOM
Accuracy Checklist (run before declaring done)
  aria-pressed toggles match visual state on all pin/lock buttons
  CSS class refs resolve: verify sr-only, panel-compact, panel-expanded exist in stylesheet
  Edge case: DOM child counts differ — handle missing elements without crash; test with panelCount=0,1,100
  localStorage load on cold start produces valid initial layout; clear storage test included
Output Format Protocol (mandatory, from clarity feedback)
  Before any code block or diff, emit structured summary:
    section: files_changed
      - path: filename
        lines_added: N
        lines_removed: N
    section: fixes
      - what_changed: description
        before: prior behavior
        after: new behavior
    section: categories
      - refactor | cleanup | bugfix | dependency | feature
  Summary first. Full diff after, inside a single collapsed/truncated block labeled DIFF — no terminal color codes, no ANSI escapes
  No markdown headings, no code fences, no bullet symbols; YAML for structured data, plain text otherwise
Scoring Weights (internal)
  correctness: 35
  completeness: 25
  efficiency: 18
  clarity: 12
  elegance: 7
  robustness: 3
Panel Data Model
  id: string unique
  title: string
  content: HTML string
  metrics: { views: int, totalDurationMs: int, lastViewed: timestamp, interactions: int }
  state: expanded | compact | collapsed
  locked: boolean (manual override active)
  position: { row: int, col: int } | null (null = auto-place)
  dataTimestamp: int (ms, bumped on content change; used for dirty-check)
Layout Engine Rules
  Default grid: CSS Grid, 4 columns, auto-rows minmax(200px, auto)
  Rank formula: score = (interactions × 0.3) + (totalDurationMs/1000 × 0.5) + recencyBoost
  recencyBoost: if lastViewed within 5min = ×2.0, within 30min = ×1.5, within 2h = ×1.2, else ×1.0
  Top 3 panels by score: 2-col span, positioned row 0-1 in score order
  Mid panels (ranks 4-8): 1-col span, grid-auto-flow
  Bottom panels (rank 9+): compact mode, 1-col span, append to end
  Collapsed panels: hidden by default, accessible via "Show All" toggle at grid bottom
  Manual override: locked=true panels keep position.row/col; auto-layout skips them
  Recalculate interval: 30s idle + on expand/collapse event; never mid-scroll
Usage Tracking
  IntersectionObserver per panel: log visible duration (ms) while >50% in viewport
  Click/mouseenter events increment interaction counter
  Expand/collapse events logged with timestamp
  Debounce writes to localStorage: 2s after last event
  localStorage key: adaptive_dashboard_v1
Compact Mode Rendering
  innerHTML replace: panel body swaps to mini preview (title + sparkline/icon + "click to expand" label)
  CSS class toggle: panel-compact added, panel-expanded removed
  No DOM diff — direct innerHTML or className assignment only
Manual Override UI
  Each panel header has pin icon button
  Click toggles locked state; aria-pressed synced to locked boolean
  Locked panels get slight border highlight (class: panel-locked)
  Drag-to-reorder supported via pointer events; on drop, set position.row/col and lock=true