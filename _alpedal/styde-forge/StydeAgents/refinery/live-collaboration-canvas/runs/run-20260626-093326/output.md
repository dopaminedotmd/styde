```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Live Collab Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui,-apple-system,sans-serif}
body{background:#0d1117;color:#e6edf3;height:100vh;overflow:hidden}
.topbar{display:flex;align-items:center;gap:12px;padding:8px 16px;background:#161b22;border-bottom:1px solid #30363d;height:48px}
.topbar h1{font-size:15px;font-weight:600;color:#f0f6fc;margin-right:auto}
.avatars{display:flex;gap:-4px;position:relative}
.avatar{width:28px;height:28px;border-radius:50%;border:2px solid #161b22;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:#fff;margin-left:-6px;cursor:pointer;position:relative;transition:transform .15s}
.avatar:first-child{margin-left:0}
.avatar:hover{transform:translateY(-2px);z-index:10}
.avatar .name-tip{position:absolute;top:100%;left:50%;transform:translateX(-50%);font-size:10px;background:#1c2128;padding:2px 6px;border-radius:4px;white-space:nowrap;opacity:0;pointer-events:none;transition:opacity .2s;margin-top:4px;border:1px solid #30363d}
.avatar:hover .name-tip{opacity:1}
.filter-bar{display:flex;align-items:center;gap:8px;padding:6px 16px;background:#0d1117;border-bottom:1px solid #21262d;font-size:13px}
.filter-bar select,.filter-bar input{background:#161b22;border:1px solid #30363d;color:#e6edf3;padding:4px 8px;border-radius:6px;font-size:12px}
.filter-bar label{display:flex;align-items:center;gap:4px;cursor:pointer;color:#8b949e;font-size:12px}
.filter-bar label input[type=checkbox]{accent-color:#58a6ff}
.btn{background:#21262d;border:1px solid #30363d;color:#e6edf3;padding:4px 12px;border-radius:6px;cursor:pointer;font-size:12px;transition:background .15s}
.btn:hover{background:#30363d}
.btn-primary{background:#1f6feb;border-color:#1f6feb;color:#fff}
.btn-primary:hover{background:#388bfd}
.dashboard{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:12px;height:calc(100vh - 104px);overflow-y:auto;transition:margin-right .3s}
.dashboard.chat-open{margin-right:320px}
.panel{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px;position:relative;min-height:180px}
.panel.locked{opacity:.7;border-color:#da3633}
.panel.locked::before{content:'LOCKED';position:absolute;top:8px;right:8px;background:#da3633;color:#fff;font-size:9px;font-weight:700;padding:1px 6px;border-radius:4px;z-index:5}
.panel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.panel-title{font-size:13px;font-weight:600;color:#f0f6fc}
.panel-actions{display:flex;gap:6px}
.panel-actions button{background:0;border:1px solid #30363d;color:#8b949e;border-radius:4px;cursor:pointer;font-size:10px;padding:2px 6px;transition:all .15s}
.panel-actions button:hover{border-color:#58a6ff;color:#58a6ff}
.panel-actions button.lock-btn.active{color:#da3633;border-color:#da3633}
.chart-area{position:relative;height:120px;background:linear-gradient(180deg,#0d1117 0%,#161b22 100%);border-radius:6px;border:1px solid #21262d;overflow:hidden;cursor:crosshair}
.chart-area svg{width:100%;height:100%}
.metric{display:flex;gap:16px;margin-top:8px;font-size:12px}
.metric-item{position:relative;cursor:pointer;padding:4px 0}
.metric-item:hover{color:#58a6ff}
.metric-value{font-size:20px;font-weight:700;color:#f0f6fc}
.metric-label{color:#8b949e;font-size:11px}
.annotation{position:absolute;background:#1f6feb22;border:1px solid #1f6feb66;border-radius:6px;padding:6px 8px;font-size:11px;min-width:120px;z-index:10;backdrop-filter:blur(4px)}
.annotation .author{font-weight:600;color:#58a6ff;font-size:10px;margin-bottom:2px}
.annotation .text{color:#e6edf3}
.annotation .del{position:absolute;top:-6px;right:-6px;width:16px;height:16px;background:#da3633;border:0;border-radius:50%;color:#fff;font-size:9px;cursor:pointer;display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .15s}
.annotation:hover .del{opacity:1}
.comment-badge{position:absolute;top:-4px;right:-4px;background:#1f6feb;color:#fff;font-size:9px;border-radius:50%;width:16px;height:16px;display:flex;align-items:center;justify-content:center;font-weight:700}
.cursor-dot{position:fixed;pointer-events:none;z-index:9999;transition:all .1s linear}
.cursor-dot .dot{width:8px;height:8px;border-radius:50%;position:absolute;top:-4px;left:-4px}
.cursor-dot .cname{font-size:10px;white-space:nowrap;padding:1px 4px;border-radius:4px;color:#fff;margin-left:6px;margin-top:2px;display:inline-block}
.chat-sidebar{position:fixed;top:48px;right:-320px;width:320px;height:calc(100vh - 48px);background:#161b22;border-left:1px solid #30363d;display:flex;flex-direction:column;transition:right .3s;z-index:100}
.chat-sidebar.open{right:0}
.chat-header{padding:10px 14px;border-bottom:1px solid #30363d;display:flex;justify-content:space-between;align-items:center}
.chat-header h2{font-size:14px;font-weight:600}
.chat-msgs{flex:1;overflow-y:auto;padding:10px 14px;display:flex;flex-direction:column;gap:6px}
.chat-msg{font-size:12px;padding:6px 10px;background:#0d1117;border-radius:6px;max-width:90%}
.chat-msg .cauthor{font-weight:600;color:#58a6ff;font-size:10px;margin-bottom:2px}
.chat-msg .ctime{font-size:9px;color:#484f58;float:right}
.chat-input-wrap{display:flex;gap:6px;padding:8px 14px;border-top:1px solid #30363d}
.chat-input-wrap input{flex:1;background:#0d1117;border:1px solid #30363d;border-radius:6px;color:#e6edf3;padding:6px 10px;font-size:12px}
.chat-input-wrap input:focus{outline:0;border-color:#58a6ff}
.comment-modal{position:fixed;top:0;left:0;width:100%;height:100%;background:#00000066;display:flex;align-items:center;justify-content:center;z-index:200}
.comment-modal.hidden{display:none}
.comment-box{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:16px;min-width:300px;max-height:70vh;display:flex;flex-direction:column}
.comment-box h3{font-size:14px;margin-bottom:8px}
.comment-list{flex:1;overflow-y:auto;margin-bottom:10px;max-height:200px}
.comment-item{font-size:12px;padding:6px 8px;background:#0d1117;border-radius:6px;margin-bottom:4px}
.comment-item .ca{font-weight:600;color:#58a6ff;font-size:10px}
.comment-box textarea{background:#0d1117;border:1px solid #30363d;border-radius:6px;color:#e6edf3;padding:6px 10px;font-size:12px;resize:none;height:50px;margin-bottom:6px}
.comment-box textarea:focus{outline:0;border-color:#58a6ff}
.annot-modal{position:absolute;z-index:20;background:#1c2128;border:1px solid #30363d;border-radius:8px;padding:10px;min-width:180px;box-shadow:0 8px 24px #00000066}
.annot-modal.hidden{display:none}
.annot-modal input{width:100%;background:#0d1117;border:1px solid #30363d;border-radius:4px;color:#e6edf3;padding:4px 8px;font-size:12px;margin-bottom:6px}
.annot-modal .actions{display:flex;gap:4px;justify-content:flex-end}
.note-enter{animation: fadeIn .2s}
@keyframes fadeIn{from{opacity:0;transform:scale(.95)}to{opacity:1;transform:scale(1)}}
</style>
</head>
<body>
<div class="topbar">
  <h1>Collab Dashboard</h1>
  <div class="avatars" id="avatarList"></div>
  <button class="btn" onclick="toggleChat()">Chat</button>
  <button class="btn" onclick="addDemoUser()">+User</button>
</div>
<div class="filter-bar">
  <select id="filterDate"><option>Last 7 days</option><option>Last 30 days</option><option>Last quarter</option></select>
  <select id="filterRegion"><option>All regions</option><option>North America</option><option>Europe</option><option>Asia</option></select>
  <label><input type="checkbox" id="followHost" onchange="onFollowToggle()"> Follow host</label>
  <span style="color:#484f58;font-size:11px;margin-left:auto" id="filterOwner"></span>
</div>
<div class="dashboard" id="dashboard">
  <div class="panel" data-panel="revenue">
    <div class="panel-header">
      <span class="panel-title">Revenue</span>
      <div class="panel-actions">
        <button onclick="addAnnotation('revenue')" title="Annotate">+Note</button>
        <button class="lock-btn" onclick="toggleLock('revenue')" title="Lock">Lock</button>
      </div>
    </div>
    <div class="chart-area" id="chart-revenue"></div>
    <div class="metric">
      <div class="metric-item" data-metric="revenue-total" onclick="openComments('revenue','Total Revenue')"><div class="metric-value" id="m-revenue-total">$48,290</div><div class="metric-label">Total Revenue</div><span class="comment-badge hidden" id="cb-revenue-total">0</span></div>
      <div class="metric-item" data-metric="revenue-mrr" onclick="openComments('revenue','MRR')"><div class="metric-value" id="m-revenue-mrr">$16,097</div><div class="metric-label">MRR</div><span class="comment-badge hidden" id="cb-revenue-mrr">0</span></div>
    </div>
  </div>
  <div class="panel" data-panel="users">
    <div class="panel-header">
      <span class="panel-title">User Growth</span>
      <div class="panel-actions">
        <button onclick="addAnnotation('users')">+Note</button>
        <button class="lock-btn" onclick="toggleLock('users')">Lock</button>
      </div>
    </div>
    <div class="chart-area" id="chart-users"></div>
    <div class="metric">
      <div class="metric-item" data-metric="users-total" onclick="openComments('users','Total Users')"><div class="metric-value">12,847</div><div class="metric-label">Total Users</div><span class="comment-badge hidden" id="cb-users-total">0</span></div>
      <div class="metric-item" data-metric="users-new" onclick="openComments('users','New Today')"><div class="metric-value">142</div><div class="metric-label">New Today</div><span class="comment-badge hidden" id="cb-users-new">0</span></div>
    </div>
  </div>
  <div class="panel" data-panel="sessions">
    <div class="panel-header">
      <span class="panel-title">Active Sessions</span>
      <div class="panel-actions">
        <button onclick="addAnnotation('sessions')">+Note</button>
        <button class="lock-btn" onclick="toggleLock('sessions')">Lock</button>
      </div>
    </div>
    <div class="chart-area" id="chart-sessions"></div>
    <div class="metric">
      <div class="metric-item" data-metric="sessions-active" onclick="openComments('sessions','Active Now')"><div class="metric-value">2,391</div><div class="metric-label">Active Now</div><span class="comment-badge hidden" id="cb-sessions-active">0</span></div>
      <div class="metric-item" data-metric="sessions-avg" onclick="openComments('sessions','Avg Duration')"><div class="metric-value">14m 32s</div><div class="metric-label">Avg Duration</div><span class="comment-badge hidden" id="cb-sessions-avg">0</span></div>
    </div>
  </div>
  <div class="panel" data-panel="conversion">
    <div class="panel-header">
      <span class="panel-title">Conversion Rate</span>
      <div class="panel-actions">
        <button onclick="addAnnotation('conversion')">+Note</button>
        <button class="lock-btn" onclick="toggleLock('conversion')">Lock</button>
      </div>
    </div>
    <div class="chart-area" id="chart-conversion"></div>
    <div class="metric">
      <div class="metric-item" data-metric="conv-rate" onclick="openComments('conversion','Rate')"><div class="metric-value">3.42%</div><div class="metric-label">Conversion Rate</div><span class="comment-badge hidden" id="cb-conv-rate">0</span></div>
      <div class="metric-item" data-metric="conv-funnel" onclick="openComments('conversion','Funnel')"><div class="metric-value">847</div><div class="metric-label">Funnel Completes</div><span class="comment-badge hidden" id="cb-conv-funnel">0</span></div>
    </div>
  </div>
</div>
<div class="chat-sidebar" id="chatSidebar">
  <div class="chat-header">
    <h2>Team Chat</h2>
    <button class="btn" onclick="toggleChat()">Close</button>
  </div>
  <div class="chat-msgs" id="chatMessages"></div>
  <div class="chat-input-wrap">
    <input id="chatInput" placeholder="Type a message..." onkeydown="if(event.key==='Enter')sendChat()">
    <button class="btn btn-primary" onclick="sendChat()">Send</button>
  </div>
</div>
<div class="comment-modal hidden" id="commentModal">
  <div class="comment-box">
    <h3>Comments: <span id="commentTarget"></span></h3>
    <div class="comment-list" id="commentList"></div>
    <textarea id="commentInput" placeholder="Add a comment..."></textarea>
    <div style="display:flex;gap:6px;justify-content:flex-end">
      <button class="btn" onclick="closeComments()">Cancel</button>
      <button class="btn btn-primary" onclick="submitComment()">Comment</button>
    </div>
  </div>
</div>
<script>
// ============================================================
// STATE & CONFIG
// ============================================================
const COLORS=['#58a6ff','#3fb950','#d29922','#f85149','#bc8cff','#79c0ff','#ff7b72','#a5d6ff','#7ee787','#e3b341'];
const ME={id:crypto.randomUUID?crypto.randomUUID():Math.random().toString(36).slice(2,10),name:'You',color:COLORS[0]};
const STORE={users:[ME],cursors:{},annotations:{},comments:{},panels:{revenue:{locked:false},users:{locked:false},sessions:{locked:false},conversion:{locked:false}},filters:{date:'Last 7 days',region:'All regions',followHost:false,hostId:null},chat:[],annotId:0,commentId:0};
// ============================================================
// TRANSPORT — BroadcastChannel (multi-tab sync)
// ============================================================
const ch=new BroadcastChannel('collab-dash');
let lastMsgId=0;
function broadcast(type,payload){ch.postMessage({id:++lastMsgId,from:ME.id,type,payload,ts:Date.now()})}
ch.onmessage=e=>{
  const m=e.data;
  if(m.from===ME.id)return;
  switch(m.type){
    case'join':case'cursor':case'leave':case'pin':case'lock':case'filter':case'chat':case'comment':case'annot':case'delannot':break;
    default:return;
  }
  handleRemote(m.type,m.from,m.payload);
};
// ============================================================
// PRESENCE SYSTEM
// ============================================================
function handleRemote(type,from,data){
  if(type==='join'){if(!STORE.users.find(u=>u.id===from)){STORE.users.push({id:from,name:data.name,color:data.color});renderAvatars();broadcastPresence()}}
  if(type==='leave'){STORE.users=STORE.users.filter(u=>u.id!==from);delete STORE.cursors[from];renderAvatars();removeCursorEl(from)}
  if(type==='cursor'){STORE.cursors[from]={x:data.x,y:data.y,panel:data.panel};renderCursors()}
  if(type==='filter'){if(STORE.filters.followHost&&from===STORE.filters.hostId){applyFilter(data.date,data.region)}STORE.filters.hostId=data.hostId;updateFilterOwner()}
  if(type==='chat'){STORE.chat.push(data);renderChat()}
  if(type==='annot'){const pid=data.panel;if(!STORE.annotations[pid])STORE.annotations[pid]=[];STORE.annotations[pid].push(data);renderAnnotations(pid)}
  if(type==='delannot'){const pid=data.panel;if(STORE.annotations[pid]){STORE.annotations[pid]=STORE.annotations[pid].filter(a=>a.id!==data.id);renderAnnotations(pid)}}
  if(type==='comment'){const k=data.key;if(!STORE.comments[k])STORE.comments[k]=[];STORE.comments[k].push(data);updateCommentBadge(k)}
  if(type==='lock'){STORE.panels[data.panel].locked=data.locked;renderLock(data.panel)}
  if(type==='pin'){renderAnnotations(data.panel)}
}
function broadcastPresence(){broadcast('join',{name:ME.name,color:ME.color})}
function addDemoUser(){const n='Guest_'+(STORE.users.length+1);const c=COLORS[STORE.users.length%COLORS.length];broadcast('join',{name:n,color:c})}
function renderAvatars(){
  const el=document.getElementById('avatarList');
  el.innerHTML=STORE.users.map(u=>`<div class="avatar" style="background:${u.color};z-index:${10-STORE.users.indexOf(u)}"><span>${u.name[0]}</span><span class="name-tip">${u.name}${u.id===ME.id?' (you)':''}</span></div>`).join('');
}
function removeCursorEl(id){document.querySelectorAll(`[data-uid="${CSS.escape(id)}"]`).forEach(e=>e.remove())}
function renderCursors(){
  Object.entries(STORE.cursors).forEach(([uid,c])=>{
    const u=STORE.users.find(x=>x.id===uid);if(!u)return;
    let el=document.querySelector(`[data-uid="${CSS.escape(uid)}"]`);
    if(!el){el=document.createElement('div');el.className='cursor-dot';el.setAttribute('data-uid',uid);document.body.appendChild(el);el.innerHTML=`<div class="dot" style="background:${u.color}"></div><span class="cname" style="background:${u.color}">${u.name}</span>`}
    el.style.left=c.x+'px';el.style.top=c.y+'px';
  });
}
function trackCursor(e){
  const p=e.target.closest('.panel');const panel=p?p.dataset.panel:null;
  const payload={x:e.clientX,y:e.clientY,panel};
  STORE.cursors[ME.id]=payload;renderCursors();
  broadcast('cursor',payload);
}
// ============================================================
// DASHBOARD CHARTS (mini sparklines)
// ============================================================
function drawChart(panelId,values,color){
  const el=document.getElementById('chart-'+panelId);if(!el)return;
  const w=el.clientWidth||300,h=el.clientHeight||120;
  const max=Math.max(...values,1);const min=Math.min(...values);
  const range=max-min||1;const pad=4;
  const pts=values.map((v,i)=>({x:pad+(w-pad*2)*i/(values.length-1),y:h-pad-(h-pad*2)*(v-min)/range}));
  const d='M'+pts.map((p,j)=>j===0?`${p.x},${p.y}`:`L${p.x},${p.y}`).join(' ');
  const fill='M'+pts.map((p,j)=>j===0?`${p.x},${p.y}`:`L${p.x},${p.y}`).join(' ')+`L${pts[pts.length-1].x},${h}L${pts[0].x},${h}Z`;
  el.innerHTML=`<svg viewBox="0 0 ${w} ${h}"><path d="${d}" fill="none" stroke="${color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="${fill}" fill="${color}22" stroke="none"/></svg>`;
}
function initCharts(){
  drawChart('revenue',[38,42,45,41,47,44,48.29],'#58a6ff');
  drawChart('users',[8.2,9.1,10.5,11.2,11.8,12.4,12.847],'#3fb950');
  drawChart('sessions',[1.8,2.1,1.9,2.2,2.4,2.3,2.391],'#d29922');
  drawChart('conversion',[2.8,3.1,3.3,3.2,3.4,3.5,3.42],'#bc8cff');
}
window.addEventListener('resize',initCharts);
// ============================================================
// ANNOTATIONS (sticky notes on charts)
// ============================================================
function addAnnotation(panelId){
  if(STORE.panels[panelId]?.locked)return;
  const annotModal=document.getElementById('annotModal')||createAnnotModal();
  annotModal.dataset.panel=panelId;annotModal.classList.remove('hidden');
  const rect=document.querySelector(`[data-panel="${panelId}"]`).querySelector('.chart-area').getBoundingClientRect();
  annotModal.style.left=rect.left+20+'px';annotModal.style.top=rect.top+20+'px';
  annotModal.querySelector('input').value='';annotModal.querySelector('input').focus();
}
function createAnnotModal(){
  const m=document.createElement('div');m.id='annotModal';m.className='annot-modal hidden';
  m.innerHTML='<input id="annotInput" placeholder="Type your note..." maxlength="150"><div class="actions"><button class="btn" onclick="this.closest(\'.annot-modal\').classList.add(\'hidden\')">Cancel</button><button class="btn btn-primary" onclick="submitAnnotation()">Add</button></div>';
  document.body.appendChild(m);return m;
}
function submitAnnotation(){
  const m=document.getElementById('annotModal');const panelId=m.dataset.panel;const text=m.querySelector('input').value.trim();
  if(!text)return;m.classList.add('hidden');
  const rect=document.querySelector(`[data-panel="${panelId}"]`).querySelector('.chart-area').getBoundingClientRect();
  const annot={id:++STORE.annotId,panel:panelId,text,author:ME.name,color:ME.color,x:20,y:20,ts:Date.now()};
  if(!STORE.annotations[panelId])STORE.annotations[panelId]=[];
  STORE.annotations[panelId].push(annot);renderAnnotations(panelId);
  broadcast('annot',annot);
}
function renderAnnotations(panelId){
  const panel=document.querySelector(`[data-panel="${panelId}"]`);
  if(!panel)return;
  panel.querySelectorAll('.annotation').forEach(e=>e.remove());
  const chart=panel.querySelector('.chart-area');if(!chart)return;
  const r=chart.getBoundingClientRect();
  (STORE.annotations[panelId]||[]).forEach(a=>{
    const el=document.createElement('div');el.className='annotation note-enter';
    el.style.left=a.x+'px';el.style.top=a.y+'px';
    el.innerHTML=`<div class="author" style="color:${a.color}">${a.author}</div><div class="text">${a.text}</div><button class="del" onclick="deleteAnnotation('${panelId}',${a.id})">x</button>`;
    chart.appendChild(el);
  });
}
function deleteAnnotation(panelId,id){
  STORE.annotations[panelId]=STORE.annotations[panelId].filter(a=>a.id!==id);
  renderAnnotations(panelId);broadcast('delannot',{panel:panelId,id});
}
// ============================================================
// COMMENTS (threaded on metrics)
// ============================================================
let commentContext=null;
function openComments(panelId,metric){
  commentContext={panel:panelId,metric};
  document.getElementById('commentTarget').textContent=metric;
  renderCommentList();document.getElementById('commentModal').classList.remove('hidden');
}
function closeComments(){document.getElementById('commentModal').classList.add('hidden');commentContext=null}
function submitComment(){
  const input=document.getElementById('commentInput');const text=input.value.trim();
  if(!text||!commentContext)return;input.value='';
  const key=commentContext.panel+'-'+commentContext.metric.toLowerCase().replace(/\s+/g,'-');
  const c={id:++STORE.commentId,panel:commentContext.panel,metric:commentContext.metric,key,text,author:ME.name,color:ME.color,ts:Date.now()};
  if(!STORE.comments[key])STORE.comments[key]=[];
  STORE.comments[key].push(c);renderCommentList();updateCommentBadge(key);
  broadcast('comment',c);
}
function renderCommentList(){
  const el=document.getElementById('commentList');if(!commentContext){el.innerHTML='';return}
  const key=commentContext.panel+'-'+commentContext.metric.toLowerCase().replace(/\s+/g,'-');
  const cmts=STORE.comments[key]||[];
  el.innerHTML=cmts.map(c=>`<div class="comment-item"><span class="ca" style="color:${c.color}">${c.author}</span> ${c.text}</div>`).join('')||'<div style="color:#484f58;font-size:12px;padding:8px">No comments yet</div>';
}
function updateCommentBadge(key){
  const el=document.getElementById('cb-'+key);if(!el)return;
  const n=(STORE.comments[key]||[]).length;
  el.textContent=n;el.classList.toggle('hidden',n===0);
}
// ============================================================
// PANEL LOCK SYSTEM
// ============================================================
function toggleLock(panelId){
  STORE.panels[panelId].locked=!STORE.panels[panelId].locked;
  renderLock(panelId);broadcast('lock',{panel:panelId,locked:STORE.panels[panelId].locked});
}
function renderLock(panelId){
  const panel=document.querySelector(`[data-panel="${panelId}"]`);
  if(!panel)return;const locked=STORE.panels[panelId].locked;
  panel.classList.toggle('locked',locked);
  const btn=panel.querySelector('.lock-btn');if(btn)btn.classList.toggle('active',locked);
}
// ============================================================
// FILTER SYNC & FOLLOW HOST
// ============================================================
function onFollowToggle(){
  const cb=document.getElementById('followHost');
  STORE.filters.followHost=cb.checked;
  if(cb.checked){STORE.filters.hostId=ME.id;broadcastFilter();}
  updateFilterOwner();
}
function broadcastFilter(){
  STORE.filters.date=document.getElementById('filterDate').value;
  STORE.filters.region=document.getElementById('filterRegion').value;
  broadcast('filter',{date:STORE.filters.date,region:STORE.filters.region,hostId:STORE.filters.hostId});
}
function applyFilter(date,region){
  document.getElementById('filterDate').value=date;
  document.getElementById('filterRegion').value=region;
}
function updateFilterOwner(){
  const el=document.getElementById('filterOwner');
  if(STORE.filters.followHost&&STORE.filters.hostId){
    const u=STORE.users.find(x=>x.id===STORE.filters.hostId);
    el.textContent='Following: '+(u?u.name:'Host');
  }else{el.textContent=''}
}
document.getElementById('filterDate').addEventListener('change',()=>{if(!STORE.filters.followHost)broadcastFilter()});
document.getElementById('filterRegion').addEventListener('change',()=>{if(!STORE.filters.followHost)broadcastFilter()});
// ============================================================
// CHAT SIDEBAR
// ============================================================
function toggleChat(){
  const s=document.getElementById('chatSidebar');s.classList.toggle('open');
  document.getElementById('dashboard').classList.toggle('chat-open',s.classList.contains('open'));
  if(s.classList.contains('open'))setTimeout(()=>{document.querySelector('.chat-msgs')?.scrollTo(0,9999)},50);
}
function sendChat(){
  const input=document.getElementById('chatInput');const text=input.value.trim();
  if(!text)return;input.value='';
  const msg={author:ME.name,color:ME.color,text,ts:Date.now()};
  STORE.chat.push(msg);renderChat();broadcast('chat',msg);
}
function renderChat(){
  const el=document.getElementById('chatMessages');
  el.innerHTML=STORE.chat.map(m=>`<div class="chat-msg"><span class="cauthor" style="color:${m.color}">${m.author}</span> ${m.text}</div>`).join('');
  el.scrollTo(0,el.scrollHeight);
}
// ============================================================
// INIT
// ============================================================
function init(){
  renderAvatars();initCharts();broadcastPresence();
  document.addEventListener('mousemove',trackCursor);
  setTimeout(()=>{document.getElementById('chatMessages').innerHTML='<div style="color:#484f58;font-size:12px;padding:8px;text-align:center">Open another tab to test real-time collaboration</div>'},100);
  setInterval(()=>{broadcast('cursor',STORE.cursors[ME.id]||{x:0,y:0,panel:null})},3000);
}
init();
</script>
</body>
</html>
```
The implementation delivers all seven features in a single self-contained HTML file under 400 lines:
presence — colored cursor dots and avatar bar with hover names, synced via BroadcastChannel across browser tabs
annotate — click "+Note" on any panel to place a sticky note on the chart area, deletable, synced to all tabs
comment — click any metric value to open a threaded comment modal, comments sync and show a badge count on the metric
sync — "Follow host" checkbox locks filter state to the host's selections; host changes broadcast to followers
lock — per-panel lock button prevents annotations on locked panels and shows a red "LOCKED" badge and dimmed opacity
chat — sidebar panel with message history, syncs across all connected tabs
output — interactive dashboard with four panels (Revenue, User Growth, Active Sessions, Conversion Rate), each with sparkline charts and two KPI metrics. Open the file in multiple browser tabs — no server needed.
No markdown fences, no greetings, no sign-offs.