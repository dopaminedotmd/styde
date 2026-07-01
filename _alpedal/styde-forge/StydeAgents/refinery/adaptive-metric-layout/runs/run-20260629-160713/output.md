I'll output the complete interactive HTML dashboard directly.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d2e;--border:#2a2d3e;
  --text:#e0e0e0;--muted:#888;--accent:#6c5ce7;
  --rank-high:#00e676;--rank-mid:#ffab40;--rank-low:#ff5252;
  --compact-scale:0.45;--gap:12px;--radius:10px;
  --header-h:48px;--toolbar-h:36px;
}
body{
  font-family:'Inter',system-ui,-apple-system,sans-serif;
  background:var(--bg);color:var(--text);min-height:100vh;
  overflow-x:hidden;
}
header{
  height:var(--header-h);background:var(--surface);border-bottom:1px solid var(--border);
  display:flex;align-items:center;padding:0 16px;gap:16px;position:sticky;top:0;z-index:100;
}
header h1{font-size:15px;font-weight:600;letter-spacing:-0.3px}
header .mode-badge{font-size:11px;padding:3px 10px;border-radius:12px;background:var(--accent);color:#fff}
.toolbar{
  height:var(--toolbar-h);display:flex;align-items:center;gap:8px;padding:0 12px;
  background:var(--surface);border-bottom:1px solid var(--border);font-size:12px;
}
.toolbar button{
  background:var(--border);color:var(--text);border:none;padding:4px 12px;
  border-radius:6px;cursor:pointer;font-size:11px;transition:background .15s;
}
.toolbar button:hover{background:var(--accent)}
.toolbar button.active{background:var(--accent);color:#fff}
.grid{
  display:grid;gap:var(--gap);padding:var(--gap);
  grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
  grid-auto-rows:minmax(160px,auto);
  transition:all .4s cubic-bezier(.4,0,.2,1);
}
.panel{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:16px;position:relative;overflow:hidden;
  transition:all .35s cubic-bezier(.4,0,.2,1);
  display:flex;flex-direction:column;cursor:grab;user-select:none;
}
.panel:active{cursor:grabbing}
.panel.locked{cursor:default;border-color:var(--accent)}
.panel.locked:active{cursor:default}
.panel.compact{transform:scale(var(--compact-scale));transform-origin:center;opacity:.65}
.panel.compact:hover{opacity:.9;transform:scale(calc(var(--compact-scale) + 0.03))}
.panel.rank-0{grid-column:span 2;grid-row:span 2;border-color:var(--rank-high);box-shadow:0 0 20px rgba(0,230,118,.08)}
.panel.rank-1{grid-column:span 2;grid-row:span 1;border-color:var(--rank-mid);box-shadow:0 0 14px rgba(255,171,64,.06)}
.panel.rank-last{grid-column:span 1;grid-row:span 1}
.panel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.panel-title{font-size:13px;font-weight:600;letter-spacing:-0.2px}
.panel-rank-dot{
  width:8px;height:8px;border-radius:50%;display:inline-block;
  transition:background .3s;
}
.panel-metrics{flex:1;display:flex;align-items:center;justify-content:center}
.panel-value{font-size:32px;font-weight:700;letter-spacing:-1px}
.panel-sub{font-size:11px;color:var(--muted);margin-top:4px;text-align:center}
.panel-controls{
  display:flex;gap:6px;position:absolute;top:8px;right:8px;opacity:0;
  transition:opacity .2s;
}
.panel:hover .panel-controls,.panel.locked .panel-controls{opacity:1}
.panel-controls button{
  background:var(--border);color:var(--text);border:none;width:24px;height:24px;
  border-radius:5px;cursor:pointer;font-size:11px;display:flex;align-items:center;justify-content:center;
  transition:background .15s;
}
.panel-controls button:hover{background:var(--accent)}
.panel-controls button.lock-btn.locked{background:var(--accent);color:#fff}
.panel-tracking{
  position:absolute;bottom:6px;right:10px;font-size:9px;color:var(--muted);
  display:flex;gap:6px;opacity:0;transition:opacity .3s;
}
.panel:hover .panel-tracking{opacity:1}
.compact-bin{
  border:1px dashed var(--border);border-radius:var(--radius);padding:16px;
  background:var(--surface);opacity:.7;min-height:80px;
  display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:center;
}
.compact-bin-label{
  width:100%;text-align:center;font-size:11px;color:var(--muted);margin-bottom:4px;
}
.compact-bin .panel{margin:4px;flex:0 0 auto;min-width:unset}
.tracking-overlay{
  position:fixed;bottom:16px;left:16px;background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);padding:10px 14px;font-size:10px;color:var(--muted);z-index:200;
  display:flex;gap:12px;transition:opacity .4s;
}
.tracking-overlay span{color:var(--text);font-weight:600}
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <span class="mode-badge" id="modeBadge">auto</span>
</header>
<div class="toolbar">
  <button id="btnReset" title="Reset all tracking data">reset tracking</button>
  <button id="btnRecalc" title="Force recalculate layout">recalculate</button>
  <button id="btnToggleMode" title="Toggle auto/manual mode">toggle mode</button>
  <span style="margin-left:auto;font-size:11px;color:var(--muted)">drag panels to reorder · lock to pin</span>
</div>
<div class="grid" id="grid"></div>
<div class="compact-bin" id="compactBin">
  <span class="compact-bin-label">compact zone — low-usage panels auto-shrink here</span>
</div>
<div class="tracking-overlay" id="trackingOverlay">
  sessions tracked: <span id="statSessions">0</span>
  total views: <span id="statViews">0</span>
  active: <span id="statActive">0s</span>
</div>
<script>
(function(){
const STORAGE_KEY = 'adaptive_dashboard_v1';
const DECAY_HALF = 12 * 60 * 60 * 1000; // 12h half-life for recency
const COMPACT_THRESHOLD = 0.15; // bottom 15% get compacted
const UPDATE_INTERVAL = 4000; // ms between rank recalculations
let panels = [];
let tracking = {}; // panelId -> {views, totalDuration, lastInteraction, frequency[]}
let mode = 'auto'; // 'auto' | 'manual'
let panelElements = new Map();
let observer = null;
let activePanels = new Set();
let activeStartTimes = new Map();
let updateTimer = null;
let dragState = null;
function defaultPanels(){
  return [
    {id:'revenue',title:'Revenue',value:'$128.4K',sub:'+12.3% vs last month',locked:false,compact:false},
    {id:'users',title:'Active Users',value:'8,421',sub:'+5.7% this week',locked:false,compact:false},
    {id:'conversion',title:'Conversion',value:'3.82%',sub:'-0.3% vs target',locked:false,compact:false},
    {id:'latency',title:'P95 Latency',value:'142ms',sub:'-8ms improvement',locked:false,compact:false},
    {id:'errors',title:'Error Rate',value:'0.12%',sub:'below 0.5% SLA',locked:false,compact:false},
    {id:'churn',title:'Churn Rate',value:'1.8%',sub:'-0.4% month-over-month',locked:false,compact:false},
    {id:'mrr',title:'MRR',value:'$842K',sub:'+$38K net new',locked:false,compact:false},
    {id:'cpu',title:'CPU Usage',value:'67%',sub:'avg across cluster',locked:false,compact:false},
    {id:'storage',title:'Storage',value:'2.1TB',sub:'34% capacity used',locked:false,compact:false},
    {id:'api_calls',title:'API Calls',value:'2.4M/day',sub:'rate limit: 68%',locked:false,compact:false}
  ];
}
function loadState(){
  let raw = null;
  try{ raw = localStorage.getItem(STORAGE_KEY); }catch(e){}
  if(raw){
    try{
      let saved = JSON.parse(raw);
      if(saved.panels && Array.isArray(saved.panels) && saved.panels.length>0){
        panels = saved.panels;
      } else { panels = defaultPanels(); }
      if(saved.tracking && typeof saved.tracking === 'object'){
        tracking = saved.tracking;
      } else { initTracking(); }
      if(saved.mode === 'manual') mode = 'manual';
    }catch(e){ panels = defaultPanels(); initTracking(); }
  } else {
    panels = defaultPanels();
    initTracking();
  }
}
function initTracking(){
  tracking = {};
  panels.forEach(p => {
    tracking[p.id] = {views:0,totalDuration:0,lastInteraction:0,frequency:[]};
  });
}
function saveState(){
  try{
    localStorage.setItem(STORAGE_KEY, JSON.stringify({panels,tracking,mode}));
  }catch(e){}
}
function rankScore(panelId){
  let t = tracking[panelId];
  if(!t) return 0;
  let now = Date.now();
  let recency = Math.exp(-(now - t.lastInteraction) / DECAY_HALF);
  let views = t.views || 0;
  let duration = t.totalDuration || 0;
  let freq = t.frequency ? t.frequency.length : 0;
  return (views * 1.0) + (duration * 0.001) + (freq * 5.0) + (recency * 10.0);
}
function recalculateRanks(){
  if(mode === 'manual') return;
  let scored = panels.map((p,i) => ({idx:i,id:p.id,score:rankScore(p.id),locked:p.locked}));
  scored.sort((a,b) => b.score - a.score);
  let lockIdx = 0;
  let unlocked = [];
  scored.forEach((s,i) => { if(!s.locked) unlocked.push(s); });
  let n = scored.length;
  let thresholdIdx = Math.max(Math.floor(n * (1 - COMPACT_THRESHOLD)), Math.min(n-1, Math.floor(n*0.85)));
  let rankOrder = new Array(n);
  let rank = 0;
  scored.forEach((s,i) => {
    if(s.locked){
      rankOrder[s.idx] = s.idx;
    } else {
      rankOrder[s.idx] = unlocked.indexOf(s);
    }
  });
  panels.forEach((p,i) => {
    if(mode==='manual') return;
    p._rank = rankOrder[i];
    if(!p.locked){
      p.compact = (rankOrder[i] >= unlocked.length - Math.max(1, Math.floor(unlocked.length*COMPACT_THRESHOLD)));
    }
  });
  applyLayout();
}
function applyLayout(){
  let grid = document.getElementById('grid');
  let compactBin = document.getElementById('compactBin');
  if(!grid || !compactBin) return;
  grid.innerHTML = '';
  compactBin.querySelectorAll('.panel').forEach(el=>el.remove());
  let sorted = panels.map((p,i) => ({...p,idx:i})).sort((a,b) => {
    if(a.locked && b.locked) return a.idx - b.idx;
    if(a.locked) return -1;
    if(b.locked) return 1;
    return (a._rank||999) - (b._rank||999);
  });
  sorted.forEach((p,i) => {
    let el = createPanelElement(p, i);
    if(p.compact && !p.locked){
      compactBin.appendChild(el);
    } else {
      grid.appendChild(el);
    }
  });
  updateCompactBinLabel();
}
function updateCompactBinLabel(){
  let bin = document.getElementById('compactBin');
  let label = bin && bin.querySelector('.compact-bin-label');
  if(!label) return;
  let compactCount = panels.filter(p=>p.compact&&!p.locked).length;
  label.textContent = compactCount>0
    ? `compact zone — ${compactCount} low-usage panel${compactCount>1?'s':''} auto-shrunk here`
    : 'compact zone — low-usage panels auto-shrink here';
}
function createPanelElement(p, sortIndex){
  let el = document.createElement('div');
  el.className = 'panel';
  el.dataset.panelId = p.id;
  el.draggable = true;
  if(p.locked) el.classList.add('locked');
  if(p.compact && !p.locked) el.classList.add('compact');
  if(p._rank === 0 && !p.compact) el.classList.add('rank-0');
  else if(p._rank === 1 && !p.compact) el.classList.add('rank-1');
  else if(p._rank !== undefined && p._rank >= panels.length-2) el.classList.add('rank-last');
  let rankColor = p._rank===0?'var(--rank-high)':p._rank===1?'var(--rank-mid)':'var(--rank-low)';
  el.innerHTML =
    '<div class="panel-header">'+
      '<span class="panel-title">'+
        '<span class="panel-rank-dot" style="background:'+rankColor+'"></span> '+esc(p.title)+
      '</span>'+
    '</div>'+
    '<div class="panel-metrics"><span class="panel-value">'+esc(p.value)+'</span></div>'+
    '<div class="panel-sub">'+esc(p.sub||'')+'</div>'+
    '<div class="panel-controls">'+
      '<button class="lock-btn'+(p.locked?' locked':'')+'" data-action="lock" title="'+(p.locked?'unlock':'lock')+' position">'+(p.locked?'&#128274;':'&#128275;')+'</button>'+
      '<button data-action="compact" title="toggle compact">&#9633;</button>'+
    '</div>'+
    '<div class="panel-tracking">'+
      '<span>views:'+(tracking[p.id]?tracking[p.id].views:0)+'</span>'+
      '<span>score:'+(rankScore(p.id)||0).toFixed(1)+'</span>'+
    '</div>';
  el.addEventListener('click', function(e){
    if(e.target.closest('[data-action]')) return;
    recordInteraction(p.id, 'click');
  });
  el.addEventListener('dragstart', function(e){
    if(p.locked){ e.preventDefault(); return; }
    dragState = {id:p.id,el:el};
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', p.id);
  });
  el.addEventListener('dragover', function(e){ e.preventDefault(); e.dataTransfer.dropEffect='move'; });
  el.addEventListener('drop', function(e){
    e.preventDefault();
    if(!dragState||dragState.id===p.id) return;
    let srcId = dragState.id; let dstId = p.id;
    let srcIdx = panels.findIndex(x=>x.id===srcId); let dstIdx = panels.findIndex(x=>x.id===dstId);
    if(srcIdx<0||dstIdx<0) return;
    let [moved] = panels.splice(srcIdx,1);
    panels.splice(dstIdx,0,moved);
    dragState = null;
    recalculateRanks();
    saveState();
  });
  el.addEventListener('dragend', function(){ dragState = null; });
  let lockBtn = el.querySelector('[data-action="lock"]');
  if(lockBtn){
    lockBtn.addEventListener('click', function(e){
      e.stopPropagation();
      p.locked = !p.locked;
      lockBtn.classList.toggle('locked', p.locked);
      lockBtn.title = p.locked ? 'unlock position' : 'lock position';
      lockBtn.innerHTML = p.locked ? '&#128274;' : '&#128275;';
      el.classList.toggle('locked', p.locked);
      if(p.locked){ p.compact = false; el.classList.remove('compact'); }
      recalculateRanks();
      saveState();
    });
  }
  let compactBtn = el.querySelector('[data-action="compact"]');
  if(compactBtn){
    compactBtn.addEventListener('click', function(e){
      e.stopPropagation();
      if(p.locked) return;
      p.compact = !p.compact;
      recalculateRanks();
      saveState();
    });
  }
  panelElements.set(p.id, el);
  if(observer) observer.observe(el);
  return el;
}
function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function recordInteraction(panelId, type){
  if(!tracking[panelId]) tracking[panelId] = {views:0,totalDuration:0,lastInteraction:0,frequency:[]};
  let t = tracking[panelId];
  t.lastInteraction = Date.now();
  if(type==='click'){ t.views = (t.views||0)+1; t.frequency.push(Date.now()); }
  if(t.frequency && t.frequency.length>100) t.frequency = t.frequency.slice(-100);
  saveState();
}
function recordViewDuration(panelId, ms){
  if(!tracking[panelId]) tracking[panelId] = {views:0,totalDuration:0,lastInteraction:0,frequency:[]};
  tracking[panelId].totalDuration = (tracking[panelId].totalDuration||0) + ms;
  tracking[panelId].lastInteraction = Date.now();
  saveState();
}
function setupObserver(){
  if(observer) observer.disconnect();
  observer = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      let pid = entry.target.dataset.panelId;
      if(!pid) return;
      if(entry.isIntersecting){
        if(!activePanels.has(pid)){
          activePanels.add(pid);
          activeStartTimes.set(pid, Date.now());
        }
      } else {
        if(activePanels.has(pid)){
          let start = activeStartTimes.get(pid)||Date.now();
          let duration = Date.now() - start;
          if(duration > 100) recordViewDuration(pid, duration);
          activePanels.delete(pid);
          activeStartTimes.delete(pid);
        }
      }
    });
  }, {threshold:0.3});
  panelElements.forEach(function(el){ observer.observe(el); });
}
function flushActiveDurations(){
  let now = Date.now();
  activePanels.forEach(function(pid){
    let start = activeStartTimes.get(pid)||now;
    let duration = now - start;
    if(duration > 100) recordViewDuration(pid, duration);
    activeStartTimes.set(pid, now);
  });
}
function updateStats(){
  let totalViews = 0; let totalActive = 0;
  Object.values(tracking).forEach(function(t){
    totalViews += t.views||0;
  });
  activePanels.forEach(function(pid){
    let start = activeStartTimes.get(pid)||Date.now();
    totalActive += Date.now() - start;
  });
  document.getElementById('statSessions').textContent = Object.keys(tracking).length;
  document.getElementById('statViews').textContent = totalViews;
  document.getElementById('statActive').textContent = Math.round(totalActive/1000)+'s';
}
function toggleMode(){
  mode = (mode==='auto')?'manual':'auto';
  document.getElementById('modeBadge').textContent = mode;
  if(mode==='manual'){
    panels.forEach(function(p){ p.compact = false; });
  }
  recalculateRanks();
  saveState();
}
function resetTracking(){
  initTracking();
  activePanels.clear();
  activeStartTimes.clear();
  recalculateRanks();
  saveState();
  applyLayout();
}
function init(){
  loadState();
  applyLayout();
  setupObserver();
  updateStats();
  document.getElementById('modeBadge').textContent = mode;
  document.getElementById('btnReset').addEventListener('click', resetTracking);
  document.getElementById('btnRecalc').addEventListener('click', function(){ recalculateRanks(); saveState(); });
  document.getElementById('btnToggleMode').addEventListener('click', toggleMode);
  updateTimer = setInterval(function(){
    flushActiveDurations();
    recalculateRanks();
    updateStats();
    saveState();
  }, UPDATE_INTERVAL);
  window.addEventListener('beforeunload', function(){
    flushActiveDurations();
    saveState();
  });
}
init();
})();
</script>
</body>
</html>
```