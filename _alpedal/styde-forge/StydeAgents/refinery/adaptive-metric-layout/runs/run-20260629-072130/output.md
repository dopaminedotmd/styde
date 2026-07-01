<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0f1117; --surface: #1a1d27; --surface2: #242836;
  --text: #e1e4eb; --text2: #9499a5; --accent: #6c8aff;
  --accent2: #4ade80; --warn: #f59e0b; --danger: #ef4444;
  --radius: 10px; --gap: 12px; --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg); color: var(--text); min-height: 100vh;
  overflow-x: hidden;
}
header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 20px; background: var(--surface); border-bottom: 1px solid #2a2e3a;
  position: sticky; top: 0; z-index: 100;
}
header h1 { font-size: 1.15rem; font-weight: 600; letter-spacing: -0.01em; }
header .controls { display: flex; gap: 8px; align-items: center; }
.btn {
  padding: 7px 14px; border-radius: 7px; border: 1px solid #3a3f50;
  background: var(--surface2); color: var(--text); cursor: pointer;
  font-size: 0.82rem; transition: all var(--transition);
}
.btn:hover { background: #2e3345; border-color: #555; }
.btn.accent { background: var(--accent); border-color: var(--accent); color: #fff; }
.btn.accent:hover { filter: brightness(1.15); }
.btn.warn { background: var(--warn); border-color: var(--warn); color: #111; }
#grid {
  display: grid; gap: var(--gap); padding: var(--gap);
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(180px, auto);
  min-height: calc(100vh - 60px);
}
@media (min-width: 1400px) { #grid { grid-template-columns: repeat(6, 1fr); } }
@media (max-width: 900px) { #grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 500px) { #grid { grid-template-columns: 1fr; } }
.panel {
  background: var(--surface); border-radius: var(--radius);
  border: 1px solid #2a2e3a; position: relative;
  display: flex; flex-direction: column; overflow: hidden;
  transition: all var(--transition); cursor: grab;
  user-select: none;
}
.panel.locked { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent); }
.panel.dragging { opacity: 0.92; z-index: 50; box-shadow: 0 8px 32px rgba(0,0,0,0.5); cursor: grabbing; transform: scale(1.02); }
.panel.compact { grid-row: span 1 !important; grid-column: span 1 !important; }
.panel.compact .panel-body { display: none; }
.panel.compact .compact-preview { display: flex; }
.panel.full  { grid-column: span 2; grid-row: span 2; }
.panel.wide  { grid-column: span 2; grid-row: span 1; }
.panel.tall  { grid-column: span 1; grid-row: span 2; }
.panel.standard { grid-column: span 1; grid-row: span 1; }
.panel-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px; background: var(--surface2); border-bottom: 1px solid #2a2e3a;
  font-size: 0.85rem; font-weight: 600; flex-shrink: 0;
}
.panel-header .left { display: flex; align-items: center; gap: 8px; }
.panel-header .indicator {
  width: 8px; height: 8px; border-radius: 50%;
}
.panel-header .indicator.hot { background: var(--accent2); box-shadow: 0 0 6px var(--accent2); }
.panel-header .indicator.warm { background: var(--warn); }
.panel-header .indicator.cold { background: #555; }
.panel-header .rank-badge {
  font-size: 0.65rem; padding: 1px 6px; border-radius: 4px;
  background: #2a2e3a; color: var(--text2);
}
.panel-actions { display: flex; gap: 4px; }
.panel-actions button {
  background: none; border: none; color: var(--text2); cursor: pointer;
  padding: 3px 6px; border-radius: 4px; font-size: 0.75rem;
  transition: all 0.15s;
}
.panel-actions button:hover { color: var(--text); background: #333; }
.panel-actions button.active { color: var(--accent); }
.panel-body { padding: 14px; flex: 1; display: flex; flex-direction: column; gap: 8px; overflow: auto; }
.compact-preview { display: none; padding: 12px; align-items: center; justify-content: center; flex: 1; color: var(--text2); font-size: 0.78rem; flex-direction: column; gap: 4px; }
.compact-preview .metric { font-size: 1.6rem; font-weight: 700; color: var(--text); }
.metric-row { display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; }
.metric-row .label { color: var(--text2); }
.metric-row .value { font-weight: 600; }
.mini-bar { height: 4px; border-radius: 2px; background: #2a2e3a; margin-top: 2px; overflow: hidden; }
.mini-bar .fill { height: 100%; border-radius: 2px; transition: width 0.6s ease; }
.score-debug {
  position: fixed; bottom: 10px; right: 10px; background: #000c; color: #0f0;
  padding: 8px 12px; border-radius: 6px; font-size: 0.7rem; font-family: monospace;
  z-index: 200; max-height: 200px; overflow-y: auto; display: none;
}
.score-debug.visible { display: block; }
.drag-ghost { opacity: 0.3; background: var(--accent); border: 2px dashed var(--accent); border-radius: var(--radius); }
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <button class="btn" onclick="Dashboard.resetLayout()" title="Reset all positions and tracking data">Reset</button>
    <button class="btn" onclick="Dashboard.toggleDebug()" title="Toggle score debug panel">Debug</button>
    <button class="btn accent" onclick="Dashboard.forceLayout()" title="Re-apply layout now">Apply Layout</button>
  </div>
</header>
<div id="grid"></div>
<div class="score-debug" id="debug"></div>
<script>
// ============ EVENT-DRIVEN REACTIVITY CORE ============
class EventBus {
  constructor() {
    this._listeners = {};
    this._pending = new Set();
    this._flushScheduled = false;
  }
  on(event, fn) { (this._listeners[event] ??= new Set()).add(fn); }
  off(event, fn) { this._listeners[event]?.delete(fn); }
  emit(event, data) {
    this._pending.add({ event, data });
    if (!this._flushScheduled) {
      this._flushScheduled = true;
      requestAnimationFrame(() => this._flush());
    }
  }
  _flush() {
    const batch = [...this._pending];
    this._pending.clear();
    this._flushScheduled = false;
    const deduped = new Map();
    for (const { event, data } of batch) {
      deduped.set(event, data);
    }
    for (const [event, data] of deduped) {
      for (const fn of this._listeners[event] ?? []) {
        try { fn(data); } catch (e) { console.error('EventBus error:', event, e); }
      }
    }
  }
}
const bus = new EventBus();
// ============ TRACKING ENGINE ============
const HALF_LIFE_DAYS = 7;
const LS_KEY = 'adaptive_dashboard_v2';
class Tracker {
  constructor() {
    this.panels = new Map();
    this.observer = null;
    this.viewTimers = new Map();
    this._restore();
  }
  initObserver() {
    if (this.observer) this.observer.disconnect();
    this.observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        const id = entry.target.dataset.panelId;
        if (!id) continue;
        if (entry.isIntersecting) {
          this._startView(id);
        } else {
          this._endView(id);
        }
      }
    }, { threshold: 0.5 });
    for (const el of document.querySelectorAll('.panel')) {
      this.observer.observe(el);
    }
  }
  _startView(id) {
    if (this.viewTimers.has(id)) return;
    this.viewTimers.set(id, Date.now());
  }
  _endView(id) {
    const start = this.viewTimers.get(id);
    if (!start) return;
    const duration = (Date.now() - start) / 1000;
    this.viewTimers.delete(id);
    const d = this.panels.get(id) || this._defaultData(id);
    d.totalViewSeconds += duration;
    d.lastViewed = Date.now();
    this.panels.set(id, d);
    this._save();
    bus.emit('tracking-updated', { id, panel: d });
  }
  recordInteraction(id) {
    const d = this.panels.get(id) || this._defaultData(id);
    d.interactions++;
    d.lastInteraction = Date.now();
    this.panels.set(id, d);
    this._save();
    bus.emit('tracking-updated', { id, panel: d });
  }
  recordExpand(id) {
    const d = this.panels.get(id) || this._defaultData(id);
    d.expands++;
    this.panels.set(id, d);
    this._save();
    bus.emit('tracking-updated', { id, panel: d });
  }
  getScore(id) {
    const d = this.panels.get(id);
    if (!d) return 0;
    const now = Date.now();
    const daysSinceView = Math.max(0, (now - d.lastViewed) / 86400000);
    const daysSinceInteraction = Math.max(0, (now - d.lastInteraction) / 86400000);
    const recencyView = Math.exp(-daysSinceView * Math.LN2 / HALF_LIFE_DAYS);
    const recencyInteraction = Math.exp(-daysSinceInteraction * Math.LN2 / HALF_LIFE_DAYS);
    const recency = 0.4 * recencyView + 0.6 * recencyInteraction;
    const freq = Math.log1p(d.interactions + d.expands);
    const dur = Math.log1p(d.totalViewSeconds / 60);
    return freq * dur * recency;
  }
  getAllScores() {
    const scores = {};
    for (const [id] of this.panels) {
      scores[id] = this.getScore(id);
    }
    return scores;
  }
  _defaultData(id) {
    return { totalViewSeconds: 0, interactions: 0, expands: 0, lastViewed: Date.now(), lastInteraction: Date.now() };
  }
  reset() {
    this.panels.clear();
    this._save();
    bus.emit('tracking-reset', {});
  }
  _save() {
    try { localStorage.setItem(LS_KEY + '_tracking', JSON.stringify([...this.panels])); } catch (e) {}
  }
  _restore() {
    try {
      const raw = localStorage.getItem(LS_KEY + '_tracking');
      if (raw) { this.panels = new Map(JSON.parse(raw)); }
    } catch (e) {}
  }
  flushViews() {
    for (const [id] of this.viewTimers) {
      this._endView(id);
    }
  }
}
const tracker = new Tracker();
// ============ LAYOUT ENGINE ============
const SIZE_CLASSES = ['full', 'wide', 'tall', 'standard', 'compact'];
class LayoutEngine {
  constructor() {
    this.locks = new Map();
    this.overrides = new Map();
    this._dragging = false;
    this._restore();
  }
  lock(id) { this.locks.set(id, true); this._save(); bus.emit('layout-changed', {}); }
  unlock(id) { this.locks.delete(id); this._save(); bus.emit('layout-changed', {}); }
  isLocked(id) { return this.locks.has(id); }
  setOverride(id, sizeClass) { this.overrides.set(id, sizeClass); this._save(); bus.emit('layout-changed', {}); }
  clearOverride(id) { this.overrides.delete(id); this._save(); bus.emit('layout-changed', {}); }
  get dragging() { return this._dragging; }
  set dragging(v) {
    if (this._dragging !== v) {
      this._dragging = v;
      if (!v) bus.emit('drag-ended', {});
    }
  }
  reset() {
    this.locks.clear();
    this.overrides.clear();
    this._save();
    bus.emit('layout-changed', {});
  }
  computeLayout(panelIds) {
    const scores = tracker.getAllScores();
    const ranked = panelIds
      .map(id => ({ id, score: scores[id] || 0 }))
      .sort((a, b) => b.score - a.score);
    const layout = {};
    const total = ranked.length;
    if (total === 0) return layout;
    for (let i = 0; i < ranked.length; i++) {
      const { id } = ranked[i];
      if (this.overrides.has(id)) {
        layout[id] = this.overrides.get(id);
      } else if (this.isLocked(id)) {
        layout[id] = 'standard';
      } else {
        const percentile = i / Math.max(total - 1, 1);
        if (percentile <= 0.15) layout[id] = 'full';
        else if (percentile <= 0.35) layout[id] = 'wide';
        else if (percentile <= 0.55) layout[id] = 'tall';
        else if (percentile <= 0.80) layout[id] = 'standard';
        else layout[id] = 'compact';
      }
    }
    return layout;
  }
  _save() {
    try {
      localStorage.setItem(LS_KEY + '_layout', JSON.stringify({
        locks: [...this.locks.keys()],
        overrides: [...this.overrides]
      }));
    } catch (e) {}
  }
  _restore() {
    try {
      const raw = localStorage.getItem(LS_KEY + '_layout');
      if (raw) {
        const d = JSON.parse(raw);
        this.locks = new Map(d.locks?.map(k => [k, true]) || []);
        this.overrides = new Map(d.overrides || []);
      }
    } catch (e) {}
  }
}
const layoutEngine = new LayoutEngine();
// ============ DRAG-DROP WITH LOCK-STEP ============
class DragManager {
  constructor(grid) {
    this.grid = grid;
    this.dragPanel = null;
    this.clone = null;
    this.startX = 0; this.startY = 0;
    this.offsetX = 0; this.offsetY = 0;
    this._boundMove = this._onMove.bind(this);
    this._boundUp = this._onUp.bind(this);
  }
  start(e, panel) {
    if (layoutEngine.isLocked(panel.dataset.panelId)) return;
    e.preventDefault();
    layoutEngine.dragging = true;
    this.dragPanel = panel;
    panel.classList.add('dragging');
    this.clone = panel.cloneNode(true);
    this.clone.classList.add('drag-ghost');
    this.clone.style.position = 'fixed';
    this.clone.style.pointerEvents = 'none';
    this.clone.style.width = panel.offsetWidth + 'px';
    this.clone.style.height = panel.offsetHeight + 'px';
    this.clone.style.zIndex = '49';
    document.body.appendChild(this.clone);
    const touch = e.touches?.[0] || e;
    this.startX = touch.clientX; this.startY = touch.clientY;
    this.clone.style.left = (touch.clientX - panel.offsetWidth / 2) + 'px';
    this.clone.style.top = (touch.clientY - panel.offsetHeight / 2) + 'px';
    document.addEventListener('mousemove', this._boundMove);
    document.addEventListener('mouseup', this._boundUp);
    document.addEventListener('touchmove', this._boundMove, { passive: false });
    document.addEventListener('touchend', this._boundUp);
  }
  _onMove(e) {
    if (!this.dragPanel) return;
    e.preventDefault();
    const touch = e.touches?.[0] || e;
    this.clone.style.left = (touch.clientX - this.dragPanel.offsetWidth / 2) + 'px';
    this.clone.style.top = (touch.clientY - this.dragPanel.offsetHeight / 2) + 'px';
    const target = document.elementFromPoint(touch.clientX, touch.clientY)?.closest('.panel');
    for (const el of document.querySelectorAll('.panel')) el.classList.remove('drag-target');
    if (target && target !== this.dragPanel) target.classList.add('drag-target');
  }
  _onUp(e) {
    if (!this.dragPanel) return;
    const touch = e.changedTouches?.[0] || e;
    const target = document.elementFromPoint(touch.clientX, touch.clientY)?.closest('.panel');
    if (target && target !== this.dragPanel) {
      this._swap(this.dragPanel.dataset.panelId, target.dataset.panelId);
    }
    this._cleanup();
    layoutEngine.dragging = false;
    bus.emit('drag-ended', {});
    bus.emit('layout-changed', {});
  }
  _swap(idA, idB) {
    const children = [...this.grid.children];
    const elA = children.find(c => c.dataset.panelId === idA);
    const elB = children.find(c => c.dataset.panelId === idB);
    if (!elA || !elB) return;
    const scores = tracker.getAllScores();
    layoutEngine.lock(idA); layoutEngine.lock(idB);
    const afterA = elB.nextSibling === elA ? elA.nextSibling : elB.nextSibling;
    this.grid.insertBefore(elB, afterA === elB ? elA.nextSibling : elA);
    tracker.recordInteraction(idA); tracker.recordInteraction(idB);
  }
  _cleanup() {
    if (this.dragPanel) this.dragPanel.classList.remove('dragging');
    if (this.clone) { this.clone.remove(); this.clone = null; }
    this.dragPanel = null;
    document.removeEventListener('mousemove', this._boundMove);
    document.removeEventListener('mouseup', this._boundUp);
    document.removeEventListener('touchmove', this._boundMove);
    document.removeEventListener('touchend', this._boundUp);
  }
}
// ============ DASHBOARD CONTROLLER ============
const PANEL_DEFS = [
  { id: 'revenue', title: 'Revenue', icon: '\u{1F4B0}', metric: '$48.2K', subtitle: '+12.3% vs last month', color: '#4ade80' },
  { id: 'users', title: 'Active Users', icon: '\u{1F465}', metric: '2,847', subtitle: '+5.7% this week', color: '#6c8aff' },
  { id: 'conversion', title: 'Conversion', icon: '\u{1F3AF}', metric: '3.24%', subtitle: '-0.3% vs target', color: '#f59e0b' },
  { id: 'latency', title: 'API Latency', icon: '\u{23F1}', metric: '142ms', subtitle: 'p95: 310ms', color: '#ef4444' },
  { id: 'errors', title: 'Error Rate', icon: '\u{26A0}', metric: '0.12%', subtitle: 'Below 1% threshold', color: '#4ade80' },
  { id: 'storage', title: 'Storage', icon: '\u{1F4BE}', metric: '67.8 GB', subtitle: '42% used', color: '#6c8aff' },
  { id: 'uptime', title: 'Uptime', icon: '\u{2705}', metric: '99.97%', subtitle: 'Last 30 days', color: '#4ade80' },
  { id: 'requests', title: 'Requests/min', icon: '\u{1F4E8}', metric: '3.2K', subtitle: 'Peak: 5.1K', color: '#a78bfa' },
];
class Dashboard {
  static grid = document.getElementById('grid');
  static dragManager = new DragManager(Dashboard.grid);
  static panels = new Map();
  static init() {
    for (const def of PANEL_DEFS) {
      const el = Dashboard._createPanel(def);
      Dashboard.grid.appendChild(el);
      Dashboard.panels.set(def.id, el);
    }
    tracker.initObserver();
    bus.on('layout-changed', () => Dashboard._applyLayout());
    bus.on('tracking-updated', () => Dashboard._updateIndicators());
    bus.on('drag-ended', () => Dashboard._applyLayout());
    bus.on('tracking-reset', () => Dashboard._applyLayout());
    window.addEventListener('beforeunload', () => tracker.flushViews());
    Dashboard._applyLayout();
    Dashboard._updateIndicators();
    Dashboard._startScorePolling();
  }
  static _createPanel(def) {
    const el = document.createElement('div');
    el.className = 'panel standard';
    el.dataset.panelId = def.id;
    el.innerHTML = `
      <div class="panel-header">
        <div class="left">
          <span class="indicator cold"></span>
          <span>${def.icon} ${def.title}</span>
          <span class="rank-badge">--</span>
        </div>
        <div class="panel-actions">
          <button class="lock-btn" title="Lock position">\u{1F512}</button>
          <button class="expand-btn" title="Expand/Collapse">\u{2195}</button>
        </div>
      </div>
      <div class="panel-body">
        <div class="metric-row"><span class="value" style="font-size:1.5rem;font-weight:700;">${def.metric}</span></div>
        <div class="metric-row"><span class="label">${def.subtitle}</span></div>
        <div class="mini-bar"><div class="fill" style="width:${40 + Math.random()*50}%;background:${def.color};"></div></div>
      </div>
      <div class="compact-preview">
        <span class="metric">${def.metric}</span>
        <span>${def.subtitle}</span>
      </div>`;
    el.addEventListener('mousedown', (e) => Dashboard.dragManager.start(e, el));
    el.addEventListener('touchstart', (e) => Dashboard.dragManager.start(e, el), { passive: false });
    el.querySelector('.lock-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      Dashboard._toggleLock(def.id);
    });
    el.querySelector('.expand-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      tracker.recordExpand(def.id);
      const isCompact = el.classList.contains('compact');
      if (isCompact) { layoutEngine.clearOverride(def.id); }
      else { layoutEngine.setOverride(def.id, 'compact'); }
      bus.emit('layout-changed', {});
    });
    el.addEventListener('click', () => tracker.recordInteraction(def.id));
    return el;
  }
  static _toggleLock(id) {
    if (layoutEngine.isLocked(id)) { layoutEngine.unlock(id); }
    else { layoutEngine.lock(id); }
    const el = Dashboard.panels.get(id);
    const btn = el?.querySelector('.lock-btn');
    if (btn) {
      btn.classList.toggle('active', layoutEngine.isLocked(id));
      btn.textContent = layoutEngine.isLocked(id) ? '\u{1F512}' : '\u{1F513}';
    }
    if (el) el.classList.toggle('locked', layoutEngine.isLocked(id));
    bus.emit('layout-changed', {});
  }
  static _applyLayout() {
    if (layoutEngine.dragging) return;
    const ids = [...Dashboard.panels.keys()];
    const layout = layoutEngine.computeLayout(ids);
    const scores = tracker.getAllScores();
    for (const [id, sizeClass] of Object.entries(layout)) {
      const el = Dashboard.panels.get(id);
      if (!el) continue;
      SIZE_CLASSES.forEach(c => el.classList.remove(c));
      el.classList.add(sizeClass);
      el.classList.toggle('locked', layoutEngine.isLocked(id));
      const btn = el.querySelector('.lock-btn');
      if (btn) {
        btn.classList.toggle('active', layoutEngine.isLocked(id));
        btn.textContent = layoutEngine.isLocked(id) ? '\u{1F512}' : '\u{1F513}';
      }
      const indicator = el.querySelector('.indicator');
      const score = scores[id] || 0;
      if (indicator) {
        indicator.classList.remove('hot', 'warm', 'cold');
        if (score > 2) indicator.classList.add('hot');
        else if (score > 0.5) indicator.classList.add('warm');
        else indicator.classList.add('cold');
      }
      const badge = el.querySelector('.rank-badge');
      if (badge) {
        const sorted = Object.entries(scores).sort((a,b) => b[1]-a[1]);
        const rank = sorted.findIndex(([i]) => i === id) + 1;
        badge.textContent = '#' + (rank || '--');
      }
    }
    Dashboard._sortGrid(scores);
  }
  static _sortGrid(scores) {
    const entries = [...Dashboard.panels.entries()]
      .map(([id, el]) => ({ id, el, score: scores[id] || 0 }));
    entries.sort((a, b) => b.score - a.score);
    const fragment = document.createDocumentFragment();
    for (const { el } of entries) fragment.appendChild(el);
    Dashboard.grid.appendChild(fragment);
    tracker.initObserver();
  }
  static _updateIndicators() {
    const scores = tracker.getAllScores();
    for (const [id, el] of Dashboard.panels) {
      const indicator = el.querySelector('.indicator');
      const score = scores[id] || 0;
      if (indicator) {
        indicator.classList.remove('hot', 'warm', 'cold');
        if (score > 2) indicator.classList.add('hot');
        else if (score > 0.5) indicator.classList.add('warm');
        else indicator.classList.add('cold');
      }
      const badge = el.querySelector('.rank-badge');
      if (badge) {
        const sorted = Object.entries(scores).sort((a,b) => b[1]-a[1]);
        const rank = sorted.findIndex(([i]) => i === id) + 1;
        badge.textContent = '#' + (rank || '--');
      }
    }
  }
  static _startScorePolling() {
    setInterval(() => {
      Dashboard._updateIndicators();
    }, 5000);
  }
  static forceLayout() {
    tracker.flushViews();
    bus.emit('layout-changed', {});
  }
  static resetLayout() {
    tracker.reset();
    layoutEngine.reset();
    for (const [id, el] of Dashboard.panels) {
      el.classList.remove('locked');
      const btn = el.querySelector('.lock-btn');
      if (btn) { btn.classList.remove('active'); btn.textContent = '\u{1F513}'; }
    }
    Dashboard._applyLayout();
    Dashboard._updateIndicators();
  }
  static toggleDebug() {
    const dbg = document.getElementById('debug');
    dbg.classList.toggle('visible');
    if (dbg.classList.contains('visible')) {
      const scores = tracker.getAllScores();
      const lines = Object.entries(scores)
        .sort((a,b) => b[1]-a[1])
        .map(([id, s]) => `${id}: ${s.toFixed(2)} ${layoutEngine.isLocked(id)?'[LOCKED]':''}`)
      dbg.textContent = 'SCORES (desc):\n' + (lines.join('\n') || 'no data');
    }
  }
}
document.addEventListener('DOMContentLoaded', () => Dashboard.init());
</script>
</body>
</html>