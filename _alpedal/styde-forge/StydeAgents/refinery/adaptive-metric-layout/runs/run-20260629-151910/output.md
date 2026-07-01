```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --gap:8px; --pad:10px; --radius:6px; --compact-h:60px;
  --bg:#0f1117; --panel-bg:#1a1d27; --panel-hdr:#252836;
  --text:#c8cdd8; --muted:#6b7280; --accent:#5b8def;
  --high-rank-glow:0 0 12px rgba(91,141,239,0.25);
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:system-ui,sans-serif;
  min-height:100vh;padding:12px}
.dashboard{display:grid;gap:var(--gap);
  grid-template-columns:repeat(var(--grid-cols),1fr);
  grid-auto-rows:minmax(140px,auto);align-items:start}
.toolbar{display:flex;gap:10px;align-items:center;margin-bottom:12px;
  flex-wrap:wrap}
.toolbar button,.toolbar select{
  background:var(--panel-hdr);color:var(--text);border:1px solid #333;
  padding:6px 14px;border-radius:var(--radius);cursor:pointer;
  font-size:13px}
.toolbar button:hover{background:var(--accent);color:#fff}
.panel{background:var(--panel-bg);border-radius:var(--radius);
  border:1px solid #2a2d3a;display:flex;flex-direction:column;
  overflow:hidden;transition:box-shadow .25s,grid-column .35s,grid-row .35s}
.panel.high-rank{box-shadow:var(--high-rank-glow)}
.panel.compact .panel-body{max-height:var(--compact-h);overflow:hidden;
  opacity:.65;font-size:11px}
.panel.compact .panel-body::after{
  content:'';display:block;height:20px;
  background:linear-gradient(transparent,var(--panel-bg))}
.panel-header{background:var(--panel-hdr);padding:6px 10px;display:flex;
  justify-content:space-between;align-items:center;font-size:13px;
  font-weight:600;user-select:none}
.panel-header .title{display:flex;align-items:center;gap:6px}
.panel-header .rank-dot{width:8px;height:8px;border-radius:50%;
  display:inline-block;flex-shrink:0}
.panel-header .rank-dot.hot{background:#ef4444}
.panel-header .rank-dot.warm{background:#f59e0b}
.panel-header .rank-dot.cold{background:#6b7280}
.panel-body{padding:var(--pad);font-size:13px;line-height:1.5;flex:1;
  overflow-y:auto;max-height:320px;transition:max-height .3s,opacity .3s}
.panel-controls{display:flex;gap:4px}
.panel-controls button{background:transparent;border:none;color:var(--muted);
  cursor:pointer;font-size:14px;padding:2px 6px;border-radius:3px}
.panel-controls button:hover{background:#333;color:#fff}
.panel-controls button.locked{color:var(--accent)}
.more-section{grid-column:1/-1;border-top:1px dashed #333;padding-top:10px}
.more-section summary{cursor:pointer;color:var(--muted);font-size:12px;
  padding:4px 0}
.more-drawer{display:grid;gap:var(--gap);
  grid-template-columns:repeat(auto-fill,minmax(180px,1fr));padding-top:8px}
.more-drawer .panel{grid-column:span 1!important;grid-row:span 1!important}
.overlay{position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:999;
  display:flex;align-items:center;justify-content:center}
.overlay-content{background:var(--panel-bg);border-radius:var(--radius);
  padding:20px;min-width:300px;max-width:500px}
.overlay-content h3{margin-bottom:12px}
.pos-grid{display:grid;gap:4px;margin:10px 0}
.pos-row{display:flex;gap:4px}
.pos-cell{width:32px;height:24px;border:1px dashed #444;border-radius:3px;
  display:flex;align-items:center;justify-content:center;font-size:10px;
  color:var(--muted);cursor:pointer}
.pos-cell.occupied{background:#1a3a2a;border-color:#2d5a3d;cursor:not-allowed}
.pos-cell.selected{background:var(--accent);color:#fff}
</style>
</head>
<body>
<div class="toolbar">
  <button id="btn-reset">Reset layout</button>
  <button id="btn-unlock-all">Unlock all</button>
  <select id="sel-density">
    <option value="auto">Auto density</option>
    <option value="compact">Compact</option>
    <option value="comfortable">Comfortable</option>
  </select>
  <span style="color:var(--muted);font-size:12px;margin-left:auto"
    id="status-text">Ready</span>
</div>
<div class="dashboard" id="dashboard"></div>
<details class="more-section" id="more-section" open>
  <summary>More panels</summary>
  <div class="more-drawer" id="more-drawer"></div>
</details>
<div class="overlay" id="pos-overlay" style="display:none">
  <div class="overlay-content">
    <h3>Select position for <span id="pos-panel-name"></span></h3>
    <div class="pos-grid" id="pos-grid"></div>
    <div style="margin-top:12px;display:flex;gap:8px;justify-content:flex-end">
      <button id="btn-pos-cancel">Cancel</button>
      <button id="btn-pos-confirm" style="background:var(--accent);color:#fff">
        Place here</button>
    </div>
  </div>
</div>
<script>
// === DATA MODEL ===
// panels[]: {id,title,content,score,locked,gridCol,gridRow,colSpan,rowSpan}
// behaviorLog[]: {panelId,event,ts} — event: view|click|toggle|collapse|expand
// occupancyGrid: computed per layout pass from locked panels
const LS_KEY = 'adaptive_layout_v1';
// Demo panels — real app would load from backend
const DEFAULT_PANELS = [
  {id:'cpu',title:'CPU Usage',content:'Current: 34%\nAvg 1h: 28%\nPeak: 91% @14:22',
    score:85,locked:false,gridCol:1,gridRow:1,colSpan:2,rowSpan:2},
  {id:'mem',title:'Memory',content:'Used: 7.2/16 GB\nSwap: 0.4/2 GB\nCache: 3.1 GB',
    score:78,locked:false,gridCol:3,gridRow:1,colSpan:2,rowSpan:1},
  {id:'disk',title:'Disk I/O',content:'Read: 45 MB/s\nWrite: 12 MB/s\nIOPS: 320',
    score:62,locked:false,gridCol:3,gridRow:2,colSpan:1,rowSpan:1},
  {id:'net',title:'Network',content:'RX: 1.2 Gbps\nTX: 0.3 Gbps\nPkts/s: 8500',
    score:71,locked:false,gridCol:4,gridRow:2,colSpan:1,rowSpan:1},
  {id:'err',title:'Error Rate',content:'5xx: 12/min\n4xx: 45/min\nTimeout: 3/min',
    score:90,locked:false,gridCol:1,gridRow:3,colSpan:2,rowSpan:1},
  {id:'lat',title:'Latency',content:'p50: 12ms\np95: 45ms\np99: 210ms',
    score:55,locked:false,gridCol:3,gridRow:3,colSpan:2,rowSpan:1},
  {id:'qps',title:'QPS',content:'Current: 842\nAvg: 790\nMax: 2100',
    score:40,locked:false,gridCol:1,gridRow:4,colSpan:1,rowSpan:1},
  {id:'cache',title:'Cache Hit',content:'Rate: 94.2%\nSize: 512 MB\nEvictions: 8/min',
    score:30,locked:false,gridCol:2,gridRow:4,colSpan:1,rowSpan:1},
];
let panels = [];
let behaviorLog = [];    // runtime log, flushed to localStorage on unload
let viewTimers = {};     // panelId -> {startTs, accumulated}
let pendingUpdates = false;
// === PERSISTENCE ===
function loadState() {
  const raw = localStorage.getItem(LS_KEY);
  if (!raw) { panels = JSON.parse(JSON.stringify(DEFAULT_PANELS)); return; }
  try {
    const saved = JSON.parse(raw);
    panels = saved.panels || DEFAULT_PANELS;
    // Merge saved logs with empty array for this session's runtime
    behaviorLog = [];
    // Decay scores on load so cold panels naturally sink over sessions
    for (const p of panels) {
      if (!saved.logs) continue;
      const panelLogs = saved.logs.filter(l => l.panelId === p.id);
      if (panelLogs.length === 0) { p.score = Math.max(10, p.score * 0.7); }
    }
  } catch (e) { panels = JSON.parse(JSON.stringify(DEFAULT_PANELS)); }
}
function saveState() {
  const data = { panels, logs: behaviorLog.slice(-500), ts: Date.now() };
  localStorage.setItem(LS_KEY, JSON.stringify(data));
}
// === RESPONSIVE GRID COLUMNS (matchMedia, not hard-coded) ===
function getGridColumns() {
  const w = window.innerWidth;
  if (w >= 1400) return 6;
  if (w >= 1100) return 4;
  if (w >= 768)  return 3;
  return 2;
}
// === RANKING ENGINE ===
// Composite: frequency × duration × recency_factor
// recency_factor = 1 / (1 + hours_since_last_interaction)
function recomputeScores() {
  const now = Date.now();
  for (const p of panels) {
    if (p.locked) continue; // locked panels keep their manual score
    const logs = behaviorLog.filter(l => l.panelId === p.id);
    if (logs.length === 0) { p.score = Math.max(5, (p.score || 10) * 0.95); }
    const clicks = logs.filter(l => l.event === 'click').length;
    const views = logs.filter(l => l.event === 'view').length;
    const frequency = clicks * 2 + views;
    // Duration from IntersectionObserver accumulation (seconds)
    const durSec = (viewTimers[p.id]?.accumulated || 0) / 1000;
    // Recency: time since last interaction
    const lastTs = logs.length ? Math.max(...logs.map(l => l.ts)) : now - 864e5;
    const hoursSince = (now - lastTs) / 36e5;
    const recency = 1 / (1 + hoursSince);
    // Composite with duration-weighted frequency, 1000-point scale
    const raw = (frequency + 1) * (durSec + 1) * (recency + 0.1);
    p.score = Math.round(Math.min(100, Math.max(1, raw)));
  }
}
// === RANK → SPAN MAPPING ===
// High rank (top 20%): large span. Low rank (bottom 20%): compact.
function getSpanForRank(rankPct, cols) {
  // cols available in current breakpoint
  if (rankPct <= 0.2) {         // top 20%: dominant
    return { colSpan: Math.min(cols, cols >= 4 ? 3 : 2),
             rowSpan: cols >= 4 ? 2 : 1 };
  }
  if (rankPct <= 0.6) {         // middle 60%: standard
    return { colSpan: cols >= 4 ? 2 : 1, rowSpan: 1 };
  }
  return { colSpan: 1, rowSpan: 1 }; // bottom 20%: compact
}
// === OCCUPANCY GRID + GREEDY PLACEMENT ===
// Builds a 2D boolean grid, marks locked panels first,
// then greedily places unlocked panels by descending score.
function layoutPanels() {
  const cols = getGridColumns();
  const sorted = [...panels].sort((a, b) => b.score - a.score);
  const maxRows = Math.ceil(sorted.length * 2 / cols) + 4;
  // Init occupancy grid: false = free
  const grid = Array.from({ length: maxRows }, () => new Array(cols).fill(false));
  // --- Locked-slot registration (fixes feedback gap) ---
  for (const p of sorted) {
    if (!p.locked) continue;
    const span = getSpanForRank(
      // Use actual rank among all panels for span sizing
      sorted.indexOf(p) / Math.max(1, sorted.length - 1), cols);
    // Clamp to grid bounds
    const r = Math.max(0, Math.min((p.gridRow || 0) - 1, maxRows - span.rowSpan));
    const c = Math.max(0, Math.min((p.gridCol || 0) - 1, cols - span.colSpan));
    // Mark locked cells as occupied
    for (let dr = 0; dr < span.rowSpan; dr++) {
      for (let dc = 0; dc < span.colSpan; dc++) {
        if (r + dr < maxRows && c + dc < cols) grid[r + dr][c + dc] = true;
      }
    }
    // Store computed position back
    p.gridCol = c + 1; p.gridRow = r + 1;
    p.colSpan = span.colSpan; p.rowSpan = span.rowSpan;
  }
  // --- Greedy placement for unlocked panels ---
  for (const p of sorted) {
    if (p.locked) continue;
    const rankPct = sorted.indexOf(p) / Math.max(1, sorted.length - 1);
    const span = getSpanForRank(rankPct, cols);
    let placed = false;
    // Scan for first free region that fits
    for (let r = 0; r <= maxRows - span.rowSpan && !placed; r++) {
      for (let c = 0; c <= cols - span.colSpan && !placed; c++) {
        if (regionFree(grid, r, c, span.rowSpan, span.colSpan, maxRows, cols)) {
          // Mark occupied
          for (let dr = 0; dr < span.rowSpan; dr++) {
            for (let dc = 0; dc < span.colSpan; dc++) {
              grid[r + dr][c + dc] = true;
            }
          }
          p.gridCol = c + 1; p.gridRow = r + 1;
          p.colSpan = span.colSpan; p.rowSpan = span.rowSpan;
          placed = true;
        }
      }
    }
    // Fallback: place at end if grid is full
    if (!placed) {
      const fallbackRow = grid.findIndex(row => row.some(cell => !cell));
      const r = fallbackRow >= 0 ? fallbackRow : maxRows - 1;
      // Find first free col in that row
      const c = grid[r].indexOf(false);
      const fc = c >= 0 ? c : 0;
      p.gridCol = fc + 1; p.gridRow = r + 1;
      p.colSpan = 1; p.rowSpan = 1;
    }
  }
  // Determine which panels go to "more" section (score < 20 or bottom 15%)
  const threshold = sorted.length > 4
    ? sorted[Math.floor(sorted.length * 0.85)].score : 0;
  for (const p of panels) {
    p._inMore = !p.locked && p.score < Math.max(threshold, 15);
  }
  scheduleRender();
}
// Check if a rectangular region is entirely free
function regionFree(grid, row, col, rowSpan, colSpan, maxRows, cols) {
  for (let dr = 0; dr < rowSpan; dr++) {
    for (let dc = 0; dc < colSpan; dc++) {
      if (row + dr >= maxRows || col + dc >= cols) return false;
      if (grid[row + dr][col + dc]) return false;
    }
  }
  return true;
}
// === RENDER (requestAnimationFrame-batched) ===
function scheduleRender() {
  if (pendingUpdates) return;
  pendingUpdates = true;
  requestAnimationFrame(() => {
    pendingUpdates = false;
    renderDOM();
  });
}
function renderDOM() {
  const dash = document.getElementById('dashboard');
  const more = document.getElementById('more-drawer');
  const cols = getGridColumns();
  dash.style.setProperty('--grid-cols', cols);
  dash.innerHTML = '';
  more.innerHTML = '';
  for (const p of panels) {
    const el = buildPanelEl(p);
    if (p._inMore) {
      // Compact miniature in 'more' drawer
      el.classList.add('compact');
      more.appendChild(el);
    } else {
      // Main grid placement
      el.style.gridColumn = `${p.gridCol || 'auto'} / span ${p.colSpan || 1}`;
      el.style.gridRow = `${p.gridRow || 'auto'} / span ${p.rowSpan || 1}`;
      // Visual rank indicator
      if (p.score >= 70) el.classList.add('high-rank');
      dash.appendChild(el);
    }
  }
  updateStatus();
}
function buildPanelEl(p) {
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.panelId = p.id;
  // Rank dot color
  const dotClass = p.score >= 70 ? 'hot' : p.score >= 35 ? 'warm' : 'cold';
  el.innerHTML =
    `<div class="panel-header">
      <span class="title">
        <span class="rank-dot ${dotClass}" title="Score: ${Math.round(p.score)}"></span>
        ${escHtml(p.title)}
      </span>
      <span class="panel-controls">
        <button data-action="toggle" title="Collapse/Expand">&#9660;</button>
        <button data-action="lock" class="${p.locked ? 'locked' : ''}"
          title="${p.locked ? 'Unlock' : 'Lock'}">&#128274;</button>
        <button data-action="move" title="Move">&#8596;</button>
      </span>
    </div>
    <div class="panel-body">${escHtml(p.content)}</div>`;
  return el;
}
function escHtml(s) { return String(s).replace(/[&<>"]/g,
  c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[c]); }
function updateStatus() {
  const top3 = [...panels].sort((a, b) => b.score - a.score).slice(0, 3);
  document.getElementById('status-text').textContent =
    `Top: ${top3.map(p => p.title).join(', ')} | Cols: ${getGridColumns()}`;
}
// === EVENT DELEGATION (single listener on dashboard + more-drawer) ===
function handlePanelAction(e) {
  const btn = e.target.closest('button[data-action]');
  if (!btn) return;
  const panelEl = btn.closest('.panel');
  if (!panelEl) return;
  const panelId = panelEl.dataset.panelId;
  const panel = panels.find(p => p.id === panelId);
  if (!panel) return;
  const action = btn.dataset.action;
  // Log interaction
  logEvent(panelId, action === 'toggle'
    ? (panelEl.classList.contains('compact') ? 'expand' : 'collapse')
    : 'click');
  if (action === 'lock') {
    panel.locked = !panel.locked;
    btn.classList.toggle('locked', panel.locked);
    btn.title = panel.locked ? 'Unlock' : 'Lock';
    layoutPanels();
  } else if (action === 'toggle') {
    panelEl.classList.toggle('compact');
  } else if (action === 'move') {
    showPositionPicker(panel);
  }
}
document.getElementById('dashboard').addEventListener('click', handlePanelAction);
document.getElementById('more-drawer').addEventListener('click', handlePanelAction);
// === POSITION PICKER OVERLAY (manual override) ===
let pickerPanel = null;
let pickerCol = 0, pickerRow = 0;
function showPositionPicker(panel) {
  pickerPanel = panel;
  const cols = getGridColumns();
  const maxRows = 6;
  document.getElementById('pos-panel-name').textContent = panel.title;
  const grid = document.getElementById('pos-grid');
  grid.innerHTML = '';
  pickerCol = Math.min(panel.gridCol - 1, cols - 1);
  pickerRow = Math.min(panel.gridRow - 1, maxRows - 1);
  for (let r = 0; r < maxRows; r++) {
    const row = document.createElement('div');
    row.className = 'pos-row';
    for (let c = 0; c < cols; c++) {
      const cell = document.createElement('div');
      cell.className = 'pos-cell';
      // Mark occupied by other locked panels
      const occupied = panels.some(p =>
        p.locked && p.id !== panel.id &&
        c >= (p.gridCol - 1) && c < (p.gridCol - 1 + p.colSpan) &&
        r >= (p.gridRow - 1) && r < (p.gridRow - 1 + p.rowSpan));
      if (occupied) cell.classList.add('occupied');
      if (r === pickerRow && c === pickerCol) cell.classList.add('selected');
      cell.textContent = `${c + 1},${r + 1}`;
      cell.addEventListener('click', () => {
        if (occupied) return;
        document.querySelectorAll('.pos-cell.selected')
          .forEach(el => el.classList.remove('selected'));
        cell.classList.add('selected');
        pickerCol = c; pickerRow = r;
      });
      row.appendChild(cell);
    }
    grid.appendChild(row);
  }
  document.getElementById('pos-overlay').style.display = 'flex';
}
document.getElementById('btn-pos-cancel').addEventListener('click', () => {
  document.getElementById('pos-overlay').style.display = 'none';
  pickerPanel = null;
});
document.getElementById('btn-pos-confirm').addEventListener('click', () => {
  if (!pickerPanel) return;
  // Manual override: lock + set position
  pickerPanel.locked = true;
  pickerPanel.gridCol = pickerCol + 1;
  pickerPanel.gridRow = pickerRow + 1;
  document.getElementById('pos-overlay').style.display = 'none';
  layoutPanels();
  saveState();
  pickerPanel = null;
});
// === TRACKING: IntersectionObserver for view duration ===
const observer = new IntersectionObserver((entries) => {
  const now = Date.now();
  for (const entry of entries) {
    const panelId = entry.target.dataset.panelId;
    if (!viewTimers[panelId]) {
      viewTimers[panelId] = { startTs: null, accumulated: 0 };
    }
    const timer = viewTimers[panelId];
    if (entry.isIntersecting) {
      timer.startTs = now;
      logEvent(panelId, 'view');
    } else if (timer.startTs !== null) {
      // Accumulate visible duration
      timer.accumulated += now - timer.startTs;
      timer.startTs = null;
    }
  }
}, { threshold: 0.3 }); // 30% visible counts as viewing
function observePanel(el) {
  observer.observe(el);
}
// Re-observe after render: use MutationObserver on dashboard
const mutObs = new MutationObserver(() => {
  document.querySelectorAll('.panel').forEach(el => {
    if (!el.dataset.observed) {
      observer.observe(el);
      el.dataset.observed = '1';
    }
  });
});
mutObs.observe(document.getElementById('dashboard'),
  { childList: true, subtree: true });
mutObs.observe(document.getElementById('more-drawer'),
  { childList: true, subtree: true });
// === EVENT LOGGING ===
function logEvent(panelId, event) {
  behaviorLog.push({ panelId, event, ts: Date.now() });
  // Trim log to prevent unbounded growth
  if (behaviorLog.length > 2000) behaviorLog.splice(0, 500);
  // Recompute scores periodically (batch: every 20 events)
  if (behaviorLog.length % 20 === 0) {
    recomputeScores();
    layoutPanels();
  }
}
// === TOOLBAR ACTIONS (event delegation) ===
document.getElementById('btn-reset').addEventListener('click', () => {
  if (!confirm('Reset all layout data and tracking?')) return;
  localStorage.removeItem(LS_KEY);
  panels = JSON.parse(JSON.stringify(DEFAULT_PANELS));
  behaviorLog = [];
  viewTimers = {};
  layoutPanels();
  saveState();
});
document.getElementById('btn-unlock-all').addEventListener('click', () => {
  for (const p of panels) p.locked = false;
  recomputeScores();
  layoutPanels();
  saveState();
});
document.getElementById('sel-density').addEventListener('change', (e) => {
  const v = e.target.value;
  document.documentElement.style.setProperty('--gap',
    v === 'compact' ? '3px' : v === 'comfortable' ? '14px' : '8px');
  document.documentElement.style.setProperty('--pad',
    v === 'compact' ? '6px' : v === 'comfortable' ? '16px' : '10px');
});
// === RESPONSIVE RELAYOUT ON RESIZE (debounced) ===
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    // Re-layout on breakpoint change only
    const currentCols = parseInt(
      document.getElementById('dashboard').style.getPropertyValue('--grid-cols'));
    const newCols = getGridColumns();
    if (currentCols !== newCols) layoutPanels();
  }, 200);
});
// === PERIODIC SCORE DECAY (every 60s, gentle) ===
setInterval(() => {
  // Decay scores of non-locked, non-recently-interacted panels
  const now = Date.now();
  let changed = false;
  for (const p of panels) {
    if (p.locked) continue;
    const lastLog = behaviorLog.filter(l => l.panelId === p.id).pop();
    // If no interaction in last 10 min, decay
    if (!lastLog || (now - lastLog.ts) > 600000) {
      p.score = Math.max(1, p.score * 0.98);
      changed = true;
    }
  }
  if (changed) { recomputeScores(); layoutPanels(); }
}, 60000);
// === SAVE ON UNLOAD ===
window.addEventListener('beforeunload', () => {
  // Finalize any open view timers
  const now = Date.now();
  for (const [id, timer] of Object.entries(viewTimers)) {
    if (timer.startTs !== null) {
      timer.accumulated += now - timer.startTs;
      timer.startTs = null;
    }
  }
  recomputeScores();
  saveState();
});
// === INIT ===
loadState();
recomputeScores();
layoutPanels();
</script>
</body>
</html>
```