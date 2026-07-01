```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0d1117;--surface:#161b22;--border:#30363d;--text:#e6edf3;--text-dim:#8b949e;--accent:#58a6ff;--accent2:#3fb950;--accent3:#d29922;--danger:#f85149;--radius:8px;--compact-w:280px;--compact-h:120px}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px}
.header{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:8px}
.header h1{font-size:20px;font-weight:600;color:var(--text)}
.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.controls select,.controls button{background:var(--surface);border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:var(--radius);font-size:13px;cursor:pointer}
.controls select:hover,.controls button:hover{border-color:var(--accent)}
.controls button.active{background:var(--accent);color:#000;border-color:var(--accent);font-weight:600}
.stats-bar{display:flex;gap:16px;margin-bottom:16px;flex-wrap:wrap;font-size:12px;color:var(--text-dim)}
.stat-item{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:6px 12px}
.stat-item span{color:var(--accent);font-weight:600}
.dashboard-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px;transition:all .4s cubic-bezier(.4,0,.2,1)}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all .4s cubic-bezier(.4,0,.2,1);position:relative;display:flex;flex-direction:column}
.panel.compact{max-width:var(--compact-w);max-height:var(--compact-h)}
.panel.compact .panel-body{display:none}
.panel.compact .panel-preview{display:flex}
.panel.compact .panel-header .panel-title{font-size:12px}
.panel.miniature{max-width:140px;max-height:60px}
.panel.miniature .panel-header{padding:4px 8px}
.panel.miniature .panel-title{font-size:10px}
.panel.miniature .panel-body,.panel.miniature .panel-preview{display:none}
.panel.locked{border-color:var(--accent3);box-shadow:0 0 0 1px var(--accent3)}
.panel.dragging{opacity:.7;transform:scale(1.02)}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:10px 12px;border-bottom:1px solid var(--border);cursor:grab;user-select:none;min-height:40px}
.panel-header:active{cursor:grabbing}
.panel-title{font-size:14px;font-weight:500;display:flex;align-items:center;gap:6px}
.panel-title .rank-badge{font-size:10px;background:var(--accent);color:#000;border-radius:99px;padding:1px 6px;font-weight:700}
.panel-actions{display:flex;gap:4px;align-items:center}
.panel-actions button{background:none;border:none;color:var(--text-dim);cursor:pointer;padding:2px 4px;font-size:12px;border-radius:4px;line-height:1}
.panel-actions button:hover{color:var(--text);background:var(--border)}
.panel-actions button.lock-btn.active{color:var(--accent3)}
.panel-body{padding:12px;flex:1;min-height:80px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:300}
.panel-preview{display:none;padding:8px 12px;align-items:center;gap:8px;font-size:11px;color:var(--text-dim);min-height:40px}
.panel-preview .preview-value{font-size:18px;font-weight:600;color:var(--accent)}
.panel-footer{display:flex;justify-content:space-between;padding:6px 12px;border-top:1px solid var(--border);font-size:10px;color:var(--text-dim)}
.panel-footer .usage-bar{display:flex;gap:8px;align-items:center}
.usage-bar .bar-track{width:60px;height:4px;background:var(--border);border-radius:2px;overflow:hidden}
.usage-bar .bar-fill{height:100%;border-radius:2px;transition:width .6s ease}
.panel[data-rank="1"] .usage-bar .bar-fill{background:var(--accent2)}
.panel[data-rank="2"] .usage-bar .bar-fill{background:var(--accent)}
.panel[data-rank="3"] .usage-bar .bar-fill{background:var(--accent3)}
.panel[data-rank="4"] .usage-bar .bar-fill{background:#f0883e}
.panel[data-rank="5"] .usage-bar .bar-fill{background:#da3633}
.more-section{margin-top:12px;border-top:1px solid var(--border);padding-top:12px}
.more-toggle{background:var(--surface);border:1px solid var(--border);color:var(--text-dim);padding:8px 16px;border-radius:var(--radius);font-size:13px;cursor:pointer;width:100%;text-align:center}
.more-toggle:hover{border-color:var(--accent);color:var(--text)}
.more-grid{display:none;grid-template-columns:repeat(auto-fill,minmax(var(--compact-w),1fr));gap:12px;margin-top:12px}
.more-grid.open{display:grid}
.reset-btn{background:var(--danger);color:#fff;border:none;padding:6px 12px;border-radius:var(--radius);font-size:12px;cursor:pointer}
.reset-btn:hover{opacity:.85}
@media(max-width:640px){
  .dashboard-grid{grid-template-columns:1fr}
  .panel.compact{max-width:100%}
  .panel.miniature{max-width:100%}
}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Metric Layout</h1>
  <div class="controls">
    <select id="view-select">
      <option value="auto">Auto-layout</option>
      <option value="manual">Manual override</option>
      <option value="locked">Locked only</option>
    </select>
    <button id="reset-btn" class="reset-btn">Reset data</button>
    <span style="font-size:12px;color:var(--text-dim);margin-left:4px" id="session-badge">session active</span>
  </div>
</div>
<div class="stats-bar">
  <div class="stat-item">panels: <span id="stat-panels">0</span></div>
  <div class="stat-item">tracked events: <span id="stat-events">0</span></div>
  <div class="stat-item">top panel: <span id="stat-top">—</span></div>
  <div class="stat-item">mode: <span id="stat-mode">auto</span></div>
</div>
<div id="dashboard" class="dashboard-grid"></div>
<div class="more-section">
  <button class="more-toggle" id="more-toggle">Show more panels (+<span id="more-count">0</span>)</button>
  <div class="more-grid" id="more-grid"></div>
</div>
<script>
// ============== DATA MODEL ==============
const PANEL_DEFS = [
  {id:'revenue',title:'Revenue',icon:'$',unit:'$',value:284750,color:'#3fb950'},
  {id:'users',title:'Active Users',icon:'U',unit:'',value:18423,color:'#58a6ff'},
  {id:'conversion',title:'Conversion Rate',icon:'%',unit:'%',value:3.42,color:'#d29922'},
  {id:'churn',title:'Churn Rate',icon:'⬇',unit:'%',value:1.87,color:'#f0883e'},
  {id:'sessions',title:'Sessions',icon:'S',unit:'',value:94210,color:'#58a6ff'},
  {id:'arpu',title:'ARPU',icon:'A',unit:'$',value:15.22,color:'#3fb950'},
  {id:'ltv',title:'LTV',icon:'L',unit:'$',value:342.10,color:'#3fb950'},
  {id:'retention',title:'Retention D7',icon:'R',unit:'%',value:68.5,color:'#d29922'},
  {id:'pageviews',title:'Page Views',icon:'P',unit:'',value:487120,color:'#58a6ff'},
  {id:'bounce',title:'Bounce Rate',icon:'↗',unit:'%',value:34.2,color:'#da3633'},
  {id:'nps',title:'NPS Score',icon:'N',unit:'',value:72,color:'#3fb950'},
  {id:'loadtime',title:'Load Time',icon:'⏱',unit:'ms',value:234,color:'#f0883e'},
];
const STORAGE_KEY = 'adaptive_metric_layout_v1';
// ============== TRACKING ==============
let usageData = {};
let modCount = 0;
let sessionStart = Date.now();
function initUsage() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if(saved){
    try{
      const parsed = JSON.parse(saved);
      if(parsed.usage) usageData = parsed.usage;
      return;
    }catch(e){}
  }
  PANEL_DEFS.forEach(p => {
    usageData[p.id] = {
      frequency: Math.floor(Math.random()*20)+1,
      duration: Math.floor(Math.random()*60000)+5000,
      lastViewed: Date.now() - Math.floor(Math.random()*86400000),
      locked: false,
      position: null,
      collapsed: false,
      expandedCount: Math.floor(Math.random()*5),
      collapsedCount: Math.floor(Math.random()*3),
    };
  });
}
function saveState(){
  const toStore = {usage:usageData, version:1, saved:Date.now()};
  localStorage.setItem(STORAGE_KEY, JSON.stringify(toStore));
}
function trackEvent(panelId, type){
  const d = usageData[panelId];
  if(!d) return;
  if(type === 'view'){ d.frequency += 1; d.duration += 2000; d.lastViewed = Date.now(); }
  else if(type === 'expand'){ d.expandedCount = (d.expandedCount||0)+1; }
  else if(type === 'collapse'){ d.collapsedCount = (d.collapsedCount||0)+1; d.collapsed = true; }
  else if(type === 'hover'){ d.frequency += 0.2; d.duration += 500; }
  modCount++;
  saveState();
  updateStats();
  if(modCount % 5 === 0) renderDashboard();
}
function resetData(){
  if(!confirm('Reset all usage data and layout preferences?')) return;
  localStorage.removeItem(STORAGE_KEY);
  usageData = {};
  initUsage();
  modCount = 0;
  saveState();
  renderDashboard();
}
// ============== RANKING ==============
function computeScore(d){
  const now = Date.now();
  const recencyHours = (now - d.lastViewed) / 3600000;
  const recencyScore = Math.max(0, 100 - recencyHours);
  const freqScore = Math.min(100, d.frequency * 5);
  const durScore = Math.min(100, d.duration / 600);
  return (freqScore * 0.4) + (durScore * 0.3) + (recencyScore * 0.3);
}
function getRankedPanels(){
  return PANEL_DEFS.map(p => {
    const u = usageData[p.id];
    const score = u ? computeScore(u) : 0;
    return {...p, usage:u, score};
  }).sort((a,b) => b.score - a.score);
}
// ============== LAYOUT ENGINE ==============
function computeLayout(){
  const ranked = getRankedPanels();
  const viewMode = document.getElementById('view-select').value;
  const gridPanels = [];
  const morePanels = [];
  let lockedCount = ranked.filter(p => p.usage && p.usage.locked).length;
  let autoOrder = viewMode === 'locked' ? ranked.filter(p => p.usage && p.usage.locked) : ranked;
  if(viewMode === 'manual'){
    autoOrder.sort((a,b) => {
      const pa = a.usage?.position;
      const pb = b.usage?.position;
      if(pa !== null && pa !== undefined && pb !== null && pb !== undefined) return pa - pb;
      if(pa !== null && pa !== undefined) return -1;
      if(pb !== null && pb !== undefined) return 1;
      return b.score - a.score;
    });
  }
  autoOrder.forEach((p, i) => {
    const locked = p.usage && p.usage.locked;
    const posOverride = p.usage && p.usage.position !== null && p.usage.position !== undefined;
    let rank = i + 1;
    let sizeClass = '';
    if(locked && viewMode !== 'locked'){
      sizeClass = 'normal';
    } else if(rank <= 3){
      sizeClass = 'normal';
    } else if(rank <= 6){
      sizeClass = 'compact';
    } else {
      sizeClass = 'miniature';
    }
    p._rank = rank;
    p._sizeClass = sizeClass;
    if(viewMode === 'auto' && !locked && rank > 6){
      morePanels.push(p);
    } else if(viewMode === 'locked' && !locked){
      morePanels.push(p);
    } else {
      gridPanels.push(p);
    }
  });
  return {gridPanels, morePanels, viewMode};
}
// ============== RENDER ==============
function renderDashboard(){
  const {gridPanels, morePanels, viewMode} = computeLayout();
  const grid = document.getElementById('dashboard');
  const moreGrid = document.getElementById('more-grid');
  const moreCount = document.getElementById('more-count');
  grid.innerHTML = '';
  moreGrid.innerHTML = '';
  moreCount.textContent = morePanels.length;
  gridPanels.forEach(p => renderPanel(grid, p, false));
  morePanels.forEach(p => renderPanel(moreGrid, p, true));
  document.getElementById('stat-panels').textContent = PANEL_DEFS.length;
  document.getElementById('stat-events').textContent = modCount;
  document.getElementById('stat-top').textContent = gridPanels[0] ? gridPanels[0].title : '—';
  document.getElementById('stat-mode').textContent = viewMode;
}
function renderPanel(container, p, isMore){
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.panelId = p.id;
  el.dataset.rank = p._rank;
  if(p._sizeClass === 'compact') el.classList.add('compact');
  else if(p._sizeClass === 'miniature') el.classList.add('miniature');
  if(p.usage && p.usage.locked) el.classList.add('locked');
  const usagePct = p.usage ? Math.min(100, Math.round(computeScore(p.usage))) : 0;
  const compactPreview = p._sizeClass === 'compact' && !isMore;
  el.innerHTML = `
    <div class="panel-header">
      <div class="panel-title">
        <span>${p.icon}</span>
        <span>${p.title}</span>
        <span class="rank-badge">#${p._rank}</span>
      </div>
      <div class="panel-actions">
        <button class="lock-btn ${p.usage?.locked?'active':''}" title="Lock panel position">🔒</button>
        <button class="collapse-btn" title="Collapse">—</button>
        <button class="remove-btn" title="Send to more">×</button>
      </div>
    </div>
    <div class="panel-body">
      <span style="font-size:28px;color:${p.color}">${p.icon}</span>
      <span style="font-size:32px;font-weight:700;margin-left:8px">${formatValue(p.value, p.unit)}</span>
    </div>
    ${compactPreview ? `
    <div class="panel-preview">
      <span class="preview-value">${formatValue(p.value, p.unit)}</span>
      <span>${p.title} — rank #${p._rank}</span>
    </div>` : ''}
    <div class="panel-footer">
      <div class="usage-bar">
        <span>${usagePct}%</span>
        <div class="bar-track"><div class="bar-fill" style="width:${usagePct}%"></div></div>
      </div>
      <span>${p.usage ? Math.round(p.usage.frequency) : 0} views · ${p.usage ? humanTime(p.usage.duration) : '0s'}</span>
    </div>
  `;
  // Event tracking for view (IntersectionObserver)
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if(e.isIntersecting){
        trackEvent(p.id, 'view');
        obs.unobserve(e.target);
      }
    });
  }, {threshold:0.3});
  obs.observe(el);
  // Hover
  let hoverTimer;
  el.addEventListener('mouseenter', () => {
    hoverTimer = setTimeout(() => trackEvent(p.id, 'hover'), 2000);
  });
  el.addEventListener('mouseleave', () => clearTimeout(hoverTimer));
  // Lock button
  el.querySelector('.lock-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    const u = usageData[p.id];
    u.locked = !u.locked;
    if(!u.locked) u.position = null;
    trackEvent(p.id, 'expand');
    renderDashboard();
  });
  // Collapse button
  el.querySelector('.collapse-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    if(el.classList.contains('compact')){
      el.classList.remove('compact');
      trackEvent(p.id, 'expand');
    } else {
      el.classList.add('compact');
      trackEvent(p.id, 'collapse');
    }
  });
  // Remove to more
  el.querySelector('.remove-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    const u = usageData[p.id];
    u.position = 999;
    trackEvent(p.id, 'collapse');
    renderDashboard();
  });
  // Drag-to-reorder (simple)
  el.draggable = true;
  el.addEventListener('dragstart', (e) => {
    e.dataTransfer.setData('text/plain', p.id);
    el.classList.add('dragging');
  });
  el.addEventListener('dragend', () => el.classList.remove('dragging'));
  el.addEventListener('dragover', (e) => e.preventDefault());
  el.addEventListener('drop', (e) => {
    e.preventDefault();
    const fromId = e.dataTransfer.getData('text/plain');
    const toId = p.id;
    if(fromId && toId && fromId !== toId){
      const fromU = usageData[fromId];
      const toU = usageData[toId];
      const tempPos = toU.position ?? PANEL_DEFS.findIndex(x=>x.id===toId);
      toU.position = fromU.position ?? PANEL_DEFS.findIndex(x=>x.id===fromId);
      fromU.position = tempPos;
      fromU.locked = true;
      toU.locked = true;
      saveState();
      renderDashboard();
    }
  });
  container.appendChild(el);
}
function formatValue(val, unit){
  if(val >= 1000000) return (val/1000000).toFixed(1)+'M'+unit;
  if(val >= 1000) return (val/1000).toFixed(1)+'K'+unit;
  return val+unit;
}
function humanTime(ms){
  if(ms < 1000) return Math.round(ms)+'ms';
  if(ms < 60000) return Math.round(ms/1000)+'s';
  return Math.round(ms/60000)+'m';
}
function updateStats(){
  const top = getRankedPanels()[0];
  document.getElementById('stat-top').textContent = top ? top.title : '—';
}
// ============== SETUP ==============
initUsage();
renderDashboard();
document.getElementById('view-select').addEventListener('change', renderDashboard);
document.getElementById('reset-btn').addEventListener('click', resetData);
document.getElementById('more-toggle').addEventListener('click', () => {
  document.getElementById('more-grid').classList.toggle('open');
});
// Periodic auto-refresh (simulate usage decay + re-layout)
setInterval(() => {
  // Decay: slowly reduce frequency for non-active panels
  PANEL_DEFS.forEach(p => {
    const u = usageData[p.id];
    if(u && Date.now() - u.lastViewed > 300000){
      u.frequency = Math.max(0.5, u.frequency - 0.3);
    }
  });
  saveState();
  updateStats();
  renderDashboard();
}, 15000);
// Random simulated activity (background behavioral tracking demo)
setInterval(() => {
  const randPanel = PANEL_DEFS[Math.floor(Math.random() * PANEL_DEFS.length)];
  const eventType = ['view','hover','expand','collapse'][Math.floor(Math.random()*4)];
  trackEvent(randPanel.id, eventType);
}, 8000);
console.log('Adaptive Metric Layout initialized. Tracking events...');
</script>
</body>
</html>
```