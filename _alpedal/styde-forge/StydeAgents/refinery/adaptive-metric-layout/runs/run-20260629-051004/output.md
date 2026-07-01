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
  --text: #e0e0e0;
  --text-muted: #888;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --danger: #ff6b6b;
  --success: #4ecdc4;
  --warn: #ffd93d;
  --compact-scale: 0.45;
  --transition-speed: 380ms;
  --radius: 10px;
  --gap: 12px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}
.toolbar {
  display: flex; gap: 10px; padding: 14px 18px;
  background: #14171f; border-bottom: 1px solid var(--panel-border);
  align-items: center; flex-wrap: wrap; position: sticky; top: 0; z-index: 100;
}
.toolbar button {
  padding: 7px 15px; border: 1px solid var(--panel-border);
  background: var(--panel-bg); color: var(--text); border-radius: 6px;
  cursor: pointer; font-size: 13px; transition: all 0.2s;
}
.toolbar button:hover { border-color: var(--accent); background: #22263a; }
.toolbar button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.toolbar .mode-indicator {
  margin-left: auto; padding: 5px 14px; border-radius: 20px; font-size: 12px;
  font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;
}
.mode-active { background: rgba(78,205,196,0.15); color: var(--success); border: 1px solid rgba(78,205,196,0.3); }
.mode-idle { background: rgba(255,217,61,0.12); color: var(--warn); border: 1px solid rgba(255,217,61,0.3); }
.mode-manual { background: rgba(108,140,255,0.12); color: var(--accent); border: 1px solid rgba(108,140,255,0.3); }
.dashboard {
  display: grid; gap: var(--gap);
  padding: 18px;
  grid-template-columns: repeat(12, 1fr);
  grid-auto-rows: minmax(160px, auto);
  transition: all var(--transition-speed) cubic-bezier(0.4, 0, 0.2, 1);
}
.panel {
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
  border-radius: var(--radius);
  padding: 16px;
  position: relative;
  transition: all var(--transition-speed) cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  display: flex; flex-direction: column;
  min-height: 160px;
}
.panel.high-rank {
  border-color: rgba(108,140,255,0.3);
  box-shadow: 0 0 20px var(--accent-glow);
}
.panel.compact {
  padding: 10px;
  min-height: 80px;
  font-size: 0.82em;
}
.panel.compact .panel-body { display: none; }
.panel.compact .panel-preview { display: flex; }
.panel.compact .panel-controls .btn-expand { display: inline-flex; }
.panel .panel-preview { display: none; flex-direction: column; gap: 4px; font-size: 0.8em; color: var(--text-muted); }
.panel-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 10px; gap: 8px;
}
.panel-header h3 { font-size: 14px; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.panel-controls { display: flex; gap: 4px; flex-shrink: 0; }
.panel-controls button {
  width: 26px; height: 26px; border: 1px solid transparent;
  background: transparent; color: var(--text-muted); border-radius: 5px;
  cursor: pointer; font-size: 14px; display: inline-flex; align-items: center; justify-content: center;
  transition: all 0.15s;
}
.panel-controls button:hover { background: #2a2d3a; color: var(--text); }
.panel-controls .btn-lock.locked { color: var(--warn); border-color: var(--warn); }
.panel-controls .btn-expand { display: none; }
.panel-body { flex: 1; display: flex; align-items: center; justify-content: center; }
.panel-score {
  position: absolute; top: 6px; right: 46px;
  font-size: 10px; color: var(--text-muted); opacity: 0.5;
  pointer-events: none;
}
.metric-chart {
  width: 100%; height: 100%;
  display: flex; align-items: flex-end; gap: 3px;
  padding: 4px 0;
}
.metric-chart .bar {
  flex: 1; background: var(--accent); border-radius: 3px 3px 0 0;
  min-height: 2px; transition: height 0.3s ease;
  opacity: 0.7;
}
.metric-chart .bar:hover { opacity: 1; }
.metric-value {
  font-size: 2em; font-weight: 700; color: var(--accent);
}
.metric-label { font-size: 0.75em; color: var(--text-muted); margin-top: 4px; }
.placeholder-indicator {
  position: absolute; top: 0; right: 0;
  background: var(--warn); color: #000; font-size: 9px;
  padding: 2px 7px; border-radius: 0 0 0 6px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.5px;
}
.collapsed-section {
  grid-column: 1 / -1;
  border-top: 1px dashed var(--panel-border);
  padding: 12px 0;
  display: flex; gap: var(--gap); flex-wrap: wrap;
  align-items: center;
}
.collapsed-section .section-label {
  font-size: 11px; text-transform: uppercase; letter-spacing: 1px;
  color: var(--text-muted); margin-right: 8px;
}
.tooltip {
  position: fixed; background: #1a1d27; border: 1px solid var(--accent);
  padding: 10px 14px; border-radius: 8px; font-size: 12px;
  pointer-events: none; z-index: 200; opacity: 0;
  transition: opacity 0.15s; box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}
.tooltip.visible { opacity: 1; }
@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 12px var(--accent-glow); }
  50% { box-shadow: 0 0 24px rgba(108,140,255,0.3); }
}
.panel.just-updated { animation: pulse-glow 0.6s ease-out; }
</style>
</head>
<body>
<div class="toolbar">
  <button id="btnReset" title="Reset all tracking data">Reset data</button>
  <button id="btnExport" title="Export tracking data as JSON">Export</button>
  <button id="btnAuto" class="active" title="Full auto-layout mode">Auto</button>
  <button id="btnManual" title="Manual override mode">Manual</button>
  <span id="modeIndicator" class="mode-indicator mode-active">Active</span>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="tooltip" id="tooltip"></div>
<script>
(function() {
  'use strict';
  const METRICS = [
    { id: 'cpu',       label: 'CPU Usage',       unit: '%',   range: [10, 95] },
    { id: 'memory',    label: 'Memory',           unit: 'GB',  range: [4, 30] },
    { id: 'disk-io',   label: 'Disk IOPS',        unit: 'K',  range: [50, 800] },
    { id: 'network',   label: 'Network Throughput', unit: 'Mbps', range: [20, 950] },
    { id: 'requests',  label: 'Requests/sec',     unit: '',   range: [100, 5000] },
    { id: 'latency',   label: 'p99 Latency',      unit: 'ms', range: [1, 250] },
    { id: 'errors',    label: 'Error Rate',       unit: '%',  range: [0.01, 5] },
    { id: 'users',     label: 'Active Users',     unit: '',   range: [50, 2000] },
    { id: 'cache',     label: 'Cache Hit Ratio',  unit: '%',  range: [60, 99] },
    { id: 'queue',     label: 'Queue Depth',      unit: '',   range: [0, 500] },
  ];
  const STORAGE_KEY = 'adaptive_dashboard_v2';
  // ── EventBus ──
  const EventBus = {
    _listeners: {},
    on(evt, fn) { (this._listeners[evt] = this._listeners[evt] || []).push(fn); return () => this.off(evt, fn); },
    off(evt, fn) { const ls = this._listeners[evt]; if (ls) { const i = ls.indexOf(fn); if (i >= 0) ls.splice(i, 1); } },
    emit(evt, data) { (this._listeners[evt] || []).forEach(fn => fn(data)); }
  };
  // ── State Machine ──
  const StateMachine = {
    _state: 'active',   // active | idle | manual
    _idleTimer: null,
    _idleTimeout: 30000,
    _pollIntervalId: null,
    _pollActive: false,
    listeners: [],
    get state() { return this._state; },
    transition(newState) {
      if (newState === this._state) return;
      const prev = this._state;
      this._state = newState;
      if (newState === 'manual' || newState === 'idle') this._stopPolling();
      if (newState === 'active') this._startPolling();
      this._resetIdleTimer();
      this.listeners.forEach(fn => fn(prev, newState));
      EventBus.emit('state-change', { from: prev, to: newState });
    },
    _resetIdleTimer() {
      clearTimeout(this._idleTimer);
      if (this._state === 'active') {
        this._idleTimer = setTimeout(() => this.transition('idle'), this._idleTimeout);
      }
    },
    _startPolling() {
      if (this._pollActive) return;
      this._pollActive = true;
    },
    _stopPolling() {
      this._pollActive = false;
      clearTimeout(this._idleTimer);
    },
    userActivity() {
      this._resetIdleTimer();
      if (this._state === 'idle') this.transition('active');
    },
    setManual(on) {
      this.transition(on ? 'manual' : 'active');
    },
    onChange(fn) { this.listeners.push(fn); }
  };
  // ── Interaction Tracker ──
  const Tracker = {
    _data: {},    // panelId -> { interactions: [{type, ts, duration}], totalViewMs, clickCount, expandCount, collapseCount }
    _viewStart: {}, // panelId -> ts
    _visiblePanels: new Set(),
    init() {
      METRICS.forEach(m => {
        this._data[m.id] = {
          interactions: [],
          totalViewMs: 0,
          clickCount: 0,
          expandCount: 0,
          collapseCount: 0,
          lockCount: 0,
        };
      });
    },
    startView(panelId) {
      if (this._viewStart[panelId]) return;
      this._viewStart[panelId] = Date.now();
      this._visiblePanels.add(panelId);
    },
    endView(panelId) {
      if (!this._viewStart[panelId]) return;
      const duration = Date.now() - this._viewStart[panelId];
      this._visiblePanels.delete(panelId);
      delete this._viewStart[panelId];
      this._data[panelId].totalViewMs += duration;
      this._data[panelId].interactions.push({ type: 'view', ts: Date.now(), duration });
      EventBus.emit('tracker-update', { panelId, type: 'view', duration });
    },
    logClick(panelId) {
      if (!this._data[panelId]) return;
      this._data[panelId].clickCount++;
      this._data[panelId].interactions.push({ type: 'click', ts: Date.now() });
      EventBus.emit('tracker-update', { panelId, type: 'click' });
    },
    logExpand(panelId) {
      if (!this._data[panelId]) return;
      this._data[panelId].expandCount++;
      this._data[panelId].interactions.push({ type: 'expand', ts: Date.now() });
      EventBus.emit('tracker-update', { panelId, type: 'expand' });
    },
    logCollapse(panelId) {
      if (!this._data[panelId]) return;
      this._data[panelId].collapseCount++;
      this._data[panelId].interactions.push({ type: 'collapse', ts: Date.now() });
      EventBus.emit('tracker-update', { panelId, type: 'collapse' });
    },
    logLock(panelId) {
      if (!this._data[panelId]) return;
      this._data[panelId].lockCount++;
      this._data[panelId].interactions.push({ type: 'lock', ts: Date.now() });
      EventBus.emit('tracker-update', { panelId, type: 'lock' });
    },
    flushViews() {
      for (const panelId of [...this._visiblePanels]) {
        this.endView(panelId);
        this.startView(panelId);
      }
    },
    export() { return JSON.parse(JSON.stringify(this._data)); },
    import(raw) {
      const d = typeof raw === 'string' ? JSON.parse(raw) : raw;
      Object.keys(d).forEach(k => {
        if (this._data[k]) this._data[k] = d[k];
      });
    },
    getAll() { return this._data; }
  };
  // ── Per-Panel Scorer ──
  const Scorer = {
    WEIGHTS: { view: 1.0, click: 3.0, expand: 2.0, collapse: 0.5, lock: 4.0 },
    BASE_DECAY_LAMBDA: 0.00005,  // per-ms decay factor
    _perPanelLambdas: {},  // panelId -> adjusted lambda
    computeScore(panelId, now) {
      const d = Tracker._data[panelId];
      if (!d || d.interactions.length === 0) return 0;
      now = now || Date.now();
      const lambda = this._perPanelLambdas[panelId] || this.BASE_DECAY_LAMBDA;
      let score = 0;
      for (const ix of d.interactions) {
        const weight = this.WEIGHTS[ix.type] || 1;
        const ageMs = now - ix.ts;
        const recencyDecay = Math.exp(-lambda * ageMs);
        const durationBonus = ix.duration ? Math.log(1 + ix.duration / 1000) : 1;
        score += weight * recencyDecay * durationBonus;
      }
      return score;
    },
    computeAllScores() {
      const now = Date.now();
      const scores = {};
      METRICS.forEach(m => { scores[m.id] = this.computeScore(m.id, now); });
      return scores;
    },
    updatePanelLambda(panelId) {
      const d = Tracker._data[panelId];
      if (!d) return;
      const total = d.clickCount + d.expandCount + d.collapseCount + 1;
      const engagementRatio = (d.clickCount * 3 + d.expandCount * 2) / total;
      this._perPanelLambdas[panelId] = this.BASE_DECAY_LAMBDA * (1 / (1 + engagementRatio));
    },
    recalculateAllLambdas() {
      METRICS.forEach(m => this.updatePanelLambda(m.id));
    }
  };
  // ── Layout Engine ──
  const LayoutEngine = {
    _locked: {},     // panelId -> { row, col, rowSpan, colSpan }
    _collapsed: {},  // panelId -> bool
    _compact: {},    // panelId -> bool
    compute(scores) {
      const sorted = Object.entries(scores)
        .filter(([id]) => !this._collapsed[id])
        .sort(([,a], [,b]) => b - a);
      const layout = [];
      const usedCells = new Set();
      const gridCols = 12;
      const rankConfig = [
        { count: 2, colSpan: 4, rowSpan: 2, cls: 'high-rank' },
        { count: 3, colSpan: 3, rowSpan: 1, cls: '' },
        { count: 3, colSpan: 2, rowSpan: 1, cls: '' },
        { count: 2, colSpan: 2, rowSpan: 1, cls: 'compact' },
      ];
      let idx = 0;
      for (const cfg of rankConfig) {
        for (let c = 0; c < cfg.count && idx < sorted.length; c++, idx++) {
          const [panelId, score] = sorted[idx];
          const isCompact = this._compact[panelId] || cfg.cls === 'compact';
          const pos = this._locked[panelId] || this._findFreeSlot(usedCells, gridCols, isCompact ? 2 : cfg.colSpan, cfg.rowSpan, gridCols);
          if (pos) {
            this._markCells(usedCells, pos.col, pos.row, pos.colSpan, pos.rowSpan, gridCols);
            layout.push({
              id: panelId,
              score,
              col: pos.col, row: pos.row,
              colSpan: pos.colSpan, rowSpan: pos.rowSpan,
              compact: isCompact,
              rankClass: cfg.cls,
            });
            this._locked[panelId] = pos;
          }
        }
      }
      const collapsedPanels = Object.keys(this._collapsed).filter(id => this._collapsed[id]);
      return { panels: layout, collapsed: collapsedPanels };
    },
    _findFreeSlot(used, cols, colSpan, rowSpan, maxCols) {
      for (let row = 1; row <= 20; row++) {
        for (let col = 1; col <= cols - colSpan + 1; col++) {
          if (this._isFree(used, col, row, colSpan, rowSpan)) {
            return { col, row, colSpan, rowSpan };
          }
        }
      }
      return { col: 1, row: Object.keys(used).length + 1, colSpan, rowSpan };
    },
    _isFree(used, col, row, colSpan, rowSpan) {
      for (let r = row; r < row + rowSpan; r++) {
        for (let c = col; c < col + colSpan; c++) {
          if (used.has(`${r}:${c}`)) return false;
        }
      }
      return true;
    },
    _markCells(used, col, row, colSpan, rowSpan) {
      for (let r = row; r < row + rowSpan; r++) {
        for (let c = col; c < col + colSpan; c++) {
          used.add(`${r}:${c}`);
        }
      }
    },
    lockPanel(panelId, pos) { this._locked[panelId] = pos; },
    unlockPanel(panelId) { if (!this._collapsed[panelId]) delete this._locked[panelId]; },
    toggleCollapse(panelId) {
      this._collapsed[panelId] = !this._collapsed[panelId];
      if (this._collapsed[panelId]) delete this._locked[panelId];
    },
    toggleCompact(panelId) { this._compact[panelId] = !this._compact[panelId]; },
    resetAll() {
      this._locked = {};
      this._collapsed = {};
      this._compact = {};
    }
  };
  // ── Adaptation Controller ──
  const AdaptationController = {
    _rafId: null,
    _running: false,
    _dirty: false,
    _throttleMs: 500,
    _lastRun: 0,
    start() {
      if (this._running) return;
      this._running = true;
      this._tick();
    },
    stop() {
      this._running = false;
      if (this._rafId) { cancelAnimationFrame(this._rafId); this._rafId = null; }
    },
    markDirty() { this._dirty = true; },
    _tick() {
      if (!this._running) return;
      this._rafId = requestAnimationFrame(() => {
        const now = Date.now();
        if (this._dirty && now - this._lastRun >= this._throttleMs && StateMachine.state !== 'manual') {
          this._lastRun = now;
          this._dirty = false;
          this._adapt();
        }
        this._tick();
      });
    },
    _adapt() {
      Tracker.flushViews();
      Scorer.recalculateAllLambdas();
      const scores = Scorer.computeAllScores();
      const layout = LayoutEngine.compute(scores);
      EventBus.emit('layout-update', layout);
      EventBus.emit('scores-update', scores);
    }
  };
  // ── Metric Data Provider ──
  const MetricProvider = {
    _data: {},    // panelId -> number[]
    _timers: {},
    USE_PROCEDURAL_FALLBACK: false,
    PLACEHOLDER_ACTIVE: true,
    init() {
      METRICS.forEach(m => {
        this._data[m.id] = this._generateRealisticTrace(m, 40);
      });
    },
    _generateRealisticTrace(metric, count) {
      const [min, max] = metric.range;
      const trace = [];
      let val = min + Math.random() * (max - min) * 0.3;
      for (let i = 0; i < count; i++) {
        const drift = (Math.random() - 0.48) * (max - min) * 0.08;
        const noise = (Math.random() - 0.5) * (max - min) * 0.04;
        val = Math.max(min, Math.min(max, val + drift + noise));
        trace.push(Math.round(val * 100) / 100);
      }
      return trace;
    },
    tick(panelId) {
      if (!this._data[panelId]) return;
      const metric = METRICS.find(m => m.id === panelId);
      if (!metric) return;
      const trace = this._data[panelId];
      const last = trace[trace.length - 1];
      const [min, max] = metric.range;
      const drift = (Math.random() - 0.48) * (max - min) * 0.06;
      const noise = (Math.random() - 0.5) * (max - min) * 0.03;
      let val = Math.max(min, Math.min(max, last + drift + noise));
      val = Math.round(val * 100) / 100;
      trace.push(val);
      if (trace.length > 60) trace.shift();
      EventBus.emit('metric-tick', { panelId, value: val, trace: [...trace] });
    },
    startFeed() {
      METRICS.forEach(m => {
        this._timers[m.id] = setInterval(() => {
          if (StateMachine.state !== 'manual' && StateMachine.state !== 'idle') {
            this.tick(m.id);
          }
        }, 2000 + Math.random() * 2000);
      });
    },
    stopFeed() {
      Object.values(this._timers).forEach(clearInterval);
      this._timers = {};
    }
  };
  // ── Persistence ──
  const Persistence = {
    save() {
      const payload = {
        tracker: Tracker.export(),
        locked: LayoutEngine._locked,
        collapsed: LayoutEngine._collapsed,
        compact: LayoutEngine._compact,
        lambdas: Scorer._perPanelLambdas,
        savedAt: Date.now(),
      };
      try { localStorage.setItem(STORAGE_KEY, JSON.stringify(payload)); } catch(e) {}
    },
    load() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) return false;
        const payload = JSON.parse(raw);
        if (payload.tracker) Tracker.import(payload.tracker);
        if (payload.locked) LayoutEngine._locked = payload.locked;
        if (payload.collapsed) LayoutEngine._collapsed = payload.collapsed;
        if (payload.compact) LayoutEngine._compact = payload.compact;
        if (payload.lambdas) Scorer._perPanelLambdas = payload.lambdas;
        return true;
      } catch(e) { return false; }
    },
    clear() {
      try { localStorage.removeItem(STORAGE_KEY); } catch(e) {}
    }
  };
  // ── Renderer (per-widget, decoupled) ──
  const Renderer = {
    _container: document.getElementById('dashboard'),
    _panelEls: {},   // panelId -> DOM element
    _tooltip: document.getElementById('tooltip'),
    _modeIndicator: document.getElementById('modeIndicator'),
    init() {
      this._container.innerHTML = '';
      METRICS.forEach(m => this._createPanelEl(m));
      this._bindGlobalEvents();
      this._updateModeUI('active');
    },
    _createPanelEl(metric) {
      const el = document.createElement('div');
      el.className = 'panel';
      el.dataset.panelId = metric.id;
      el.innerHTML = `
        <div class="panel-score">-</div>
        <div class="panel-header">
          <h3>${metric.label}</h3>
          <div class="panel-controls">
            <button class="btn-expand" title="Expand">↕</button>
            <button class="btn-compact" title="Toggle compact">⊟</button>
            <button class="btn-lock" title="Lock position">🔒</button>
            <button class="btn-collapse" title="Collapse">×</button>
          </div>
        </div>
        <div class="panel-preview">
          <span class="preview-value">--</span>
          <span class="preview-label">${metric.unit || ''}</span>
        </div>
        <div class="panel-body">
          <div class="metric-chart"></div>
        </div>
        ${MetricProvider.PLACEHOLDER_ACTIVE ? '<div class="placeholder-indicator">CHARTS DISABLED</div>' : ''}
      `;
      this._container.appendChild(el);
      this._panelEls[metric.id] = el;
      this._bindPanelEvents(metric.id, el);
    },
    _bindPanelEvents(panelId, el) {
      el.addEventListener('mouseenter', () => {
        Tracker.startView(panelId);
        StateMachine.userActivity();
      });
      el.addEventListener('mouseleave', () => Tracker.endView(panelId));
      el.addEventListener('click', (e) => {
        if (e.target.closest('button')) return;
        Tracker.logClick(panelId);
        StateMachine.userActivity();
        AdaptationController.markDirty();
      });
      el.querySelector('.btn-lock').addEventListener('click', (e) => {
        e.stopPropagation();
        const btn = el.querySelector('.btn-lock');
        const isLocked = btn.classList.toggle('locked');
        if (isLocked) {
          const style = getComputedStyle(el);
          LayoutEngine.lockPanel(panelId, {
            col: parseInt(style.gridColumnStart) || 1,
            row: parseInt(style.gridRowStart) || 1,
            colSpan: parseInt(style.gridColumnEnd || 3) - parseInt(style.gridColumnStart || 1) || 3,
            rowSpan: parseInt(style.gridRowEnd || 2) - parseInt(style.gridRowStart || 1) || 1,
          });
          Tracker.logLock(panelId);
        } else {
          LayoutEngine.unlockPanel(panelId);
        }
        StateMachine.userActivity();
        AdaptationController.markDirty();
      });
      el.querySelector('.btn-collapse').addEventListener('click', (e) => {
        e.stopPropagation();
        LayoutEngine.toggleCollapse(panelId);
        if (LayoutEngine._collapsed[panelId]) Tracker.logCollapse(panelId);
        else Tracker.logExpand(panelId);
        StateMachine.userActivity();
        AdaptationController.markDirty();
      });
      el.querySelector('.btn-compact').addEventListener('click', (e) => {
        e.stopPropagation();
        LayoutEngine.toggleCompact(panelId);
        StateMachine.userActivity();
        AdaptationController.markDirty();
      });
      el.querySelector('.btn-expand').addEventListener('click', (e) => {
        e.stopPropagation();
        LayoutEngine.toggleCollapse(panelId);
        Tracker.logExpand(panelId);
        StateMachine.userActivity();
        AdaptationController.markDirty();
      });
    },
    _bindGlobalEvents() {
      document.addEventListener('mousemove', () => StateMachine.userActivity());
      document.addEventListener('keydown', () => StateMachine.userActivity());
      document.getElementById('btnReset').addEventListener('click', () => {
        Tracker.init();
        LayoutEngine.resetAll();
        Scorer._perPanelLambdas = {};
        Persistence.clear();
        AdaptationController.markDirty();
      });
      document.getElementById('btnExport').addEventListener('click', () => {
        const data = Persistence.save();
        const blob = new Blob([JSON.stringify({
          tracker: Tracker.export(),
          locked: LayoutEngine._locked,
          collapsed: LayoutEngine._collapsed,
          compact: LayoutEngine._compact,
          lambdas: Scorer._perPanelLambdas,
        }, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = 'dashboard-layout.json'; a.click();
        URL.revokeObjectURL(url);
      });
      document.getElementById('btnAuto').addEventListener('click', () => {
        StateMachine.setManual(false);
        document.getElementById('btnAuto').classList.add('active');
        document.getElementById('btnManual').classList.remove('active');
      });
      document.getElementById('btnManual').addEventListener('click', () => {
        StateMachine.setManual(true);
        document.getElementById('btnManual').classList.add('active');
        document.getElementById('btnAuto').classList.remove('active');
      });
      StateMachine.onChange((from, to) => this._updateModeUI(to));
      EventBus.on('layout-update', (layout) => this._applyLayout(layout));
      EventBus.on('scores-update', (scores) => this._updateScores(scores));
      EventBus.on('metric-tick', ({ panelId, value, trace }) => this._updateMetric(panelId, value, trace));
      this._container.addEventListener('mousemove', (e) => {
        const panelEl = e.target.closest('.panel');
        if (panelEl) {
          const id = panelEl.dataset.panelId;
          const score = Scorer.computeScore(id);
          const d = Tracker._data[id];
          const totalInteractions = d ? d.interactions.length : 0;
          this._tooltip.innerHTML = `Score: ${score.toFixed(2)} | Interactions: ${totalInteractions} | Clicks: ${d?.clickCount || 0}`;
          this._tooltip.classList.add('visible');
          this._tooltip.style.left = (e.clientX + 14) + 'px';
          this._tooltip.style.top = (e.clientY - 50) + 'px';
        } else {
          this._tooltip.classList.remove('visible');
        }
      });
      window.addEventListener('beforeunload', () => Persistence.save());
    },
    _applyLayout(layout) {
      const container = this._container;
      const existingIds = new Set(layout.panels.map(p => p.id));
      METRICS.forEach(m => {
        const el = this._panelEls[m.id];
        if (!el) return;
        if (!existingIds.has(m.id) && !layout.collapsed.includes(m.id)) {
          el.style.display = '';
        }
      });
      layout.panels.forEach(p => {
        const el = this._panelEls[p.id];
        if (!el) return;
        el.style.display = '';
        el.style.gridColumn = `${p.col} / span ${p.colSpan}`;
        el.style.gridRow = `${p.row} / span ${p.rowSpan}`;
        el.classList.toggle('high-rank', p.rankClass === 'high-rank');
        el.classList.toggle('compact', p.compact && p.rankClass !== 'high-rank');
        el.querySelector('.panel-score').textContent = p.score.toFixed(1);
      });
      layout.collapsed.forEach(id => {
        const el = this._panelEls[id];
        if (el) el.style.display = 'none';
      });
      let collapsedSection = container.querySelector('.collapsed-section');
      if (layout.collapsed.length > 0) {
        if (!collapsedSection) {
          collapsedSection = document.createElement('div');
          collapsedSection.className = 'collapsed-section';
          collapsedSection.innerHTML = '<span class="section-label">Collapsed</span>';
          container.appendChild(collapsedSection);
        }
        collapsedSection.querySelectorAll('.collapsed-chip').forEach(c => c.remove());
        layout.collapsed.forEach(id => {
          const metric = METRICS.find(m => m.id === id);
          const chip = document.createElement('button');
          chip.className = 'collapsed-chip';
          chip.style.cssText = 'padding:4px 10px;border:1px solid var(--panel-border);background:var(--panel-bg);color:var(--text-muted);border-radius:14px;cursor:pointer;font-size:11px;';
          chip.textContent = metric ? metric.label : id;
          chip.addEventListener('click', () => {
            LayoutEngine.toggleCollapse(id);
            Tracker.logExpand(id);
            AdaptationController.markDirty();
          });
          collapsedSection.appendChild(chip);
        });
      } else if (collapsedSection) {
        collapsedSection.remove();
      }
    },
    _updateScores(scores) {
      Object.entries(scores).forEach(([id, score]) => {
        const el = this._panelEls[id];
        if (el) {
          const scoreEl = el.querySelector('.panel-score');
          if (scoreEl) scoreEl.textContent = score.toFixed(1);
        }
      });
    },
    _updateMetric(panelId, value, trace) {
      const el = this._panelEls[panelId];
      if (!el) return;
      const previewVal = el.querySelector('.preview-value');
      if (previewVal) previewVal.textContent = value;
      const chartContainer = el.querySelector('.metric-chart');
      if (!chartContainer) return;
      const metric = METRICS.find(m => m.id === panelId);
      const max = metric ? metric.range[1] : Math.max(...trace, 1);
      const bars = chartContainer.children;
      if (bars.length !== trace.length) {
        chartContainer.innerHTML = '';
        trace.forEach(v => {
          const bar = document.createElement('div');
          bar.className = 'bar';
          bar.style.height = Math.max(2, (v / max) * 100) + '%';
          chartContainer.appendChild(bar);
        });
      } else {
        for (let i = 0; i < bars.length; i++) {
          bars[i].style.height = Math.max(2, (trace[i] / max) * 100) + '%';
        }
      }
      el.classList.add('just-updated');
      setTimeout(() => el.classList.remove('just-updated'), 600);
    },
    _updateModeUI(state) {
      this._modeIndicator.textContent = state.charAt(0).toUpperCase() + state.slice(1);
      this._modeIndicator.className = 'mode-indicator mode-' + state;
    }
  };
  // ── Init ──
  Tracker.init();
  MetricProvider.init();
  const restored = Persistence.load();
  Renderer.init();
  AdaptationController.start();
  MetricProvider.startFeed();
  if (restored) {
    AdaptationController.markDirty();
  } else {
    setTimeout(() => AdaptationController.markDirty(), 500);
  }
  setInterval(() => Persistence.save(), 15000);
  window._dashboard = {
    Tracker, Scorer, LayoutEngine, AdaptationController,
    MetricProvider, StateMachine, EventBus, Persistence, Renderer
  };
})();
</script>
</body>
</html>