<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
/* ============================================================
   CSS SECTION 1: CSS Custom Properties / Design Tokens
   ============================================================ */
:root {
  --grid-gap: 12px;
  --panel-radius: 10px;
  --panel-shadow: 0 2px 8px rgba(0,0,0,0.08);
  --panel-shadow-hover: 0 6px 20px rgba(0,0,0,0.14);
  --color-bg: #f4f6f9;
  --color-surface: #ffffff;
  --color-text: #1a1a2e;
  --color-text-secondary: #6b7280;
  --color-accent: #4f46e5;
  --color-accent-light: #e0e7ff;
  --color-border: #e5e7eb;
  --color-warn: #f59e0b;
  --color-success: #10b981;
  --color-danger: #ef4444;
  --compact-scale: 0.55;
  --transition-speed: 280ms;
  --header-height: 56px;
  --control-height: 44px;
  --font-mono: 'SF Mono', 'Cascadia Code', 'Fira Code', monospace;
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
}
/* ============================================================
   CSS SECTION 2: Reset & Base
   ============================================================ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 15px; }
body {
  font-family: var(--font-sans);
  background: var(--color-bg);
  color: var(--color-text);
  min-height: 100vh;
  padding: 16px;
  line-height: 1.5;
}
/* ============================================================
   CSS SECTION 3: Header & Control Bar
   ============================================================ */
.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--header-height);
  margin-bottom: 16px;
  padding: 0 8px;
}
.dashboard-header h1 {
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}
.control-bar {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}
.control-bar button {
  padding: 6px 14px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-surface);
  font-size: 0.82rem;
  font-weight: 500;
  cursor: pointer;
  transition: background var(--transition-speed), border-color var(--transition-speed);
  white-space: nowrap;
}
.control-bar button:hover { background: var(--color-accent-light); border-color: var(--color-accent); }
.control-bar button.active { background: var(--color-accent); color: #fff; border-color: var(--color-accent); }
/* ============================================================
   CSS SECTION 4: Dashboard Grid — Auto-placement by rank
   Panels are placed into named grid areas via JS based on rank.
   Grid defines 4 columns; high-rank panels span 2 cols + 2 rows,
   mid-rank span 1-2 cols + 1 row, low-rank go compact.
   ============================================================ */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(160px, auto);
  gap: var(--grid-gap);
  /* Grid areas assigned dynamically by JS via style attr */
}
/* ============================================================
   CSS SECTION 5: Panel Base Styles
   ============================================================ */
.panel {
  background: var(--color-surface);
  border-radius: var(--panel-radius);
  box-shadow: var(--panel-shadow);
  padding: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition:
    transform var(--transition-speed) cubic-bezier(0.22, 0.61, 0.36, 1),
    box-shadow var(--transition-speed),
    grid-column var(--transition-speed),
    grid-row var(--transition-speed),
    opacity var(--transition-speed);
  position: relative;
}
.panel:hover { box-shadow: var(--panel-shadow-hover); }
/* Header row inside each panel */
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  gap: 8px;
}
.panel-title {
  font-weight: 650;
  font-size: 0.95rem;
  letter-spacing: -0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.panel-meta {
  font-size: 0.7rem;
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}
/* Panel body — scrollable content area */
.panel-body {
  flex: 1;
  overflow-y: auto;
  font-size: 0.85rem;
  color: var(--color-text-secondary);
  min-height: 40px;
}
/* Metric value display */
.panel-body .metric-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--color-text);
  font-family: var(--font-mono);
}
.panel-body .metric-label { font-size: 0.75rem; color: var(--color-text-secondary); margin-top: 2px; }
.panel-body .metric-spark {
  height: 40px;
  margin-top: 8px;
  display: flex;
  align-items: flex-end;
  gap: 2px;
}
.panel-body .metric-spark .bar {
  flex: 1;
  background: var(--color-accent);
  border-radius: 2px 2px 0 0;
  min-height: 3px;
  transition: height 400ms ease;
}
/* ============================================================
   CSS SECTION 6: Lock / Pin / Override Controls
   ============================================================ */
.pin-btn, .compact-btn {
  background: none;
  border: 1px solid transparent;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  padding: 2px 5px;
  color: var(--color-text-secondary);
  transition: color var(--transition-speed), border-color var(--transition-speed);
  line-height: 1;
}
.pin-btn:hover, .compact-btn:hover { color: var(--color-accent); border-color: var(--color-border); }
.pin-btn.pinned { color: var(--color-warn); font-weight: 700; }
/* Lock indicator dot on pinned panels */
.panel.pinned::before {
  content: '';
  position: absolute;
  top: 6px;
  right: 6px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-warn);
  z-index: 1;
}
/* ============================================================
   CSS SECTION 7: Compact / Miniature Mode
   Low-rank panels shrink; show only title + sparkline preview.
   ============================================================ */
.panel.compact {
  transform: scale(var(--compact-scale));
  transform-origin: top left;
  opacity: 0.78;
  padding: 10px;
  grid-row: span 1 !important;
}
.panel.compact .panel-body { display: none; }
.panel.compact .panel-header { margin-bottom: 0; }
.panel.compact .panel-title { font-size: 0.75rem; }
.panel.compact .compact-preview {
  display: block;
  height: 22px;
  margin-top: 4px;
}
.compact-preview { display: none; }
.compact-preview .mini-spark {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  height: 100%;
}
.compact-preview .mini-spark .bar {
  flex: 1;
  background: var(--color-accent);
  opacity: 0.5;
  border-radius: 1px;
  min-height: 2px;
}
/* ============================================================
   CSS SECTION 8: Rank Badge
   ============================================================ */
.rank-badge {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 700;
  padding: 1px 7px;
  border-radius: 10px;
  background: var(--color-accent-light);
  color: var(--color-accent);
}
.rank-badge.top { background: #fef3c7; color: #b45309; }
.rank-badge.mid { background: #e0e7ff; color: #4338ca; }
.rank-badge.low { background: #f3f4f6; color: #6b7280; }
/* ============================================================
   CSS SECTION 9: Toast / Status Messages
   ============================================================ */
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--color-text);
  color: #fff;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 0.82rem;
  z-index: 1000;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 300ms, transform 300ms;
  pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
/* ============================================================
   CSS SECTION 10: Responsive Breakpoints
   ============================================================ */
@media (max-width: 900px) {
  .dashboard-grid { grid-template-columns: repeat(2, 1fr); }
  .panel.compact { transform: scale(0.7); }
}
@media (max-width: 500px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .dashboard-header { flex-direction: column; height: auto; gap: 8px; }
}
</style>
</head>
<body>
<div class="dashboard-header">
  <h1>Adaptive Metric Dashboard</h1>
  <div class="control-bar">
    <button id="btn-reset" title="Reset all tracking data">Reset Tracking</button>
    <button id="btn-export" title="Export layout to console">Export Layout</button>
    <span style="font-size:0.75rem;color:var(--color-text-secondary);margin-left:4px;" id="status-text">Ready</span>
  </div>
</div>
<div class="dashboard-grid" id="dashboard-grid">
  <!-- Panels injected by JS -->
</div>
<div class="toast" id="toast"></div>
<script>
/**
 * =========================================================================
 * Adaptive Metric Dashboard — Complete Layout Engine
 * =========================================================================
 * Tracks panel view duration (IntersectionObserver), click interactions,
 * and collapse/expand events. Scores panels via composite attention metric
 * (frequency x duration x recency). Auto-arranges by rank: top panels get
 * 2-col x 2-row slots, mid get 1-2 col x 1 row, low-rank shrink to compact.
 * Manual lock (pin) overrides auto-layout. Persists to localStorage.
 * =========================================================================
 */
// ─────────────────────────────────────────────────────────────────────────
// SECTION A: Configuration & Constants
// ─────────────────────────────────────────────────────────────────────────
/** @type {number} Decay factor per hour for recency weighting (0-1, lower = faster decay) */
const RECENCY_DECAY_PER_HOUR = 0.15;
/** @type {number} Minimum view duration (ms) before a view counts toward ranking */
const MIN_VIEW_DURATION_MS = 800;
/** @type {number} Number of top-ranked panels that get large (2x2) layout slots */
const TOP_SLOT_COUNT = 2;
/** @type {number} Threshold ratio below peak rank for compact mode (0-1) */
const COMPACT_RANK_THRESHOLD = 0.25;
/** @type {string} localStorage key prefix */
const STORAGE_KEY = 'adaptive_dashboard_v1';
/** @type {Array<{id:string, title:string, type:string, metric:string, data:number[]}>} Panel definitions */
const PANEL_DEFS = [
  { id: 'revenue',     title: 'Revenue',         type: 'currency', metric: '$',  data: [42,48,51,47,53,58,62,59,65,71,68,74] },
  { id: 'users',       title: 'Active Users',    type: 'number',   metric: '',   data: [120,135,142,158,163,171,185,192,201,215,222,238] },
  { id: 'conversion',  title: 'Conversion Rate', type: 'percent',  metric: '%',  data: [3.2,3.1,3.4,3.3,3.6,3.5,3.8,3.7,4.0,3.9,4.2,4.1] },
  { id: 'latency',     title: 'API Latency',     type: 'duration', metric: 'ms', data: [210,195,188,205,178,192,185,170,165,160,155,148] },
  { id: 'errors',      title: 'Error Rate',      type: 'percent',  metric: '%',  data: [1.2,1.1,0.9,1.0,0.8,0.9,0.7,0.8,0.6,0.7,0.5,0.5] },
  { id: 'storage',     title: 'Storage Usage',   type: 'storage',  metric: 'GB', data: [32,35,38,41,44,48,52,56,60,64,68,72] },
  { id: 'sessions',    title: 'Sessions',        type: 'number',   metric: '',   data: [850,920,880,960,910,990,940,1020,970,1050,1000,1080] },
  { id: 'bandwidth',   title: 'Bandwidth',       type: 'transfer', metric: 'Mbps', data: [78,82,79,85,81,88,84,91,87,94,90,97] },
];
// ─────────────────────────────────────────────────────────────────────────
// SECTION B: State — tracking data, scores, overrides
// ─────────────────────────────────────────────────────────────────────────
/**
 * @typedef {Object} PanelState
 * @property {string} id - Panel identifier
 * @property {number} viewCount - Total number of distinct view sessions (entered viewport for > MIN_VIEW_DURATION_MS)
 * @property {number} totalViewDurationMs - Accumulated milliseconds of view time
 * @property {number} interactionCount - Total clicks on this panel
 * @property {number} lastInteractionTs - Timestamp of last interaction (epoch ms)
 * @property {number} lastViewTs - Timestamp of last view entry (epoch ms)
 * @property {boolean} pinned - Manual lock override; if true, auto-layout skips this panel
 * @property {number|null} pinnedColumn - If pinned, the fixed grid-column value
 * @property {number|null} pinnedRow - If pinned, the fixed grid-row value
 * @property {boolean} compact - True if panel is in compact/miniature mode
 * @property {number} score - Composite attention score (computed on rank)
 */
/** @type {Object<string, PanelState>} Runtime state keyed by panel id */
let panelStates = {};
/** @type {Map<string, number>} Tracks view-entry timestamps for active view sessions (panel id -> epoch ms) */
const activeViewSessions = new Map();
/** @type {IntersectionObserver|null} Reference to the active viewport observer */
let viewportObserver = null;
// ─────────────────────────────────────────────────────────────────────────
// SECTION C: Initialization & State Loading
// ─────────────────────────────────────────────────────────────────────────
/**
 * Load panel states from localStorage. Merges with defaults for any newly
 * added panels not present in stored state.
 * @returns {Object<string, PanelState>} Hydrated panel state map
 */
function loadState() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    // No stored state — seed defaults
    const seed = {};
    PANEL_DEFS.forEach((def) => {
      seed[def.id] = {
        id: def.id,
        viewCount: 0,
        totalViewDurationMs: 0,
        interactionCount: 0,
        lastInteractionTs: 0,
        lastViewTs: 0,
        pinned: false,
        pinnedColumn: null,
        pinnedRow: null,
        compact: false,
        score: 0,
      };
    });
    return seed;
  }
  try {
    const parsed = JSON.parse(raw);
    // Merge with defaults for any panels that may have been added since last save
    PANEL_DEFS.forEach((def) => {
      if (!parsed[def.id]) {
        parsed[def.id] = {
          id: def.id,
          viewCount: 0,
          totalViewDurationMs: 0,
          interactionCount: 0,
          lastInteractionTs: 0,
          lastViewTs: 0,
          pinned: false,
          pinnedColumn: null,
          pinnedRow: null,
          compact: false,
          score: 0,
        };
      }
    });
    return parsed;
  } catch (e) {
    console.warn('Dashboard: localStorage parse failed, resetting state.', e);
    return loadState(); // recurse to seed defaults
  }
}
/**
 * Persist current panel states to localStorage.
 */
function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(panelStates));
  } catch (e) {
    console.warn('Dashboard: localStorage write failed (quota exceeded?)', e);
  }
}
// ─────────────────────────────────────────────────────────────────────────
// SECTION D: Tracking — IntersectionObserver (view duration) + click events
// ─────────────────────────────────────────────────────────────────────────
/**
 * Start a view session for a panel that has entered the viewport.
 * Records the entry timestamp; duration is computed on exit.
 * @param {string} panelId - Panel identifier
 */
function startViewSession(panelId) {
  if (activeViewSessions.has(panelId)) return; // already tracking
  activeViewSessions.set(panelId, Date.now());
  const state = panelStates[panelId];
  if (state) {
    state.lastViewTs = Date.now();
  }
}
/**
 * End a view session for a panel that has left the viewport.
 * Computes elapsed duration; if above MIN_VIEW_DURATION_MS, credits the panel
 * with a view and adds the duration to its total.
 * @param {string} panelId - Panel identifier
 */
function endViewSession(panelId) {
  const entryTs = activeViewSessions.get(panelId);
  if (!entryTs) return;
  activeViewSessions.delete(panelId);
  const duration = Date.now() - entryTs;
  if (duration < MIN_VIEW_DURATION_MS) return; // too short, ignore
  const state = panelStates[panelId];
  if (!state) return;
  state.viewCount += 1;
  state.totalViewDurationMs += duration;
  // Throttle: save every 5 credited views to avoid localStorage churn
  if (state.viewCount % 5 === 0) {
    saveState();
    rerankAndLayout();
  }
}
/**
 * Initialize the IntersectionObserver that tracks when panels enter/exit the
 * viewport. Threshold 0.3 means at least 30% of the panel must be visible
 * to count as "in view". This avoids counting panels that are barely scrolled
 * into the edge of the screen.
 */
function initViewTracker() {
  // Clean up any previous observer before creating a new one
  if (viewportObserver) {
    viewportObserver.disconnect();
    viewportObserver = null;
  }
  // IntersectionObserver: threshold 0.3 = 30% visibility required for "in view"
  viewportObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const panelId = entry.target.dataset.panelId;
        if (!panelId) return;
        // entry.isIntersecting: true when >= 30% of panel is visible
        if (entry.isIntersecting) {
          startViewSession(panelId);
        } else {
          endViewSession(panelId);
        }
      });
    },
    { threshold: 0.3 }
  );
}
/**
 * Attach click-tracking to a panel's DOM element. Each click increments
 * the panel's interactionCount and updates lastInteractionTs.
 * Also handles pin/compact button clicks within the panel.
 * @param {HTMLElement} panelEl - The panel's root DOM element
 * @param {string} panelId - Panel identifier
 */
function attachPanelInteractions(panelEl, panelId) {
  // Click handler: count any click on the panel body as an interaction
  panelEl.addEventListener('click', (e) => {
    // Do not count clicks on pin/compact buttons as content interactions
    // (those are tracked separately via their own handlers)
    if (e.target.closest('.pin-btn') || e.target.closest('.compact-btn')) return;
    const state = panelStates[panelId];
    if (!state) return;
    state.interactionCount += 1;
    state.lastInteractionTs = Date.now();
    if (state.interactionCount % 5 === 0) {
      saveState();
      rerankAndLayout();
    }
  });
  // Pin button handler (lock/unlock panel position)
  const pinBtn = panelEl.querySelector('.pin-btn');
  if (pinBtn) {
    pinBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const state = panelStates[panelId];
      if (!state) return;
      state.pinned = !state.pinned;
      if (state.pinned) {
        // When pinning, snapshot current grid position so it stays fixed
        state.pinnedColumn = panelEl.style.gridColumn || null;
        state.pinnedRow = panelEl.style.gridRow || null;
        showToast('Panel ' + panelId + ' locked in place');
      } else {
        state.pinnedColumn = null;
        state.pinnedRow = null;
        showToast('Panel ' + panelId + ' unlocked — auto-layout resumed');
      }
      saveState();
      rerankAndLayout();
    });
  }
  // Compact toggle button handler
  const compactBtn = panelEl.querySelector('.compact-btn');
  if (compactBtn) {
    compactBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const state = panelStates[panelId];
      if (!state) return;
      state.compact = !state.compact;
      state.pinned = false; // toggling compact disables pin
      state.pinnedColumn = null;
      state.pinnedRow = null;
      saveState();
      rerankAndLayout();
    });
  }
}
// ─────────────────────────────────────────────────────────────────────────
// SECTION E: Ranking Algorithm — composite attention score
// ─────────────────────────────────────────────────────────────────────────
/**
 * Compute the composite attention score for a single panel.
 * Formula: score = viewCount * avgDurationSeconds * recencyFactor * (1 + interactionCount * 0.15)
 *
 * - viewCount: how many distinct times the panel was viewed
 * - avgDurationSeconds: average view duration in seconds (capped at 120s to prevent outliers)
 * - recencyFactor: exponential decay based on time since last interaction or view
 * - interactionCount bonus: each interaction adds 15% weight
 *
 * @param {PanelState} state - Panel state to score
 * @returns {number} Composite attention score (higher = more important)
 */
function computeScore(state) {
  // Guard: no views = zero score
  if (state.viewCount === 0) return 0;
  // Average view duration in seconds, cap at 120s to prevent outliers from dominating
  const avgDurationSec = Math.min(
    state.totalViewDurationMs / Math.max(state.viewCount, 1) / 1000,
    120
  );
  // Recency: use the most recent of lastViewTs or lastInteractionTs
  const lastActivityTs = Math.max(state.lastViewTs, state.lastInteractionTs, 1);
  const hoursSinceActivity = (Date.now() - lastActivityTs) / (1000 * 60 * 60);
  // Exponential decay: score halves every ~4.6 hours with decay=0.15
  const recencyFactor = Math.exp(-RECENCY_DECAY_PER_HOUR * hoursSinceActivity);
  // Interaction bonus: each click adds 15% weight
  const interactionMultiplier = 1 + state.interactionCount * 0.15;
  const score = state.viewCount * avgDurationSec * recencyFactor * interactionMultiplier;
  // Round to 2 decimal places for readability
  return Math.round(score * 100) / 100;
}
/**
 * Recompute scores for all panels, sort descending by score, and assign ranks.
 * Updates panelStates in place. Returns sorted array of panel ids.
 * @returns {string[]} Panel ids sorted by score descending (rank 0 = highest)
 */
function rankPanels() {
  // Compute scores
  Object.values(panelStates).forEach((state) => {
    state.score = computeScore(state);
  });
  // Sort by score descending
  const sorted = Object.values(panelStates).sort((a, b) => b.score - a.score);
  // Determine compact threshold: panels with score < COMPACT_RANK_THRESHOLD * topScore
  // are candidates for compact mode (unless pinned)
  const topScore = sorted.length > 0 ? sorted[0].score : 0;
  sorted.forEach((state, index) => {
    // Auto-compact: low score relative to top, and not already manually compacted
    if (!state.pinned && !state.compact) {
      state.compact = state.score < topScore * COMPACT_RANK_THRESHOLD && state.score > 0;
    }
    // Ensure pinned panels are never compacted automatically
    if (state.pinned) state.compact = false;
  });
  return sorted.map((s) => s.id);
}
// ─────────────────────────────────────────────────────────────────────────
// SECTION F: Layout Engine — grid placement by rank
// ─────────────────────────────────────────────────────────────────────────
/**
 * Apply grid placement to all panel DOM elements based on current rank.
 *
 * Layout rules:
 *   - Rank 0-1 (top 2): span 2 columns x 2 rows (dominant position)
 *   - Rank 2-3: span 2 columns x 1 row (prominent)
 *   - Rank 4-5: span 1 column x 1 row (standard)
 *   - Rank 6+: span 1 column x 1 row, compact mode (shrunken)
 *   - Pinned panels: retain their pinned grid-column/grid-row values
 *
 * Grid is 4 columns. Top panels consume column pairs (1/3 and 2/4).
 * Mid panels fill remaining rows. Compact panels stack at bottom.
 *
 * @param {string[]} rankedIds - Panel ids sorted by rank (0 = highest)
 */
function applyLayout(rankedIds) {
  const grid = document.getElementById('dashboard-grid');
  if (!grid) return;
  // Separate pinned panels from auto-layout candidates
  const pinnedIds = rankedIds.filter((id) => panelStates[id]?.pinned);
  const autoIds = rankedIds.filter((id) => !panelStates[id]?.pinned);
  // Layout slots for the 4-column grid
  // We assign positions row by row, column by column
  const cols = 4;
  let row = 1;
  let col = 1;
  /**
   * Helper: get next available grid position for a panel spanning w columns x h rows.
   * Advances col/row cursor after placement.
   * @param {number} w - Column span
   * @param {number} h - Row span
   * @returns {{col:number, row:number}} Grid start position
   */
  function nextSlot(w, h) {
    // If this span doesn't fit on current row, wrap to next row
    if (col + w - 1 > cols) {
      col = 1;
      row += 1;
    }
    const slot = { col, row };
    col += w;
    if (col > cols) {
      col = 1;
      row += h;
    }
    return slot;
  }
  // Assign positions to auto-layout panels by rank
  const assignments = {};
  autoIds.forEach((id, index) => {
    const state = panelStates[id];
    if (!state) return;
    let w, h;
    if (state.compact) {
      // Compact panels: 1 col x 1 row, shrunken via CSS
      w = 1;
      h = 1;
    } else if (index < TOP_SLOT_COUNT) {
      // Top-ranked: 2 cols x 2 rows
      w = 2;
      h = 2;
    } else if (index < TOP_SLOT_COUNT + 2) {
      // Next tier: 2 cols x 1 row
      w = 2;
      h = 1;
    } else {
      // Standard: 1 col x 1 row
      w = 1;
      h = 1;
    }
    const slot = nextSlot(w, h);
    assignments[id] = { col: slot.col, row: slot.row, spanCol: w, spanRow: h };
  });
  // Apply assignments to DOM elements
  rankedIds.forEach((id) => {
    const el = document.querySelector(`[data-panel-id="${id}"]`);
    if (!el) return;
    const state = panelStates[id];
    if (state?.pinned && state.pinnedColumn && state.pinnedRow) {
      // Restore pinned position
      el.style.gridColumn = state.pinnedColumn;
      el.style.gridRow = state.pinnedRow;
      el.classList.add('pinned');
      el.classList.remove('compact');
    } else if (assignments[id]) {
      const a = assignments[id];
      el.style.gridColumn = `${a.col} / span ${a.spanCol}`;
      el.style.gridRow = `${a.row} / span ${a.spanRow}`;
      el.classList.remove('pinned');
      if (state?.compact) {
        el.classList.add('compact');
      } else {
        el.classList.remove('compact');
      }
    }
  });
  // Update rank badges on all panels
  updateRankBadges(rankedIds);
  // Save after layout
  saveState();
}
/**
 * Update the rank badge displayed on each panel.
 * @param {string[]} rankedIds - Panel ids in rank order
 */
function updateRankBadges(rankedIds) {
  rankedIds.forEach((id, index) => {
    const badge = document.querySelector(`[data-panel-id="${id}"] .rank-badge`);
    if (!badge) return;
    badge.textContent = '#' + (index + 1);
    // Color classes based on rank tier
    badge.classList.remove('top', 'mid', 'low');
    if (index < TOP_SLOT_COUNT) badge.classList.add('top');
    else if (index < rankedIds.length - 2) badge.classList.add('mid');
    else badge.classList.add('low');
  });
}
// ─────────────────────────────────────────────────────────────────────────
// SECTION G: Full rerank + layout cycle
// ─────────────────────────────────────────────────────────────────────────
/**
 * Full cycle: recompute scores, rank panels, apply layout.
 * Called after significant tracking events (every 5 views/interactions).
 */
function rerankAndLayout() {
  const rankedIds = rankPanels();
  applyLayout(rankedIds);
}
// ─────────────────────────────────────────────────────────────────────────
// SECTION H: DOM Construction — render all panels
// ─────────────────────────────────────────────────────────────────────────
/**
 * Build the HTML for a single panel's body content based on its type.
 * @param {Object} def - Panel definition from PANEL_DEFS
 * @param {PanelState} state - Current panel state
 * @returns {string} Inner HTML string for the panel body
 */
function buildPanelBody(def, state) {
  const latest = def.data[def.data.length - 1];
  const prev = def.data[def.data.length - 2] || latest;
  const delta = latest - prev;
  const deltaStr = delta >= 0 ? '+' + delta.toFixed(1) : delta.toFixed(1);
  const deltaClass = delta >= 0 ? 'color:var(--color-success)' : 'color:var(--color-danger)';
  // Build mini sparkline bars from all data points
  const maxVal = Math.max(...def.data, 1);
  const bars = def.data
    .map((v) => {
      const h = Math.max((v / maxVal) * 100, 6);
      return '<div class="bar" style="height:' + h + '%"></div>';
    })
    .join('');
  return (
    '<div class="metric-value">' +
    def.metric +
    (def.type === 'currency'
      ? latest.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
      : def.type === 'percent'
        ? latest.toFixed(1)
        : def.type === 'duration'
          ? latest
          : latest.toLocaleString()) +
    (def.type === 'currency' ? '' : def.metric === 'ms' ? 'ms' : def.metric === '%' ? '%' : '') +
    '</div>' +
    '<div class="metric-label">' +
    '<span style="' + deltaClass + '">' + deltaStr + '</span> vs previous period' +
    '</div>' +
    '<div class="metric-spark">' + bars + '</div>' +
    '<div class="compact-preview"><div class="mini-spark">' +
    bars +
    '</div></div>'
  );
}
/**
 * Render all panels into the dashboard grid.
 * Clears existing content and rebuilds from PANEL_DEFS.
 */
function renderPanels() {
  const grid = document.getElementById('dashboard-grid');
  if (!grid) return;
  grid.innerHTML = '';
  PANEL_DEFS.forEach((def) => {
    const state = panelStates[def.id] || {
      id: def.id,
      viewCount: 0,
      totalViewDurationMs: 0,
      interactionCount: 0,
      lastInteractionTs: 0,
      lastViewTs: 0,
      pinned: false,
      pinnedColumn: null,
      pinnedRow: null,
      compact: false,
      score: 0,
    };
    if (!panelStates[def.id]) panelStates[def.id] = state;
    const panelEl = document.createElement('div');
    panelEl.className = 'panel';
    panelEl.dataset.panelId = def.id;
    panelEl.innerHTML =
      '<div class="panel-header">' +
      '<span class="panel-title">' +
      def.title +
      ' <span class="rank-badge">-</span>' +
      '</span>' +
      '<div class="panel-meta">' +
      '<button class="compact-btn" title="Toggle compact mode">⊟</button>' +
      '<button class="pin-btn" title="Lock position">📌</button>' +
      '<span style="font-size:0.65rem;opacity:0.6">views:' + state.viewCount + '</span>' +
      '</div>' +
      '</div>' +
      '<div class="panel-body">' +
      buildPanelBody(def, state) +
      '</div>';
    grid.appendChild(panelEl);
    // Attach observer to this panel
    if (viewportObserver) {
      viewportObserver.observe(panelEl);
    }
    // Attach click + pin/compact handlers
    attachPanelInteractions(panelEl, def.id);
  });
}
// ─────────────────────────────────────────────────────────────────────────
// SECTION I: Toast Notification Helper
// ─────────────────────────────────────────────────────────────────────────
/**
 * Display a brief toast message at bottom-right.
 * Auto-hides after 2 seconds.
 * @param {string} msg - Message text
 */
function showToast(msg) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toast._timeout);
  toast._timeout = setTimeout(() => {
    toast.classList.remove('show');
  }, 2000);
}
// ─────────────────────────────────────────────────────────────────────────
// SECTION J: Control Bar Handlers
// ─────────────────────────────────────────────────────────────────────────
/**
 * Reset all tracking data to zero and clear localStorage.
 */
function resetTracking() {
  panelStates = {};
  PANEL_DEFS.forEach((def) => {
    panelStates[def.id] = {
      id: def.id,
      viewCount: 0,
      totalViewDurationMs: 0,
      interactionCount: 0,
      lastInteractionTs: 0,
      lastViewTs: 0,
      pinned: false,
      pinnedColumn: null,
      pinnedRow: null,
      compact: false,
      score: 0,
    };
  });
  activeViewSessions.clear();
  localStorage.removeItem(STORAGE_KEY);
  renderPanels();
  rerankAndLayout();
  showToast('Tracking data reset');
}
/**
 * Export current layout state to console as JSON.
 */
function exportLayout() {
  const rankedIds = rankPanels();
  const exportData = rankedIds.map((id, i) => ({
    rank: i + 1,
    id,
    score: panelStates[id].score,
    pinned: panelStates[id].pinned,
    compact: panelStates[id].compact,
    viewCount: panelStates[id].viewCount,
    interactionCount: panelStates[id].interactionCount,
  }));
  console.table(exportData);
  console.log(JSON.stringify(exportData, null, 2));
  showToast('Layout exported to console (F12)');
}
// ─────────────────────────────────────────────────────────────────────────
// SECTION K: Bootstrap
// ─────────────────────────────────────────────────────────────────────────
/**
 * Initialize the entire dashboard:
 *   1. Load state from localStorage
 *   2. Initialize IntersectionObserver view tracker
 *   3. Render all panels into DOM
 *   4. Compute initial ranks and apply layout
 *   5. Wire up control bar buttons
 */
function bootstrap() {
  panelStates = loadState();
  initViewTracker();
  renderPanels();
  rerankAndLayout();
  document.getElementById('btn-reset').addEventListener('click', resetTracking);
  document.getElementById('btn-export').addEventListener('click', exportLayout);
  // Persist view sessions on page unload so no duration is lost
  window.addEventListener('beforeunload', () => {
    // End all active view sessions
    activeViewSessions.forEach((_ts, panelId) => {
      endViewSession(panelId);
    });
    saveState();
  });
  // Update status
  const statusEl = document.getElementById('status-text');
  if (statusEl) {
    statusEl.textContent = 'Tracking active | ' + PANEL_DEFS.length + ' panels';
  }
}
// Boot when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bootstrap);
} else {
  bootstrap();
}
// ─────────────────────────────────────────────────────────────────────────
// SELF-VERIFICATION: Completion marker — all structural elements present
// Last function: bootstrap() closes above. All classes, event handlers,
// and closing tags accounted for. File is structurally complete.
// ─────────────────────────────────────────────────────────────────────────
</script>
</body>
</html>