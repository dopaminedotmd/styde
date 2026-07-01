```html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Cognitive Personalization Engine</title>
<style>
:root {
  --bg: #f5f5f7;
  --surface: #ffffff;
  --text: #1d1d1f;
  --text-secondary: #6e6e73;
  --border: #d2d2d7;
  --accent: #0071e3;
  --accent-hover: #0060c0;
  --shadow: 0 2px 8px rgba(0,0,0,0.08);
  --radius: 10px;
  --spacing: 16px;
  --font-size: 14px;
  --density-mult: 1;
}
.dark {
  --bg: #1c1c1e;
  --surface: #2c2c2e;
  --text: #f5f5f7;
  --text-secondary: #98989d;
  --border: #48484a;
  --shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.compact { --spacing: 8px; --font-size: 12px; }
.comfortable { --spacing: 20px; --font-size: 15px; }
.font-small { --font-size: 12px; }
.font-medium { --font-size: 14px; }
.font-large { --font-size: 16px; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  font-size: var(--font-size);
  transition: background 0.3s, color 0.3s;
  min-height: 100vh;
}
button, select, input {
  font-family: inherit;
  font-size: inherit;
}
.app-header {
  display: flex;
  align-items: center;
  gap: var(--spacing);
  padding: var(--spacing);
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  box-shadow: var(--shadow);
  flex-wrap: wrap;
  position: sticky;
  top: 0;
  z-index: 100;
}
.app-header h1 {
  font-size: calc(var(--font-size) * 1.4);
  font-weight: 600;
  margin-right: auto;
  white-space: nowrap;
}
.header-group {
  display: flex;
  align-items: center;
  gap: 6px;
}
.header-group label {
  font-size: calc(var(--font-size) * 0.85);
  color: var(--text-secondary);
}
.btn {
  padding: 6px 14px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
  font-size: calc(var(--font-size) * 0.9);
  white-space: nowrap;
  transition: all 0.15s;
}
.btn:hover { background: var(--accent); color: white; border-color: var(--accent); }
.btn-accent { background: var(--accent); color: white; border-color: var(--accent); }
.btn-accent:hover { background: var(--accent-hover); }
.btn-sm { padding: 4px 10px; font-size: calc(var(--font-size) * 0.8); }
.btn-danger { color: #ff453a; border-color: #ff453a; }
.btn-danger:hover { background: #ff453a; color: white; }
select, input[type=text], input[type=color] {
  padding: 6px 10px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--surface);
  color: var(--text);
  font-size: calc(var(--font-size) * 0.9);
}
input[type=color] { width: 36px; height: 32px; padding: 2px; cursor: pointer; }
input[type=text] { min-width: 140px; }
.main-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: var(--spacing);
  padding: var(--spacing);
  max-width: 1400px;
  margin: 0 auto;
}
.main-content { min-width: 0; }
.sidebar { min-width: 0; }
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--spacing);
}
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: var(--spacing);
  box-shadow: var(--shadow);
  transition: box-shadow 0.2s;
}
.card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.12); }
.card h3 {
  font-size: calc(var(--font-size) * 1.1);
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card .value {
  font-size: calc(var(--font-size) * 2);
  font-weight: 700;
  color: var(--accent);
}
.card .sub {
  font-size: calc(var(--font-size) * 0.8);
  color: var(--text-secondary);
}
.card .bar {
  height: 6px;
  background: var(--border);
  border-radius: 3px;
  margin-top: 8px;
  overflow: hidden;
}
.card .bar-fill {
  height: 100%;
  background: var(--accent);
  border-radius: 3px;
  transition: width 0.5s;
}
.bookmark-btn {
  cursor: pointer;
  opacity: 0.5;
  font-size: calc(var(--font-size) * 1.2);
  transition: opacity 0.15s;
  background: none;
  border: none;
  color: var(--text);
}
.bookmark-btn:hover { opacity: 1; }
.bookmark-btn.active { opacity: 1; color: #ffd60a; }
.section-title {
  font-size: calc(var(--font-size) * 1.2);
  font-weight: 600;
  margin: var(--spacing) 0 calc(var(--spacing) * 0.5);
  padding-bottom: 6px;
  border-bottom: 1px solid var(--border);
}
.sidebar-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: var(--spacing);
  margin-bottom: var(--spacing);
  box-shadow: var(--shadow);
}
.sidebar-panel h3 {
  font-size: calc(var(--font-size) * 1.05);
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.sidebar-panel ul {
  list-style: none;
}
.sidebar-panel li {
  padding: 6px 0;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 4px;
  font-size: calc(var(--font-size) * 0.9);
}
.sidebar-panel li:last-child { border-bottom: none; }
.sidebar-panel .item-name { flex: 1; cursor: pointer; }
.sidebar-panel .item-name:hover { color: var(--accent); }
.toast-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.toast {
  padding: 12px 20px;
  border-radius: 8px;
  background: var(--surface);
  border: 1px solid var(--border);
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  animation: slideIn 0.3s ease;
  font-size: calc(var(--font-size) * 0.9);
  max-width: 320px;
}
.toast.info { border-left: 4px solid var(--accent); }
.toast.warn { border-left: 4px solid #ff9f0a; }
@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: calc(var(--spacing) * 1.5);
  min-width: 340px;
  max-width: 480px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.2);
}
.modal h2 { margin-bottom: 12px; }
.modal .field { margin-bottom: 10px; }
.modal .field label { display: block; font-size: calc(var(--font-size) * 0.85); color: var(--text-secondary); margin-bottom: 4px; }
.modal .field input, .modal .field select { width: 100%; }
.modal .actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px; }
.alert-config-item { margin-bottom: 10px; padding: 8px; border: 1px solid var(--border); border-radius: 6px; }
.alert-config-item .row { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
.alert-config-item label { font-size: calc(var(--font-size) * 0.8); color: var(--text-secondary); }
#mute-schedule { margin-top: 8px; padding: 8px; background: var(--bg); border-radius: 6px; }
#mute-schedule .row { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-bottom: 4px; }
.stat-row { display: flex; gap: var(--spacing); flex-wrap: wrap; margin-bottom: var(--spacing); }
.stat-item { font-size: calc(var(--font-size) * 0.8); color: var(--text-secondary); }
@media (max-width: 860px) {
  .main-layout { grid-template-columns: 1fr; }
  .app-header { flex-direction: column; align-items: stretch; }
  .app-header h1 { margin-right: 0; }
}
</style>
</head>
<body>
<div class=app-header id=app-header>
  <h1>Cognitive Personalization Engine</h1>
  <div class=header-group>
    <label>User:</label>
    <select id=user-select></select>
    <button class="btn btn-sm" onclick=showModal('user-add')>+</button>
    <button class="btn btn-sm btn-danger" onclick=showModal('user-del')>-</button>
  </div>
  <div class=header-group>
    <label>Theme:</label>
    <select id=theme-select>
      <option value=light>Light</option>
      <option value=dark>Dark</option>
    </select>
  </div>
  <div class=header-group>
    <label>Accent:</label>
    <input type=color id=accent-picker value=#0071e3>
  </div>
  <div class=header-group>
    <label>Density:</label>
    <select id=density-select>
      <option value=comfortable>Comfortable</option>
      <option value=compact>Compact</option>
    </select>
  </div>
  <div class=header-group>
    <label>Font:</label>
    <select id=font-scale>
      <option value=small>Small</option>
      <option value=medium selected>Medium</option>
      <option value=large>Large</option>
    </select>
  </div>
  <div class=header-group>
    <label>View:</label>
    <select id=view-select>
      <option value=__default__>Default</option>
    </select>
    <button class="btn btn-sm" onclick=showModal('view-save')>Save</button>
    <button class="btn btn-sm btn-danger" onclick=showModal('view-del')>Del</button>
  </div>
</div>
<div class=main-layout>
  <div class=main-content>
    <div class=stat-row id=usage-stats></div>
    <div class="section-title">Dashboard Metrics</div>
    <div class=dashboard-grid id=metrics-grid></div>
    <div class="section-title">Alert Configuration</div>
    <div id=alert-config-area></div>
  </div>
  <div class=sidebar>
    <div class=sidebar-panel>
      <h3>Bookmarks <button class="btn btn-sm btn-accent" onclick=showModal('bookmark-add')>+</button></h3>
      <ul id=bookmark-list></ul>
    </div>
    <div class=sidebar-panel>
      <h3>Saved Views</h3>
      <ul id=saved-views-list></ul>
    </div>
    <div class=sidebar-panel>
      <h3>Usage History</h3>
      <ul id=usage-list></ul>
    </div>
  </div>
</div>
<div class=toast-container id=toast-container></div>
<div id=modal-area></div>
<script>
(function(){
'use strict';
/* ---------- data layer ---------- */
const DEFAULT_METRICS = [
  { id:'revenue', label:'Revenue', value:84700, unit:'kr', min:0, max:200000, bookmarkable:true },
  { id:'users', label:'Active Users', value:1823, unit:'', min:0, max:5000, bookmarkable:true },
  { id:'conversion', label:'Conversion Rate', value:3.4, unit:'%', min:0, max:15, bookmarkable:true },
  { id:'orders', label:'Orders', value:312, unit:'', min:0, max:800, bookmarkable:true },
  { id:'churn', label:'Churn Rate', value:1.2, unit:'%', min:0, max:10, bookmarkable:true },
  { id:'satisfaction', label:'Satisfaction', value:4.2, unit:'/5', min:0, max:5, bookmarkable:true },
];
const STORE_KEY = 'cpe_store';
function newUserId(){ return 'u_' + Date.now() + '_' + Math.random().toString(36).slice(2,6); }
function freshProfile(name){
  return {
    id: newUserId(),
    name: name || 'New User',
    createdAt: Date.now(),
    theme: 'light',
    accentColor: '#0071e3',
    density: 'comfortable',
    fontScale: 'medium',
    views: [],
    bookmarks: [],
    alerts: DEFAULT_METRICS.map(function(m){ return { metricId:m.id, enabled:true, threshold:m.max * 0.8, direction:'above', notify:'toast' }; }),
    muteSchedule: { enabled:false, start:'22:00', end:'07:00' },
    usage: [],
    metrics: JSON.parse(JSON.stringify(DEFAULT_METRICS)),
  };
}
function loadStore(){
  var raw = localStorage.getItem(STORE_KEY);
  if(raw) try { return JSON.parse(raw); } catch(e){}
  return null;
}
function saveStore(s){ localStorage.setItem(STORE_KEY, JSON.stringify(s)); }
function getStore(){
  var s = loadStore();
  if(!s){
    s = { profiles:[], activeUserId:null, nextViewId:1 };
    var p = freshProfile('Default User');
    s.profiles.push(p);
    s.activeUserId = p.id;
    saveStore(s);
  }
  return s;
}
/* ---------- helpers ---------- */
function activeUser(s){ return s.profiles.find(function(p){ return p.id === s.activeUserId; }); }
function setActiveUser(s, id){ s.activeUserId = id; saveStore(s); }
function metricValue(profile, metricId){
  var m = profile.metrics.find(function(x){ return x.id === metricId; });
  return m ? m.value : 0;
}
function addUsage(profile, action){
  var entry = { action:action, at:Date.now() };
  profile.usage.unshift(entry);
  if(profile.usage.length > 50) profile.usage.length = 50;
}
/* ---------- modals ---------- */
function showModal(type, data){
  var area = document.getElementById('modal-area');
  var h = '';
  if(type === 'user-add'){
    h = '<div class=modal-overlay onclick=closeModal(event)><div class=modal onclick=event.stopPropagation()><h2>Add User</h2><div class=field><label>Name</label><input type=text id=modal-user-name placeholder="User name"></div><div class=actions><button class=btn onclick=closeModal()>Cancel</button><button class="btn btn-accent" onclick=doAddUser()>Add</button></div></div></div>';
  } else if(type === 'user-del'){
    h = '<div class=modal-overlay onclick=closeModal(event)><div class=modal onclick=event.stopPropagation()><h2>Delete Current User</h2><p style="margin-bottom:8px;color:var(--text-secondary)">This will permanently remove the current user and all their data.</p><div class=actions><button class=btn onclick=closeModal()>Cancel</button><button class="btn btn-danger" onclick=doDeleteUser()>Delete</button></div></div></div>';
  } else if(type === 'view-save'){
    h = '<div class=modal-overlay onclick=closeModal(event)><div class=modal onclick=event.stopPropagation()><h2>Save Current View</h2><div class=field><label>View Name</label><input type=text id=modal-view-name placeholder="e.g., Weekly Overview"></div><div class=actions><button class=btn onclick=closeModal()>Cancel</button><button class="btn btn-accent" onclick=doSaveView()>Save</button></div></div></div>';
  } else if(type === 'view-del'){
    var s = getStore();
    var u = activeUser(s);
    var viewOpts = (u.views||[]).map(function(v){ return '<option value="'+v.id+'">'+v.name+'</option>'; }).join('');
    h = '<div class=modal-overlay onclick=closeModal(event)><div class=modal onclick=event.stopPropagation()><h2>Delete Saved View</h2>' +
      (viewOpts ? '<div class=field><label>View</label><select id=modal-view-del-select>'+viewOpts+'</select></div><div class=actions><button class=btn onclick=closeModal()>Cancel</button><button class="btn btn-danger" onclick=doDeleteView()>Delete</button></div>' :
      '<p style="color:var(--text-secondary)">No saved views.</p><div class=actions><button class=btn onclick=closeModal()>Close</button></div>') +
      '</div></div>';
  } else if(type === 'bookmark-add'){
    h = '<div class=modal-overlay onclick=closeModal(event)><div class=modal onclick=event.stopPropagation()><h2>Add Bookmark</h2><div class=field><label>Metric</label><select id=modal-bm-metric>' +
      DEFAULT_METRICS.map(function(m){ return '<option value="'+m.id+'">'+m.label+'</option>'; }).join('') +
      '</select></div><div class=field><label>Annotation</label><input type=text id=modal-bm-annotation placeholder="Why this matters"></div><div class=actions><button class=btn onclick=closeModal()>Cancel</button><button class="btn btn-accent" onclick=doAddBookmark()>Add</button></div></div></div>';
  }
  area.innerHTML = h;
}
function closeModal(e){
  if(e && e.target !== e.currentTarget) return;
  document.getElementById('modal-area').innerHTML = '';
}
function doAddUser(){
  var name = document.getElementById('modal-user-name').value.trim() || 'User ' + (getStore().profiles.length + 1);
  var s = getStore();
  var p = freshProfile(name);
  s.profiles.push(p);
  var count = s.profiles.length;
  s.activeUserId = p.id;
  saveStore(s);
  closeModal();
  render();
  toast('User "'+name+'" added', 'info');
}
function doDeleteUser(){
  var s = getStore();
  if(s.profiles.length <= 1){ closeModal(); toast('Cannot delete the last user', 'warn'); return; }
  var idx = s.profiles.findIndex(function(p){ return p.id === s.activeUserId; });
  s.profiles.splice(idx,1);
  s.activeUserId = s.profiles[0].id;
  saveStore(s);
  closeModal();
  render();
  toast('User deleted', 'info');
}
function doSaveView(){
  var name = document.getElementById('modal-view-name').value.trim();
  if(!name){ toast('View name required', 'warn'); return; }
  var s = getStore();
  var u = activeUser(s);
  var currentMetrics = u.metrics.map(function(m){ return { id:m.id, value:m.value }; });
  s.nextViewId = s.nextViewId || 1;
  var view = { id:'v_'+s.nextViewId, name:name, savedAt:Date.now(), metricValues:currentMetrics, theme:u.theme, accentColor:u.accentColor, density:u.density, fontScale:u.fontScale };
  s.nextViewId++;
  u.views = u.views || [];
  u.views.push(view);
  addUsage(u, 'Saved view: '+name);
  saveStore(s);
  closeModal();
  render();
  toast('View "'+name+'" saved', 'info');
}
function doDeleteView(){
  var sel = document.getElementById('modal-view-del-select');
  if(!sel) return;
  var vid = sel.value;
  var s = getStore();
  var u = activeUser(s);
  u.views = (u.views||[]).filter(function(v){ return v.id !== vid; });
  saveStore(s);
  closeModal();
  render();
  toast('View deleted', 'info');
}
function doAddBookmark(){
  var mid = document.getElementById('modal-bm-metric').value;
  var ann = document.getElementById('modal-bm-annotation').value.trim() || 'Bookmarked metric';
  var s = getStore();
  var u = activeUser(s);
  var m = u.metrics.find(function(x){ return x.id === mid; });
  var val = m ? m.value : 0;
  var bm = { id:'bm_'+Date.now(), metricId:mid, value:val, annotation:ann, createdAt:Date.now() };
  u.bookmarks = u.bookmarks || [];
  u.bookmarks.push(bm);
  addUsage(u, 'Bookmarked '+mid+': '+ann);
  saveStore(s);
  closeModal();
  render();
  toast('Bookmark added', 'info');
}
function removeBookmark(bmid){
  var s = getStore();
  var u = activeUser(s);
  u.bookmarks = (u.bookmarks||[]).filter(function(b){ return b.id !== bmid; });
  saveStore(s);
  render();
}
function restoreView(vid){
  var s = getStore();
  var u = activeUser(s);
  var v = (u.views||[]).find(function(x){ return x.id === vid; });
  if(!v){ toast('View not found', 'warn'); return; }
  v.metricValues.forEach(function(mv){
    var t = u.metrics.find(function(x){ return x.id === mv.id; });
    if(t) t.value = mv.value;
  });
  if(v.theme) u.theme = v.theme;
  if(v.accentColor) u.accentColor = v.accentColor;
  if(v.density) u.density = v.density;
  if(v.fontScale) u.fontScale = v.fontScale;
  addUsage(u, 'Restored view: '+v.name);
  saveStore(s);
  render();
  toast('View "'+v.name+'" restored', 'info');
}
function restoreBookmark(bmid){
  var s = getStore();
  var u = activeUser(s);
  var bm = (u.bookmarks||[]).find(function(b){ return b.id === bmid; });
  if(!bm){ toast('Bookmark not found', 'warn'); return; }
  var m = u.metrics.find(function(x){ return x.id === bm.metricId; });
  if(m){ m.value = bm.value; }
  addUsage(u, 'Restored bookmark: '+bm.annotation);
  saveStore(s);
  render();
  toast('Bookmark restored', 'info');
}
function toast(msg, type){
  type = type || 'info';
  var c = document.getElementById('toast-container');
  var el = document.createElement('div');
  el.className = 'toast ' + type;
  el.textContent = msg;
  c.appendChild(el);
  setTimeout(function(){ el.style.opacity = '0'; el.style.transition = 'opacity 0.3s'; setTimeout(function(){ el.remove(); }, 300); }, 3000);
}
/* ---------- event handlers ---------- */
function onUserChange(){
  var sel = document.getElementById('user-select');
  var s = getStore();
  var p = s.profiles.find(function(x){ return x.name === sel.value; });
  if(p){ s.activeUserId = p.id; saveStore(s); render(); }
}
function onThemeChange(){
  var v = document.getElementById('theme-select').value;
  var s = getStore();
  var u = activeUser(s);
  u.theme = v;
  addUsage(u, 'Theme: '+v);
  saveStore(s);
  applyTheme(u);
}
function onAccentChange(){
  var v = document.getElementById('accent-picker').value;
  var s = getStore();
  var u = activeUser(s);
  u.accentColor = v;
  addUsage(u, 'Accent: '+v);
  saveStore(s);
  applyTheme(u);
}
function onDensityChange(){
  var v = document.getElementById('density-select').value;
  var s = getStore();
  var u = activeUser(s);
  u.density = v;
  saveStore(s);
  applyTheme(u);
}
function onFontChange(){
  var v = document.getElementById('font-scale').value;
  var s = getStore();
  var u = activeUser(s);
  u.fontScale = v;
  saveStore(s);
  applyTheme(u);
}
function onViewSelect(){
  var sel = document.getElementById('view-select');
  var vid = sel.value;
  if(vid && vid !== '__default__') restoreView(vid);
}
/* ---------- render ---------- */
function applyTheme(u){
  var root = document.documentElement;
  root.classList.toggle('dark', u.theme === 'dark');
  root.classList.toggle('compact', u.density === 'compact');
  root.classList.toggle('comfortable', u.density === 'comfortable');
  root.classList.toggle('font-small', u.fontScale === 'small');
  root.classList.toggle('font-medium', u.fontScale === 'medium');
  root.classList.toggle('font-large', u.fontScale === 'large');
  root.style.setProperty('--accent', u.accentColor);
  var r = parseInt(u.accentColor.slice(1,3),16);
  var g = parseInt(u.accentColor.slice(3,5),16);
  var b = parseInt(u.accentColor.slice(5,7),16);
  root.style.setProperty('--accent-hover', 'rgb('+Math.max(0,r-30)+','+Math.max(0,g-30)+','+Math.max(0,b-30)+')');
}
function render(){
  var s = getStore();
  var u = activeUser(s);
  if(!u) { s.activeUserId = s.profiles[0].id; u = s.profiles[0]; saveStore(s); }
  applyTheme(u);
  /* user select */
  var usel = document.getElementById('user-select');
  usel.innerHTML = s.profiles.map(function(p){ return '<option value="'+p.name+'"'+(p.id===u.id?' selected':'')+'>'+p.name+'</option>'; }).join('');
  /* theme controls */
  document.getElementById('theme-select').value = u.theme || 'light';
  document.getElementById('accent-picker').value = u.accentColor || '#0071e3';
  document.getElementById('density-select').value = u.density || 'comfortable';
  document.getElementById('font-scale').value = u.fontScale || 'medium';
  /* view select */
  var vsel = document.getElementById('view-select');
  var currentVid = vsel.value;
  vsel.innerHTML = '<option value=__default__>Default</option>' + (u.views||[]).map(function(v){ return '<option value="'+v.id+'"'+(v.id===currentVid?' selected':'')+'>'+v.name+'</option>'; }).join('');
  /* usage stats */
  var us = document.getElementById('usage-stats');
  us.innerHTML = '<div class=stat-item>User: <b>'+u.name+'</b></div><div class=stat-item>Views saved: <b>'+(u.views||[]).length+'</b></div><div class=stat-item>Bookmarks: <b>'+(u.bookmarks||[]).length+'</b></div><div class=stat-item>Actions: <b>'+(u.usage||[]).length+'</b></div>';
  /* metrics grid */
  var grid = document.getElementById('metrics-grid');
  grid.innerHTML = u.metrics.map(function(m){
    var pct = m.max > 0 ? Math.min(100, (m.value / m.max) * 100) : 0;
    var isBmed = (u.bookmarks||[]).some(function(b){ return b.metricId === m.id; });
    return '<div class=card>' +
      '<h3><span>'+m.label+'</span>' +
      (m.bookmarkable ? '<button class="bookmark-btn'+(isBmed?' active':'')+'" onclick=showModal("bookmark-add") title="Bookmark this metric">&#9733;</button>' : '') +
      '</h3>' +
      '<div class=value>'+m.value.toLocaleString()+(m.unit?' '+m.unit:'')+'</div>' +
      '<div class=sub>Target: '+m.max.toLocaleString()+m.unit+'</div>' +
      '<div class=bar><div class=bar-fill style="width:'+pct+'%"></div></div>' +
      '</div>';
  }).join('');
  /* alert config */
  var ac = document.getElementById('alert-config-area');
  ac.innerHTML = '<div id=mute-schedule><div class=row><label><input type=checkbox id=mute-enabled '+(u.muteSchedule.enabled?'checked':'')+' onchange=onMuteToggle()> Mute notifications</label></div>' +
    '<div class=row><label>From</label><input type=time id=mute-start value="'+(u.muteSchedule.start||'22:00')+'" onchange=onMuteChange()>' +
    '<label>To</label><input type=time id=mute-end value="'+(u.muteSchedule.end||'07:00')+'" onchange=onMuteChange()></div></div>' +
    (u.alerts||[]).map(function(a){
      var m = u.metrics.find(function(x){ return x.id === a.metricId; });
      return '<div class=alert-config-item><div class=row>' +
        '<label><input type=checkbox '+(a.enabled?'checked':'')+' onchange="onAlertToggle(\''+a.metricId+'\')"> '+(m?m.label:a.metricId)+'</label>' +
        '<label>Threshold</label><input type=number value="'+a.threshold+'" style="width:80px" onchange="onAlertThreshold(\''+a.metricId+'\',this.value)">' +
        '<label>Direction</label><select onchange="onAlertDirection(\''+a.metricId+'\',this.value)"><option value=above'+(a.direction==='above'?' selected':'')+'>Above</option><option value=below'+(a.direction==='below'?' selected':'')+'>Below</option></select>' +
        '<label>Notify</label><select onchange="onAlertNotify(\''+a.metricId+'\',this.value)"><option value=toast'+(a.notify==='toast'?' selected':'')+'>Toast</option><option value=banner'+(a.notify==='banner'?' selected':'')+'>Banner</option><option value=sound'+(a.notify==='sound'?' selected':'')+'>Sound</option></select>' +
        '</div></div>';
    }).join('');
  /* bookmark list */
  var bl = document.getElementById('bookmark-list');
  bl.innerHTML = (u.bookmarks||[]).length === 0 ? '<li style="color:var(--text-secondary)">No bookmarks yet</li>' :
    (u.bookmarks||[]).map(function(b){
      var m = u.metrics.find(function(x){ return x.id === b.metricId; });
      return '<li><span class=item-name onclick="restoreBookmark(\''+b.id+'\')" title="Click to restore">'+(m?m.label:b.metricId)+': '+b.value.toLocaleString()+'</span><span style="font-size:calc(var(--font-size)*0.75);color:var(--text-secondary);flex:0 0 auto">'+b.annotation+'</span><button class="btn btn-sm btn-danger" onclick="removeBookmark(\''+b.id+'\')">x</button></li>';
    }).join('');
  /* saved views list */
  var svl = document.getElementById('saved-views-list');
  svl.innerHTML = (u.views||[]).length === 0 ? '<li style="color:var(--text-secondary)">No saved views</li>' :
    (u.views||[]).map(function(v){
      return '<li><span class=item-name onclick="restoreView(\''+v.id+'\')" title="Click to restore">'+v.name+'</span><span style="font-size:calc(var(--font-size)*0.75);color:var(--text-secondary)">'+new Date(v.savedAt).toLocaleDateString()+'</span></li>';
    }).join('');
  /* usage list */
  var ul = document.getElementById('usage-list');
  ul.innerHTML = (u.usage||[]).length === 0 ? '<li style="color:var(--text-secondary)">No activity yet</li>' :
    (u.usage||[]).slice(0,10).map(function(entry){
      return '<li><span style="font-size:calc(var(--font-size)*0.75);color:var(--text-secondary)">'+new Date(entry.at).toLocaleString()+'</span> '+entry.action+'</li>';
    }).join('');
  /* check alerts */
  (u.alerts||[]).forEach(function(a){
    if(!a.enabled || u.muteSchedule.enabled) return;
    var m = u.metrics.find(function(x){ return x.id === a.metricId; });
    if(!m) return;
    var triggered = a.direction === 'above' ? m.value > a.threshold : m.value < a.threshold;
    if(triggered){
      var msg = (m?m.label:a.metricId)+' ('+m.value+') '+(a.direction==='above'?'exceeded':'fell below')+' threshold ('+a.threshold+')';
      if(a.notify === 'sound'){
        try { var ctx = new (window.AudioContext||window.webkitAudioContext)(); var osc = ctx.createOscillator(); osc.connect(ctx.destination); osc.frequency.value=880; osc.start(); setTimeout(function(){ osc.stop(); }, 200); } catch(e){}
      }
      toast(msg, 'warn');
    }
  });
  /* progressive personalization: sort views by usage recency */
  var usageViews = (u.usage||[]).filter(function(e){ return e.action.indexOf('Saved view:')===0 || e.action.indexOf('Restored view:')===0; });
  if(usageViews.length > 3){
    var recent = usageViews.slice(0,5).map(function(e){ return e.action.replace(/^(Saved|Restored) view: /,''); });
    var opts = vsel.querySelectorAll('option');
    var scored = [];
    opts.forEach(function(o){
      if(o.value === '__default__') return;
      var score = recent.indexOf(o.textContent);
      scored.push({ el:o, score: score >= 0 ? recent.length - score : 0 });
    });
    scored.sort(function(a,b){ return b.score - a.score; });
    scored.forEach(function(s){ vsel.appendChild(s.el); });
  }
}
/* ---------- alert handlers ---------- */
function onAlertToggle(mid){
  var s = getStore(); var u = activeUser(s); var a = (u.alerts||[]).find(function(x){ return x.metricId === mid; }); if(a) a.enabled = !a.enabled; saveStore(s);
}
function onAlertThreshold(mid, val){
  var s = getStore(); var u = activeUser(s); var a = (u.alerts||[]).find(function(x){ return x.metricId === mid; }); if(a) a.threshold = parseFloat(val) || 0; saveStore(s);
}
function onAlertDirection(mid, val){
  var s = getStore(); var u = activeUser(s); var a = (u.alerts||[]).find(function(x){ return x.metricId === mid; }); if(a) a.direction = val; saveStore(s);
}
function onAlertNotify(mid, val){
  var s = getStore(); var u = activeUser(s); var a = (u.alerts||[]).find(function(x){ return x.metricId === mid; }); if(a) a.notify = val; saveStore(s);
}
function onMuteToggle(){
  var s = getStore(); var u = activeUser(s); u.muteSchedule.enabled = document.getElementById('mute-enabled').checked; saveStore(s);
}
function onMuteChange(){
  var s = getStore(); var u = activeUser(s); u.muteSchedule.start = document.getElementById('mute-start').value; u.muteSchedule.end = document.getElementById('mute-end').value; saveStore(s);
}
/* ---------- init ---------- */
document.getElementById('user-select').addEventListener('change', onUserChange);
document.getElementById('theme-select').addEventListener('change', onThemeChange);
document.getElementById('accent-picker').addEventListener('input', onAccentChange);
document.getElementById('density-select').addEventListener('change', onDensityChange);
document.getElementById('font-scale').addEventListener('change', onFontChange);
document.getElementById('view-select').addEventListener('change', onViewSelect);
render();
})();
</script>
</body>
</html>
```