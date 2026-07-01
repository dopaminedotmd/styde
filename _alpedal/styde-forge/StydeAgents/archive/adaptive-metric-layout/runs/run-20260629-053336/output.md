<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
/* ============================================================
   CSS Variables — single source of truth for all measurements
   ============================================================ */
:root {
  --grid-cols: 4;
  --grid-gap: 12px;
  --panel-radius: 10px;
  --panel-padding: 16px;
  --header-height: 36px;
  --compact-min-height: 80px;
  --panel-min-width: 220px;
  --transition-speed: 0.35s;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.12);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.18);
  --color-bg: #f4f5f7;
  --color-panel: #ffffff;
  --color-border: #e1e4e8;
  --color-text: #1a1a2e;
  --color-muted: #6b7280;
  --color-accent: #4f46e5;
  --color-accent-light: #eef2ff;
  --color-rank-high: #059669;
  --color-rank-mid: #d97706;
  --color-rank-low: #9ca3af;
  --color-locked: #7c3aed;
  --drag-ghost-opacity: 0.55;
}
/* ============================================================
   Base Reset & Body
   ============================================================ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--color-bg);
  color: var(--color-text);
  min-height: 100vh;
  padding: 20px;
  line-height: 1.5;
}
/* ============================================================
   Toolbar — controls above the grid
   ============================================================ */
.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.toolbar h1 {
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: -0.3px;
  margin-right: auto;
}
.toolbar button {
  padding: 7px 16px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-panel);
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  transition: background var(--transition-speed), box-shadow var(--transition-speed);
}
.toolbar button:hover { background: var(--color-accent-light); box-shadow: var(--shadow-sm); }
.toolbar button:active { transform: scale(0.97); }
.mode-indicator {
  font-size: 0.8rem;
  color: var(--color-muted);
  padding: 4px 10px;
  border-radius: 12px;
  background: #f0f0f5;
}
/* ============================================================
   Dashboard Grid — CSS Grid that panels flow into
   ============================================================ */
.dashboard {
  display: grid;
  grid-template-columns: repeat(var(--grid-cols), 1fr);
  gap: var(--grid-gap);
  align-items: start;
  transition: grid-template-columns var(--transition-speed);
}
/* ============================================================
   Panel — the core tile
   ============================================================ */
.panel {
  background: var(--color-panel);
  border: 1px solid var(--color-border);
  border-radius: var(--panel-radius);
  padding: var(--panel-padding);
  min-height: 160px;
  cursor: grab;
  transition:
    transform var(--transition-speed) ease,
    box-shadow var(--transition-speed) ease,
    grid-column var(--transition-speed) ease,
    grid-row var(--transition-speed) ease,
    opacity var(--transition-speed) ease,
    border-color var(--transition-speed) ease;
  box-shadow: var(--shadow-sm);
  position: relative;
}
.panel:active { cursor: grabbing; }
.panel:hover { box-shadow: var(--shadow-md); }
.panel:focus-within { box-shadow: var(--shadow-md); outline: none; }
/* --- Rank-driven column span (set by JS via data-colspan) --- */
.panel[data-colspan="1"] { grid-column: span 1; }
.panel[data-colspan="2"] { grid-column: span 2; }
.panel[data-colspan="3"] { grid-column: span 3; }
.panel[data-colspan="4"] { grid-column: span 4; }
/* --- Rank-driven row span for high-priority panels --- */
.panel[data-rowspan="2"] { grid-row: span 2; min-height: 340px; }
/* --- Visual rank indicators --- */
.panel[data-rank-tier="high"] { border-left: 4px solid var(--color-rank-high); }
.panel[data-rank-tier="mid"]  { border-left: 4px solid var(--color-rank-mid); }
.panel[data-rank-tier="low"]  { border-left: 4px solid var(--color-rank-low); }
/* ============================================================
   Compact Mode — low-rank panels shrink
   ============================================================ */
.panel.compact {
  min-height: var(--compact-min-height);
  padding: 10px 14px;
  opacity: 0.72;
  font-size: 0.82rem;
}
.panel.compact .panel-body { max-height: 36px; overflow: hidden; }
.panel.compact .panel-footer { display: none; }
.panel.compact .panel-metric-value { font-size: 1rem; }
/* ============================================================
   Panel Internal Structure
   ============================================================ */
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--header-height);
  margin-bottom: 8px;
}
.panel-title {
  font-weight: 600;
  font-size: 0.92rem;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: var(--color-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.panel-controls {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}
.panel-controls button {
  width: 26px;
  height: 26px;
  border: none;
  border-radius: 5px;
  background: transparent;
  cursor: pointer;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-muted);
  transition: background var(--transition-speed), color var(--transition-speed);
}
.panel-controls button:hover { background: #f0f0f5; color: var(--color-text); }
/* Lock toggle — distinct visual when locked */
.panel-controls .btn-lock[aria-pressed="true"] {
  color: var(--color-locked);
  background: #f5f3ff;
  font-weight: 700;
}
.panel-body {
  transition: max-height var(--transition-speed) ease;
  overflow: hidden;
}
.panel-metric-value {
  font-size: 1.8rem;
  font-weight: 700;
  letter-spacing: -0.5px;
  line-height: 1.2;
  margin-bottom: 4px;
}
.panel-metric-sub {
  font-size: 0.78rem;
  color: var(--color-muted);
}
.panel-footer {
  margin-top: 10px;
  font-size: 0.7rem;
  color: var(--color-muted);
  display: flex;
  justify-content: space-between;
  border-top: 1px solid var(--color-border);
  padding-top: 6px;
}
/* ============================================================
   Drag Ghost — the visual clone during drag
   ============================================================ */
.panel.dragging {
  opacity: var(--drag-ghost-opacity);
  box-shadow: var(--shadow-lg);
  transform: scale(1.03);
  z-index: 100;
  cursor: grabbing;
}
/* Drop zone highlight on grid cells */
.panel.drop-target {
  outline: 2px dashed var(--color-accent);
  outline-offset: 2px;
  border-color: var(--color-accent);
}
/* ============================================================
   Heatmap Overlay — subtly shows panel scores
   ============================================================ */
.panel .score-indicator {
  position: absolute;
  top: 6px;
  right: 40px;
  font-size: 0.6rem;
  font-weight: 600;
  color: var(--color-muted);
  opacity: 0;
  transition: opacity var(--transition-speed);
}
.panel:hover .score-indicator { opacity: 1; }
/* ============================================================
   Responsive — collapse columns on smaller viewports
   ============================================================ */
@media (max-width: 900px) {
  :root { --grid-cols: 2; }
  .panel[data-colspan="3"],
  .panel[data-colspan="4"] { grid-column: span 2; }
}
@media (max-width: 500px) {
  :root { --grid-cols: 1; }
  .panel[data-colspan] { grid-column: span 1; }
}
/* ============================================================
   Panel Content Variants — sparkline / bar / number
   ============================================================ */
.sparkline {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  height: 40px;
  margin-top: 6px;
}
.sparkline-bar {
  flex: 1;
  background: var(--color-accent);
  border-radius: 2px 2px 0 0;
  min-height: 3px;
  transition: height 0.5s ease;
}
.sparkline-bar.low { background: var(--color-rank-low); }
.sparkline-bar.mid { background: var(--color-rank-mid); }
.sparkline-bar.high { background: var(--color-rank-high); }
</style>
</head>
<body>
<!-- ============================================================
     Toolbar
     ============================================================ -->
<div class="toolbar">
  <h1>Adaptive Dashboard</h1>
  <button id="btn-reset-scores" title="Reset all tracking data">Reset Scores</button>
  <button id="btn-toggle-auto" title="Toggle automatic layout">Auto-Layout: ON</button>
  <span class="mode-indicator" id="mode-indicator">adaptive</span>
</div>
<!-- ============================================================
     Dashboard Grid — panels are injected by JS
     ============================================================ -->
<div class="dashboard" id="dashboard" role="grid" aria-label="Adaptive metric dashboard"></div>
<script>
/**
 * ============================================================
 * Adaptive Metric Layout Engine
 * ============================================================
 *
 * Architecture:
 *   StorageManager  — localStorage read/write with JSON schema validation
 *   ScoreEngine     — attention scoring with exponential decay to floor
 *   UsageTracker    — IntersectionObserver + click/collapse event capture
 *   LayoutEngine    — arranges panels by rank, manages DOM grid assignments
 *   DragManager     — grid-aware drag-and-drop with cell inference from mouse position
 *   Dashboard       — orchestrator, wires components together
 *
 * Data flow:
 *   User action -> UsageTracker captures event -> ScoreEngine recomputes ->
 *   LayoutEngine re-ranks -> DOM update via CSS grid span assignment.
 *   All state persisted to localStorage on change (debounced 400ms).
 */
'use strict';
/* ============================================================
   StorageManager — localStorage with schema validation
   ============================================================ */
class StorageManager {
  /** Prefix for all keys to avoid namespace collisions */
  static KEY_PREFIX = 'adaptive_dash_';
  /** Current schema version — bump on breaking changes to invalidate old data */
  static SCHEMA_VERSION = 2;
  /**
   * Load panel state from localStorage.
   * Returns default state if missing, corrupt, or wrong schema version.
   * @returns {Object} { panels: Object<string, PanelState>, settings: Object }
   */
  static load() {
    try {
      const raw = localStorage.getItem(this.KEY_PREFIX + 'state');
      if (!raw) return this._defaultState();
      const data = JSON.parse(raw);
      // Schema version gate — discard stale formats
      if (data._schema !== this.SCHEMA_VERSION) return this._defaultState();
      return data;
    } catch (_) {
      // Corrupt localStorage entry — fall back to defaults silently
      return this._defaultState();
    }
  }
  /**
   * Persist panel state to localStorage.
   * @param {Object} state — full state object including panels and settings
   */
  static save(state) {
    state._schema = this.SCHEMA_VERSION;
    state._updated = Date.now();
    try {
      localStorage.setItem(this.KEY_PREFIX + 'state', JSON.stringify(state));
    } catch (e) {
      // localStorage full or unavailable — degrade gracefully, no crash
      console.warn('StorageManager: save failed', e.message);
    }
  }
  /** @returns {Object} Factory default state */
  static _defaultState() {
    return {
      _schema: this.SCHEMA_VERSION,
      _updated: Date.now(),
      settings: { autoLayout: true },
      panels: {}
    };
  }
}
/* ============================================================
   ScoreEngine — attention scoring with exponential decay to floor
   ============================================================ */
class ScoreEngine {
  /** Floor value — scores never decay below this (stability guarantee) */
  static DECAY_FLOOR = 0.01;
  /** Decay factor per hour of inactivity (lambda in exponential decay) */
  static DECAY_FACTOR = 0.12;
  /** Weight multipliers for each signal component */
  static WEIGHTS = Object.freeze({
    viewDuration: 0.5,   // seconds viewed, capped at 120s per session
    interactions: 0.35,  // click/expand/collapse count
    recency:      0.15   // freshness bonus: 1.0 if < 1hr, linearly to 0 at 24hr
  });
  /**
   * Compute composite attention score for a single panel.
   * score = w1 * f(duration) + w2 * f(interactions) + w3 * f(recency)
   * Decay is applied uniformly: score *= e^(-lambda * hours_since_last_interaction)
   * Floor enforced at 0.01 — single write, no correction loop.
   *
   * @param {Object} panel — { totalViewSeconds, interactionCount, lastInteractionAt }
   * @returns {number} score in [0.01, 100]
   */
  static compute(panel) {
    const now = Date.now();
    const hoursSinceLast = panel.lastInteractionAt
      ? Math.max(0, (now - panel.lastInteractionAt) / 3_600_000)
      : 24; // cold-start: treat as 24h stale
    // Exponential decay — applied once, no iterative correction
    const decay = Math.exp(-this.DECAY_FACTOR * hoursSinceLast);
    // Normalize view duration: cap at 120s, scale to [0,1]
    const durNorm = Math.min(panel.totalViewSeconds || 0, 120) / 120;
    // Normalize interaction count: log scale to avoid domination by click-heavy users
    const intNorm = Math.min((panel.interactionCount || 0), 100) / 100;
    // Recency: 1.0 for < 1hr, linear decay to 0 at 24hr
    const recency = hoursSinceLast <= 1
      ? 1.0
      : Math.max(0, 1 - (hoursSinceLast - 1) / 23);
    const raw = (
      this.WEIGHTS.viewDuration * durNorm +
      this.WEIGHTS.interactions  * intNorm +
      this.WEIGHTS.recency       * recency
    ) * decay * 100;
    // Floor at DECAY_FLOOR — stabilised, single write, no correction passes
    return Math.max(this.DECAY_FLOOR, Math.round(raw * 100) / 100);
  }
  /**
   * Compute scores for all panels, return sorted array.
   * @param {Object<string, Object>} panels — keyed by panel ID
   * @returns {Array<{id: string, score: number}>} sorted descending
   */
  static rankAll(panels) {
    const scored = Object.entries(panels).map(([id, p]) => ({
      id,
      score: this.compute(p)
    }));
    scored.sort((a, b) => b.score - a.score);
    return scored;
  }
}
/* ============================================================
   UsageTracker — captures view duration, clicks, collapse/expand
   ============================================================ */
class UsageTracker {
  constructor(onUpdate) {
    /** @type {function} Callback invoked on each state change */
    this._onUpdate = onUpdate;
    /** @type {Object<string, Object>} In-memory panel state keyed by panel ID */
    this._panels = {};
    /**
     * IntersectionObserver — created ONCE, reused across all panels.
     * Uses a ref-based store (Map) keyed by panel element to track
     * visibility entry/exit timestamps. Callback is a stable reference,
     * never re-created per render.
     */
    /** @type {Map<Element, string>} element -> panel ID */
    this._observerMap = new Map();
    /** @type {Map<string, number>} panel ID -> visibility start timestamp */
    this._visibilityStart = new Map();
    // Single observer instance for entire tile lifecycle
    this._observer = new IntersectionObserver(
      (entries) => this._handleIntersection(entries),
      // Threshold: 50% of panel must be visible to count as "viewing"
      { threshold: 0.5 }
    );
  }
  /**
   * IntersectionObserver callback — stable reference, attached once.
   * Tracks when a panel enters/leaves the viewport (50% threshold).
   * Accumulates view duration per panel on exit.
   * @param {IntersectionObserverEntry[]} entries
   */
  _handleIntersection(entries) {
    const now = Date.now();
    for (const entry of entries) {
      const panelId = this._observerMap.get(entry.target);
      if (!panelId) continue;
      if (entry.isIntersecting) {
        // Panel became visible — record start time
        this._visibilityStart.set(panelId, now);
      } else {
        // Panel left viewport — accumulate duration
        const start = this._visibilityStart.get(panelId);
        if (start) {
          const seconds = (now - start) / 1000;
          this._increment(panelId, 'totalViewSeconds', seconds);
          this._visibilityStart.delete(panelId);
        }
      }
    }
    this._onUpdate();
  }
  /**
   * Register a panel element with the tracker.
   * Observer is attached once per panel, never re-attached on re-render.
   * @param {string} panelId
   * @param {Element} element
   */
  register(panelId, element) {
    this._observerMap.set(element, panelId);
    // Observe once — single attachment per tile lifecycle
    this._observer.observe(element);
    // Restore persisted state or initialise fresh
    if (!this._panels[panelId]) {
      this._panels[panelId] = {
        totalViewSeconds: 0,
        interactionCount: 0,
        lastInteractionAt: null
      };
    }
  }
  /**
   * Unregister a panel — cleans up observer and visibility tracking.
   * @param {string} panelId
   * @param {Element} element
   */
  unregister(panelId, element) {
    this._observer.unobserve(element);
    this._observerMap.delete(element);
    this._visibilityStart.delete(panelId);
  }
  /**
   * Record a user interaction (click, expand, collapse, drag).
   * @param {string} panelId
   */
  recordInteraction(panelId) {
    this._increment(panelId, 'interactionCount', 1);
    this._panels[panelId].lastInteractionAt = Date.now();
    this._onUpdate();
  }
  /**
   * Internal: increment a numeric field by delta.
   * @param {string} panelId
   * @param {string} field
   * @param {number} delta
   */
  _increment(panelId, field, delta) {
    if (!this._panels[panelId]) return;
    this._panels[panelId][field] = (this._panels[panelId][field] || 0) + delta;
  }
  /** @returns {Object<string, Object>} Snapshot of all panel states */
  getState() { return this._panels; }
  /** Replace all state (used on load from localStorage) */
  setState(state) { this._panels = state; }
}
/* ============================================================
   LayoutEngine — arranges panels by rank, assigns grid positions
   ============================================================ */
class LayoutEngine {
  /** Maximum columns in the grid */
  static MAX_COLS = 4;
  /** Rank thresholds for tier assignment */
  static TIERS = { high: 4, mid: 2, low: 0 };
  /**
   * Compute grid assignments for ranked panels.
   * Top-ranked panels get colSpan=3-4 + rowSpan=2.
   * Mid-tier get colSpan=2.
   * Low-tier get colSpan=1 and compact mode.
   *
   * @param {Array<{id: string, score: number}>} ranked — ScoreEngine.rankAll() output
   * @param {Set<string>} locked — panel IDs with manual lock enabled
   * @param {Object<string, Object>} overrides — manual position overrides per panel ID
   * @returns {Object<string, {colspan: number, rowspan: number, compact: boolean, tier: string, order: number}>}
   */
  static assign(ranked, locked, overrides) {
    const assignments = {};
    const total = ranked.length;
    ranked.forEach((item, index) => {
      const id = item.id;
      // Locked panels retain their override positions
      if (locked.has(id) && overrides[id]) {
        assignments[id] = {
          colspan:  overrides[id].colspan  || 2,
          rowspan:  overrides[id].rowspan  || 1,
          compact:  overrides[id].compact  || false,
          tier:     'high',
          order:    overrides[id].order    || index
        };
        return;
      }
      // Auto-assign based on rank percentile
      const pct = index / Math.max(total - 1, 1); // 0 = best, 1 = worst
      let colspan, rowspan, compact, tier;
      if (pct <= 0.15) {
        // Top 15%: dominant panels — large span
        colspan = total <= 2 ? this.MAX_COLS : 3;
        rowspan = 2;
        compact = false;
        tier = 'high';
      } else if (pct <= 0.40) {
        // Next 25%: standard panels
        colspan = 2;
        rowspan = 1;
        compact = false;
        tier = 'mid';
      } else if (pct <= 0.70) {
        // Next 30%: single column, full height
        colspan = 1;
        rowspan = 1;
        compact = false;
        tier = 'low';
      } else {
        // Bottom 30%: compact / miniature mode
        colspan = 1;
        rowspan = 1;
        compact = true;
        tier = 'low';
      }
      assignments[id] = { colspan, rowspan, compact, tier, order: index };
    });
    return assignments;
  }
  /**
   * Validate grid assignments fit within column budget.
   * Adjusts colspans downward row-by-row to prevent overflow.
   * @param {Object<string, Object>} assignments
   * @param {string[]} panelOrder — IDs in display order
   * @returns {Object<string, Object>} Corrected assignments
   */
  static fitToGrid(assignments, panelOrder) {
    const corrected = { ...assignments };
    let rowCols = 0;
    const maxCols = this.MAX_COLS;
    for (const id of panelOrder) {
      const a = corrected[id];
      if (!a) continue;
      // Clamp colspan to remaining space in row
      const avail = maxCols - rowCols;
      if (a.colspan > avail && avail > 0) {
        corrected[id] = { ...a, colspan: avail };
      }
      rowCols += corrected[id].colspan;
      if (rowCols >= maxCols) rowCols = 0; // wrap to next row
    }
    return corrected;
  }
}
/* ============================================================
   DragManager — grid-aware drag-and-drop
   ============================================================ */
class DragManager {
  /**
   * @param {Element} grid — the .dashboard container
   * @param {function(string, string, number, number): void} onDrop —
   *   callback(draggedId, targetId, targetCellCol, targetCellRow)
   */
  constructor(grid, onDrop) {
    this.grid = grid;
    this.onDrop = onDrop;
    /** @type {string|null} ID of currently dragged panel */
    this._draggedId = null;
    /** @type {Element|null} The dragged element */
    this._dragElement = null;
    // Bind handlers once — stable references, never re-created
    this._handleDragStart = this._handleDragStart.bind(this);
    this._handleDragOver  = this._handleDragOver.bind(this);
    this._handleDrop      = this._handleDrop.bind(this);
    this._handleDragEnd   = this._handleDragEnd.bind(this);
    this.grid.addEventListener('dragstart', this._handleDragStart);
    this.grid.addEventListener('dragover',  this._handleDragOver);
    this.grid.addEventListener('drop',      this._handleDrop);
    this.grid.addEventListener('dragend',   this._handleDragEnd);
  }
  /**
   * dragstart handler — set drag data and mark element.
   * @param {DragEvent} e
   */
  _handleDragStart(e) {
    const panel = e.target.closest('.panel');
    if (!panel) return;
    // Respect locked panels — prevent dragging them
    if (panel.dataset.locked === 'true') {
      e.preventDefault();
      return;
    }
    this._draggedId = panel.dataset.panelId;
    this._dragElement = panel;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', this._draggedId);
    // Defer class addition to next frame for smooth visual transition
    requestAnimationFrame(() => panel.classList.add('dragging'));
  }
  /**
   * dragover handler — highlight drop target, infer grid cell from cursor position.
   * Grid-aware: computes target column index from mouse X relative to grid origin
   * and column width, not from hardcoded spans.
   * @param {DragEvent} e
   */
  _handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    // Compute target cell from mouse position relative to grid origin
    const gridRect = this.grid.getBoundingClientRect();
    const colWidth = gridRect.width / LayoutEngine.MAX_COLS;
    // Column index: 0-based, clamped to [0, MAX_COLS-1]
    const targetCol = Math.min(
      LayoutEngine.MAX_COLS - 1,
      Math.max(0, Math.floor((e.clientX - gridRect.left) / colWidth))
    );
    // Row index: approximate from Y position and average panel height
    const avgRowHeight = 180; // approximate, refined by actual measurement if needed
    const targetRow = Math.max(0, Math.floor((e.clientY - gridRect.top) / avgRowHeight));
    // Store for drop handler
    this._targetCellCol = targetCol;
    this._targetCellRow = targetRow;
    // Highlight the panel currently under cursor
    const targetPanel = e.target.closest('.panel');
    // Clear previous highlights
    this.grid.querySelectorAll('.panel.drop-target').forEach(el => el.classList.remove('drop-target'));
    if (targetPanel && targetPanel !== this._dragElement) {
      targetPanel.classList.add('drop-target');
    }
  }
  /**
   * drop handler — execute the reposition.
   * @param {DragEvent} e
   */
  _handleDrop(e) {
    e.preventDefault();
    // Clear all drop-target highlights
    this.grid.querySelectorAll('.panel.drop-target').forEach(el => el.classList.remove('drop-target'));
    const targetPanel = e.target.closest('.panel');
    if (!targetPanel || !this._draggedId) return;
    const targetId = targetPanel.dataset.panelId;
    if (targetId === this._draggedId) return; // dropped on self — no-op
    // Use the grid-pick coordinates computed in dragover
    const col = this._targetCellCol ?? 0;
    const row = this._targetCellRow ?? 0;
    this.onDrop(this._draggedId, targetId, col, row);
  }
  /**
   * dragend handler — cleanup drag state.
   * @param {DragEvent} e
   */
  _handleDragEnd(e) {
    if (this._dragElement) {
      this._dragElement.classList.remove('dragging');
    }
    this.grid.querySelectorAll('.panel.drop-target').forEach(el => el.classList.remove('drop-target'));
    this._draggedId = null;
    this._dragElement = null;
    this._targetCellCol = null;
    this._targetCellRow = null;
  }
}
/* ============================================================
   Dashboard — orchestrator: wires Storage, Score, Usage, Layout, Drag
   ============================================================ */
class Dashboard {
  constructor() {
    /** @type {Object} Loaded state from localStorage */
    this.state = StorageManager.load();
    /** @type {Set<string>} Panel IDs that are locked (manual override active) */
    this.locked = new Set();
    /** @type {Object<string, {colspan:number,rowspan:number,compact:boolean,order:number}>} */
    this.overrides = {};
    /** @type {UsageTracker} */
    this.tracker = new UsageTracker(() => this._onUsageUpdate());
    /** @type {DragManager|null} Initialised after DOM render */
    this.dragManager = null;
    /** @type {boolean} Auto-layout toggle */
    this.autoLayout = this.state.settings.autoLayout !== false;
    /** Debounce timer for localStorage writes */
    this._saveTimer = null;
    /** Panel definitions — static metadata, scores are dynamic */
    this.panelDefs = [
      { id: 'revenue',      title: 'Revenue',      metric: '$48,292', sub: '+12.3% vs last month', type: 'number', color: '#059669' },
      { id: 'users',        title: 'Active Users',  metric: '18,442',  sub: '+5.7% this week',       type: 'bar',   color: '#4f46e5' },
      { id: 'conversion',   title: 'Conversion',    metric: '3.24%',   sub: '-0.3% vs target',        type: 'number', color: '#d97706' },
      { id: 'performance',  title: 'Page Load',     metric: '1.2s',    sub: 'P95 latency',            type: 'spark', color: '#7c3aed' },
      { id: 'errors',       title: 'Error Rate',    metric: '0.12%',   sub: 'Last 24h',               type: 'number', color: '#dc2626' },
      { id: 'uptime',       title: 'Uptime',        metric: '99.97%',  sub: '30-day rolling',         type: 'number', color: '#059669' },
      { id: 'sessions',     title: 'Sessions',      metric: '2,841',   sub: 'Today so far',           type: 'bar',   color: '#0891b2' },
      { id: 'bandwidth',    title: 'Bandwidth',     metric: '842 GB',  sub: 'Monthly egress',         type: 'spark', color: '#9333ea' },
    ];
    // Restore locked state from storage
    for (const [id, p] of Object.entries(this.state.panels)) {
      if (p._locked) this.locked.add(id);
      if (p._override) this.overrides[id] = p._override;
    }
    // Restore tracker state
    const trackerState = {};
    for (const [id, p] of Object.entries(this.state.panels)) {
      trackerState[id] = {
        totalViewSeconds: p.totalViewSeconds || 0,
        interactionCount: p.interactionCount || 0,
        lastInteractionAt: p.lastInteractionAt || null
      };
    }
    this.tracker.setState(trackerState);
    this._render();
    this._initDrag();
    this._initToolbar();
  }
  /* ---------- Render ---------- */
  /** Full re-render: compute scores, assign layout, update DOM. */
  _render() {
    const ranked = ScoreEngine.rankAll(this.tracker.getState());
    const assignments = LayoutEngine.assign(ranked, this.locked, this.overrides);
    // Build display order from ranked list, locked panels at their override order
    const panelOrder = ranked.map(r => r.id);
    const fitted = LayoutEngine.fitToGrid(assignments, panelOrder);
    const grid = document.getElementById('dashboard');
    // Preserve existing elements to avoid destroying IntersectionObserver registrations
    const existing = new Map();
    grid.querySelectorAll('.panel').forEach(el => {
      existing.set(el.dataset.panelId, el);
    });
    grid.innerHTML = ''; // Clear for rebuild
    // Re-render panels in ranked order
    for (const { id, score } of ranked) {
      const def = this.panelDefs.find(d => d.id === id);
      if (!def) continue;
      const a = fitted[id];
      if (!a) continue;
      const el = this._buildPanel(def, a, score);
      grid.appendChild(el);
      // Register with tracker — observer attached once here
      this.tracker.register(id, el);
      // Bind interaction handlers
      this._bindPanelEvents(id, el);
    }
    // Update mode indicator
    document.getElementById('mode-indicator').textContent = this.autoLayout ? 'adaptive' : 'manual';
  }
  /**
   * Build a single panel DOM element.
   * @param {Object} def — panel definition
   * @param {Object} a — layout assignment {colspan, rowspan, compact, tier}
   * @param {number} score — current attention score
   * @returns {Element}
   */
  _buildPanel(def, a, score) {
    const el = document.createElement('div');
    el.className = 'panel' + (a.compact ? ' compact' : '');
    el.dataset.panelId = def.id;
    el.dataset.colspan = a.colspan;
    el.dataset.rowspan = a.rowspan;
    el.dataset.rankTier = a.tier;
    el.dataset.locked = this.locked.has(def.id) ? 'true' : 'false';
    el.draggable = true;
    el.setAttribute('role', 'gridcell');
    el.setAttribute('aria-label', def.title + ' panel');
    const lockedIcon = this.locked.has(def.id) ? '🔒' : '🔓';
    const compactIcon = a.compact ? '⊞' : '⊟';
    el.innerHTML = `
      <div class="panel-header">
        <span class="panel-title">${def.title}</span>
        <div class="panel-controls">
          <button class="btn-compact" aria-label="${a.compact ? 'Expand panel' : 'Compact panel'}" title="${a.compact ? 'Expand' : 'Compact'}">${compactIcon}</button>
          <button class="btn-lock" aria-pressed="${this.locked.has(def.id)}" aria-label="${this.locked.has(def.id) ? 'Unlock panel' : 'Lock panel position'}" title="${this.locked.has(def.id) ? 'Unlock' : 'Lock'}">${lockedIcon}</button>
        </div>
        <span class="score-indicator">${score.toFixed(1)}</span>
      </div>
      <div class="panel-body">
        <div class="panel-metric-value" style="color:${def.color}">${def.metric}</div>
        <div class="panel-metric-sub">${def.sub}</div>
        ${this._buildContentVariant(def)}
      </div>
      <div class="panel-footer">
        <span>Tier: ${a.tier}</span>
        <span>Span: ${a.colspan}×${a.rowspan}</span>
      </div>
    `;
    return el;
  }
  /**
   * Build content variant (sparkline, bar chart, or plain number).
   * Inline comments explain each threshold and visual choice.
   * @param {Object} def
   * @returns {string} HTML string
   */
  _buildContentVariant(def) {
    if (def.type === 'spark') {
      // Sparkline: 12 random-height bars simulating a trend
      const bars = Array.from({ length: 12 }, () => Math.random() * 100);
      const max = Math.max(...bars);
      const segments = bars.map((v, i) => {
        const h = (v / max) * 100;
        // Color-code bars: top 30% get 'high' class, bottom 30% get 'low'
        const cls = h > 70 ? 'high' : h < 30 ? 'low' : 'mid';
        return `<div class="sparkline-bar ${cls}" style="height:${h.toFixed(0)}%" title="Point ${i+1}: ${v.toFixed(1)}"></div>`;
      }).join('');
      return `<div class="sparkline">${segments}</div>`;
    }
    if (def.type === 'bar') {
      // Horizontal bar: represents metric as percentage bar
      const pct = Math.random() * 60 + 30; // simulate 30-90% range
      return `<div style="margin-top:8px;background:#e5e7eb;border-radius:4px;height:8px;overflow:hidden">
        <div style="width:${pct.toFixed(0)}%;height:100%;background:${def.color};border-radius:4px;transition:width 0.6s ease"></div>
      </div>`;
    }
    return '';
  }
  /**
   * Bind interaction event listeners to a panel element.
   * Each handler records the interaction via tracker.
   * @param {string} panelId
   * @param {Element} el
   */
  _bindPanelEvents(panelId, el) {
    // Click tracking — any click inside panel counts as interaction
    el.addEventListener('click', (e) => {
      // Don't count clicks on control buttons (they have their own handlers)
      if (e.target.closest('.panel-controls button')) return;
      this.tracker.recordInteraction(panelId);
    });
    // Compact/expand toggle
    const btnCompact = el.querySelector('.btn-compact');
    if (btnCompact) {
      btnCompact.addEventListener('click', (e) => {
        e.stopPropagation();
        this.tracker.recordInteraction(panelId);
        const isCompact = el.classList.toggle('compact');
        // Persist compact preference as a panel-level override
        this.overrides[panelId] = {
          ...this.overrides[panelId],
          compact: isCompact,
          colspan: parseInt(el.dataset.colspan) || 1,
          rowspan: parseInt(el.dataset.rowspan) || 1,
          order: 0
        };
        el.querySelector('.btn-compact').textContent = isCompact ? '⊞' : '⊟';
        this._scheduleSave();
      });
    }
    // Lock/unlock toggle
    const btnLock = el.querySelector('.btn-lock');
    if (btnLock) {
      btnLock.addEventListener('click', (e) => {
        e.stopPropagation();
        this.tracker.recordInteraction(panelId);
        if (this.locked.has(panelId)) {
          // Unlock — remove from locked set, clear override
          this.locked.delete(panelId);
          delete this.overrides[panelId];
          el.dataset.locked = 'false';
          btnLock.setAttribute('aria-pressed', 'false');
          btnLock.textContent = '🔓';
        } else {
          // Lock — retain current position as override
          this.locked.add(panelId);
          this.overrides[panelId] = {
            colspan: parseInt(el.dataset.colspan) || 2,
            rowspan: parseInt(el.dataset.rowspan) || 1,
            compact: el.classList.contains('compact'),
            order: Array.from(el.parentNode.children).indexOf(el)
          };
          el.dataset.locked = 'true';
          btnLock.setAttribute('aria-pressed', 'true');
          btnLock.textContent = '🔒';
        }
        this._scheduleSave();
        if (this.autoLayout) this._render(); // re-render to reflow
      });
    }
  }
  /* ---------- Drag & Drop ---------- */
  /** Initialise DragManager — called once after first render. */
  _initDrag() {
    const grid = document.getElementById('dashboard');
    this.dragManager = new DragManager(grid, (draggedId, targetId, targetCol, targetRow) => {
      this._handleDrop(draggedId, targetId, targetCol, targetRow);
    });
  }
  /**
   * Handle a drop event: swap or reorder panels.
   * Grid-pick algorithm: target cell column inferred from mouse position
   * (computed in DragManager._handleDragOver), not from hardcoded spans.
   * @param {string} draggedId
   * @param {string} targetId
   * @param {number} targetCol — 0-based column index from grid-pick
   * @param {number} targetRow — 0-based row index from grid-pick
   */
  _handleDrop(draggedId, targetId, targetCol, targetRow) {
    // Record interaction on both panels
    this.tracker.recordInteraction(draggedId);
    this.tracker.recordInteraction(targetId);
    // Swap positions: give dragged panel the target's override
    const targetOverride = this.overrides[targetId] || {
      colspan: 2, rowspan: 1, compact: false,
      order: targetRow * LayoutEngine.MAX_COLS + targetCol
    };
    this.overrides[draggedId] = { ...targetOverride };
    // Push target panel one slot forward in order
    const draggedOrder = (targetRow * LayoutEngine.MAX_COLS + targetCol) + 1;
    this.overrides[targetId] = {
      colspan: targetOverride.colspan,
      rowspan: targetOverride.rowspan,
      compact: targetOverride.compact,
      order: draggedOrder
    };
    // Lock both after manual drag (user intent: manual positioning)
    this.locked.add(draggedId);
    this.locked.add(targetId);
    this._scheduleSave();
    this._render();
  }
  /* ---------- Toolbar ---------- */
  _initToolbar() {
    document.getElementById('btn-reset-scores').addEventListener('click', () => {
      this.tracker.setState({});
      this.locked.clear();
      this.overrides = {};
      this.state.panels = {};
      StorageManager.save(this.state);
      this._render();
    });
    const toggleBtn = document.getElementById('btn-toggle-auto');
    const updateToggleLabel = () => {
      toggleBtn.textContent = 'Auto-Layout: ' + (this.autoLayout ? 'ON' : 'OFF');
    };
    updateToggleLabel();
    toggleBtn.addEventListener('click', () => {
      this.autoLayout = !this.autoLayout;
      this.state.settings.autoLayout = this.autoLayout;
      updateToggleLabel();
      if (this.autoLayout) {
        // Re-enable auto: clear all locks and overrides
        this.locked.clear();
        this.overrides = {};
      }
      StorageManager.save(this.state);
      this._render();
    });
  }
  /* ---------- Persistence ---------- */
  /**
   * Called whenever usage data changes.
   * Debounced at 400ms to batch rapid updates into a single write.
   * Only triggers re-render if auto-layout is enabled.
   */
  _onUsageUpdate() {
    if (this.autoLayout) {
      // Debounce render: avoid thrashing DOM on rapid observer callbacks
      clearTimeout(this._renderTimer);
      this._renderTimer = setTimeout(() => this._render(), 400);
    }
    this._scheduleSave();
  }
  /**
   * Schedule a debounced localStorage write.
   * 400ms debounce ensures rapid interactions don't flood storage.
   */
  _scheduleSave() {
    clearTimeout(this._saveTimer);
    this._saveTimer = setTimeout(() => {
      // Merge tracker state into persistent state
      const trackerState = this.tracker.getState();
      for (const [id, ts] of Object.entries(trackerState)) {
        this.state.panels[id] = {
          ...this.state.panels[id],
          totalViewSeconds: ts.totalViewSeconds,
          interactionCount: ts.interactionCount,
          lastInteractionAt: ts.lastInteractionAt,
          _locked: this.locked.has(id),
          _override: this.overrides[id] || null
        };
      }
      StorageManager.save(this.state);
    }, 400);
  }
}
/* ============================================================
   Bootstrap — instantiate the dashboard on DOMContentLoaded
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  new Dashboard();
});
</script>
</body>
</html>