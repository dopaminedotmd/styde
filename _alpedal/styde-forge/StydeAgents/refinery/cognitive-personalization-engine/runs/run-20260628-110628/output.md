```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cognitive Personalization Engine</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui,-apple-system,sans-serif}
:root{--bg:#f8fafc;--surface:#fff;--surface2:#f1f5f9;--border:#e2e8f0;--text:#0f172a;--text2:#475569;--accent:#6366f1;--accent-light:#eef2ff;--danger:#ef4444;--success:#22c55e;--radius:8px;--shadow:0 1px 3px rgba(0,0,0,.08);--density:1}
[data-theme=dark]{--bg:#0f172a;--surface:#1e293b;--surface2:#334155;--border:#475569;--text:#f1f5f9;--text2:#94a3b8;--accent-light:#1e1b4b;--shadow:0 1px 3px rgba(0,0,0,.3)}
[data-density=compact]{--density:.75}
[data-density=spacious]{--density:1.5}
body{background:var(--bg);color:var(--text);min-height:100vh;font-size:calc(14px * var(--density))}
.app-bar{background:var(--surface);border-bottom:1px solid var(--border);padding:12px 24px;display:flex;align-items:center;gap:16px;flex-wrap:wrap;box-shadow:var(--shadow)}
.app-bar h1{font-size:calc(18px * var(--density));font-weight:700;background:linear-gradient(135deg,var(--accent),#a855f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.profile-selector{display:flex;align-items:center;gap:8px;margin-left:auto}
.profile-selector select{padding:6px 12px;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);color:var(--text);font-size:calc(13px * var(--density))}
.btn{padding:6px 14px;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);color:var(--text);cursor:pointer;font-size:calc(13px * var(--density))}
.btn:hover{background:var(--surface2)}
.btn-primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.btn-primary:hover{opacity:.9}
.btn-sm{padding:4px 10px;font-size:calc(12px * var(--density))}
.btn-danger{background:var(--danger);color:#fff;border-color:var(--danger)}
.btn-outline{background:transparent;border:1px solid var(--border);color:var(--text)}
.dashboard{padding:20px 24px;display:grid;grid-template-columns:280px 1fr;gap:20px;max-width:1600px;margin:0 auto}
.sidebar{background:var(--surface);border-radius:var(--radius);padding:16px;box-shadow:var(--shadow);height:fit-content}
.sidebar h3{font-size:calc(13px * var(--density));text-transform:uppercase;letter-spacing:.5px;color:var(--text2);margin-bottom:12px;margin-top:16px}
.sidebar h3:first-child{margin-top:0}
.main-area{display:flex;flex-direction:column;gap:20px}
.toolbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;background:var(--surface);padding:12px 16px;border-radius:var(--radius);box-shadow:var(--shadow)}
.toolbar-group{display:flex;gap:4px;align-items:center;margin-right:8px}
.toolbar-group label{font-size:calc(12px * var(--density));color:var(--text2);margin-right:4px}
.metrics-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
.metric-card{background:var(--surface);border-radius:var(--radius);padding:20px;box-shadow:var(--shadow);position:relative;border:1px solid transparent;transition:border-color .2s}
.metric-card:hover{border-color:var(--accent)}
.metric-card.bookmarked{border-color:var(--accent);background:var(--accent-light)}
.metric-card h4{font-size:calc(14px * var(--density));margin-bottom:4px}
.metric-card .value{font-size:calc(28px * var(--density));font-weight:700;color:var(--accent);margin-bottom:8px}
.metric-card .sub{font-size:calc(12px * var(--density));color:var(--text2)}
.metric-card .card-actions{position:absolute;top:12px;right:12px;display:flex;gap:4px}
.metric-card .card-actions button{opacity:0;transition:opacity .2s}
.metric-card:hover .card-actions button{opacity:1}
.metric-card .badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:calc(11px * var(--density));margin-top:8px}
.badge-warn{background:#fef3c7;color:#92400e}
.badge-ok{background:#dcfce7;color:#166534}
.badge-critical{background:#fee2e2;color:#991b1b}
[data-theme=dark] .badge-warn{background:#451a03;color:#fbbf24}
[data-theme=dark] .badge-ok{background:#052e16;color:#4ade80}
[data-theme=dark] .badge-critical{background:#450a0a;color:#f87171}
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;z-index:1000}
.modal{background:var(--surface);border-radius:12px;padding:24px;width:90%;max-width:520px;max-height:80vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,.2)}
.modal h2{font-size:calc(18px * var(--density));margin-bottom:16px}
.modal label{display:block;font-size:calc(13px * var(--density));color:var(--text2);margin-bottom:4px;margin-top:12px}
.modal label:first-child{margin-top:0}
.modal input[type=text],.modal input[type=number],.modal select{width:100%;padding:8px 12px;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);color:var(--text);font-size:calc(14px * var(--density));margin-bottom:4px}
.modal input[type=color]{width:48px;height:36px;border:1px solid var(--border);border-radius:var(--radius);padding:2px;cursor:pointer}
.modal .modal-actions{display:flex;gap:8px;justify-content:flex-end;margin-top:20px}
.theme-preview{display:flex;gap:8px;align-items:center;margin-top:12px}
.theme-swatch{width:24px;height:24px;border-radius:50%;border:2px solid var(--border);cursor:pointer}
.theme-swatch.active{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent)}
.saved-view-item{padding:8px 10px;border-radius:6px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;font-size:calc(13px * var(--density));margin-bottom:4px}
.saved-view-item:hover{background:var(--surface2)}
.saved-view-item.active{background:var(--accent-light);color:var(--accent);font-weight:600}
.hidden{display:none!important}
.tab-bar{display:flex;gap:2px;background:var(--surface2);padding:3px;border-radius:var(--radius);margin-bottom:12px}
.tab{flex:1;text-align:center;padding:6px 0;border-radius:6px;font-size:calc(12px * var(--density));cursor:pointer;color:var(--text2);transition:all .2s}
.tab.active{background:var(--surface);color:var(--text);font-weight:600;box-shadow:var(--shadow)}
.sidebar-content .tab-panel{padding:4px 0}
.bookmark-item{padding:8px 10px;border-radius:6px;cursor:pointer;font-size:calc(13px * var(--density));margin-bottom:4px;display:flex;align-items:center;justify-content:space-between}
.bookmark-item:hover{background:var(--surface2)}
.bookmark-item .bm-title{display:flex;flex-direction:column}
.bookmark-item .bm-title small{font-size:calc(11px * var(--density));color:var(--text2)}
.density-btns{display:flex;gap:4px}
.density-btns .btn{padding:4px 8px;font-size:calc(11px * var(--density))}
@media(max-width:900px){.dashboard{grid-template-columns:1fr}.sidebar{order:2}}
.empty-state{text-align:center;padding:40px;color:var(--text2);font-size:calc(14px * var(--density))}
</style>
</head>
<body>
<div class="app-bar">
  <h1>Cognitive Personalization Engine</h1>
  <div class="profile-selector">
    <label style="font-size:calc(13px * var(--density));color:var(--text2)">Profile:</label>
    <select id="profileSelect"></select>
    <button class="btn btn-sm" onclick="openModal('profile')">+ New</button>
    <button class="btn btn-sm btn-danger" onclick="deleteProfile()">Del</button>
  </div>
</div>
<div class="dashboard">
  <div class="sidebar">
    <div class="tab-bar" id="sidebarTabs">
      <div class="tab active" data-tab="views">Views</div>
      <div class="tab" data-tab="bookmarks">Bookmarks</div>
      <div class="tab" data-tab="alerts">Alerts</div>
      <div class="tab" data-tab="theme">Theme</div>
    </div>
    <div class="sidebar-content">
      <div class="tab-panel" id="panel-views">
        <button class="btn btn-sm btn-primary" onclick="openModal('saveview')" style="width:100%;margin-bottom:8px">Save Current View</button>
        <div id="viewsList"></div>
      </div>
      <div class="tab-panel hidden" id="panel-bookmarks">
        <div id="bookmarksList"></div>
        <div class="empty-state" id="emptyBookmarks">No bookmarks yet.<br>Click the bookmark icon on any metric card.</div>
      </div>
      <div class="tab-panel hidden" id="panel-alerts">
        <button class="btn btn-sm btn-primary" onclick="openModal('alert')" style="width:100%;margin-bottom:8px">+ New Alert</button>
        <div id="alertsList"></div>
        <div class="empty-state" id="emptyAlerts">No alerts configured.</div>
      </div>
      <div class="tab-panel hidden" id="panel-theme">
        <h3>Mode</h3>
        <select id="themeMode" onchange="updateTheme()" style="width:100%;padding:6px;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);color:var(--text);font-size:calc(13px * var(--density));margin-bottom:12px">
          <option value="light">Light</option>
          <option value="dark">Dark</option>
        </select>
        <h3>Accent Color</h3>
        <input type="color" id="accentColor" value="#6366f1" onchange="updateTheme()" style="width:100%;height:40px;border:1px solid var(--border);border-radius:var(--radius);padding:2px;cursor:pointer;margin-bottom:12px">
        <h3>Density</h3>
        <div class="density-btns" style="margin-bottom:12px">
          <button class="btn btn-sm" onclick="setDensity('compact')">Compact</button>
          <button class="btn btn-sm btn-primary" onclick="setDensity('normal')">Normal</button>
          <button class="btn btn-sm" onclick="setDensity('spacious')">Spacious</button>
        </div>
        <h3>Font Scale</h3>
        <input type="range" id="fontScale" min=".7" max="1.6" step=".1" value="1" oninput="setFontScale(this.value)" style="width:100%;margin-bottom:8px">
        <div style="display:flex;justify-content:space-between;font-size:calc(11px * var(--density));color:var(--text2)">
          <span>0.7x</span><span>1.0x</span><span>1.6x</span>
        </div>
      </div>
    </div>
  </div>
  <div class="main-area">
    <div class="toolbar">
      <div class="toolbar-group">
        <label>View:</label>
        <select id="viewSelect" onchange="applyView(this.value)" style="padding:4px 8px;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);color:var(--text);font-size:calc(13px * var(--density))">
          <option value="default">Default</option>
        </select>
      </div>
      <div class="toolbar-group">
        <label>Filter:</label>
        <select id="metricFilter" onchange="renderMetrics()" style="padding:4px 8px;border:1px solid var(--border);border-radius:var(--radius);background:var(--surface);color:var(--text);font-size:calc(13px * var(--density))">
          <option value="all">All</option>
          <option value="critical">Critical</option>
          <option value="warn">Warning</option>
          <option value="ok">OK</option>
        </select>
      </div>
      <div style="margin-left:auto;display:flex;gap:4px">
        <button class="btn btn-sm" onclick="openModal('newuser')">New User Walkthrough</button>
      </div>
    </div>
    <div class="metrics-grid" id="metricsGrid"></div>
  </div>
</div>
<div class="modal-overlay hidden" id="modalOverlay">
  <div class="modal" id="modalContent"></div>
</div>
<script>
// ── DATA ──────────────────────────────────────────────
const DEFAULT_METRICS = [
  {id:'cpu', label:'CPU Usage', value:()=>Math.round(15+Math.random()*75), unit:'%', threshold:80, warnThreshold:60, category:'infra'},
  {id:'mem', label:'Memory', value:()=>Math.round(40+Math.random()*50), unit:'%', threshold:85, warnThreshold:65, category:'infra'},
  {id:'disk', label:'Disk I/O', value:()=>Math.round(5+Math.random()*40), unit:'MB/s', threshold:50, warnThreshold:30, category:'infra'},
  {id:'requests', label:'Requests/min', value:()=>Math.round(200+Math.random()*800), unit:'rpm', threshold:900, warnThreshold:600, category:'traffic'},
  {id:'latency', label:'P99 Latency', value:()=>(15+Math.random()*45).toFixed(1), unit:'ms', threshold:50, warnThreshold:30, category:'traffic'},
  {id:'errors', label:'Error Rate', value:()=>(Math.random()*3).toFixed(2), unit:'%', threshold:2, warnThreshold:1, category:'traffic'},
  {id:'users_active', label:'Active Users', value:()=>Math.round(800+Math.random()*1200), unit:'users', threshold:1800, warnThreshold:1400, category:'users'},
  {id:'signups', label:'Signups (24h)', value:()=>Math.round(20+Math.random()*80), unit:'users', threshold:100, warnThreshold:70, category:'users'},
  {id:'revenue', label:'Revenue (MTD)', value:()=>'$'+(12000+Math.round(Math.random()*8000)).toLocaleString(), unit:'', threshold:0, warnThreshold:0, category:'business'},
  {id:'conversion', label:'Conversion Rate', value:()=>(1.8+Math.random()*3.2).toFixed(1), unit:'%', threshold:5, warnThreshold:3.5, category:'business'},
];
const DEFAULT_ALERTS = [
  {id:'a1', metric:'cpu', operator:'>', threshold:80, enabled:true, notify:true},
  {id:'a2', metric:'errors', operator:'>', threshold:2, enabled:true, notify:true},
];
const PRESET_ACCENTS = ['#6366f1','#ec4899','#f59e0b','#10b981','#3b82f6','#8b5cf6','#ef4444'];
// ── STATE ─────────────────────────────────────────────
let state = {
  users: {},
  currentUser: 'default',
  metrics: JSON.parse(JSON.stringify(DEFAULT_METRICS)),
  sidebarTab: 'views',
  intervalId: null,
};
function loadState() {
  try {
    const raw = localStorage.getItem('cpe_state');
    if (raw) {
      const parsed = JSON.parse(raw);
      state.users = parsed.users || {};
      state.currentUser = parsed.currentUser || 'default';
    }
  } catch(e) {}
  if (!state.users['default']) {
    state.users['default'] = createDefaultUser('default');
  }
  if (!state.users[state.currentUser]) {
    state.currentUser = 'default';
  }
  ensureUserViews(state.users[state.currentUser]);
  applyUserTheme(state.users[state.currentUser]);
}
function createDefaultUser(name) {
  return {
    name: name,
    created: Date.now(),
    theme: {mode:'light', accent:'#6366f1', density:'normal', fontScale:1},
    views: [
      {id:'v_default', name:'Default View', filter:'all', visibleMetrics:['cpu','mem','disk','requests','latency','errors','users_active','signups','revenue','conversion'], layout:'grid'},
      {id:'v_infra', name:'Infrastructure', filter:'all', visibleMetrics:['cpu','mem','disk','latency','errors'], layout:'grid'},
    ],
    activeView: 'v_default',
    bookmarks: {},
    alerts: JSON.parse(JSON.stringify(DEFAULT_ALERTS)),
    usageHistory: [],
    muteSchedule: null,
  };
}
function ensureUserViews(user) {
  if (!user.views || user.views.length === 0) {
    user.views = [
      {id:'v_default', name:'Default View', filter:'all', visibleMetrics:['cpu','mem','disk','requests','latency','errors','users_active','signups','revenue','conversion'], layout:'grid'},
    ];
    user.activeView = 'v_default';
  }
  if (!user.bookmarks) user.bookmarks = {};
  if (!user.alerts) user.alerts = JSON.parse(JSON.stringify(DEFAULT_ALERTS));
  if (!user.usageHistory) user.usageHistory = [];
  if (!user.theme) user.theme = {mode:'light', accent:'#6366f1', density:'normal', fontScale:1};
}
function saveState() {
  localStorage.setItem('cpe_state', JSON.stringify({
    users: state.users,
    currentUser: state.currentUser,
  }));
}
function getCurrentUser() {
  return state.users[state.currentUser];
}
// ── THEME ─────────────────────────────────────────────
function applyUserTheme(user) {
  const t = user.theme;
  document.documentElement.setAttribute('data-theme', t.mode);
  document.documentElement.setAttribute('data-density', t.density);
  document.documentElement.style.setProperty('--accent', t.accent);
  document.documentElement.style.setProperty('--font-scale', t.fontScale);
  document.getElementById('themeMode').value = t.mode;
  document.getElementById('accentColor').value = t.accent;
  document.getElementById('fontScale').value = t.fontScale;
  document.querySelectorAll('.density-btns .btn').forEach(b => b.classList.remove('btn-primary'));
  const densityBtn = Array.from(document.querySelectorAll('.density-btns .btn')).find(b => b.textContent.toLowerCase() === t.density);
  if (densityBtn) { densityBtn.classList.add('btn-primary'); }
}
function updateTheme() {
  const user = getCurrentUser();
  user.theme.mode = document.getElementById('themeMode').value;
  user.theme.accent = document.getElementById('accentColor').value;
  applyUserTheme(user);
  saveState();
}
function setDensity(d) {
  const user = getCurrentUser();
  user.theme.density = d;
  applyUserTheme(user);
  saveState();
}
function setFontScale(v) {
  const user = getCurrentUser();
  user.theme.fontScale = parseFloat(v);
  document.documentElement.style.setProperty('--font-scale', user.theme.fontScale);
  saveState();
}
// ── PROFILE MANAGEMENT ───────────────────────────────
function renderProfileSelect() {
  const sel = document.getElementById('profileSelect');
  sel.innerHTML = '';
  Object.keys(state.users).forEach(name => {
    const opt = document.createElement('option');
    opt.value = name;
    opt.textContent = name;
    if (name === state.currentUser) opt.selected = true;
    sel.appendChild(opt);
  });
}
function switchProfile(name) {
  if (!state.users[name]) return;
  state.currentUser = name;
  ensureUserViews(state.users[name]);
  applyUserTheme(state.users[name]);
  saveState();
  renderAll();
}
document.getElementById('profileSelect').addEventListener('change', function() {
  switchProfile(this.value);
});
function deleteProfile() {
  const name = state.currentUser;
  if (Object.keys(state.users).length <= 1) { alert('Cannot delete the last profile.'); return; }
  if (!confirm('Delete profile "'+name+'" and all its data?')) return;
  delete state.users[name];
  state.currentUser = Object.keys(state.users)[0];
  saveState();
  renderAll();
}
// ── MODAL ─────────────────────────────────────────────
function openModal(type, data) {
  const overlay = document.getElementById('modalOverlay');
  const content = document.getElementById('modalContent');
  overlay.classList.remove('hidden');
  if (type === 'profile') {
    content.innerHTML = `
      <h2>New Profile</h2>
      <label>Profile Name</label>
      <input type="text" id="newProfileName" placeholder="e.g. Work, Personal">
      <div class="modal-actions">
        <button class="btn" onclick="closeModal()">Cancel</button>
        <button class="btn btn-primary" onclick="createProfile()">Create</button>
      </div>`;
    setTimeout(()=>document.getElementById('newProfileName').focus(),100);
  } else if (type === 'saveview') {
    content.innerHTML = `
      <h2>Save Current View</h2>
      <label>View Name</label>
      <input type="text" id="newViewName" placeholder="e.g. My Dashboard" value="View ${Object.keys(getCurrentUser().views).length}">
      <div class="modal-actions">
        <button class="btn" onclick="closeModal()">Cancel</button>
        <button class="btn btn-primary" onclick="saveCurrentView()">Save</button>
      </div>`;
    setTimeout(()=>document.getElementById('newViewName').select(),100);
  } else if (type === 'alert') {
    const metrics = state.metrics;
    content.innerHTML = `
      <h2>New Alert</h2>
      <label>Metric</label>
      <select id="alertMetric">${metrics.map(m=>'<option value="'+m.id+'">'+m.label+'</option>').join('')}</select>
      <label>Condition</label>
      <select id="alertOperator"><option value=">">Greater than</option><option value="<">Less than</option></select>
      <label>Threshold</label>
      <input type="number" id="alertThreshold" value="80">
      <label>Notify <input type="checkbox" id="alertNotify" checked></label>
      <div class="modal-actions">
        <button class="btn" onclick="closeModal()">Cancel</button>
        <button class="btn btn-primary" onclick="createAlert()">Create</button>
      </div>`;
  } else if (type === 'bookmark') {
    const metric = state.metrics.find(m => m.id === data);
    if (!metric) return;
    content.innerHTML = `
      <h2>Bookmark: ${metric.label}</h2>
      <label>Label</label>
      <input type="text" id="bmLabel" value="${metric.label} - ${metric.value()}${metric.unit}">
      <label>Note (optional)</label>
      <input type="text" id="bmNote" placeholder="Why this matters...">
      <div class="modal-actions">
        <button class="btn" onclick="closeModal()">Cancel</button>
        <button class="btn btn-primary" onclick="createBookmark('${metric.id}')">Save</button>
      </div>`;
  } else if (type === 'newuser') {
    content.innerHTML = `
      <h2>Welcome to Your Dashboard</h2>
      <p style="color:var(--text2);margin-bottom:16px;line-height:1.5">
        This dashboard personalizes itself as you use it.<br><br>
        <strong>Get started:</strong><br>
        1. Save your first view with the filters you like<br>
        2. Click the bookmark icon on any metric to save it<br>
        3. Set alerts for metrics you care about<br>
        4. Switch between light and dark themes<br>
        5. Create separate profiles for different contexts
      </p>
      <div class="modal-actions">
        <button class="btn btn-primary" onclick="closeModal()">Got it</button>
      </div>`;
  }
}
function closeModal() {
  document.getElementById('modalOverlay').classList.add('hidden');
}
document.getElementById('modalOverlay').addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});
function createProfile() {
  const name = document.getElementById('newProfileName').value.trim();
  if (!name) { alert('Enter a name'); return; }
  if (state.users[name]) { alert('Profile already exists'); return; }
  state.users[name] = createDefaultUser(name);
  state.currentUser = name;
  saveState();
  renderAll();
  closeModal();
}
function saveCurrentView() {
  const name = document.getElementById('newViewName').value.trim();
  if (!name) { alert('Enter a name'); return; }
  const user = getCurrentUser();
  const id = 'v_'+Date.now();
  const filter = document.getElementById('metricFilter').value;
  user.views.push({
    id, name,
    filter: filter,
    visibleMetrics: user.views[0] ? user.views[0].visibleMetrics : state.metrics.map(m=>m.id),
    layout: 'grid'
  });
  user.activeView = id;
  saveState();
  renderAll();
  closeModal();
}
function applyView(viewId) {
  const user = getCurrentUser();
  user.activeView = viewId;
  saveState();
  renderViewsList();
  renderMetrics();
}
function loadView(viewId) {
  const user = getCurrentUser();
  user.activeView = viewId;
  saveState();
  renderAll();
}
function deleteView(viewId, e) {
  e.stopPropagation();
  const user = getCurrentUser();
  user.views = user.views.filter(v => v.id !== viewId);
  if (user.activeView === viewId) {
    user.activeView = user.views[0] ? user.views[0].id : null;
  }
  saveState();
  renderAll();
}
// ── BOOKMARKS ─────────────────────────────────────────
function toggleBookmark(metricId) {
  const user = getCurrentUser();
  if (user.bookmarks[metricId]) {
    delete user.bookmarks[metricId];
  } else {
    openModal('bookmark', metricId);
    return;
  }
  saveState();
  renderAll();
}
function createBookmark(metricId) {
  const label = document.getElementById('bmLabel').value.trim();
  const note = document.getElementById('bmNote').value.trim();
  if (!label) { alert('Enter a label'); return; }
  const user = getCurrentUser();
  const metric = state.metrics.find(m => m.id === metricId);
  user.bookmarks[metricId] = {
    metricId,
    label,
    note: note || '',
    value: metric.value() + (metric.unit ? metric.unit : ''),
    timestamp: Date.now(),
  };
  saveState();
  renderAll();
  closeModal();
}
function removeBookmark(metricId, e) {
  e.stopPropagation();
  const user = getCurrentUser();
  delete user.bookmarks[metricId];
  saveState();
  renderAll();
}
// ── ALERTS ────────────────────────────────────────────
function createAlert() {
  const user = getCurrentUser();
  const metric = document.getElementById('alertMetric').value;
  const operator = document.getElementById('alertOperator').value;
  const threshold = parseFloat(document.getElementById('alertThreshold').value);
  const notify = document.getElementById('alertNotify').checked;
  user.alerts.push({
    id: 'a'+Date.now(),
    metric, operator, threshold, enabled:true, notify
  });
  saveState();
  renderAll();
  closeModal();
}
function toggleAlert(id) {
  const user = getCurrentUser();
  const alert = user.alerts.find(a => a.id === id);
  if (alert) { alert.enabled = !alert.enabled; saveState(); renderAll(); }
}
function deleteAlert(id, e) {
  e.stopPropagation();
  const user = getCurrentUser();
  user.alerts = user.alerts.filter(a => a.id !== id);
  saveState();
  renderAll();
}
// ── RENDER ────────────────────────────────────────────
function renderAll() {
  renderProfileSelect();
  renderViewsList();
  renderBookmarks();
  renderAlerts();
  renderMetrics();
  renderViewSelect();
  updateSidebarTab();
  applyUserTheme(getCurrentUser());
}
function renderViewSelect() {
  const sel = document.getElementById('viewSelect');
  const user = getCurrentUser();
  const current = sel.value;
  sel.innerHTML = '';
  user.views.forEach(v => {
    const opt = document.createElement('option');
    opt.value = v.id;
    opt.textContent = v.name;
    sel.appendChild(opt);
  });
  sel.value = user.activeView || (user.views[0] ? user.views[0].id : '');
}
function renderViewsList() {
  const container = document.getElementById('viewsList');
  const user = getCurrentUser();
  container.innerHTML = '';
  user.views.forEach(v => {
    const div = document.createElement('div');
    div.className = 'saved-view-item' + (v.id === user.activeView ? ' active' : '');
    div.innerHTML = '<span>'+v.name+'</span><button class="btn btn-sm btn-outline" onclick="deleteView(\''+v.id+'\',event)" style="font-size:calc(11px * var(--density));padding:2px 6px">&times;</button>';
    div.onclick = () => loadView(v.id);
    container.appendChild(div);
  });
}
function renderBookmarks() {
  const container = document.getElementById('bookmarksList');
  const empty = document.getElementById('emptyBookmarks');
  const user = getCurrentUser();
  const bmKeys = Object.keys(user.bookmarks);
  container.innerHTML = '';
  if (bmKeys.length === 0) { empty.classList.remove('hidden'); return; }
  empty.classList.add('hidden');
  bmKeys.forEach(k => {
    const bm = user.bookmarks[k];
    const div = document.createElement('div');
    div.className = 'bookmark-item';
    div.innerHTML ='<div class="bm-title"><span>'+bm.label+'</span><small>'+bm.value+(bm.note?' - '+bm.note:'')+'</small></div><button class="btn btn-sm btn-outline" onclick="removeBookmark(\''+k+'\',event)" style="font-size:calc(11px * var(--density));padding:2px 6px">&times;</button>';
    container.appendChild(div);
  });
}
function renderAlerts() {
  const container = document.getElementById('alertsList');
  const empty = document.getElementById('emptyAlerts');
  const user = getCurrentUser();
  container.innerHTML = '';
  if (user.alerts.length === 0) { empty.classList.remove('hidden'); return; }
  empty.classList.add('hidden');
  user.alerts.forEach(a => {
    const metric = state.metrics.find(m => m.id === a.metric);
    const div = document.createElement('div');
    div.className = 'saved-view-item';
    div.innerHTML = '<span style="display:flex;align-items:center;gap:8px"><input type="checkbox" '+(a.enabled?'checked':'')+' onchange="toggleAlert(\''+a.id+'\')"> <span style="font-size:calc(13px * var(--density))">'+(metric?metric.label:a.metric)+' '+a.operator+' '+a.threshold+'</span></span><button class="btn btn-sm btn-outline" onclick="deleteAlert(\''+a.id+'\',event)" style="font-size:calc(11px * var(--density));padding:2px 6px">&times;</button>';
    container.appendChild(div);
  });
}
function renderMetrics() {
  const grid = document.getElementById('metricsGrid');
  const user = getCurrentUser();
  const filter = document.getElementById('metricFilter').value;
  const activeView = user.views.find(v => v.id === user.activeView);
  let visibleIds = activeView ? activeView.visibleMetrics : state.metrics.map(m=>m.id);
  let metrics = state.metrics.filter(m => visibleIds.includes(m.id));
  grid.innerHTML = '';
  metrics.forEach(m => {
    const val = m.value();
    const numVal = parseFloat(val);
    const isBookmarked = !!user.bookmarks[m.id];
    let status = 'ok';
    let badgeText = 'OK';
    let badgeClass = 'badge-ok';
    const alertDef = user.alerts.find(a => a.metric === m.id && a.enabled);
    if (alertDef) {
      if (alertDef.operator === '>' && numVal > alertDef.threshold) { status = 'critical'; badgeText = 'CRITICAL'; badgeClass = 'badge-critical'; }
      else if (alertDef.operator === '<' && numVal < alertDef.threshold) { status = 'critical'; badgeText = 'CRITICAL'; badgeClass = 'badge-critical'; }
    }
    if (status === 'ok' && m.warnThreshold && numVal > m.warnThreshold) { status = 'warn'; badgeText = 'WARNING'; badgeClass = 'badge-warn'; }
    if (status === 'ok' && m.threshold && numVal > m.threshold) { status = 'critical'; badgeText = 'CRITICAL'; badgeClass = 'badge-critical'; }
    if (filter !== 'all' && filter !== status) return;
    const card = document.createElement('div');
    card.className = 'metric-card' + (isBookmarked ? ' bookmarked' : '');
    card.innerHTML = `
      <div class="card-actions">
        <button class="btn btn-sm ${isBookmarked?'btn-primary':'btn-outline'}" onclick="toggleBookmark('${m.id}')" title="Bookmark">&#9733;</button>
      </div>
      <h4>${m.label}</h4>
      <div class="value">${val}${m.unit ? '<span style="font-size:14px;font-weight:400;color:var(--text2)"> '+m.unit+'</span>' : ''}</div>
      <div class="sub">Threshold: ${m.threshold || 'N/A'} ${m.unit||''}</div>
      <div><span class="badge ${badgeClass}">${badgeText}</span></div>
    `;
    grid.appendChild(card);
  });
  if (grid.children.length === 0) {
    grid.innerHTML = '<div class="empty-state">No metrics match the current filter or view.<br>Try changing the filter or selecting a different view.</div>';
  }
}
function updateSidebarTab() {
  document.querySelectorAll('.tab-bar .tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));
  document.querySelector('.tab[data-tab="'+state.sidebarTab+'"]').classList.add('active');
  document.getElementById('panel-'+state.sidebarTab).classList.remove('hidden');
}
document.querySelectorAll('.tab-bar .tab').forEach(tab => {
  tab.addEventListener('click', function() {
    state.sidebarTab = this.dataset.tab;
    updateSidebarTab();
  });
});
// ── INIT ──────────────────────────────────────────────
loadState();
renderAll();
state.intervalId = setInterval(renderMetrics, 3000);
</script>
</body>
</html>
```