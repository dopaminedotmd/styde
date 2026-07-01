UsageTracker
  track: IntersectionObserver per panel — view duration, interaction count, collapse/expand events, recency timestamp
  score: (frequency × duration × recency_weight) — recency_weight = 1.0 if last_interaction < 300s, else decays linearly to 0.1 over 24h
  persist: localStorage key `adp_layout_usage` — JSON blob per panel id
  fallback: after 3 interactions, if < 2 panels have real data, seed demo dataset (5 synthetic sessions with varied panel usage)
  cleanup: disconnect() all observers on window beforeunload; tracked in `_observerRegistry` array
RankEngine
  input: usage map from tracker
  output: ordered panel list by composite score descending
  threshold: panels scoring < 20% of max score → compact mode
  compact: reduced to 1×1 grid cell, shows title + sparkline preview, expand button
  stable: ranking only recomputed when real data change detected (hash compare of usage map before/after)
  method: rank() returns {ordered: [], compacted: [], hash: string}
LayoutEngine
  grid: CSS Grid, 12-column, auto-rows
  arrange: panels placed in rank order — top-left fill, highest rank gets colspan=4 rowspan=2
  override: locked panels have `data-locked="true"` — skipped during reorder, position frozen
  refresh guard: before re-render, compare new layout hash with current DOM layout hash; skip if identical
  apply: updates grid-column, grid-row, data-compact attributes; adds transition class for 300ms CSS ease
  cleanup: debounce timer cleared on apply()
ManualOverride
  lock: click lock icon on panel header — toggles data-locked, saves to localStorage `adp_layout_locks`
  move: drag handle on locked panels — swaps position with target drop zone
  reset: "Reset Layout" button clears localStorage and re-ranks from scratch
  indicator: locked panels show pin icon; compacted panels show expand arrow
ScopeLock
  gate: feature X only activates after feature X-1 passes all assertions
  assertions per feature:
    1. Tracker: IntersectionObserver fires for ≥1 panel, usage written to localStorage
    2. Ranker: rank() returns non-empty ordered array, compact flag set for bottom panel
    3. Layout: DOM reflows, at least one panel changes grid-column/grid-row
    4. Override: lock toggle adds data-locked, drag swaps two panel positions
    5. Persist: page reload restores layout from localStorage within 200ms
  autotest: `runAutotest()` validates all assertions, logs failures to console group, blocks feature enablement on fail
  demo fallback: `seedDemoData()` injects 5 synthetic user sessions covering 8 panels with varied scores
HTML output follows. Single file, no external deps.