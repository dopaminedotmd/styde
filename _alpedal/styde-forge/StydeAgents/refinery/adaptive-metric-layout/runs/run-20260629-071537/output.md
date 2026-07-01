<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
:root {
  --bg: #0f1117; --surface: #1a1d27; --surface2: #22263b; --border: #2a2e40;
  --text: #e1e4ed; --text2: #8b90a5; --accent: #6c8cff; --accent2: #4ade80;
  --warn: #f59e0b; --danger: #ef4444; --radius: 10px; --gap: 12px;
  --compact-scale: 0.45; --transition: 0.35s cubic-bezier(0.4,0,0.2,1);
}
* { box-sizing:border-box; margin:0; padding:0 }
body { background:var(--bg); color:var(--text); font-family:system-ui,-apple-system,sans-serif;
  padding:16px; min-height:100vh }
header { display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;
  flex-wrap:wrap; gap:8px }
h1 { font-size:1.3rem; font-weight:600; letter-spacing:-0.01em }
.controls { display:flex; gap:8px; align-items:center; flex-wrap:wrap }
.btn { background:var(--surface2); border:1px solid var(--border); color:var(--text);
  padding:6px 14px; border-radius:6px; cursor:pointer; font-size:0.82rem; transition:0.15s }
.btn:hover { background:var(--border); border-color:var(--accent) }
.btn.active { background:var(--accent); color:#fff; border-color:var(--accent) }
.stats { font-size:0.75rem; color:var(--text2) }
.grid { display:grid; grid-template-columns:repeat(4,1fr);
  grid-auto-rows:minmax(160px,auto); gap:var(--gap); transition:var(--transition) }
.panel { background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
  overflow:hidden; transition:all var(--transition); position:relative;
  display:flex; flex-direction:column; cursor:grab; user-select:none }
.panel:active { cursor:grabbing }
.panel.dragging { opacity:0.5; border-style:dashed; transform:scale(0.97) }
.panel.drag-over { border-color:var(--accent); box-shadow:0 0 0 2px var(--accent) }
.panel.compact { transform:scale(var(--compact-scale)); transform-origin:top left;
  margin-bottom:calc((1 - var(--compact-scale)) * -100%); z-index:1 }
.panel.compact .panel-body { display:none }
.panel.compact .panel-preview { display:flex }
.panel.compact:hover { transform:scale(0.55); z-index:10; box-shadow:0 8px 32px rgba(0,0,0,0.5) }
.panel.locked { border-left:3px solid var(--warn) }
.panel-header { display:flex; align-items:center; padding:10px 12px; gap:8px;
  border-bottom:1px solid var(--border); background:var(--surface2) }
.panel-title { font-size:0.82rem; font-weight:600; flex:1; white-space:nowrap; overflow:hidden;
  text-overflow:ellipsis }
.panel-score { font-size:0.65rem; color:var(--text2); background:var(--surface);
  padding:2px 6px; border-radius:4px; white-space:nowrap }
.panel-actions { display:flex; gap:4px }
.panel-btn { background:none; border:none; color:var(--text2); cursor:pointer;
  padding:4px 6px; border-radius:4px; font-size:0.9rem; line-height:1; transition:0.15s }
.panel-btn:hover { color:var(--text); background:var(--border) }
.panel-btn.lock-btn.locked { color:var(--warn) }
.panel-drag { cursor:grab; color:var(--text2); font-size:0.85rem }
.panel-body { padding:12px; flex:1; display:flex; flex-direction:column; gap:8px;
  min-height:80px }
.panel-preview { display:none; padding:8px 12px; align-items:center; gap:8px; font-size:0.75rem;
  color:var(--text2) }
.panel-preview .mini-chart { width:40px; height:24px; flex-shrink:0 }
.panel-preview .mini-val { font-weight:600; color:var(--text); font-size:0.85rem }
.metric-val { font-size:1.6rem; font-weight:700; letter-spacing:-0.02em }
.metric-label { font-size:0.72rem; color:var(--text2); text-transform:uppercase;
  letter-spacing:0.05em }
.metric-sub { font-size:0.75rem; color:var(--accent2) }
.metric-sub.down { color:var(--danger) }
.bar-group { display:flex; gap:4px; align-items:flex-end; height:60px }
.bar { flex:1; border-radius:3px 3px 0 0; transition:height 0.5s; min-width:8px }
.tag { display:inline-block; padding:2px 8px; border-radius:4px; font-size:0.68rem;
  font-weight:600 }
.tag.ok { background:#4ade8020; color:var(--accent2) }
.tag.warn { background:#f59e0b20; color:var(--warn) }
.tag.bad { background:#ef444420; color:var(--danger) }
.sparkline { width:100%; height:36px }
.gauge-svg { width:80px; height:50px }
.event-row { display:flex; justify-content:space-between; padding:4px 0; font-size:0.72rem;
  border-bottom:1px solid var(--border) }
.event-row:last-child { border-bottom:none }
.event-time { color:var(--text2) }
.compact-zone { grid-column:1/-1; display:flex; flex-wrap:wrap; gap:var(--gap);
  padding:8px; border:1px dashed var(--border); border-radius:var(--radius);
  min-height:50px; align-items:flex-start }
.compact-zone-label { width:100%; font-size:0.7rem; color:var(--text2); text-transform:uppercase;
  letter-spacing:0.08em; margin-bottom:4px }
@media (max-width:900px) { .grid { grid-template-columns:repeat(2,1fr) } }
@media (max-width:500px) { .grid { grid-template-columns:1fr } }
</style>
</head>
<body>
<header>
  <div>
    <h1>Adaptive Dashboard</h1>
    <div class="stats" id="stats">Tracking 0 panels &middot; 0 interactions logged</div>
  </div>
  <div class="controls">
    <button class="btn" id="btnReset" title="Clear all tracking data and reset layout">Reset</button>
    <button class="btn" id="btnExport" title="Export tracking data as JSON">Export</button>
    <button class="btn" id="btnCompactAll">Compact All</button>
    <span class="stats" id="persistStatus"></span>
  </div>
</header>
<div class="grid" id="grid"></div>
<script>
// --- State ---
const STORAGE_KEY = 'adaptive_dashboard_v1';
const PANEL_DEFS = [
  { id:'cpu', title:'CPU Usage', icon:'', type:'spark', unit:'%', val:()=>23+Math.sin(Date.now()/5000)*8 },
  { id:'mem', title:'Memory', icon:'', type:'bar', unit:'GB', vals:()=>[12.4,8.1,3.2,1.8], labels:['Used','Cache','Free','Swap'] },
  { id:'net', title:'Network Throughput', icon:'', type:'gauge', unit:'Mbps', val:()=>340+Math.random()*120 },
  { id:'err', title:'Error Rate', icon:'', type:'counter', unit:'%', val:()=>Math.max(0,0.7+Math.sin(Date.now()/30000)*0.6) },
  { id:'lat', title:'Request Latency', icon:'', type:'spark', unit:'ms', val:()=>45+Math.random()*30 },
  { id:'users', title:'Active Users', icon:'', type:'counter', unit:'', val:()=>Math.floor(1200+Math.sin(Date.now()/60000)*400) },
  { id:'disk', title:'Disk I/O', icon:'', type:'bar', unit:'MB/s', vals:()=>[87,42,15,8], labels:['Read','Write','Queue','Wait'] },
  { id:'events', title:'Recent Events', icon:'', type:'events', events:()=>[
    {t:'Deploy v2.4.1',ts:Date.now()-120000,s:'ok'},
    {t:'SSL cert renew',ts:Date.now()-600000,s:'ok'},
    {t:'DB conn spike',ts:Date.now()-900000,s:'warn'},
    {t:'Cache cleared',ts:Date.now()-1800000,s:'ok'}
  ]},
];
// --- Persistence queue (batched, 500ms debounce + idle flush) ---
let persistQueue = {};
let persistTimer = null;
function queuePersist(key, data) {
  persistQueue[key] = JSON.stringify(data);
  if (persistTimer) clearTimeout(persistTimer);
  persistTimer = setTimeout(flushPersist, 500);
  if (typeof requestIdleCallback !== 'undefined') requestIdleCallback(flushPersist);
}
function flushPersist() {
  if (persistTimer) { clearTimeout(persistTimer); persistTimer = null; }
  const keys = Object.keys(persistQueue);
  if (!keys.length) return;
  keys.forEach(k => { try { localStorage.setItem(STORAGE_KEY+':'+k, persistQueue[k]) } catch(e){} });
  persistQueue = {};
  updatePersistStatus('Saved');
  setTimeout(() => updatePersistStatus(''), 2000);
}
function updatePersistStatus(msg) {
  document.getElementById('persistStatus').textContent = msg;
}
function loadState() {
  const raw = localStorage.getItem(STORAGE_KEY+':panels');
  return raw ? JSON.parse(raw) : {};
}
function saveState(state) { queuePersist('panels', state); }
// --- Panel state ---
let panels = {}; // id -> {viewCount, totalDuration, lastViewed, locked, manualPos, compactForced}
PANEL_DEFS.forEach(d => {
  panels[d.id] = { viewCount:0, totalDuration:0, lastViewed:0, locked:false,
    manualPos:-1, compactForced:false };
});
let interactionCount = 0;
// --- Recency decay: half-life 7 days ---
function recencyFactor(lastViewed) {
  if (!lastViewed) return 0.01;
  const days = (Date.now() - lastViewed) / (1000 * 60 * 60 * 24);
  return Math.exp(-days / 7);
}
function scorePanel(id) {
  const p = panels[id];
  const freq = Math.log(1 + p.viewCount);
  const dur = Math.log(1 + p.totalDuration / 1000);
  const rec = recencyFactor(p.lastViewed);
  return freq * dur * rec;
}
// --- DOM diffing: reorder children without full rebuild ---
function diffReorder(container, desiredIds) {
  const children = Array.from(container.children);
  const currentIds = children.map(c => c.dataset.pid);
  // Build target positions
  const targetPos = {};
  desiredIds.forEach((id, i) => { targetPos[id] = i; });
  // Iterate and move misplaced nodes
  for (let i = 0; i < children.length; i++) {
    const child = children[i];
    const pid = child.dataset.pid;
    const targetIdx = targetPos[pid];
    if (targetIdx !== undefined && targetIdx !== i) {
      // Find reference node at target position
      const ref = container.children[targetIdx] || null;
      container.insertBefore(child, ref);
      // Rebuild children array since DOM changed
      const updated = Array.from(container.children);
      children.splice(0, children.length, ...updated);
      i = -1; // restart loop
    }
  }
}
// --- Build panel DOM ---
function buildPanelHTML(def, st) {
  const locked = st.locked ? 'locked' : '';
  const compact = st.compactForced ? 'compact' : '';
  return `<div class="panel ${locked} ${compact}" data-pid="${def.id}" draggable="true">
    <div class="panel-header">
      <span class="panel-drag" title="Drag to reorder">:</span>
      <span class="panel-title">${def.title}</span>
      <span class="panel-score" data-score="${def.id}">--</span>
      <div class="panel-actions">
        <button class="panel-btn lock-btn ${locked}" data-action="lock" data-pid="${def.id}"
          title="${locked?'Unlock (auto-layout)':'Lock position'}">${locked?'':'}'</button>
        <button class="panel-btn" data-action="compact" data-pid="${def.id}"
          title="Toggle compact">${compact?'':'}'</button>
      </div>
    </div>
    <div class="panel-body" data-panel-body="${def.id}"></div>
    <div class="panel-preview" data-preview="${def.id}"></div>
  </div>`;
}
function renderPanelBody(def) {
  const v = typeof def.val === 'function' ? def.val() : (def.val || 0);
  const vs = typeof def.vals === 'function' ? def.vals() : (def.vals || []);
  const labs = def.labels || [];
  const evts = typeof def.events === 'function' ? def.events() : (def.events || []);
  switch(def.type) {
    case 'spark':
      return `<div class="metric-val">${v.toFixed(1)}<span style="font-size:0.7em">${def.unit}</span></div>
        <svg class="sparkline" id="spark-${def.id}"><polyline fill="none" stroke="var(--accent)" stroke-width="2"/></svg>`;
    case 'counter':
      return `<div class="metric-val">${typeof v==='number'?v.toLocaleString():v}<span style="font-size:0.5em;margin-left:4px">${def.unit}</span></div>
        <div class="metric-sub ${v>1?'down':''}">${v>1?'Above threshold':'Normal'}</div>`;
    case 'bar': {
      const max = Math.max(...vs, 1);
      const colors = ['var(--accent)','var(--accent2)','var(--warn)','var(--danger)'];
      return `<div class="bar-group">${vs.map((b,i)=>`<div class="bar" style="height:${(b/max)*100}%;background:${colors[i]||'var(--border)'}" title="${labs[i]||''}: ${b}${def.unit}"></div>`).join('')}</div>
        <div style="display:flex;justify-content:space-between;font-size:0.65rem;color:var(--text2)">${labs.map((l,i)=>`<span>${l}: ${vs[i]}${def.unit}</span>`).join('')}</div>`;
    }
    case 'gauge': {
      const pct = Math.min(100, Math.max(0, (v / 500) * 100));
      const ang = (pct / 100) * 180;
      const rad = ang * Math.PI / 180;
      const r = 35, cx = 40, cy = 40;
      const x = cx + r * Math.cos(Math.PI - rad);
      const y = cy - r * Math.sin(Math.PI - rad);
      return `<svg class="gauge-svg" viewBox="0 0 80 50" style="width:100%;height:60px">
        <path d="M5,45 A35,35 0 0,1 75,45" fill="none" stroke="var(--border)" stroke-width="8" stroke-linecap="round"/>
        <path d="M5,45 A35,35 0 0,1 ${x},${y}" fill="none" stroke="var(--accent2)" stroke-width="8" stroke-linecap="round"/>
        <text x="40" y="42" text-anchor="middle" font-size="11" fill="var(--text)" font-weight="600">${v.toFixed(0)}</text>
      </svg><div style="text-align:center;font-size:0.7rem;color:var(--text2)">${def.unit}</div>`;
    }
    case 'events':
      return evts.map(e => {
        const ago = Math.round((Date.now() - e.ts) / 60000);
        return `<div class="event-row"><span>${e.t}</span><span class="event-time">${ago}m ago <span class="tag ${e.s}">${e.s}</span></span></div>`;
      }).join('');
    default: return `<div class="metric-val">${v}</div>`;
  }
}
function renderPreview(def) {
  const v = typeof def.val === 'function' ? def.val() : (def.val || 0);
  return `<svg class="mini-chart" viewBox="0 0 40 24"><rect width="40" height="24" fill="none"/>
    <polyline fill="none" stroke="var(--accent)" stroke-width="1.5" points="0,20 10,12 20,18 30,6 40,10"/></svg>
    <span class="mini-val">${typeof v==='number'?v.toFixed(1):v}</span> <span style="font-size:0.65rem">${def.unit||''}</span>`;
}
function updateSparkline(def) {
  const svg = document.getElementById('spark-'+def.id);
  if (!svg) return;
  const poly = svg.querySelector('polyline');
  if (!poly) return;
  const pts = [];
  for (let i = 0; i < 20; i++) {
    const v = typeof def.val === 'function' ? (def.val() + Math.sin(i*0.7+Date.now()/3000)*(def.unit==='ms'?15:4)) : 0;
    pts.push(`${i*2},${24 - (v / (def.unit==='ms'?100:50)) * 20}`);
  }
  poly.setAttribute('points', pts.join(' '));
}
// --- Layout engine ---
function computeLayout() {
  const scores = PANEL_DEFS.map(d => ({ id:d.id, score:scorePanel(d.id), locked:panels[d.id].locked }));
  // Locked panels keep manual positions, others sorted by score
  const lockedItems = scores.filter(s => s.locked);
  const unlockedItems = scores.filter(s => !s.locked).sort((a,b) => b.score - a.score);
  // Assign grid positions
  const layout = [];
  // High-rank (top 3): span 2 cols x 2 rows for #1, then 1 col x 1 row
  // Low-rank (bottom 2): compact zone
  const total = scores.length;
  const compactThreshold = Math.max(2, total - 3);
  scores.forEach(s => {
    const idx = unlockedItems.findIndex(u => u.id === s.id);
    if (s.locked) {
      layout.push({ id:s.id, compact:panels[s.id].compactForced || false });
    } else {
      const compact = idx >= compactThreshold || panels[s.id].compactForced;
      layout.push({ id:s.id, compact, rank: idx });
    }
  });
  return layout;
}
function applyLayout() {
  const layout = computeLayout();
  const grid = document.getElementById('grid');
  // Build desired order: non-compact first (by rank), then compact
  const nonCompact = layout.filter(l => !l.compact).sort((a,b) => {
    if (a.locked && b.locked) return 0;
    if (a.locked) return -1;
    if (b.locked) return 1;
    return (a.rank||99) - (b.rank||99);
  });
  const compactItems = layout.filter(l => l.compact);
  const desiredIds = [...nonCompact.map(l => l.id), ...compactItems.map(l => l.id)];
  // Ensure all panels exist in DOM
  const existingIds = new Set(Array.from(grid.children).map(c => c.dataset.pid));
  PANEL_DEFS.forEach(def => {
    if (!existingIds.has(def.id)) {
      const st = panels[def.id];
      grid.insertAdjacentHTML('beforeend', buildPanelHTML(def, st));
    }
  });
  // Update compact/expand classes via DOM diffing for classes only
  layout.forEach(l => {
    const el = grid.querySelector(`[data-pid="${l.id}"]`);
    if (!el) return;
    if (l.compact !== el.classList.contains('compact')) {
      el.classList.toggle('compact', l.compact);
      panels[l.id].compactForced = false; // reset forced flag if auto-decided
    }
    // Update score display
    const scoreEl = el.querySelector('[data-score]');
    if (scoreEl) scoreEl.textContent = scorePanel(l.id).toFixed(1);
    // Update locked class
    el.classList.toggle('locked', panels[l.id].locked);
    const lockBtn = el.querySelector('.lock-btn');
    if (lockBtn) {
      lockBtn.classList.toggle('locked', panels[l.id].locked);
      lockBtn.textContent = panels[l.id].locked ? '' : '';
      lockBtn.title = panels[l.id].locked ? 'Unlock (auto-layout)' : 'Lock position';
    }
  });
  // DOM-diff reorder
  diffReorder(grid, desiredIds);
  // Manage compact zone wrapper
  let compactZone = grid.querySelector('.compact-zone');
  if (compactItems.length > 0) {
    if (!compactZone) {
      compactZone = document.createElement('div');
      compactZone.className = 'compact-zone';
      compactZone.innerHTML = '<span class="compact-zone-label">Compact zone &mdash; rarely used panels</span>';
      grid.appendChild(compactZone);
    }
    // Move compact panels into compact zone
    compactItems.forEach(l => {
      const el = grid.querySelector(`[data-pid="${l.id}"]`);
      if (el && el.parentElement !== compactZone) {
        compactZone.appendChild(el);
      }
    });
  } else if (compactZone) {
    compactZone.remove();
  }
  // Update body content
  PANEL_DEFS.forEach(def => {
    const body = document.querySelector(`[data-panel-body="${def.id}"]`);
    if (body) body.innerHTML = renderPanelBody(def);
    const preview = document.querySelector(`[data-preview="${def.id}"]`);
    if (preview) preview.innerHTML = renderPreview(def);
    updateSparkline(def);
  });
  document.getElementById('stats').textContent =
    `Tracking ${PANEL_DEFS.length} panels · ${interactionCount} interactions`;
}
// --- IntersectionObserver for visibility tracking ---
const visibilityTimes = {};
let lastVisibilityUpdate = Date.now();
const observer = new IntersectionObserver((entries) => {
  const now = Date.now();
  entries.forEach(entry => {
    const pid = entry.target.dataset.pid;
    if (!pid) return;
    if (entry.isIntersecting) {
      visibilityTimes[pid] = now;
    } else if (visibilityTimes[pid]) {
      const duration = now - visibilityTimes[pid];
      panels[pid].totalDuration += duration;
      panels[pid].viewCount++;
      panels[pid].lastViewed = now;
      delete visibilityTimes[pid];
      interactionCount++;
      saveState(panels);
    }
  });
}, { threshold: 0.3 });
// Finalize duration for visible panels on unload
function finalizeAllDurations() {
  const now = Date.now();
  Object.keys(visibilityTimes).forEach(pid => {
    const duration = now - visibilityTimes[pid];
    panels[pid].totalDuration += duration;
    panels[pid].viewCount++;
    panels[pid].lastViewed = now;
    delete visibilityTimes[pid];
  });
  saveState(panels);
}
// --- Event delegation ---
document.getElementById('grid').addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;
  const action = btn.dataset.action;
  const pid = btn.dataset.pid;
  if (action === 'lock') {
    panels[pid].locked = !panels[pid].locked;
    if (!panels[pid].locked) panels[pid].manualPos = -1;
    interactionCount++;
    saveState(panels);
    applyLayout();
  } else if (action === 'compact') {
    panels[pid].compactForced = !panels[pid].compactForced;
    interactionCount++;
    saveState(panels);
    applyLayout();
  }
});
// Drag and drop
let dragSrcId = null;
document.getElementById('grid').addEventListener('dragstart', e => {
  const panel = e.target.closest('.panel');
  if (!panel) return;
  dragSrcId = panel.dataset.pid;
  panel.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', dragSrcId);
});
document.getElementById('grid').addEventListener('dragend', e => {
  const panel = e.target.closest('.panel');
  if (panel) panel.classList.remove('dragging');
  document.querySelectorAll('.panel.drag-over').forEach(p => p.classList.remove('drag-over'));
  dragSrcId = null;
});
document.getElementById('grid').addEventListener('dragover', e => {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
  const panel = e.target.closest('.panel');
  if (panel && panel.dataset.pid !== dragSrcId) {
    panel.classList.add('drag-over');
  }
});
document.getElementById('grid').addEventListener('dragleave', e => {
  const panel = e.target.closest('.panel');
  if (panel) panel.classList.remove('drag-over');
});
document.getElementById('grid').addEventListener('drop', e => {
  e.preventDefault();
  const targetPanel = e.target.closest('.panel');
  document.querySelectorAll('.panel.drag-over').forEach(p => p.classList.remove('drag-over'));
  if (!targetPanel || !dragSrcId || targetPanel.dataset.pid === dragSrcId) return;
  const grid = document.getElementById('grid');
  const children = Array.from(grid.children).filter(c => c.classList.contains('panel'));
  const srcIdx = children.findIndex(c => c.dataset.pid === dragSrcId);
  const tgtIdx = children.findIndex(c => c.dataset.pid === targetPanel.dataset.pid);
  if (srcIdx === -1 || tgtIdx === -1) return;
  // Move in DOM
  if (tgtIdx > srcIdx) {
    grid.insertBefore(children[srcIdx], children[tgtIdx].nextSibling);
  } else {
    grid.insertBefore(children[srcIdx], children[tgtIdx]);
  }
  // Lock both panels at their new positions
  panels[dragSrcId].locked = true;
  panels[targetPanel.dataset.pid].locked = true;
  panels[dragSrcId].manualPos = tgtIdx;
  panels[targetPanel.dataset.pid].manualPos = srcIdx;
  interactionCount++;
  saveState(panels);
  applyLayout();
});
// --- Buttons ---
document.getElementById('btnReset').addEventListener('click', () => {
  PANEL_DEFS.forEach(d => {
    panels[d.id] = { viewCount:0, totalDuration:0, lastViewed:0, locked:false, manualPos:-1, compactForced:false };
  });
  interactionCount = 0;
  Object.keys(visibilityTimes).forEach(k => delete visibilityTimes[k]);
  saveState(panels);
  applyLayout();
  updatePersistStatus('Reset');
});
document.getElementById('btnExport').addEventListener('click', () => {
  const data = { panels, interactionCount, exportedAt: new Date().toISOString() };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type:'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'dashboard-tracking.json'; a.click();
  URL.revokeObjectURL(url);
});
document.getElementById('btnCompactAll').addEventListener('click', () => {
  const allCompact = PANEL_DEFS.every(d => panels[d.id].compactForced);
  PANEL_DEFS.forEach(d => { panels[d.id].compactForced = !allCompact; });
  interactionCount++;
  saveState(panels);
  applyLayout();
});
// --- Init ---
function init() {
  const saved = loadState();
  if (saved && Object.keys(saved).length) {
    PANEL_DEFS.forEach(d => {
      if (saved[d.id]) {
        panels[d.id] = { ...panels[d.id], ...saved[d.id] };
      }
    });
  }
  applyLayout();
  // Observe all panels
  document.querySelectorAll('.panel').forEach(el => observer.observe(el));
  // Re-observe on DOM changes
  const mo = new MutationObserver(() => {
    document.querySelectorAll('.panel').forEach(el => {
      if (!visibilityTimes[el.dataset.pid] && !el.dataset.observed) {
        observer.observe(el);
        el.dataset.observed = '1';
      }
    });
  });
  mo.observe(document.getElementById('grid'), { childList: true, subtree: true });
  // Periodic refresh for live metrics
  setInterval(() => {
    PANEL_DEFS.forEach(def => {
      const body = document.querySelector(`[data-panel-body="${def.id}"]`);
      if (body && !body.closest('.compact')) body.innerHTML = renderPanelBody(def);
      updateSparkline(def);
      const scoreEl = document.querySelector(`[data-score="${def.id}"]`);
      if (scoreEl) scoreEl.textContent = scorePanel(def.id).toFixed(1);
    });
  }, 2000);
  // Periodic persistence flush for visibility durations
  setInterval(() => {
    const now = Date.now();
    let changed = false;
    Object.keys(visibilityTimes).forEach(pid => {
      panels[pid].totalDuration += now - visibilityTimes[pid];
      visibilityTimes[pid] = now;
      changed = true;
    });
    if (changed) saveState(panels);
  }, 5000);
  window.addEventListener('beforeunload', finalizeAllDurations);
  window.addEventListener('pagehide', finalizeAllDurations);
}
init();
</script>
</body>
</html>