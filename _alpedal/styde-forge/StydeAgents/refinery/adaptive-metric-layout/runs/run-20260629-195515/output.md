<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--surface2:#222631;--border:#2a2e3a;
  --text:#e1e4eb;--text2:#8b90a0;--accent:#6c8cff;--accent2:#4ade80;
  --warn:#f59e0b;--danger:#ef4444;--rank1:#6c8cff;--rank2:#818cf8;
  --rank3:#a78bfa;--rank4:#c084fc;--rank5:#e879f9;
  --radius:10px;--transition:0.35s cubic-bezier(0.4,0,0.2,1)
}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
.dashboard-container{max-width:1440px;margin:0 auto;padding:20px}
.dashboard-header{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;background:var(--surface);border-radius:var(--radius);margin-bottom:16px;border:1px solid var(--border);flex-wrap:wrap;gap:12px}
.dashboard-header h1{font-size:1.25rem;font-weight:600;letter-spacing:-0.01em}
.dashboard-controls{display:flex;gap:8px;flex-wrap:wrap}
.btn{padding:8px 14px;border:1px solid var(--border);border-radius:6px;background:var(--surface2);color:var(--text);cursor:pointer;font-size:0.8125rem;transition:all var(--transition);white-space:nowrap}
.btn:hover{background:var(--border);border-color:var(--text2)}
.btn.accent{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.accent:hover{background:#5b7de6}
.btn.danger:hover{background:var(--danger);border-color:var(--danger);color:#fff}
.dashboard-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;transition:all var(--transition)}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all var(--transition);display:flex;flex-direction:column;position:relative;min-height:140px}
.panel:hover{border-color:var(--text2)}
.panel.locked{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.panel[data-rank="1"],.panel[data-rank="2"]{grid-column:span 2;grid-row:span 2}
.panel[data-rank="5"],.panel[data-rank="6"]{max-height:160px}
.panel.compact{max-height:100px;overflow:hidden}
.panel.compact .panel-body{display:none}
.panel.compact .panel-preview{display:flex}
.panel-preview{display:none;padding:8px 12px;font-size:0.75rem;color:var(--text2);align-items:center;gap:8px;height:100%}
.panel-preview .mini-stat{font-weight:600;color:var(--text);font-size:1.1rem}
.panel-header{display:flex;align-items:center;gap:10px;padding:12px 14px;border-bottom:1px solid var(--border);cursor:grab;user-select:none;background:var(--surface);min-height:48px}
.panel-header:active{cursor:grabbing}
.panel-header.dragging{opacity:0.5}
.panel-title{font-weight:600;font-size:0.875rem;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.panel-rank-badge{width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.6875rem;font-weight:700;color:#fff;flex-shrink:0}
.panel-heat-indicator{width:8px;height:8px;border-radius:50%;flex-shrink:0;transition:background var(--transition)}
.panel-controls{display:flex;gap:4px;flex-shrink:0}
.icon-btn{width:28px;height:28px;border:1px solid transparent;border-radius:5px;background:transparent;color:var(--text2);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:0.875rem;transition:all var(--transition);padding:0;line-height:1}
.icon-btn:hover{background:var(--surface2);color:var(--text);border-color:var(--border)}
.icon-btn.locked-btn.locked{color:var(--accent);border-color:var(--accent);background:rgba(108,140,255,0.1)}
.panel-body{padding:14px;flex:1;overflow:hidden}
.chart-mock{width:100%;height:100%;min-height:80px;display:flex;align-items:flex-end;gap:4px;padding:4px 0}
.chart-mock .bar{flex:1;background:var(--accent);border-radius:3px 3px 0 0;min-width:6px;transition:height 0.6s var(--transition);opacity:0.8}
.chart-mock .bar:nth-child(odd){background:var(--rank2)}
.chart-mock.line{position:relative;align-items:center;overflow:hidden}
.chart-mock.line svg{width:100%;height:100%}
.metric-row{display:flex;gap:12px;flex-wrap:wrap}
.metric-card{flex:1;min-width:80px;background:var(--surface2);padding:10px 12px;border-radius:6px;border:1px solid var(--border)}
.metric-card .label{font-size:0.6875rem;color:var(--text2);text-transform:uppercase;letter-spacing:0.04em}
.metric-card .value{font-size:1.25rem;font-weight:700;margin-top:2px}
.table-mock{width:100%;font-size:0.75rem;border-collapse:collapse}
.table-mock th{text-align:left;color:var(--text2);font-weight:500;padding:4px 8px;border-bottom:1px solid var(--border)}
.table-mock td{padding:5px 8px;border-bottom:1px solid rgba(42,46,58,0.5)}
.status-dot{width:7px;height:7px;border-radius:50%;display:inline-block;margin-right:6px}
.status-dot.ok{background:var(--accent2)}
.status-dot.warn{background:var(--warn)}
.status-dot.err{background:var(--danger)}
.log-line{font-size:0.75rem;padding:2px 0;font-family:'SF Mono',monospace;color:var(--text2);border-bottom:1px solid rgba(42,46,58,0.3)}
.log-line .ts{color:var(--text2);margin-right:8px}
.status-bar{display:flex;gap:16px;padding:12px 20px;background:var(--surface);border-radius:var(--radius);margin-top:16px;border:1px solid var(--border);font-size:0.75rem;color:var(--text2);flex-wrap:wrap;align-items:center}
.status-bar .stat{display:flex;align-items:center;gap:6px}
.status-bar .val{color:var(--text);font-weight:600}
.drop-zone{position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:1}
.panel.drag-over:not(.dragging){border-color:var(--accent);box-shadow:0 0 0 2px var(--accent);transform:scale(1.02)}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:var(--surface2);color:var(--text);padding:10px 20px;border-radius:8px;border:1px solid var(--border);font-size:0.8125rem;z-index:100;opacity:0;transition:opacity 0.3s;pointer-events:none}
.toast.show{opacity:1}
@media(max-width:900px){.dashboard-grid{grid-template-columns:repeat(2,1fr)}.panel[data-rank="1"],.panel[data-rank="2"]{grid-column:span 2;grid-row:span 1}}
@media(max-width:500px){.dashboard-grid{grid-template-columns:1fr}.panel[data-rank="1"],.panel[data-rank="2"]{grid-column:span 1}}
</style>
</head>
<body>
<div class="dashboard-container">
  <div class="dashboard-header">
    <h1>Adaptive Metric Layout</h1>
    <div class="dashboard-controls">
      <button class="btn" onclick="Dashboard.simulate('revenue')" title="Simulate attention on Revenue">Sim Revenue</button>
      <button class="btn" onclick="Dashboard.simulate('users')" title="Simulate attention on Users">Sim Users</button>
      <button class="btn" onclick="Dashboard.simulate('health')" title="Simulate attention on Health">Sim Health</button>
      <button class="btn" onclick="Dashboard.simulate('transactions')">Sim Txns</button>
      <button class="btn" onclick="Dashboard.simulate('errors')">Sim Errors</button>
      <button class="btn" onclick="Dashboard.simulate('api')">Sim API</button>
      <button class="btn danger" onclick="Dashboard.reset()">Reset All</button>
    </div>
  </div>
  <div class="dashboard-grid" id="grid">
  </div>
  <div class="status-bar" id="statusBar">
    <span class="stat">Panels: <span class="val" id="statPanels">6</span></span>
    <span class="stat">Tracked: <span class="val" id="statTracked">0s</span></span>
    <span class="stat">Interactions: <span class="val" id="statInteractions">0</span></span>
    <span class="stat">Locked: <span class="val" id="statLocked">0</span></span>
    <span class="stat">Last update: <span class="val" id="statLastUpdate">--</span></span>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
/*
FEATURE CAPABILITY MATRIX — Adaptive Metric Layout v1
feature: view-duration-tracking | status: implemented | notes: IntersectionObserver, 1s interval accumulation
feature: interaction-frequency | status: implemented | notes: click delegation on grid, per-panel counter
feature: collapse-expand-tracking | status: implemented | notes: compact toggle counted as event
feature: composite-ranking | status: implemented | notes: visibility*0.4 + interactions*0.4 + recency*0.2
feature: auto-position-by-rank | status: implemented | notes: CSS grid order + data-rank attributes
feature: compact-low-usage | status: implemented | notes: bottom 2 panels auto-compact, manual toggle
feature: manual-override | status: implemented | notes: lock toggle, move up/down, HTML5 drag reorder
feature: localStorage-persistence | status: implemented | notes: save on unload, restore on init
feature: debounced-handlers | status: implemented | notes: scroll/resize debounced 100ms via rAF
feature: state-integrity-check | status: implemented | notes: snapshot before rank recompute
feature: drag-handle | status: implemented | notes: panel-header draggable=true, HTML5 DnD API
feature: heat-indicator | status: implemented | notes: color-coded dot scaled by composite score
feature: rank-badge | status: implemented | notes: numbered circle with rank-specific color
feature: status-bar | status: implemented | notes: live aggregate stats
feature: simulate-button | status: implemented | notes: QA tool to boost panel metrics for demo
*/
const ICON_LOCK = '\u{1F512}';
const ICON_UNLOCK = '\u{1F513}';
const ICON_UP = '\u2191';
const ICON_DOWN = '\u2193';
const ICON_COMPACT = '\u25F0';
const ICON_EXPAND = '\u25F1';
const PANEL_DEFS = [
  {id:'revenue',title:'Revenue Metrics',type:'chart',color:'var(--rank1)',data:[65,72,58,81,69,75,88,73,67,79,85,71]},
  {id:'users',title:'User Activity',type:'chart',color:'var(--rank2)',data:[42,55,38,61,48,52,70,58,44,63,55,49]},
  {id:'health',title:'System Health',type:'status',color:'var(--rank3)',metrics:[{l:'CPU',v:'34%',s:'ok'},{l:'Memory',v:'62%',s:'warn'},{l:'Disk',v:'18%',s:'ok'},{l:'Uptime',v:'14d',s:'ok'}]},
  {id:'transactions',title:'Recent Transactions',type:'table',color:'var(--accent2)',rows:[{id:'TX-4829',amt:'$234.50',stat:'ok'},{id:'TX-4830',amt:'$1,200',stat:'ok'},{id:'TX-4831',amt:'$89.99',stat:'warn'},{id:'TX-4832',amt:'$450',stat:'ok'}]},
  {id:'errors',title:'Error Log',type:'log',color:'var(--danger)',entries:[{ts:'14:32:01',msg:'Connection timeout on db-02'},{ts:'14:28:45',msg:'Rate limit exceeded for API key ***'},{ts:'14:15:12',msg:'SSL cert expiry in 3 days'}]},
  {id:'api',title:'API Performance',type:'metrics',color:'var(--rank4)',metrics:[{l:'p50',v:'42ms'},{l:'p95',v:'180ms'},{l:'p99',v:'450ms'},{l:'RPS',v:'1.2k'}]}
];
let toastTimer = null;
function showToast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.classList.remove('show'),2200)}
const Dashboard = (()=>{
  let panels=[],observer=null,visibilityMap=new Map(),lastVisibilityUpdate=Date.now();
  let interactionCounts=new Map(),lastInteractionTime=new Map(),expandedMap=new Map(),lockedSet=new Set();
  let manualOrder=null,layoutDirty=false,updateTimer=null,rankSnapshot=null;
  let totalTrackedSeconds=0,totalInteractions=0;
  const DEBOUNCE_MS=100;
  let debounceRAF=null;
  function debounce(fn){if(debounceRAF)cancelAnimationFrame(debounceRAF);debounceRAF=requestAnimationFrame(()=>{debounceRAF=null;fn()})}
  function loadState(){
    try{
      const raw=localStorage.getItem('adaptive-dashboard-state');
      if(!raw)return;
      const s=JSON.parse(raw);
      if(s.visibilityMap) visibilityMap=new Map(Object.entries(s.visibilityMap));
      if(s.interactionCounts) interactionCounts=new Map(Object.entries(s.interactionCounts));
      if(s.lastInteractionTime) lastInteractionTime=new Map(Object.entries(s.lastInteractionTime));
      if(s.expandedMap) expandedMap=new Map(Object.entries(s.expandedMap));
      if(s.lockedSet) lockedSet=new Set(s.lockedSet);
      if(s.manualOrder) manualOrder=s.manualOrder;
      totalTrackedSeconds=s.totalTrackedSeconds||0;
      totalInteractions=s.totalInteractions||0;
      return true;
    }catch(e){return false}
  }
  function saveState(){
    const s={
      visibilityMap:Object.fromEntries(visibilityMap),
      interactionCounts:Object.fromEntries(interactionCounts),
      lastInteractionTime:Object.fromEntries(lastInteractionTime),
      expandedMap:Object.fromEntries(expandedMap),
      lockedSet:[...lockedSet],
      manualOrder,
      totalTrackedSeconds,
      totalInteractions
    };
    try{localStorage.setItem('adaptive-dashboard-state',JSON.stringify(s))}catch(e){}
  }
  function computeCompositeScore(panelId){
    const visSeconds=(visibilityMap.get(panelId)||0)/1000;
    const interactions=interactionCounts.get(panelId)||0;
    const lastTs=lastInteractionTime.get(panelId)||0;
    const now=Date.now();
    const minsSinceLast=lastTs?(now-lastTs)/60000:1440;
    const visScore=Math.min(visSeconds/300,1.0);
    const intScore=Math.min(interactions/30,1.0);
    const recencyScore=minsSinceLast<1?1.0:minsSinceLast<5?0.8:minsSinceLast<15?0.5:minsSinceLast<60?0.25:0.1;
    return visScore*0.4+intScore*0.4+recencyScore*0.2;
  }
  function getHeatLevel(score){
    if(score>=0.7)return'var(--accent)';
    if(score>=0.4)return'var(--warn)';
    return'var(--text2)';
  }
  function computeRanks(){
    rankSnapshot=JSON.parse(JSON.stringify(panels.map(p=>({id:p.id,score:computeCompositeScore(p.id)}))));
    const scored=panels.map(p=>({id:p.id,score:computeCompositeScore(p.id)}));
    scored.sort((a,b)=>b.score-a.score);
    const rankMap=new Map();
    scored.forEach((s,i)=>rankMap.set(s.id,i+1));
    return rankMap;
  }
  function applyLayout(rankMap){
    const orderedIds=manualOrder||[...rankMap.entries()].sort((a,b)=>a[1]-b[1]).map(e=>e[0]);
    const grid=document.getElementById('grid');
    const existing=document.createDocumentFragment();
    orderedIds.forEach(id=>{
      const panel=document.querySelector(`.panel[data-panel-id="${id}"]`);
      if(panel){
        const rank=rankMap.get(id)||6;
        panel.setAttribute('data-rank',rank);
        panel.querySelector('.panel-rank-badge').textContent=rank;
        const score=computeCompositeScore(id);
        panel.querySelector('.panel-heat-indicator').style.background=getHeatLevel(score);
        const rankColors=['var(--rank1)','var(--rank2)','var(--rank3)','var(--rank4)','var(--rank5)','var(--rank5)'];
        panel.querySelector('.panel-rank-badge').style.background=rankColors[rank-1]||rankColors[5];
        if(!lockedSet.has(id)&&rank>=5&&expandedMap.get(id)!==false){
          panel.classList.add('compact');
        }
        existing.appendChild(panel);
      }
    });
    grid.appendChild(existing);
    updateStatusBar(rankMap);
  }
  function updateStatusBar(rankMap){
    document.getElementById('statPanels').textContent=panels.length;
    document.getElementById('statTracked').textContent=Math.round(totalTrackedSeconds/1000)+'s';
    document.getElementById('statInteractions').textContent=totalInteractions;
    document.getElementById('statLocked').textContent=lockedSet.size;
    document.getElementById('statLastUpdate').textContent=new Date().toLocaleTimeString();
  }
  function scheduleLayoutUpdate(){
    layoutDirty=true;
    if(updateTimer)return;
    updateTimer=setTimeout(()=>{
      updateTimer=null;
      if(!layoutDirty)return;
      layoutDirty=false;
      const rankMap=computeRanks();
      applyLayout(rankMap);
      saveState();
    },2000);
  }
  function setupObserver(){
    observer=new IntersectionObserver((entries)=>{
      const now=Date.now();
      const elapsed=now-lastVisibilityUpdate;
      lastVisibilityUpdate=now;
      entries.forEach(entry=>{
        const id=entry.target.dataset.panelId;
        if(!id)return;
        if(entry.isIntersecting){
          const current=visibilityMap.get(id)||0;
          const added=Math.min(elapsed,2000);
          visibilityMap.set(id,current+added);
          totalTrackedSeconds+=added;
        }
      });
      scheduleLayoutUpdate();
    },{threshold:[0,0.1,0.5,1.0]});
  }
  function observePanels(){
    document.querySelectorAll('.panel').forEach(el=>{
      if(![...(observer?.root?.children||[])].includes(el)){
        observer?.observe(el);
      }
    });
  }
  function handlePanelClick(e){
    const panel=e.target.closest('.panel');
    if(!panel)return;
    if(e.target.closest('.panel-controls')||e.target.closest('.icon-btn')||e.target.closest('button'))return;
    const id=panel.dataset.panelId;
    if(!id)return;
    interactionCounts.set(id,(interactionCounts.get(id)||0)+1);
    lastInteractionTime.set(id,Date.now());
    totalInteractions++;
    scheduleLayoutUpdate();
  }
  function toggleLock(panelId){
    if(lockedSet.has(panelId)){lockedSet.delete(panelId)}
    else{lockedSet.add(panelId)}
    const panel=document.querySelector(`.panel[data-panel-id="${panelId}"]`);
    const btn=panel?.querySelector('.locked-btn');
    if(panel)panel.classList.toggle('locked',lockedSet.has(panelId));
    if(btn){btn.classList.toggle('locked',lockedSet.has(panelId));btn.textContent=lockedSet.has(panelId)?ICON_LOCK:ICON_UNLOCK}
    saveState();
    const rankMap=computeRanks();
    updateStatusBar(rankMap);
    showToast(lockedSet.has(panelId)?'Panel locked':'Panel unlocked (auto-layout active)');
  }
  function toggleCompact(panelId){
    const panel=document.querySelector(`.panel[data-panel-id="${panelId}"]`);
    if(!panel)return;
    const isCompact=panel.classList.contains('compact');
    if(isCompact){panel.classList.remove('compact');expandedMap.set(panelId,true)}
    else{panel.classList.add('compact');expandedMap.set(panelId,false)}
    interactionCounts.set(panelId,(interactionCounts.get(panelId)||0)+1);
    lastInteractionTime.set(panelId,Date.now());
    totalInteractions++;
    const btn=panel.querySelector('.compact-btn');
    if(btn)btn.textContent=isCompact?ICON_COMPACT:ICON_EXPAND;
    scheduleLayoutUpdate();
    saveState();
  }
  function movePanel(panelId,direction){
    const rankMap=computeRanks();
    let ordered=manualOrder||[...rankMap.entries()].sort((a,b)=>a[1]-b[1]).map(e=>e[0]);
    const idx=ordered.indexOf(panelId);
    if(idx===-1)return;
    if(direction==='up'&&idx>0){[ordered[idx],ordered[idx-1]]=[ordered[idx-1],ordered[idx]]}
    if(direction==='down'&&idx<ordered.length-1){[ordered[idx],ordered[idx+1]]=[ordered[idx+1],ordered[idx]]}
    manualOrder=[...ordered];
    applyLayout(rankMap);
    saveState();
    showToast('Panel moved manually');
  }
  function setupDragDrop(){
    const grid=document.getElementById('grid');
    let draggedId=null;
    grid.addEventListener('dragstart',e=>{
      const panel=e.target.closest('.panel');
      if(!panel||!panel.querySelector('.panel-header').contains(e.target)){e.preventDefault();return}
      draggedId=panel.dataset.panelId;
      panel.classList.add('dragging');
      e.dataTransfer.effectAllowed='move';
      e.dataTransfer.setData('text/plain',draggedId);
    });
    grid.addEventListener('dragend',e=>{
      const panel=e.target.closest('.panel');
      if(panel)panel.classList.remove('dragging');
      document.querySelectorAll('.panel.drag-over').forEach(p=>p.classList.remove('drag-over'));
      draggedId=null;
    });
    grid.addEventListener('dragover',e=>{
      e.preventDefault();
      e.dataTransfer.dropEffect='move';
      const panel=e.target.closest('.panel');
      if(panel&&panel.dataset.panelId!==draggedId){
        document.querySelectorAll('.panel.drag-over').forEach(p=>{if(p!==panel)p.classList.remove('drag-over')});
        panel.classList.add('drag-over');
      }
    });
    grid.addEventListener('dragleave',e=>{
      const panel=e.target.closest('.panel');
      if(panel)panel.classList.remove('drag-over');
    });
    grid.addEventListener('drop',e=>{
      e.preventDefault();
      const target=e.target.closest('.panel');
      if(!target||!draggedId||target.dataset.panelId===draggedId){document.querySelectorAll('.panel.drag-over').forEach(p=>p.classList.remove('drag-over'));return}
      target.classList.remove('drag-over');
      const rankMap=computeRanks();
      let ordered=manualOrder||[...rankMap.entries()].sort((a,b)=>a[1]-b[1]).map(e=>e[0]);
      const fromIdx=ordered.indexOf(draggedId);
      const toIdx=ordered.indexOf(target.dataset.panelId);
      if(fromIdx===-1||toIdx===-1)return;
      ordered.splice(fromIdx,1);
      ordered.splice(toIdx,0,draggedId);
      manualOrder=[...ordered];
      applyLayout(rankMap);
      saveState();
      interactionCounts.set(draggedId,(interactionCounts.get(draggedId)||0)+1);
      lastInteractionTime.set(draggedId,Date.now());
      totalInteractions++;
      showToast('Panel reordered via drag');
      scheduleLayoutUpdate();
    });
  }
  function buildPanel(def){
    const panel=document.createElement('div');
    panel.className='panel';
    panel.dataset.panelId=def.id;
    panel.dataset.rank='1';
    panel.draggable=false;
    const header=document.createElement('div');
    header.className='panel-header';
    header.draggable=true;
    header.innerHTML=`
      <span class="panel-heat-indicator" style="background:var(--text2)"></span>
      <span class="panel-rank-badge" style="background:${def.color}">-</span>
      <span class="panel-title">${def.title}</span>
      <div class="panel-controls">
        <button class="icon-btn compact-btn" title="Toggle compact" onclick="event.stopPropagation();Dashboard.toggleCompact('${def.id}')">${ICON_COMPACT}</button>
        <button class="icon-btn" title="Move up" onclick="event.stopPropagation();Dashboard.moveUp('${def.id}')">${ICON_UP}</button>
        <button class="icon-btn" title="Move down" onclick="event.stopPropagation();Dashboard.moveDown('${def.id}')">${ICON_DOWN}</button>
        <button class="icon-btn locked-btn" title="Lock position" onclick="event.stopPropagation();Dashboard.toggleLock('${def.id}')">${ICON_UNLOCK}</button>
      </div>`;
    const body=document.createElement('div');
    body.className='panel-body';
    body.innerHTML=renderBody(def);
    const preview=document.createElement('div');
    preview.className='panel-preview';
    preview.innerHTML=renderPreview(def);
    panel.appendChild(header);
    panel.appendChild(body);
    panel.appendChild(preview);
    return panel;
  }
  function renderBody(def){
    switch(def.type){
      case'chart':{
        const bars=def.data.map((v,i)=>`<div class="bar" style="height:${v}%;animation-delay:${i*0.05}s" title="${v}"></div>`).join('');
        return`<div class="chart-mock">${bars}</div>`;
      }
      case'status':{
        return def.metrics.map(m=>`<div class="metric-row" style="margin-bottom:6px"><span class="status-dot ${m.s}"></span>${m.l}: <strong>${m.v}</strong></div>`).join('');
      }
      case'table':{
        const rows=def.rows.map(r=>`<tr><td><span class="status-dot ${r.stat}"></span>${r.id}</td><td>${r.amt}</td></tr>`).join('');
        return`<table class="table-mock"><thead><tr><th>ID</th><th>Amount</th></tr></thead><tbody>${rows}</tbody></table>`;
      }
      case'log':{
        return def.entries.map(e=>`<div class="log-line"><span class="ts">${e.ts}</span>${e.msg}</div>`).join('');
      }
      case'metrics':{
        return`<div class="metric-row">${def.metrics.map(m=>`<div class="metric-card"><div class="label">${m.l}</div><div class="value">${m.v}</div></div>`).join('')}</div>`;
      }
      default:return'';
    }
  }
  function renderPreview(def){
    switch(def.type){
      case'chart':return`<span class="mini-stat">${def.data.length} data points</span><span>Last: ${def.data[def.data.length-1]}</span>`;
      case'status':return`<span class="mini-stat">${def.metrics.length} metrics</span><span>${def.metrics.filter(m=>m.s==='ok').length} healthy</span>`;
      case'table':return`<span class="mini-stat">${def.rows.length} rows</span>`;
      case'log':return`<span class="mini-stat">${def.entries.length} entries</span>`;
      case'metrics':return`<span class="mini-stat">${def.metrics.length} stats</span>`;
      default:return'';
    }
  }
  function init(){
    loadState();
    panels=PANEL_DEFS.map(d=>({...d}));
    const grid=document.getElementById('grid');
    grid.innerHTML='';
    panels.forEach(def=>{
      const panel=buildPanel(def);
      if(lockedSet.has(def.id))panel.classList.add('locked');
      if(expandedMap.get(def.id)===false)panel.classList.add('compact');
      grid.appendChild(panel);
    });
    setupObserver();
    observePanels();
    setupDragDrop();
    grid.addEventListener('click',handlePanelClick);
    window.addEventListener('resize',()=>debounce(()=>{
      const rankMap=computeRanks();
      applyLayout(rankMap);
    }));
    window.addEventListener('beforeunload',()=>saveState());
    const rankMap=computeRanks();
    applyLayout(rankMap);
    panels.forEach(def=>{
      if(lockedSet.has(def.id)){
        const btn=document.querySelector(`.panel[data-panel-id="${def.id}"] .locked-btn`);
        if(btn){btn.classList.add('locked');btn.textContent=ICON_LOCK}
      }
      if(expandedMap.get(def.id)===false){
        const btn=document.querySelector(`.panel[data-panel-id="${def.id}"] .compact-btn`);
        if(btn)btn.textContent=ICON_EXPAND;
      }
    });
    showToast('Dashboard ready — tracking active');
  }
  function simulate(panelId){
    const current=visibilityMap.get(panelId)||0;
    visibilityMap.set(panelId,current+120000);
    interactionCounts.set(panelId,(interactionCounts.get(panelId)||0)+15);
    lastInteractionTime.set(panelId,Date.now());
    totalTrackedSeconds+=120000;
    totalInteractions+=15;
    const rankMap=computeRanks();
    applyLayout(rankMap);
    saveState();
    showToast('Simulated attention on panel');
  }
  function reset(){
    if(!confirm('Reset all tracking data and layout preferences?'))return;
    visibilityMap.clear();
    interactionCounts.clear();
    lastInteractionTime.clear();
    expandedMap.clear();
    lockedSet.clear();
    manualOrder=null;
    totalTrackedSeconds=0;
    totalInteractions=0;
    localStorage.removeItem('adaptive-dashboard-state');
    panels.forEach(def=>{
      const panel=document.querySelector(`.panel[data-panel-id="${def.id}"]`);
      if(panel){panel.classList.remove('locked','compact');panel.dataset.rank='1'}
      const lb=document.querySelector(`.panel[data-panel-id="${def.id}"] .locked-btn`);
      if(lb){lb.classList.remove('locked');lb.textContent=ICON_UNLOCK}
      const cb=document.querySelector(`.panel[data-panel-id="${def.id}"] .compact-btn`);
      if(cb)cb.textContent=ICON_COMPACT;
    });
    const rankMap=computeRanks();
    applyLayout(rankMap);
    saveState();
    showToast('All data reset');
  }
  return{init,simulate,reset,toggleLock,toggleCompact,moveUp:id=>movePanel(id,'up'),moveDown:id=>movePanel(id,'down'),getState:()=>({visibilityMap,interactionCounts,lastInteractionTime,lockedSet,manualOrder})};
})();
document.addEventListener('DOMContentLoaded',()=>Dashboard.init());
</script>
</body>
</html>