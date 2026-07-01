<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --bg: #0f1117;
  --panel-bg: #1a1d27;
  --panel-border: #2a2d3a;
  --text: #e1e4eb;
  --text-dim: #8b8fa3;
  --accent: #5b8def;
  --accent-glow: rgba(91,141,239,0.25);
  --danger: #ef5b5b;
  --success: #4caf7d;
  --warn: #f0a040;
  --overlay: rgba(0,0,0,0.6);
  --radius: 10px;
  --transition: 0.3s cubic-bezier(0.4,0,0.2,1);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,sans-serif;min-height:100vh;overflow-x:hidden}
header{display:flex;align-items:center;justify-content:space-between;padding:14px 24px;border-bottom:1px solid var(--panel-border);flex-wrap:wrap;gap:10px}
header h1{font-size:1.2rem;font-weight:600;letter-spacing:-0.01em}
.toolbar{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.btn{padding:7px 14px;border:1px solid var(--panel-border);border-radius:6px;background:var(--panel-bg);color:var(--text);cursor:pointer;font-size:0.82rem;transition:var(--transition)}
.btn:hover{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-glow)}
.btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
#grid{display:grid;gap:12px;padding:16px;transition:var(--transition)}
.panel{background:var(--panel-bg);border:1px solid var(--panel-border);border-radius:var(--radius);overflow:hidden;transition:var(--transition);position:relative;display:flex;flex-direction:column}
.panel.dominant{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-glow),0 4px 24px rgba(91,141,239,0.15)}
.panel.compact{min-height:52px;max-height:52px;cursor:pointer}
.panel.compact .panel-body{display:none}
.panel.compact .panel-preview{display:flex}
.panel.compact .panel-score{display:inline}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-bottom:1px solid var(--panel-border);gap:8px;flex-shrink:0}
.panel-title{font-size:0.88rem;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-actions{display:flex;gap:4px;align-items:center}
.panel-actions button{background:none;border:none;color:var(--text-dim);cursor:pointer;padding:4px 6px;border-radius:4px;font-size:0.75rem;transition:var(--transition)}
.panel-actions button:hover{color:var(--text);background:rgba(255,255,255,0.06)}
.panel-actions button.locked{color:var(--warn)}
.panel-body{padding:12px 14px;flex:1;display:flex;flex-direction:column;gap:8px;overflow:hidden}
.panel-preview{display:none;align-items:center;gap:8px;padding:0 14px;height:52px}
.panel-preview .preview-value{font-size:1rem;font-weight:700}
.panel-preview .preview-label{font-size:0.72rem;color:var(--text-dim)}
.panel-score{font-size:0.68rem;color:var(--text-dim);display:none}
.metric-row{display:flex;align-items:center;justify-content:space-between;gap:8px}
.metric-label{font-size:0.76rem;color:var(--text-dim)}
.metric-value{font-size:0.9rem;font-weight:600;font-variant-numeric:tabular-nums}
.metric-bar{height:4px;border-radius:2px;background:var(--panel-border);overflow:hidden;flex-shrink:0}
.metric-bar-fill{height:100%;border-radius:2px;transition:width 0.6s ease}
.fill-accent{background:var(--accent)}.fill-success{background:var(--success)}.fill-danger{background:var(--danger)}.fill-warn{background:var(--warn)}
.chart-container{position:relative;flex:1;min-height:0}
.chart-container canvas{width:100%;height:100%}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-glow),0 0 40px var(--accent-glow)}
.drag-handle{cursor:grab;color:var(--text-dim);font-size:0.8rem;user-select:none;padding:0 2px}
.drag-handle:active{cursor:grabbing}
.panel.dragging{opacity:0.5;transform:scale(0.97)}
footer{text-align:center;padding:16px;color:var(--text-dim);font-size:0.72rem;border-top:1px solid var(--panel-border);margin-top:8px}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
.updating{animation:pulse 0.3s ease}
</style>
</head>
<body>
<header>
  <h1>Adaptive Metric Layout</h1>
  <div class="toolbar">
    <button class="btn" id="btnReset" title="Reset all tracking data and layout">Reset Layout</button>
    <button class="btn" id="btnFreeze" title="Pause auto-rearrangement">Freeze</button>
    <span style="font-size:0.72rem;color:var(--text-dim)" id="statusText">Active</span>
  </div>
</header>
<div id="grid"></div>
<footer>Panels auto-arrange by attention score. Drag to override. Lock to pin.</footer>
<script>
// ===== METRIC SOURCE INTERFACE =====
// Pluggable: pass url, wsUrl, or callback. Falls back to realistic simulation with trend.
class MetricSource {
  constructor(config) {
    this.url = config.url || null;
    this.wsUrl = config.wsUrl || null;
    this.callback = config.callback || null;
    this.interval = config.interval || 3000;
    this._timer = null;
    this._ws = null;
    this._listeners = new Set();
    this._lastValues = {};
    this._trend = {};
  }
  onData(fn) { this._listeners.add(fn); return () => this._listeners.delete(fn); }
  _emit(panelId, data) { for (const fn of this._listeners) fn(panelId, data); }
  start(panelIds) {
    if (this.url) {
      this._timer = setInterval(async () => {
        try {
          const res = await fetch(this.url);
          const json = await res.json();
          for (const pid of panelIds) if (json[pid]) this._emit(pid, json[pid]);
        } catch(e) { /* silent */ }
      }, this.interval);
    } else if (this.wsUrl) {
      this._ws = new WebSocket(this.wsUrl);
      this._ws.onmessage = (e) => {
        try {
          const json = JSON.parse(e.data);
          for (const pid of panelIds) if (json[pid]) this._emit(pid, json[pid]);
        } catch(ex) {}
      };
    } else if (this.callback) {
      this._timer = setInterval(async () => {
        const data = await this.callback();
        for (const pid of panelIds) if (data[pid]) this._emit(pid, data[pid]);
      }, this.interval);
    } else {
      this._timer = setInterval(() => {
        for (const pid of panelIds) this._emit(pid, this._generate(pid));
      }, this.interval);
    }
  }
  stop() {
    if (this._timer) { clearInterval(this._timer); this._timer = null; }
    if (this._ws) { this._ws.close(); this._ws = null; }
  }
  _generate(panelId) {
    if (!this._lastValues[panelId]) {
      this._lastValues[panelId] = {};
      this._trend[panelId] = {};
    }
    const prev = this._lastValues[panelId];
    const trend = this._trend[panelId];
    const walk = (key, min, max, step) => {
      if (trend[key] === undefined) trend[key] = (Math.random() - 0.5) * step;
      prev[key] = (prev[key] || (min + max) / 2) + trend[key];
      if (prev[key] > max || prev[key] < min) trend[key] *= -1;
      prev[key] += (Math.random() - 0.5) * step * 0.3;
      return Math.round(prev[key] * 10) / 10;
    };
    switch(panelId) {
      case 'cpu': return { usage: walk('usage', 10, 95, 8), temp: walk('temp', 35, 85, 2), cores: 8, processes: Math.floor(walk('proc', 120, 400, 15)) };
      case 'memory': return { used: walk('used', 2, 15.5, 0.5), total: 16, swap: walk('swap', 0, 4, 0.2), cached: walk('cached', 1, 8, 0.3) };
      case 'network': return { rx: walk('rx', 0.5, 950, 80), tx: walk('tx', 0.2, 400, 40), connections: Math.floor(walk('conn', 20, 500, 30)), latency: walk('lat', 2, 120, 8) };
      case 'disk': return { read: walk('read', 5, 500, 40), write: walk('write', 2, 300, 30), iops: Math.floor(walk('iops', 100, 8000, 600)), util: walk('util', 5, 98, 7) };
      case 'api': return { latency: walk('lat2', 15, 350, 25), rate: walk('rate', 50, 2000, 150), errors: walk('err', 0.01, 5, 0.4), p99: walk('p99', 50, 800, 60) };
      case 'errors': return { total: Math.floor(walk('tot', 0, 50, 4)), critical: Math.floor(walk('crit', 0, 8, 1)), rate: walk('erate', 0.01, 3, 0.2), mtbf: walk('mtbf', 1, 720, 50) };
      default: return {};
    }
  }
}
// ===== LAYOUT ENGINE =====
// ALL expand/collapse/reset MUST go through reconcile()
class LayoutEngine {
  constructor() {
    this._panels = new Map();
    this._scores = new Map();
    this._locked = new Set();
    this._positions = new Map();
    this._frozen = false;
    this._onChange = null;
  }
  onChange(fn) { this._onChange = fn; }
  register(id, config) { this._panels.set(id, config); this._scores.set(id, 0); this._positions.set(id, null); }
  getScore(id) { return this._scores.get(id) || 0; }
  isLocked(id) { return this._locked.has(id); }
  isFrozen() { return this._frozen; }
  // PRIMARY API: all state mutations go through reconcile
  reconcile(action, payload) {
    switch(action) {
      case 'track_view': this._trackView(payload.panelId, payload.duration); break;
      case 'track_interact': this._trackInteract(payload.panelId); break;
      case 'lock': this._locked.add(payload.panelId); break;
      case 'unlock': this._locked.delete(payload.panelId); break;
      case 'freeze': this._frozen = true; break;
      case 'unfreeze': this._frozen = false; break;
      case 'move': this._positions.set(payload.panelId, payload.index); break;
      case 'reset': this._reset(); break;
      case 'compact': this._panels.get(payload.panelId).compacted = true; break;
      case 'expand': this._panels.get(payload.panelId).compacted = false; break;
      default: return null;
    }
    const layout = this._computeLayout();
    if (this._onChange) this._onChange(layout);
    return layout;
  }
  _trackView(panelId, durationMs) {
    const s = this._scores.get(panelId) || 0;
    const now = Date.now();
    const recency = 1 / (1 + (now - (this._panels.get(panelId)._lastSeen || now)) / 3600000);
    this._scores.set(panelId, s + (durationMs / 1000) * recency);
    this._panels.get(panelId)._lastSeen = now;
  }
  _trackInteract(panelId) {
    const s = this._scores.get(panelId) || 0;
    this._scores.set(panelId, s + 5);
  }
  _reset() {
    for (const [id] of this._scores) this._scores.set(id, 0);
    this._locked.clear();
    this._positions.clear();
    this._frozen = false;
  }
  _computeLayout() {
    const entries = [];
    for (const [id] of this._panels) {
      entries.push({ id, score: this._scores.get(id), locked: this._locked.has(id), pos: this._positions.get(id) });
    }
    const lockedItems = entries.filter(e => e.locked && e.pos !== null).sort((a,b) => a.pos - b.pos);
    const unlocked = entries.filter(e => !e.locked || e.pos === null).sort((a,b) => b.score - a.score);
    const usedPositions = new Set(lockedItems.map(e => e.pos));
    let nextPos = 0;
    for (const item of unlocked) {
      while (usedPositions.has(nextPos)) nextPos++;
      item.pos = nextPos;
      usedPositions.add(nextPos);
    }
    const merged = [...lockedItems, ...unlocked.filter(e => !e.locked || e.pos === null)];
    merged.sort((a,b) => a.pos - b.pos);
    return merged.map((e, i) => {
      const rank = i;
      const size = rank < 2 ? 'dominant' : rank < 4 ? 'normal' : rank < 6 ? 'small' : 'compact';
      return { id: e.id, rank, size, score: e.score, locked: e.locked, position: e.pos };
    });
  }
}
// ===== TRACKING SYSTEM =====
class TrackingSystem {
  constructor(engine) {
    this._engine = engine;
    this._observer = null;
    this._viewTimers = new Map();
    this._interactHandlers = new Map();
  }
  start() {
    this._observer = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        const id = entry.target.dataset.panelId;
        if (!id) continue;
        if (entry.isIntersecting) {
          this._viewTimers.set(id, Date.now());
        } else if (this._viewTimers.has(id)) {
          const duration = Date.now() - this._viewTimers.get(id);
          this._viewTimers.delete(id);
          this._engine.reconcile('track_view', { panelId: id, duration });
        }
      }
    }, { threshold: 0.5 });
    return this;
  }
  observe(el) {
    this._observer.observe(el);
    const id = el.dataset.panelId;
    const handler = () => this._engine.reconcile('track_interact', { panelId: id });
    el.addEventListener('click', handler);
    el.addEventListener('mouseenter', handler);
    this._interactHandlers.set(el, handler);
  }
  unobserve(el) {
    this._observer.unobserve(el);
    const handler = this._interactHandlers.get(el);
    if (handler) {
      el.removeEventListener('click', handler);
      el.removeEventListener('mouseenter', handler);
      this._interactHandlers.delete(el);
    }
    // flush any active view timer
    const id = el.dataset.panelId;
    if (id && this._viewTimers.has(id)) {
      const duration = Date.now() - this._viewTimers.get(id);
      this._viewTimers.delete(id);
      this._engine.reconcile('track_view', { panelId: id, duration });
    }
  }
  stop() {
    if (this._observer) this._observer.disconnect();
    for (const [el, handler] of this._interactHandlers) {
      el.removeEventListener('click', handler);
      el.removeEventListener('mouseenter', handler);
    }
    this._interactHandlers.clear();
  }
}
// ===== DOM RENDERER =====
// Uses targeted element updates — NO innerHTML on whole containers
class DashboardRenderer {
  constructor(engine, gridEl) {
    this._engine = engine;
    this._grid = gridEl;
    this._els = new Map();
    this._metricSource = null;
    this._unsubs = [];
  }
  setMetricSource(src) { this._metricSource = src; }
  createPanel(id, config) {
    // Check existing — NEVER destroy/recreate, update in-place
    let panel = this._els.get(id);
    if (!panel) {
      panel = this._buildPanelDOM(id, config);
      this._grid.appendChild(panel);
      this._els.set(id, panel);
    }
    this._updatePanelContent(id, config);
    return panel;
  }
  _buildPanelDOM(id, config) {
    const panel = document.createElement('div');
    panel.className = 'panel';
    panel.dataset.panelId = id;
    panel.draggable = true;
    const header = document.createElement('div');
    header.className = 'panel-header';
    const dragHandle = document.createElement('span');
    dragHandle.className = 'drag-handle';
    dragHandle.textContent = '⋮⋮';
    const title = document.createElement('span');
    title.className = 'panel-title';
    title.textContent = config.title || id;
    const actions = document.createElement('div');
    actions.className = 'panel-actions';
    const scoreEl = document.createElement('span');
    scoreEl.className = 'panel-score';
    const lockBtn = document.createElement('button');
    lockBtn.textContent = '🔓';
    lockBtn.title = 'Lock position';
    lockBtn.onclick = (e) => {
      e.stopPropagation();
      const locked = !this._engine.isLocked(id);
      this._engine.reconcile(locked ? 'lock' : 'unlock', { panelId: id });
    };
    const compactBtn = document.createElement('button');
    compactBtn.textContent = '⊟';
    compactBtn.title = 'Toggle compact';
    compactBtn.onclick = (e) => {
      e.stopPropagation();
      const isCompact = panel.classList.contains('compact');
      this._engine.reconcile(isCompact ? 'expand' : 'compact', { panelId: id });
    };
    actions.appendChild(scoreEl);
    actions.appendChild(compactBtn);
    actions.appendChild(lockBtn);
    header.appendChild(dragHandle);
    header.appendChild(title);
    header.appendChild(actions);
    const body = document.createElement('div');
    body.className = 'panel-body';
    const preview = document.createElement('div');
    preview.className = 'panel-preview';
    panel.appendChild(header);
    panel.appendChild(body);
    panel.appendChild(preview);
    // Drag and drop
    panel.addEventListener('dragstart', (e) => {
      if (this._engine.isLocked(id)) { e.preventDefault(); return; }
      panel.classList.add('dragging');
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', id);
    });
    panel.addEventListener('dragend', () => panel.classList.remove('dragging'));
    panel.addEventListener('dragover', (e) => { e.preventDefault(); panel.classList.add('drag-over'); });
    panel.addEventListener('dragleave', () => panel.classList.remove('drag-over'));
    panel.addEventListener('drop', (e) => {
      e.preventDefault();
      panel.classList.remove('drag-over');
      const fromId = e.dataTransfer.getData('text/plain');
      if (fromId && fromId !== id) {
        const fromEl = this._els.get(fromId);
        const toEl = panel;
        const children = [...this._grid.children];
        const fromIdx = children.indexOf(fromEl);
        const toIdx = children.indexOf(toEl);
        if (fromIdx !== -1 && toIdx !== -1) {
          this._engine.reconcile('move', { panelId: fromId, index: toIdx });
        }
      }
    });
    return panel;
  }
  applyLayout(layout) {
    if (!layout) return;
    const fragment = document.createDocumentFragment();
    // Map id -> size class
    const sizeMap = {};
    for (const item of layout) sizeMap[item.id] = item.size;
    for (const item of layout) {
      const el = this._els.get(item.id);
      if (!el) continue;
      // Targeted class updates only
      const isDominant = item.size === 'dominant';
      const isCompact = item.size === 'compact';
      if (isDominant !== el.classList.contains('dominant')) {
        el.classList.toggle('dominant', isDominant);
      }
      // Use reconcile for compact/expand
      const currentlyCompact = el.classList.contains('compact');
      if (isCompact !== currentlyCompact) {
        this._engine.reconcile(isCompact ? 'compact' : 'expand', { panelId: item.id });
        el.classList.toggle('compact', isCompact);
      }
      // Update score display
      const scoreEl = el.querySelector('.panel-score');
      if (scoreEl) scoreEl.textContent = `score:${Math.round(item.score)}`;
      // Update lock button
      const lockBtn = el.querySelector('.panel-actions button');
      if (lockBtn) lockBtn.textContent = item.locked ? '🔒' : '🔓';
      if (lockBtn) lockBtn.classList.toggle('locked', item.locked);
      // Update compact button icon
      const compactBtn = lockBtn?.nextElementSibling?.previousElementSibling;
      if (compactBtn) compactBtn.textContent = isCompact ? '⊞' : '⊟';
      fragment.appendChild(el);
    }
    // Efficient reorder: replaceChildren preserves references, no cloneNode
    this._grid.replaceChildren(fragment);
    // Update grid template
    const total = layout.length;
    const dominantCount = layout.filter(l => l.size === 'dominant').length;
    const compactCount = layout.filter(l => l.size === 'compact').length;
    if (dominantCount >= 2 && total >= 4) {
      this._grid.style.gridTemplateColumns = '2fr 1fr 1fr';
    } else if (dominantCount >= 1 && total >= 3) {
      this._grid.style.gridTemplateColumns = '1.5fr 1fr 1fr';
    } else {
      this._grid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(280px, 1fr))';
    }
  }
  _updatePanelContent(id, config) {
    const el = this._els.get(id);
    if (!el) return;
    const body = el.querySelector('.panel-body');
    const preview = el.querySelector('.panel-preview');
    if (!body || !preview) return;
    // Build body content based on panel type using targeted DOM construction
    body.replaceChildren(); // clear body only, not the whole panel
    preview.replaceChildren();
    switch(config.type) {
      case 'gauge':
        this._buildGaugeContent(body, preview, config);
        break;
      case 'chart':
        this._buildChartContent(body, preview, config);
        break;
      case 'stats':
      default:
        this._buildStatsContent(body, preview, config);
        break;
    }
  }
  _buildStatsContent(body, preview, config) {
    for (const metric of (config.metrics || [])) {
      const row = document.createElement('div');
      row.className = 'metric-row';
      const label = document.createElement('span');
      label.className = 'metric-label';
      label.textContent = metric.label;
      const value = document.createElement('span');
      value.className = 'metric-value';
      value.dataset.metricKey = metric.key;
      value.textContent = '--';
      row.appendChild(label);
      row.appendChild(value);
      if (metric.showBar) {
        const bar = document.createElement('div');
        bar.className = 'metric-bar';
        const fill = document.createElement('div');
        fill.className = 'metric-bar-fill';
        fill.dataset.metricBar = metric.key;
        bar.appendChild(fill);
        body.appendChild(row);
        body.appendChild(bar);
      } else {
        body.appendChild(row);
      }
    }
    // Preview
    const pv = document.createElement('span');
    pv.className = 'preview-value';
    pv.dataset.previewKey = config.previewKey || config.metrics[0]?.key;
    pv.textContent = '--';
    const pl = document.createElement('span');
    pl.className = 'preview-label';
    pl.textContent = config.previewLabel || config.metrics[0]?.label;
    preview.appendChild(pv);
    preview.appendChild(pl);
  }
  _buildGaugeContent(body, preview, config) {
    const gaugeWrap = document.createElement('div');
    gaugeWrap.style.cssText = 'display:flex;align-items:center;justify-content:center;flex:1;position:relative';
    const canvas = document.createElement('canvas');
    canvas.width = 120; canvas.height = 120;
    canvas.style.cssText = 'width:120px;height:120px';
    canvas.dataset.gaugeKey = config.gaugeKey || 'usage';
    gaugeWrap.appendChild(canvas);
    body.appendChild(gaugeWrap);
    const pv = document.createElement('span');
    pv.className = 'preview-value';
    pv.dataset.previewKey = config.gaugeKey || 'usage';
    pv.textContent = '--';
    const pl = document.createElement('span');
    pl.className = 'preview-label';
    pl.textContent = config.previewLabel || config.title;
    preview.appendChild(pv);
    preview.appendChild(pl);
  }
  _buildChartContent(body, preview, config) {
    const chartWrap = document.createElement('div');
    chartWrap.className = 'chart-container';
    const canvas = document.createElement('canvas');
    canvas.dataset.chartKey = config.chartKey || 'main';
    chartWrap.appendChild(canvas);
    body.appendChild(chartWrap);
    const pv = document.createElement('span');
    pv.className = 'preview-value';
    pv.dataset.previewKey = config.previewKey || 'latest';
    pv.textContent = '--';
    const pl = document.createElement('span');
    pl.className = 'preview-label';
    pl.textContent = config.previewLabel || config.title;
    preview.appendChild(pv);
    preview.appendChild(pl);
  }
  // Targeted metric update — NO innerHTML on containers
  updateMetric(panelId, data) {
    const el = this._els.get(panelId);
    if (!el) return;
    // Update metric values in-place
    for (const [key, val] of Object.entries(data)) {
      const valueEl = el.querySelector(`[data-metric-key="${key}"]`);
      if (valueEl) {
        const formatted = typeof val === 'number' ? (val % 1 ? val.toFixed(1) : val.toLocaleString()) : val;
        if (valueEl.textContent !== formatted) {
          valueEl.textContent = formatted;
          valueEl.classList.add('updating');
          setTimeout(() => valueEl.classList.remove('updating'), 300);
        }
      }
      const barEl = el.querySelector(`[data-metric-bar="${key}"]`);
      if (barEl) {
        const maxMap = { usage: 100, temp: 100, used: 16, total: 16, swap: 8, cached: 8, rx: 1000, tx: 500, conn: 500, lat: 150, read: 500, write: 300, iops: 10000, util: 100, lat2: 400, rate: 2000, err: 5, p99: 1000, tot: 50, crit: 10, erate: 5, mtbf: 1000 };
        const max = maxMap[key] || 100;
        const pct = Math.min(100, Math.max(0, (val / max) * 100));
        barEl.style.width = pct + '%';
        barEl.className = barEl.className.replace(/fill-\w+/g, '');
        barEl.classList.add(pct > 80 ? 'fill-danger' : pct > 60 ? 'fill-warn' : pct > 30 ? 'fill-accent' : 'fill-success');
      }
    }
    // Update gauge canvas if present
    const gaugeCanvas = el.querySelector('canvas[data-gauge-key]');
    if (gaugeCanvas && data[gaugeCanvas.dataset.gaugeKey] !== undefined) {
      this._drawGauge(gaugeCanvas, data[gaugeCanvas.dataset.gaugeKey]);
    }
    // Update chart canvas if present
    const chartCanvas = el.querySelector('canvas[data-chart-key]');
    if (chartCanvas) {
      this._appendChartPoint(chartCanvas, data);
    }
    // Update preview
    const previewKey = Object.keys(data)[0];
    const pv = el.querySelector('[data-preview-key]');
    if (pv && data[previewKey] !== undefined) {
      pv.textContent = typeof data[previewKey] === 'number' ? data[previewKey].toFixed(1) : data[previewKey];
    }
  }
  _drawGauge(canvas, value) {
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    const cx = w/2, cy = h/2, r = 45;
    ctx.clearRect(0, 0, w, h);
    // Background arc
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0.75 * Math.PI, 2.25 * Math.PI);
    ctx.strokeStyle = '#2a2d3a';
    ctx.lineWidth = 8;
    ctx.stroke();
    // Value arc
    const pct = Math.min(100, Math.max(0, value)) / 100;
    const startAngle = 0.75 * Math.PI;
    const endAngle = startAngle + pct * 1.5 * Math.PI;
    ctx.beginPath();
    ctx.arc(cx, cy, r, startAngle, endAngle);
    const grad = ctx.createLinearGradient(0, 0, w, 0);
    grad.addColorStop(0, '#4caf7d'); grad.addColorStop(0.6, '#f0a040'); grad.addColorStop(1, '#ef5b5b');
    ctx.strokeStyle = grad;
    ctx.lineWidth = 8;
    ctx.lineCap = 'round';
    ctx.stroke();
    // Text
    ctx.fillStyle = '#e1e4eb';
    ctx.font = 'bold 16px system-ui';
    ctx.textAlign = 'center';
    ctx.fillText(value.toFixed(1) + '%', cx, cy + 6);
  }
  _appendChartPoint(canvas, data) {
    if (!canvas._history) {
      canvas._history = [];
      canvas._maxPoints = 60;
    }
    const key = Object.keys(data).find(k => typeof data[k] === 'number' && k !== 'total' && k !== 'connections' && k !== 'processes') || Object.keys(data)[0];
    canvas._history.push(data[key]);
    if (canvas._history.length > canvas._maxPoints) canvas._history.shift();
    this._drawLineChart(canvas, canvas._history);
  }
  _drawLineChart(canvas, points) {
    const ctx = canvas.getContext('2d');
    const w = canvas.width || canvas.clientWidth, h = canvas.height || canvas.clientHeight;
    if (!w || !h) return;
    canvas.width = w; canvas.height = h;
    ctx.clearRect(0, 0, w, h);
    const pad = { top: 8, right: 8, bottom: 16, left: 8 };
    const pw = w - pad.left - pad.right;
    const ph = h - pad.top - pad.bottom;
    if (points.length < 2 || pw <= 0 || ph <= 0) return;
    const min = Math.min(...points) * 0.9;
    const max = Math.max(...points) * 1.1;
    const range = max - min || 1;
    const stepX = pw / (points.length - 1);
    // Grid
    ctx.strokeStyle = '#2a2d3a';
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= 3; i++) {
      const y = pad.top + (ph / 3) * i;
      ctx.beginPath();
      ctx.moveTo(pad.left, y);
      ctx.lineTo(pad.left + pw, y);
      ctx.stroke();
    }
    // Line
    ctx.beginPath();
    ctx.strokeStyle = '#5b8def';
    ctx.lineWidth = 2;
    ctx.lineJoin = 'round';
    for (let i = 0; i < points.length; i++) {
      const x = pad.left + stepX * i;
      const y = pad.top + ph - ((points[i] - min) / range) * ph;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
    // Fill
    ctx.lineTo(pad.left + stepX * (points.length - 1), pad.top + ph);
    ctx.lineTo(pad.left, pad.top + ph);
    ctx.closePath();
    const fillGrad = ctx.createLinearGradient(0, pad.top, 0, pad.top + ph);
    fillGrad.addColorStop(0, 'rgba(91,141,239,0.3)');
    fillGrad.addColorStop(1, 'rgba(91,141,239,0.02)');
    ctx.fillStyle = fillGrad;
    ctx.fill();
    // Last value label
    const lastVal = points[points.length - 1];
    ctx.fillStyle = '#e1e4eb';
    ctx.font = '10px system-ui';
    ctx.textAlign = 'right';
    ctx.fillText(lastVal.toFixed(1), pad.left + pw, pad.top + 8);
  }
}
// ===== PERSISTENCE =====
class Persistence {
  static save(key, data) {
    try { localStorage.setItem('aml_' + key, JSON.stringify(data)); } catch(e) {}
  }
  static load(key) {
    try { const v = localStorage.getItem('aml_' + key); return v ? JSON.parse(v) : null; } catch(e) { return null; }
  }
  static saveScores(engine) {
    const data = {};
    for (const [id, score] of engine._scores) data[id] = score;
    this.save('scores', data);
  }
  static loadScores(engine) {
    const data = this.load('scores');
    if (data) for (const [id, score] of Object.entries(data)) engine._scores.set(id, score);
  }
  static saveLocks(engine) {
    this.save('locks', [...engine._locked]);
  }
  static loadLocks(engine) {
    const data = this.load('locks');
    if (data) for (const id of data) engine._locked.add(id);
  }
  static savePositions(engine) {
    const data = {};
    for (const [id, pos] of engine._positions) data[id] = pos;
    this.save('positions', data);
  }
  static loadPositions(engine) {
    const data = this.load('positions');
    if (data) for (const [id, pos] of Object.entries(data)) engine._positions.set(id, pos);
  }
}
// ===== INIT =====
const PANEL_CONFIGS = [
  { id: 'cpu', title: 'CPU Usage', type: 'gauge', gaugeKey: 'usage', previewLabel: 'CPU', metrics: [
    { key: 'usage', label: 'Usage', showBar: true }, { key: 'temp', label: 'Temperature', showBar: true }, { key: 'processes', label: 'Processes' }
  ]},
  { id: 'memory', title: 'Memory', type: 'stats', previewKey: 'used', previewLabel: 'Used GB', metrics: [
    { key: 'used', label: 'Used', showBar: true }, { key: 'cached', label: 'Cached', showBar: true }, { key: 'swap', label: 'Swap' }
  ]},
  { id: 'network', title: 'Network', type: 'chart', chartKey: 'rx', previewKey: 'rx', previewLabel: 'RX Mbps', gaugeKey: 'latency', metrics: [
    { key: 'rx', label: 'RX Mbps', showBar: true }, { key: 'tx', label: 'TX Mbps', showBar: true }, { key: 'latency', label: 'Latency ms' }
  ]},
  { id: 'disk', title: 'Disk I/O', type: 'stats', previewKey: 'iops', previewLabel: 'IOPS', metrics: [
    { key: 'read', label: 'Read MB/s', showBar: true }, { key: 'write', label: 'Write MB/s', showBar: true }, { key: 'util', label: 'Utilization %', showBar: true }
  ]},
  { id: 'api', title: 'API Gateway', type: 'chart', chartKey: 'latency', previewKey: 'rate', previewLabel: 'Req/s', metrics: [
    { key: 'rate', label: 'Requests/s' }, { key: 'latency', label: 'Latency ms', showBar: true }, { key: 'p99', label: 'P99 ms' }
  ]},
  { id: 'errors', title: 'Error Rates', type: 'stats', previewKey: 'total', previewLabel: 'Errors', metrics: [
    { key: 'total', label: 'Total', showBar: true }, { key: 'rate', label: 'Error Rate %', showBar: true }, { key: 'mtbf', label: 'MTBF min' }
  ]}
];
const engine = new LayoutEngine();
const grid = document.getElementById('grid');
const renderer = new DashboardRenderer(engine, grid);
const tracker = new TrackingSystem(engine);
const metricSource = new MetricSource({ interval: 3000 });
// Register panels
for (const cfg of PANEL_CONFIGS) engine.register(cfg.id, cfg);
// Load persisted state
Persistence.loadScores(engine);
Persistence.loadLocks(engine);
Persistence.loadPositions(engine);
// Render panels
renderer.setMetricSource(metricSource);
for (const cfg of PANEL_CONFIGS) {
  const el = renderer.createPanel(cfg.id, cfg);
  tracker.start().observe(el);
}
// Apply initial layout
const initialLayout = engine.reconcile('track_interact', { panelId: 'cpu' });
renderer.applyLayout(initialLayout);
// Auto-save and periodic relayout
setInterval(() => {
  Persistence.saveScores(engine);
  Persistence.saveLocks(engine);
  Persistence.savePositions(engine);
}, 5000);
setInterval(() => {
  if (!engine.isFrozen()) {
    const layout = engine.reconcile('track_view', { panelId: PANEL_CONFIGS[0].id, duration: 0 });
    renderer.applyLayout(layout);
  }
}, 15000);
// Metric updates
metricSource.onData((panelId, data) => {
  renderer.updateMetric(panelId, data);
});
metricSource.start(PANEL_CONFIGS.map(c => c.id));
// Toolbar
document.getElementById('btnReset').onclick = () => {
  engine.reconcile('reset', {});
  localStorage.removeItem('aml_scores');
  localStorage.removeItem('aml_locks');
  localStorage.removeItem('aml_positions');
  renderer.applyLayout(engine.reconcile('track_interact', { panelId: 'cpu' }));
};
let isFrozen = false;
document.getElementById('btnFreeze').onclick = function() {
  isFrozen = !isFrozen;
  engine.reconcile(isFrozen ? 'freeze' : 'unfreeze', {});
  this.textContent = isFrozen ? 'Unfreeze' : 'Freeze';
  this.classList.toggle('active', isFrozen);
  document.getElementById('statusText').textContent = isFrozen ? 'Frozen' : 'Active';
};
// Score decay for recency (run every 60s)
setInterval(() => {
  for (const [id, score] of engine._scores) {
    engine._scores.set(id, score * 0.995);
  }
}, 60000);
</script>
</body>
</html>