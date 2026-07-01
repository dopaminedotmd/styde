<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--border:#2a2d3a;--text:#e1e4ed;--text-muted:#8b8fa6;
  --accent:#6c8cff;--accent-glow:#6c8cff44;--danger:#ff6b7a;--success:#4ade80;--warning:#fbbf24;
  --rank-1-size:2fr;--rank-2-size:2fr;--rank-3-size:1.5fr;--rank-4-size:1fr;--rank-5-size:0.8fr;
  --compact-min:120px;--gap:12px;--radius:10px;--transition:300ms cubic-bezier(0.4,0,0.2,1);
}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px}
header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px}
h1{font-size:1.3rem;font-weight:600;letter-spacing:-0.02em}
.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.btn{background:var(--surface);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.8rem;transition:all var(--transition);white-space:nowrap}
.btn:hover{background:#252836;border-color:var(--accent)}
.btn.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.btn.danger{color:var(--danger);border-color:var(--danger)}
.btn.small{padding:3px 8px;font-size:0.7rem}
.dashboard{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:var(--gap);transition:all var(--transition)}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px;transition:all var(--transition);position:relative;overflow:hidden;min-height:var(--compact-min);display:flex;flex-direction:column}
.panel.rank-1{grid-column:span 2;grid-row:span 2}
.panel.rank-2{grid-column:span 2}
.panel.rank-3{grid-column:span 1;grid-row:span 1}
.panel.rank-4{grid-column:span 1;grid-row:span 1;min-height:100px}
.panel.rank-5{grid-column:span 1;grid-row:span 1;min-height:90px;opacity:0.75;font-size:0.85em}
.panel.compact{min-height:70px;padding:10px}
.panel.compact .panel-body{display:none}
.panel.compact .panel-chart{display:none}
.panel.locked{border-color:var(--warning);box-shadow:0 0 0 1px var(--warning)}
.panel.dragging{opacity:0.5;cursor:grabbing}
.panel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;gap:6px}
.panel-title{font-weight:600;font-size:0.9rem;display:flex;align-items:center;gap:6px}
.panel-rank-badge{font-size:0.65rem;background:var(--accent);color:#fff;padding:1px 6px;border-radius:10px;opacity:0.8}
.panel-actions{display:flex;gap:4px}
.panel-body{flex:1;font-size:0.82rem;color:var(--text-muted);line-height:1.4}
.metric-value{font-size:1.6rem;font-weight:700;color:var(--text);margin:4px 0}
.metric-trend{font-size:0.75rem}
.metric-trend.up{color:var(--success)}
.metric-trend.down{color:var(--danger)}
.panel-chart{height:60px;margin-top:8px;position:relative}
.panel-chart canvas{width:100%;height:100%}
.score-trace{display:none;font-size:0.65rem;color:var(--text-muted);margin-top:6px;padding:6px;background:#00000022;border-radius:4px;font-family:monospace;line-height:1.3;white-space:pre-wrap}
.panel.debug .score-trace{display:block}
.heat-indicator{position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--danger),var(--warning),var(--success));border-radius:var(--radius) var(--radius) 0 0;transform-origin:left;transition:transform var(--transition)}
.drag-handle{cursor:grab;color:var(--text-muted);font-size:0.8rem;user-select:none;padding:2px 4px}
.drag-handle:active{cursor:grabbing}
.empty-state{grid-column:1/-1;text-align:center;padding:40px;color:var(--text-muted)}
.sortable-ghost{opacity:0.3;background:var(--accent-glow)}
.sortable-chosen{box-shadow:0 8px 25px rgba(0,0,0,0.4)}
</style>
</head>
<body>
<header>
  <h1>Adaptive Metrics</h1>
  <div class="controls">
    <button class="btn" id="btnReset" title="Reset all tracking data">Reset</button>
    <button class="btn" id="btnDebug" title="Toggle score computation trace">Debug</button>
    <button class="btn" id="btnAutoLayout" title="Re-run auto-layout">Auto-Layout</button>
    <button class="btn" id="btnAddPanel">+ Panel</button>
  </div>
</header>
<div class="dashboard" id="dashboard"></div>
<script>
(function(){
'use strict';
const ID = id => document.getElementById(id);
const QS = (sel,el=document) => el.querySelector(sel);
const QSA = (sel,el=document) => el.querySelectorAll(sel);
const now = () => Date.now();
// Persistence
const STORE_KEY = 'adaptive_dashboard_v2';
function saveStore(data){ try{ localStorage.setItem(STORE_KEY, JSON.stringify(data)); }catch(e){} }
function loadStore(){ try{ const d=localStorage.getItem(STORE_KEY); return d ? JSON.parse(d) : null; }catch(e){ return null; } }
// Config
const CONFIG = {
  targetChartResolution: 48,
  decayHalfLife: 7 * 24 * 60 * 60 * 1000,
  weights: { frequency: 0.4, duration: 0.4, recency: 0.2 },
  rankThresholds: [0.8, 0.6, 0.4, 0.2, 0],
  minDurationMs: 500,
  idleTimeoutMs: 3000,
  compactThreshold: 0.15,
  observerThreshold: [0, 0.25, 0.5, 0.75, 1],
};
// ============= MEMOIZATION / CACHE =============
const panelMetaCache = new Map();
function getPanelMeta(panelId) {
  if (panelMetaCache.has(panelId)) return panelMetaCache.get(panelId);
  const meta = { el: null, observer: null, visibleStart: 0, totalVisible: 0, interactions: 0, lastInteraction: 0 };
  panelMetaCache.set(panelId, meta);
  return meta;
}
function invalidateMeta(panelId) { panelMetaCache.delete(panelId); }
// ============= TRACKING ENGINE =============
const trackingState = { panels: {} };
function initTracking(panelId) {
  if (!trackingState.panels[panelId]) {
    trackingState.panels[panelId] = {
      viewDuration: 0,
      interactions: 0,
      lastInteraction: 0,
      expandCount: 0,
      collapseCount: 0,
      viewSessions: [],
    };
  }
  return trackingState.panels[panelId];
}
const observerMap = new Map();
let globalObserver = null;
function getObserver() {
  if (!globalObserver) {
    globalObserver = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        const panelId = entry.target.dataset.panelId;
        if (!panelId) continue;
        const meta = getPanelMeta(panelId);
        const track = initTracking(panelId);
        if (entry.isIntersecting && entry.intersectionRatio >= 0.25) {
          if (!meta.visibleStart) meta.visibleStart = now();
        } else if (meta.visibleStart) {
          const dur = now() - meta.visibleStart;
          if (dur >= CONFIG.minDurationMs) {
            track.viewDuration += dur;
            track.viewSessions.push({ start: meta.visibleStart, duration: dur });
            if (track.viewSessions.length > 100) track.viewSessions.shift();
          }
          meta.visibleStart = 0;
        }
      }
    }, { threshold: CONFIG.observerThreshold });
  }
  return globalObserver;
}
function trackInteraction(panelId, type) {
  const track = initTracking(panelId);
  track.interactions++;
  track.lastInteraction = now();
  if (type === 'expand') track.expandCount++;
  if (type === 'collapse') track.collapseCount++;
  const meta = getPanelMeta(panelId);
  meta.interactions = track.interactions;
  meta.lastInteraction = track.lastInteraction;
}
function computeScore(panelId, track) {
  const age = now() - track.lastInteraction || 1;
  const decayFactor = Math.exp(-Math.LN2 * age / CONFIG.decayHalfLife);
  const durMs = track.viewDuration || 0;
  const durScore = Math.min(1, durMs / (60 * 60 * 1000));
  const freqScore = Math.min(1, track.interactions / 50);
  const recencyScore = Math.min(1, decayFactor);
  const raw = CONFIG.weights.frequency * freqScore + CONFIG.weights.duration * durScore + CONFIG.weights.recency * recencyScore;
  const final = Math.round(raw * 1000) / 1000;
  return { raw, final, freqScore, durScore, recencyScore, decayFactor, interactions: track.interactions, viewDuration: track.viewDuration, lastInteraction: track.lastInteraction };
}
function rankPanels(panelIds) {
  const scored = panelIds.map(id => {
    const track = initTracking(id);
    const score = computeScore(id, track);
    return { id, track, ...score };
  });
  scored.sort((a, b) => b.final - a.final);
  for (let i = 0; i < scored.length; i++) {
    const ratio = scored.length > 1 ? (scored[0].final > 0 ? scored[i].final / scored[0].final : 0) : 0;
    let rank = 5;
    if (ratio >= 0.8) rank = 1;
    else if (ratio >= 0.6) rank = 2;
    else if (ratio >= 0.4) rank = 3;
    else if (ratio >= 0.2) rank = 4;
    scored[i].rank = rank;
    scored[i].ratio = ratio;
    scored[i].compact = ratio < CONFIG.compactThreshold;
  }
  return scored;
}
// ============= CHART RENDERER (dynamic normalization) =============
function normalizeData(data, targetRes) {
  if (!data || !data.length) return [];
  if (data.length <= targetRes) return [...data];
  const binSize = data.length / targetRes;
  const result = new Array(targetRes);
  for (let i = 0; i < targetRes; i++) {
    const start = Math.floor(i * binSize);
    const end = Math.floor((i + 1) * binSize);
    let sum = 0, count = 0;
    for (let j = start; j < end && j < data.length; j++) { sum += data[j]; count++; }
    result[i] = count > 0 ? sum / count : 0;
  }
  return result;
}
function drawChart(canvas, data, color) {
  if (!canvas || !data || !data.length) return;
  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  const w = rect.width * dpr;
  const h = rect.height * dpr;
  canvas.width = w;
  canvas.height = h;
  ctx.scale(dpr, dpr);
  const cw = rect.width, ch = rect.height;
  ctx.clearRect(0, 0, cw, ch);
  const normalized = normalizeData(data, CONFIG.targetChartResolution);
  if (!normalized.length) return;
  const maxVal = Math.max(...normalized, 0.001);
  const minVal = Math.min(...normalized, 0);
  const range = maxVal - minVal || 1;
  const padX = 2, padY = 4;
  const plotW = cw - padX * 2, plotH = ch - padY * 2;
  const gradient = ctx.createLinearGradient(0, 0, 0, ch);
  gradient.addColorStop(0, color + '44');
  gradient.addColorStop(1, color + '08');
  ctx.beginPath();
  const stepX = plotW / (normalized.length - 1);
  for (let i = 0; i < normalized.length; i++) {
    const x = padX + i * stepX;
    const y = padY + plotH - ((normalized[i] - minVal) / range) * plotH;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  }
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.5;
  ctx.stroke();
  ctx.lineTo(padX + plotW, padY + plotH);
  ctx.lineTo(padX, padY + plotH);
  ctx.closePath();
  ctx.fillStyle = gradient;
  ctx.fill();
}
// ============= DOM HELPERS =============
function getDemoData(panelId) {
  const seed = panelId.split('').reduce((a,c)=>a+c.charCodeAt(0),0);
  const len = 30 + (seed % 70);
  const data = [];
  for (let i = 0; i < len; i++) {
    data.push(20 + Math.sin(i * 0.3 + seed) * 15 + Math.cos(i * 0.17) * 10 + Math.random() * 8);
  }
  return data;
}
function buildPanelHTML(panel, scored, debug) {
  const s = scored.find(x => x.id === panel.id) || { rank: 3, final: 0, compact: false, freqScore: 0, durScore: 0, recencyScore: 0, decayFactor: 0, interactions: 0, viewDuration: 0 };
  const track = trackingState.panels[panel.id] || { viewDuration: 0, interactions: 0 };
  const pct = Math.round(s.final * 100);
  const heatPct = Math.round(Math.min(100, s.final * 100));
  const data = panel.data || getDemoData(panel.id);
  const trendVal = data.length >= 2 ? data[data.length-1] - data[data.length-2] : 0;
  const trendCls = trendVal > 0 ? 'up' : trendVal < 0 ? 'down' : '';
  const trendStr = trendVal > 0 ? '▲ ' + trendVal.toFixed(1) : trendVal < 0 ? '▼ ' + Math.abs(trendVal).toFixed(1) : '—';
  return `
    <div class="heat-indicator" style="transform:scaleX(${heatPct/100})"></div>
    <div class="panel-header">
      <span class="panel-title">
        <span class="drag-handle" data-action="drag">⠿</span>
        ${panel.label}
        <span class="panel-rank-badge">R${s.rank}·${pct}%</span>
      </span>
      <div class="panel-actions">
        <button class="btn small" data-action="toggle-compact">${s.compact?'⊞':'⊟'}</button>
        <button class="btn small" data-action="lock">${panel.locked?'🔒':'🔓'}</button>
        <button class="btn small danger" data-action="remove">×</button>
      </div>
    </div>
    <div class="panel-body">
      <div class="metric-value">${panel.value !== undefined ? panel.value : Math.round(data[data.length-1]*10)/10}</div>
      <div class="metric-trend ${trendCls}">${trendStr} (last period)</div>
      <div class="panel-chart"><canvas></canvas></div>
    </div>
    <div class="score-trace">${debug ? buildScoreTrace(s, track) : ''}</div>`;
}
function buildScoreTrace(scored, track) {
  return `freq: ${scored.freqScore.toFixed(3)} × ${CONFIG.weights.frequency} = ${(scored.freqScore*CONFIG.weights.frequency).toFixed(3)}
dur:  ${scored.durScore.toFixed(3)} × ${CONFIG.weights.duration} = ${(scored.durScore*CONFIG.weights.duration).toFixed(3)}
rec:  ${scored.recencyScore.toFixed(3)} × ${CONFIG.weights.recency} = ${(scored.recencyScore*CONFIG.weights.recency).toFixed(3)}
decay: ${scored.decayFactor.toExponential(2)}  age: ${Math.round((now()-scored.lastInteraction)/3600000)}h
Σ=${scored.final.toFixed(3)}  rank=${scored.rank}  interacts=${scored.interactions}  view=${Math.round(scored.viewDuration/1000)}s`;
}
// ============= RENDER WITH TARGETED DOM PATCHING =============
let currentPanelOrder = [];
let currentPanelState = new Map();
function renderGrid(panels, scored, debug) {
  const container = ID('dashboard');
  const newOrder = scored.map(s => s.id);
  const containerChildren = Array.from(container.children);
  const idToEl = new Map();
  for (const child of containerChildren) {
    if (child.dataset.panelId) idToEl.set(child.dataset.panelId, child);
  }
  const fragment = document.createDocumentFragment();
  const usedIds = new Set();
  for (let i = 0; i < scored.length; i++) {
    const s = scored[i];
    const panel = panels.find(p => p.id === s.id);
    if (!panel) continue;
    usedIds.add(s.id);
    let el = idToEl.get(s.id);
    if (!el) {
      el = document.createElement('div');
      el.className = 'panel';
      el.dataset.panelId = s.id;
      el.draggable = true;
      el.innerHTML = buildPanelHTML(panel, scored, debug);
    } else {
      const oldState = currentPanelState.get(s.id) || '';
      const newState = `${s.rank}|${s.compact}|${panel.locked}|${debug}`;
      if (oldState !== newState || !el.children.length) {
        el.innerHTML = buildPanelHTML(panel, scored, debug);
      }
    }
    el.className = `panel rank-${s.rank}${s.compact ? ' compact' : ''}${panel.locked ? ' locked' : ''}${debug ? ' debug' : ''}`;
    currentPanelState.set(s.id, `${s.rank}|${s.compact}|${panel.locked}|${debug}`);
    if (s.compact) el.style.gridColumn = 'span 1';
    else el.style.gridColumn = '';
    fragment.appendChild(el);
    requestAnimationFrame(() => {
      const canvas = QS('canvas', el);
      if (canvas && !s.compact) {
        drawChart(canvas, panel.data || getDemoData(panel.id), panel.color || '#6c8cff');
      }
    });
    if (!observerMap.has(s.id)) {
      const obs = getObserver();
      obs.observe(el);
      observerMap.set(s.id, true);
    }
  }
  for (const [id, el] of idToEl) {
    if (!usedIds.has(id)) {
      if (observerMap.has(id)) {
        getObserver().unobserve(el);
        observerMap.delete(id);
      }
      invalidateMeta(id);
      el.remove();
    }
  }
  container.innerHTML = '';
  container.appendChild(fragment);
  currentPanelOrder = newOrder;
}
// ============= STATE MANAGEMENT =============
let panels = [];
let nextId = 0;
let debugMode = false;
function initPanels() {
  const saved = loadStore();
  if (saved && saved.panels && saved.panels.length) {
    panels = saved.panels;
    nextId = saved.nextId || panels.length;
    if (saved.tracking) Object.assign(trackingState.panels, saved.tracking);
  } else {
    const defaults = [
      { label: 'Active Users', value: 1247, data: [], color: '#6c8cff' },
      { label: 'Revenue', value: '$45.2k', data: [], color: '#4ade80' },
      { label: 'Conversion Rate', value: '3.2%', data: [], color: '#fbbf24' },
      { label: 'Latency p95', value: '142ms', data: [], color: '#ff6b7a' },
      { label: 'Error Rate', value: '0.12%', data: [], color: '#a78bfa' },
      { label: 'CPU Load', value: '67%', data: [], color: '#38bdf8' },
    ];
    panels = defaults.map((d, i) => ({ id: 'p' + i, ...d, locked: false, data: d.data.length ? d.data : getDemoData('p'+i) }));
    nextId = panels.length;
  }
}
function generateDemoPanel() {
  const id = 'p' + (nextId++);
  const names = ['Sessions', 'Bounce Rate', 'Page Views', 'Signups', 'Churn', 'NPS', 'TTFB', 'Cache Hit', 'Queue Depth', 'Disk IO'];
  const name = names[Math.floor(Math.random() * names.length)] + ' ' + Math.floor(Math.random() * 100);
  const vals = [Math.floor(Math.random()*5000), '$'+Math.floor(Math.random()*50)+'k', (Math.random()*10).toFixed(1)+'%', Math.floor(Math.random()*500)+'ms'];
  return {
    id, label: name,
    value: vals[Math.floor(Math.random()*vals.length)],
    data: getDemoData(id),
    color: ['#6c8cff','#4ade80','#fbbf24','#ff6b7a','#a78bfa','#38bdf8'][Math.floor(Math.random()*6)],
    locked: false,
  };
}
function refresh() {
  const scored = rankPanels(panels.map(p => p.id));
  renderGrid(panels, scored, debugMode);
  saveStore({ panels, nextId, tracking: trackingState.panels });
}
// ============= EVENT HANDLERS =============
ID('dashboard').addEventListener('click', e => {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;
  const action = btn.dataset.action;
  const panelEl = btn.closest('.panel');
  if (!panelEl) return;
  const panelId = panelEl.dataset.panelId;
  const panel = panels.find(p => p.id === panelId);
  if (!panel) return;
  if (action === 'toggle-compact') {
    trackInteraction(panelId, panelEl.classList.contains('compact') ? 'expand' : 'collapse');
    refresh();
  } else if (action === 'lock') {
    panel.locked = !panel.locked;
    trackInteraction(panelId, 'lock');
    refresh();
  } else if (action === 'remove') {
    panels = panels.filter(p => p.id !== panelId);
    const el = panelEl;
    if (observerMap.has(panelId)) {
      getObserver().unobserve(el);
      observerMap.delete(panelId);
    }
    invalidateMeta(panelId);
    delete trackingState.panels[panelId];
    refresh();
  }
  trackInteraction(panelId, 'click');
});
ID('btnReset').addEventListener('click', () => {
  for (const [id] of observerMap) {
    const el = QS(`[data-panel-id="${id}"]`);
    if (el) getObserver().unobserve(el);
    invalidateMeta(id);
  }
  observerMap.clear();
  trackingState.panels = {};
  panelMetaCache.clear();
  currentPanelState.clear();
  try { localStorage.removeItem(STORE_KEY); } catch(e) {}
  panels = [];
  nextId = 0;
  initPanels();
  refresh();
});
ID('btnDebug').addEventListener('click', () => {
  debugMode = !debugMode;
  ID('btnDebug').classList.toggle('active', debugMode);
  refresh();
});
ID('btnAutoLayout').addEventListener('click', () => {
  panelMetaCache.clear();
  refresh();
});
ID('btnAddPanel').addEventListener('click', () => {
  const p = generateDemoPanel();
  panels.push(p);
  refresh();
});
// Drag and drop (manual override)
let dragSrc = null;
ID('dashboard').addEventListener('dragstart', e => {
  const panelEl = e.target.closest('.panel');
  if (!panelEl || !e.target.closest('[data-action="drag"]')) { e.preventDefault(); return; }
  dragSrc = panelEl;
  panelEl.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', panelEl.dataset.panelId);
  setTimeout(() => panelEl.classList.add('dragging'), 0);
});
ID('dashboard').addEventListener('dragend', e => {
  const panelEl = e.target.closest('.panel');
  if (panelEl) panelEl.classList.remove('dragging');
  dragSrc = null;
});
ID('dashboard').addEventListener('dragover', e => {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
});
ID('dashboard').addEventListener('drop', e => {
  e.preventDefault();
  const targetEl = e.target.closest('.panel');
  if (!targetEl || !dragSrc || targetEl === dragSrc) return;
  const srcId = dragSrc.dataset.panelId;
  const dstId = targetEl.dataset.panelId;
  const srcIdx = panels.findIndex(p => p.id === srcId);
  const dstIdx = panels.findIndex(p => p.id === dstId);
  if (srcIdx < 0 || dstIdx < 0) return;
  const [moved] = panels.splice(srcIdx, 1);
  panels.splice(dstIdx, 0, moved);
  moved.locked = true;
  trackInteraction(srcId, 'drag');
  panelMetaCache.clear();
  refresh();
});
// Scroll-aware: recalculate on scroll
let scrollTicking = false;
window.addEventListener('scroll', () => {
  if (!scrollTicking) {
    requestAnimationFrame(() => {
      const scored = rankPanels(panels.map(p => p.id));
      for (const s of scored) {
        const meta = getPanelMeta(s.id);
        const el = QS(`[data-panel-id="${s.id}"]`);
        if (el) {
          const rect = el.getBoundingClientRect();
          const vpHeight = window.innerHeight;
          const visible = rect.top < vpHeight && rect.bottom > 0;
          if (!visible && meta.visibleStart) {
            const dur = now() - meta.visibleStart;
            const track = initTracking(s.id);
            if (dur >= CONFIG.minDurationMs) {
              track.viewDuration += dur;
              track.viewSessions.push({ start: meta.visibleStart, duration: dur });
            }
            meta.visibleStart = 0;
          }
        }
      }
      scrollTicking = false;
    });
    scrollTicking = true;
  }
});
// Periodic save
setInterval(() => {
  saveStore({ panels, nextId, tracking: trackingState.panels });
}, 5000);
// Init
initPanels();
panelMetaCache.clear();
refresh();
})();
</script>
</body>
</html>