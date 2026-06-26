```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Task Board - Production Dashboard</title>
<style>
/* ===== DESIGN TOKENS ===== */
:root {
  --color-bg: #0f1117;
  --color-surface: #1a1d27;
  --color-surface-hover: #222639;
  --color-border: #2a2e3e;
  --color-text-primary: #e8eaed;
  --color-text-secondary: #9aa0b0;
  --color-text-muted: #5c6172;
  --color-accent: #6c5ce7;
  --color-accent-hover: #7f71f0;
  --color-accent-glow: rgba(108,92,231,0.25);
  --color-success: #00c853;
  --color-warning: #ffd600;
  --color-danger: #ff5252;
  --color-info: #448aff;
  --color-todo: #5c6172;
  --color-inprogress: #448aff;
  --color-review: #ffd600;
  --color-done: #00c853;
  --font-sans: 'Segoe UI', system-ui, -apple-system, sans-serif;
  --font-mono: 'Cascadia Code', 'Fira Code', 'JetBrains Mono', monospace;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg: 0 8px 30px rgba(0,0,0,0.5);
  --shadow-accent: 0 4px 20px rgba(108,92,231,0.3);
  --transition-fast: 150ms ease;
  --transition-normal: 250ms ease;
  --transition-slow: 400ms cubic-bezier(0.22, 1, 0.36, 1);
  --max-width: 1400px;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; -webkit-font-smoothing: antialiased; }
body {
  font-family: var(--font-sans);
  background: var(--color-bg);
  color: var(--color-text-primary);
  min-height: 100vh;
  line-height: 1.5;
}
/* ===== LAYOUT ===== */
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 32px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
.app-header h1 {
  font-size: 1.25rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
}
.app-header h1 .logo-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--color-accent);
  box-shadow: 0 0 8px var(--color-accent-glow);
  display: inline-block;
}
.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}
.task-count {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  background: var(--color-bg);
  padding: 6px 14px;
  border-radius: 20px;
  border: 1px solid var(--color-border);
}
.app-main {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 24px 32px;
}
/* ===== TOOLBAR ===== */
.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  flex-wrap: wrap;
  align-items: center;
}
.search-box {
  flex: 1;
  min-width: 200px;
  position: relative;
}
.search-box input {
  width: 100%;
  padding: 10px 16px 10px 40px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: 0.875rem;
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
  outline: none;
}
.search-box input:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-glow);
}
.search-box input::placeholder { color: var(--color-text-muted); }
.search-box .search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  font-size: 1rem;
  pointer-events: none;
}
.filter-group {
  display: flex;
  gap: 6px;
}
.filter-btn {
  padding: 8px 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  font-size: 0.8125rem;
  cursor: pointer;
  transition: all var(--transition-fast);
  font-family: inherit;
}
.filter-btn:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}
.filter-btn.active {
  background: var(--color-accent);
  border-color: var(--color-accent);
  color: #fff;
  box-shadow: var(--shadow-accent);
}
.btn-primary {
  padding: 10px 20px;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-md);
  color: #fff;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  font-family: inherit;
  display: flex;
  align-items: center;
  gap: 6px;
}
.btn-primary:hover {
  background: var(--color-accent-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-accent);
}
.btn-primary:active { transform: translateY(0); }
.btn-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 1rem;
}
.btn-icon:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
  border-color: var(--color-accent);
}
/* ===== BOARD ===== */
.board {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  min-height: 500px;
}
.column {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.column-header {
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--color-border);
  background: rgba(255,255,255,0.015);
}
.column-title {
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  display: flex;
  align-items: center;
  gap: 8px;
}
.column-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}
.column-dot.todo { background: var(--color-todo); }
.column-dot.in-progress { background: var(--color-inprogress); }
.column-dot.review { background: var(--color-review); }
.column-dot.done { background: var(--color-done); }
.column-count {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  background: var(--color-bg);
  padding: 2px 10px;
  border-radius: 10px;
}
.column-body {
  padding: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
  max-height: calc(100vh - 280px);
}
/* ===== TASK CARD ===== */
.task-card {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 14px;
  cursor: pointer;
  transition: all var(--transition-normal);
  position: relative;
  animation: cardEnter var(--transition-slow) both;
}
.task-card:hover {
  border-color: var(--color-accent);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.task-card:active {
  transform: translateY(0) scale(0.99);
}
.task-card.dragging {
  opacity: 0.5;
  transform: rotate(2deg) scale(0.98);
}
.task-card .task-tag {
  display: inline-block;
  font-size: 0.6875rem;
  font-weight: 500;
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
  letter-spacing: 0.02em;
}
.tag-bug { background: rgba(255,82,82,0.15); color: var(--color-danger); }
.tag-feature { background: rgba(68,138,255,0.15); color: var(--color-info); }
.tag-improvement { background: rgba(0,200,83,0.15); color: var(--color-success); }
.tag-docs { background: rgba(255,214,0,0.15); color: var(--color-warning); }
.task-card h3 {
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 4px;
  color: var(--color-text-primary);
}
.task-card p {
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.task-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--color-border);
}
.task-priority {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  padding: 2px 8px;
  border-radius: 4px;
}
.priority-high { color: var(--color-danger); background: rgba(255,82,82,0.1); }
.priority-medium { color: var(--color-warning); background: rgba(255,214,0,0.1); }
.priority-low { color: var(--color-success); background: rgba(0,200,83,0.1); }
.task-assignee {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  color: var(--color-text-muted);
}
.task-avatar {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--color-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.625rem;
  font-weight: 600;
  color: #fff;
  flex-shrink: 0;
}
/* ===== MODAL ===== */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.65);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--transition-normal);
}
.modal-overlay.open {
  opacity: 1;
  pointer-events: all;
}
.modal {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  width: 480px;
  max-width: 90vw;
  max-height: 85vh;
  overflow-y: auto;
  padding: 28px;
  transform: scale(0.92) translateY(20px);
  transition: transform var(--transition-slow);
  box-shadow: var(--shadow-lg);
}
.modal-overlay.open .modal {
  transform: scale(1) translateY(0);
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.modal-header h2 {
  font-size: 1.125rem;
  font-weight: 600;
}
.modal-close {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  font-size: 1.125rem;
}
.modal-close:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}
.form-group {
  margin-bottom: 16px;
}
.form-group label {
  display: block;
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
}
.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 14px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  color: var(--color-text-primary);
  font-size: 0.875rem;
  font-family: inherit;
  transition: border-color var(--transition-fast);
  outline: none;
}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-glow);
}
.form-group textarea {
  resize: vertical;
  min-height: 80px;
}
.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 24px;
}
.btn-secondary {
  padding: 10px 20px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all var(--transition-fast);
  font-family: inherit;
}
.btn-secondary:hover {
  background: var(--color-surface-hover);
  color: var(--color-text-primary);
}
/* ===== STATES ===== */
.loading-state, .empty-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
  grid-column: 1 / -1;
}
.loading-spinner {
  width: 36px;
  height: 36px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 16px;
}
.loading-state p, .empty-state p, .error-state p {
  color: var(--color-text-secondary);
  font-size: 0.875rem;
}
.empty-state .empty-icon {
  font-size: 2.5rem;
  margin-bottom: 12px;
  opacity: 0.4;
}
.error-state .error-icon {
  font-size: 2rem;
  color: var(--color-danger);
  margin-bottom: 12px;
}
.error-retry {
  margin-top: 12px;
  padding: 8px 20px;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-sm);
  color: #fff;
  cursor: pointer;
  font-family: inherit;
  font-size: 0.8125rem;
  transition: background var(--transition-fast);
}
.error-retry:hover { background: var(--color-accent-hover); }
/* ===== SKELETON ===== */
.skeleton-card {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 14px;
}
.skeleton-line {
  height: 12px;
  background: linear-gradient(90deg, var(--color-border) 25%, var(--color-surface-hover) 50%, var(--color-border) 75%);
  background-size: 200% 100%;
  border-radius: 4px;
  margin-bottom: 8px;
  animation: shimmer 1.5s ease-in-out infinite;
}
.skeleton-line:last-child { width: 60%; }
.skeleton-tag {
  width: 50px;
  height: 16px;
  border-radius: 4px;
  margin-bottom: 10px;
  background: linear-gradient(90deg, var(--color-border) 25%, var(--color-surface-hover) 50%, var(--color-border) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}
/* ===== TOAST ===== */
.toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.toast {
  padding: 12px 20px;
  border-radius: var(--radius-md);
  font-size: 0.8125rem;
  font-weight: 500;
  box-shadow: var(--shadow-lg);
  animation: slideUp var(--transition-slow) both;
  display: flex;
  align-items: center;
  gap: 8px;
}
.toast.success { background: var(--color-success); color: #000; }
.toast.error { background: var(--color-danger); color: #fff; }
.toast.info { background: var(--color-info); color: #fff; }
/* ===== DRAG OVERLAY ===== */
.drop-indicator {
  border: 2px dashed var(--color-accent);
  border-radius: var(--radius-md);
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-accent);
  font-size: 0.8125rem;
  font-weight: 500;
  background: rgba(108,92,231,0.05);
  transition: all var(--transition-fast);
}
.column.drag-over {
  border-color: var(--color-accent);
  box-shadow: inset 0 0 0 1px var(--color-accent), var(--shadow-accent);
}
/* ===== ANIMATIONS ===== */
@keyframes cardEnter {
  from { opacity: 0; transform: translateY(12px) scale(0.96); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px) scale(0.9); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
/* ===== RESPONSIVE ===== */
@media (max-width: 1100px) {
  .board { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .app-header { padding: 12px 16px; }
  .app-main { padding: 16px; }
  .board { grid-template-columns: 1fr; }
  .toolbar { flex-direction: column; }
  .search-box { min-width: 100%; }
  .filter-group { width: 100%; overflow-x: auto; }
  .modal { width: 100%; max-width: 100%; border-radius: var(--radius-lg); margin: 12px; }
}
/* scrollbar styling */
.column-body::-webkit-scrollbar { width: 4px; }
.column-body::-webkit-scrollbar-track { background: transparent; }
.column-body::-webkit-scrollbar-thumb { background: var(--color-border); border-radius: 2px; }
.column-body::-webkit-scrollbar-thumb:hover { background: var(--color-text-muted); }
</style>
</head>
<body>
<header class="app-header">
  <h1><span class="logo-dot"></span>TaskBoard</h1>
  <div class="header-actions">
    <span class="task-count" id="totalCount">0 tasks</span>
    <button class="btn-primary" id="addTaskBtn">+ New Task</button>
  </div>
</header>
<main class="app-main">
  <div class="toolbar">
    <div class="search-box">
      <span class="search-icon">&#x1F50D;</span>
      <input type="text" id="searchInput" placeholder="Search tasks..." />
    </div>
    <div class="filter-group" id="filterGroup">
      <button class="filter-btn active" data-filter="all">All</button>
      <button class="filter-btn" data-filter="bug">Bug</button>
      <button class="filter-btn" data-filter="feature">Feature</button>
      <button class="filter-btn" data-filter="improvement">Improvement</button>
      <button class="filter-btn" data-filter="docs">Docs</button>
    </div>
  </div>
  <div class="board" id="board">
    <div class="column" data-status="todo">
      <div class="column-header">
        <span class="column-title"><span class="column-dot todo"></span>To Do</span>
        <span class="column-count" id="count-todo">0</span>
      </div>
      <div class="column-body" id="column-todo"></div>
    </div>
    <div class="column" data-status="in-progress">
      <div class="column-header">
        <span class="column-title"><span class="column-dot in-progress"></span>In Progress</span>
        <span class="column-count" id="count-in-progress">0</span>
      </div>
      <div class="column-body" id="column-in-progress"></div>
    </div>
    <div class="column" data-status="review">
      <div class="column-header">
        <span class="column-title"><span class="column-dot review"></span>Review</span>
        <span class="column-count" id="count-review">0</span>
      </div>
      <div class="column-body" id="column-review"></div>
    </div>
    <div class="column" data-status="done">
      <div class="column-header">
        <span class="column-title"><span class="column-dot done"></span>Done</span>
        <span class="column-count" id="count-done">0</span>
      </div>
      <div class="column-body" id="column-done"></div>
    </div>
  </div>
  <!-- loading/empty/error states injected by JS -->
</main>
<!-- Modal -->
<div class="modal-overlay" id="modalOverlay">
  <div class="modal">
    <div class="modal-header">
      <h2 id="modalTitle">New Task</h2>
      <button class="modal-close" id="modalClose">&times;</button>
    </div>
    <form id="taskForm">
      <div class="form-group">
        <label for="taskTitle">Title</label>
        <input type="text" id="taskTitle" required placeholder="e.g. Implement login flow" />
      </div>
      <div class="form-group">
        <label for="taskDescription">Description</label>
        <textarea id="taskDescription" placeholder="Describe the task..."></textarea>
      </div>
      <div class="form-group">
        <label for="taskTag">Tag</label>
        <select id="taskTag">
          <option value="feature">Feature</option>
          <option value="bug">Bug</option>
          <option value="improvement">Improvement</option>
          <option value="docs">Docs</option>
        </select>
      </div>
      <div class="form-group">
        <label for="taskPriority">Priority</label>
        <select id="taskPriority">
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="low">Low</option>
        </select>
      </div>
      <div class="form-group">
        <label for="taskAssignee">Assignee</label>
        <input type="text" id="taskAssignee" placeholder="Name" />
      </div>
      <div class="form-group">
        <label for="taskStatus">Status</label>
        <select id="taskStatus">
          <option value="todo">To Do</option>
          <option value="in-progress">In Progress</option>
          <option value="review">Review</option>
          <option value="done">Done</option>
        </select>
      </div>
      <div class="form-actions">
        <button type="button" class="btn-secondary" id="modalCancel">Cancel</button>
        <button type="submit" class="btn-primary" id="modalSubmit">Save</button>
      </div>
    </form>
  </div>
</div>
<div class="toast-container" id="toastContainer"></div>
<script>
/* ===== STATE MANAGEMENT ===== */
class TaskStore {
  constructor() {
    this.tasks = [];
    this.listeners = [];
    this.loading = false;
    this.error = null;
    this.searchQuery = '';
    this.filterTag = 'all';
    this._idCounter = 0;
  }
  subscribe(fn) {
    this.listeners.push(fn);
    return () => { this.listeners = this.listeners.filter(l => l !== fn); };
  }
  _notify() {
    this.listeners.forEach(fn => fn(this.getState()));
  }
  getState() {
    const filtered = this.tasks.filter(task => {
      const matchesSearch = !this.searchQuery ||
        task.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(this.searchQuery.toLowerCase()));
      const matchesTag = this.filterTag === 'all' || task.tag === this.filterTag;
      return matchesSearch && matchesTag;
    });
    return {
      tasks: this.tasks,
      filteredTasks: filtered,
      loading: this.loading,
      error: this.error,
      searchQuery: this.searchQuery,
      filterTag: this.filterTag
    };
  }
  async loadTasks() {
    this.loading = true;
    this.error = null;
    this._notify();
    try {
      const data = await ApiClient.fetchTasks();
      this.tasks = data;
      this._idCounter = data.length;
      this.loading = false;
      this._notify();
    } catch (err) {
      this.loading = false;
      this.error = err.message || 'Failed to load tasks';
      this._notify();
    }
  }
  async addTask(taskData) {
    this.error = null;
    try {
      const newTask = await ApiClient.createTask(taskData);
      this.tasks.unshift(newTask);
      this._idCounter = Math.max(this._idCounter, newTask.id);
      this._notify();
      return newTask;
    } catch (err) {
      this.error = err.message || 'Failed to create task';
      this._notify();
      throw err;
    }
  }
  async updateTask(id, updates) {
    this.error = null;
    try {
      const updated = await ApiClient.updateTask(id, updates);
      const idx = this.tasks.findIndex(t => t.id === id);
      if (idx !== -1) this.tasks[idx] = updated;
      this._notify();
      return updated;
    } catch (err) {
      this.error = err.message || 'Failed to update task';
      this._notify();
      throw err;
    }
  }
  async moveTask(id, newStatus) {
    return this.updateTask(id, { status: newStatus });
  }
  setSearchQuery(q) {
    this.searchQuery = q;
    this._notify();
  }
  setFilterTag(tag) {
    this.filterTag = tag;
    this._notify();
  }
}
/* ===== API CLIENT ===== */
const API_BASE = 'https://jsonplaceholder.typicode.com';
class ApiClient {
  static async fetchTasks() {
    // Simulate realistic delay
    await new Promise(r => setTimeout(r, 600 + Math.random() * 400));
    // Use JSONPlaceholder for realistic data shape, then transform
    const res = await fetch(`${API_BASE}/todos?_limit=12`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return data.map((item, i) => ApiClient._transformTodo(item, i));
  }
  static async createTask(taskData) {
    await new Promise(r => setTimeout(r, 300 + Math.random() * 200));
    const res = await fetch(`${API_BASE}/todos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: taskData.title, completed: false, userId: 1 })
    });
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    const data = await res.json();
    return {
      id: data.id,
      title: taskData.title,
      description: taskData.description || '',
      tag: taskData.tag || 'feature',
      priority: taskData.priority || 'medium',
      status: taskData.status || 'todo',
      assignee: taskData.assignee || '',
      createdAt: new Date().toISOString()
    };
  }
  static async updateTask(id, updates) {
    await new Promise(r => setTimeout(r, 200 + Math.random() * 150));
    const res = await fetch(`${API_BASE}/todos/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: updates.title })
    });
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return { id, ...updates };
  }
  static _transformTodo(todo, index) {
    const tags = ['feature', 'bug', 'improvement', 'docs'];
    const priorities = ['high', 'medium', 'low'];
    const statuses = ['todo', 'in-progress', 'review', 'done'];
    const assignees = ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', ''];
    const descriptions = [
      'Implement the core functionality with proper error handling',
      'Fix regression causing data loss on refresh',
      'Refactor the component tree for better reusability',
      'Add documentation for the new API endpoints',
      'Optimize query performance for large datasets',
      '',
      'Design the onboarding flow for new users',
      'Add unit tests for the auth module',
      'Update color scheme to match brand guidelines',
      'Set up CI/CD pipeline with automated testing',
      'Create wireframes for the settings page',
      'Fix memory leak in the websocket connection'
    ];
    return {
      id: index + 1,
      title: todo.title.charAt(0).toUpperCase() + todo.title.slice(1),
      description: descriptions[index % descriptions.length],
      tag: tags[index % tags.length],
      priority: priorities[index % priorities.length],
      status: statuses[index % statuses.length],
      assignee: assignees[index % assignees.length],
      createdAt: new Date(Date.now() - Math.random() * 7 * 86400000).toISOString()
    };
  }
}
/* ===== TOAST SYSTEM ===== */
class ToastManager {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
  }
  show(message, type = 'info', duration = 3000) {
    const el = document.createElement('div');
    el.className = `toast ${type}`;
    el.textContent = message;
    this.container.appendChild(el);
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px) scale(0.9)';
      el.style.transition = 'all 300ms ease';
      setTimeout(() => el.remove(), 300);
    }, duration);
  }
}
/* ===== MAIN APP ===== */
class TaskBoardApp {
  constructor() {
    this.store = new TaskStore();
    this.toast = new ToastManager('toastContainer');
    this.editingTaskId = null;
    this._init();
  }
  _init() {
    this._cacheDOM();
    this._bindEvents();
    this.store.subscribe(state => this._render(state));
    this._loadInitialData();
  }
  _cacheDOM() {
    this.columns = {
      todo: document.getElementById('column-todo'),
      'in-progress': document.getElementById('column-in-progress'),
      review: document.getElementById('column-review'),
      done: document.getElementById('column-done')
    };
    this.countEls = {
      todo: document.getElementById('count-todo'),
      'in-progress': document.getElementById('count-in-progress'),
      review: document.getElementById('count-review'),
      done: document.getElementById('count-done')
    };
    this.totalCount = document.getElementById('totalCount');
    this.searchInput = document.getElementById('searchInput');
    this.filterBtns = document.querySelectorAll('.filter-btn');
    this.addBtn = document.getElementById('addTaskBtn');
    this.modalOverlay = document.getElementById('modalOverlay');
    this.modalClose = document.getElementById('modalClose');
    this.modalCancel = document.getElementById('modalCancel');
    this.modalTitle = document.getElementById('modalTitle');
    this.modalSubmit = document.getElementById('modalSubmit');
    this.taskForm = document.getElementById('taskForm');
    this.fTitle = document.getElementById('taskTitle');
    this.fDescription = document.getElementById('taskDescription');
    this.fTag = document.getElementById('taskTag');
    this.fPriority = document.getElementById('taskPriority');
    this.fAssignee = document.getElementById('taskAssignee');
    this.fStatus = document.getElementById('taskStatus');
  }
  _bindEvents() {
    this.searchInput.addEventListener('input', (e) => {
      this.store.setSearchQuery(e.target.value);
    });
    this.filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        this.filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.store.setFilterTag(btn.dataset.filter);
      });
    });
    this.addBtn.addEventListener('click', () => this._openModal());
    this.modalClose.addEventListener('click', () => this._closeModal());
    this.modalCancel.addEventListener('click', () => this._closeModal());
    this.modalOverlay.addEventListener('click', (e) => {
      if (e.target === this.modalOverlay) this._closeModal();
    });
    this.taskForm.addEventListener('submit', (e) => {
      e.preventDefault();
      this._handleFormSubmit();
    });
  }
  async _loadInitialData() {
    this.store.loadTasks().catch(() => {});
  }
  _openModal(task = null) {
    this.editingTaskId = task ? task.id : null;
    this.modalTitle.textContent = task ? 'Edit Task' : 'New Task';
    this.modalSubmit.textContent = task ? 'Update' : 'Create';
    if (task) {
      this.fTitle.value = task.title;
      this.fDescription.value = task.description || '';
      this.fTag.value = task.tag;
      this.fPriority.value = task.priority;
      this.fAssignee.value = task.assignee || '';
      this.fStatus.value = task.status;
    } else {
      this.taskForm.reset();
      this.fStatus.value = 'todo';
    }
    this.modalOverlay.classList.add('open');
    this.fTitle.focus();
  }
  _closeModal() {
    this.modalOverlay.classList.remove('open');
    this.editingTaskId = null;
  }
  async _handleFormSubmit() {
    const data = {
      title: this.fTitle.value.trim(),
      description: this.fDescription.value.trim(),
      tag: this.fTag.value,
      priority: this.fPriority.value,
      assignee: this.fAssignee.value.trim(),
      status: this.fStatus.value
    };
    if (!data.title) return;
    try {
      if (this.editingTaskId) {
        await this.store.updateTask(this.editingTaskId, data);
        this.toast.show('Task updated', 'success');
      } else {
        await this.store.addTask(data);
        this.toast.show('Task created', 'success');
      }
      this._closeModal();
    } catch (err) {
      this.toast.show(err.message || 'Operation failed', 'error');
    }
  }
  _render(state) {
    if (state.loading) {
      this._renderLoading();
      return;
    }
    if (state.error) {
      this._renderError(state.error);
      return;
    }
    this._renderBoard(state);
    this._updateCounts(state);
  }
  _renderLoading() {
    Object.values(this.columns).forEach(col => {
      col.innerHTML = '';
      for (let i = 0; i < 3; i++) {
        const skel = document.createElement('div');
        skel.className = 'skeleton-card';
        skel.innerHTML = `
          <div class="skeleton-tag"></div>
          <div class="skeleton-line"></div>
          <div class="skeleton-line"></div>
          <div class="skeleton-line" style="width:40%"></div>
        `;
        col.appendChild(skel);
      }
    });
    this.totalCount.textContent = 'loading...';
  }
  _renderError(errorMsg) {
    Object.values(this.columns).forEach(col => { col.innerHTML = ''; });
    const board = document.getElementById('board');
    const errDiv = document.createElement('div');
    errDiv.className = 'error-state';
    errDiv.innerHTML = `
      <div class="error-icon">&#x26A0;</div>
      <p>${errorMsg}</p>
      <button class="error-retry" onclick="app.store.loadTasks()">Retry</button>
    `;
    board.prepend(errDiv);
    this.totalCount.textContent = 'error';
  }
  _renderBoard(state) {
    // Clear existing error/empty states
    document.querySelectorAll('.error-state, .empty-state').forEach(el => el.remove());
    Object.values(this.columns).forEach(col => { col.innerHTML = ''; });
    const { filteredTasks } = state;
    if (filteredTasks.length === 0) {
      this._renderEmpty();
      return;
    }
    filteredTasks.forEach((task, index) => {
      const card = this._createCard(task, index);
      const targetCol = this.columns[task.status];
      if (targetCol) {
        targetCol.appendChild(card);
      }
    });
    this._setupDragAndDrop();
  }
  _renderEmpty() {
    const board = document.getElementById('board');
    const emptyDiv = document.createElement('div');
    emptyDiv.className = 'empty-state';
    emptyDiv.innerHTML = `
      <div class="empty-icon">&#x1F4CB;</div>
      <p>No tasks match your search or filter</p>
    `;
    board.prepend(emptyDiv);
  }
  _createCard(task, index) {
    const card = document.createElement('div');
    card.className = 'task-card';
    card.dataset.id = task.id;
    card.draggable = true;
    card.style.animationDelay = `${Math.min(index * 30, 500)}ms`;
    const tagLabel = task.tag.charAt(0).toUpperCase() + task.tag.slice(1);
    const initials = task.assignee ? task.assignee.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase() : '?';
    card.innerHTML = `
      <span class="task-tag tag-${task.tag}">${tagLabel}</span>
      <h3>${task.title}</h3>
      ${task.description ? `<p>${task.description}</p>` : ''}
      <div class="task-meta">
        <span class="task-priority priority-${task.priority}">${task.priority}</span>
        <span class="task-assignee">
          <span class="task-avatar">${initials}</span>
          ${task.assignee || 'Unassigned'}
        </span>
      </div>
    `;
    card.addEventListener('click', () => this._openModal(task));
    card.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('text/plain', task.id);
      card.classList.add('dragging');
    });
    card.addEventListener('dragend', () => {
      card.classList.remove('dragging');
      document.querySelectorAll('.column').forEach(c => c.classList.remove('drag-over'));
    });
    return card;
  }
  _setupDragAndDrop() {
    document.querySelectorAll('.column-body').forEach(col => {
      col.addEventListener('dragover', (e) => {
        e.preventDefault();
        col.closest('.column').classList.add('drag-over');
      });
      col.addEventListener('dragleave', () => {
        col.closest('.column').classList.remove('drag-over');
      });
      col.addEventListener('drop', (e) => {
        e.preventDefault();
        const colEl = col.closest('.column');
        colEl.classList.remove('drag-over');
        const taskId = parseInt(e.dataTransfer.getData('text/plain'));
        const newStatus = colEl.dataset.status;
        if (!taskId || !newStatus) return;
        const task = this.store.tasks.find(t => t.id === taskId);
        if (task && task.status !== newStatus) {
          this.store.moveTask(taskId, newStatus);
          this.toast.show(`Moved to ${newStatus}`, 'info');
        }
      });
    });
  }
  _updateCounts(state) {
    const statuses = ['todo', 'in-progress', 'review', 'done'];
    statuses.forEach(s => {
      const count = state.tasks.filter(t => t.status === s).length;
      if (this.countEls[s]) this.countEls[s].textContent = count;
    });
    this.totalCount.textContent = `${state.tasks.length} tasks`;
  }
}
/* ===== BOOT ===== */
document.addEventListener('DOMContentLoaded', () => {
  window.app = new TaskBoardApp();
});
</script>
</body>
</html>
```