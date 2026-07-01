<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--surface2:#222632;--border:#2a2e3a;
  --text:#e1e4ed;--text2:#8b90a0;--accent:#6c8cff;--accent2:#4ade80;
  --warn:#f59e0b;--danger:#ef4444;--radius:8px;--gap:8px;
  --panel-min:120px;--panel-compact:48px;--transition:200ms ease;
}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:12px}
.header{display:flex;justify-content:space-between;align-items:center;padding:8px 0;margin-bottom:8px}
.header h1{font-size:1.1rem;font-weight:600;letter-spacing:-0.01em}
.header .meta{font-size:0.75rem;color:var(--text2)}
.dashboard{display:grid;gap:var(--gap);grid-template-columns:repeat(auto-fit,minmax(280px,1fr));transition:grid-template-columns var(--transition),grid-template-rows var(--transition)}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all var(--transition);position:relative;display:flex;flex-direction:column}
.panel.compact{grid-row:span 1!important;grid-column:span 1!important;max-height:var(--panel-compact)}
.panel.compact .panel-body{display:none}
.panel.compact .panel-header{padding:6px 10px}
.panel-header{display:flex;align-items:center;gap:8px;padding:10px 12px;border-bottom:1px solid var(--border);cursor:grab;user-select:none;background:var(--surface2);min-height:38px}
.panel-header:active{cursor:grabbing}
.panel-title{font-size:0.8rem;font-weight:600;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-rank{font-size:0.65rem;color:var(--text2);background:var(--surface);padding:1px 6px;border-radius:10px;white-space:nowrap}
.panel-actions{display:flex;gap:4px;flex-shrink:0}
.panel-actions button{background:none;border:1px solid var(--border);color:var(--text2);cursor:pointer;padding:3px 7px;border-radius:4px;font-size:0.7rem;transition:all var(--transition)}
.panel-actions button:hover{background:var(--surface);color:var(--text)}
.panel-actions button.locked{background:var(--accent);color:#fff;border-color:var(--accent)}
.panel-actions button.expanded-btn{font-size:0.8rem;padding:3px 6px}
.panel-body{padding:12px;flex:1;display:flex;flex-direction:column;gap:8px;overflow:hidden}
.panel.large .panel-body{font-size:1rem}
.metric-value{font-size:1.6rem;font-weight:700;line-height:1.2}
.metric-label{font-size:0.7rem;color:var(--text2);text-transform:uppercase;letter-spacing:0.05em}
.metric-change{font-size:0.75rem;padding:2px 6px;border-radius:4px;display:inline-block}
.metric-change.up{background:#1a3a1a;color:var(--accent2)}
.metric-change.down{background:#3a1a1a;color:var(--danger)}
.sparkline{display:flex;align-items:flex-end;gap:2px;height:40px;padding:4px 0}
.sparkline .bar{flex:1;background:var(--accent);border-radius:1px;transition:height 300ms ease;min-width:3px}
.sparkline .bar.tail{opacity:0.3}
.gauge{position:relative;height:8px;background:var(--surface2);border-radius:4px;overflow:hidden;margin:8px 0}
.gauge-fill{height:100%;border-radius:4px;transition:width 400ms ease}
.gauge-fill.good{background:var(--accent2)}
.gauge-fill.warn{background:var(--warn)}
.gauge-fill.bad{background:var(--danger)}
.log-line{font-size:0.7rem;font-family:monospace;padding:3px 0;border-bottom:1px solid var(--border);color:var(--text2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.log-line.error{color:var(--danger)}
.log-line.warn{color:var(--warn)}
.table-compact{width:100%;font-size:0.7rem;border-collapse:collapse}
.table-compact td,.table-compact th{padding:4px 6px;text-align:left;border-bottom:1px solid var(--border)}
.table-compact th{color:var(--text2);font-weight:500}
.ghost{opacity:0.4;border-style:dashed!important}
.drag-over{border-color:var(--accent)!important;box-shadow:0 0 12px rgba(108,140,255,0.15)}
.empty-state{display:flex;align-items:center;justify-content:center;height:60px;color:var(--text2);font-size:0.75rem}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Metric Dashboard</h1>
  <div class="meta">Auto-layout active &middot; Panels re-rank every 15s</div>
</div>
<div class="dashboard" id="dashboard"></div>
<script>
(function(){
'use strict';
const DASHBOARD = document.getElementById('dashboard');
const DEBOUNCE_MS = 100;
const RERANK_INTERVAL_MS = 15000;
const DECAY_HALFLIFE_MS = 3600000;
const COMPACT_THRESHOLD = 0.15;
const STORAGE_KEY = 'aml_layout_v1';
let panels = [];
let observer = null;
let visibilityMap = new Map();
let visibilityTimers = new Map();
let rerankTimer = null;
let debounceTimer = null;
let dragState = null;
function now(){return Date.now()}
function decayWeight(ts){
  var age = now() - ts;
  return Math.pow(0.5, age / DECAY_HALFLIFE_MS);
}
function computeScore(p){
  var freq = p.interactionCount || 0;
  var dur = p.visibleDuration || 0;
  var recency = decayWeight(p.lastInteraction || p.createdAt);
  return (freq * 0.4 + (dur / 1000) * 0.35 + recency * 100 * 0.25);
}
function computeRanks(){
  var i, len = panels.length;
  for(i=0;i<len;i++){panels[i].score = computeScore(panels[i])}
  panels.sort(function(a,b){return b.score - a.score});
  var maxScore = panels.length > 0 ? panels[0].score : 1;
  for(i=0;i<len;i++){
    panels[i].rank = i;
    panels[i].compact = !panels[i].locked && (panels[i].score / Math.max(maxScore, 0.001)) < COMPACT_THRESHOLD;
  }
}
function batchUpdate(){
  computeRanks();
  patchLayout();
  persistState();
}
function debouncedBatchUpdate(){
  if(debounceTimer)return;
  debounceTimer = setTimeout(function(){
    debounceTimer = null;
    batchUpdate();
  }, DEBOUNCE_MS);
}
function getPanelEl(id){
  return document.querySelector('[data-panel-id="' + id + '"]');
}
function patchLayout(){
  var i, len = panels.length, el, rankEl, headerEl;
  for(i=0;i<len;i++){
    el = getPanelEl(panels[i].id);
    if(!el)continue;
    if(panels[i].locked)continue;
    el.style.order = panels[i].rank;
    if(panels[i].compact){el.classList.add('compact')}
    else{el.classList.remove('compact')}
    el.classList.toggle('large', panels[i].rank < 3);
    rankEl = el.querySelector('.panel-rank');
    if(rankEl)rankEl.textContent = '#' + (panels[i].rank + 1) + ' · ' + Math.round(panels[i].score * 10) / 10;
  }
  if(dragState)return;
  var sorted = panels.slice().sort(function(a,b){return a.rank - b.rank});
  for(i=0;i<sorted.length;i++){
    el = getPanelEl(sorted[i].id);
    if(!el)continue;
    DASHBOARD.appendChild(el);
  }
}
function trackView(id, visible){
  var p = panels.find(function(x){return x.id === id});
  if(!p)return;
  if(visible){
    if(visibilityMap.get(id))return;
    visibilityMap.set(id, true);
    visibilityTimers.set(id, now());
  }else{
    if(!visibilityMap.get(id))return;
    visibilityMap.set(id, false);
    var start = visibilityTimers.get(id);
    if(start){p.visibleDuration = (p.visibleDuration || 0) + (now() - start)}
    visibilityTimers.delete(id);
    debouncedBatchUpdate();
  }
}
function trackInteraction(id, type){
  var p = panels.find(function(x){return x.id === id});
  if(!p)return;
  p.interactionCount = (p.interactionCount || 0) + 1;
  p.lastInteraction = now();
  p.lastAction = type;
  debouncedBatchUpdate();
}
function setupObserver(){
  if(observer)observer.disconnect();
  observer = new IntersectionObserver(function(entries){
    var i, len = entries.length, e;
    for(i=0;i<len;i++){
      e = entries[i];
      trackView(e.target.dataset.panelId, e.isIntersecting);
    }
  }, {threshold: 0.3});
  panels.forEach(function(p){
    var el = getPanelEl(p.id);
    if(el)observer.observe(el);
  });
}
function reObserve(){
  if(!observer)return;
  observer.disconnect();
  panels.forEach(function(p){
    var el = getPanelEl(p.id);
    if(el)observer.observe(el);
  });
}
function persistState(){
  try{
    var data = panels.map(function(p){
      return {
        id:p.id,title:p.title,type:p.type,rank:p.rank,score:p.score,
        compact:p.compact,locked:p.locked,
        visibleDuration:p.visibleDuration,interactionCount:p.interactionCount,
        lastInteraction:p.lastInteraction,lastAction:p.lastAction,
        createdAt:p.createdAt
      };
    });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  }catch(e){}
}
function restoreState(){
  try{
    var raw = localStorage.getItem(STORAGE_KEY);
    if(!raw)return null;
    return JSON.parse(raw);
  }catch(e){return null}
}
function createPanelHTML(p){
  var div = document.createElement('div');
  div.className = 'panel' + (p.compact ? ' compact' : '') + (p.rank < 3 ? ' large' : '');
  div.dataset.panelId = p.id;
  div.style.order = p.rank;
  div.draggable = true;
  var header = document.createElement('div');
  header.className = 'panel-header';
  header.innerHTML = '<span class="panel-title">' + esc(p.title) + '</span>' +
    '<span class="panel-rank">#' + (p.rank + 1) + ' · ' + (Math.round(p.score * 10) / 10) + '</span>' +
    '<span class="panel-actions">' +
      '<button class="expand-btn" data-action="expand" data-panel="' + p.id + '">' + (p.compact ? '↕' : '⊟') + '</button>' +
      '<button class="lock-btn' + (p.locked ? ' locked' : '') + '" data-action="lock" data-panel="' + p.id + '">' + (p.locked ? '🔒' : '🔓') + '</button>' +
    '</span>';
  div.appendChild(header);
  var body = document.createElement('div');
  body.className = 'panel-body';
  body.id = 'body-' + p.id;
  div.appendChild(body);
  return div;
}
function renderPanelContent(id){
  var p = panels.find(function(x){return x.id === id});
  if(!p)return;
  var body = document.getElementById('body-' + id);
  if(!body)return;
  var html = '';
  switch(p.type){
    case 'metric':
      html = '<div class="metric-value">' + p.data.value + '</div>' +
        '<div class="metric-label">' + esc(p.data.label) + '</div>' +
        (p.data.change != null ? '<span class="metric-change ' + (p.data.change >= 0 ? 'up' : 'down') + '">' + (p.data.change >= 0 ? '+' : '') + p.data.change + '%</span>' : '');
      break;
    case 'sparkline':
      html = '<div class="metric-value">' + p.data.value + '</div>' +
        '<div class="metric-label">' + esc(p.data.label || 'Trend') + '</div>' +
        '<div class="sparkline">' + buildSparklineBars(p.data.points || []) + '</div>';
      break;
    case 'gauge':
      var pct = Math.min(100, Math.max(0, p.data.percent || 0));
      var cls = pct > 80 ? 'bad' : (pct > 50 ? 'warn' : 'good');
      html = '<div class="metric-value">' + pct + '%</div>' +
        '<div class="metric-label">' + esc(p.data.label || 'Utilization') + '</div>' +
        '<div class="gauge"><div class="gauge-fill ' + cls + '" style="width:' + pct + '%"></div></div>';
      break;
    case 'table':
      html = '<table class="table-compact"><thead><tr>';
      if(p.data.headers){for(var h=0;h<p.data.headers.length;h++){html += '<th>' + esc(p.data.headers[h]) + '</th>'}}
      html += '</tr></thead><tbody>';
      if(p.data.rows){for(var r=0;r<p.data.rows.length;r++){html += '<tr>';for(var c=0;c<p.data.rows[r].length;c++){html += '<td>' + esc(String(p.data.rows[r][c])) + '</td>'}html += '</tr>'}}
      html += '</tbody></table>';
      break;
    case 'log':
      html = '<div style="max-height:120px;overflow-y:auto">';
      if(p.data.lines){for(var l=0;l<p.data.lines.length;l++){html += '<div class="log-line ' + (p.data.lines[l].level || '') + '">' + esc(p.data.lines[l].text) + '</div>'}}
      html += '</div>';
      break;
    default:
      html = '<div class="empty-state">' + esc(p.data.label || 'No data') + '</div>';
  }
  body.innerHTML = html;
}
function buildSparklineBars(points){
  var i, len = points.length, max = 0, out = '';
  for(i=0;i<len;i++){if(points[i] > max)max = points[i]}
  if(max === 0)max = 1;
  for(i=0;i<len;i++){
    var h = Math.max(4, (points[i] / max) * 36);
    var cls = i < len - 3 ? 'bar tail' : 'bar';
    out += '<div class="' + cls + '" style="height:' + h + 'px"></div>';
  }
  return out;
}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function renderAllPanels(){
  var frag = document.createDocumentFragment();
  panels.forEach(function(p){
    frag.appendChild(createPanelHTML(p));
  });
  DASHBOARD.textContent = '';
  DASHBOARD.appendChild(frag);
  panels.forEach(function(p){renderPanelContent(p.id)});
  reObserve();
}
function handleAction(action, panelId){
  var p = panels.find(function(x){return x.id === panelId});
  if(!p)return;
  trackInteraction(panelId, action);
  if(action === 'lock'){
    p.locked = !p.locked;
    if(p.locked){p.compact = false}
    var lockBtn = document.querySelector('[data-action="lock"][data-panel="' + panelId + '"]');
    if(lockBtn){
      lockBtn.textContent = p.locked ? '\ud83d\udd12' : '\ud83d\udd13';
      lockBtn.classList.toggle('locked', p.locked);
    }
    persistState();
    batchUpdate();
  }else if(action === 'expand'){
    p.compact = !p.compact;
    if(!p.compact){p.visibleDuration = (p.visibleDuration || 0) + 5000}
    var el = getPanelEl(panelId);
    var expandBtn = document.querySelector('[data-action="expand"][data-panel="' + panelId + '"]');
    if(el){el.classList.toggle('compact', p.compact);el.classList.toggle('large', !p.compact && p.rank < 3)}
    if(expandBtn)expandBtn.textContent = p.compact ? '\u2195' : '\u229f';
    persistState();
    debouncedBatchUpdate();
  }
}
function handleDragStart(e){
  var panelEl = e.target.closest('.panel');
  if(!panelEl)return;
  if(e.target.closest('button')){e.preventDefault();return}
  var panelId = panelEl.dataset.panelId;
  var p = panels.find(function(x){return x.id === panelId});
  if(!p)return;
  trackInteraction(panelId, 'drag_start');
  dragState = {id:panelId, el:panelEl, startIndex:p.rank};
  panelEl.classList.add('ghost');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', panelId);
}
function handleDragOver(e){
  e.preventDefault();
  if(!dragState)return;
  e.dataTransfer.dropEffect = 'move';
  var target = e.target.closest('.panel');
  if(target && target !== dragState.el){
    target.classList.add('drag-over');
  }
}
function handleDragLeave(e){
  var target = e.target.closest('.panel');
  if(target)target.classList.remove('drag-over');
}
function handleDrop(e){
  e.preventDefault();
  if(!dragState)return;
  dragState.el.classList.remove('ghost');
  var target = e.target.closest('.panel');
  if(target && target !== dragState.el){
    target.classList.remove('drag-over');
    var targetId = target.dataset.panelId;
    var src = panels.find(function(x){return x.id === dragState.id});
    var dst = panels.find(function(x){return x.id === targetId});
    if(src && dst){
      src.locked = true;
      src.compact = false;
      var srcRank = src.rank;
      src.rank = dst.rank;
      dst.rank = srcRank;
      var el = getPanelEl(src.id);
      if(el){el.classList.remove('compact');el.style.order = src.rank}
      getPanelEl(dst.id).style.order = dst.rank;
      trackInteraction(src.id, 'drag_drop');
      var lockBtn = document.querySelector('[data-action="lock"][data-panel="' + src.id + '"]');
      if(lockBtn){lockBtn.textContent = '\ud83d\udd12';lockBtn.classList.add('locked')}
      persistState();
    }
  }
  dragState = null;
  document.querySelectorAll('.drag-over').forEach(function(el){el.classList.remove('drag-over')});
}
function handleDragEnd(e){
  if(dragState){
    dragState.el.classList.remove('ghost');
    dragState = null;
  }
  document.querySelectorAll('.drag-over').forEach(function(el){el.classList.remove('drag-over')});
}
function delegateClick(e){
  var btn = e.target.closest('button[data-action]');
  if(!btn)return;
  e.preventDefault();
  e.stopPropagation();
  handleAction(btn.dataset.action, btn.dataset.panel);
}
function delegateDblClick(e){
  var header = e.target.closest('.panel-header');
  if(!header)return;
  var panelEl = header.closest('.panel');
  if(!panelEl)return;
  if(e.target.closest('button'))return;
  handleAction('expand', panelEl.dataset.panelId);
}
function initPanels(defaultPanels){
  var saved = restoreState();
  if(saved && saved.length > 0){
    panels = saved.map(function(s){
      var def = defaultPanels.find(function(d){return d.id === s.id}) || {};
      var p = {
        id:s.id,title:def.title || s.title,type:def.type || s.type,
        data:def.data || {},rank:s.rank,score:s.score || 0,
        compact:s.compact || false,locked:s.locked || false,
        visibleDuration:s.visibleDuration || 0,
        interactionCount:s.interactionCount || 0,
        lastInteraction:s.lastInteraction || s.createdAt || now(),
        lastAction:s.lastAction || null,
        createdAt:s.createdAt || now()
      };
      return p;
    });
    var missingIds = new Set(defaultPanels.map(function(d){return d.id}));
    panels.forEach(function(p){missingIds.delete(p.id)});
    missingIds.forEach(function(id){
      var def = defaultPanels.find(function(d){return d.id === id});
      panels.push({id:def.id,title:def.title,type:def.type,data:def.data||{},rank:panels.length,score:0,compact:false,locked:false,visibleDuration:0,interactionCount:0,lastInteraction:now(),lastAction:null,createdAt:now()});
    });
  }else{
    panels = defaultPanels.map(function(d,i){
      return {id:d.id,title:d.title,type:d.type,data:d.data||{},rank:i,score:0,compact:false,locked:false,visibleDuration:0,interactionCount:0,lastInteraction:now(),lastAction:null,createdAt:now()};
    });
  }
  computeRanks();
}
var SEED = 42;
function seededRand(){
  SEED = (SEED * 16807) % 2147483647;
  return (SEED - 1) / 2147483646;
}
function buildTrend(len, base, amp){
  var out = [], i, v = base;
  for(i=0;i<len;i++){v += (seededRand() - 0.5) * amp;v = Math.max(0, v);out.push(Math.round(v))}
  return out;
}
var defaultPanels = [
  {id:'revenue',title:'Revenue',type:'sparkline',data:{value:'$847.2K',label:'Monthly Revenue',points:buildTrend(20,800,120)}},
  {id:'users',title:'Active Users',type:'metric',data:{value:'12,847',label:'Online Now',change:8.3}},
  {id:'conversion',title:'Conversion Rate',type:'metric',data:{value:'3.42%',label:'This Week',change:-0.8}},
  {id:'cpu',title:'Server Load',type:'gauge',data:{percent:62,label:'CPU Utilization'}},
  {id:'memory',title:'Memory',type:'gauge',data:{percent:78,label:'RAM Usage'}},
  {id:'orders',title:'Recent Orders',type:'table',data:{headers:['Order','Amount','Status'],rows:[['#1042','$240','Shipped'],['#1043','$890','Processing'],['#1044','$120','Pending'],['#1045','$3.2K','Delivered']]}},
  {id:'errors',title:'Error Log',type:'log',data:{lines:[{level:'error',text:'[14:23] Connection timeout to DB primary'},{level:'warn',text:'[14:18] Retry queue depth: 142'},{level:'error',text:'[14:11] SSL cert expiry in 3 days'},{level:'info',text:'[13:58] Deploy v2.4.1 complete'}]}},
  {id:'throughput',title:'API Throughput',type:'sparkline',data:{value:'1.2K/s',label:'Requests/sec',points:buildTrend(20,1200,300)}}
];
function startRerankCycle(){
  if(rerankTimer)clearInterval(rerankTimer);
  rerankTimer = setInterval(function(){
    computeRanks();
    patchLayout();
    persistState();
    reObserve();
  }, RERANK_INTERVAL_MS);
}
function init(){
  initPanels(defaultPanels);
  renderAllPanels();
  setupObserver();
  startRerankCycle();
  DASHBOARD.addEventListener('click', delegateClick);
  DASHBOARD.addEventListener('dblclick', delegateDblClick);
  DASHBOARD.addEventListener('dragstart', handleDragStart);
  DASHBOARD.addEventListener('dragover', handleDragOver);
  DASHBOARD.addEventListener('dragleave', handleDragLeave);
  DASHBOARD.addEventListener('drop', handleDrop);
  DASHBOARD.addEventListener('dragend', handleDragEnd);
}
init();
})();
</script>
</body>
</html>