```html
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
  --text: #e1e4ed;
  --text-dim: #888ba0;
  --accent: #6c8cff;
  --accent-glow: #6c8cff44;
  --warn: #ffaa44;
  --danger: #ff5566;
  --success: #44cc88;
  --radius: 10px;
  --gap: 12px;
  --transition: 0.3s cubic-bezier(0.4,0,0.2,1);
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
.toolbar{display:flex;align-items:center;gap:16px;padding:12px 20px;background:#141820;border-bottom:1px solid var(--panel-border);position:sticky;top:0;z-index:100}
.toolbar h1{font-size:18px;font-weight:600;letter-spacing:-0.3px}
.toolbar .badge{font-size:11px;background:var(--accent);color:#fff;padding:3px 10px;border-radius:20px;font-weight:500}
.toolbar .spacer{flex:1}
.toolbar button{background:#1e2230;border:1px solid var(--panel-border);color:var(--text);padding:7px 14px;border-radius:6px;cursor:pointer;font-size:13px;transition:var(--transition)}
.toolbar button:hover{background:#2a2e3e;border-color:var(--accent)}
.toolbar button.ghost{background:transparent;border-color:transparent}
.toolbar .score{font-size:12px;color:var(--text-dim)}
.dashboard{display:grid;gap:var(--gap);padding:16px;grid-auto-flow:dense;transition:var(--transition)}
.dashboard.cols-4{grid-template-columns:repeat(4,1fr)}
.dashboard.cols-3{grid-template-columns:repeat(3,1fr)}
.dashboard.cols-2{grid-template-columns:repeat(2,1fr)}
.panel{background:var(--panel-bg);border:1px solid var(--panel-border);border-radius:var(--radius);padding:16px;position:relative;transition:all var(--transition);display:flex;flex-direction:column;gap:10px;min-height:120px}
.panel:hover{border-color:#3a3f55}
.panel.locked{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent),0 0 20px var(--accent-glow)}
.panel.high-rank{grid-column:span 2;grid-row:span 2;min-height:260px}
.panel.normal-rank{grid-column:span 1;grid-row:span 1}
.panel.compact-rank{grid-column:span 1;grid-row:span 1;min-height:80px;padding:10px;font-size:12px}
.panel.dimmed{opacity:0.55;transform:scale(0.97)}
.panel.dragging{opacity:0.85;z-index:50;box-shadow:0 8px 40px #00000055}
.panel.drag-over{border-color:var(--accent);background:#1e2438}
.panel-header{display:flex;align-items:center;gap:8px}
.panel-header .title{font-size:14px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-header .rank-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.panel-header .rank-dot.hot{background:var(--danger);box-shadow:0 0 8px var(--danger)}
.panel-header .rank-dot.warm{background:var(--warn);box-shadow:0 0 6px var(--warn)}
.panel-header .rank-dot.cold{background:var(--text-dim)}
.panel-metric{font-size:28px;font-weight:700;letter-spacing:-0.5px}
.panel-compact .panel-metric{font-size:20px}
.panel-sub{font-size:11px;color:var(--text-dim)}
.panel-actions{display:flex;gap:6px;margin-left:auto}
.panel-actions button{background:transparent;border:none;color:var(--text-dim);cursor:pointer;font-size:16px;padding:2px 6px;border-radius:4px;line-height:1;transition:var(--transition)}
.panel-actions button:hover{color:var(--text);background:#2a2e3e}
.panel-actions button.lock-btn.locked{color:var(--accent)}
.panel-actions button.expand-btn{font-size:18px}
.panel-bar{height:3px;border-radius:2px;position:absolute;bottom:0;left:0;transition:width 0.5s}
.panel-bar.hot{background:var(--danger)}
.panel-bar.warm{background:var(--warn)}
.panel-bar.cold{background:var(--text-dim)}
.drawer-toggle{position:fixed;right:0;top:50%;transform:translateY(-50%);background:var(--panel-bg);border:1px solid var(--panel-border);border-right:none;color:var(--text);padding:12px 8px;border-radius:8px 0 0 8px;cursor:pointer;z-index:90;writing-mode:vertical-rl;font-size:12px;letter-spacing:1px;transition:var(--transition)}
.drawer-toggle:hover{background:#2a2e3e;padding-right:12px}
.drawer-toggle .count{font-weight:700;color:var(--accent)}
.drawer{position:fixed;right:-360px;top:0;width:340px;height:100vh;background:#141820;border-left:1px solid var(--panel-border);z-index:95;transition:right var(--transition);overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}
.drawer.open{right:0}
.drawer h3{font-size:14px;color:var(--text-dim);text-transform:uppercase;letter-spacing:1px;margin-bottom:4px}
.drawer-panel{background:var(--panel-bg);border:1px solid var(--panel-border);border-radius:var(--radius);padding:12px;cursor:grab;transition:var(--transition);font-size:12px}
.drawer-panel:hover{border-color:var(--accent)}
.drawer-panel:active{cursor:grabbing}
.drawer-panel .title{font-weight:600;font-size:13px}
.drawer-panel .metric{font-size:18px;font-weight:700;margin-top:4px}
.drawer-panel .score-text{font-size:10px;color:var(--text-dim);margin-top:2px}
.picker-overlay{position:fixed;inset:0;background:#00000088;z-index:200;display:none;align-items:center;justify-content:center}
.picker-overlay.active{display:flex}
.picker{background:var(--panel-bg);border:1px solid var(--panel-border);border-radius:14px;padding:24px;width:420px;max-width:90vw}
.picker h3{margin-bottom:12px}
.picker-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:16px}
.picker-cell{aspect-ratio:1;border:1px solid var(--panel-border);border-radius:6px;cursor:pointer;transition:var(--transition);position:relative}
.picker-cell:hover{background:#2a2e3e}
.picker-cell.selected{background:var(--accent);border-color:var(--accent)}
.picker-cell.occupied{background:#2a1a1a;border-color:var(--danger);cursor:not-allowed}
.picker-cell.in-region{background:var(--accent-glow)}
.picker-actions{display:flex;gap:8px;justify-content:flex-end}
.picker-actions button{padding:8px 18px;border-radius:6px;border:1px solid var(--panel-border);background:#1e2230;color:var(--text);cursor:pointer}
.picker-actions button.primary{background:var(--accent);border-color:var(--accent)}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#2a2e3e;border:1px solid var(--panel-border);color:var(--text);padding:10px 20px;border-radius:8px;font-size:13px;z-index:300;opacity:0;transition:opacity 0.3s}
.toast.show{opacity:1}
@media(max-width:900px){.dashboard.cols-4{grid-template-columns:repeat(3,1fr)}.panel.high-rank{grid-column:span 2}}
@media(max-width:600px){.dashboard.cols-4,.dashboard.cols-3{grid-template-columns:repeat(2,1fr)}.panel.high-rank{grid-column:span 2;grid-row:span 1}}
</style>
</head>
<body>
<div class="toolbar">
  <h1>Adaptive Dashboard</h1>
  <span class="badge" id="trackBadge">tracking</span>
  <span class="spacer"></span>
  <span class="score" id="layoutScore">Layout score: 0</span>
  <button onclick="resetAll()" class="ghost">Reset</button>
  <button onclick="toggleDrawer()">Drawer <span id="drawerCount">0</span></button>
</div>
<div class="dashboard cols-4" id="dashboard"></div>
<div class="drawer-toggle" onclick="toggleDrawer()">MORE <span class="count" id="drawerCount2">0</span></div>
<div class="drawer" id="drawer"></div>
<div class="picker-overlay" id="pickerOverlay">
  <div class="picker">
    <h3>Select region for <span id="pickerPanelName"></span></h3>
    <p style="font-size:12px;color:var(--text-dim);margin-bottom:8px">Click start cell, then end cell to define span. Occupied cells shown in red.</p>
    <div class="picker-grid" id="pickerGrid"></div>
    <div class="picker-actions">
      <button onclick="closePicker()">Cancel</button>
      <button class="primary" onclick="confirmPicker()">Place Here</button>
    </div>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
// ── State ──────────────────────────────────────────────
const LS_KEY = 'adaptive_dashboard_v2';
let panels = [];
let layout = {};       // panelId -> {row,col,rowSpan,colSpan,locked}
let behaviorLog = {};  // panelId -> {viewMs,freq,lastTs,heatmap[]}
let viewTimers = {};
let activeColumns = 4;
let drawerOpen = false;
let draggedPanel = null;
let pickerData = null;
// ── Default panels ────────────────────────────────────
const DEFAULT_PANELS = [
  {id:'cpu',title:'CPU Usage',metric:'23%',sub:'4 cores · 2.1 GHz',color:'#6c8cff'},
  {id:'mem',title:'Memory',metric:'7.2 GB',sub:'15.6 GB total',color:'#44cc88'},
  {id:'disk',title:'Disk I/O',metric:'142 MB/s',sub:'NVMe · 78% health',color:'#ffaa44'},
  {id:'net',title:'Network',metric:'1.2 Gbps',sub:'↓ 890 · ↑ 310 Mbps',color:'#cc66ff'},
  {id:'temp',title:'CPU Temp',metric:'62°C',sub:'Max 85°C · Fan 2400 RPM',color:'#ff5566'},
  {id:'req',title:'Requests/s',metric:'8,432',sub:'p99 23ms · err 0.02%',color:'#44cc88'},
  {id:'cache',title:'Cache Hit',metric:'94.2%',sub:'12 GB · TTL 300s',color:'#6c8cff'},
  {id:'queue',title:'Job Queue',metric:'47',sub:'Active 12 · Failed 3',color:'#ffaa44'},
  {id:'users',title:'Active Users',metric:'1,204',sub:'Peak 3,410 · 24h',color:'#cc66ff'},
  {id:'revenue',title:'Revenue',metric:'€12.4K',sub:'+8.3% vs yesterday',color:'#44cc88'},
  {id:'errors',title:'Error Rate',metric:'0.03%',sub:'4xx: 12 · 5xx: 1',color:'#ff5566'},
  {id:'latency',title:'Latency',metric:'18ms',sub:'p50 12ms · p99 45ms',color:'#6c8cff'},
];
// ── Load / Save ───────────────────────────────────────
function loadState(){
  const raw = localStorage.getItem(LS_KEY);
  if(raw){
    const data = JSON.parse(raw);
    panels = data.panels || [...DEFAULT_PANELS];
    layout = data.layout || {};
    behaviorLog = data.behaviorLog || {};
  } else {
    panels = [...DEFAULT_PANELS];
    layout = {};
    behaviorLog = {};
  }
  // ensure behaviorLog entries exist
  panels.forEach(p => {
    if(!behaviorLog[p.id]) behaviorLog[p.id] = {viewMs:0,freq:0,lastTs:0,heatmap:[]};
  });
}
function saveState(){
  localStorage.setItem(LS_KEY, JSON.stringify({panels,layout,behaviorLog}));
}
// ── Scoring ───────────────────────────────────────────
function compositeScore(log){
  const now = Date.now();
  const ageHours = Math.max(0.1, (now - (log.lastTs||0)) / 3600000);
  const recency = 1 / (1 + ageHours * 0.5);
  const freqNorm = Math.log10(1 + (log.freq||0));
  const durNorm = Math.log10(1 + (log.viewMs||0) / 1000);
  return freqNorm * durNorm * recency;
}
function scoreRank(score){
  if(score > 1.5) return {tier:'hot',span:2};
  if(score > 0.6) return {tier:'warm',span:1};
  if(score > 0.15) return {tier:'cold',span:1};
  return {tier:'frozen',span:0}; // drawer-bound
}
// ── Responsive columns ────────────────────────────────
function computeColumns(){
  const w = window.innerWidth;
  if(w >= 1200) return 4;
  if(w >= 800) return 3;
  return 2;
}
function applyColumns(){
  const cols = computeColumns();
  if(cols !== activeColumns){
    activeColumns = cols;
    const dash = document.getElementById('dashboard');
    dash.className = 'dashboard cols-'+cols;
  }
}
// ── Occupancy Grid ────────────────────────────────────
function buildOccupancyGrid(cols, rows){
  const grid = [];
  for(let r=0;r<rows;r++){
    grid[r] = new Array(cols).fill(null);
  }
  // Register locked slots first
  const sorted = [...panels].sort((a,b) => {
    const sa = compositeScore(behaviorLog[a.id]||{viewMs:0,freq:0,lastTs:0});
    const sb = compositeScore(behaviorLog[b.id]||{viewMs:0,freq:0,lastTs:0});
    return sb - sa;
  });
  for(const p of sorted){
    const lp = layout[p.id];
    if(lp && lp.locked && lp.row !== undefined && lp.col !== undefined){
      const rs = lp.rowSpan || 1;
      const cs = lp.colSpan || 1;
      let fits = true;
      for(let r=lp.row;r<lp.row+rs && fits;r++){
        for(let c=lp.col;c<lp.col+cs && fits;c++){
          if(r>=rows || c>=cols || grid[r] && grid[r][c] !== null) fits = false;
        }
      }
      if(fits){
        for(let r=lp.row;r<lp.row+rs;r++){
          for(let c=lp.col;c<lp.col+cs;c++){
            if(r<rows && c<cols) grid[r][c] = p.id;
          }
        }
      }
    }
  }
  return {grid, sorted};
}
function findFirstSlot(grid, cols, rows, spanW, spanH){
  for(let r=0;r<rows;r++){
    for(let c=0;c<cols;c++){
      if(r+spanH > rows || c+spanW > cols) continue;
      let fits = true;
      for(let dr=0;dr<spanH && fits;dr++){
        for(let dc=0;dc<spanW && fits;dc++){
          if(grid[r+dr][c+dc] !== null) fits = false;
        }
      }
      if(fits) return {row:r, col:c};
    }
  }
  return null; // no slot found => drawer
}
// ── Layout computation (memoized) ─────────────────────
const layoutMemo = {key:'',result:null};
function computeLayout(){
  const cols = activeColumns;
  const rows = 12;
  const key = cols + '|' + panels.map(p=>p.id+(layout[p.id]?.locked?'L':'')).join(',');
  if(layoutMemo.key === key && layoutMemo.result) return layoutMemo.result;
  const {grid, sorted} = buildOccupancyGrid(cols, rows);
  const result = {};
  const drawerPanels = [];
  for(const p of sorted){
    if(layout[p.id] && layout[p.id].locked){
      result[p.id] = {...layout[p.id]};
      continue;
    }
    const score = compositeScore(behaviorLog[p.id]||{viewMs:0,freq:0,lastTs:0});
    const {tier,span} = scoreRank(score);
    if(span === 0){
      drawerPanels.push(p.id);
      continue;
    }
    const slot = findFirstSlot(grid, cols, rows, span, span);
    if(slot){
      for(let r=slot.row;r<slot.row+span;r++){
        for(let c=slot.col;c<slot.col+span;c++){
          grid[r][c] = p.id;
        }
      }
      result[p.id] = {row:slot.row, col:slot.col, rowSpan:span, colSpan:span, locked:false};
    } else {
      drawerPanels.push(p.id);
    }
  }
  layoutMemo.key = key;
  layoutMemo.result = {placed:result, drawer:drawerPanels};
  return layoutMemo.result;
}
// ── Render ────────────────────────────────────────────
function render(){
  applyColumns();
  const dash = document.getElementById('dashboard');
  const drawerEl = document.getElementById('drawer');
  const {placed, drawer:drawerPanels} = computeLayout();
  // Collect unused from layout
  for(const pid of drawerPanels){
    if(!placed[pid]) placed[pid] = {row:0,col:0,rowSpan:0,colSpan:0,locked:false};
  }
  // Render dashboard panels
  const ordered = [...panels].sort((a,b) => {
    const pa = placed[a.id]; const pb = placed[b.id];
    if(pa && !pb) return -1;
    if(!pa && pb) return 1;
    if(pa && pb){
      if(pa.row !== pb.row) return pa.row - pb.row;
      return pa.col - pb.col;
    }
    return 0;
  });
  dash.innerHTML = '';
  for(const p of ordered){
    const pl = placed[p.id];
    const isDrawer = drawerPanels.includes(p.id);
    if(isDrawer){
      continue; // skip drawer panels in main grid
    }
    const score = compositeScore(behaviorLog[p.id]||{viewMs:0,freq:0,lastTs:0});
    const {tier} = scoreRank(score);
    const locked = pl && pl.locked;
    const span = pl ? (pl.colSpan || 1) : 1;
    const cls = span >= 2 ? 'high-rank' : (tier==='cold'?'compact-rank dimmed':'normal-rank');
    const el = document.createElement('div');
    el.className = 'panel '+cls+(locked?' locked':'')+(tier==='cold'?' dimmed':'');
    el.dataset.panelId = p.id;
    el.draggable = true;
    if(pl){
      el.style.gridRow = (pl.row+1)+' / span '+(pl.rowSpan||1);
      el.style.gridColumn = (pl.col+1)+' / span '+(pl.colSpan||1);
    }
    el.innerHTML = `
      <div class="panel-header">
        <div class="rank-dot ${tier}"></div>
        <span class="title">${p.title}</span>
        <div class="panel-actions">
          <button class="lock-btn ${locked?'locked':''}" onclick="toggleLock('${p.id}')" title="${locked?'Unlock':'Lock'}">${locked?'🔒':'🔓'}</button>
          <button class="expand-btn" onclick="openPicker('${p.id}')" title="Move/Resize">⛶</button>
          <button onclick="collapsePanel('${p.id}')" title="Collapse to drawer">◀</button>
        </div>
      </div>
      <div class="panel-metric" style="color:${p.color}">${p.metric}</div>
      <div class="panel-sub">${p.sub}</div>
      <div class="panel-bar ${tier}" style="width:${Math.min(100,score*40)}%"></div>`;
    el.addEventListener('dragstart', onDragStart);
    el.addEventListener('dragend', onDragEnd);
    el.addEventListener('dragover', e => {e.preventDefault();el.classList.add('drag-over')});
    el.addEventListener('dragleave', () => el.classList.remove('drag-over'));
    el.addEventListener('drop', onDrop);
    dash.appendChild(el);
  }
  // Render drawer
  drawerEl.innerHTML = '<h3>Collapsed Panels ('+drawerPanels.length+')</h3>';
  for(const pid of drawerPanels){
    const p = panels.find(x=>x.id===pid);
    if(!p) continue;
    const score = compositeScore(behaviorLog[p.id]||{viewMs:0,freq:0,lastTs:0});
    const de = document.createElement('div');
    de.className = 'drawer-panel';
    de.draggable = true;
    de.dataset.panelId = p.id;
    de.innerHTML = `<div class="title">${p.title}</div><div class="metric" style="color:${p.color}">${p.metric}</div><div class="score-text">Score: ${score.toFixed(2)}</div>`;
    de.addEventListener('dragstart', onDrawerDragStart);
    de.addEventListener('dragend', onDragEnd);
    drawerEl.appendChild(de);
  }
  document.getElementById('drawerCount').textContent = drawerPanels.length;
  document.getElementById('drawerCount2').textContent = drawerPanels.length;
  // Intersection observers for view tracking
  setupObservers();
  saveState();
  updateLayoutScore();
}
// ── Tracking ──────────────────────────────────────────
function setupObservers(){
  // Clean up old
  Object.values(viewTimers).forEach(t => clearInterval(t));
  viewTimers = {};
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const pid = entry.target.dataset.panelId || entry.target.closest('.panel')?.dataset?.panelId;
      if(!pid) return;
      if(entry.isIntersecting){
        if(!viewTimers[pid]){
          viewTimers[pid] = setInterval(() => {
            if(!behaviorLog[pid]) behaviorLog[pid] = {viewMs:0,freq:0,lastTs:0,heatmap:[]};
            behaviorLog[pid].viewMs += 500;
            behaviorLog[pid].lastTs = Date.now();
          }, 500);
        }
        // Record interaction on observe
        if(!behaviorLog[pid]) behaviorLog[pid] = {viewMs:0,freq:0,lastTs:0,heatmap:[]};
        behaviorLog[pid].freq += 1;
        behaviorLog[pid].lastTs = Date.now();
      } else {
        if(viewTimers[pid]){
          clearInterval(viewTimers[pid]);
          delete viewTimers[pid];
        }
      }
    });
  }, {threshold:0.3});
  document.querySelectorAll('.panel').forEach(el => observer.observe(el));
}
// Record click interactions
document.addEventListener('click', e => {
  const panel = e.target.closest('.panel');
  if(!panel) return;
  const pid = panel.dataset.panelId;
  if(!pid) return;
  if(!behaviorLog[pid]) behaviorLog[pid] = {viewMs:0,freq:0,lastTs:0,heatmap:[]};
  behaviorLog[pid].freq += 2;
  behaviorLog[pid].lastTs = Date.now();
  saveState();
});
// ── Drag & Drop ───────────────────────────────────────
function onDragStart(e){
  draggedPanel = e.target.closest('.panel')?.dataset?.panelId || null;
  if(draggedPanel) e.target.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', draggedPanel||'');
}
function onDrawerDragStart(e){
  draggedPanel = e.target.closest('.drawer-panel')?.dataset?.panelId || null;
  if(draggedPanel) e.target.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', draggedPanel||'');
}
function onDragEnd(e){
  e.target.classList.remove('dragging');
  document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
}
function onDrop(e){
  e.preventDefault();
  const targetPanel = e.target.closest('.panel');
  const targetId = targetPanel?.dataset?.panelId;
  document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
  if(!draggedPanel || draggedPanel === targetId) return;
  // Swap positions or pull from drawer
  const srcLayout = layout[draggedPanel];
  const dstLayout = targetId ? layout[targetId] : null;
  if(targetId && dstLayout){
    // Swap
    const tmp = {...dstLayout};
    if(srcLayout){
      layout[draggedPanel] = {...tmp, locked: srcLayout.locked};
    } else {
      layout[draggedPanel] = {...tmp, locked: false};
    }
    layout[targetId] = srcLayout ? {...srcLayout, locked: dstLayout.locked} : {row:0,col:0,rowSpan:1,colSpan:1,locked:false};
  } else if(targetId && !dstLayout){
    // Place in target's spot, move target to drawer
    if(srcLayout){
      layout[draggedPanel] = {row:0,col:0,rowSpan:1,colSpan:1,locked:false};
    } else {
      layout[draggedPanel] = {row:0,col:0,rowSpan:1,colSpan:1,locked:false};
    }
    delete layout[targetId];
  }
  layoutMemo.key = '';
  saveState();
  render();
  toast('Panel moved');
}
// ── Lock / Unlock ─────────────────────────────────────
function toggleLock(pid){
  if(!layout[pid]) layout[pid] = {row:0,col:0,rowSpan:1,colSpan:1,locked:true};
  else layout[pid].locked = !layout[pid].locked;
  layoutMemo.key = '';
  saveState();
  render();
  toast(layout[pid].locked ? 'Panel locked' : 'Panel unlocked');
}
// ── Collapse to drawer ────────────────────────────────
function collapsePanel(pid){
  delete layout[pid];
  layoutMemo.key = '';
  saveState();
  render();
  toast('Panel moved to drawer');
}
// ── Drawer toggle ─────────────────────────────────────
function toggleDrawer(){
  drawerOpen = !drawerOpen;
  document.getElementById('drawer').classList.toggle('open', drawerOpen);
}
// ── Position Picker (multi-cell region selection) ─────
function openPicker(pid){
  pickerData = {pid, start:null, end:null};
  const overlay = document.getElementById('pickerOverlay');
  overlay.classList.add('active');
  document.getElementById('pickerPanelName').textContent = panels.find(p=>p.id===pid)?.title || pid;
  renderPickerGrid();
}
function closePicker(){
  document.getElementById('pickerOverlay').classList.remove('active');
  pickerData = null;
}
function renderPickerGrid(){
  const grid = document.getElementById('pickerGrid');
  const cols = activeColumns;
  const rows = 4;
  grid.style.gridTemplateColumns = 'repeat('+cols+',1fr)';
  grid.innerHTML = '';
  const {grid:occGrid} = buildOccupancyGrid(cols, rows);
  for(let r=0;r<rows;r++){
    for(let c=0;c<cols;c++){
      const cell = document.createElement('div');
      cell.className = 'picker-cell';
      cell.dataset.row = r;
      cell.dataset.col = c;
      const occupied = occGrid[r]?.[c] && occGrid[r][c] !== pickerData?.pid;
      if(occupied) cell.classList.add('occupied');
      // Highlight region
      if(pickerData.start && pickerData.end){
        const rMin = Math.min(pickerData.start.row, pickerData.end.row);
        const rMax = Math.max(pickerData.start.row, pickerData.end.row);
        const cMin = Math.min(pickerData.start.col, pickerData.end.col);
        const cMax = Math.max(pickerData.start.col, pickerData.end.col);
        if(r>=rMin && r<=rMax && c>=cMin && c<=cMax && !occupied){
          cell.classList.add('in-region');
        }
      }
      if(pickerData.start && pickerData.start.row===r && pickerData.start.col===c){
        cell.classList.add('selected');
      }
      cell.addEventListener('click', () => {
        if(occupied && !(pickerData.start && pickerData.start.row===r && pickerData.start.col===c)) return;
        if(!pickerData.start){
          pickerData.start = {row:r, col:c};
        } else if(!pickerData.end){
          pickerData.end = {row:r, col:c};
        }
        renderPickerGrid();
      });
      grid.appendChild(cell);
    }
  }
}
function confirmPicker(){
  if(!pickerData || !pickerData.start) return;
  const start = pickerData.start;
  const end = pickerData.end || start;
  const rowSpan = Math.abs(end.row - start.row) + 1;
  const colSpan = Math.abs(end.col - start.col) + 1;
  const row = Math.min(start.row, end.row);
  const col = Math.min(start.col, end.col);
  layout[pickerData.pid] = {row, col, rowSpan, colSpan, locked:true};
  layoutMemo.key = '';
  saveState();
  closePicker();
  render();
  toast('Panel placed & locked');
}
// ── Toast ──────────────────────────────────────────────
function toast(msg){
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._timeout);
  el._timeout = setTimeout(() => el.classList.remove('show'), 2000);
}
// ── Layout score (debug) ──────────────────────────────
function updateLayoutScore(){
  let totalScore = 0;
  for(const p of panels){
    const score = compositeScore(behaviorLog[p.id]||{viewMs:0,freq:0,lastTs:0});
    const {span} = scoreRank(score);
    const pl = layout[p.id];
    const actualSpan = pl ? (pl.colSpan||1) : 0;
    // Score how well actual span matches desired span
    totalScore += 1 - Math.abs(span - actualSpan) / Math.max(1,span);
  }
  const avg = panels.length ? Math.round((totalScore/panels.length)*100) : 0;
  document.getElementById('layoutScore').textContent = 'Layout fit: '+avg+'%';
}
// ── Reset ──────────────────────────────────────────────
function resetAll(){
  localStorage.removeItem(LS_KEY);
  panels = [...DEFAULT_PANELS];
  layout = {};
  behaviorLog = {};
  layoutMemo.key = '';
  layoutMemo.result = null;
  render();
  toast('Dashboard reset');
}
// ── Periodic re-layout ────────────────────────────────
let reLayoutTimer = null;
function scheduleReLayout(){
  clearTimeout(reLayoutTimer);
  reLayoutTimer = setTimeout(() => {
    layoutMemo.key = '';
    render();
  }, 30000); // every 30s of changes
}
// Monitor behavior changes
const origSave = saveState;
saveState = function(){
  origSave();
  scheduleReLayout();
};
// ── Init ──────────────────────────────────────────────
window.addEventListener('resize', () => {
  applyColumns();
  layoutMemo.key = '';
  render();
});
loadState();
render();
// Simulate some initial activity for demo
if(!localStorage.getItem(LS_KEY+'_seeded')){
  localStorage.setItem(LS_KEY+'_seeded','1');
  behaviorLog['cpu'] = {viewMs:45000,freq:28,lastTs:Date.now()-120000,heatmap:[]};
  behaviorLog['req'] = {viewMs:38000,freq:22,lastTs:Date.now()-300000,heatmap:[]};
  behaviorLog['mem'] = {viewMs:12000,freq:8,lastTs:Date.now()-1800000,heatmap:[]};
  behaviorLog['errors'] = {viewMs:3000,freq:3,lastTs:Date.now()-7200000,heatmap:[]};
  behaviorLog['users'] = {viewMs:20000,freq:12,lastTs:Date.now()-600000,heatmap:[]};
  saveState();
  layoutMemo.key = '';
  render();
}
</script>
</body>
</html>
```