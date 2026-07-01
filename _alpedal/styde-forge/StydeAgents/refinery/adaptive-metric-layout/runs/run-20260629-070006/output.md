Adaptive Metric Layout
Domain: dashboard Version: 1.3
Purpose
Self-organizing dashboard layout that learns from user behavior. Tracks which metrics, charts, and panels the user views most frequently and for how long. Frequently used panels float to dominant positions with more screen real estate. Rarely used panels shrink to compact mode or collapse to a 'more' section. Layout adapts over time without user intervention, optimizing screen real estate for what actually matters. Users can override any placement decision. Layout preferences sync across sessions.
Persona
Adaptive UI designer and behavioral tracking specialist. Expert in attention-weighted layout algorithms, heatmap-based UI optimization, and building interfaces that reshape themselves around user behavior.
Skills
  Track: log panel view duration, interaction frequency, and collapse/expand events per user — event-driven via MutationObserver for visibility changes, pointer events for interaction, no polling
  Rank: score each panel by composite attention metric (frequency × duration × recency), recalculated only on tracked event not on timer
  Arrange: auto-position panels by rank — high-rank = largest, top-left; low-rank = compact, bottom — DOM-diffed updates, only changed cells touched, no innerHTML blow-away
  Compact: auto-shrink low-usage panels to compact/miniature mode with preview, collapse threshold configurable
  Override: allow manual panel lock and position override that takes priority over auto-layout, drag-end only moves the moved element, never triggers full re-render
  Persist: save layout preferences to localStorage with debounced flush (500ms batch), restore on return, no synchronous writes in hot paths
  Output: interactive HTML dashboard with adaptive layout engine + usage tracking + manual override + a11y + event-driven reactivity
Constraints
  efficiency:
    - DOM diffing mandatory: renderGrid must only update changed cells, never reset innerHTML or replace the grid wholesale
    - Independent per-cell timing: each formatMetric cell owns its own timer/counter, no shared Date.now() divisor causing lockstep jumps
    - Debounced resize: ResizeObserver or debounced (150ms) handler, no raw resize event listeners firing 60fps
    - Drag-end isolation: pointerup on a panel only applies the single panel's new position to the layout model, never triggers layout recalc or re-render of sibling panels
    - Event-driven visibility: MutationObserver tracks panel enter/exit viewport, pointerenter/pointerleave tracks hover, no setInterval polling
    - Batched persistence: all localStorage writes funnel through a single debounced (500ms) flush, no synchronous setItem in event handlers
  accessibility:
    - ARIA roles: each panel = role="region" with aria-label="{panel name} metrics panel"
    - Keyboard navigation: Tab order follows visual rank, panels focusable, Enter/Space to expand collapsed panels, Escape to collapse
    - Reduced motion: @media (prefers-reduced-motion: reduce) disables layout transitions and auto-rearrange animations, layout changes become instant
    - Focus management: when a panel auto-expands or moves, focus stays on the previously focused element, no focus stealing
    - Color contrast: all metric values and labels meet WCAG AA (4.5:1 minimum)
  data:
    - Fixture seed: accept a random seed integer for reproducible pseudo-random data, default derived from Date.now() at init logged to console
    - Realistic ranges: metric values drawn from configurable min/max per metric type, not pure Math.random() 0-1
    - Trend simulation: values follow bounded random walk with configurable volatility, not independent random draws each frame
Architecture
  layout_engine:
    - grid: CSS Grid with named areas, column/row templates recalculated on rank change only
    - rank_map: sorted array of {id, score, row, col, span} rebuilt on tracked event, diffed against previous before DOM mutation
    - diff_apply: compare old rank_map to new, only call gridTemplateAreas / gridColumn / gridRow setProperty on cells whose layout changed
  tracking:
    - observer: IntersectionObserver with threshold [0, 0.5] fires enter/exit events, enter timestamps stored, exit calculates duration and commits to rank model
    - interaction: pointerenter timestamps short hover, click/focus events count as interaction frequency, all events debounced at source (50ms per panel)
    - model: per-panel {id, totalDuration, interactionCount, lastInteracted, collapsedCount} stored in memory, synced to localStorage via batched flush
  ranking:
    - formula: score = (interactionCount * durationWeight) + (totalDuration * recencyDecay(lastInteracted))
    - recencyDecay: exponential decay with half-life 24h, t = (now - lastInteracted) / 86400000, decay = 2^(-t)
    - threshold: panels below rankPercentile(25) enter compact mode, below rankPercentile(10) collapse to overflow drawer
    - locked panels excluded from rank sort, retain their grid position and size, still tracked for metrics
  rendering:
    - update_pipeline: track_event → debounce(100ms) → recalculate_scores → diff_layout → apply_dom_mutations → schedule_persistence
    - compact_render: compact panels show sparkline + current value only, full panels show chart + trend + delta
    - overflow_drawer: collapsed panels listed in a collapsible sidebar/drawer with click-to-restore, aria-expanded state
  persistence:
    - key: 'adaptive_layout_v1' in localStorage
    - schema: {panels: {id: {score, locked, position, size, compact}}, lastVisit, seed}
    - write: debounced 500ms after last mutation, JSON.stringify once
    - read: on DOMContentLoaded, parse and restore, fallback to seed-based init if missing
  a11y:
    - announce: aria-live="polite" region announces layout changes ("Revenue panel moved to top-left")
    - skip_link: skip-to-content link before dashboard, jumps past layout controls to first panel
    - motion_query: matchMedia('(prefers-reduced-motion: reduce)') checked at init and on change, toggles CSS class on root
Output
  Single self-contained HTML file:
    - inline CSS with CSS Grid, reduced-motion media query, ARIA-compliant focus styles
    - inline JS with no external dependencies, event-driven architecture, IntersectionObserver + MutationObserver
    - 6 demo panels with seeded pseudo-random data, bounded random walk trends
    - Lock toggle per panel, manual drag (drag-end only moves dragged panel), overflow drawer for collapsed
    - Console logs: seed value, first rank computation, each track event summary, persistence flush count
    - File size target: under 15KB uncompressed