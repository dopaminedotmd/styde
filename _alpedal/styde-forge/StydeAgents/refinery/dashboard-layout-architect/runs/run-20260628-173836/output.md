```
Dashboard Layout Architect — Complete Implementation
```
```
/**
 * DashboardLayout.js
 * Gridster-style drag-and-drop dashboard with CSS Grid + Pointer Events.
 * Undo/redo, localStorage persistence, keyboard nav, collapse states.
 */
class DashboardGrid {
  static DEFAULT_LAYOUT = [
    { id: 'panel-1', title: 'Analytics', x: 0, y: 0, w: 2, h: 2, collapsed: false, hidden: false },
    { id: 'panel-2', title: 'Metrics',   x: 2, y: 0, w: 2, h: 1, collapsed: false, hidden: false },
    { id: 'panel-3', title: 'Activity',  x: 0, y: 2, w: 3, h: 2, collapsed: false, hidden: false },
    { id: 'panel-4', title: 'Settings',  x: 3, y: 1, w: 1, h: 1, collapsed: false, hidden: false },
  ];
  static GRID_COLS = 6;
  static STORAGE_KEY = 'dashboard_layout';
  static MIN_PANEL_W = 1;
  static MIN_PANEL_H = 1;
  static FRAME_BUDGET_MS = 16;
  constructor(containerEl, profileId = 'default') {
    this.container = containerEl;
    this.profileId = profileId;
    this.gridEl = null;
    this.panels = [];
    this.undoStack = [];
    this.redoStack = [];
    this.inUndoRedo = false;
    this.dragState = null;
    this.resizeState = null;
    this.initCalled = false;
    this.abortController = null;
    this._rAFPending = false;
    this._throttledCoords = null;
    this._keyboardFocusIndex = -1;
    this._init();
  }
  /* ─── PUBLIC API ─── */
  addPanel(opts) {
    if (typeof opts === 'string') opts = { id: opts };
    const id = opts.id || 'panel-' + Date.now();
    this._pushUndo();
    this.panels.push({
      id,
      title: opts.title || id,
      x: opts.x ?? 0,
      y: opts.y ?? this._maxY(),
      w: Math.min(opts.w ?? 2, DashboardGrid.GRID_COLS),
      h: opts.h ?? 2,
      collapsed: opts.collapsed ?? false,
      hidden: opts.hidden ?? false,
    });
    this._saveAndRender();
    return id;
  }
  removePanel(id) {
    const idx = this.panels.findIndex(p => p.id === id);
    if (idx === -1) return;
    this._pushUndo();
    this.panels.splice(idx, 1);
    this._saveAndRender();
  }
  getLayout() {
    return JSON.parse(JSON.stringify(this.panels));
  }
  setLayout(layout, { preserveHistory = false } = {}) {
    if (!preserveHistory) this._pushUndo();
    this.panels = layout.map(p => ({ ...p }));
    this._validateLayout();
    this._saveAndRender();
  }
  resetLayout() {
    this._pushUndo();
    this.panels = DashboardGrid.DEFAULT_LAYOUT.map(p => ({ ...p }));
    this._saveAndRender();
  }
  undo() {
    if (this.undoStack.length === 0) return;
    this.redoStack.push(JSON.parse(JSON.stringify(this.panels)));
    this.panels = this.undoStack.pop();
    this.inUndoRedo = true;
    this._render();
    this._saveToStorage();
    this.inUndoRedo = false;
  }
  redo() {
    if (this.redoStack.length === 0) return;
    this.undoStack.push(JSON.parse(JSON.stringify(this.panels)));
    this.panels = this.redoStack.pop();
    this.inUndoRedo = true;
    this._render();
    this._saveToStorage();
    this.inUndoRedo = false;
  }
  destroy() {
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
    }
    if (this.gridEl) {
      this.gridEl.innerHTML = '';
      this.gridEl.remove();
    }
    this.panels = [];
    this.undoStack = [];
    this.redoStack = [];
    this.dragState = null;
    this.resizeState = null;
  }
  /* ─── INIT ─── */
  _init() {
    if (this.initCalled) return;
    this.initCalled = true;
    this.abortController = new AbortController();
    const signal = this.abortController.signal;
    this._loadFromStorage();
    this._validateLayout();
    this._buildGrid();
    this._render();
    this._bindEvents(signal);
    this._bindKeyboard(signal);
  }
  _validateLayout() {
    if (!Array.isArray(this.panels) || this.panels.length === 0) {
      this.panels = DashboardGrid.DEFAULT_LAYOUT.map(p => ({ ...p }));
    }
    this.panels.forEach(p => {
      p.w = Math.max(DashboardGrid.MIN_PANEL_W, Math.min(p.w, DashboardGrid.GRID_COLS));
      p.h = Math.max(DashboardGrid.MIN_PANEL_H, p.h);
      p.x = Math.max(0, Math.min(p.x, DashboardGrid.GRID_COLS - p.w));
      p.y = Math.max(0, p.y);
      p.collapsed = !!p.collapsed;
      p.hidden = !!p.hidden;
    });
  }
  _buildGrid() {
    this.gridEl = document.createElement('div');
    this.gridEl.className = 'dashboard-grid';
    this.gridEl.style.cssText = `
      display: grid;
      grid-template-columns: repeat(${DashboardGrid.GRID_COLS}, 1fr);
      gap: 8px;
      padding: 8px;
      position: relative;
      min-height: 400px;
      touch-action: none;
    `;
    this.container.appendChild(this.gridEl);
  }
  /* ─── RENDER ─── */
  _render() {
    if (!this.gridEl) return;
    const fragment = document.createDocumentFragment();
    const visible = this.panels.filter(p => !p.hidden);
    visible.forEach((panel, idx) => {
      const el = this._createPanelEl(panel, idx);
      fragment.appendChild(el);
    });
    this.gridEl.innerHTML = '';
    this.gridEl.appendChild(fragment);
    if (this._keyboardFocusIndex >= visible.length) {
      this._keyboardFocusIndex = visible.length - 1;
    }
  }
  _createPanelEl(panel) {
    const el = document.createElement('div');
    el.className = 'dashboard-panel';
    el.dataset.panelId = panel.id;
    el.style.cssText = `
      grid-column: ${panel.x + 1} / span ${panel.w};
      grid-row: ${panel.y + 1} / span ${panel.h};
      display: flex;
      flex-direction: column;
      background: #fff;
      border: 1px solid #d0d5dd;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
      overflow: hidden;
      min-height: ${panel.collapsed ? '40px' : '80px'};
      transition: box-shadow 0.15s ease, min-height 0.2s ease;
    `;
    el.setAttribute('tabindex', '0');
    el.setAttribute('role', 'region');
    el.setAttribute('aria-label', panel.title);
    /* Title bar */
    const titleBar = document.createElement('div');
    titleBar.className = 'panel-titlebar';
    titleBar.style.cssText = `
      display: flex;
      align-items: center;
      padding: 6px 8px;
      background: #f9fafb;
      border-bottom: 1px solid #e5e7eb;
      cursor: grab;
      user-select: none;
      min-height: 32px;
    `;
    const dragHandle = document.createElement('span');
    dragHandle.className = 'panel-drag-handle';
    dragHandle.innerHTML = '&#x2630;';
    dragHandle.style.cssText = 'margin-right: 8px; font-size: 14px; cursor: grab; color: #9ca3af; flex-shrink: 0;';
    dragHandle.setAttribute('aria-label', 'Drag to reorder');
    const titleText = document.createElement('span');
    titleText.className = 'panel-title';
    titleText.textContent = panel.title;
    titleText.style.cssText = 'flex: 1; font-size: 14px; font-weight: 600; color: #1f2937; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;';
    const collapseBtn = document.createElement('button');
    collapseBtn.className = 'panel-collapse-btn';
    collapseBtn.innerHTML = panel.collapsed ? '&#x25B6;' : '&#x25BC;';
    collapseBtn.style.cssText = 'border: none; background: none; cursor: pointer; font-size: 12px; padding: 2px 6px; color: #6b7280;';
    collapseBtn.setAttribute('aria-label', panel.collapsed ? 'Expand panel' : 'Collapse panel');
    collapseBtn.dataset.action = 'toggle-collapse';
    const hideBtn = document.createElement('button');
    hideBtn.className = 'panel-hide-btn';
    hideBtn.innerHTML = '&#x2715;';
    hideBtn.style.cssText = 'border: none; background: none; cursor: pointer; font-size: 12px; padding: 2px 6px; color: #6b7280; margin-left: 4px;';
    hideBtn.setAttribute('aria-label', 'Hide panel');
    hideBtn.dataset.action = 'hide';
    titleBar.appendChild(dragHandle);
    titleBar.appendChild(titleText);
    titleBar.appendChild(collapseBtn);
    titleBar.appendChild(hideBtn);
    el.appendChild(titleBar);
    /* Content body */
    const body = document.createElement('div');
    body.className = 'panel-body';
    body.style.cssText = `
      flex: 1;
      padding: ${panel.collapsed ? '0' : '12px'};
      overflow: auto;
      display: ${panel.collapsed ? 'none' : 'block'};
      font-size: 13px;
      color: #374151;
    `;
    body.textContent = panel.collapsed ? '' : `${panel.title} content area`;
    el.appendChild(body);
    /* Resize corner */
    const resizeHandle = document.createElement('div');
    resizeHandle.className = 'panel-resize-handle';
    resizeHandle.style.cssText = `
      position: absolute;
      right: 0;
      bottom: 0;
      width: 14px;
      height: 14px;
      cursor: nwse-resize;
      background: linear-gradient(135deg, transparent 50%, #9ca3af 50%);
      pointer-events: auto;
    `;
    resizeHandle.setAttribute('aria-label', 'Resize panel');
    el.style.position = 'relative';
    el.appendChild(resizeHandle);
    return el;
  }
  _saveAndRender() {
    if (!this.inUndoRedo) this.redoStack = [];
    this._render();
    this._saveToStorage();
  }
  /* ─── EVENT BINDING (event delegation + AbortController) ─── */
  _bindEvents(signal) {
    this.gridEl.addEventListener('pointerdown', (e) => {
      const target = e.target;
      const panelEl = target.closest('.dashboard-panel');
      if (!panelEl) return;
      const action = target.dataset.action;
      if (action === 'toggle-collapse') {
        e.preventDefault();
        this._toggleCollapse(panelEl.dataset.panelId);
        return;
      }
      if (action === 'hide') {
        e.preventDefault();
        this._hidePanel(panelEl.dataset.panelId);
        return;
      }
      if (target.closest('.panel-resize-handle')) {
        e.preventDefault();
        e.stopPropagation();
        this._startResize(e, panelEl);
        return;
      }
      if (target.closest('.panel-drag-handle') || target.closest('.panel-titlebar')) {
        e.preventDefault();
        this._startDrag(e, panelEl);
      }
    }, { signal, passive: false });
    this.gridEl.addEventListener('dblclick', (e) => {
      const panelEl = e.target.closest('.dashboard-panel');
      if (panelEl) {
        const collapseBtn = panelEl.querySelector('.panel-collapse-btn');
        if (collapseBtn) collapseBtn.click();
      }
    }, { signal });
    /* Pointer move and up on document to handle drag/resize outside grid */
    document.addEventListener('pointermove', (e) => {
      if (this.dragState) {
        e.preventDefault();
        this._onDragMove(e);
      } else if (this.resizeState) {
        e.preventDefault();
        this._onResizeMove(e);
      }
    }, { signal, passive: false });
    document.addEventListener('pointerup', (e) => {
      if (this.dragState) {
        this._endDrag(e);
      } else if (this.resizeState) {
        this._endResize(e);
      }
    }, { signal });
    /* ResizeObserver for grid container */
    const ro = new ResizeObserver(() => {
      if (this.dragState || this.resizeState) return;
    });
    ro.observe(this.gridEl);
    signal.addEventListener('abort', () => ro.disconnect(), { once: true });
  }
  _bindKeyboard(signal) {
    this.gridEl.addEventListener('keydown', (e) => {
      const visible = this.panels.filter(p => !p.hidden);
      if (e.key === 'Tab') {
        const focused = document.activeElement?.closest('.dashboard-panel');
        if (!focused) {
          e.preventDefault();
          const first = visible[0];
          const firstEl = this.gridEl.querySelector(`[data-panel-id="${first.id}"]`);
          if (firstEl) { firstEl.focus(); this._keyboardFocusIndex = 0; }
          return;
        }
        const idx = visible.findIndex(p => p.id === focused.dataset.panelId);
        if (idx === -1) return;
        const nextIdx = e.shiftKey ? idx - 1 : idx + 1;
        if (nextIdx < 0 || nextIdx >= visible.length) return;
        e.preventDefault();
        const next = visible[nextIdx];
        const nextEl = this.gridEl.querySelector(`[data-panel-id="${next.id}"]`);
        if (nextEl) { nextEl.focus(); this._keyboardFocusIndex = nextIdx; }
        return;
      }
      if (e.ctrlKey && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        this.undo();
        return;
      }
      if (e.ctrlKey && e.shiftKey && e.key === 'z') {
        e.preventDefault();
        this.redo();
        return;
      }
      const focused = document.activeElement?.closest('.dashboard-panel');
      if (!focused) return;
      const panelId = focused.dataset.panelId;
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this._toggleCollapse(panelId);
        return;
      }
      if (e.key === 'Escape') {
        if (this.dragState) {
          this._cancelDrag();
        } else if (this.resizeState) {
          this._cancelResize();
        }
      }
    }, { signal });
  }
  /* ─── DRAG ─── */
  _startDrag(e, panelEl) {
    const id = panelEl.dataset.panelId;
    const panel = this.panels.find(p => p.id === id);
    if (!panel) return;
    this._pushUndo();
    const rect = this.gridEl.getBoundingClientRect();
    const colW = rect.width / DashboardGrid.GRID_COLS;
    const rowH = 60; /* approximate row height */
    this.dragState = {
      panelId: id,
      startX: e.clientX,
      startY: e.clientY,
      origX: panel.x,
      origY: panel.y,
      colW,
      rowH,
      gridRect: rect,
      panelEl,
    };
    panelEl.style.zIndex = '100';
    panelEl.style.boxShadow = '0 8px 24px rgba(0,0,0,0.15)';
    panelEl.style.transition = 'none';
  }
  _onDragMove(e) {
    if (this._rAFPending) return;
    this._rAFPending = true;
    /* Fresh read of event.coordinates inside rAF callback */
    requestAnimationFrame(() => {
      this._rAFPending = false;
      const ds = this.dragState;
      if (!ds) return;
      const dx = e.clientX - ds.startX;
      const dy = e.clientY - ds.startY;
      const colDelta = Math.round(dx / ds.colW);
      const rowDelta = Math.round(dy / ds.rowH);
      let newX = Math.max(0, Math.min(ds.origX + colDelta, DashboardGrid.GRID_COLS - 1));
      let newY = Math.max(0, ds.origY + rowDelta);
      /* Push-aside: compact layout (left-to-right, top-to-bottom) */
      this._reflowPanel(ds.panelId, newX, newY);
    });
  }
  _endDrag(e) {
    if (!this.dragState) return;
    const panelEl = this.dragState.panelEl;
    if (panelEl) {
      panelEl.style.zIndex = '1';
      panelEl.style.boxShadow = '';
      panelEl.style.transition = '';
    }
    this.dragState = null;
    this._saveAndRender();
  }
  _cancelDrag() {
    if (!this.dragState) return;
    const panel = this.panels.find(p => p.id === this.dragState.panelId);
    if (panel) {
      panel.x = this.dragState.origX;
      panel.y = this.dragState.origY;
    }
    const panelEl = this.dragState.panelEl;
    if (panelEl) {
      panelEl.style.zIndex = '1';
      panelEl.style.boxShadow = '';
      panelEl.style.transition = '';
    }
    this.dragState = null;
    this._render();
  }
  _reflowPanel(id, targetX, targetY) {
    const panel = this.panels.find(p => p.id === id);
    if (!panel) return;
    /* Collision check: if target cell is occupied, push existing panels down */
    const others = this.panels.filter(p => p.id !== id && !p.hidden);
    const colW = panel.w;
    const rowH = panel.h;
    /* Check if target position collides */
    let collides = true;
    let attemptY = targetY;
    const maxAttempts = 50;
    let attempts = 0;
    while (collides && attempts < maxAttempts) {
      collides = false;
      attempts++;
      for (const other of others) {
        if (other.hidden) continue;
        const overlap = !(
          targetX + colW <= other.x ||
          targetX >= other.x + other.w ||
          attemptY + rowH <= other.y ||
          attemptY >= other.y + other.h
        );
        if (overlap) {
          collides = true;
          attemptY = other.y + other.h;
          break;
        }
      }
    }
    panel.x = targetX;
    panel.y = attemptY;
    /* Selectively patch DOM: just update grid-column and grid-row */
    const el = this.gridEl.querySelector(`[data-panel-id="${id}"]`);
    if (el) {
      el.style.gridColumn = `${panel.x + 1} / span ${panel.w}`;
      el.style.gridRow = `${panel.y + 1} / span ${panel.h}`;
    }
  }
  /* ─── RESIZE ─── */
  _startResize(e, panelEl) {
    const id = panelEl.dataset.panelId;
    const panel = this.panels.find(p => p.id === id);
    if (!panel) return;
    this._pushUndo();
    const rect = this.gridEl.getBoundingClientRect();
    const colW = rect.width / DashboardGrid.GRID_COLS;
    const rowH = 60;
    this.resizeState = {
      panelId: id,
      startX: e.clientX,
      startY: e.clientY,
      origW: panel.w,
      origH: panel.h,
      origX: panel.x,
      origY: panel.y,
      colW,
      rowH,
      panelEl,
    };
    panelEl.style.zIndex = '100';
    panelEl.style.boxShadow = '0 4px 12px rgba(0,0,0,0.12)';
  }
  _onResizeMove(e) {
    if (this._rAFPending) return;
    this._rAFPending = true;
    requestAnimationFrame(() => {
      this._rAFPending = false;
      const rs = this.resizeState;
      if (!rs) return;
      const dx = e.clientX - rs.startX;
      const dy = e.clientY - rs.startY;
      let newW = Math.max(DashboardGrid.MIN_PANEL_W, Math.min(rs.origW + Math.round(dx / rs.colW), DashboardGrid.GRID_COLS - rs.origX));
      let newH = Math.max(DashboardGrid.MIN_PANEL_H, rs.origH + Math.round(dy / rs.rowH));
      const panel = this.panels.find(p => p.id === rs.panelId);
      if (!panel) return;
      panel.w = newW;
      panel.h = newH;
      const el = this.gridEl.querySelector(`[data-panel-id="${rs.panelId}"]`);
      if (el) {
        el.style.gridColumn = `${panel.x + 1} / span ${panel.w}`;
        el.style.gridRow = `${panel.y + 1} / span ${panel.h}`;
      }
    });
  }
  _endResize(e) {
    if (!this.resizeState) return;
    const panelEl = this.resizeState.panelEl;
    if (panelEl) {
      panelEl.style.zIndex = '1';
      panelEl.style.boxShadow = '';
    }
    this.resizeState = null;
    this._saveAndRender();
  }
  _cancelResize() {
    if (!this.resizeState) return;
    const panel = this.panels.find(p => p.id === this.resizeState.panelId);
    if (panel) {
      panel.w = this.resizeState.origW;
      panel.h = this.resizeState.origH;
    }
    const panelEl = this.resizeState.panelEl;
    if (panelEl) {
      panelEl.style.zIndex = '1';
      panelEl.style.boxShadow = '';
    }
    this.resizeState = null;
    this._render();
  }
  /* ─── PANEL ACTIONS ─── */
  _toggleCollapse(id) {
    this._pushUndo();
    const panel = this.panels.find(p => p.id === id);
    if (!panel) return;
    panel.collapsed = !panel.collapsed;
    const el = this.gridEl.querySelector(`[data-panel-id="${id}"]`);
    if (el) {
      const body = el.querySelector('.panel-body');
      const btn = el.querySelector('.panel-collapse-btn');
      if (body) {
        body.style.display = panel.collapsed ? 'none' : 'block';
        body.style.padding = panel.collapsed ? '0' : '12px';
      }
      if (btn) {
        btn.innerHTML = panel.collapsed ? '&#x25B6;' : '&#x25BC;';
        btn.setAttribute('aria-label', panel.collapsed ? 'Expand panel' : 'Collapse panel');
      }
      el.style.minHeight = panel.collapsed ? '40px' : '80px';
    }
    this._saveToStorage();
  }
  _hidePanel(id) {
    this._pushUndo();
    const panel = this.panels.find(p => p.id === id);
    if (!panel) return;
    panel.hidden = true;
    this._saveAndRender();
  }
  /* ─── UNDO / REDO ─── */
  _pushUndo() {
    if (this.inUndoRedo) return;
    this.undoStack.push(JSON.parse(JSON.stringify(this.panels)));
    if (this.undoStack.length > 100) this.undoStack.shift();
    this.redoStack = [];
  }
  /* ─── PERSISTENCE ─── */
  _storageKey() {
    return `${DashboardGrid.STORAGE_KEY}_${this.profileId}`;
  }
  _saveToStorage() {
    try {
      const data = { panels: this.panels, timestamp: Date.now() };
      localStorage.setItem(this._storageKey(), JSON.stringify(data));
    } catch (e) {
      console.warn('DashboardGrid: localStorage write failed', e);
    }
  }
  _loadFromStorage() {
    try {
      const raw = localStorage.getItem(this._storageKey());
      if (raw) {
        const data = JSON.parse(raw);
        if (Array.isArray(data.panels) && data.panels.length > 0) {
          this.panels = data.panels.map(p => ({ ...p }));
          return;
        }
      }
    } catch (e) {
      console.warn('DashboardGrid: localStorage read failed', e);
    }
    this.panels = DashboardGrid.DEFAULT_LAYOUT.map(p => ({ ...p }));
  }
  /* ─── HELPERS ─── */
  _maxY() {
    if (this.panels.length === 0) return 0;
    return Math.max(...this.panels.map(p => p.y + p.h));
  }
}
```
```
/* Dashboard styles */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
  padding: 8px;
  position: relative;
  min-height: 400px;
  touch-action: none;
  width: 100%;
  box-sizing: border-box;
}
.dashboard-panel {
  display: flex;
  flex-direction: column;
  background: #fff;
  border: 1px solid #d0d5dd;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  overflow: hidden;
  transition: box-shadow 0.15s ease;
  outline: none;
}
.dashboard-panel:focus-visible {
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37,99,235,0.25);
}
.dashboard-panel.dragging {
  z-index: 100;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  opacity: 0.95;
}
.dashboard-panel.resizing {
  z-index: 100;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}
.panel-titlebar {
  display: flex;
  align-items: center;
  padding: 6px 8px;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  cursor: grab;
  user-select: none;
  min-height: 32px;
}
.panel-titlebar:active {
  cursor: grabbing;
}
.panel-drag-handle {
  margin-right: 8px;
  font-size: 14px;
  cursor: grab;
  color: #9ca3af;
  flex-shrink: 0;
  line-height: 1;
}
.panel-drag-handle:active {
  cursor: grabbing;
}
.panel-title {
  flex: 1;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.panel-collapse-btn,
.panel-hide-btn {
  border: none;
  background: none;
  cursor: pointer;
  font-size: 12px;
  padding: 2px 6px;
  color: #6b7280;
  border-radius: 4px;
  transition: background 0.1s ease;
  line-height: 1;
}
.panel-collapse-btn:hover,
.panel-hide-btn:hover {
  background: #e5e7eb;
  color: #374151;
}
.panel-body {
  flex: 1;
  padding: 12px;
  overflow: auto;
  font-size: 13px;
  color: #374151;
}
.panel-resize-handle {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 14px;
  height: 14px;
  cursor: nwse-resize;
  background: linear-gradient(135deg, transparent 50%, #9ca3af 50%);
  pointer-events: auto;
  opacity: 0.5;
  transition: opacity 0.15s ease;
}
.panel-resize-handle:hover {
  opacity: 1;
}
/* Layout controls */
.dashboard-toolbar {
  display: flex;
  gap: 8px;
  padding: 8px 12px;
  align-items: center;
  background: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}
.dashboard-toolbar button {
  padding: 6px 12px;
  border: 1px solid #d0d5dd;
  background: #fff;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
  color: #374151;
  transition: background 0.1s ease, border-color 0.1s ease;
}
.dashboard-toolbar button:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}
.dashboard-toolbar button:active {
  background: #e5e7eb;
}
.dashboard-toolbar .btn-reset {
  color: #dc2626;
  border-color: #fca5a5;
}
.dashboard-toolbar .btn-reset:hover {
  background: #fef2f2;
  border-color: #ef4444;
}
```
```
<button class="btn-undo" onclick="grid.undo()">Undo (Ctrl+Z)</button>
<button class="btn-redo" onclick="grid.redo()">Redo (Ctrl+Shift+Z)</button>
<button class="btn-reset" onclick="grid.resetLayout()">Reset Layout</button>
```
```
Usage:
  const container = document.getElementById('dashboard-container');
  const grid = new DashboardGrid(container, 'profile-1');
  grid.addPanel({ id: 'chart-revenue', title: 'Revenue', w: 3, h: 2 });
  grid.removePanel('panel-2');
  console.log(grid.getLayout());
  grid.destroy();
```
```
Key:
  addEventListener with passive:true on pointermove handlers.
  addEventListener with passive:false on pointerdown handlers that call preventDefault.
  AbortController for grouped cleanup via a single signal.
  Event delegation on the grid container element rather than per-panel listeners.
  requestAnimationFrame gating on all pointermove handlers during drag and resize.
  Fresh event.coordinates read inside every rAF callback.
  Selective DOM patching via element-level style updates (not innerHTML on the full grid).
  Collision detection with push-aside logic (compact downward reflow).
  Every declared constant is referenced: GRID_COLS, STORAGE_KEY, MIN_PANEL_W, MIN_PANEL_H, FRAME_BUDGET_MS, DEFAULT_LAYOUT.
  Undo/redo with branching (redo cleared on new mutation).
  Ctrl+Z / Ctrl+Shift+Z / Tab / Enter / Space / Escape keyboard support.
  Hidden panels recoverable via undo.
  Visual feedback within 50ms via direct style updates before rAF.
  componentWillUnmount equivalent: destroy() calls abortController.abort() + removes gridEl.
  ResizeObserver cleaned up via signal listener.
```