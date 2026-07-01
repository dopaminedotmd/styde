```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--panel-bg:#1a1d27;--panel-border:#2a2d3a;
  --text:#e4e6ef;--muted:#7a7f93;--accent:#6c5ce7;--accent-hover:#7c6ef7;
  --compact-h:#120px;--min-h:80px;--gap:12px;--radius:10px;
  --transition:0.35s cubic-bezier(0.4,0,0.2,1)
}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);padding:20px;min-height:100vh}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px}
.header h1{font-size:22px;font-weight:600;letter-spacing:-0.3px}
.header-controls{display:flex;gap:8px;align-items:center}
.btn{background:var(--panel-bg);border:1px solid var(--panel-border);color:var(--text);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:13px;transition:background var(--transition),border-color var(--transition)}
.btn:hover{background:var(--panel-border);border-color:var(--accent)}
.btn.active{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.danger{color:#ff6b6b}
.badge{font-size:11px;background:var(--accent);color:#fff;padding:2px 8px;border-radius:10px;margin-left:6px}
.dashboard-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--gap);transition:grid-template-columns var(--transition)}
.panel{
  background:var(--panel-bg);border:1px solid var(--panel-border);border-radius:var(--radius);
  padding:16px;min-height:var(--min-h);transition:all var(--transition);
  position:relative;overflow:hidden;display:flex;flex-direction:column
}
.panel:hover{border-color:var(--accent)}
.panel.locked{outline:2px solid var(--accent);outline-offset:-2px}
.panel.compact{min-height:var(--compact-h);max-height:var(--compact-h);overflow:hidden;cursor:pointer}
.panel.compact .panel-body{max-height:40px;overflow:hidden;opacity:0.6}
.panel.compact .panel-chart{display:none}
.panel.miniature{min-height:60px;max-height:60px;padding:8px 12px}
.panel.miniature .panel-title{font-size:12px}
.panel.miniature .panel-body,.panel.miniature .panel-chart,.panel.miniature .panel-stats{display:none}
.panel-title{font-size:14px;font-weight:500;color:var(--muted);margin-bottom:6px;display:flex;justify-content:space-between;align-items:center}
.panel-title .panel-actions{display:flex;gap:4px;opacity:0;transition:opacity var(--transition)}
.panel:hover .panel-actions{opacity:1}
.panel-actions button{background:none;border:none;color:var(--muted);cursor:pointer;font-size:13px;padding:2px 4px;border-radius:4px;transition:color var(--transition),background var(--transition)}
.panel-actions button:hover{color:var(--text);background:rgba(255,255,255,0.06)}
.panel-actions button.lock-btn.active{color:var(--accent)}
.panel-value{font-size:28px;font-weight:700;letter-spacing:-0.5px;line-height:1.2}
.panel-label{font-size:12px;color:var(--muted);margin-top:2px}
.panel-stats{display:flex;gap:12px;margin-top:8px;font-size:11px;color:var(--muted)}
.panel-stats span{display:flex;align-items:center;gap:3px}
.chart-bar{height:4px;background:var(--accent);border-radius:2px;margin-top:8px;transition:width var(--transition)}
.rank-badge{position:absolute;top:8px;right:8px;font-size:10px;background:rgba(108,92,231,0.2);color:var(--accent);padding:2px 6px;border-radius:4px}
.heatmap-overlay{position:fixed;bottom:20px;right:20px;background:var(--panel-bg);border:1px solid var(--panel-border);border-radius:var(--radius);padding:12px 16px;font-size:12px;z-index:100;max-width:220px;opacity:0.9}
.heatmap-overlay .h-title{font-weight:500;margin-bottom:4px}
.heatmap-overlay .h-bar{display:flex;align-items:center;gap:6px;margin:2px 0}
.heatmap-overlay .h-bar-fill{height:4px;background:var(--accent);border-radius:2px;transition:width var(--transition)}
.heatmap-overlay .h-bar-label{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:80px}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Metric Layout <span class="badge">learning</span></h1>
  <div class="header-controls">
    <button class="btn" onclick="toggleHeatmap()">heatmap</button>
    <button class="btn" onclick="resetLayout()">reset</button>
    <button class="btn active" onclick="toggleAutoArrange()" id="autoBtn">auto</button>
  </div>
</div>
<div class="dashboard-grid" id="dashboard"></div>
<div id="heatmapOverlay" class="heatmap-overlay" style="display:none">
  <div class="h-title">attention heatmap</div>
  <div id="heatmapBars"></div>
</div>
<script>
// ===== CONFIG =====
const PANEL_DEFS = [
  {id:'revenue',title:'Revenue',value:'$284.5k',label:'+12.3% vs last month',chart:85},
  {id:'users',title:'Active Users',value:'12,847',label:'+8.1% vs last week',chart:72},
  {id:'conversion',title:'Conversion Rate',value:'3.42%',label:'+0.18pp',chart:58},
  {id:'bounce',title:'Bounce Rate',value:'28.1%',label:'-2.4pp',chart:34},
  {id:'sessions',title:'Sessions',value:'48,203',label:'+5.7%',chart:90},
  {id:'avg_time',title:'Avg. Session',value:'4m 32s',label:'+22s',chart:65},
  {id:'retention',title:'Retention (D7)',value:'41.3%',label:'+1.8pp',chart:48},
  {id:'pageviews',title:'Page Views',value:'142,887',label:'+9.2%',chart:78},
  {id:'errors',title:'Error Rate',value:'0.21%',label:'-0.04pp',chart:15}
];
const STORE_KEY = 'aml_layout';
// ===== STATE =====
let state = {
  panels: PANEL_DEFS.map(p => ({
    ...p,
    frequency: 0,
    totalDuration: 0,
    lastViewed: 0,
    viewCount: 0,
    locked: false,
    position: null,
    compact: false,
    miniature: false
  })),
  autoArrange: true,
  heatmapVisible: false,
  viewStart: null,
  currentView: null
};
// ===== TRACKING =====
function trackOpen(panelId) {
  const p = state.panels.find(x => x.id === panelId);
  if(!p) return;
  p.viewCount++;
  p.lastViewed = Date.now();
  p.frequency = p.viewCount / (1 + (Date.now() - p.lastViewed) / 60000);
  state.currentView = panelId;
  state.viewStart = Date.now();
  saveState();
}
function trackClose(panelId) {
  if(!state.viewStart || !panelId) return;
  const dur = Date.now() - state.viewStart;
  const p = state.panels.find(x => x.id === panelId);
  if(p) {
    p.totalDuration += dur;
    p.frequency = (p.viewCount * 1000) / (1 + p.totalDuration / 60000);
  }
  state.viewStart = null;
  state.currentView = null;
  saveState();
  if(state.autoArrange) arrangePanels();
}
// ===== RANKING =====
function computeScore(p) {
  if(p.locked) return 100 + (p.position !== null ? p.position * 10 : 0);
  const freq = p.frequency || 0.01;
  const dur = p.totalDuration || 0;
  const recency = Math.max(0, 1 - (Date.now() - p.lastViewed) / (7 * 86400000));
  return freq * 0.4 + (dur / 60000) * 0.35 + recency * 0.25;
}
function rankPanels() {
  const scored = state.panels.map(p => ({...p, score: computeScore(p)}));
  scored.sort((a,b) => b.score - a.score);
  return scored;
}
// ===== LAYOUT ARRANGEMENT =====
function arrangePanels() {
  if(!state.autoArrange) return;
  const ranked = rankPanels();
  const grid = document.getElementById('dashboard');
  const children = Array.from(grid.children);
  ranked.forEach((p, idx) => {
    const el = children.find(c => c.dataset.panelId === p.id);
    if(!el) return;
    if(p.locked) return;
    const total = ranked.length;
    const pos = idx;
    el.dataset.rank = pos;
    if(pos < Math.ceil(total * 0.3)) {
      el.classList.remove('compact','miniature');
      el.style.gridColumn = pos < 2 ? 'span 2' : 'span 1';
      el.style.gridRow = 'span 1';
    } else if(pos < Math.ceil(total * 0.6)) {
      el.classList.add('compact');
      el.classList.remove('miniature');
      el.style.gridColumn = 'span 1';
      el.style.gridRow = 'span 1';
    } else {
      el.classList.remove('compact');
      el.classList.add('miniature');
      el.style.gridColumn = 'span 1';
      el.style.gridRow = 'span 1';
    }
  });
}
// ===== RENDER =====
function renderPanel(p) {
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.panelId = p.id;
  if(p.locked) el.classList.add('locked');
  el.innerHTML = `
    <div class="panel-title">
      ${p.title}
      <div class="panel-actions">
        <button class="lock-btn ${p.locked?'active':''}" onclick="toggleLock('${p.id}')" title="lock position">&#128274;</button>
        <button onclick="compactToggle('${p.id}')" title="toggle compact">&#9632;</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="panel-value">${p.value}</div>
      <div class="panel-label">${p.label}</div>
      <div class="panel-stats">
        <span>&#128200; ${p.chart}%</span>
        <span>&#128065; ${p.viewCount} views</span>
      </div>
      <div class="chart-bar" style="width:${p.chart}%"></div>
    </div>
    <div class="rank-badge">#</div>
  `;
  el.addEventListener('mouseenter', () => { trackOpen(p.id); });
  el.addEventListener('mouseleave', () => { trackClose(p.id); });
  return el;
}
function renderDashboard() {
  const grid = document.getElementById('dashboard');
  grid.innerHTML = '';
  state.panels.forEach(p => {
    grid.appendChild(renderPanel(p));
  });
  arrangePanels();
}
// ===== ACTIONS =====
function toggleLock(panelId) {
  const p = state.panels.find(x => x.id === panelId);
  if(!p) return;
  p.locked = !p.locked;
  const el = document.querySelector(`[data-panel-id="${panelId}"]`);
  if(el) el.classList.toggle('locked');
  saveState();
  if(state.autoArrange) arrangePanels();
  updateHeatmap();
}
function compactToggle(panelId) {
  const p = state.panels.find(x => x.id === panelId);
  const el = document.querySelector(`[data-panel-id="${panelId}"]`);
  if(!p || !el) return;
  if(el.classList.contains('miniature')) {
    el.classList.remove('miniature');
    p.miniature = false;
  } else if(el.classList.contains('compact')) {
    el.classList.remove('compact');
    p.compact = false;
  } else {
    el.classList.add('compact');
    p.compact = true;
  }
  saveState();
}
function toggleHeatmap() {
  state.heatmapVisible = !state.heatmapVisible;
  const overlay = document.getElementById('heatmapOverlay');
  overlay.style.display = state.heatmapVisible ? 'block' : 'none';
  if(state.heatmapVisible) updateHeatmap();
}
function updateHeatmap() {
  const bars = document.getElementById('heatmapBars');
  const ranked = rankPanels();
  const maxScore = ranked.length > 0 ? ranked[0].score : 1;
  bars.innerHTML = ranked.map((p,i) => {
    const w = Math.max(5, (p.score / maxScore) * 100);
    const lockIcon = p.locked ? ' &#128274;' : '';
    return `<div class="h-bar"><span class="h-bar-label">${i+1}. ${p.title}${lockIcon}</span><div class="h-bar-fill" style="width:${w}%"></div><span>${p.score.toFixed(1)}</span></div>`;
  }).join('');
}
function toggleAutoArrange() {
  state.autoArrange = !state.autoArrange;
  document.getElementById('autoBtn').classList.toggle('active');
  if(state.autoArrange) arrangePanels();
  saveState();
}
function resetLayout() {
  localStorage.removeItem(STORE_KEY);
  state.panels.forEach(p => {
    p.frequency = 0;
    p.totalDuration = 0;
    p.lastViewed = 0;
    p.viewCount = 0;
    p.locked = false;
    p.position = null;
    p.compact = false;
    p.miniature = false;
  });
  renderDashboard();
  updateHeatmap();
}
// ===== PERSISTENCE =====
function saveState() {
  try {
    const data = state.panels.map(p => ({
      id: p.id, frequency: p.frequency, totalDuration: p.totalDuration,
      lastViewed: p.lastViewed, viewCount: p.viewCount, locked: p.locked,
      position: p.position, compact: p.compact, miniature: p.miniature
    }));
    localStorage.setItem(STORE_KEY, JSON.stringify(data));
  } catch(e) {}
}
function loadState() {
  try {
    const raw = localStorage.getItem(STORE_KEY);
    if(!raw) return;
    const data = JSON.parse(raw);
    data.forEach(d => {
      const p = state.panels.find(x => x.id === d.id);
      if(p) Object.assign(p, d);
    });
  } catch(e) {}
}
// ===== INIT =====
loadState();
renderDashboard();
if(state.heatmapVisible) { document.getElementById('heatmapOverlay').style.display = 'block'; updateHeatmap(); }
// periodic persist + re-rank
setInterval(() => { saveState(); if(state.autoArrange) arrangePanels(); if(state.heatmapVisible) updateHeatmap(); }, 15000);
// window unload guard
window.addEventListener('beforeunload', () => { if(state.currentView) trackClose(state.currentView); });
console.log('Adaptive Metric Layout initialized');
console.log('Panels:', state.panels.length, '| Auto-arrange:', state.autoArrange);
</script>
</body>
</html>
```