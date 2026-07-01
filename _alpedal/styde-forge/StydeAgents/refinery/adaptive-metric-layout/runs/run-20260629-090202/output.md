```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Dashboard</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;background:#0f172a;color:#e2e8f0;min-height:100vh;overflow-x:hidden}
#grid{display:grid;gap:12px;padding:16px;min-height:calc(100vh - 80px);transition:all .35s ease;grid-auto-rows:minmax(120px,auto)}
.panel{background:#1e293b;border-radius:10px;border:1px solid #334155;padding:16px;position:relative;transition:all .35s ease;overflow:hidden;display:flex;flex-direction:column;cursor:grab}
.panel:active{cursor:grabbing}
.panel.compact{grid-row:span 1!important;grid-column:span 1!important;padding:10px;font-size:.8em}
.panel.compact .panel-body{display:none}
.panel.compact .panel-preview{display:block}
.panel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;gap:8px;flex-shrink:0}
.panel-title{font-weight:600;font-size:1rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-rank{font-size:.7rem;color:#64748b;white-space:nowrap}
.panel-body{flex:1;display:flex;align-items:center;justify-content:center;font-size:2rem;font-weight:700;color:#38bdf8;min-height:calc(100% - 40px)}
.panel-preview{display:none;font-size:.75rem;color:#94a3b8}
.panel-controls{display:flex;gap:6px;align-items:center}
.panel-controls button{background:#334155;border:none;color:#e2e8f0;width:26px;height:26px;border-radius:5px;cursor:pointer;font-size:.75rem;display:flex;align-items:center;justify-content:center;transition:background .15s}
.panel-controls button:hover{background:#475569}
.panel-controls button.locked{background:#f59e0b;color:#0f172a}
.panel.dragging{opacity:.5;z-index:10}
.panel.drop-target{outline:2px dashed #38bdf8;outline-offset:-4px}
#toolbar{display:flex;gap:10px;padding:12px 16px;background:#1e293b;border-bottom:1px solid #334155;align-items:center;flex-wrap:wrap}
#toolbar button{padding:7px 14px;background:#334155;border:none;color:#e2e8f0;border-radius:6px;cursor:pointer;font-size:.8rem;transition:background .15s}
#toolbar button:hover{background:#475569}
#toolbar button.active{background:#38bdf8;color:#0f172a}
#log-panel{position:fixed;bottom:0;right:0;width:340px;max-height:220px;background:#0f172aee;border:1px solid #334155;border-radius:10px 0 0 0;padding:10px;font-size:.7rem;overflow-y:auto;z-index:100;backdrop-filter:blur(10px)}
#log-panel h4{margin-bottom:6px;color:#64748b;font-size:.7rem}
.log-entry{padding:2px 0;border-bottom:1px solid #1e293b;color:#94a3b8}
.tooltip{position:fixed;background:#1e293b;border:1px solid #38bdf8;color:#e2e8f0;padding:6px 10px;border-radius:5px;font-size:.75rem;pointer-events:none;z-index:200;opacity:0;transition:opacity .15s;white-space:nowrap}
</style>
</head>
<body>
<div id="toolbar">
  <button onclick="Dashboard.resetLayout()">Reset Layout</button>
  <button id="btn-auto" class="active" onclick="Dashboard.toggleAuto()">Auto: ON</button>
  <button onclick="Dashboard.resetTracking()">Reset Tracking</button>
  <span style="margin-left:auto;color:#64748b;font-size:.75rem" id="status-text">Ready</span>
</div>
<div id="grid"></div>
<div id="log-panel"><h4>Activity Log</h4><div id="log-entries"></div></div>
<script>
/* === MODEL: Tracking Engine === */
const Model = {
  _storeKey: 'adaptive_dashboard_v1',
  _defaultData: () => ({
    panels: {
      cpu:    { id:'cpu',    title:'CPU Usage',     value:'42%',  unit:'%',  locked:false, collapsed:false, position:0 },
      memory: { id:'memory', title:'Memory',         value:'7.2',  unit:'GB', locked:false, collapsed:false, position:1 },
      disk:   { id:'disk',   title:'Disk I/O',       value:'128',  unit:'MB/s',locked:false, collapsed:false, position:2 },
      net:    { id:'net',    title:'Network',        value:'3.1',  unit:'Gbps',locked:false, collapsed:false, position:3 },
      reqs:   { id:'reqs',   title:'Requests/s',     value:'2.4k', unit:'',    locked:false, collapsed:false, position:4 },
      errors: { id:'errors', title:'Error Rate',     value:'0.12', unit:'%',   locked:false, collapsed:false, position:5 },
      users:  { id:'users',  title:'Active Users',   value:'189',  unit:'',    locked:false, collapsed:false, position:6 },
      latency:{ id:'latency',title:'P95 Latency',    value:'34',   unit:'ms',  locked:false, collapsed:false, position:7 },
    },
    tracking: {},
    layoutOrder: null,
  }),
  load() {
    try {
      const raw = localStorage.getItem(this._storeKey);
      if (!raw) return this._defaultData();
      const saved = JSON.parse(raw);
      const def = this._defaultData();
      for (const [id, p] of Object.entries(saved.panels||{})) {
        if (def.panels[id]) Object.assign(def.panels[id], p);
      }
      if (saved.layoutOrder) {
        def.layoutOrder = saved.layoutOrder;
        def.layoutOrder.forEach((id, i) => { if (def.panels[id]) def.panels[id].position = i; });
      }
      def.tracking = saved.tracking || {};
      return def;
    } catch { return this._defaultData(); }
  },
  save(data) {
    try { localStorage.setItem(this._storeKey, JSON.stringify(data)); } catch {}
  },
  getScore(panelId, tracking) {
    const t = tracking[panelId] || { views:0, totalDuration:0, interactions:0, lastSeen:0 };
    const now = Date.now();
    const recencyHours = Math.max(0.1, (now - (t.lastSeen||now)) / 3600000);
    const recency = 1 / recencyHours;
    const freq = t.views || 1;
    const dur = Math.max(1, (t.totalDuration||0) / 1000);
    return freq * dur * recency;
  },
  rankPanels(data) {
    const entries = Object.values(data.panels).map(p => ({
      id: p.id,
      score: this.getScore(p.id, data.tracking),
      locked: p.locked,
      collapsed: p.collapsed,
      position: p.position,
    }));
    const unlocked = entries.filter(e => !e.locked).sort((a,b) => b.score - a.score);
    const locked = entries.filter(e => e.locked).sort((a,b) => a.position - b.position);
    const ranked = [];
    let ui = 0;
    for (let i = 0; i < entries.length; i++) {
      const lockAtPos = locked.find(l => l.position === i);
      if (lockAtPos) { ranked.push(lockAtPos); continue; }
      if (ui < unlocked.length) ranked.push(unlocked[ui++]);
    }
    for (; ui < unlocked.length; ui++) ranked.push(unlocked[ui]);
    return ranked.map((e, i) => ({ ...e, rank: i }));
  }
};
/* === CONTROLLER: Dashboard Logic === */
const Dashboard = {
  _data: null,
  _ranked: null,
  _viewTimers: {},
  _dragState: null,
  _autoEnabled: true,
  _intersectionObserver: null,
  init() {
    this._data = Model.load();
    this._ranked = Model.rankPanels(this._data);
    this.render();
    this._setupIntersectionObserver();
    setInterval(() => this._heartbeat(), 2000);
    this._log('Dashboard initialized');
  },
  _setupIntersectionObserver() {
    this._intersectionObserver = new IntersectionObserver((entries) => {
      for (const e of entries) {
        const panelId = e.target.dataset.panelId;
        if (!panelId) continue;
        if (e.isIntersecting) {
          this._viewTimers[panelId] = Date.now();
        } else if (this._viewTimers[panelId]) {
          const duration = Date.now() - this._viewTimers[panelId];
          this.track(panelId, 'view', duration);
          delete this._viewTimers[panelId];
        }
      }
    }, { threshold: 0.5 });
  },
  _observePanels() {
    document.querySelectorAll('.panel').forEach(el => {
      this._intersectionObserver.unobserve(el);
      this._intersectionObserver.observe(el);
    });
  },
  _heartbeat() {
    const now = Date.now();
    for (const [id, start] of Object.entries(this._viewTimers)) {
      if (start) {
        this.track(id, 'view', now - start);
        this._viewTimers[id] = now;
      }
    }
  },
  track(panelId, event, duration = 0) {
    if (!this._data.tracking[panelId]) {
      this._data.tracking[panelId] = { views:0, totalDuration:0, interactions:0, lastSeen:0 };
    }
    const t = this._data.tracking[panelId];
    if (event === 'view') {
      t.views++;
      t.totalDuration += duration;
      t.lastSeen = Date.now();
    } else {
      t.interactions++;
      t.lastSeen = Date.now();
    }
    Model.save(this._data);
    this._log(`${panelId}: ${event}${duration ? ' ('+Math.round(duration/1000)+'s)' : ''}`);
  },
  _log(msg) {
    const el = document.getElementById('log-entries');
    if (!el) return;
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.textContent = new Date().toLocaleTimeString() + ' ' + msg;
    el.prepend(entry);
    if (el.children.length > 50) el.lastChild.remove();
  },
  render() {
    if (!this._autoEnabled && this._data.layoutOrder) {
      this._ranked = this._data.layoutOrder.map((id, i) => ({
        id, score: Model.getScore(id, this._data.tracking),
        locked: this._data.panels[id]?.locked || false,
        collapsed: this._data.panels[id]?.collapsed || false,
        position: i, rank: i,
      }));
    } else {
      this._ranked = Model.rankPanels(this._data);
    }
    this._updateGrid();
    this._observePanels();
  },
  _updateGrid() {
    const grid = document.getElementById('grid');
    const ranked = this._ranked;
    const total = ranked.length;
    const topCutoff = Math.ceil(total * 0.5);
    const spans = ranked.map((r, i) => {
      if (r.locked && this._data.panels[r.id]) {
        this._data.panels[r.id].position = i;
        return { id: r.id, compact: this._data.panels[r.id].collapsed, position: i };
      }
      const compact = i >= topCutoff || (r.score < (ranked[0]?.score||1) * 0.15 && i > 2);
      if (this._data.panels[r.id]) this._data.panels[r.id].collapsed = compact;
      return { id: r.id, compact, position: i };
    });
    grid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(220px, 1fr))';
    const existing = new Map();
    grid.querySelectorAll('.panel').forEach(el => existing.set(el.dataset.panelId, el));
    const fragment = document.createDocumentFragment();
    for (const s of spans) {
      let el = existing.get(s.id);
      if (!el) {
        el = this._createPanelElement(s.id);
      } else {
        existing.delete(s.id);
      }
      el.style.order = s.position;
      if (s.compact) {
        el.classList.add('compact');
        el.style.gridColumn = 'span 1';
        el.style.gridRow = 'span 1';
      } else {
        el.classList.remove('compact');
        const isTop = s.position < 2;
        el.style.gridColumn = isTop ? 'span 2' : 'span 1';
        el.style.gridRow = isTop ? 'span 2' : 'span 1';
      }
      fragment.appendChild(el);
    }
    grid.innerHTML = '';
    grid.appendChild(fragment);
    existing.forEach(el => el.remove());
    this._data.layoutOrder = spans.map(s => s.id);
    Model.save(this._data);
  },
  _createPanelElement(panelId) {
    const p = this._data.panels[panelId];
    const el = document.createElement('div');
    el.className = 'panel';
    el.dataset.panelId = panelId;
    el.draggable = true;
    el.innerHTML =
      '<div class="panel-header">' +
        '<span class="panel-title">' + this._esc(p.title) + '</span>' +
        '<span class="panel-rank">#' + (this._ranked.findIndex(r=>r.id===panelId)+1) + ' | ' + (Model.getScore(panelId, this._data.tracking)/1000).toFixed(1) + '</span>' +
        '<div class="panel-controls">' +
          '<button class="btn-collapse" title="Toggle compact">' + (p.collapsed ? '⊞' : '⊟') + '</button>' +
          '<button class="btn-lock ' + (p.locked ? 'locked' : '') + '" title="Lock position">🔒</button>' +
        '</div>' +
      '</div>' +
      '<div class="panel-body">' + this._esc(p.value) + '<span style="font-size:.6em;color:#64748b">' + this._esc(p.unit) + '</span></div>' +
      '<div class="panel-preview">' + this._esc(p.title) + ': ' + this._esc(p.value) + this._esc(p.unit) + '</div>';
    el.querySelector('.btn-collapse').addEventListener('click', (e) => {
      e.stopPropagation();
      this.togglePanel(panelId);
    });
    el.querySelector('.btn-lock').addEventListener('click', (e) => {
      e.stopPropagation();
      this.toggleLock(panelId);
    });
    el.addEventListener('click', () => this.track(panelId, 'interaction'));
    el.addEventListener('dragstart', (e) => this._onDragStart(e, panelId));
    el.addEventListener('dragover', (e) => e.preventDefault());
    el.addEventListener('drop', (e) => this._onDrop(e, panelId));
    el.addEventListener('dragend', () => this._onDragEnd());
    return el;
  },
  _esc(s) { const d=document.createElement('div'); d.textContent=s; return d.innerHTML; },
  togglePanel(panelId) {
    if (!this._data.panels[panelId]) return;
    this._data.panels[panelId].collapsed = !this._data.panels[panelId].collapsed;
    this.track(panelId, this._data.panels[panelId].collapsed ? 'collapse' : 'expand');
    this.render();
    this._updateStatus('Panel ' + panelId + ' ' + (this._data.panels[panelId].collapsed ? 'collapsed' : 'expanded'));
  },
  toggleLock(panelId) {
    if (!this._data.panels[panelId]) return;
    this._data.panels[panelId].locked = !this._data.panels[panelId].locked;
    this._data.panels[panelId].position = this._ranked.findIndex(r => r.id === panelId);
    this.track(panelId, this._data.panels[panelId].locked ? 'lock' : 'unlock');
    this.render();
    const status = document.getElementById('status-text');
    if (status) status.textContent = panelId + ' ' + (this._data.panels[panelId].locked ? 'locked' : 'unlocked');
  },
  toggleAuto() {
    this._autoEnabled = !this._autoEnabled;
    const btn = document.getElementById('btn-auto');
    if (btn) { btn.textContent = 'Auto: ' + (this._autoEnabled ? 'ON' : 'OFF'); btn.classList.toggle('active', this._autoEnabled); }
    if (!this._autoEnabled) {
      this._data.layoutOrder = this._ranked.map(r => r.id);
      Model.save(this._data);
    }
    this.render();
    this._updateStatus('Auto-layout ' + (this._autoEnabled ? 'enabled' : 'disabled — manual override active'));
  },
  resetLayout() {
    this._data = Model._defaultData();
    this._ranked = Model.rankPanels(this._data);
    Model.save(this._data);
    this.render();
    this._updateStatus('Layout reset to defaults');
  },
  resetTracking() {
    this._data.tracking = {};
    this._ranked = Model.rankPanels(this._data);
    Model.save(this._data);
    this.render();
    this._updateStatus('Tracking data cleared');
  },
  _updateStatus(msg) {
    const el = document.getElementById('status-text');
    if (el) el.textContent = msg;
  },
  _onDragStart(e, panelId) {
    this._dragState = { panelId, el: e.target };
    e.target.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', panelId);
  },
  _onDrop(e, targetPanelId) {
    e.preventDefault();
    if (!this._dragState || this._dragState.panelId === targetPanelId) return;
    const fromId = this._dragState.panelId;
    if (!this._data.panels[fromId] || !this._data.panels[targetPanelId]) return;
    const fromIdx = this._ranked.findIndex(r => r.id === fromId);
    const toIdx = this._ranked.findIndex(r => r.id === targetPanelId);
    if (fromIdx < 0 || toIdx < 0) return;
    const [moved] = this._ranked.splice(fromIdx, 1);
    this._ranked.splice(toIdx, 0, moved);
    this._data.layoutOrder = this._ranked.map(r => r.id);
    if (this._data.panels[fromId]) this._data.panels[fromId].position = toIdx;
    if (this._data.panels[fromId]) this._data.panels[fromId].locked = true;
    Model.save(this._data);
    this.track(fromId, 'drag-drop');
    this.render();
    this._updateStatus('Panel ' + fromId + ' moved to position ' + (toIdx+1) + ' (locked)');
  },
  _onDragEnd() {
    if (this._dragState?.el) this._dragState.el.classList.remove('dragging');
    this._dragState = null;
  },
};
document.addEventListener('DOMContentLoaded', () => Dashboard.init());
</script>
</body>
</html>
```