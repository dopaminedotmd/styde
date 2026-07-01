<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --border: #2a2d3a;
  --text: #e1e4ed;
  --text-dim: #8b8fa3;
  --accent: #5b8def;
  --accent-glow: rgba(91,141,239,0.15);
  --danger: #ef5b5b;
  --success: #4caf88;
  --warn: #f0a050;
  --radius: 10px;
  --gap: 12px;
  --transition: 0.35s cubic-bezier(0.25, 0.8, 0.25, 1.2);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 16px;
  user-select: none;
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 10px;
}
h1 { font-size: 1.3rem; font-weight: 600; letter-spacing: -0.3px; }
.controls { display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
.btn {
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: background 0.2s;
  white-space: nowrap;
}
.btn:hover { background: #252836; }
.btn.active { border-color: var(--accent); background: var(--accent-glow); }
.dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--gap);
  transition: all var(--transition);
}
.dashboard.ranked {
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(140px, auto);
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 16px;
  position: relative;
  transition: all var(--transition);
  display: flex;
  flex-direction: column;
  gap: 8px;
  cursor: grab;
  min-height: 120px;
}
.panel:active { cursor: grabbing; }
.panel.large { grid-column: span 2; grid-row: span 2; }
.panel.normal { grid-column: span 1; grid-row: span 1; }
.panel.compact { grid-column: span 1; grid-row: span 1; padding: 8px 12px; min-height: 60px; }
.panel.compact .panel-body { display: none; }
.panel.compact .panel-value { font-size: 0.9rem; }
.panel.compact .panel-preview { display: block; font-size: 0.7rem; color: var(--text-dim); }
.panel.locked { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-glow); }
.panel.dragging { opacity: 0.4; transform: scale(0.95); }
.panel.drag-over { border-color: var(--accent); box-shadow: 0 0 20px var(--accent-glow); }
.panel-header { display: flex; justify-content: space-between; align-items: flex-start; }
.panel-title { font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }
.panel-actions { display: flex; gap: 4px; }
.panel-actions button {
  background: none; border: none; color: var(--text-dim);
  cursor: pointer; font-size: 0.85rem; padding: 2px 4px; border-radius: 4px; line-height: 1;
}
.panel-actions button:hover { color: var(--text); background: var(--border); }
.panel-actions button.locked { color: var(--accent); }
.panel-value { font-size: 1.6rem; font-weight: 700; letter-spacing: -0.5px; line-height: 1.1; }
.panel-sub { font-size: 0.75rem; color: var(--text-dim); }
.panel-body { flex: 1; display: flex; flex-direction: column; gap: 6px; }
.panel-preview { display: none; }
.metric-bar {
  height: 4px; border-radius: 2px; background: var(--border); overflow: hidden;
}
.metric-bar-fill {
  height: 100%; border-radius: 2px; transition: width 0.6s ease;
}
.chart-inline {
  flex: 1; display: flex; align-items: flex-end; gap: 2px; min-height: 40px;
}
.chart-inline .bar {
  flex: 1; border-radius: 2px 2px 0 0; min-width: 4px;
  transition: height 0.5s ease;
}
.sparkline { display: flex; align-items: flex-end; gap: 1px; height: 30px; }
.sparkline .pt { flex:1; border-radius: 1px 1px 0 0; min-width: 2px; transition: height 0.4s; }
.rank-badge {
  position: absolute; top: -6px; right: -6px;
  font-size: 0.6rem; background: var(--accent); color: #fff;
  border-radius: 50%; width: 20px; height: 20px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; z-index: 2;
}
.rank-badge.top { background: var(--accent); }
.rank-badge.mid { background: var(--warn); }
.rank-badge.low { background: var(--text-dim); }
.stats-bar {
  display: flex; gap: 16px; margin-bottom: 16px; flex-wrap: wrap;
}
.stat-item {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 10px 14px; min-width: 100px;
}
.stat-label { font-size: 0.65rem; color: var(--text-dim); text-transform: uppercase; }
.stat-value { font-size: 1rem; font-weight: 600; }
.toast {
  position: fixed; bottom: 20px; right: 20px;
  background: var(--accent); color: #fff; padding: 10px 18px;
  border-radius: 8px; font-size: 0.8rem; z-index: 100;
  animation: slideIn 0.3s ease, fadeOut 0.3s ease 1.7s forwards;
  max-width: 300px;
}
@keyframes slideIn { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
@keyframes fadeOut { to { opacity: 0; transform: translateY(10px); } }
@media (max-width: 640px) {
  body { padding: 8px; }
  .dashboard { grid-template-columns: 1fr; gap: 8px; }
  .dashboard.ranked { grid-template-columns: 1fr; }
  .panel.large { grid-column: span 1; grid-row: span 1; }
  .panel { min-height: 80px; padding: 10px 12px; }
  .panel-actions button { padding: 4px 6px; font-size: 1rem; }
  .btn { padding: 8px 12px; font-size: 0.75rem; }
}
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <button class="btn active" id="btnAuto" onclick="setMode('auto')">Auto Layout</button>
    <button class="btn" id="btnManual" onclick="setMode('manual')">Manual</button>
    <button class="btn" onclick="resetTracking()">Reset Tracking</button>
    <span style="font-size:0.7rem;color:var(--text-dim);margin-left:8px;" id="lastUpdate"></span>
  </div>
</header>
<div class="stats-bar" id="statsBar"></div>
<div class="dashboard ranked" id="dashboard"></div>
<script>
const PANELS = [
  { id:'revenue', title:'Revenue', value:'$128,430', sub:'+12.3% vs last week', color:'#5b8def', chart:[65,70,68,80,82,78,85,88,82,90,95,92] },
  { id:'users', title:'Active Users', value:'24,891', sub:'+5.7% DAU', color:'#4caf88', chart:[40,45,42,50,48,55,52,60,58,62,65,68] },
  { id:'conversion', title:'Conversion', value:'3.82%', sub:'-0.3% MoM', color:'#f0a050', chart:[4.2,4.0,3.9,4.1,3.8,3.7,3.9,3.8,3.6,3.9,3.8,3.82].map(v=>v*20) },
  { id:'cpu', title:'CPU Load', value:'47%', sub:'Avg across 8 cores', color:'#ef5b5b', chart:[30,45,55,40,60,50,35,48,52,44,47,42] },
  { id:'memory', title:'Memory', value:'62.3 GB', sub:'78% of 80GB total', color:'#9b7fd4', chart:[70,72,68,75,78,74,76,80,77,73,75,78] },
  { id:'network', title:'Network I/O', value:'1.2 Gbps', sub:'↓ 840 Mbps / ↑ 360 Mbps', color:'#3db8b8', chart:[20,25,30,22,28,35,32,27,33,29,31,28] },
  { id:'errors', title:'Error Rate', value:'0.12%', sub:'23 errors / 19.2k req', color:'#ef5b5b', chart:[0.5,0.3,0.8,0.2,0.4,0.1,0.6,0.3,0.2,0.15,0.12,0.18].map(v=>v*100) },
  { id:'latency', title:'P95 Latency', value:'142ms', sub:'-18ms vs baseline', color:'#f0a050', chart:[200,180,190,170,160,155,165,150,148,145,142,140] },
  { id:'storage', title:'Storage', value:'1.8 TB', sub:'42% utilized', color:'#5b8def', chart:[30,32,35,38,36,40,42,39,41,43,42,42] },
  { id:'sessions', title:'Sessions', value:'3,421', sub:'Active right now', color:'#4caf88', chart:[60,55,70,65,75,68,80,72,78,74,82,76] },
  { id:'cache', title:'Cache Hit', value:'94.2%', sub:'CDN + Redis aggregate', color:'#9b7fd4', chart:[90,92,91,93,94,92,95,93,94,96,94,94.2] },
  { id:'queue', title:'Queue Depth', value:'847', sub:'Jobs pending', color:'#3db8b8', chart:[100,200,350,500,450,600,700,650,800,780,850,847].map(v=>v/10) }
];
const STORAGE_KEY = 'adaptive_dashboard_state';
let state = loadState();
let mode = 'auto';
let trackedInteractions = new Map();
let dragState = null;
let observer = null;
let visibilityTimers = new Map();
function defaultState() {
  const s = { panels:{}, mode:'auto', lastRank:Date.now() };
  PANELS.forEach((p,i) => {
    s.panels[p.id] = {
      id:p.id, locked:false, manualPos:i, size:'normal',
      views:0, totalDuration:0, interactions:0, lastInteraction:0,
      score:0, rank:i, customSize:null
    };
  });
  return s;
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const s = JSON.parse(raw);
      if (s.panels && Object.keys(s.panels).length === PANELS.length) return s;
    }
  } catch(e) {}
  return defaultState();
}
function saveState() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e) {}
}
function track(panelId, type) {
  let s = state.panels[panelId];
  if (!s) return;
  const now = Date.now();
  s.interactions++;
  s.lastInteraction = now;
  if (type === 'view_start') {
    s.views++;
    visibilityTimers.set(panelId, now);
  }
  if (type === 'view_end') {
    const start = visibilityTimers.get(panelId);
    if (start) {
      s.totalDuration += (now - start);
      visibilityTimers.delete(panelId);
    }
  }
  recalcRanks();
  saveState();
  requestAnimationFrame(renderDashboard);
}
function recalcRanks() {
  const now = Date.now();
  const entries = Object.values(state.panels);
  const maxDuration = Math.max(1, ...entries.map(e=>e.totalDuration));
  const maxFreq = Math.max(1, ...entries.map(e=>e.interactions));
  entries.forEach(e => {
    const freqNorm = e.interactions / maxFreq;
    const durNorm = e.totalDuration / maxDuration;
    const hoursSince = Math.max(0.01, (now - e.lastInteraction) / 3600000);
    const recencyFactor = 1 / Math.log(2 + hoursSince);
    e.score = (freqNorm * 0.35 + durNorm * 0.35 + recencyFactor * 0.30) * 100;
  });
  entries.sort((a,b) => b.score - a.score);
  entries.forEach((e,i) => { e.rank = i; });
  const topN = Math.ceil(entries.length * 0.33);
  const midN = Math.ceil(entries.length * 0.66);
  entries.forEach((e,i) => {
    if (e.locked && e.customSize) { e.size = e.customSize; return; }
    if (i < topN) e.size = 'large';
    else if (i < midN) e.size = 'normal';
    else e.size = 'compact';
  });
  state.lastRank = now;
}
function renderDashboard() {
  const container = document.getElementById('dashboard');
  // Collect existing panels for diff-based update
  const existing = new Map();
  container.querySelectorAll('.panel').forEach(el => existing.set(el.dataset.pid, el));
  const entries = Object.values(state.panels).sort((a,b) => a.rank - b.rank);
  const orderedIds = entries.map(e => e.id);
  // Build fragment for new/changed panels
  const fragment = document.createDocumentFragment();
  const newOrder = [];
  orderedIds.forEach(pid => {
    const ps = state.panels[pid];
    const pdef = PANELS.find(p => p.id === pid);
    if (!pdef) return;
    let el = existing.get(pid);
    const sizeClass = ps.size;
    const oldSizeClass = el ? [...el.classList].find(c => ['large','normal','compact'].includes(c)) : null;
    const oldLocked = el ? el.classList.contains('locked') : false;
    const needsRebuild = !el || oldSizeClass !== sizeClass || oldLocked !== ps.locked;
    if (needsRebuild) {
      if (el) el.remove();
      el = buildPanelElement(pdef, ps);
    } else {
      existing.delete(pid);
      el.style.order = ps.rank;
      updatePanelMetrics(el, pdef);
    }
    newOrder.push({ el, rank: ps.rank });
  });
  // Remove panels no longer in state
  existing.forEach(el => el.remove());
  // Apply order and append
  newOrder.sort((a,b) => a.rank - b.rank);
  newOrder.forEach(({el, rank}) => {
    el.style.order = rank;
    if (!el.parentNode) fragment.appendChild(el);
  });
  if (fragment.childNodes.length > 0) {
    container.appendChild(fragment);
  }
  // Re-apply order to existing nodes
  newOrder.forEach(({el, rank}) => {
    if (el.parentNode === container) el.style.order = rank;
  });
  updateStatsBar();
  document.getElementById('lastUpdate').textContent = 'Updated: ' + new Date().toLocaleTimeString();
}
function buildPanelElement(pdef, ps) {
  const el = document.createElement('div');
  el.className = 'panel ' + ps.size;
  el.dataset.pid = pdef.id;
  el.style.order = ps.rank;
  if (ps.locked) el.classList.add('locked');
  el.draggable = true;
  el.innerHTML = buildPanelHTML(pdef, ps);
  bindPanelEvents(el, pdef.id);
  return el;
}
function buildPanelHTML(pdef, ps) {
  const rankLabel = ps.rank < Math.ceil(PANELS.length*0.33) ? 'top' : ps.rank < Math.ceil(PANELS.length*0.66) ? 'mid' : 'low';
  const isCompact = ps.size === 'compact';
  const bars = pdef.chart.map((v,i) => {
    const h = Math.max(4, (v / Math.max(...pdef.chart)) * 100);
    return '<div class="pt" style="height:'+h+'%;background:'+pdef.color+'"></div>';
  }).join('');
  return `
    <div class="rank-badge ${rankLabel}">${ps.rank+1}</div>
    <div class="panel-header">
      <span class="panel-title">${pdef.title}</span>
      <div class="panel-actions">
        <button class="${ps.locked?'locked':''}" onclick="event.stopPropagation();toggleLock('${pdef.id}')" title="${ps.locked?'Unlock':'Lock'} position">&#128274;</button>
        <button onclick="event.stopPropagation();cycleSize('${pdef.id}')" title="Cycle size">&#8644;</button>
      </div>
    </div>
    <div class="panel-value">${pdef.value}</div>
    <div class="panel-sub">${pdef.sub}</div>
    <div class="panel-preview">${pdef.value} &middot; ${pdef.sub}</div>
    <div class="panel-body">
      <div class="sparkline">${bars}</div>
    </div>
  `;
}
function updatePanelMetrics(el, pdef) {
  const valueEl = el.querySelector('.panel-value');
  const subEl = el.querySelector('.panel-sub');
  const previewEl = el.querySelector('.panel-preview');
  if (valueEl) valueEl.textContent = pdef.value;
  if (subEl) subEl.textContent = pdef.sub;
  if (previewEl) previewEl.textContent = pdef.value + ' · ' + pdef.sub;
}
function bindPanelEvents(el, pid) {
  el.addEventListener('click', (e) => {
    if (e.target.closest('button')) return;
    track(pid, 'interaction');
  });
  el.addEventListener('dragstart', (e) => {
    if (mode !== 'manual') { e.preventDefault(); return; }
    dragState = { pid, el };
    el.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', pid);
  });
  el.addEventListener('dragend', () => {
    if (dragState) dragState.el.classList.remove('dragging');
    dragState = null;
    document.querySelectorAll('.drag-over').forEach(e=>e.classList.remove('drag-over'));
  });
  el.addEventListener('dragover', (e) => {
    if (mode !== 'manual') return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    if (dragState && dragState.el !== el) {
      el.classList.add('drag-over');
    }
  });
  el.addEventListener('dragleave', () => { el.classList.remove('drag-over'); });
  el.addEventListener('drop', (e) => {
    e.preventDefault();
    el.classList.remove('drag-over');
    if (mode !== 'manual' || !dragState || dragState.el === el) return;
    const srcPid = dragState.pid;
    const dstPid = el.dataset.pid;
    swapPanels(srcPid, dstPid);
  });
}
function swapPanels(srcPid, dstPid) {
  const src = state.panels[srcPid];
  const dst = state.panels[dstPid];
  const tmpRank = src.rank;
  src.rank = dst.rank;
  dst.rank = tmpRank;
  src.manualPos = src.rank;
  dst.manualPos = dst.rank;
  saveState();
  renderDashboard();
}
function toggleLock(pid) {
  const ps = state.panels[pid];
  ps.locked = !ps.locked;
  if (ps.locked) ps.customSize = ps.size;
  saveState();
  renderDashboard();
  toast(ps.locked ? pid + ' locked' : pid + ' unlocked');
}
function cycleSize(pid) {
  const ps = state.panels[pid];
  const sizes = ['large','normal','compact'];
  const idx = sizes.indexOf(ps.size);
  ps.size = sizes[(idx + 1) % 3];
  ps.locked = true;
  ps.customSize = ps.size;
  saveState();
  renderDashboard();
  toast(pid + ' → ' + ps.size);
}
function setMode(m) {
  mode = m;
  state.mode = m;
  document.getElementById('btnAuto').classList.toggle('active', m==='auto');
  document.getElementById('btnManual').classList.toggle('active', m==='manual');
  if (m === 'auto') {
    Object.values(state.panels).forEach(p => {
      if (!p.locked) { p.customSize = null; }
    });
    recalcRanks();
  }
  saveState();
  renderDashboard();
  toast('Mode: ' + m);
}
function resetTracking() {
  state = defaultState();
  saveState();
  recalcRanks();
  renderDashboard();
  toast('Tracking reset');
}
function updateStatsBar() {
  const entries = Object.values(state.panels);
  const totalViews = entries.reduce((s,e)=>s+e.views,0);
  const totalInteractions = entries.reduce((s,e)=>s+e.interactions,0);
  const totalDuration = entries.reduce((s,e)=>s+e.totalDuration,0);
  const mins = Math.round(totalDuration / 60000);
  document.getElementById('statsBar').innerHTML = `
    <div class="stat-item"><div class="stat-label">Total Views</div><div class="stat-value">${totalViews}</div></div>
    <div class="stat-item"><div class="stat-label">Interactions</div><div class="stat-value">${totalInteractions}</div></div>
    <div class="stat-item"><div class="stat-label">View Time</div><div class="stat-value">${mins}m</div></div>
    <div class="stat-item"><div class="stat-label">Mode</div><div class="stat-value">${mode}</div></div>
    <div class="stat-item"><div class="stat-label">Panels</div><div class="stat-value">${PANELS.length}</div></div>
  `;
}
function toast(msg) {
  const t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 2200);
}
// IntersectionObserver for view duration tracking
function setupObserver() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const pid = entry.target.dataset.pid;
      if (!pid) return;
      if (entry.isIntersecting) {
        track(pid, 'view_start');
      } else {
        track(pid, 'view_end');
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.panel').forEach(el => observer.observe(el));
}
// Live metric simulation
function simulateMetrics() {
  PANELS.forEach(p => {
    const lastVal = parseFloat(p.value.replace(/[^0-9.]/g,''));
    if (isNaN(lastVal)) return;
    const variance = lastVal * (Math.random() * 0.04 - 0.02);
    let newVal = lastVal + variance;
    if (p.id === 'errors') newVal = Math.max(0.01, Math.min(2, newVal));
    if (p.id === 'cache') newVal = Math.min(99.9, Math.max(80, newVal));
    if (p.id === 'latency') newVal = Math.max(80, Math.min(300, newVal));
    const formatted = formatMetricValue(p.id, newVal);
    p.value = formatted;
    p.sub = randomSubtext(p.id, newVal);
    p.chart.push(newVal);
    if (p.chart.length > 24) p.chart.shift();
  });
}
function formatMetricValue(id, val) {
  if (id === 'revenue') return '$' + Math.round(val).toLocaleString();
  if (id === 'users') return Math.round(val).toLocaleString();
  if (id === 'conversion' || id === 'errors') return val.toFixed(2) + '%';
  if (id === 'cpu') return Math.round(val) + '%';
  if (id === 'memory' || id === 'storage') return (val/1000).toFixed(1) + ' ' + (id==='storage'?'TB':'GB');
  if (id === 'network') return (val/100).toFixed(1) + ' Gbps';
  if (id === 'latency') return Math.round(val) + 'ms';
  if (id === 'sessions') return Math.round(val).toLocaleString();
  if (id === 'cache') return val.toFixed(1) + '%';
  if (id === 'queue') return Math.round(val).toString();
  return val.toString();
}
function randomSubtext(id, val) {
  const subs = {
    revenue: ['+'+((Math.random()*20-2).toFixed(1))+'% vs last week', 'Up from yesterday', 'On track for target'],
    users: ['+'+((Math.random()*8-1).toFixed(1))+'% DAU', 'Engagement rising', 'Retention: '+(70+Math.random()*20).toFixed(1)+'%'],
    conversion: [(Math.random()>0.5?'+':'-')+((Math.random()*2).toFixed(1))+'% MoM', 'Funnel optimizing', 'Cart: '+(60+Math.random()*20).toFixed(0)+'%'],
    cpu: ['Avg across 8 cores', 'Peak: '+(50+Math.random()*40).toFixed(0)+'%', 'Thermal: OK'],
    memory: [(70+Math.random()*15).toFixed(0)+'% of total', 'Cache: '+(20+Math.random()*30).toFixed(0)+'GB', 'Swap: 0%'],
    network: ['In: '+(600+Math.random()*400).toFixed(0)+' Mbps', 'Out: '+(200+Math.random()*300).toFixed(0)+' Mbps', 'Packets OK'],
    errors: [Math.round(Math.random()*50)+' errors', 'SLA: 99.9%', 'Mostly 5xx'],
    latency: ['-'+(10+Math.random()*30).toFixed(0)+'ms vs baseline', 'P50: '+(30+Math.random()*40).toFixed(0)+'ms', 'P99: '+(200+Math.random()*200).toFixed(0)+'ms'],
    storage: [(40+Math.random()*10).toFixed(0)+'% utilized', 'IOPS: '+(1000+Math.random()*3000).toFixed(0), 'Growth: +'+(Math.random()*3).toFixed(1)+'%/day'],
    sessions: ['Active now', 'Bounce: '+(20+Math.random()*30).toFixed(0)+'%', 'Avg duration: '+(3+Math.random()*10).toFixed(0)+'m'],
    cache: ['CDN+Redis', 'Miss: '+(3+Math.random()*5).toFixed(1)+'%', 'Warmup: done'],
    queue: [(Math.random()*200).toFixed(0)+' jobs pending', 'Processed: '+(500+Math.random()*500).toFixed(0)+'/h', 'Oldest: '+(1+Math.random()*10).toFixed(0)+'s']
  };
  const opts = subs[id] || ['Stable'];
  return opts[Math.floor(Math.random() * opts.length)];
}
// Initial render
recalcRanks();
renderDashboard();
setMode(state.mode || 'auto');
setupObserver();
// Live updates every 5s
setInterval(() => {
  simulateMetrics();
  renderDashboard();
  setupObserver();
}, 5000);
// Interaction decay: simulate viewing top panels over time
setInterval(() => {
  const entries = Object.values(state.panels).sort((a,b) => b.score - a.score);
  if (entries.length > 3) {
    track(entries[0].id, 'interaction');
    track(entries[1].id, 'interaction');
  }
}, 30000);
</script>
</body>
</html>