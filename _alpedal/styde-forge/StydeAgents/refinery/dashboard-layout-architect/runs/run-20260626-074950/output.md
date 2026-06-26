```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Layout</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface-hover: #242838;
  --border: #2a2e3a;
  --text: #e4e6ed;
  --text-dim: #8b8fa3;
  --accent: #6c8aff;
  --accent-glow: rgba(108,138,255,0.15);
  --radius: 10px;
  --handle-w: 32px;
  --header-h: 40px;
  --gap: 12px;
  --cols: 4;
  --min-col-w: 200px;
}
body {
  font-family: system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 20px;
}
.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto 16px;
  padding: 0 4px;
}
.dashboard-header h1 { font-size: 20px; font-weight: 600; }
.header-actions { display: flex; gap: 8px; }
.btn {
  padding: 6px 14px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
  font-size: 13px;
  transition: background 0.15s, border-color 0.15s;
}
.btn:hover { background: var(--surface-hover); border-color: var(--accent); }
.btn-primary {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}
.btn-primary:hover { filter: brightness(1.1); }
.grid-container {
  max-width: 1200px;
  margin: 0 auto;
}
.grid {
  display: grid;
  gap: var(--gap);
  grid-template-columns: repeat(var(--cols), 1fr);
  position: relative;
  min-height: 400px;
}
.grid.dragging * { pointer-events: none; user-select: none; }
.grid.dragging .panel { transition: transform 0.2s ease; }
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  transition: box-shadow 0.2s, border-color 0.2s;
  min-height: 80px;
}
.panel:hover { border-color: var(--accent); }
.panel.dragging {
  opacity: 0.6;
  z-index: 10;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}
.panel.drag-over { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-glow); }
.panel.collapsed .panel-body { display: none; }
.panel.collapsed { min-height: unset; }
.panel.collapsed .panel-header { border-bottom: none; }
[data-cols="1"] { grid-column: span 1; }
[data-cols="2"] { grid-column: span 2; }
[data-cols="3"] { grid-column: span 3; }
[data-cols="4"] { grid-column: span 4; }
[data-rows="1"] { grid-row: span 1; }
[data-rows="2"] { grid-row: span 2; }
[data-rows="3"] { grid-row: span 3; }
.panel-header {
  display: flex;
  align-items: center;
  height: var(--header-h);
  padding: 0 8px 0 4px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  cursor: grab;
  gap: 4px;
}
.panel-header:active { cursor: grabbing; }
.drag-handle {
  width: var(--handle-w);
  height: var(--handle-w);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-dim);
  cursor: grab;
  flex-shrink: 0;
}
.drag-handle svg { width: 16px; height: 16px; }
.drag-handle:active { cursor: grabbing; }
.panel-title {
  flex: 1;
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding: 0 4px;
}
.panel-controls {
  display: flex;
  gap: 2px;
  flex-shrink: 0;
}
.panel-controls button {
  width: 26px;
  height: 26px;
  border: none;
  background: transparent;
  color: var(--text-dim);
  cursor: pointer;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  transition: background 0.15s, color 0.15s;
}
.panel-controls button:hover {
  background: var(--surface-hover);
  color: var(--text);
}
.panel-controls .collapse-btn:hover { color: var(--accent); }
.panel-controls .hide-btn:hover { color: #f56c6c; }
.panel-body {
  flex: 1;
  padding: 16px;
  font-size: 13px;
  color: var(--text-dim);
  line-height: 1.5;
  min-height: 60px;
  overflow-y: auto;
}
.resize-handle {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 14px;
  height: 14px;
  cursor: nwse-resize;
  z-index: 5;
}
.resize-handle::after {
  content: '';
  position: absolute;
  right: 3px;
  bottom: 3px;
  width: 6px;
  height: 6px;
  border-right: 2px solid var(--text-dim);
  border-bottom: 2px solid var(--text-dim);
  opacity: 0.4;
  transition: opacity 0.15s;
}
.panel:hover .resize-handle::after { opacity: 0.8; }
.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--text-dim);
  border: 2px dashed var(--border);
  border-radius: var(--radius);
  font-size: 14px;
  gap: 8px;
}
.empty-state.hidden { display: none; }
</style>
</head>
<body>
<div class="dashboard-header">
  <h1>Dashboard</h1>
  <div class="header-actions">
    <button class="btn" onclick="Layout.reset()">Reset layout</button>
    <button class="btn btn-primary" onclick="Layout.save()">Save layout</button>
  </div>
</div>
<div class="grid-container">
  <div class="grid" id="grid"></div>
  <div class="empty-state hidden" id="emptyState">
    <span style="font-size:32px; opacity:0.3;">[]</span>
    <span>No panels visible. Add panels or reset layout.</span>
  </div>
</div>
<script>
// ---------- Default layout ----------
const DEFAULT_PANELS = [
  { id: 'metrics',     title: 'Metrics',       cols: 2, rows: 1, content: 'Active users, revenue, bounce rate. Key metrics at a glance.' },
  { id: 'chart',       title: 'Revenue Chart', cols: 2, rows: 2, content: 'Line chart showing 30-day revenue trend with forecast overlay.' },
  { id: 'activity',    title: 'Recent Activity', cols: 1, rows: 2, content: 'User signups, purchases, support tickets from last 24h.' },
  { id: 'alerts',      title: 'Alerts',        cols: 1, rows: 1, content: '3 critical alerts, 12 warnings. Review recommended.' },
  { id: 'top-users',   title: 'Top Users',     cols: 1, rows: 1, content: '1. alice (342 pts)  2. bob (289 pts)  3. carol (201 pts)' },
  { id: 'settings-summary', title: 'Settings', cols: 1, rows: 1, content: 'Theme: dark. Notifications: on. Auto-refresh: 30s.' },
];
const STORAGE_KEY_PREFIX = 'dashboard_layout_';
// ---------- Layout engine ----------
class DashboardLayout {
  constructor(gridEl, emptyEl, profile = 'default') {
    this.grid = gridEl;
    this.empty = emptyEl;
    this.profile = profile;
    this.panels = [];
    this.dragState = null;
    this.resizeState = null;
    this.load();
  }
  get storageKey() { return STORAGE_KEY_PREFIX + this.profile; }
  serialize() {
    return this.panels.map(p => ({
      id: p.id, title: p.title, cols: p.cols, rows: p.rows,
      content: p.content, collapsed: p.collapsed, visible: p.visible,
      order: p.order
    }));
  }
  deserialize(data) {
    return data.map(d => this._createPanel(d.id, d.title, d.cols, d.rows, d.content, d.collapsed, d.visible, d.order));
  }
  _createPanel(id, title, cols, rows, content, collapsed = false, visible = true, order = null) {
    return { id, title, cols: Math.min(cols, 4), rows, content, collapsed, visible, order, el: null };
  }
  load() {
    let data;
    try {
      const raw = localStorage.getItem(this.storageKey);
      data = raw ? JSON.parse(raw) : null;
    } catch(e) { data = null; }
    if (data && Array.isArray(data) && data.length) {
      this.panels = this.deserialize(data);
      // Ensure order field for sorting
      this.panels.forEach((p, i) => { if (p.order === undefined || p.order === null) p.order = i; });
      this.panels.sort((a, b) => (a.order || 0) - (b.order || 0));
    } else {
      this.resetToDefault();
    }
    this.render();
  }
  save() {
    this.panels.forEach((p, i) => p.order = i);
    localStorage.setItem(this.storageKey, JSON.stringify(this.serialize()));
  }
  syncToServer() {
    // Stub: POST /api/profile/layout with this.serialize()
    // fetch('/api/profile/layout', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(this.serialize()) });
  }
  reset() {
    if (!confirm('Reset layout to default? Unsaved changes will be lost.')) return;
    this.resetToDefault();
    this.save();
    this.render();
  }
  resetToDefault() {
    this.panels = this.deserialize(DEFAULT_PANELS.map((d, i) => ({
      ...d, collapsed: false, visible: true, order: i
    })));
  }
  render() {
    this.grid.innerHTML = '';
    const visible = this.panels.filter(p => p.visible);
    if (visible.length === 0) {
      this.empty.classList.remove('hidden');
      this.grid.style.display = 'none';
      return;
    }
    this.empty.classList.add('hidden');
    this.grid.style.display = 'grid';
    visible.forEach((panel, idx) => {
      panel.order = idx;
      const el = document.createElement('div');
      el.className = 'panel' + (panel.collapsed ? ' collapsed' : '');
      el.dataset.id = panel.id;
      el.dataset.cols = panel.cols;
      el.dataset.rows = panel.rows;
      el.draggable = false;
      el.innerHTML = `
        <div class="panel-header">
          <div class="drag-handle" data-action="drag">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M5 4h6M5 8h6M5 12h6"/></svg>
          </div>
          <span class="panel-title">${this._esc(panel.title)}</span>
          <div class="panel-controls">
            <button class="collapse-btn" data-action="collapse" title="${panel.collapsed ? 'Expand' : 'Collapse'}">${panel.collapsed ? '+' : '−'}</button>
            <button class="hide-btn" data-action="hide" title="Hide panel">✕</button>
          </div>
        </div>
        <div class="panel-body">${this._esc(panel.content)}</div>
        <div class="resize-handle" data-action="resize"></div>
      `;
      panel.el = el;
      panel._body = el.querySelector('.panel-body');
      this.grid.appendChild(el);
    });
    this._bindEvents();
  }
  _esc(s) {
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }
  _bindEvents() {
    // --- Drag via pointer events ---
    const onPointerDown = (e) => {
      const handle = e.target.closest('[data-action="drag"]');
      if (!handle) return;
      const panelEl = handle.closest('.panel');
      if (!panelEl) return;
      e.preventDefault();
      panelEl.setPointerCapture(e.pointerId);
      const panel = this.panels.find(p => p.id === panelEl.dataset.id);
      if (!panel) return;
      this.dragState = {
        panel, el: panelEl,
        startX: e.clientX, startY: e.clientY,
        startCol: parseInt(panelEl.dataset.cols),
        startRow: parseInt(panelEl.dataset.rows),
      };
      panelEl.classList.add('dragging');
      this.grid.classList.add('dragging');
    };
    const onPointerMove = (e) => {
      if (!this.dragState) return;
      e.preventDefault();
      const { el, startX, startY } = this.dragState;
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      if (Math.abs(dx) < 8 && Math.abs(dy) < 8) return;
      // Find drop target
      const target = document.elementFromPoint(e.clientX, e.clientY);
      if (!target) return;
      const targetPanel = target.closest('.panel');
      if (!targetPanel || targetPanel === el) {
        document.querySelectorAll('.panel.drag-over').forEach(p => p.classList.remove('drag-over'));
        return;
      }
      document.querySelectorAll('.panel.drag-over').forEach(p => p.classList.remove('drag-over'));
      targetPanel.classList.add('drag-over');
    };
    const onPointerUp = (e) => {
      if (!this.dragState) return;
      const { el } = this.dragState;
      el.classList.remove('dragging');
      this.grid.classList.remove('dragging');
      document.querySelectorAll('.panel.drag-over').forEach(p => p.classList.remove('drag-over'));
      // Swapping logic
      const dropEl = document.querySelector('.panel.drag-over');
      if (dropEl && dropEl !== el) {
        const dragId = el.dataset.id;
        const dropId = dropEl.dataset.id;
        const dragIdx = this.panels.findIndex(p => p.id === dragId);
        const dropIdx = this.panels.findIndex(p => p.id === dropId);
        if (dragIdx !== -1 && dropIdx !== -1) {
          // Swap in the panels array
          const visiblePanels = this.panels.filter(p => p.visible);
          const dragVisibleIdx = visiblePanels.indexOf(this.panels[dragIdx]);
          const dropVisibleIdx = visiblePanels.indexOf(this.panels[dropIdx]);
          if (dragVisibleIdx !== -1 && dropVisibleIdx !== -1) {
            // Swap order
            const tempOrder = this.panels[dragIdx].order;
            this.panels[dragIdx].order = this.panels[dropIdx].order;
            this.panels[dropIdx].order = tempOrder;
            this.panels.sort((a, b) => (a.order || 0) - (b.order || 0));
            this.render();
            this.save();
          }
        }
      }
      this.dragState = null;
    };
    this.grid.addEventListener('pointerdown', onPointerDown);
    this.grid.addEventListener('pointermove', onPointerMove);
    this.grid.addEventListener('pointerup', onPointerUp);
    this.grid.addEventListener('pointercancel', onPointerUp);
    // --- Collapse / Hide / Resize via delegation ---
    this.grid.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      const action = btn.dataset.action;
      if (action === 'drag' || action === 'resize') return;
      const panelEl = btn.closest('.panel');
      if (!panelEl) return;
      const panel = this.panels.find(p => p.id === panelEl.dataset.id);
      if (!panel) return;
      if (action === 'collapse') {
        panel.collapsed = !panel.collapsed;
        this.render();
        this.save();
      } else if (action === 'hide') {
        panel.visible = false;
        this.render();
        this.save();
      }
    });
    // --- Resize via pointer ---
    const onResizeDown = (e) => {
      const handle = e.target.closest('[data-action="resize"]');
      if (!handle) return;
      const panelEl = handle.closest('.panel');
      if (!panelEl) return;
      e.preventDefault();
      panelEl.setPointerCapture(e.pointerId);
      const panel = this.panels.find(p => p.id === panelEl.dataset.id);
      if (!panel) return;
      this.resizeState = {
        panel, el: panelEl,
        startX: e.clientX, startY: e.clientY,
        startCols: panel.cols,
        startRows: panel.rows,
      };
    };
    const onResizeMove = (e) => {
      if (!this.resizeState) return;
      e.preventDefault();
      const { el, startX, startY, startCols, startRows, panel } = this.resizeState;
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      // Determine grid cell size
      const gridRect = this.grid.getBoundingClientRect();
      const cols = parseInt(getComputedStyle(this.grid).getPropertyValue('--cols')) || 4;
      const gap = parseFloat(getComputedStyle(this.grid).gap) || 12;
      const cellW = (gridRect.width - gap * (cols - 1)) / cols;
      // Estimate row height from one panel
      const sample = this.grid.querySelector('.panel');
      const cellH = sample ? sample.getBoundingClientRect().height : 80;
      let newCols = Math.max(1, Math.min(4, Math.round(startCols + dx / (cellW + gap))));
      let newRows = Math.max(1, Math.min(4, Math.round(startRows + dy / (cellH + gap))));
      if (newCols !== panel.cols || newRows !== panel.rows) {
        panel.cols = newCols;
        panel.rows = newRows;
        el.dataset.cols = newCols;
        el.dataset.rows = newRows;
      }
    };
    const onResizeUp = (e) => {
      if (!this.resizeState) return;
      this.resizeState = null;
      this.save();
    };
    this.grid.addEventListener('pointerdown', onResizeDown);
    this.grid.addEventListener('pointermove', onResizeMove);
    this.grid.addEventListener('pointerup', onResizeUp);
    this.grid.addEventListener('pointercancel', onResizeUp);
  }
  // Public API for test/settings panel
  togglePanel(id) { const p = this.panels.find(p => p.id === id); if (p) { p.visible = !p.visible; this.render(); this.save(); } }
  collapsePanel(id) { const p = this.panels.find(p => p.id === id); if (p) { p.collapsed = !p.collapsed; this.render(); this.save(); } }
  getPanels() { return this.panels; }
}
// ---------- Init ----------
const profileKey = localStorage.getItem('dashboard_profile') || 'default';
const Layout = new DashboardLayout(
  document.getElementById('grid'),
  document.getElementById('emptyState'),
  profileKey
);
</script>
</body>
</html>
```