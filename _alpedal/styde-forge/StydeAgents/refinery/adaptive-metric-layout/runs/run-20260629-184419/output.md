<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface2: #22263a;
  --border: #2a2e3f;
  --text: #e1e4ed;
  --text2: #8b90a5;
  --accent: #6c8cff;
  --accent2: #4ade80;
  --warn: #f59e0b;
  --danger: #ef4444;
  --radius: 10px;
  --gap: 14px;
  --header-h: 52px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:system-ui,-apple-system,'Segoe UI',sans-serif;
  background:var(--bg);color:var(--text);
  min-height:100vh;padding:16px;
}
.dashboard{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(300px,1fr));
  gap:var(--gap);
  max-width:1400px;margin:0 auto;
  transition:grid-template-columns .35s ease;
}
.panel{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:var(--radius);
  display:flex;flex-direction:column;
  overflow:hidden;
  transition:opacity .25s,transform .25s,grid-column .35s,grid-row .35s;
  position:relative;
}
.panel.size-lg{grid-column:span 2;grid-row:span 2;min-height:360px}
.panel.size-md{grid-column:span 1;grid-row:span 1;min-height:260px}
.panel.size-sm{grid-column:span 1;grid-row:span 1;min-height:160px;font-size:.88em}
.panel.size-xs{grid-column:span 1;grid-row:span 1;min-height:100px;font-size:.8em;opacity:.75}
.panel.compact .panel-body{display:none}
.panel.compact{min-height:auto}
.panel-header{
  display:flex;align-items:center;gap:8px;
  padding:10px 14px;min-height:var(--header-h);
  background:var(--surface2);border-bottom:1px solid var(--border);
  cursor:grab;user-select:none;
}
.panel-header:active{cursor:grabbing}
.panel-header .title{font-weight:600;font-size:.95em;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-header .rank-badge{
  font-size:.72em;background:var(--accent);color:#000;
  border-radius:10px;padding:2px 8px;font-weight:700;
}
.panel-header .rank-badge.low{background:var(--text2);color:var(--bg)}
.panel-body{flex:1;padding:12px 14px;display:flex;align-items:center;justify-content:center;min-height:0}
.panel-body canvas{max-width:100%;max-height:100%}
.metric-value{font-size:2.4em;font-weight:800;text-align:center}
.metric-label{font-size:.85em;color:var(--text2);text-align:center;margin-top:4px}
.btn-group{display:flex;gap:4px}
.btn{
  background:transparent;border:1px solid var(--border);
  color:var(--text2);border-radius:6px;padding:4px 8px;
  cursor:pointer;font-size:.78em;transition:all .15s;
}
.btn:hover{background:var(--surface2);color:var(--text)}
.btn.active{background:var(--accent);color:#000;border-color:var(--accent)}
.btn.locked{background:var(--warn);color:#000;border-color:var(--warn)}
.more-section{
  grid-column:1/-1;background:var(--surface);
  border:1px dashed var(--border);border-radius:var(--radius);
  padding:10px 14px;
}
.more-section summary{font-weight:600;cursor:pointer;color:var(--text2);padding:4px 0}
.more-section summary:hover{color:var(--text)}
.more-panels{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px}
.more-panels .mini{flex:0 0 180px;background:var(--surface2);border-radius:8px;padding:10px;font-size:.8em;cursor:pointer;border:1px solid var(--border)}
.more-panels .mini:hover{border-color:var(--accent)}
.more-panels .mini .mini-title{font-weight:600;margin-bottom:4px}
.more-panels .mini .mini-val{color:var(--accent2);font-size:1.2em;font-weight:700}
.scoring-debug{
  grid-column:1/-1;background:var(--surface2);
  border:1px solid var(--border);border-radius:var(--radius);
  padding:10px 14px;font-size:.75em;color:var(--text2);
  display:none;
}
.scoring-debug.visible{display:block}
.scoring-debug table{width:100%;border-collapse:collapse;margin-top:6px}
.scoring-debug th,.scoring-debug td{text-align:left;padding:3px 6px;border-bottom:1px solid var(--border)}
.scoring-debug .match{color:var(--accent2)}
.scoring-debug .mismatch{color:var(--danger)}
.drag-ghost{opacity:.45;background:var(--accent);border:2px dashed var(--accent)}
</style>
</head>
<body>
<div class="dashboard" id="dashboard"></div>
<details class="more-section" id="moreSection">
  <summary>Compact panels (<span id="moreCount">0</span>)</summary>
  <div class="more-panels" id="morePanels"></div>
</details>
<div class="scoring-debug visible" id="scoringDebug">
  <strong>Scoring validation:</strong> computed vs manual baseline
  <table><thead><tr><th>Panel</th><th>Freq</th><th>AvgDur(s)</th><th>Recency(h)</th><th>Computed</th><th>Manual</th><th>Match</th></tr></thead><tbody id="debugBody"></tbody></table>
</div>
<script>
(function(){
'use strict';
const NS = {}; // single namespace — no duplicate utilities
// --- Constants ---
NS.TICK_MS = 1000;
NS.PERSIST_KEY = 'adaptive_layout_v1';
NS.SIZE_TIERS = ['xs','sm','md','lg'];
NS.TOP_VISIBLE = 6;
NS.COMPACT_THRESHOLD = 15; // score below this → compact
// --- State (single source of truth) ---
NS.state = {
  panels: [],
  order: [],
  locks: {},
  tracking: {}, // {id: {clicks, totalVisibleMs, lastVisibleStart, lastInteractionTs, intervals[]}}
  scores: {},
  sizes: {},
  compacted: new Set(),
  drag: null, // {id, startIdx, ghostEl}
  frameCount: 0,
  dirty: true,
  scoreDirty: true,
};
// --- Panel definitions ---
NS.PANEL_DEFS = [
  {id:'revenue',  title:'Revenue',        type:'chart', chartType:'bar',    data:[420,380,490,510,470,530,580], labels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], color:'#6c8cff'},
  {id:'users',    title:'Active Users',   type:'chart', chartType:'line',   data:[1200,1350,1280,1420,1390,1510,1620], labels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], color:'#4ade80'},
  {id:'churn',    title:'Churn Rate',     type:'chart', chartType:'doughnut',data:[85,15], labels:['Retained','Churned'], color:'#f59e0b'},
  {id:'latency',  title:'API Latency',    type:'metric', value:'142ms',     label:'p95 — last 24h', trend:'down'},
  {id:'errors',   title:'Error Rate',     type:'metric', value:'0.12%',     label:'7-day avg', trend:'stable'},
  {id:'sessions', title:'Sessions',       type:'chart', chartType:'bar',    data:[890,920,870,950,910,980,1020], labels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], color:'#a78bfa'},
  {id:'cpu',      title:'CPU Usage',      type:'metric', value:'67%',       label:'avg across nodes', trend:'up'},
  {id:'storage',  title:'Storage',        type:'metric', value:'4.2 TB',    label:'of 6 TB allocated', trend:'stable'},
  {id:'bandwidth',title:'Bandwidth',      type:'chart', chartType:'line',   data:[32,38,35,42,40,45,48], labels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], color:'#ef4444'},
  {id:'uptime',   title:'Uptime',         type:'metric', value:'99.97%',    label:'last 30 days', trend:'stable'},
];
// --- Utility functions (all in NS, no duplicates) ---
NS.el = (sel, ctx) => (ctx||document).querySelector(sel);
NS.els = (sel, ctx) => [...(ctx||document).querySelectorAll(sel)];
NS.clamp = (v, lo, hi) => v < lo ? lo : v > hi ? hi : v;
NS.now = () => Date.now();
NS.hoursSince = (ts) => ts ? (NS.now() - ts) / 3600000 : Infinity;
// --- Scoring model: composite = frequency × avgDuration × recencyDecay ---
NS.computeScore = function(track, now) {
  if (!track || track.clicks === 0) return 0;
  const freq = track.clicks;
  const avgDur = track.totalVisibleMs ? (track.totalVisibleMs / Math.max(1, track.clicks)) / 1000 : 0;
  const hours = NS.hoursSince(track.lastInteractionTs);
  const recencyFactor = 1 / (1 + hours / 24); // decays: 24h → 0.5, 48h → 0.33
  return freq * avgDur * recencyFactor;
};
// --- Validation: manual calculation for first panel ---
NS.validateScoring = function() {
  const rows = [];
  for (const p of NS.state.panels) {
    const t = NS.state.tracking[p.id] || {clicks:0,totalVisibleMs:0,lastInteractionTs:0};
    const freq = t.clicks;
    const avgDur = t.totalVisibleMs ? (t.totalVisibleMs / Math.max(1, t.clicks)) / 1000 : 0;
    const hours = NS.hoursSince(t.lastInteractionTs);
    const rf = 1 / (1 + hours / 24);
    const manual = freq * avgDur * rf;
    const computed = NS.state.scores[p.id] || 0;
    const match = Math.abs(manual - computed) < 0.001;
    rows.push({id:p.id, freq, avgDur:avgDur.toFixed(1), hours:hours.toFixed(1), computed:computed.toFixed(2), manual:manual.toFixed(2), match});
  }
  return rows;
};
// --- Initialize state ---
NS.initState = function() {
  const saved = localStorage.getItem(NS.PERSIST_KEY);
  const savedData = saved ? JSON.parse(saved) : null;
  NS.state.panels = NS.PANEL_DEFS.map(def => {
    const savedPanel = savedData?.panels?.find(p => p.id === def.id);
    return {
      ...def,
      order: savedPanel?.order ?? 0,
    };
  });
  if (savedData) {
    NS.state.order = savedData.order || NS.PANEL_DEFS.map(d => d.id);
    NS.state.locks = savedData.locks || {};
    NS.state.tracking = savedData.tracking || {};
    NS.state.scores = savedData.scores || {};
    NS.state.sizes = savedData.sizes || {};
    if (savedData.compacted) NS.state.compacted = new Set(savedData.compacted);
  } else {
    NS.state.order = NS.PANEL_DEFS.map(d => d.id);
    for (const p of NS.state.panels) {
      if (!NS.state.tracking[p.id]) {
        NS.state.tracking[p.id] = {clicks:0, totalVisibleMs:0, lastVisibleStart:0, lastInteractionTs:0};
      }
    }
  }
};
// --- Persist ---
NS.persist = function() {
  const data = {
    order: NS.state.order,
    locks: NS.state.locks,
    tracking: NS.state.tracking,
    scores: NS.state.scores,
    sizes: NS.state.sizes,
    panels: NS.state.panels.map(p => ({id:p.id, order:p.order})),
    compacted: [...NS.state.compacted],
  };
  localStorage.setItem(NS.PERSIST_KEY, JSON.stringify(data));
};
// --- Assign sizes based on scores ---
NS.assignSizes = function() {
  const active = NS.state.order.filter(id => !NS.state.compacted.has(id));
  const scored = active.map(id => ({id, score: NS.state.scores[id] || 0}));
  scored.sort((a,b) => b.score - a.score);
  const newSizes = {};
  const newCompacted = new Set(NS.state.compacted);
  for (let i = 0; i < scored.length; i++) {
    const id = scored[i].id;
    if (scored[i].score < NS.COMPACT_THRESHOLD && i >= NS.TOP_VISIBLE) {
      newCompacted.add(id);
      continue;
    }
    if (!NS.state.locks[id]) {
      if (i === 0) newSizes[id] = 'lg';
      else if (i <= 2) newSizes[id] = 'md';
      else if (i <= 5) newSizes[id] = 'sm';
      else newSizes[id] = 'xs';
    }
  }
  // locked panels keep their size
  for (const id of Object.keys(NS.state.locks)) {
    if (NS.state.locks[id] && NS.state.sizes[id]) {
      newSizes[id] = NS.state.sizes[id];
    }
  }
  if (JSON.stringify(NS.state.sizes) !== JSON.stringify(newSizes)) {
    NS.state.sizes = newSizes;
    NS.state.dirty = true;
  }
  if (setsDiffer(NS.state.compacted, newCompacted)) {
    NS.state.compacted = newCompacted;
    NS.state.dirty = true;
  }
};
function setsDiffer(a, b) {
  if (a.size !== b.size) return true;
  for (const v of a) if (!b.has(v)) return true;
  return false;
}
// --- Build order from scores ---
NS.buildOrder = function() {
  const active = NS.state.panels.filter(p => !NS.state.compacted.has(p.id));
  const locked = active.filter(p => NS.state.locks[p.id]);
  const unlocked = active.filter(p => !NS.state.locks[p.id]);
  unlocked.sort((a,b) => (NS.state.scores[b.id]||0) - (NS.state.scores[a.id]||0));
  const newOrder = [...unlocked.map(p => p.id), ...locked.map(p => p.id)];
  if (JSON.stringify(newOrder) !== JSON.stringify(NS.state.order)) {
    NS.state.order = newOrder;
    NS.state.dirty = true;
  }
};
// --- Targeted DOM reconciliation ---
// Never uses innerHTML on containers. Updates only changed attributes/text.
NS.panelCache = new Map();
NS.reconcilePanel = function(panelDef, idx) {
  const id = panelDef.id;
  let el = NS.panelCache.get(id);
  const inDOM = !!el && document.contains(el);
  if (!inDOM) {
    el = NS.buildPanelElement(panelDef);
    NS.panelCache.set(id, el);
    return {el, action:'create'};
  }
  // Update size class if changed
  const size = NS.state.sizes[id] || 'md';
  const oldSize = [...el.classList].find(c => c.startsWith('size-'));
  if (oldSize && oldSize !== 'size-'+size) {
    el.classList.remove(oldSize);
    el.classList.add('size-'+size);
  } else if (!oldSize) {
    el.classList.add('size-'+size);
  }
  // Update compact state
  const isCompacted = NS.state.compacted.has(id);
  el.classList.toggle('compact', isCompacted);
  // Update lock button state
  const lockBtn = NS.el('.btn-lock', el);
  if (lockBtn) {
    lockBtn.classList.toggle('locked', !!NS.state.locks[id]);
    lockBtn.textContent = NS.state.locks[id] ? 'locked' : 'lock';
  }
  // Update rank badge
  const badge = NS.el('.rank-badge', el);
  if (badge && !NS.state.locks[id]) {
    const rank = NS.state.order.indexOf(id);
    badge.textContent = '#'+(rank+1);
    badge.classList.toggle('low', rank >= 4);
  } else if (badge && NS.state.locks[id]) {
    badge.textContent = 'pinned';
    badge.classList.add('low');
  }
  // Update chart data if applicable (targeted, not full rebuild)
  if (panelDef.type === 'chart') {
    NS.updateChartData(id, panelDef);
  }
  return {el, action:'reuse'};
};
NS.buildPanelElement = function(panelDef) {
  const el = document.createElement('div');
  el.className = 'panel';
  el.dataset.panelId = panelDef.id;
  el.draggable = true;
  const size = NS.state.sizes[panelDef.id] || 'md';
  el.classList.add('size-'+size);
  if (NS.state.compacted.has(panelDef.id)) el.classList.add('compact');
  const header = document.createElement('div');
  header.className = 'panel-header';
  const title = document.createElement('span');
  title.className = 'title';
  title.textContent = panelDef.title;
  const badge = document.createElement('span');
  badge.className = 'rank-badge';
  const rank = NS.state.order.indexOf(panelDef.id);
  badge.textContent = NS.state.locks[panelDef.id] ? 'pinned' : '#'+(rank+1);
  if (rank >= 4) badge.classList.add('low');
  const btns = document.createElement('div');
  btns.className = 'btn-group';
  const lockBtn = document.createElement('button');
  lockBtn.className = 'btn btn-lock' + (NS.state.locks[panelDef.id] ? ' locked' : '');
  lockBtn.textContent = NS.state.locks[panelDef.id] ? 'locked' : 'lock';
  lockBtn.onclick = (e) => { e.stopPropagation(); NS.toggleLock(panelDef.id); };
  const collapseBtn = document.createElement('button');
  collapseBtn.className = 'btn';
  collapseBtn.textContent = '−';
  collapseBtn.onclick = (e) => { e.stopPropagation(); NS.toggleCollapse(panelDef.id); };
  btns.append(lockBtn, collapseBtn);
  header.append(title, badge, btns);
  const body = document.createElement('div');
  body.className = 'panel-body';
  body.dataset.panelBody = panelDef.id;
  if (panelDef.type === 'chart') {
    const canvas = document.createElement('canvas');
    canvas.dataset.chartId = panelDef.id;
    body.appendChild(canvas);
  } else if (panelDef.type === 'metric') {
    const val = document.createElement('div');
    val.className = 'metric-value';
    val.textContent = panelDef.value;
    const label = document.createElement('div');
    label.className = 'metric-label';
    label.textContent = panelDef.label;
    body.append(val, label);
  }
  el.append(header, body);
  NS.attachTracking(el, panelDef.id);
  NS.attachDrag(el, panelDef.id);
  return el;
};
// --- Chart instances (single map, no duplicates) ---
NS.charts = new Map();
NS.updateChartData = function(id, panelDef) {
  if (!panelDef || panelDef.type !== 'chart') return;
  const chart = NS.charts.get(id);
  if (chart) {
    chart.data.labels = panelDef.labels;
    chart.data.datasets[0].data = panelDef.data;
    chart.update('none'); // silent update, no animation spam
  }
};
NS.createChart = function(id, panelDef) {
  if (NS.charts.has(id)) return;
  const canvas = NS.el('[data-chart-id="'+id+'"]');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const config = {
    type: panelDef.chartType,
    data: {
      labels: panelDef.labels,
      datasets: [{
        data: panelDef.data,
        backgroundColor: panelDef.chartType === 'doughnut'
          ? [panelDef.color, '#2a2e3f']
          : panelDef.color+'44',
        borderColor: panelDef.color,
        borderWidth: 2,
        tension: 0.3,
        fill: panelDef.chartType === 'line',
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {duration: 400},
      plugins: {
        legend: {display: false},
        tooltip: {enabled: true},
      },
      scales: panelDef.chartType === 'doughnut' ? {} : {
        x: {display:true, grid:{color:'#2a2e3f44'}, ticks:{color:'#8b90a5',font:{size:10}}},
        y: {display:true, grid:{color:'#2a2e3f44'}, ticks:{color:'#8b90a5',font:{size:10}}, beginAtZero:false},
      },
    },
  };
  NS.charts.set(id, new Chart(ctx, config));
};
NS.destroyChart = function(id) {
  const chart = NS.charts.get(id);
  if (chart) { chart.destroy(); NS.charts.delete(id); }
};
// --- Tracking ---
NS.attachTracking = function(el, id) {
  el.addEventListener('click', (e) => {
    if (e.target.closest('button')) return; // ignore button clicks for tracking
    const t = NS.state.tracking[id] || {clicks:0,totalVisibleMs:0,lastVisibleStart:0,lastInteractionTs:0};
    t.clicks = (t.clicks||0) + 1;
    t.lastInteractionTs = NS.now();
    NS.state.tracking[id] = t;
    NS.state.scoreDirty = true;
  });
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      const t = NS.state.tracking[id] || {clicks:0,totalVisibleMs:0,lastVisibleStart:0,lastInteractionTs:0};
      if (entry.isIntersecting) {
        t.lastVisibleStart = NS.now();
      } else if (t.lastVisibleStart) {
        t.totalVisibleMs = (t.totalVisibleMs||0) + (NS.now() - t.lastVisibleStart);
        t.lastVisibleStart = 0;
      }
      NS.state.tracking[id] = t;
    }
  }, {threshold: 0.5});
  observer.observe(el);
};
// --- Drag and Drop ---
NS.attachDrag = function(el, id) {
  el.addEventListener('dragstart', (e) => {
    if (!NS.state.locks[id]) return;
    NS.state.drag = {id, startIdx: NS.state.order.indexOf(id)};
    el.classList.add('drag-ghost');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', id);
  });
  el.addEventListener('dragend', (e) => {
    el.classList.remove('drag-ghost');
    NS.state.drag = null;
  });
  el.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  });
  el.addEventListener('drop', (e) => {
    e.preventDefault();
    const fromId = e.dataTransfer.getData('text/plain');
    const toId = id;
    if (fromId === toId) return;
    if (!NS.state.locks[fromId] || !NS.state.locks[toId]) return;
    const fromIdx = NS.state.order.indexOf(fromId);
    const toIdx = NS.state.order.indexOf(toId);
    if (fromIdx < 0 || toIdx < 0) return;
    const newOrder = [...NS.state.order];
    newOrder.splice(fromIdx, 1);
    newOrder.splice(toIdx, 0, fromId);
    NS.state.order = newOrder;
    NS.state.dirty = true;
    NS.persist();
  });
};
// --- Actions ---
NS.toggleLock = function(id) {
  if (NS.state.locks[id]) {
    delete NS.state.locks[id];
  } else {
    NS.state.locks[id] = true;
    NS.state.sizes[id] = NS.state.sizes[id] || 'md';
  }
  NS.state.compacted.delete(id);
  NS.state.dirty = true;
  NS.state.scoreDirty = true;
  NS.persist();
};
NS.toggleCollapse = function(id) {
  if (NS.state.compacted.has(id)) {
    NS.state.compacted.delete(id);
  } else {
    NS.state.compacted.add(id);
  }
  NS.state.dirty = true;
  NS.persist();
};
NS.restoreFromCompact = function(id) {
  NS.state.compacted.delete(id);
  NS.state.dirty = true;
  NS.persist();
};
// --- Single unified render loop (requestAnimationFrame only, no setTimeout/setInterval) ---
NS.lastScoreUpdate = 0;
NS.SCORE_INTERVAL = 2000; // throttle scoring to every 2s
NS.lastPersist = 0;
NS.PERSIST_INTERVAL = 5000; // throttle persist to every 5s
NS.renderLoop = function(timestamp) {
  NS.state.frameCount++;
  // Throttled scoring (frame-skip counter pattern)
  if (NS.state.scoreDirty && (timestamp - NS.lastScoreUpdate) >= NS.SCORE_INTERVAL) {
    NS.updateScores();
    NS.buildOrder();
    NS.assignSizes();
    NS.state.scoreDirty = false;
    NS.lastScoreUpdate = timestamp;
  }
  // Throttled persist
  if (NS.state.dirty && (timestamp - NS.lastPersist) >= NS.PERSIST_INTERVAL) {
    NS.persist();
    NS.lastPersist = timestamp;
  }
  // DOM reconciliation (targeted, only when dirty)
  if (NS.state.dirty) {
    NS.reconcileDOM();
    NS.state.dirty = false;
  }
  // Validation display (every 60 frames ~1s)
  if (NS.state.frameCount % 60 === 0) {
    NS.renderValidation();
  }
  requestAnimationFrame(NS.renderLoop);
};
NS.updateScores = function() {
  const now = NS.now();
  for (const p of NS.state.panels) {
    const t = NS.state.tracking[p.id] || {clicks:0,totalVisibleMs:0,lastInteractionTs:0};
    // Also factor in current visible time if panel is being viewed
    let total = t.totalVisibleMs || 0;
    if (t.lastVisibleStart) {
      total += now - t.lastVisibleStart;
    }
    const effectiveTrack = {...t, totalVisibleMs: total};
    NS.state.scores[p.id] = NS.computeScore(effectiveTrack, now);
  }
};
// --- Targeted DOM reconciliation (no full rebuild) ---
NS.reconcileDOM = function() {
  const dash = NS.el('#dashboard');
  const currentOrder = NS.state.order.filter(id => !NS.state.compacted.has(id));
  // Build a map of current DOM children by data-panel-id
  const domMap = new Map();
  for (const child of dash.children) {
    if (child.dataset.panelId) domMap.set(child.dataset.panelId, child);
  }
  // Remove panels that shouldn't be visible
  for (const [id, el] of domMap) {
    if (!currentOrder.includes(id)) {
      el.remove();
      domMap.delete(id);
      NS.panelCache.delete(id);
    }
  }
  // Insert/update panels in correct order (targeted)
  let refNode = null;
  for (let i = currentOrder.length - 1; i >= 0; i--) {
    const id = currentOrder[i];
    const panelDef = NS.state.panels.find(p => p.id === id);
    if (!panelDef) continue;
    let el = domMap.get(id);
    if (!el) {
      el = NS.buildPanelElement(panelDef);
      NS.panelCache.set(id, el);
      dash.insertBefore(el, refNode);
    } else {
      const {action} = NS.reconcilePanel(panelDef, i);
      if (action === 'reuse') {
        // Move to correct position if needed (targeted reorder)
        if (el.nextSibling !== refNode) {
          dash.insertBefore(el, refNode);
        }
      }
    }
    refNode = el;
  }
  // Create charts for newly added panels (targeted)
  for (const id of currentOrder) {
    const panelDef = NS.state.panels.find(p => p.id === id);
    if (panelDef && panelDef.type === 'chart' && !NS.charts.has(id)) {
      requestAnimationFrame(() => NS.createChart(id, panelDef));
    }
  }
  // Render compact panels in "more" section
  NS.renderCompactSection();
};
NS.renderCompactSection = function() {
  const container = NS.el('#morePanels');
  const countEl = NS.el('#moreCount');
  const compactedIds = [...NS.state.compacted];
  countEl.textContent = compactedIds.length;
  // Targeted reconciliation for compact section
  const existingMap = new Map();
  for (const child of container.children) {
    if (child.dataset.compactId) existingMap.set(child.dataset.compactId, child);
  }
  // Remove stale
  for (const [id, el] of existingMap) {
    if (!compactedIds.includes(id)) el.remove();
  }
  // Add/update
  for (const id of compactedIds) {
    const panelDef = NS.state.panels.find(p => p.id === id);
    if (!panelDef) continue;
    let el = existingMap.get(id);
    if (!el) {
      el = document.createElement('div');
      el.className = 'mini';
      el.dataset.compactId = id;
      el.onclick = () => NS.restoreFromCompact(id);
      const title = document.createElement('div');
      title.className = 'mini-title';
      title.textContent = panelDef.title;
      const val = document.createElement('div');
      val.className = 'mini-val';
      val.textContent = panelDef.type === 'metric' ? panelDef.value : (panelDef.data ? panelDef.data[panelDef.data.length-1] : '—');
      el.append(title, val);
      container.appendChild(el);
    } else {
      const valEl = NS.el('.mini-val', el);
      if (valEl && panelDef.type === 'metric') valEl.textContent = panelDef.value;
    }
  }
};
// --- Validation rendering ---
NS.renderValidation = function() {
  const rows = NS.validateScoring();
  const tbody = NS.el('#debugBody');
  if (!tbody) return;
  let html = '';
  for (const r of rows) {
    html += '<tr><td>'+r.id+'</td><td>'+r.freq+'</td><td>'+r.avgDur+'</td><td>'+r.hours+'</td><td>'+r.computed+'</td><td>'+r.manual+'</td><td class="'+(r.match?'match':'mismatch')+'">'+(r.match?'PASS':'FAIL')+'</td></tr>';
  }
  if (tbody.innerHTML !== html) tbody.innerHTML = html;
};
// --- Init ---
NS.init = function() {
  NS.initState();
  // Initial score computation
  NS.updateScores();
  NS.buildOrder();
  NS.assignSizes();
  NS.state.dirty = true;
  NS.reconcileDOM();
  // Persist initial state
  NS.persist();
  NS.lastPersist = NS.lastScoreUpdate = performance.now();
  // Start single unified render loop — only requestAnimationFrame
  requestAnimationFrame(NS.renderLoop);
};
// --- No setTimeout, no setInterval anywhere ---
// --- Single rAF loop with frame-skip counters for throttling ---
document.addEventListener('DOMContentLoaded', NS.init);
})();
</script>
</body>
</html>