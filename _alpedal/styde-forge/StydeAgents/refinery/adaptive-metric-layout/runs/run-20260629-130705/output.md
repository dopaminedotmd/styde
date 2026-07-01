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
  --surface: #1a1d27;
  --border: #2a2d3a;
  --text: #e1e4ed;
  --text-dim: #8b8fa3;
  --accent: #6c8cff;
  --accent-glow: rgba(108,140,255,0.25);
  --warn: #ff9940;
  --compact-ratio: 0.6;
  --gap: 8px;
  --radius: 10px;
}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,sans-serif;min-height:100vh;overflow-x:hidden}
.header{display:flex;align-items:center;justify-content:space-between;padding:12px 20px;background:var(--surface);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100}
.header h1{font-size:1.1rem;font-weight:600;letter-spacing:-0.01em}
.header .controls{display:flex;gap:8px;align-items:center}
.header button{padding:6px 14px;border:1px solid var(--border);border-radius:6px;background:var(--surface);color:var(--text);cursor:pointer;font-size:0.8rem;transition:opacity 0.15s,transform 0.15s}
.header button:hover{opacity:0.85;transform:translateY(-1px)}
.header button.active{background:var(--accent);border-color:var(--accent);color:#fff}
.grid-container{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:minmax(140px,auto);gap:var(--gap);padding:16px;max-width:1600px;margin:0 auto}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px;position:relative;overflow:hidden;transition:opacity 0.25s,transform 0.25s,box-shadow 0.25s}
.panel:hover{box-shadow:0 0 0 1px var(--accent-glow)}
.panel.compact{font-size:0.8rem;padding:10px}
.panel.compact .panel-body{max-height:60px;overflow:hidden;mask-image:linear-gradient(to bottom,black 40%,transparent)}
.panel.dominant{grid-column:span 2;grid-row:span 2;box-shadow:0 0 20px var(--accent-glow)}
.panel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.panel-title{font-weight:600;font-size:0.9rem;display:flex;align-items:center;gap:6px}
.panel-actions{display:flex;gap:4px}
.panel-actions button{background:none;border:none;color:var(--text-dim);cursor:pointer;padding:2px 6px;border-radius:4px;font-size:0.75rem;transition:opacity 0.15s}
.panel-actions button:hover{color:var(--text);background:var(--border)}
.panel-actions button.locked{color:var(--accent)}
.panel-rank{font-size:0.65rem;color:var(--text-dim);background:var(--bg);padding:2px 6px;border-radius:4px}
.panel-stat{font-size:1.6rem;font-weight:700;letter-spacing:-0.02em}
.panel-label{font-size:0.72rem;color:var(--text-dim)}
.panel-bar{height:4px;border-radius:2px;margin-top:8px;background:var(--border);overflow:hidden}
.panel-bar-fill{height:100%;border-radius:2px;background:var(--accent);transition:width 0.4s}
.panel-heat{position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none;opacity:0.04;transition:opacity 0.6s}
.panel-heat.active{opacity:0.12}
.compact-zone{border:1px dashed var(--border);border-radius:var(--radius);padding:12px;margin-top:12px;grid-column:1/-1}
.compact-zone h3{font-size:0.8rem;color:var(--text-dim);margin-bottom:8px}
.compact-grid{display:flex;flex-wrap:wrap;gap:6px}
.compact-grid .panel{flex:0 0 160px;min-height:80px}
.toast{position:fixed;bottom:20px;right:20px;background:var(--surface);border:1px solid var(--border);padding:10px 16px;border-radius:8px;font-size:0.8rem;opacity:0;transform:translateY(10px);pointer-events:none;z-index:200;transition:opacity 0.3s,transform 0.3s}
.toast.show{opacity:1;transform:translateY(0)}
.score-badge{font-size:0.6rem;padding:1px 5px;border-radius:3px;margin-left:4px}
.score-badge.hot{background:#ff994022;color:var(--warn)}
.score-badge.warm{background:#ffcc0022;color:#ffcc00}
.score-badge.cold{background:#6c8cff22;color:var(--accent)}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <span style="font-size:0.75rem;color:var(--text-dim)" id="sessionTimer">Session: 0s</span>
    <button id="btnReset" title="Reset layout">Reset</button>
    <button id="btnExport" title="Export tracking data">Export</button>
  </div>
</div>
<div class="grid-container" id="gridContainer"></div>
<div class="toast" id="toast"></div>
<script>
(function(){
  // ─── Deterministic Seeded PRNG (mulberry32) ───
  function mulberry32(seed){return function(){seed|=0;seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
  const APP_SEED = 20260629;
  const rng = mulberry32(APP_SEED);
  function generateValue(min,max){return Math.floor(rng()*(max-min+1))+min}
  // ─── DOM Cache ───
  const $ = (sel,ctx)=>(ctx||document).querySelector(sel);
  const $$ = (sel,ctx)=>(ctx||document).querySelectorAll(sel);
  const domCache = {};
  function dom(id){return domCache[id]||(domCache[id]=document.getElementById(id))}
  function invalidateDom(){for(const k in domCache)delete domCache[k]}
  const gridContainer = () => dom('gridContainer') || (domCache['gridContainer'] = document.getElementById('gridContainer'));
  const toast = () => dom('toast') || (domCache['toast'] = document.getElementById('toast'));
  const sessionTimer = () => dom('sessionTimer') || (domCache['sessionTimer'] = document.getElementById('sessionTimer'));
  // ─── Panel Definitions ───
  const panels = [
    {id:'traffic',title:'Traffic',icon:'📊',min:1200,max:8900,unit:'req/s'},
    {id:'latency',title:'Latency',icon:'⏱',min:12,max:340,unit:'ms'},
    {id:'errors',title:'Error Rate',icon:'⚠',min:0.1,max:12.5,unit:'%'},
    {id:'cpu',title:'CPU',icon:'🖥',min:8,max:98,unit:'%'},
    {id:'memory',title:'Memory',icon:'🧠',min:2.1,max:64,unit:'GB'},
    {id:'users',title:'Active Users',icon:'👥',min:80,max:4200,unit:''},
    {id:'revenue',title:'Revenue',icon:'💰',min:1200,max:9800,unit:'$/h'},
    {id:'uptime',title:'Uptime',icon:'✅',min:99.1,max:99.99,unit:'%'},
    {id:'errors_detail',title:'Error Breakdown',icon:'🔍',min:0,max:200,unit:''},
    {id:'throughput',title:'Throughput',icon:'🚀',min:8,max:450,unit:'MB/s'},
    {id:'sessions',title:'Sessions',icon:'📋',min:40,max:890,unit:''},
    {id:'cache',title:'Cache Hit Rate',icon:'💾',min:42,max:99,unit:'%'}
  ];
  // ─── State ───
  const LS_KEY = 'adaptive_layout_v1';
  let tracking = null;    // {[panelId]:{views,duration,lastView,frequency,interactions,locked,overrideCol,overrideRow,overrideSpan}}
  let layoutOrder = null; // ordered panel ids by rank
  let sessionStart = Date.now();
  let viewTimers = {};
  let panelDomCache = {}; // {id: {el,bodyEl,statEl,barEl,...}}
  function defaultTracking(){
    const t = {};
    panels.forEach(p => {
      t[p.id] = {views:0,duration:0,lastView:0,frequency:0,interactions:0,locked:false,overrideCol:null,overrideRow:null,overrideSpan:null};
    });
    return t;
  }
  function loadState(){
    try{
      const raw = localStorage.getItem(LS_KEY);
      if(raw){
        const parsed = JSON.parse(raw);
        if(parsed.tracking && parsed.layoutOrder){
          tracking = parsed.tracking;
          layoutOrder = parsed.layoutOrder;
          return true;
        }
      }
    }catch(e){}
    tracking = defaultTracking();
    layoutOrder = panels.map(p=>p.id);
    return false;
  }
  function saveState(){
    try{
      localStorage.setItem(LS_KEY, JSON.stringify({tracking,layoutOrder}));
    }catch(e){}
  }
  // ─── Scoring & Ranking ───
  const RECENCY_HALFLIFE = 300000; // 5min in ms
  function computeScore(panelId){
    const t = tracking[panelId] || {views:0,duration:0,lastView:0};
    const now = Date.now();
    const recencyFactor = Math.exp(-(now - t.lastView) / RECENCY_HALFLIFE);
    const frequency = t.frequency; // interactions per session-minute (calculated elsewhere)
    const duration = Math.min(t.duration, 600000); // cap at 10min
    const views = t.views;
    const score = (frequency * 40) + (Math.log1p(duration/1000) * 30) + (Math.log1p(views) * 20) + (recencyFactor * 10);
    return Math.round(score * 10) / 10;
  }
  function rankPanels(){
    const now = Date.now();
    panels.forEach(p => {
      if(!tracking[p.id]) tracking[p.id] = defaultTracking()[p.id];
      const t = tracking[p.id];
      const sessionMin = (now - sessionStart) / 60000;
      t.frequency = sessionMin > 0 ? t.interactions / sessionMin : 0;
    });
    layoutOrder = panels.map(p=>p.id).sort((a,b)=>computeScore(b)-computeScore(a));
    saveState();
  }
  // ─── Tracking ───
  function startViewTimer(panelId){
    viewTimers[panelId] = Date.now();
  }
  function stopViewTimer(panelId){
    if(viewTimers[panelId]){
      const elapsed = Date.now() - viewTimers[panelId];
      if(tracking[panelId]){
        tracking[panelId].duration += elapsed;
        tracking[panelId].views += 1;
        tracking[panelId].lastView = Date.now();
      }
      delete viewTimers[panelId];
    }
  }
  function recordInteraction(panelId){
    if(tracking[panelId]){
      tracking[panelId].interactions += 1;
      tracking[panelId].lastView = Date.now();
    }
    rankPanels();
    renderLayout();
  }
  // ─── Observers: view duration via IntersectionObserver ───
  let observer = null;
  function setupObserver(){
    if(observer) observer.disconnect();
    observer = new IntersectionObserver((entries)=>{
      entries.forEach(e=>{
        const pid = e.target.dataset.panelId;
        if(!pid) return;
        if(e.isIntersecting && e.intersectionRatio > 0.5){
          if(!viewTimers[pid]) startViewTimer(pid);
        } else {
          stopViewTimer(pid);
        }
      });
    },{threshold:[0,0.5]});
    document.querySelectorAll('.panel').forEach(el=>observer.observe(el));
  }
  // ─── Render ───
  function scoreLabel(panelId){
    const s = computeScore(panelId);
    if(s >= 50) return 'hot';
    if(s >= 25) return 'warm';
    return 'cold';
  }
  function renderLayout(){
    const container = gridContainer();
    if(!container) return;
    rankPanels();
    container.innerHTML = '';
    panelDomCache = {};
    const dominant = layoutOrder.slice(0,2);
    const normal = layoutOrder.slice(2,8);
    const compact = layoutOrder.slice(8);
    function createPanelEl(panelId, isDominant, isCompact){
      const p = panels.find(x=>x.id===panelId) || {};
      const t = tracking[panelId] || defaultTracking()[panelId];
      const value = generateValue(p.min||0,p.max||100);
      const pct = p.max ? ((value-(p.min||0))/(p.max-(p.min||0))*100) : 50;
      const rankIdx = layoutOrder.indexOf(panelId);
      const score = computeScore(panelId);
      const el = document.createElement('div');
      el.className = 'panel' + (isDominant?' dominant':'') + (isCompact?' compact':'');
      el.dataset.panelId = panelId;
      el.draggable = true;
      let barColor = 'var(--accent)';
      if(p.id==='errors'||p.id==='errors_detail') barColor = value > 5 ? 'var(--warn)' : 'var(--accent)';
      el.innerHTML =
        '<div class="panel-heat" style="background:radial-gradient(circle at 30% 30%,var(--accent),transparent)"></div>'+
        '<div class="panel-header">'+
          '<span class="panel-title">'+(p.icon||'')+' '+(p.title||panelId)+
            '<span class="score-badge '+scoreLabel(panelId)+'">'+score.toFixed(0)+'</span>'+
          '</span>'+
          '<div class="panel-actions">'+
            (isCompact ? '<button class="expand-btn" title="Expand" data-pid="'+panelId+'">↥</button>' : '')+
            (!isCompact ? '<button class="collapse-btn" title="Compact" data-pid="'+panelId+'">↧</button>' : '')+
            '<button class="lock-btn'+(t.locked?' locked':'')+'" title="Lock position" data-pid="'+panelId+'">'+(t.locked?'🔒':'🔓')+'</button>'+
          '</div>'+
        '</div>'+
        '<div class="panel-body">'+
          (!isCompact ? '<div class="panel-stat">'+value.toFixed(p.unit==='%'?1:0)+(p.unit?' <span style="font-size:0.7rem;opacity:0.6">'+p.unit+'</span>':'')+'</div>'+
          '<div class="panel-label">Rank #'+(rankIdx+1)+' · '+t.views+' views · '+(t.duration/1000).toFixed(0)+'s watched</div>'+
          '<div class="panel-bar"><div class="panel-bar-fill" style="width:'+pct+'%;background:'+barColor+'"></div></div>' : '')+
          (isCompact ? '<div class="panel-stat" style="font-size:1rem">'+value.toFixed(p.unit==='%'?1:0)+(p.unit||'')+'</div><div class="panel-label">Compact · click to expand</div>' : '')+
        '</div>';
      // cache DOM refs
      panelDomCache[panelId] = {
        el,
        bodyEl: el.querySelector('.panel-body'),
        statEl: el.querySelector('.panel-stat'),
        barEl: el.querySelector('.panel-bar-fill'),
        heatEl: el.querySelector('.panel-heat'),
        lockBtn: el.querySelector('.lock-btn'),
        collapseBtn: el.querySelector('.collapse-btn'),
        expandBtn: el.querySelector('.expand-btn'),
        scoreBadge: el.querySelector('.score-badge')
      };
      // Event delegation for buttons
      el.addEventListener('click', function(e){
        const btn = e.target.closest('button');
        if(!btn) return;
        const pid = btn.dataset.pid;
        if(!pid) return;
        if(btn.classList.contains('lock-btn')){
          tracking[pid].locked = !tracking[pid].locked;
          recordInteraction(pid);
          showToast(tracking[pid].locked ? 'Locked: '+p.title : 'Unlocked: '+p.title);
        }
        if(btn.classList.contains('collapse-btn')){
          const idx = layoutOrder.indexOf(pid);
          if(idx >= 2 && layoutOrder.length > 8){
            layoutOrder.splice(idx,1);
            layoutOrder.push(pid);
          }
          recordInteraction(pid);
          showToast('Collapsed: '+p.title);
        }
        if(btn.classList.contains('expand-btn')){
          const idx = layoutOrder.indexOf(pid);
          if(idx >= 8){
            layoutOrder.splice(idx,1);
            layoutOrder.splice(2,0,pid);
          }
          recordInteraction(pid);
          showToast('Expanded: '+p.title);
        }
        if(btn.classList.contains('panel-body') && !e.target.closest('button')){
          recordInteraction(pid);
        }
      });
      el.addEventListener('mouseenter',function(){
        if(panelDomCache[panelId] && panelDomCache[panelId].heatEl){
          panelDomCache[panelId].heatEl.classList.add('active');
        }
      });
      el.addEventListener('mouseleave',function(){
        if(panelDomCache[panelId] && panelDomCache[panelId].heatEl){
          panelDomCache[panelId].heatEl.classList.remove('active');
        }
      });
      // Drag and drop
      el.addEventListener('dragstart',function(e){
        e.dataTransfer.setData('text/plain',panelId);
        el.style.opacity = '0.5';
      });
      el.addEventListener('dragend',function(e){
        el.style.opacity = '1';
        document.querySelectorAll('.panel').forEach(p=>p.style.outline='');
      });
      el.addEventListener('dragover',function(e){
        e.preventDefault();
        el.style.outline = '2px dashed var(--accent)';
      });
      el.addEventListener('dragleave',function(e){
        el.style.outline = '';
      });
      el.addEventListener('drop',function(e){
        e.preventDefault();
        el.style.outline = '';
        const srcId = e.dataTransfer.getData('text/plain');
        const dstId = panelId;
        if(srcId && srcId !== dstId){
          const srcIdx = layoutOrder.indexOf(srcId);
          const dstIdx = layoutOrder.indexOf(dstId);
          if(srcIdx >= 0 && dstIdx >= 0){
            layoutOrder.splice(srcIdx,1);
            layoutOrder.splice(dstIdx,0,srcId);
            rankPanels();
            renderLayout();
            showToast('Rearranged');
          }
        }
      });
      return el;
    }
    // Render dominant panels
    dominant.forEach(id => {
      const el = createPanelEl(id, true, false);
      container.appendChild(el);
    });
    // Render normal panels
    normal.forEach(id => {
      const el = createPanelEl(id, false, false);
      container.appendChild(el);
    });
    // Render compact zone
    if(compact.length > 0){
      const zone = document.createElement('div');
      zone.className = 'compact-zone';
      zone.innerHTML = '<h3>Compact Panels (auto-shrunk by low usage)</h3><div class="compact-grid"></div>';
      const grid = zone.querySelector('.compact-grid');
      compact.forEach(id => {
        grid.appendChild(createPanelEl(id, false, true));
      });
      container.appendChild(zone);
    }
    setupObserver();
    saveState();
  }
  // ─── Periodic refresh (soft update, no full re-render) ───
  function softRefresh(){
    const now = Date.now();
    dom('sessionTimer').textContent = 'Session: '+Math.floor((now-sessionStart)/1000)+'s';
    panels.forEach(p => {
      const cached = panelDomCache[p.id];
      if(!cached || !cached.el || !cached.el.isConnected) return;
      const value = generateValue(p.min||0,p.max||100);
      const pct = p.max ? ((value-(p.min||0))/(p.max-(p.min||0))*100) : 50;
      // Update in-place via cached refs
      if(cached.statEl){
        cached.statEl.innerHTML = value.toFixed(p.unit==='%'?1:0)+(p.unit?' <span style="font-size:0.7rem;opacity:0.6">'+p.unit+'</span>':'');
      }
      if(cached.barEl){
        cached.barEl.style.width = pct+'%';
      }
      if(cached.scoreBadge){
        const score = computeScore(p.id);
        cached.scoreBadge.textContent = score.toFixed(0);
        cached.scoreBadge.className = 'score-badge '+scoreLabel(p.id);
      }
    });
  }
  // ─── Toast ───
  let toastTimer;
  function showToast(msg){
    const t = toast();
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(()=>t.classList.remove('show'), 2000);
  }
  // ─── Full re-rank every 30s ───
  function periodicRerank(){
    rankPanels();
    renderLayout();
  }
  // ─── Init ───
  function init(){
    loadState();
    renderLayout();
    setupObserver();
    // Soft refresh every 3s (updates values in-place, no re-query)
    setInterval(softRefresh, 3000);
    // Full re-rank every 30s
    setInterval(periodicRerank, 30000);
    dom('btnReset').addEventListener('click',function(){
      tracking = defaultTracking();
      layoutOrder = panels.map(p=>p.id);
      sessionStart = Date.now();
      panelDomCache = {};
      invalidateDom();
      saveState();
      renderLayout();
      showToast('Layout reset');
    });
    dom('btnExport').addEventListener('click',function(){
      const data = {tracking,layoutOrder,panelScores:layoutOrder.map(id=>({id,score:computeScore(id)})),sessionDuration:(Date.now()-sessionStart)/1000};
      console.log('Export:',JSON.stringify(data,null,2));
      showToast('Data exported to console');
    });
    // Track body clicks for interaction counting
    document.addEventListener('click',function(e){
      const panel = e.target.closest('[data-panel-id]');
      if(panel && !e.target.closest('button')){
        recordInteraction(panel.dataset.panelId);
      }
    });
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',init);
  } else {
    init();
  }
  // ─── Output integrity marker ───
  console.log('Adaptive Metric Layout initialized. Panels:',panels.length,'Seed:',APP_SEED);
})();
</script>
</body>
</html>```