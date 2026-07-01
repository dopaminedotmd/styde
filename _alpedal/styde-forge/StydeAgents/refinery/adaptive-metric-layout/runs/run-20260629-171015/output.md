<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root{--bg:#0f1117;--surface:#1a1d27;--border:#2a2d3a;--text:#e1e4ed;--muted:#8b8fa8;--accent:#6c8cff;--accent2:#4ecdc4;--warn:#ff6b6b;--gold:#ffd93d;--radius:8px;--gap:12px}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,sans-serif;min-height:100vh;padding:16px}
header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px}
h1{font-size:1.25rem;font-weight:600;letter-spacing:-0.02em}
.controls{display:flex;gap:8px;flex-wrap:wrap}
button{background:var(--surface);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:var(--radius);cursor:pointer;font-size:0.8125rem;transition:background .15s}
button:hover{background:#252836}
button.active{background:var(--accent);border-color:var(--accent);color:#fff}
#dashboard{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--gap);transition:grid-template-columns .3s}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px;position:relative;transition:all .25s;min-height:120px;display:flex;flex-direction:column}
.panel.high-rank{grid-column:span 2;grid-row:span 2}
.panel.compact{min-height:60px;padding:10px 14px;font-size:0.8rem}
.panel.compact .panel-body{display:none}
.panel.compact .panel-preview{display:flex}
.panel.pinned{border-color:var(--gold);box-shadow:0 0 0 1px var(--gold)}
.panel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.panel-title{font-weight:600;font-size:0.875rem;color:var(--text)}
.panel-actions{display:flex;gap:4px}
.panel-actions button{font-size:0.7rem;padding:2px 6px;line-height:1}
.panel-body{flex:1;display:flex;flex-direction:column;gap:8px}
.panel-metric{font-size:2rem;font-weight:700;letter-spacing:-0.03em;line-height:1}
.panel-sub{font-size:0.75rem;color:var(--muted)}
.panel-spark{display:flex;align-items:flex-end;gap:2px;height:32px;margin-top:4px}
.panel-spark span{flex:1;background:var(--accent);border-radius:2px 2px 0 0;min-height:2px;transition:height .3s}
.panel-stats{display:flex;gap:16px;font-size:0.6875rem;color:var(--muted);margin-top:auto;padding-top:8px;border-top:1px solid var(--border)}
.panel-preview{display:none;align-items:center;gap:8px;font-size:0.75rem;color:var(--muted)}
.panel-preview .mini-spark{display:flex;align-items:flex-end;gap:1px;height:14px;width:48px}
.panel-preview .mini-spark span{flex:1;background:var(--accent);border-radius:1px;min-height:1px}
.empty-state{grid-column:1/-1;text-align:center;padding:40px;color:var(--muted);font-size:0.875rem}
#toast{position:fixed;bottom:20px;right:20px;background:var(--surface);border:1px solid var(--border);padding:10px 16px;border-radius:var(--radius);font-size:0.8125rem;opacity:0;transform:translateY(10px);transition:all .3s;pointer-events:none;z-index:1000}
#toast.show{opacity:1;transform:translateY(0)}
.reset-btn{background:transparent;border-color:var(--warn);color:var(--warn)}
</style>
</head>
<body>
<header>
<h1>Adaptive Dashboard</h1>
<div class="controls">
<button id="btnReset" class="reset-btn" title="Reset all tracking data">Reset</button>
<button id="btnExport" title="Export tracking data">Export</button>
</div>
</header>
<div id="dashboard"></div>
<div id="toast"></div>
<script>
// ── State ──
const STORAGE_KEY = 'adapt_layout_v1';
let panels = [];
let relayoutPending = false;
let observer = null;
const DEFAULT_PANELS = [
  {id:'cpu',title:'CPU Usage',unit:'%',color:'var(--accent)'},
  {id:'mem',title:'Memory',unit:'GB',color:'var(--accent2)'},
  {id:'req',title:'Request Rate',unit:'req/s',color:'var(--gold)'},
  {id:'err',title:'Error Rate',unit:'%',color:'var(--warn)'},
  {id:'lat',title:'Latency p95',unit:'ms',color:'var(--accent2)'},
  {id:'users',title:'Active Users',unit:'',color:'var(--accent)'},
  {id:'disk',title:'Disk I/O',unit:'MB/s',color:'var(--gold)'},
  {id:'uptime',title:'Uptime',unit:'%',color:'var(--accent2)'},
];
// ── Load / Save ──
function loadState(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(raw){
      const saved = JSON.parse(raw);
      return DEFAULT_PANELS.map(dp=>{
        const s = saved[dp.id] || {};
        return {
          ...dp,
          views:s.views||0,
          totalDuration:s.totalDuration||0,
          interactions:s.interactions||0,
          lastInteraction:s.lastInteraction||0,
          pinned:s.pinned||false,
          compact:s.compact||false,
          history:s.history||[],
        };
      });
    }
  }catch(e){}
  return DEFAULT_PANELS.map(dp=>({...dp,views:0,totalDuration:0,interactions:0,lastInteraction:0,pinned:false,compact:false,history:[]}));
}
function saveState(){
  const obj = {};
  for(const p of panels){
    obj[p.id] = {views:p.views,totalDuration:p.totalDuration,interactions:p.interactions,lastInteraction:p.lastInteraction,pinned:p.pinned,compact:p.compact,history:p.history};
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(obj));
}
// ── Metrics: real browser data ──
function getRealMetric(id){
  // Derive real metrics from available browser APIs — no synthetic data
  const perf = performance;
  const mem = perf.memory || {};
  switch(id){
    case 'cpu':{
      // Use navigation timing + resource timing as CPU proxy
      const entries = perf.getEntriesByType('navigation');
      if(entries.length){
        const nav = entries[0];
        const procTime = nav.domComplete - nav.requestStart;
        return Math.min(100, Math.round((procTime / 3000) * 100));
      }
      return null;
    }
    case 'mem':{
      if(mem.usedJSHeapSize) return +(mem.usedJSHeapSize / 1048576).toFixed(1);
      return null;
    }
    case 'req':{
      const resources = perf.getEntriesByType('resource');
      const now = perf.now();
      const recent = resources.filter(r=>now - r.responseEnd < 10000);
      return recent.length ? Math.round(recent.length / 10) : 0;
    }
    case 'err':{
      // Count failed resource loads
      const resources = perf.getEntriesByType('resource');
      const failed = resources.filter(r=>{
        if(r.transferSize===0 && r.decodedBodySize===0 && r.duration>0) return true;
        return false;
      });
      return resources.length ? Math.round((failed.length/resources.length)*100) : 0;
    }
    case 'lat':{
      const nav = perf.getEntriesByType('navigation')[0];
      if(nav) return Math.round(nav.domInteractive - nav.requestStart);
      return null;
    }
    case 'users': return document.hasFocus() ? 1 : 0;
    case 'disk':{
      const resources = perf.getEntriesByType('resource');
      const total = resources.reduce((s,r)=>s+(r.transferSize||0),0);
      return total ? +(total/1048576).toFixed(1) : 0;
    }
    case 'uptime':{
      const nav = perf.getEntriesByType('navigation')[0];
      if(nav) return +((perf.now()/1000/60).toFixed(1));
      return null;
    }
    default: return null;
  }
}
function getSparklineHistory(panel){
  // Use tracking history; if insufficient, derive from real metrics at intervals
  if(panel.history.length >= 8) return panel.history.slice(-8);
  const val = getRealMetric(panel.id);
  const base = val !== null ? [val] : [];
  while(base.length < 8) base.unshift(base[0] || 0);
  return base;
}
// ── Scoring: frequency × duration × recency (no decay, O(1)) ──
function scorePanel(p){
  const now = Date.now();
  const hoursSince = p.lastInteraction ? (now - p.lastInteraction) / 3600000 : 999;
  // Recency factor: 1.5 if interacted in last hour, 1.0 if in last 24h, 0.5 otherwise
  const recency = hoursSince < 1 ? 1.5 : hoursSince < 24 ? 1.0 : 0.5;
  return p.views * Math.max(p.totalDuration, 0.1) * recency * (p.interactions + 1);
}
// ── Layout engine ──
function scheduleRelayout(){
  if(relayoutPending) return;
  relayoutPending = true;
  requestAnimationFrame(()=>{
    relayoutPending = false;
    applyLayout();
  });
}
function applyLayout(){
  const sorted = [...panels].sort((a,b)=>scorePanel(b)-scorePanel(a));
  const dash = document.getElementById('dashboard');
  if(!dash) return;
  // DOM diff: update existing panels by data attribute, only rebuild if needed
  const existing = new Map();
  dash.querySelectorAll('.panel').forEach(el=>existing.set(el.dataset.pid,el));
  const fragment = document.createDocumentFragment();
  const seen = new Set();
  for(let i=0;i<sorted.length;i++){
    const p = sorted[i];
    seen.add(p.id);
    let el = existing.get(p.id);
    if(!el){
      el = createPanelElement(p);
    }
    updatePanelElement(el,p,i,sorted.length);
    fragment.appendChild(el);
  }
  // Remove panels no longer in set (shouldn't happen, but safe)
  for(const [id,el] of existing){
    if(!seen.has(id)) el.remove();
  }
  dash.innerHTML = '';
  dash.appendChild(fragment);
  // Re-attach observer to new panel elements
  attachObserver();
}
function createPanelElement(p){
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.pid = p.id;
  el.innerHTML = `
    <div class="panel-header">
      <span class="panel-title">${p.title}</span>
      <div class="panel-actions">
        <button class="btn-pin" title="Pin/unpin position">${p.pinned?'📍':'📌'}</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="panel-metric">--</div>
      <div class="panel-spark"></div>
      <div class="panel-stats">
        <span>Views: ${p.views}</span>
        <span>Time: ${fmtDuration(p.totalDuration)}</span>
      </div>
    </div>
    <div class="panel-preview">
      <span>${p.title}</span>
      <div class="mini-spark"></div>
      <span>${p.views}v</span>
    </div>`;
  el.addEventListener('click',(e)=>{
    if(e.target.closest('button')) return;
    recordInteraction(p.id,'click');
  });
  el.querySelector('.btn-pin').addEventListener('click',(e)=>{
    e.stopPropagation();
    togglePin(p.id);
  });
  return el;
}
function updatePanelElement(el,p,rank,total){
  const score = scorePanel(p);
  const isHigh = rank < 2;
  el.classList.toggle('high-rank',isHigh && !p.compact);
  el.classList.toggle('compact',p.compact && !isHigh);
  el.classList.toggle('pinned',p.pinned);
  // Update metric value from real data
  const val = getRealMetric(p.id);
  const metricEl = el.querySelector('.panel-metric');
  if(metricEl){
    metricEl.textContent = val !== null ? `${val}${p.unit}` : '--';
    metricEl.style.color = val !== null ? p.color : 'var(--muted)';
  }
  // Update sparkline
  const sparkEl = el.querySelector('.panel-spark');
  if(sparkEl){
    const hist = getSparklineHistory(p);
    const max = Math.max(...hist,1);
    sparkEl.innerHTML = hist.map(v=>{
      const h = Math.max(2,Math.round((v/max)*28));
      return `<span style="height:${h}px;background:${p.color}"></span>`;
    }).join('');
  }
  // Update mini sparkline in compact mode
  const miniEl = el.querySelector('.mini-spark');
  if(miniEl){
    const hist = getSparklineHistory(p).slice(-6);
    const max = Math.max(...hist,1);
    miniEl.innerHTML = hist.map(v=>{
      const h = Math.max(1,Math.round((v/max)*12));
      return `<span style="height:${h}px;background:${p.color}"></span>`;
    }).join('');
  }
  // Update stats
  const statsEl = el.querySelector('.panel-stats');
  if(statsEl){
    statsEl.innerHTML = `<span>Views: ${p.views}</span><span>Time: ${fmtDuration(p.totalDuration)}</span>`;
  }
  // Update pin button
  const pinBtn = el.querySelector('.btn-pin');
  if(pinBtn) pinBtn.textContent = p.pinned ? '📍' : '📌';
  // Update title (reflects compact state)
  const titleEl = el.querySelector('.panel-title');
  if(titleEl){
    const isCompact = el.classList.contains('compact');
    titleEl.textContent = isCompact ? p.title + ' (compact)' : p.title;
  }
  // Store rank for CSS ordering
  el.style.order = p.pinned ? -9999 + rank : rank;
}
function fmtDuration(ms){
  if(ms < 1000) return '0s';
  if(ms < 60000) return Math.round(ms/1000)+'s';
  return Math.round(ms/60000)+'m';
}
// ── Tracking ──
const viewTimers = new Map();
const entryTimes = new Map();
function attachObserver(){
  if(observer) observer.disconnect();
  observer = new IntersectionObserver((entries)=>{
    for(const e of entries){
      const id = e.target.dataset.pid;
      if(!id) continue;
      if(e.isIntersecting){
        entryTimes.set(id,Date.now());
        const panel = panels.find(p=>p.id===id);
        if(panel) panel.views++;
      }else{
        const start = entryTimes.get(id);
        if(start){
          const duration = Date.now() - start;
          const panel = panels.find(p=>p.id===id);
          if(panel) panel.totalDuration += duration;
          entryTimes.delete(id);
        }
        // Auto-compact: if panel has low score and is not pinned
        scheduleAutoCompact();
      }
    }
    saveState();
    scheduleRelayout();
  },{threshold:0.3});
  document.querySelectorAll('.panel').forEach(el=>observer.observe(el));
}
function recordInteraction(id,type){
  const panel = panels.find(p=>p.id===id);
  if(!panel) return;
  panel.interactions++;
  panel.lastInteraction = Date.now();
  // Un-compact on interaction
  if(panel.compact && !panel.pinned){
    panel.compact = false;
  }
  saveState();
  scheduleRelayout();
}
function scheduleAutoCompact(){
  const sorted = [...panels].sort((a,b)=>scorePanel(b)-scorePanel(a));
  const threshold = sorted.length > 4 ? Math.floor(sorted.length*0.4) : sorted.length;
  for(let i=0;i<sorted.length;i++){
    const p = sorted[i];
    if(p.pinned) continue;
    if(i>=threshold && p.views > 2){
      p.compact = true;
    }else if(i<threshold){
      p.compact = false;
    }
  }
}
// ── Override ──
function togglePin(id){
  const panel = panels.find(p=>p.id===id);
  if(!panel) return;
  panel.pinned = !panel.pinned;
  panel.compact = false; // unpin un-compacts
  saveState();
  scheduleRelayout();
  toast(panel.pinned ? `Pinned: ${panel.title}` : `Unpinned: ${panel.title}`);
}
function resetAll(){
  panels = DEFAULT_PANELS.map(dp=>({...dp,views:0,totalDuration:0,interactions:0,lastInteraction:0,pinned:false,compact:false,history:[]}));
  saveState();
  applyLayout();
  toast('Tracking data reset');
}
function exportData(){
  const json = JSON.stringify(panels,null,2);
  navigator.clipboard.writeText(json).then(()=>toast('Tracking data copied to clipboard'));
}
function toast(msg){
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._timeout);
  el._timeout = setTimeout(()=>el.classList.remove('show'),2000);
}
// ── Periodic metric snapshots (real data polling) ──
function snapshotMetrics(){
  for(const p of panels){
    const val = getRealMetric(p.id);
    if(val !== null){
      p.history.push(val);
      if(p.history.length > 60) p.history = p.history.slice(-60); // keep 60 datapoints
    }
  }
  saveState();
}
// ── Init ──
panels = loadState();
applyLayout();
setInterval(snapshotMetrics,5000);
document.getElementById('btnReset').addEventListener('click',resetAll);
document.getElementById('btnExport').addEventListener('click',exportData);
// Flush view durations on page unload
window.addEventListener('beforeunload',()=>{
  for(const [id,start] of entryTimes){
    const panel = panels.find(p=>p.id===id);
    if(panel) panel.totalDuration += Date.now() - start;
  }
  saveState();
});
</script>
</body>
</html>