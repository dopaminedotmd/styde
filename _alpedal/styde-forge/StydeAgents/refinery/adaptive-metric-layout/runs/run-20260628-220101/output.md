Adaptive Metric Layout
Domain: dashboard
Version: 2
Purpose
Self-organizing dashboard layout that learns from user behavior. Tracks which metrics, charts, and panels the user views most frequently and for how long. Frequently used panels float to dominant positions with more screen real estate. Rarely used panels shrink to compact mode or collapse to a 'more' section. Layout adapts over time without user intervention, optimizing screen real estate for what actually matters. Users can override any placement decision. Layout preferences sync across sessions.
Persona
Adaptive UI designer and behavioral tracking specialist. Expert in attention-weighted layout algorithms, heatmap-based UI optimization, and building interfaces that reshape themselves around user behavior.
Skills
  Track: log panel view duration, interaction frequency, and collapse/expand events per user
  Rank: score each panel by composite attention metric (frequency x duration x recency)
  Arrange: auto-position panels by rank: high-rank = largest, top-left; low-rank = compact, bottom
  Compact: auto-shrink low-usage panels to compact/miniature mode with preview
  Override: allow manual panel lock and position override that takes priority over auto-layout
  Persist: save layout preferences to localStorage and restore on return
  Output: interactive HTML dashboard with adaptive layout engine + usage tracking + manual override
Ranking Formula Specification
compositeScore = frequencyWeight * panel.frequency + durationWeight * panel.duration + recencyWeight * panel.recency
Where:
  frequencyWeight = 0.4, durationWeight = 0.35, recencyWeight = 0.25
  panel.frequency = clickCount / maxClickCount across all panels (0..1 normalized)
  panel.duration = totalViewMs / maxViewMs across all panels (0..1 normalized)
  panel.recency = exponentialDecay(lastViewedTimestamp, now) with halfLife = 86400000 (24 hours in ms)
    decay(t) = exp(-ln2 * (now - t) / halfLife)
    Result range: 0..1 where 1 = just viewed, near-0 = not viewed in days
Edge Cases and Missing Features
Toggle state cycles. Any toggle interaction (expand/collapse, lock/unlock, compact/normal) must provide a restore path. Toggling a panel to compact mode must expose a one-click restore button in the compacted preview header. Toggling lock off must pop up a confirmation before the panel re-enters auto-layout, with an undo option that persists for 5 seconds. Cycle detection: if the user toggles the same state more than 3 times in 10 seconds, the engine must pause auto-layout on that panel for 30 seconds and display a stabilization notice.
Drag-and-drop is not optional for dashboard UIs. Every panel must support HTML5 drag-and-drop with the following invariants:
  1. Drag starts only on the panel header area (not on chart content).
  2. During drag, a translucent ghost follows cursor. The drop zone shows a highlighted insertion marker.
  3. On drop, the dragged panel swaps positions with the panel at the drop target.
  4. If drop target panel is locked, the drag must snap back to origin and show a locked-panel indicator tooltip.
  5. Drop must trigger localStorage persist immediately.
  6. Touch devices: fall back to long-press drag via pointer events with identical behavior.
  7. Drag must work across dashboard sections (main grid to sidebar and vice versa).
Scoring formulas with temporal decay must be tested with synthetic extreme recency values. The exponential decay formula recency = exp(-ln2 * (now - t) / halfLife) with halfLife = 86400000 must produce correct values for:
  - t = now (just viewed): recency = 1.0
  - t = now - 1 hour: recency approx 0.97
  - t = now - 24 hours: recency = 0.5
  - t = now - 7 days: recency approx 0.0078
  - t = now - 30 days: recency approx 0.00000012
  - t = now + 1 hour (future timestamp, should be clamped): recency = 1.0, clamp t to <= now before computation
  - t = null or undefined: treat as epoch 0, recency approaches 0, never NaN
Counterintuitive-Values Test
After implementing the ranking formula, before any auto-arrange logic runs, verify with at least three synthetic input sets:
  Set A (all recent): 5 panels, all viewed within the last 5 minutes, similar frequency and duration. Verify scores cluster within 10% of each other. No single panel dominates.
  Set B (all old): 5 panels, last viewed > 7 days ago. Verify all recency contributions are below 0.01, and ranking is determined by frequency*duration only.
  Set C (mixed): 5 panels with extreme recency gradients: one viewed 1 second ago, one viewed 1 hour ago, one viewed 23 hours ago, one viewed exactly 24 hours ago, one viewed 7 days ago. Verify ordering is: newest first, and the 23-hour vs 24-hour panels differ by roughly 2x in recency weight (0.52 vs 0.25).
If any test produces counterintuitive ordering (e.g., an old low-frequency panel ranked above a recent high-frequency panel), fail the test and adjust weights. Record test results in the Performance constants section of the code.
Resource Cleanup Checklist
Every panel registration and interaction handler MUST include explicit cleanup. The following resources must be tracked and released:
  1. Timers: any setInterval or setTimeout created during panel mount must have a clearInterval/clearTimeout call paired in the cleanup function. Store timer IDs in an array panel.timers = []. On cleanup, iterate and clear each.
  2. Event listeners: any addEventListener call must have a paired removeEventListener call. Use named functions (not anonymous lambdas) so removeEventListener can reference them by identity. Store listener references in panel.listeners = [{target, type, handler}]. On cleanup, iterate and call removeEventListener for each.
  3. ResizeObserver / MutationObserver: disconnect all observers on cleanup. Store in panel.observers = []. On cleanup, call observer.disconnect() for each.
  4. IntersectionObserver (used for visibility tracking): disconnect and nullify. Failure to disconnect causes memory leaks and phantom visibility events.
  5. Incomplete state mutations: if a panel is mid-transition (dragging, animating, saving to localStorage) when cleanup runs, the mutation must be completed or rolled back. Define a panel.pendingMutations = [] array. On cleanup, resolve or reject each pending promise. Never leave a half-written localStorage entry or a half-applied DOM transform.
  6. localStorage write queue: if batch saving to localStorage, flush the queue on cleanup. If flush fails (quota exceeded, storage disabled), degrade gracefully by capping stored panels to 10 most recent and log a warning.
  7. Web Worker or MessageChannel: terminate worker on cleanup. Close MessageChannel port.
  8. Panel DOM elements: after cleanup, remove panel root from the dashboard container. Check for orphaned child elements via container.children.length reconciliation.
Cleanup must run on: panel removal, dashboard reset, browser beforeunload, and visibilitychange to hidden.
Known Pitfalls
setInterval called inside render body without cleanup. This creates a new timer on every render cycle with no handle stored for clearing. The old timers accumulate, firing callbacks against stale closure state. Fix: store the interval ID in a ref or module-level variable. Always call clearInterval before assigning a new setInterval. Verify that the interval function uses the latest state reference, not the closure-captured one.
Stale closures in event handlers. When an event handler references panel state variables captured at setup time, by the time the handler fires the state may have changed. Fix: use event delegation with data attributes (read current state from dataset on each invocation) instead of closure variables. Or re-bind handlers on each state change with the latest values.
Shallow object updates breaking React/memo comparison. Spreading state without creating a new reference for nested objects (e.g., {...panels, [id]: {...panels[id], compact: true}}) works correctly. But mutating the same object reference in place and then setting state will suppress re-render. Fix: always create a new top-level reference and a new panel object reference for the mutated panel. Never do panels[id].compact = true; setPanels(panels).
Event listener leaks on dynamic panels. Adding a resize listener to window inside a panel constructor but never removing it when the panel is removed. The listener holds a reference to the panel's closure scope, preventing garbage collection. Fix: always pair addEventListener with removeEventListener in the cleanup section. Use AbortController for a single cleanup signal if supported.
localStorage quota exceeded. Writing the full panel state on every interaction can exceed the 5-10MB localStorage limit (especially with serialized chart data). Fix: limit persisted state to panel id, position, size, compact flag, and lock flag only. Never persist raw metric data. On QuotaExceededError, catch it, truncate the saved panels list to the 5 most recently interacted, re-attempt save, and display a storage warning badge.
DOM thrash during auto-arrange. Re-flowing all panels simultaneously on every layout tick triggers forced synchronous layouts (layout thrashing). Fix: batch style changes. Read all current panel rects in one pass, compute new positions, then write all style changes in a single pass using requestAnimationFrame. Use transform (position) and scale (size) instead of top/left/width/height where possible to keep layout off the critical path.
config.yaml
judge_config:
  dimensions:
    efficiency:
      weight: 0.28
      scoring:
        type: negative
        rules:
          - pattern: "setInterval in render without cleanup"
            penalty: -15
            category: resource_leak
          - pattern: "addEventListener without removeEventListener"
            penalty: -15
            category: resource_leak
          - pattern: "incomplete state mutation on unmount"
            penalty: -10
            category: resource_leak
          - pattern: "innerHTML in hot path"
            penalty: -10
            category: dom_perf
          - pattern: "layout thrash in arrange loop"
            penalty: -8
            category: dom_perf
          - pattern: "localStorage write per interaction"
            penalty: -5
            category: i_o_perf
      criteria:
        - code_contains_cleanup_section
        - no_timer_leaks
        - no_listener_leaks
        - no_layout_thrash
        - batch_localsavage_writes
    completeness:
      weight: 0.22
      criteria:
        - covers_toggle_state_cycles_with_restore
        - covers_drag_and_drop
        - covers_temporal_decay_scoring_test
        - covers_resource_cleanup
        - covers_counterintuitive_test
    usefulness:
      weight: 0.25
      criteria:
        - partial_input_handling (missing metrics, null data, storage unavailable)
        - error_recovery_visible_in_ui
        - fallback_options_on_failure
    correctness:
      weight: 0.25
      criteria:
        - ranking_formula_matches_spec
        - drag_and_drop_swaps_correctly
        - persist_restore_roundtrip
        - compact_expand_toggles_correctly
eval_weights:
  efficiency: 0.28
  completeness: 0.22
  usefulness: 0.25
  correctness: 0.25
Performance Constraints
All per-user-action code paths must complete in O(1) or O(n) where n = number of dashboard panels (typically <= 12). No O(n^2) or worse.
Specifically:
  1. Auto-arrange: compute scores for all panels in a single pass. Sort by score descending. Assign positions based on sorted order. O(n log n) overall, with n <= 12, no perceptible cost.
  2. Drag-and-drop swap: O(1) swap of two panel positions in the state array. No full re-sort on drop.
  3. localStorage persist: batch writes via requestAnimationFrame coalescing. No write per event. Accumulate state changes for 500ms, then write once.
  4. Visibility tracking: IntersectionObserver callback processes only entries with isIntersecting change, not every scroll frame. Store lastKnownVisibility per panel to suppress duplicate events.
  5. Score recalculation: skip if no tracked event occurred in the last 1000ms. Use a dirty flag per panel that is set on interaction, cleared after score recompute.
  6. Compact mode rendering: compact panels render a minified preview only (header + sparkline or single stat). Full chart DOM is not created until the panel is expanded. Use a placeholder div during compact mode.
Data Ingestion
Usage events must arrive through one of:
  - Direct DOM event capturing (click, mouseenter, mouseleave on panel elements)
  - CustomEvent dispatch from external dashboard components
  - Programmatic push via window.__trackUsage(panelId, eventType)
All sources converge into a single usage event queue processed by the rank engine on each tick.
Validation Criteria
Ranking correctness. With all panels having identical frequency and duration, recency alone must determine order (most recently viewed first). With all panels having identical recency, frequency x duration must determine order. With extreme values (one panel used 100x more than others), that panel must always rank first regardless of recency unless recency is 0.
Drag-and-drop correctness. After swapping panel A to position of panel B, panel A must occupy that position on screen and in state. After page reload, the persisted positions must match. Dropping a locked panel must be rejected with visual feedback.
Compact mode correctness. Toggling a panel to compact must reduce its DOM footprint to a preview element. Expanding must restore the full panel in the same grid position. If the full panel's content has pending state (e.g., chart zoom level), it must be preserved in memory during compact mode, not destroyed.
Persist restore roundtrip. Save all panel positions, compact flags, and lock flags to localStorage. On page load (or across browser tabs), restore exact state. If localStorage is corrupted (invalid JSON, missing keys), fall back to default grid layout and overwrite the corrupted entry with a fresh initial state.
Counterintuitive-Values Test. Every run of the rank engine with new metrics data must pass the three synthetic test sets (all recent, all old, mixed extreme recency). Results must be logged to console on each test run. If any test fails, the layout engine must fall back to a simple grid (no auto-arrange) until the test is passed again on the next data update.
Output
Interactive single-file HTML dashboard with:
  - Grid of 6-12 panels, each containing a sample chart or metric display
  - Usage tracking engine (IntersectionObserver for visibility, click count, view duration)
  - Rank engine applying compositeScore = 0.4*freq + 0.35*duration + 0.25*recency with exponential decay
  - Auto-arrange layout engine that positions panels by rank: highest rank = top-left, largest size; lowest rank = bottom-right, compact size
  - Compact mode for low-rank panels (header + sparkline only, expand on click)
  - Manual drag-and-drop with position swap, locked-panel detection, and ghost-follows-cursor
  - Manual lock toggle (pin icon) that exempts panel from auto-arrange
  - localStorage persist on drag-drop and lock/compact toggle only (batch writes every 500ms)
  - Counterintuitive-Values Test on every rank cycle with visual pass/fail indicator
  - Resource Cleanup Checklist enforced: timers cleared, listeners removed, observers disconnected on panel removal
  - Error recovery: localStorage quota error caught with truncation, corrupted data falls back to defaults, IntersectionObserver unavailability falls back to scroll-based visibility approximation
  - Dark theme with glassmorphism panel styling, responsive for 768px and above
  - Demo mode: 5 minutes of simulated user behavior to demonstrate layout adaptation over time