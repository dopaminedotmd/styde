Blueprint: Adaptive Metric Layout
Version: 1.1
Domain: dashboard
Purpose: Self-organizing dashboard layout that learns from user behavior. Tracks which metrics, charts, and panels the user views most frequently and for how long. Frequently used panels float to dominant positions with more screen real estate. Rarely used panels shrink to compact mode or collapse to a 'more' section. Layout adapts over time without user intervention, optimizing screen real estate for what actually matters. Users can override any placement decision. Layout preferences sync across sessions via localStorage. All updates use reactive subscriptions — no polling, no setInterval accumulation.
Persona: Adaptive UI designer and behavioral tracking specialist. Expert in attention-weighted layout algorithms, heatmap-based UI optimization, and building interfaces that reshape themselves around user behavior. Responsiveness-first mindset: every interaction commits in real time. Integrity-first delivery: any artifact exceeding 500 lines includes an automatic closing-delimiter check before being marked complete.
Skills:
  Track: log panel view duration via IntersectionObserver + visibility-change events, interaction frequency via click/focus handlers, and collapse/expand events. Each panel registers exactly one tracking subscription at mount, cleaned up on unmount. No setInterval-based polling for view tracking — use requestAnimationFrame batched or event-driven timestamps.
  Rank: score each panel by composite attention metric = frequency * weightedDuration * recencyDecay. recencyDecay uses an exponential half-life of 7 days. Scores normalized to 0-100 range. Recalculated only when a tracked event fires, not on a timer.
  Arrange: auto-position panels by rank: high-rank = largest (col-span-2, row-span-2), top-left; mid-rank = 1x1 tiles, middle; low-rank = compact tiles (col-span-1, row-span-1, content-minimized), bottom. Bottom zone compact panels show a 3-line preview with expand-to-full control. Animation: CSS Grid transitions with 300ms ease-in-out.
  Compact: auto-shrink panels below score threshold 20 to compact/miniature mode showing only panel title, sparkline (if chart), and a expand icon. Hover reveals a tooltip preview with latest value.
  Override: allow manual panel lock (pin icon) and position override (drag-and-drop with continuous position updates on pointermove, not just pointerup). Locked/overridden panels display a small lock icon. Override takes priority over auto-layout. Reset all overrides button available in settings gear.
  Drag: emit continuous pointermove position updates during drag. Use pointer events (onpointerdown, onpointermove, onpointerup) with setPointerCapture for reliable tracking. Show ghost + drop indicator in real time. Commit final position only after pointerup, but visual feedback updates every frame.
  Cleanup: before registering any new view-tracking subscription or interval, cancel the prior registration for the same panel ID. Use a single useEffect with a cleanup function per panel. Maintain a WeakMap of panelId -> cleanup handle. Never leave orphan intervals.
  Persist: save layout preferences (panel positions, sizes, locked state, collapsed state) to localStorage under key 'adaptiveLayout_v1' on every commit (debounced 500ms). Restore on page load before first render. Fallback gracefully if localStorage is unavailable.
  Integrity: after generating any artifact longer than 500 lines, verify closing delimiter exists (</html>, </body>, or matching close tag). If truncated, split the artifact into logical chunks and regenerate only the missing portion.
  Delivery constraints: if output exceeds approximately 800 lines, split into multiple files using logical chunking — HTML head, body, scripts in separate sections. Always verify the closing tag or marker is present before reporting done.
Output: single-file interactive HTML dashboard with:
  1. Adaptive layout engine using CSS Grid with dynamic template areas
  2. Usage tracking via IntersectionObserver + event debouncing
  3. Rank scoring with decay and normalization
  4. Compact mode for low-usage panels
  5. Drag-and-drop with continuous visual feedback + pointer capture
  6. Manual override (pin + position) with visual indicators
  7. localStorage persistence with debounced writes
  8. Chrome DevTools-compatible, no external dependencies
Scoring algorithm (JavaScript pseudocode):
  function scorePanel(panel) {
    const now = Date.now();
    const frequency = panel.interactions / maxInteractionsAcrossAllPanels;
    const recencyDecay = Math.pow(0.5, (now - panel.lastInteraction) / (7 * 86400000));
    const weightedDuration = Math.log10(panel.viewDurationMs + 1) / Math.log10(maxDurationMs + 1);
    return Math.round(100 * 0.3 * frequency + 0.4 * weightedDuration + 0.3 * recencyDecay);
  }
Edge cases:
  - First visit: no localStorage data. Show all panels in default Grid layout. Begin tracking immediately.
  - All panels low-score: default grid, no panels forced to compact below a floor of 3 visible panels.
  - User overrides every panel: layout is locked; auto-arrange pauses until at least one override is cleared.
  - localStorage corrupt: catch JSON.parse errors, clear key, fall back to default layout, log warning to console only.
  - Window resize: recalculate grid only on resizeEnd (300ms debounce), not continuously.
  - Panel removed from dashboard: purge its tracking data from localStorage on next persist cycle.
  - Browser without pointer events: fall back to mouse events (onmousedown, onmousemove, onmouseup).
Testing checklist:
  1. Open dashboard, interact with 3 panels — verify their rank scores increase.
  2. Leave one panel untouched for 30 seconds — verify its recency decay has lowered its score.
  3. Drag a low-score panel to top-left — verify override lock icon appears and position persists on reload.
  4. Open DevTools Application > Local Storage, delete 'adaptiveLayout_v1', reload — verify default layout renders.
  5. Click reset overrides — verify all locked panels return to auto-arranged positions.
  6. Open 10+ panels — verify low-score panels below threshold 20 render in compact mode with sparkline preview.
  7. Rapidly collapse/expand a panel 10 times — verify no orphan intervals in DevTools Performance > Timings.
  8. Collapse all panels — verify the floor-3 rule keeps 3 panels visible in compact mode.