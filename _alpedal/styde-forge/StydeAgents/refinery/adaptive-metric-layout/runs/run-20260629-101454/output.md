<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Layout Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0f1117;--surface:#1a1d27;--border:#2a2d3a;--text:#e1e4ed;--text-muted:#6b7084;--accent:#6c5ce7;--accent-glow:rgba(108,92,231,0.3);--rank-1:#00d2ff;--rank-2:#7b68ee;--rank-3:#a29bfe;--rank-low:#4a4d5a;--compact-bg:#14161f;--lock:#ffd700;--attention-ring:rgba(0,210,255,0.4)}
body{font-family:'Inter',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
.header{display:flex;align-items:center;justify-content:space-between;padding:12px 20px;background:var(--surface);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100}
.header h1{font-size:1.1rem;font-weight:600;letter-spacing:-0.02em}
.controls{display:flex;gap:8px;align-items:center}
.btn{background:var(--surface);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.8rem;transition:all 0.15s}
.btn:hover{background:var(--border);border-color:var(--accent)}
.btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.locked{border-color:var(--lock);box-shadow:0 0 8px rgba(255,215,0,0.3)}
.heat-toggle{display:flex;align-items:center;gap:8px;font-size:0.8rem;color:var(--text-muted)}
.dashboard{display:grid;gap:12px;padding:16px;min-height:calc(100vh - 60px);transition:grid-template-columns 0.5s ease,grid-template-rows 0.5s ease}
.dashboard.mode-auto{grid-template-columns:repeat(4,1fr);grid-auto-rows:minmax(180px,auto)}
.dashboard.mode-compact{grid-template-columns:repeat(4,1fr);grid-auto-rows:minmax(80px,auto)}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px;position:relative;transition:all 0.4s cubic-bezier(0.25,1,0.5,1);overflow:hidden;cursor:grab;display:flex;flex-direction:column;min-height:0}
.panel:active{cursor:grabbing}
.panel.rank-1{border-color:var(--rank-1);box-shadow:0 0 20px var(--attention-ring)}
.panel.rank-2{border-color:var(--rank-2)}
.panel.rank-3{border-color:var(--rank-3)}
.panel.rank-low{border-color:var(--rank-low)}
.panel.compact{padding:10px;grid-row:span 1!important;font-size:0.75rem}
.panel.compact .panel-body{display:none}
.panel.compact .panel-header{font-size:0.8rem}
.panel.locked{border-style:dashed;border-color:var(--lock)}
.panel.dragging{opacity:0.6;z-index:50;transform:scale(0.98)}
.panel-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;flex-shrink:0}
.panel-title{font-weight:600;font-size:0.85rem;display:flex;align-items:center;gap:6px}
.panel-rank-badge{font-size:0.6rem;padding:1px 6px;border-radius:10px;background:var(--accent);color:#fff;opacity:0.9}
.panel-meta{display:flex;gap:6px;align-items:center}
.panel-lock-btn{background:none;border:none;color:var(--text-muted);cursor:pointer;font-size:0.8rem;padding:2px 4px;border-radius:4px;transition:all 0.15s}
.panel-lock-btn:hover{color:var(--lock)}
.panel-lock-btn.locked{color:var(--lock)}
.panel-body{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;font-size:0.8rem;color:var(--text-muted);overflow:hidden}
.attention-bar{position:absolute;bottom:0;left:0;height:3px;background:var(--accent);transition:width 0.5s ease;border-radius:0 2px 0 0;opacity:0.6}
.attention-heatmap{position:absolute;inset:0;pointer-events:none;opacity:0;transition:opacity 0.3s}
.heatmap-visible .attention-heatmap{opacity:0.15}
.attention-dot{position:absolute;width:40px;height:40px;border-radius:50%;background:radial-gradient(circle,var(--accent) 0%,transparent 70%);transform:translate(-50%,-50%);opacity:0.6;animation:fadeDot 3s ease-out forwards}
@keyframes fadeDot{to{opacity:0;transform:translate(-50%,-50%) scale(2)}}
.metric-chart{width:100%;height:100%;display:flex;align-items:flex-end;gap:2px;padding:0 4px}
.metric-chart .bar{flex:1;background:var(--accent);border-radius:2px 2px 0 0;transition:height 0.3s ease;min-width:3px}
.metric-value{font-size:1.8rem;font-weight:700;line-height:1;letter-spacing:-0.03em}
.metric-label{font-size:0.65rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em}
.compact-preview{display:flex;align-items:center;gap:8px}
.compact-preview .spark{flex:1;height:20px;display:flex;align-items:flex-end;gap:1px}
.compact-preview .spark-dot{flex:1;background:var(--accent);border-radius:1px;opacity:0.5}
.panel-grid-2{grid-column:span 2;grid-row:span 2}
.panel-grid-1-2{grid-column:span 1;grid-row:span 2}
.panel-expand-btn{background:none;border:none;color:var(--text-muted);cursor:pointer;font-size:0.7rem;padding:2px 6px;border-radius:4px}
.panel-expand-btn:hover{color:var(--text)}
.more-section{grid-column:1/-1;border:1px dashed var(--border);border-radius:10px;padding:12px;display:flex;flex-wrap:wrap;gap:8px;align-items:center;min-height:50px}
.more-section-label{font-size:0.7rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.08em}
.more-section .mini-panel{background:var(--compact-bg);border:1px solid var(--border);border-radius:6px;padding:6px 10px;font-size:0.7rem;cursor:pointer;transition:all 0.2s;display:flex;align-items:center;gap:4px}
.more-section .mini-panel:hover{border-color:var(--accent)}
.tooltip{position:fixed;background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:10px 14px;font-size:0.75rem;pointer-events:none;z-index:200;opacity:0;transition:opacity 0.15s;box-shadow:0 8px 24px rgba(0,0,0,0.4)}
.tooltip.visible{opacity:1}
.reset-btn{background:transparent;border:1px solid var(--border);color:var(--text-muted);padding:4px 10px;border-radius:6px;cursor:pointer;font-size:0.7rem}
.reset-btn:hover{color:var(--text);border-color:var(--accent)}
.drag-ghost{position:fixed;pointer-events:none;z-index:1000;opacity:0.9;background:var(--surface);border:2px solid var(--accent);border-radius:10px;padding:12px;font-size:0.8rem;box-shadow:0 12px 40px rgba(0,0,0,0.5);transform:translate(-50%,-50%);display:none}
</style>
</head>
<body>
<div class="header">
<h1>Adaptive Layout</h1>
<div class="controls">
<label class="heat-toggle"><input type="checkbox" id="heatmapToggle">Heatmap</label>
<button class="btn" id="autoLayoutBtn" onclick="toggleLayoutMode()">Auto: ON</button>
<button class="btn reset-btn" onclick="resetAll()">Reset Behavior</button>
<button class="btn reset-btn" onclick="exportData()">Export</button>
</div>
</div>
<div class="dashboard mode-auto" id="dashboard"></div>
<div class="tooltip" id="tooltip"></div>
<div class="drag-ghost" id="dragGhost"></div>
<script>
const STORAGE_KEY = 'adaptive_layout_v1';
const DECAY_HALFLIFE = 7 * 24 * 60 * 60 * 1000;
const VIEWPORT_THRESHOLD = 0.5;
const COMPACT_THRESHOLD_PCT = 15;
const RANK_UPDATE_INTERVAL = 5000;
const MAX_HEAT_DOTS = 100;
let panels = [];
let layoutMode = 'auto';
let showHeatmap = false;
let rankUpdateTimer = null;
let observers = new Map();
let dragState = null;
const DEFAULT_PANELS = [
  {id:'revenue',title:'Revenue',type:'metric',value:284659,unit:'$',trend:[65,72,78,71,85,82,90,88,95,92],locked:false,compact:false},
  {id:'users',title:'Active Users',type:'metric',value:12453,unit:'',trend:[8,9,10,9,11,10,12,11,13,12],locked:false,compact:false},
  {id:'conversion',title:'Conversion Rate',type:'metric',value:3.82,unit:'%',trend:[3.2,3.4,3.1,3.5,3.3,3.6,3.4,3.7,3.6,3.8],locked:false,compact:false},
  {id:'latency',title:'Avg Latency',type:'metric',value:142,unit:'ms',trend:[180,175,168,160,155,150,148,145,143,142],locked:false,compact:false},
  {id:'errors',title:'Error Rate',type:'metric',value:0.12,unit:'%',trend:[0.3,0.25,0.22,0.2,0.18,0.15,0.14,0.13,0.12,0.12],locked:false,compact:false},
  {id:'bandwidth',title:'Bandwidth',type:'chart',value:876,unit:'Mbps',trend:[400,520,610,700,750,800,820,850,860,876],locked:false,compact:false},
  {id:'cpu',title:'CPU Usage',type:'chart',value:67,unit:'%',trend:[55,60,58,62,65,63,68,66,70,67],locked:false,compact:false},
  {id:'memory',title:'Memory',type:'chart',value:72,unit:'%',trend:[60,62,65,68,66,70,69,73,71,72],locked:false,compact:false},
  {id:'sessions',title:'Sessions',type:'metric',value:3421,unit:'',trend:[2800,2900,3100,3000,3200,3150,3300,3280,3400,3421],locked:false,compact:false},
  {id:'api_calls',title:'API Calls/min',type:'chart',value:4520,unit:'',trend:[3800,3900,4100,4200,4300,4350,4400,4450,4500,4520],locked:false,compact:false},
  {id:'uptime',title:'Uptime',type:'metric',value:99.97,unit:'%',trend:[99.9,99.91,99.93,99.92,99.94,99.95,99.94,99.96,99.95,99.97],locked:false,compact:false},
  {id:'disk_io',title:'Disk I/O',type:'chart',value:320,unit:'MB/s',trend:[280,290,300,310,305,315,325,318,322,320],locked:false,compact:false}
];
function loadState(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(!raw) return initFresh();
    const data = JSON.parse(raw);
    const now = Date.now();
    panels = data.panels || DEFAULT_PANELS.map(p=>({...p}));
    panels.forEach(p=>{
      p._attention = p._attention || {score:0,frequency:0,totalDuration:0,lastSeen:now-86400000,interactions:0,viewports:0};
      if(!p._attention.clickHistory) p._attention.clickHistory = [];
      p._rank = p._rank || panels.indexOf(p)+1;
    });
    layoutMode = data.layoutMode || 'auto';
    showHeatmap = data.showHeatmap || false;
  }catch(e){initFresh()}
}
function initFresh(){
  const now = Date.now();
  panels = DEFAULT_PANELS.map((p,i)=>{
    const panel = {...p};
    panel._attention = {score:50-i*4,frequency:10-i,totalDuration:60000-(i*5000),lastSeen:now-3600000+(i*300000),interactions:5-i,clickHistory:[]};
    panel._rank = i+1;
    return panel;
  });
  layoutMode = 'auto';
  showHeatmap = false;
  saveState();
}
function saveState(){
  const data = {panels,layoutMode,showHeatmap,timestamp:Date.now()};
  localStorage.setItem(STORAGE_KEY,JSON.stringify(data));
}
function attentionScore(p){
  const a = p._attention;
  const now = Date.now();
  const hoursSinceSeen = Math.max(0,(now - a.lastSeen)/3600000);
  const recencyFactor = Math.exp(-hoursSinceSeen * Math.LN2 / (DECAY_HALFLIFE/3600000));
  const freqNorm = Math.min(a.frequency/50,1);
  const durNorm = Math.min(a.totalDuration/300000,1);
  const interactNorm = Math.min(a.interactions/30,1);
  return (freqNorm*0.25 + durNorm*0.25 + recencyFactor*0.35 + interactNorm*0.15)*100;
}
function rankAll(){
  panels.forEach(p=>{
    p._attention.score = attentionScore(p);
  });
  panels.sort((a,b)=>{
    if(a.locked && b.locked) return 0;
    if(a.locked) return -1;
    if(b.locked) return 1;
    return b._attention.score - a._attention.score;
  });
  panels.forEach((p,i)=>{p._rank = i+1;});
  const maxScore = Math.max(...panels.map(p=>p._attention.score),1);
  panels.forEach(p=>{
    if(!p.locked){
      p.compact = (p._attention.score / maxScore * 100) < COMPACT_THRESHOLD_PCT;
    }
  });
}
function rankClass(p){
  if(p.compact) return 'rank-low';
  if(p._rank <= 2) return 'rank-1';
  if(p._rank <= 4) return 'rank-2';
  if(p._rank <= 7) return 'rank-3';
  return 'rank-low';
}
function gridClass(p){
  if(p.compact) return '';
  if(p._rank === 1) return 'panel-grid-2';
  if(p._rank === 2) return 'panel-grid-1-2';
  if(p._rank <= 4 && p.type === 'chart') return 'panel-grid-1-2';
  if(p._rank <= 3) return '';
  return '';
}
function buildSparkline(trend,h=24){
  const max=Math.max(...trend,1),min=Math.min(...trend);
  const range=max-min||1;
  return trend.map(v=>{
    const ht=((v-min)/range)*h;
    return `<div class="spark-dot" style="height:${Math.max(2,ht)}px"></div>`;
  }).join('');
}
function buildChart(trend,h=50){
  const max=Math.max(...trend,1),min=Math.min(...trend);
  const range=max-min||1;
  return trend.map(v=>{
    const ht=((v-min)/range)*h;
    return `<div class="bar" style="height:${Math.max(4,ht)}px" title="${v}"></div>`;
  }).join('');
}
function buildPanelHTML(p){
  const cls = [rankClass(p),gridClass(p),p.compact?'compact':'',p.locked?'locked':''].filter(Boolean).join(' ');
  const attn = p._attention.score.toFixed(1);
  let body = '';
  if(p.compact){
    body = `<div class="compact-preview"><div class="spark">${buildSparkline(p.trend,20)}</div><span style="font-weight:700">${p.value.toLocaleString()}${p.unit}</span></div>`;
  }else if(p.type==='chart'){
    body = `<div class="metric-chart">${buildChart(p.trend,60)}</div>`;
  }else{
    body = `<div class="metric-value">${p.value.toLocaleString()}<span style="font-size:0.6em;color:var(--text-muted)">${p.unit}</span></div><div class="metric-chart" style="height:40px;margin-top:8px">${buildChart(p.trend,30)}</div>`;
  }
  return `<div class="panel ${cls}" data-panel-id="${p.id}" draggable="${p.locked?'false':'true'}">
<div class="attention-bar" style="width:${Math.min(attn,100)}%"></div>
<div class="attention-heatmap" id="heat-${p.id}"></div>
<div class="panel-header">
<span class="panel-title">${p.title}<span class="panel-rank-badge">#${p._rank}</span></span>
<div class="panel-meta">
<span style="font-size:0.6rem;color:var(--text-muted)">${attn}</span>
<button class="panel-lock-btn ${p.locked?'locked':''}" onclick="toggleLock('${p.id}')" title="${p.locked?'Unlock':'Lock'}">${p.locked?'🔒':'🔓'}</button>
</div>
</div>
<div class="panel-body">${body}</div>
</div>`;
}
function render(){
  rankAll();
  const dash = document.getElementById('dashboard');
  const html = panels.map(p=>buildPanelHTML(p)).join('');
  const compacted = panels.filter(p=>p.compact && !p.locked);
  let moreHTML = '';
  if(compacted.length > 4){
    const overflow = compacted.slice(4);
    moreHTML = `<div class="more-section"><span class="more-section-label">More (${overflow.length})</span>${overflow.map(p=>`<div class="mini-panel" onclick="expandPanel('${p.id}')">${p.title} · ${p.value}${p.unit} <span style="font-size:0.6rem;color:var(--text-muted)">${p._attention.score.toFixed(0)}</span></div>`).join('')}</div>`;
  }
  dash.innerHTML = html + moreHTML;
  dash.className = `dashboard mode-${layoutMode}` + (showHeatmap?' heatmap-visible':'');
  document.getElementById('heatmapToggle').checked = showHeatmap;
  document.getElementById('autoLayoutBtn').textContent = layoutMode==='auto'?'Auto: ON':'Auto: OFF';
  document.getElementById('autoLayoutBtn').className = layoutMode==='auto'?'btn active':'btn';
  setupObservers();
  setupDragListeners();
}
function setupObservers(){
  observers.forEach(o=>o.disconnect());
  observers.clear();
  const opts = {threshold:[0,0.25,0.5,0.75,1.0]};
  const cb = (entries)=>{
    entries.forEach(e=>{
      const id = e.target.dataset.panelId;
      const p = panels.find(x=>x.id===id);
      if(!p) return;
      if(e.intersectionRatio >= VIEWPORT_THRESHOLD){
        if(!p._viewportStart) p._viewportStart = Date.now();
        p._attention.viewports++;
      }else{
        if(p._viewportStart){
          p._attention.totalDuration += Date.now() - p._viewportStart;
          p._viewportStart = null;
        }
        p._attention.lastSeen = Date.now();
      }
    });
  };
  document.querySelectorAll('.panel').forEach(el=>{
    const obs = new IntersectionObserver(cb,opts);
    obs.observe(el);
    observers.set(el.dataset.panelId,obs);
  });
}
function setupDragListeners(){
  document.querySelectorAll('.panel[draggable="true"]').forEach(el=>{
    el.addEventListener('dragstart',onDragStart);
    el.addEventListener('dragend',onDragEnd);
    el.addEventListener('click',onPanelClick);
  });
  document.querySelectorAll('.panel').forEach(el=>{
    el.addEventListener('mouseenter',onPanelEnter);
    el.addEventListener('mouseleave',onPanelLeave);
  });
  const dash = document.getElementById('dashboard');
  dash.addEventListener('dragover',e=>e.preventDefault());
  dash.addEventListener('drop',onDrop);
}
function onDragStart(e){
  const id = e.target.closest('.panel')?.dataset.panelId;
  if(!id) return;
  const p = panels.find(x=>x.id===id);
  if(!p || p.locked){e.preventDefault();return;}
  e.target.classList.add('dragging');
  e.dataTransfer.setData('text/plain',id);
  e.dataTransfer.effectAllowed = 'move';
  dragState = {id,panel:p,startIdx:panels.indexOf(p)};
}
function onDragEnd(e){
  e.target.classList.remove('dragging');
  dragState = null;
  saveState();
  render();
}
function onDrop(e){
  e.preventDefault();
  const srcId = e.dataTransfer.getData('text/plain');
  const targetEl = e.target.closest('.panel');
  if(!targetEl || !srcId) return;
  const dstId = targetEl.dataset.panelId;
  if(srcId === dstId) return;
  const srcIdx = panels.findIndex(p=>p.id===srcId);
  const dstIdx = panels.findIndex(p=>p.id===dstId);
  if(srcIdx<0||dstIdx<0) return;
  const src = panels[srcIdx];
  if(src.locked) return;
  const dst = panels[dstIdx];
  if(dst.locked){
    showTooltip(e,'Cannot swap with locked panel');
    return;
  }
  [panels[srcIdx],panels[dstIdx]] = [panels[dstIdx],panels[srcIdx]];
  saveState();
  render();
}
function onPanelClick(e){
  if(e.target.closest('.panel-lock-btn')) return;
  const id = e.target.closest('.panel')?.dataset.panelId;
  const p = panels.find(x=>x.id===id);
  if(!p) return;
  p._attention.interactions++;
  p._attention.frequency++;
  p._attention.lastSeen = Date.now();
  if(showHeatmap){
    const heatEl = document.getElementById('heat-'+id);
    if(heatEl){
      const rect = heatEl.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const dot = document.createElement('div');
      dot.className = 'attention-dot';
      dot.style.left = x+'px';
      dot.style.top = y+'px';
      heatEl.appendChild(dot);
      setTimeout(()=>dot.remove(),3000);
      const dots = heatEl.querySelectorAll('.attention-dot');
      if(dots.length > MAX_HEAT_DOTS) dots[0].remove();
    }
  }
  saveState();
}
function onPanelEnter(e){
  const id = e.target.closest('.panel')?.dataset.panelId;
  const p = panels.find(x=>x.id===id);
  if(!p) return;
  if(!p._enterTime) p._enterTime = Date.now();
}
function onPanelLeave(e){
  const id = e.target.closest('.panel')?.dataset.panelId;
  const p = panels.find(x=>x.id===id);
  if(!p) return;
  if(p._enterTime){
    p._attention.totalDuration += Date.now() - p._enterTime;
    p._enterTime = null;
    p._attention.lastSeen = Date.now();
    saveState();
  }
}
function toggleLock(id){
  const p = panels.find(x=>x.id===id);
  if(!p) return;
  p.locked = !p.locked;
  p.compact = false;
  saveState();
  render();
  showTooltip(null,p.locked?`${p.title} locked in place`:`${p.title} unlocked`);
}
function expandPanel(id){
  const p = panels.find(x=>x.id===id);
  if(!p) return;
  p.compact = false;
  p._attention.interactions += 2;
  p._attention.frequency += 2;
  p._attention.lastSeen = Date.now();
  saveState();
  render();
}
function toggleLayoutMode(){
  layoutMode = layoutMode==='auto'?'compact':'auto';
  saveState();
  render();
}
function showTooltip(e,msg){
  const tt = document.getElementById('tooltip');
  tt.textContent = msg;
  tt.classList.add('visible');
  if(e){
    tt.style.left = (e.clientX+12)+'px';
    tt.style.top = (e.clientY-30)+'px';
  }else{
    tt.style.left = '50%';
    tt.style.top = '10px';
  }
  clearTimeout(tt._timeout);
  tt._timeout = setTimeout(()=>tt.classList.remove('visible'),2000);
}
function resetAll(){
  if(!confirm('Reset all tracking data and layout? This cannot be undone.')) return;
  localStorage.removeItem(STORAGE_KEY);
  initFresh();
  render();
}
function exportData(){
  const data = {panels:panels.map(p=>({id:p.id,title:p.title,attention:p._attention,rank:p._rank,locked:p.locked,compact:p.compact})),layoutMode,exportedAt:new Date().toISOString()};
  const blob = new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'adaptive-layout-export.json';
  a.click();
  URL.revokeObjectURL(url);
}
document.getElementById('heatmapToggle').addEventListener('change',function(e){
  showHeatmap = e.target.checked;
  saveState();
  render();
});
function rankUpdateLoop(){
  rankAll();
  saveState();
  render();
  rankUpdateTimer = setTimeout(rankUpdateLoop,RANK_UPDATE_INTERVAL);
}
window.addEventListener('beforeunload',()=>{
  panels.forEach(p=>{
    if(p._viewportStart){
      p._attention.totalDuration += Date.now() - p._viewportStart;
      p._viewportStart = null;
    }
    if(p._enterTime){
      p._attention.totalDuration += Date.now() - p._enterTime;
      p._enterTime = null;
    }
    p._attention.lastSeen = Date.now();
    p._attention.score = attentionScore(p);
  });
  saveState();
});
loadState();
render();
rankUpdateTimer = setTimeout(rankUpdateLoop,RANK_UPDATE_INTERVAL);
</script>
</body>
</html>