start_of_file: adaptive_dashboard.html (self-contained, no dependencies)
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --panel-bg: #1a1d2e;
  --panel-border: #2a2d3e;
  --text: #e0e0e0;
  --text-dim: #8888aa;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.15);
  --rank-1: #6c8cff;
  --rank-2: #5cc9a0;
  --rank-3: #f0a060;
  --compact-bg: #141720;
  --heat-low: rgba(108,140,255,0.05);
  --heat-mid: rgba(108,140,255,0.15);
  --heat-high: rgba(108,140,255,0.30);
  --lock-color: #ffb347;
  --transition: 0.4s cubic-bezier(0.25, 0.8, 0.25, 1.2);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  min-height: 100vh;
  overflow-x: hidden;
}
/* Header */
.header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 20px; border-bottom: 1px solid var(--panel-border);
  background: var(--panel-bg); position: sticky; top: 0; z-index: 100;
}
.header h1 { font-size: 1.2rem; font-weight: 600; letter-spacing: 0.02em; }
.header .sub { font-size: 0.75rem; color: var(--text-dim); }
.header .controls { display: flex; gap: 8px; align-items: center; }
.header button {
  background: var(--panel-border); color: var(--text); border: none;
  padding: 6px 14px; border-radius: 6px; cursor: pointer;
  font-size: 0.8rem; transition: background 0.2s;
}
.header button:hover { background: #3a3d5e; }
.header button.active { background: var(--accent); color: #fff; }
/* Grid */
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 200px;
  gap: 12px;
  padding: 16px;
  transition: all var(--transition);
  max-width: 1600px;
  margin: 0 auto;
}
/* Panel */
.panel {
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
  border-radius: 10px;
  overflow: hidden;
  display: flex; flex-direction: column;
  position: relative;
  transition: all var(--transition);
  cursor: default;
}
.panel:hover { border-color: var(--accent); box-shadow: 0 0 20px var(--accent-glow); }
.panel.locked { border-color: var(--lock-color); box-shadow: 0 0 12px rgba(255,179,71,0.12); }
.panel.compact { grid-row: span 1; min-height: 80px; max-height: 120px; }
.panel.expanded { grid-column: span 2; grid-row: span 2; }
.panel.rank-1 { grid-column: span 2; grid-row: span 2; }
.panel.rank-2 { grid-column: span 2; grid-row: span 1; }
.panel.rank-3 { grid-column: span 1; grid-row: span 1; }
.panel.rank-4 { grid-column: span 1; grid-row: span 1; }
.panel.rank-below { grid-column: span 1; grid-row: span 1; }
/* Heatmap overlay */
.panel::after {
  content: ''; position: absolute; inset: 0; pointer-events: none;
  transition: background var(--transition); z-index: 0; border-radius: 10px;
}
.panel.heat-low::after { background: var(--heat-low); }
.panel.heat-mid::after { background: var(--heat-mid); }
.panel.heat-high::after { background: var(--heat-high); }
/* Panel header bar */
.panel-bar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px; background: rgba(0,0,0,0.2);
  border-bottom: 1px solid var(--panel-border); z-index: 1;
  flex-shrink: 0;
}
.panel-bar .title-group { display: flex; align-items: center; gap: 8px; }
.panel-bar .title { font-size: 0.85rem; font-weight: 600; }
.panel-bar .score-badge {
  font-size: 0.65rem; padding: 2px 8px; border-radius: 10px;
  background: var(--panel-border); color: var(--text-dim);
}
.panel-bar .actions { display: flex; gap: 4px; }
.panel-bar button {
  background: transparent; border: none; color: var(--text-dim);
  cursor: pointer; padding: 4px 6px; border-radius: 4px;
  font-size: 0.75rem; transition: all 0.2s;
}
.panel-bar button:hover { background: var(--panel-border); color: var(--text); }
.panel-bar button.lock-btn.locked { color: var(--lock-color); }
.panel-bar .expand-btn { font-size: 0.7rem; }
/* Panel body */
.panel-body {
  flex: 1; padding: 14px; overflow: hidden; z-index: 1;
  display: flex; flex-direction: column; gap: 8px;
}
.compact .panel-body { padding: 8px 14px; flex-direction: row; align-items: center; gap: 12px; }
/* Mini metric display */
.metric-row { display: flex; gap: 16px; flex-wrap: wrap; }
.metric { display: flex; flex-direction: column; gap: 2px; }
.metric .label { font-size: 0.65rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.05em; }
.metric .value { font-size: 1.4rem; font-weight: 700; }
.metric .delta { font-size: 0.7rem; }
.metric .delta.up { color: #5cc9a0; }
.metric .delta.down { color: #f06060; }
/* Mini chart (pure CSS bar) */
.bar-chart { display: flex; align-items: flex-end; gap: 3px; height: 60px; }
.bar-chart .bar {
  flex: 1; background: var(--accent); border-radius: 2px 2px 0 0;
  transition: height 0.5s ease; min-width: 4px; opacity: 0.7;
}
.compact .bar-chart { height: 30px; flex: 1; max-width: 200px; }
/* Sparkline */
.sparkline { display: flex; align-items: flex-end; gap: 1px; height: 50px; }
.sparkline .dot { flex: 1; background: var(--accent); border-radius: 1px; transition: height 0.3s; }
/* Empty state */
.empty-hint { color: var(--text-dim); font-size: 0.8rem; font-style: italic; }
/* Compact preview strip */
.compact-preview { display: flex; align-items: center; gap: 10px; flex: 1; }
.compact-preview .mini-val { font-size: 1.1rem; font-weight: 700; }
.compact-preview .mini-label { font-size: 0.65rem; color: var(--text-dim); }
/* More section */
.more-section { grid-column: 1 / -1; display: none; }
.more-section.visible { display: block; }
.more-section .more-header {
  font-size: 0.8rem; color: var(--text-dim); padding: 8px 0;
  border-top: 1px dashed var(--panel-border); margin-top: 8px;
  cursor: pointer;
}
.more-section .more-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-top: 8px;
}
/* Toast */
.toast {
  position: fixed; bottom: 20px; right: 20px; background: var(--panel-bg);
  border: 1px solid var(--accent); padding: 10px 18px; border-radius: 8px;
  font-size: 0.8rem; z-index: 999; opacity: 0; transform: translateY(10px);
  transition: all 0.3s;
}
.toast.show { opacity: 1; transform: translateY(0); }
/* Responsive */
@media (max-width: 900px) { .grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 500px) { .grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="header">
  <div>
    <h1>Adaptive Dashboard</h1>
    <span class="sub">Layout adjusts to how you use it</span>
  </div>
  <div class="controls">
    <button onclick="resetAll()" title="Reset all tracking and layout">Reset</button>
    <button id="autoBtn" class="active" onclick="toggleAutoMode()">Auto-Layout: ON</button>
  </div>
</div>
<div class="grid" id="grid"></div>
<div class="toast" id="toast"></div>
<script>
// ── DATA ──────────────────────────────────────────
const PANEL_DEFS = [
  { id:'cpu',      title:'CPU Usage',      icon:'⚡', type:'metric',   data:{val:'34%', delta:'+2%', dir:'up',   bars:[45,52,38,60,55,48,42,50,58,44,40,34] }},
  { id:'memory',   title:'Memory',         icon:'🧠', type:'metric',   data:{val:'7.2 GB', delta:'-0.3', dir:'down', bars:[72,68,75,70,65,62,78,71,69,73,70,72] }},
  { id:'disk',     title:'Disk I/O',       icon:'💾', type:'metric',   data:{val:'128 MB/s', delta:'+12', dir:'up',  bars:[80,85,90,82,78,95,100,88,92,86,80,128] }},
  { id:'network',  title:'Network',        icon:'🌐', type:'metric',   data:{val:'2.4 Gbps', delta:'-0.1', dir:'down', bars:[24,22,28,26,30,25,23,27,29,24,22,24] }},
  { id:'users',    title:'Active Users',   icon:'👥', type:'metric',   data:{val:'1,247', delta:'+84', dir:'up',   bars:[900,950,1020,980,1100,1050,1150,1200,1180,1220,1190,1247] }},
  { id:'revenue',  title:'Revenue',        icon:'💰', type:'metric',   data:{val:'$48.2K', delta:'+3.1', dir:'up',  bars:[38,40,42,39,44,46,43,45,47,44,46,48] }},
  { id:'errors',   title:'Error Rate',     icon:'⚠️', type:'metric',   data:{val:'0.12%', delta:'-0.03', dir:'down', bars:[15,12,18,14,11,9,13,10,8,12,11,12] }},
  { id:'latency',  title:'API Latency',    icon:'⏱️', type:'metric',   data:{val:'42ms', delta:'+5', dir:'up',    bars:[35,38,40,37,42,39,41,43,38,40,42,42] }},
  { id:'cache',    title:'Cache Hit Rate', icon:'🎯', type:'metric',   data:{val:'94.2%', delta:'+1.1', dir:'up',  bars:[88,90,91,89,92,93,91,94,92,93,94,94] }},
  { id:'queue',    title:'Queue Depth',    icon:'📊', type:'metric',   data:{val:'18', delta:'-5', dir:'down',   bars:[30,28,25,22,24,20,18,22,19,21,23,18] }},
  { id:'uptime',   title:'Uptime',         icon:'🟢', type:'metric',   data:{val:'99.97%', delta:'+0.01', dir:'up', bars:[99,99,99,99,99,99,99,99,99,99,99,99] }},
  { id:'cost',     title:'Cloud Cost',     icon:'☁️', type:'metric',   data:{val:'$2.1K', delta:'+0.2', dir:'up',  bars:[18,19,20,18,21,22,19,20,21,20,19,21] }},
];
// ── STATE ────────────────────────────────────────
const STORAGE_KEY = 'adaptive_dashboard_v2';
let state = loadState();
let autoMode = state.autoMode !== false;
let viewTimers = {};       // panelId -> { startTime, accumulated }
let interactionCounts = {}; // panelId -> { clicks, hovers, expands }
let observer = null;
let resizeTimer = null;
function defaultState() {
  return {
    scores: {},           // panelId -> number
    locks: {},            // panelId -> boolean
    interactions: {},     // panelId -> { clicks, hovers, expands, lastViewDuration }
    sessionViews: {},     // panelId -> total view seconds
    viewHistory: {},      // panelId -> [timestamps of views]
    manualOrder: null,    // null or [panelId, ...] when manually reordered
    autoMode: true,
  };
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      // Merge with defaults for forward compat
      const def = defaultState();
      for (const k of Object.keys(def)) {
        if (!(k in parsed)) parsed[k] = def[k];
      }
      // Ensure all panel IDs exist in score maps
      for (const p of PANEL_DEFS) {
        if (!(p.id in parsed.scores)) parsed.scores[p.id] = 0;
        if (!(p.id in parsed.locks)) parsed.locks[p.id] = false;
        if (!(p.id in parsed.interactions)) parsed.interactions[p.id] = {clicks:0,hovers:0,expands:0,lastViewDuration:0};
        if (!(p.id in parsed.sessionViews)) parsed.sessionViews[p.id] = 0;
        if (!(p.id in parsed.viewHistory)) parsed.viewHistory[p.id] = [];
      }
      return parsed;
    }
  } catch(e) { console.warn('State load failed, using defaults', e); }
  return defaultState();
}
function saveState() {
  state.autoMode = autoMode;
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e) {}
}
// ── SCORING ──────────────────────────────────────
function computeScore(panelId) {
  const s = state;
  const intr = s.interactions[panelId] || {clicks:0,hovers:0,expands:0,lastViewDuration:0};
  const views = s.sessionViews[panelId] || 0;
  const history = s.viewHistory[panelId] || [];
  // Frequency: total interaction events
  const freq = intr.clicks + intr.hovers * 0.5 + intr.expands * 2;
  // Duration: total view seconds
  const dur = views;
  // Recency: how recently was it viewed (0-1, 1 = viewed in last minute)
  let recency = 0;
  if (history.length > 0) {
    const lastView = Math.max(...history);
    const ageSeconds = (Date.now() - lastView) / 1000;
    recency = Math.max(0, 1 - ageSeconds / 3600); // decays over 1 hour
  }
  // Composite score
  const score = (freq * 0.4 + dur * 0.4) * 10 + recency * 100;
  return Math.round(score * 100) / 100;
}
function recomputeAllScores() {
  for (const p of PANEL_DEFS) {
    state.scores[p.id] = computeScore(p.id);
  }
  saveState();
}
function getRankedPanels() {
  const ranked = PANEL_DEFS.map(p => ({
    ...p,
    score: state.scores[p.id] || 0,
    locked: state.locks[p.id] || false,
  }));
  ranked.sort((a, b) => b.score - a.score);
  return ranked;
}
function getRankClass(rank, total) {
  if (total <= 4) {
    if (rank === 0) return 'rank-1';
    if (rank === 1) return 'rank-2';
    if (rank <= 3) return 'rank-3';
    return 'rank-below';
  }
  const pct = rank / total;
  if (pct < 0.15) return 'rank-1';
  if (pct < 0.35) return 'rank-2';
  if (pct < 0.60) return 'rank-3';
  return 'rank-below';
}
function getHeatClass(score, maxScore) {
  if (maxScore <= 0) return '';
  const ratio = score / maxScore;
  if (ratio > 0.7) return 'heat-high';
  if (ratio > 0.3) return 'heat-mid';
  return 'heat-low';
}
// ── TRACKING ─────────────────────────────────────
function startViewTimer(panelId) {
  if (!viewTimers[panelId]) {
    viewTimers[panelId] = { startTime: Date.now() };
  }
}
function stopViewTimer(panelId) {
  const timer = viewTimers[panelId];
  if (timer && timer.startTime) {
    const elapsed = (Date.now() - timer.startTime) / 1000;
    state.sessionViews[panelId] = (state.sessionViews[panelId] || 0) + elapsed;
    state.viewHistory[panelId] = state.viewHistory[panelId] || [];
    state.viewHistory[panelId].push(Date.now());
    // Keep last 50 view records
    if (state.viewHistory[panelId].length > 50) {
      state.viewHistory[panelId] = state.viewHistory[panelId].slice(-50);
    }
    delete viewTimers[panelId];
    recomputeAllScores();
    if (autoMode) renderGrid();
  }
}
function recordInteraction(panelId, type) {
  const intr = state.interactions[panelId] || {clicks:0,hovers:0,expands:0,lastViewDuration:0};
  intr[type] = (intr[type] || 0) + 1;
  state.interactions[panelId] = intr;
  recomputeAllScores();
}
function setupTracking() {
  // IntersectionObserver for view duration
  if (observer) observer.disconnect();
  observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      const panelId = entry.target.dataset.panelId;
      if (!panelId) continue;
      if (entry.isIntersecting) {
        startViewTimer(panelId);
      } else {
        stopViewTimer(panelId);
      }
    }
  }, { threshold: 0.3 });
  // Observe all panels
  document.querySelectorAll('.panel').forEach(el => observer.observe(el));
  // Click tracking via delegation
  document.getElementById('grid').addEventListener('click', (e) => {
    const panel = e.target.closest('.panel');
    if (!panel) return;
    const panelId = panel.dataset.panelId;
    if (!panelId) return;
    if (e.target.closest('.lock-btn')) {
      toggleLock(panelId);
    } else if (e.target.closest('.expand-btn') || e.target.closest('.compact-preview')) {
      toggleExpand(panelId);
    } else {
      recordInteraction(panelId, 'clicks');
    }
  });
  // Hover tracking (debounced)
  let hoverTimers = {};
  document.getElementById('grid').addEventListener('mouseover', (e) => {
    const panel = e.target.closest('.panel');
    if (!panel) return;
    const panelId = panel.dataset.panelId;
    if (!panelId) return;
    if (hoverTimers[panelId]) return;
    hoverTimers[panelId] = setTimeout(() => {
      recordInteraction(panelId, 'hovers');
      delete hoverTimers[panelId];
    }, 800);
  });
}
// ── ACTIONS ──────────────────────────────────────
function toggleLock(panelId) {
  state.locks[panelId] = !state.locks[panelId];
  saveState();
  renderGrid();
  const action = state.locks[panelId] ? 'locked' : 'unlocked';
  showToast(`${PANEL_DEFS.find(p=>p.id===panelId)?.title} ${action} — manual override ${state.locks[panelId]?'active':'released'}`);
}
function toggleExpand(panelId) {
  recordInteraction(panelId, 'expands');
  // Toggle between compact and expanded by adjusting score temporarily
  const currentScore = state.scores[panelId] || 0;
  // Increase score significantly to force expansion, or drop to force compact
  const panel = document.querySelector(`[data-panel-id="${panelId}"]`);
  const isCompact = panel?.classList.contains('compact');
  if (isCompact) {
    // Boost score temporarily (stored)
    state.sessionViews[panelId] = (state.sessionViews[panelId] || 0) + 30;
    state.viewHistory[panelId].push(Date.now());
  } else {
    // Penalize
    state.sessionViews[panelId] = Math.max(0, (state.sessionViews[panelId] || 0) - 30);
  }
  recomputeAllScores();
  saveState();
  if (autoMode) renderGrid();
  showToast(`${PANEL_DEFS.find(p=>p.id===panelId)?.title} ${isCompact?'expanded':'compacted'}`);
}
function toggleAutoMode() {
  autoMode = !autoMode;
  saveState();
  const btn = document.getElementById('autoBtn');
  btn.textContent = `Auto-Layout: ${autoMode ? 'ON' : 'OFF'}`;
  btn.classList.toggle('active', autoMode);
  renderGrid();
  showToast(`Auto-layout ${autoMode ? 'enabled' : 'disabled — manual mode'}`);
}
function resetAll() {
  if (!confirm('Reset all tracking data and layout preferences?')) return;
  localStorage.removeItem(STORAGE_KEY);
  state = defaultState();
  viewTimers = {};
  interactionCounts = {};
  autoMode = true;
  document.getElementById('autoBtn').textContent = 'Auto-Layout: ON';
  document.getElementById('autoBtn').classList.add('active');
  renderGrid();
  showToast('All data reset');
}
function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toast._timeout);
  toast._timeout = setTimeout(() => toast.classList.remove('show'), 2000);
}
// ── RENDER ───────────────────────────────────────
function renderGrid() {
  const grid = document.getElementById('grid');
  const ranked = getRankedPanels();
  const maxScore = ranked.length > 0 ? Math.max(...ranked.map(p => p.score), 1) : 1;
  // Determine which panels go compact (bottom 25% by score, and not locked)
  const compactThreshold = Math.floor(ranked.length * 0.75);
  const topPanels = [];
  const compactPanels = [];
  for (let i = 0; i < ranked.length; i++) {
    const panel = ranked[i];
    if (i >= compactThreshold && !panel.locked && panel.score < maxScore * 0.2) {
      compactPanels.push({...panel, rank: i});
    } else {
      topPanels.push({...panel, rank: i});
    }
  }
  // Build DOM using DocumentFragment for efficiency
  const frag = document.createDocumentFragment();
  // Render top panels
  for (const panel of topPanels) {
    const el = createPanelElement(panel, maxScore, false, ranked.length);
    frag.appendChild(el);
  }
  // Compact panels in a "more" section
  if (compactPanels.length > 0) {
    const moreSection = document.createElement('div');
    moreSection.className = 'more-section visible';
    moreSection.innerHTML = `<div class="more-header" onclick="this.parentElement.querySelector('.more-grid').classList.toggle('visible'); this.textContent = this.textContent.includes('Show') ? '▼ Compact panels (' + ${compactPanels.length} + ')' : '▲ Hide compact panels';">
      ▼ Compact panels (${compactPanels.length})
    </div>`;
    const moreGrid = document.createElement('div');
    moreGrid.className = 'more-grid visible';
    for (const panel of compactPanels) {
      const el = createPanelElement(panel, maxScore, true, ranked.length);
      moreGrid.appendChild(el);
    }
    moreSection.appendChild(moreGrid);
    frag.appendChild(moreSection);
  }
  // Clear and replace
  grid.innerHTML = '';
  grid.appendChild(frag);
  // Re-attach observers
  setupTracking();
}
function createPanelElement(panel, maxScore, forceCompact, totalPanels) {
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.panelId = panel.id;
  // Rank class
  if (!forceCompact) {
    el.classList.add(getRankClass(panel.rank, totalPanels));
  }
  // Compact class
  if (forceCompact) {
    el.classList.add('compact');
  }
  // Heat class
  const heatClass = getHeatClass(panel.score, maxScore);
  if (heatClass) el.classList.add(heatClass);
  // Lock class
  if (panel.locked) el.classList.add('locked');
  // Score display
  const scoreDisplay = panel.score > 0 ? `Score: ${Math.round(panel.score)}` : 'New';
  // Build inner HTML once
  const bodyContent = forceCompact
    ? buildCompactBody(panel)
    : buildFullBody(panel);
  el.innerHTML = `
    <div class="panel-bar">
      <div class="title-group">
        <span>${panel.icon}</span>
        <span class="title">${panel.title}</span>
        <span class="score-badge">${scoreDisplay}</span>
      </div>
      <div class="actions">
        <button class="expand-btn" title="${forceCompact?'Expand':'Compact'}">${forceCompact?'⤢':'⤓'}</button>
        <button class="lock-btn ${panel.locked?'locked':''}" title="${panel.locked?'Unlock':'Lock'} position">${panel.locked?'🔒':'🔓'}</button>
      </div>
    </div>
    ${bodyContent}
  `;
  return el;
}
function buildFullBody(panel) {
  const d = panel.data;
  const bars = d.bars || [];
  const maxBar = Math.max(...bars, 1);
  const barHtml = bars.map(v => {
    const h = Math.round((v / maxBar) * 100);
    return `<div class="bar" style="height:${h}%"></div>`;
  }).join('');
  return `
    <div class="panel-body">
      <div class="metric-row">
        <div class="metric">
          <span class="label">Current</span>
          <span class="value">${d.val}</span>
        </div>
        <div class="metric">
          <span class="label">Change</span>
          <span class="value delta ${d.dir}">${d.delta}</span>
        </div>
      </div>
      <div class="bar-chart">${barHtml}</div>
    </div>
  `;
}
function buildCompactBody(panel) {
  const d = panel.data;
  return `
    <div class="panel-body">
      <div class="compact-preview">
        <span class="mini-val">${d.val}</span>
        <span class="mini-label">${d.delta < 0 ? '↓' : '↑'} ${d.delta}</span>
      </div>
      <div class="bar-chart" style="max-width:120px">
        ${(d.bars||[]).slice(-6).map(v => {
          const maxB = Math.max(...(d.bars||[]), 1);
          return `<div class="bar" style="height:${Math.round((v/maxB)*100)}%"></div>`;
        }).join('')}
      </div>
    </div>
  `;
}
// ── INIT ─────────────────────────────────────────
function init() {
  recomputeAllScores();
  renderGrid();
  // Periodically recompute scores to apply recency decay
  setInterval(() => {
    recomputeAllScores();
    if (autoMode) renderGrid();
  }, 30000); // every 30 seconds
}
document.addEventListener('DOMContentLoaded', init);
// Handle page unload — stop all view timers
window.addEventListener('beforeunload', () => {
  for (const panelId of Object.keys(viewTimers)) {
    stopViewTimer(panelId);
  }
  saveState();
});
// Handle visibility change (tab switch)
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    for (const panelId of Object.keys(viewTimers)) {
      stopViewTimer(panelId);
    }
  } else {
    // Restart timers for visible panels
    document.querySelectorAll('.panel').forEach(el => {
      const panelId = el.dataset.panelId;
      const rect = el.getBoundingClientRect();
      const vh = window.innerHeight;
      if (rect.top < vh && rect.bottom > 0) {
        startViewTimer(panelId);
      }
    });
  }
});
</script>
</body>
</html>