`html
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
  --surface2: #22263a;
  --border: #2a2e3f;
  --text: #c8ccd4;
  --text2: #8890a4;
  --accent: #6c8cff;
  --accent2: #50c878;
  --danger: #ff6b6b;
  --warn: #ffb347;
  --radius: 8px;
  --gap: 10px;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; display: flex; }
#sidebar { width: 52px; background: var(--surface); border-right: 1px solid var(--border); display: flex; flex-direction: column; align-items: center; padding: 12px 0; gap: 8px; flex-shrink: 0; }
#sidebar .dot { width: 32px; height: 32px; border-radius: 50%; background: var(--surface2); display: flex; align-items: center; justify-content: center; font-size: 14px; cursor: pointer; transition: background .2s; border: 2px solid transparent; }
#sidebar .dot:hover { background: var(--border); }
#sidebar .dot.active { border-color: var(--accent); background: var(--surface2); }
#main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
#toolbar { display: flex; align-items: center; padding: 10px 16px; gap: 12px; border-bottom: 1px solid var(--border); flex-shrink: 0; background: var(--surface); }
#toolbar .title { font-weight: 600; font-size: 15px; margin-right: auto; }
#toolbar button { background: var(--surface2); border: 1px solid var(--border); color: var(--text); padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 13px; transition: all .15s; }
#toolbar button:hover { background: var(--border); }
#toolbar button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
#grid { flex: 1; overflow-y: auto; padding: var(--gap); display: grid; gap: var(--gap); grid-auto-flow: dense; }
.panel { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); display: flex; flex-direction: column; overflow: hidden; transition: box-shadow .25s, border-color .25s; position: relative; }
.panel:hover { border-color: #3a3f55; }
.panel.pinned { border-color: var(--accent); box-shadow: 0 0 12px rgba(108,140,255,0.15); }
.panel.compact .panel-body { max-height: 80px; overflow: hidden; }
.panel.compact .panel-body canvas { transform: scale(0.5); transform-origin: top left; }
.panel-header { display: flex; align-items: center; padding: 8px 10px; gap: 6px; border-bottom: 1px solid var(--border); flex-shrink: 0; cursor: move; user-select: none; font-size: 13px; font-weight: 500; background: var(--surface2); }
.panel-header .drag-handle { cursor: grab; color: var(--text2); margin-right: 4px; }
.panel-header .drag-handle:active { cursor: grabbing; }
.panel-header .title { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.panel-header .actions { display: flex; gap: 4px; }
.panel-header .actions button { background: none; border: none; color: var(--text2); cursor: pointer; padding: 2px 6px; font-size: 15px; border-radius: 4px; line-height: 1; }
.panel-header .actions button:hover { color: var(--text); background: var(--border); }
.panel-header .actions .pin-btn.pinned { color: var(--accent); }
.panel-body { flex: 1; padding: 12px; display: flex; align-items: center; justify-content: center; min-height: 60px; position: relative; overflow: hidden; }
.panel-body .metric-value { font-size: 28px; font-weight: 700; }
.panel-body .metric-label { font-size: 12px; color: var(--text2); }
.panel-body .sparkline { width: 100%; height: 60px; }
.panel-badge { position: absolute; top: 6px; right: 8px; font-size: 10px; background: var(--surface2); padding: 1px 6px; border-radius: 10px; color: var(--text2); }
.rank-1 .panel-badge { background: rgba(108,140,255,0.2); color: var(--accent); }
.rank-2 .panel-badge { background: rgba(80,200,120,0.2); color: var(--accent2); }
#toast { position: fixed; bottom: 20px; right: 20px; background: var(--surface2); border: 1px solid var(--border); padding: 10px 16px; border-radius: var(--radius); font-size: 13px; opacity: 0; transition: opacity .3s; pointer-events: none; z-index: 100; }
#toast.show { opacity: 1; }
.grid-4cols { grid-template-columns: repeat(4, 1fr); }
.grid-3cols { grid-template-columns: repeat(3, 1fr); }
.grid-2cols { grid-template-columns: repeat(2, 1fr); }
</style>
</head>
<body>
<div id="sidebar">
  <div class="dot active" data-grid="4" title="4 columns">4</div>
  <div class="dot" data-grid="3" title="3 columns">3</div>
  <div class="dot" data-grid="2" title="2 columns">2</div>
  <div class="dot" style="margin-top:auto;background:var(--danger);color:#fff;font-size:11px;" title="Reset layout" id="btn-reset">R</div>
</div>
<div id="main">
  <div id="toolbar">
    <span class="title">Adaptive Metric Layout</span>
    <button id="btn-lock-all">Lock All</button>
    <button id="btn-unlock-all">Unlock All</button>
    <button id="btn-reset-rank">Reset Tracking</button>
  </div>
  <div id="grid" class="grid-4cols"></div>
</div>
<div id="toast"></div>
<script>
(function(){
"use strict";
const STORAGE_KEY = 'adaptive_layout_v1';
const DEBOUNCE_MS = 100;
const VIEW_DURATION_INTERVAL = 2000;
const DECAY_ALPHA = 0.92;
const RANK_INTERVAL = 5000;
const MIN_VIEW_MS = 500;
let panels = [];
let gridCols = 4;
let rankDebounce = null;
let viewTimer = null;
let interactionBuffer = [];
const defaultPanels = [
  { id:'revenue', title:'Revenue', metric:'$128.4K', label:'+12.3% vs last month', color:'#6c8cff' },
  { id:'users', title:'Active Users', metric:'8,421', label:'+5.7% this week', color:'#50c878' },
  { id:'latency', title:'API Latency', metric:'43ms', label:'-8ms from baseline', color:'#ffb347' },
  { id:'errors', title:'Error Rate', metric:'0.12%', label:'Below 0.5% threshold', color:'#ff6b6b' },
  { id:'cpu', title:'CPU Usage', metric:'62%', label:'Avg across nodes', color:'#9b6cff' },
  { id:'memory', title:'Memory', metric:'14.2GB', label:'/ 32GB total', color:'#50b8c8' },
  { id:'requests', title:'Requests/s', metric:'3.2K', label:'Peak: 4.1K', color:'#c86cff' },
  { id:'uptime', title:'Uptime', metric:'99.97%', label:'Last 30 days', color:'#6cc8a0' },
  { id:'disk', title:'Disk I/O', metric:'210MB/s', label:'Read: 180, Write: 30', color:'#c8a06c' },
  { id:'cache', title:'Cache Hit Rate', metric:'94.8%', label:'Target: >90%', color:'#6ca0c8' },
  { id:'queue', title:'Queue Depth', metric:'17', label:'Avg wait: 2.3s', color:'#c86c8c' },
  { id:'cost', title:'Cloud Cost', metric:'$4.2K', label:'MTD, -3% forecast', color:'#8cc86c' }
];
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch(e) { return null; }
}
function saveState() {
  try {
    const data = {
      panels: panels.map(p => ({
        id: p.id,
        rank: p.rank,
        pinned: p.pinned,
        compact: p.compact,
        viewCount: p.viewCount,
        totalViewMs: p.totalViewMs,
        lastViewed: p.lastViewed,
        expandCount: p.expandCount,
        collapseCount: p.collapseCount,
        interactions: p.interactions
      })),
      gridCols,
      savedAt: Date.now()
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch(e) {}
}
function initPanels() {
  const saved = loadState();
  panels = defaultPanels.map((d,i) => {
    const savedP = saved && saved.panels ? saved.panels.find(sp => sp.id === d.id) : null;
    return {
      ...d,
      rank: savedP ? savedP.rank : 0,
      pinned: savedP ? savedP.pinned : false,
      compact: savedP ? savedP.compact : false,
      viewCount: savedP ? savedP.viewCount : 0,
      totalViewMs: savedP ? savedP.totalViewMs : 0,
      lastViewed: savedP ? savedP.lastViewed : 0,
      expandCount: savedP ? savedP.expandCount : 0,
      collapseCount: savedP ? savedP.collapseCount : 0,
      interactions: savedP ? savedP.interactions : 0,
      visible: false
    };
  });
  if (saved && saved.gridCols) gridCols = saved.gridCols;
}
function computeScore(p) {
  const now = Date.now();
  const hoursSince = Math.max(0, (now - p.lastViewed)) / 3600000;
  const recencyBoost = Math.exp(-hoursSince / 24);
  const freqScore = Math.log2(p.viewCount + 1);
  const durScore = Math.log2((p.totalViewMs / 1000) + 1);
  const interactionBonus = Math.log2(p.interactions + 1) * 0.3;
  const expandPenalty = p.collapseCount > p.expandCount ? -0.2 * (p.collapseCount - p.expandCount) : 0;
  let score = (freqScore * 0.4 + durScore * 0.35 + recencyBoost * 0.25 + interactionBonus + expandPenalty);
  score = Math.max(0.1, score);
  return score;
}
function rankPanels() {
  if (rankDebounce) clearTimeout(rankDebounce);
  rankDebounce = setTimeout(() => {
    const cw = document.getElementById('grid').clientWidth || 1200;
    const sizes = gridCols === 4 ? 4 : gridCols === 3 ? 3 : gridCols === 2 ? 2 : 4;
    panels.sort((a,b) => {
      if (a.pinned && !b.pinned) return -1;
      if (!a.pinned && b.pinned) return 1;
      const sa = computeScore(a);
      const sb = computeScore(b);
      return sb - sa;
    });
    panels.forEach((p,i) => {
      p.rank = i;
      p.compact = i >= sizes * 2 && !p.pinned && p.viewCount < 3;
    });
    renderGrid();
    saveState();
    rankDebounce = null;
  }, DEBOUNCE_MS);
}
let rafId = null;
function renderGrid() {
  if (rafId) cancelAnimationFrame(rafId);
  rafId = requestAnimationFrame(() => {
    const grid = document.getElementById('grid');
    const existing = {};
    grid.querySelectorAll('.panel').forEach(el => existing[el.dataset.pid] = el);
    panels.forEach((p,i) => {
      let el = existing[p.id];
      if (!el) {
        el = createPanelElement(p);
        existing[p.id] = el;
      }
      updatePanelElement(el, p, i);
      el.dataset.rank = i+1;
      if (p.compact) el.classList.add('compact'); else el.classList.remove('compact');
      if (p.pinned) el.classList.add('pinned'); else el.classList.remove('pinned');
      el.style.order = i;
      el.dataset.pid = p.id;
      const classListCache = el.classList;
      const needsCompact = p.compact && !classListCache.contains('compact');
      const needsPinned = p.pinned && !classListCache.contains('pinned');
      if (needsCompact) el.classList.add('compact');
      else if (!p.compact && classListCache.contains('compact')) el.classList.remove('compact');
      if (needsPinned) el.classList.add('pinned');
      else if (!p.pinned && classListCache.contains('pinned')) el.classList.remove('pinned');
    });
    const ordered = panels.map(p => existing[p.id]);
    ordered.forEach(el => grid.appendChild(el));
    rafId = null;
  });
}
function createPanelElement(p) {
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.pid = p.id;
  el.innerHTML = [
    '<div class="panel-header">',
      '<span class="drag-handle">&#9776;</span>',
      '<span class="title">'+esc(p.title)+'</span>',
      '<div class="actions">',
        '<button class="pin-btn" title="Toggle pin">&#128204;</button>',
        '<button class="compact-btn" title="Toggle compact">&#9660;</button>',
      '</div>',
    '</div>',
    '<div class="panel-body">',
      '<div style="text-align:center">',
        '<div class="metric-value" style="color:'+esc(p.color)+'">'+esc(p.metric)+'</div>',
        '<div class="metric-label">'+esc(p.label)+'</div>',
      '</div>',
    '</div>',
    '<div class="panel-badge">#'+(p.rank+1)+'</div>'
  ].join('');
  el.querySelector('.pin-btn').addEventListener('click', e => { e.stopPropagation(); togglePin(p.id); });
  el.querySelector('.compact-btn').addEventListener('click', e => { e.stopPropagation(); toggleCompact(p.id); });
  el.addEventListener('click', () => logInteraction(p.id, 'click'));
  el.addEventListener('mouseenter', () => logInteraction(p.id, 'hover'));
  return el;
}
function updatePanelElement(el, p, idx) {
  const rankBadge = el.querySelector('.panel-badge');
  if (rankBadge) rankBadge.textContent = '#'+(idx+1);
  const pinBtn = el.querySelector('.pin-btn');
  if (pinBtn) {
    if (p.pinned) pinBtn.classList.add('pinned');
    else pinBtn.classList.remove('pinned');
  }
  const compactBtn = el.querySelector('.compact-btn');
  if (compactBtn) compactBtn.textContent = p.compact ? '\u25B2' : '\u25BC';
}
function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function togglePin(id) {
  const p = panels.find(px => px.id === id);
  if (!p) return;
  p.pinned = !p.pinned;
  logInteraction(id, p.pinned ? 'pin' : 'unpin');
  rankPanels();
  toast(p.pinned ? 'Pinned: '+p.title : 'Unpinned: '+p.title);
}
function toggleCompact(id) {
  const p = panels.find(px => px.id === id);
  if (!p) return;
  p.compact = !p.compact;
  if (p.compact) p.collapseCount++; else p.expandCount++;
  logInteraction(id, p.compact ? 'collapse' : 'expand');
  rankPanels();
  toast(p.compact ? 'Compact: '+p.title : 'Expanded: '+p.title);
}
function logInteraction(id, type) {
  const p = panels.find(px => px.id === id);
  if (!p) return;
  interactionBuffer.push({ id, type, ts: Date.now() });
}
function flushInteractions() {
  if (!interactionBuffer.length) return;
  const now = Date.now();
  const deduped = {};
  interactionBuffer.forEach(ev => {
    const key = ev.id + ':' + ev.type;
    if (!deduped[key] || now - deduped[key].ts > 5000) {
      deduped[key] = ev;
    }
  });
  interactionBuffer = [];
  Object.values(deduped).forEach(ev => {
    const p = panels.find(px => px.id === ev.id);
    if (!p) return;
    p.interactions++;
    p.lastViewed = ev.ts;
    if (ev.type === 'click') p.viewCount++;
  });
  rankPanels();
}
setInterval(flushInteractions, 2000);
function trackVisiblePanels() {
  const grid = document.getElementById('grid');
  const gridRect = grid.getBoundingClientRect();
  panels.forEach(p => {
    const el = document.querySelector('.panel[data-pid="'+p.id+'"]');
    if (!el) { p.visible = false; return; }
    const r = el.getBoundingClientRect();
    const overlap = Math.max(0, Math.min(r.bottom, gridRect.bottom) - Math.max(r.top, gridRect.top));
    p.visible = overlap > 50;
  });
}
function accumulateViewDuration() {
  const now = Date.now();
  panels.forEach(p => {
    if (p.visible) {
      p.totalViewMs += VIEW_DURATION_INTERVAL;
      p.lastViewed = now;
    }
  });
  saveState();
}
function periodicDecay() {
  panels.forEach(p => {
    if (p.totalViewMs > 0) p.totalViewMs *= DECAY_ALPHA;
    if (p.interactions > 0) p.interactions *= DECAY_ALPHA;
    if (p.viewCount > 0) p.viewCount = Math.max(0, p.viewCount * DECAY_ALPHA);
    if (p.lastViewed > 0 && Date.now() - p.lastViewed > 86400000) {
      p.viewCount *= 0.9;
      p.totalViewMs *= 0.9;
    }
  });
  rankPanels();
  saveState();
}
function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._timeout);
  el._timeout = setTimeout(() => el.classList.remove('show'), 2000);
}
function setGridCols(n) {
  gridCols = n;
  const grid = document.getElementById('grid');
  grid.className = 'grid-'+n+'cols';
  document.querySelectorAll('#sidebar .dot').forEach(d => d.classList.remove('active'));
  const dot = document.querySelector('#sidebar .dot[data-grid="'+n+'"]');
  if (dot) dot.classList.add('active');
  rankPanels();
  saveState();
  toast(n+' column grid');
}
function lockAll() {
  panels.forEach(p => p.pinned = true);
  rankPanels();
  toast('All panels locked');
}
function unlockAll() {
  panels.forEach(p => p.pinned = false);
  rankPanels();
  toast('All panels unlocked');
}
function resetTracking() {
  panels.forEach(p => {
    p.viewCount = 0;
    p.totalViewMs = 0;
    p.lastViewed = 0;
    p.interactions = 0;
    p.expandCount = 0;
    p.collapseCount = 0;
    p.pinned = false;
    p.compact = false;
    p.rank = 0;
  });
  rankPanels();
  toast('Tracking data reset');
}
document.getElementById('btn-lock-all').addEventListener('click', lockAll);
document.getElementById('btn-unlock-all').addEventListener('click', unlockAll);
document.getElementById('btn-reset-rank').addEventListener('click', resetTracking);
document.getElementById('btn-reset').addEventListener('click', () => {
  localStorage.removeItem(STORAGE_KEY);
  location.reload();
});
document.querySelectorAll('#sidebar .dot[data-grid]').forEach(dot => {
  dot.addEventListener('click', () => setGridCols(parseInt(dot.dataset.grid)));
});
initPanels();
rankPanels();
setGridCols(gridCols);
viewTimer = setInterval(() => {
  trackVisiblePanels();
  accumulateViewDuration();
}, VIEW_DURATION_INTERVAL);
setInterval(periodicDecay, 60000);
})();
</script>
</body>
</html>
```