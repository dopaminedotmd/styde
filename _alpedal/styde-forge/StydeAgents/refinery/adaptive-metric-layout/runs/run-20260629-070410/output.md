```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--surface2:#22263a;--border:#2a2e3f;
  --text:#e1e4ed;--text2:#9498a8;--accent:#6c8cff;--accent2:#4ade80;
  --warn:#f59e0b;--danger:#ef4444;--radius:10px;--gap:10px;
  --transition:0.3s cubic-bezier(0.4,0,0.2,1);
}
body{
  font-family:system-ui,-apple-system,sans-serif;background:var(--bg);
  color:var(--text);min-height:100vh;padding:16px;
  -webkit-font-smoothing:antialiased;
}
header{
  display:flex;align-items:center;justify-content:space-between;
  padding:0 0 16px;flex-wrap:wrap;gap:12px;
}
h1{font-size:1.4rem;font-weight:600;letter-spacing:-0.02em}
.controls{display:flex;gap:8px;flex-wrap:wrap}
.controls button,.controls select{
  padding:6px 14px;border-radius:6px;border:1px solid var(--border);
  background:var(--surface);color:var(--text);cursor:pointer;
  font-size:0.8rem;transition:var(--transition);
}
.controls button:hover{background:var(--surface2);border-color:var(--accent)}
.controls button.active{background:var(--accent);border-color:var(--accent);color:#fff}
.toast{
  position:fixed;bottom:20px;right:20px;padding:10px 18px;
  border-radius:8px;font-size:0.78rem;z-index:9999;
  background:var(--surface2);border:1px solid var(--border);
  opacity:0;transform:translateY(10px);transition:all 0.25s;
  pointer-events:none;max-width:340px;
}
.toast.show{opacity:1;transform:translateY(0)}
.toast.warn{border-color:var(--warn);color:var(--warn)}
.toast.err{border-color:var(--danger);color:var(--danger)}
.grid{
  display:grid;gap:var(--gap);
  grid-template-columns:repeat(4,1fr);
  grid-auto-rows:minmax(140px,auto);
  transition:grid-template-columns 0.4s,grid-template-rows 0.4s;
}
.panel{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);position:relative;
  transition:grid-row 0.4s,grid-column 0.4s,border-color var(--transition),
    box-shadow var(--transition),opacity 0.3s;
  overflow:hidden;display:flex;flex-direction:column;
  cursor:grab;min-height:140px;
}
.panel:active{cursor:grabbing}
.panel.dragging{opacity:0.7;z-index:100;box-shadow:0 8px 32px rgba(0,0,0,0.5);
  border-color:var(--accent);cursor:grabbing;pointer-events:none}
.panel.drag-over{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent)}
.panel.locked .panel-handle{cursor:not-allowed;opacity:0.4}
.panel.locked{border-color:var(--accent2);box-shadow:0 0 0 1px var(--accent2)}
.panel.compact{min-height:90px}
.panel.compact .panel-body{display:none}
.panel.collapsed{min-height:44px}
.panel.collapsed .panel-body,.panel.collapsed .panel-actions{display:none}
.panel-handle{
  display:flex;align-items:center;justify-content:space-between;
  padding:10px 14px;gap:8px;cursor:inherit;user-select:none;
  background:linear-gradient(180deg,var(--surface2),var(--surface));
  border-bottom:1px solid var(--border);min-height:42px;
}
.panel-title{font-weight:600;font-size:0.82rem;letter-spacing:0.01em;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-actions{display:flex;gap:4px;flex-shrink:0}
.panel-actions button{
  background:none;border:none;color:var(--text2);cursor:pointer;
  padding:4px 6px;border-radius:4px;font-size:0.85rem;line-height:1;
  transition:var(--transition);
}
.panel-actions button:hover{background:var(--surface2);color:var(--text)}
.panel-actions button.active{color:var(--accent2)}
.panel-body{padding:14px;flex:1;display:flex;flex-direction:column;gap:8px}
.panel-body .metric-value{font-size:1.6rem;font-weight:700;letter-spacing:-0.03em}
.panel-body .metric-label{font-size:0.72rem;color:var(--text2);text-transform:uppercase;
  letter-spacing:0.05em}
.panel-body .metric-change{font-size:0.78rem;display:flex;align-items:center;gap:4px}
.panel-body .metric-change.up{color:var(--accent2)}
.panel-body .metric-change.down{color:var(--danger)}
.sparkline{display:flex;align-items:flex-end;gap:2px;height:40px;padding:4px 0}
.sparkline-bar{flex:1;background:var(--accent);border-radius:2px 2px 0 0;
  min-width:3px;transition:height 0.4s}
.sparkline-bar.low{background:var(--text2);opacity:0.4}
.sparkline-bar.mid{background:var(--accent);opacity:0.6}
.sparkline-bar.high{background:var(--accent2)}
.more-section{
  margin-top:12px;padding:10px 14px;background:var(--surface);
  border:1px dashed var(--border);border-radius:var(--radius);
  display:flex;align-items:center;justify-content:space-between;
  cursor:pointer;transition:var(--transition);font-size:0.8rem;
  color:var(--text2);
}
.more-section:hover{background:var(--surface2);border-color:var(--accent)}
.more-section .count-badge{
  background:var(--accent);color:#fff;padding:2px 8px;
  border-radius:10px;font-size:0.7rem;font-weight:600;
}
.more-drawer{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));
  gap:var(--gap);padding:8px 0 0;max-height:0;overflow:hidden;
  transition:max-height 0.4s,padding 0.4s;
}
.more-drawer.open{max-height:600px;padding:8px 0}
.rank-badge{
  position:absolute;top:8px;right:8px;font-size:0.6rem;font-weight:700;
  padding:2px 6px;border-radius:4px;background:var(--surface2);
  color:var(--text2);opacity:0;transition:opacity 0.3s;
  pointer-events:none;z-index:2;
}
.panel:hover .rank-badge{opacity:1}
.toolbar-hint{
  font-size:0.7rem;color:var(--text2);opacity:0.6;text-align:right;
  padding:4px 0 0;
}
.reset-link{font-size:0.72rem;color:var(--text2);cursor:pointer;
  text-decoration:underline;text-underline-offset:2px}
.reset-link:hover{color:var(--danger)}
</style>
</head>
<body>
<header>
  <div>
    <h1>Adaptive Dashboard</h1>
    <div class="toolbar-hint">Drag panels to override · Layout learns from your behavior</div>
  </div>
  <div class="controls">
    <button id="btn-reset" class="reset-link" title="Clear all tracking data and reset layout">Reset All Data</button>
    <select id="sort-mode">
      <option value="auto">Auto (Adaptive)</option>
      <option value="recent">By Recency</option>
      <option value="manual">Manual Only</option>
    </select>
    <button id="btn-expand-all">Expand All</button>
  </div>
</header>
<div class="grid" id="grid"></div>
<div class="more-section" id="more-toggle">
  <span>More panels</span>
  <span class="count-badge" id="more-count">0</span>
</div>
<div class="more-drawer" id="more-drawer"></div>
<div class="toast" id="toast"></div>
<script>
'use strict';
// ── Constants ──────────────────────────────────────────────
const DURATION_WEIGHT = 0.1;       // 1 click ≈ 10 seconds of view time
const RECENCY_HALF_LIFE_H = 24;    // half-life in hours for recency decay
const COMPACT_THRESHOLD = 0.25;    // bottom 25% get compacted
const COLLAPSE_THRESHOLD = 0.08;   // bottom 8% get collapsed to "more"
const DEBOUNCE_MS = 150;
const SAVE_DEBOUNCE_MS = 800;
const MIN_VIEW_DURATION_S = 0.5;   // ignore sub-500ms views (scroll-through)
// ── State ──────────────────────────────────────────────────
let panels = [];
let overrides = {};       // {panelId: {locked:bool, row:str, col:str}}
let rankOrder = [];
let sortMode = 'auto';
let resizeTimer = null;
let saveTimer = null;
let moreOpen = false;
// ── Initial panel definitions ──────────────────────────────
const PANEL_DEFS = [
  {id:'revenue',title:'Revenue',type:'big-number',value:128400,change:12.3,
   unit:'$',spark:[30,45,38,52,60,48,55,70,65,78,82,75,88,95,90,105,110,100,118,128]},
  {id:'users',title:'Active Users',type:'big-number',value:2847,change:-3.1,
   unit:'',spark:[2100,2200,2150,2400,2350,2500,2600,2550,2700,2800,2750,2900,2850,2950,3000,2900,2800,2750,2880,2847]},
  {id:'conversion',title:'Conversion Rate',type:'percentage',value:4.8,change:0.5,
   unit:'%',spark:[3.2,3.5,3.1,3.8,3.6,4.0,3.9,4.2,4.1,4.5,4.3,4.7,4.4,4.6,4.9,4.5,4.8,4.6,4.7,4.8]},
  {id:'session',title:'Avg Session',type:'duration',value:312,change:8.7,
   unit:'s',spark:[280,290,270,300,310,295,305,320,315,330,325,310,340,335,350,345,330,320,315,312]},
  {id:'bounce',title:'Bounce Rate',type:'percentage-inv',value:34.2,change:-2.8,
   unit:'%',spark:[42,40,38,39,37,36,35,38,36,34,35,33,32,34,33,35,34,33,35,34]},
  {id:'loadtime',title:'Page Load',type:'duration',value:1.4,change:-0.2,
   unit:'s',spark:[2.1,1.9,1.8,2.0,1.7,1.6,1.8,1.5,1.6,1.4,1.5,1.3,1.4,1.2,1.3,1.5,1.4,1.3,1.5,1.4]},
  {id:'errors',title:'Error Rate',type:'percentage-inv',value:0.12,change:-0.03,
   unit:'%',spark:[0.25,0.22,0.20,0.18,0.19,0.17,0.15,0.16,0.14,0.13,0.15,0.12,0.14,0.11,0.13,0.10,0.12,0.11,0.13,0.12]},
  {id:'throughput',title:'Throughput',type:'big-number',value:15600,change:22.1,
   unit:'/min',spark:[8000,8500,8200,9000,9500,10000,10500,11000,10800,11500,12000,12500,13000,13500,14000,14500,15000,14800,15200,15600]},
];
// ── Utility: formatMetric ──────────────────────────────────
function formatMetric(value, type) {
  switch (type) {
    case 'duration':
      if (value >= 3600) { const h=Math.floor(value/3600),m=Math.floor((value%3600)/60); return h+'h '+m+'m'; }
      if (value >= 60) { const m=Math.floor(value/60),s=Math.round(value%60); return m+'m '+s+'s'; }
      return Math.round(value*10)/10+'s';
    case 'big-number':
      if (value >= 1e6) return (value/1e6).toFixed(1)+'M';
      if (value >= 1e3) return (value/1e3).toFixed(1)+'K';
      return String(Math.round(value));
    case 'percentage':
      return value.toFixed(1)+'%';
    case 'percentage-inv':
      return value.toFixed(2)+'%';
    default:
      return String(value);
  }
}
// ── Persistence ────────────────────────────────────────────
const STORAGE_KEY = 'adaptive_dashboard_v1';
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const data = JSON.parse(raw);
    if (!data || typeof data !== 'object') return null;
    return data;
  } catch (e) {
    if (e.name === 'QuotaExceededError' || e.code === 22) {
      showToast('Storage full — using in-memory mode. Clear some data to re-enable persistence.', 'warn');
    }
    return null;
  }
}
function saveState() {
  const data = {
    panels: panels.map(p => ({
      id: p.id, frequency: p.frequency, totalDuration: p.totalDuration,
      lastInteraction: p.lastInteraction
    })),
    overrides,
    sortMode,
    savedAt: Date.now()
  };
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (e) {
    if (e.name === 'QuotaExceededError' || e.code === 22) {
      showToast('Cannot save — localStorage full. Layout will reset on reload.', 'err');
    }
  }
}
function debouncedSave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveState, SAVE_DEBOUNCE_MS);
}
// ── Toast ──────────────────────────────────────────────────
let toastTimer = null;
function showToast(msg, type) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = 'toast ' + (type||'') + ' show';
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('show'), 3000);
}
// ── Scoring engine ─────────────────────────────────────────
function computeRecencyFactor(lastInteraction) {
  if (!lastInteraction) return 1.0;
  const hoursSince = (Date.now() - lastInteraction) / 3600000;
  // Half-life decay: factor = 2^(-hours/halfLife)
  return Math.pow(2, -hoursSince / RECENCY_HALF_LIFE_H);
}
function computeScore(panel) {
  const freq = panel.frequency || 0;
  const dur = (panel.totalDuration || 0) / 1000; // convert ms to seconds
  const recency = computeRecencyFactor(panel.lastInteraction);
  // Composite: frequency × (1 + durationWeight × totalDuration) × recency
  // Adding 1 to duration term so panels with zero duration still get frequency credit
  return freq * (1 + dur * DURATION_WEIGHT) * recency;
}
function rankPanels() {
  const scored = panels.map(p => ({id:p.id, score:computeScore(p)}));
  scored.sort((a,b) => b.score - a.score);
  rankOrder = scored.map(s => s.id);
  return scored;
}
// ── Layout engine ──────────────────────────────────────────
function computeLayout() {
  const scored = rankPanels();
  const n = scored.length;
  if (n === 0) return {positions:{},compact:[],collapsed:[]};
  const positions = {};
  const compact = [];
  const collapsed = [];
  // Check overrides first
  const overriddenIds = new Set();
  const overridePositions = {};
  for (const [id, ov] of Object.entries(overrides)) {
    if (ov.locked && ov.row && ov.col) {
      overridePositions[id] = {row:ov.row, col:ov.col, locked:true};
      overriddenIds.add(id);
    }
  }
  // Non-overridden panels sorted by score
  const freePanels = scored.filter(s => !overriddenIds.has(s.id));
  // Grid layout: 4 columns, auto rows
  // High rank: larger span (2x2), then 2x1, 1x2, 1x1
  // Position mapping by rank (0-indexed among free panels)
  const GRID_COLS = 4;
  // Define slot sizes: index → {rowSpan, colSpan}
  const SLOTS = [
    {rs:2,cs:2}, // rank 0: featured (2x2)
    {rs:2,cs:1}, // rank 1
    {rs:1,cs:1}, // rank 2
    {rs:1,cs:2}, // rank 3
    {rs:1,cs:1}, // rank 4
    {rs:1,cs:1}, // rank 5
    {rs:1,cs:1}, // rank 6
    {rs:1,cs:1}, // rank 7
  ];
  // Place overridden panels first (they keep their positions)
  // Then fill remaining grid cells with free panels
  // Track occupied cells
  const occupied = new Set(); // "row,col" strings
  for (const [id, pos] of Object.entries(overridePositions)) {
    const [r,c] = [pos.row, pos.col].map(Number);
    // Mark the override position as occupied (assume 1x1 for override slots)
    for (let dr=0;dr<1;dr++)
      for (let dc=0;dc<1;dc++)
        occupied.add((r+dr)+','+(c+dc));
    positions[id] = {row:r, col:c, rowSpan:1, colSpan:1, locked:true};
  }
  // Fill free panels into remaining slots
  // Walk the grid row by row, column by column, place panels
  let freeIdx = 0;
  let row = 1;
  const MAX_COL = GRID_COLS + 1;
  outer:
  while (freeIdx < freePanels.length && row < 50) {
    for (let col = 1; col <= GRID_COLS; col++) {
      if (occupied.has(row+','+col)) continue;
      // Determine slot size based on rank
      const slotRank = freeIdx;
      let rs = 1, cs = 1;
      if (slotRank < SLOTS.length) {
        rs = SLOTS[slotRank].rs;
        cs = SLOTS[slotRank].cs;
      }
      // Clamp to grid bounds
      if (col + cs - 1 > GRID_COLS) cs = GRID_COLS - col + 1;
      if (cs < 1) cs = 1;
      // Check if entire slot is free
      let slotFree = true;
      for (let dr=0;dr<rs&&slotFree;dr++)
        for (let dc=0;dc<cs&&slotFree;dc++)
          if (occupied.has((row+dr)+','+(col+dc)))
            slotFree = false;
      if (!slotFree) continue;
      // Place panel
      for (let dr=0;dr<rs;dr++)
        for (let dc=0;dc<cs;dc++)
          occupied.add((row+dr)+','+(col+dc));
      const pid = freePanels[freeIdx].id;
      const panel = panels.find(p=>p.id===pid);
      const scoreVal = freePanels[freeIdx].score;
      const maxScore = freePanels.length>0?Math.max(...freePanels.map(s=>s.score)):1;
      let state = 'normal';
      if (scoreVal < maxScore * COLLAPSE_THRESHOLD && maxScore > 0) state = 'collapsed';
      else if (scoreVal < maxScore * COMPACT_THRESHOLD && maxScore > 0) state = 'compact';
      positions[pid] = {row, col, rowSpan:rs, colSpan:cs, locked:false, state};
      if (state === 'compact') compact.push(pid);
      if (state === 'collapsed') collapsed.push(pid);
      freeIdx++;
    }
    row++;
  }
  // Any remaining free panels go to collapsed
  while (freeIdx < freePanels.length) {
    const pid = freePanels[freeIdx].id;
    positions[pid] = {row:99, col:1, rowSpan:1, colSpan:1, locked:false, state:'collapsed'};
    collapsed.push(pid);
    freeIdx++;
  }
  return {positions, compact, collapsed};
}
// ── DOM Rendering (efficient, per-panel updates) ───────────
function getPanelElement(id) {
  return document.getElementById('panel-' + id);
}
function createPanelElement(panel, pos) {
  const el = document.createElement('div');
  el.className = 'panel';
  el.id = 'panel-' + panel.id;
  el.draggable = true;
  el.dataset.panelId = panel.id;
  if (pos.state === 'compact') el.classList.add('compact');
  if (pos.state === 'collapsed') el.classList.add('collapsed');
  if (pos.locked) el.classList.add('locked');
  el.style.gridRow = pos.row + ' / span ' + (pos.rowSpan||1);
  el.style.gridColumn = pos.col + ' / span ' + (pos.colSpan||1);
  const def = PANEL_DEFS.find(d=>d.id===panel.id)||{};
  el.innerHTML =
    '<div class="rank-badge">#'+(rankOrder.indexOf(panel.id)+1)+'</div>'+
    '<div class="panel-handle">'+
      '<span class="panel-title">'+escHtml(def.title||panel.id)+'</span>'+
      '<div class="panel-actions">'+
        '<button class="btn-compact" title="Toggle compact" data-action="compact">⊟</button>'+
        '<button class="btn-lock '+(pos.locked?'active':'')+'" title="Lock position" data-action="lock">'+(pos.locked?'🔒':'🔓')+'</button>'+
        '<button class="btn-collapse" title="Collapse" data-action="collapse">'+(pos.state==='collapsed'?'⊞':'⊟')+'</button>'+
      '</div>'+
    '</div>'+
    '<div class="panel-body">'+
      renderPanelBody(def, panel)+
    '</div>';
  // Event delegation on the panel (not individual buttons to reduce listeners)
  el.addEventListener('click', handlePanelClick);
  el.addEventListener('dragstart', handleDragStart);
  el.addEventListener('dragend', handleDragEnd);
  el.addEventListener('dragover', handleDragOver);
  el.addEventListener('dragleave', handleDragLeave);
  el.addEventListener('drop', handleDrop);
  return el;
}
function updatePanelElement(panel, pos, prevPos) {
  const el = getPanelElement(panel.id);
  if (!el) return;
  const changed = {};
  // Grid position (only if changed — DOM diffing)
  const newRow = pos.row + ' / span ' + (pos.rowSpan||1);
  const newCol = pos.col + ' / span ' + (pos.colSpan||1);
  const oldRow = el.style.gridRow;
  const oldCol = el.style.gridColumn;
  if (newRow !== oldRow) { el.style.gridRow = newRow; changed.row=true; }
  if (newCol !== oldCol) { el.style.gridColumn = newCol; changed.col=true; }
  // State classes
  ['compact','collapsed','locked'].forEach(cls => {
    const has = el.classList.contains(cls);
    const want =
      cls==='compact' ? pos.state==='compact' :
      cls==='collapsed' ? pos.state==='collapsed' :
      pos.locked;
    if (has !== want) {
      el.classList.toggle(cls, want);
      changed[cls]=true;
    }
  });
  // Rank badge
  const badge = el.querySelector('.rank-badge');
  if (badge) {
    const newRank = '#'+(rankOrder.indexOf(panel.id)+1);
    if (badge.textContent !== newRank) badge.textContent = newRank;
  }
  // Lock button
  const lockBtn = el.querySelector('.btn-lock');
  if (lockBtn) {
    const wantLock = pos.locked ? '🔒' : '🔓';
    if (lockBtn.textContent !== wantLock) lockBtn.textContent = wantLock;
    lockBtn.classList.toggle('active', pos.locked);
  }
  // Collapse button
  const collapseBtn = el.querySelector('.btn-collapse');
  if (collapseBtn) {
    const wantCollapse = pos.state==='collapsed' ? '⊞' : '⊟';
    if (collapseBtn.textContent !== wantCollapse) collapseBtn.textContent = wantCollapse;
  }
  // Body content (only if something relevant changed)
  if (changed.compact || changed.collapsed) {
    const def = PANEL_DEFS.find(d=>d.id===panel.id)||{};
    const body = el.querySelector('.panel-body');
    if (body && !pos.state) body.innerHTML = renderPanelBody(def, panel);
  }
}
function renderPanelBody(def, panel) {
  if (!def) return '<div class="metric-value">—</div>';
  const val = formatMetric(def.value, def.type);
  const changeClass = def.change >= 0 ? 'up' : 'down';
  const changeArrow = def.change >= 0 ? '↑' : '↓';
  const sparkHtml = def.spark ? renderSparkline(def.spark) : '';
  return (
    '<div class="metric-value">'+val+(def.unit&&def.type!=='percentage'&&def.type!=='percentage-inv'?' <span style="font-size:0.7em;color:var(--text2)">'+escHtml(def.unit)+'</span>':'')+'</div>'+
    '<div class="metric-label">'+escHtml(def.title)+'</div>'+
    '<div class="metric-change '+changeClass+'">'+changeArrow+' '+Math.abs(def.change).toFixed(1)+'% vs last period</div>'+
    sparkHtml
  );
}
function renderSparkline(values) {
  if (!values||values.length===0) return '';
  const max = Math.max(...values);
  const min = Math.min(...values);
  const range = max-min||1;
  return '<div class="sparkline">'+values.map(v=>{
    const pct = ((v-min)/range*100).toFixed(0);
    let cls = 'sparkline-bar low';
    if (pct>66) cls='sparkline-bar high';
    else if (pct>33) cls='sparkline-bar mid';
    return '<div class="'+cls+'" style="height:'+Math.max(4,Number(pct)*0.38)+'px"></div>';
  }).join('')+'</div>';
}
function escHtml(s) {
  const d=document.createElement('div');
  d.textContent=s;
  return d.innerHTML;
}
// ── Full render (initial only) ─────────────────────────────
function fullRender() {
  const grid = document.getElementById('grid');
  const moreDrawer = document.getElementById('more-drawer');
  const moreToggle = document.getElementById('more-toggle');
  const moreCount = document.getElementById('more-count');
  const layout = computeLayout();
  const {positions, collapsed} = layout;
  // Remove panels no longer in the set
  const currentIds = new Set(panels.map(p=>p.id));
  ['grid','more-drawer'].forEach(containerId=>{
    const container = document.getElementById(containerId);
    Array.from(container.children).forEach(child=>{
      const pid = child.dataset.panelId;
      if (pid && !currentIds.has(pid)) child.remove();
    });
  });
  // Update or create panels
  const gridPanels = panels.filter(p=>!collapsed.includes(p.id));
  const morePanels = panels.filter(p=>collapsed.includes(p.id));
  // Grid panels
  gridPanels.forEach(panel=>{
    const pos = positions[panel.id];
    let el = getPanelElement(panel.id);
    if (!el) {
      el = createPanelElement(panel, pos);
      grid.appendChild(el);
    } else {
      // Check if it's in the wrong container
      if (el.parentElement !== grid) {
        el.remove();
        grid.appendChild(el);
      }
      updatePanelElement(panel, pos);
    }
  });
  // More drawer panels
  morePanels.forEach(panel=>{
    const pos = positions[panel.id];
    let el = getPanelElement(panel.id);
    if (!el) {
      el = createPanelElement(panel, pos);
      moreDrawer.appendChild(el);
    } else {
      if (el.parentElement !== moreDrawer) {
        el.remove();
        moreDrawer.appendChild(el);
      }
      updatePanelElement(panel, pos);
    }
  });
  moreCount.textContent = morePanels.length;
  moreToggle.style.display = morePanels.length > 0 ? 'flex' : 'none';
  if (morePanels.length === 0) moreDrawer.classList.remove('open');
}
// ── Efficient layout update (only changed positions) ───────
function updateLayout() {
  const layout = computeLayout();
  const {positions, collapsed} = layout;
  const grid = document.getElementById('grid');
  const moreDrawer = document.getElementById('more-drawer');
  const moreCount = document.getElementById('more-count');
  const moreToggle = document.getElementById('more-toggle');
  // Track which panels need to move between containers
  panels.forEach(panel => {
    const pos = positions[panel.id];
    const el = getPanelElement(panel.id);
    if (!el) return;
    const isCollapsed = collapsed.includes(panel.id);
    const inGrid = el.parentElement === grid;
    const inMore = el.parentElement === moreDrawer;
    if (isCollapsed && inGrid) {
      el.remove();
      moreDrawer.appendChild(el);
      updatePanelElement(panel, pos);
    } else if (!isCollapsed && inMore) {
      el.remove();
      grid.appendChild(el);
      updatePanelElement(panel, pos);
    } else {
      updatePanelElement(panel, pos);
    }
  });
  moreCount.textContent = collapsed.length;
  moreToggle.style.display = collapsed.length > 0 ? 'flex' : 'none';
  if (collapsed.length === 0) moreDrawer.classList.remove('open');
}
// ── Event handlers ─────────────────────────────────────────
function handlePanelClick(e) {
  const btn = e.target.closest('button[data-action]');
  if (!btn) {
    // Click on panel body: record interaction
    const panelEl = e.target.closest('.panel');
    if (panelEl) recordInteraction(panelEl.dataset.panelId, 'click');
    return;
  }
  e.preventDefault();
  e.stopPropagation();
  const panelEl = btn.closest('.panel');
  const pid = panelEl.dataset.panelId;
  const action = btn.dataset.action;
  switch (action) {
    case 'compact': {
      const panel = panels.find(p=>p.id===pid);
      if (!panel) break;
      const el = getPanelElement(pid);
      const isCompact = el.classList.contains('compact');
      if (isCompact) {
        el.classList.remove('compact');
        recordInteraction(pid, 'expand');
      } else {
        el.classList.add('compact');
        recordInteraction(pid, 'compact');
      }
      break;
    }
    case 'lock': {
      if (!overrides[pid]) overrides[pid]={};
      overrides[pid].locked = !overrides[pid].locked;
      if (!overrides[pid].locked) {
        // Unlock: remove position override
        delete overrides[pid].row;
        delete overrides[pid].col;
      } else {
        // Lock: record current position
        const el = getPanelElement(pid);
        if (el) {
          const rowMatch = el.style.gridRow.match(/^(\d+)/);
          const colMatch = el.style.gridColumn.match(/^(\d+)/);
          if (rowMatch) overrides[pid].row = parseInt(rowMatch[1]);
          if (colMatch) overrides[pid].col = parseInt(colMatch[1]);
        }
      }
      recordInteraction(pid, overrides[pid].locked?'lock':'unlock');
      updateLayout();
      debouncedSave();
      break;
    }
    case 'collapse': {
      const panel = panels.find(p=>p.id===pid);
      if (!panel) break;
      const el = getPanelElement(pid);
      const isCollapsed = el.classList.contains('collapsed');
      if (isCollapsed) {
        el.classList.remove('collapsed');
        recordInteraction(pid, 'expand');
      } else {
        el.classList.add('collapsed');
        recordInteraction(pid, 'collapse');
      }
      break;
    }
  }
}
function recordInteraction(panelId, type) {
  const panel = panels.find(p=>p.id===panelId);
  if (!panel) return;
  panel.frequency = (panel.frequency||0) + 1;
  panel.lastInteraction = Date.now();
  // Don't re-rank on every click — debounce
  clearTimeout(saveTimer);
  saveTimer = setTimeout(()=>{updateLayout();saveState();},1000);
}
// ── View duration tracking (IntersectionObserver) ──────────
const viewStartTimes = {};
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    const pid = entry.target.dataset.panelId;
    if (!pid) return;
    const panel = panels.find(p=>p.id===pid);
    if (!panel) return;
    if (entry.isIntersecting) {
      viewStartTimes[pid] = performance.now();
    } else if (viewStartTimes[pid]) {
      const elapsed = performance.now() - viewStartTimes[pid];
      if (elapsed >= MIN_VIEW_DURATION_S * 1000) {
        panel.totalDuration = (panel.totalDuration||0) + elapsed;
      }
      delete viewStartTimes[pid];
    }
  });
}, {threshold: 0.3});
function observePanel(el) {
  if (el && el.dataset.panelId) observer.observe(el);
}
// ── Drag and drop ──────────────────────────────────────────
let dragSourceId = null;
function handleDragStart(e) {
  const panelEl = e.target.closest('.panel');
  if (!panelEl) return;
  if (overrides[panelEl.dataset.panelId]?.locked) {
    e.preventDefault();
    return;
  }
  dragSourceId = panelEl.dataset.panelId;
  panelEl.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', dragSourceId);
}
function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  const panelEl = e.target.closest('.panel');
  if (panelEl && panelEl.dataset.panelId !== dragSourceId) {
    panelEl.classList.add('drag-over');
  }
}
function handleDragLeave(e) {
  const panelEl = e.target.closest('.panel');
  if (panelEl) panelEl.classList.remove('drag-over');
}
function handleDrop(e) {
  e.preventDefault();
  const targetEl = e.target.closest('.panel');
  const sourceEl = document.querySelector('.panel.dragging');
  // Clean up drag state on ALL panels (not full re-render)
  document.querySelectorAll('.panel.dragging').forEach(el=>el.classList.remove('dragging'));
  document.querySelectorAll('.panel.drag-over').forEach(el=>el.classList.remove('drag-over'));
  if (!targetEl || !sourceEl) { dragSourceId=null; return; }
  const targetId = targetEl.dataset.panelId;
  const sourceId = sourceEl.dataset.panelId;
  if (targetId === sourceId) { dragSourceId=null; return; }
  // Swap positions: only update the two affected panels
  const sourcePos = {
    row: sourceEl.style.gridRow,
    col: sourceEl.style.gridColumn
  };
  const targetPos = {
    row: targetEl.style.gridRow,
    col: targetEl.style.gridColumn
  };
  // Apply swap directly to DOM (no full re-render)
  sourceEl.style.gridRow = targetPos.row;
  sourceEl.style.gridColumn = targetPos.col;
  targetEl.style.gridRow = sourcePos.row;
  targetEl.style.gridColumn = sourcePos.col;
  // Record manual override for both
  const extractStart = (gridVal) => {
    const m = String(gridVal).match(/^(\d+)/);
    return m ? parseInt(m[1]) : 1;
  };
  if (!overrides[sourceId]) overrides[sourceId]={};
  overrides[sourceId].row = extractStart(targetPos.row);
  overrides[sourceId].col = extractStart(targetPos.col);
  overrides[sourceId].locked = true;
  if (!overrides[targetId]) overrides[targetId]={};
  overrides[targetId].row = extractStart(sourcePos.row);
  overrides[targetId].col = extractStart(sourcePos.col);
  overrides[targetId].locked = true;
  // Update lock button visuals
  [sourceEl,targetEl].forEach(el=>{
    if(el)el.classList.add('locked');
    const lockBtn=el?.querySelector('.btn-lock');
    if(lockBtn){lockBtn.textContent='🔒';lockBtn.classList.add('active');}
  });
  recordInteraction(sourceId, 'drag');
  debouncedSave();
  dragSourceId = null;
}
function handleDragEnd(e) {
  const el = document.querySelector('.panel.dragging');
  if (el) el.classList.remove('dragging');
  document.querySelectorAll('.panel.drag-over').forEach(el=>el.classList.remove('drag-over'));
  dragSourceId = null;
}
// ── Debounced resize ───────────────────────────────────────
function handleResize() {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    // Only re-rank if viewport change could affect layout thresholds
    updateLayout();
  }, DEBOUNCE_MS);
}
// ── More toggle ────────────────────────────────────────────
document.getElementById('more-toggle').addEventListener('click', () => {
  moreOpen = !moreOpen;
  document.getElementById('more-drawer').classList.toggle('open', moreOpen);
});
// ── Sort mode ──────────────────────────────────────────────
document.getElementById('sort-mode').addEventListener('change', (e) => {
  sortMode = e.target.value;
  if (sortMode === 'manual') {
    // Lock all panels
    panels.forEach(p => {
      if (!overrides[p.id]) overrides[p.id] = {};
      overrides[p.id].locked = true;
      const el = getPanelElement(p.id);
      if (el) {
        const rm = String(el.style.gridRow).match(/^(\d+)/);
        const cm = String(el.style.gridColumn).match(/^(\d+)/);
        if (rm) overrides[p.id].row = parseInt(rm[1]);
        if (cm) overrides[p.id].col = parseInt(cm[1]);
      }
    });
  } else if (sortMode === 'recent') {
    // Sort by recency: override the ranking
    panels.sort((a,b)=>(b.lastInteraction||0)-(a.lastInteraction||0));
    // Clear position overrides but keep lock status
    Object.values(overrides).forEach(o=>{delete o.row;delete o.col;});
  } else {
    // Auto: clear all overrides
    overrides = {};
  }
  updateLayout();
  debouncedSave();
});
// ── Expand all ─────────────────────────────────────────────
document.getElementById('btn-expand-all').addEventListener('click', () => {
  panels.forEach(p => {
    const el = getPanelElement(p.id);
    if (el) {
      el.classList.remove('compact','collapsed');
    }
  });
  // Clear collapse/compact related overrides
  Object.values(overrides).forEach(o=>{delete o.row;delete o.col;});
  overrides = {};
  updateLayout();
  debouncedSave();
});
// ── Reset ──────────────────────────────────────────────────
document.getElementById('btn-reset').addEventListener('click', () => {
  if (!confirm('Reset all tracking data and clear saved layout?')) return;
  try { localStorage.removeItem(STORAGE_KEY); } catch(e){}
  panels = [];
  overrides = {};
  rankOrder = [];
  initializePanels();
  fullRender();
  showToast('All data reset — fresh start');
});
// ── Initialization ─────────────────────────────────────────
function initializePanels() {
  const saved = loadState();
  PANEL_DEFS.forEach(def => {
    let panelData = {frequency:0, totalDuration:0, lastInteraction:null};
    if (saved && saved.panels) {
      const sp = saved.panels.find(p=>p.id===def.id);
      if (sp) {
        panelData.frequency = sp.frequency||0;
        panelData.totalDuration = sp.totalDuration||0;
        panelData.lastInteraction = sp.lastInteraction||null;
      }
    }
    panels.push({id:def.id, ...panelData});
  });
  if (saved && saved.overrides) overrides = saved.overrides;
  if (saved && saved.sortMode) sortMode = saved.sortMode;
  document.getElementById('sort-mode').value = sortMode;
}
// ── Bootstrap ──────────────────────────────────────────────
initializePanels();
fullRender();
// Observe all panel elements after render
panels.forEach(p => {
  const el = getPanelElement(p.id);
  if (el) observePanel(el);
});
// Watch for new panels added to the DOM
const domObserver = new MutationObserver((mutations) => {
  mutations.forEach(m => {
    m.addedNodes.forEach(node => {
      if (node.nodeType === 1 && node.classList.contains('panel')) {
        observePanel(node);
      }
    });
  });
});
domObserver.observe(document.getElementById('grid'), {childList:true});
domObserver.observe(document.getElementById('more-drawer'), {childList:true});
window.addEventListener('resize', handleResize);
// Initial save
debouncedSave();
// Periodic re-rank (every 30s) to age out recency
setInterval(() => {
  updateLayout();
  debouncedSave();
}, 30000);
console.log('Adaptive Dashboard v1 ready — tracking active, layout learning');
</script>
</body>
</html>
```