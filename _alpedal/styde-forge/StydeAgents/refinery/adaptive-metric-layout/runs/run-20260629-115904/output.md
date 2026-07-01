<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,-apple-system,sans-serif;background:#0f1117;color:#e1e4e8;min-height:100vh;overflow-x:hidden}
.toolbar{display:flex;align-items:center;gap:12px;padding:12px 20px;background:#161b22;border-bottom:1px solid #30363d;position:sticky;top:0;z-index:100}
.toolbar h2{font-size:14px;font-weight:600;color:#58a6ff;margin-right:auto}
.toolbar button{padding:6px 14px;border:1px solid #30363d;border-radius:6px;background:#21262d;color:#c9d1d9;cursor:pointer;font-size:12px;transition:all .15s}
.toolbar button:hover{background:#30363d;border-color:#58a6ff}
.toolbar button.active{background:#1f6feb33;border-color:#58a6ff;color:#58a6ff}
.toolbar .badge{background:#30363d;padding:2px 8px;border-radius:10px;font-size:11px;color:#8b949e}
.grid{display:grid;gap:12px;padding:16px;grid-template-columns:repeat(4,1fr);grid-auto-rows:minmax(160px,auto);transition:all .4s cubic-bezier(.4,0,.2,1);max-width:1400px;margin:0 auto}
.panel{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:16px;position:relative;transition:all .35s cubic-bezier(.4,0,.2,1);cursor:grab;display:flex;flex-direction:column;overflow:hidden;min-height:140px}
.panel:hover{border-color:#58a6ff55;box-shadow:0 0 20px #58a6ff0a}
.panel.dragging{opacity:.5;cursor:grabbing;z-index:50;box-shadow:0 8px 32px #00000055}
.panel.drag-over{border-color:#58a6ff;box-shadow:0 0 24px #58a6ff22;transform:scale(1.02)}
.panel.locked{border-color:#d2992240}
.panel.locked::after{content:'🔒';position:absolute;top:8px;right:36px;font-size:12px;opacity:.7}
.panel.compact{grid-row:span 1!important;min-height:80px;padding:10px 14px;font-size:12px}
.panel.compact .panel-value{font-size:20px}
.panel.compact .panel-chart{display:none}
.panel.compact .panel-details{display:none}
.panel.collapsed{grid-row:span 1!important;min-height:48px;padding:8px 14px;display:flex;flex-direction:row;align-items:center;gap:12px}
.panel.collapsed .panel-value{font-size:16px;margin:0}
.panel.collapsed .panel-chart{display:none}
.panel.collapsed .panel-details{display:none}
.panel.collapsed .panel-title{font-size:13px;margin:0}
.panel-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px}
.panel-title{font-size:12px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px;font-weight:500}
.panel-controls{display:flex;gap:4px}
.panel-controls button{border:none;background:none;color:#8b949e;cursor:pointer;padding:2px 4px;font-size:13px;border-radius:4px;transition:all .12s;line-height:1}
.panel-controls button:hover{color:#e1e4e8;background:#30363d}
.panel-controls button.pinned{color:#d29922}
.panel-value{font-size:28px;font-weight:700;color:#e1e4e8;margin:4px 0;line-height:1.1}
.panel-sub{font-size:11px;color:#484f58;margin-bottom:4px}
.panel-chart{flex:1;min-height:40px;position:relative;margin-top:4px}
.panel-chart canvas{width:100%;height:100%}
.panel-details{font-size:10px;color:#484f58;margin-top:6px;display:flex;gap:12px}
.panel-rank{position:absolute;top:8px;right:8px;font-size:10px;color:#30363d;font-weight:600;transition:color .3s}
.panel:hover .panel-rank{color:#484f58}
.panel.high-rank{border-color:#58a6ff33}
.panel.high-rank .panel-rank{color:#58a6ff55}
.more-section{margin:0 16px 16px;max-width:1400px;margin-left:auto;margin-right:auto}
.more-toggle{display:flex;align-items:center;gap:8px;padding:8px 16px;background:#161b22;border:1px solid #30363d;border-radius:8px;color:#8b949e;cursor:pointer;font-size:12px;width:100%;text-align:left;transition:all .15s}
.more-toggle:hover{color:#c9d1d9;border-color:#58a6ff55}
.more-toggle .count{background:#30363d;padding:1px 7px;border-radius:8px;font-size:10px}
.more-panels{display:flex;gap:8px;flex-wrap:wrap;padding:8px 0}
.more-panels .mini-panel{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:6px 10px;font-size:11px;cursor:pointer;transition:all .15s;display:flex;align-items:center;gap:8px}
.more-panels .mini-panel:hover{border-color:#58a6ff;color:#58a6ff}
.stats-bar{display:flex;gap:16px;font-size:11px;color:#484f58;padding:0 4px}
.stats-bar span{display:flex;align-items:center;gap:4px}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
.updating{animation:pulse .6s ease-in-out}
</style>
</head>
<body>
<div class="toolbar">
  <h2>Adaptive Dashboard</h2>
  <span class="badge" id="sessionTime">00:00</span>
  <span class="badge" id="totalEvents">0 events</span>
  <button id="btnReset" title="Reset all tracking data">Reset</button>
  <button id="btnExport" title="Export layout">Export</button>
  <button id="btnAuto" class="active" title="Auto-layout enabled">Auto</button>
</div>
<div class="grid" id="grid"></div>
<div class="more-section" id="moreSection" style="display:none">
  <button class="more-toggle" id="moreToggle">
    Collapsed panels <span class="count" id="collapsedCount">0</span>
  </button>
  <div class="more-panels" id="morePanels" style="display:none"></div>
</div>
<script>
const PANELS = [
  {id:'revenue',title:'Revenue',value:'$12,430',sub:'+12.3% vs last week',trend:[30,35,32,38,42,39,45,48,44,50,47,52,49,55,53,58,56,62,60,65],color:'#58a6ff',rowSpan:2,colSpan:2},
  {id:'users',title:'Active Users',value:'1,847',sub:'+5.7% today',trend:[1200,1180,1220,1250,1230,1280,1300,1320,1290,1350,1380,1400,1420,1450,1480,1500,1530,1560,1600,1650,1680,1700,1730,1760,1780,1800,1810,1830,1840,1847],color:'#3fb950',rowSpan:1,colSpan:1},
  {id:'conversion',title:'Conversion Rate',value:'3.2%',sub:'-0.1% from yesterday',trend:[3.8,3.7,3.9,3.6,3.5,3.4,3.2,3.3,3.1,3.0,3.2,3.1,2.9,3.0,3.1,3.0,3.1,3.2,3.2,3.2],color:'#d29922',rowSpan:1,colSpan:1},
  {id:'latency',title:'Avg Response',value:'145ms',sub:'P95: 320ms',trend:[160,155,150,148,152,145,140,142,138,135,140,148,150,145,142,140,138,142,145,145],color:'#f0883e',rowSpan:1,colSpan:1},
  {id:'errors',title:'Error Rate',value:'0.12%',sub:'23 errors last hour',trend:[0.3,0.25,0.28,0.2,0.18,0.15,0.22,0.2,0.14,0.12,0.1,0.13,0.11,0.09,0.12,0.12,0.08,0.1,0.11,0.12],color:'#f85149',rowSpan:1,colSpan:1},
  {id:'cpu',title:'CPU Load',value:'67%',sub:'4 cores / 8 threads',trend:[45,50,48,55,52,58,60,62,58,65,68,70,72,68,65,62,64,66,68,67],color:'#a371f7',rowSpan:1,colSpan:1},
  {id:'memory',title:'Memory',value:'8.2GB',sub:'of 16GB (51%)',trend:[9.5,9.2,9.0,8.8,8.5,8.7,8.4,8.6,8.3,8.1,8.0,8.2,8.0,7.9,8.1,8.3,8.5,8.4,8.3,8.2],color:'#79c0ff',rowSpan:1,colSpan:1},
  {id:'diskio',title:'Disk I/O',value:'34 MB/s',sub:'Read: 22 / Write: 12',trend:[40,38,42,35,30,28,32,34,36,33,31,29,33,35,32,30,34,32,33,34],color:'#56d364',rowSpan:1,colSpan:1}
];
const STORAGE_KEY = 'adaptive_dashboard_state';
const SCORE_INTERVAL = 10000;
const DECAY_HALF_LIFE = 3600000;
let state = loadState();
let viewStartTimes = {};
let sessionStart = Date.now();
let autoLayout = true;
function defaultState(){
  return {
    panels:{},
    order:PANELS.map(p=>p.id),
    layoutVersion:0,
    totalSessionTime:0
  };
}
function loadState(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(raw){
      const s = JSON.parse(raw);
      PANELS.forEach(p=>{
        if(!s.panels[p.id]) s.panels[p.id] = defaultPanelState();
      });
      return s;
    }
  }catch(e){}
  const s = defaultState();
  PANELS.forEach(p=>{s.panels[p.id]=defaultPanelState();});
  return s;
}
function defaultPanelState(){
  return {
    viewDuration:0,
    interactionCount:0,
    lastInteraction:0,
    collapsed:false,
    locked:false,
    userIndex:null
  };
}
function saveState(){
  state.totalSessionTime += (Date.now() - sessionStart);
  sessionStart = Date.now();
  state.layoutVersion++;
  try{localStorage.setItem(STORAGE_KEY,JSON.stringify(state));}catch(e){}
}
function computeScore(ps){
  const now = Date.now();
  const duration = Math.max(ps.viewDuration, 100);
  const freq = Math.max(ps.interactionCount, 1);
  const age = Math.max(now - ps.lastInteraction, 1000);
  const recency = Math.exp(-age / DECAY_HALF_LIFE);
  return freq * (duration / 1000) * recency;
}
function rankPanels(){
  const scores = PANELS.map(p=>{
    const ps = state.panels[p.id];
    return {id:p.id, score:computeScore(ps), locked:ps.locked, userIndex:ps.userIndex};
  });
  scores.sort((a,b)=>b.score-a.score);
  const locked = scores.filter(s=>s.locked);
  const unlocked = scores.filter(s=>!s.locked);
  locked.sort((a,b)=>(a.userIndex??999)-(b.userIndex??999));
  unlocked.sort((a,b)=>b.score-a.score);
  const ordered = [...locked, ...unlocked];
  return ordered.map((s,i)=>({...s,rank:i+1}));
}
function buildGrid(){
  const rankings = rankPanels();
  const grid = document.getElementById('grid');
  const visible = rankings.filter(r=>!state.panels[r.id].collapsed);
  const collapsed = rankings.filter(r=>state.panels[r.id].collapsed);
  grid.innerHTML = '';
  visible.forEach((r,i)=>{
    const p = PANELS.find(p=>p.id===r.id);
    const ps = state.panels[r.id];
    const el = createPanel(p, ps, r.rank, i);
    el.dataset.panelId = p.id;
    if(ps.locked) el.classList.add('locked');
    grid.appendChild(el);
  });
  updateMoreSection(collapsed);
  updateStatsBar(rankings);
}
function updateMoreSection(collapsed){
  const section = document.getElementById('moreSection');
  const panels = document.getElementById('morePanels');
  const count = document.getElementById('collapsedCount');
  if(collapsed.length === 0){section.style.display='none';return}
  section.style.display='block';
  count.textContent = collapsed.length;
  panels.innerHTML = collapsed.map(r=>{
    const p = PANELS.find(p=>p.id===r.id);
    return `<div class="mini-panel" data-panel-id="${p.id}" onclick="expandPanel('${p.id}')" title="Click to restore">
      <strong>${p.title}</strong> ${p.value}
    </div>`;
  }).join('');
  document.getElementById('moreToggle').onclick = ()=>{
    const vis = panels.style.display !== 'none';
    panels.style.display = vis ? 'none' : 'flex';
  };
}
function updateStatsBar(rankings){
  const totalEvents = rankings.reduce((s,r)=>s+state.panels[r.id].interactionCount,0);
  document.getElementById('totalEvents').textContent = totalEvents + ' events';
}
function createPanel(panel, ps, rank, gridIndex){
  const el = document.createElement('div');
  el.className = 'panel';
  if(rank <= 2) el.classList.add('high-rank');
  el.draggable = true;
  el.dataset.panelId = panel.id;
  const compactThreshold = PANELS.length - 2;
  if(rank > compactThreshold && !ps.locked){
    el.classList.add('compact');
  }
  el.style.gridRow = `span ${panel.rowSpan}`;
  el.style.gridColumn = `span ${panel.colSpan}`;
  el.style.order = ps.locked ? (ps.userIndex ?? gridIndex) : gridIndex;
  el.innerHTML = `
    <div class="panel-header">
      <span class="panel-title">${panel.title}</span>
      <div class="panel-controls">
        <button class="pin-btn ${ps.locked?'pinned':''}" data-action="lock" title="${ps.locked?'Unlock':'Lock'} position">📌</button>
        <button data-action="collapse" title="Collapse">−</button>
      </div>
    </div>
    <div class="panel-value">${panel.value}</div>
    <div class="panel-sub">${panel.sub}</div>
    <div class="panel-chart"><canvas></canvas></div>
    <div class="panel-details">
      <span>👁 ${fmtDuration(ps.viewDuration)}</span>
      <span>👆 ${ps.interactionCount}</span>
      <span>⭐ ${computeScore(ps).toFixed(1)}</span>
    </div>
    <div class="panel-rank">#${rank}</div>
  `;
  return el;
}
function fmtDuration(ms){
  if(ms < 60000) return Math.round(ms/1000)+'s';
  return Math.round(ms/60000)+'m';
}
function drawSparklines(){
  document.querySelectorAll('.panel-chart canvas').forEach(canvas=>{
    const panelEl = canvas.closest('.panel');
    if(!panelEl) return;
    const pid = panelEl.dataset.panelId;
    const panel = PANELS.find(p=>p.id===pid);
    if(!panel || panelEl.classList.contains('compact') || panelEl.classList.contains('collapsed')) return;
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width * 2;
    canvas.height = rect.height * 2;
    canvas.style.width = rect.width+'px';
    canvas.style.height = rect.height+'px';
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    const data = panel.trend;
    const min = Math.min(...data), max = Math.max(...data);
    const range = max - min || 1;
    const pad = 4;
    ctx.clearRect(0,0,w,h);
    const grad = ctx.createLinearGradient(0,0,0,h);
    grad.addColorStop(0, panel.color+'50');
    grad.addColorStop(1, panel.color+'05');
    ctx.beginPath();
    ctx.moveTo(pad, h-pad);
    data.forEach((v,i)=>{
      const x = pad + (i/(data.length-1))*(w-2*pad);
      const y = h-pad - ((v-min)/range)*(h-2*pad);
      ctx.lineTo(x,y);
    });
    ctx.lineTo(w-pad, h-pad);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.fill();
    ctx.beginPath();
    data.forEach((v,i)=>{
      const x = pad + (i/(data.length-1))*(w-2*pad);
      const y = h-pad - ((v-min)/range)*(h-2*pad);
      if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    });
    ctx.strokeStyle = panel.color;
    ctx.lineWidth = 2.5;
    ctx.stroke();
    const last = data[data.length-1];
    const lx = pad + ((data.length-1)/(data.length-1))*(w-2*pad);
    const ly = h-pad - ((last-min)/range)*(h-2*pad);
    ctx.beginPath();
    ctx.arc(lx,ly,4,0,Math.PI*2);
    ctx.fillStyle = panel.color;
    ctx.fill();
    ctx.strokeStyle = '#161b22';
    ctx.lineWidth = 2;
    ctx.stroke();
  });
}
function setupObservers(){
  if(window._observer) window._observer.disconnect();
  const observer = new IntersectionObserver((entries)=>{
    const now = Date.now();
    entries.forEach(e=>{
      const pid = e.target.dataset.panelId;
      if(!pid) return;
      if(e.isIntersecting){
        viewStartTimes[pid] = now;
      }else if(viewStartTimes[pid]){
        const elapsed = now - viewStartTimes[pid];
        state.panels[pid].viewDuration += elapsed;
        delete viewStartTimes[pid];
      }
    });
  },{threshold:0.3});
  document.querySelectorAll('.panel').forEach(el=>observer.observe(el));
  window._observer = observer;
}
function flushViewTimes(){
  const now = Date.now();
  Object.keys(viewStartTimes).forEach(pid=>{
    if(viewStartTimes[pid]){
      state.panels[pid].viewDuration += now - viewStartTimes[pid];
      viewStartTimes[pid] = now;
    }
  });
}
function setupInteractions(){
  document.getElementById('grid').addEventListener('click',e=>{
    const btn = e.target.closest('button[data-action]');
    if(!btn) return;
    const panelEl = btn.closest('.panel');
    if(!panelEl) return;
    const pid = panelEl.dataset.panelId;
    const action = btn.dataset.action;
    recordInteraction(pid);
    if(action === 'lock') toggleLock(pid);
    if(action === 'collapse') collapsePanel(pid);
  });
  document.getElementById('grid').addEventListener('mouseover',e=>{
    const panelEl = e.target.closest('.panel');
    if(panelEl) recordInteraction(panelEl.dataset.panelId);
  });
  document.getElementById('btnReset').addEventListener('click',()=>{
    if(confirm('Reset all tracking data and layout?')){
      state = defaultState();
      PANELS.forEach(p=>{state.panels[p.id]=defaultPanelState();});
      saveState();
      rebuild();
    }
  });
  document.getElementById('btnExport').addEventListener('click',()=>{
    flushViewTimes();
    saveState();
    const blob = new Blob([JSON.stringify(state,null,2)],{type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href=url;a.download='dashboard-layout-'+new Date().toISOString().slice(0,10)+'.json';
    a.click();
    URL.revokeObjectURL(url);
  });
  document.getElementById('btnAuto').addEventListener('click',function(){
    autoLayout = !autoLayout;
    this.classList.toggle('active',autoLayout);
    this.textContent = autoLayout ? 'Auto' : 'Manual';
    if(autoLayout) rebuild();
  });
  setupDragDrop();
}
function setupDragDrop(){
  const grid = document.getElementById('grid');
  let draggedEl = null;
  grid.addEventListener('dragstart',e=>{
    const panel = e.target.closest('.panel');
    if(!panel) return;
    draggedEl = panel;
    panel.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', panel.dataset.panelId);
  });
  grid.addEventListener('dragend',e=>{
    if(draggedEl){
      draggedEl.classList.remove('dragging');
      const pid = draggedEl.dataset.panelId;
      state.panels[pid].locked = true;
      const children = [...grid.children];
      state.panels[pid].userIndex = children.indexOf(draggedEl);
      autoLayout = false;
      document.getElementById('btnAuto').classList.remove('active');
      document.getElementById('btnAuto').textContent = 'Manual';
      saveState();
      rebuild();
      draggedEl = null;
    }
  });
  grid.addEventListener('dragover',e=>{
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    document.querySelectorAll('.panel.drag-over').forEach(el=>el.classList.remove('drag-over'));
    const target = e.target.closest('.panel');
    if(target && target !== draggedEl) target.classList.add('drag-over');
  });
  grid.addEventListener('drop',e=>{
    e.preventDefault();
    document.querySelectorAll('.panel.drag-over').forEach(el=>el.classList.remove('drag-over'));
    if(!draggedEl) return;
    const target = e.target.closest('.panel');
    if(!target || target === draggedEl) return;
    const children = [...grid.children];
    const fromIdx = children.indexOf(draggedEl);
    const toIdx = children.indexOf(target);
    if(fromIdx >= 0 && toIdx >= 0){
      grid.insertBefore(draggedEl, fromIdx < toIdx ? target.nextSibling : target);
    }
  });
}
function recordInteraction(pid){
  if(!pid) return;
  state.panels[pid].interactionCount++;
  state.panels[pid].lastInteraction = Date.now();
}
function toggleLock(pid){
  state.panels[pid].locked = !state.panels[pid].locked;
  if(state.panels[pid].locked){
    const children = [...document.getElementById('grid').children];
    const idx = children.findIndex(c=>c.dataset.panelId===pid);
    state.panels[pid].userIndex = idx;
  }else{
    state.panels[pid].userIndex = null;
  }
  saveState();
  rebuild();
}
function collapsePanel(pid){
  state.panels[pid].collapsed = true;
  recordInteraction(pid);
  saveState();
  rebuild();
}
function expandPanel(pid){
  state.panels[pid].collapsed = false;
  recordInteraction(pid);
  saveState();
  rebuild();
}
function rebuild(){
  flushViewTimes();
  buildGrid();
  setTimeout(()=>{
    drawSparklines();
    setupObservers();
  },100);
  saveState();
}
function updateSessionTimer(){
  const elapsed = state.totalSessionTime + (Date.now() - sessionStart);
  const mins = Math.floor(elapsed/60000);
  const secs = Math.floor((elapsed%60000)/1000);
  document.getElementById('sessionTime').textContent =
    String(mins).padStart(2,'0')+':'+String(secs).padStart(2,'0');
}
setInterval(()=>{
  flushViewTimes();
  saveState();
  if(autoLayout) rebuild();
}, SCORE_INTERVAL);
setInterval(updateSessionTimer, 1000);
const resizeObserver = new ResizeObserver(()=>{
  drawSparklines();
});
resizeObserver.observe(document.getElementById('grid'));
window.addEventListener('beforeunload',()=>{
  flushViewTimes();
  saveState();
});
window.addEventListener('visibilitychange',()=>{
  if(document.hidden){
    flushViewTimes();
    saveState();
  }else{
    sessionStart = Date.now();
  }
});
rebuild();
updateSessionTimer();
</script>
</body>
</html>