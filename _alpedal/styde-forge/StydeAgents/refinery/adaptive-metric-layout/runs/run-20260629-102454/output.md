Adaptive Metric Layout
Domain: dashboard Version: 2
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
Structural completeness checks:
  panic_on_missing: config, state, DOM_root, panel_data, observer_handles
  panic_on_empty: panel_data array, config.columns, config.breakpoints
  warn_on_stale: observer_handles older than 30s without re-registration
  guard_truncation: max_panels=50, max_tracking_events=10000, max_state_size_kb=500
Rendering engine — targeted diff updates:
  render(changeSet): receives {added:[], removed:[], updated:[panelId,field]} or null for full init
  Full render path only executes on mount, panel add, or panel remove
  Update path targets a single card by id: locate cached DOM ref in refMap, mutate only changed fields (size class, position order, compact toggle, lock icon, rank badge)
  Lock toggle: patchDataset(refMap[id].lockIcon, 'locked', newVal) + toggleCSS class only; no rebuild
  Rank update (every 5s): iterate rank-sorted ids, apply CSS order property to grid container; DOM elements stay in place, only flex/grid order changes; heatmap dots preserved via position:absolute within their card — never detached
  refMap: WeakMap<id, {el, lockIcon, rankBadge, sizeContainer}> rebuilt only on add/remove; update path reads from refMap, never from querySelector
State persistence — debounced batching:
  pendingWrites: Map<key, value> accumulated per 300ms window
  debounceTimer: null | setTimeout handle
  saveState(key, value): writes to pendingWrites, starts or resets 300ms debounceTimer
  flushWrites(): on timer fire, JSON.stringify entire pendingWrites, single localStorage.setItem, clear pendingWrites
  Sync across tabs: storage event listener reads external changes, merges with in-memory state using lastWrite timestamp (highest wins per key)
Drag-drop — complete persistence path:
  dragStart(e): capture dragged panelId, set dataTransfer data, no ghost DOM element created (removed)
  dragOver(e): preventDefault, compute drop index from cursor position relative to grid children
  drop(e): extract panelId from dataTransfer, compute targetIndex, call applyManualOrder(panelId, targetIndex)
  applyManualOrder(id, index): splice id from manualOrder array, insert at index; saveState('manualOrder', manualOrder); trigger render({updated:[id,'order']}) — target-only update
  No drag-ghost element in DOM, no related CSS, no related JS — fully removed
Attention tracking:
  viewPortObserver: IntersectionObserver per panel, logs entry/exit timestamps, accumulates durationMs
  interactionListener: single delegated click/mousedown handler on grid container, filters by data-panel-id, increments interactionCount on matching panel
  collapseListener: single delegated handler on grid container for data-action="toggle-compact", toggles compact flag, does NOT trigger render — just toggles CSS class on refMap entry
  Score formula per panel: (interactionCount + 1) x (totalDurationMs / 1000 + 1) x recencyBoost
  recencyBoost: 1.0 default, 2.0 if lastInteraction within 5min, 1.5 within 30min, decays to 1.0 beyond
  Rank calculation runs every 5 seconds via setInterval, produces sorted array of ids, applies CSS order to grid cells only
Lock override — targeted toggle:
  onLockClick(panelId): toggle state.blockedPanels[panelId], patch refMap[panelId].lockIcon via dataset + CSS class
  Blocked panels excluded from rank-sort: their order comes from manualOrder or original mount position
  persist toggle immediately: saveState('blockedPanels', state.blockedPanels) — goes through debounce batching
Compact mode:
  Threshold: bottom 30% by score auto-compact, top 70% full-size
  Compact card: reduced height (60px), sparkline-only chart, tooltip-on-hover for detail
  Manual expand: click compact card toggles userOverride.compact[panelId] = false, persists, renders that card only
  render path: toggles CSS class on refMap[panelId].sizeContainer between 'panel-full' and 'panel-compact'
Observer lifecycle — refMap-driven:
  refMap built once on mount from panelData array, each entry stores: {el, lockIcon, rankBadge, sizeContainer}
  panel add: create DOM card, append to grid, create refMap entry, register observer
  panel remove: disconnect observer, delete refMap entry, remove DOM card
  panel update: no refMap change, no observer re-registration — directly mutate stored DOM refs
  Stale observer guard: interval every 30s checks observerCount === panelCount, logs warning on mismatch, auto-heals by re-registering missing observers
Config schema:
  columns: {sm:1, md:2, lg:3, xl:4}
  breakpoints: {sm:640, md:1024, lg:1440}
  rankIntervalMs: 5000
  compactThreshold: 0.3
  debounceMs: 300
  recencyWindows: {hot:300000, warm:1800000}
  maxPanels: 50
  maxTrackingEvents: 10000
  maxStateSizeKb: 500
  truncationPolicy: drop_oldest
Output:
  Single self-contained HTML file
  Inline CSS (no external dependencies)
  Vanilla JS (no framework)
  Responsive CSS grid: grid-template-columns scales by breakpoint
  Each panel: data-panel-id attribute, CSS class panel-full or panel-compact
  Lock icon: data-locked attribute, toggles CSS .locked class
  Rank badge: data-rank attribute, updated via CSS order property only
  All tracking data in memory, persisted to localStorage keyed by 'adaptive-dashboard-state'
  Storage event listener for cross-tab sync with timestamp-based conflict resolution
  Structural integrity: on mount, validate config completeness, panel data non-emptiness, truncate state if oversized — throw clear console.error on violation, halt render on critical, warn on non-critical