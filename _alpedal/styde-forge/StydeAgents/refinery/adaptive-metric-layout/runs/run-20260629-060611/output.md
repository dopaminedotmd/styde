Feedback integrerat. Refined Adaptive Metric Layout v1.1
---
blueprint: Adaptive Metric Layout
version: 1.1
domain: dashboard
changes:
  - id: "FIX-1"
    severity: medium
    source: "drag fragility"
    action: "Clamp drop coordinates to nearest valid grid cell boundary before applying relayout"
    implementation: |
      function clampToGrid(x, y, gridCols, gridRows, cellW, cellH) {
        const col = Math.min(gridCols - 1, Math.max(0, Math.round(x / cellW)));
        const row = Math.min(gridRows - 1, Math.max(0, Math.round(y / cellH)));
        return { col, row };
      }
    guard: "Cooldown 300ms suppresses overlapping drag events via trailing debounce"
    signal: "let dragCooldown = false; if (dragCooldown) return; dragCooldown = true; setTimeout(() => dragCooldown = false, 300);"
  - id: "FIX-2"
    severity: medium
    source: "timer double-counting"
    action: "Monotonic session ID on timer start; ignore stop if running session ID does not match"
    implementation: |
      let timerSessionId = 0;
      function startViewTimer(panelId) {
        const sid = ++timerSessionId;
        return { panelId, sid, start: performance.now() };
      }
      function stopViewTimer(panelId, sid) {
        if (sid !== timerSessionId) return null; // idempotent: stale call
        const duration = performance.now() - currentSession.start;
        timerSessionId = 0;
        return { panelId, duration };
      }
  - id: "FIX-3"
    severity: medium
    source: "meaningless preview tiles"
    action: "Replace fixed-size mini/chart preview tiles with summary-stat overlay or sparkline"
    constraint: "max 2x2 grid cells, labeled 'preview'"
    layout: |
      .panel-compact {
        grid-column: span 2;
        grid-row: span 2;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .panel-compact .sparkline { width: 100%; height: 32px; }
      .panel-compact .summary-stat { font-size: 0.75rem; text-align: center; }
  - id: "FIX-4"
    severity: medium
    source: "full re-renders per interaction"
    action: "Batch state updates; debounced scoring recalculation; target only changed DOM nodes"
    implementation: |
      const batchedUpdates = [];
      let rafScheduled = false;
      function scheduleUpdate(fn) {
        batchedUpdates.push(fn);
        if (!rafScheduled) {
          rafScheduled = true;
          requestAnimationFrame(() => {
            const fns = batchedUpdates.splice(0);
            rafScheduled = false;
            fns.forEach(f => f());
          });
        }
      }
    scoring: "Debounce recalc 500ms after last interaction via trailing debounce"
    dom: "Use data-panel-id attributes + querySelector for targeted DOM writes, not innerHTML"
skills:
  - track:
      log: [panel_view_duration, interaction_frequency, collapse_expand_events]
      idempotent: "stopViewTimer returns null when session ID mismatches (FIX-2)"
  - rank:
      formula: "frequency x duration x recency"
      debounce: "500ms trailing debounce before scoring recalculation (FIX-4)"
  - arrange:
      auto: "high-rank = largest + top-left; low-rank = compact + bottom"
      clamp: "drop coordinates clamped to nearest grid cell boundary before relayout (FIX-1)"
      cooldown: "300ms drag event suppression (FIX-1)"
  - compact:
      threshold: "bottom quartile → compact mode"
      render: "summary-stat overlay OR sparkline, max 2x2 cells, labeled preview (FIX-3)"
  - override:
      priority: "manual lock/position overrides auto-layout entirely"
      persist: true
  - persist:
      storage: localStorage
      keys: [layout_preferences, panel_rankings, view_durations]
      restore: "on page load, before first render cycle"
performance:
  batch_state_updates: true
  debounced_scoring: 500
  targeted_dom: true
  drag_cooldown_ms: 300
  raf_batching: true
  audit_checklist:
    - "Verify no innerHTML calls in hot paths"
    - "Confirm requestAnimationFrame batching for all DOM mutations"
    - "Profile drag handlers with 100+ rapid events"
    - "Test double-stop idempotency with rapid expand/collapse"
    - "Assert compact preview tiles never exceed 2x2 grid footprint"
expected_impact:
  efficiency_gap: 15
  recovered: 15
  target_score: 91