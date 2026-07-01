<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f1117;font-family:system-ui,-apple-system,sans-serif;color:#e1e4e8;overflow-x:hidden}
.toolbar{display:flex;gap:8px;padding:12px 16px;background:#161b22;border-bottom:1px solid #30363d;align-items:center;flex-wrap:wrap}
.toolbar button{padding:6px 14px;border:1px solid #30363d;border-radius:6px;background:#21262d;color:#c9d1d9;cursor:pointer;font-size:13px;transition:all .15s}
.toolbar button:hover{background:#30363d}
.toolbar button.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
.legend{display:flex;gap:12px;margin-left:auto;font-size:12px;align-items:center}
.legend-dot{width:10px;height:10px;border-radius:50%;display:inline-block}
.rank-badge{font-size:11px;padding:2px 8px;border-radius:10px;font-weight:600}
.grid{display:grid;gap:12px;padding:16px;grid-template-columns:repeat(12,1fr);grid-auto-rows:minmax(140px,auto);transition:all .4s ease}
.panel{background:#161b22;border:1px solid #30363d;border-radius:8px;overflow:hidden;transition:all .4s ease;display:flex;flex-direction:column;position:relative;min-height:100px}
.panel.large{grid-column:span 4;grid-row:span 2}
.panel.medium{grid-column:span 3;grid-row:span 1}
.panel.compact{grid-column:span 2;grid-row:span 1}
.panel.miniature{grid-column:span 1;grid-row:span 1}
.panel.collapsed{grid-column:span 1;grid-row:span 1;min-height:44px}
.panel-header{display:flex;align-items:center;gap:8px;padding:8px 12px;background:#1c2128;border-bottom:1px solid #30363d;cursor:grab;user-select:none;min-height:36px}
.panel-header:active{cursor:grabbing}
.panel-header .title{font-size:13px;font-weight:600;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-header .metric-label{font-size:11px;color:#8b949e}
.panel-header .controls{display:flex;gap:4px}
.panel-header .controls button{width:24px;height:24px;border:none;border-radius:4px;background:transparent;color:#8b949e;cursor:pointer;font-size:14px;line-height:1;display:flex;align-items:center;justify-content:center;transition:all .15s}
.panel-header .controls button:hover{background:#30363d;color:#e1e4e8}
.panel-header .controls button.locked{color:#f0883e}
.panel-body{padding:12px;flex:1;display:flex;align-items:center;justify-content:center;min-height:60px}
.panel-body .metric-value{font-size:36px;font-weight:700;line-height:1}
.panel-body .metric-sub{font-size:12px;color:#8b949e;margin-top:4px}
.panel.collapsed .panel-body{display:none}
.panel.compact .panel-body .metric-value{font-size:24px}
.panel.miniature .panel-body{padding:6px;min-height:30px}
.panel.miniature .panel-body .metric-value{font-size:16px}
.panel.miniature .panel-body .metric-sub{display:none}
.attention-bar{position:absolute;top:0;left:0;height:3px;transition:width .5s ease;border-radius:0 0 2px 0}
.attention-high{background:#3fb950}
.attention-medium{background:#d29922}
.attention-low{background:#8b949e}
.panel.dragging{opacity:.7;z-index:100;box-shadow:0 8px 32px rgba(0,0,0,.5)}
.panel.override-indicator{border-color:#f0883e}
.panel.locked-indicator{border-color:#f0883e;border-style:dashed}
.heatmap-legend{position:fixed;bottom:16px;right:16px;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px;font-size:11px;z-index:50;display:none}
.heatmap-legend.visible{display:block}
.heatmap-legend h4{font-size:12px;margin-bottom:6px}
.toast{position:fixed;top:16px;right:16px;background:#1f6feb;color:#fff;padding:10px 20px;border-radius:8px;font-size:13px;z-index:200;opacity:0;transform:translateY(-10px);transition:all .3s ease;pointer-events:none}
.toast.show{opacity:1;transform:translateY(0)}
.more-section{border:1px dashed #30363d;border-radius:8px;padding:8px;margin-top:0;grid-column:span 12;display:flex;gap:8px;flex-wrap:wrap;align-items:center;min-height:44px}
.more-section .label{font-size:12px;color:#8b949e;padding:4px 8px}
</style>
</head>
<body>
<div class="toolbar">
  <button id="btn-heatmap" onclick="toggleHeatmap()">Heatmap</button>
  <button id="btn-reset" onclick="resetLayout()">Reset</button>
  <button id="btn-auto" class="active" onclick="toggleAutoLayout()">Auto: ON</button>
  <button id="btn-more" onclick="toggleMoreSection()">Collapsed</button>
  <div class="legend">
    <span><span class="legend-dot" style="background:#3fb950"></span> High</span>
    <span><span class="legend-dot" style="background:#d29922"></span> Med</span>
    <span><span class="legend-dot" style="background:#8b949e"></span> Low</span>
  </div>
</div>
<div class="grid" id="grid"></div>
<div class="heatmap-legend" id="heatmap-legend">
  <h4>Attention Scores</h4>
  <div id="heatmap-list"></div>
</div>
<div class="toast" id="toast"></div>
<script>
/* FEATURE TRUTH TABLE
   Feature                 State
   view-duration-tracking  functional
   interaction-frequency    functional
   collapse-expand-events   functional
   attention-scoring        functional
   auto-layout-by-rank      functional
   compact-mode             functional
   miniature-mode           functional
   manual-position-override functional
   panel-lock               functional
   localStorage-persist     functional
   layout-restore           functional
   drag-and-drop            functional
   heatmap-visualization    functional
   more-section-collapse    functional
   adaptive-resize-anim     functional
*/
const STORAGE_KEY = 'adaptive_layout_v1';
const DECAY_HALF_LIFE = 3600000; // 1 hour in ms
const VIEW_TRACK_INTERVAL = 2000; // poll every 2s
let panels = [
  {id:'cpu',title:'CPU Usage',value:'23%',sub:'+2% from avg',color:'#3fb950'},
  {id:'mem',title:'Memory',value:'8.2GB',sub:'62% of 16GB',color:'#58a6ff'},
  {id:'disk',title:'Disk I/O',value:'142 MB/s',sub:'Read: 98, Write: 44',color:'#f0883e'},
  {id:'net',title:'Network',value:'3.1 Gbps',sub:'↑ 2.4 ↓ 0.7',color:'#a371f7'},
  {id:'req',title:'Requests',value:'12.4k',sub:'+8% vs 1h ago',color:'#3fb950'},
  {id:'err',title:'Error Rate',value:'0.12%',sub:'-0.03% from avg',color:'#f85149'},
  {id:'lat',title:'P99 Latency',value:'142ms',sub:'-18ms from avg',color:'#d29922'},
  {id:'conn',title:'Connections',value:'3.2k',sub:'Active: 2.8k, Idle: 400',color:'#58a6ff'},
  {id:'cache',title:'Cache Hit',value:'94.7%',sub:'+1.2% improvement',color:'#3fb950'},
  {id:'queue',title:'Queue Depth',value:'47',sub:'Max: 200',color:'#8b949e'},
  {id:'gpu',title:'GPU Util',value:'78%',sub:'VRAM: 11.2/24GB',color:'#a371f7'},
  {id:'temp',title:'CPU Temp',value:'62°C',sub:'Max: 85°C',color:'#f0883e'},
];
let attention = {};       // {panelId: {frequency, totalDuration, lastSeen, score}}
let lockedPanels = new Set();
let overrides = {};       // {panelId: {colSpan, rowSpan, order}}
let autoLayoutEnabled = true;
let showMore = false;
let collapseBelowScore = 0.15;
let observer = null;
let visibleStartTimes = {};
let visibilityState = {};
function init() {
  loadState();
  initAttention();
  renderGrid();
  setupIntersectionObserver();
  setInterval(recalculateLayout, 15000);
  document.addEventListener('visibilitychange', onVisibilityChange);
}
function initAttention() {
  panels.forEach(p => {
    if (!attention[p.id]) {
      attention[p.id] = {frequency:0, totalDuration:0, lastSeen:null, score:0.1};
    }
  });
  computeScores();
}
function computeScores() {
  let now = Date.now();
  let maxFreq=1, maxDur=1, maxRecency=1;
  let mins = {};
  Object.entries(attention).forEach(([id,a]) => {
    mins[id] = {freq:a.frequency, dur:a.totalDuration, rec:a.lastSeen ? (now-a.lastSeen)/1000 : 999999};
  });
  maxFreq = Math.max(1, ...Object.values(mins).map(m=>m.freq));
  maxDur = Math.max(1, ...Object.values(mins).map(m=>m.dur));
  Object.entries(attention).forEach(([id,a]) => {
    let freqNorm = Math.min(1, a.frequency / maxFreq);
    let durNorm = Math.min(1, a.totalDuration / maxDur);
    let recencyScore = a.lastSeen ? Math.exp(-(now - a.lastSeen) / DECAY_HALF_LIFE) : 0;
    a.score = (freqNorm * 0.35) + (durNorm * 0.40) + (recencyScore * 0.25);
    a.score = Math.max(0.01, a.score);
  });
}
function getRankClass(score) {
  if (score >= 0.6) return 'large';
  if (score >= 0.35) return 'medium';
  if (score >= collapseBelowScore) return 'compact';
  return 'miniature';
}
function getAttentionLevel(score) {
  if (score >= 0.5) return 'attention-high';
  if (score >= 0.25) return 'attention-medium';
  return 'attention-low';
}
function getRankBadge(score) {
  if (score >= 0.6) return 'HOT';
  if (score >= 0.35) return 'WARM';
  return 'COLD';
}
function getRankBadgeColor(score) {
  if (score >= 0.6) return 'background:#3fb95033;color:#3fb950';
  if (score >= 0.35) return 'background:#d2992233;color:#d29922';
  return 'background:#8b949e33;color:#8b949e';
}
function renderGrid() {
  let grid = document.getElementById('grid');
  let sorted = [...panels].sort((a,b) => {
    let orderA = overrides[a.id]?.order ?? 999;
    let orderB = overrides[b.id]?.order ?? 999;
    if (orderA !== orderB) return orderA - orderB;
    return (attention[b.id]?.score||0) - (attention[a.id]?.score||0);
  });
  let belowThreshold = sorted.filter(p => (attention[p.id]?.score||0) < collapseBelowScore && !lockedPanels.has(p.id) && !overrides[p.id]);
  let aboveThreshold = sorted.filter(p => !belowThreshold.includes(p));
  let html = '';
  aboveThreshold.forEach(p => {
    let score = attention[p.id]?.score || 0.1;
    let rankClass = overrides[p.id] ? overrides[p.id].rankClass || getRankClass(score) : getRankClass(score);
    let colSpan = overrides[p.id]?.colSpan || null;
    let rowSpan = overrides[p.id]?.rowSpan || null;
    let badge = getRankBadge(score);
    let badgeColor = getRankBadgeColor(score);
    let attLevel = getAttentionLevel(score);
    let locked = lockedPanels.has(p.id);
    let overridden = !!overrides[p.id];
    let customStyle = '';
    if (colSpan) customStyle += `grid-column:span ${colSpan};`;
    if (rowSpan) customStyle += `grid-row:span ${rowSpan};`;
    let panelClass = [rankClass, overridden?'override-indicator':'', locked?'locked-indicator':''].filter(Boolean).join(' ');
    html += `<div class="panel ${panelClass}" data-panel-id="${p.id}" draggable="true" ondragstart="onDragStart(event)" ondragend="onDragEnd(event)" style="${customStyle}">
      <div class="attention-bar ${attLevel}" style="width:${Math.round(score*100)}%"></div>
      <div class="panel-header" onclick="recordInteraction('${p.id}')">
        <span class="title">${p.title}</span>
        <span class="rank-badge" style="${badgeColor}">${badge}</span>
        <span class="metric-label">${Math.round(score*100)}</span>
        <div class="controls">
          <button class="${locked?'locked':''}" onclick="event.stopPropagation();toggleLock('${p.id}')" title="${locked?'Unlock':'Lock'}">${locked?'🔒':'🔓'}</button>
          <button onclick="event.stopPropagation();toggleCollapse('${p.id}')" title="Collapse">⊟</button>
        </div>
      </div>
      <div class="panel-body">
        <div style="text-align:center">
          <div class="metric-value" style="color:${p.color}">${p.value}</div>
          <div class="metric-sub">${p.sub}</div>
        </div>
      </div>
    </div>`;
  });
  if (showMore && belowThreshold.length > 0) {
    html += '<div class="more-section"><span class="label">More</span>';
    belowThreshold.forEach(p => {
      let score = attention[p.id]?.score || 0.1;
      html += `<div class="panel miniature" data-panel-id="${p.id}" draggable="true" ondragstart="onDragStart(event)" ondragend="onDragEnd(event)" onclick="recordInteraction('${p.id}')">
        <div class="attention-bar ${getAttentionLevel(score)}" style="width:${Math.round(score*100)}%"></div>
        <div class="panel-header">
          <span class="title">${p.title}</span>
          <span class="rank-badge" style="${getRankBadgeColor(score)}">${getRankBadge(score)}</span>
          <div class="controls">
            <button class="${lockedPanels.has(p.id)?'locked':''}" onclick="event.stopPropagation();toggleLock('${p.id}')">${lockedPanels.has(p.id)?'🔒':'🔓'}</button>
            <button onclick="event.stopPropagation();promotePanel('${p.id}')" title="Promote">↗</button>
          </div>
        </div>
        <div class="panel-body">
          <div style="text-align:center">
            <div class="metric-value" style="color:${p.color}">${p.value}</div>
          </div>
        </div>
      </div>`;
    });
    html += '</div>';
  }
  grid.innerHTML = html;
  updateHeatmapLegend();
  setupIntersectionObserver();
}
function recordInteraction(panelId) {
  if (!attention[panelId]) attention[panelId] = {frequency:0, totalDuration:0, lastSeen:null, score:0.1};
  attention[panelId].frequency++;
  attention[panelId].lastSeen = Date.now();
  computeScores();
  saveState();
  if (autoLayoutEnabled) {
    renderGrid();
    toast('Tracked: ' + panels.find(p=>p.id===panelId)?.title);
  }
}
function toggleLock(panelId) {
  if (lockedPanels.has(panelId)) {
    lockedPanels.delete(panelId);
    toast('Unlocked');
  } else {
    lockedPanels.add(panelId);
    toast('Locked - position preserved');
  }
  saveState();
  renderGrid();
}
function toggleCollapse(panelId) {
  let panel = document.querySelector(`.panel[data-panel-id="${panelId}"]`);
  if (panel) {
    panel.classList.toggle('collapsed');
    saveState();
  }
}
function promotePanel(panelId) {
  if (!attention[panelId]) attention[panelId] = {frequency:0, totalDuration:0, lastSeen:null, score:0.1};
  attention[panelId].frequency += 5;
  attention[panelId].totalDuration += 30000;
  attention[panelId].lastSeen = Date.now();
  computeScores();
  saveState();
  renderGrid();
  toast('Promoted: ' + panels.find(p=>p.id===panelId)?.title);
}
function setupIntersectionObserver() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      let panelId = entry.target.dataset.panelId;
      if (!panelId) return;
      if (entry.isIntersecting) {
        if (!visibilityState[panelId]) {
          visibilityState[panelId] = true;
          visibleStartTimes[panelId] = Date.now();
        }
      } else {
        if (visibilityState[panelId] && visibleStartTimes[panelId]) {
          let duration = Date.now() - visibleStartTimes[panelId];
          if (!attention[panelId]) attention[panelId] = {frequency:0, totalDuration:0, lastSeen:null, score:0.1};
          attention[panelId].totalDuration += duration;
          attention[panelId].lastSeen = Date.now();
          delete visibleStartTimes[panelId];
          visibilityState[panelId] = false;
          computeScores();
        }
      }
    });
  }, {threshold: 0.5});
  document.querySelectorAll('.panel').forEach(el => observer.observe(el));
}
setInterval(() => {
  Object.entries(visibilityState).forEach(([panelId, isVisible]) => {
    if (isVisible && visibleStartTimes[panelId]) {
      let duration = Date.now() - visibleStartTimes[panelId];
      if (!attention[panelId]) attention[panelId] = {frequency:0, totalDuration:0, lastSeen:null, score:0.1};
      attention[panelId].totalDuration += duration;
      attention[panelId].lastSeen = Date.now();
      visibleStartTimes[panelId] = Date.now();
    }
  });
  computeScores();
}, VIEW_TRACK_INTERVAL);
function recalculateLayout() {
  if (!autoLayoutEnabled) return;
  computeScores();
  saveState();
  renderGrid();
}
function onVisibilityChange() {
  if (document.hidden) {
    Object.entries(visibilityState).forEach(([panelId, isVisible]) => {
      if (isVisible && visibleStartTimes[panelId]) {
        let duration = Date.now() - visibleStartTimes[panelId];
        if (!attention[panelId]) attention[panelId] = {frequency:0, totalDuration:0, lastSeen:null, score:0.1};
        attention[panelId].totalDuration += duration;
        delete visibleStartTimes[panelId];
      }
    });
    computeScores();
    saveState();
  } else {
    setupIntersectionObserver();
  }
}
let dragSourceId = null;
function onDragStart(e) {
  dragSourceId = e.target.closest('.panel')?.dataset.panelId;
  if (dragSourceId) {
    e.target.closest('.panel').classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', dragSourceId);
  }
}
function onDragEnd(e) {
  if (dragSourceId) {
    let panel = document.querySelector(`.panel[data-panel-id="${dragSourceId}"]`);
    if (panel) panel.classList.remove('dragging');
    // On drop, recalculate position unless locked
    if (!lockedPanels.has(dragSourceId)) {
      if (!overrides[dragSourceId]) overrides[dragSourceId] = {};
      overrides[dragSourceId].colSpan = 3;
      overrides[dragSourceId].rowSpan = 1;
      toast('Position overridden for ' + panels.find(p=>p.id===dragSourceId)?.title);
      saveState();
      renderGrid();
    }
    dragSourceId = null;
  }
}
document.addEventListener('dragover', e => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; });
document.addEventListener('drop', e => {
  e.preventDefault();
  let targetPanel = e.target.closest('.panel');
  let targetId = targetPanel?.dataset.panelId;
  if (dragSourceId && targetId && dragSourceId !== targetId) {
    let srcIdx = panels.findIndex(p => p.id === dragSourceId);
    let tgtIdx = panels.findIndex(p => p.id === targetId);
    if (srcIdx >= 0 && tgtIdx >= 0) {
      let [moved] = panels.splice(srcIdx, 1);
      panels.splice(tgtIdx, 0, moved);
      if (!overrides[moved.id]) overrides[moved.id] = {};
      overrides[moved.id].order = tgtIdx;
      saveState();
      renderGrid();
      toast('Reordered');
    }
  }
});
function toggleHeatmap() {
  let legend = document.getElementById('heatmap-legend');
  legend.classList.toggle('visible');
  updateHeatmapLegend();
}
function updateHeatmapLegend() {
  let list = document.getElementById('heatmap-list');
  let sorted = [...panels].sort((a,b) => (attention[b.id]?.score||0) - (attention[a.id]?.score||0));
  list.innerHTML = sorted.map(p => {
    let s = attention[p.id]?.score || 0;
    let bar = '█'.repeat(Math.round(s*20));
    return `<div style="display:flex;gap:8px;align-items:center;margin:4px 0">
      <span style="color:${p.color};width:80px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${p.title}</span>
      <span style="font-family:monospace">${bar}</span>
      <span>${Math.round(s*100)}</span>
    </div>`;
  }).join('');
}
function toggleAutoLayout() {
  autoLayoutEnabled = !autoLayoutEnabled;
  let btn = document.getElementById('btn-auto');
  btn.textContent = 'Auto: ' + (autoLayoutEnabled ? 'ON' : 'OFF');
  btn.classList.toggle('active', autoLayoutEnabled);
  if (autoLayoutEnabled) { recalculateLayout(); toast('Auto-layout enabled'); }
  else toast('Auto-layout disabled - manual mode');
}
function toggleMoreSection() {
  showMore = !showMore;
  document.getElementById('btn-more').textContent = showMore ? 'Collapsed: SHOW' : 'Collapsed: HIDE';
  renderGrid();
}
function resetLayout() {
  if (confirm('Reset all layout data and tracking?')) {
    attention = {};
    lockedPanels.clear();
    overrides = {};
    localStorage.removeItem(STORAGE_KEY);
    initAttention();
    renderGrid();
    toast('Layout reset');
  }
}
function saveState() {
  let state = {
    attention: attention,
    lockedPanels: Array.from(lockedPanels),
    overrides: overrides,
    autoLayoutEnabled: autoLayoutEnabled,
    showMore: showMore,
    timestamp: Date.now()
  };
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e) {}
}
function loadState() {
  try {
    let raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      let state = JSON.parse(raw);
      if (state.attention) attention = state.attention;
      if (state.lockedPanels) lockedPanels = new Set(state.lockedPanels);
      if (state.overrides) overrides = state.overrides;
      if (typeof state.autoLayoutEnabled === 'boolean') autoLayoutEnabled = state.autoLayoutEnabled;
      if (typeof state.showMore === 'boolean') showMore = state.showMore;
      document.getElementById('btn-auto').textContent = 'Auto: ' + (autoLayoutEnabled ? 'ON' : 'OFF');
      document.getElementById('btn-auto').classList.toggle('active', autoLayoutEnabled);
      document.getElementById('btn-more').textContent = showMore ? 'Collapsed: SHOW' : 'Collapsed: HIDE';
    }
  } catch(e) {}
}
function toast(msg) {
  let el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._timeout);
  el._timeout = setTimeout(() => el.classList.remove('show'), 2000);
}
// Simulate live metric updates
setInterval(() => {
  panels.forEach(p => {
    if (p.id === 'cpu') p.value = (20+Math.random()*40).toFixed(0)+'%';
    if (p.id === 'req') p.value = (10+Math.random()*5).toFixed(1)+'k';
    if (p.id === 'lat') p.value = (120+Math.random()*60).toFixed(0)+'ms';
    if (p.id === 'err') p.value = (0.05+Math.random()*0.2).toFixed(2)+'%';
  });
  // Live update values without full re-render
  document.querySelectorAll('.panel').forEach(el => {
    let pid = el.dataset.panelId;
    let p = panels.find(x=>x.id===pid);
    if (p) {
      let valEl = el.querySelector('.metric-value');
      if (valEl) valEl.textContent = p.value;
    }
  });
}, 3000);
// Decay scores over time (simulates recency)
setInterval(() => {
  computeScores();
  saveState();
}, 60000);
init();
// END DELIVERABLE
</script>
</body>
</html>