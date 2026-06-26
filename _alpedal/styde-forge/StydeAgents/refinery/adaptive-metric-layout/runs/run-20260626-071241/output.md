```html
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
/* HEADER */
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
.badge {
  font-size: 10px; padding: 2px 8px; border-radius: 10px;
  background: var(--surface3); color: var(--text2);
}
/* GRID */
.grid-container {
  flex:1; padding: 20px; display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(120px, auto); gap: 16px;
  transition: all var(--transition);
  position: relative;
}
/* PANEL */
.panel {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); overflow: hidden;
  transition: all var(--transition); position: relative;
  display: flex; flex-direction: column; min-height: 0;
}
.panel:hover { border-color: rgba(108,140,255,0.3); }
.panel.dragging { opacity: 0.5; transform: scale(0.97); }
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
.panel-header .title { font-size: 13px; font-weight: 500; flex:1; }
.panel-header .rank-badge {
  font-size: 10px; padding: 1px 6px; border-radius: 8px;
  background: var(--surface3); color: var(--text2);
}
.panel-header .panel-actions { display: flex; gap: 4px; }
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
/* OVERRIDE MENU */
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
/* USAGE HEATMAP OVERLAY */
.heat-overlay {
  position: fixed; bottom: 20px; right: 20px; z-index: 50;
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  padding: 12px 16px; width: 280px; font-size: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5); display: none;
}
.heat-overlay.open { display: block; }
.heat-overlay h3 { font-size: 13px; margin-bottom: 8px; }
.heat-overlay .heat-item {
  display: flex; align-items: center; gap: 8px; padding: 4px 0;
}
.heat-overlay .heat-bar {
  flex:1; height: 8px; background: var(--surface3); border-radius: 4px; overflow: hidden;
}
.heat-overlay .heat-bar .fill { height: 100%; border-radius: 4px; transition: width 0.5s; }
.heat-overlay .heat-label { width: 80px; font-size: 11px; color: var(--text2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.heat-overlay .heat-score { width: 40px; text-align: right; font-size: 10px; color: var(--text2); }
/* TOOLTIP */
.tooltip {
  position: fixed; padding: 6px 10px; background: var(--surface2);
  border: 1px solid var(--border); border-radius: 4px; font-size: 11px;
  pointer-events: none; z-index: 200; display: none;
  box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}
/* EMPTY STATE */
.empty-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  grid-column: 1 / -1; padding: 60px; color: var(--text2); gap: 12px;
}
.empty-state .icon { font-size: 48px; opacity: 0.3; }
.empty-state .text { font-size: 14px; }
/* RESPONSIVE */
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
    <button class="btn btn-sm" id="resetBtn" title="Reset all tracking data">Reset data</button>
    <button class="btn btn-sm" id="heatBtn" title="Show attention heatmap">Heatmap</button>
    <button class="btn btn-sm btn-primary" id="rearrangeBtn" title="Run layout optimization now">Rearrange</button>
    <span class="badge" id="sessionBadge">session: new</span>
  </div>
</div>
<div class="grid-container" id="grid"></div>
<div class="heat-overlay" id="heatOverlay">
  <h3>Attention Heatmap</h3>
  <div id="heatList"></div>
  <div style="margin-top:8px;font-size:10px;color:var(--text2);">
    score = freq &times; duration &times; recency
  </div>
</div>
<div class="tooltip" id="tooltip"></div>
<script>
// ============================================================
// CONFIG
// ============================================================
const STORAGE_KEY = 'aml_layout_v1';
const ADAPT_INTERVAL_MS = 60000; // auto-rearrange every 60s
const TRACK_FLUSH_MS = 5000;
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
let tracking = {};              // { panelId: { views, durationMs, clicks, expands, lastSeen, score } }
let layoutOverrides = {};       // { panelId: { locked, position, compact } }
let isDragging = false;
let dragPanelId = null;
let adaptTimer = null;
// ============================================================
// INIT
// ============================================================
function init() {
  loadState();
  renderGrid();
  startTracking();
  startAdaptTimer();
  bindGlobalEvents();
}
// ============================================================
// STATE PERSISTENCE
// ============================================================
function loadState() {
  let saved = null;
  try { saved = JSON.parse(localStorage.getItem(STORAGE_KEY)); } catch(e) {}
  if (saved && saved.panels && saved.tracking && saved.layoutOverrides) {
    panels = saved.panels;
    tracking = saved.tracking;
    layoutOverrides = saved.layoutOverrides || {};
    document.getElementById('sessionBadge').textContent = 'session: restored';
  } else {
    panels = DEFAULT_PANELS.map(p => ({ ...p }));
    tracking = {};
    layoutOverrides = {};
    panels.forEach(p => {
      tracking[p.id] = { views:1, durationMs:5000, clicks:0, expands:0, lastSeen:Date.now(), score:1 };
    });
    document.getElementById('sessionBadge').textContent = 'session: new';
  }
}
function saveState() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      panels, tracking, layoutOverrides, savedAt: Date.now()
    }));
  } catch(e) { /* quota exceeded, ignore */ }
}
function flushTracking() {
  saveState();
}
// ============================================================
// RANKING ENGINE
// ============================================================
function computeScore(pid) {
  const t = tracking[pid];
  if (!t) return 0;
  const now = Date.now();
  const hoursSinceLastSeen = (now - t.lastSeen) / 3600000;
  const recencyFactor = Math.max(0.1, 1 - hoursSinceLastSeen / 168); // 1-week decay
  const freq = Math.max(0.1, t.views + t.expands);
  const dur = Math.max(100, t.durationMs) / 1000;
  return freq * dur * recencyFactor;
}
function rankPanels() {
  const scored = panels.map(p => ({
    ...p,
    score: computeScore(p.id)
  }));
  scored.sort((a, b) => b.score - a.score);
  return scored;
}
// ============================================================
// LAYOUT ENGINE
// ============================================================
function arrange() {
  const ranked = rankPanels();
  const grid = document.getElementById('grid');
  const total = ranked.length;
  // Determine positions based on rank + overrides
  const assignments = {}; // panelId -> { gridColumn, gridRow, compact, miniature }
  // Column distribution: 4-col grid
  // Top 2: span 2 cols, 2 rows
  // 3-4: span 2 cols, 1 row
  // 5-8: span 1 col, 1 row
  // 9+: compact/miniature
  const colMap = [1,2,3,4];
  let rowIdx = 1;
  let colIdx = 0;
  // First pass: manual overrides
  const overridden = new Set();
  Object.entries(layoutOverrides).forEach(([pid, ov]) => {
    if (ov.position !== undefined && panels.find(p => p.id === pid)) {
      overridden.add(pid);
      assignments[pid] = {
        gridColumn: `${ov.position.col || 1} / span ${ov.position.span || 1}`,
        gridRow: `${ov.position.row || 1} / span ${ov.position.rows || 1}`,
        compact: ov.compact || false,
        miniature: ov.miniature || false,
        locked: ov.locked || false,
        manual: true
      };
    }
  });
  // Second pass: auto-layout for non-overridden, by rank
  const autoRanked = ranked.filter(p => !overridden.has(p.id));
  // Auto grid builder
  function nextPosition(colSpan, rowSpan) {
    colIdx += colSpan;
    if (colIdx >= 4) {
      colIdx = 0;
      rowIdx += 1;
    }
    // Check for column overflow
    if (colIdx + colSpan > 4) {
      colIdx = 0;
      rowIdx += 1;
    }
    return { col: colIdx + 1, row: rowIdx, span: colSpan, rows: rowSpan };
  }
  autoRanked.forEach((p, i) => {
    let colSpan = 1, rowSpan = 1;
    let compact = false, miniature = false;
    if (i === 0) { colSpan = 2; rowSpan = 2; }
    else if (i === 1) { colSpan = 2; rowSpan = 2; }
    else if (i < 4) { colSpan = 2; rowSpan = 1; }
    else if (i < 8) { colSpan = 1; rowSpan = 1; }
    else if (i < 12) { colSpan = 1; rowSpan = 1; compact = true; }
    else { colSpan = 1; rowSpan = 1; miniature = true; }
    // Check if this panel has a lock override
    const ov = layoutOverrides[p.id];
    if (ov && ov.compact) compact = true;
    if (ov && ov.miniature) miniature = true;
    const pos = nextPosition(colSpan, rowSpan);
    assignments[p.id] = {
      gridColumn: `${pos.col} / span ${pos.span}`,
      gridRow: `${pos.row} / span ${pos.rows}`,
      compact, miniature,
      locked: ov ? ov.locked : false,
      manual: false
    };
  });
  // Render
  grid.innerHTML = '';
  ranked.forEach(p => {
    const a = assignments[p.id];
    if (!a) return;
    const el = createPanelElement(p, a);
    el.style.gridColumn = a.gridColumn;
    el.style.gridRow = a.gridRow;
    grid.appendChild(el);
  });
  updateHeatmap();
  saveState();
}
// ============================================================
// PANEL ELEMENT FACTORY
// ============================================================
function createPanelElement(p, layout) {
  const t = tracking[p.id] || { views:0, durationMs:0, clicks:0, expands:0, lastSeen:0, score:0 };
  const score = computeScore(p.id);
  const rank = rankPanels().findIndex(r => r.id === p.id) + 1;
  const isLocked = layout.locked || (layoutOverrides[p.id] && layoutOverrides[p.id].locked);
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.panelId = p.id;
  if (isLocked) el.classList.add('locked');
  if (layout.compact) el.classList.add('compact');
  if (layout.miniature) el.classList.add('miniature');
  // Mini preview bar
  const miniFillPct = Math.min(100, (score / 50) * 100);
  el.innerHTML = `
    <div class="panel-header">
      <div class="icon" style="background:${p.iconBg || '#1e2430'}">${p.icon}</div>
      <span class="title">${p.title}</span>
      <span class="rank-badge">#${rank}</span>
      <div class="panel-actions">
        <button class="btn btn-sm btn-lock ${isLocked?'btn-danger':'btn'}" title="Lock/unlock position">${isLocked?'🔓':'🔒'}</button>
        <button class="btn btn-sm btn-menu" title="Position override">⚙️</button>
      </div>
    </div>
    <div class="mini-preview">
      <span>${score.toFixed(1)}</span>
      <div class="mini-bar"><div class="fill" style="width:${miniFillPct}%"></div></div>
    </div>
    <div class="panel-body">
      <div class="metric-value">${p.metric}</div>
      <div class="metric-label">${p.label}</div>
      <div class="chart-placeholder" data-chart="${p.chart}">
        ${p.chart === 'spark' ? '<div class="spark"></div>' : '<div class="spark"></div>'}
      </div>
    </div>
    <div class="panel-footer">
      <div class="stats">
        <span>👁️ ${t.views}</span>
        <span>⏱️ ${(t.durationMs/1000).toFixed(1)}s</span>
        <span>🎯 ${t.clicks}</span>
      </div>
      <span>score ${score.toFixed(1)}</span>
    </div>
    <div class="override-menu" data-panel="${p.id}">
      <label>Lock position</label>
      <button class="btn btn-sm btn-lock-menu ${isLocked?'btn-danger':'btn'}">${isLocked?'Unlock':'Lock'}</button>
      <label>Size</label>
      <select class="size-select">
        <option value="auto" ${(!layout.compact && !layout.miniature) ? 'selected':''}>Auto (adaptive)</option>
        <option value="compact" ${layout.compact?'selected':''}>Compact</option>
        <option value="miniature" ${layout.miniature?'selected':''}>Miniature</option>
      </select>
      <label>Position column (1-4)</label>
      <select class="pos-col">
        <option value="">auto</option>
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
      </select>
      <label>Column span</label>
      <select class="pos-span">
        <option value="">auto</option>
        <option value="1">1</option>
        <option value="2">2</option>
        <option value="3">3</option>
        <option value="4">4</option>
      </select>
      <div style="display:flex;gap:4px;margin-top:4px">
        <button class="btn btn-sm btn-primary apply-override">Apply</button>
        <button class="btn btn-sm btn-reset-override">Reset</button>
      </div>
    </div>
  `;
  // Bind events
  bindPanelEvents(el, p, layout);
  return el;
}
// ============================================================
// PANEL EVENT BINDING
// ============================================================
function bindPanelEvents(el, p, layout) {
  const pid = p.id;
  // Ensure tracking entry
  if (!tracking[pid]) {
    tracking[pid] = { views:0, durationMs:0, clicks:0, expands:0, lastSeen:Date.now(), score:0 };
  }
  // --- View tracking (intersection + hover) ---
  let viewStart = null;
  let isVisible = false;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        isVisible = true;
        viewStart = performance.now();
        tracking[pid].views += 1;
        tracking[pid].lastSeen = Date.now();
        updateFooterStats(el, pid);
      } else {
        if (isVisible && viewStart !== null) {
          tracking[pid].durationMs += (performance.now() - viewStart);
          viewStart = null;
          isVisible = false;
          updateFooterStats(el, pid);
          flushTracking();
        }
      }
    });
  }, { threshold: 0.3 });
  obs.observe(el);
  // Hover tracking (fine-grained duration)
  let hoverStart = null;
  el.addEventListener('mouseenter', () => {
    hoverStart = performance.now();
  });
  el.addEventListener('mouseleave', () => {
    if (hoverStart !== null) {
      tracking[pid].durationMs += (performance.now() - hoverStart);
      hoverStart = null;
      updateFooterStats(el, pid);
      flushTracking();
    }
  });
  // Click tracking
  el.addEventListener('click', (e) => {
    // Don't count clicks on buttons/menus
    if (e.target.closest('button, select, .override-menu')) return;
    tracking[pid].clicks += 1;
    tracking[pid].lastSeen = Date.now();
    updateFooterStats(el, pid);
    flushTracking();
  });
  // --- Expand/collapse toggle on compact panels ---
  const header = el.querySelector('.panel-header');
  if (layout.compact || layout.miniature) {
    // Click on title area expands temporarily
    const titleArea = el.querySelector('.title');
    if (titleArea) {
      titleArea.style.cursor = 'pointer';
      titleArea.addEventListener('click', () => {
        el.classList.toggle('compact');
        el.classList.toggle('miniature');
        tracking[pid].expands += 1;
        tracking[pid].lastSeen = Date.now();
        updateFooterStats(el, pid);
        flushTracking();
        // Auto-collapse after 5s if not locked
        if (!el.classList.contains('locked')) {
          setTimeout(() => {
            if (!el.classList.contains('compact') && !el.classList.contains('miniature')) {
              if (layoutOverrides[pid] && layoutOverrides[pid].compact) {
                el.classList.add('compact');
              } else if (layoutOverrides[pid] && layoutOverrides[pid].miniature) {
                el.classList.add('miniature');
              } else {
                // Restore based on rank
                const r = rankPanels().findIndex(rr => rr.id === pid);
                if (r >= 8) el.classList.add('compact');
                if (r >= 12) el.classList.add('miniature');
              }
            }
          }, 5000);
        }
      });
    }
  }
  // --- Lock button ---
  const lockBtn = el.querySelector('.btn-lock');
  if (lockBtn) {
    lockBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (!layoutOverrides[pid]) layoutOverrides[pid] = {};
      layoutOverrides[pid].locked = !layoutOverrides[pid].locked;
      el.classList.toggle('locked');
      lockBtn.textContent = layoutOverrides[pid].locked ? '🔓' : '🔒';
      lockBtn.className = `btn btn-sm ${layoutOverrides[pid].locked ? 'btn-danger' : 'btn'}`;
      // Also update menu
      const menuLockBtn = el.querySelector('.btn-lock-menu');
      if (menuLockBtn) {
        menuLockBtn.textContent = layoutOverrides[pid].locked ? 'Unlock' : 'Lock';
        menuLockBtn.className = `btn btn-sm ${layoutOverrides[pid].locked ? 'btn-danger' : 'btn'}`;
      }
      saveState();
    });
  }
  // --- Menu toggle ---
  const menuBtn = el.querySelector('.btn-menu');
  const menu = el.querySelector('.override-menu');
  if (menuBtn && menu) {
    menuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      menu.classList.toggle('open');
    });
    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!menu.contains(e.target) && !menuBtn.contains(e.target)) {
        menu.classList.remove('open');
      }
    });
  }
  // --- Menu: Lock ---
  const menuLockBtn = el.querySelector('.btn-lock-menu');
  if (menuLockBtn) {
    menuLockBtn.addEventListener('click', () => {
      if (!layoutOverrides[pid]) layoutOverrides[pid] = {};
      layoutOverrides[pid].locked = !layoutOverrides[pid].locked;
      el.classList.toggle('locked');
      lockBtn.textContent = layoutOverrides[pid].locked ? '🔓' : '🔒';
      lockBtn.className = `btn btn-sm ${layoutOverrides[pid].locked ? 'btn-danger' : 'btn'}`;
      menuLockBtn.textContent = layoutOverrides[pid].locked ? 'Unlock' : 'Lock';
      menuLockBtn.className = `btn btn-sm ${layoutOverrides[pid].locked ? 'btn-danger' : 'btn'}`;
      saveState();
    });
  }
  // --- Menu: Size select ---
  const sizeSelect = el.querySelector('.size-select');
  if (sizeSelect) {
    sizeSelect.addEventListener('change', () => {
      if (!layoutOverrides[pid]) layoutOverrides[pid] = {};
      layoutOverrides[pid].compact = (sizeSelect.value === 'compact');
      layoutOverrides[pid].miniature = (sizeSelect.value === 'miniature');
    });
  }
  // --- Menu: Apply override ---
  const applyBtn = el.querySelector('.apply-override');
  if (applyBtn) {
    applyBtn.addEventListener('click', () => {
      const col = el.querySelector('.pos-col').value;
      const span = el.querySelector('.pos-span').value;
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
      menu.classList.remove('open');
      arrange(); // re-render
    });
  }
  // --- Menu: Reset override ---
  const resetBtn = el.querySelector('.btn-reset-override');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      delete layoutOverrides[pid];
      menu.classList.remove('open');
      arrange();
    });
  }
  // Generate sparkline bars
  const chartEl = el.querySelector('.chart-placeholder .spark');
  if (chartEl) {
    const count = layout.compact || layout.miniature ? 8 : 16;
    for (let i = 0; i < count; i++) {
      const h = 15 + Math.random() * 70;
      const bar = document.createElement('div');
      bar.className = 'bar';
      bar.style.height = h + '%';
      bar.style.background = `rgba(108,140,255,${0.2 + Math.random() * 0.4})`;
      chartEl.appendChild(bar);
    }
  }
}
// ============================================================
// FOOTER STATS UPDATE
// ============================================================
function updateFooterStats(el, pid) {
  const t = tracking[pid];
  if (!t) return;
  const footer = el.querySelector('.panel-footer .stats');
  if (footer) {
    footer.innerHTML = `
      <span>👁️ ${t.views}</span>
      <span>⏱️ ${(t.durationMs/1000).toFixed(1)}s</span>
      <span>🎯 ${t.clicks}</span>
    `;
  }
  const scoreEl = el.querySelector('.panel-footer span:last-child');
  if (scoreEl) {
    scoreEl.textContent = `score ${computeScore(pid).toFixed(1)}`;
  }
  // Update mini preview
  const miniScore = el.querySelector('.mini-preview span');
  const miniFill = el.querySelector('.mini-bar .fill');
  if (miniScore) miniScore.textContent = computeScore(pid).toFixed(1);
  if (miniFill) miniFill.style.width = Math.min(100, (computeScore(pid) / 50) * 100) + '%';
}
// ============================================================
// HEATMAP OVERLAY
// ============================================================
function updateHeatmap() {
  const list = document.getElementById('heatList');
  if (!list) return;
  const ranked = rankPanels();
  const maxScore = Math.max(1, ...ranked.map(p => computeScore(p.id)));
  list.innerHTML = ranked.map(p => {
    const score = computeScore(p.id);
    const pct = (score / maxScore) * 100;
    const hue = 120 - (pct / 100) * 120; // green (120) -> red (0)
    return `
      <div class="heat-item">
        <span class="heat-label">${p.icon} ${p.title}</span>
        <div class="heat-bar"><div class="fill" style="width:${pct}%;background:hsl(${hue},70%,50%)"></div></div>
        <span class="heat-score">${score.toFixed(1)}</span>
      </div>
    `;
  }).join('');
}
// ============================================================
// TRACKING — periodic flush
// ============================================================
function startTracking() {
  setInterval(flushTracking, TRACK_FLUSH_MS);
}
function startAdaptTimer() {
  adaptTimer = setInterval(() => {
    arrange();
  }, ADAPT_INTERVAL_MS);
}
// ============================================================
// RENDER
// ============================================================
function renderGrid() {
  arrange();
}
// ============================================================
// GLOBAL EVENTS
// ============================================================
function bindGlobalEvents() {
  // Reset
  document.getElementById('resetBtn').addEventListener('click', () => {
    if (!confirm('Reset all tracking data and layout overrides?')) return;
    localStorage.removeItem(STORAGE_KEY);
    tracking = {};
    layoutOverrides = {};
    panels = DEFAULT_PANELS.map(p => ({ ...p }));
    panels.forEach(p => {
      tracking[p.id] = { views:1, durationMs:5000, clicks:0, expands:0, lastSeen:Date.now(), score:1 };
    });
    document.getElementById('sessionBadge').textContent = 'session: reset';
    arrange();
  });
  // Heatmap toggle
  const heatBtn = document.getElementById('heatBtn');
  const heatOverlay = document.getElementById('heatOverlay');
  heatBtn.addEventListener('click', () => {
    heatOverlay.classList.toggle('open');
    if (heatOverlay.classList.contains('open')) updateHeatmap();
  });
  // Rearrange now
  document.getElementById('rearrangeBtn').addEventListener('click', () => {
    arrange();
  });
  // Track visibility change (tab switch)
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      flushTracking();
    } else {
      // Refresh on return
      arrange();
    }
  });
}
// ============================================================
// BOOT
// ============================================================
document.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>
```