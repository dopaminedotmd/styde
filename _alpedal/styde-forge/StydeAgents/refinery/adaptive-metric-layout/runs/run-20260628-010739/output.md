```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0d1117;color:#c9d1d9;padding:16px;min-height:100vh}
h1{font-size:20px;font-weight:600;margin-bottom:16px;color:#f0f6fc;display:flex;align-items:center;gap:12px}
h1 small{font-size:12px;color:#8b949e;font-weight:400}
#layout-controls{display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap;align-items:center}
#layout-controls label{font-size:13px;color:#8b949e}
#layout-controls select{padding:4px 8px;border-radius:6px;border:1px solid #30363d;background:#161b22;color:#c9d1d9;font-size:13px}
#layout-controls button{padding:6px 14px;border-radius:6px;border:1px solid #30363d;background:#21262d;color:#c9d1d9;font-size:13px;cursor:pointer;transition:all .15s}
#layout-controls button:hover{background:#30363d;border-color:#58a6ff}
#layout-controls .stat-badge{font-size:12px;color:#8b949e;background:#161b22;padding:4px 10px;border-radius:12px;border:1px solid #30363d}
#dashboard{display:grid;gap:12px;transition:grid-template-columns .5s ease,grid-template-rows .5s ease}
.panel{border:1px solid #30363d;border-radius:8px;background:#161b22;overflow:hidden;position:relative;transition:all .35s cubic-bezier(.4,0,.2,1)}
.panel.dragging{opacity:.7;box-shadow:0 8px 32px rgba(0,0,0,.5)}
.panel.locked{border-color:#d29922;box-shadow:0 0 0 1px rgba(210,153,34,.3)}
.panel.compact .panel-header{cursor:pointer}
.panel.compact .panel-body{display:none}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:#1c2128;border-bottom:1px solid #30363d;cursor:grab;user-select:none}
.panel.locked .panel-header{cursor:default}
.panel-header h3{font-size:13px;font-weight:500;color:#f0f6fc;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1}
.panel-header .panel-actions{display:flex;gap:4px;align-items:center}
.panel-header .panel-actions button{background:0 0;border:none;color:#8b949e;cursor:pointer;padding:2px 4px;border-radius:4px;font-size:13px;transition:color .15s}
.panel-header .panel-actions button:hover{color:#f0f6fc;background:#30363d}
.panel-header .panel-actions .lock-btn.locked{color:#d29922}
.panel-header .attention-badge{font-size:10px;padding:1px 6px;border-radius:8px;background:#21262d;color:#8b949e;margin-right:6px}
.panel-header .rank-badge{font-size:9px;padding:1px 5px;border-radius:4px;background:#1f6feb22;color:#58a6ff;margin-right:6px}
.panel-header .drag-handle{color:#484f58;font-size:14px;margin-right:8px;cursor:grab}
.panel-body{padding:14px;min-height:60px;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:8px}
.panel-body .metric-value{font-size:28px;font-weight:700;color:#f0f6fc}
.panel-body .metric-label{font-size:12px;color:#8b949e}
.panel-body .metric-bar{width:100%;height:6px;background:#21262d;border-radius:3px;overflow:hidden;margin-top:6px}
.panel-body .metric-bar-fill{height:100%;border-radius:3px;transition:width .5s ease}
.panel-body .chart-svg{width:100%;height:50px}
.panel-body .process-list{width:100%;font-size:12px;display:flex;flex-direction:column;gap:3px}
.panel-body .process-list .proc-row{display:flex;justify-content:space-between;color:#8b949e}
.panel-body .process-list .proc-row .proc-name{flex:1}
.panel-body .process-list .proc-row .proc-cpu{width:40px;text-align:right;color:#58a6ff}
.panel-body .log-line{width:100%;font-size:11px;font-family:monospace;color:#8b949e;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:1px 0}
.panel-body .log-line.error{color:#f85149}
.panel-body .log-line.warn{color:#d29922}
.panel.compact .panel-body{display:flex;flex-direction:row;padding:6px 14px;min-height:auto;gap:8px}
.panel.compact .panel-body .metric-value{font-size:16px}
.panel.compact .panel-body .metric-label{font-size:10px}
.panel.compact .panel-body .metric-bar{display:none}
.panel.compact .panel-body .chart-svg{height:24px}
.panel.compact .panel-body .process-list{flex-direction:row;gap:6px;overflow:hidden}
.panel.compact .panel-body .log-line{font-size:10px;max-width:120px}
#toast{position:fixed;bottom:20px;right:20px;background:#1c2128;border:1px solid #30363d;border-radius:8px;padding:10px 16px;font-size:13px;color:#c9d1d9;opacity:0;transform:translateY(10px);transition:all .3s ease;z-index:100;pointer-events:none}
#toast.show{opacity:1;transform:translateY(0)}
</style>
</head>
<body>
<h1>Adaptive Metric Layout <small id="layout-mode-label">auto-arrange active</small></h1>
<div id="layout-controls">
  <label>Layout mode:</label>
  <select id="layout-mode-select">
    <option value="auto">Auto (attention-weighted)</option>
    <option value="manual">Manual only</option>
    <option value="reset">Reset &amp; re-learn</option>
  </select>
  <button id="save-snapshot-btn">Save snapshot</button>
  <button id="reset-stats-btn">Reset usage stats</button>
  <span class="stat-badge" id="total-interactions-badge">0 interactions</span>
  <span class="stat-badge" id="panels-tracked-badge">0 panels</span>
</div>
<div id="dashboard"></div>
<div id="toast"></div>
<script>
(function(){
'use strict';
const STORAGE_KEY = 'aml_layout_v1';
const STORAGE_STATS_KEY = 'aml_usage_stats_v1';
const PANEL_DEFS = [
  {id:'cpu', title:'CPU Usage', type:'metric', color:'#58a6ff'},
  {id:'memory', title:'Memory Usage', type:'metric', color:'#3fb950'},
  {id:'network', title:'Network I/O', type:'chart', color:'#bc8cff'},
  {id:'disk', title:'Disk Activity', type:'chart', color:'#f0883e'},
  {id:'processes', title:'Active Processes', type:'list', color:'#79c0ff'},
  {id:'uptime', title:'System Uptime', type:'stat', color:'#7ee787'},
  {id:'temperature', title:'Temperature', type:'metric', color:'#ff7b72'},
  {id:'errors', title:'Error Log', type:'log', color:'#f85149'}
];
const GRID_COLS = {4:'repeat(2,1fr)',6:'repeat(3,1fr)',8:'repeat(4,1fr)'};
// ---- State ----
let panels = [];
let usageStats = {};
let layoutMode = 'auto';
let totalInteractions = 0;
let toastTimeout = null;
let layoutTimer = null;
const LAYOUT_DEBOUNCE_MS = 500;
// ---- Init Stats ----
function initStats() {
  const saved = localStorage.getItem(STORAGE_STATS_KEY);
  if(saved){
    try{
      const parsed = JSON.parse(saved);
      usageStats = parsed.stats || {};
      totalInteractions = parsed.totalInteractions || 0;
      return;
    }catch(e){}
  }
  usageStats = {};
  totalInteractions = 0;
  PANEL_DEFS.forEach(p => {
    usageStats[p.id] = {views:0, totalDuration:0, interactions:0, lastViewTime:0, collapsed:false, locked:false, manualPos:null};
  });
}
initStats();
// ---- Panel State Factory ----
function createPanelState(def){
  const stats = usageStats[def.id] || {views:0, totalDuration:0, interactions:0, lastViewTime:0, collapsed:false, locked:false, manualPos:null};
  return {
    ...def,
    views: stats.views,
    totalDuration: stats.totalDuration,
    interactions: stats.interactions,
    lastViewTime: stats.lastViewTime,
    collapsed: stats.collapsed,
    locked: stats.locked || false,
    manualPos: stats.manualPos || null,
    attentionScore: 0
  };
}
// ---- Attention Score ----
function computeAttention(stat){
  const freq = (stat.views || 0) + (stat.interactions || 0) * 2;
  const dur = stat.totalDuration || 0;
  const recency = stat.lastViewTime > 0 ? 1 / ((Date.now() - stat.lastViewTime) / 3600000 + 1) : 0.1;
  return Math.round((freq * 0.25 + dur * 0.5 + recency * 100 * 0.25) * 100) / 100;
}
function recalcScores(){
  panels.forEach(p => {
    const stat = usageStats[p.id];
    p.attentionScore = computeAttention(stat);
    p.views = stat.views;
    p.totalDuration = stat.totalDuration;
    p.interactions = stat.interactions;
    p.lastViewTime = stat.lastViewTime;
  });
}
// ---- Layout Engine ----
function computeLayout(){
  if(layoutMode === 'manual'){
    const locked = panels.filter(p => p.locked);
    const unlocked = panels.filter(p => !p.locked);
    const sorted = [...locked, ...unlocked];
    return assignGrid(sorted);
  }
  const locked = panels.filter(p => p.locked && p.manualPos !== null).sort((a,b) => a.manualPos - b.manualPos);
  const autoRanked = panels.filter(p => !p.locked || p.manualPos === null)
    .sort((a,b) => b.attentionScore - a.attentionScore);
  const ordered = [];
  const usedPositions = new Set(locked.map(p => p.manualPos));
  let ai = 0;
  let li = 0;
  for(let pos=0; pos<panels.length; pos++){
    if(usedPositions.has(pos)){
      ordered.push(locked[li]);
      li++;
    } else {
      ordered.push(autoRanked[ai]);
      ai++;
    }
  }
  return assignGrid(ordered);
}
function assignGrid(ordered){
  const total = ordered.length;
  const cols = total <= 4 ? 2 : total <= 6 ? 3 : 4;
  const rows = Math.ceil(total / cols);
  const grid = [];
  ordered.forEach((p, i) => {
    const row = Math.floor(i / cols);
    const col = i % cols;
    let spanW = 1, spanH = 1;
    if(p.attentionScore > 50 && !p.locked && col === 0 && row === 0){
      spanW = 2;
      spanH = 1;
    }
    const rank = i + 1;
    const isCompact = rank > Math.min(6, Math.ceil(total * 0.6)) && !p.locked;
    grid.push({
      panelId: p.id,
      col: col,
      row: row,
      spanW: Math.min(spanW, cols - col),
      spanH: spanH,
      compact: isCompact,
      rank: rank,
      panel: p
    });
  });
  return {grid, cols, rows};
}
// ---- Render ----
function render(){
  const {grid, cols} = computeLayout();
  const gridColStr = cols <= 4 ? 'repeat(2,1fr)' : cols <= 6 ? 'repeat(3,1fr)' : 'repeat(4,1fr)';
  const dash = document.getElementById('dashboard');
  dash.style.gridTemplateColumns = gridColStr;
  recalcScores();
  const existingIds = new Set();
  grid.forEach(g => existingIds.add(g.panelId));
  const currentPanelIds = new Set();
  dash.querySelectorAll('.panel').forEach(el => {
    const pid = el.dataset.panelId;
    if(!existingIds.has(pid)){
      el.remove();
    } else {
      currentPanelIds.add(pid);
    }
  });
  grid.forEach(g => {
    const p = g.panel;
    let el = dash.querySelector(`[data-panel-id="${p.id}"]`);
    if(!el){
      el = document.createElement('div');
      el.className = 'panel';
      el.dataset.panelId = p.id;
      el.innerHTML = `
        <div class="panel-header">
          <span class="drag-handle">&#9776;</span>
          <span class="rank-badge" id="rank-${p.id}">#${g.rank}</span>
          <span class="attention-badge" id="attn-${p.id}">${p.attentionScore.toFixed(1)}</span>
          <h3>${p.title}</h3>
          <div class="panel-actions">
            <button class="lock-btn" id="lock-${p.id}" title="Lock position">&#128274;</button>
            <button class="collapse-btn" id="collapse-${p.id}" title="Collapse">&#8722;</button>
          </div>
        </div>
        <div class="panel-body" id="body-${p.id}"></div>
      `;
      dash.appendChild(el);
      el.querySelector('.lock-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        toggleLock(p.id);
      });
      el.querySelector('.collapse-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        toggleCollapse(p.id);
      });
      el.addEventListener('mouseenter', () => trackView(p.id));
      el.addEventListener('click', () => trackInteraction(p.id));
      makeDraggable(el, p.id);
    }
    el.className = 'panel';
    if(p.locked) el.classList.add('locked');
    if(g.compact && !p.locked) el.classList.add('compact');
    el.style.gridColumn = `${g.col + 1} / span ${g.spanW}`;
    el.style.gridRow = `${g.row + 1} / span ${g.spanH}`;
    const rankEl = el.querySelector('.rank-badge');
    if(rankEl) rankEl.textContent = `#${g.rank}`;
    const attnEl = el.querySelector('.attention-badge');
    if(attnEl) attnEl.textContent = p.attentionScore.toFixed(1);
    const lockEl = el.querySelector('.lock-btn');
    if(lockEl) lockEl.className = `lock-btn${p.locked ? ' locked' : ''}`;
    const collapseEl = el.querySelector('.collapse-btn');
    if(collapseEl) collapseEl.textContent = p.collapsed ? '+' : '\u2212';
    const bodyEl = document.getElementById(`body-${p.id}`);
    if(bodyEl) renderPanelBody(bodyEl, p, g.compact && !p.locked);
  });
  updateBadges();
  saveState();
}
// ---- Panel Body Rendering ----
function renderPanelBody(el, panel, compact){
  const c = panel.color;
  el.innerHTML = '';
  const styleCompact = compact ? ' style="flex-direction:row;gap:12px;min-height:auto;padding:6px 14px"' : '';
  switch(panel.type){
    case 'metric':
      if(panel.id === 'cpu'){
        const val = Math.round(20 + Math.random() * 60);
        el.innerHTML = `<span class="metric-value" style="color:${c}">${val}%</span>` +
          (!compact ? `<span class="metric-label">current load</span><div class="metric-bar"><div class="metric-bar-fill" style="width:${val}%;background:${c}"></div></div>` : '');
      } else if(panel.id === 'memory'){
        const used = Math.round(40 + Math.random() * 40);
        el.innerHTML = `<span class="metric-value" style="color:${c}">${used}%</span>` +
          (!compact ? `<span class="metric-label">of 32 GB used</span><div class="metric-bar"><div class="metric-bar-fill" style="width:${used}%;background:${c}"></div></div>` : '');
      } else if(panel.id === 'temperature'){
        const temp = (50 + Math.random() * 30).toFixed(1);
        el.innerHTML = `<span class="metric-value" style="color:${c}">${temp}°C</span>` +
          (!compact ? `<span class="metric-label">core temp</span><div class="metric-bar"><div class="metric-bar-fill" style="width:${((temp-40)/40*100).toFixed(0)}%;background:${c}"></div></div>` : '');
      }
      break;
    case 'chart':
      const pts = Array.from({length:20},()=>Math.round(Math.random()*40+10));
      const max = Math.max(...pts);
      const path = pts.map((v,i)=>`${i*5},${50-(v/max*40)}`).join(' ');
      el.innerHTML = `<svg viewBox="0 0 100 50" class="chart-svg"><polyline points="${path}" fill="none" stroke="${c}" stroke-width="1.5"/></svg>` +
        (!compact ? `<span class="metric-label" style="color:${c}">${panel.id==='network'?'MB/s':'IOPS'}</span>` : '');
      break;
    case 'list':
      const procs = [
        {name:'nginx',cpu:'2.1%'},{name:'node',cpu:'8.4%'},{name:'python3',cpu:'12.7%'},{name:'postgres',cpu:'3.2%'}
      ];
      if(compact){
        el.innerHTML = `<span style="font-size:11px;color:#8b949e">${procs.slice(0,2).map(p=>p.name).join(', ')}</span>`;
      } else {
        el.innerHTML = `<div class="process-list">${procs.map(p=>
          `<div class="proc-row"><span class="proc-name">${p.name}</span><span class="proc-cpu">${p.cpu}</span></div>`
        ).join('')}</div>`;
      }
      break;
    case 'stat':
      const hours = Math.floor(Math.random()*200+100);
      if(compact){
        el.innerHTML = `<span style="font-size:14px;color:${c}">${hours}h</span>`;
      } else {
        el.innerHTML = `<span class="metric-value" style="font-size:36px;color:${c}">${hours}h</span><span class="metric-label">since last restart</span>`;
      }
      break;
    case 'log':
      const logs = [
        '2026-06-28 03:07:42 [INFO] Connection pool refreshed',
        '2026-06-28 03:07:15 [WARN] Disk I/O latency spike at 142ms',
        '2026-06-28 03:06:58 [ERROR] Timeout on upstream health check',
        '2026-06-28 03:06:30 [INFO] Session store replicated OK'
      ];
      if(compact){
        el.innerHTML = `<span style="font-size:10px;color:${c}">${logs[2].slice(-40)}</span>`;
      } else {
        el.innerHTML = logs.map(l => {
          const cls = l.includes('[ERROR]') ? 'error' : l.includes('[WARN]') ? 'warn' : '';
          return `<div class="log-line ${cls}">${l}</div>`;
        }).join('');
      }
      break;
  }
}
// ---- Tracking ----
let viewTimers = {};
function trackView(panelId){
  const now = Date.now();
  const stat = usageStats[panelId];
  if(!stat) return;
  stat.views = (stat.views || 0) + 1;
  stat.lastViewTime = now;
  if(viewTimers[panelId]) clearInterval(viewTimers[panelId]);
  const start = now;
  viewTimers[panelId] = setInterval(() => {
    const elapsed = (Date.now() - start) / 1000;
    usageStats[panelId].totalDuration = (usageStats[panelId].totalDuration || 0) + elapsed;
  }, 1000);
  render();
}
function trackInteraction(panelId){
  const stat = usageStats[panelId];
  if(!stat) return;
  stat.interactions = (stat.interactions || 0) + 1;
  totalInteractions++;
  recalcScores();
  scheduleLayoutUpdate();
  updateBadges();
  saveState();
}
function toggleLock(panelId){
  const p = panels.find(x => x.id === panelId);
  if(!p) return;
  p.locked = !p.locked;
  usageStats[panelId].locked = p.locked;
  if(p.locked){
    p.manualPos = panels.indexOf(p);
    usageStats[panelId].manualPos = p.manualPos;
  } else {
    p.manualPos = null;
    usageStats[panelId].manualPos = null;
  }
  trackInteraction(panelId);
  showToast(p.locked ? `Locked ${p.title} position` : `Unlocked ${p.title}`);
  render();
}
function toggleCollapse(panelId){
  const p = panels.find(x => x.id === panelId);
  if(!p) return;
  p.collapsed = !p.collapsed;
  usageStats[panelId].collapsed = p.collapsed;
  trackInteraction(panelId);
  const el = document.querySelector(`[data-panel-id="${panelId}"]`);
  if(el) el.classList.toggle('compact', p.collapsed);
  showToast(p.collapsed ? `Collapsed ${p.title}` : `Expanded ${p.title}`);
  saveState();
}
function scheduleLayoutUpdate(){
  if(layoutTimer) clearTimeout(layoutTimer);
  layoutTimer = setTimeout(() => { layoutTimer = null; render(); }, LAYOUT_DEBOUNCE_MS);
}
// ---- Drag ----
function makeDraggable(el, panelId){
  let isDragging = false;
  let startX, startY, origCol, origRow;
  el.querySelector('.panel-header').addEventListener('mousedown', (e) => {
    if(e.target.closest('.panel-actions')) return;
    const p = panels.find(x => x.id === panelId);
    if(p && p.locked) return;
    isDragging = true;
    startX = e.clientX;
    startY = e.clientY;
    const rect = el.getBoundingClientRect();
    const dash = document.getElementById('dashboard');
    const dashRect = dash.getBoundingClientRect();
    const grid = window.getComputedStyle(dash).gridTemplateColumns.split(' ').length;
    const colW = dashRect.width / grid;
    const rowH = dashRect.height / Math.ceil(panels.length / grid);
    origCol = Math.floor((rect.left - dashRect.left) / colW);
    origRow = Math.floor((rect.top - dashRect.top) / rowH);
    el.classList.add('dragging');
    e.preventDefault();
  });
  document.addEventListener('mousemove', (e) => {
    if(!isDragging) return;
    el.style.opacity = '0.6';
  });
  document.addEventListener('mouseup', (e) => {
    if(!isDragging) return;
    isDragging = false;
    el.classList.remove('dragging');
    el.style.opacity = '';
    const dash = document.getElementById('dashboard');
    const dashRect = dash.getBoundingClientRect();
    const grid = window.getComputedStyle(dash).gridTemplateColumns.split(' ').length;
    const colW = dashRect.width / grid;
    const rowH = dashRect.height / Math.ceil(panels.length / grid);
    const dropCol = Math.floor((e.clientX - dashRect.left) / colW);
    const dropRow = Math.floor((e.clientY - dashRect.top) / rowH);
    if(dropCol < 0 || dropCol >= grid) return;
    const p = panels.find(x => x.id === panelId);
    if(!p) return;
    const targetIdx = dropRow * grid + dropCol;
    if(targetIdx < 0 || targetIdx >= panels.length) return;
    p.locked = true;
    p.manualPos = targetIdx;
    usageStats[panelId].locked = true;
    usageStats[panelId].manualPos = targetIdx;
    trackInteraction(panelId);
    showToast(`Moved ${p.title} to position ${targetIdx + 1}`);
    render();
  });
}
// ---- Persistence ----
function saveState(){
  const layoutData = panels.map(p => ({
    id: p.id,
    locked: p.locked,
    manualPos: p.manualPos,
    collapsed: p.collapsed
  }));
  localStorage.setItem(STORAGE_KEY, JSON.stringify({layoutMode, layoutData, timestamp: Date.now()}));
  const statsData = {stats: usageStats, totalInteractions, timestamp: Date.now()};
  localStorage.setItem(STORAGE_STATS_KEY, JSON.stringify(statsData));
}
function loadState(){
  const saved = localStorage.getItem(STORAGE_KEY);
  if(saved){
    try{
      const data = JSON.parse(saved);
      if(data.layoutMode) layoutMode = data.layoutMode;
      if(data.layoutData){
        data.layoutData.forEach(d => {
          if(usageStats[d.id]){
            usageStats[d.id].locked = d.locked || false;
            usageStats[d.id].manualPos = d.manualPos || null;
            usageStats[d.id].collapsed = d.collapsed || false;
          }
        });
      }
    }catch(e){}
  }
}
loadState();
// ---- Badges ----
function updateBadges(){
  document.getElementById('total-interactions-badge').textContent = `${totalInteractions} interactions`;
  document.getElementById('panels-tracked-badge').textContent = `${panels.length} panels`;
  document.getElementById('layout-mode-label').textContent = layoutMode === 'auto' ? 'auto-arrange active' : 'manual override';
}
// ---- Controls ----
document.getElementById('layout-mode-select').addEventListener('change', (e) => {
  const val = e.target.value;
  if(val === 'reset'){
    layoutMode = 'auto';
    document.getElementById('layout-mode-select').value = 'auto';
    PANEL_DEFS.forEach(p => {
      usageStats[p.id] = {views:0, totalDuration:0, interactions:0, lastViewTime:0, collapsed:false, locked:false, manualPos:null};
    });
    totalInteractions = 0;
    panels = PANEL_DEFS.map(createPanelState);
    showToast('Reset layout & stats');
    render();
    return;
  }
  layoutMode = val;
  showToast(layoutMode === 'auto' ? 'Auto-arrange enabled' : 'Manual layout mode');
  render();
});
document.getElementById('save-snapshot-btn').addEventListener('click', () => {
  showToast('Layout snapshot saved');
  saveState();
});
document.getElementById('reset-stats-btn').addEventListener('click', () => {
  PANEL_DEFS.forEach(p => {
    usageStats[p.id] = {views:0, totalDuration:0, interactions:0, lastViewTime:0, collapsed:false, locked:usageStats[p.id]?.locked||false, manualPos:usageStats[p.id]?.manualPos||null};
  });
  totalInteractions = 0;
  panels = PANEL_DEFS.map(createPanelState);
  showToast('Usage stats reset (kept locks)');
  render();
});
// ---- Toast ----
function showToast(msg){
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  if(toastTimeout) clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => el.classList.remove('show'), 2000);
}
// ---- Init ----
panels = PANEL_DEFS.map(createPanelState);
recalcScores();
render();
// ---- Periodic refresh ----
setInterval(() => {
  document.querySelectorAll('.panel-body').forEach(el => {
    const panelEl = el.closest('.panel');
    if(!panelEl) return;
    const pid = panelEl.dataset.panelId;
    const p = panels.find(x => x.id === pid);
    if(!p) return;
    const isCompact = panelEl.classList.contains('compact');
    renderPanelBody(el, p, isCompact);
  });
}, 3000);
})();
</script>
</body>
</html>
```