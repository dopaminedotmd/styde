```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Layout</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #0f1117; color: #e8eaed; min-height: 100vh;
}
.dashboard-wrapper {
  max-width: 1280px; margin: 0 auto; padding: 20px;
}
.toolbar {
  display: flex; gap: 12px; align-items: center;
  margin-bottom: 20px; padding: 12px 16px;
  background: #1a1d27; border-radius: 8px; border: 1px solid #2a2d3a;
}
.toolbar h1 { font-size: 18px; font-weight: 600; flex: 1; }
.toolbar button {
  padding: 8px 16px; border-radius: 6px; border: 1px solid #3a3d4a;
  background: #252833; color: #e8eaed; cursor: pointer;
  font-size: 13px; font-weight: 500; transition: background .15s;
}
.toolbar button:hover { background: #323644; }
.toolbar button:active { background: #3a3e4e; }
.toolbar button:focus-visible { outline: 2px solid #5b9aff; outline-offset: 2px; }
.toolbar .undo-redo { display: flex; gap: 4px; }
.toolbar .undo-redo button { padding: 8px 12px; min-width: 36px; }
.grid-container {
  position: relative;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 12px;
  padding: 4px;
  min-height: 400px;
}
.grid-item {
  position: relative;
  background: #1a1d27;
  border: 1px solid #2a2d3a;
  border-radius: 8px;
  overflow: hidden;
  display: flex; flex-direction: column;
  transition: box-shadow .2s;
  user-select: none;
}
.grid-item:focus-within { border-color: #5b9aff; }
.grid-item.dragging {
  z-index: 100;
  opacity: 0.85;
  box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.grid-item.collapsed .panel-body { display: none; }
.grid-item.hidden { display: none; }
.panel-header {
  display: flex; align-items: center;
  padding: 8px 10px; gap: 6px;
  background: #22263a; border-bottom: 1px solid #2a2d3a;
  cursor: grab; min-height: 36px;
}
.panel-header:active { cursor: grabbing; }
.panel-header.drag-active { background: #2a2e44; }
.panel-header .panel-title {
  flex: 1; font-size: 13px; font-weight: 500;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.panel-header .panel-controls {
  display: flex; gap: 2px; align-items: center;
}
.panel-controls button {
  width: 26px; height: 26px; border-radius: 4px;
  border: none; background: transparent; color: #9aa0b0;
  cursor: pointer; display: flex; align-items: center;
  justify-content: center; font-size: 14px; line-height: 1;
  transition: background .15s, color .15s;
}
.panel-controls button:hover { background: #2e324a; color: #e8eaed; }
.panel-controls button:focus-visible { outline: 2px solid #5b9aff; outline-offset: 1px; }
.panel-controls button.collapse-btn { font-size: 10px; }
.panel-body {
  flex: 1; padding: 16px; min-height: 60px;
  display: flex; align-items: center; justify-content: center;
  color: #6b7180; font-size: 13px;
}
.resize-handle {
  position: absolute; bottom: 0; right: 0;
  width: 14px; height: 14px; cursor: nwse-resize;
  z-index: 10;
}
.resize-handle::after {
  content: ''; position: absolute; bottom: 3px; right: 3px;
  width: 8px; height: 8px;
  border-right: 2px solid #5a6070;
  border-bottom: 2px solid #5a6070;
}
.resize-handle:hover::after { border-color: #8a90a0; }
.placeholder {
  position: relative;
  background: #1e212b; border: 1px dashed #2e324a;
  border-radius: 8px; min-height: 60px;
}
.toast {
  position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
  background: #252833; color: #e8eaed;
  padding: 10px 20px; border-radius: 6px; border: 1px solid #3a3d4a;
  font-size: 13px; z-index: 1000;
  opacity: 0; transition: opacity .3s;
  pointer-events: none;
}
.toast.visible { opacity: 1; }
</style>
</head>
<body>
<div class="dashboard-wrapper">
  <div class="toolbar" role="toolbar" aria-label="Dashboard toolbar">
    <h1>Dashboard</h1>
    <div class="undo-redo">
      <button id="undoBtn" title="Undo (Ctrl+Z)" aria-label="Undo">&larr;</button>
      <button id="redoBtn" title="Redo (Ctrl+Shift+Z)" aria-label="Redo">&rarr;</button>
    </div>
    <button id="resetBtn" title="Reset to default layout">Reset</button>
  </div>
  <div id="grid" class="grid-container" role="grid" aria-label="Dashboard grid"></div>
</div>
<div id="toast" class="toast"></div>
<script>
class DashboardLayout {
  static DEFAULT_PROFILE = 'default';
  static STORAGE_KEY = 'dash_layout';
  static GRID_COLS = 12;
  static MIN_COL = 2;
  static MIN_ROW = 1;
  constructor(containerEl, options = {}) {
    this.container = containerEl;
    this.profile = options.profile || DashboardLayout.DEFAULT_PROFILE;
    this.onSave = options.onSave || null;
    this.panels = [];
    this.nextId = 1;
    this.undoStack = [];
    this.redoStack = [];
    this.maxUndo = 50;
    this.dragState = null;
    this.resizeState = null;
    this.signal = null;
    this.destroyed = false;
    this._bind();
    this._load();
    this._render();
  }
  // --- Public API ---
  addPanel(panel) {
    this._pushUndo();
    const p = { id: this.nextId++, ...panel };
    if (!p.col) p.col = 1;
    if (!p.row) p.row = this._nextFreeRow();
    if (!p.w) p.w = 3;
    if (!p.h) p.h = 2;
    p.collapsed = false;
    p.hidden = false;
    this.panels.push(p);
    this._save();
    this._render();
    this._toast('Panel added');
    return p.id;
  }
  removePanel(id) {
    const idx = this.panels.findIndex(p => p.id === id);
    if (idx === -1) return;
    this._pushUndo();
    this.panels.splice(idx, 1);
    this._save();
    this._render();
    this._toast('Panel removed');
  }
  getLayout() {
    return this.panels.map(p => ({
      id: p.id, title: p.title, col: p.col, row: p.row,
      w: p.w, h: p.h, collapsed: p.collapsed, hidden: p.hidden
    }));
  }
  setLayout(layout) {
    this._pushUndo();
    this.panels = layout.map((item, i) => ({
      id: item.id || this.nextId++,
      title: item.title || `Panel ${i+1}`,
      content: item.content || '',
      col: item.col || 1,
      row: item.row || (i + 1),
      w: item.w || 3,
      h: item.h || 2,
      collapsed: !!item.collapsed,
      hidden: !!item.hidden
    }));
    this.nextId = Math.max(this.nextId, ...this.panels.map(p => p.id)) + 1;
    this._save();
    this._render();
    this._toast('Layout applied');
  }
  resetToDefault() {
    this._pushUndo();
    this._loadDefaultPanels();
    this._save();
    this._render();
    this._toast('Reset to default layout');
  }
  destroy() {
    this.destroyed = true;
    if (this.signal) {
      this.signal.abort();
      this.signal = null;
    }
    this.dragState = null;
    this.resizeState = null;
  }
  // --- Internal ---
  _bind() {
    if (this.signal) this.signal.abort();
    this.signal = new AbortController();
    const opts = { signal: this.signal };
    // Event delegation on container
    this.container.addEventListener('pointerdown', e => this._onPointerDown(e), opts);
    document.addEventListener('pointermove', e => this._onPointerMove(e), { ...opts, passive: true });
    document.addEventListener('pointerup', e => this._onPointerUp(e), opts);
    document.addEventListener('pointercancel', e => this._onPointerUp(e), opts);
    document.addEventListener('keydown', e => this._onKeyDown(e), opts);
    // Toolbar buttons
    document.getElementById('undoBtn').addEventListener('click', () => this.undo(), opts);
    document.getElementById('redoBtn').addEventListener('click', () => this.redo(), opts);
    document.getElementById('resetBtn').addEventListener('click', () => this.resetToDefault(), opts);
  }
  _nextFreeRow() {
    if (this.panels.length === 0) return 1;
    return Math.max(...this.panels.map(p => p.row + p.h)) + 1;
  }
  _loadDefaultPanels() {
    this.panels = [
      { id: this.nextId++, title: 'Metrics', content: 'KPI dashboard', col: 1, row: 1, w: 4, h: 2, collapsed: false, hidden: false, },
      { id: this.nextId++, title: 'Chart', content: 'Line chart widget', col: 5, row: 1, w: 4, h: 3, collapsed: false, hidden: false, },
      { id: this.nextId++, title: 'Activity', content: 'Recent activity feed', col: 9, row: 1, w: 4, h: 2, collapsed: false, hidden: false, },
      { id: this.nextId++, title: 'Tasks', content: 'Task list widget', col: 1, row: 3, w: 4, h: 2, collapsed: false, hidden: false, },
      { id: this.nextId++, title: 'Calendar', content: 'Upcoming events', col: 5, row: 4, w: 4, h: 2, collapsed: false, hidden: false, },
      { id: this.nextId++, title: 'Notes', content: 'Quick notes panel', col: 9, row: 3, w: 4, h: 3, collapsed: false, hidden: false, },
    ];
  }
  _save() {
    const data = this.panels.map(p => ({
      id: p.id, title: p.title, content: p.content,
      col: p.col, row: p.row, w: p.w, h: p.h,
      collapsed: p.collapsed, hidden: p.hidden
    }));
    const key = `${DashboardLayout.STORAGE_KEY}_${this.profile}`;
    try { localStorage.setItem(key, JSON.stringify(data)); } catch(e) {}
    if (this.onSave) this.onSave(this.getLayout());
  }
  _load() {
    const key = `${DashboardLayout.STORAGE_KEY}_${this.profile}`;
    let data;
    try { data = JSON.parse(localStorage.getItem(key)); } catch(e) {}
    if (data && Array.isArray(data) && data.length > 0) {
      this.panels = data.map((d, i) => ({
        id: d.id || this.nextId++,
        title: d.title || `Panel ${i+1}`,
        content: d.content || '',
        col: d.col || 1,
        row: d.row || (i + 1),
        w: d.w || 3,
        h: d.h || 2,
        collapsed: !!d.collapsed,
        hidden: !!d.hidden
      }));
      this.nextId = Math.max(this.nextId, ...this.panels.map(p => p.id)) + 1;
    } else {
      this._loadDefaultPanels();
    }
  }
  _clonePanels() {
    return this.panels.map(p => ({ ...p }));
  }
  _pushUndo() {
    const snapshot = this._clonePanels();
    this.undoStack.push(JSON.stringify(snapshot));
    if (this.undoStack.length > this.maxUndo) this.undoStack.shift();
    this.redoStack = [];
    this._updateUndoButtons();
  }
  undo() {
    if (this.undoStack.length === 0) return;
    const current = JSON.stringify(this._clonePanels());
    this.redoStack.push(current);
    const prev = JSON.parse(this.undoStack.pop());
    this.panels = prev;
    this._save();
    this._render();
    this._updateUndoButtons();
    this._toast('Undo');
  }
  redo() {
    if (this.redoStack.length === 0) return;
    const current = JSON.stringify(this._clonePanels());
    this.undoStack.push(current);
    const next = JSON.parse(this.redoStack.pop());
    this.panels = next;
    this._save();
    this._render();
    this._updateUndoButtons();
    this._toast('Redo');
  }
  _updateUndoButtons() {
    document.getElementById('undoBtn').disabled = this.undoStack.length === 0;
    document.getElementById('redoBtn').disabled = this.redoStack.length === 0;
  }
  _toast(msg) {
    const el = document.getElementById('toast');
    el.textContent = msg;
    el.classList.add('visible');
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => el.classList.remove('visible'), 2000);
  }
  _resolveCollisions(excludeId) {
    // push-down-with-gravity: move overlapping panels below
    const sorted = [...this.panels].filter(p => p.id !== excludeId)
      .sort((a, b) => a.row - b.row || a.col - b.col);
    const occupied = new Set();
    for (const p of sorted) {
      if (p.hidden) continue;
      for (let r = p.row; r < p.row + p.h; r++) {
        for (let c = p.col; c < p.col + p.w; c++) {
          occupied.add(`${r},${c}`);
        }
      }
    }
    // Simple O(n) pass — push down until no overlap
    let changed = true;
    let iterations = 0;
    const maxIter = this.panels.length * 4;
    while (changed && iterations < maxIter) {
      changed = false;
      iterations++;
      occupied.clear();
      for (const p of sorted) {
        if (p.hidden) continue;
        for (let r = p.row; r < p.row + p.h; r++) {
          for (let c = p.col; c < p.col + p.w; c++) {
            occupied.add(`${r},${c}`);
          }
        }
      }
      for (const p of sorted) {
        if (p.hidden) continue;
        // Check if current position overlaps something it shouldn't
        let overlap = false;
        check: for (let r = p.row; r < p.row + p.h; r++) {
          for (let c = p.col; c < p.col + p.w; c++) {
            if (r !== p.row || c !== p.col) {
              // Check if this cell is occupied by another panel
              const cellKey = `${r},${c}`;
              // Recalculate occupied excluding current panel
              let cellOccupied = false;
              for (const op of sorted) {
                if (op.id === p.id || op.hidden) continue;
                if (r >= op.row && r < op.row + op.h && c >= op.col && c < op.col + op.w) {
                  cellOccupied = true; break;
                }
              }
              if (cellOccupied) { overlap = true; break check; }
            }
          }
        }
        if (overlap) {
          p.row++;
          changed = true;
        }
      }
    }
    // Update the panels array
    for (const p of sorted) {
      const idx = this.panels.findIndex(pp => pp.id === p.id);
      if (idx !== -1) this.panels[idx] = p;
    }
  }
  _render() {
    const grid = this.container;
    grid.innerHTML = '';
    for (const p of this.panels) {
      if (p.hidden) continue;
      const el = document.createElement('div');
      el.className = 'grid-item' + (p.collapsed ? ' collapsed' : '');
      el.dataset.panelId = p.id;
      el.style.gridColumn = `${p.col} / span ${p.w}`;
      el.style.gridRow = `${p.row} / span ${p.h}`;
      el.setAttribute('role', 'gridcell');
      el.setAttribute('tabindex', '0');
      el.setAttribute('aria-label', `${p.title} panel`);
      const header = document.createElement('div');
      header.className = 'panel-header';
      header.dataset.action = 'drag';
      const title = document.createElement('span');
      title.className = 'panel-title';
      title.textContent = p.title;
      const controls = document.createElement('div');
      controls.className = 'panel-controls';
      const collapseBtn = document.createElement('button');
      collapseBtn.className = 'collapse-btn';
      collapseBtn.dataset.action = 'collapse';
      collapseBtn.dataset.panelId = p.id;
      collapseBtn.setAttribute('aria-label', p.collapsed ? 'Expand panel' : 'Collapse panel');
      collapseBtn.setAttribute('tabindex', '0');
      collapseBtn.innerHTML = p.collapsed ? '&#9654;' : '&#9660;';
      const hideBtn = document.createElement('button');
      hideBtn.className = 'hide-btn';
      hideBtn.dataset.action = 'hide';
      hideBtn.dataset.panelId = p.id;
      hideBtn.setAttribute('aria-label', 'Hide panel');
      hideBtn.setAttribute('tabindex', '0');
      hideBtn.innerHTML = '&#10005;';
      controls.appendChild(collapseBtn);
      controls.appendChild(hideBtn);
      header.appendChild(title);
      header.appendChild(controls);
      const body = document.createElement('div');
      body.className = 'panel-body';
      body.textContent = p.content || ' ';
      const resize = document.createElement('div');
      resize.className = 'resize-handle';
      resize.dataset.action = 'resize';
      resize.dataset.panelId = p.id;
      resize.setAttribute('aria-label', 'Resize panel');
      resize.setAttribute('tabindex', '0');
      el.appendChild(header);
      el.appendChild(body);
      el.appendChild(resize);
      grid.appendChild(el);
    }
    this._updateUndoButtons();
  }
  _getPanelEl(id) {
    return this.container.querySelector(`[data-panel-id="${id}"]`);
  }
  _getPanelById(id) {
    return this.panels.find(p => p.id === Number(id));
  }
  _getActionElement(e) {
    const target = e.target.closest('[data-action]');
    if (!target) return null;
    const action = target.dataset.action;
    const panelId = target.dataset.panelId
      ? Number(target.dataset.panelId)
      : (target.closest('.grid-item') ? Number(target.closest('.grid-item').dataset.panelId) : null);
    return { action, panelId, el: target };
  }
  _onPointerDown(e) {
    if (this.destroyed) return;
    const actionInfo = this._getActionElement(e);
    if (!actionInfo) return;
    const { action, panelId } = actionInfo;
    if (!panelId) return;
    const panel = this._getPanelById(panelId);
    if (!panel) return;
    // Ignore button clicks on controls (handled by click later)
    if (action === 'collapse' || action === 'hide') {
      return; // handled on click
    }
    if (action === 'drag') {
      e.preventDefault();
      this._startDrag(e, panel);
    } else if (action === 'resize') {
      e.preventDefault();
      this._startResize(e, panel);
    }
  }
  _startDrag(e, panel) {
    this._pushUndo();
    const el = this._getPanelEl(panel.id);
    if (!el) return;
    el.classList.add('dragging');
    el.style.zIndex = '100';
    const rect = el.getBoundingClientRect();
    const gridRect = this.container.getBoundingClientRect();
    this.dragState = {
      panelId: panel.id,
      startCol: panel.col,
      startRow: panel.row,
      col: panel.col,
      row: panel.row,
      offsetX: e.clientX - rect.left,
      offsetY: e.clientY - rect.top,
      gridRect,
      cellW: rect.width,
      cellH: rect.height,
      pointerId: e.pointerId,
    };
    el.setPointerCapture(e.pointerId);
  }
  _startResize(e, panel) {
    this._pushUndo();
    this.resizeState = {
      panelId: panel.id,
      startX: e.clientX,
      startY: e.clientY,
      startW: panel.w,
      startH: panel.h,
      pointerId: e.pointerId,
      rafId: null,
    };
  }
  _onPointerMove(e) {
    if (this.dragState) {
      this._updateDrag(e);
    }
    if (this.resizeState) {
      this._scheduleResize(e);
    }
  }
  _updateDrag(e) {
    const ds = this.dragState;
    if (!ds) return;
    const panel = this._getPanelById(ds.panelId);
    if (!panel) return;
    const gridRect = this.container.getBoundingClientRect();
    const gap = 12;
    const colW = (gridRect.width - gap * (DashboardLayout.GRID_COLS - 1)) / DashboardLayout.GRID_COLS;
    const rowH = colW * 0.5; // approximate cell height
    const x = e.clientX - gridRect.left - ds.offsetX;
    const y = e.clientY - gridRect.top - ds.offsetY;
    let newCol = Math.round(x / (colW + gap)) + 1;
    let newRow = Math.round(y / (rowH + gap)) + 1;
    newCol = Math.max(1, Math.min(newCol, DashboardLayout.GRID_COLS - panel.w + 1));
    newRow = Math.max(1, newRow);
    // Update panel position
    panel.col = newCol;
    panel.row = newRow;
    const el = this._getPanelEl(panel.id);
    if (el) {
      el.style.gridColumn = `${panel.col} / span ${panel.w}`;
      el.style.gridRow = `${panel.row} / span ${panel.h}`;
    }
  }
  _scheduleResize(e) {
    const rs = this.resizeState;
    if (!rs) return;
    // rAF gating: read inside rAF
    if (!rs.rafId) {
      rs.rafId = requestAnimationFrame(() => {
        if (!this.resizeState || this.resizeState.rafId !== rs.rafId) return;
        this._applyResize(rs);
        rs.rafId = null;
      });
    }
  }
  _applyResize(rs) {
    const panel = this._getPanelById(rs.panelId);
    if (!panel) return;
    const gridRect = this.container.getBoundingClientRect();
    const gap = 12;
    const colW = (gridRect.width - gap * (DashboardLayout.GRID_COLS - 1)) / DashboardLayout.GRID_COLS;
    const rowH = colW * 0.5;
    // Read pointer coords inside rAF — we stored them at rs.storedX/Y
    const dx = rs.dx || 0;
    const dy = rs.dy || 0;
    let newW = Math.round((rs.startW * (colW + gap) + dx) / (colW + gap));
    let newH = Math.round((rs.startH * (rowH + gap) + dy) / (rowH + gap));
    newW = Math.max(DashboardLayout.MIN_COL, Math.min(newW, DashboardLayout.GRID_COLS - panel.col + 1));
    newH = Math.max(DashboardLayout.MIN_ROW, newH);
    panel.w = newW;
    panel.h = newH;
    const el = this._getPanelEl(panel.id);
    if (el) {
      el.style.gridColumn = `${panel.col} / span ${panel.w}`;
      el.style.gridRow = `${panel.row} / span ${panel.h}`;
    }
  }
  _onPointerUp(e) {
    if (this.dragState) {
      const panel = this._getPanelById(this.dragState.panelId);
      if (panel) {
        const el = this._getPanelEl(panel.id);
        if (el) {
          el.classList.remove('dragging');
          el.style.zIndex = '';
          el.releasePointerCapture(e.pointerId);
        }
        this._resolveCollisions(panel.id);
        this._save();
        this._render();
      }
      this.dragState = null;
    }
    if (this.resizeState) {
      const panel = this._getPanelById(this.resizeState.panelId);
      if (panel) {
        this._resolveCollisions(panel.id);
        this._save();
        this._render();
      }
      if (this.resizeState.rafId) {
        cancelAnimationFrame(this.resizeState.rafId);
      }
      this.resizeState = null;
    }
  }
  _onKeyDown(e) {
    if (e.ctrlKey && e.key === 'z' && !e.shiftKey) {
      e.preventDefault(); this.undo();
    } else if (e.ctrlKey && e.key === 'z' && e.shiftKey) {
      e.preventDefault(); this.redo();
    } else if (e.ctrlKey && e.key === 'Z') {
      e.preventDefault(); this.redo();
    } else if (e.key === 'Escape') {
      if (this.dragState) { this._cancelDrag(); }
      if (this.resizeState) { this._cancelResize(); }
    } else if (e.key === 'Enter' || e.key === ' ') {
      const target = e.target.closest('[data-action]');
      if (!target) return;
      const panelId = Number(target.dataset.panelId);
      if (!panelId) return;
      const action = target.dataset.action;
      if (action === 'collapse') { this._toggleCollapse(panelId); e.preventDefault(); }
      else if (action === 'hide') { this._toggleHide(panelId); e.preventDefault(); }
    }
  }
  _cancelDrag() {
    if (!this.dragState) return;
    const panel = this._getPanelById(this.dragState.panelId);
    if (panel) {
      panel.col = this.dragState.startCol;
      panel.row = this.dragState.startRow;
      const el = this._getPanelEl(panel.id);
      if (el) {
        el.classList.remove('dragging');
        el.style.gridColumn = `${panel.col} / span ${panel.w}`;
        el.style.gridRow = `${panel.row} / span ${panel.h}`;
      }
    }
    this.dragState = null;
  }
  _cancelResize() {
    if (!this.resizeState) return;
    const panel = this._getPanelById(this.resizeState.panelId);
    if (panel) {
      panel.w = this.resizeState.startW;
      panel.h = this.resizeState.startH;
      const el = this._getPanelEl(panel.id);
      if (el) {
        el.style.gridColumn = `${panel.col} / span ${panel.w}`;
        el.style.gridRow = `${panel.row} / span ${panel.h}`;
      }
    }
    if (this.resizeState.rafId) cancelAnimationFrame(this.resizeState.rafId);
    this.resizeState = null;
  }
  _toggleCollapse(id) {
    this._pushUndo();
    const panel = this._getPanelById(id);
    if (!panel) return;
    panel.collapsed = !panel.collapsed;
    this._save();
    this._render();
    this._toast(panel.collapsed ? 'Panel collapsed' : 'Panel expanded');
  }
  _toggleHide(id) {
    this._pushUndo();
    const panel = this._getPanelById(id);
    if (!panel) return;
    panel.hidden = true;
    this._save();
    this._render();
    this._toast('Panel hidden (undo to restore)');
  }
  _onClick(e) {
    const actionInfo = this._getActionElement(e);
    if (!actionInfo) return;
    const { action, panelId } = actionInfo;
    if (!panelId) return;
    if (action === 'collapse') this._toggleCollapse(panelId);
    else if (action === 'hide') this._toggleHide(panelId);
  }
}
// --- Init ---
const grid = document.getElementById('grid');
const dash = new DashboardLayout(grid, {
  profile: 'user_demo',
  onSave: (layout) => console.log('Layout saved:', layout)
});
// Delegate click events for controls (button clicks fire after pointerup)
grid.addEventListener('click', e => dash._onClick(e));
// Expose for debugging
window.dash = dash;
</script>
</body>
</html>
```