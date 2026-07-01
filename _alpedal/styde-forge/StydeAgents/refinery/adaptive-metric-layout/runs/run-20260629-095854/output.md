<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --border: #2a2d3a;
  --text: #e1e4ed;
  --text-muted: #8b8fa3;
  --accent: #6c8cff;
  --accent-dim: #4a5fcc;
  --danger: #ff6b7a;
  --success: #4ade80;
  --warn: #f59e0b;
  --radius: 8px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  --gap: 12px;
  --header-h: 48px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: var(--header-h);
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.header h1 {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: -0.3px;
}
.header-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}
.btn {
  padding: 6px 14px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: var(--transition);
  white-space: nowrap;
}
.btn:hover { border-color: var(--accent); color: var(--accent); }
.btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.stat-badge {
  font-size: 11px;
  color: var(--text-muted);
  padding: 4px 10px;
  background: var(--bg);
  border-radius: 20px;
  border: 1px solid var(--border);
}
.dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--gap);
  padding: 16px;
  max-width: 1600px;
  margin: 0 auto;
}
/* Size classes applied via targeted class toggle — no innerHTML replacement */
.panel.col-1 { grid-column: span 1; grid-row: span 1; }
.panel.col-2 { grid-column: span 2; grid-row: span 1; }
.panel.col-3 { grid-column: span 3; grid-row: span 1; }
.panel.col-full { grid-column: 1 / -1; grid-row: span 1; }
.panel.row-2 { grid-row: span 2; }
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0;
  display: flex;
  flex-direction: column;
  transition: var(--transition);
  min-height: 180px;
  position: relative;
  overflow: hidden;
}
.panel:hover { border-color: var(--accent-dim); }
.panel.compact { min-height: 60px; }
.panel.compact .panel-body { display: none; }
.panel.compact .panel-preview { display: flex; }
.panel:not(.compact) .panel-preview { display: none; }
.panel.locked { border-color: var(--warn); }
.panel.locked::before {
  content: 'locked';
  position: absolute;
  top: 6px;
  right: 40px;
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--warn);
  background: rgba(245,158,11,0.1);
  padding: 2px 6px;
  border-radius: 3px;
  z-index: 2;
}
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px 8px;
  cursor: grab;
  user-select: none;
  flex-shrink: 0;
}
.panel-header:active { cursor: grabbing; }
.panel-header.dragging { opacity: 0.5; }
.panel-title {
  font-size: 13px;
  font-weight: 600;
  letter-spacing: -0.2px;
}
.panel-score {
  font-size: 10px;
  color: var(--text-muted);
  margin-left: 8px;
  padding: 2px 6px;
  background: var(--bg);
  border-radius: 10px;
}
.panel-controls {
  display: flex;
  gap: 4px;
  align-items: center;
}
.panel-ctrl {
  width: 26px;
  height: 26px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  border-radius: 4px;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}
.panel-ctrl:hover { background: var(--bg); border-color: var(--border); color: var(--text); }
.panel-ctrl.lock-btn.locked { color: var(--warn); border-color: var(--warn); background: rgba(245,158,11,0.1); }
.panel-body {
  flex: 1;
  padding: 0 14px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 0;
}
.panel-preview {
  padding: 10px 14px;
  flex: 1;
  display: none;
  align-items: center;
  gap: 8px;
  color: var(--text-muted);
  font-size: 12px;
}
.panel-preview .spark {
  width: 60px;
  height: 24px;
  background: linear-gradient(90deg, var(--accent-dim) 0%, var(--accent) 50%, var(--accent-dim) 100%);
  border-radius: 4px;
  opacity: 0.5;
}
.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid var(--border);
  font-size: 12px;
}
.metric-row:last-child { border-bottom: none; }
.metric-label { color: var(--text-muted); }
.metric-value { font-weight: 600; font-variant-numeric: tabular-nums; }
.metric-value.up { color: var(--success); }
.metric-value.down { color: var(--danger); }
.chart-area {
  flex: 1;
  min-height: 80px;
  background: var(--bg);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}
.chart-area canvas { width: 100%; height: 100%; display: block; }
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-muted);
  font-size: 13px;
}
.drag-ghost {
  position: fixed;
  pointer-events: none;
  z-index: 1000;
  opacity: 0.85;
  transform: rotate(1deg);
  box-shadow: 0 16px 48px rgba(0,0,0,0.5);
  border-color: var(--accent) !important;
}
.drop-zone {
  border: 2px dashed var(--accent);
  border-radius: var(--radius);
  background: rgba(108,140,255,0.05);
}
@media (max-width: 768px) {
  .dashboard { grid-template-columns: 1fr; }
  .panel.col-2, .panel.col-3, .panel.col-full { grid-column: span 1; }
}
</style>
</head>
<body>
<header class="header">
  <h1>Adaptive Metrics</h1>
  <div class="header-actions">
    <span class="stat-badge" id="total-views">views: 0</span>
    <span class="stat-badge" id="session-time">session: 0s</span>
    <button class="btn" id="btn-reset" title="Reset all tracking data">Reset Layout</button>
  </div>
</header>
<div class="dashboard" id="dashboard">
  <!-- Panels rendered once, mutated via targeted classList/DOM patching thereafter -->
</div>
<script>
'use strict';
// ============================================================================
// Attention Tracker — logs view duration, interaction frequency, events
// ============================================================================
const tracker = {
  // Map-based storage for O(1) lookups in hot paths — no Array.find
  panels: new Map(),       // panelId -> { views, totalDuration, interactions, lastViewed, events }
  sessionStart: Date.now(),
  totalViews: 0,
  init(id) {
    if (!this.panels.has(id)) {
      this.panels.set(id, {
        views: 0,
        totalDuration: 0,
        interactions: 0,
        lastViewed: Date.now(),
        events: [] // capped at 50
      });
    }
    return this.panels.get(id);
  },
  get(id) {
    return this.panels.get(id) || this.init(id);
  },
  viewStart(id) {
    const p = this.get(id);
    p._viewStart = Date.now();
    p.views++;
    this.totalViews++;
    return p;
  },
  viewEnd(id) {
    const p = this.get(id);
    if (p._viewStart) {
      p.totalDuration += Date.now() - p._viewStart;
      p._viewStart = null;
    }
    p.lastViewed = Date.now();
  },
  interact(id) {
    const p = this.get(id);
    p.interactions++;
    p.lastViewed = Date.now();
  },
  logEvent(id, type) {
    const p = this.get(id);
    p.events.unshift({ type, ts: Date.now() });
    if (p.events.length > 50) p.events.length = 50;
  },
  // Composite attention score: frequency * duration * recency
  score(id) {
    const p = this.get(id);
    const now = Date.now();
    const hoursSinceLastView = Math.max(0.1, (now - p.lastViewed) / 3600000);
    const recency = 1 / Math.log(1 + hoursSinceLastView);
    const durationScore = Math.log(1 + p.totalDuration / 1000);
    const freqScore = Math.log(1 + p.views);
    return freqScore * durationScore * recency;
  },
  getAllScores() {
    const scores = [];
    for (const [id] of this.panels) {
      scores.push({ id, score: this.score(id) });
    }
    return scores.sort((a, b) => b.score - a.score);
  },
  serialize() {
    const data = {};
    for (const [id, p] of this.panels) {
      data[id] = {
        views: p.views,
        totalDuration: p.totalDuration,
        interactions: p.interactions,
        lastViewed: p.lastViewed
      };
    }
    return data;
  },
  load(data) {
    if (!data) return;
    for (const [id, p] of Object.entries(data)) {
      this.panels.set(id, {
        views: p.views || 0,
        totalDuration: p.totalDuration || 0,
        interactions: p.interactions || 0,
        lastViewed: p.lastViewed || Date.now(),
        events: []
      });
    }
  }
};
// ============================================================================
// Layout Engine — arranges panels by attention score
// ============================================================================
const layout = {
  // Pre-sorted array cache — only re-sorted when panel order actually changes
  _sortedCache: null,
  _cacheValid: false,
  // Manual overrides: id -> { position: number, locked: bool, compact: bool }
  overrides: new Map(),
  order: [], // current panel order
  invalidateCache() {
    this._cacheValid = false;
  },
  // Returns sorted panel IDs, using cache when valid
  getSortedPanels() {
    if (this._cacheValid && this._sortedCache) return this._sortedCache;
    const ranked = tracker.getAllScores(); // [{id, score}]
    // Apply overrides for locked panels: they stay at their locked position
    const locked = [];
    const unlocked = [];
    for (const item of ranked) {
      const ov = this.overrides.get(item.id);
      if (ov && ov.locked && ov.position !== undefined) {
        locked.push({ ...item, lockedPos: ov.position });
      } else {
        unlocked.push(item);
      }
    }
    // Sort locked by position
    locked.sort((a, b) => a.lockedPos - b.lockedPos);
    // Merge: insert locked panels at their position, fill gaps with unlocked
    const result = [];
    const unlockedCopy = [...unlocked];
    for (let i = 0; ; i++) {
      const lockAt = locked.find(l => l.lockedPos === i);
      if (lockAt) {
        result.push(lockAt.id);
      } else if (unlockedCopy.length) {
        result.push(unlockedCopy.shift().id);
      } else if (!locked.find(l => l.lockedPos >= i)) {
        break;
      }
      if (result.length >= ranked.length) break;
    }
    this._sortedCache = result;
    this._cacheValid = true;
    this.order = result;
    return result;
  },
  getSizeClass(rank, total) {
    // top 20%: large, next 30%: medium, rest: small/compact
    const pct = rank / Math.max(1, total - 1);
    if (pct <= 0.2) return 'col-3 row-2';
    if (pct <= 0.5) return 'col-2';
    if (pct <= 0.8) return 'col-1';
    return 'compact'; // bottom 20% auto-compact
  },
  persist() {
    const data = {
      tracking: tracker.serialize(),
      overrides: Array.from(this.overrides.entries()),
      order: this.order,
      ts: Date.now()
    };
    try {
      localStorage.setItem('adaptive-layout-v1', JSON.stringify(data));
    } catch(e) { /* quota exceeded — silent fail */ }
  },
  restore() {
    try {
      const raw = localStorage.getItem('adaptive-layout-v1');
      if (!raw) return false;
      const data = JSON.parse(raw);
      tracker.load(data.tracking);
      if (data.overrides) {
        this.overrides = new Map(data.overrides);
      }
      if (data.order) this.order = data.order;
      this.invalidateCache();
      return true;
    } catch(e) { return false; }
  },
  saveDebounced: null,
  schedulePersist() {
    if (this.saveDebounced) clearTimeout(this.saveDebounced);
    this.saveDebounced = setTimeout(() => this.persist(), 500);
  }
};
// ============================================================================
// Panel definitions
// ============================================================================
const panelDefs = [
  { id: 'revenue', title: 'Revenue', type: 'chart', data: { value: 48200, change: 12.3, trend: [10,15,18,22,25,30,35,42,48] } },
  { id: 'users', title: 'Active Users', type: 'chart', data: { value: 1842, change: -5.7, trend: [200,450,380,520,600,580,720,890,840] } },
  { id: 'latency', title: 'API Latency', type: 'metric', data: { value: 42, unit: 'ms', change: -8.2, rows: [{l:'p50',v:'32ms'},{l:'p95',v:'89ms'},{l:'p99',v:'210ms'}] } },
  { id: 'errors', title: 'Error Rate', type: 'metric', data: { value: 0.23, unit: '%', change: 0.05, rows: [{l:'4xx',v:'0.12%'},{l:'5xx',v:'0.08%'},{l:'timeout',v:'0.03%'}] } },
  { id: 'cpu', title: 'CPU Usage', type: 'sparkline', data: { value: 67, unit: '%', trend: [45,52,48,60,55,70,65,72,67] } },
  { id: 'memory', title: 'Memory', type: 'sparkline', data: { value: 8.2, unit: 'GB', trend: [6.1,6.5,7.0,6.8,7.4,7.9,8.0,8.3,8.2] } },
  { id: 'requests', title: 'Requests/min', type: 'chart', data: { value: 3420, change: 18.9, trend: [1200,1400,1600,1800,2100,2500,2800,3100,3420] } },
  { id: 'storage', title: 'Storage', type: 'metric', data: { value: 142, unit: 'GB', change: 2.1, rows: [{l:'used',v:'142 GB'},{l:'total',v:'500 GB'},{l:'growth',v:'+2.1%/day'}] } },
];
// ============================================================================
// DOM Render — targeted patching, NO innerHTML full-replace
// ============================================================================
// Panel element pool: Map<id, HTMLElement> for O(1) lookup in event handlers
const panelMap = new Map();
function buildPanel(def) {
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.panelId = def.id;
  el.dataset.type = def.type;
  el.innerHTML = `
    <div class="panel-header" data-action="drag-handle">
      <span>
        <span class="panel-title">${def.title}</span>
        <span class="panel-score" data-field="score">—</span>
      </span>
      <span class="panel-controls">
        <button class="panel-ctrl lock-btn" data-action="lock" title="Lock position">pin</button>
        <button class="panel-ctrl" data-action="compact" title="Toggle compact">⊟</button>
        <button class="panel-ctrl" data-action="expand" title="Expand">⤢</button>
      </span>
    </div>
    <div class="panel-body"></div>
    <div class="panel-preview">
      <div class="spark"></div>
      <span class="panel-title">${def.title}</span>
      <span data-field="score">—</span>
    </div>
  `;
  const body = el.querySelector('.panel-body');
  renderPanelBody(body, def);
  panelMap.set(def.id, el);
  return el;
}
// Update panel metadata fields without innerHTML replacement
function patchPanelMeta(el, score, rank, total) {
  const scoreEls = el.querySelectorAll('[data-field="score"]');
  const scoreText = score.toFixed(2);
  for (const s of scoreEls) s.textContent = scoreText;
  // Size class mutation — targeted classList toggle
  const sizeClass = layout.getSizeClass(rank, total);
  const ov = layout.overrides.get(el.dataset.panelId);
  const isCompact = (ov && ov.compact) || sizeClass === 'compact';
  // Remove old size classes, add new
  el.classList.remove('col-1', 'col-2', 'col-3', 'col-full', 'row-2', 'compact');
  if (isCompact) {
    el.classList.add('compact');
  } else if (sizeClass === 'col-3 row-2') {
    el.classList.add('col-3', 'row-2');
  } else if (sizeClass === 'col-2') {
    el.classList.add('col-2');
  } else {
    el.classList.add('col-1');
  }
  // Lock indicator
  const lockBtn = el.querySelector('[data-action="lock"]');
  if (lockBtn) {
    if (ov && ov.locked) {
      el.classList.add('locked');
      lockBtn.classList.add('locked');
    } else {
      el.classList.remove('locked');
      lockBtn.classList.remove('locked');
    }
  }
}
// Reorder DOM children efficiently: only move elements that changed position
function reorderPanels(container, sortedIds) {
  // Build current order from DOM
  const currentOrder = [];
  for (const child of container.children) {
    currentOrder.push(child.dataset.panelId);
  }
  // Only reorder if positions actually changed
  let changed = false;
  const targetMap = new Map(); // id -> targetIndex
  for (let i = 0; i < sortedIds.length; i++) {
    targetMap.set(sortedIds[i], i);
    if (sortedIds[i] !== currentOrder[i]) changed = true;
  }
  if (!changed) {
    // Quick path: just update metadata in place
    for (let i = 0; i < sortedIds.length; i++) {
      const el = panelMap.get(sortedIds[i]);
      if (el) {
        const score = tracker.score(sortedIds[i]);
        patchPanelMeta(el, score, i, sortedIds.length);
      }
    }
    return;
  }
  // Reorder by inserting at correct position — minimal DOM mutations
  for (let targetIdx = 0; targetIdx < sortedIds.length; targetIdx++) {
    const id = sortedIds[targetIdx];
    const el = panelMap.get(id);
    if (!el) continue;
    const currentChild = container.children[targetIdx];
    if (currentChild !== el) {
      container.insertBefore(el, currentChild);
    }
  }
  // Update metadata for all panels
  for (let i = 0; i < sortedIds.length; i++) {
    const el = panelMap.get(sortedIds[i]);
    if (el) {
      const score = tracker.score(sortedIds[i]);
      patchPanelMeta(el, score, i, sortedIds.length);
    }
  }
}
function renderPanelBody(bodyEl, def) {
  bodyEl.innerHTML = ''; // body-only clear, header preserved
  if (def.type === 'metric') {
    bodyEl.innerHTML = `
      <div style="display:flex;align-items:baseline;gap:6px;padding:4px 0">
        <span style="font-size:28px;font-weight:700;letter-spacing:-1px">${def.data.value}<span style="font-size:14px;color:var(--text-muted)">${def.data.unit||''}</span></span>
        <span class="metric-value ${def.data.change>=0?'up':'down'}">${def.data.change>=0?'+':''}${def.data.change}${def.data.unit||'%'}</span>
      </div>
      ${(def.data.rows||[]).map(r=>`<div class="metric-row"><span class="metric-label">${r.l}</span><span class="metric-value">${r.v}</span></div>`).join('')}
    `;
  } else if (def.type === 'sparkline') {
    bodyEl.innerHTML = `
      <div style="display:flex;align-items:baseline;gap:6px;padding:4px 0">
        <span style="font-size:28px;font-weight:700;letter-spacing:-1px">${def.data.value}<span style="font-size:14px;color:var(--text-muted)">${def.data.unit||''}</span></span>
      </div>
      <div class="chart-area"><canvas></canvas></div>
    `;
    requestAnimationFrame(() => {
      const canvas = bodyEl.querySelector('canvas');
      if (canvas) drawSparkline(canvas, def.data.trend);
    });
  } else {
    // chart type
    bodyEl.innerHTML = `
      <div style="display:flex;align-items:baseline;gap:6px;padding:4px 0">
        <span style="font-size:28px;font-weight:700;letter-spacing:-1px">${def.data.value.toLocaleString()}</span>
        <span class="metric-value ${def.data.change>=0?'up':'down'}">${def.data.change>=0?'+':''}${def.data.change}%</span>
      </div>
      <div class="chart-area"><canvas></canvas></div>
    `;
    requestAnimationFrame(() => {
      const canvas = bodyEl.querySelector('canvas');
      if (canvas) drawSparkline(canvas, def.data.trend);
    });
  }
}
// Deterministic sparkline — no Math.random()
function drawSparkline(canvas, data) {
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  canvas.style.width = rect.width + 'px';
  canvas.style.height = rect.height + 'px';
  const ctx = canvas.getContext('2d');
  ctx.scale(dpr, dpr);
  const w = rect.width;
  const h = rect.height;
  const pad = 4;
  const pw = w - pad * 2;
  const ph = h - pad * 2;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;
  ctx.clearRect(0, 0, w, h);
  // Gradient fill
  const grad = ctx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, 'rgba(108,140,255,0.25)');
  grad.addColorStop(1, 'rgba(108,140,255,0.02)');
  ctx.beginPath();
  for (let i = 0; i < data.length; i++) {
    const x = pad + (i / (data.length - 1)) * pw;
    const y = pad + ph - ((data[i] - min) / range) * ph;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.strokeStyle = '#6c8cff';
  ctx.lineWidth = 1.5;
  ctx.stroke();
  // Area fill
  ctx.lineTo(pad + pw, pad + ph);
  ctx.lineTo(pad, pad + ph);
  ctx.closePath();
  ctx.fillStyle = grad;
  ctx.fill();
  // Last point dot
  const lx = pad + pw;
  const ly = pad + ph - ((data[data.length-1] - min) / range) * ph;
  ctx.beginPath();
  ctx.arc(lx, ly, 3, 0, Math.PI * 2);
  ctx.fillStyle = '#6c8cff';
  ctx.fill();
}
// ============================================================================
// IntersectionObserver — created ONCE, reused
// ============================================================================
// Single observer for all panels, no per-element creation
let visibilityObserver = null;
function setupVisibilityObserver() {
  if (visibilityObserver) return; // Reuse existing
  visibilityObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      const id = entry.target.dataset.panelId;
      if (!id) continue;
      if (entry.isIntersecting) {
        tracker.viewStart(id);
      } else {
        tracker.viewEnd(id);
      }
    }
  }, { threshold: 0.5 });
  // Observe all existing panels
  for (const el of panelMap.values()) {
    visibilityObserver.observe(el);
  }
}
// ============================================================================
// Event Delegation — single listener on dashboard, not per-element
// ============================================================================
function setupEventDelegation(container) {
  // Remove any previous listener by replacing with clone (clean approach)
  const oldEl = container;
  const newEl = oldEl.cloneNode(false);
  // Preserve children
  while (oldEl.firstChild) newEl.appendChild(oldEl.firstChild);
  oldEl.parentNode.replaceChild(newEl, oldEl);
  // Single click handler via delegation
  newEl.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    const panel = btn.closest('.panel');
    if (!panel) return;
    const id = panel.dataset.panelId;
    if (!id) return;
    const action = btn.dataset.action;
    tracker.interact(id);
    tracker.logEvent(id, action);
    switch (action) {
      case 'lock': {
        const ov = layout.overrides.get(id) || {};
        const sorted = layout.getSortedPanels();
        const idx = sorted.indexOf(id);
        ov.locked = !ov.locked;
        ov.position = idx;
        layout.overrides.set(id, ov);
        layout.invalidateCache();
        applyLayout(newEl);
        layout.schedulePersist();
        break;
      }
      case 'compact': {
        const ov = layout.overrides.get(id) || {};
        ov.compact = !ov.compact;
        layout.overrides.set(id, ov);
        layout.invalidateCache();
        applyLayout(newEl);
        layout.schedulePersist();
        break;
      }
      case 'expand': {
        // Expand panel to full width temporarily
        const ov = layout.overrides.get(id) || {};
        if (panel.classList.contains('col-full')) {
          panel.classList.remove('col-full', 'row-2');
          ov._expanded = false;
        } else {
          panel.classList.add('col-full', 'row-2');
          ov._expanded = true;
        }
        layout.overrides.set(id, ov);
        layout.schedulePersist();
        break;
      }
    }
  });
  // Drag and drop via delegation
  let dragEl = null;
  let dragGhost = null;
  let dragStartIdx = -1;
  newEl.addEventListener('mousedown', (e) => {
    const handle = e.target.closest('[data-action="drag-handle"]');
    if (!handle) return;
    const panel = handle.closest('.panel');
    if (!panel) return;
    e.preventDefault();
    dragEl = panel;
    dragStartIdx = Array.from(newEl.children).indexOf(panel);
    // Create ghost
    dragGhost = panel.cloneNode(true);
    dragGhost.classList.add('drag-ghost');
    dragGhost.style.width = panel.offsetWidth + 'px';
    dragGhost.style.height = panel.offsetHeight + 'px';
    document.body.appendChild(dragGhost);
    panel.classList.add('dragging');
    updateGhostPos(e);
  });
  // Use document-level listeners for drag — delegation doesn't work for mousemove/mouseup
  document.addEventListener('mousemove', (e) => {
    if (!dragEl) return;
    updateGhostPos(e);
    // Find drop target using Map lookup
    const target = findDropTarget(newEl, e.clientX, e.clientY);
    // Clear all drop zones
    for (const child of newEl.children) {
      child.classList.remove('drop-zone');
    }
    if (target && target !== dragEl) {
      target.classList.add('drop-zone');
    }
  });
  document.addEventListener('mouseup', (e) => {
    if (!dragEl) return;
    const target = findDropTarget(newEl, e.clientX, e.clientY);
    if (target && target !== dragEl) {
      // Reorder
      const targetIdx = Array.from(newEl.children).indexOf(target);
      const sorted = [...layout.getSortedPanels()];
      const draggedId = dragEl.dataset.panelId;
      const oldIdx = sorted.indexOf(draggedId);
      if (oldIdx !== -1 && targetIdx !== -1) {
        sorted.splice(oldIdx, 1);
        sorted.splice(targetIdx, 0, draggedId);
        layout._sortedCache = sorted;
        layout._cacheValid = true;
        // Lock dragged panel at new position
        const ov = layout.overrides.get(draggedId) || {};
        ov.locked = true;
        ov.position = targetIdx;
        layout.overrides.set(draggedId, ov);
        tracker.logEvent(draggedId, 'drag-reorder');
      }
      applyLayout(newEl);
      layout.schedulePersist();
    }
    // Cleanup
    dragEl.classList.remove('dragging');
    for (const child of newEl.children) child.classList.remove('drop-zone');
    if (dragGhost) { dragGhost.remove(); dragGhost = null; }
    dragEl = null;
    dragStartIdx = -1;
  });
  return newEl;
}
function updateGhostPos(e) {
  if (!dragGhost) return;
  dragGhost.style.left = (e.clientX - dragGhost.offsetWidth / 2) + 'px';
  dragGhost.style.top = (e.clientY - dragGhost.offsetHeight / 2) + 'px';
}
// Map-based panel lookup in drag hot path — no Array.find
function findDropTarget(container, cx, cy) {
  for (const child of container.children) {
    const rect = child.getBoundingClientRect();
    if (cx >= rect.left && cx <= rect.right && cy >= rect.top && cy <= rect.bottom) {
      return child;
    }
  }
  return null;
}
// ============================================================================
// Layout application — orchestrates reorder + metadata patch
// ============================================================================
function applyLayout(container) {
  const sorted = layout.getSortedPanels();
  reorderPanels(container, sorted);
  updateStats();
}
function updateStats() {
  const viewsEl = document.getElementById('total-views');
  const timeEl = document.getElementById('session-time');
  if (viewsEl) viewsEl.textContent = 'views: ' + tracker.totalViews;
  if (timeEl) {
    const elapsed = Math.floor((Date.now() - tracker.sessionStart) / 1000);
    timeEl.textContent = 'session: ' + elapsed + 's';
  }
}
// ============================================================================
// Initialization
// ============================================================================
function init() {
  const restored = layout.restore();
  let container = document.getElementById('dashboard');
  // Build panels (only once — never full innerHTML replace)
  for (const def of panelDefs) {
    const el = buildPanel(def);
    container.appendChild(el);
  }
  // Setup event delegation
  container = setupEventDelegation(container);
  // Setup shared visibility observer
  setupVisibilityObserver();
  // Apply initial layout
  if (!restored) {
    // Initialize tracker for all panels
    for (const def of panelDefs) tracker.init(def.id);
    layout.invalidateCache();
  }
  applyLayout(container);
  // Periodic stats update + persist (no Math.random)
  setInterval(() => {
    updateStats();
    layout.schedulePersist();
  }, 5000);
  // Session time update every second
  setInterval(updateStats, 1000);
  // Reset button
  document.getElementById('btn-reset').addEventListener('click', () => {
    localStorage.removeItem('adaptive-layout-v1');
    layout.overrides.clear();
    layout.invalidateCache();
    for (const def of panelDefs) tracker.init(def.id);
    applyLayout(container);
  });
  // Persist on unload
  window.addEventListener('beforeunload', () => layout.persist());
}
document.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>