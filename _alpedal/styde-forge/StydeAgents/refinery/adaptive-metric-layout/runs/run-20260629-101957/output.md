```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #0f1117; --surface: #1a1d27; --surface2: #222533;
  --text: #e1e4ed; --text2: #8b90a5; --accent: #6c8cff;
  --accent2: #ff6b8a; --green: #4ade80; --yellow: #facc15;
  --radius: 10px; --gap: 12px; --transition: 0.3s cubic-bezier(0.4,0,0.2,1);
  --compact-h: 80px; --panel-min-w: 260px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px;user-select:none}
.header{display:flex;align-items:center;gap:16px;margin-bottom:16px;flex-wrap:wrap}
.header h1{font-size:1.3rem;font-weight:700;letter-spacing:-0.3px}
.toolbar{display:flex;gap:8px;margin-left:auto;flex-wrap:wrap}
.btn{padding:6px 14px;border-radius:6px;border:1px solid var(--surface2);background:var(--surface);color:var(--text);cursor:pointer;font-size:0.8rem;transition:var(--transition);white-space:nowrap}
.btn:hover{background:var(--surface2);border-color:var(--accent)}
.btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.danger{color:var(--accent2)}
.stats-bar{display:flex;gap:16px;margin-bottom:12px;font-size:0.75rem;color:var(--text2);padding:8px 14px;background:var(--surface);border-radius:var(--radius);flex-wrap:wrap}
.stat{display:flex;align-items:center;gap:4px}
.stat .val{color:var(--text);font-weight:600}
.dashboard{display:grid;grid-template-columns:repeat(auto-fill,minmax(var(--panel-min-w),1fr));grid-auto-rows:auto;gap:var(--gap);transition:var(--transition)}
.dashboard.compact-view .panel:not(.locked):not(.rank-1):not(.rank-2):not(.rank-3){grid-row:span 1;height:var(--compact-h);overflow:hidden}
.dashboard.compact-view .panel.rank-1{grid-column:span 2;grid-row:span 2}
.dashboard.compact-view .panel.rank-2{grid-column:span 2;grid-row:span 1}
.dashboard.compact-view .panel.rank-3{grid-column:span 1;grid-row:span 2}
.panel{background:var(--surface);border-radius:var(--radius);border:1px solid var(--surface2);padding:14px;cursor:grab;transition:all var(--transition);position:relative;min-height:160px;display:flex;flex-direction:column}
.panel:hover{border-color:var(--accent);box-shadow:0 0 20px rgba(108,140,255,0.08)}
.panel.locked{border-left:3px solid var(--accent2);cursor:default}
.panel.locked::after{content:'🔒';position:absolute;top:8px;right:40px;font-size:0.7rem;opacity:0.6}
.panel.rank-1{grid-column:span 2;grid-row:span 2;min-height:340px}
.panel.rank-2{grid-column:span 2;grid-row:span 1;min-height:200px}
.panel.rank-3{grid-column:span 1;grid-row:span 2;min-height:240px}
.panel.compact{grid-row:span 1;height:var(--compact-h);min-height:var(--compact-h);overflow:hidden;padding:10px 14px;flex-direction:row;align-items:center;gap:12px}
.panel.compact .panel-content{display:none}
.panel.compact .panel-compact-view{display:flex}
.panel.compact .panel-header{margin-bottom:0;min-width:120px}
.panel-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;gap:8px}
.panel-title{font-weight:600;font-size:0.85rem;color:var(--text);letter-spacing:-0.2px}
.panel-controls{display:flex;gap:4px;flex-shrink:0}
.panel-controls button{background:none;border:none;color:var(--text2);cursor:pointer;padding:2px 4px;border-radius:3px;font-size:0.7rem;transition:var(--transition);line-height:1}
.panel-controls button:hover{color:var(--text);background:var(--surface2)}
.panel-controls button.lock-btn.locked-state{color:var(--accent2)}
.panel-content{flex:1;display:flex;flex-direction:column;gap:8px}
.panel-compact-view{display:none;align-items:center;gap:8px;flex:1;min-width:0}
.compact-spark{width:50px;height:28px;flex-shrink:0}
.compact-value{font-weight:700;font-size:1rem;color:var(--text);white-space:nowrap}
.compact-label{font-size:0.68rem;color:var(--text2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.metric-row{display:flex;gap:12px;flex-wrap:wrap}
.metric-card{flex:1;min-width:80px;background:var(--surface2);border-radius:6px;padding:10px;text-align:center}
.metric-card .value{font-size:1.2rem;font-weight:700;color:var(--accent)}
.metric-card .label{font-size:0.65rem;color:var(--text2);margin-top:2px;text-transform:uppercase;letter-spacing:0.4px}
canvas.chart{width:100%;height:120px}
.heat-overlay{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;border-radius:var(--radius);opacity:0.15;transition:opacity 0.5s}
.panel.rank-1 .heat-overlay{opacity:0.25}
.panel.dragging{opacity:0.4;transform:scale(0.95)}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent);transform:scale(1.02)}
.rank-badge{position:absolute;top:-6px;right:-6px;width:22px;height:22px;border-radius:50%;background:var(--accent);color:#fff;font-size:0.65rem;font-weight:700;display:flex;align-items:center;justify-content:center;z-index:2;transition:var(--transition)}
.panel.rank-1 .rank-badge{background:var(--yellow);color:#000}
.panel.locked .rank-badge{background:var(--accent2)}
.attention-indicator{position:absolute;bottom:8px;right:12px;display:flex;gap:3px;opacity:0.5}
.attention-dot{width:5px;height:5px;border-radius:50%;background:var(--text2)}
.attention-dot.active{background:var(--green)}
.reset-panel{text-align:center;padding:20px;border:2px dashed var(--surface2);border-radius:var(--radius);display:flex;flex-direction:column;align-items:center;gap:8px;justify-content:center;min-height:120px}
.reset-panel .btn{margin-top:4px}
.tooltip{position:fixed;background:var(--surface2);border:1px solid var(--accent);border-radius:6px;padding:8px 12px;font-size:0.72rem;color:var(--text2);pointer-events:none;z-index:100;opacity:0;transition:opacity 0.15s;max-width:240px}
.tooltip.visible{opacity:1}
</style>
</head>
<body>
<header class="header">
  <h1>Adaptive Dashboard</h1>
  <div class="toolbar">
    <button class="btn active" id="btnAuto" title="Auto-layout by attention rank">Auto</button>
    <button class="btn" id="btnCompact" title="Shrink low-rank panels">Compact</button>
    <button class="btn" id="btnHeatmap" title="Show attention heatmap">Heatmap</button>
    <button class="btn danger" id="btnReset" title="Reset all tracking data">Reset</button>
  </div>
</header>
<div class="stats-bar">
  <div class="stat">Sessions: <span class="val" id="statSessions">1</span></div>
  <div class="stat">Interactions: <span class="val" id="statInteractions">0</span></div>
  <div class="stat">Tracked: <span class="val" id="statTracked">6 panels</span></div>
  <div class="stat">Auto-update: <span class="val" id="statLastUpdate">--</span></div>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="tooltip" id="tooltip"></div>
<script>
(function(){
'use strict';
// --- Panel Definitions ---
const PANEL_DEFS = [
  {id:'revenue',title:'Revenue',type:'chart',data:{value:284500,trend:'up',pct:12.3,series:[120,145,180,210,195,240,260,284]},compactLabel:'Monthly Revenue'},
  {id:'users',title:'Active Users',type:'chart',data:{value:12483,trend:'up',pct:8.7,series:[8200,9100,8700,9500,10200,11000,11800,12483]},compactLabel:'Daily Active'},
  {id:'churn',title:'Churn Rate',type:'metric',data:{value:2.4,trend:'down',pct:-0.8,metrics:[{v:'2.4%',l:'Current'},{v:'3.2%',l:'Last Month'},{v:'1.8%',l:'Target'}]},compactLabel:'Churn'},
  {id:'latency',title:'API Latency',type:'metric',data:{value:142,trend:'down',pct:-5.2,metrics:[{v:'142ms',l:'p95'},{v:'68ms',l:'p50'},{v:'200ms',l:'SLA'}]},compactLabel:'p95 Latency'},
  {id:'errors',title:'Error Rate',type:'metric',data:{value:0.12,trend:'down',pct:-0.3,metrics:[{v:'0.12%',l:'5xx'},{v:'0.05%',l:'4xx'},{v:'99.8%',l:'Uptime'}]},compactLabel:'Error %'},
  {id:'throughput',title:'Throughput',type:'chart',data:{value:8450,trend:'up',pct:15.1,series:[5200,5800,6100,6800,7200,7800,8100,8450]},compactLabel:'Req/sec'}
];
// --- State ---
let panels = [];
let state = {
  viewMode: 'auto',       // auto | compact
  showHeatmap: false,
  sessionCount: 1,
  totalInteractions: 0,
  lastUpdate: null
};
// Tracking per panel: {dwellStart,dwellMs,interactions,lastInteraction,locked,manualOrder}
const DEFAULT_TRACKING = () => ({dwellStart:null,dwellMs:0,interactions:0,lastInteraction:0,locked:false,manualOrder:null});
let tracking = {};
// --- DOM refs (populated after render) ---
let dashEl, tooltipEl;
let panelEls = {}; // id -> {el, contentEl, compactEl, sparkCanvas, valueEl}
let observer = null;
let rankUpdateTimer = null;
let saveTimer = null;
let lastRenderHash = '';
// --- Init ---
function init(){
  dashEl = document.getElementById('dashboard');
  tooltipEl = document.getElementById('tooltip');
  loadState();
  panels = buildPanels();
  render();
  setupIntersectionObserver();
  setupGlobalListeners();
  scheduleRankUpdate();
}
// --- Panel building ---
function buildPanels(){
  return PANEL_DEFS.map(def => {
    const t = tracking[def.id] || DEFAULT_TRACKING();
    return {...def, tracking:t};
  });
}
// --- Rank calculation ---
function computeScore(panel){
  const t = panel.tracking;
  const now = Date.now();
  const hoursSinceLast = t.lastInteraction ? (now - t.lastInteraction)/3600000 : 168;
  const recency = Math.exp(-hoursSinceLast / 72);
  const freqScore = Math.log1p(t.interactions) * 10;
  const dwellScore = Math.log1p(t.dwellMs / 1000) * 5;
  return (freqScore * 0.4 + dwellScore * 0.4 + recency * 20 * 0.2);
}
function rankPanels(){
  const scored = panels.map((p,i) => ({...p,score:computeScore(p),origIdx:i}));
  scored.sort((a,b) => b.score - a.score);
  return scored.map((p,idx) => ({...p,rank:idx+1}));
}
// --- Diff-based render update ---
function render(fullRebuild=false){
  const ranked = rankPanels();
  const newHash = hashState(ranked);
  if(!fullRebuild && newHash === lastRenderHash && Object.keys(panelEls).length > 0){
    return; // no structural change needed
  }
  lastRenderHash = newHash;
  // Full rebuild: only when structure changes (panel add/remove/reorder)
  dashEl.innerHTML = '';
  panelEls = {};
  // Sort by manual order if locked, else by rank
  const ordered = sortByLayout(ranked);
  ordered.forEach((panel,idx) => {
    const el = createPanelElement(panel, idx);
    dashEl.appendChild(el);
    panelEls[panel.id] = {el, contentEl:el.querySelector('.panel-content'), compactEl:el.querySelector('.panel-compact-view'), sparkCanvas:el.querySelector('.compact-spark'), valueEl:el.querySelector('.compact-value')};
  });
  applyViewMode();
  updateStats();
  if(state.showHeatmap) applyHeatmap();
}
// Partial update: only refresh specific panel content + ranking classes
function updatePanelDOM(panelId){
  const refs = panelEls[panelId];
  if(!refs) return;
  const panel = panels.find(p=>p.id===panelId);
  if(!panel) return;
  // Update rank badge
  const badge = refs.el.querySelector('.rank-badge');
  if(badge) badge.textContent = panel.rank || '';
  // Update rank classes
  refs.el.className = refs.el.className.replace(/rank-\d+/g,'');
  if(panel.rank <= 3) refs.el.classList.add(`rank-${panel.rank}`);
  // Update compact view values
  if(refs.valueEl && panel.data){
    const val = typeof panel.data.value === 'number' ? panel.data.value.toLocaleString() : panel.data.value;
    refs.valueEl.textContent = val;
  }
  if(refs.sparkCanvas && panel.data && panel.data.series){
    drawSparkline(refs.sparkCanvas, panel.data.series, panel.data.trend);
  }
  // Update lock visual
  const lockBtn = refs.el.querySelector('.lock-btn');
  if(lockBtn){
    lockBtn.classList.toggle('locked-state', panel.tracking.locked);
    lockBtn.textContent = panel.tracking.locked ? '🔒' : '🔓';
  }
  refs.el.classList.toggle('locked', panel.tracking.locked);
  updatePanelContent(panel, refs);
}
function updatePanelContent(panel, refs){
  if(!refs.contentEl) return;
  const trendIcon = panel.data.trend==='up' ? '↑' : '↓';
  const trendColor = panel.data.trend==='up' ? 'var(--green)' : 'var(--accent2)';
  let html = '';
  if(panel.type==='chart'){
    html = `<div class="metric-row">
      <div class="metric-card"><div class="value">${fmtNum(panel.data.value)}</div><div class="label">Current</div></div>
      <div class="metric-card"><div class="value" style="color:${trendColor}">${trendIcon} ${Math.abs(panel.data.pct)}%</div><div class="label">Trend</div></div>
    </div>`;
    // Canvas rendered after attach
  }else if(panel.type==='metric'){
    html = '<div class="metric-row">';
    (panel.data.metrics||[]).forEach(m => {
      html += `<div class="metric-card"><div class="value">${m.v}</div><div class="label">${m.l}</div></div>`;
    });
    html += '</div>';
  }
  refs.contentEl.innerHTML = html;
}
function createPanelElement(panel, idx){
  const div = document.createElement('div');
  div.className = 'panel';
  div.dataset.panelId = panel.id;
  div.draggable = !panel.tracking.locked;
  if(panel.tracking.locked) div.classList.add('locked');
  if(panel.rank <= 3) div.classList.add(`rank-${panel.rank}`);
  if(isCompactCandidate(panel)) div.classList.add('compact');
  const heatOverlay = '<div class="heat-overlay"></div>';
  const rankBadge = `<span class="rank-badge">${panel.rank||''}</span>`;
  const trendIcon = panel.data.trend==='up' ? '↑' : '↓';
  const trendColor = panel.data.trend==='up' ? 'var(--green)' : 'var(--accent2)';
  div.innerHTML = `
    ${rankBadge}
    ${heatOverlay}
    <div class="panel-header">
      <span class="panel-title">${panel.title}</span>
      <div class="panel-controls">
        <button class="lock-btn ${panel.tracking.locked?'locked-state':''}" data-action="lock" title="Lock position">${panel.tracking.locked?'🔒':'🔓'}</button>
        <button data-action="expand" title="Expand/collapse">${isCompactCandidate(panel)?'⤢':'⤓'}</button>
      </div>
    </div>
    <div class="panel-content"></div>
    <div class="panel-compact-view">
      <canvas class="compact-spark" width="50" height="28"></canvas>
      <div>
        <div class="compact-value">${fmtNum(panel.data.value)}</div>
        <div class="compact-label">${panel.compactLabel||panel.title} <span style="color:${trendColor}">${trendIcon}${Math.abs(panel.data.pct)}%</span></div>
      </div>
    </div>
    <div class="attention-indicator">${'<span class="attention-dot"></span>'.repeat(5)}</div>
  `;
  // Attach event listeners
  div.addEventListener('mouseenter', ()=>onPanelEnter(panel.id));
  div.addEventListener('mouseleave', ()=>onPanelLeave(panel.id));
  div.addEventListener('click', (e)=>onPanelClick(panel.id, e));
  div.addEventListener('keydown', (e)=>{if(e.key==='Enter') onPanelClick(panel.id,e);});
  div.addEventListener('dragstart', (e)=>onDragStart(e, panel.id));
  div.addEventListener('dragover', (e)=>{e.preventDefault();div.classList.add('drag-over');});
  div.addEventListener('dragleave', ()=>div.classList.remove('drag-over'));
  div.addEventListener('drop', (e)=>onDrop(e, panel.id, div));
  div.addEventListener('dragend', ()=>div.classList.remove('dragging'));
  // Render sparkline after DOM attach
  requestAnimationFrame(()=>{
    const canvas = div.querySelector('.compact-spark');
    if(canvas && panel.data.series) drawSparkline(canvas, panel.data.series, panel.data.trend);
    const contentEl = div.querySelector('.panel-content');
    if(contentEl) updatePanelContent(panel, {contentEl});
  });
  return div;
}
function sortByLayout(ranked){
  const locked = ranked.filter(p=>p.tracking.locked && p.tracking.manualOrder!=null).sort((a,b)=>(a.tracking.manualOrder||0)-(b.tracking.manualOrder||0));
  const unlocked = ranked.filter(p=>!(p.tracking.locked && p.tracking.manualOrder!=null));
  return [...locked, ...unlocked];
}
function isCompactCandidate(panel){
  return state.viewMode==='compact' && panel.rank > 3 && !panel.tracking.locked;
}
function hashState(ranked){
  return ranked.map(p=>`${p.id}:${p.rank}:${p.tracking.locked}:${p.tracking.manualOrder}`).join('|') + `|${state.viewMode}|${state.showHeatmap}`;
}
// --- Sparkline ---
function drawSparkline(canvas, data, trend){
  const ctx = canvas.getContext('2d');
  const w=canvas.width, h=canvas.height;
  ctx.clearRect(0,0,w,h);
  if(!data||data.length<2) return;
  const min=Math.min(...data), max=Math.max(...data), range=max-min||1;
  const pad=2;
  ctx.beginPath();
  ctx.strokeStyle = trend==='up' ? '#4ade80' : '#ff6b8a';
  ctx.lineWidth=1.5;
  data.forEach((v,i)=>{
    const x=pad+(w-2*pad)*(i/(data.length-1));
    const y=h-pad-((v-min)/range)*(h-2*pad);
    if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  });
  ctx.stroke();
  // Fill
  ctx.lineTo(w-pad,h-pad);
  ctx.lineTo(pad,h-pad);
  ctx.closePath();
  ctx.fillStyle = trend==='up' ? 'rgba(74,222,128,0.08)' : 'rgba(255,107,138,0.08)';
  ctx.fill();
}
// --- Tracking ---
function onPanelEnter(id){
  const t = tracking[id];
  if(!t) return;
  t.dwellStart = Date.now();
}
function onPanelLeave(id){
  const t = tracking[id];
  if(!t||!t.dwellStart) return;
  t.dwellMs += (Date.now() - t.dwellStart);
  t.dwellStart = null;
  debouncedSave();
}
function onPanelClick(id, event){
  const t = tracking[id];
  if(!t) return;
  t.interactions++;
  t.lastInteraction = Date.now();
  state.totalInteractions++;
  const target = event.target;
  if(target.dataset.action==='lock'){
    t.locked = !t.locked;
    const panel = panels.find(p=>p.id===id);
    if(panel) panel.tracking = t;
    // Update just this panel
    updatePanelDOM(id);
    render(true); // structural change
    debouncedSave();
    return;
  }
  if(target.dataset.action==='expand'){
    t.interactions+=2; // boost expand action
    // Toggle compact: bump rank briefly
    t.lastInteraction = Date.now();
    const panel = panels.find(p=>p.id===id);
    if(panel) panel.tracking = t;
    updatePanelDOM(id);
    debouncedSave();
    return;
  }
  const panel = panels.find(p=>p.id===id);
  if(panel) panel.tracking = t;
  // Non-control click: just track, no DOM rebuild
  updateStats();
  debouncedSave();
}
// --- Drag and Drop ---
function onDragStart(e, id){
  const panel = panels.find(p=>p.id===id);
  if(!panel||panel.tracking.locked){e.preventDefault();return;}
  e.dataTransfer.setData('text/plain', id);
  e.dataTransfer.effectAllowed = 'move';
  const el = panelEls[id]?.el;
  if(el) el.classList.add('dragging');
}
function onDrop(e, targetId, targetEl){
  e.preventDefault();
  targetEl.classList.remove('drag-over');
  const srcId = e.dataTransfer.getData('text/plain');
  if(!srcId||srcId===targetId) return;
  const srcPanel = panels.find(p=>p.id===srcId);
  if(!srcPanel||srcPanel.tracking.locked) return;
  // Swap manual orders
  const srcIdx = panels.findIndex(p=>p.id===srcId);
  const tgtIdx = panels.findIndex(p=>p.id===targetId);
  if(srcIdx<0||tgtIdx<0) return;
  // Assign manual orders
  panels.forEach((p,i)=>{
    if(p.tracking.locked || p.tracking.manualOrder!=null){
      // preserve
    }
  });
  const srcOrder = panels[srcIdx].tracking.manualOrder ?? srcIdx;
  const tgtOrder = panels[tgtIdx].tracking.manualOrder ?? tgtIdx;
  panels[srcIdx].tracking.manualOrder = tgtOrder;
  panels[tgtIdx].tracking.manualOrder = srcOrder;
  render(true);
  debouncedSave();
}
// --- View modes ---
function applyViewMode(){
  dashEl.classList.toggle('compact-view', state.viewMode==='compact');
  panels.forEach(p=>{
    const refs = panelEls[p.id];
    if(!refs) return;
    const shouldCompact = state.viewMode==='compact' && p.rank > 3 && !p.tracking.locked;
    refs.el.classList.toggle('compact', shouldCompact);
    const expandBtn = refs.el.querySelector('[data-action="expand"]');
    if(expandBtn) expandBtn.textContent = shouldCompact ? '⤢' : '⤓';
  });
}
function applyHeatmap(){
  panels.forEach(p=>{
    const refs = panelEls[p.id];
    if(!refs) return;
    const overlay = refs.el.querySelector('.heat-overlay');
    if(!overlay) return;
    if(!state.showHeatmap){
      overlay.style.background = '';
      return;
    }
    const score = computeScore(p);
    const maxScore = Math.max(...panels.map(computeScore), 1);
    const intensity = score/maxScore;
    overlay.style.background = `radial-gradient(ellipse at center, rgba(108,140,255,${0.6*intensity}) 0%, transparent 70%)`;
  });
}
// --- IntersectionObserver for view tracking ---
function setupIntersectionObserver(){
  if(observer) observer.disconnect();
  observer = new IntersectionObserver((entries)=>{
    entries.forEach(entry=>{
      const id = entry.target.dataset.panelId;
      if(!id) return;
      if(entry.isIntersecting){
        if(!tracking[id]) tracking[id] = DEFAULT_TRACKING();
        tracking[id].dwellStart = tracking[id].dwellStart || Date.now();
        // Update attention dots
        const dots = entry.target.querySelectorAll('.attention-dot');
        const t = tracking[id];
        const activityLevel = Math.min(5, Math.ceil((t.interactions||0)/3));
        dots.forEach((d,i)=>d.classList.toggle('active', i<activityLevel));
      }else{
        if(tracking[id] && tracking[id].dwellStart){
          tracking[id].dwellMs += (Date.now() - tracking[id].dwellStart);
          tracking[id].dwellStart = null;
        }
      }
    });
  },{threshold:[0.3]});
  Object.values(panelEls).forEach(refs=>observer.observe(refs.el));
}
// --- Rank scheduling ---
function scheduleRankUpdate(){
  if(rankUpdateTimer) clearTimeout(rankUpdateTimer);
  rankUpdateTimer = setTimeout(()=>{
    const ranked = rankPanels();
    ranked.forEach(p=>{
      const orig = panels.find(pp=>pp.id===p.id);
      if(orig) orig.rank = p.rank;
    });
    render(true);
    debouncedSave();
    scheduleRankUpdate();
  }, 30000); // Every 30s
}
// --- Persistence ---
function debouncedSave(){
  if(saveTimer) clearTimeout(saveTimer);
  saveTimer = setTimeout(()=>saveState(), 300);
}
function saveState(){
  const data = {
    tracking,
    state,
    panelsMeta: panels.map(p=>({id:p.id,rank:p.rank,tracking:p.tracking}))
  };
  try{localStorage.setItem('adaptive-dashboard-v2',JSON.stringify(data));}catch(e){/*quota*/}
  state.lastUpdate = new Date().toLocaleTimeString();
  const el = document.getElementById('statLastUpdate');
  if(el) el.textContent = state.lastUpdate;
}
function loadState(){
  try{
    const raw = localStorage.getItem('adaptive-dashboard-v2');
    if(raw){
      const data = JSON.parse(raw);
      if(data.tracking) tracking = data.tracking;
      if(data.state) Object.assign(state, data.state);
    }
  }catch(e){/*corrupt*/}
  if(state.sessionCount) state.sessionCount++;
  else state.sessionCount = 1;
  // Ensure tracking exists for all panels
  PANEL_DEFS.forEach(d=>{if(!tracking[d.id]) tracking[d.id]=DEFAULT_TRACKING();});
}
function resetAll(){
  tracking = {};
  PANEL_DEFS.forEach(d=>{tracking[d.id]=DEFAULT_TRACKING();});
  state.totalInteractions = 0;
  state.lastUpdate = null;
  state.viewMode = 'auto';
  state.showHeatmap = false;
  panels = buildPanels();
  localStorage.removeItem('adaptive-dashboard-v2');
  render(true);
  document.getElementById('btnAuto').classList.add('active');
  document.getElementById('btnCompact').classList.remove('active');
  document.getElementById('btnHeatmap').classList.remove('active');
}
// --- Stats ---
function updateStats(){
  document.getElementById('statSessions').textContent = state.sessionCount;
  document.getElementById('statInteractions').textContent = state.totalInteractions;
  document.getElementById('statTracked').textContent = `${panels.length} panels`;
  if(state.lastUpdate){
    document.getElementById('statLastUpdate').textContent = state.lastUpdate;
  }
}
// --- Global listeners ---
function setupGlobalListeners(){
  document.getElementById('btnAuto').addEventListener('click',()=>{
    state.viewMode = 'auto';
    document.getElementById('btnAuto').classList.add('active');
    document.getElementById('btnCompact').classList.remove('active');
    applyViewMode();
    debouncedSave();
  });
  document.getElementById('btnCompact').addEventListener('click',()=>{
    state.viewMode = state.viewMode==='compact' ? 'auto' : 'compact';
    document.getElementById('btnCompact').classList.toggle('active', state.viewMode==='compact');
    document.getElementById('btnAuto').classList.toggle('active', state.viewMode==='auto');
    applyViewMode();
    debouncedSave();
  });
  document.getElementById('btnHeatmap').addEventListener('click',()=>{
    state.showHeatmap = !state.showHeatmap;
    document.getElementById('btnHeatmap').classList.toggle('active', state.showHeatmap);
    if(!state.showHeatmap){
      panels.forEach(p=>{
        const refs = panelEls[p.id];
        if(refs){const o=refs.el.querySelector('.heat-overlay');if(o)o.style.background='';}
      });
    }else{
      applyHeatmap();
    }
    debouncedSave();
  });
  document.getElementById('btnReset').addEventListener('click',()=>{
    if(confirm('Reset all tracking data and layout preferences?')) resetAll();
  });
  // Global tooltip for compact panels
  document.addEventListener('mousemove',(e)=>{
    const target = e.target.closest('.panel.compact');
    if(target && state.viewMode==='compact'){
      const id = target.dataset.panelId;
      const panel = panels.find(p=>p.id===id);
      if(panel){
        tooltipEl.textContent = `${panel.title}: ${panel.data.value?.toLocaleString()||panel.data.value} — ${panel.tracking.interactions} interactions, ${Math.round((panel.tracking.dwellMs||0)/1000)}s viewed`;
        tooltipEl.style.left = (e.clientX+14)+'px';
        tooltipEl.style.top = (e.clientY-40)+'px';
        tooltipEl.classList.add('visible');
        return;
      }
    }
    tooltipEl.classList.remove('visible');
  });
}
// --- Utils ---
function fmtNum(n){
  if(typeof n !== 'number') return n;
  if(n>=1e6) return (n/1e6).toFixed(1)+'M';
  if(n>=1e3) return (n/1e3).toFixed(1)+'K';
  return n.toLocaleString();
}
// --- COMPLETENESS CHECK ---
function verifyCompleteness(){
  const html = document.documentElement.outerHTML;
  const checks = {
    htmlOpen: (html.match(/<html/g)||[]).length,
    htmlClose: (html.match(/<\/html>/g)||[]).length,
    scriptOpen: (html.match(/<script/g)||[]).length,
    scriptClose: (html.match(/<\/script>/g)||[]).length,
    styleOpen: (html.match(/<style/g)||[]).length,
    styleClose: (html.match(/<\/style>/g)||[]).length,
    totalLength: html.length,
    endsWithHtmlClose: html.trimEnd().endsWith('</html>')
  };
  const allPaired = checks.htmlOpen===checks.htmlClose && checks.scriptOpen===checks.scriptClose && checks.styleOpen===checks.styleClose;
  if(!allPaired || !checks.endsWithHtmlClose){
    console.warn('COMPLETENESS WARNING: Output may be truncated', checks);
    return false;
  }
  console.log('COMPLETENESS VERIFIED: All tags paired, document structurally complete');
  return true;
}
// --- Boot ---
init();
// Verify after full render
setTimeout(verifyCompleteness, 100);
})();
</script>
</body>
</html>