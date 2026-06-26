<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Project Dashboard</title>
<style>
:root {
  --primary: #6366f1;
  --primary-hover: #4f46e5;
  --primary-light: #eef2ff;
  --surface: #ffffff;
  --surface-alt: #f8fafc;
  --border: #e2e8f0;
  --text: #0f172a;
  --text-secondary: #64748b;
  --text-muted: #94a3b8;
  --success: #22c55e;
  --error: #ef4444;
  --warning: #f59e0b;
  --radius: 12px;
  --radius-sm: 8px;
  --shadow: 0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,.08), 0 2px 4px -2px rgba(0,0,0,.06);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,.1), 0 4px 6px -4px rgba(0,0,0,.06);
  --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --transition: 200ms cubic-bezier(.4,0,.2,1);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--font);
  background: var(--surface-alt);
  color: var(--text);
  line-height: 1.6;
  min-height: 100vh;
}
.app-header {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 16px 24px;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(8px);
  background: rgba(255,255,255,.92);
}
.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
.app-title {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -.02em;
  display: flex;
  align-items: center;
  gap: 10px;
}
.app-title svg { flex-shrink: 0; }
.header-actions { display: flex; align-items: center; gap: 12px; }
.search-wrapper {
  position: relative;
  width: 280px;
}
.search-wrapper svg {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}
.search-input {
  width: 100%;
  padding: 9px 12px 9px 38px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-family: var(--font);
  background: var(--surface-alt);
  transition: border-color var(--transition), box-shadow var(--transition);
  outline: none;
}
.search-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(99,102,241,.15);
}
.search-input::placeholder { color: var(--text-muted); }
.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 18px;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 600;
  font-family: var(--font);
  cursor: pointer;
  transition: background var(--transition), transform var(--transition), box-shadow var(--transition);
}
.btn:active { transform: scale(.97); }
.btn-primary {
  background: var(--primary);
  color: #fff;
}
.btn-primary:hover { background: var(--primary-hover); box-shadow: var(--shadow-md); }
.btn-secondary {
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
}
.btn-secondary:hover { background: var(--surface-alt); border-color: var(--text-muted); }
.btn-icon {
  padding: 8px;
  border: 1px solid var(--border);
  background: var(--surface);
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--transition), border-color var(--transition);
}
.btn-icon:hover { background: var(--surface-alt); border-color: var(--text-muted); }
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}
.stats-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow);
  transition: box-shadow var(--transition), transform var(--transition);
}
.stat-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}
.stat-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 4px;
}
.stat-value {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -.03em;
}
.stat-trend {
  font-size: 12px;
  font-weight: 600;
  margin-top: 4px;
}
.stat-trend.up { color: var(--success); }
.stat-trend.down { color: var(--error); }
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.section-title {
  font-size: 18px;
  font-weight: 700;
}
.section-actions { display: flex; gap: 8px; }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow);
  transition: box-shadow var(--transition), transform var(--transition);
}
.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
.card-header {
  padding: 16px 16px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.card-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 100px;
  text-transform: uppercase;
  letter-spacing: .04em;
}
.badge-active { background: #dcfce7; color: #166534; }
.badge-draft { background: #fef9c3; color: #854d0e; }
.badge-archived { background: #f1f5f9; color: #475569; }
.card-body { padding: 12px 16px 16px; }
.card-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.card-desc {
  font-size: 13px;
  color: var(--text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 12px;
  line-height: 1.5;
}
.card-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: var(--text-muted);
}
.card-meta svg { flex-shrink: 0; }
.card-meta span { display: flex; align-items: center; gap: 4px; }
.card-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
.card-footer .btn {
  padding: 6px 14px;
  font-size: 13px;
}
.skeleton {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
}
.skeleton-line {
  height: 14px;
  background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 12px;
}
.skeleton-line:last-child { width: 60%; }
.skeleton-line:nth-child(2) { width: 85%; }
.skeleton-line:nth-child(3) { width: 45%; }
.skeleton-block {
  height: 120px;
  background: linear-gradient(90deg, #e2e8f0 25%, #f1f5f9 50%, #e2e8f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
  margin-bottom: 12px;
}
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
.empty-state {
  text-align: center;
  padding: 48px 24px;
  grid-column: 1 / -1;
}
.empty-state svg { margin-bottom: 16px; opacity: .4; }
.empty-state h3 { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
.empty-state p { color: var(--text-secondary); font-size: 14px; margin-bottom: 20px; }
.error-state {
  text-align: center;
  padding: 40px 24px;
  grid-column: 1 / -1;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: var(--radius);
}
.error-state h3 { color: var(--error); font-size: 18px; font-weight: 600; margin-bottom: 8px; }
.error-state p { color: #7f1d1d; font-size: 14px; margin-bottom: 16px; }
.error-state .btn { background: var(--error); color: #fff; }
.error-state .btn:hover { background: #dc2626; }
.toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 200;
}
.toast {
  padding: 12px 20px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 500;
  box-shadow: var(--shadow-lg);
  animation: slideIn .3s ease-out;
  display: flex;
  align-items: center;
  gap: 8px;
}
.toast-success { background: #166534; color: #fff; }
.toast-error { background: #991b1b; color: #fff; }
@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
.view-toggle { display: flex; border: 1px solid var(--border); border-radius: var(--radius-sm); overflow: hidden; }
.view-toggle button {
  padding: 7px 12px;
  border: none;
  background: var(--surface);
  cursor: pointer;
  font-family: var(--font);
  font-size: 13px;
  transition: background var(--transition), color var(--transition);
  display: flex; align-items: center; gap: 4px;
}
.view-toggle button.active { background: var(--primary); color: #fff; }
.view-toggle button:not(.active):hover { background: var(--surface-alt); }
@media (max-width: 768px) {
  .header-inner { flex-wrap: wrap; }
  .search-wrapper { width: 100%; order: 3; }
  .stats-bar { grid-template-columns: repeat(2, 1fr); }
  .grid { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
  .stats-bar { grid-template-columns: 1fr; }
  .app-title { font-size: 17px; }
  .main-content { padding: 16px; }
}
</style>
</head>
<body>
<header class="app-header">
  <div class="header-inner">
    <div class="app-title">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>
      Project Dashboard
    </div>
    <div class="header-actions">
      <div class="search-wrapper">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input class="search-input" type="text" id="searchInput" placeholder="Search projects..." autocomplete="off">
      </div>
      <div class="view-toggle" id="viewToggle">
        <button data-view="grid" class="active" title="Grid view">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
          Grid
        </button>
        <button data-view="list" title="List view">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
          List
        </button>
      </div>
      <button class="btn btn-primary" id="refreshBtn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>
        Refresh
      </button>
    </div>
  </div>
</header>
<main class="main-content">
  <div class="stats-bar" id="statsBar">
    <div class="stat-card"><div class="stat-label">Total Projects</div><div class="stat-value" id="statTotal">--</div><div class="stat-trend up" id="statTotalTrend">+12%</div></div>
    <div class="stat-card"><div class="stat-label">Active</div><div class="stat-value" id="statActive">--</div><div class="stat-trend up" id="statActiveTrend">+3</div></div>
    <div class="stat-card"><div class="stat-label">Completed</div><div class="stat-value" id="statCompleted">--</div><div class="stat-trend up" id="statCompletedTrend">+8%</div></div>
    <div class="stat-card"><div class="stat-label">Overdue</div><div class="stat-value" id="statOverdue">--</div><div class="stat-trend down" id="statOverdueTrend">-2</div></div>
  </div>
  <div class="section-header">
    <h2 class="section-title" id="sectionTitle">All Projects</h2>
    <div class="section-actions">
      <button class="btn btn-secondary" id="filterActiveBtn">Active</button>
      <button class="btn btn-secondary" id="filterAllBtn">All</button>
    </div>
  </div>
  <div class="grid" id="projectGrid"></div>
</main>
<div class="toast-container" id="toastContainer"></div>
<script>
(() => {
  'use strict';
  const API_BASE = 'https://jsonplaceholder.typicode.com';
  const MAX_RETRIES = 2;
  const RETRY_DELAY = 1000;
  const store = {
    _projects: [],
    _filtered: [],
    _filter: 'all',
    _search: '',
    _view: 'grid',
    _loading: false,
    _error: null,
    get projects() { return this._filtered; },
    set projects(v) { this._projects = v; this._applyFilters(); },
    set filter(v) { this._filter = v; this._applyFilters(); },
    get filter() { return this._filter; },
    set search(v) { this._search = v.toLowerCase(); this._applyFilters(); },
    set view(v) { this._view = v; },
    get view() { return this._view; },
    set loading(v) { this._loading = v; },
    get loading() { return this._loading; },
    set error(v) { this._error = v; },
    get error() { return this._error; },
    _applyFilters() {
      let list = this._projects;
      if (this._filter === 'active') {
        list = list.filter(p => p.status === 'active');
      }
      if (this._search) {
        list = list.filter(p =>
          p.title.toLowerCase().includes(this._search) ||
          (p.body && p.body.toLowerCase().includes(this._search))
        );
      }
      this._filtered = list;
    }
  };
  function buildStatus(id) {
    const idx = id % 3;
    if (idx === 0) return { label: 'Active', cls: 'badge-active' };
    if (idx === 1) return { label: 'Draft', cls: 'badge-draft' };
    return { label: 'Archived', cls: 'badge-archived' };
  }
  function buildMeta(id) {
    return {
      tasks: (id % 7) + 3,
      comments: (id * 3) % 13,
      date: new Date(Date.now() - id * 86400000).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    };
  }
  function fetchWithRetry(url, retries = MAX_RETRIES) {
    return fetch(url)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .catch(err => {
        if (retries > 0) {
          return new Promise(resolve => setTimeout(resolve, RETRY_DELAY))
            .then(() => fetchWithRetry(url, retries - 1));
        }
        throw err;
      });
  }
  function createCardHTML(project) {
    const status = buildStatus(project.id);
    const meta = buildMeta(project.id);
    const title = project.title.charAt(0).toUpperCase() + project.title.slice(1);
    const desc = project.body ? project.body.split('\n')[0] : 'No description available.';
    return `
      <div class="card" data-id="${project.id}">
        <div class="card-header">
          <span class="card-badge ${status.cls}">${status.label}</span>
          <button class="btn-icon card-fav" data-id="${project.id}" title="Bookmark">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
          </button>
        </div>
        <div class="card-body">
          <div class="card-title" title="${title}">${title}</div>
          <div class="card-desc">${desc}</div>
          <div class="card-meta">
            <span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
              ${meta.tasks} tasks
            </span>
            <span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              ${meta.comments}
            </span>
            <span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              ${meta.date}
            </span>
          </div>
        </div>
        <div class="card-footer">
          <button class="btn btn-secondary card-edit" data-id="${project.id}">Edit</button>
          <button class="btn btn-primary card-view" data-id="${project.id}">View</button>
        </div>
      </div>`;
  }
  function createListRowHTML(project) {
    const status = buildStatus(project.id);
    const meta = buildMeta(project.id);
    const title = project.title.charAt(0).toUpperCase() + project.title.slice(1);
    return `
      <div class="card" data-id="${project.id}" style="display:flex;align-items:center;padding:12px 16px;gap:16px;">
        <span class="card-badge ${status.cls}" style="flex-shrink:0;">${status.label}</span>
        <div style="flex:1;min-width:0;">
          <div class="card-title" style="margin:0;">${title}</div>
        </div>
        <div style="display:flex;gap:16px;font-size:12px;color:var(--text-muted);flex-shrink:0;">
          <span>${meta.tasks} tasks</span>
          <span>${meta.comments} comments</span>
          <span>${meta.date}</span>
        </div>
        <div style="display:flex;gap:6px;flex-shrink:0;">
          <button class="btn btn-secondary card-edit" data-id="${project.id}" style="padding:4px 10px;font-size:12px;">Edit</button>
          <button class="btn btn-primary card-view" data-id="${project.id}" style="padding:4px 10px;font-size:12px;">View</button>
        </div>
      </div>`;
  }
  function createSkeletons(count = 6) {
    return Array.from({ length: count }, () => `
      <div class="skeleton">
        <div class="skeleton-block"></div>
        <div class="skeleton-line"></div>
        <div class="skeleton-line"></div>
        <div class="skeleton-line"></div>
      </div>`).join('');
  }
  function createEmptyHTML() {
    return `
      <div class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg>
        <h3>No projects found</h3>
        <p>${store._search ? 'No results match your search. Try a different term.' : 'No projects match the current filter.'}</p>
      </div>`;
  }
  function createErrorHTML(errMsg) {
    return `
      <div class="error-state">
        <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="var(--error)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <h3>Failed to load projects</h3>
        <p>${errMsg || 'An unexpected error occurred. Please try again.'}</p>
        <button class="btn" id="retryBtn">Retry</button>
      </div>`;
  }
  function updateStats() {
    const all = store._projects;
    document.getElementById('statTotal').textContent = all.length;
    document.getElementById('statActive').textContent = all.filter(p => p.id % 3 === 0).length;
    document.getElementById('statCompleted').textContent = all.filter(p => p.id % 3 === 2).length;
    document.getElementById('statOverdue').textContent = all.filter(p => p.id % 3 === 1).length;
  }
  function render() {
    const grid = document.getElementById('projectGrid');
    if (store._loading) {
      grid.innerHTML = createSkeletons();
      return;
    }
    if (store._error) {
      grid.innerHTML = createErrorHTML(store._error);
      document.getElementById('retryBtn')?.addEventListener('click', loadProjects);
      return;
    }
    const items = store.projects;
    if (items.length === 0) {
      grid.innerHTML = createEmptyHTML();
      return;
    }
    const fn = store._view === 'list' ? createListRowHTML : createCardHTML;
    grid.innerHTML = items.map(fn).join('');
    document.querySelectorAll('.card-fav').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        const id = btn.dataset.id;
        showToast(`Bookmarked project #${id}`, 'success');
      });
    });
    document.querySelectorAll('.card-edit').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        const id = btn.dataset.id;
        showToast(`Opening project #${id} for editing`, 'success');
      });
    });
    document.querySelectorAll('.card-view').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        const id = btn.dataset.id;
        showToast(`Viewing project #${id}`, 'success');
      });
    });
  }
  function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(100%)'; toast.style.transition = 'var(--transition)'; }, 3000);
    setTimeout(() => toast.remove(), 3500);
  }
  function loadProjects() {
    store._loading = true;
    store._error = null;
    render();
    fetchWithRetry(`${API_BASE}/posts`)
      .then(data => {
        const projects = data.slice(0, 12).map(item => ({
          ...item,
          title: item.title.length > 50 ? item.title.slice(0, 47) + '...' : item.title
        }));
        store.projects = projects;
        store._loading = false;
        store._error = null;
        updateStats();
        render();
        showToast('Projects loaded successfully', 'success');
      })
      .catch(err => {
        store._loading = false;
        store._error = err.message || 'Network error';
        render();
        showToast('Failed to load projects', 'error');
      });
  }
  document.getElementById('searchInput').addEventListener('input', e => {
    store.search = e.target.value;
    render();
  });
  document.getElementById('filterActiveBtn').addEventListener('click', () => {
    store.filter = 'active';
    document.getElementById('sectionTitle').textContent = 'Active Projects';
    render();
  });
  document.getElementById('filterAllBtn').addEventListener('click', () => {
    store.filter = 'all';
    document.getElementById('sectionTitle').textContent = 'All Projects';
    render();
  });
  document.getElementById('refreshBtn').addEventListener('click', loadProjects);
  document.querySelectorAll('#viewToggle button').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#viewToggle button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      store.view = btn.dataset.view;
      render();
    });
  });
  loadProjects();
})();
</script>
</body>
</html>