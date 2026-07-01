```html
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
  --border: #2a2d3a;
  --text: #e1e3eb;
  --muted: #8b8fa6;
  --accent: #6c8cff;
  --accent-dim: #4a5fb5;
  --warn: #ffb347;
  --danger: #ff5c5c;
  --success: #4ce1a0;
  --radius: 10px;
  --gap: 10px;
}
* { margin:0; padding:0; box-sizing:border-box }
body {
  font-family: system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 16px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 10px;
}
.header h1 { font-size: 1.4rem; font-weight: 600; color: var(--text) }
.controls { display: flex; gap: 8px; align-items: center }
.btn {
  padding: 6px 14px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
  font-size: 0.85rem;
  transition: background 0.15s, border-color 0.15s;
}
.btn:hover { border-color: var(--accent-dim); background: #22253a }
.btn.active { background: var(--accent); border-color: var(--accent); color: #fff }
.stats-row {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  font-size: 0.78rem;
  color: var(--muted);
  flex-wrap: wrap;
}
.stats-row span { background: var(--surface); padding: 3px 10px; border-radius: 4px }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--gap);
  align-items: start;
  transition: all 0.3s ease;
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  transition: grid-column 0.3s ease, grid-row 0.3s ease, opacity 0.25s;
  position: relative;
}
.panel.large { grid-column: span 2; grid-row: span 2 }
.panel.medium { grid-column: span 1; grid-row: span 1 }
.panel.compact {
  grid-column: span 1;
  max-height: 90px;
  opacity: 0.75;
}
.panel.compact:hover { opacity: 1 }
.panel.locked { border-color: var(--warn) }
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: rgba(255,255,255,0.03);
  border-bottom: 1px solid var(--border);
  cursor: move;
  user-select: none;
}
.panel-header h3 { font-size: 0.95rem; font-weight: 500 }
.panel-actions { display: flex; gap: 4px }
.icon-btn {
  width: 28px; height: 28px;
  border: none; background: none;
  color: var(--muted); cursor: pointer;
  border-radius: 4px; font-size: 0.9rem;
  display: flex; align-items: center; justify-content: center;
  transition: color 0.15s, background 0.15s;
}
.icon-btn:hover { color: var(--text); background: rgba(255,255,255,0.06) }
.icon-btn.lock-active { color: var(--warn) }
.panel-body {
  padding: 14px;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.panel.compact .panel-body { min-height: 0; padding: 8px 14px }
.panel.compact .panel-body canvas { display: none }
.panel.compact .panel-body .compact-preview { display: flex }
.compact-preview { display: none; width: 100%; justify-content: space-between; align-items: center; font-size: 0.8rem; color: var(--muted) }
.compact-preview .metric-val { font-size: 1.1rem; color: var(--text); font-weight: 600 }
.panel-body canvas { max-width: 100%; height: auto }
.panel-body .full-content { display: block }
.panel.compact .panel-body .full-content { display: none }
.score-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  font-size: 0.65rem;
  background: var(--accent-dim);
  color: #fff;
  padding: 2px 7px;
  border-radius: 10px;
  opacity: 0;
  transition: opacity 0.2s;
  pointer-events: none;
}
.panel:hover .score-badge { opacity: 1 }
.metrics-chart {
  width: 100%;
  height: 180px;
}
.panel.medium .metrics-chart { height: 140px }
.compact-chart { display: none }
.more-section {
  margin-top: 16px;
  border-top: 1px solid var(--border);
  padding-top: 12px;
}
.more-section summary {
  cursor: pointer;
  color: var(--muted);
  font-size: 0.82rem;
  padding: 4px 0;
  user-select: none;
}
.more-section .grid { margin-top: 10px }
.drag-ghost { opacity: 0.4; border: 2px dashed var(--accent) }
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 10px 18px;
  border-radius: var(--radius);
  font-size: 0.82rem;
  z-index: 100;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.25s;
  pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0) }
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <button class="btn" id="btnReset" title="Reset all tracking data">Reset</button>
    <button class="btn" id="btnAuto" title="Toggle auto-arrange">Auto: ON</button>
    <button class="btn" id="btnExport" title="Export layout">Export</button>
  </div>
</div>
<div class="stats-row">
  <span id="statSessions">Sessions: 0</span>
  <span id="statTracked">Events tracked: 0</span>
  <span id="statCacheSize">Cache: 0 entries</span>
</div>
<div class="grid" id="mainGrid"></div>
<details class="more-section" id="moreSection" open>
  <summary>More panels (<span id="moreCount">0</span>)</summary>
  <div class="grid" id="moreGrid"></div>
</details>
<div class="toast" id="toast"></div>
<script>
'use strict';
const PANEL_DEFS = [
  { id:'revenue',   title:'Revenue',       metric:'$',  val: '$14,582',   spark: [30,45,38,52,48,60,55,70,65,80,72,88] },
  { id:'users',     title:'Active Users',  metric:'',   val: '2,847',     spark: [20,25,22,30,28,35,32,40,38,45,42,50] },
  { id:'conversion',title:'Conversion',    metric:'%',  val: '4.8%',      spark: [3,4,3.5,5,4.5,5.5,5,6,5.5,6.5,6,7] },
  { id:'latency',   title:'API Latency',   metric:'ms', val: '142ms',     spark: [200,180,190,160,170,150,155,140,145,130,135,142] },
  { id:'errors',    title:'Error Rate',    metric:'%',  val: '0.12%',     spark: [0.5,0.4,0.3,0.35,0.2,0.25,0.15,0.18,0.1,0.12,0.08,0.12] },
  { id:'bw',        title:'Bandwidth',     metric:'GB', val: '342 GB',    spark: [50,80,90,120,140,160,200,220,250,280,310,342] },
  { id:'sessions',  title:'Sessions',      metric:'',   val: '12,401',    spark: [100,200,300,400,500,600,700,800,900,1000,1100,1240] },
  { id:'cpu',       title:'CPU Usage',     metric:'%',  val: '67%',       spark: [40,50,45,55,60,65,70,68,72,65,68,67] },
];
const SCORE_TTL = 30000;
const PREF_TTL = 300000;
const SCORE_CACHE_SIZE = 50;
const COMPACT_THRESHOLD = 0.20;
const NEGATIVE_DECAY = 0.35;
const DECAY_INTERVAL = 60000;
let panels = [];
let autoArrange = true;
let trackEvents = 0;
let sessionCount = 0;
let observers = {};
let visibilityMap = {};
let interactionMap = {};
let collapseEvents = {};
let closeEvents = {};
let manualOverrides = {};
let dragState = null;
const scoreCache = new Map();
function cacheGet(k) {
  const e = scoreCache.get(k);
  if (!e) return null;
  if (Date.now() > e.expires) { scoreCache.delete(k); return null }
  scoreCache.delete(k);
  scoreCache.set(k, e);
  return e.val;
}
function cacheSet(k, v, ttl) {
  if (scoreCache.size >= SCORE_CACHE_SIZE) {
    const first = scoreCache.keys().next().value;
    scoreCache.delete(first);
  }
  scoreCache.set(k, { val:v, expires: Date.now() + ttl });
}
function calcScore(pid) {
  const ck = 'score_' + pid;
  const hit = cacheGet(ck);
  if (hit !== null) return hit;
  const freq = interactionMap[pid] || 0;
  const dur = visibilityMap[pid] || 0;
  const rec = Date.now() - ((collapseEvents[pid] || 0) + (closeEvents[pid] || 0));
  const recency = Math.max(0, 1 - rec / (24 * 3600000));
  const neg = (collapseEvents[pid] || 0) + (closeEvents[pid] || 0);
  const raw = (freq * (dur + 1) * (recency + 0.1));
  const decay = neg * NEGATIVE_DECAY * (dur + 1);
  const score = Math.max(0, raw - decay);
  cacheSet(ck, score, SCORE_TTL);
  return score;
}
function persistPrefs() {
  const data = {
    interactionMap, visibilityMap, collapseEvents, closeEvents,
    manualOverrides, sessionCount, trackEvents, ts: Date.now()
  };
  const meta = { t: Date.now(), keys: Object.keys(data) };
  try {
    localStorage.setItem('ad_layout_data', JSON.stringify(data));
    localStorage.setItem('ad_layout_meta', JSON.stringify(meta));
  } catch(e) {}
}
function loadPrefs() {
  try {
    const metaRaw = localStorage.getItem('ad_layout_meta');
    if (!metaRaw) return;
    const meta = JSON.parse(metaRaw);
    const age = Date.now() - meta.t;
    const dataRaw = localStorage.getItem('ad_layout_data');
    if (!dataRaw) return;
    const data = JSON.parse(dataRaw);
    if (age > PREF_TTL) {
      for (const k of ['interactionMap','visibilityMap','collapseEvents','closeEvents','manualOverrides']) {
        const d = data[k];
        if (!d) continue;
        for (const key of Object.keys(d)) {
          if (typeof d[key] === 'number') d[key] = Math.max(0, d[key] * Math.exp(-age / PREF_TTL));
        }
      }
    }
    if (data.interactionMap) interactionMap = data.interactionMap;
    if (data.visibilityMap) visibilityMap = data.visibilityMap;
    if (data.collapseEvents) collapseEvents = data.collapseEvents;
    if (data.closeEvents) closeEvents = data.closeEvents;
    if (data.manualOverrides) manualOverrides = data.manualOverrides;
    if (data.sessionCount) sessionCount = data.sessionCount + 1;
    if (data.trackEvents) trackEvents = data.trackEvents;
  } catch(e) {}
}
function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(t._tid);
  t._tid = setTimeout(() => t.classList.remove('show'), 2000);
}
function sparkToSvg(data, w, h, color) {
  if (!data || data.length < 2) return '';
  const max = Math.max(...data);
  const min = Math.min(...data);
  const r = max - min || 1;
  const pad = 4;
  const xs = data.map((_,i) => pad + (i/(data.length-1))*(w-2*pad));
  const ys = data.map(v => pad + (1-(v-min)/r)*(h-2*pad));
  let path = `M${xs[0]},${ys[0]}`;
  for (let i=1; i<xs.length; i++) path += ` L${xs[i]},${ys[i]}`;
  const fillPath = path + ` L${w-pad},${h-pad} L${pad},${h-pad} Z`;
  return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
    <defs><linearGradient id="g_${color}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="${color}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="${color}" stop-opacity="0.02"/>
    </linearGradient></defs>
    <path d="${fillPath}" fill="url(#g_${color})"/>
    <path d="${path}" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>`;
}
function renderPanelDOM(p) {
  const el = document.getElementById('panel_' + p.id);
  if (!el) return;
  const body = el.querySelector('.panel-body');
  if (!body) return;
  const isCompact = el.classList.contains('compact');
  if (isCompact) {
    if (p._lastCompactRendered) return;
    p._lastCompactRendered = true;
    p._lastFullRendered = false;
    body.innerHTML = `<div class="compact-preview">
      <span>${p.title}</span>
      <span class="metric-val">${p.def.val}</span>
      <span style="font-size:0.7rem;color:var(--muted);">${sparkToSvg(p.def.spark, 80, 24, 'var(--accent)')}</span>
    </div>`;
  } else {
    if (p._lastFullRendered) return;
    p._lastFullRendered = true;
    p._lastCompactRendered = false;
    body.innerHTML = `<div class="full-content">
      <div class="metrics-chart">${sparkToSvg(p.def.spark, el.classList.contains('large') ? 400 : 280, el.classList.contains('large') ? 180 : 140, 'var(--accent)')}</div>
      <div style="margin-top:8px;font-size:0.82rem;color:var(--muted);display:flex;justify-content:space-between;">
        <span>Current: <strong style="color:var(--text)">${p.def.val}</strong></span>
        <span>Score: ${calcScore(p.id).toFixed(1)}</span>
      </div>
    </div>`;
  }
}
function buildPanel(p) {
  const existing = document.getElementById('panel_' + p.id);
  if (existing) {
    const s = calcScore(p.id);
    const sb = existing.querySelector('.score-badge');
    if (sb) sb.textContent = s.toFixed(1);
    const isCompact = s < COMPACT_THRESHOLD * getMaxScore();
    const wasCompact = existing.classList.contains('compact');
    if (isCompact !== wasCompact) {
      existing.classList.toggle('compact', isCompact);
      existing.classList.toggle('medium', !isCompact);
      p._lastCompactRendered = false;
      p._lastFullRendered = false;
    }
    if (isCompact) {
      const cp = existing.querySelector('.compact-preview .metric-val');
      if (cp) cp.textContent = p.def.val;
    }
    return existing;
  }
  const div = document.createElement('div');
  div.className = 'panel medium';
  div.id = 'panel_' + p.id;
  div.draggable = true;
  if (manualOverrides[p.id]) div.classList.add('locked');
  const header = document.createElement('div');
  header.className = 'panel-header';
  header.innerHTML = `<h3>${p.title}</h3>
    <div class="panel-actions">
      <button class="icon-btn lock-btn ${manualOverrides[p.id]?'lock-active':''}" data-action="lock" title="Lock position">&#128274;</button>
      <button class="icon-btn" data-action="expand" title="Expand">&#x26F6;</button>
      <button class="icon-btn" data-action="collapse" title="Compact">&#x25BC;</button>
      <button class="icon-btn" data-action="close" title="Hide">&#x2715;</button>
    </div>`;
  const body = document.createElement('div');
  body.className = 'panel-body';
  const badge = document.createElement('div');
  badge.className = 'score-badge';
  badge.textContent = calcScore(p.id).toFixed(1);
  div.append(header, body, badge);
  header.addEventListener('mousedown', e => { if (!e.target.closest('button')) startDrag(e, p.id) });
  header.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      handleAction(p.id, btn.dataset.action);
    });
  });
  div.addEventListener('dragstart', e => { e.preventDefault() });
  return div;
}
function startDrag(e, pid) {
  if (!autoArrange) return;
  dragState = { pid, startX: e.clientX, startY: e.clientY, el: document.getElementById('panel_' + pid) };
  const onMove = ev => {
    if (!dragState) return;
    dragState.el.style.transform = `translate(${ev.clientX - dragState.startX}px, ${ev.clientY - dragState.startY}px)`;
  };
  const onUp = () => {
    if (!dragState) return;
    dragState.el.style.transform = '';
    manualOverrides[dragState.pid] = { locked: true, x: 0, y: 0 };
    const pel = document.getElementById('panel_' + dragState.pid);
    if (pel) pel.classList.add('locked');
    const lb = pel?.querySelector('.lock-btn');
    if (lb) lb.classList.add('lock-active');
    toast('Panel locked in position');
    persistPrefs();
    dragState = null;
    document.removeEventListener('mousemove', onMove);
    document.removeEventListener('mouseup', onUp);
  };
  document.addEventListener('mousemove', onMove);
  document.addEventListener('mouseup', onUp);
}
function handleAction(pid, action) {
  trackEvents++;
  const el = document.getElementById('panel_' + pid);
  if (!el) return;
  switch(action) {
    case 'lock':
      if (manualOverrides[pid]) {
        delete manualOverrides[pid];
        el.classList.remove('locked');
        const lb = el.querySelector('.lock-btn');
        if (lb) lb.classList.remove('lock-active');
        toast('Panel unlocked');
      } else {
        manualOverrides[pid] = { locked: true };
        el.classList.add('locked');
        const lb = el.querySelector('.lock-btn');
        if (lb) lb.classList.add('lock-active');
        toast('Panel locked');
      }
      break;
    case 'expand':
      el.classList.remove('compact');
      el.classList.add('large');
      interactionMap[pid] = (interactionMap[pid] || 0) + 2;
      p._lastCompactRendered = false;
      p._lastFullRendered = false;
      const p2 = panels.find(pp => pp.id === pid);
      if (p2) renderPanelDOM(p2);
      toast('Expanded: ' + pid);
      break;
    case 'collapse':
      collapseEvents[pid] = (collapseEvents[pid] || 0) + 1;
      interactionMap[pid] = (interactionMap[pid] || 0) - 1;
      el.classList.add('compact');
      el.classList.remove('large', 'medium');
      p._lastCompactRendered = false;
      p._lastFullRendered = false;
      const p3 = panels.find(pp => pp.id === pid);
      if (p3) renderPanelDOM(p3);
      toast('Collapsed: ' + pid);
      break;
    case 'close':
      closeEvents[pid] = (closeEvents[pid] || 0) + 1;
      el.style.display = 'none';
      toast('Hidden: ' + pid);
      break;
  }
  scoreCache.delete('score_' + pid);
  persistPrefs();
  updateStats();
}
function getMaxScore() {
  let m = 0;
  for (const p of panels) { const s = calcScore(p.id); if (s > m) m = s }
  return m || 1;
}
function arrangePanels() {
  if (!autoArrange) return;
  const sorted = [...panels].sort((a,b) => calcScore(b.id) - calcScore(a.id));
  const mainGrid = document.getElementById('mainGrid');
  const moreGrid = document.getElementById('moreGrid');
  const maxScore = getMaxScore();
  const threshold = COMPACT_THRESHOLD * maxScore;
  const active = [];
  const compacted = [];
  for (const p of sorted) {
    if (manualOverrides[p.id]) { active.push(p); continue }
    if (calcScore(p.id) < threshold) compacted.push(p);
    else active.push(p);
  }
  const stateHash = active.map(p => p.id + ':' + (calcScore(p.id) < threshold ? 'c' : 'a') + ':' + (manualOverrides[p.id]?'l':'')).join(',') + '|' + compacted.map(p => p.id).join(',');
  if (stateHash === mainGrid.dataset.layoutHash) return;
  mainGrid.dataset.layoutHash = stateHash;
  mainGrid.innerHTML = '';
  moreGrid.innerHTML = '';
  for (let i = 0; i < active.length; i++) {
    const p = active[i];
    const s = calcScore(p.id);
    const el = buildPanel(p);
    el.classList.remove('compact', 'large', 'medium');
    if (i === 0 && s > maxScore * 0.6) el.classList.add('large');
    else el.classList.add('medium');
    renderPanelDOM(p);
    mainGrid.appendChild(el);
  }
  for (const p of compacted) {
    const el = buildPanel(p);
    el.classList.remove('large', 'medium');
    el.classList.add('compact');
    renderPanelDOM(p);
    moreGrid.appendChild(el);
  }
  document.getElementById('moreCount').textContent = compacted.length;
  document.getElementById('moreSection').open = compacted.length > 0;
}
function setupTracking(p) {
  const el = document.getElementById('panel_' + p.id);
  if (!el) return;
  if (observers[p.id]) observers[p.id].disconnect();
  const obs = new IntersectionObserver(entries => {
    for (const e of entries) {
      if (e.isIntersecting) {
        if (!visibilityMap[p.id]) visibilityMap[p.id] = 0;
        p._visibleSince = Date.now();
        interactionMap[p.id] = (interactionMap[p.id] || 0) + 1;
        trackEvents++;
      } else {
        if (p._visibleSince) {
          visibilityMap[p.id] += (Date.now() - p._visibleSince);
          p._visibleSince = null;
        }
      }
    }
    updateStats();
  }, { threshold: 0.3 });
  obs.observe(el);
  observers[p.id] = obs;
  el.addEventListener('click', () => {
    interactionMap[p.id] = (interactionMap[p.id] || 0) + 1;
    trackEvents++;
    persistPrefs();
    updateStats();
  });
}
function updateStats() {
  document.getElementById('statTracked').textContent = 'Events tracked: ' + trackEvents;
  document.getElementById('statSessions').textContent = 'Sessions: ' + sessionCount;
  document.getElementById('statCacheSize').textContent = 'Cache: ' + scoreCache.size + ' entries';
}
function resetAll() {
  interactionMap = {};
  visibilityMap = {};
  collapseEvents = {};
  closeEvents = {};
  manualOverrides = {};
  trackEvents = 0;
  scoreCache.clear();
  for (const p of panels) { p._lastFullRendered = false; p._lastCompactRendered = false }
  try { localStorage.removeItem('ad_layout_data'); localStorage.removeItem('ad_layout_meta') } catch(e) {}
  const mg = document.getElementById('mainGrid');
  mg.dataset.layoutHash = '';
  mg.innerHTML = '';
  document.getElementById('moreGrid').innerHTML = '';
  document.getElementById('moreCount').textContent = '0';
  document.getElementById('moreSection').open = false;
  panels = PANEL_DEFS.map(d => ({ id: d.id, title: d.title, def: d }));
  arrangePanels();
  for (const p of panels) setupTracking(p);
  updateStats();
  toast('All data reset');
}
function init() {
  loadPrefs();
  sessionCount++;
  panels = PANEL_DEFS.map(d => ({ id: d.id, title: d.title, def: d }));
  document.getElementById('mainGrid').dataset.layoutHash = '';
  arrangePanels();
  for (const p of panels) setupTracking(p);
  updateStats();
  document.getElementById('btnReset').addEventListener('click', resetAll);
  document.getElementById('btnAuto').addEventListener('click', function() {
    autoArrange = !autoArrange;
    this.textContent = 'Auto: ' + (autoArrange ? 'ON' : 'OFF');
    this.classList.toggle('active', autoArrange);
    if (autoArrange) { document.getElementById('mainGrid').dataset.layoutHash = ''; arrangePanels() }
    toast('Auto-arrange: ' + (autoArrange ? 'ON' : 'OFF'));
  });
  document.getElementById('btnAuto').classList.add('active');
  document.getElementById('btnExport').addEventListener('click', () => {
    const data = { interactionMap, visibilityMap, collapseEvents, closeEvents, manualOverrides, sessionCount, trackEvents };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'dashboard_layout_' + Date.now() + '.json';
    a.click();
    toast('Layout exported');
  });
  setInterval(() => {
    for (const p of panels) {
      scoreCache.delete('score_' + p.id);
      p._lastCompactRendered = false;
      p._lastFullRendered = false;
    }
    document.getElementById('mainGrid').dataset.layoutHash = '';
    arrangePanels();
    for (const p of panels) setupTracking(p);
    updateStats();
  }, DECAY_INTERVAL);
}
document.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>
```