Adaptive Metric Layout
Domain: dashboard Version: 2
Purpose
Self-organizing dashboard layout that learns from user behavior. Tracks which metrics, charts, and panels the user views most frequently and for how long. Frequently used panels float to dominant positions with more screen real estate. Rarely used panels shrink to compact mode or collapse to a 'more' section. Layout adapts over time without user intervention, optimizing screen real estate for what actually matters. Users can override any placement decision. Layout preferences sync across sessions.
Production readiness: >=90 requires zero dead code, all CSS selectors verified against rendered DOM, and per-feature cleanup sections satisfied.
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
Code Quality Spec
  dead_code_policy: Every exported function must be called in at least one code path. Remove or inline unused functions before submission. No placeholder stubs that return without implementation.
  css_selector_verification: All CSS classes referenced in JS selectors must be applied to DOM elements in the rendered output. Run integration test that queries actual class names from rendered layout and cross-references against all querySelector/querySelectorAll calls.
  resource_cleanup: Every feature spec must include a cleanup section naming which resources (timers, observers, listeners) must be released and their teardown hook. Unmanaged IntersectionObserver, MutationObserver, ResizeObserver, setInterval, setTimeout, and addEventListener instances are blocking defects.
Track
  events:
    - panel_visible: IntersectionObserver detects panel entering viewport, starts duration timer
    - panel_hidden: panel leaves viewport, stops timer, logs duration
    - panel_interaction: click, scroll, resize within panel increments interaction counter
    - panel_toggle: collapse/expand event logged with timestamp
  storage: write to localStorage key 'adl_events' as JSON array, append-only per session, flush every 5s via debounced write
  cleanup:
    resources:
      - IntersectionObserver: stored as this._visibilityObserver, disconnected in teardown()
      - flush timer: stored as this._flushTimer, cleared via clearInterval in teardown()
      - event listeners: all addEventListener calls removed via removeEventListener with same reference in teardown()
    teardown_hook: trackEngine.teardown() — call before re-render or page unload
  verification:
    - all 4 event types reachable from UI interactions? YES/NO per event
    - localStorage write completes without JSON circular reference errors? YES/NO
    - flush timer cleared on teardown — no dangling intervals in browser devtools? YES/NO
    - event listeners removed — zero retained listeners on re-render per getEventListeners()? YES/NO
Rank
  input: events array from localStorage key 'adl_events'
  algorithm:
    decay_factor: 0.95 per day since event
    composite: sum over events of (interaction_count * avg_duration_seconds * decay_factor^days_ago)
  output: sorted panel_ids by composite descending
  edge_cases:
    - zero events for panel: assign base_score = 0, place in 'more' section
    - localStorage empty or corrupted: all panels start with base_score = 0, equal footing
    - NaN from corrupted event data: skip event, log warning to console, continue with remaining
  cleanup:
    resources:
      - none persistent; pure computation, no observers/timers
    teardown_hook: none required
  verification:
    - rank changes when new events added? YES/NO
    - decay reduces old event weight vs fresh events? YES/NO
    - NaN event data does not crash ranking? YES/NO
Arrange
  function: arrangeDOM(scores, overrides)
    - NOT arrangeDOM() dead stub returning without side effects
    - NOT arrangeSplice() — removed, functionality merged into arrangeDOM
    - sorts panel_ids by score descending
    - applies overrides: if panel has locked position, skip auto-placement, use override.grid_area
    - top-2 panels: grid span 2 cols × 2 rows (dominant tile)
    - next-3 panels: grid span 1 col × 1 row (standard tile)
    - remainder: compact mode (see Compact skill)
    - applies CSS grid-area assignments to DOM elements
  selector_binding: CSS classes for grid layout queries (.panel-card, .panel-dominant, .panel-standard, .panel-compact, .panel-more) must match elements actually rendered. Integration test step: querySelectorAll('.panel-card') returned N elements, expected N matching rendered panels.
  drag_drop: boundary detection queries real rendered class names (not assumed/hardcoded) — getComputedStyle on drop target, not string match against whitelist
  cleanup:
    resources:
      - ResizeObserver (if used for responsive grid): stored as this._resizeObserver, disconnected in teardown()
    teardown_hook: arrangeEngine.teardown() — call before re-render
  verification:
    - arrangeDOM is the single entry point, not a dead stub? YES/NO
    - arrangeSplice does not exist in final code? YES/NO
    - all CSS selectors in JS match classes on rendered DOM elements? YES/NO (integration test)
    - drag-drop boundary detection uses getComputedStyle or classList.contains on actual element? YES/NO
    - locked panels stay in override position after re-rank? YES/NO
    - unlocked panels move according to new rank? YES/NO
Compact
  trigger: panel rank below top-5 threshold
  modes:
    - miniature: 80px × 80px card showing panel title + sparkline/trend arrow only
    - collapsed: hidden behind 'more' drawer, toggled by "+N more" button
  preview: hover on compact panel shows tooltip with full metric summary
  expand: click compact panel or "more" drawer item restores to standard size
  cleanup:
    resources:
      - tooltip show/hide timer: stored as this._tooltipTimer, cleared in teardown()
      - drawer toggle listener: removed in teardown()
    teardown_hook: compactEngine.teardown()
  verification:
    - panels below threshold auto-compact on next arrange? YES/NO
    - hovering compact panel shows tooltip? YES/NO
    - clicking compact panel expands it? YES/NO
    - "+N more" drawer lists all compacted panels? YES/NO
    - expanding from drawer restores standard size? YES/NO
Override
  mechanism:
    - lock: toggle per-panel — locked panels skip auto-arrange, keep current position
    - pin: drag panel to new position, sets override.grid_area, auto-applies lock
    - unlock: removes override, panel resumes auto-placement on next arrange
  UI: lock icon on each panel card, toggle on click. Visual indicator: locked panels show border color change.
  storage: overrides saved to localStorage key 'adl_overrides' as {panel_id: {locked: bool, grid_area: string}}
  cleanup:
    resources:
      - drag event listeners (dragstart, dragover, drop): removed in teardown()
      - lock icon click listeners: removed in teardown()
    teardown_hook: overrideEngine.teardown()
  verification:
    - lock toggle prevents auto-arrange for that panel? YES/NO
    - drag-pin sets grid_area and auto-locks? YES/NO
    - unlock resumes auto-placement? YES/NO
    - overrides persist across page reload? YES/NO
    - visual indicator changes on lock? YES/NO
Persist
  keys:
    - adl_events: tracking event log
    - adl_overrides: user overrides
    - adl_layout: last computed layout state (grid template, panel positions)
  sync: on page load, restore from localStorage. If keys missing, start fresh with defaults.
  write: debounced 2s after last state change to avoid thrashing
  cross_session: layout restores exactly. Events persist across sessions for accurate long-term ranking.
  storage_limit: check remaining quota, warn console if usage > 80% of 5MB localStorage limit
  cleanup:
    resources:
      - debounce timer: stored as this._persistTimer, cleared in teardown()
    teardown_hook: persistEngine.teardown()
  verification:
    - layout restores on page reload? YES/NO
    - ranking events survive browser restart? YES/NO
    - overrides survive browser restart? YES/NO
    - quota warning fires before limit exceeded? YES/NO
Output
  deliverable: single self-contained HTML file with inline CSS + JS, zero external dependencies
  structure:
    - grid container: CSS Grid with named areas, responsive breakpoints at 768px and 1024px
    - panel cards: styled with border-radius 8px, box-shadow, transition on grid-area change (200ms ease)
    - lock indicator: SVG padlock icon inline, toggled class .panel-locked
    - compact cards: reduced size, grayscale filter at 30%, sparkline from 7-day trend data
    - more drawer: slide-in from right, overlay background, lists compacted panel names
  integration_test:
    step: "Verify all CSS classes referenced in JS selectors are actually applied to DOM elements in the rendered output"
    method: after render, iterate all querySelector/querySelectorAll calls in source, confirm each returns non-empty NodeList or non-null element
  live_data_refresh:
    requirement: optional stretch goal for production readiness
    implementation: WebSocket or polling (setInterval 30s) to refresh metric values without full page reload
    scope: only panel data values update; layout does not re-rank on data refresh (ranking uses interaction events, not metric values)
    cleanup: polling interval or WebSocket connection closed in teardown()
  verification:
    - HTML file opens and renders in Chrome/Firefox/Safari without console errors? YES/NO
    - CSS grid responds to viewport breakpoints? YES/NO
    - all selectors resolve to DOM elements? YES/NO (integration test)
    - panel move transitions animate smoothly? YES/NO
Global Verification Checklist
  completeness:
    - all 7 skills implemented with no stubs? YES/NO
    - every exported function called in at least one code path? YES/NO
    - all 6 teardown hooks implemented and wired to page unload + re-render? YES/NO
  accuracy:
    - all states handled per feature (empty, error, normal, edge)? YES/NO
    - zero observer/listener leaks on re-render (check devtools)? YES/NO
    - zero dead code paths (no unreachable branches)? YES/NO
  integration:
    - CSS selector verification test passes? YES/NO
    - drag-drop uses runtime class queries not hardcoded strings? YES/NO
    - localStorage quota check functional? YES/NO
  stretch:
    - live data refresh mechanism present (polling or WebSocket)? YES/NO