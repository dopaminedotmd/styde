```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cognitive Personalization Engine</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#f4f6f9;--surface:#fff;--text:#1a1a2e;--text-secondary:#64748b;--border:#e2e8f0;--accent:#6366f1;--accent-hover:#4f46e5;--accent-light:#eef2ff;--danger:#ef4444;--success:#22c55e;--warning:#f59e0b;--radius:10px;--radius-sm:6px;--shadow:0 1px 3px rgba(0,0,0,.08),0 1px 2px rgba(0,0,0,.06);--shadow-lg:0 10px 25px rgba(0,0,0,.1);--font-scale:1;--density:1;transition:background-color .3s,color .3s,border-color .3s}
[data-theme=dark]{--bg:#0f172a;--surface:#1e293b;--text:#e2e8f0;--text-secondary:#94a3b8;--border:#334155;--accent-light:#1e1b4b}
[data-density=compact]{--density:.75}
[data-density=spacious]{--density:1.5}
html{font-size:calc(14px*var(--font-scale))}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px;line-height:1.5}
.app{max-width:1400px;margin:0 auto}
.top-bar{display:flex;align-items:center;gap:12px;padding:calc(12px*var(--density)) 16px;background:var(--surface);border-radius:var(--radius);box-shadow:var(--shadow);margin-bottom:16px;flex-wrap:wrap}
.top-bar h1{font-size:1.25rem;font-weight:700;flex:1;min-width:180px}
.btn{display:inline-flex;align-items:center;gap:6px;padding:calc(8px*var(--density)) calc(16px*var(--density));border-radius:var(--radius-sm);border:1px solid var(--border);background:var(--surface);color:var(--text);font-size:.875rem;cursor:pointer;transition:all .15s;white-space:nowrap}
.btn:hover{background:var(--accent-light);border-color:var(--accent);color:var(--accent)}
.btn-primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.btn-primary:hover{background:var(--accent-hover);color:#fff}
.btn-sm{padding:calc(4px*var(--density)) calc(10px*var(--density));font-size:.75rem}
.btn-danger{border-color:var(--danger);color:var(--danger)}
.btn-danger:hover{background:#fef2f2;border-color:var(--danger)}
.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));margin-bottom:16px}
.card{background:var(--surface);border-radius:var(--radius);box-shadow:var(--shadow);padding:calc(16px*var(--density));border:1px solid var(--border);transition:all .2s}
.card:hover{box-shadow:var(--shadow-lg)}
.card-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px}
.card-title{font-size:.95rem;font-weight:600;color:var(--text-secondary);text-transform:uppercase;letter-spacing:.5px}
.card-value{font-size:1.75rem;font-weight:700;margin:4px 0}
.card-label{font-size:.8rem;color:var(--text-secondary)}
.metric-trend{font-size:.8rem;font-weight:600;padding:2px 8px;border-radius:99px}
.metric-trend.up{background:#dcfce7;color:#166534}
.metric-trend.down{background:#fef2f2;color:#991b1b}
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:100;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity .25s}
.modal-overlay.active{opacity:1;pointer-events:all}
.modal{background:var(--surface);border-radius:var(--radius);padding:24px;max-width:480px;width:90%;max-height:80vh;overflow-y:auto;box-shadow:var(--shadow-lg);transform:translateY(10px);transition:transform .25s}
.modal-overlay.active .modal{transform:translateY(0)}
.modal h2{font-size:1.1rem;margin-bottom:16px}
.modal label{display:block;font-size:.85rem;font-weight:600;margin-bottom:4px;color:var(--text-secondary)}
.modal input,.modal select,.modal textarea{width:100%;padding:8px 12px;border:1px solid var(--border);border-radius:var(--radius-sm);background:var(--bg);color:var(--text);font-size:.875rem;margin-bottom:12px}
.modal textarea{resize:vertical;min-height:60px}
.modal-actions{display:flex;gap:8px;justify-content:flex-end;margin-top:8px}
.tabs{display:flex;gap:2px;margin-bottom:12px;border-bottom:2px solid var(--border);flex-wrap:wrap}
.tab{padding:calc(8px*var(--density)) calc(16px*var(--density));cursor:pointer;border:none;background:none;color:var(--text-secondary);font-size:.875rem;font-weight:500;border-bottom:2px solid transparent;margin-bottom:-2px;transition:all .15s}
.tab.active{color:var(--accent);border-bottom-color:var(--accent)}
.tab:hover{color:var(--text)}
.section-title{font-size:1.1rem;font-weight:700;margin:20px 0 12px;padding-bottom:8px;border-bottom:1px solid var(--border)}
.empty-state{text-align:center;padding:32px;color:var(--text-secondary);font-size:.9rem}
.badge{display:inline-block;padding:2px 8px;border-radius:99px;font-size:.7rem;font-weight:600;background:var(--accent-light);color:var(--accent)}
.alert-item,.bookmark-item,.view-item{display:flex;justify-content:space-between;align-items:center;padding:calc(8px*var(--density)) 0;border-bottom:1px solid var(--border)}
.alert-item:last-child,.bookmark-item:last-child,.view-item:last-child{border-bottom:none}
.settings-row{display:flex;justify-content:space-between;align-items:center;padding:calc(10px*var(--density)) 0;border-bottom:1px solid var(--border)}
.color-swatches{display:flex;gap:8px;margin:8px 0}
.color-swatch{width:28px;height:28px;border-radius:50%;border:2px solid transparent;cursor:pointer;transition:all .15s}
.color-swatch.active{border-color:var(--text);transform:scale(1.15)}
.user-badge{display:flex;align-items:center;gap:8px;padding:4px 12px 4px 4px;border-radius:99px;background:var(--accent-light);font-size:.8rem;font-weight:500;cursor:pointer;transition:all .15s}
.user-badge:hover{background:var(--accent);color:#fff}
.user-avatar{width:24px;height:24px;border-radius:50%;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700}
.profile-section{display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.activity-log{max-height:200px;overflow-y:auto;font-size:.8rem}
.activity-log div{padding:4px 0;border-bottom:1px solid var(--border);color:var(--text-secondary)}
.activity-log div:last-child{border-bottom:none}
.activity-time{color:var(--text-secondary);margin-right:8px;font-size:.7rem}
@media(max-width:640px){.top-bar{flex-direction:column;align-items:stretch}.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="app" id="app"></div>
<script>
(function(){
'use strict';
const LS_KEY='cpe_data';
function loadData(){
try{
const raw=localStorage.getItem(LS_KEY);
if(raw)return JSON.parse(raw);
}catch(e){}
return null;
}
function saveData(data){
try{localStorage.setItem(LS_KEY,JSON.stringify(data));}catch(e){}
}
const COLORS=['#6366f1','#8b5cf6','#ec4899','#f43f5e','#f97316','#eab308','#22c55e','#14b8a6','#06b6d4','#3b82f6'];
const DEFAULT_PROFILES=[
{id:'alice',name:'Alice Chen',avatar:null,theme:'light',accent:COLORS[0],density:'normal',fontScale:1,created:Date.now()-86400000*30,history:[]},
{id:'bob',name:'Bob Smith',avatar:null,theme:'dark',accent:COLORS[4],density:'compact',fontScale:1,created:Date.now()-86400000*14,history:[]},
{id:'new_user',name:'New Explorer',avatar:null,theme:'light',accent:COLORS[0],density:'normal',fontScale:1,created:Date.now(),history:[]}
];
function freshData(){
const now=Date.now();
return{
profiles:JSON.parse(JSON.stringify(DEFAULT_PROFILES)),
views:{},
bookmarks:{},
alerts:{},
currentUser:'alice',
nextId:1
};
}
let state=loadData()||freshData();
if(!state.profiles||!state.profiles.length){state.profiles=JSON.parse(JSON.stringify(DEFAULT_PROFILES));}
if(!state.views)state.views={};
if(!state.bookmarks)state.bookmarks={};
if(!state.alerts)state.alerts={};
if(!state.currentUser)state.currentUser='alice';
if(typeof state.nextId!=='number')state.nextId=1;
function persist(){saveData(state);}
function getProfile(id){return state.profiles.find(p=>p.id===id);}
function getCurrentProfile(){return getProfile(state.currentUser);}
function logActivity(userId,action){
const p=getProfile(userId);
if(!p)return;
if(!p.history)p.history=[];
p.history.unshift({action,time:Date.now()});
if(p.history.length>100)p.history.length=100;
persist();
}
function formatTime(ts){
const d=new Date(ts);
return d.toLocaleDateString()+' '+d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});
}
function abbreviate(n){
if(n>=1000000)return (n/1000000).toFixed(1)+'M';
if(n>=1000)return (n/1000).toFixed(1)+'K';
return n.toString();
}
function renderCard(tag,opts){
const el=document.createElement(tag||'div');
if(opts.className)el.className=opts.className;
if(opts.text)el.textContent=opts.text;
if(opts.html)el.innerHTML=opts.html;
if(opts.attrs)for(const [k,v]of Object.entries(opts.attrs))el.setAttribute(k,v);
if(opts.on)for(const [ev,fn]of Object.entries(opts.on))el.addEventListener(ev,fn);
if(opts.children)for(const c of opts.children)el.appendChild(typeof c==='string'?document.createTextNode(c):c);
if(opts.style)Object.assign(el.style,opts.style);
return el;
}
function renderMetric(name,value,trend,onBookmark,onAlert){
const trendCls=trend>0?'up':trend<0?'down':'';
const trendLabel=trend>0?'+'+trend+'%':trend<0?trend+'%':'—';
const card=renderCard('div',{className:'card'});
card.appendChild(renderCard('div',{className:'card-header',children:[
renderCard('div',{className:'card-title',text:name}),
renderCard('div',{className:'metric-trend '+trendCls,text:trendLabel})
]}));
card.appendChild(renderCard('div',{className:'card-value',text:abbreviate(value)}));
card.appendChild(renderCard('div',{className:'card-label',text:'Current value'}));
const actions=renderCard('div',{style:{display:'flex',gap:'6px',marginTop:'10px'}});
const bmBtn=renderCard('button',{className:'btn btn-sm',text:'Bookmark',on:{click:onBookmark}});
const alBtn=renderCard('button',{className:'btn btn-sm',text:'Alert',on:{click:onAlert}});
actions.appendChild(bmBtn);
actions.appendChild(alBtn);
card.appendChild(actions);
return card;
}
function renderAlertItem(a,onEdit,onDelete){
const row=renderCard('div',{className:'alert-item'});
const info=renderCard('div',{children:[
renderCard('div',{style:{fontWeight:600},text:a.metric||'All metrics'}),
renderCard('div',{style:{fontSize:'.8rem',color:'var(--text-secondary)'},text:a.condition+' '+a.threshold+(a.enabled?'':' (muted)')})
]});
const act=renderCard('div',{style:{display:'flex',gap:'6px'}});
const editBtn=renderCard('button',{className:'btn btn-sm',text:'Edit',on:{click:()=>onEdit(a)}});
const delBtn=renderCard('button',{className:'btn btn-sm btn-danger',text:'X',on:{click:()=>onDelete(a.id)}});
act.appendChild(editBtn);
act.appendChild(delBtn);
row.appendChild(info);
row.appendChild(act);
return row;
}
function renderViewItem(v,onRestore,onDelete){
const row=renderCard('div',{className:'view-item'});
const info=renderCard('div',{children:[
renderCard('div',{style:{fontWeight:600},text:v.name}),
renderCard('div',{style:{fontSize:'.8rem',color:'var(--text-secondary)'},text:'Saved '+formatTime(v.savedAt)})
]});
const act=renderCard('div',{style:{display:'flex',gap:'6px'}});
const restBtn=renderCard('button',{className:'btn btn-sm',text:'Restore',on:{click:()=>onRestore(v.id)}});
const delBtn=renderCard('button',{className:'btn btn-sm btn-danger',text:'X',on:{click:()=>onDelete(v.id)}});
act.appendChild(restBtn);
act.appendChild(delBtn);
row.appendChild(info);
row.appendChild(act);
return row;
}
function renderBookmarkItem(b,onDelete){
const row=renderCard('div',{className:'bookmark-item'});
const info=renderCard('div',{children:[
renderCard('div',{style:{fontWeight:600},text:b.metricName}),
renderCard('div',{style:{fontSize:'.8rem',color:'var(--text-secondary)'},text:'Value: '+abbreviate(b.value)+' | '+formatTime(b.savedAt)+(b.note?' | Note: '+b.note:'')})
]});
const act=renderCard('div',{style:{display:'flex',gap:'6px'}});
const delBtn=renderCard('button',{className:'btn btn-sm btn-danger',text:'X',on:{click:()=>onDelete(b.id)}});
act.appendChild(delBtn);
row.appendChild(info);
row.appendChild(act);
return row;
}
function openModal(html){
const overlay=renderCard('div',{className:'modal-overlay',on:{click:function(e){if(e.target===this)closeModal();}}});
const modal=renderCard('div',{className:'modal',html:html});
overlay.appendChild(modal);
document.body.appendChild(overlay);
requestAnimationFrame(()=>overlay.classList.add('active'));
return {overlay,modal};
}
function closeModal(){
const ov=document.querySelector('.modal-overlay');
if(ov){ov.classList.remove('active');setTimeout(()=>ov.remove(),250);}
}
const METRICS_DATA=[
{name:'Active Users',value:2847,trend:12},
{name:'Revenue (MRR)',value:45800,trend:-3},
{name:'Conversion Rate',value:3.2,trend:0.4},
{name:'Avg Session',value:4.7,trend:8},
{name:'Support Tickets',value:42,trend:-15},
{name:'Feature Usage',value:76,trend:5},
{name:'Load Time (ms)',value:234,trend:-22},
{name:'Retention Rate',value:94.1,trend:1.2},
{name:'Page Views',value:12400,trend:7},
{name:'Bounce Rate',value:32,trend:-4},
{name:'API Calls (k)',value:892,trend:14},
{name:'Error Rate',value:0.08,trend:-33}
];
const DEFAULT_VIEW={visibleMetrics:METRICS_DATA.map(m=>m.name),layout:'grid',filters:{search:'',minVal:0}};
let currentViewState=JSON.parse(JSON.stringify(DEFAULT_VIEW));
function getFilteredMetrics(){
const profile=getCurrentProfile();
const term=(currentViewState.filters.search||'').toLowerCase();
const min=currentViewState.filters.minVal||0;
const visibleSet=new Set(currentViewState.visibleMetrics||METRICS_DATA.map(m=>m.name));
return METRICS_DATA.filter(m=>visibleSet.has(m.name)&&m.name.toLowerCase().includes(term)&&m.value>=min);
}
function renderDashboard(){
const app=document.getElementById('app');
app.innerHTML='';
const profile=getCurrentProfile();
if(!profile){
app.textContent='No profile found.';
return;
}
const accent=profile.accent||COLORS[0];
const density=profile.density||'normal';
const fontScale=profile.fontScale||1;
document.documentElement.setAttribute('data-theme',profile.theme||'light');
document.documentElement.setAttribute('data-density',density);
document.documentElement.style.setProperty('--font-scale',fontScale);
document.documentElement.style.setProperty('--accent',accent);
document.documentElement.style.setProperty('--accent-hover',accent+'dd');
document.documentElement.style.setProperty('--accent-light',accent+'20');
const topBar=renderCard('div',{className:'top-bar'});
topBar.appendChild(renderCard('h1',{text:'Personal Dashboard'}));
const userBadge=renderCard('div',{className:'user-badge',on:{click:showProfileSwitcher},children:[
renderCard('div',{className:'user-avatar',text:profile.name.charAt(0).toUpperCase()}),
document.createTextNode(profile.name)
]});
topBar.appendChild(userBadge);
const themeBtn=renderCard('button',{className:'btn btn-sm',text:profile.theme==='dark'?'Light Mode':'Dark Mode',on:{click:toggleTheme}});
topBar.appendChild(themeBtn);
const saveViewBtn=renderCard('button',{className:'btn btn-sm',text:'Save View',on:{click:showSaveView}});
topBar.appendChild(saveViewBtn);
const settingsBtn=renderCard('button',{className:'btn btn-sm',text:'Settings',on:{click:showSettings}});
topBar.appendChild(settingsBtn);
app.appendChild(topBar);
const tabs=renderCard('div',{className:'tabs'});
const tabNames=['Dashboard','Alerts','Bookmarks','Views','Activity'];
let activeTab=0;
tabNames.forEach((name,i)=>{
const tab=renderCard('button',{className:'tab'+(i===activeTab?' active':''),text:name,on:{click:()=>switchTab(i)}});
tabs.appendChild(tab);
});
app.appendChild(tabs);
const content=renderCard('div',{id:'content-area'});
app.appendChild(content);
function switchTab(idx){
activeTab=idx;
const allTabs=tabs.querySelectorAll('.tab');
allTabs.forEach((t,i)=>t.classList.toggle('active',i===idx));
renderTabContent();
}
function renderTabContent(){
content.innerHTML='';
const profile=getCurrentProfile();
switch(activeTab){
case 0:renderDashboardTab();break;
case 1:renderAlertsTab();break;
case 2:renderBookmarksTab();break;
case 3:renderViewsTab();break;
case 4:renderActivityTab();break;
}
}
function renderDashboardTab(){
const metrics=getFilteredMetrics();
const filterBar=renderCard('div',{style:{display:'flex',gap:'8px',marginBottom:'12px',flexWrap:'wrap',alignItems:'center'}});
const searchInput=renderCard('input',{attrs:{type:'text',placeholder:'Search metrics...',value:currentViewState.filters.search||''},style:{padding:'6px 12px',border:'1px solid var(--border)',borderRadius:'var(--radius-sm)',background:'var(--surface)',color:'var(--text)',fontSize:'.85rem',flex:'1',minWidth:'150px'}});
searchInput.addEventListener('input',function(){
currentViewState.filters.search=this.value;
renderDashboardTab();
});
filterBar.appendChild(searchInput);
const minLabel=renderCard('label',{style:{fontSize:'.8rem',color:'var(--text-secondary)',display:'flex',alignItems:'center',gap:'6px'},children:[
document.createTextNode('Min:'),
renderCard('input',{attrs:{type:'number',placeholder:'0',value:currentViewState.filters.minVal||'',min:'0',style:{width:'70px',padding:'4px 8px',border:'1px solid var(--border)',borderRadius:'var(--radius-sm)',background:'var(--surface)',color:'var(--text)',fontSize:'.8rem'}}})
]});
const minInput=minLabel.querySelector('input');
minInput.addEventListener('input',function(){
currentViewState.filters.minVal=parseFloat(this.value)||0;
renderDashboardTab();
});
filterBar.appendChild(minLabel);
content.appendChild(filterBar);
const grid=renderCard('div',{className:'grid'});
metrics.forEach(m=>{
const card=renderMetric(m.name,m.value,m.trend,
function(){showBookmarkModal(m);},
function(){showAlertModal(m);}
);
grid.appendChild(card);
});
content.appendChild(grid);
if(metrics.length===0){
content.appendChild(renderCard('div',{className:'empty-state',text:'No metrics match your filters.'}));
}
}
function renderAlertsTab(){
const profile=getCurrentProfile();
const alerts=(state.alerts[profile.id]||[]);
const header=renderCard('div',{style:{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:'12px'}});
header.appendChild(renderCard('h3',{style:{fontSize:'1rem',fontWeight:600},text:'Alert Rules ('+alerts.length+')'}));
header.appendChild(renderCard('button',{className:'btn btn-sm btn-primary',text:'+ Add Alert',on:{click:()=>showAlertModal(null)}}));
content.appendChild(header);
if(alerts.length===0){
content.appendChild(renderCard('div',{className:'empty-state',text:'No alerts configured. Click + Add Alert to create one.'}));
}else{
alerts.forEach(a=>{
content.appendChild(renderAlertItem(a,
function(){showAlertModal(a);},
function(id){
state.alerts[profile.id]=state.alerts[profile.id].filter(x=>x.id!==id);
persist();logActivity(profile.id,'Deleted alert');renderTabContent();
}
));
});
}
}
function renderBookmarksTab(){
const profile=getCurrentProfile();
const bms=(state.bookmarks[profile.id]||[]);
const header=renderCard('div',{style:{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:'12px'}});
header.appendChild(renderCard('h3',{style:{fontSize:'1rem',fontWeight:600},text:'Bookmarks ('+bms.length+')'}));
content.appendChild(header);
if(bms.length===0){
content.appendChild(renderCard('div',{className:'empty-state',text:'No bookmarks saved. Bookmark a metric from the Dashboard tab.'}));
}else{
bms.forEach(b=>{
content.appendChild(renderBookmarkItem(b,function(id){
state.bookmarks[profile.id]=state.bookmarks[profile.id].filter(x=>x.id!==id);
persist();logActivity(profile.id,'Removed bookmark');renderTabContent();
}));
});
}
}
function renderViewsTab(){
const profile=getCurrentProfile();
const views=(state.views[profile.id]||[]);
const header=renderCard('div',{style:{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:'12px'}});
header.appendChild(renderCard('h3',{style:{fontSize:'1rem',fontWeight:600},text:'Saved Views ('+views.length+')'}));
content.appendChild(header);
if(views.length===0){
content.appendChild(renderCard('div',{className:'empty-state',text:'No saved views. Save your current dashboard layout from the top bar.'}));
}else{
views.forEach(v=>{
content.appendChild(renderViewItem(v,
function(id){
const found=state.views[profile.id].find(x=>x.id===id);
if(found){
currentViewState=JSON.parse(JSON.stringify(found.state));
logActivity(profile.id,'Restored view: '+found.name);
renderDashboardTab();
if(activeTab!==0)switchTab(0);
}
},
function(id){
state.views[profile.id]=state.views[profile.id].filter(x=>x.id!==id);
persist();logActivity(profile.id,'Deleted view');renderTabContent();
}
));
});
}
}
function renderActivityTab(){
const profile=getCurrentProfile();
const history=profile.history||[];
content.appendChild(renderCard('h3',{style:{fontSize:'1rem',fontWeight:600,marginBottom:'12px'},text:'Activity History'}));
if(history.length===0){
content.appendChild(renderCard('div',{className:'empty-state',text:'No activity yet. Interact with the dashboard to build history.'}));
}else{
const log=renderCard('div',{className:'activity-log'});
history.forEach(h=>{
log.appendChild(renderCard('div',{children:[
renderCard('span',{className:'activity-time',text:formatTime(h.time)}),
document.createTextNode(h.action)
]}));
});
content.appendChild(log);
}
}
renderTabContent();
}
function toggleTheme(){
const profile=getCurrentProfile();
profile.theme=profile.theme==='dark'?'light':'dark';
persist();logActivity(profile.id,'Switched to '+profile.theme+' mode');
renderDashboard();
}
function showProfileSwitcher(){
const html=`
<h2>Switch Profile</h2>
<div id="profile-list"></div>
<div style="margin-top:12px">
<button class="btn btn-sm btn-primary" onclick="showNewProfileModal()">+ New Profile</button>
</div>`;
const {overlay,modal}=openModal(html);
const list=modal.querySelector('#profile-list');
state.profiles.forEach(p=>{
const row=renderCard('div',{style:{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'8px 0',borderBottom:'1px solid var(--border)',cursor:'pointer'},on:{click:function(){
state.currentUser=p.id;
logActivity(p.id,'Switched to profile');
persist();
closeModal();
renderDashboard();
}},children:[
renderCard('div',{style:{display:'flex',alignItems:'center',gap:'8px'},children:[
renderCard('div',{className:'user-avatar',text:p.name.charAt(0).toUpperCase()}),
renderCard('span',{style:{fontWeight:p.id===state.currentUser?700:400},text:p.name+(p.id===state.currentUser?' (active)':'')})
]}),
p.id!=='new_user'?renderCard('button',{className:'btn btn-sm btn-danger',text:'Delete',on:{click:function(e){e.stopPropagation();deleteProfile(p.id);list.removeChild(row.parentElement||row);}}}):null
].filter(Boolean));
list.appendChild(row);
});
}
function showNewProfileModal(){
closeModal();
const html=`
<h2>New Profile</h2>
<label>Name</label>
<input type="text" id="newProfileName" placeholder="Your name" value="">
<label>Theme</label>
<select id="newProfileTheme"><option value="light">Light</option><option value="dark">Dark</option></select>
<label>Accent Color</label>
<div class="color-swatches" id="newAccentSwatches"></div>
<div class="modal-actions">
<button class="btn" onclick="closeModal()">Cancel</button>
<button class="btn btn-primary" id="createProfileBtn">Create</button>
</div>`;
const {overlay,modal}=openModal(html);
let selectedAccent=COLORS[0];
const swatchContainer=modal.querySelector('#newAccentSwatches');
COLORS.forEach(c=>{
const sw=renderCard('div',{className:'color-swatch'+(c===selectedAccent?' active':''),style:{background:c},on:{click:function(){
swatchContainer.querySelectorAll('.color-swatch').forEach(s=>s.classList.remove('active'));
this.classList.add('active');selectedAccent=c;
}}});
swatchContainer.appendChild(sw);
});
modal.querySelector('#createProfileBtn').addEventListener('click',function(){
const name=modal.querySelector('#newProfileName').value.trim();
if(!name)return;
const id=name.toLowerCase().replace(/\s+/g,'_')+'_'+Date.now();
const profile={id:id,name:name,avatar:null,theme:modal.querySelector('#newProfileTheme').value,accent:selectedAccent,density:'normal',fontScale:1,created:Date.now(),history:[]};
state.profiles.push(profile);
state.currentUser=id;
if(!state.alerts[id])state.alerts[id]=[];
if(!state.bookmarks[id])state.bookmarks[id]=[];
if(!state.views[id])state.views[id]=[];
persist();
closeModal();
renderDashboard();
});
}
function deleteProfile(id){
if(state.profiles.length<=1)return;
state.profiles=state.profiles.filter(p=>p.id!==id);
if(state.currentUser===id)state.currentUser=state.profiles[0].id;
persist();
renderDashboard();
}
function showSaveView(){
const html=`
<h2>Save Current View</h2>
<label>View Name</label>
<input type="text" id="viewName" placeholder="e.g. Executive Overview" value="">
<div class="modal-actions">
<button class="btn" onclick="closeModal()">Cancel</button>
<button class="btn btn-primary" id="saveViewConfirmBtn">Save</button>
</div>`;
const {overlay,modal}=openModal(html);
modal.querySelector('#saveViewConfirmBtn').addEventListener('click',function(){
const name=modal.querySelector('#viewName').value.trim();
if(!name)return;
const profile=getCurrentProfile();
if(!state.views[profile.id])state.views[profile.id]=[];
state.views[profile.id].push({id:state.nextId++,name:name,savedAt:Date.now(),state:JSON.parse(JSON.stringify(currentViewState))});
logActivity(profile.id,'Saved view: '+name);
persist();
closeModal();
renderDashboard();
});
}
function showSettings(){
const profile=getCurrentProfile();
const html=`
<h2>Settings — ${profile.name}</h2>
<div class="settings-row">
<span>Density</span>
<select id="densitySelect">
<option value="compact"${profile.density==='compact'?' selected':''}>Compact</option>
<option value="normal"${profile.density==='normal'?' selected':''}>Normal</option>
<option value="spacious"${profile.density==='spacious'?' selected':''}>Spacious</option>
</select>
</div>
<div class="settings-row">
<span>Font Scale</span>
<input type="range" id="fontScaleRange" min="0.75" max="1.5" step="0.05" value="${profile.fontScale}">
</div>
<div class="settings-row">
<span>Accent Color</span>
</div>
<div class="color-swatches" id="settingsSwatches"></div>
<div class="modal-actions" style="margin-top:16px">
<button class="btn" onclick="closeModal()">Cancel</button>
<button class="btn btn-primary" id="settingsSaveBtn">Save</button>
</div>`;
const {overlay,modal}=openModal(html);
let newAccent=profile.accent;
const swatchContainer=modal.querySelector('#settingsSwatches');
COLORS.forEach(c=>{
const sw=renderCard('div',{className:'color-swatch'+(c===newAccent?' active':''),style:{background:c},on:{click:function(){
swatchContainer.querySelectorAll('.color-swatch').forEach(s=>s.classList.remove('active'));
this.classList.add('active');newAccent=c;
}}});
swatchContainer.appendChild(sw);
});
modal.querySelector('#settingsSaveBtn').addEventListener('click',function(){
profile.density=modal.querySelector('#densitySelect').value;
profile.fontScale=parseFloat(modal.querySelector('#fontScaleRange').value);
profile.accent=newAccent;
logActivity(profile.id,'Updated settings');
persist();
closeModal();
renderDashboard();
});
}
function showAlertModal(metricOrAlert){
const isEdit=metricOrAlert&&metricOrAlert.id;
const metricName=isEdit?metricOrAlert.metric:(metricOrAlert?metricOrAlert.name:'');
const condition=isEdit?metricOrAlert.condition:'above';
const threshold=isEdit?metricOrAlert.threshold:'';
const enabled=isEdit?metricOrAlert.enabled:true;
const html=`
<h2>${isEdit?'Edit Alert':'New Alert'}</h2>
<label>Metric</label>
<select id="alertMetric">
<option value="">All Metrics</option>
${METRICS_DATA.map(m=>'<option value="'+m.name+'"'+(m.name===metricName?' selected':'')+'>'+m.name+'</option>').join('')}
</select>
<label>Condition</label>
<select id="alertCondition">
<option value="above"${condition==='above'?' selected':''}>Above</option>
<option value="below"${condition==='below'?' selected':''}>Below</option>
</select>
<label>Threshold</label>
<input type="number" id="alertThreshold" value="${threshold}" step="any">
<label>
<input type="checkbox" id="alertEnabled"${enabled?' checked':''}> Enabled
</label>
<div class="modal-actions">
<button class="btn" onclick="closeModal()">Cancel</button>
<button class="btn btn-primary" id="alertSaveBtn">${isEdit?'Update':'Create'}</button>
</div>`;
const {overlay,modal}=openModal(html);
modal.querySelector('#alertSaveBtn').addEventListener('click',function(){
const profile=getCurrentProfile();
const alMetric=modal.querySelector('#alertMetric').value;
const alCondition=modal.querySelector('#alertCondition').value;
const alThreshold=parseFloat(modal.querySelector('#alertThreshold').value);
const alEnabled=modal.querySelector('#alertEnabled').checked;
if(isNaN(alThreshold))return;
if(!state.alerts[profile.id])state.alerts[profile.id]=[];
if(isEdit){
const idx=state.alerts[profile.id].findIndex(a=>a.id===metricOrAlert.id);
if(idx>=0){state.alerts[profile.id][idx]={...state.alerts[profile.id][idx],metric:alMetric,condition:alCondition,threshold:alThreshold,enabled:alEnabled};}
logActivity(profile.id,'Updated alert');
}else{
state.alerts[profile.id].push({id:state.nextId++,metric:alMetric,condition:alCondition,threshold:alThreshold,enabled:alEnabled});
logActivity(profile.id,'Created alert');
}
persist();
closeModal();
renderDashboard();
});
}
function showBookmarkModal(metric){
const html=`
<h2>Bookmark Metric</h2>
<p style="margin-bottom:12px;color:var(--text-secondary);font-size:.9rem">Save ${metric.name} (${abbreviate(metric.value)}) for later reference.</p>
<label>Note (optional)</label>
<textarea id="bookmarkNote" placeholder="Why are you bookmarking this?"></textarea>
<div class="modal-actions">
<button class="btn" onclick="closeModal()">Cancel</button>
<button class="btn btn-primary" id="bookmarkSaveBtn">Save Bookmark</button>
</div>`;
const {overlay,modal}=openModal(html);
modal.querySelector('#bookmarkSaveBtn').addEventListener('click',function(){
const profile=getCurrentProfile();
if(!state.bookmarks[profile.id])state.bookmarks[profile.id]=[];
state.bookmarks[profile.id].push({
id:state.nextId++,
metricName:metric.name,
value:metric.value,
trend:metric.trend,
savedAt:Date.now(),
note:modal.querySelector('#bookmarkNote').value.trim()
});
logActivity(profile.id,'Bookmarked: '+metric.name);
persist();
closeModal();
renderDashboard();
});
}
renderDashboard();
window.showNewProfileModal=showNewProfileModal;
window.closeModal=closeModal;
})();
</script>
</body>
</html>
```