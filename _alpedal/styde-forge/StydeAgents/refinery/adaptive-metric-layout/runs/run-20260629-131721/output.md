<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --bg:#0f1117; --surface:#1a1d27; --border:#2a2d3a; --text:#e0e0e0;
  --text2:#a0a4b8; --accent:#6c8cff; --accent2:#4ecdc4; --warn:#ffb347;
  --danger:#ff6b6b; --radius:8px; --gap:10px; --trans:0.25s ease;
  --tier1-min:300px; --tier2-min:200px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px}
header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px}
header h1{font-size:1.2rem;font-weight:600;color:var(--text)}
.controls{display:flex;gap:8px;flex-wrap:wrap}
.btn{padding:6px 12px;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);color:var(--text2);cursor:pointer;font-size:0.8rem;transition:var(--trans);white-space:nowrap}
.btn:hover{color:var(--text);border-color:var(--accent)}
.btn.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.btn.locked{background:var(--warn);color:#1a1a1a;border-color:var(--warn)}
.dashboard{display:grid;grid-template-columns:repeat(auto-fill,minmax(var(--tier2-min),1fr));gap:var(--gap);grid-auto-rows:minmax(120px,auto);grid-auto-flow:dense}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:12px;transition:var(--trans);position:relative;cursor:grab;display:flex;flex-direction:column;min-height:120px}
.panel.dragging{opacity:0.5;cursor:grabbing;z-index:100}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent)}
.panel.compact{grid-column:span 1;grid-row:span 1;font-size:0.75rem;padding:8px}
.panel.compact .panel-body{display:none}
.panel.compact .panel-preview{display:block}
.panel.expanded{grid-column:span 2;grid-row:span 2}
.panel.tier1{grid-column:span 2;grid-row:span 2;min-height:280px}
.panel.tier2{grid-column:span 1;grid-row:span 1}
.panel.tier3{grid-column:span 1;grid-row:span 1;opacity:0.7}
.panel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;gap:4px}
.panel-title{font-weight:600;font-size:0.9rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1}
.panel-actions{display:flex;gap:4px;flex-shrink:0}
.panel-actions .btn{padding:3px 6px;font-size:0.7rem;min-width:28px;text-align:center}
.panel-body{flex:1;display:flex;flex-direction:column;gap:8px;overflow:hidden}
.panel-preview{display:none;font-size:0.7rem;color:var(--text2)}
.metric{display:flex;justify-content:space-between;align-items:baseline}
.metric-label{font-size:0.75rem;color:var(--text2)}
.metric-value{font-size:1.4rem;font-weight:700}
.metric-value.up{color:var(--accent2)}
.metric-value.down{color:var(--danger)}
.metric-value.neutral{color:var(--warn)}
.score-bar{height:3px;background:var(--border);border-radius:2px;margin-top:4px;overflow:hidden}
.score-fill{height:100%;background:var(--accent);border-radius:2px;transition:width var(--trans)}
.panel-rank{position:absolute;top:4px;right:4px;font-size:0.6rem;color:var(--text2);opacity:0.5}
.tier-divider{grid-column:1/-1;height:2px;background:var(--border);margin:4px 0;border-radius:1px;position:relative}
.tier-divider::after{content:attr(data-label);position:absolute;left:50%;top:-8px;transform:translateX(-50%);background:var(--bg);padding:0 8px;font-size:0.65rem;color:var(--text2);white-space:nowrap}
.stats{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:12px;font-size:0.75rem;color:var(--text2)}
.stats span{background:var(--surface);padding:4px 8px;border-radius:4px;border:1px solid var(--border)}
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:200;justify-content:center;align-items:center}
.modal-overlay.open{display:flex}
.modal{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;min-width:300px;max-width:90vw}
.modal h2{font-size:1rem;margin-bottom:12px;color:var(--text)}
.modal-close{float:right;background:none;border:none;color:var(--text2);cursor:pointer;font-size:1.2rem;padding:0 4px}
.settings-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border);gap:8px}
.settings-row:last-child{border-bottom:none}
.settings-row label{font-size:0.8rem;color:var(--text2)}
select,input[type=range]{background:var(--bg);color:var(--text);border:1px solid var(--border);border-radius:4px;padding:4px 8px;font-size:0.8rem}
.toast{position:fixed;bottom:20px;right:20px;background:var(--accent);color:#fff;padding:10px 16px;border-radius:var(--radius);font-size:0.8rem;z-index:300;opacity:0;transform:translateY(10px);transition:opacity 0.3s,transform 0.3s;pointer-events:none}
.toast.show{opacity:1;transform:translateY(0)}
.tier-boundary{grid-column:1/-1;height:0;position:relative}
.tier-boundary.forbidden{background:rgba(255,107,107,0.08)}
.tier-boundary::before{content:'';position:absolute;inset:0 -8px;background:transparent;transition:background 0.2s}
.tier-boundary.drag-near::before{background:rgba(255,107,107,0.2)}
@media(max-width:600px){
  .dashboard{grid-template-columns:1fr}
  .panel.expanded,.panel.tier1{grid-column:span 1;grid-row:span 1}
}
</style>
</head>
<body>
<header>
  <h1>Adaptive Metric Dashboard</h1>
  <div class="controls">
    <button class="btn" id="btnAuto" onclick="toggleAuto()" aria-pressed="true">Auto: ON</button>
    <button class="btn" id="btnReset" onclick="resetTracking()">Reset Tracking</button>
    <button class="btn" id="btnSettings" onclick="toggleSettings()">Settings</button>
  </div>
</header>
<div class="stats" id="statsBar">
  <span id="statPanels">Panels: 0</span>
  <span id="statTracked">Tracked: 0s</span>
  <span id="statUpdates">Updates: 0</span>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="modal-overlay" id="settingsModal">
  <div class="modal">
    <button class="modal-close" onclick="toggleSettings()" aria-label="Close settings">&times;</button>
    <h2>Layout Settings</h2>
    <div class="settings-row">
      <label for="decayRate">Recency decay rate</label>
      <input type="range" id="decayRate" min="0.5" max="0.99" step="0.01" value="0.9" oninput="updateDecayLabel()">
      <span id="decayLabel">0.90</span>
    </div>
    <div class="settings-row">
      <label for="updateInterval">Auto-update interval (s)</label>
      <select id="updateInterval" onchange="setUpdateInterval(this.value)">
        <option value="5">5</option>
        <option value="15" selected>15</option>
        <option value="30">30</option>
        <option value="60">60</option>
      </select>
    </div>
    <div class="settings-row">
      <label for="compactThreshold">Compact threshold (score)</label>
      <input type="range" id="compactThreshold" min="0" max="100" value="10" oninput="updateCompactLabel()">
      <span id="compactLabel">10</span>
    </div>
    <button class="btn" onclick="applySettings()" style="margin-top:12px;width:100%">Apply</button>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
'use strict';
const LS_KEY = 'adaptive_dashboard_v2';
const DECAY = 0.9;
const UPDATE_IV = 15000;
const COMPACT_THRESHOLD = 10;
const MIN_PANELS = 2;
const state = {
  panels: [],
  autoMode: true,
  decayRate: DECAY,
  updateInterval: UPDATE_IV,
  compactThreshold: COMPACT_THRESHOLD,
  updateTimer: null,
  observer: null,
  dragState: null,
  updates: 0
};
const METRICS = [
  {id:'revenue',title:'Revenue',value:'$48,293',change:'+12.4%',dir:'up',color:0},
  {id:'users',title:'Active Users',value:'8,421',change:'+5.7%',dir:'up',color:1},
  {id:'conversion',title:'Conversion Rate',value:'3.24%',change:'-0.3%',dir:'down',color:2},
  {id:'latency',title:'API Latency',value:'142ms',change:'-8ms',dir:'up',color:3},
  {id:'errors',title:'Error Rate',value:'0.12%',change:'+0.02%',dir:'down',color:4},
  {id:'sessions',title:'Sessions',value:'12.4k',change:'+2.1%',dir:'up',color:5},
  {id:'bounce',title:'Bounce Rate',value:'42.1%',change:'+1.2%',dir:'down',color:6},
  {id:'nps',title:'NPS Score',value:'72',change:'+3',dir:'up',color:7}
];
const COLORS = ['#6c8cff','#4ecdc4','#ffb347','#ff6b6b','#a78bfa','#f472b6','#38bdf8','#34d399'];
function createPanel(m, i) {
  return {
    id: m.id, title: m.title, value: m.value, change: m.change, dir: m.dir, color: COLORS[m.color],
    tracking: { views: 0, viewMs: 0, clicks: 0, lastInteraction: Date.now(), inView: false, viewStart: 0 },
    locked: false, compact: false, tier: 1, order: i,
    domId: 'panel-' + m.id
  };
}
function initPanels() {
  state.panels = METRICS.map((m, i) => createPanel(m, i));
}
function score(p) {
  const t = p.tracking;
  const recency = Math.exp(-(Date.now() - t.lastInteraction) / (1000 * 60 * 60) * (1 - state.decayRate));
  const freq = Math.log2(t.clicks + 2);
  const dur = Math.log2(t.viewMs / 1000 + 2);
  return +(freq * dur * recency * 10).toFixed(1);
}
function rankAll() {
  const scored = state.panels.map(p => ({p, s: score(p)}));
  scored.sort((a, b) => b.s - a.s);
  const n = scored.length;
  const t1 = Math.max(1, Math.ceil(n * 0.35));
  const t2 = Math.max(t1, Math.ceil(n * 0.7));
  scored.forEach(({p}, i) => {
    p.tier = i < t1 ? 1 : i < t2 ? 2 : 3;
    p.order = i;
    p.compact = score(p) < state.compactThreshold && p.tier >= 2;
  });
}
function arrangeDOM() {
  if (!state.autoMode) return;
  if (state.panels.length < MIN_PANELS) return;
  rankAll();
  const dash = document.getElementById('dashboard');
  const sorted = [...state.panels].sort((a, b) => a.order - b.order);
  const frag = document.createDocumentFragment();
  let lastTier = 0;
  sorted.forEach(p => {
    const el = document.getElementById(p.domId);
    if (!el) return;
    if (p.tier !== lastTier && lastTier !== 0) {
      const div = document.createElement('div');
      div.className = 'tier-divider';
      div.dataset.label = 'Tier ' + p.tier;
      frag.appendChild(div);
    }
    lastTier = p.tier;
    el.className = buildPanelClass(p);
    el.querySelector('.panel-rank').textContent = '#' + (p.order + 1);
    el.querySelector('.score-fill').style.width = Math.min(100, score(p)) + '%';
    frag.appendChild(el);
  });
  dash.textContent = '';
  dash.appendChild(frag);
  state.updates++;
  updateStats();
}
function buildPanelClass(p) {
  let cls = 'panel tier' + p.tier;
  if (p.compact) cls += ' compact';
  else if (p.tier === 1) cls += ' expanded';
  if (p.locked) cls += ' locked';
  return cls;
}
function spliceUpdate(panelId, changes) {
  const el = document.getElementById(panelId);
  if (!el) return;
  if ('tier' in changes) {
    el.classList.remove('tier1', 'tier2', 'tier3');
    el.classList.add('tier' + changes.tier);
  }
  if ('compact' in changes) {
    el.classList.toggle('compact', changes.compact);
    el.classList.toggle('expanded', !changes.compact && el.classList.contains('tier1'));
  }
  if ('locked' in changes) {
    el.classList.toggle('locked', changes.locked);
  }
  if ('order' in changes) {
    const rankEl = el.querySelector('.panel-rank');
    if (rankEl) rankEl.textContent = '#' + (changes.order + 1);
  }
  if ('score' in changes) {
    const fill = el.querySelector('.score-fill');
    if (fill) fill.style.width = Math.min(100, changes.score) + '%';
  }
}
function arrangeSplice() {
  if (!state.autoMode) return;
  if (state.panels.length < MIN_PANELS) return;
  rankAll();
  const sorted = [...state.panels].sort((a, b) => a.order - b.order);
  const dash = document.getElementById('dashboard');
  const existing = new Map();
  dash.querySelectorAll('.panel').forEach(el => existing.set(el.id, el));
  const frag = document.createDocumentFragment();
  let lastTier = 0;
  sorted.forEach(p => {
    if (p.tier !== lastTier && lastTier !== 0) {
      const div = document.createElement('div');
      div.className = 'tier-divider';
      div.dataset.label = 'Tier ' + p.tier;
      frag.appendChild(div);
    }
    lastTier = p.tier;
    const el = existing.get(p.domId);
    if (el) {
      el.className = buildPanelClass(p);
      const rankEl = el.querySelector('.panel-rank');
      if (rankEl) rankEl.textContent = '#' + (p.order + 1);
      const fill = el.querySelector('.score-fill');
      if (fill) fill.style.width = Math.min(100, score(p)) + '%';
      frag.appendChild(el);
      existing.delete(p.domId);
    }
  });
  existing.forEach(el => frag.appendChild(el));
  dash.textContent = '';
  dash.appendChild(frag);
  state.updates++;
  updateStats();
}
function toggleLock(panelId) {
  const p = state.panels.find(x => x.id === panelId);
  if (!p) return;
  p.locked = !p.locked;
  const el = document.getElementById(p.domId);
  if (!el) return;
  const btn = el.querySelector('.btn-lock');
  if (p.locked) {
    el.classList.add('locked');
    el.draggable = false;
    el.style.cursor = 'default';
    if (btn) { btn.textContent = '🔒'; btn.classList.add('locked'); btn.title = 'Unlock panel'; btn.setAttribute('aria-pressed', 'true'); }
  } else {
    el.classList.remove('locked');
    el.draggable = true;
    el.style.cursor = 'grab';
    if (btn) { btn.textContent = '🔓'; btn.classList.remove('locked'); btn.title = 'Lock panel'; btn.setAttribute('aria-pressed', 'false'); }
  }
  persistState();
  showToast(p.locked ? p.title + ' locked' : p.title + ' unlocked');
}
function toggleCompact(panelId) {
  const p = state.panels.find(x => x.id === panelId);
  if (!p) return;
  p.compact = !p.compact;
  const el = document.getElementById(p.domId);
  if (!el) return;
  const btn = el.querySelector('.btn-compact');
  el.classList.toggle('compact', p.compact);
  if (p.compact) {
    el.classList.remove('expanded');
    if (btn) { btn.textContent = '⊞'; btn.title = 'Expand panel'; btn.setAttribute('aria-pressed', 'true'); }
  } else {
    if (p.tier === 1) el.classList.add('expanded');
    if (btn) { btn.textContent = '⊟'; btn.title = 'Compact panel'; btn.setAttribute('aria-pressed', 'false'); }
  }
  persistState();
}
function toggleAuto() {
  state.autoMode = !state.autoMode;
  const btn = document.getElementById('btnAuto');
  if (state.autoMode) {
    btn.textContent = 'Auto: ON';
    btn.classList.add('active');
    btn.setAttribute('aria-pressed', 'true');
    arrangeSplice();
  } else {
    btn.textContent = 'Auto: OFF';
    btn.classList.remove('active');
    btn.setAttribute('aria-pressed', 'false');
  }
  persistState();
}
function toggleSettings() {
  const modal = document.getElementById('settingsModal');
  const open = modal.classList.toggle('open');
  modal.setAttribute('aria-hidden', String(!open));
}
function updateDecayLabel() {
  document.getElementById('decayLabel').textContent = document.getElementById('decayRate').value;
}
function updateCompactLabel() {
  document.getElementById('compactLabel').textContent = document.getElementById('compactThreshold').value;
}
function setUpdateInterval(v) {
  state.updateInterval = +v * 1000;
  clearInterval(state.updateTimer);
  state.updateTimer = setInterval(arrangeSplice, state.updateInterval);
}
function applySettings() {
  state.decayRate = +document.getElementById('decayRate').value;
  state.compactThreshold = +document.getElementById('compactThreshold').value;
  persistState();
  toggleSettings();
  arrangeSplice();
  showToast('Settings applied');
}
function updateStats() {
  document.getElementById('statPanels').textContent = 'Panels: ' + state.panels.length;
  const totalMs = state.panels.reduce((s, p) => s + p.tracking.viewMs, 0);
  document.getElementById('statTracked').textContent = 'Tracked: ' + (totalMs / 1000).toFixed(0) + 's';
  document.getElementById('statUpdates').textContent = 'Updates: ' + state.updates;
}
function trackClick(panelId) {
  const p = state.panels.find(x => x.id === panelId);
  if (!p) return;
  p.tracking.clicks++;
  p.tracking.lastInteraction = Date.now();
  persistState();
}
function startObserver() {
  if (state.observer) state.observer.disconnect();
  state.observer = new IntersectionObserver(entries => {
    const now = Date.now();
    entries.forEach(e => {
      const panelId = e.target.dataset.panelId;
      const p = state.panels.find(x => x.id === panelId);
      if (!p) return;
      if (e.isIntersecting && !p.tracking.inView) {
        p.tracking.inView = true;
        p.tracking.viewStart = now;
        p.tracking.views++;
        p.tracking.lastInteraction = now;
      } else if (!e.isIntersecting && p.tracking.inView) {
        p.tracking.inView = false;
        p.tracking.viewMs += now - p.tracking.viewStart;
        p.tracking.viewStart = 0;
      }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('.panel').forEach(el => state.observer.observe(el));
}
function flushViewTimes() {
  const now = Date.now();
  state.panels.forEach(p => {
    if (p.tracking.inView && p.tracking.viewStart) {
      p.tracking.viewMs += now - p.tracking.viewStart;
      p.tracking.viewStart = now;
    }
  });
}
function persistState() {
  const data = {
    panels: state.panels.map(p => ({
      id: p.id, locked: p.locked, compact: p.compact, order: p.order,
      tracking: p.tracking
    })),
    autoMode: state.autoMode,
    decayRate: state.decayRate,
    updateInterval: state.updateInterval,
    compactThreshold: state.compactThreshold
  };
  localStorage.setItem(LS_KEY, JSON.stringify(data));
}
function restoreState() {
  const raw = localStorage.getItem(LS_KEY);
  if (!raw) return;
  try {
    const data = JSON.parse(raw);
    state.autoMode = data.autoMode !== false;
    state.decayRate = data.decayRate || DECAY;
    state.updateInterval = data.updateInterval || UPDATE_IV;
    state.compactThreshold = data.compactThreshold || COMPACT_THRESHOLD;
    (data.panels || []).forEach(sp => {
      const p = state.panels.find(x => x.id === sp.id);
      if (p) {
        p.locked = !!sp.locked;
        p.compact = !!sp.compact;
        p.order = sp.order || p.order;
        if (sp.tracking) Object.assign(p.tracking, sp.tracking);
      }
    });
    document.getElementById('btnAuto').textContent = state.autoMode ? 'Auto: ON' : 'Auto: OFF';
    document.getElementById('btnAuto').classList.toggle('active', state.autoMode);
    document.getElementById('btnAuto').setAttribute('aria-pressed', String(state.autoMode));
    document.getElementById('decayRate').value = state.decayRate;
    document.getElementById('decayLabel').textContent = state.decayRate.toFixed(2);
    document.getElementById('updateInterval').value = String(state.updateInterval / 1000);
    document.getElementById('compactThreshold').value = state.compactThreshold;
    document.getElementById('compactLabel').textContent = state.compactThreshold;
    clearInterval(state.updateTimer);
    state.updateTimer = setInterval(arrangeSplice, state.updateInterval);
  } catch (e) { /* corrupt storage, ignore */ }
}
function resetTracking() {
  state.panels.forEach(p => {
    p.tracking = { views: 0, viewMs: 0, clicks: 0, lastInteraction: Date.now(), inView: false, viewStart: 0 };
    p.locked = false;
    p.compact = false;
    p.order = METRICS.findIndex(m => m.id === p.id);
  });
  localStorage.removeItem(LS_KEY);
  arrangeSplice();
  showToast('Tracking reset');
}
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._tid);
  t._tid = setTimeout(() => t.classList.remove('show'), 2000);
}
function panelHTML(p) {
  const s = score(p);
  return '<div class="' + buildPanelClass(p) + '" id="' + p.domId + '" data-panel-id="' + p.id + '" draggable="' + (!p.locked) + '" style="cursor:' + (p.locked ? 'default' : 'grab') + '" onclick="trackClick(\'' + p.id + '\')">' +
    '<div class="panel-rank">#' + (p.order + 1) + '</div>' +
    '<div class="panel-header">' +
      '<div class="panel-title">' + p.title + '</div>' +
      '<div class="panel-actions">' +
        '<button class="btn btn-compact" onclick="event.stopPropagation();toggleCompact(\'' + p.id + '\')" title="' + (p.compact ? 'Expand panel' : 'Compact panel') + '" aria-pressed="' + p.compact + '">' + (p.compact ? '⊞' : '⊟') + '</button>' +
        '<button class="btn btn-lock' + (p.locked ? ' locked' : '') + '" onclick="event.stopPropagation();toggleLock(\'' + p.id + '\')" title="' + (p.locked ? 'Unlock panel' : 'Lock panel') + '" aria-pressed="' + p.locked + '">' + (p.locked ? '🔒' : '🔓') + '</button>' +
      '</div>' +
    '</div>' +
    '<div class="panel-body">' +
      '<div class="metric"><span class="metric-label">Value</span><span class="metric-value ' + p.dir + '">' + p.value + '</span></div>' +
      '<div class="metric"><span class="metric-label">Change</span><span class="metric-value ' + p.dir + '">' + p.change + '</span></div>' +
      '<div class="metric"><span class="metric-label">Score</span><span class="metric-value neutral">' + s + '</span></div>' +
      '<div class="score-bar"><div class="score-fill" style="width:' + Math.min(100, s) + '%"></div></div>' +
    '</div>' +
    '<div class="panel-preview">' + p.value + ' ' + p.change + ' · Score: ' + s + '</div>' +
  '</div>';
}
function renderAll() {
  const dash = document.getElementById('dashboard');
  rankAll();
  dash.innerHTML = state.panels.map(p => panelHTML(p)).join('');
  startObserver();
  setupDragDrop();
  updateStats();
  state.updates++;
}
function setupDragDrop() {
  const panels = document.querySelectorAll('.panel[draggable="true"]');
  panels.forEach(el => {
    el.addEventListener('dragstart', onDragStart);
    el.addEventListener('dragend', onDragEnd);
  });
  document.querySelectorAll('.panel').forEach(el => {
    el.addEventListener('dragover', onDragOver);
    el.addEventListener('dragleave', onDragLeave);
    el.addEventListener('drop', onDrop);
  });
}
function getTier(el) {
  if (el.classList.contains('tier1')) return 1;
  if (el.classList.contains('tier2')) return 2;
  if (el.classList.contains('tier3')) return 3;
  return 0;
}
function detectTierBoundary(dragEl, targetEl) {
  const dragTier = getTier(dragEl);
  const targetTier = getTier(targetEl);
  if (dragTier === 0 || targetTier === 0) return false;
  return dragTier !== targetTier;
}
function onDragStart(e) {
  const el = e.target.closest('.panel');
  if (!el) return;
  const panelId = el.dataset.panelId;
  const p = state.panels.find(x => x.id === panelId);
  if (!p || p.locked) { e.preventDefault(); return; }
  el.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', panelId);
  state.dragState = { sourceId: panelId, sourceTier: p.tier };
}
function onDragEnd(e) {
  const el = e.target.closest('.panel');
  if (el) el.classList.remove('dragging');
  document.querySelectorAll('.panel.drag-over, .tier-boundary.drag-near').forEach(x => {
    x.classList.remove('drag-over', 'drag-near');
  });
  state.dragState = null;
}
function onDragOver(e) {
  e.preventDefault();
  const el = e.target.closest('.panel');
  if (!el || !state.dragState) return;
  const targetId = el.dataset.panelId;
  if (targetId === state.dragState.sourceId) return;
  const p = state.panels.find(x => x.id === targetId);
  if (p && p.locked) return;
  if (detectTierBoundary(document.getElementById('panel-' + state.dragState.sourceId), el)) {
    el.classList.add('drag-over');
    const divider = el.previousElementSibling;
    if (divider && divider.classList.contains('tier-divider')) divider.classList.add('drag-near');
    e.dataTransfer.dropEffect = 'none';
  } else {
    el.classList.add('drag-over');
    e.dataTransfer.dropEffect = 'move';
  }
}
function onDragLeave(e) {
  const el = e.target.closest('.panel');
  if (el) el.classList.remove('drag-over');
}
function onDrop(e) {
  e.preventDefault();
  const el = e.target.closest('.panel');
  if (!el || !state.dragState) return;
  el.classList.remove('drag-over');
  document.querySelectorAll('.tier-boundary.drag-near').forEach(x => x.classList.remove('drag-near'));
  const targetId = el.dataset.panelId;
  if (targetId === state.dragState.sourceId) return;
  const targetP = state.panels.find(x => x.id === targetId);
  if (targetP && targetP.locked) return;
  const srcP = state.panels.find(x => x.id === state.dragState.sourceId);
  if (!srcP || srcP.locked) return;
  if (detectTierBoundary(document.getElementById('panel-' + state.dragState.sourceId), el)) {
    showToast('Cannot move panel across tier boundary');
    return;
  }
  const srcIdx = state.panels.indexOf(srcP);
  const tgtIdx = state.panels.indexOf(targetP);
  state.panels.splice(srcIdx, 1);
  state.panels.splice(tgtIdx, 0, srcP);
  state.panels.forEach((p, i) => { p.order = i; });
  persistState();
  arrangeSplice();
  showToast(srcP.title + ' moved');
  state.dragState = null;
}
function init() {
  initPanels();
  restoreState();
  renderAll();
  clearInterval(state.updateTimer);
  state.updateTimer = setInterval(() => {
    flushViewTimes();
    persistState();
    arrangeSplice();
  }, state.updateInterval);
  document.getElementById('decayRate').value = state.decayRate;
  document.getElementById('decayLabel').textContent = state.decayRate.toFixed(2);
  document.getElementById('updateInterval').value = String(state.updateInterval / 1000);
  document.getElementById('compactThreshold').value = state.compactThreshold;
  document.getElementById('compactLabel').textContent = state.compactThreshold;
  const autoBtn = document.getElementById('btnAuto');
  autoBtn.textContent = state.autoMode ? 'Auto: ON' : 'Auto: OFF';
  autoBtn.classList.toggle('active', state.autoMode);
  autoBtn.setAttribute('aria-pressed', String(state.autoMode));
}
document.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>