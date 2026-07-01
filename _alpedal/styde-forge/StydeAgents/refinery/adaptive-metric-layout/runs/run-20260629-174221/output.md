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
  --accent2: #3fb950;
  --warn: #d2991d;
  --danger: #f85149;
  --panel-gap: 8px;
  --radius: 8px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;overflow-x:hidden}
.toolbar{display:flex;align-items:center;gap:12px;padding:10px 16px;background:var(--surface);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100}
.toolbar h1{font-size:16px;font-weight:600;margin-right:auto}
.toolbar button{background:var(--surface);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:13px;transition:all .15s}
.toolbar button:hover{background:#1f2937;border-color:var(--accent)}
.toolbar button.active{background:var(--accent);color:#000;border-color:var(--accent)}
.toolbar .badge{background:var(--accent2);color:#000;font-size:11px;padding:2px 7px;border-radius:10px;font-weight:600}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--panel-gap);padding:12px;transition:all .4s ease}
.grid.compact-view .panel.low-rank{grid-column:span 1;max-height:120px;overflow:hidden}
.grid.compact-view .panel.low-rank .panel-body{display:none}
.grid.compact-view .panel.low-rank .panel-preview{display:block}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);transition:all .4s ease;position:relative;overflow:hidden;display:flex;flex-direction:column}
.panel.high-rank{grid-column:span 2;grid-row:span 2;min-height:280px}
.panel.mid-rank{grid-column:span 1;min-height:180px}
.panel.low-rank{grid-column:span 1;max-height:180px;opacity:.85}
.panel.pinned{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:10px 12px;border-bottom:1px solid var(--border);cursor:grab;user-select:none;flex-shrink:0}
.panel-header:active{cursor:grabbing}
.panel-header.dragging{opacity:.5}
.panel-title{font-weight:600;font-size:14px;display:flex;align-items:center;gap:6px}
.panel-score{font-size:11px;color:var(--text-dim);background:#1a1f2b;padding:2px 8px;border-radius:4px}
.panel-actions{display:flex;gap:4px}
.panel-actions button{background:none;border:none;color:var(--text-dim);cursor:pointer;padding:2px 6px;border-radius:4px;font-size:12px;transition:all .15s}
.panel-actions button:hover{color:var(--text);background:#1f2937}
.panel-actions button.locked{color:var(--accent)}
.panel-body{padding:12px;flex:1;overflow:auto}
.panel-preview{display:none;padding:8px 12px;font-size:12px;color:var(--text-dim)}
.sparkline{display:flex;align-items:flex-end;gap:2px;height:40px;margin-top:6px}
.sparkline-bar{flex:1;background:var(--accent);border-radius:1px 1px 0 0;min-height:2px;transition:height .5s ease}
.metric-value{font-size:28px;font-weight:700;font-family:'SF Mono',monospace}
.metric-label{font-size:12px;color:var(--text-dim)}
.metric-delta{font-size:13px;margin-left:6px}
.metric-delta.up{color:var(--accent2)}
.metric-delta.down{color:var(--danger)}
.heatmap-cell{display:inline-block;width:10px;height:10px;border-radius:2px;margin:1px;transition:background .3s}
.rank-badge{position:absolute;top:6px;right:6px;font-size:10px;background:#00000055;color:var(--text-dim);padding:1px 6px;border-radius:3px;pointer-events:none}
.tracking-indicator{width:6px;height:6px;border-radius:50%;background:var(--accent2);opacity:0;transition:opacity .3s}
.tracking-indicator.active{opacity:1;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:.3}50%{opacity:1}}
.drag-ghost{position:fixed;pointer-events:none;z-index:1000;opacity:.7;transform:rotate(2deg)}
.toast{position:fixed;bottom:20px;right:20px;background:var(--surface);border:1px solid var(--border);padding:10px 18px;border-radius:8px;font-size:13px;z-index:200;animation:slideUp .3s ease;box-shadow:0 4px 20px #00000055}
@keyframes slideUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
</style>
</head>
<body>
<div class="toolbar">
  <h1>Adaptive Dashboard</h1>
  <span id="trackCount" class="badge">0 events</span>
  <button id="btnCompact" onclick="toggleCompact()">Compact Low-Rank</button>
  <button id="btnReset" onclick="resetLayout()">Reset Learning</button>
  <button id="btnExport" onclick="exportState()">Export State</button>
</div>
<div class="grid" id="grid"></div>
<script>
'use strict';
// ─── Deterministic seed per metric ID ───
function cyrb53(str, seed=0) {
  let h1 = 0xdeadbeef ^ seed, h2 = 0x41c6ce57 ^ seed;
  for (let i = 0, ch; i < str.length; i++) {
    ch = str.charCodeAt(i);
    h1 = Math.imul(h1 ^ ch, 2654435761);
    h2 = Math.imul(h2 ^ ch, 1597334677);
  }
  h1 = Math.imul(h1 ^ (h1>>>16), 2246822507) ^ Math.imul(h2 ^ (h2>>>13), 3266489909);
  h2 = Math.imul(h2 ^ (h2>>>16), 2246822507) ^ Math.imul(h1 ^ (h1>>>13), 3266489909);
  return 4294967296 * (2097151 & h2) + (h1>>>0);
}
function seededRandom(metricId) {
  let seed = cyrb53(metricId);
  return function() {
    seed = (seed * 16807 + 0) % 2147483647;
    return (seed - 1) / 2147483646;
  };
}
// ─── Panel definitions ───
const DEFAULT_PANELS = [
  {id:'cpu',title:'CPU Usage',unit:'%',base:45,range:20,decimals:0,icon:'⚡'},
  {id:'memory',title:'Memory',unit:'GB',base:12.4,range:3,decimals:1,icon:'🧠'},
  {id:'requests',title:'Requests/s',unit:'',base:2840,range:800,decimals:0,icon:'📡'},
  {id:'latency',title:'P95 Latency',unit:'ms',base:120,range:40,decimals:0,icon:'⏱️'},
  {id:'errors',title:'Error Rate',unit:'%',base:0.8,range:0.6,decimals:2,icon:'🚨'},
  {id:'throughput',title:'Throughput',unit:'Mbps',base:940,range:200,decimals:0,icon:'📶'},
  {id:'connections',title:'Connections',unit:'',base:1520,range:400,decimals:0,icon:'🔌'},
  {id:'disk',title:'Disk I/O',unit:'MB/s',base:85,range:30,decimals:1,icon:'💾'},
  {id:'cache',title:'Cache Hit',unit:'%',base:94,range:8,decimals:1,icon:'💎'},
  {id:'queue',title:'Queue Depth',unit:'',base:23,range:15,decimals:0,icon:'📋'}
];
// ─── State ───
let panels = [];
let behaviorLog = [];
let attentionScores = {};
let compactMode = false;
let pinnedPanels = new Set();
let manualPositions = {};
let viewportTimers = {};
let renderScheduled = false;
let eventCount = 0;
// ─── Persistence ───
const STORAGE_KEY = 'adaptive_dashboard_v2';
function saveState() {
  const state = {
    panels: panels.map(p => ({id:p.id,title:p.title,unit:p.unit,base:p.base,range:p.range,decimals:p.decimals,icon:p.icon})),
    behaviorLog: behaviorLog.slice(-500),
    attentionScores,
    compactMode,
    pinnedPanels: [...pinnedPanels],
    manualPositions,
    eventCount
  };
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e) {}
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return false;
    const state = JSON.parse(raw);
    panels = state.panels || DEFAULT_PANELS;
    behaviorLog = state.behaviorLog || [];
    attentionScores = state.attentionScores || {};
    compactMode = state.compactMode || false;
    pinnedPanels = new Set(state.pinnedPanels || []);
    manualPositions = state.manualPositions || {};
    eventCount = state.eventCount || 0;
    return true;
  } catch(e) { return false; }
}
// ─── Behavioral Tracking ───
function logEvent(type, panelId, detail={}) {
  const entry = {ts:Date.now(),type,panelId,detail};
  behaviorLog.push(entry);
  eventCount++;
  document.getElementById('trackCount').textContent = eventCount + ' events';
  if (behaviorLog.length > 1000) behaviorLog = behaviorLog.slice(-1000);
  recalcScores();
}
function recalcScores() {
  const now = Date.now();
  const scores = {};
  for (const p of panels) {
    const events = behaviorLog.filter(e => e.panelId === p.id);
    const viewEvents = events.filter(e => e.type === 'view' || e.type === 'view_end');
    const clickEvents = events.filter(e => e.type === 'click' || e.type === 'expand' || e.type === 'collapse');
    let totalDuration = 0;
    for (let i = 0; i < viewEvents.length; i += 2) {
      if (viewEvents[i].type === 'view' && viewEvents[i+1] && viewEvents[i+1].type === 'view_end') {
        totalDuration += (viewEvents[i+1].ts - viewEvents[i].ts);
      }
    }
    const frequency = clickEvents.length + viewEvents.length * 0.3;
    const durationSec = totalDuration / 1000;
    const recency = events.length > 0 ? Math.max(0, 1 - (now - events[events.length-1].ts) / 3600000) : 0;
    scores[p.id] = (frequency * 0.4 + durationSec * 0.35 + recency * 25) || 0.1;
  }
  attentionScores = scores;
}
// ─── Ranking ───
function getRankedPanels() {
  const sorted = [...panels].sort((a,b) => (attentionScores[b.id]||0) - (attentionScores[a.id]||0));
  const maxScore = Math.max(...sorted.map(p => attentionScores[p.id]||0), 1);
  return sorted.map((p,i) => {
    const score = attentionScores[p.id]||0;
    const normalized = score / maxScore;
    let tier;
    if (normalized > 0.6 || i < 3) tier = 'high';
    else if (normalized > 0.25) tier = 'mid';
    else tier = 'low';
    return {...p, score: Math.round(score*100)/100, tier, rank: i+1};
  });
}
// ─── DOM (targeted updates) ───
let prevPanelData = new Map();
function generateSparkline(metricId, points=12) {
  const rng = seededRandom(metricId);
  const values = [];
  for (let i = 0; i < points; i++) values.push(rng());
  return values;
}
function generateHeatmap(metricId, rows=4, cols=8) {
  const rng = seededRandom(metricId);
  const cells = [];
  for (let i = 0; i < rows*cols; i++) cells.push(rng());
  return {cells,rows,cols};
}
function getMetricValue(panel) {
  const rng = seededRandom(panel.id);
  const noise = (rng() - 0.5) * 2;
  const val = panel.base + noise * panel.range;
  const prev = (prevPanelData.get(panel.id)||{}).value || val;
  const delta = val - prev;
  prevPanelData.set(panel.id, {...prevPanelData.get(panel.id), value:val, delta});
  return {value: val.toFixed(panel.decimals), delta: delta.toFixed(panel.decimals), prev};
}
function renderPanelDOM(panel, ranked) {
  const existing = document.getElementById('panel-' + panel.id);
  const metric = getMetricValue(panel);
  const sparkData = generateSparkline(panel.id);
  const heatData = generateHeatmap(panel.id);
  const score = attentionScores[panel.id] || 0;
  if (existing) {
    targetedUpdate(existing, panel, ranked, metric, sparkData, heatData, score);
    return existing;
  }
  const el = document.createElement('div');
  el.id = 'panel-' + panel.id;
  el.className = 'panel ' + ranked.tier + '-rank';
  if (pinnedPanels.has(panel.id)) el.classList.add('pinned');
  el.setAttribute('draggable','true');
  el.innerHTML = buildPanelHTML(panel, ranked, metric, sparkData, heatData, score);
  el.addEventListener('dragstart', onDragStart);
  el.addEventListener('dragover', e => e.preventDefault());
  el.addEventListener('drop', onDrop);
  setupPanelEvents(el, panel);
  return el;
}
function buildPanelHTML(panel, ranked, metric, sparkData, heatData, score) {
  const deltaClass = metric.delta >= 0 ? 'up' : 'down';
  return `
    <div class="panel-header">
      <span class="panel-title">${panel.icon} ${panel.title}</span>
      <span class="panel-score" id="score-${panel.id}">r${ranked.rank} · ${score.toFixed(1)}</span>
      <div class="panel-actions">
        <button class="${pinnedPanels.has(panel.id)?'locked':''}" onclick="togglePin('${panel.id}')" title="Lock position">📌</button>
        <button onclick="toggleCompact('${panel.id}')" title="Compact">⊟</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="metric-value" id="val-${panel.id}">${metric.value}<span class="metric-unit" style="font-size:14px;color:var(--text-dim)"> ${panel.unit}</span></div>
      <div class="metric-label">
        <span class="metric-delta ${deltaClass}" id="delta-${panel.id}">${metric.delta>=0?'+':''}${metric.delta} ${panel.unit}</span>
      </div>
      <div class="sparkline" id="spark-${panel.id}">${sparkData.map(v => `<div class="sparkline-bar" style="height:${Math.max(3,v*40)}px"></div>`).join('')}</div>
      <div style="margin-top:8px;font-size:11px;color:var(--text-dim)">Activity</div>
      <div class="heatmap" id="heat-${panel.id}">${heatData.cells.map(c => `<span class="heatmap-cell" style="background:rgba(88,166,255,${c.toFixed(2)})"></span>`).join('')}</div>
      <div class="tracking-indicator" id="track-${panel.id}"></div>
    </div>
    <div class="panel-preview" id="preview-${panel.id}">${panel.icon} ${panel.title}: ${metric.value}${panel.unit} — rank #${ranked.rank}</div>
    <div class="rank-badge">#${ranked.rank}</div>
  `;
}
function targetedUpdate(el, panel, ranked, metric, sparkData, heatData, score) {
  const valEl = el.querySelector('#val-' + panel.id);
  const deltaEl = el.querySelector('#delta-' + panel.id);
  const scoreEl = el.querySelector('#score-' + panel.id);
  const sparkEl = el.querySelector('#spark-' + panel.id);
  const heatEl = el.querySelector('#heat-' + panel.id);
  const previewEl = el.querySelector('#preview-' + panel.id);
  const rankBadge = el.querySelector('.rank-badge');
  const deltaClass = metric.delta >= 0 ? 'up' : 'down';
  if (valEl && valEl.childNodes[0]) {
    const unitSpan = valEl.querySelector('.metric-unit');
    valEl.childNodes[0].textContent = metric.value;
    if (unitSpan) unitSpan.textContent = ' ' + panel.unit;
  }
  if (deltaEl) {
    deltaEl.className = 'metric-delta ' + deltaClass;
    deltaEl.textContent = (metric.delta>=0?'+':'') + metric.delta + ' ' + panel.unit;
  }
  if (scoreEl) scoreEl.textContent = 'r' + ranked.rank + ' · ' + score.toFixed(1);
  if (sparkEl && sparkData) {
    const existingBars = sparkEl.children;
    for (let i = 0; i < Math.min(sparkData.length, existingBars.length); i++) {
      existingBars[i].style.height = Math.max(3, sparkData[i]*40) + 'px';
    }
  }
  if (heatEl && heatData) {
    const existingCells = heatEl.children;
    for (let i = 0; i < Math.min(heatData.cells.length, existingCells.length); i++) {
      existingCells[i].style.background = 'rgba(88,166,255,' + heatData.cells[i].toFixed(2) + ')';
    }
  }
  if (previewEl) previewEl.textContent = panel.icon + ' ' + panel.title + ': ' + metric.value + panel.unit + ' — rank #' + ranked.rank;
  if (rankBadge) rankBadge.textContent = '#' + ranked.rank;
  el.className = 'panel ' + ranked.tier + '-rank' + (pinnedPanels.has(panel.id) ? ' pinned' : '');
}
function setupPanelEvents(el, panel) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        viewportTimers[panel.id] = Date.now();
        logEvent('view', panel.id);
        const indicator = el.querySelector('.tracking-indicator');
        if (indicator) indicator.classList.add('active');
      } else if (viewportTimers[panel.id]) {
        logEvent('view_end', panel.id, {duration: Date.now() - viewportTimers[panel.id]});
        delete viewportTimers[panel.id];
        const indicator = el.querySelector('.tracking-indicator');
        if (indicator) indicator.classList.remove('active');
      }
    });
  }, {threshold: 0.3});
  observer.observe(el);
  el._observer = observer;
  el.addEventListener('click', e => {
    if (e.target.closest('button')) return;
    logEvent('click', panel.id);
  });
}
// ─── Drag & Drop ───
let dragPanel = null;
function onDragStart(e) {
  dragPanel = e.target.closest('.panel');
  if (!dragPanel) return;
  e.dataTransfer.effectAllowed = 'move';
  dragPanel.classList.add('dragging');
}
function onDrop(e) {
  e.preventDefault();
  const target = e.target.closest('.panel');
  if (!target || !dragPanel || target === dragPanel) { dragPanel = null; return; }
  const grid = document.getElementById('grid');
  const children = [...grid.children];
  const fromIdx = children.indexOf(dragPanel);
  const toIdx = children.indexOf(target);
  if (fromIdx < 0 || toIdx < 0) { dragPanel = null; return; }
  const panelId = dragPanel.id.replace('panel-','');
  manualPositions[panelId] = toIdx;
  pinnedPanels.add(panelId);
  logEvent('move', panelId, {from:fromIdx, to:toIdx});
  grid.insertBefore(dragPanel, toIdx > fromIdx ? target.nextSibling : target);
  dragPanel.classList.remove('dragging');
  dragPanel = null;
  renderGrid(true);
  saveState();
  toast('Panel pinned to position ' + (toIdx+1));
}
// ─── Actions ───
function togglePin(panelId) {
  if (pinnedPanels.has(panelId)) {
    pinnedPanels.delete(panelId);
    delete manualPositions[panelId];
    logEvent('unpin', panelId);
    toast('Panel unlocked — auto-layout restored');
  } else {
    pinnedPanels.add(panelId);
    const idx = [...document.getElementById('grid').children].findIndex(c => c.id === 'panel-' + panelId);
    if (idx >= 0) manualPositions[panelId] = idx;
    logEvent('pin', panelId);
    toast('Panel pinned at current position');
  }
  renderGrid(true);
  saveState();
}
function toggleCompact(panelId) {
  logEvent(compactMode ? 'expand' : 'collapse', panelId);
  compactMode = !compactMode;
  document.getElementById('btnCompact').classList.toggle('active', compactMode);
  document.getElementById('grid').classList.toggle('compact-view', compactMode);
  saveState();
}
function toggleCompact() {
  compactMode = !compactMode;
  document.getElementById('btnCompact').classList.toggle('active', compactMode);
  document.getElementById('grid').classList.toggle('compact-view', compactMode);
  saveState();
}
function resetLayout() {
  if (!confirm('Reset all learned preferences? This clears behavior history and layout.')) return;
  behaviorLog = [];
  attentionScores = {};
  pinnedPanels.clear();
  manualPositions = {};
  compactMode = false;
  eventCount = 0;
  prevPanelData.clear();
  document.getElementById('btnCompact').classList.remove('active');
  document.getElementById('grid').classList.remove('compact-view');
  document.getElementById('trackCount').textContent = '0 events';
  panels = [...DEFAULT_PANELS];
  renderGrid(false);
  saveState();
  toast('Layout reset — all learning cleared');
}
function exportState() {
  const state = {attentionScores, pinnedPanels:[...pinnedPanels], manualPositions, compactMode, eventCount, panelCount:panels.length};
  const blob = new Blob([JSON.stringify(state,null,2)], {type:'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'dashboard-state-' + Date.now() + '.json';
  a.click();
  URL.revokeObjectURL(url);
  toast('State exported');
}
function toast(msg) {
  const existing = document.querySelector('.toast');
  if (existing) existing.remove();
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 2500);
}
// ─── Render scheduler (targeted) ───
function renderGrid(forceFull=false) {
  const grid = document.getElementById('grid');
  const ranked = getRankedPanels();
  if (forceFull || !grid.children.length) {
    grid.innerHTML = '';
    const sortedForRender = [...ranked];
    sortedForRender.sort((a,b) => {
      const pa = pinnedPanels.has(a.id) ? (manualPositions[a.id] ?? 999) : 999;
      const pb = pinnedPanels.has(b.id) ? (manualPositions[b.id] ?? 999) : 999;
      if (pa !== 999 || pb !== 999) return pa - pb;
      return a.rank - b.rank;
    });
    for (const p of sortedForRender) {
      const el = renderPanelDOM(p, ranked.find(r => r.id===p.id));
      grid.appendChild(el);
    }
    return;
  }
  for (const p of ranked) {
    const el = document.getElementById('panel-' + p.id);
    if (!el) {
      const newEl = renderPanelDOM(p, p);
      grid.appendChild(newEl);
      continue;
    }
    const metric = getMetricValue(p);
    const sparkData = generateSparkline(p.id);
    const heatData = generateHeatmap(p.id);
    const score = attentionScores[p.id] || 0;
    targetedUpdate(el, p, p, metric, sparkData, heatData, score);
  }
}
// ─── Periodic refresh (targeted DOM updates) ───
function periodicRefresh() {
  const ranked = getRankedPanels();
  for (const p of ranked) {
    const el = document.getElementById('panel-' + p.id);
    if (!el) continue;
    const metric = getMetricValue(p);
    const sparkData = generateSparkline(p.id);
    const heatData = generateHeatmap(p.id);
    const score = attentionScores[p.id] || 0;
    targetedUpdate(el, p, p, metric, sparkData, heatData, score);
  }
  saveState();
}
// ─── Init ───
function init() {
  const loaded = loadState();
  if (!loaded) {
    panels = [...DEFAULT_PANELS];
  }
  renderGrid(true);
  if (compactMode) {
    document.getElementById('btnCompact').classList.add('active');
    document.getElementById('grid').classList.add('compact-view');
  }
  document.getElementById('trackCount').textContent = eventCount + ' events';
  setInterval(periodicRefresh, 5000);
  setInterval(saveState, 10000);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) saveState();
  });
}
init();
</script>
</body>
</html>