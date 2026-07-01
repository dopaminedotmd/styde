```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
/* --- reset & base --- */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--border:#2a2d3a;
  --text:#c8ccd4;--muted:#6b7080;--accent:#5b8def;
  --warn:#e0a040;--high:#4caf93;--compact-scale:0.45;
  --gap:10px;--radius:8px;--transition:0.35s cubic-bezier(0.25,0.8,0.25,1.2);
}
body{
  background:var(--bg);color:var(--text);
  font:14px/1.5 system-ui,-apple-system,sans-serif;
  min-height:100vh;padding:12px;
  /* mobile base: single column at 320px */
  min-width:320px;
}
/* --- toolbar --- */
.toolbar{
  display:flex;flex-wrap:wrap;gap:8px;align-items:center;
  margin-bottom:12px;padding:8px 0;
}
.toolbar button,.toolbar .stat{
  background:var(--surface);color:var(--text);
  border:1px solid var(--border);border-radius:6px;
  padding:6px 14px;font-size:13px;cursor:pointer;
  transition:background 0.2s;
  /* touch-friendly: min 44px */ min-height:44px;
  display:inline-flex;align-items:center;gap:6px;
}
.toolbar button:hover{background:#252836}
.toolbar .stat{background:transparent;border:none;color:var(--muted)}
/* --- grid --- */
.grid{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  grid-auto-rows:minmax(140px,auto);
  gap:var(--gap);
  transition:grid-template-columns var(--transition);
}
/* responsive breakpoints */
@media(max-width:768px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:480px){.grid{grid-template-columns:1fr}}
/* --- panel --- */
.panel{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);overflow:hidden;
  display:flex;flex-direction:column;
  transition:grid-column var(--transition),grid-row var(--transition),
             opacity var(--transition),transform var(--transition);
  cursor:grab;position:relative;
  min-width:0;/* prevent grid blowout */
}
.panel:active{cursor:grabbing}
.panel.dragging{opacity:0.55;transform:scale(0.97);z-index:10}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent)}
.panel.locked{border-left:3px solid var(--warn)}
.panel.compact{grid-row:span 1!important;grid-column:span 1!important}
.panel.compact .panel-body{display:none}
.panel.compact .panel-footer{display:none}
.panel.compact .compact-preview{display:flex}
/* --- panel header --- */
.panel-header{
  display:flex;align-items:center;gap:6px;
  padding:8px 10px;background:#1e2130;
  border-bottom:1px solid var(--border);
  /* touch-friendly drag handle */ min-height:44px;
}
.panel-title{
  flex:1;font-weight:600;font-size:13px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.panel-score{
  font-size:11px;color:var(--muted);
  background:#252836;border-radius:4px;padding:1px 6px;
}
.panel-header button{
  background:none;border:none;color:var(--muted);
  cursor:pointer;font-size:15px;padding:4px;line-height:1;
  min-width:32px;min-height:32px;/* touch target */
  border-radius:4px;transition:color 0.15s,background 0.15s;
}
.panel-header button:hover{color:var(--text);background:#2e3240}
.panel-header .btn-lock.active{color:var(--warn)}
/* --- panel body --- */
.panel-body{
  flex:1;padding:10px;overflow:auto;
  font-size:13px;color:var(--text);
}
/* compact preview (shown when compacted) */
.compact-preview{
  display:none;flex:1;align-items:center;justify-content:center;
  padding:6px;flex-direction:column;gap:4px;
}
.compact-preview .spark{
  width:100%;height:32px;background:#1e2130;
  border-radius:4px;overflow:hidden;
  /* placeholder sparkline — real impl would be canvas/svg */
  display:flex;align-items:flex-end;gap:1px;padding:2px;
}
.compact-preview .spark-bar{
  flex:1;background:var(--accent);border-radius:1px 1px 0 0;
  min-height:2px;opacity:0.7;
}
.compact-preview .metric-val{
  font-size:18px;font-weight:700;color:var(--high);
}
/* --- panel footer --- */
.panel-footer{
  display:flex;gap:8px;padding:6px 10px;
  border-top:1px solid var(--border);
  font-size:10px;color:var(--muted);
}
.panel-footer span{display:inline-flex;align-items:center;gap:3px}
/* attention heat indicator */
.heat-dot{
  width:8px;height:8px;border-radius:50%;display:inline-block;
  background:var(--muted);transition:background 0.3s;
}
.heat-dot.hot{background:var(--accent)}
.heat-dot.warm{background:var(--warn)}
/* --- drag placeholder --- */
.drag-placeholder{
  border:2px dashed var(--accent);border-radius:var(--radius);
  background:rgba(91,141,239,0.05);grid-row:span 1;grid-column:span 1;
}
/* reset button variant */
.btn-reset{color:var(--warn)!important;border-color:var(--warn)!important}
</style>
</head>
<body>
<div class="toolbar" id="toolbar">
  <button id="btn-auto" title="Toggle auto-layout">Auto: ON</button>
  <button id="btn-reset" class="btn-reset" title="Reset all tracking data">
    Reset
  </button>
  <span class="stat" id="stat-panels"></span>
  <span class="stat" id="stat-session"></span>
</div>
<div class="grid" id="grid"></div>
<script>
/* ============================================================
   Adaptive Metric Layout — v1
   Self-organizing dashboard with behavioral tracking.
   ============================================================ */
// --- constants ---
var COLS = 4;                  // grid columns
var COMPACT_THRESHOLD = 0.25;  // bottom 25% percentile → compact
var DECAY_HALF_LIFE = 86400000;// 24h in ms for recency decay
var SAVE_KEY = 'adaptive_dash_v1';
var RECALC_DEBOUNCE = 2000;    // ms between recalc batches
var DEFAULT_CONTENT =
  '<div style="display:flex;align-items:center;justify-content:center;'+
  'height:100%;color:var(--muted);font-size:24px;font-weight:200">'+
  '{value}</div>';
// --- sample panels (replace with real data) ---
var DEFAULT_PANELS = [
  {id:'cpu',title:'CPU Usage',content:cp,'val':42},
  {id:'mem',title:'Memory',content:cp,'val':67},
  {id:'disk',title:'Disk I/O',content:cp,'val':23},
  {id:'net',title:'Network',content:cp,'val':89},
  {id:'err',title:'Error Rate',content:cp,'val':3},
  {id:'lat',title:'P99 Latency',content:cp,'val':145},
  {id:'qps',title:'Queries/s',content:cp,'val':1205},
  {id:'cache',title:'Cache Hit %',content:cp,'val':94},
];
function cp(){return DEFAULT_CONTENT.replace('{value}',
  String(this.val||0))}
/* ============================================================
   STORE — single source of truth, mutated in place.
   ============================================================ */
var Store = {
  panels: [],       // array of panel objects
  autoLayout: true, // whether auto-layout is active
  recalcTimer: null,// debounce handle
  observer: null,   // IntersectionObserver instance
  visibilityMap: {},// {panelId: {enterTime, accumulated}}
};
/* ============================================================
   PANEL FACTORY — normalizes raw panel data.
   ============================================================ */
function createPanel(raw, idx) {
  var now = Date.now();
  return {
    id: raw.id || 'panel_' + idx,
    title: raw.title || 'Panel ' + idx,
    contentFn: raw.content || cp,   // function returning HTML string
    data: raw,                       // original data for contentFn context
    // tracking metrics
    viewDuration: 0,                 // cumulative ms visible
    interactions: 0,                // click/event count
    lastInteraction: now,           // timestamp
    firstSeen: now,                 // timestamp
    // layout state
    locked: false,
    compacted: false,
    gridArea: null,                 // computed by layout engine
    rank: 0,
    score: 0,
    // DOM ref (set after render)
    el: null,
  };
}
/* ============================================================
   SCORING — attention metric = freq × duration × recency.
   ============================================================ */
function scorePanel(p) {
  var now = Date.now();
  var freq = p.interactions + 1;          // +1 to avoid zero
  var dur = Math.max(p.viewDuration, 1000);// min 1s baseline
  // recency decay: exponential, half-life = DECAY_HALF_LIFE
  var age = Math.max(now - p.lastInteraction, 0);
  var lambda = Math.LN2 / DECAY_HALF_LIFE;
  var recency = Math.exp(-lambda * age);   // 1.0 = just now, →0 = old
  p.score = freq * (dur / 1000) * recency;
  return p.score;
}
/* ============================================================
   RANKING — sort by score, assign percentile ranks.
   ============================================================ */
function rankPanels() {
  var i, len = Store.panels.length;
  for (i = 0; i < len; i++) { scorePanel(Store.panels[i]); }
  // sort descending by score; locked panels keep their position
  var sorted = Store.panels.slice().sort(function(a, b) {
    return b.score - a.score;
  });
  // assign ranks (0 = highest score)
  for (i = 0; i < sorted.length; i++) { sorted[i].rank = i; }
  // compact low-rank panels (bottom COMPACT_THRESHOLD percentile)
  var compactFrom = Math.floor(len * (1 - COMPACT_THRESHOLD));
  for (i = 0; i < Store.panels.length; i++) {
    var p = Store.panels[i];
    // never compact locked panels
    p.compacted = !p.locked && p.rank >= compactFrom;
  }
}
/* ============================================================
   LAYOUT ENGINE — map rank → grid-area (row, col, span).
   Layout: high rank = large (2×2), top-left priority.
   Medium = 1×2 or 2×1. Low/compact = 1×1.
   ============================================================ */
function assignLayout() {
  var panels = Store.panels;
  var len = panels.length;
  if (len === 0) return;
  // sort by rank (ascending: best first)
  var ordered = panels.slice().sort(function(a, b) {
    return a.rank - b.rank;
  });
  // grid cell allocator: tracks occupied cells in [row][col]
  var occupied = {}; // "row,col" → true
  function occupy(r, c, rs, cs) {
    for (var dr = 0; dr < rs; dr++) {
      for (var dc = 0; dc < cs; dc++) {
        occupied[(r + dr) + ',' + (c + dc)] = true;
      }
    }
  }
  function isFree(r, c, rs, cs) {
    for (var dr = 0; dr < rs; dr++) {
      for (var dc = 0; dc < cs; dc++) {
        if (occupied[(r + dr) + ',' + (c + dc)]) return false;
      }
    }
    return r + rs <= 20 && c + cs <= COLS; // cap rows at 20
  }
  /* find next free cell scanning row-major */
  function nextFree(rs, cs) {
    for (var r = 0; r < 20; r++) {
      for (var c = 0; c <= COLS - cs; c++) {
        if (isFree(r, c, rs, cs)) return {row: r, col: c};
      }
    }
    // fallback: append at bottom, full width
    var maxRow = 0;
    Object.keys(occupied).forEach(function(k) {
      var rr = parseInt(k.split(',')[0], 10);
      if (rr >= maxRow) maxRow = rr + 1;
    });
    return {row: maxRow, col: 0};
  }
  // assign: top 25% → 2×2, next 50% → 1×2 or 2×1, bottom 25% → 1×1
  for (var i = 0; i < len; i++) {
    var p = ordered[i];
    if (p.locked && p.gridArea) continue; // locked: keep position
    var rs, cs;
    if (p.compacted)               { rs = 1; cs = 1; }
    else if (p.rank < len * 0.25)  { rs = 2; cs = 2; }  // top tier
    else if (p.rank < len * 0.60)  { rs = 2; cs = 1; }  // mid tier
    else                           { rs = 1; cs = 1; }  // lower tier
    var cell = nextFree(rs, cs);
    p.gridArea = {
      row: cell.row + 1, col: cell.col + 1,
      rowSpan: rs, colSpan: cs,
    };
    occupy(cell.row, cell.col, rs, cs);
  }
}
/* ============================================================
   DOM RENDER — targeted mutations, no full re-render.
   Uses requestAnimationFrame for batching.
   ============================================================ */
var rafPending = false;
var pendingUpdates = {}; // panelId → true
function scheduleDOMUpdate(panelId) {
  pendingUpdates[panelId] = true;
  if (!rafPending) {
    rafPending = true;
    requestAnimationFrame(flushDOMUpdates);
  }
}
function flushDOMUpdates() {
  rafPending = false;
  var ids = Object.keys(pendingUpdates);
  pendingUpdates = {};
  for (var i = 0; i < ids.length; i++) {
    var p = findPanel(ids[i]);
    if (p && p.el) { applyPanelDOM(p); }
  }
  updateStats();
}
/* apply single panel's state to its DOM node (targeted mutation) */
function applyPanelDOM(p) {
  var el = p.el;
  // grid placement
  if (p.gridArea) {
    el.style.gridRow = p.gridArea.row + ' / span ' + p.gridArea.rowSpan;
    el.style.gridColumn = p.gridArea.col + ' / span ' + p.gridArea.colSpan;
  }
  // locked class
  el.classList.toggle('locked', p.locked);
  // compact class
  el.classList.toggle('compact', p.compacted);
  // score badge
  var scoreEl = el.querySelector('.panel-score');
  if (scoreEl) { scoreEl.textContent = Math.round(p.score); }
  // heat dot
  var dot = el.querySelector('.heat-dot');
  if (dot) {
    dot.classList.toggle('hot', p.rank < Store.panels.length * 0.3);
    dot.classList.toggle('warm',
      p.rank >= Store.panels.length * 0.3 &&
      p.rank < Store.panels.length * 0.6);
  }
  // footer stats
  var durEl = el.querySelector('.stat-dur');
  if (durEl) { durEl.textContent = fmtDuration(p.viewDuration); }
  var intEl = el.querySelector('.stat-int');
  if (intEl) { intEl.textContent = p.interactions; }
  // compact preview sparkline (simple bar heights from score percentile)
  var sparkEl = el.querySelector('.spark');
  if (sparkEl && p.compacted) {
    var bars = sparkEl.children;
    var h = Math.min(100, Math.max(5, (p.score / (Store.panels[0] ?
      Store.panels[0].score || 1 : 1)) * 100));
    for (var b = 0; b < bars.length; b++) {
      bars[b].style.height = (h * (0.3 + 0.7 * Math.random())) + '%';
    }
  }
}
/* ============================================================
   FULL REBUILD — only called on init or reset.
   ============================================================ */
function fullRebuild() {
  var grid = document.getElementById('grid');
  grid.innerHTML = '';
  for (var i = 0; i < Store.panels.length; i++) {
    var p = Store.panels[i];
    var el = buildPanelDOM(p);
    p.el = el;
    grid.appendChild(el);
  }
  // re-attach observer after DOM rebuild
  attachObserver();
}
/* build a single panel's DOM fragment */
function buildPanelDOM(p) {
  var el = document.createElement('div');
  el.className = 'panel';
  el.setAttribute('data-panel-id', p.id);
  el.draggable = true;
  // grid area
  if (p.gridArea) {
    el.style.gridRow = p.gridArea.row + ' / span ' + p.gridArea.rowSpan;
    el.style.gridColumn = p.gridArea.col + ' / span ' + p.gridArea.colSpan;
  }
  // header
  var hdr = document.createElement('div');
  hdr.className = 'panel-header';
  hdr.innerHTML =
    '<span class="heat-dot"></span>' +
    '<span class="panel-title">' + esc(p.title) + '</span>' +
    '<span class="panel-score">' + Math.round(p.score) + '</span>' +
    '<button class="btn-lock" data-action="lock" ' +
    'title="Lock position">&#128274;</button>' +
    '<button class="btn-compact" data-action="compact" ' +
    'title="Toggle compact">&#9776;</button>';
  // body
  var body = document.createElement('div');
  body.className = 'panel-body';
  try {
    body.innerHTML = p.contentFn.call(p.data, p.data);
  } catch(e) {
    body.innerHTML = '<span style="color:var(--warn)">Render error</span>';
  }
  // compact preview
  var preview = document.createElement('div');
  preview.className = 'compact-preview';
  var spark = document.createElement('div');
  spark.className = 'spark';
  for (var s = 0; s < 8; s++) {
    var bar = document.createElement('div');
    bar.className = 'spark-bar';
    bar.style.height = (20 + Math.random() * 60) + '%';
    spark.appendChild(bar);
  }
  var val = document.createElement('div');
  val.className = 'metric-val';
  val.textContent = (p.data && p.data.val != null) ?
    p.data.val : '--';
  preview.appendChild(spark);
  preview.appendChild(val);
  // footer
  var footer = document.createElement('div');
  footer.className = 'panel-footer';
  footer.innerHTML =
    '<span title="View duration">&#9200; ' +
    '<span class="stat-dur">' + fmtDuration(p.viewDuration) +
    '</span></span>' +
    '<span title="Interactions">&#128064; ' +
    '<span class="stat-int">' + p.interactions + '</span></span>';
  // assemble
  el.appendChild(hdr);
  el.appendChild(body);
  el.appendChild(preview);
  el.appendChild(footer);
  // apply state classes
  el.classList.toggle('locked', p.locked);
  el.classList.toggle('compact', p.compacted);
  var lockBtn = hdr.querySelector('.btn-lock');
  if (p.locked) lockBtn.classList.add('active');
  return el;
}
/* ============================================================
   EVENT DELEGATION — single handler on grid container.
   Handles: lock, compact, dragstart/dragend.
   ============================================================ */
function handleGridClick(e) {
  var btn = e.target.closest('button');
  if (!btn) return;
  var action = btn.getAttribute('data-action');
  var panelEl = e.target.closest('.panel');
  if (!panelEl) return;
  var panelId = panelEl.getAttribute('data-panel-id');
  var p = findPanel(panelId);
  if (!p) return;
  // record interaction
  p.interactions++;
  p.lastInteraction = Date.now();
  if (action === 'lock') {
    p.locked = !p.locked;
    btn.classList.toggle('active', p.locked);
    panelEl.classList.toggle('locked', p.locked);
    // if unlocking, allow re-rank in next recalc
    if (!p.locked) { p.gridArea = null; }
    scheduleRecalc();
  } else if (action === 'compact') {
    p.compacted = !p.compacted;
    panelEl.classList.toggle('compact', p.compacted);
    // force relayout if manually expanding a compacted panel
    if (!p.compacted) { p.gridArea = null; }
    scheduleRecalc();
  }
  scheduleDOMUpdate(panelId);
}
/* drag-and-drop via event delegation */
function handleDragStart(e) {
  var panelEl = e.target.closest('.panel');
  if (!panelEl) return;
  var panelId = panelEl.getAttribute('data-panel-id');
  e.dataTransfer.setData('text/plain', panelId);
  e.dataTransfer.effectAllowed = 'move';
  panelEl.classList.add('dragging');
}
function handleDragEnd(e) {
  var panelEl = e.target.closest('.panel');
  if (panelEl) { panelEl.classList.remove('dragging'); }
  // remove all drag-over highlights
  var overs = document.querySelectorAll('.panel.drag-over');
  for (var i = 0; i < overs.length; i++) {
    overs[i].classList.remove('drag-over');
  }
  // remove placeholder
  var ph = document.querySelector('.drag-placeholder');
  if (ph) { ph.remove(); }
}
function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  var panelEl = e.target.closest('.panel');
  if (panelEl) {
    // remove highlight from others, add to current
    var overs = document.querySelectorAll('.panel.drag-over');
    for (var i = 0; i < overs.length; i++) {
      if (overs[i] !== panelEl) overs[i].classList.remove('drag-over');
    }
    panelEl.classList.add('drag-over');
  }
}
function handleDrop(e) {
  e.preventDefault();
  var targetEl = e.target.closest('.panel');
  var srcId = e.dataTransfer.getData('text/plain');
  if (!srcId || !targetEl) return;
  var tgtId = targetEl.getAttribute('data-panel-id');
  if (srcId === tgtId) return;
  var srcPanel = findPanel(srcId);
  var tgtPanel = findPanel(tgtId);
  if (!srcPanel || !tgtPanel) return;
  // swap positions in panels array
  var srcIdx = Store.panels.indexOf(srcPanel);
  var tgtIdx = Store.panels.indexOf(tgtPanel);
  Store.panels.splice(srcIdx, 1);
  // re-insert at adjusted target index
  var newIdx = srcIdx < tgtIdx ? tgtIdx - 1 : tgtIdx;
  Store.panels.splice(newIdx, 0, srcPanel);
  // lock both after manual reorder
  srcPanel.locked = true;
  tgtPanel.locked = true;
  srcPanel.gridArea = null;
  tgtPanel.gridArea = null;
  // clean up visuals
  handleDragEnd(e);
  scheduleRecalc();
  fullRebuild();
}
/* ============================================================
   VISIBILITY TRACKING — IntersectionObserver.
   ============================================================ */
function attachObserver() {
  if (Store.observer) { Store.observer.disconnect(); }
  Store.observer = new IntersectionObserver(
    handleVisibility, { threshold: [0, 0.5, 1.0] }
  );
  for (var i = 0; i < Store.panels.length; i++) {
    var el = Store.panels[i].el;
    if (el) { Store.observer.observe(el); }
  }
}
function handleVisibility(entries) {
  var now = Date.now();
  for (var i = 0; i < entries.length; i++) {
    var entry = entries[i];
    var panelEl = entry.target;
    var panelId = panelEl.getAttribute('data-panel-id');
    var p = findPanel(panelId);
    if (!p) continue;
    var vm = Store.visibilityMap[panelId] ||
      (Store.visibilityMap[panelId] = { enterTime: 0, accumulated: 0 });
    if (entry.isIntersecting && entry.intersectionRatio >= 0.5) {
      // panel became visible (≥50%)
      if (!vm.enterTime) { vm.enterTime = now; }
    } else {
      // panel hidden or below 50% threshold
      if (vm.enterTime) {
        vm.accumulated += (now - vm.enterTime);
        vm.enterTime = 0;
      }
    }
    // flush accumulated into panel metric
    p.viewDuration = vm.accumulated +
      (vm.enterTime ? (now - vm.enterTime) : 0);
    // schedule DOM update (throttled via rAF batching)
    scheduleDOMUpdate(panelId);
  }
}
/* flush accumulated durations on page unload */
function flushVisibility() {
  var now = Date.now();
  for (var id in Store.visibilityMap) {
    var vm = Store.visibilityMap[id];
    if (vm.enterTime) {
      vm.accumulated += (now - vm.enterTime);
      vm.enterTime = 0;
    }
    var p = findPanel(id);
    if (p) { p.viewDuration = vm.accumulated; }
  }
}
window.addEventListener('beforeunload', flushVisibility);
/* ============================================================
   PERSISTENCE — localStorage save/restore.
   ============================================================ */
function persist() {
  flushVisibility();
  var data = {
    panels: Store.panels.map(function(p) {
      return {
        id: p.id, title: p.title, data: p.data,
        viewDuration: p.viewDuration, interactions: p.interactions,
        lastInteraction: p.lastInteraction, firstSeen: p.firstSeen,
        locked: p.locked, compacted: p.compacted,
        gridArea: p.gridArea, rank: p.rank, score: p.score,
      };
    }),
    autoLayout: Store.autoLayout,
  };
  try {
    localStorage.setItem(SAVE_KEY, JSON.stringify(data));
  } catch(e) {
    // quota exceeded — silently fail, data stays in memory
  }
}
function restore() {
  try {
    var raw = localStorage.getItem(SAVE_KEY);
    if (!raw) return false;
    var data = JSON.parse(raw);
    Store.panels = data.panels.map(function(rawPanel, idx) {
      var p = createPanel(rawPanel.data || rawPanel, idx);
      // restore metrics
      p.viewDuration = rawPanel.viewDuration || 0;
      p.interactions = rawPanel.interactions || 0;
      p.lastInteraction = rawPanel.lastInteraction || Date.now();
      p.firstSeen = rawPanel.firstSeen || Date.now();
      p.locked = rawPanel.locked || false;
      p.compacted = rawPanel.compacted || false;
      p.gridArea = rawPanel.gridArea || null;
      p.rank = rawPanel.rank || 0;
      p.score = rawPanel.score || 0;
      p.id = rawPanel.id;
      p.title = rawPanel.title;
      return p;
    });
    Store.autoLayout = data.autoLayout !== false;
    return true;
  } catch(e) {
    return false;
  }
}
/* ============================================================
   RECALC SCHEDULER — debounced rank + layout + persist.
   ============================================================ */
function scheduleRecalc() {
  if (Store.recalcTimer) { clearTimeout(Store.recalcTimer); }
  Store.recalcTimer = setTimeout(doRecalc, RECALC_DEBOUNCE);
}
function doRecalc() {
  Store.recalcTimer = null;
  rankPanels();
  if (Store.autoLayout) { assignLayout(); }
  // targeted DOM updates for all panels
  for (var i = 0; i < Store.panels.length; i++) {
    scheduleDOMUpdate(Store.panels[i].id);
  }
  persist();
  updateStats();
}
/* ============================================================
   UTILS
   ============================================================ */
function findPanel(id) {
  for (var i = 0; i < Store.panels.length; i++) {
    if (Store.panels[i].id === id) return Store.panels[i];
  }
  return null;
}
function fmtDuration(ms) {
  if (ms < 1000) return '<1s';
  if (ms < 60000) return Math.round(ms / 1000) + 's';
  return Math.round(ms / 60000) + 'm';
}
function esc(s) {
  var div = document.createElement('div');
  div.textContent = s;
  return div.innerHTML;
}
function updateStats() {
  var el = document.getElementById('stat-panels');
  if (el) {
    el.textContent = Store.panels.length + ' panels | ' +
      Store.panels.filter(function(p) { return p.compacted; }).length +
      ' compact';
  }
  var ses = document.getElementById('stat-session');
  if (ses) {
    var total = Store.panels.reduce(function(acc, p) {
      return acc + p.interactions;
    }, 0);
    ses.textContent = total + ' interactions';
  }
}
/* ============================================================
   INIT — bootstrap the dashboard.
   ============================================================ */
function init() {
  var restored = restore();
  if (!restored) {
    // first run: initialize from defaults
    Store.panels = DEFAULT_PANELS.map(function(raw, idx) {
      return createPanel(raw, idx);
    });
    rankPanels();
    assignLayout();
    persist();
  }
  // ensure all panels have contentFn if restored from old format
  for (var i = 0; i < Store.panels.length; i++) {
    var p = Store.panels[i];
    if (!p.contentFn && p.data) {
      p.contentFn = cp;
    }
  }
  // auto-layout button state
  document.getElementById('btn-auto').textContent =
    'Auto: ' + (Store.autoLayout ? 'ON' : 'OFF');
  // event delegation on grid
  var grid = document.getElementById('grid');
  grid.addEventListener('click', handleGridClick);
  grid.addEventListener('dragstart', handleDragStart);
  grid.addEventListener('dragend', handleDragEnd);
  grid.addEventListener('dragover', handleDragOver);
  grid.addEventListener('drop', handleDrop);
  // toolbar
  document.getElementById('btn-auto').addEventListener('click',
    function() {
      Store.autoLayout = !Store.autoLayout;
      this.textContent = 'Auto: ' + (Store.autoLayout ? 'ON' : 'OFF');
      if (Store.autoLayout) {
        // reset all grid areas and recalc
        for (var i = 0; i < Store.panels.length; i++) {
          if (!Store.panels[i].locked) {
            Store.panels[i].gridArea = null;
          }
        }
        assignLayout();
        fullRebuild();
      }
      persist();
    });
  document.getElementById('btn-reset').addEventListener('click',
    function() {
      if (!confirm('Reset all tracking data and layout?')) return;
      localStorage.removeItem(SAVE_KEY);
      Store.panels = DEFAULT_PANELS.map(function(raw, idx) {
        return createPanel(raw, idx);
      });
      Store.visibilityMap = {};
      rankPanels();
      assignLayout();
      fullRebuild();
      persist();
      updateStats();
    });
  // periodic persist (every 30s)
  setInterval(persist, 30000);
  // initial render
  fullRebuild();
  updateStats();
  // start periodic recalc for decay (every 60s)
  setInterval(function() {
    if (Store.autoLayout) { scheduleRecalc(); }
  }, 60000);
}
// --- boot ---
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
</script>
</body>
</html>
```