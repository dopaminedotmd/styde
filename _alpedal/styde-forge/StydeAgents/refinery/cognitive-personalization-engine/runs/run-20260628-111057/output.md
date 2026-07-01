<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Personalized Dashboard</title>
<style>
:root {
  --bg: #f5f7fa;
  --surface: #ffffff;
  --text: #1a1a2e;
  --text-secondary: #6c757d;
  --border: #dee2e6;
  --accent: #4361ee;
  --accent-hover: #3a56d4;
  --accent-light: #eef0ff;
  --danger: #e63946;
  --success: #2ec4b6;
  --warning: #ff9f1c;
  --radius: 12px;
  --radius-sm: 8px;
  --shadow: 0 2px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.12);
  --font-size: 14px;
  --spacing: 16px;
  --sidebar-width: 280px;
  --header-height: 60px;
  --density: 1;
}
.dark {
  --bg: #0f0f23;
  --surface: #1a1a35;
  --text: #e0e0ff;
  --text-secondary: #8888aa;
  --border: #2a2a4a;
  --accent-light: #1a1a3a;
  --shadow: 0 2px 12px rgba(0,0,0,0.3);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.4);
}
.compact { --spacing: 8px; --font-size: 13px; }
.comfortable { --spacing: 24px; --font-size: 16px; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); font-size: var(--font-size); min-height: 100vh; display: flex; }
h1, h2, h3 { font-weight: 600; }
h2 { font-size: calc(var(--font-size) * 1.4); margin-bottom: var(--spacing); }
h3 { font-size: calc(var(--font-size) * 1.15); margin-bottom: calc(var(--spacing) * 0.5); }
button { font-family: inherit; font-size: var(--font-size); cursor: pointer; border: none; border-radius: var(--radius-sm); padding: calc(6px * var(--density)) calc(14px * var(--density)); transition: all 0.2s; }
select, input { font-family: inherit; font-size: var(--font-size); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: calc(6px * var(--density)) calc(10px * var(--density)); background: var(--surface); color: var(--text); }
label { display: block; font-size: calc(var(--font-size) * 0.85); color: var(--text-secondary); margin-bottom: 4px; }
.sidebar {
  width: var(--sidebar-width); min-width: var(--sidebar-width);
  background: var(--surface); border-right: 1px solid var(--border);
  height: 100vh; overflow-y: auto; padding: var(--spacing);
  display: flex; flex-direction: column; gap: calc(var(--spacing) * 0.7);
}
.main { flex: 1; padding: var(--spacing); overflow-y: auto; height: 100vh; }
.profile-header { display: flex; align-items: center; gap: 12px; padding-bottom: var(--spacing); border-bottom: 1px solid var(--border); margin-bottom: calc(var(--spacing) * 0.5); }
.avatar { width: 40px; height: 40px; border-radius: 50%; background: var(--accent); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px; }
.profile-info h3 { margin: 0; font-size: calc(var(--font-size) * 1.1); }
.profile-info span { font-size: calc(var(--font-size) * 0.8); color: var(--text-secondary); }
.side-section { margin-bottom: calc(var(--spacing) * 0.3); }
.side-section h3 { font-size: calc(var(--font-size) * 0.85); color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
.side-section .item { padding: calc(4px * var(--density)) calc(8px * var(--density)); border-radius: var(--radius-sm); cursor: pointer; font-size: calc(var(--font-size) * 0.95); display: flex; align-items: center; gap: 8px; }
.side-section .item:hover { background: var(--accent-light); }
.side-section .item.active { background: var(--accent); color: white; }
.side-section .item .badge { margin-left: auto; font-size: 10px; background: var(--accent); color: white; border-radius: 10px; padding: 1px 6px; }
.side-section .item.active .badge { background: rgba(255,255,255,0.3); }
.profile-select { width: 100%; margin-bottom: var(--spacing); }
.card {
  background: var(--surface); border-radius: var(--radius); padding: var(--spacing);
  box-shadow: var(--shadow); border: 1px solid var(--border);
  margin-bottom: var(--spacing);
}
.metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--spacing); margin-bottom: var(--spacing); }
.metric-card { background: var(--surface); border-radius: var(--radius); padding: var(--spacing); box-shadow: var(--shadow); border: 1px solid var(--border); text-align: center; }
.metric-card .value { font-size: calc(var(--font-size) * 2.2); font-weight: 700; color: var(--accent); margin: 6px 0; }
.metric-card .label { font-size: calc(var(--font-size) * 0.85); color: var(--text-secondary); }
.metric-card .trend { font-size: calc(var(--font-size) * 0.8); margin-top: 4px; }
.trend.up { color: var(--success); } .trend.down { color: var(--danger); }
.flex-row { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.flex-between { display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap; }
.gap { gap: var(--spacing); }
.mb { margin-bottom: var(--spacing); }
.hidden { display: none !important; }
.btn-primary { background: var(--accent); color: white; }
.btn-primary:hover { background: var(--accent-hover); }
.btn-danger { background: var(--danger); color: white; }
.btn-outline { background: transparent; color: var(--text); border: 1px solid var(--border); }
.btn-outline:hover { background: var(--accent-light); }
.btn-sm { padding: 4px 10px; font-size: calc(var(--font-size) * 0.85); }
.btn-icon { padding: 4px 8px; font-size: calc(var(--font-size) * 0.85); }
.tag { display: inline-block; background: var(--accent-light); border: 1px solid var(--accent); color: var(--accent); padding: 2px 8px; border-radius: 12px; font-size: calc(var(--font-size) * 0.75); font-weight: 500; margin: 2px; cursor: pointer; }
.tag.active-tag { background: var(--accent); color: white; }
.tab-bar { display: flex; gap: 0; border-bottom: 2px solid var(--border); margin-bottom: var(--spacing); }
.tab { padding: calc(8px * var(--density)) calc(16px * var(--density)); cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -2px; color: var(--text-secondary); font-weight: 500; }
.tab:hover { color: var(--text); }
.tab.active { color: var(--accent); border-bottom-color: var(--accent); }
.color-swatch { width: 28px; height: 28px; border-radius: 50%; border: 2px solid var(--border); cursor: pointer; display: inline-block; transition: transform 0.15s; }
.color-swatch:hover { transform: scale(1.15); }
.color-swatch.selected { border-color: var(--accent); box-shadow: 0 0 0 2px var(--surface), 0 0 0 4px var(--accent); }
.alert-item { padding: calc(8px * var(--density)); border: 1px solid var(--border); border-radius: var(--radius-sm); margin-bottom: 6px; }
.alert-item .flex-between { gap: 4px; }
.alert-tag { font-size: 10px; padding: 1px 6px; border-radius: 4px; font-weight: 600; }
.alert-tag.warning { background: #fff3cd; color: #856404; }
.alert-tag.danger { background: #f8d7da; color: #721c24; }
.alert-tag.info { background: #d1ecf1; color: #0c5460; }
.bookmark-item { padding: calc(6px * var(--density)) calc(8px * var(--density)); border: 1px solid var(--border); border-radius: var(--radius-sm); margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }
.bookmark-item .bm-title { font-weight: 500; flex: 1; }
.bookmark-item .bm-meta { font-size: calc(var(--font-size) * 0.75); color: var(--text-secondary); }
.view-item { padding: calc(6px * var(--density)) calc(8px * var(--density)); border: 1px solid var(--border); border-radius: var(--radius-sm); margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }
.view-item .vi-name { flex: 1; font-weight: 500; }
.theme-grid { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
.progress-bar { height: 3px; background: var(--border); border-radius: 2px; margin: 8px 0; overflow: hidden; }
.progress-fill { height: 100%; background: var(--accent); border-radius: 2px; transition: width 0.5s; }
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.modal { background: var(--surface); border-radius: var(--radius); padding: calc(var(--spacing) * 1.5); min-width: 360px; max-width: 500px; box-shadow: var(--shadow-lg); }
.modal h2 { margin-bottom: var(--spacing); }
.modal .field { margin-bottom: calc(var(--spacing) * 0.7); }
.modal .field label { margin-bottom: 4px; }
.modal .field input, .modal .field select, .modal .field textarea { width: 100%; }
.modal textarea { font-family: inherit; font-size: var(--font-size); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 8px; background: var(--surface); color: var(--text); resize: vertical; min-height: 60px; }
.modal .modal-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: var(--spacing); }
.toast {
  position: fixed; bottom: 24px; right: 24px;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius-sm); padding: 12px 20px;
  box-shadow: var(--shadow-lg); z-index: 2000;
  font-size: calc(var(--font-size) * 0.95);
  animation: slideIn 0.3s ease;
}
@keyframes slideIn { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
@media (max-width: 768px) {
  body { flex-direction: column; }
  .sidebar { width: 100%; min-width: unset; height: auto; max-height: 40vh; }
  .main { height: auto; }
  .metrics-grid { grid-template-columns: 1fr 1fr; }
}
</style>
</head>
<body>
<div class="sidebar" id="sidebar">
  <div class="profile-header">
    <div class="avatar" id="avatar">U</div>
    <div class="profile-info">
      <h3 id="profileName">User</h3>
      <span id="profileBio">New user</span>
    </div>
  </div>
  <div class="side-section">
    <label for="profileSelect">Switch Profile</label>
    <select id="profileSelect" class="profile-select"></select>
  </div>
  <div class="side-section">
    <h3>Progress</h3>
    <div class="flex-between">
      <span id="levelDisplay" style="font-size:12px;color:var(--text-secondary)">Level 1</span>
      <span id="xpDisplay" style="font-size:12px;color:var(--text-secondary)">0 XP</span>
    </div>
    <div class="progress-bar"><div class="progress-fill" id="xpBar" style="width:0%"></div></div>
  </div>
  <div class="side-section">
    <h3>Views</h3>
    <div id="viewList"></div>
    <button class="btn-outline btn-sm" style="width:100%;margin-top:4px" onclick="showSaveViewModal()">+ Save Current View</button>
  </div>
  <div class="side-section">
    <h3>Bookmarks</h3>
    <div id="bookmarkList"></div>
  </div>
  <div class="side-section">
    <h3>Theme</h3>
    <label for="themeMode">Mode</label>
    <select id="themeMode" onchange="applyTheme()"><option value="light">Light</option><option value="dark">Dark</option></select>
    <label style="margin-top:6px">Accent</label>
    <div class="theme-grid" id="accentGrid"></div>
    <label style="margin-top:6px">Density</label>
    <select id="densitySelect" onchange="applyTheme()"><option value="1">Default</option><option value="0.85">Compact</option><option value="1.15">Comfortable</option></select>
    <label style="margin-top:6px">Font Scale</label>
    <input type="range" id="fontScale" min="12" max="20" value="14" oninput="applyTheme()" style="width:100%">
  </div>
</div>
<div class="main" id="mainArea">
  <div class="tab-bar" id="tabBar">
    <div class="tab active" data-tab="dashboard" onclick="switchTab('dashboard')">Dashboard</div>
    <div class="tab" data-tab="alerts" onclick="switchTab('alerts')">Alerts</div>
    <div class="tab" data-tab="settings" onclick="switchTab('settings')">Settings</div>
  </div>
  <div id="tabDashboard">
    <div class="flex-between mb">
      <h2>Dashboard</h2>
      <div class="flex-row">
        <span style="font-size:12px;color:var(--text-secondary);padding:4px 8px;background:var(--accent-light);border-radius:4px" id="widgetCount">0 widgets</span>
      </div>
    </div>
    <div class="metrics-grid" id="metricsGrid"></div>
    <div class="card">
      <div class="flex-between mb">
        <h3>Recent Activity</h3>
        <span style="font-size:12px;color:var(--text-secondary)" id="activityCount">0 events</span>
      </div>
      <div id="activityFeed"></div>
    </div>
    <div class="card" id="suggestionCard">
      <div class="flex-between mb">
        <h3 id="suggestionTitle">Suggestions</h3>
      </div>
      <div id="suggestionList"></div>
    </div>
  </div>
  <div id="tabAlerts" class="hidden">
    <div class="flex-between mb">
      <h2>Alert Configuration</h2>
      <button class="btn-primary btn-sm" onclick="showAddAlertModal()">+ New Alert</button>
    </div>
    <div class="card">
      <h3>Notification Preferences</h3>
      <div class="flex-row" style="margin-top:8px;gap:16px;flex-wrap:wrap">
        <label style="display:flex;align-items:center;gap:6px;cursor:pointer"><input type="checkbox" id="notifEmail" onchange="saveAlertPrefs()"> Email</label>
        <label style="display:flex;align-items:center;gap:6px;cursor:pointer"><input type="checkbox" id="notifPush" onchange="saveAlertPrefs()"> Push</label>
        <label style="display:flex;align-items:center;gap:6px;cursor:pointer"><input type="checkbox" id="notifSms" onchange="saveAlertPrefs()"> SMS</label>
        <label style="display:flex;align-items:center;gap:6px;cursor:pointer"><input type="checkbox" id="notifInApp" onchange="saveAlertPrefs()"> In-App</label>
      </div>
      <div style="margin-top:12px">
        <label>Mute Schedule</label>
        <div class="flex-row" style="gap:8px;flex-wrap:wrap;margin-top:4px">
          <label style="display:flex;align-items:center;gap:4px;cursor:pointer"><input type="checkbox" class="muteDay" value="0"> Sun</label>
          <label style="display:flex;align-items:center;gap:4px;cursor:pointer"><input type="checkbox" class="muteDay" value="1"> Mon</label>
          <label style="display:flex;align-items:center;gap:4px;cursor:pointer"><input type="checkbox" class="muteDay" value="2"> Tue</label>
          <label style="display:flex;align-items:center;gap:4px;cursor:pointer"><input type="checkbox" class="muteDay" value="3"> Wed</label>
          <label style="display:flex;align-items:center;gap:4px;cursor:pointer"><input type="checkbox" class="muteDay" value="4"> Thu</label>
          <label style="display:flex;align-items:center;gap:4px;cursor:pointer"><input type="checkbox" class="muteDay" value="5"> Fri</label>
          <label style="display:flex;align-items:center;gap:4px;cursor:pointer"><input type="checkbox" class="muteDay" value="6"> Sat</label>
        </div>
      </div>
      <div style="margin-top:12px">
        <label>Mute Start / End</label>
        <div class="flex-row" style="gap:8px">
          <input type="time" id="muteStart" value="22:00" onchange="saveAlertPrefs()">
          <span style="color:var(--text-secondary)">to</span>
          <input type="time" id="muteEnd" value="08:00" onchange="saveAlertPrefs()">
        </div>
      </div>
    </div>
    <div class="card">
      <h3>Alert Thresholds</h3>
      <div id="alertThresholds"></div>
    </div>
  </div>
  <div id="tabSettings" class="hidden">
    <h2>Settings</h2>
    <div class="card">
      <h3>User Profile</h3>
      <div class="field" style="margin-bottom:8px">
        <label>Display Name</label>
        <input type="text" id="editName" style="width:100%" onchange="updateProfile()">
      </div>
      <div class="field" style="margin-bottom:8px">
        <label>Bio</label>
        <input type="text" id="editBio" style="width:100%" onchange="updateProfile()">
      </div>
      <div class="field" style="margin-bottom:8px">
        <label>Avatar Initial</label>
        <input type="text" id="editInitial" maxlength="2" style="width:60px" onchange="updateProfile()">
      </div>
      <button class="btn-outline btn-sm" onclick="resetProfile()">Reset to Defaults</button>
      <button class="btn-danger btn-sm" style="margin-left:8px" onclick="deleteProfile()">Delete Profile</button>
    </div>
    <div class="card">
      <h3>Export / Import</h3>
      <div class="flex-row">
        <button class="btn-outline btn-sm" onclick="exportProfile()">Export Profile JSON</button>
        <button class="btn-outline btn-sm" onclick="document.getElementById('importInput').click()">Import Profile</button>
        <input type="file" id="importInput" accept=".json" style="display:none" onchange="importProfile(event)">
      </div>
    </div>
  </div>
</div>
<div id="modalOverlay" class="modal-overlay hidden">
  <div class="modal" id="modalContent"></div>
</div>
<script>
var ACCENT_COLORS = ['#4361ee','#e63946','#2ec4b6','#ff9f1c','#9b5de5','#f15bb5','#00bbf9','#06d6a0','#7209b7','#3a0ca3','#f77f00','#588157'];
var profileId = 'default';
var profiles = {
  'default': { name: 'Default User', bio: 'New user — dashboard adapting', initial: 'D', xp: 0, level: 1, theme: { mode: 'light', accent: '#4361ee', density: '1', fontSize: 14 }, views: {}, bookmarks: [], alerts: { thresholds: [], channels: { email: true, push: true, sms: false, inApp: true }, muteDays: [], muteStart: '22:00', muteEnd: '08:00' }, interactions: 0, hiddenMetrics: [] },
  'alice': { name: 'Alice Chen', bio: 'Data analyst — 127 interactions', initial: 'A', xp: 340, level: 4, theme: { mode: 'dark', accent: '#2ec4b6', density: '1', fontSize: 14 }, views: { 'Analytics Overview': { metrics: ['Revenue','Users','Sessions'], layout: 'grid' }, 'Support View': { metrics: ['Tickets','SLA','CSAT'], layout: 'grid' } }, bookmarks: [{ metric: 'Revenue', annotation: 'Q3 peak on Sep 15 — investigate what drove this', ts: Date.now() - 86400000 }, { metric: 'CSAT', annotation: 'Dropped after v2.3 deploy', ts: Date.now() - 172800000 }], alerts: { thresholds: [ { metric: 'Error Rate', operator: '>', value: 2, severity: 'danger' }, { metric: 'SLA', operator: '<', value: 99.5, severity: 'warning' } ], channels: { email: true, push: true, sms: true, inApp: true }, muteDays: [0,6], muteStart: '23:00', muteEnd: '07:00' }, interactions: 127, hiddenMetrics: [] },
  'bob': { name: 'Bob Martinez', bio: 'Engineering lead — 89 interactions', initial: 'B', xp: 210, level: 3, theme: { mode: 'light', accent: '#e63946', density: '0.85', fontSize: 13 }, views: { 'Deploy Dashboard': { metrics: ['Deployments','Error Rate','Latency','SLA'], layout: 'grid' } }, bookmarks: [{ metric: 'Latency', annotation: 'P95 spiked after CDN migration', ts: Date.now() - 3600000 }], alerts: { thresholds: [ { metric: 'Error Rate', operator: '>', value: 1, severity: 'danger' }, { metric: 'Latency', operator: '>', value: 500, severity: 'warning' } ], channels: { email: false, push: true, sms: true, inApp: true }, muteDays: [], muteStart: '22:00', muteEnd: '06:00' }, interactions: 89, hiddenMetrics: [] },
  'clara': { name: 'Clara Johnson', bio: 'Product manager — 63 interactions', initial: 'C', xp: 150, level: 2, theme: { mode: 'light', accent: '#9b5de5', density: '1.15', fontSize: 16 }, views: { 'Weekly Review': { metrics: ['MAU','Revenue','Retention','NPS'], layout: 'grid' } }, bookmarks: [{ metric: 'NPS', annotation: 'Check after feature launch next week', ts: Date.now() - 43200000 }], alerts: { thresholds: [ { metric: 'Revenue', operator: '<', value: 10000, severity: 'danger' } ], channels: { email: true, push: false, sms: false, inApp: true }, muteDays: [0], muteStart: '21:00', muteEnd: '09:00' }, interactions: 63, hiddenMetrics: ['Error Rate','Latency'] },
  'dave': { name: 'Dave Kim', bio: 'SRE — 201 interactions', initial: 'D', xp: 520, level: 6, theme: { mode: 'dark', accent: '#f77f00', density: '0.85', fontSize: 13 }, views: { 'SRE Console': { metrics: ['Error Rate','Latency','Uptime','SLA','Deployments'], layout: 'grid' }, 'Incident Review': { metrics: ['SLA','Uptime','Error Rate'], layout: 'grid' } }, bookmarks: [{ metric: 'Uptime', annotation: '99.99% target breached in October — root cause infra scaling', ts: Date.now() - 604800000 }, { metric: 'Error Rate', annotation: 'Spike correlates with deploy frequency', ts: Date.now() - 259200000 }], alerts: { thresholds: [ { metric: 'Uptime', operator: '<', value: 99.99, severity: 'danger' }, { metric: 'Error Rate', operator: '>', value: 0.5, severity: 'warning' }, { metric: 'Latency', operator: '>', value: 300, severity: 'warning' } ], channels: { email: true, push: true, sms: true, inApp: true }, muteDays: [], muteStart: '00:00', muteEnd: '06:00' }, interactions: 201, hiddenMetrics: [] }
};
var allMetrics = [
  { id: 'Revenue', value: 28450, prefix: '$', suffix: '', trend: 12.3, up: true },
  { id: 'Users', value: 14238, prefix: '', suffix: '', trend: 8.7, up: true },
  { id: 'Sessions', value: 89342, prefix: '', suffix: '', trend: -2.1, up: false },
  { id: 'Error Rate', value: 0.87, prefix: '', suffix: '%', trend: -0.3, up: false },
  { id: 'Latency', value: 245, prefix: '', suffix: 'ms', trend: 15, up: false },
  { id: 'SLA', value: 99.87, prefix: '', suffix: '%', trend: 0.02, up: true },
  { id: 'Tickets', value: 47, prefix: '', suffix: '', trend: -12, up: false },
  { id: 'CSAT', value: 4.2, prefix: '', suffix: '/5', trend: -0.1, up: false },
  { id: 'Deployments', value: 23, prefix: '', suffix: '', trend: 5, up: true },
  { id: 'Uptime', value: 99.993, prefix: '', suffix: '%', trend: 0.001, up: true },
  { id: 'MAU', value: 187000, prefix: '', suffix: '', trend: 15.4, up: true },
  { id: 'Retention', value: 76.4, prefix: '', suffix: '%', trend: 2.1, up: true },
  { id: 'NPS', value: 42, prefix: '', suffix: '', trend: 3, up: true }
];
var suggestions = [
  'Try saving your current layout as a view',
  'Click any metric name to bookmark it',
  'Switch to dark mode in the sidebar',
  'Export your profile from Settings',
  'Set alert thresholds in the Alerts tab'
];
function getProfile() { return profiles[profileId] || profiles['default']; }
function saveProfiles() {
  try {
    var data = JSON.stringify(profiles);
    localStorage.setItem('dashProfiles', data);
  } catch(e) {}
}
function loadProfiles() {
  try {
    var raw = localStorage.getItem('dashProfiles');
    if (raw) { var p = JSON.parse(raw); Object.keys(p).forEach(function(k) { profiles[k] = p[k]; }); }
  } catch(e) {}
}
function init() {
  loadProfiles();
  populateProfileSelect();
  populateAccentGrid();
  var urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('profile')) { profileId = urlParams.get('profile'); }
  if (urlParams.get('theme')) { getProfile().theme.mode = urlParams.get('theme'); }
  loadProfile(profileId);
  render();
}
function populateProfileSelect() {
  var sel = document.getElementById('profileSelect');
  sel.innerHTML = '';
  var keys = Object.keys(profiles);
  keys.forEach(function(k) {
    var opt = document.createElement('option');
    opt.value = k;
    opt.textContent = profiles[k].name + ' (Lv.' + profiles[k].level + ')';
    sel.appendChild(opt);
  });
  sel.value = profileId;
  sel.onchange = function() {
    profileId = this.value;
    var url = new URL(window.location);
    url.searchParams.set('profile', profileId);
    window.history.replaceState({}, '', url);
    loadProfile(profileId);
    render();
    showToast('Switched to ' + getProfile().name);
  };
}
function populateAccentGrid() {
  var grid = document.getElementById('accentGrid');
  grid.innerHTML = '';
  ACCENT_COLORS.forEach(function(c) {
    var sw = document.createElement('span');
    sw.className = 'color-swatch';
    sw.style.background = c;
    sw.dataset.color = c;
    sw.onclick = function() {
      getProfile().theme.accent = c;
      applyTheme();
      saveProfiles();
      document.querySelectorAll('.color-swatch').forEach(function(s) { s.classList.remove('selected'); });
      this.classList.add('selected');
    };
    grid.appendChild(sw);
  });
}
function loadProfile(id) {
  var p = profiles[id];
  if (!p) { profiles[id] = JSON.parse(JSON.stringify(profiles['default'])); p = profiles[id]; }
  applyTheme();
  document.getElementById('profileSelect').value = id;
  document.getElementById('editName').value = p.name;
  document.getElementById('editBio').value = p.bio;
  document.getElementById('editInitial').value = p.initial;
}
function applyTheme() {
  var p = getProfile();
  p.theme.mode = document.getElementById('themeMode').value;
  p.theme.density = document.getElementById('densitySelect').value;
  p.theme.fontSize = parseInt(document.getElementById('fontScale').value);
  var root = document.documentElement;
  var accent = p.theme.accent || '#4361ee';
  root.style.setProperty('--accent', accent);
  root.style.setProperty('--accent-hover', accent + 'dd');
  root.classList.toggle('dark', p.theme.mode === 'dark');
  if (p.theme.density === '0.85') { root.classList.add('compact'); root.classList.remove('comfortable'); }
  else if (p.theme.density === '1.15') { root.classList.add('comfortable'); root.classList.remove('compact'); }
  else { root.classList.remove('compact','comfortable'); }
  root.style.setProperty('--font-size', p.theme.fontSize + 'px');
  document.getElementById('themeMode').value = p.theme.mode;
  document.getElementById('densitySelect').value = p.theme.density;
  document.getElementById('fontScale').value = p.theme.fontSize;
  document.querySelectorAll('.color-swatch').forEach(function(s) { s.classList.toggle('selected', s.dataset.color === accent); });
  saveProfiles();
}
function render() {
  var p = getProfile();
  document.getElementById('profileName').textContent = p.name;
  document.getElementById('profileBio').textContent = p.bio;
  document.getElementById('avatar').textContent = p.initial;
  document.getElementById('levelDisplay').textContent = 'Level ' + p.level;
  document.getElementById('xpDisplay').textContent = p.xp + ' XP';
  var nextLvl = p.level * 100;
  var pct = Math.min(100, (p.xp / nextLvl) * 100);
  document.getElementById('xpBar').style.width = pct + '%';
  renderMetrics(p);
  renderViews(p);
  renderBookmarks(p);
  renderAlerts(p);
  renderActivity();
  renderSuggestions(p);
}
function renderMetrics(p) {
  var grid = document.getElementById('metricsGrid');
  grid.innerHTML = '';
  var visible = allMetrics.filter(function(m) { return p.hiddenMetrics.indexOf(m.id) === -1; });
  document.getElementById('widgetCount').textContent = visible.length + ' widgets';
  visible.forEach(function(m) {
    var card = document.createElement('div');
    card.className = 'metric-card';
    var val = m.prefix + m.value.toLocaleString() + m.suffix;
    var trendCls = m.up ? 'up' : 'down';
    var trendSign = m.up ? '+' : '';
    var isBookmarked = p.bookmarks.some(function(b) { return b.metric === m.id; });
    card.innerHTML =
      '<div class="flex-between" style="gap:4px;margin-bottom:4px">' +
      '<span class="label" style="cursor:pointer" onclick="bookmarkMetric(\'' + m.id + '\')" title="Bookmark this metric">' + m.id + '</span>' +
      '<span style="display:flex;gap:4px">' +
      (isBookmarked ? '<span class="tag active-tag" style="font-size:9px;cursor:default">saved</span>' : '') +
      '<span class="tag" style="font-size:9px;cursor:pointer" onclick="pinMetric(\'' + m.id + '\')">pin</span>' +
      '<span class="tag" style="font-size:9px;cursor:pointer;color:var(--danger)" onclick="hideMetric(\'' + m.id + '\')">hide</span>' +
      '</span></div>' +
      '<div class="value">' + val + '</div>' +
      '<div class="trend ' + trendCls + '">' + trendSign + m.trend + '% vs last period</div>';
    grid.appendChild(card);
  });
}
function renderViews(p) {
  var list = document.getElementById('viewList');
  list.innerHTML = '';
  var vkeys = Object.keys(p.views);
  if (vkeys.length === 0) {
    list.innerHTML = '<div style="font-size:12px;color:var(--text-secondary);padding:4px 8px">No saved views yet</div>';
    return;
  }
  vkeys.forEach(function(name) {
    var div = document.createElement('div');
    div.className = 'view-item';
    div.innerHTML = '<span class="vi-name">' + name + '</span><button class="btn-icon btn-outline" onclick="loadView(\'' + name.replace(/'/g,"\\'") + '\')" title="Load">L</button><button class="btn-icon btn-danger" onclick="deleteView(\'' + name.replace(/'/g,"\\'") + '\')" title="Delete">X</button>';
    list.appendChild(div);
  });
}
function renderBookmarks(p) {
  var list = document.getElementById('bookmarkList');
  list.innerHTML = '';
  if (p.bookmarks.length === 0) {
    list.innerHTML = '<div style="font-size:12px;color:var(--text-secondary);padding:4px 8px">Click a metric name to bookmark</div>';
    return;
  }
  p.bookmarks.forEach(function(b, i) {
    var div = document.createElement('div');
    div.className = 'bookmark-item';
    var d = new Date(b.ts);
    div.innerHTML = '<span class="bm-title">' + b.metric + '</span><span class="bm-meta">' + (b.annotation ? b.annotation.substring(0, 30) : '') + '</span><span style="font-size:10px;color:var(--text-secondary)">' + d.toLocaleDateString() + '</span><button class="btn-icon btn-danger" onclick="deleteBookmark(' + i + ')">X</button>';
    list.appendChild(div);
  });
}
function renderAlerts(p) {
  var container = document.getElementById('alertThresholds');
  container.innerHTML = '';
  if (p.alerts.thresholds.length === 0) {
    container.innerHTML = '<div style="color:var(--text-secondary);padding:8px 0;font-size:13px">No alert thresholds configured. Add one above.</div>';
    return;
  }
  p.alerts.thresholds.forEach(function(t, i) {
    var div = document.createElement('div');
    div.className = 'alert-item';
    div.innerHTML =
      '<div class="flex-between"><span style="font-weight:500">' + t.metric + ' ' + t.operator + ' ' + t.value + '</span>' +
      '<span class="alert-tag ' + t.severity + '">' + t.severity + '</span></div>' +
      '<div class="flex-row" style="margin-top:4px"><button class="btn-icon btn-danger btn-sm" onclick="deleteAlert(' + i + ')">Remove</button></div>';
    container.appendChild(div);
  });
  var ch = p.alerts.channels;
  document.getElementById('notifEmail').checked = ch.email;
  document.getElementById('notifPush').checked = ch.push;
  document.getElementById('notifSms').checked = ch.sms;
  document.getElementById('notifInApp').checked = ch.inApp;
  document.querySelectorAll('.muteDay').forEach(function(cb) {
    cb.checked = p.alerts.muteDays.indexOf(parseInt(cb.value)) !== -1;
    cb.onchange = saveAlertPrefs;
  });
  document.getElementById('muteStart').value = p.alerts.muteStart;
  document.getElementById('muteEnd').value = p.alerts.muteEnd;
}
var activityLog = [
  { type: 'login', text: 'Logged in', ts: Date.now() - 300000 },
  { type: 'view', text: 'Viewed Dashboard', ts: Date.now() - 600000 },
  { type: 'export', text: 'Exported profile data', ts: Date.now() - 86400000 }
];
function renderActivity() {
  var feed = document.getElementById('activityFeed');
  feed.innerHTML = '';
  document.getElementById('activityCount').textContent = activityLog.length + ' events';
  activityLog.slice().reverse().slice(0, 10).forEach(function(a) {
    var d = new Date(a.ts);
    var rel = Math.floor((Date.now() - a.ts) / 60000);
    var timeStr = rel < 1 ? 'just now' : rel < 60 ? rel + 'm ago' : Math.floor(rel / 60) + 'h ago';
    var div = document.createElement('div');
    div.style.cssText = 'padding:6px 0;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center';
    div.innerHTML = '<span>' + a.text + '</span><span style="font-size:11px;color:var(--text-secondary)">' + timeStr + '</span>';
    feed.appendChild(div);
  });
}
function renderSuggestions(p) {
  var list = document.getElementById('suggestionList');
  list.innerHTML = '';
  var shown = 0;
  suggestions.forEach(function(s, i) {
    if (i > p.level * 2) return;
    if (shown > 3) return;
    if (p.interactions > (i + 1) * 20) return;
    shown++;
    var div = document.createElement('div');
    div.style.cssText = 'padding:6px 8px;margin-bottom:4px;background:var(--accent-light);border-radius:var(--radius-sm);font-size:calc(var(--font-size) * 0.95);cursor:pointer;display:flex;align-items:center;gap:8px';
    div.innerHTML = '<span style="color:var(--accent);font-weight:700">~</span> ' + s;
    div.onclick = function() { this.style.opacity = '0.5'; };
    list.appendChild(div);
  });
  if (shown === 0 || p.interactions > 100) {
    // DATA IS MOCK: progressive personalization suggestions
    document.getElementById('suggestionCard').classList.add('hidden');
  } else {
    document.getElementById('suggestionCard').classList.remove('hidden');
  }
}
function switchTab(tab) {
  ['dashboard','alerts','settings'].forEach(function(t) {
    document.getElementById('tab' + t.charAt(0).toUpperCase() + t.slice(1)).classList.toggle('hidden', t !== tab);
  });
  document.querySelectorAll('.tab').forEach(function(el) {
    el.classList.toggle('active', el.dataset.tab === tab);
  });
}
function showSaveViewModal() {
  var p = getProfile();
  var visible = allMetrics.filter(function(m) { return p.hiddenMetrics.indexOf(m.id) === -1; });
  var names = visible.map(function(m) { return m.id; }).join(', ');
  document.getElementById('modalOverlay').classList.remove('hidden');
  document.getElementById('modalContent').innerHTML =
    '<h2>Save Current View</h2>' +
    '<div class="field"><label>View Name</label><input type="text" id="viewNameInput" placeholder="e.g. Weekly Review"></div>' +
    '<div class="field"><label>Metrics visible</label><div style="font-size:13px;color:var(--text-secondary)">' + names + '</div></div>' +
    '<div class="modal-actions">' +
    '<button class="btn-outline" onclick="closeModal()">Cancel</button>' +
    '<button class="btn-primary" onclick="saveCurrentView()">Save View</button></div>';
}
function saveCurrentView() {
  var name = document.getElementById('viewNameInput').value.trim();
  if (!name) { showToast('Enter a view name'); return; }
  var p = getProfile();
  var visible = allMetrics.filter(function(m) { return p.hiddenMetrics.indexOf(m.id) === -1; });
  p.views[name] = { metrics: visible.map(function(m) { return m.id; }), layout: 'grid' };
  saveProfiles();
  closeModal();
  render();
  showToast('View "' + name + '" saved');
}
function loadView(name) {
  var p = getProfile();
  var view = p.views[name];
  if (!view) { showToast('View not found'); return; }
  p.hiddenMetrics = allMetrics.map(function(m) { return m.id; }).filter(function(id) { return view.metrics.indexOf(id) === -1; });
  saveProfiles();
  render();
  showToast('Loaded view: ' + name);
}
function deleteView(name) {
  var p = getProfile();
  delete p.views[name];
  saveProfiles();
  render();
  showToast('View "' + name + '" deleted');
}
function bookmarkMetric(id) {
  var p = getProfile();
  var existing = p.bookmarks.findIndex(function(b) { return b.metric === id; });
  if (existing !== -1) {
    p.bookmarks.splice(existing, 1);
    showToast('Bookmark removed: ' + id);
  } else {
    p.bookmarks.push({ metric: id, annotation: '', ts: Date.now() });
    p.xp = Math.min((p.level + 1) * 100, p.xp + 5);
    checkLevelUp(p);
    showToast('Bookmarked: ' + id + ' (+5 XP)');
    activityLog.push({ type: 'bookmark', text: 'Bookmarked ' + id, ts: Date.now() });
  }
  saveProfiles();
  render();
}
function deleteBookmark(i) {
  var p = getProfile();
  var b = p.bookmarks[i];
  p.bookmarks.splice(i, 1);
  saveProfiles();
  render();
  showToast('Bookmark removed: ' + b.metric);
}
function pinMetric(id) {
  showToast('Pin ' + id + ' — would reorder to top in production');
}
function hideMetric(id) {
  var p = getProfile();
  if (p.hiddenMetrics.indexOf(id) === -1) {
    p.hiddenMetrics.push(id);
    p.xp = Math.min((p.level + 1) * 100, p.xp + 3);
    checkLevelUp(p);
    showToast('Hidden: ' + id + ' (+3 XP)');
    activityLog.push({ type: 'hide', text: 'Removed ' + id + ' from dashboard', ts: Date.now() });
  }
  saveProfiles();
  render();
}
function checkLevelUp(p) {
  var nextLvl = p.level * 100;
  if (p.xp >= nextLvl) {
    p.xp = p.xp - nextLvl;
    p.level++;
    showToast('Level Up! You are now level ' + p.level);
    activityLog.push({ type: 'levelup', text: 'Reached level ' + p.level, ts: Date.now() });
  }
  var sel = document.getElementById('profileSelect');
  var opt = sel.querySelector('option[value="' + profileId + '"]');
  if (opt) { opt.textContent = p.name + ' (Lv.' + p.level + ')'; }
}
function showAddAlertModal() {
  var metricOptions = allMetrics.map(function(m) { return '<option value="' + m.id + '">' + m.id + '</option>'; }).join('');
  document.getElementById('modalOverlay').classList.remove('hidden');
  document.getElementById('modalContent').innerHTML =
    '<h2>Add Alert Threshold</h2>' +
    '<div class="field"><label>Metric</label><select id="alertMetric">' + metricOptions + '</select></div>' +
    '<div class="field"><label>Operator</label><select id="alertOperator"><option value=">">Greater than</option><option value="<">Less than</option><option value=">=">Greater or equal</option><option value="<=">Less or equal</option></select></div>' +
    '<div class="field"><label>Value</label><input type="number" id="alertValue" step="any" value="0"></div>' +
    '<div class="field"><label>Severity</label><select id="alertSeverity"><option value="warning">Warning</option><option value="danger">Danger</option><option value="info">Info</option></select></div>' +
    '<div class="modal-actions">' +
    '<button class="btn-outline" onclick="closeModal()">Cancel</button>' +
    '<button class="btn-primary" onclick="saveNewAlert()">Add Alert</button></div>';
}
function saveNewAlert() {
  var metric = document.getElementById('alertMetric').value;
  var operator = document.getElementById('alertOperator').value;
  var value = parseFloat(document.getElementById('alertValue').value);
  var severity = document.getElementById('alertSeverity').value;
  if (isNaN(value)) { showToast('Enter a valid number'); return; }
  var p = getProfile();
  p.alerts.thresholds.push({ metric: metric, operator: operator, value: value, severity: severity });
  p.xp = Math.min((p.level + 1) * 100, p.xp + 10);
  checkLevelUp(p);
  saveProfiles();
  closeModal();
  render();
  showToast('Alert added for ' + metric + ' (+10 XP)');
  activityLog.push({ type: 'alert', text: 'Created alert: ' + metric + ' ' + operator + ' ' + value, ts: Date.now() });
}
function deleteAlert(i) {
  var p = getProfile();
  var a = p.alerts.thresholds[i];
  p.alerts.thresholds.splice(i, 1);
  saveProfiles();
  render();
  showToast('Alert removed: ' + a.metric);
}
function saveAlertPrefs() {
  var p = getProfile();
  p.alerts.channels.email = document.getElementById('notifEmail').checked;
  p.alerts.channels.push = document.getElementById('notifPush').checked;
  p.alerts.channels.sms = document.getElementById('notifSms').checked;
  p.alerts.channels.inApp = document.getElementById('notifInApp').checked;
  p.alerts.muteDays = [];
  document.querySelectorAll('.muteDay:checked').forEach(function(cb) { p.alerts.muteDays.push(parseInt(cb.value)); });
  p.alerts.muteStart = document.getElementById('muteStart').value;
  p.alerts.muteEnd = document.getElementById('muteEnd').value;
  saveProfiles();
}
function updateProfile() {
  var p = getProfile();
  p.name = document.getElementById('editName').value.trim() || p.name;
  p.bio = document.getElementById('editBio').value.trim() || p.bio;
  var init = document.getElementById('editInitial').value.trim().toUpperCase();
  if (init.length >= 1) { p.initial = init.substring(0, 2); }
  p.xp = Math.min((p.level + 1) * 100, p.xp + 2);
  checkLevelUp(p);
  saveProfiles();
  render();
  showToast('Profile updated (+2 XP)');
}
function resetProfile() {
  if (!confirm('Reset profile to default settings?')) return;
  var defaults = JSON.parse(JSON.stringify(profiles['default']));
  defaults.name = getProfile().name;
  profiles[profileId] = defaults;
  saveProfiles();
  loadProfile(profileId);
  render();
  showToast('Profile reset');
}
function deleteProfile() {
  if (profileId === 'default') { showToast('Cannot delete default profile'); return; }
  if (!confirm('Delete profile "' + getProfile().name + '"?')) return;
  delete profiles[profileId];
  profileId = 'default';
  var url = new URL(window.location);
  url.searchParams.set('profile', 'default');
  window.history.replaceState({}, '', url);
  saveProfiles();
  populateProfileSelect();
  loadProfile('default');
  render();
  showToast('Profile deleted');
}
function exportProfile() {
  var p = getProfile();
  var data = JSON.stringify(p, null, 2);
  var blob = new Blob([data], { type: 'application/json' });
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'profile-' + profileId + '.json';
  a.click();
  URL.revokeObjectURL(a.href);
  showToast('Profile exported');
}
function importProfile(e) {
  var file = e.target.files[0];
  if (!file) return;
  var reader = new FileReader();
  reader.onload = function(ev) {
    try {
      var data = JSON.parse(ev.target.result);
      var p = getProfile();
      Object.keys(data).forEach(function(k) { p[k] = data[k]; });
      saveProfiles();
      loadProfile(profileId);
      render();
      showToast('Profile imported successfully');
    } catch(err) {
      showToast('Invalid profile file');
    }
  };
  reader.readAsText(file);
  e.target.value = '';
}
function closeModal() {
  document.getElementById('modalOverlay').classList.add('hidden');
}
document.getElementById('modalOverlay').onclick = function(e) {
  if (e.target === this) closeModal();
};
function showToast(msg) {
  var existing = document.querySelector('.toast');
  if (existing) existing.remove();
  var t = document.createElement('div');
  t.className = 'toast';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(function() { t.remove(); }, 3000);
}
document.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>