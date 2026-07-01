```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Personal Dashboard</title>
<style>
:root{--bg:#f5f7fa;--card-bg:#fff;--text:#1a1a2e;--accent:#4361ee;--accent-hover:#3651d4;--border:#e0e3eb;--shadow:0 2px 8px rgba(0,0,0,.08);--radius:8px;--font-size:14px;--density:1}
.dark{--bg:#1a1a2e;--card-bg:#16213e;--text:#e0e3eb;--accent:#4cc9f0;--accent-hover:#3ab8df;--border:#2a2a4a;--shadow:0 2px 8px rgba(0,0,0,.3)}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);font-size:var(--font-size);line-height:1.5;padding:20px;transition:background .3s,color .3s}
.layout{display:grid;grid-template-columns:280px 1fr;gap:20px;max-width:1400px;margin:0 auto}
.topbar{grid-column:1/-1;display:flex;align-items:center;gap:12px;padding:12px 16px;background:var(--card-bg);border-radius:var(--radius);box-shadow:var(--shadow);flex-wrap:wrap}
.topbar select,.topbar button,.topbar input{font-size:13px;padding:6px 12px;border:1px solid var(--border);border-radius:var(--radius);background:var(--bg);color:var(--text);cursor:pointer}
.topbar input[type=color]{width:32px;height:32px;padding:2px;border-radius:50%;cursor:pointer}
.topbar label{font-size:12px;opacity:.7}
.sidebar{background:var(--card-bg);border-radius:var(--radius);box-shadow:var(--shadow);padding:16px;display:flex;flex-direction:column;gap:16px}
.sidebar h3{font-size:13px;text-transform:uppercase;letter-spacing:.5px;opacity:.6;margin-bottom:6px}
.sidebar button,.sidebar select{width:100%;padding:8px 12px;border:1px solid var(--border);border-radius:var(--radius);background:var(--bg);color:var(--text);cursor:pointer;text-align:left;font-size:13px}
.sidebar button:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
.main{display:flex;flex-direction:column;gap:16px}
.metrics{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.card{background:var(--card-bg);border-radius:var(--radius);box-shadow:var(--shadow);padding:16px;transition:transform .15s,box-shadow .15s;position:relative}
.card:hover{transform:translateY(-2px);box-shadow:0 4px 16px rgba(0,0,0,.12)}
.card .val{font-size:28px;font-weight:700;margin:4px 0 2px}
.card .lbl{font-size:12px;opacity:.6;margin-bottom:4px}
.card .meta{font-size:11px;opacity:.4;display:flex;gap:8px;flex-wrap:wrap}
.card .actions{position:absolute;top:8px;right:8px;display:flex;gap:4px;opacity:0;transition:opacity .2s}
.card:hover .actions{opacity:1}
.card .actions button{background:var(--bg);border:1px solid var(--border);border-radius:4px;padding:2px 6px;font-size:11px;cursor:pointer;color:var(--text)}
.card .actions button:hover{background:var(--accent);color:#fff}
.alert-badge{font-size:10px;padding:2px 6px;border-radius:10px;background:#e63946;color:#fff;margin-left:6px;cursor:pointer}
.bookmark-star{color:#f4a261;cursor:pointer;font-size:14px;margin-left:4px;user-select:none}
.bookmark-star.active{color:#e9c46a}
.save-view-input{display:flex;gap:6px;margin-top:4px}
.save-view-input input{flex:1;padding:6px 8px;border:1px solid var(--border);border-radius:var(--radius);font-size:12px;background:var(--bg);color:var(--text)}
.save-view-input button{padding:6px 10px}
.modal-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;z-index:1000}
.modal{background:var(--card-bg);border-radius:var(--radius);padding:24px;min-width:340px;max-width:480px;box-shadow:0 8px 32px rgba(0,0,0,.2)}
.modal h3{margin-bottom:12px}
.modal textarea{width:100%;min-height:60px;padding:8px;border:1px solid var(--border);border-radius:var(--radius);background:var(--bg);color:var(--text);resize:vertical;font-size:13px;margin-bottom:8px}
.modal .modal-actions{display:flex;gap:8px;justify-content:flex-end;margin-top:12px}
.modal .modal-actions button{padding:6px 14px;border:1px solid var(--border);border-radius:var(--radius);cursor:pointer;font-size:13px;background:var(--bg);color:var(--text)}
.modal .modal-actions button.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.hidden{display:none!important}
.density-compact{--density:.85;--font-size:12px;padding:12px}
.density-compact .card{padding:10px}
.density-compact .card .val{font-size:22px}
.density-spacious{--density:1.15;--font-size:16px;padding:28px}
.density-spacious .card{padding:22px}
</style>
</head>
<body>
<div class="layout" id="app">
<div class="topbar">
<span style="font-weight:700;font-size:16px">Dashboard</span>
<label>User:</label>
<select id="userSelect"></select>
<label>View:</label>
<select id="viewSelect"><option value="">-- active --</option></select>
<label>Theme:</label>
<select id="themeSelect"><option value="light">Light</option><option value="dark">Dark</option></select>
<label>Accent:</label>
<input type="color" id="accentPicker" value="#4361ee">
<label>Density:</label>
<select id="densitySelect"><option value="normal">Normal</option><option value="compact">Compact</option><option value="spacious">Spacious</option></select>
<label>Font:</label>
<select id="fontSelect"><option value="14">14px</option><option value="12">12px</option><option value="16">16px</option><option value="18">18px</option></select>
<button id="addMetricBtn">+ Add Metric</button>
</div>
<div class="sidebar">
<div>
<h3>Users</h3>
<div id="userList"></div>
<button id="addUserBtn">+ New User</button>
</div>
<div>
<h3>Saved Views</h3>
<div id="viewList"></div>
<div class="save-view-input"><input type="text" id="viewNameInput" placeholder="View name..."><button id="saveViewBtn">Save</button></div>
</div>
<div>
<h3>Bookmarks</h3>
<div id="bookmarkList"></div>
</div>
<div>
<h3>Alerts</h3>
<div id="alertList"></div>
<button id="addAlertBtn">+ Threshold Alert</button>
</div>
</div>
<div class="main">
<div class="metrics" id="metricsGrid"></div>
</div>
</div>
<div id="modalContainer" class="hidden"></div>
<script>
(function() {
'use strict';
var DB_KEY = 'dash_profiles';
var STOCK_METRICS = [
{id:'m1',label:'Revenue',value:'$48,290',change:'+12.3%',up:true,cat:'finance'},
{id:'m2',label:'New Users',value:'1,842',change:'+8.7%',up:true,cat:'growth'},
{id:'m3',label:'Avg Session',value:'4m 32s',change:'-2.1%',up:false,cat:'engagement'},
{id:'m4',label:'Conversion',value:'3.21%',change:'+0.4pp',up:true,cat:'growth'},
{id:'m5',label:'Churn Rate',value:'1.8%',change:'-0.3pp',up:true,cat:'retention'},
{id:'m6',label:'Support Tickets',value:'127',change:'-5%',up:true,cat:'support'},
{id:'m7',label:'API Latency',value:'245ms',change:'+12ms',up:false,cat:'perf'},
{id:'m8',label:'Active Users',value:'6,433',change:'+2.1%',up:true,cat:'engagement'}
];
function defaultProfile(name) {
return {
name:name,
theme:'light',
accent:'#4361ee',
density:'normal',
fontSize:14,
metricIds:STOCK_METRICS.map(function(m){return m.id}),
views:[],
bookmarks:{},
alerts:{},
history:[]
};
}
function loadProfiles() {
try {
var raw = localStorage.getItem(DB_KEY);
if(raw) return JSON.parse(raw);
}catch(e){}
var alice = defaultProfile('Alice');
alice.theme='dark';alice.accent='#4cc9f0';
var bob = defaultProfile('Bob');
return {users:[alice,bob],active:0};
}
function saveProfiles(data) {
localStorage.setItem(DB_KEY,JSON.stringify(data));
}
function genId() {
return '_'+Math.random().toString(36).slice(2,8);
}
var data = loadProfiles();
var currentUserIdx = data.active >= 0 && data.active < data.users.length ? data.active : 0;
var currentUser = data.users[currentUserIdx];
var metricDefs = STOCK_METRICS.slice();
function getCurrentProfile() {
return data.users[currentUserIdx];
}
function persist() {
saveProfiles(data);
}
// ----- DOM refs -----
var userSelect = document.getElementById('userSelect');
var viewSelect = document.getElementById('viewSelect');
var themeSelect = document.getElementById('themeSelect');
var accentPicker = document.getElementById('accentPicker');
var densitySelect = document.getElementById('densitySelect');
var fontSelect = document.getElementById('fontSelect');
var metricsGrid = document.getElementById('metricsGrid');
var userList = document.getElementById('userList');
var viewList = document.getElementById('viewList');
var bookmarkList = document.getElementById('bookmarkList');
var alertList = document.getElementById('alertList');
var addMetricBtn = document.getElementById('addMetricBtn');
var addUserBtn = document.getElementById('addUserBtn');
var saveViewBtn = document.getElementById('saveViewBtn');
var viewNameInput = document.getElementById('viewNameInput');
var modalContainer = document.getElementById('modalContainer');
// ----- apply theme -----
function applyTheme() {
var p = getCurrentProfile();
document.body.classList.toggle('dark',p.theme==='dark');
document.documentElement.style.setProperty('--accent',p.accent);
document.documentElement.style.setProperty('--accent-hover',adjustColor(p.accent,-20));
document.body.style.fontSize=p.fontSize+'px';
document.body.className=document.body.className.replace(/density-\w+/g,'').trim();
if(p.density!=='normal') document.body.classList.add('density-'+p.density);
if(themeSelect) themeSelect.value=p.theme;
if(accentPicker) accentPicker.value=p.accent;
if(densitySelect) densitySelect.value=p.density;
if(fontSelect) fontSelect.value=String(p.fontSize);
}
function adjustColor(hex,amt){
var c=parseInt(hex.slice(1),16);
var r=Math.max(0,Math.min(255,(c>>16)+amt));
var g=Math.max(0,Math.min(255,((c>>8)&0xFF)+amt));
var b=Math.max(0,Math.min(255,(c&0xFF)+amt));
return '#'+(r<<16|g<<8|b).toString(16).padStart(6,'0');
}
// ----- render metrics -----
function renderMetrics() {
var p = getCurrentProfile();
var ids = p.metricIds && p.metricIds.length ? p.metricIds : STOCK_METRICS.map(function(m){return m.id});
metricsGrid.innerHTML = '';
ids.forEach(function(id){
var m = metricDefs.find(function(x){return x.id===id});
if(!m) return;
var bookmarked = p.bookmarks && p.bookmarks[id];
var alertThresh = p.alerts && p.alerts[id];
var card = document.createElement('div');
card.className='card';
card.dataset.id=id;
card.innerHTML=
'<div class="lbl">'+m.label+'</div>'+
'<div class="val">'+m.value+'</div>'+
'<div class="meta">'+
'<span style="color:'+(m.up?'#2a9d8f':'#e63946')+'">'+m.change+'</span>'+
'<span style="opacity:.5">'+m.cat+'</span>'+
(alertThresh ? '<span class="alert-badge" data-alert-id="'+id+'" title="Threshold: '+alertThresh+'">!'+alertThresh+'</span>' : '')+
'<span class="bookmark-star'+(bookmarked?' active':'')+'" data-bm-id="'+id+'">'+(bookmarked?'★':'☆')+'</span>'+
'</div>'+
'<div class="actions">'+
'<button data-action="bookmark" data-id="'+id+'">'+(bookmarked?'Unbookmark':'Bookmark')+'</button>'+
'<button data-action="alert" data-id="'+id+'">Alert</button>'+
'<button data-action="remove" data-id="'+id+'">&times;</button>'+
'</div>';
metricsGrid.appendChild(card);
});
}
// ----- user list -----
function renderUsers() {
userSelect.innerHTML = '';
data.users.forEach(function(u,i){
var opt = document.createElement('option');
opt.value=i;
opt.textContent=u.name;
if(i===currentUserIdx) opt.selected=true;
userSelect.appendChild(opt);
});
userList.innerHTML = '';
data.users.forEach(function(u,i){
var btn = document.createElement('button');
btn.textContent=(i===currentUserIdx?'> ':'')+u.name+' '+(u.bookmarks?Object.keys(u.bookmarks).length:0)+'★';
btn.dataset.idx=i;
btn.addEventListener('click',function(){switchUser(i);});
userList.appendChild(btn);
});
}
function switchUser(idx) {
if(idx<0||idx>=data.users.length) return;
currentUserIdx=idx;
data.active=idx;
persist();
fullRefresh();
}
// ----- views -----
function renderViews() {
var p = getCurrentProfile();
viewSelect.innerHTML = '<option value="">-- active --</option>';
viewList.innerHTML = '';
(p.views||[]).forEach(function(v,i){
var opt = document.createElement('option');
opt.value=i;
opt.textContent=v.name;
viewSelect.appendChild(opt);
var row = document.createElement('div');
row.style.cssText='display:flex;gap:4px;margin-bottom:4px;align-items:center';
var nameSpan = document.createElement('span');
nameSpan.style.cssText='flex:1;font-size:12px;cursor:pointer';
nameSpan.textContent=v.name;
var loadBtn = document.createElement('button');
loadBtn.textContent='load';
loadBtn.style.cssText='font-size:11px;padding:2px 6px';
loadBtn.addEventListener('click',function(){loadView(i);});
var delBtn = document.createElement('button');
delBtn.textContent='x';
delBtn.style.cssText='font-size:11px;padding:2px 6px;color:#e63946';
delBtn.addEventListener('click',function(){deleteView(i);});
row.appendChild(nameSpan);
row.appendChild(loadBtn);
row.appendChild(delBtn);
viewList.appendChild(row);
});
viewSelect.addEventListener('change',function(){
var v = viewSelect.value;
if(v!=='') loadView(parseInt(v));
});
}
function saveView(name) {
if(!name.trim()) return;
var p = getCurrentProfile();
var view = {
name:name.trim(),
metricIds:(p.metricIds||[]).slice(),
layout:{}
};
if(!p.views) p.views=[];
p.views.push(view);
persist();
renderViews();
}
function loadView(idx) {
var p = getCurrentProfile();
var v = p.views&&p.views[idx];
if(!v) return;
p.metricIds = (v.metricIds||[]).slice();
persist();
fullRefresh();
}
function deleteView(idx) {
var p = getCurrentProfile();
if(!p.views) return;
p.views.splice(idx,1);
persist();
renderViews();
}
// ----- bookmarks -----
function renderBookmarks() {
var p = getCurrentProfile();
bookmarkList.innerHTML = '';
if(!p.bookmarks) {p.bookmarks={};}
var entries = Object.entries(p.bookmarks);
if(!entries.length) {
bookmarkList.innerHTML='<div style="font-size:12px;opacity:.5">No bookmarks yet</div>';
return;
}
entries.forEach(function(kv){
var id=kv[0],note=kv[1];
var m = metricDefs.find(function(x){return x.id===id});
if(!m) return;
var row = document.createElement('div');
row.style.cssText='display:flex;gap:4px;margin-bottom:4px;align-items:center';
var label = document.createElement('span');
label.style.cssText='flex:1;font-size:12px;cursor:pointer';
label.textContent=m.label+(note?'...'+(note.slice(0,20)+(note.length>20?'...':'')):'');
label.title=note||'';
var delBtn = document.createElement('button');
delBtn.textContent='x';
delBtn.style.cssText='font-size:11px;padding:2px 6px;color:#e63946';
delBtn.addEventListener('click',function(){deleteBookmark(id);});
row.appendChild(label);
row.appendChild(delBtn);
bookmarkList.appendChild(row);
});
}
function toggleBookmark(id,note) {
var p = getCurrentProfile();
if(!p.bookmarks) p.bookmarks={};
if(p.bookmarks[id]) {
delete p.bookmarks[id];
} else {
p.bookmarks[id]=note||'';
}
persist();
renderMetrics();
renderBookmarks();
}
function deleteBookmark(id) {
var p = getCurrentProfile();
if(p.bookmarks) delete p.bookmarks[id];
persist();
renderMetrics();
renderBookmarks();
}
function showBookmarkDialog(id) {
modalContainer.classList.remove('hidden');
modalContainer.innerHTML=
'<div class="modal-overlay"><div class="modal">'+
'<h3>Add Bookmark</h3>'+
'<textarea id="bmNoteInput" placeholder="Optional annotation for this metric..."></textarea>'+
'<div class="modal-actions">'+
'<button id="bmCancelBtn">Cancel</button>'+
'<button id="bmSaveBtn" class="primary">Save Bookmark</button>'+
'</div></div></div>';
document.getElementById('bmSaveBtn').addEventListener('click',function(){
var note = document.getElementById('bmNoteInput').value;
toggleBookmark(id,note);
modalContainer.classList.add('hidden');
});
document.getElementById('bmCancelBtn').addEventListener('click',function(){
modalContainer.classList.add('hidden');
});
}
// ----- alerts -----
function renderAlerts() {
var p = getCurrentProfile();
alertList.innerHTML = '';
if(!p.alerts) p.alerts={};
var entries = Object.entries(p.alerts);
if(!entries.length) {
alertList.innerHTML='<div style="font-size:12px;opacity:.5">No alerts set</div>';
return;
}
entries.forEach(function(kv){
var id=kv[0],thresh=kv[1];
var m = metricDefs.find(function(x){return x.id===id});
if(!m) return;
var row = document.createElement('div');
row.style.cssText='display:flex;gap:4px;margin-bottom:4px;align-items:center';
var label = document.createElement('span');
label.style.cssText='flex:1;font-size:12px';
label.textContent=m.label+' > '+thresh;
var delBtn = document.createElement('button');
delBtn.textContent='x';
delBtn.style.cssText='font-size:11px;padding:2px 6px;color:#e63946';
delBtn.addEventListener('click',function(){deleteAlert(id);});
row.appendChild(label);
row.appendChild(delBtn);
alertList.appendChild(row);
});
}
function setAlert(id,threshold) {
var p = getCurrentProfile();
if(!p.alerts) p.alerts={};
p.alerts[id]=threshold;
persist();
renderMetrics();
renderAlerts();
}
function deleteAlert(id) {
var p = getCurrentProfile();
if(p.alerts) delete p.alerts[id];
persist();
renderMetrics();
renderAlerts();
}
function showAlertDialog(id) {
modalContainer.classList.remove('hidden');
modalContainer.innerHTML=
'<div class="modal-overlay"><div class="modal">'+
'<h3>Set Alert Threshold</h3>'+
'<p style="font-size:13px;opacity:.6;margin-bottom:8px">Enter a threshold value for this metric. You will be notified when it crosses.</p>'+
'<input type="text" id="alertThreshInput" placeholder="e.g. 5% or 1000" style="width:100%;padding:8px;border:1px solid var(--border);border-radius:var(--radius);background:var(--bg);color:var(--text);font-size:13px">'+
'<div class="modal-actions">'+
'<button id="alertCancelBtn">Cancel</button>'+
'<button id="alertSaveBtn" class="primary">Set Alert</button>'+
'</div></div></div>';
document.getElementById('alertSaveBtn').addEventListener('click',function(){
var val = document.getElementById('alertThreshInput').value.trim();
if(val) setAlert(id,val);
modalContainer.classList.add('hidden');
});
document.getElementById('alertCancelBtn').addEventListener('click',function(){
modalContainer.classList.add('hidden');
});
}
// ----- add metric -----
function showAddMetricDialog() {
var p = getCurrentProfile();
var available = metricDefs.filter(function(m){return !p.metricIds||p.metricIds.indexOf(m.id)===-1;});
if(!available.length) {
modalContainer.classList.remove('hidden');
modalContainer.innerHTML=
'<div class="modal-overlay"><div class="modal">'+
'<h3>All Metrics Added</h3>'+
'<p style="font-size:13px;opacity:.6">All available metrics are already on this dashboard.</p>'+
'<div class="modal-actions"><button id="addCloseBtn" class="primary">OK</button></div></div></div>';
document.getElementById('addCloseBtn').addEventListener('click',function(){modalContainer.classList.add('hidden');});
return;
}
modalContainer.classList.remove('hidden');
var html='<div class="modal-overlay"><div class="modal"><h3>Add Metric</h3><div style="max-height:250px;overflow-y:auto">';
available.forEach(function(m){
html+='<label style="display:flex;align-items:center;gap:8px;padding:6px 0;font-size:13px;cursor:pointer">'+
'<input type="checkbox" class="add-metric-cb" value="'+m.id+'">'+
m.label+' <span style="opacity:.5">'+m.cat+'</span></label>';
});
html+='</div><div class="modal-actions">'+
'<button id="addMetricCancelBtn">Cancel</button>'+
'<button id="addMetricConfirmBtn" class="primary">Add Selected</button>'+
'</div></div></div>';
modalContainer.innerHTML=html;
document.getElementById('addMetricConfirmBtn').addEventListener('click',function(){
var cbs = document.querySelectorAll('.add-metric-cb:checked');
var ids = Array.from(cbs).map(function(cb){return cb.value;});
if(ids.length) {
if(!p.metricIds) p.metricIds=metricDefs.map(function(m){return m.id;});
ids.forEach(function(id){
if(p.metricIds.indexOf(id)===-1) p.metricIds.push(id);
});
persist();
fullRefresh();
}
modalContainer.classList.add('hidden');
});
document.getElementById('addMetricCancelBtn').addEventListener('click',function(){modalContainer.classList.add('hidden');});
}
// ----- add user -----
function showAddUserDialog() {
modalContainer.classList.remove('hidden');
modalContainer.innerHTML=
'<div class="modal-overlay"><div class="modal">'+
'<h3>New User</h3>'+
'<input type="text" id="newUserName" placeholder="User name..." style="width:100%;padding:8px;border:1px solid var(--border);border-radius:var(--radius);background:var(--bg);color:var(--text);font-size:13px">'+
'<div class="modal-actions">'+
'<button id="newUserCancelBtn">Cancel</button>'+
'<button id="newUserSaveBtn" class="primary">Create</button>'+
'</div></div></div>';
document.getElementById('newUserSaveBtn').addEventListener('click',function(){
var name = document.getElementById('newUserName').value.trim();
if(name) {
var p = defaultProfile(name);
data.users.push(p);
currentUserIdx=data.users.length-1;
data.active=currentUserIdx;
persist();
fullRefresh();
}
modalContainer.classList.add('hidden');
});
document.getElementById('newUserCancelBtn').addEventListener('click',function(){modalContainer.classList.add('hidden');});
}
// ----- full refresh -----
function fullRefresh() {
currentUser = getCurrentProfile();
applyTheme();
renderMetrics();
renderUsers();
renderViews();
renderBookmarks();
renderAlerts();
// update topbar selects
if(userSelect) userSelect.value=currentUserIdx;
}
// ----- event delegation on metricsGrid -----
metricsGrid.addEventListener('click',function(e){
var action = e.target.dataset.action;
var id = e.target.dataset.id;
if(!action||!id) return;
e.stopPropagation();
switch(action) {
case 'bookmark':
showBookmarkDialog(id);
break;
case 'alert':
showAlertDialog(id);
break;
case 'remove':
var p = getCurrentProfile();
if(p.metricIds) {
p.metricIds = p.metricIds.filter(function(mid){return mid!==id;});
}
persist();
fullRefresh();
break;
}
});
// ----- bookmark star clicks (delegated) -----
metricsGrid.addEventListener('click',function(e){
var star = e.target.closest('.bookmark-star');
if(!star) return;
var id = star.dataset.bmId;
if(!id) return;
e.stopPropagation();
var p = getCurrentProfile();
if(p.bookmarks && p.bookmarks[id]) {
delete p.bookmarks[id];
} else {
showBookmarkDialog(id);
}
});
// alert badge clicks (delegated)
metricsGrid.addEventListener('click',function(e){
var badge = e.target.closest('.alert-badge');
if(!badge) return;
var id = badge.dataset.alertId;
if(!id) return;
e.stopPropagation();
showAlertDialog(id);
});
// ----- topbar change handlers -----
userSelect.addEventListener('change',function(){
var idx = parseInt(this.value);
switchUser(idx);
});
themeSelect.addEventListener('change',function(){
var p = getCurrentProfile();
p.theme = this.value;
persist();
applyTheme();
});
accentPicker.addEventListener('input',function(){
var p = getCurrentProfile();
p.accent = this.value;
persist();
applyTheme();
});
densitySelect.addEventListener('change',function(){
var p = getCurrentProfile();
p.density = this.value;
persist();
applyTheme();
});
fontSelect.addEventListener('change',function(){
var p = getCurrentProfile();
p.fontSize = parseInt(this.value);
persist();
applyTheme();
});
// ----- button handlers -----
addMetricBtn.addEventListener('click',showAddMetricDialog);
addUserBtn.addEventListener('click',showAddUserDialog);
saveViewBtn.addEventListener('click',function(){
var name = viewNameInput.value.trim();
if(name) {
saveView(name);
viewNameInput.value='';
}
});
viewNameInput.addEventListener('keydown',function(e){
if(e.key==='Enter') saveViewBtn.click();
});
// ----- modal overlay close on backdrop click -----
modalContainer.addEventListener('click',function(e){
if(e.target.classList.contains('modal-overlay')) {
modalContainer.classList.add('hidden');
}
});
// ----- init -----
fullRefresh();
})();
</script>
</body>
</html>
```