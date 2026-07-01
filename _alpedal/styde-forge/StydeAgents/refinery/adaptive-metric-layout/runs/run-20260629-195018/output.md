<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--surface2:#222636;--border:#2d3344;
  --text:#e1e4eb;--text2:#949cb0;--accent:#6c8cff;--accent2:#4ade80;
  --warn:#f59e0b;--danger:#ef4444;--radius:10px;--gap:10px;
  --transition:0.35s cubic-bezier(0.4,0,0.2,1);
}
body{background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,sans-serif;min-height:100vh;padding:12px;overflow-x:hidden}
.ctrl-bar{display:flex;gap:8px;padding:6px 10px;margin-bottom:12px;background:var(--surface);border-radius:var(--radius);align-items:center;flex-wrap:wrap;position:sticky;top:8px;z-index:100;border:1px solid var(--border)}
.ctrl-bar button{padding:6px 14px;border:1px solid var(--border);border-radius:6px;background:var(--surface2);color:var(--text);cursor:pointer;font-size:0.82rem;transition:var(--transition);white-space:nowrap}
.ctrl-bar button:hover{background:var(--border);border-color:var(--accent)}
.ctrl-bar button.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.ctrl-bar .spacer{flex:1}
.ctrl-bar .stat{font-size:0.75rem;color:var(--text2);padding:4px 10px;background:var(--bg);border-radius:4px}
.dashboard{display:grid;grid-template-columns:repeat(12,1fr);gap:var(--gap);min-height:60vh;align-items:start}
.panel{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  transition:all var(--transition);position:relative;overflow:hidden;
  display:flex;flex-direction:column;min-height:120px;
}
.panel:hover{border-color:var(--accent);box-shadow:0 4px 20px rgba(108,140,255,0.12)}
.panel.size-xl{grid-column:span 6;grid-row:span 2}
.panel.size-lg{grid-column:span 4;grid-row:span 2}
.panel.size-md{grid-column:span 3;grid-row:span 2}
.panel.size-sm{grid-column:span 3;grid-row:span 1}
.panel.size-compact{grid-column:span 2;grid-row:span 1;min-height:80px;font-size:0.78rem}
.panel.size-compact .panel-body{padding:8px;opacity:0.7}
.panel.collapsed{display:none}
.panel.locked{border-color:var(--warn);box-shadow:0 0 0 2px rgba(245,158,11,0.25)}
.panel.dragging{opacity:0.7;z-index:200;box-shadow:0 12px 40px rgba(0,0,0,0.5);transform:scale(1.02)}
.panel-header{
  display:flex;align-items:center;gap:6px;padding:8px 10px;
  background:var(--surface2);border-bottom:1px solid var(--border);
  cursor:grab;user-select:none;min-height:36px;
}
.panel-header:active{cursor:grabbing}
.panel-header .title{font-weight:600;font-size:0.85rem;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-header .rank-badge{
  font-size:0.65rem;padding:1px 6px;border-radius:10px;background:var(--bg);
  color:var(--text2);font-weight:700;min-width:22px;text-align:center;
}
.panel-header .score-bar{
  width:40px;height:4px;background:var(--border);border-radius:2px;overflow:hidden;flex-shrink:0;
}
.panel-header .score-bar-fill{height:100%;background:var(--accent);transition:width 0.5s}
.panel-header button{
  background:none;border:none;color:var(--text2);cursor:pointer;
  font-size:0.8rem;padding:2px 4px;border-radius:4px;line-height:1;
  transition:var(--transition);flex-shrink:0;
}
.panel-header button:hover{color:var(--text);background:var(--border)}
.panel-header button.lock-btn.locked{color:var(--warn)}
.panel-body{padding:12px;flex:1;overflow:auto;font-size:0.82rem;color:var(--text2)}
.panel-body .metric{display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid var(--border);font-size:0.78rem}
.panel-body .metric .val{font-weight:700;color:var(--text)}
.panel-body .placeholder-chart{
  height:80px;background:linear-gradient(135deg,var(--accent) 0%,var(--accent2) 100%);
  border-radius:6px;opacity:0.15;margin-bottom:8px;
}
.more-section{margin-top:12px;background:var(--surface);border:1px dashed var(--border);border-radius:var(--radius);padding:8px 12px}
.more-section .more-header{display:flex;align-items:center;gap:8px;cursor:pointer;font-size:0.82rem;color:var(--text2)}
.more-section .more-header:hover{color:var(--text)}
.more-section .more-count{font-size:0.7rem;background:var(--border);border-radius:10px;padding:1px 8px}
.more-section .more-panels{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.more-section .mini-panel{
  padding:6px 10px;background:var(--surface2);border-radius:6px;
  font-size:0.72rem;cursor:pointer;border:1px solid var(--border);
  transition:var(--transition);display:flex;align-items:center;gap:6px;
}
.more-section .mini-panel:hover{border-color:var(--accent)}
.more-section .mini-panel .dot{width:6px;height:6px;border-radius:50%;background:var(--accent2)}
.toast{
  position:fixed;bottom:20px;right:20px;padding:8px 16px;background:var(--accent);
  color:#fff;border-radius:6px;font-size:0.8rem;z-index:999;
  animation:fadeInOut 2s forwards;pointer-events:none;
}
@keyframes fadeInOut{0%{opacity:0;transform:translateY(10px)}15%{opacity:1;transform:translateY(0)}70%{opacity:1}100%{opacity:0;transform:translateY(-8px)}}
@media(max-width:900px){
  .dashboard{grid-template-columns:repeat(6,1fr)}
  .panel.size-xl{grid-column:span 6}
  .panel.size-lg{grid-column:span 4}
  .panel.size-md{grid-column:span 3}
  .panel.size-sm{grid-column:span 3}
  .panel.size-compact{grid-column:span 2}
}
@media(max-width:500px){
  .dashboard{grid-template-columns:repeat(2,1fr)}
  .panel.size-xl,.panel.size-lg,.panel.size-md,.panel.size-sm{grid-column:span 2}
  .panel.size-compact{grid-column:span 1}
}
</style>
</head>
<body>
<div class="ctrl-bar">
  <button id="btn-reset" title="Reset all tracking data">Reset tracking</button>
  <button id="btn-auto" class="active" title="Auto-layout based on behavior">Auto-layout</button>
  <button id="btn-freeze" title="Freeze current layout">Freeze</button>
  <button id="btn-expand-all" title="Expand all panels">Expand all</button>
  <span class="spacer"></span>
  <span class="stat" id="stat-panels">panels: -</span>
  <span class="stat" id="stat-updates">updates: 0</span>
  <span class="stat" id="stat-session">session: 0s</span>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="more-section" id="more-section" style="display:none">
  <div class="more-header" id="more-toggle">
    Collapsed panels <span class="more-count" id="more-count">0</span>
  </div>
  <div class="more-panels" id="more-panels"></div>
</div>
<script>
// ── Adaptive Metric Layout Engine ──
const CONFIG = {
  decayHalfLife: 300_000,
  viewportThreshold: 0.5,
  recalcInterval: 15000,
  scoreWeightFreq: 0.35,
  scoreWeightDur: 0.40,
  scoreWeightRecency: 0.25,
  compactThreshold: 0.15,
  collapseThreshold: 0.05,
  maxPanels: 12,
  storageKey: 'adaptive-dashboard-v1'
};
const SIZE_CLASSES = ['size-xl','size-lg','size-md','size-sm','size-compact'];
function uid(){return Date.now().toString(36)+Math.random().toString(36).slice(2,7)}
function clamp(v,lo,hi){return Math.max(lo,Math.min(hi,v))}
// ── Panel Data ──
const INITIAL_PANELS = [
  {id:'revenue',title:'Revenue Overview',type:'chart',content:{chart:'bar',data:[120,245,310,190,340,280]}},
  {id:'users',title:'Active Users',type:'metric',content:{value:12453,delta:'+12.4%',spark:[80,95,110,105,120,130]}},
  {id:'orders',title:'Recent Orders',type:'table',content:{cols:['ID','Customer','Total'],rows:[['#1023','Acme','$240'],['#1024','Globex','$890'],['#1025','Initech','$120']]}},
  {id:'traffic',title:'Site Traffic',type:'chart',content:{chart:'line',data:[3400,3800,4200,3900,4600,5100]}},
  {id:'errors',title:'Error Rate',type:'metric',content:{value:'0.23%',delta:'-0.05%',alert:false}},
  {id:'latency',title:'API Latency',type:'chart',content:{chart:'area',data:[45,52,48,61,49,44]}},
  {id:'tasks',title:'Task Queue',type:'list',content:{items:[{t:'Deploy v2.4',s:'done'},{t:'DB migration',s:'active'},{t:'SSL renewal',s:'pending'},{t:'Audit logs',s:'pending'}]}},
  {id:'alerts',title:'System Alerts',type:'feed',content:{items:[{t:'CPU spike',ts:Date.now()-120000},{t:'Memory 82%',ts:Date.now()-300000},{t:'Disk 91%',ts:Date.now()-600000}]}},
  {id:'conversions',title:'Conversion Funnel',type:'funnel',content:{stages:[{label:'Visit',val:5400},{label:'Signup',val:1200},{label:'Trial',val:480},{label:'Paid',val:89}]}},
  {id:'support',title:'Support Tickets',type:'metric',content:{value:34,delta:'+5',spark:[12,18,15,22,28,34]}},
  {id:'backups',title:'Backup Status',type:'status',content:{status:'ok',lastRun:'2h ago',nextRun:'4h'}},
  {id:'costs',title:'Cloud Costs',type:'metric',content:{value:'$4,230',delta:'+8.3%',budget:'$5,000'}}
];
// ── State ──
let state = {
  panels: [],
  tracking: {},
  scores: {},
  ranks: {},
  layoutEpoch: 0,
  sessionStart: Date.now(),
  updateCount: 0,
  frozen: false,
  draggedPanelId: null
};
function initState(){
  const saved = localStorage.getItem(CONFIG.storageKey);
  if(saved){
    try{
      const parsed = JSON.parse(saved);
      state.panels = parsed.panels || structuredClone(INITIAL_PANELS);
      state.tracking = parsed.tracking || {};
      state.layoutEpoch = parsed.layoutEpoch || 0;
    }catch(e){ loadDefaults(); }
  }else{ loadDefaults(); }
  state.panels.forEach(p => {
    if(!state.tracking[p.id]) state.tracking[p.id] = freshTracking();
  });
  state.sessionStart = Date.now();
  document.getElementById('stat-panels').textContent = 'panels: '+state.panels.length;
}
function loadDefaults(){
  state.panels = INITIAL_PANELS.map(p => ({...p,locked:false,manualRow:null,manualCol:null,collapsed:false}));
  state.tracking = {};
  state.panels.forEach(p => { state.tracking[p.id] = freshTracking(); });
  state.layoutEpoch = 0;
}
function freshTracking(){
  return {
    viewDuration: 0, viewStart: null, interactionCount: 0,
    collapseCount: 0, expandCount: 0, lastInteraction: Date.now(),
    firstSeen: Date.now()
  };
}
function persist(){
  const data = {
    panels: state.panels.map(p => ({id:p.id,locked:p.locked,manualRow:p.manualRow,manualCol:p.manualCol,collapsed:p.collapsed})),
    tracking: state.tracking, layoutEpoch: state.layoutEpoch
  };
  try{ localStorage.setItem(CONFIG.storageKey,JSON.stringify(data)); }catch(e){}
}
// ── Scoring ──
function computeScores(){
  const now = Date.now();
  const scores = {};
  const allFreq=[], allDur=[];
  for(const p of state.panels){
    const t = state.tracking[p.id] || freshTracking();
    const sessionAge = (now - state.sessionStart) / 1000;
    const freq = sessionAge > 0 ? t.interactionCount / Math.max(sessionAge,1) : 0;
    const dur = sessionAge > 0 ? t.viewDuration / Math.max(sessionAge*1000,1) : 0;
    allFreq.push(freq); allDur.push(dur);
  }
  const maxF = Math.max(...allFreq,0.001), maxD = Math.max(...allDur,0.001);
  for(const p of state.panels){
    const t = state.tracking[p.id] || freshTracking();
    const sessionAge = (now - state.sessionStart) / 1000;
    const freq = sessionAge > 0 ? t.interactionCount / Math.max(sessionAge,1) : 0;
    const dur = sessionAge > 0 ? t.viewDuration / Math.max(sessionAge*1000,1) : 0;
    const age = (now - t.lastInteraction) / 1000;
    const halfLife = CONFIG.decayHalfLife / 1000;
    const recency = Math.exp(-age * Math.LN2 / halfLife);
    const score =
      CONFIG.scoreWeightFreq * (freq/maxF) +
      CONFIG.scoreWeightDur * (dur/maxD) +
      CONFIG.scoreWeightRecency * recency;
    scores[p.id] = clamp(Math.round(score*1000)/10,0,100);
  }
  state.scores = scores;
  state.ranks = rankPanels(scores);
}
function rankPanels(scores){
  const entries = Object.entries(scores).sort((a,b)=>b[1]-a[1]);
  const ranks = {};
  entries.forEach(([id,_],i)=>{ ranks[id]=i+1; });
  return ranks;
}
// ── Layout Assignment ──
function assignSizes(){
  const n = state.panels.length;
  const ranked = state.panels.map(p=>({...p,score:state.scores[p.id]||0,rank:state.ranks[p.id]||n}));
  ranked.sort((a,b)=>a.rank-b.rank);
  // Cap thresholds based on panel count
  const tiers = [];
  if(n>=6){ tiers.push({pct:0.2,cls:'size-xl',count:Math.max(1,Math.floor(n*0.08))}); }
  tiers.push({pct:0.25,cls:'size-lg',count:Math.max(1,Math.floor(n*0.2))});
  tiers.push({pct:0.35,cls:'size-md',count:Math.max(1,Math.floor(n*0.25))});
  tiers.push({pct:0.7,cls:'size-sm',count:Math.max(1,Math.floor(n*0.3))});
  let assigned = 0;
  for(const tier of tiers){
    const end = Math.min(assigned+tier.count, n);
    for(let i=assigned;i<end;i++) ranked[i].sizeClass = tier.cls;
    assigned = end;
  }
  for(let i=assigned;i<n;i++){
    const score = ranked[i].score;
    const maxScore = state.scores[ranked[0]?.id] || 100;
    const rel = maxScore>0 ? score/maxScore : 0;
    if(rel <= CONFIG.collapseThreshold) ranked[i].sizeClass = 'collapsed';
    else if(rel <= CONFIG.compactThreshold) ranked[i].sizeClass = 'size-compact';
    else ranked[i].sizeClass = 'size-sm';
  }
  // Apply overrides: locked panels keep their manual position
  for(const p of ranked){
    const full = state.panels.find(pp=>pp.id===p.id);
    if(full?.locked && full.manualRow!=null && full.manualCol!=null){
      p.sizeClass = full.sizeClass || p.sizeClass;
    }
    if(full?.collapsed){ p.sizeClass = 'collapsed'; }
  }
  return ranked;
}
// ── Render ──
function render(){
  const dash = document.getElementById('dashboard');
  const layout = assignSizes();
  const collapsed = layout.filter(p=>p.sizeClass==='collapsed');
  const visible = layout.filter(p=>p.sizeClass!=='collapsed');
  dash.innerHTML = '';
  for(const p of visible){
    const el = buildPanelDOM(p);
    dash.appendChild(el);
  }
  // More section
  const moreSec = document.getElementById('more-section');
  const morePanels = document.getElementById('more-panels');
  const moreCount = document.getElementById('more-count');
  if(collapsed.length > 0){
    moreSec.style.display = 'block';
    moreCount.textContent = collapsed.length;
    morePanels.innerHTML = '';
    for(const p of collapsed){
      const mini = document.createElement('div');
      mini.className = 'mini-panel';
      mini.innerHTML = '<span class="dot"></span>'+p.title;
      mini.title = 'Click to expand';
      mini.addEventListener('click',()=>{
        const fp = state.panels.find(pp=>pp.id===p.id);
        if(fp){ fp.collapsed = false; state.tracking[p.id].expandCount++; }
        recalcAndRender();
        persist();
      });
      morePanels.appendChild(mini);
    }
  }else{
    moreSec.style.display = 'none';
  }
  // Re-bind observers
  bindObservers();
  updateStats();
}
function buildPanelDOM(p){
  const el = document.createElement('div');
  el.className = 'panel '+p.sizeClass;
  if(p.locked) el.classList.add('locked');
  el.dataset.panelId = p.id;
  el.setAttribute('draggable','true');
  const score = state.scores[p.id]||0;
  const rank = state.ranks[p.id]||'-';
  el.innerHTML = `
    <div class="panel-header">
      <span class="rank-badge" title="Rank">#${rank}</span>
      <span class="title">${p.title}</span>
      <div class="score-bar"><div class="score-bar-fill" style="width:${score}%"></div></div>
      <button class="lock-btn ${p.locked?'locked':''}" data-action="lock" title="${p.locked?'Unlock':'Lock'} position">${p.locked?'🔒':'🔓'}</button>
      <button data-action="collapse" title="Collapse">⊟</button>
    </div>
    <div class="panel-body">${renderPanelBody(p)}</div>
  `;
  // Event bindings
  const header = el.querySelector('.panel-header');
  header.addEventListener('click',e=>{
    const btn = e.target.closest('button');
    if(!btn) return;
    const action = btn.dataset.action;
    if(action==='lock') toggleLock(p.id);
    if(action==='collapse') toggleCollapse(p.id);
    trackInteraction(p.id,'click');
  });
  el.addEventListener('click',()=>trackInteraction(p.id,'click'));
  el.addEventListener('mouseenter',()=>trackInteraction(p.id,'hover'));
  // Drag and drop
  el.addEventListener('dragstart',handleDragStart);
  el.addEventListener('dragend',handleDragEnd);
  el.addEventListener('dragover',e=>{e.preventDefault();el.classList.add('drag-over')});
  el.addEventListener('dragleave',()=>el.classList.remove('drag-over'));
  el.addEventListener('drop',handleDrop);
  // Scroll tracking
  el.addEventListener('scroll',()=>trackInteraction(p.id,'scroll'),{passive:true});
  return el;
}
function renderPanelBody(p){
  const c = p.content;
  switch(p.type){
    case 'chart':
      return `<div class="placeholder-chart" style="height:${p.sizeClass==='size-compact'?'40px':'80px'}"></div>
        <div style="display:flex;gap:4px;align-items:flex-end;height:${p.sizeClass==='size-compact'?'30px':'50px'}">
        ${(c.data||[]).map((v,i)=>
          `<div style="flex:1;background:var(--accent);opacity:${0.3+(v/Math.max(...c.data))*0.6};height:${(v/Math.max(...c.data))*100}%;border-radius:2px 2px 0 0;min-height:2px" title="${v}"></div>`
        ).join('')}</div>`;
    case 'metric':
      return `<div style="font-size:${p.sizeClass==='size-compact'?'1rem':'1.8rem'};font-weight:800;color:var(--text)">${c.value}</div>
        <div style="color:${(c.delta||'').startsWith('+')?'var(--accent2)':'var(--danger)'};font-size:0.78rem">${c.delta||''}</div>`;
    case 'table':
      return `<table style="width:100%;font-size:0.72rem;border-collapse:collapse">
        <tr>${(c.cols||[]).map(h=>`<th style="text-align:left;padding:3px 4px;border-bottom:1px solid var(--border);color:var(--text2)">${h}</th>`).join('')}</tr>
        ${(c.rows||[]).map(row=>`<tr>${row.map(v=>`<td style="padding:3px 4px;border-bottom:1px solid var(--border)">${v}</td>`).join('')}</tr>`).join('')}</table>`;
    case 'list':
      return `<div>${(c.items||[]).map(i=>
        `<div class="metric"><span>${i.t}</span><span class="val" style="color:${i.s==='done'?'var(--accent2)':i.s==='active'?'var(--accent)':'var(--text2)'}">${i.s}</span></div>`
      ).join('')}</div>`;
    case 'feed':
      return `<div>${(c.items||[]).map(i=>
        `<div class="metric"><span>${i.t}</span><span>${timeAgo(i.ts)}</span></div>`
      ).join('')}</div>`;
    case 'funnel':
      const maxV = Math.max(...(c.stages||[]).map(s=>s.val),1);
      return `<div>${(c.stages||[]).map(s=>
        `<div class="metric"><span>${s.label}</span><span>${s.val}</span></div>
        <div style="height:6px;background:var(--border);border-radius:3px;margin-bottom:4px;overflow:hidden">
        <div style="width:${(s.val/maxV)*100}%;height:100%;background:var(--accent);border-radius:3px"></div></div>`
      ).join('')}</div>`;
    case 'status':
      const color = c.status==='ok'?'var(--accent2)':c.status==='warn'?'var(--warn)':'var(--danger)';
      return `<div style="font-size:1.2rem;font-weight:700;color:${color}">${c.status.toUpperCase()}</div>
        <div style="font-size:0.72rem">Last: ${c.lastRun} · Next: ${c.nextRun}</div>`;
    default:
      return `<div style="color:var(--text2);font-style:italic">No preview</div>`;
  }
}
function timeAgo(ts){
  const s = Math.round((Date.now()-ts)/1000);
  if(s<60) return s+'s ago';
  if(s<3600) return Math.floor(s/60)+'m ago';
  return Math.floor(s/3600)+'h ago';
}
// ── Tracking ──
function trackInteraction(panelId, type){
  if(!state.tracking[panelId]) state.tracking[panelId] = freshTracking();
  const t = state.tracking[panelId];
  t.interactionCount++;
  t.lastInteraction = Date.now();
  if(type==='collapse') t.collapseCount++;
  if(type==='expand') t.expandCount++;
}
let observer = null;
function bindObservers(){
  if(observer) observer.disconnect();
  observer = new IntersectionObserver((entries)=>{
    const now = Date.now();
    for(const e of entries){
      const pid = e.target.dataset.panelId;
      if(!pid || !state.tracking[pid]) continue;
      if(e.isIntersecting){
        state.tracking[pid].viewStart = now;
      }else{
        if(state.tracking[pid].viewStart){
          state.tracking[pid].viewDuration += now - state.tracking[pid].viewStart;
          state.tracking[pid].viewStart = null;
        }
      }
    }
  },{threshold:CONFIG.viewportThreshold});
  document.querySelectorAll('.panel').forEach(el=>observer.observe(el));
}
// ── Actions ──
function toggleLock(panelId){
  const p = state.panels.find(pp=>pp.id===panelId);
  if(!p) return;
  p.locked = !p.locked;
  if(p.locked){
    const idx = state.panels.indexOf(p);
    p.manualRow = idx;
    p.manualCol = 0;
    p.sizeClass = p.sizeClass || 'size-md';
  }else{
    p.manualRow = null;
    p.manualCol = null;
  }
  trackInteraction(panelId,p.locked?'lock':'unlock');
  recalcAndRender();
  persist();
  toast(p.locked?p.title+' locked':p.title+' unlocked');
}
function toggleCollapse(panelId){
  const p = state.panels.find(pp=>pp.id===panelId);
  if(!p) return;
  p.collapsed = !p.collapsed;
  trackInteraction(panelId,p.collapsed?'collapse':'expand');
  recalcAndRender();
  persist();
}
// ── Drag & Drop ──
function handleDragStart(e){
  state.draggedPanelId = e.currentTarget.dataset.panelId;
  e.currentTarget.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain',state.draggedPanelId);
}
function handleDragEnd(e){
  e.currentTarget.classList.remove('dragging');
  document.querySelectorAll('.drag-over').forEach(el=>el.classList.remove('drag-over'));
  const panelId = state.draggedPanelId;
  state.draggedPanelId = null;
  // Auto-lock dragged panel
  if(panelId){
    const p = state.panels.find(pp=>pp.id===panelId);
    if(p && !p.locked){
      p.locked = true;
      p.manualRow = state.panels.indexOf(p);
      p.manualCol = 0;
      p.sizeClass = p.sizeClass || 'size-md';
      trackInteraction(panelId,'lock');
      recalcAndRender();
      persist();
      toast(p.title+' locked via drag');
    }
  }
}
function handleDrop(e){
  e.preventDefault();
  e.currentTarget.classList.remove('drag-over');
  const targetId = e.currentTarget.dataset.panelId;
  const sourceId = state.draggedPanelId || e.dataTransfer.getData('text/plain');
  if(!sourceId || !targetId || sourceId===targetId) return;
  const srcIdx = state.panels.findIndex(p=>p.id===sourceId);
  const tgtIdx = state.panels.findIndex(p=>p.id===targetId);
  if(srcIdx<0||tgtIdx<0) return;
  // Swap positions
  const [moved] = state.panels.splice(srcIdx,1);
  state.panels.splice(tgtIdx,0,moved);
  // Lock both
  const src = state.panels.find(p=>p.id===sourceId);
  const tgt = state.panels.find(p=>p.id===targetId);
  if(src){ src.locked=true; src.manualRow=state.panels.indexOf(src); src.manualCol=0; src.sizeClass=src.sizeClass||'size-md'; }
  if(tgt){ tgt.locked=true; tgt.manualRow=state.panels.indexOf(tgt); tgt.manualCol=0; tgt.sizeClass=tgt.sizeClass||'size-md'; }
  trackInteraction(sourceId,'drag-drop');
  recalcAndRender();
  persist();
}
// ── Recalc cycle ──
function recalcAndRender(){
  // Flush active view timers
  if(observer){
    const now = Date.now();
    document.querySelectorAll('.panel').forEach(el=>{
      const pid = el.dataset.panelId;
      if(!pid||!state.tracking[pid]) return;
      const rect = el.getBoundingClientRect();
      const inView = rect.top < window.innerHeight && rect.bottom > 0 && rect.left < window.innerWidth && rect.right > 0;
      if(inView && state.tracking[pid].viewStart===null){
        state.tracking[pid].viewStart = now;
      }else if(!inView && state.tracking[pid].viewStart){
        state.tracking[pid].viewDuration += now - state.tracking[pid].viewStart;
        state.tracking[pid].viewStart = null;
      }
    });
  }
  computeScores();
  if(!state.frozen) render();
  state.updateCount++;
  state.layoutEpoch++;
  document.getElementById('stat-updates').textContent = 'updates: '+state.updateCount;
  persist();
}
function updateStats(){
  document.getElementById('stat-panels').textContent = 'panels: '+state.panels.length;
  document.getElementById('stat-updates').textContent = 'updates: '+state.updateCount;
  const sec = Math.floor((Date.now()-state.sessionStart)/1000);
  document.getElementById('stat-session').textContent = 'session: '+sec+'s';
}
function toast(msg){
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(()=>el.remove(),2100);
}
// ── Buttons ──
document.getElementById('btn-reset').addEventListener('click',()=>{
  localStorage.removeItem(CONFIG.storageKey);
  loadDefaults();
  recalcAndRender();
  toast('Tracking reset');
});
document.getElementById('btn-auto').addEventListener('click',function(){
  state.frozen = false;
  this.classList.add('active');
  document.getElementById('btn-freeze').classList.remove('active');
  state.panels.forEach(p=>{p.locked=false;p.manualRow=null;p.manualCol=null;});
  recalcAndRender();
  toast('Auto-layout enabled');
});
document.getElementById('btn-freeze').addEventListener('click',function(){
  state.frozen = !state.frozen;
  this.classList.toggle('active',state.frozen);
  document.getElementById('btn-auto').classList.toggle('active',!state.frozen);
  if(!state.frozen) recalcAndRender();
  toast(state.frozen?'Layout frozen':'Layout unfrozen');
});
document.getElementById('btn-expand-all').addEventListener('click',()=>{
  state.panels.forEach(p=>{p.collapsed=false;});
  state.frozen = false;
  document.getElementById('btn-auto').classList.add('active');
  document.getElementById('btn-freeze').classList.remove('active');
  recalcAndRender();
  toast('All panels expanded');
});
document.getElementById('more-toggle').addEventListener('click',()=>{
  const more = document.getElementById('more-panels');
  more.style.display = more.style.display==='none'?'flex':'none';
});
// ── Init ──
initState();
computeScores();
render();
// Periodic recalculation
setInterval(()=>{
  if(!state.frozen) recalcAndRender();
  else updateStats();
}, CONFIG.recalcInterval);
// Session timer
setInterval(updateStats, 5000);
// Persist on unload
window.addEventListener('beforeunload',()=>{
  if(observer) observer.disconnect();
  persist();
});
// Keyboard shortcuts
window.addEventListener('keydown',e=>{
  if(e.key==='f' && e.ctrlKey){ e.preventDefault(); document.getElementById('btn-freeze').click(); }
  if(e.key==='r' && e.ctrlKey){ e.preventDefault(); document.getElementById('btn-reset').click(); }
});
</script>
</body>
</html>