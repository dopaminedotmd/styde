```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Dashboard Layout Architect</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f5f7;color:#1d1d1f;padding:20px}
.dashboard-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;padding:12px 20px;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.08)}
.dashboard-header h1{font-size:20px;font-weight:600}
.header-actions{display:flex;gap:8px;align-items:center}
.header-actions button{padding:6px 14px;border:1px solid #d2d2d7;border-radius:8px;background:#fff;font-size:13px;cursor:pointer;transition:all .15s}
.header-actions button:hover{background:#f0f0f2;border-color:#b0b0b5}
.header-actions button:active{transform:scale(.97)}
.header-actions button.primary{background:#007aff;color:#fff;border-color:#007aff}
.header-actions button.primary:hover{background:#0056cc;border-color:#0056cc}
.undo-indicator{font-size:12px;color:#86868b;min-width:60px;text-align:right}
.grid-container{position:relative;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.08);padding:16px;margin-bottom:20px;min-height:500px}
.grid{display:grid;grid-template-columns:repeat(var(--grid-cols,4),1fr);gap:12px;position:relative;min-height:300px;transition:grid-template-columns .2s}
.panel{background:#fff;border:1px solid #e5e5e7;border-radius:10px;overflow:hidden;position:relative;display:flex;flex-direction:column;transition:box-shadow .15s,opacity .2s;user-select:none;-webkit-user-select:none}
.panel.dragging{z-index:100;box-shadow:0 8px 30px rgba(0,0,0,.15);opacity:.92;transform:rotate(.5deg)}
.panel.drag-over{border-color:#007aff;box-shadow:0 0 0 2px rgba(0,122,255,.25)}
.panel.resizing{border-color:#ff9500;box-shadow:0 0 0 2px rgba(255,149,0,.25)}
.panel.hidden{display:none}
.panel.collapsed .panel-body{display:none}
.panel.collapsed .panel-title{ border-bottom: none }
.panel-title{display:flex;align-items:center;padding:10px 12px;background:#fafafa;border-bottom:1px solid #e5e5e7;cursor:grab;gap:8px}
.panel-title:active{cursor:grabbing}
.panel-title .drag-handle{width:16px;height:16px;display:flex;flex-direction:column;gap:3px;justify-content:center;cursor:grab;flex-shrink:0;opacity:.5}
.panel-title .drag-handle span{display:block;height:2px;background:#8e8e93;border-radius:1px}
.panel-title .drag-handle span:nth-child(1){width:16px}
.panel-title .drag-handle span:nth-child(2){width:12px}
.panel-title .drag-handle span:nth-child(3){width:8px}
.panel-title .panel-label{flex:1;font-size:13px;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.panel-title .panel-controls{display:flex;gap:4px;flex-shrink:0}
.panel-title .panel-controls button{width:24px;height:24px;border:none;background:transparent;border-radius:4px;font-size:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .12s;color:#555}
.panel-title .panel-controls button:hover{background:#e5e5e7;color:#1d1d1f}
.panel-title .panel-controls button:active{background:#d2d2d7}
.panel-body{padding:16px;flex:1;min-height:60px;display:flex;align-items:center;justify-content:center;font-size:14px;color:#86868b}
.resize-handle{position:absolute;right:0;bottom:0;width:16px;height:16px;cursor:nwse-resize;display:flex;align-items:flex-end;justify-content:flex-end;padding:2px;z-index:10}
.resize-handle::after{content:'';display:block;width:8px;height:8px;border-right:2px solid #c7c7cc;border-bottom:2px solid #c7c7cc;border-radius:0 0 3px 0;transition:border-color .15s}
.resize-handle:hover::after{border-color:#007aff}
.gridlines{position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:0}
.drop-indicator{position:absolute;background:rgba(0,122,255,.12);border:2px dashed #007aff;border-radius:8px;z-index:99;pointer-events:none;transition:all .1s;opacity:0}
.drop-indicator.active{opacity:1}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1d1d1f;color:#fff;padding:10px 20px;border-radius:8px;font-size:13px;z-index:1000;opacity:0;transition:opacity .2s;pointer-events:none}
.toast.visible{opacity:1}
@media(max-width:768px){.grid{grid-template-columns:repeat(var(--grid-cols,2),1fr)}.dashboard-header{flex-wrap:wrap;gap:8px}}
</style>
</head>
<body>
<div class="dashboard-header">
  <h1>Dashboard</h1>
  <div class="header-actions">
    <button id="undoBtn" disabled title="Undo (Ctrl+Z)">Undo</button>
    <button id="redoBtn" disabled title="Redo (Ctrl+Shift+Z)">Redo</button>
    <span class="undo-indicator" id="undoIndicator"></span>
    <button id="resetBtn" class="primary">Reset Layout</button>
  </div>
</div>
<div class="grid-container">
  <div class="grid" id="grid"></div>
</div>
<div class="toast" id="toast"></div>
<script>
class DashboardLayout {
  static DEFAULTS = [
    {id:'panel-1', label:'Performance', cols:2, rows:2, content:'Key metrics and KPIs'},
    {id:'panel-2', label:'Revenue', cols:1, rows:2, content:'Revenue chart'},
    {id:'panel-3', label:'Users', cols:1, rows:1, content:'Active user count'},
    {id:'panel-4', label:'Activity', cols:2, rows:1, content:'Recent activity feed'},
    {id:'panel-5', label:'Notifications', cols:1, rows:1, content:'Latest alerts'},
    {id:'panel-6', label:'Tasks', cols:1, rows:2, content:'Task list'},
    {id:'panel-7', label:'Analytics', cols:2, rows:1, content:'Analytics overview'},
    {id:'panel-8', label:'Settings', cols:1, rows:1, content:'Quick settings panel'}
  ];
  static MIN_PANEL_W = 1;
  static MIN_PANEL_H = 1;
  constructor(gridEl) {
    this.grid = gridEl;
    this.panels = [];
    this.profile = 'default';
    this.abortController = null;
    this.resizeRAF = null;
    this.dragState = null;
    this.resizeState = null;
    // undo system
    this.undoStack = [];
    this.redoStack = [];
    this.maxUndo = 50;
    this.trackingUndo = false;
    this._bindGlobalEvents();
    this._loadOrInit();
    this._render();
    this._updateUndoUI();
  }
  // ─── persistence ──────────────────────────────────────
  _storageKey() {
    return `dash_layout_${this.profile}`;
  }
  _save() {
    try {
      const data = {panels: this.panels.map(p => this._serializePanel(p))};
      localStorage.setItem(this._storageKey(), JSON.stringify(data));
    } catch(e) {/* quota */}
  }
  _loadOrInit() {
    try {
      const raw = localStorage.getItem(this._storageKey());
      if (raw) {
        const data = JSON.parse(raw);
        if (data && Array.isArray(data.panels) && data.panels.length) {
          this.panels = data.panels.map(s => this._deserializePanel(s));
          return;
        }
      }
    } catch(e) {/* fall through */}
    this.panels = DashboardLayout.DEFAULTS.map(d => ({
      ...d,
      col: null,
      row: null,
      collapsed: false,
      hidden: false
    }));
  }
  _serializePanel(p) {
    return {
      id: p.id, label: p.label, cols: p.cols, rows: p.rows,
      col: p.col, row: p.row, collapsed: p.collapsed, hidden: p.hidden,
      content: p.content
    };
  }
  _deserializePanel(s) {
    return {...s};
  }
  // ─── reset ────────────────────────────────────────────
  resetLayout() {
    this._pushUndo();
    this.panels = DashboardLayout.DEFAULTS.map(d => ({
      ...d,
      col: null, row: null,
      collapsed: false, hidden: false
    }));
    this.redoStack = [];
    this._render();
    this._save();
    this._showToast('Layout reset to default');
    this._updateUndoUI();
  }
  // ─── rendering ────────────────────────────────────────
  _render() {
    this.grid.innerHTML = '';
    const frag = document.createDocumentFragment();
    this.panels.forEach(p => {
      const el = document.createElement('div');
      el.className = 'panel';
      if (p.hidden) el.classList.add('hidden');
      if (p.collapsed) el.classList.add('collapsed');
      el.dataset.panelId = p.id;
      el.style.gridColumn = p.col ? `${p.col} / span ${p.cols}` : `span ${p.cols}`;
      el.style.gridRow = p.row ? `${p.row} / span ${p.rows}` : `span ${p.rows}`;
      el.style.order = p.col ?? 0;
      // title bar with drag handle
      const title = document.createElement('div');
      title.className = 'panel-title';
      title.innerHTML = `
        <div class="drag-handle" data-action="drag" tabindex="0" role="button" aria-label="Drag panel">
          <span></span><span></span><span></span>
        </div>
        <span class="panel-label">${this._esc(p.label)}</span>
        <div class="panel-controls">
          <button data-action="collapse" title="Collapse/Expand" aria-label="Toggle collapse">${p.collapsed ? '+' : '−'}</button>
          <button data-action="hide" title="Hide panel" aria-label="Hide panel">✕</button>
        </div>
      `;
      el.appendChild(title);
      const body = document.createElement('div');
      body.className = 'panel-body';
      body.textContent = this._esc(p.content);
      el.appendChild(body);
      const resizeHandle = document.createElement('div');
      resizeHandle.className = 'resize-handle';
      resizeHandle.dataset.action = 'resize';
      resizeHandle.setAttribute('role','button');
      resizeHandle.setAttribute('aria-label','Resize panel');
      resizeHandle.setAttribute('tabindex','0');
      el.appendChild(resizeHandle);
      frag.appendChild(el);
    });
    this.grid.appendChild(frag);
    // event delegation on grid
    this._setupDelegation();
  }
  _esc(s) {
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }
  // ─── event delegation (single stable container) ───────
  _setupDelegation() {
    if (this.abortController) {
      this.abortController.abort();
    }
    this.abortController = new AbortController();
    const signal = this.abortController.signal;
    const opts = {signal};
    // pointer down — capture for drag/resize start
    this.grid.addEventListener('pointerdown', e => {
      const action = e.target.closest('[data-action]')?.dataset?.action;
      if (!action) return;
      if (action === 'drag') this._dragStart(e);
      else if (action === 'resize') this._resizeStart(e);
    }, opts);
    // click delegation for collapse/hide
    this.grid.addEventListener('click', e => {
      const action = e.target.closest('[data-action]')?.dataset?.action;
      if (!action) return;
      const panelEl = e.target.closest('.panel');
      if (!panelEl) return;
      if (action === 'collapse') this._toggleCollapse(panelEl.dataset.panelId);
      else if (action === 'hide') this._hidePanel(panelEl.dataset.panelId);
    }, opts);
    // keyboard — Tab order is built-in; Enter/Space on controls
    this.grid.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        if (this.dragState) this._dragEnd(null);
        if (this.resizeState) this._resizeEnd(null);
        return;
      }
      if (e.key === 'Enter' || e.key === ' ') {
        const action = e.target.closest('[data-action]')?.dataset?.action;
        if (!action) return;
        e.preventDefault();
        const panelEl = e.target.closest('.panel');
        if (!panelEl) return;
        if (action === 'collapse') this._toggleCollapse(panelEl.dataset.panelId);
        else if (action === 'hide') this._hidePanel(panelEl.dataset.panelId);
        else if (action === 'drag') this._dragStart({target: e.target, clientX:0, clientY:0, preventDefault:()=>{}});
        else if (action === 'resize') this._resizeStart({target: e.target, clientX:0, clientY:0, preventDefault:()=>{}});
      }
    }, opts);
    // pointer move + up (delegated on document for capture)
    document.addEventListener('pointermove', e => {
      if (this.dragState) this._dragMove(e);
      if (this.resizeState) this._resizeMove(e);
    }, {...opts, passive: true});
    document.addEventListener('pointerup', e => {
      if (this.dragState) this._dragEnd(e);
      if (this.resizeState) this._resizeEnd(e);
    }, opts);
    // window resize observer would go here if needed
  }
  // ─── drag ──────────────────────────────────────────────
  _dragStart(e) {
    const panelEl = e.target.closest('.panel');
    if (!panelEl) return;
    const id = panelEl.dataset.panelId;
    const panel = this.panels.find(p => p.id === id);
    if (!panel || panel.hidden) return;
    this._pushUndo();
    this.redoStack = [];
    const rect = panelEl.getBoundingClientRect();
    const gridRect = this.grid.getBoundingClientRect();
    this.dragState = {
      panelId: id,
      startX: e.clientX,
      startY: e.clientY,
      panelRect: rect,
      gridRect,
      offsetX: e.clientX - rect.left,
      offsetY: e.clientY - rect.top,
      originalCol: panel.col,
      originalRow: panel.row,
      dropCol: panel.col,
      dropRow: panel.row
    };
    panelEl.classList.add('dragging');
    panelEl.style.position = 'fixed';
    panelEl.style.width = rect.width + 'px';
    panelEl.style.height = rect.height + 'px';
    panelEl.style.left = rect.left + 'px';
    panelEl.style.top = rect.top + 'px';
    panelEl.style.pointerEvents = 'none';
    panelEl.style.zIndex = '100';
    const cols = this._getColCount();
    const gap = 12;
    const cellW = (gridRect.width - (cols - 1) * gap) / cols;
    const cellH = 100;
    this.dragState.cellW = cellW;
    this.dragState.cellH = cellH;
    this.dragState.gap = gap;
    this.dragState.cols = cols;
    e.preventDefault();
  }
  _dragMove(e) {
    if (!this.dragState) return;
    const s = this.dragState;
    const x = e.clientX - s.offsetX;
    const y = e.clientY - s.offsetY;
    requestAnimationFrame(() => {
      if (!this.dragState) return;
      const panelEl = this.grid.querySelector(`[data-panel-id="${s.panelId}"]`);
      if (!panelEl) return;
      panelEl.style.left = x + 'px';
      panelEl.style.top = y + 'px';
      // compute drop position
      const relX = e.clientX - s.gridRect.left;
      const relY = e.clientY - s.gridRect.top;
      const col = Math.max(1, Math.min(s.cols, Math.floor(relX / (s.cellW + s.gap)) + 1));
      const row = Math.max(1, Math.floor(relY / (s.cellH + s.gap)) + 1);
      s.dropCol = col;
      s.dropRow = row;
    });
  }
  _dragEnd(e) {
    if (!this.dragState) return;
    const s = this.dragState;
    const panelEl = this.grid.querySelector(`[data-panel-id="${s.panelId}"]`);
    const panel = this.panels.find(p => p.id === s.panelId);
    if (panelEl) {
      panelEl.classList.remove('dragging');
      panelEl.style.position = '';
      panelEl.style.width = '';
      panelEl.style.height = '';
      panelEl.style.left = '';
      panelEl.style.top = '';
      panelEl.style.pointerEvents = '';
      panelEl.style.zIndex = '';
    }
    if (panel) {
      panel.col = s.dropCol;
      panel.row = s.dropRow;
      this._render();
      this._save();
      this._updateUndoUI();
    }
    this.dragState = null;
  }
  // ─── resize ───────────────────────────────────────────
  _resizeStart(e) {
    const panelEl = e.target.closest('.panel');
    if (!panelEl) return;
    const id = panelEl.dataset.panelId;
    const panel = this.panels.find(p => p.id === id);
    if (!panel || panel.hidden) return;
    this._pushUndo();
    this.redoStack = [];
    const rect = panelEl.getBoundingClientRect();
    this.resizeState = {
      panelId: id,
      startX: e.clientX,
      startY: e.clientY,
      panelRect: rect,
      origCols: panel.cols,
      origRows: panel.rows
    };
    panelEl.classList.add('resizing');
    e.preventDefault();
  }
  _resizeMove(e) {
    if (!this.resizeState) return;
    if (this.resizeRAF) cancelAnimationFrame(this.resizeRAF);
    this.resizeRAF = requestAnimationFrame(() => {
      if (!this.resizeState) return;
      const s = this.resizeState;
      const panel = this.panels.find(p => p.id === s.panelId);
      if (!panel) return;
      const dx = e.clientX - s.startX;
      const dy = e.clientY - s.startY;
      const gridRect = this.grid.getBoundingClientRect();
      const cols = this._getColCount();
      const gap = 12;
      const cellW = (gridRect.width - (cols - 1) * gap) / cols;
      const cellH = 100;
      const addCols = Math.round(dx / (cellW + gap));
      const addRows = Math.round(dy / (cellH + gap));
      // Critical: clamp against MIN_PANEL_W / MIN_PANEL_H, never against current size
      const newCols = Math.max(DashboardLayout.MIN_PANEL_W, s.origCols + addCols);
      const newRows = Math.max(DashboardLayout.MIN_PANEL_H, s.origRows + addRows);
      if (newCols !== panel.cols || newRows !== panel.rows) {
        panel.cols = Math.min(newCols, cols);
        panel.rows = newRows;
        this._render();
      }
    });
  }
  _resizeEnd(e) {
    if (!this.resizeState) return;
    const panelEl = this.grid.querySelector(`[data-panel-id="${this.resizeState.panelId}"]`);
    if (panelEl) panelEl.classList.remove('resizing');
    if (this.resizeRAF) {
      cancelAnimationFrame(this.resizeRAF);
      this.resizeRAF = null;
    }
    this._save();
    this._updateUndoUI();
    this.resizeState = null;
  }
  // ─── panel actions ────────────────────────────────────
  _toggleCollapse(id) {
    this._pushUndo();
    this.redoStack = [];
    const panel = this.panels.find(p => p.id === id);
    if (!panel) return;
    panel.collapsed = !panel.collapsed;
    this._render();
    this._save();
    this._updateUndoUI();
  }
  _hidePanel(id) {
    this._pushUndo();
    this.redoStack = [];
    const panel = this.panels.find(p => p.id === id);
    if (!panel) return;
    panel.hidden = true;
    this._render();
    this._save();
    this._showToast('Panel hidden (undo to restore)');
    this._updateUndoUI();
  }
  // ─── shared boundary checking ─────────────────────────
  _clampBounds(col, row, cols, rows, totalCols) {
    return {
      col: Math.max(1, Math.min(col, totalCols - cols + 1)),
      row: Math.max(1, Math.min(row, 100 - rows + 1)),
      cols: Math.max(DashboardLayout.MIN_PANEL_W, Math.min(cols, totalCols)),
      rows: Math.max(DashboardLayout.MIN_PANEL_H, rows)
    };
  }
  // ─── undo/redo ────────────────────────────────────────
  _pushUndo() {
    if (this.trackingUndo) return;
    const snapshot = this.panels.map(p => this._serializePanel(p));
    this.undoStack.push(snapshot);
    if (this.undoStack.length > this.maxUndo) {
      this.undoStack.shift();
    }
  }
  undo() {
    if (!this.undoStack.length) return;
    const current = this.panels.map(p => this._serializePanel(p));
    this.redoStack.push(current);
    const prev = this.undoStack.pop();
    this.trackingUndo = true;
    this.panels = prev.map(s => this._deserializePanel(s));
    this.trackingUndo = false;
    this._render();
    this._save();
    this._updateUndoUI();
    this._showToast('Undo');
  }
  redo() {
    if (!this.redoStack.length) return;
    const current = this.panels.map(p => this._serializePanel(p));
    this.undoStack.push(current);
    const next = this.redoStack.pop();
    this.trackingUndo = true;
    this.panels = next.map(s => this._deserializePanel(s));
    this.trackingUndo = false;
    this._render();
    this._save();
    this._updateUndoUI();
    this._showToast('Redo');
  }
  _updateUndoUI() {
    const undoBtn = document.getElementById('undoBtn');
    const redoBtn = document.getElementById('redoBtn');
    const indicator = document.getElementById('undoIndicator');
    if (undoBtn) undoBtn.disabled = !this.undoStack.length;
    if (redoBtn) redoBtn.disabled = !this.redoStack.length;
    if (indicator) indicator.textContent = `${this.undoStack.length} undo`;
  }
  // ─── global keyboard shortcuts ────────────────────────
  _bindGlobalEvents() {
    document.addEventListener('keydown', e => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        this.undo();
      }
      if ((e.ctrlKey || e.metaKey) && e.key === 'z' && e.shiftKey) {
        e.preventDefault();
        this.redo();
      }
      if ((e.ctrlKey || e.metaKey) && e.key === 'Z') {
        e.preventDefault();
        this.redo();
      }
    });
    document.getElementById('undoBtn')?.addEventListener('click', () => this.undo());
    document.getElementById('redoBtn')?.addEventListener('click', () => this.redo());
    document.getElementById('resetBtn')?.addEventListener('click', () => this.resetLayout());
  }
  // ─── helpers ──────────────────────────────────────────
  _getColCount() {
    return parseInt(getComputedStyle(this.grid).getPropertyValue('--grid-cols')) || 4;
  }
  _showToast(msg) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('visible');
    clearTimeout(toast._hideTimer);
    toast._hideTimer = setTimeout(() => toast.classList.remove('visible'), 2000);
  }
  // ─── destructor ───────────────────────────────────────
  destroy() {
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
    }
    if (this.resizeRAF) {
      cancelAnimationFrame(this.resizeRAF);
      this.resizeRAF = null;
    }
    this.dragState = null;
    this.resizeState = null;
  }
}
// ─── init ───────────────────────────────────────────────
const dashboard = new DashboardLayout(document.getElementById('grid'));
</script>
</body>
</html>
```