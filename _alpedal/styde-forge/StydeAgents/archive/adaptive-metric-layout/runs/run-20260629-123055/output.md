<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --border: #30363d;
  --text: #c9d1d9;
  --text-dim: #8b949e;
  --accent: #58a6ff;
  --accent-glow: rgba(88,166,255,0.15);
  --danger: #f85149;
  --success: #3fb950;
  --warning: #d2991d;
  --panel-radius: 8px;
  --transition: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 16px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 8px;
}
.header h1 { font-size: 1.3rem; font-weight: 600; color: var(--text); }
.controls { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.btn {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.82rem;
  transition: background 0.15s;
  white-space: nowrap;
}
.btn:hover { background: #21262d; }
.btn.active { background: var(--accent-glow); border-color: var(--accent); color: var(--accent); }
.stats-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  font-size: 0.78rem;
  color: var(--text-dim);
}
.stat { display: flex; gap: 4px; }
.stat-val { color: var(--accent); font-weight: 600; }
.dashboard {
  display: grid;
  gap: 12px;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(180px, auto);
  transition: grid-template-columns var(--transition), grid-template-rows var(--transition);
}
@media (max-width: 1200px) { .dashboard { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 900px) { .dashboard { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .dashboard { grid-template-columns: 1fr; } }
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--panel-radius);
  padding: 14px;
  position: relative;
  transition: all var(--transition);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 160px;
}
.panel.rank-1 { grid-column: span 2; grid-row: span 2; min-height: 380px; }
.panel.rank-2 { grid-column: span 2; min-height: 280px; }
.panel.rank-3 { grid-column: span 1; min-height: 220px; }
.panel.compact { min-height: 80px; padding: 10px 14px; display: grid; grid-template-columns: 1fr auto; align-items: center; }
.panel.compact .panel-body { display: none; }
.panel.compact .compact-preview { display: flex; }
.panel.locked { border-color: var(--warning); box-shadow: 0 0 0 1px var(--warning); }
.panel.locked::after {
  content: 'LOCKED';
  position: absolute;
  top: 6px;
  right: 42px;
  font-size: 0.6rem;
  color: var(--warning);
  font-weight: 700;
  letter-spacing: 0.05em;
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  flex-shrink: 0;
}
.panel-title { font-weight: 600; font-size: 0.9rem; }
.panel-actions { display: flex; gap: 4px; }
.panel-actions button {
  background: none;
  border: 1px solid transparent;
  color: var(--text-dim);
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
  transition: all 0.15s;
}
.panel-actions button:hover { color: var(--text); border-color: var(--border); }
.panel-actions button.lock-btn.locked { color: var(--warning); }
.panel-body { flex: 1; display: flex; flex-direction: column; gap: 8px; }
.panel-score {
  font-size: 0.7rem;
  color: var(--text-dim);
  margin-top: auto;
  padding-top: 8px;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
}
.compact-preview { display: none; gap: 12px; align-items: center; font-size: 0.78rem; color: var(--text-dim); }
.metric-row { display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem; }
.metric-val { font-weight: 600; font-variant-numeric: tabular-nums; }
.metric-bar {
  height: 6px;
  border-radius: 3px;
  background: var(--border);
  overflow: hidden;
}
.metric-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s ease;
}
.metric-bar-fill.cpu { background: var(--accent); }
.metric-bar-fill.mem { background: var(--success); }
.metric-bar-fill.net { background: var(--warning); }
.metric-bar-fill.disk { background: #bc8cff; }
.chart-mini {
  display: flex;
  align-items: flex-end;
  gap: 2px;
  height: 50px;
  flex: 1;
}
.chart-mini .bar {
  flex: 1;
  background: var(--accent);
  border-radius: 2px 2px 0 0;
  min-height: 2px;
  transition: height 0.3s ease;
}
.heat-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 2px;
}
.heat-dot.hot { background: var(--danger); }
.heat-dot.warm { background: var(--warning); }
.heat-dot.cool { background: var(--accent); }
.heat-dot.cold { background: var(--text-dim); }
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--surface);
  border: 1px solid var(--accent);
  color: var(--text);
  padding: 10px 18px;
  border-radius: 6px;
  font-size: 0.8rem;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.25s ease;
  pointer-events: none;
  z-index: 100;
}
.toast.show { opacity: 1; transform: translateY(0); }
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Metric Dashboard</h1>
  <div class="controls">
    <button class="btn" onclick="resetAll()">Reset Layout</button>
    <button class="btn" onclick="exportData()">Export</button>
    <span style="font-size:0.75rem;color:var(--text-dim)">
      Auto-adapt: <span id="adapt-status">active</span>
    </span>
  </div>
</div>
<div class="stats-bar">
  <div class="stat">Panels: <span class="stat-val" id="stat-panels">8</span></div>
  <div class="stat">Locked: <span class="stat-val" id="stat-locked">0</span></div>
  <div class="stat">Compact: <span class="stat-val" id="stat-compact">0</span></div>
  <div class="stat">Sessions: <span class="stat-val" id="stat-sessions">1</span></div>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="toast" id="toast"></div>
<script>
// ─── STORAGE WITH PER-KEY TTL ───────────────────────────────────
const TTL = {
  scores: 30000,       // 30s — real-time attention scores
  preferences: 300000, // 5min — user preferences, lock state
  layout: 86400000,    // 24h — full layout snapshot
  events: 60000        // 1min — raw event buffer
};
const Storage = {
  set(key, value, category) {
    const entry = { v: value, ts: Date.now(), cat: category || 'scores' };
    try { localStorage.setItem('ad_' + key, JSON.stringify(entry)); } catch(e) {}
  },
  get(key) {
    try {
      const raw = localStorage.getItem('ad_' + key);
      if (!raw) return null;
      const entry = JSON.parse(raw);
      const maxAge = TTL[entry.cat] || TTL.scores;
      if (Date.now() - entry.ts > maxAge) { localStorage.removeItem('ad_' + key); return null; }
      return entry.v;
    } catch(e) { return null; }
  },
  remove(key) { localStorage.removeItem('ad_' + key); },
  keys() {
    const keys = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k.startsWith('ad_')) keys.push(k.slice(3));
    }
    return keys;
  }
};
// ─── PANEL DEFINITIONS ──────────────────────────────────────────
const PANEL_DEFS = [
  { id: 'cpu', title: 'CPU Usage', icon: '⚡', metric: 'cpu', color: '#58a6ff' },
  { id: 'memory', title: 'Memory', icon: '🧠', metric: 'mem', color: '#3fb950' },
  { id: 'network', title: 'Network I/O', icon: '🌐', metric: 'net', color: '#d2991d' },
  { id: 'disk', title: 'Disk Usage', icon: '💾', metric: 'disk', color: '#bc8cff' },
  { id: 'requests', title: 'Requests/sec', icon: '📊', metric: 'req', color: '#f0883e' },
  { id: 'errors', title: 'Error Rate', icon: '🚨', metric: 'err', color: '#f85149' },
  { id: 'latency', title: 'Latency p95', icon: '⏱️', metric: 'lat', color: '#79c0ff' },
  { id: 'active_users', title: 'Active Users', icon: '👥', metric: 'users', color: '#d2a8ff' }
];
// ─── STATE ──────────────────────────────────────────────────────
let state = {
  panels: {},          // { id: { score, frequency, totalDuration, lastInteraction, locked, compact, closed, hiddenDuration, interactions:[] } }
  sessionStart: Date.now(),
  sessionCount: (Storage.get('session_count') || 0) + 1,
  observer: null,
  visiblePanels: new Set(),
  visibilityTimers: new Map(),
  renderQueue: new Set(),
  renderScheduled: false,
  lastRender: 0,
  MIN_RENDER_INTERVAL: 250  // debounce renders; incremental, not fixed 60s
};
// ─── INIT ───────────────────────────────────────────────────────
function initState() {
  Storage.set('session_count', state.sessionCount, 'preferences');
  const saved = Storage.get('panel_state');
  PANEL_DEFS.forEach(def => {
    const savedPanel = saved && saved[def.id];
    state.panels[def.id] = {
      id: def.id,
      score: savedPanel ? savedPanel.score : 50,
      frequency: savedPanel ? savedPanel.frequency : 0,
      totalDuration: savedPanel ? savedPanel.totalDuration : 0,
      lastInteraction: savedPanel ? savedPanel.lastInteraction : Date.now(),
      locked: savedPanel ? savedPanel.locked : false,
      compact: savedPanel ? savedPanel.compact : false,
      closed: false,
      hiddenDuration: 0,
      hideStartTime: null,
      interactions: savedPanel ? savedPanel.interactions : [],
      dataVersion: savedPanel ? savedPanel.dataVersion || 0 : 0
    };
  });
  // Load lock overrides
  const locks = Storage.get('locks');
  if (locks) {
    Object.keys(locks).forEach(id => {
      if (state.panels[id]) {
        state.panels[id].locked = locks[id].locked;
        if (locks[id].compact !== undefined) state.panels[id].compact = locks[id].compact;
      }
    });
  }
}
// ─── SCORING ────────────────────────────────────────────────────
const NOW = () => Date.now();
const HOUR = 3600000;
function computeScore(panel) {
  const now = NOW();
  const age = Math.max(0, now - panel.lastInteraction);
  // Recency decay: half-life of 2 hours
  const recencyFactor = Math.exp(-age * Math.LN2 / (2 * HOUR));
  // Positive signal: frequency × duration × recency
  const positive = (1 + panel.frequency) * (1 + panel.totalDuration / 1000) * (0.1 + recencyFactor);
  // Negative signal decay: hidden/closed panels accumulate penalty, decays over 30min
  const negAge = panel.hideStartTime ? Math.max(0, now - panel.hideStartTime) : 0;
  const negDecay = Math.exp(-negAge * Math.LN2 / (0.5 * HOUR));
  const negative = panel.closed ? 50 * negDecay : panel.hiddenDuration > 10000 ? 20 * negDecay : 0;
  let score = positive - negative;
  // Floor at 1; locked panels keep minimum 5
  score = Math.max(panel.locked ? 5 : 1, score);
  // Cap at 100
  score = Math.min(100, Math.round(score * 10) / 10);
  return score;
}
function updateAllScores() {
  let changed = false;
  Object.values(state.panels).forEach(p => {
    const oldScore = p.score;
    p.score = computeScore(p);
    if (Math.abs(p.score - oldScore) > 0.5) changed = true;
  });
  return changed;
}
// ─── RANKING ────────────────────────────────────────────────────
function getRanked() {
  const panels = Object.values(state.panels).filter(p => !p.closed);
  panels.sort((a, b) => b.score - a.score);
  return panels.map((p, i) => ({ ...p, rank: i + 1 }));
}
// ─── TARGETED DOM UPDATES ───────────────────────────────────────
function renderPanel(panel, rank, container) {
  const def = PANEL_DEFS.find(d => d.id === panel.id);
  let el = container.querySelector(`[data-panel-id="${panel.id}"]`);
  const wasCompact = el ? el.classList.contains('compact') : false;
  const wasLocked = el ? el.classList.contains('locked') : false;
  if (!el) {
    el = document.createElement('div');
    el.className = 'panel';
    el.setAttribute('data-panel-id', panel.id);
    container.appendChild(el);
  }
  // Update rank class
  const rankClass = panel.compact ? 'compact' : `rank-${Math.min(rank, 3)}`;
  el.classList.remove('rank-1', 'rank-2', 'rank-3', 'compact');
  el.classList.add(rankClass);
  if (panel.locked && !el.classList.contains('locked')) el.classList.add('locked');
  if (!panel.locked && el.classList.contains('locked')) el.classList.remove('locked');
  // Only rebuild inner HTML if state changed
  const innerKey = `${panel.id}-${panel.score.toFixed(1)}-${panel.compact}-${panel.locked}-${rank}`;
  if (el.dataset.innerKey !== innerKey) {
    el.dataset.innerKey = innerKey;
    const metricVal = getMetricValue(panel.id);
    el.innerHTML = `
      <div class="panel-header">
        <span class="panel-title">${def.icon} ${def.title}</span>
        <div class="panel-actions">
          <button class="lock-btn${panel.locked ? ' locked' : ''}" onclick="toggleLock('${panel.id}')" title="Lock position">${panel.locked ? '🔒' : '🔓'}</button>
          <button onclick="toggleCompact('${panel.id}')" title="Compact mode">${panel.compact ? '⤢' : '⤡'}</button>
          <button onclick="closePanel('${panel.id}')" title="Hide panel">✕</button>
        </div>
      </div>
      <div class="compact-preview">
        <span>${def.icon} <strong>${def.title}</strong></span>
        <span>${metricVal.text}</span>
        <span style="font-size:0.7rem">score: ${panel.score.toFixed(1)}</span>
      </div>
      <div class="panel-body">
        ${renderPanelBody(panel, def, metricVal)}
      </div>
      <div class="panel-score">
        <span>Score: ${panel.score.toFixed(1)}</span>
        <span>${renderHeatDots(panel.score)}</span>
        <span>Views: ${panel.frequency}</span>
      </div>`;
  }
  return el;
}
function renderPanelBody(panel, def, mv) {
  return `
    <div class="metric-row"><span>Current</span><span class="metric-val">${mv.text}</span></div>
    <div class="metric-bar"><div class="metric-bar-fill ${def.metric}" style="width:${mv.pct}%"></div></div>
    <div class="chart-mini">${renderMiniChart(panel.id, 24)}</div>
    <div class="metric-row"><span>Duration (s)</span><span>${(panel.totalDuration/1000).toFixed(1)}</span></div>
    <div class="metric-row"><span>Last active</span><span>${formatTime(panel.lastInteraction)}</span></div>`;
}
function renderMiniChart(panelId, bars) {
  const vals = getChartData(panelId, bars);
  const max = Math.max(...vals, 1);
  return vals.map(v => {
    const h = Math.max(2, (v / max) * 100);
    return `<div class="bar" style="height:${h}%;background:${v > max*0.8 ? 'var(--danger)' : 'var(--accent)'}"></div>`;
  }).join('');
}
function renderHeatDots(score) {
  if (score >= 80) return '<span class="heat-dot hot"></span><span class="heat-dot hot"></span><span class="heat-dot warm"></span>';
  if (score >= 50) return '<span class="heat-dot warm"></span><span class="heat-dot warm"></span><span class="heat-dot cool"></span>';
  if (score >= 20) return '<span class="heat-dot cool"></span><span class="heat-dot cool"></span><span class="heat-dot cold"></span>';
  return '<span class="heat-dot cold"></span><span class="heat-dot cold"></span><span class="heat-dot cold"></span>';
}
function formatTime(ts) {
  const diff = NOW() - ts;
  if (diff < 60000) return 'just now';
  if (diff < 3600000) return Math.round(diff/60000) + 'm ago';
  return Math.round(diff/3600000) + 'h ago';
}
// ─── SIMULATED METRICS ──────────────────────────────────────────
const metricCache = {};
function getMetricValue(panelId) {
  if (!metricCache[panelId] || NOW() - metricCache[panelId].ts > 2000) {
    const vals = {
      cpu: { text: (Math.random()*60+10).toFixed(0)+'%', pct: Math.random()*60+10 },
      memory: { text: (Math.random()*40+30).toFixed(0)+'%', pct: Math.random()*40+30 },
      network: { text: (Math.random()*800+100).toFixed(0)+' MB/s', pct: Math.random()*60+5 },
      disk: { text: (Math.random()*50+20).toFixed(0)+'%', pct: Math.random()*50+20 },
      requests: { text: Math.floor(Math.random()*2000+200)+'/s', pct: Math.random()*70+10 },
      errors: { text: (Math.random()*4+0.1).toFixed(1)+'%', pct: Math.random()*8 },
      latency: { text: (Math.random()*200+20).toFixed(0)+'ms', pct: Math.random()*30+5 },
      active_users: { text: Math.floor(Math.random()*500+50), pct: Math.random()*80+10 }
    };
    metricCache[panelId] = { ...vals[panelId] || { text: '--', pct: 0 }, ts: NOW() };
  }
  return metricCache[panelId];
}
const chartHistory = {};
function getChartData(panelId, count) {
  if (!chartHistory[panelId]) chartHistory[panelId] = [];
  const h = chartHistory[panelId];
  h.push(Math.random() * 100);
  if (h.length > count) h.shift();
  return h;
}
// ─── INTERACTION TRACKING ───────────────────────────────────────
function trackInteraction(panelId, type) {
  const p = state.panels[panelId];
  if (!p) return;
  p.frequency++;
  p.lastInteraction = NOW();
  p.interactions.push({ type, ts: NOW() });
  // Keep only last 200 interactions
  if (p.interactions.length > 200) p.interactions = p.interactions.slice(-200);
  // If panel was hidden, clear hidden tracking on interaction
  if (p.hideStartTime) {
    p.hiddenDuration += NOW() - p.hideStartTime;
    p.hideStartTime = null;
  }
  if (p.closed) {
    p.closed = false;
    p.hiddenDuration = 0;
  }
  updateAllScores();
  queueRender(panelId);
}
function trackVisibilityChange(panelId, isVisible) {
  const p = state.panels[panelId];
  if (!p || p.closed) return;
  if (isVisible) {
    if (!state.visibilityTimers.has(panelId)) {
      state.visibilityTimers.set(panelId, NOW());
    }
    if (p.hideStartTime) {
      p.hiddenDuration += NOW() - p.hideStartTime;
      p.hideStartTime = null;
    }
  } else {
    if (state.visibilityTimers.has(panelId)) {
      const start = state.visibilityTimers.get(panelId);
      p.totalDuration += NOW() - start;
      state.visibilityTimers.delete(panelId);
    }
    if (!p.hideStartTime) {
      p.hideStartTime = NOW();
    }
    // Negative signal: being hidden reduces score
    updateAllScores();
    queueRender(panelId);
  }
}
// ─── RENDER QUEUE (targeted, debounced) ─────────────────────────
function queueRender(panelId) {
  state.renderQueue.add(panelId);
  if (!state.renderScheduled) {
    state.renderScheduled = true;
    const delay = Math.max(0, state.MIN_RENDER_INTERVAL - (NOW() - state.lastRender));
    setTimeout(flushRender, delay);
  }
}
function flushRender() {
  state.renderScheduled = false;
  state.lastRender = NOW();
  const container = document.getElementById('dashboard');
  if (!container) return;
  const ranked = getRanked();
  // Update scores for changed panels
  if (state.renderQueue.size > 0) {
    updateAllScores();
  }
  // Targeted updates: only re-render panels whose score/rank/compact/locked changed
  const toRender = new Set(state.renderQueue);
  // Also check if any panel's rank changed due to score shifts
  ranked.forEach((rp, idx) => {
    const el = container.querySelector(`[data-panel-id="${rp.id}"]`);
    if (!el || el.dataset.rank !== String(rp.rank) || el.dataset.compact !== String(rp.compact)) {
      toRender.add(rp.id);
    }
  });
  state.renderQueue.clear();
  // Batch DOM updates
  const fragment = document.createDocumentFragment();
  const existingPanels = new Set();
  ranked.forEach(rp => {
    existingPanels.add(rp.id);
    if (toRender.has(rp.id)) {
      renderPanel(rp, rp.rank, container);
    } else {
      // Just update position: move existing element to match new rank order
      const el = container.querySelector(`[data-panel-id="${rp.id}"]`);
      if (el && Array.from(container.children).indexOf(el) !== ranked.indexOf(rp)) {
        container.appendChild(el); // moves to end, we reorder below
      }
    }
  });
  // Remove panels not in ranked list (closed)
  Array.from(container.children).forEach(child => {
    const pid = child.getAttribute('data-panel-id');
    if (pid && !existingPanels.has(pid)) {
      child.remove();
    }
  });
  // Reorder children to match rank order
  ranked.forEach(rp => {
    const el = container.querySelector(`[data-panel-id="${rp.id}"]`);
    if (el && container.lastChild !== el) {
      container.appendChild(el);
    }
  });
  // Persist state (per-item TTL already in Storage)
  persistState();
  updateStats();
}
function persistState() {
  const panelState = {};
  Object.values(state.panels).forEach(p => {
    panelState[p.id] = {
      score: p.score, frequency: p.frequency, totalDuration: p.totalDuration,
      lastInteraction: p.lastInteraction, locked: p.locked, compact: p.compact,
      interactions: p.interactions.slice(-50), dataVersion: (p.dataVersion || 0) + 1
    };
  });
  Storage.set('panel_state', panelState, 'scores');
  const locks = {};
  Object.values(state.panels).forEach(p => {
    if (p.locked || p.compact) locks[p.id] = { locked: p.locked, compact: p.compact };
  });
  Storage.set('locks', locks, 'preferences');
  const layout = {
    ranked: getRanked().map(p => ({ id: p.id, rank: p.rank, score: p.score })),
    ts: NOW()
  };
  Storage.set('layout_snapshot', layout, 'layout');
}
function updateStats() {
  const panels = Object.values(state.panels);
  document.getElementById('stat-panels').textContent = panels.filter(p => !p.closed).length;
  document.getElementById('stat-locked').textContent = panels.filter(p => p.locked).length;
  document.getElementById('stat-compact').textContent = panels.filter(p => p.compact).length;
  document.getElementById('stat-sessions').textContent = state.sessionCount;
}
// ─── MANUAL OVERRIDE ────────────────────────────────────────────
function toggleLock(id) {
  const p = state.panels[id];
  p.locked = !p.locked;
  updateAllScores();
  queueRender(id);
  toast(p.locked ? `Locked: ${PANEL_DEFS.find(d=>d.id===id).title}` : `Unlocked: ${PANEL_DEFS.find(d=>d.id===id).title}`);
}
function toggleCompact(id) {
  const p = state.panels[id];
  p.compact = !p.compact;
  updateAllScores();
  queueRender(id);
  toast(p.compact ? `Compact: ${PANEL_DEFS.find(d=>d.id===id).title}` : `Expanded: ${PANEL_DEFS.find(d=>d.id===id).title}`);
}
function closePanel(id) {
  const p = state.panels[id];
  if (p.locked) { toast('Unlock first to close'); return; }
  p.closed = true;
  p.hideStartTime = NOW();
  updateAllScores();
  queueRender(id);
  toast(`Hidden: ${PANEL_DEFS.find(d=>d.id===id).title} (will reappear if clicked)`);
  // Show a "closed panels" bar if any are closed
  showClosedPanelsBar();
}
function showClosedPanelsBar() {
  const closed = Object.values(state.panels).filter(p => p.closed);
  let bar = document.getElementById('closed-bar');
  if (closed.length === 0) {
    if (bar) bar.remove();
    return;
  }
  if (!bar) {
    bar = document.createElement('div');
    bar.id = 'closed-bar';
    bar.style.cssText = 'display:flex;gap:8px;padding:8px 0;flex-wrap:wrap';
    const db = document.getElementById('dashboard');
    db.parentNode.insertBefore(bar, db);
  }
  bar.innerHTML = closed.map(p => {
    const def = PANEL_DEFS.find(d => d.id === p.id);
    return `<button class="btn" onclick="restorePanel('${p.id}')" style="font-size:0.75rem">${def.icon} ${def.title} (restore)</button>`;
  }).join('');
}
function restorePanel(id) {
  const p = state.panels[id];
  p.closed = false;
  p.hiddenDuration = 0;
  p.hideStartTime = null;
  p.frequency++; // restoration counts as interaction
  p.lastInteraction = NOW();
  updateAllScores();
  queueRender(id);
  showClosedPanelsBar();
}
function resetAll() {
  Object.values(state.panels).forEach(p => {
    p.score = 50;
    p.frequency = 0;
    p.totalDuration = 0;
    p.lastInteraction = NOW();
    p.locked = false;
    p.compact = false;
    p.closed = false;
    p.hiddenDuration = 0;
    p.hideStartTime = null;
    p.interactions = [];
    p.dataVersion = 0;
  });
  Storage.remove('panel_state');
  Storage.remove('locks');
  Storage.remove('layout_snapshot');
  const container = document.getElementById('dashboard');
  container.innerHTML = '';
  state.renderQueue = new Set(PANEL_DEFS.map(d => d.id));
  flushRender();
  showClosedPanelsBar();
  toast('Layout reset to defaults');
}
function exportData() {
  const data = {
    panels: state.panels,
    sessionCount: state.sessionCount,
    sessionUptime: Math.round((NOW() - state.sessionStart) / 1000),
    exported: new Date().toISOString()
  };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `dashboard-export-${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
  toast('Exported tracking data');
}
function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._timeout);
  el._timeout = setTimeout(() => el.classList.remove('show'), 2000);
}
// ─── INTERSECTION OBSERVER ──────────────────────────────────────
function setupObserver() {
  if (state.observer) state.observer.disconnect();
  state.observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const pid = entry.target.getAttribute('data-panel-id');
      if (!pid) return;
      const wasVisible = state.visiblePanels.has(pid);
      const isVisible = entry.isIntersecting;
      if (wasVisible !== isVisible) {
        if (isVisible) {
          state.visiblePanels.add(pid);
        } else {
          state.visiblePanels.delete(pid);
        }
        trackVisibilityChange(pid, isVisible);
      }
    });
  }, { threshold: [0, 0.25, 0.5, 0.75, 1] });
  // Observe existing panels
  document.querySelectorAll('[data-panel-id]').forEach(el => {
    state.observer.observe(el);
  });
  // MutationObserver to catch new panels added by render
  const mo = new MutationObserver(mutations => {
    mutations.forEach(m => {
      m.addedNodes.forEach(node => {
        if (node.nodeType === 1 && node.hasAttribute && node.hasAttribute('data-panel-id')) {
          state.observer.observe(node);
          // Set up interaction listeners on new panel
          setupPanelListeners(node);
        }
        if (node.nodeType === 1 && node.querySelectorAll) {
          node.querySelectorAll('[data-panel-id]').forEach(el => {
            state.observer.observe(el);
            setupPanelListeners(el);
          });
        }
      });
    });
  });
  mo.observe(document.getElementById('dashboard'), { childList: true, subtree: true });
}
function setupPanelListeners(el) {
  const pid = el.getAttribute('data-panel-id');
  if (!pid || el.dataset.listenersSetup) return;
  el.dataset.listenersSetup = '1';
  el.addEventListener('click', (e) => {
    // Don't track clicks on action buttons (they call their own trackInteraction)
    if (e.target.closest('.panel-actions')) return;
    trackInteraction(pid, 'click');
  });
  el.addEventListener('mouseenter', () => trackInteraction(pid, 'hover'));
  el.addEventListener('focusin', () => trackInteraction(pid, 'focus'));
  // Scroll tracking within panel
  const scrollable = el.querySelector('.panel-body');
  if (scrollable) {
    scrollable.addEventListener('scroll', () => trackInteraction(pid, 'scroll'), { passive: true });
  }
}
// ─── GLOBAL CLICK TRACKING (closed panels restoration) ──────────
document.addEventListener('click', (e) => {
  // Check if click is on a closed-panel restore button
  const restoreBtn = e.target.closest('[onclick*="restorePanel"]');
  if (restoreBtn) return; // handled by onclick
});
// ─── PERIODIC CLEANUP ───────────────────────────────────────────
function periodicCleanup() {
  // Flush visibility timers into duration
  state.visibilityTimers.forEach((start, panelId) => {
    const p = state.panels[panelId];
    if (p) {
      p.totalDuration += NOW() - start;
      state.visibilityTimers.set(panelId, NOW());
    }
  });
  updateAllScores();
  // Check if any panel needs compact auto-toggle
  Object.values(state.panels).forEach(p => {
    if (!p.locked) {
      const shouldCompact = p.score < 15 && !p.compact && p.frequency > 0;
      const shouldExpand = p.score > 30 && p.compact;
      if (shouldCompact || shouldExpand) {
        p.compact = shouldCompact;
        queueRender(p.id);
      }
    }
  });
  persistState();
  updateStats();
}
// ─── BOOT ───────────────────────────────────────────────────────
function boot() {
  initState();
  state.renderQueue = new Set(PANEL_DEFS.map(d => d.id));
  flushRender();
  setupObserver();
  updateStats();
  showClosedPanelsBar();
  // Periodic incremental updates (every 10s, not 60s full rebuild)
  setInterval(() => {
    // Update metric cache expiry to force fresh values
    Object.keys(metricCache).forEach(k => {
      if (NOW() - metricCache[k].ts > 3000) delete metricCache[k];
    });
    periodicCleanup();
  }, 10000);
  // Score recalculation every 5s for recency decay
  setInterval(() => {
    if (updateAllScores()) {
      // Queue render for any panel whose score changed significantly
      Object.values(state.panels).forEach(p => {
        if (Math.abs(p.score - (p._lastRenderedScore || 0)) > 2) {
          queueRender(p.id);
          p._lastRenderedScore = p.score;
        }
      });
      persistState();
      updateStats();
    }
  }, 5000);
  console.log('Adaptive Metric Dashboard v1 — targeted DOM, negative-signal decay, per-item TTL');
}
document.addEventListener('DOMContentLoaded', boot);
</script>
</body>
</html>