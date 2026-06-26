<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Layout Architect</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f0f2f5; color: #1a1a2e; min-height: 100vh; }
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 12px;
  padding: 16px;
  max-width: 1440px;
  margin: 0 auto;
  position: relative;
  min-height: 400px;
  touch-action: none;
}
.panel {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  user-select: none;
  contain: layout style;
}
.panel:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.10);
}
.panel.dragging {
  opacity: 0.88;
  box-shadow: 0 12px 32px rgba(0,0,0,0.18);
  z-index: 100;
  transition: none;
  pointer-events: none;
}
.panel.resize-active {
  z-index: 100;
  box-shadow: 0 4px 16px rgba(59,130,246,0.20);
}
.panel.hidden { display: none; }
.panel.collapsed .panel-body { display: none; }
.panel-header {
  display: flex;
  align-items: center;
  padding: 6px 10px;
  gap: 6px;
  min-height: 36px;
  cursor: default;
  border-bottom: 1px solid #edf2f7;
}
.panel.collapsed .panel-header {
  border-bottom: none;
}
.panel-drag-handle {
  cursor: grab;
  color: #94a3b8;
  padding: 2px 6px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  font-size: 14px;
  line-height: 1;
  flex-shrink: 0;
  touch-action: none;
}
.panel-drag-handle:hover {
  color: #475569;
  background: #f1f5f9;
}
.panel-drag-handle:active { cursor: grabbing; }
.panel-title {
  flex: 1;
  font-weight: 600;
  font-size: 13px;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: pointer;
}
.panel-controls {
  display: flex;
  gap: 2px;
  flex-shrink: 0;
  align-items: center;
}
.panel-btn {
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  color: #64748b;
  transition: background 0.12s, color 0.12s;
}
.panel-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}
.panel-btn:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 1px;
}
.panel-body {
  padding: 12px;
  flex: 1;
  font-size: 13px;
  color: #475569;
  line-height: 1.5;
  min-height: 40px;
  white-space: pre-line;
}
.panel-resize-corner {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 18px;
  height: 18px;
  cursor: nwse-resize;
  z-index: 2;
  touch-action: none;
}
.panel-resize-corner::after {
  content: '';
  position: absolute;
  right: 4px;
  bottom: 4px;
  width: 8px;
  height: 8px;
  border-right: 2px solid #94a3b8;
  border-bottom: 2px solid #94a3b8;
  border-radius: 0 0 2px 0;
}
.panel-resize-corner:hover::after {
  border-color: #3b82f6;
}
.dashboard-controls {
  display: flex;
  gap: 8px;
  align-items: center;
  padding: 10px 16px;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 50;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.control-btn {
  padding: 6px 14px;
  border: 1px solid #d1d5db;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  color: #374151;
  transition: all 0.12s;
}
.control-btn:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}
.control-btn:active { background: #f3f4f6; }
.control-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}
.control-btn.primary {
  background: #3b82f6;
  color: #fff;
  border-color: #3b82f6;
}
.control-btn.primary:hover { background: #2563eb; }
.control-btn.danger {
  color: #dc2626;
  border-color: #fca5a5;
}
.control-btn.danger:hover { background: #fef2f2; }
.control-label {
  font-size: 11px;
  color: #94a3b8;
  margin-right: auto;
  font-weight: 500;
  letter-spacing: 0.02em;
}
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: #1e293b;
  color: #f8fafc;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 13px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.20);
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 0.2s, transform 0.2s;
  z-index: 1000;
  pointer-events: none;
}
.toast.visible {
  opacity: 1;
  transform: translateY(0);
}
.dashboard-empty {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
  font-size: 14px;
}
.panel:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: -2px;
  border-radius: 8px;
}
</style>
</head>
<body>
<div id="dashboard-root"></div>
<script>
(() => {
'use strict';
var DEFAULT_LAYOUT = {
columns: 12,
panels: [
{ id: 'metrics', title: 'System Metrics', content: 'CPU Usage: 45%\nMemory: 6.2 / 16 GB\nDisk: 78%\nNetwork: 1.2 Gbps', row: 1, col: 1, width: 4, height: 2, collapsed: false, hidden: false },
{ id: 'activity', title: 'User Activity', content: 'Active Sessions: 23\nNew Users (24h): 156\nPage Views: 12.4K\nAvg Session: 4m 32s', row: 1, col: 5, width: 4, height: 2, collapsed: false, hidden: false },
{ id: 'alerts', title: 'Alerts', content: '3 Critical\n12 Warning\n28 Info\nLast: DB replication lag at 02:34 UTC', row: 1, col: 9, width: 4, height: 2, collapsed: false, hidden: false },
{ id: 'performance', title: 'Performance', content: 'API Response: 234ms avg\nError Rate: 0.02%\nThroughput: 1,892 req/s\nP99: 890ms', row: 3, col: 1, width: 6, height: 2, collapsed: false, hidden: false },
{ id: 'orders', title: 'Recent Orders', content: 'Order #10482 — Alice M. — $129.99\nOrder #10483 — Bob K. — $45.00\nOrder #10484 — Carol S. — $299.00\nOrder #10485 — Dave L. — $79.50', row: 3, col: 7, width: 6, height: 3, collapsed: false, hidden: false },
{ id: 'analytics', title: 'Analytics Overview', content: 'Revenue: $48,230 (+12% vs last week)\nConversion: 3.8%\nBounce: 24%\nTop page: /pricing', row: 6, col: 1, width: 12, height: 2, collapsed: false, hidden: false }
]
};
function deepClone(obj) {
return JSON.parse(JSON.stringify(obj));
}
function UndoManager(maxSize) {
this.undoStack = [];
this.redoStack = [];
this.maxSize = maxSize || 50;
}
UndoManager.prototype.push = function(state) {
this.undoStack.push(deepClone(state));
if (this.undoStack.length > this.maxSize) {
this.undoStack.shift();
}
this.redoStack = [];
};
UndoManager.prototype.undo = function(currentState) {
if (this.undoStack.length === 0) return null;
this.redoStack.push(deepClone(currentState));
return this.undoStack.pop();
};
UndoManager.prototype.redo = function(currentState) {
if (this.redoStack.length === 0) return null;
this.undoStack.push(deepClone(currentState));
return this.redoStack.pop();
};
UndoManager.prototype.canUndo = function() {
return this.undoStack.length > 0;
};
UndoManager.prototype.canRedo = function() {
return this.redoStack.length > 0;
};
UndoManager.prototype.clear = function() {
this.undoStack = [];
this.redoStack = [];
};
function DashboardLayout(container, options) {
if (!container) throw new Error('Container element is required');
this.container = container;
this.options = options || {};
this.options.columns = this.options.columns || 12;
this.options.gap = this.options.gap || 12;
this.options.userProfile = this.options.userProfile || 'default';
this.options.storageKey = this.options.storageKey || 'styde-dashboard-layout';
this.options.minPanelWidth = this.options.minPanelWidth || 2;
this.options.minPanelHeight = this.options.minPanelHeight || 1;
this.options.maxPanelWidth = this.options.maxPanelWidth || 12;
this.options.maxPanelHeight = this.options.maxPanelHeight || 8;
this.state = null;
this.undoManager = new UndoManager(50);
this.ac = new AbortController();
this.dragContext = null;
this.resizeContext = null;
this.gridEl = null;
this.controlsEl = null;
this.toastTimer = null;
this.init();
}
DashboardLayout.prototype.init = function() {
var saved = this.loadLayout();
this.state = saved || deepClone(DEFAULT_LAYOUT);
this.render();
this.bindEvents();
this.bindKeyboard();
this.updateControls();
};
DashboardLayout.prototype.getDefaultLayout = function() {
return deepClone(DEFAULT_LAYOUT);
};
DashboardLayout.prototype.render = function() {
if (!this.container) return;
this.container.innerHTML = '';
this.controlsEl = document.createElement('div');
this.controlsEl.className = 'dashboard-controls';
this.controlsEl.innerHTML =
'<span class="control-label">Dashboard Layout</span>' +
'<button class="control-btn" data-action="undo" disabled>Undo (Ctrl+Z)</button>' +
'<button class="control-btn" data-action="redo" disabled>Redo (Ctrl+Shift+Z)</button>' +
'<button class="control-btn primary" data-action="save">Save Layout</button>' +
'<button class="control-btn danger" data-action="reset">Reset Default</button>';
this.container.appendChild(this.controlsEl);
this.gridEl = document.createElement('div');
this.gridEl.className = 'dashboard-grid';
this.gridEl.style.gap = this.options.gap + 'px';
this.container.appendChild(this.gridEl);
var visible = this.state.panels.filter(function(p) { return !p.hidden; });
if (visible.length === 0) {
var empty = document.createElement('div');
empty.className = 'dashboard-empty';
empty.textContent = 'All panels are hidden. Use Undo (Ctrl+Z) to restore them.';
this.gridEl.appendChild(empty);
return;
}
var frag = document.createDocumentFragment();
var self = this;
this.state.panels.forEach(function(panel) {
if (panel.hidden) return;
frag.appendChild(self.createPanelElement(panel));
});
this.gridEl.appendChild(frag);
this.undoManager.push(deepClone(this.state));
};
DashboardLayout.prototype.createPanelElement = function(panel) {
var el = document.createElement('div');
el.className = 'panel' + (panel.collapsed ? ' collapsed' : '');
el.dataset.panelId = panel.id;
el.setAttribute('role', 'region');
el.setAttribute('aria-label', panel.title);
el.tabIndex = 0;
el.style.gridRow = panel.row + ' / span ' + panel.height;
el.style.gridColumn = panel.col + ' / span ' + panel.width;
var header = document.createElement('div');
header.className = 'panel-header';
var dragHandle = document.createElement('span');
dragHandle.className = 'panel-drag-handle';
dragHandle.innerHTML = '⠿';
dragHandle.title = 'Drag to reorder';
dragHandle.setAttribute('role', 'button');
dragHandle.setAttribute('aria-label', 'Drag panel');
dragHandle.tabIndex = 0;
var title = document.createElement('span');
title.className = 'panel-title';
title.textContent = panel.title;
title.setAttribute('role', 'button');
title.setAttribute('aria-label', (panel.collapsed ? 'Expand' : 'Collapse') + ' ' + panel.title);
title.dataset.action = 'toggle-collapse';
var controls = document.createElement('span');
controls.className = 'panel-controls';
var collapseBtn = document.createElement('button');
collapseBtn.className = 'panel-btn';
collapseBtn.innerHTML = panel.collapsed ? '&#9660;' : '&#9650;';
collapseBtn.title = panel.collapsed ? 'Expand' : 'Collapse';
collapseBtn.dataset.action = 'toggle-collapse';
collapseBtn.setAttribute('aria-label', panel.collapsed ? 'Expand panel' : 'Collapse panel');
var hideBtn = document.createElement('button');
hideBtn.className = 'panel-btn';
hideBtn.innerHTML = '&#10005;';
hideBtn.title = 'Hide panel';
hideBtn.dataset.action = 'toggle-hide';
hideBtn.setAttribute('aria-label', 'Hide panel');
controls.appendChild(collapseBtn);
controls.appendChild(hideBtn);
header.appendChild(dragHandle);
header.appendChild(title);
header.appendChild(controls);
var body = document.createElement('div');
body.className = 'panel-body';
body.textContent = panel.content;
var resizeCorner = document.createElement('div');
resizeCorner.className = 'panel-resize-corner';
resizeCorner.dataset.action = 'resize';
resizeCorner.title = 'Drag to resize';
el.appendChild(header);
el.appendChild(body);
el.appendChild(resizeCorner);
return el;
};
DashboardLayout.prototype.bindEvents = function() {
var signal = this.ac.signal;
var self = this;
this.gridEl.addEventListener('pointerdown', function(e) {
self.handleGridPointerDown(e);
}, { signal });
this.gridEl.addEventListener('pointermove', function(e) {
self.handleGridPointerMove(e);
}, { signal, passive: true });
this.gridEl.addEventListener('pointerup', function(e) {
self.handleGridPointerUp(e);
}, { signal });
this.gridEl.addEventListener('pointercancel', function(e) {
self.handleGridPointerUp(e);
}, { signal });
this.controlsEl.addEventListener('click', function(e) {
var btn = e.target.closest('[data-action]');
if (!btn) return;
var action = btn.dataset.action;
if (action === 'undo') self.undo();
else if (action === 'redo') self.redo();
else if (action === 'save') self.saveLayoutWithFeedback();
else if (action === 'reset') self.resetLayout();
}, { signal });
this.gridEl.addEventListener('click', function(e) {
var target = e.target.closest('[data-action]');
if (!target) return;
var action = target.dataset.action;
if (action !== 'toggle-collapse' && action !== 'toggle-hide') return;
var panelEl = target.closest('[data-panel-id]');
if (!panelEl) return;
var panelId = panelEl.dataset.panelId;
if (action === 'toggle-collapse') {
self.pushUndoState();
self.toggleCollapse(panelId);
} else if (action === 'toggle-hide') {
self.pushUndoState();
self.toggleHide(panelId);
}
}, { signal });
};
DashboardLayout.prototype.bindKeyboard = function() {
var signal = this.ac.signal;
var self = this;
document.addEventListener('keydown', function(e) {
self.handleKeyboard(e);
}, { signal });
};
DashboardLayout.prototype.handleGridPointerDown = function(e) {
if (e.target.closest('.panel-drag-handle')) {
e.preventDefault();
var panelEl = e.target.closest('[data-panel-id]');
if (!panelEl) return;
this.pushUndoState();
this.startDrag(panelEl.dataset.panelId, e);
return;
}
var target = e.target.closest('[data-action="resize"]');
if (target) {
e.preventDefault();
var panelEl = target.closest('[data-panel-id]');
if (!panelEl) return;
this.pushUndoState();
this.startResize(panelEl.dataset.panelId, e);
return;
}
};
DashboardLayout.prototype.handleGridPointerMove = function(e) {
if (this.dragContext) {
this.dragContext.latestX = e.clientX;
this.dragContext.latestY = e.clientY;
if (!this.dragContext.rAFId) {
var self = this;
this.dragContext.rAFId = requestAnimationFrame(function() {
self.doDragFrame();
});
}
}
if (this.resizeContext) {
this.resizeContext.latestX = e.clientX;
this.resizeContext.latestY = e.clientY;
if (!this.resizeContext.rAFId) {
var self = this;
this.resizeContext.rAFId = requestAnimationFrame(function() {
self.doResizeFrame();
});
}
}
};
DashboardLayout.prototype.handleGridPointerUp = function(e) {
if (this.dragContext) {
this.endDrag();
}
if (this.resizeContext) {
this.endResize();
}
};
DashboardLayout.prototype.startDrag = function(panelId, e) {
var panel = null;
for (var i = 0; i < this.state.panels.length; i++) {
if (this.state.panels[i].id === panelId) { panel = this.state.panels[i]; break; }
}
if (!panel) return;
var el = this.gridEl.querySelector('[data-panel-id="' + panelId + '"]');
if (!el) return;
var rect = el.getBoundingClientRect();
this.dragContext = {
panelId: panelId,
pointerId: e.pointerId,
startX: e.clientX,
startY: e.clientY,
latestX: e.clientX,
latestY: e.clientY,
startRow: panel.row,
startCol: panel.col,
offsetX: e.clientX - rect.left,
offsetY: e.clientY - rect.top,
rAFId: null
};
el.classList.add('dragging');
this.gridEl.setPointerCapture(e.pointerId);
};
DashboardLayout.prototype.doDragFrame = function() {
var ctx = this.dragContext;
if (!ctx) return;
ctx.rAFId = null;
var x = ctx.latestX;
var y = ctx.latestY;
var el = this.gridEl.querySelector('[data-panel-id="' + ctx.panelId + '"]');
if (!el) return;
var dx = x - ctx.startX;
var dy = y - ctx.startY;
el.style.transform = 'translate(' + dx + 'px, ' + dy + 'px)';
el.style.transition = 'none';
};
DashboardLayout.prototype.endDrag = function() {
var ctx = this.dragContext;
if (!ctx) return;
if (ctx.rAFId) {
cancelAnimationFrame(ctx.rAFId);
}
var el = this.gridEl.querySelector('[data-panel-id="' + ctx.panelId + '"]');
if (el) {
el.classList.remove('dragging');
el.style.transform = '';
el.style.transition = '';
}
this.gridEl.releasePointerCapture(ctx.pointerId);
var panel = null;
for (var i = 0; i < this.state.panels.length; i++) {
if (this.state.panels[i].id === ctx.panelId) { panel = this.state.panels[i]; break; }
}
if (panel) {
var gridRect = this.gridEl.getBoundingClientRect();
var totalGap = (this.options.columns - 1) * this.options.gap;
var colWidth = (gridRect.width - totalGap) / this.options.columns;
var rowHeight = 80;
var localX = ctx.latestX - gridRect.left - ctx.offsetX;
var localY = ctx.latestY - gridRect.top - ctx.offsetY;
var targetCol = Math.round(localX / (colWidth + this.options.gap)) + 1;
var targetRow = Math.round(localY / (rowHeight + this.options.gap)) + 1;
targetCol = Math.max(1, Math.min(targetCol, this.options.columns - panel.width + 1));
targetRow = Math.max(1, targetRow);
if (targetRow !== panel.row || targetCol !== panel.col) {
panel.row = targetRow;
panel.col = targetCol;
this.resolveCollisions(panel);
this.repositionAllPanels();
this.saveLayout();
this.updateControls();
}
}
this.dragContext = null;
};
DashboardLayout.prototype.resolveCollisions = function(movedPanel) {
var panels = this.state.panels;
var MAX_ITER = 20;
var iter = 0;
while (iter < MAX_ITER) {
var hit = false;
for (var i = 0; i < panels.length; i++) {
var other = panels[i];
if (other.id === movedPanel.id || other.hidden) continue;
if (this.panelsOverlap(movedPanel, other)) {
other.row = movedPanel.row + movedPanel.height;
hit = true;
}
}
if (!hit) break;
iter++;
}
};
DashboardLayout.prototype.panelsOverlap = function(a, b) {
var aR1 = a.row, aR2 = a.row + a.height - 1;
var aC1 = a.col, aC2 = a.col + a.width - 1;
var bR1 = b.row, bR2 = b.row + b.height - 1;
var bC1 = b.col, bC2 = b.col + b.width - 1;
return aR1 <= bR2 && aR2 >= bR1 && aC1 <= bC2 && aC2 >= bC1;
};
DashboardLayout.prototype.repositionAllPanels = function() {
var self = this;
this.state.panels.forEach(function(panel) {
if (panel.hidden) return;
var el = self.gridEl.querySelector('[data-panel-id="' + panel.id + '"]');
if (!el) return;
el.style.gridRow = panel.row + ' / span ' + panel.height;
el.style.gridColumn = panel.col + ' / span ' + panel.width;
});
};
DashboardLayout.prototype.startResize = function(panelId, e) {
var panel = null;
for (var i = 0; i < this.state.panels.length; i++) {
if (this.state.panels[i].id === panelId) { panel = this.state.panels[i]; break; }
}
if (!panel) return;
var el = this.gridEl.querySelector('[data-panel-id="' + panelId + '"]');
if (!el) return;
this.resizeContext = {
panelId: panelId,
pointerId: e.pointerId,
startX: e.clientX,
startY: e.clientY,
latestX: e.clientX,
latestY: e.clientY,
startWidth: panel.width,
startHeight: panel.height,
startCol: panel.col,
startRow: panel.row,
rAFId: null
};
el.classList.add('resize-active');
this.gridEl.setPointerCapture(e.pointerId);
};
DashboardLayout.prototype.doResizeFrame = function() {
var ctx = this.resizeContext;
if (!ctx) return;
ctx.rAFId = null;
var x = ctx.latestX;
var y = ctx.latestY;
var gridRect = this.gridEl.getBoundingClientRect();
var totalGap = (this.options.columns - 1) * this.options.gap;
var colWidth = (gridRect.width - totalGap) / this.options.columns;
var rowHeight = 80;
var dx = x - ctx.startX;
var dy = y - ctx.startY;
var newWidth = ctx.startWidth + Math.round(dx / (colWidth + this.options.gap));
var newHeight = ctx.startHeight + Math.round(dy / (rowHeight + this.options.gap));
newWidth = Math.max(this.options.minPanelWidth, Math.min(this.options.maxPanelWidth, newWidth));
newHeight = Math.max(this.options.minPanelHeight, Math.min(this.options.maxPanelHeight, newHeight));
var maxW = this.options.columns - ctx.startCol + 1;
if (newWidth > maxW) newWidth = maxW;
var panel = null;
for (var i = 0; i < this.state.panels.length; i++) {
if (this.state.panels[i].id === ctx.panelId) { panel = this.state.panels[i]; break; }
}
if (!panel) return;
panel.width = newWidth;
panel.height = newHeight;
var el = this.gridEl.querySelector('[data-panel-id="' + ctx.panelId + '"]');
if (el) {
el.style.gridRow = panel.row + ' / span ' + panel.height;
el.style.gridColumn = panel.col + ' / span ' + panel.width;
}
};
DashboardLayout.prototype.endResize = function() {
var ctx = this.resizeContext;
if (!ctx) return;
if (ctx.rAFId) {
cancelAnimationFrame(ctx.rAFId);
}
var el = this.gridEl.querySelector('[data-panel-id="' + ctx.panelId + '"]');
if (el) {
el.classList.remove('resize-active');
}
this.gridEl.releasePointerCapture(ctx.pointerId);
this.saveLayout();
this.updateControls();
this.resizeContext = null;
};
DashboardLayout.prototype.toggleCollapse = function(panelId) {
var panel = null;
for (var i = 0; i < this.state.panels.length; i++) {
if (this.state.panels[i].id === panelId) { panel = this.state.panels[i]; break; }
}
if (!panel) return;
panel.collapsed = !panel.collapsed;
var el = this.gridEl.querySelector('[data-panel-id="' + panelId + '"]');
if (el) {
el.classList.toggle('collapsed', panel.collapsed);
var btn = el.querySelector('[data-action="toggle-collapse"]');
if (btn) {
btn.innerHTML = panel.collapsed ? '&#9660;' : '&#9650;';
btn.title = panel.collapsed ? 'Expand' : 'Collapse';
}
var titleBtn = el.querySelector('.panel-title');
if (titleBtn) {
titleBtn.setAttribute('aria-label', (panel.collapsed ? 'Expand' : 'Collapse') + ' ' + panel.title);
}
}
this.saveLayout();
this.updateControls();
};
DashboardLayout.prototype.toggleHide = function(panelId) {
var panel = null;
for (var i = 0; i < this.state.panels.length; i++) {
if (this.state.panels[i].id === panelId) { panel = this.state.panels[i]; break; }
}
if (!panel) return;
panel.hidden = !panel.hidden;
this.reconcileDom();
this.saveLayout();
this.updateControls();
};
DashboardLayout.prototype.reconcileDom = function() {
var existing = this.gridEl.querySelectorAll('[data-panel-id]');
var self = this;
existing.forEach(function(el) {
var id = el.dataset.panelId;
var found = false;
for (var i = 0; i < self.state.panels.length; i++) {
if (self.state.panels[i].id === id && !self.state.panels[i].hidden) {
found = true;
break;
}
}
if (!found) el.remove();
});
var visible = this.state.panels.filter(function(p) { return !p.hidden; });
var emptyState = this.gridEl.querySelector('.dashboard-empty');
if (visible.length === 0) {
if (!emptyState) {
var empty = document.createElement('div');
empty.className = 'dashboard-empty';
empty.textContent = 'All panels are hidden. Use Undo (Ctrl+Z) to restore them.';
this.gridEl.appendChild(empty);
}
return;
}
if (emptyState) emptyState.remove();
var self = this;
this.state.panels.forEach(function(panel) {
if (panel.hidden) return;
var el = self.gridEl.querySelector('[data-panel-id="' + panel.id + '"]');
if (!el) {
el = self.createPanelElement(panel);
self.gridEl.appendChild(el);
} else {
el.style.gridRow = panel.row + ' / span ' + panel.height;
el.style.gridColumn = panel.col + ' / span ' + panel.width;
}
});
};
DashboardLayout.prototype.updateControls = function() {
if (!this.controlsEl) return;
var undoBtn = this.controlsEl.querySelector('[data-action="undo"]');
var redoBtn = this.controlsEl.querySelector('[data-action="redo"]');
if (undoBtn) undoBtn.disabled = !this.undoManager.canUndo();
if (redoBtn) redoBtn.disabled = !this.undoManager.canRedo();
};
DashboardLayout.prototype.undo = function() {
var prev = this.undoManager.undo(deepClone(this.state));
if (!prev) return;
this.state = prev;
this.reconcileDom();
this.saveLayout();
this.updateControls();
this.showToast('Undo applied');
};
DashboardLayout.prototype.redo = function() {
var next = this.undoManager.redo(deepClone(this.state));
if (!next) return;
this.state = next;
this.reconcileDom();
this.saveLayout();
this.updateControls();
this.showToast('Redo applied');
};
DashboardLayout.prototype.resetLayout = function() {
this.undoManager.push(deepClone(this.state));
this.state = deepClone(DEFAULT_LAYOUT);
this.container.innerHTML = '';
this.render();
this.bindEvents();
this.saveLayout();
this.updateControls();
this.showToast('Layout reset to default');
};
DashboardLayout.prototype.saveLayout = function() {
try {
var key = this.options.storageKey + '-' + this.options.userProfile;
localStorage.setItem(key, JSON.stringify(this.state));
} catch (e) {
console.warn('Failed to save layout:', e);
}
};
DashboardLayout.prototype.saveLayoutWithFeedback = function() {
this.saveLayout();
this.showToast('Layout saved');
};
DashboardLayout.prototype.loadLayout = function() {
try {
var key = this.options.storageKey + '-' + this.options.userProfile;
var raw = localStorage.getItem(key);
if (!raw) return null;
var parsed = JSON.parse(raw);
if (!parsed || !Array.isArray(parsed.panels)) return null;
return parsed;
} catch (e) {
console.warn('Failed to load layout:', e);
return null;
}
};
DashboardLayout.prototype.handleKeyboard = function(e) {
if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
e.preventDefault();
this.undo();
return;
}
if ((e.ctrlKey || e.metaKey) && e.key === 'z' && e.shiftKey) {
e.preventDefault();
this.redo();
return;
}
if ((e.ctrlKey || e.metaKey) && e.key === 'y') {
e.preventDefault();
this.redo();
return;
}
if (e.key === 'Escape') {
if (this.dragContext) this.endDrag();
if (this.resizeContext) this.endResize();
return;
}
if (e.key === 'Tab') {
var panels = this.gridEl.querySelectorAll('[data-panel-id]');
if (panels.length === 0) return;
var current = document.activeElement ? document.activeElement.closest('[data-panel-id]') : null;
var idx = -1;
if (current) {
var arr = Array.from(panels);
idx = arr.indexOf(current);
}
if (e.shiftKey) {
idx = idx <= 0 ? panels.length - 1 : idx - 1;
} else {
idx = idx >= panels.length - 1 ? 0 : idx + 1;
}
e.preventDefault();
panels[idx].focus();
panels[idx].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
return;
}
if (e.key === 'Enter' || e.key === ' ') {
var focused = document.activeElement;
if (!focused) return;
var actionEl = focused.closest('[data-action]');
if (!actionEl) return;
var action = actionEl.dataset.action;
var panelEl = focused.closest('[data-panel-id]');
if (!panelEl) return;
e.preventDefault();
if (action === 'toggle-collapse') {
this.pushUndoState();
this.toggleCollapse(panelEl.dataset.panelId);
} else if (action === 'toggle-hide') {
this.pushUndoState();
this.toggleHide(panelEl.dataset.panelId);
}
}
};
DashboardLayout.prototype.showToast = function(message) {
var toast = document.querySelector('.toast');
if (!toast) {
toast = document.createElement('div');
toast.className = 'toast';
document.body.appendChild(toast);
}
toast.textContent = message;
toast.classList.add('visible');
clearTimeout(this.toastTimer);
var self = this;
this.toastTimer = setTimeout(function() {
toast.classList.remove('visible');
}, 2000);
};
DashboardLayout.prototype.destroy = function() {
if (this.dragContext && this.dragContext.rAFId) {
cancelAnimationFrame(this.dragContext.rAFId);
}
if (this.resizeContext && this.resizeContext.rAFId) {
cancelAnimationFrame(this.resizeContext.rAFId);
}
this.ac.abort();
if (this.container) this.container.innerHTML = '';
this.dragContext = null;
this.resizeContext = null;
this.state = null;
};
var root = document.getElementById('dashboard-root');
if (root) {
new DashboardLayout(root, { userProfile: 'default' });
}
})();
</script>
</body>
</html>