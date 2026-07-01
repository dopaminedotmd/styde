<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface2: #22262f;
  --border: #2a2e39;
  --text: #e1e4ea;
  --text2: #8b8fa6;
  --accent: #6c8cff;
  --accent2: #44d4a8;
  --warn: #f0a050;
  --danger: #e85050;
  --radius: 10px;
  --gap: 12px;
  --transition: 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  min-height: 100vh;
  padding: 20px;
  user-select: none;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}
header h1 { font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; }
.toolbar { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.toolbar button {
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 7px 14px;
  border-radius: 7px;
  cursor: pointer;
  font-size: 0.82rem;
  transition: background var(--transition);
}
.toolbar button:hover { background: var(--border); }
.toolbar button.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.toolbar .reset-btn { color: var(--warn); border-color: var(--warn); }
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 160px;
  gap: var(--gap);
  transition: all var(--transition);
}
.dashboard.compact-view { grid-auto-rows: 90px; }
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 16px;
  position: relative;
  overflow: hidden;
  transition: all var(--transition);
  display: flex;
  flex-direction: column;
  cursor: grab;
}
.panel:active { cursor: grabbing; }
.panel.dragging {
  opacity: 0.7;
  z-index: 100;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  transform: scale(1.02);
  cursor: grabbing;
}
.panel.drag-over { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent); }
.panel.locked { cursor: default; border-left: 3px solid var(--warn); }
.panel.locked .lock-indicator { display: block; }
.panel.compact { grid-row: span 1 !important; padding: 8px 14px; flex-direction: row; align-items: center; gap: 12px; font-size: 0.82rem; }
.panel.compact .panel-body { flex-direction: row; gap: 10px; }
.panel.compact .panel-value { font-size: 1.3rem; }
.panel.compact .panel-label { font-size: 0.7rem; }
.panel.compact .panel-chart,
.panel.compact .panel-detail,
.panel.compact .panel-actions { display: none; }
.panel.compact .panel-preview { display: block; }
.panel.collapsed {
  grid-column: span 1 !important;
  grid-row: span 1 !important;
  padding: 8px 14px;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  height: 44px;
  min-height: unset;
}
.panel.collapsed .panel-body { display: none; }
.panel.collapsed .panel-collapsed-title { display: block; }
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 6px;
}
.panel-label {
  font-size: 0.75rem;
  color: var(--text2);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 500;
}
.panel-actions { display: flex; gap: 4px; opacity: 0; transition: opacity 0.2s; }
.panel:hover .panel-actions { opacity: 1; }
.panel-actions button {
  background: none;
  border: none;
  color: var(--text2);
  cursor: pointer;
  font-size: 0.85rem;
  padding: 2px 5px;
  border-radius: 4px;
  transition: all 0.2s;
}
.panel-actions button:hover { background: var(--surface2); color: var(--text); }
.panel-actions .lock-btn.locked-state { color: var(--warn); }
.panel-body { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 4px; }
.panel-value { font-size: 2rem; font-weight: 700; letter-spacing: -0.03em; line-height: 1; }
.panel-sub { font-size: 0.78rem; color: var(--text2); }
.panel-sub.up { color: var(--accent2); }
.panel-sub.down { color: var(--danger); }
.panel-chart { flex: 1; min-height: 0; margin-top: 6px; }
.panel-detail { font-size: 0.75rem; color: var(--text2); margin-top: 4px; }
.panel-collapsed-title { display: none; font-size: 0.78rem; font-weight: 500; }
.panel-preview { display: none; }
.lock-indicator {
  display: none;
  position: absolute;
  top: 6px;
  right: 6px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--warn);
}
.more-section {
  margin-top: 12px;
  padding: 12px 16px;
  background: var(--surface);
  border: 1px dashed var(--border);
  border-radius: var(--radius);
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
  min-height: 40px;
}
.more-section:empty { display: none; }
.more-section .more-label { font-size: 0.75rem; color: var(--text2); margin-right: 8px; }
.more-section .more-chip {
  background: var(--surface2);
  border: 1px solid var(--border);
  padding: 4px 10px;
  border-radius: 14px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s;
}
.more-section .more-chip:hover { border-color: var(--accent); color: var(--accent); }
.rank-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  font-size: 0.65rem;
  color: var(--text2);
  opacity: 0.5;
}
.panel.large .rank-badge { opacity: 0.8; color: var(--accent); }
.score-toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: var(--surface2);
  border: 1px solid var(--border);
  padding: 10px 18px;
  border-radius: var(--radius);
  font-size: 0.78rem;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s;
  pointer-events: none;
  z-index: 200;
}
.score-toast.show { opacity: 1; transform: translateY(0); }
.bar { height: 4px; background: var(--border); border-radius: 2px; overflow: hidden; margin-top: 4px; }
.bar-fill { height: 100%; border-radius: 2px; transition: width 0.6s ease; }
.sparkline { display: flex; align-items: flex-end; gap: 2px; height: 40px; }
.sparkline-bar { flex: 1; background: var(--accent); border-radius: 1px 1px 0 0; min-height: 2px; transition: height 0.5s ease; opacity: 0.7; }
.sparkline-bar:last-child { opacity: 1; }
.health-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }
.health-dot.ok { background: var(--accent2); }
.health-dot.warn { background: var(--warn); }
.health-dot.bad { background: var(--danger); }
.activity-line { font-size: 0.75rem; color: var(--text2); padding: 2px 0; border-bottom: 1px solid var(--border); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.progress-row { display: flex; align-items: center; gap: 8px; font-size: 0.73rem; margin: 2px 0; }
.progress-bar { flex: 1; height: 6px; background: var(--border); border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 3px; transition: width 0.5s ease; }
.status-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px 12px; font-size: 0.72rem; }
.status-grid span { color: var(--text2); }
.status-grid strong { color: var(--text); font-weight: 500; }
@media (max-width: 900px) { .dashboard { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 500px) { .dashboard { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="toolbar">
    <button onclick="toggleAutoLayout()" id="autoBtn" class="active">Auto-Layout: ON</button>
    <button onclick="resetTracking()" class="reset-btn">Reset All Tracking</button>
    <button onclick="forceRelayout()">Recalculate Now</button>
  </div>
</header>
<div class="dashboard" id="dashboard"></div>
<div class="more-section" id="moreSection"><span class="more-label">Collapsed:</span></div>
<div class="score-toast" id="scoreToast"></div>
<script>
(() => {
const STORAGE_KEY = 'adaptive_dashboard_v2';
const DECAY_HALF = 24 * 60 * 60 * 1000;
const RELAYOUT_DEBOUNCE = 2000;
const SCORE_DEBOUNCE = 5000;
let panels = [];
let tracking = {};
let autoLayout = true;
let observers = [];
let scoreTimeout = null;
let relayoutTimeout = null;
let dragState = null;
const panelDefs = [
  { id: 'revenue', label: 'Revenue', value: '$48,294', sub: '+12.3%', subClass: 'up', type: 'metric', color: '#6c8cff', detail: 'vs last month' },
  { id: 'users', label: 'Active Users', value: '18,472', sub: '+5.7%', subClass: 'up', type: 'metric', color: '#44d4a8', detail: 'Daily active' },
  { id: 'conversion', label: 'Conversion', value: '4.82%', sub: '-0.3%', subClass: 'down', type: 'metric', color: '#f0a050', detail: 'Checkout funnel' },
  { id: 'server', label: 'Server Load', value: '67%', sub: 'Normal', subClass: '', type: 'chart', color: '#6c8cff', detail: '4 nodes healthy' },
  { id: 'activity', label: 'Recent Activity', type: 'activity', color: '#a78bfa', detail: 'Last 24h' },
  { id: 'health', label: 'System Health', type: 'health', color: '#44d4a8', detail: 'All systems' },
  { id: 'errors', label: 'Error Rate', value: '0.12%', sub: 'Below threshold', subClass: 'up', type: 'metric', color: '#e85050', detail: 'Last 60 min' },
  { id: 'pipeline', label: 'Sales Pipeline', type: 'pipeline', color: '#6c8cff', detail: 'This quarter' }
];
function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const data = JSON.parse(raw);
      tracking = data.tracking || {};
      autoLayout = data.autoLayout !== false;
      return data;
    }
  } catch (e) {}
  const init = {};
  panelDefs.forEach(p => {
    init[p.id] = { views: 0, totalMs: 0, clicks: 0, lastView: 0, locked: false, collapsed: false, overridePos: null };
  });
  tracking = init;
  return { tracking: init, autoLayout: true };
}
function saveState() {
  const data = { tracking, autoLayout, savedAt: Date.now() };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}
function computeScore(panelId, now) {
  const t = tracking[panelId] || { views: 0, totalMs: 0, clicks: 0, lastView: 0 };
  const frequency = t.views + t.clicks * 2;
  const duration = Math.min(t.totalMs / 1000, 3600) / 3600;
  const ageMs = now - t.lastView;
  const recency = Math.exp(-Math.log(2) * ageMs / DECAY_HALF);
  return frequency * (1 + duration) * (0.3 + 0.7 * recency);
}
function getRanked() {
  const now = Date.now();
  return panelDefs.map(p => ({
    ...p,
    score: computeScore(p.id, now),
    track: tracking[p.id] || {}
  })).sort((a, b) => b.score - a.score);
}
function assignLayout(ranked) {
  const now = Date.now();
  const assignments = [];
  ranked.forEach((p, i) => {
    const trk = tracking[p.id] || {};
    if (trk.locked && trk.overridePos !== null) {
      assignments.push({ id: p.id, pos: trk.overridePos, size: 'large', locked: true });
      return;
    }
    if (trk.collapsed) {
      assignments.push({ id: p.id, pos: -1, size: 'collapsed', collapsed: true });
      return;
    }
    let size = 'medium';
    let pos = i;
    if (i === 0) { size = 'large'; pos = 0; }
    else if (i === 1) { size = 'large'; pos = 2; }
    else if (i <= 3) { size = 'medium'; pos = i + 1; }
    else if (i <= 5) { size = 'compact'; pos = i + 1; }
    else { size = 'collapsed'; pos = -1; }
    assignments.push({ id: p.id, pos, size, locked: false });
  });
  assignments.sort((a, b) => {
    if (a.pos === -1 && b.pos === -1) return 0;
    if (a.pos === -1) return 1;
    if (b.pos === -1) return -1;
    return a.pos - b.pos;
  });
  return assignments;
}
function getGridStyle(size) {
  switch (size) {
    case 'large': return 'grid-column: span 2; grid-row: span 2;';
    case 'medium': return 'grid-column: span 1; grid-row: span 1;';
    case 'compact': return 'grid-column: span 1; grid-row: span 1;';
    default: return 'grid-column: span 1; grid-row: span 1;';
  }
}
function buildSparkline(id) {
  const bars = [];
  for (let i = 0; i < 12; i++) {
    const h = 20 + Math.random() * 25;
    bars.push(`<div class="sparkline-bar" style="height:${h}px"></div>`);
  }
  return `<div class="sparkline">${bars.join('')}</div>`;
}
function buildActivity() {
  const lines = [
    'User jane.doe completed checkout — 2m ago',
    'New deployment v4.2.1 rolled out — 18m ago',
    'Alert: CPU spike on node-3 resolved — 34m ago',
    'User mark.t signed up via Google — 1h ago',
    'Database backup completed successfully — 2h ago'
  ];
  return lines.map(l => `<div class="activity-line">${l}</div>`).join('');
}
function buildHealth() {
  return `
    <div class="status-grid">
      <span class="health-dot ok"></span><strong>API Gateway</strong><span>OK</span><span>12ms</span>
      <span class="health-dot ok"></span><strong>Database</strong><span>OK</span><span>0.4ms</span>
      <span class="health-dot ok"></span><strong>Cache</strong><span>OK</span><span>99.8% hit</span>
      <span class="health-dot warn"></span><strong>Queue</strong><span>Warn</span><span>342 pending</span>
    </div>`;
}
function buildPipeline() {
  const stages = [
    { name: 'Leads', val: 1420, max: 2000, color: '#6c8cff' },
    { name: 'Contacted', val: 890, max: 1420, color: '#44d4a8' },
    { name: 'Demo', val: 340, max: 890, color: '#f0a050' },
    { name: 'Proposal', val: 120, max: 340, color: '#a78bfa' },
    { name: 'Closed', val: 48, max: 120, color: '#e85050' }
  ];
  return stages.map(s =>
    `<div class="progress-row"><span>${s.name}</span><div class="progress-bar"><div class="progress-fill" style="width:${(s.val/s.max*100).toFixed(0)}%;background:${s.color}"></div></div><span>${s.val}</span></div>`
  ).join('');
}
function buildPanelHTML(panel, track, size) {
  const sizeClass = size === 'large' ? 'large' : size === 'compact' ? 'compact' : size === 'collapsed' ? 'collapsed' : '';
  const locked = track.locked || false;
  const lockClass = locked ? 'locked' : '';
  const gridStyle = getGridStyle(size);
  const collapsed = track.collapsed || false;
  let bodyHTML = '';
  if (panel.type === 'metric' || panel.type === 'chart') {
    const subHTML = panel.sub ? `<span class="panel-sub ${panel.subClass || ''}">${panel.sub}</span>` : '';
    bodyHTML = `
      <div class="panel-value">${panel.value || ''}</div>
      ${subHTML}
      ${panel.detail ? `<div class="panel-detail">${panel.detail}</div>` : ''}
      ${panel.type === 'chart' ? buildSparkline(panel.id) : ''}`;
  } else if (panel.type === 'activity') {
    bodyHTML = `<div class="panel-detail" style="margin-top:0">${panel.detail || ''}</div>${buildActivity()}`;
  } else if (panel.type === 'health') {
    bodyHTML = `<div class="panel-detail" style="margin-top:0">${panel.detail || ''}</div>${buildHealth()}`;
  } else if (panel.type === 'pipeline') {
    bodyHTML = `<div class="panel-detail" style="margin-top:0">${panel.detail || ''}</div>${buildPipeline()}`;
  }
  return `
    <div class="panel ${sizeClass} ${lockClass}" data-panel-id="${panel.id}" style="${gridStyle}">
      <div class="lock-indicator"></div>
      <div class="rank-badge">#---</div>
      <div class="panel-header">
        <span class="panel-label">${panel.label}</span>
        <div class="panel-actions">
          <button class="lock-btn ${locked ? 'locked-state' : ''}" data-action="lock" title="Lock position">&#128274;</button>
          <button data-action="collapse" title="Collapse">&#9642;</button>
        </div>
      </div>
      <div class="panel-body">${bodyHTML}</div>
      <div class="panel-collapsed-title">${panel.label}</div>
      <div class="panel-preview">${panel.value || panel.detail || ''}</div>
    </div>`;
}
function render(ranked, assignments) {
  const dashboard = document.getElementById('dashboard');
  const moreSection = document.getElementById('moreSection');
  const existingEls = {};
  dashboard.querySelectorAll('.panel').forEach(el => {
    existingEls[el.dataset.panelId] = el;
  });
  const frag = document.createDocumentFragment();
  const collapsedFrag = document.createDocumentFragment();
  assignments.forEach((ass, idx) => {
    const panel = panelDefs.find(p => p.id === ass.id);
    const trk = tracking[ass.id] || {};
    const existing = existingEls[ass.id];
    if (ass.size === 'collapsed' || ass.pos === -1) {
      if (existing) {
        const clone = existing.cloneNode(true);
        clone.className = `panel collapsed ${trk.locked ? 'locked' : ''}`;
        clone.style.cssText = '';
        clone.querySelector('.panel-body') && (clone.querySelector('.panel-body').style.display = 'none');
        const ct = clone.querySelector('.panel-collapsed-title');
        if (ct) ct.style.display = 'block';
        clone.querySelector('.rank-badge') && (clone.querySelector('.rank-badge').textContent = '');
        collapsedFrag.appendChild(clone);
      } else {
        const div = document.createElement('div');
        div.innerHTML = buildPanelHTML(panel, trk, 'collapsed');
        collapsedFrag.appendChild(div.firstElementChild);
      }
      return;
    }
    if (existing && !trk.locked) {
      const el = existing;
      const newSizeClass = ass.size === 'large' ? 'large' : ass.size === 'compact' ? 'compact' : '';
      const newLockClass = trk.locked ? 'locked' : '';
      el.className = `panel ${newSizeClass} ${newLockClass}`;
      el.style.cssText = getGridStyle(ass.size);
      const badge = el.querySelector('.rank-badge');
      if (badge) badge.textContent = `#${idx + 1}`;
      const lockBtn = el.querySelector('.lock-btn');
      if (lockBtn) lockBtn.className = `lock-btn ${trk.locked ? 'locked-state' : ''}`;
      frag.appendChild(el);
    } else if (existing && trk.locked) {
      frag.appendChild(existing);
    } else {
      const div = document.createElement('div');
      div.innerHTML = buildPanelHTML(panel, trk, ass.size);
      const el = div.firstElementChild;
      const badge = el.querySelector('.rank-badge');
      if (badge) badge.textContent = `#${idx + 1}`;
      frag.appendChild(el);
    }
  });
  dashboard.innerHTML = '';
  dashboard.appendChild(frag);
  const moreChildren = moreSection.querySelectorAll('.more-chip');
  moreChildren.forEach(c => c.remove());
  const moreLabel = moreSection.querySelector('.more-label');
  if (!moreLabel) {
    const lbl = document.createElement('span');
    lbl.className = 'more-label';
    lbl.textContent = 'Collapsed:';
    moreSection.appendChild(lbl);
  }
  assignments.filter(a => a.size === 'collapsed' || a.pos === -1).forEach(ass => {
    const panel = panelDefs.find(p => p.id === ass.id);
    const chip = document.createElement('span');
    chip.className = 'more-chip';
    chip.textContent = panel.label;
    chip.title = 'Click to expand';
    chip.dataset.panelId = ass.id;
    chip.addEventListener('click', () => expandPanel(ass.id));
    moreSection.appendChild(chip);
  });
}
function computeAndRender() {
  const ranked = getRanked();
  const assignments = assignLayout(ranked);
  render(ranked, assignments);
  saveState();
  document.getElementById('autoBtn').textContent = autoLayout ? 'Auto-Layout: ON' : 'Auto-Layout: OFF';
  document.getElementById('autoBtn').className = autoLayout ? 'active' : '';
}
function expandPanel(id) {
  if (tracking[id]) tracking[id].collapsed = false;
  saveState();
  computeAndRender();
}
function toggleAutoLayout() {
  autoLayout = !autoLayout;
  if (autoLayout) {
    panelDefs.forEach(p => {
      if (tracking[p.id]) { tracking[p.id].locked = false; tracking[p.id].overridePos = null; }
    });
  }
  saveState();
  computeAndRender();
  showToast(autoLayout ? 'Auto-layout enabled — panels will adapt to usage' : 'Auto-layout disabled — manual mode');
}
function resetTracking() {
  panelDefs.forEach(p => {
    tracking[p.id] = { views: 0, totalMs: 0, clicks: 0, lastView: 0, locked: false, collapsed: false, overridePos: null };
  });
  saveState();
  computeAndRender();
  showToast('Tracking data reset');
}
function forceRelayout() {
  computeAndRender();
  showToast('Layout recalculated');
}
function showToast(msg) {
  const toast = document.getElementById('scoreToast');
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toast._timeout);
  toast._timeout = setTimeout(() => toast.classList.remove('show'), 2000);
}
function setupObservers() {
  observers.forEach(o => o.disconnect());
  observers = [];
  document.querySelectorAll('.panel').forEach(el => {
    const panelId = el.dataset.panelId;
    if (!panelId) return;
    let visibleStart = null;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && visibleStart === null) {
          visibleStart = Date.now();
        } else if (!entry.isIntersecting && visibleStart !== null) {
          const duration = Date.now() - visibleStart;
          if (tracking[panelId]) {
            tracking[panelId].totalMs = (tracking[panelId].totalMs || 0) + duration;
            tracking[panelId].views = (tracking[panelId].views || 0) + 1;
            tracking[panelId].lastView = Date.now();
          }
          visibleStart = null;
          scheduleScoreSave();
        }
      });
    }, { threshold: 0.3 });
    observer.observe(el);
    observers.push(observer);
    el.addEventListener('click', (e) => {
      if (e.target.closest('button')) return;
      if (tracking[panelId]) {
        tracking[panelId].clicks = (tracking[panelId].clicks || 0) + 1;
        tracking[panelId].lastView = Date.now();
      }
      scheduleScoreSave();
    });
  });
}
function scheduleScoreSave() {
  clearTimeout(scoreTimeout);
  scoreTimeout = setTimeout(() => {
    saveState();
    if (autoLayout) scheduleRelayout();
  }, SCORE_DEBOUNCE);
}
function scheduleRelayout() {
  clearTimeout(relayoutTimeout);
  relayoutTimeout = setTimeout(() => {
    if (autoLayout) computeAndRender();
  }, RELAYOUT_DEBOUNCE);
}
function setupDragDrop() {
  const dashboard = document.getElementById('dashboard');
  dashboard.addEventListener('pointerdown', (e) => {
    const panel = e.target.closest('.panel');
    if (!panel) return;
    const panelId = panel.dataset.panelId;
    if (tracking[panelId] && tracking[panelId].locked) return;
    if (e.target.closest('button')) return;
    dragState = {
      el: panel,
      id: panelId,
      startX: e.clientX,
      startY: e.clientY,
      moved: false
    };
    const onMove = (ev) => {
      if (!dragState) return;
      const dx = ev.clientX - dragState.startX;
      const dy = ev.clientY - dragState.startY;
      if (Math.abs(dx) > 5 || Math.abs(dy) > 5) {
        if (!dragState.moved) {
          dragState.moved = true;
          dragState.el.classList.add('dragging');
        }
        dragState.el.style.transform = `translate(${dx}px, ${dy}px)`;
        dragState.el.style.zIndex = '100';
        const target = document.elementFromPoint(ev.clientX, ev.clientY)?.closest('.panel');
        document.querySelectorAll('.panel.drag-over').forEach(p => p.classList.remove('drag-over'));
        if (target && target !== dragState.el) {
          target.classList.add('drag-over');
          dragState.target = target;
        } else {
          dragState.target = null;
        }
      }
    };
    const onUp = (ev) => {
      document.removeEventListener('pointermove', onMove);
      document.removeEventListener('pointerup', onUp);
      if (!dragState) return;
      dragState.el.classList.remove('dragging');
      dragState.el.style.transform = '';
      dragState.el.style.zIndex = '';
      document.querySelectorAll('.panel.drag-over').forEach(p => p.classList.remove('drag-over'));
      if (dragState.moved && dragState.target && dragState.target !== dragState.el) {
        const targetId = dragState.target.dataset.panelId;
        const srcId = dragState.id;
        const allPanels = [...dashboard.querySelectorAll('.panel')];
        const srcIdx = allPanels.indexOf(dragState.el);
        const tgtIdx = allPanels.indexOf(dragState.target);
        if (srcIdx !== -1 && tgtIdx !== -1 && srcIdx !== tgtIdx) {
          if (tracking[srcId]) {
            tracking[srcId].locked = true;
            tracking[srcId].overridePos = tgtIdx;
          }
          if (tracking[targetId]) {
            tracking[targetId].locked = true;
            tracking[targetId].overridePos = srcIdx;
          }
          saveState();
          computeAndRender();
          showToast('Positions swapped & locked');
        }
      }
      dragState = null;
    };
    document.addEventListener('pointermove', onMove);
    document.addEventListener('pointerup', onUp);
  });
  dashboard.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    const panel = e.target.closest('.panel');
    if (!panel) return;
    const panelId = panel.dataset.panelId;
    const action = btn.dataset.action;
    if (action === 'lock') {
      if (tracking[panelId]) {
        tracking[panelId].locked = !tracking[panelId].locked;
        if (!tracking[panelId].locked) tracking[panelId].overridePos = null;
        saveState();
        computeAndRender();
        showToast(tracking[panelId].locked ? 'Panel locked' : 'Panel unlocked');
      }
    } else if (action === 'collapse') {
      if (tracking[panelId]) {
        tracking[panelId].collapsed = !tracking[panelId].collapsed;
        saveState();
        computeAndRender();
      }
    }
  });
}
function init() {
  loadState();
  document.getElementById('autoBtn').classList.toggle('active', autoLayout);
  computeAndRender();
  setupDragDrop();
  setupObservers();
  setInterval(() => {
    if (autoLayout) {
      const now = Date.now();
      let anyChanged = false;
      panelDefs.forEach(p => {
        const oldScore = (p._cachedScore || 0);
        const newScore = computeScore(p.id, now);
        if (Math.abs(oldScore - newScore) > 0.01) anyChanged = true;
        p._cachedScore = newScore;
      });
      if (anyChanged) scheduleRelayout();
    }
  }, 30000);
}
init();
})();
</script>
</body>
</html>