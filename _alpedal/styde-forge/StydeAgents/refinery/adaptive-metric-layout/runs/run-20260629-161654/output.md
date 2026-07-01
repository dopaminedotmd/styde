<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--surface2:#22263a;--border:#2d3148;
  --text:#e1e4ed;--text2:#9298b0;--accent:#6c8cff;--accent2:#45d9c0;
  --danger:#ff6b7a;--warn:#ffb347;--radius:10px;--gap:12px;
  --transition:0.3s cubic-bezier(0.4,0,0.2,1);
}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
.toolbar{display:flex;align-items:center;gap:12px;padding:10px 16px;background:var(--surface);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;flex-wrap:wrap}
.toolbar h1{font-size:1.1rem;font-weight:600;white-space:nowrap}
.toolbar .stats{font-size:0.75rem;color:var(--text2);display:flex;gap:16px;margin-left:auto;flex-wrap:wrap}
.toolbar button{background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.8rem;transition:var(--transition)}
.toolbar button:hover{background:var(--accent);border-color:var(--accent)}
.toolbar button.reset{background:transparent;border-color:var(--danger);color:var(--danger)}
.toolbar button.reset:hover{background:var(--danger);color:#fff}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--gap);padding:16px;max-width:1600px;margin:0 auto;transition:var(--transition)}
@media(max-width:1024px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.grid{grid-template-columns:1fr}}
.panel{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  transition:all var(--transition);position:relative;overflow:hidden;
  display:flex;flex-direction:column;min-height:180px;
}
.panel:hover{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.panel.span-2{grid-column:span 2}
.panel.span-3{grid-column:span 3}
.panel.span-4{grid-column:span 4}
.panel.compact{min-height:80px;max-height:120px;opacity:0.7;filter:grayscale(30%)}
.panel.compact .panel-body{display:none}
.panel.compact .panel-preview{display:flex}
.panel.locked{border-color:var(--accent2);box-shadow:0 0 0 2px var(--accent2)}
.panel.dragging{opacity:0.85;z-index:50;box-shadow:0 8px 32px rgba(0,0,0,0.5);cursor:grabbing}
.panel-header{
  display:flex;align-items:center;gap:8px;padding:10px 14px;
  background:var(--surface2);border-bottom:1px solid var(--border);
  cursor:grab;user-select:none;flex-shrink:0;
}
.panel-header:active{cursor:grabbing}
.panel-header .title{font-weight:600;font-size:0.9rem;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-header .rank-badge{
  font-size:0.65rem;padding:2px 7px;border-radius:10px;background:var(--accent);
  color:#fff;font-weight:700;
}
.panel-header .actions{display:flex;gap:4px}
.panel-header .actions button{
  background:transparent;border:none;color:var(--text2);cursor:pointer;
  padding:4px 6px;border-radius:4px;font-size:0.85rem;transition:var(--transition);
  line-height:1;
}
.panel-header .actions button:hover{color:var(--text);background:var(--border)}
.panel-header .actions button.lock-btn.locked{color:var(--accent2)}
.panel-body{padding:14px;flex:1;overflow:auto}
.panel-preview{display:none;padding:8px 14px;font-size:0.75rem;color:var(--text2);align-items:center;gap:8px}
.panel-preview .mini-chart{width:60px;height:30px;background:var(--surface2);border-radius:4px;overflow:hidden}
.heatmap-dot{position:absolute;width:6px;height:6px;border-radius:50%;background:var(--accent);opacity:0.4;pointer-events:none;transition:opacity 2s}
.metric-value{font-size:2rem;font-weight:700;line-height:1}
.metric-label{font-size:0.75rem;color:var(--text2);margin-top:4px}
.metric-change{font-size:0.8rem;margin-top:4px}
.metric-change.up{color:var(--accent2)}
.metric-change.down{color:var(--danger)}
.chart-area{width:100%;height:120px;background:var(--surface2);border-radius:6px;position:relative;overflow:hidden}
.chart-area canvas{width:100%;height:100%}
.compact-section{border-top:1px dashed var(--border);margin-top:16px;padding-top:12px}
.compact-section summary{color:var(--text2);font-size:0.85rem;cursor:pointer;padding:8px;border-radius:6px}
.compact-section summary:hover{color:var(--text)}
.overlay{position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:200;display:none;align-items:center;justify-content:center}
.overlay.show{display:flex}
.overlay .dialog{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;max-width:400px;width:90%}
.overlay .dialog h3{margin-bottom:12px}
.overlay .dialog button{margin-top:12px;margin-right:8px}
@keyframes pulse{0%,100%{opacity:0.4}50%{opacity:1}}
.recording-dot{width:8px;height:8px;border-radius:50%;background:var(--accent2);animation:pulse 1.5s infinite;display:inline-block}
</style>
</head>
<body>
<div class="toolbar">
  <h1>Adaptive Dashboard</h1>
  <div class="stats">
    <span><span class="recording-dot"></span> Tracking</span>
    <span id="stat-sessions">Sessions: 0</span>
    <span id="stat-events">Events: 0</span>
    <span id="stat-adapts">Adapts: 0</span>
  </div>
  <button onclick="engine.resetAll()" class="reset">Reset</button>
</div>
<div class="grid" id="grid"></div>
<details class="compact-section" id="compactSection" style="display:none;max-width:1600px;margin:0 auto 40px;padding:0 16px">
  <summary id="compactSummary">Compact panels (0)</summary>
  <div class="grid" id="compactGrid" style="grid-template-columns:repeat(4,1fr)"></div>
</details>
<div class="overlay" id="overlay">
  <div class="dialog" id="dialog"></div>
</div>
<script>
(function(){
'use strict';
const LS_KEY = 'adaptive_dashboard_v3';
const ADAPT_INTERVAL = 8000;
const SAVE_DEBOUNCE = 500;
const RECENCY_HALFLIFE_HOURS = 48;
const COMPACT_SCORE_THRESHOLD = 0.15;
const panelMetaCache = new Map();
function safeLS(method, key, data) {
  try {
    if (method === 'get') {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : null;
    }
    if (method === 'set') localStorage.setItem(key, JSON.stringify(data));
    if (method === 'remove') localStorage.removeItem(key);
    return true;
  } catch(e) {
    return method === 'get' ? null : false;
  }
}
const PANEL_DEFS = [
  {id:'revenue',title:'Revenue Overview',type:'chart',color:'#6c8cff'},
  {id:'users',title:'User Activity',type:'chart',color:'#45d9c0'},
  {id:'conversion',title:'Conversion Rate',type:'metric',value:'8.72%',change:'+0.4%',trend:'up'},
  {id:'server',title:'Server Status',type:'metric',value:'99.9%',label:'Uptime 30d'},
  {id:'orders',title:'Recent Orders',type:'table',rows:8},
  {id:'tickets',title:'Support Tickets',type:'list',rows:6},
  {id:'logs',title:'System Logs',type:'terminal'},
  {id:'api',title:'API Performance',type:'chart',color:'#ffb347'},
];
function makePanelData(def) {
  return {
    id: def.id,
    title: def.title,
    type: def.type,
    color: def.color || '#6c8cff',
    value: def.value || '',
    change: def.change || '',
    trend: def.trend || '',
    label: def.label || '',
    rows: def.rows || 0,
    locked: false,
    span: 1,
    compact: false,
    order: 0,
  };
}
function makeInitialState() {
  const panels = PANEL_DEFS.map((d,i) => {
    const p = makePanelData(d);
    p.span = (i < 2) ? 2 : 1;
    p.order = i;
    return p;
  });
  return {
    panels,
    tracking: {},
    scores: {},
    adaptCount: 0,
    sessionCount: 0,
    totalEvents: 0,
    _v: 3,
  };
}
function initTracking(panelId) {
  return {
    viewMs: 0,
    clicks: 0,
    expands: 0,
    collapses: 0,
    drags: 0,
    lastInteraction: Date.now(),
    viewStart: null,
  };
}
class DashboardEngine {
  constructor() {
    this.state = safeLS('get', LS_KEY) || makeInitialState();
    if (!this.state._v || this.state._v < 3) this.state = makeInitialState();
    this.state.panels.forEach(p => {
      if (!this.state.tracking[p.id]) this.state.tracking[p.id] = initTracking(p.id);
      if (!this.state.scores[p.id]) this.state.scores[p.id] = 0;
    });
    this.state.sessionCount = (this.state.sessionCount || 0) + 1;
    this.state.totalEvents = this.state.totalEvents || 0;
    this.dragState = null;
    this.visiblePanels = new Set();
    this.viewStartTimes = {};
    this.saveTimer = null;
    this.observer = null;
    this.heatmapDots = [];
    this.renderCache = null;
    this.lastRenderHash = '';
  }
  getPanelMeta(id) {
    if (panelMetaCache.has(id)) return panelMetaCache.get(id);
    const meta = this.state.panels.find(p => p.id === id) || null;
    panelMetaCache.set(id, meta);
    return meta;
  }
  invalidateCache() { panelMetaCache.clear(); this.renderCache = null; }
  trackEvent(panelId, type) {
    const t = this.state.tracking[panelId];
    if (!t) return;
    if (type === 'click') t.clicks++;
    else if (type === 'expand') t.expands++;
    else if (type === 'collapse') t.collapses++;
    else if (type === 'drag') t.drags++;
    t.lastInteraction = Date.now();
    this.state.totalEvents++;
    this.scheduleSave();
  }
  addViewTime(panelId, ms) {
    const t = this.state.tracking[panelId];
    if (!t) return;
    t.viewMs += ms;
  }
  computeScore(panelId) {
    const t = this.state.tracking[panelId];
    if (!t) return 0;
    const freq = t.clicks + t.expands * 0.8 + t.drags * 1.5 + 1;
    const dur = Math.log(t.viewMs / 1000 + 1) + 1;
    const hoursSince = Math.max(0, (Date.now() - t.lastInteraction) / 3600000);
    const recency = 1 / (1 + hoursSince / RECENCY_HALFLIFE_HOURS);
    return freq * dur * recency;
  }
  computeAllScores() {
    const scores = {};
    this.state.panels.forEach(p => {
      scores[p.id] = this.computeScore(p.id);
      this.state.scores[p.id] = scores[p.id];
    });
    return scores;
  }
  adaptLayout() {
    const scores = this.computeAllScores();
    const maxScore = Math.max(...Object.values(scores), 1);
    const sorted = [...this.state.panels].filter(p => !p.locked).sort((a,b) => (scores[b.id]||0) - (scores[a.id]||0));
    const locked = this.state.panels.filter(p => p.locked);
    sorted.forEach((p, i) => {
      const normalized = (scores[p.id] || 0) / maxScore;
      if (i === 0) p.span = 2;
      else if (i === 1 && normalized > 0.6) p.span = 2;
      else p.span = 1;
      p.compact = normalized < COMPACT_SCORE_THRESHOLD;
      p.order = i;
    });
    locked.forEach(p => {
      p.span = p.span || 1;
    });
    const allSorted = [
      ...this.state.panels.filter(p => !p.compact && !p.locked).sort((a,b) => (scores[b.id]||0) - (scores[a.id]||0)),
      ...locked.filter(p => !p.compact),
      ...this.state.panels.filter(p => p.compact && !p.locked).sort((a,b) => (scores[b.id]||0) - (scores[a.id]||0)),
      ...locked.filter(p => p.compact),
    ];
    allSorted.forEach((p,i) => { p.order = i; });
    this.state.adaptCount++;
    this.invalidateCache();
    this.renderGrid();
    this.scheduleSave();
  }
  scheduleSave() {
    if (this.saveTimer) clearTimeout(this.saveTimer);
    this.saveTimer = setTimeout(() => {
      safeLS('set', LS_KEY, this.state);
      this.saveTimer = null;
    }, SAVE_DEBOUNCE);
  }
  saveNow() {
    if (this.saveTimer) { clearTimeout(this.saveTimer); this.saveTimer = null; }
    safeLS('set', LS_KEY, this.state);
  }
  resetAll() {
    if (confirm('Reset all tracking data, layout, and preferences?')) {
      safeLS('remove', LS_KEY);
      this.state = makeInitialState();
      this.invalidateCache();
      this.renderGrid();
      this.updateStats();
    }
  }
  toggleLock(panelId) {
    const p = this.getPanelMeta(panelId);
    if (!p) return;
    p.locked = !p.locked;
    this.trackEvent(panelId, p.locked ? 'expand' : 'collapse');
    this.invalidateCache();
    this.renderGrid();
    this.scheduleSave();
  }
  toggleCompact(panelId) {
    const p = this.getPanelMeta(panelId);
    if (!p) return;
    if (p.locked) {
      p.compact = !p.compact;
      this.trackEvent(panelId, p.compact ? 'collapse' : 'expand');
      this.invalidateCache();
      this.renderGrid();
      this.scheduleSave();
    }
  }
  movePanel(panelId, toIndex) {
    const fromIdx = this.state.panels.findIndex(p => p.id === panelId);
    if (fromIdx < 0) return;
    const [moved] = this.state.panels.splice(fromIdx, 1);
    this.state.panels.splice(toIndex, 0, moved);
    this.state.panels.forEach((p,i) => { p.order = i; });
    this.invalidateCache();
    this.renderGrid();
    this.scheduleSave();
  }
  renderGrid() {
    const grid = document.getElementById('grid');
    const compactGrid = document.getElementById('compactGrid');
    const compactSection = document.getElementById('compactSection');
    const compactSummary = document.getElementById('compactSummary');
    const hash = this.state.panels.map(p => `${p.id}:${p.order}:${p.span}:${p.compact}:${p.locked}`).join('|');
    if (hash === this.lastRenderHash) return;
    this.lastRenderHash = hash;
    const mainPanels = this.state.panels.filter(p => !p.compact).sort((a,b) => a.order - b.order);
    const compactPanels = this.state.panels.filter(p => p.compact).sort((a,b) => a.order - b.order);
    const existingEls = new Map();
    grid.querySelectorAll('.panel').forEach(el => existingEls.set(el.dataset.panelId, el));
    compactGrid.querySelectorAll('.panel').forEach(el => existingEls.set(el.dataset.panelId, el));
    const fragment = document.createDocumentFragment();
    const used = new Set();
    mainPanels.forEach(p => {
      used.add(p.id);
      let el = existingEls.get(p.id);
      if (el) {
        const wasInCompact = el.parentElement === compactGrid;
        if (wasInCompact) {
          el = this.buildPanelElement(p);
          fragment.appendChild(el);
        } else {
          this.updatePanelElement(el, p);
          fragment.appendChild(el);
        }
      } else {
        el = this.buildPanelElement(p);
        fragment.appendChild(el);
      }
    });
    const compactFrag = document.createDocumentFragment();
    compactPanels.forEach(p => {
      used.add(p.id);
      let el = existingEls.get(p.id);
      if (el) {
        const wasInMain = el.parentElement === grid;
        if (wasInMain) {
          el = this.buildPanelElement(p);
        } else {
          this.updatePanelElement(el, p);
        }
        compactFrag.appendChild(el);
      } else {
        compactFrag.appendChild(this.buildPanelElement(p));
      }
    });
    existingEls.forEach((el, id) => {
      if (!used.has(id)) el.remove();
    });
    grid.innerHTML = '';
    grid.appendChild(fragment);
    if (compactPanels.length > 0) {
      compactGrid.innerHTML = '';
      compactGrid.appendChild(compactFrag);
      compactSection.style.display = 'block';
      compactSummary.textContent = `Compact panels (${compactPanels.length})`;
    } else {
      compactSection.style.display = 'none';
      compactGrid.innerHTML = '';
    }
    this.reobserve();
    this.updateStats();
  }
  buildPanelElement(p) {
    const el = document.createElement('div');
    el.className = `panel${p.span > 1 ? ' span-'+p.span : ''}${p.compact ? ' compact' : ''}${p.locked ? ' locked' : ''}`;
    el.dataset.panelId = p.id;
    el.draggable = true;
    el.innerHTML = this.panelHTML(p);
    this.bindPanelEvents(el, p);
    return el;
  }
  updatePanelElement(el, p) {
    el.className = `panel${p.span > 1 ? ' span-'+p.span : ''}${p.compact ? ' compact' : ''}${p.locked ? ' locked' : ''}`;
    el.dataset.panelId = p.id;
    const header = el.querySelector('.panel-header');
    if (header) {
      const titleEl = header.querySelector('.title');
      const rankBadge = header.querySelector('.rank-badge');
      const lockBtn = header.querySelector('.lock-btn');
      if (titleEl) titleEl.textContent = p.title;
      if (rankBadge) rankBadge.textContent = '#' + (p.order + 1);
      if (lockBtn) {
        lockBtn.className = 'lock-btn' + (p.locked ? ' locked' : '');
        lockBtn.textContent = p.locked ? 'Locked' : 'Lock';
      }
    }
    if (p.compact) {
      const body = el.querySelector('.panel-body');
      if (body) body.style.display = 'none';
      let preview = el.querySelector('.panel-preview');
      if (!preview) {
        preview = document.createElement('div');
        preview.className = 'panel-preview';
        el.insertBefore(preview, el.querySelector('.panel-body') || null);
      }
      preview.innerHTML = this.previewHTML(p);
      preview.style.display = 'flex';
    } else {
      const body = el.querySelector('.panel-body');
      if (body) body.style.display = '';
      const preview = el.querySelector('.panel-preview');
      if (preview) preview.style.display = 'none';
    }
  }
  panelHTML(p) {
    const bodyContent = this.bodyContent(p);
    const previewContent = p.compact ? this.previewHTML(p) : '';
    return `
      <div class="panel-header">
        <span class="title">${this.esc(p.title)}</span>
        <span class="rank-badge">#${p.order+1}</span>
        <div class="actions">
          <button class="lock-btn${p.locked?' locked':''}" data-action="lock">${p.locked?'Locked':'Lock'}</button>
          <button data-action="compact">${p.compact?'Expand':'Compact'}</button>
        </div>
      </div>
      ${p.compact ? `<div class="panel-preview" style="display:flex">${previewContent}</div>` : ''}
      <div class="panel-body"${p.compact?' style="display:none"':''}>${bodyContent}</div>
    `;
  }
  previewHTML(p) {
    const t = this.state.tracking[p.id];
    const clicks = t ? t.clicks : 0;
    const views = t ? Math.round(t.viewMs / 1000) : 0;
    return `<span>${clicks} clicks</span><span>${views}s viewed</span><span style="margin-left:auto;font-size:0.7rem;opacity:0.6">Score: ${(this.state.scores[p.id]||0).toFixed(1)}</span>`;
  }
  bodyContent(p) {
    switch(p.type) {
      case 'metric': return this.metricBody(p);
      case 'chart': return this.chartBody(p);
      case 'table': return this.tableBody();
      case 'list': return this.listBody();
      case 'terminal': return this.terminalBody();
      default: return '<div style="color:var(--text2)">No content</div>';
    }
  }
  metricBody(p) {
    const changeClass = p.trend === 'up' ? 'up' : (p.trend === 'down' ? 'down' : '');
    return `
      <div class="metric-value">${this.esc(p.value)}</div>
      <div class="metric-label">${this.esc(p.label)}</div>
      ${p.change ? `<div class="metric-change ${changeClass}">${p.change} vs last period</div>` : ''}
    `;
  }
  chartBody(p) {
    return `<div class="chart-area"><canvas id="chart-${p.id}" data-color="${p.color}"></canvas></div>`;
  }
  tableBody() {
    const rows = [
      ['#1023','$149.99','Shipped','2m ago'],
      ['#1022','$89.50','Processing','5m ago'],
      ['#1021','$320.00','Delivered','12m ago'],
      ['#1020','$67.25','Shipped','18m ago'],
      ['#1019','$210.00','Pending','23m ago'],
     ];
    return `<table style="width:100%;font-size:0.78rem;border-collapse:collapse">
      <tr style="color:var(--text2)"><th style="text-align:left;padding:4px">Order</th><th style="text-align:right;padding:4px">Amount</th><th style="text-align:left;padding:4px">Status</th><th style="text-align:right;padding:4px">Time</th></tr>
      ${rows.map(r=>`<tr style="border-top:1px solid var(--border)"><td style="padding:4px">${r[0]}</td><td style="text-align:right;padding:4px">${r[1]}</td><td style="padding:4px">${r[2]}</td><td style="text-align:right;padding:4px">${r[3]}</td></tr>`).join('')}
    </table>`;
  }
  listBody() {
    const items = ['Login issue – user #4421','Billing discrepancy #889','Feature request: dark mode','Bug: chart not rendering','API timeout on /reports'];
    return `<ul style="list-style:none;font-size:0.78rem">${items.map((t,i)=>`<li style="padding:4px 0;border-bottom:1px solid var(--border)"><span style="color:var(--accent2);margin-right:6px">#${i+1}</span>${this.esc(t)}</li>`).join('')}</ul>`;
  }
  terminalBody() {
    const lines = ['[OK] health check passed','[OK] db replication OK','[WARN] memory 72%','[INFO] deploy v2.4.1','[OK] cert valid 89d'];
    return `<div style="font-family:monospace;font-size:0.72rem;line-height:1.8;color:var(--text2)">${lines.map(l=>{
      const c = l.startsWith('[WARN]')?'var(--warn)':l.startsWith('[ERR]')?'var(--danger)':'var(--accent2)';
      return `<div style="color:${c}">${this.esc(l)}</div>`;
    }).join('')}</div>`;
  }
  esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  bindPanelEvents(el, p) {
    el.querySelectorAll('[data-action="lock"]').forEach(btn => {
      btn.onclick = (e) => { e.stopPropagation(); this.toggleLock(p.id); };
    });
    el.querySelectorAll('[data-action="compact"]').forEach(btn => {
      btn.onclick = (e) => { e.stopPropagation(); this.toggleCompact(p.id); };
    });
    el.addEventListener('click', () => this.trackEvent(p.id, 'click'));
    el.addEventListener('dragstart', (e) => {
      if (!p.locked) {
        el.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', p.id);
        this.dragState = { id: p.id, el };
      } else {
        e.preventDefault();
      }
    });
    el.addEventListener('dragend', () => {
      el.classList.remove('dragging');
      this.dragState = null;
      this.trackEvent(p.id, 'drag');
      this.saveNow();
    });
    el.addEventListener('dragover', (e) => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; });
    el.addEventListener('drop', (e) => {
      e.preventDefault();
      const srcId = e.dataTransfer.getData('text/plain');
      if (srcId && srcId !== p.id) {
        const targetIdx = this.state.panels.findIndex(pp => pp.id === p.id);
        this.movePanel(srcId, targetIdx);
      }
    });
  }
  setupObserver() {
    if (this.observer) this.observer.disconnect();
    this.viewStartTimes = {};
    this.observer = new IntersectionObserver((entries) => {
      const now = Date.now();
      entries.forEach(entry => {
        const id = entry.target.dataset.panelId;
        if (!id) return;
        if (entry.isIntersecting) {
          this.viewStartTimes[id] = now;
          this.visiblePanels.add(id);
        } else {
          if (this.viewStartTimes[id]) {
            const duration = now - this.viewStartTimes[id];
            this.addViewTime(id, duration);
            delete this.viewStartTimes[id];
          }
          this.visiblePanels.delete(id);
        }
      });
    }, { threshold: 0.3 });
    document.querySelectorAll('.panel').forEach(el => this.observer.observe(el));
  }
  reobserve() {
    if (this.observer) this.observer.disconnect();
    this.observer = null;
    this.setupObserver();
  }
  updateStats() {
    document.getElementById('stat-sessions').textContent = 'Sessions: ' + this.state.sessionCount;
    document.getElementById('stat-events').textContent = 'Events: ' + this.state.totalEvents;
    document.getElementById('stat-adapts').textContent = 'Adapts: ' + this.state.adaptCount;
  }
  drawCharts() {
    this.state.panels.forEach(p => {
      if (p.type !== 'chart' || p.compact) return;
      const canvas = document.getElementById('chart-' + p.id);
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const rect = canvas.parentElement.getBoundingClientRect();
      canvas.width = rect.width * devicePixelRatio;
      canvas.height = rect.height * devicePixelRatio;
      canvas.style.width = rect.width + 'px';
      canvas.style.height = rect.height + 'px';
      ctx.scale(devicePixelRatio, devicePixelRatio);
      const w = rect.width;
      const h = rect.height;
      ctx.clearRect(0, 0, w, h);
      const color = canvas.dataset.color || '#6c8cff';
      const points = [];
      const seed = p.id.charCodeAt(0) + p.id.charCodeAt(p.id.length-1);
      for (let i = 0; i < 24; i++) {
        const x = (i / 23) * w;
        const val = 0.3 + 0.5 * Math.sin(i * 0.8 + seed) + 0.2 * Math.sin(i * 0.3);
        points.push({x, y: h - val * h * 0.8});
      }
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      for (let i = 1; i < points.length; i++) {
        const prev = points[i-1];
        const cur = points[i];
        const cp1x = prev.x + (cur.x - prev.x) / 3;
        const cp2x = prev.x + (cur.x - prev.x) * 2/3;
        ctx.bezierCurveTo(cp1x, prev.y, cp2x, cur.y, cur.x, cur.y);
      }
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.stroke();
      const grad = ctx.createLinearGradient(0, 0, 0, h);
      grad.addColorStop(0, color + '40');
      grad.addColorStop(1, color + '05');
      ctx.lineTo(w, h);
      ctx.lineTo(0, h);
      ctx.closePath();
      ctx.fillStyle = grad;
      ctx.fill();
    });
  }
  start() {
    this.renderGrid();
    this.updateStats();
    this.drawCharts();
    window.addEventListener('resize', () => { this.drawCharts(); });
    setInterval(() => {
      this.adaptLayout();
      this.drawCharts();
    }, ADAPT_INTERVAL);
    window.addEventListener('beforeunload', () => {
      const now = Date.now();
      this.visiblePanels.forEach(id => {
        if (this.viewStartTimes[id]) {
          this.addViewTime(id, now - this.viewStartTimes[id]);
          delete this.viewStartTimes[id];
        }
      });
      this.saveNow();
    });
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        const now = Date.now();
        this.visiblePanels.forEach(id => {
          if (this.viewStartTimes[id]) {
            this.addViewTime(id, now - this.viewStartTimes[id]);
            delete this.viewStartTimes[id];
          }
        });
        this.saveNow();
      } else {
        this.setupObserver();
      }
    });
  }
}
window.engine = new DashboardEngine();
document.addEventListener('DOMContentLoaded', () => window.engine.start());
})();
</script>
</body>
</html>