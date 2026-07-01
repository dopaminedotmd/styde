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
  --surface-hover: #222533;
  --border: #2a2d3a;
  --text: #e1e4ed;
  --text-muted: #8b8fa3;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --rank-1: #6c8cff;
  --rank-2: #7c5ce7;
  --rank-3: #00b894;
  --rank-4: #fdcb6e;
  --rank-5: #e17055;
  --rank-6: #a29bfe;
  --danger: #ff6b6b;
  --success: #00d68f;
  --radius: 10px;
  --transition: 0.35s cubic-bezier(0.4,0,0.2,1);
  --shadow: 0 4px 24px rgba(0,0,0,0.3);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
}
.header h1 {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.3px;
  color: var(--text);
}
.header-controls { display: flex; gap: 10px; align-items: center; }
.btn {
  padding: 8px 16px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.btn:hover { background: var(--surface-hover); border-color: var(--accent); }
.btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
.badge {
  background: var(--accent);
  color: #fff;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
}
.dashboard {
  display: grid;
  gap: 12px;
  padding: 20px;
  grid-template-columns: repeat(6, 1fr);
  grid-auto-rows: minmax(180px, auto);
  max-width: 1600px;
  margin: 0 auto;
  transition: all var(--transition);
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: all var(--transition);
  cursor: default;
  min-height: 180px;
  box-shadow: var(--shadow);
}
.panel:hover { border-color: var(--accent); box-shadow: 0 4px 32px var(--accent-glow); }
.panel.rank-1 { grid-column: span 3; grid-row: span 2; }
.panel.rank-2 { grid-column: span 2; grid-row: span 2; }
.panel.rank-3 { grid-column: span 2; grid-row: span 1; }
.panel.rank-4 { grid-column: span 1; grid-row: span 1; }
.panel.rank-5 { grid-column: span 1; grid-row: span 1; }
.panel.rank-6 { grid-column: span 1; grid-row: span 1; }
.panel.compact {
  grid-column: span 1 !important;
  grid-row: span 1 !important;
  min-height: 100px !important;
  opacity: 0.72;
}
.panel.compact .panel-body { display: none; }
.panel.compact .panel-header { padding: 8px 12px; }
.panel.compact .panel-preview { display: flex; }
.panel.collapsed {
  grid-column: span 1 !important;
  grid-row: span 1 !important;
  min-height: 52px !important;
  opacity: 0.55;
}
.panel.collapsed .panel-body, .panel.collapsed .panel-preview { display: none; }
.panel.collapsed .panel-header { padding: 8px 12px; border-bottom: none; }
.panel.locked { border-color: var(--accent); box-shadow: 0 0 0 1px var(--accent), var(--shadow); }
.panel.locked::after {
  content: 'locked';
  position: absolute;
  top: 8px;
  right: 38px;
  font-size: 10px;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.8px;
  opacity: 0.8;
  pointer-events: none;
}
.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  font-weight: 600;
  font-size: 13px;
  user-select: none;
  cursor: grab;
}
.panel-header:active { cursor: grabbing; }
.panel-title { display: flex; align-items: center; gap: 8px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.panel-title .dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.panel-actions { display: flex; gap: 4px; align-items: center; }
.panel-actions button {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1;
  transition: all 0.12s ease;
}
.panel-actions button:hover { color: var(--text); background: var(--surface-hover); }
.panel-body { flex: 1; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
.panel-preview { display: none; padding: 8px 16px 12px; font-size: 11px; color: var(--text-muted); }
.metric-value { font-size: 36px; font-weight: 700; letter-spacing: -1px; line-height: 1; }
.metric-label { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
.metric-change { font-size: 13px; font-weight: 600; }
.metric-change.up { color: var(--success); }
.metric-change.down { color: var(--danger); }
.chart-bar {
  display: flex;
  align-items: flex-end;
  gap: 4px;
  height: 80px;
  flex: 1;
}
.chart-bar .bar {
  flex: 1;
  background: var(--accent);
  border-radius: 3px 3px 0 0;
  transition: height 0.4s ease;
  min-width: 6px;
  opacity: 0.8;
}
.chart-bar .bar:nth-child(odd) { opacity: 0.6; }
.sparkline {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  height: 50px;
  flex: 1;
}
.sparkline .point {
  flex: 1;
  background: var(--accent);
  border-radius: 2px;
  opacity: 0.7;
  min-height: 2px;
  transition: height 0.3s ease;
}
.heatmap-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.35;
  transition: opacity 0.5s ease;
}
.heatmap-overlay.hidden { opacity: 0; }
.heatmap-cell {
  position: absolute;
  border-radius: 8px;
  transition: background 0.8s ease;
}
.more-section {
  grid-column: 1 / -1;
  background: var(--surface);
  border: 1px dashed var(--border);
  border-radius: var(--radius);
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 13px;
  color: var(--text-muted);
}
.more-section:hover { border-color: var(--accent); color: var(--text); }
.more-section .count { color: var(--accent); font-weight: 600; }
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--surface);
  border: 1px solid var(--accent);
  color: var(--text);
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 13px;
  z-index: 200;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.25s ease;
  pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Dashboard</h1>
  <div class="header-controls">
    <span class="badge" id="sessionBadge">session 0m</span>
    <button class="btn" id="btnReset" title="Reset layout">Reset</button>
    <button class="btn" id="btnHeatmap" title="Toggle heatmap">Heatmap</button>
    <button class="btn" id="btnAuto" title="Toggle auto-arrange">Auto: ON</button>
  </div>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="heatmap-overlay hidden" id="heatmapOverlay"></div>
<div class="toast" id="toast"></div>
<script>
(function() {
  'use strict';
  const STORAGE_KEY = 'adaptive_dashboard_v2';
  const DEBOUNCE_MS = 180;
  const THROTTLE_MS = 250;
  const COMPACT_THRESHOLD = 0.18;
  const COLLAPSE_THRESHOLD = 0.06;
  const DECAY_HALF_LIFE = 1000 * 60 * 30;
  const SAVE_DEBOUNCE_MS = 800;
  const RECALC_THROTTLE_MS = 500;
  const HEATMAP_RESOLUTION = 12;
  const defaultPanels = [
    { id: 'revenue', title: 'Revenue', color: '#6c8cff', data: { value: '$48.2K', change: '+12.5%', dir: 'up', bars: [0.65,0.72,0.58,0.81,0.68,0.75,0.88,0.70,0.79,0.85], spark: [0.3,0.5,0.4,0.7,0.6,0.8,0.65,0.9,0.75,0.85] } },
    { id: 'users', title: 'Active Users', color: '#7c5ce7', data: { value: '2,847', change: '+8.3%', dir: 'up', bars: [0.55,0.68,0.72,0.61,0.79,0.85,0.73,0.81,0.88,0.76], spark: [0.5,0.6,0.55,0.7,0.65,0.8,0.72,0.85,0.78,0.82] } },
    { id: 'latency', title: 'API Latency', color: '#00b894', data: { value: '142ms', change: '-5.1%', dir: 'down', bars: [0.42,0.38,0.45,0.35,0.40,0.33,0.37,0.31,0.34,0.29], spark: [0.8,0.7,0.6,0.5,0.45,0.4,0.42,0.35,0.38,0.32] } },
    { id: 'errors', title: 'Error Rate', color: '#e17055', data: { value: '0.12%', change: '-0.03%', dir: 'down', bars: [0.15,0.18,0.12,0.14,0.11,0.13,0.09,0.10,0.08,0.07], spark: [0.3,0.25,0.2,0.18,0.15,0.14,0.13,0.11,0.10,0.08] } },
    { id: 'storage', title: 'Storage', color: '#fdcb6e', data: { value: '74.2GB', change: '+2.8%', dir: 'up', bars: [0.60,0.63,0.65,0.68,0.70,0.72,0.71,0.74,0.73,0.76], spark: [0.4,0.45,0.5,0.55,0.6,0.62,0.65,0.7,0.72,0.74] } },
    { id: 'throughput', title: 'Throughput', color: '#a29bfe', data: { value: '3.2K/s', change: '+15.2%', dir: 'up', bars: [0.70,0.75,0.68,0.82,0.78,0.85,0.80,0.88,0.83,0.90], spark: [0.5,0.55,0.6,0.65,0.7,0.75,0.78,0.82,0.85,0.88] } },
  ];
  let state = loadState();
  let panelEls = {};
  let sessionStart = Date.now();
  let autoArrange = true;
  let heatmapVisible = false;
  let heatmapData = initHeatmap();
  let resizeObserver = null;
  let intersectionObserver = null;
  let visibilityMap = {};
  let dirty = false;
  let saveTimer = null;
  let recalcTimer = null;
  let debounceTimers = {};
  let throttleTimers = {};
  let interactionQueue = [];
  function db(key, ms) {
    return function(fn) {
      return function(...args) {
        if (debounceTimers[key]) clearTimeout(debounceTimers[key]);
        debounceTimers[key] = setTimeout(() => { delete debounceTimers[key]; fn.apply(this, args); }, ms);
      };
    };
  }
  function th(key, ms) {
    return function(fn) {
      return function(...args) {
        if (throttleTimers[key]) return;
        throttleTimers[key] = setTimeout(() => { delete throttleTimers[key]; }, ms);
        fn.apply(this, args);
      };
    };
  }
  const debouncedSave = db('save', SAVE_DEBOUNCE_MS)(saveState);
  const throttledRecalc = th('recalc', RECALC_THROTTLE_MS)(recalcAndRender);
  const debouncedHeatmap = db('heatmap', 400)(renderHeatmap);
  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const s = JSON.parse(raw);
        if (s.panels && Array.isArray(s.panels) && s.panels.length === defaultPanels.length) {
          return s;
        }
      }
    } catch(e) {}
    return {
      panels: defaultPanels.map((p, i) => ({
        id: p.id,
        rank: i + 1,
        compact: false,
        collapsed: false,
        locked: false,
        interactions: 0,
        totalViewMs: 0,
        lastInteraction: 0,
        viewStart: null,
      })),
    };
  }
  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch(e) {}
  }
  function initHeatmap() {
    const grid = [];
    for (let r = 0; r < HEATMAP_RESOLUTION; r++) {
      grid[r] = new Float32Array(HEATMAP_RESOLUTION);
    }
    return grid;
  }
  function getPanelState(id) {
    return state.panels.find(p => p.id === id) || null;
  }
  function interactionScore(ps) {
    if (!ps) return 0;
    const now = Date.now();
    const recency = Math.exp(-(now - ps.lastInteraction) / DECAY_HALF_LIFE);
    const freqWeight = Math.log(ps.interactions + 1) + 1;
    const durationWeight = Math.log((ps.totalViewMs / 1000) + 1) + 1;
    return freqWeight * durationWeight * Math.max(recency, 0.05);
  }
  function rankPanels() {
    const scored = state.panels.map(ps => ({ ...ps, score: interactionScore(ps) }));
    scored.sort((a, b) => b.score - a.score);
    scored.forEach((ps, i) => { ps.rank = i + 1; });
    const maxScore = scored[0]?.score || 1;
    scored.forEach(ps => {
      const ratio = ps.score / maxScore;
      if (ratio < COLLAPSE_THRESHOLD && ps.rank > 3) { ps.compact = true; ps.collapsed = true; }
      else if (ratio < COMPACT_THRESHOLD && ps.rank > 2) { ps.compact = true; ps.collapsed = false; }
      else { ps.compact = false; ps.collapsed = false; }
    });
    state.panels = scored;
  }
  function recalcAndRender() {
    if (!autoArrange) return;
    const prev = state.panels.map(p => ({ id: p.id, rank: p.rank, compact: p.compact, collapsed: p.collapsed }));
    rankPanels();
    const changed = state.panels.some((p, i) => {
      return p.rank !== prev[i].rank || p.compact !== prev[i].compact || p.collapsed !== prev[i].collapsed;
    });
    if (changed) {
      applyLayout();
      debouncedSave();
    }
  }
  function applyLayout() {
    const sorted = [...state.panels].sort((a, b) => a.rank - b.rank);
    const dash = document.getElementById('dashboard');
    const fragments = [];
    sorted.forEach(ps => {
      const el = panelEls[ps.id];
      if (!el) return;
      el.className = 'panel';
      el.classList.add('rank-' + Math.min(ps.rank, 6));
      if (ps.compact) el.classList.add('compact');
      if (ps.collapsed) el.classList.add('collapsed');
      if (ps.locked) el.classList.add('locked');
      const previewEl = el.querySelector('.panel-preview');
      if (previewEl) {
        previewEl.textContent = ps.collapsed ? 'Click to expand' : 'Preview mode — interact to expand';
      }
      fragments.push(el);
    });
    dash.innerHTML = '';
    fragments.forEach(el => dash.appendChild(el));
    const collapsedCount = sorted.filter(p => p.collapsed).length;
    if (collapsedCount > 0) {
      const more = document.createElement('div');
      more.className = 'more-section';
      more.innerHTML = 'Show <span class="count">' + collapsedCount + '</span> hidden panel' + (collapsedCount > 1 ? 's' : '');
      more.addEventListener('click', () => {
        state.panels.forEach(p => { p.collapsed = false; p.compact = false; });
        applyLayout();
        debouncedSave();
        toast('All panels expanded');
      });
      dash.appendChild(more);
    }
    updateHeatmapData();
  }
  function updateHeatmapData() {
    const sorted = [...state.panels].sort((a, b) => a.rank - b.rank);
    sorted.forEach((ps, idx) => {
      const row = Math.floor(idx / 3);
      const col = idx % 3;
      const rStart = Math.floor((row / 4) * HEATMAP_RESOLUTION);
      const rEnd = Math.floor(((row + 1 + (ps.rank <= 2 ? 1 : 0)) / 4) * HEATMAP_RESOLUTION);
      const cStart = Math.floor((col / 3) * HEATMAP_RESOLUTION);
      const cEnd = Math.floor(((col + 1 + (ps.rank === 1 ? 1 : 0)) / 3) * HEATMAP_RESOLUTION);
      const intensity = Math.min(ps.interactions / 30, 1) * 0.7 + 0.05;
      for (let r = rStart; r < Math.min(rEnd, HEATMAP_RESOLUTION); r++) {
        for (let c = cStart; c < Math.min(cEnd, HEATMAP_RESOLUTION); c++) {
          heatmapData[r][c] = Math.max(heatmapData[r][c], intensity);
        }
      }
    });
    for (let r = 0; r < HEATMAP_RESOLUTION; r++) {
      for (let c = 0; c < HEATMAP_RESOLUTION; c++) {
        heatmapData[r][c] *= 0.998;
      }
    }
    if (heatmapVisible) debouncedHeatmap();
  }
  function renderHeatmap() {
    const overlay = document.getElementById('heatmapOverlay');
    const rect = overlay.getBoundingClientRect();
    const w = rect.width || window.innerWidth;
    const h = rect.height || window.innerHeight;
    const cellW = w / HEATMAP_RESOLUTION;
    const cellH = h / HEATMAP_RESOLUTION;
    let html = '';
    for (let r = 0; r < HEATMAP_RESOLUTION; r++) {
      for (let c = 0; c < HEATMAP_RESOLUTION; c++) {
        const v = heatmapData[r][c];
        if (v < 0.02) continue;
        const alpha = Math.min(v, 0.55);
        html += '<div class="heatmap-cell" style="left:' + (c * cellW) + 'px;top:' + (r * cellH) + 'px;width:' + cellW + 'px;height:' + cellH + 'px;background:rgba(108,140,255,' + alpha + ')"></div>';
      }
    }
    overlay.innerHTML = html;
  }
  function recordInteraction(panelId, type) {
    const ps = getPanelState(panelId);
    if (!ps) return;
    ps.interactions++;
    ps.lastInteraction = Date.now();
    interactionQueue.push({ id: panelId, type: type, ts: Date.now() });
    if (interactionQueue.length > 50) interactionQueue.shift();
    dirty = true;
    throttledRecalc();
  }
  function startView(panelId) {
    const ps = getPanelState(panelId);
    if (!ps || ps.viewStart) return;
    ps.viewStart = Date.now();
  }
  function endView(panelId) {
    const ps = getPanelState(panelId);
    if (!ps || !ps.viewStart) return;
    ps.totalViewMs += Date.now() - ps.viewStart;
    ps.viewStart = null;
    dirty = true;
    throttledRecalc();
  }
  function toast(msg) {
    const el = document.getElementById('toast');
    el.textContent = msg;
    el.classList.add('show');
    setTimeout(() => el.classList.remove('show'), 2000);
  }
  function togglePanel(panelId, mode) {
    const ps = getPanelState(panelId);
    if (!ps || ps.locked) return;
    if (mode === 'compact') {
      ps.compact = !ps.compact;
      if (!ps.compact) ps.collapsed = false;
    } else if (mode === 'collapse') {
      ps.collapsed = !ps.collapsed;
      if (ps.collapsed) ps.compact = true;
    }
    recordInteraction(panelId, mode);
    applyLayout();
    debouncedSave();
  }
  function lockPanel(panelId) {
    const ps = getPanelState(panelId);
    if (!ps) return;
    ps.locked = !ps.locked;
    const el = panelEls[panelId];
    if (el) {
      if (ps.locked) el.classList.add('locked');
      else el.classList.remove('locked');
    }
    debouncedSave();
    toast(ps.locked ? 'Panel locked' : 'Panel unlocked');
  }
  function buildPanel(dp, ps) {
    const el = document.createElement('div');
    el.className = 'panel rank-' + Math.min(ps.rank, 6);
    if (ps.compact) el.classList.add('compact');
    if (ps.collapsed) el.classList.add('collapsed');
    if (ps.locked) el.classList.add('locked');
    el.setAttribute('data-panel-id', dp.id);
    el.innerHTML =
      '<div class="panel-header">' +
        '<span class="panel-title"><span class="dot" style="background:' + dp.color + '"></span>' + dp.title + '</span>' +
        '<span class="panel-actions">' +
          '<button class="btn-compact" title="Compact mode">⊟</button>' +
          '<button class="btn-collapse" title="Collapse">⊖</button>' +
          '<button class="btn-lock" title="Lock position">' + (ps.locked ? 'locked' : 'unlocked') + '</button>' +
        '</span>' +
      '</div>' +
      '<div class="panel-preview">' + (ps.collapsed ? 'Click to expand' : 'Preview — interact to expand') + '</div>' +
      '<div class="panel-body">' +
        '<div class="metric-value">' + dp.data.value + '</div>' +
        '<div class="metric-label">' + dp.title + ' <span class="metric-change ' + dp.data.dir + '">' + dp.data.change + '</span></div>' +
        '<div class="chart-bar">' + dp.data.bars.map(v => '<div class="bar" style="height:' + (v * 100) + '%"></div>').join('') + '</div>' +
        '<div class="sparkline">' + dp.data.spark.map(v => '<div class="point" style="height:' + (v * 100) + '%"></div>').join('') + '</div>' +
      '</div>';
    el.addEventListener('click', function(e) {
      if (e.target.closest('button')) return;
      if (ps.collapsed) { togglePanel(dp.id, 'collapse'); return; }
      if (ps.compact) { togglePanel(dp.id, 'compact'); return; }
      recordInteraction(dp.id, 'click');
    });
    el.addEventListener('mouseenter', function() { startView(dp.id); });
    el.addEventListener('mouseleave', function() { endView(dp.id); });
    const btnCompact = el.querySelector('.btn-compact');
    const btnCollapse = el.querySelector('.btn-collapse');
    const btnLock = el.querySelector('.btn-lock');
    btnCompact.addEventListener('click', function(e) { e.stopPropagation(); togglePanel(dp.id, 'compact'); });
    btnCollapse.addEventListener('click', function(e) { e.stopPropagation(); togglePanel(dp.id, 'collapse'); });
    btnLock.addEventListener('click', function(e) {
      e.stopPropagation();
      lockPanel(dp.id);
      const updatedPs = getPanelState(dp.id);
      btnLock.textContent = updatedPs && updatedPs.locked ? 'locked' : 'unlocked';
    });
    panelEls[dp.id] = el;
    return el;
  }
  function renderAll() {
    const dash = document.getElementById('dashboard');
    dash.innerHTML = '';
    panelEls = {};
    const sorted = [...state.panels].sort((a, b) => a.rank - b.rank);
    sorted.forEach(ps => {
      const dp = defaultPanels.find(p => p.id === ps.id);
      if (!dp) return;
      const el = buildPanel(dp, ps);
      dash.appendChild(el);
    });
    const collapsedCount = sorted.filter(p => p.collapsed).length;
    if (collapsedCount > 0) {
      const more = document.createElement('div');
      more.className = 'more-section';
      more.innerHTML = 'Show <span class="count">' + collapsedCount + '</span> hidden panel' + (collapsedCount > 1 ? 's' : '');
      more.addEventListener('click', () => {
        state.panels.forEach(p => { p.collapsed = false; p.compact = false; });
        renderAll();
        debouncedSave();
        toast('All panels expanded');
      });
      dash.appendChild(more);
    }
    setupObservers();
  }
  function setupObservers() {
    if (resizeObserver) resizeObserver.disconnect();
    if (intersectionObserver) intersectionObserver.disconnect();
    intersectionObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        const id = entry.target.getAttribute('data-panel-id');
        if (!id) return;
        if (entry.isIntersecting) {
          if (!visibilityMap[id]) { visibilityMap[id] = true; startView(id); }
        } else {
          if (visibilityMap[id]) { visibilityMap[id] = false; endView(id); }
        }
      });
    }, { threshold: 0.3 });
    Object.values(panelEls).forEach(function(el) { intersectionObserver.observe(el); });
    resizeObserver = new ResizeObserver(th('resize', 200)(function() {
      if (heatmapVisible) debouncedHeatmap();
    }));
    resizeObserver.observe(document.getElementById('dashboard'));
  }
  function cleanup() {
    if (resizeObserver) { resizeObserver.disconnect(); resizeObserver = null; }
    if (intersectionObserver) { intersectionObserver.disconnect(); intersectionObserver = null; }
    if (saveTimer) clearTimeout(saveTimer);
    if (recalcTimer) clearTimeout(recalcTimer);
    Object.keys(debounceTimers).forEach(function(k) { clearTimeout(debounceTimers[k]); });
    Object.keys(throttleTimers).forEach(function(k) { clearTimeout(throttleTimers[k]); });
    debounceTimers = {};
    throttleTimers = {};
    state.panels.forEach(function(ps) { if (ps.viewStart) { ps.totalViewMs += Date.now() - ps.viewStart; ps.viewStart = null; } });
    saveState();
  }
  function updateSessionTimer() {
    var elapsed = Math.floor((Date.now() - sessionStart) / 60000);
    var badge = document.getElementById('sessionBadge');
    if (badge) badge.textContent = 'session ' + elapsed + 'm';
  }
  document.getElementById('btnReset').addEventListener('click', function() {
    state.panels = defaultPanels.map(function(p, i) { return { id: p.id, rank: i + 1, compact: false, collapsed: false, locked: false, interactions: 0, totalViewMs: 0, lastInteraction: 0, viewStart: null }; });
    heatmapData = initHeatmap();
    renderAll();
    saveState();
    toast('Layout reset');
  });
  document.getElementById('btnHeatmap').addEventListener('click', function() {
    heatmapVisible = !heatmapVisible;
    var overlay = document.getElementById('heatmapOverlay');
    if (heatmapVisible) { overlay.classList.remove('hidden'); renderHeatmap(); this.classList.add('active'); }
    else { overlay.classList.add('hidden'); this.classList.remove('active'); }
  });
  document.getElementById('btnAuto').addEventListener('click', function() {
    autoArrange = !autoArrange;
    this.textContent = 'Auto: ' + (autoArrange ? 'ON' : 'OFF');
    if (!autoArrange) this.classList.remove('active');
    else this.classList.add('active');
    toast(autoArrange ? 'Auto-arrange enabled' : 'Auto-arrange disabled — manual mode');
  });
  setInterval(updateSessionTimer, 30000);
  updateSessionTimer();
  window.addEventListener('beforeunload', cleanup);
  window.addEventListener('pagehide', cleanup);
  document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
      state.panels.forEach(function(ps) { if (ps.viewStart) { ps.totalViewMs += Date.now() - ps.viewStart; ps.viewStart = null; } });
    } else {
      Object.entries(visibilityMap).forEach(function(_a) { var id = _a[0]; var vis = _a[1]; if (vis) startView(id); });
    }
    debouncedSave();
  });
  renderAll();
})();
</script>
</body>
</html>