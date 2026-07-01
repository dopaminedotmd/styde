<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --bg: #0d0f14;
  --surface: #161a22;
  --surface2: #1e2430;
  --surface3: #282f3e;
  --border: #2a3344;
  --text: #e2e6ed;
  --text2: #8892a8;
  --accent: #6c8cff;
  --accent2: #45e0a0;
  --warn: #f0b34b;
  --danger: #f06060;
  --radius: 8px;
  --radius-sm: 4px;
  --transition: 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg); color: var(--text); min-height: 100vh;
  display: flex; flex-direction: column;
}
.header {
  padding: 16px 24px; display: flex; align-items: center; gap: 16px;
  border-bottom: 1px solid var(--border); background: var(--surface);
  flex-wrap: wrap;
}
.header h1 { font-size: 18px; font-weight: 600; letter-spacing: 0.3px; }
.header .subtitle { font-size: 12px; color: var(--text2); }
.header-actions { margin-left: auto; display: flex; gap: 8px; align-items: center; }
.btn {
  padding: 6px 14px; border-radius: var(--radius-sm); border: 1px solid var(--border);
  background: var(--surface2); color: var(--text); cursor: pointer; font-size: 12px;
  transition: all 0.2s; white-space: nowrap;
}
.btn:hover { background: var(--surface3); border-color: var(--accent); }
.btn-primary { background: var(--accent); color: #fff; border-color: var(--accent); }
.btn-primary:hover { background: #7f9aff; }
.btn-danger { border-color: var(--danger); color: var(--danger); }
.btn-danger:hover { background: var(--danger); color: #fff; }
.btn-sm { padding: 3px 8px; font-size: 11px; }
.btn-icon { background: transparent; border: none; cursor: pointer; font-size: 14px; padding: 2px 4px; line-height: 1; }
.badge {
  font-size: 10px; padding: 2px 8px; border-radius: 10px;
  background: var(--surface3); color: var(--text2);
}
.grid-container {
  flex: 1; padding: 20px; display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(120px, auto); gap: 16px;
  transition: all var(--transition);
  position: relative;
}
.panel {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); overflow: hidden;
  transition: all var(--transition); position: relative;
  display: flex; flex-direction: column; min-height: 0;
}
.panel:hover { border-color: rgba(108,140,255,0.3); }
.panel.drag-over { border-color: var(--accent); box-shadow: 0 0 0 2px rgba(108,140,255,0.3); }
.panel.dragging { opacity: 0.4; }
.panel.locked { border-left: 3px solid var(--warn); }
.panel.compact { max-height: 60px; overflow: hidden; }
.panel.compact .panel-body { display: none; }
.panel.compact .panel-footer { display: none; }
.panel.compact .mini-preview { display: flex; }
.panel.miniature {
  max-height: 44px; grid-column: span 1; overflow: hidden;
}
.panel.miniature .panel-header { padding: 8px 12px; }
.panel.miniature .panel-body { display: none; }
.panel.miniature .panel-footer { display: none; }
.panel.miniature .mini-preview { display: flex; }
.mini-preview {
  display: none; align-items: center; gap: 8px;
  padding: 4px 12px 8px; font-size: 11px; color: var(--text2);
  overflow: hidden;
}
.mini-preview .mini-bar {
  flex:1; height: 6px; background: var(--surface3); border-radius: 3px; overflow: hidden;
}
.mini-preview .mini-bar .fill {
  height: 100%; background: var(--accent2); border-radius: 3px; transition: width 0.6s;
}
.panel-header {
  padding: 12px 14px 8px; display: flex; align-items: center; gap: 8px;
  cursor: grab; user-select: none;
}
.panel.locked .panel-header { cursor: default; }
.panel-header .icon {
  width: 28px; height: 28px; border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; flex-shrink: 0;
}
.panel-header .title { font-size: 13px; font-weight: 500; flex: 1; }
.panel-header .rank-badge {
  font-size: 10px; padding: 1px 6px; border-radius: 8px;
  background: var(--surface3); color: var(--text2);
}
.panel-header .panel-actions { display: flex; gap: 4px; align-items: center; }
.panel-body {
  padding: 8px 14px 12px; flex:1; display: flex; flex-direction: column;
  gap: 8px; min-height: 60px;
}
.panel-body .metric-value { font-size: 28px; font-weight: 700; line-height: 1; }
.panel-body .metric-label { font-size: 11px; color: var(--text2); }
.panel-body .chart-placeholder {
  flex:1; min-height: 50px; background: var(--surface2); border-radius: 4px;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; color: var(--text2); position: relative; overflow: hidden;
}
.chart-placeholder .spark {
  position: absolute; bottom: 0; left: 0; right: 0; height: 100%;
  display: flex; align-items: flex-end; gap: 2px; padding: 4px;
}
.chart-placeholder .spark .bar {
  flex:1; background: var(--accent); border-radius: 2px 2px 0 0;
  opacity: 0.3; transition: height 0.5s;
}
.panel-footer {
  padding: 6px 14px; border-top: 1px solid var(--border); font-size: 10px;
  color: var(--text2); display: flex; justify-content: space-between; align-items: center;
}
.panel-footer .stats { display: flex; gap: 12px; }
.panel-footer .stats span { white-space: nowrap; }
.panel-footer .score-text { text-align: right; }
.override-menu {
  position: absolute; top: 100%; right: 0; z-index: 100;
  background: var(--surface2); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 8px; min-width: 180px; display: none; flex-direction: column; gap: 4px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.override-menu.open { display: flex; }
.override-menu label { font-size: 11px; color: var(--text2); }
.override-menu select, .override-menu input[type=number] {
  width: 100%; padding: 4px 8px; background: var(--surface); border: 1px solid var(--border);
  border-radius: 4px; color: var(--text); font-size: 11px;
}
.heat-overlay {
  position: fixed; bottom: 20px; right: 20px; z-index: 50;
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 12px 16px; width: 280px; font-size: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5); display: none;
}
.heat-overlay.open { display: block; }
.heat-overlay h3 { font-size: 13px; margin-bottom: 8px; }
.heat-item {
  display: flex; align-items: center; gap: 8px; padding: 4px 0;
}
.heat-bar {
  flex:1; height: 8px; background: var(--surface3); border-radius: 4px; overflow: hidden;
}
.heat-bar .fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
.heat-label { width: 80px; font-size: 11px; color: var(--text2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.heat-score { width: 40px; text-align: right; font-size: 10px; color: var(--text2); }
.tooltip {
  position: fixed; padding: 6px 10px; background: var(--surface2);
  border: 1px solid var(--border); border-radius: 4px; font-size: 11px;
  pointer-events: none; z-index: 200; display: none;
  box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}
.drag-ghost {
  position: fixed; pointer-events: none; z-index: 999;
  opacity: 0.7; transform: scale(0.95);
}
@media (max-width: 900px) {
  .grid-container { grid-template-columns: repeat(2, 1fr); padding: 12px; gap: 12px; }
}
@media (max-width: 500px) {
  .grid-container { grid-template-columns: 1fr; padding: 8px; gap: 10px; }
  .header { padding: 12px 16px; }
  .header h1 { font-size: 15px; }
}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Metric Layout</h1>
  <span class="subtitle">self-organizing dashboard</span>
  <div class="header-actions">
    <button class="btn btn-sm" data-action="reset-all" title="Reset all tracking data">Reset data</button>
    <button class="btn btn-sm" data-action="toggle-heatmap" title="Show attention heatmap">Heatmap</button>
    <button class="btn btn-sm btn-primary" data-action="rearrange-now" title="Run layout optimization now">Rearrange</button>
    <span class="badge" id="sessionBadge">session: new</span>
  </div>
</div>
<div class="grid-container" id="grid"></div>
<div class="heat-overlay" id="heatOverlay">
  <h3>Attention Heatmap</h3>
  <div id="heatList"></div>
  <div style="margin-top:8px;font-size:10px;color:var(--text2);">score = freq &times; duration &times; recency</div>
</div>
<div class="tooltip" id="tooltip"></div>
<script>
(function() {
// ============================================================
// CONFIG
// ============================================================
const STORAGE_KEY = 'aml_layout_v2';
const SCORE_TICK_MS = 3000;
const ADAPT_INTERVAL_MS = 60000;
const TRACK_FLUSH_MS = 5000;
const PANEL_DRAGGABLE_SELECTOR = '.panel-header';
const DEFAULT_PANELS = [
  { id:'revenue',      title:'Revenue',        icon:'📈', iconBg:'#1a2a40', metric:'$284,592', label:'this month',  chart:'spark' },
  { id:'users',        title:'Active Users',    icon:'👥', iconBg:'#1a3528', metric:'12,847',   label:'right now',   chart:'spark' },
  { id:'conversion',   title:'Conversion',      icon:'🎯', iconBg:'#2a1a35', metric:'4.82%',    label:'+0.34% vs last', chart:'bar' },
  { id:'sessions',     title:'Sessions',        icon:'⏱️', iconBg:'#35281a', metric:'89.3k',    label:'this week',   chart:'spark' },
  { id:'bounce',       title:'Bounce Rate',     icon:'🔄', iconBg:'#351a1a', metric:'32.1%',    label:'-2.1% trend', chart:'bar' },
  { id:'aov',          title:'Avg Order Value', icon:'🛒', iconBg:'#1a3535', metric:'$147.20',  label:'+$12.40 WoW', chart:'spark' },
  { id:'retention',    title:'Retention',       icon:'📊', iconBg:'#2a2a1a', metric:'78.3%',    label:'D30 cohort',  chart:'bar' },
  { id:'churn',        title:'Churn Forecast',  icon:'⚠️', iconBg:'#3a2020', metric:'5.2%',     label:'projected',   chart:'spark' },
  { id:'pageviews',    title:'Page Views',      icon:'👁️', iconBg:'#1a2a30', metric:'1.42M',    label:'total',       chart:'spark' },
  { id:'top-source',   title:'Top Source',      icon:'🔗', iconBg:'#2a1a20', metric:'Organic',   label:'42.3% share', chart:'bar' },
  { id:'load-time',    title:'Load Time',       icon:'⚡', iconBg:'#1a3520', metric:'1.2s',      label:'p95',        chart:'bar' },
  { id:'errors',       title:'Error Rate',      icon:'🔴', iconBg:'#3a1a1a', metric:'0.04%',    label:'last 24h',    chart:'spark' },
];
// ============================================================
// STATE
// ============================================================
let panels = [];
let tracking = {};
let layoutOverrides = {};
let prevScores = {};
// DOM references — stable panel element map, one observer per panel
const panelElements = new Map();
const panelObservers = new Map();
const panelHoverRecords = new Map();
let scoreTickId = null;
let adaptTickId = null;
let flushTickId = null;
// ============================================================
// PERSISTENCE
// ============================================================
function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      panels, tracking, layoutOverrides, savedAt: Date.now()
    }));
  } catch(e) {}
}
function loadState() {
  let saved = null;
  try { saved = JSON.parse(localStorage.getItem(STORAGE_KEY)); } catch(e) {}
  if (saved && saved.panels && saved.tracking) {
    panels = saved.panels;
    tracking = saved.tracking;
    layoutOverrides = saved.layoutOverrides || {};
    document.getElementById('sessionBadge').textContent = 'session: restored';
  } else {
    panels = DEFAULT_PANELS.map(p => ({ ...p }));
    tracking = {};
    layoutOverrides = {};
    panels.forEach(p => {
      tracking[p.id] = { views: 1, durationMs: 5000, clicks: 0, expands: 0, lastSeen: Date.now(), score: 1 };
    });
    document.getElementById('sessionBadge').textContent = 'session: new';
  }
}
// ============================================================
// SCORING ENGINE
// ============================================================
function computeScore(pid) {
  const t = tracking[pid];
  if (!t) return 0;
  const now = Date.now();
  const hoursSinceLastSeen = (now - t.lastSeen) / 3600000;
  const recencyFactor = Math.max(0.1, 1 - hoursSinceLastSeen / 168);
  const freq = Math.max(0.1, t.views + t.expands);
  const dur = Math.max(100, t.durationMs) / 1000;
  return freq * dur * recencyFactor;
}
function rankPanels() {
  return panels.map(p => ({ ...p, score: computeScore(p.id) }))
    .sort((a, b) => b.score - a.score);
}
// ============================================================
// LAYOUT ENGINE — DOM-diffing arrange
// ============================================================
function arrange() {
  const grid = document.getElementById('grid');
  const ranked = rankPanels();
  const assignments = {};
  const overridden = new Set();
  let rowIdx = 1, colIdx = 0;
  Object.entries(layoutOverrides).forEach(([pid, ov]) => {
    if (ov.position !== undefined && panels.find(p => p.id === pid)) {
      overridden.add(pid);
      assignments[pid] = {
        gridColumn: ov.position.col + ' / span ' + (ov.position.span || 1),
        gridRow: (ov.position.row || 1) + ' / span ' + (ov.position.rows || 1),
        compact: !!ov.compact, miniature: !!ov.miniature, locked: !!ov.locked, manual: true
      };
    }
  });
  const autoRanked = ranked.filter(p => !overridden.has(p.id));
  function nextPosition(cs, rs) {
    colIdx += cs;
    if (colIdx >= 4) { colIdx = 0; rowIdx++; }
    if (colIdx + cs > 4) { colIdx = 0; rowIdx++; }
    return { col: colIdx + 1, row: rowIdx, span: cs, rows: rs };
  }
  autoRanked.forEach((p, i) => {
    let cs = 1, rs = 1, compact = false, miniature = false;
    if (i === 0) { cs = 2; rs = 2; }
    else if (i === 1) { cs = 2; rs = 2; }
    else if (i < 4) { cs = 2; rs = 1; }
    else if (i < 8) { cs = 1; rs = 1; }
    else if (i < 12) { cs = 1; rs = 1; compact = true; }
    else { cs = 1; rs = 1; miniature = true; }
    const ov = layoutOverrides[p.id];
    if (ov && ov.compact) compact = true;
    if (ov && ov.miniature) miniature = true;
    const pos = nextPosition(cs, rs);
    assignments[p.id] = {
      gridColumn: pos.col + ' / span ' + pos.span,
      gridRow: pos.row + ' / span ' + pos.rows,
      compact, miniature, locked: ov ? !!ov.locked : false, manual: false
    };
  });
  // --- DOM diff: patch existing elements, create new, remove stale ---
  const newPanelIds = new Set(ranked.map(p => p.id));
  // 1. Remove panels no longer in layout
  for (const [pid, el] of panelElements) {
    if (!newPanelIds.has(pid)) {
      const obs = panelObservers.get(pid);
      if (obs) { obs.disconnect(); panelObservers.delete(pid); }
      el.remove();
      panelElements.delete(pid);
    }
  }
  // 2. Arrange in DOM order matching ranked order
  // Use a document fragment to batch DOM moves
  const frag = document.createDocumentFragment();
  ranked.forEach(p => {
    const a = assignments[p.id];
    if (!a) return;
    let el = panelElements.get(p.id);
    if (!el) {
      el = createPanelElement(p);
      panelElements.set(p.id, el);
      prevScores[p.id] = computeScore(p.id);
    }
    // Update position
    el.style.gridColumn = a.gridColumn;
    el.style.gridRow = a.gridRow;
    // Update size modes
    el.classList.toggle('compact', a.compact);
    el.classList.toggle('miniature', a.miniature);
    el.classList.toggle('locked', a.locked);
    // Update rank badge
    const rankEl = el.querySelector('.rank-badge');
    if (rankEl) {
      const rank = ranked.findIndex(r => r.id === p.id) + 1;
      rankEl.textContent = '#' + rank;
    }
    frag.appendChild(el);
  });
  // 3. Single DOM write
  grid.textContent = '';
  grid.appendChild(frag);
  updateHeatmap();
  saveState();
}
// ============================================================
// PANEL ELEMENT FACTORY — creates once, returns stable refs
// ============================================================
function createPanelElement(p) {
  const pid = p.id;
  const isLocked = layoutOverrides[pid] && layoutOverrides[pid].locked;
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.panelId = pid;
  if (isLocked) el.classList.add('locked');
  // --- Panel Header (stable, created once) ---
  const header = document.createElement('div');
  header.className = 'panel-header';
  header.draggable = true;
  header.dataset.draggable = 'true';
  const icon = document.createElement('div');
  icon.className = 'icon';
  icon.style.background = p.iconBg || '#1e2430';
  icon.textContent = p.icon;
  const title = document.createElement('span');
  title.className = 'title';
  title.textContent = p.title;
  const rankBadge = document.createElement('span');
  rankBadge.className = 'rank-badge';
  rankBadge.textContent = '#0';
  const actions = document.createElement('div');
  actions.className = 'panel-actions';
  const lockBtn = document.createElement('button');
  lockBtn.className = 'btn btn-sm' + (isLocked ? ' btn-danger' : '');
  lockBtn.dataset.action = 'toggle-lock';
  lockBtn.textContent = isLocked ? '\uD83D\uDD13' : '\uD83D\uDD12';
  const menuBtn = document.createElement('button');
  menuBtn.className = 'btn btn-sm';
  menuBtn.dataset.action = 'toggle-menu';
  menuBtn.textContent = '\u2699\uFE0F';
  actions.appendChild(lockBtn);
  actions.appendChild(menuBtn);
  header.appendChild(icon);
  header.appendChild(title);
  header.appendChild(rankBadge);
  header.appendChild(actions);
  el.appendChild(header);
  // --- Mini Preview (stable) ---
  const mini = document.createElement('div');
  mini.className = 'mini-preview';
  const miniSpan = document.createElement('span');
  miniSpan.className = 'mini-score';
  miniSpan.textContent = '0.0';
  const miniBar = document.createElement('div');
  miniBar.className = 'mini-bar';
  const miniFill = document.createElement('div');
  miniFill.className = 'fill';
  miniFill.style.width = '0%';
  miniFill.dataset.scoreFill = '';
  miniBar.appendChild(miniFill);
  mini.appendChild(miniSpan);
  mini.appendChild(miniBar);
  el.appendChild(mini);
  // --- Panel Body (stable, created once) ---
  const body = document.createElement('div');
  body.className = 'panel-body';
  const metricVal = document.createElement('div');
  metricVal.className = 'metric-value';
  metricVal.textContent = p.metric;
  const metricLabel = document.createElement('div');
  metricLabel.className = 'metric-label';
  metricLabel.textContent = p.label;
  const chartHolder = document.createElement('div');
  chartHolder.className = 'chart-placeholder';
  const spark = document.createElement('div');
  spark.className = 'spark';
  // Generate spark bars once
  const barCount = 16;
  for (let i = 0; i < barCount; i++) {
    const bar = document.createElement('div');
    bar.className = 'bar';
    bar.style.height = (15 + Math.random() * 70) + '%';
    bar.style.background = 'rgba(108,140,255,' + (0.2 + Math.random() * 0.4) + ')';
    spark.appendChild(bar);
  }
  chartHolder.appendChild(spark);
  body.appendChild(metricVal);
  body.appendChild(metricLabel);
  body.appendChild(chartHolder);
  el.appendChild(body);
  // --- Panel Footer (stable refs kept for score tick updates) ---
  const footer = document.createElement('div');
  footer.className = 'panel-footer';
  const stats = document.createElement('div');
  stats.className = 'stats';
  stats.dataset.panelStats = pid;
  // Create three stat spans as stable DOM refs
  const viewsSpan = document.createElement('span');
  viewsSpan.dataset.stat = 'views';
  const durSpan = document.createElement('span');
  durSpan.dataset.stat = 'duration';
  const clickSpan = document.createElement('span');
  clickSpan.dataset.stat = 'clicks';
  stats.appendChild(viewsSpan);
  stats.appendChild(durSpan);
  stats.appendChild(clickSpan);
  const scoreSpan = document.createElement('span');
  scoreSpan.className = 'score-text';
  scoreSpan.dataset.panelScore = pid;
  scoreSpan.textContent = 'score 0.0';
  footer.appendChild(stats);
  footer.appendChild(scoreSpan);
  el.appendChild(footer);
  // --- Override Menu (stable) ---
  const menu = document.createElement('div');
  menu.className = 'override-menu';
  menu.dataset.panel = pid;
  const lockLabel = document.createElement('label');
  lockLabel.textContent = 'Lock position';
  menu.appendChild(lockLabel);
  const menuLockBtn = document.createElement('button');
  menuLockBtn.className = 'btn btn-sm' + (isLocked ? ' btn-danger' : '');
  menuLockBtn.dataset.action = 'menu-lock';
  menuLockBtn.textContent = isLocked ? 'Unlock' : 'Lock';
  menu.appendChild(menuLockBtn);
  const sizeLabel = document.createElement('label');
  sizeLabel.textContent = 'Size';
  menu.appendChild(sizeLabel);
  const sizeSelect = document.createElement('select');
  sizeSelect.className = 'size-select';
  sizeSelect.dataset.action = 'size-select';
  const optAuto = document.createElement('option');
  optAuto.value = 'auto'; optAuto.textContent = 'Auto (adaptive)';
  const optCompact = document.createElement('option');
  optCompact.value = 'compact'; optCompact.textContent = 'Compact';
  const optMini = document.createElement('option');
  optMini.value = 'miniature'; optMini.textContent = 'Miniature';
  sizeSelect.appendChild(optAuto);
  sizeSelect.appendChild(optCompact);
  sizeSelect.appendChild(optMini);
  menu.appendChild(sizeSelect);
  const colLabel = document.createElement('label');
  colLabel.textContent = 'Position column (1-4)';
  menu.appendChild(colLabel);
  const colSelect = document.createElement('select');
  colSelect.className = 'pos-col';
  colSelect.dataset.action = 'pos-col';
  for (const v of ['auto','1','2','3','4']) {
    const o = document.createElement('option');
    o.value = v === 'auto' ? '' : v;
    o.textContent = v;
    colSelect.appendChild(o);
  }
  menu.appendChild(colSelect);
  const spanLabel = document.createElement('label');
  spanLabel.textContent = 'Column span';
  menu.appendChild(spanLabel);
  const spanSelect = document.createElement('select');
  spanSelect.className = 'pos-span';
  spanSelect.dataset.action = 'pos-span';
  for (const v of ['auto','1','2','3','4']) {
    const o = document.createElement('option');
    o.value = v === 'auto' ? '' : v;
    o.textContent = v;
    spanSelect.appendChild(o);
  }
  menu.appendChild(spanSelect);
  const btnRow = document.createElement('div');
  btnRow.style.cssText = 'display:flex;gap:4px;margin-top:4px';
  const applyBtn = document.createElement('button');
  applyBtn.className = 'btn btn-sm btn-primary';
  applyBtn.dataset.action = 'apply-override';
  applyBtn.textContent = 'Apply';
  const resetBtn = document.createElement('button');
  resetBtn.className = 'btn btn-sm';
  resetBtn.dataset.action = 'reset-override';
  resetBtn.textContent = 'Reset';
  btnRow.appendChild(applyBtn);
  btnRow.appendChild(resetBtn);
  menu.appendChild(btnRow);
  el.appendChild(menu);
  // Set up IntersectionObserver for this panel — stable across layout changes
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        tracking[pid].views += 1;
        tracking[pid].lastSeen = Date.now();
        panelHoverRecords.set(pid, { viewStart: performance.now(), hoverStart: null });
      } else {
        const rec = panelHoverRecords.get(pid);
        if (rec && rec.viewStart !== null) {
          tracking[pid].durationMs += (performance.now() - rec.viewStart);
          rec.viewStart = null;
        }
      }
    });
  }, { threshold: 0.3 });
  obs.observe(el);
  panelObservers.set(pid, obs);
  // Hover tracking ref
  panelHoverRecords.set(pid, { viewStart: null, hoverStart: null });
  // Store tracking ref in DOM for event delegation stats updates
  el.dataset.trackingPid = pid;
  return el;
}
// ============================================================
// SCORE TICK — update only panels whose score changed
// ============================================================
function scoreTick() {
  const ranked = rankPanels();
  for (const p of ranked) {
    const newScore = p.score;
    const oldScore = prevScores[p.id];
    if (newScore === oldScore) continue;
    prevScores[p.id] = newScore;
    updatePanelDisplay(p.id, newScore, ranked);
  }
}
function updatePanelDisplay(pid, score, ranked) {
  const el = panelElements.get(pid);
  if (!el) return;
  const t = tracking[pid];
  if (!t) return;
  if (!ranked) ranked = rankPanels();
  const rank = ranked.findIndex(r => r.id === pid) + 1;
  // Rank badge — direct textContent update
  const rankEl = el.querySelector('.rank-badge');
  if (rankEl) rankEl.textContent = '#' + rank;
  // Footer stats — update by textContent on stable child elements
  const viewsEl = el.querySelector('[data-stat="views"]');
  const durEl = el.querySelector('[data-stat="duration"]');
  const clickEl = el.querySelector('[data-stat="clicks"]');
  if (viewsEl) viewsEl.textContent = '\uD83D\uDC41\uFE0F ' + t.views;
  if (durEl) durEl.textContent = '\u23F1\uFE0F ' + (t.durationMs / 1000).toFixed(1) + 's';
  if (clickEl) clickEl.textContent = '\uD83C\uDFAF ' + t.clicks;
  // Score text
  const scoreEl = el.querySelector('[data-panel-score="' + pid + '"]');
  if (scoreEl) scoreEl.textContent = 'score ' + score.toFixed(1);
  // Mini preview
  const miniScore = el.querySelector('.mini-score');
  const miniFill = el.querySelector('[data-score-fill]');
  if (miniScore) miniScore.textContent = score.toFixed(1);
  if (miniFill) miniFill.style.width = Math.min(100, (score / 50) * 100) + '%';
  // Update menu lock button state if needed
  const menuLock = el.querySelector('[data-action="menu-lock"]');
  if (menuLock) {
    const locked = el.classList.contains('locked');
    menuLock.textContent = locked ? 'Unlock' : 'Lock';
    menuLock.className = 'btn btn-sm' + (locked ? ' btn-danger' : '');
  }
}
// ============================================================
// HEATMAP OVERLAY
// ============================================================
function updateHeatmap() {
  const list = document.getElementById('heatList');
  if (!list) return;
  if (!document.getElementById('heatOverlay').classList.contains('open')) return;
  const ranked = rankPanels();
  const maxScore = Math.max(1, ...ranked.map(p => p.score));
  // Rebuild heatmap is fine — it's a small, non-performance-critical overlay
  list.textContent = '';
  const frag = document.createDocumentFragment();
  ranked.forEach(p => {
    const pct = (p.score / maxScore) * 100;
    const hue = 120 - (pct / 100) * 120;
    const item = document.createElement('div');
    item.className = 'heat-item';
    const lbl = document.createElement('span');
    lbl.className = 'heat-label';
    lbl.textContent = p.icon + ' ' + p.title;
    const bar = document.createElement('div');
    bar.className = 'heat-bar';
    const fill = document.createElement('div');
    fill.className = 'fill';
    fill.style.width = pct + '%';
    fill.style.background = 'hsl(' + hue + ',70%,50%)';
    bar.appendChild(fill);
    const sc = document.createElement('span');
    sc.className = 'heat-score';
    sc.textContent = p.score.toFixed(1);
    item.appendChild(lbl);
    item.appendChild(bar);
    item.appendChild(sc);
    frag.appendChild(item);
  });
  list.appendChild(frag);
}
// ============================================================
// EVENT DELEGATION — single listener on grid container
// ============================================================
function handleGridClick(e) {
  const panelEl = e.target.closest('.panel');
  if (!panelEl) return;
  const pid = panelEl.dataset.panelId;
  if (!pid) return;
  const actionEl = e.target.closest('[data-action]');
  if (!actionEl) {
    // Plain click on panel body — count as interaction
    if (!e.target.closest('button, select, .override-menu, .panel-header')) {
      if (tracking[pid]) {
        tracking[pid].clicks += 1;
        tracking[pid].lastSeen = Date.now();
      }
      return;
    }
    return;
  }
  const action = actionEl.dataset.action;
  switch (action) {
    case 'toggle-lock': {
      e.stopPropagation();
      if (!layoutOverrides[pid]) layoutOverrides[pid] = {};
      layoutOverrides[pid].locked = !layoutOverrides[pid].locked;
      panelEl.classList.toggle('locked');
      // Update lock button text
      const lockBtn = panelEl.querySelector('[data-action="toggle-lock"]');
      if (lockBtn) {
        lockBtn.textContent = layoutOverrides[pid].locked ? '\uD83D\uDD13' : '\uD83D\uDD12';
        lockBtn.className = 'btn btn-sm' + (layoutOverrides[pid].locked ? ' btn-danger' : '');
      }
      // Sync menu lock
      const menuLock = panelEl.querySelector('[data-action="menu-lock"]');
      if (menuLock) {
        menuLock.textContent = layoutOverrides[pid].locked ? 'Unlock' : 'Lock';
        menuLock.className = 'btn btn-sm' + (layoutOverrides[pid].locked ? ' btn-danger' : '');
      }
      saveState();
      break;
    }
    case 'toggle-menu': {
      e.stopPropagation();
      const menu = panelEl.querySelector('.override-menu');
      if (menu) {
        const isOpen = menu.classList.toggle('open');
        // Sync menu state with current layout
        if (isOpen) {
          const ov = layoutOverrides[pid];
          const sizeSel = menu.querySelector('.size-select');
          if (sizeSel) {
            if (ov && ov.compact) sizeSel.value = 'compact';
            else if (ov && ov.miniature) sizeSel.value = 'miniature';
            else sizeSel.value = 'auto';
          }
          const colSel = menu.querySelector('.pos-col');
          const spanSel = menu.querySelector('.pos-span');
          if (ov && ov.position) {
            if (colSel) colSel.value = String(ov.position.col || '');
            if (spanSel) spanSel.value = String(ov.position.span || '');
          } else {
            if (colSel) colSel.value = '';
            if (spanSel) spanSel.value = '';
          }
        }
      }
      break;
    }
    case 'menu-lock': {
      e.stopPropagation();
      if (!layoutOverrides[pid]) layoutOverrides[pid] = {};
      layoutOverrides[pid].locked = !layoutOverrides[pid].locked;
      panelEl.classList.toggle('locked');
      const lockBtn = panelEl.querySelector('[data-action="toggle-lock"]');
      if (lockBtn) {
        lockBtn.textContent = layoutOverrides[pid].locked ? '\uD83D\uDD13' : '\uD83D\uDD12';
        lockBtn.className = 'btn btn-sm' + (layoutOverrides[pid].locked ? ' btn-danger' : '');
      }
      actionEl.textContent = layoutOverrides[pid].locked ? 'Unlock' : 'Lock';
      actionEl.className = 'btn btn-sm' + (layoutOverrides[pid].locked ? ' btn-danger' : '');
      saveState();
      break;
    }
    case 'size-select': {
      e.stopPropagation();
      // Just store — no immediate rearrange
      break;
    }
    case 'apply-override': {
      e.stopPropagation();
      const menu = panelEl.querySelector('.override-menu');
      const col = menu ? menu.querySelector('.pos-col').value : '';
      const span = menu ? menu.querySelector('.pos-span').value : '';
      const sizeSel = menu ? menu.querySelector('.size-select').value : 'auto';
      if (!layoutOverrides[pid]) layoutOverrides[pid] = {};
      if (col) {
        layoutOverrides[pid].position = {
          col: parseInt(col),
          span: span ? parseInt(span) : 1,
          row: 1
        };
      } else {
        delete layoutOverrides[pid].position;
      }
      layoutOverrides[pid].compact = (sizeSel === 'compact');
      layoutOverrides[pid].miniature = (sizeSel === 'miniature');
      if (menu) menu.classList.remove('open');
      // Close all other menus
      document.querySelectorAll('.override-menu.open').forEach(m => m.classList.remove('open'));
      arrange();
      break;
    }
    case 'reset-override': {
      e.stopPropagation();
      delete layoutOverrides[pid];
      const menu = panelEl.querySelector('.override-menu');
      if (menu) menu.classList.remove('open');
      arrange();
      break;
    }
  }
}
// Close menus on outside click
function handleDocClick(e) {
  if (!e.target.closest('.override-menu') && !e.target.closest('[data-action="toggle-menu"]')) {
    document.querySelectorAll('.override-menu.open').forEach(m => m.classList.remove('open'));
  }
}
// ============================================================
// DRAG AND DROP
// ============================================================
let dragSourcePid = null;
function handleDragStart(e) {
  const header = e.target.closest(PANEL_DRAGGABLE_SELECTOR);
  if (!header) return;
  const panelEl = header.closest('.panel');
  if (!panelEl) return;
  const pid = panelEl.dataset.panelId;
  if (!pid) return;
  if (panelEl.classList.contains('locked')) { e.preventDefault(); return; }
  dragSourcePid = pid;
  panelEl.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', pid);
  // Custom drag ghost
  const ghost = panelEl.cloneNode(true);
  ghost.style.width = panelEl.offsetWidth + 'px';
  ghost.style.height = panelEl.offsetHeight + 'px';
  ghost.style.position = 'fixed';
  ghost.style.pointerEvents = 'none';
  ghost.style.opacity = '0.7';
  ghost.style.transform = 'scale(0.95)';
  ghost.style.zIndex = '999';
  ghost.style.border = '1px solid ' + getComputedStyle(document.documentElement).getPropertyValue('--accent').trim();
  ghost.classList.remove('dragging');
  ghost.id = 'drag-ghost';
  document.body.appendChild(ghost);
  e.dataTransfer.setDragImage(ghost, 0, 0);
}
function handleDragOver(e) {
  const panelEl = e.target.closest('.panel');
  if (!panelEl) return;
  const pid = panelEl.dataset.panelId;
  if (!pid || pid === dragSourcePid) return;
  if (panelEl.classList.contains('locked')) return;
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  panelEl.classList.add('drag-over');
}
function handleDragLeave(e) {
  const panelEl = e.target.closest('.panel');
  if (!panelEl) return;
  panelEl.classList.remove('drag-over');
}
function handleDrop(e) {
  e.preventDefault();
  document.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
  const targetEl = e.target.closest('.panel');
  if (!targetEl) return;
  const targetPid = targetEl.dataset.panelId;
  if (!targetPid || !dragSourcePid || targetPid === dragSourcePid) return;
  if (targetEl.classList.contains('locked')) return;
  // Swap positions in layoutOverrides
  const srcPos = layoutOverrides[dragSourcePid] && layoutOverrides[dragSourcePid].position;
  const tgtPos = layoutOverrides[targetPid] && layoutOverrides[targetPid].position;
  if (!layoutOverrides[dragSourcePid]) layoutOverrides[dragSourcePid] = {};
  if (!layoutOverrides[targetPid]) layoutOverrides[targetPid] = {};
  // Swap manual positions so the two panels exchange grid spots
  const temp = layoutOverrides[dragSourcePid].position;
  layoutOverrides[dragSourcePid].position = layoutOverrides[targetPid].position;
  layoutOverrides[targetPid].position = temp;
  dragSourcePid = null;
  arrange();
}
function handleDragEnd(e) {
  document.querySelectorAll('.dragging, .drag-over').forEach(el => {
    el.classList.remove('dragging', 'drag-over');
  });
  const ghost = document.getElementById('drag-ghost');
  if (ghost) ghost.remove();
  dragSourcePid = null;
}
// ============================================================
// HEADER CONTROLS (via delegation on document)
// ============================================================
function handleHeaderClick(e) {
  const actionEl = e.target.closest('[data-action]');
  if (!actionEl) return;
  const action = actionEl.dataset.action;
  switch (action) {
    case 'reset-all': {
      if (!confirm('Reset all tracking data and layout overrides?')) return;
      localStorage.removeItem(STORAGE_KEY);
      tracking = {};
      layoutOverrides = {};
      panels = DEFAULT_PANELS.map(p => ({ ...p }));
      panels.forEach(p => {
        tracking[p.id] = { views: 1, durationMs: 5000, clicks: 0, expands: 0, lastSeen: Date.now(), score: 1 };
      });
      prevScores = {};
      // Clean up all observers and panel elements
      for (const obs of panelObservers.values()) obs.disconnect();
      panelObservers.clear();
      panelElements.clear();
      panelHoverRecords.clear();
      document.getElementById('sessionBadge').textContent = 'session: reset';
      arrange();
      break;
    }
    case 'toggle-heatmap': {
      const overlay = document.getElementById('heatOverlay');
      overlay.classList.toggle('open');
      if (overlay.classList.contains('open')) updateHeatmap();
      break;
    }
    case 'rearrange-now': {
      arrange();
      break;
    }
  }
}
// ============================================================
// VISIBILITY HANDLING
// ============================================================
function handleVisibilityChange() {
  if (document.hidden) {
    flushTracking();
  } else {
    arrange();
  }
}
// ============================================================
// FLUSH
// ============================================================
function flushTracking() {
  // Finalize any ongoing hover/view durations
  for (const [pid, rec] of panelHoverRecords) {
    if (rec.viewStart !== null) {
      tracking[pid].durationMs += (performance.now() - rec.viewStart);
      rec.viewStart = null;
    }
    if (rec.hoverStart !== null) {
      tracking[pid].durationMs += (performance.now() - rec.hoverStart);
      rec.hoverStart = null;
    }
  }
  saveState();
}
// ============================================================
// MOUSEENTER/MOUSELEAVE via delegation (hover tracking)
// ============================================================
function handleGridMouseEnter(e) {
  const panelEl = e.target.closest('.panel');
  if (!panelEl) return;
  const pid = panelEl.dataset.panelId;
  if (!pid) return;
  const rec = panelHoverRecords.get(pid);
  if (rec) rec.hoverStart = performance.now();
}
function handleGridMouseLeave(e) {
  const panelEl = e.target.closest('.panel');
  if (!panelEl) return;
  const pid = panelEl.dataset.panelId;
  if (!pid) return;
  const rec = panelHoverRecords.get(pid);
  if (rec && rec.hoverStart !== null) {
    tracking[pid].durationMs += (performance.now() - rec.hoverStart);
    rec.hoverStart = null;
  }
}
// ============================================================
// INIT
// ============================================================
function init() {
  loadState();
  prevScores = {};
  panels.forEach(p => { prevScores[p.id] = computeScore(p.id); });
  // Wire event delegation
  const grid = document.getElementById('grid');
  grid.addEventListener('click', handleGridClick);
  grid.addEventListener('mouseenter', handleGridMouseEnter, true);
  grid.addEventListener('mouseleave', handleGridMouseLeave, true);
  grid.addEventListener('dragstart', handleDragStart);
  grid.addEventListener('dragover', handleDragOver);
  grid.addEventListener('dragleave', handleDragLeave);
  grid.addEventListener('drop', handleDrop);
  grid.addEventListener('dragend', handleDragEnd);
  document.addEventListener('click', handleDocClick);
  document.addEventListener('click', handleHeaderClick);
  document.addEventListener('visibilitychange', handleVisibilityChange);
  // First render
  arrange();
  // Single score tick at the higher frequency — only updates changed scores
  scoreTickId = setInterval(scoreTick, SCORE_TICK_MS);
  // Separate adapt timer for layout rearrangement
  adaptTickId = setInterval(arrange, ADAPT_INTERVAL_MS);
  // Periodic flush
  flushTickId = setInterval(flushTracking, TRACK_FLUSH_MS);
}
document.addEventListener('DOMContentLoaded', init);
})();
</script>
</body>
</html>