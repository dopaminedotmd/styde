<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Live Collaboration Canvas</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0d1117;--surface:#161b22;--border:#30363d;--text:#e6edf3;--muted:#8b949e;--accent:#58a6ff;--green:#3fb950;--yellow:#d29922;--red:#f85149;--purple:#bc8cff;--radius:8px;--shadow:0 2px 8px rgba(0,0,0,0.3)}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);height:100vh;overflow:hidden}
.layout{display:grid;grid-template-columns:1fr 320px;grid-template-rows:48px 1fr;height:100vh;transition:grid-template-columns 0.3s}
.layout.chat-collapsed{grid-template-columns:1fr 0px}
.topbar{grid-column:1/-1;background:var(--surface);border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 16px;gap:12px;z-index:100}
.topbar .logo{font-weight:700;font-size:14px;color:var(--accent);white-space:nowrap}
.presence-bar{display:flex;align-items:center;gap:6px;flex:1;overflow-x:auto;padding:0 8px}
.avatar{width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;border:2px solid var(--border);cursor:pointer;position:relative;flex-shrink:0;transition:transform 0.15s}
.avatar:hover{transform:scale(1.15);z-index:2}
.avatar .cursor-label{position:absolute;top:100%;left:50%;transform:translateX(-50%);margin-top:2px;font-size:9px;background:var(--surface);padding:1px 4px;border-radius:3px;border:1px solid var(--border);white-space:nowrap;opacity:0;pointer-events:none;transition:opacity 0.15s}
.avatar:hover .cursor-label{opacity:1}
.avatar.self{border-color:var(--accent)}
.presence-more{font-size:11px;color:var(--muted);padding:0 4px}
.topbar-actions{display:flex;gap:8px;align-items:center}
.topbar-actions button{padding:4px 12px;border-radius:var(--radius);border:1px solid var(--border);background:var(--surface);color:var(--text);cursor:pointer;font-size:12px;transition:all 0.15s}
.topbar-actions button:hover{background:var(--border);border-color:var(--accent)}
.topbar-actions button.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.dashboard{overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:16px;position:relative}
.panel-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:16px}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px;position:relative;transition:border-color 0.2s}
.panel.locked{border-color:var(--yellow)}
.panel.focused{box-shadow:0 0 0 2px var(--accent)}
.panel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--border)}
.panel-title{font-size:13px;font-weight:600}
.panel-actions{display:flex;gap:6px;align-items:center}
.panel-actions button{padding:2px 8px;border-radius:4px;border:1px solid transparent;background:transparent;color:var(--muted);cursor:pointer;font-size:11px;transition:all 0.15s}
.panel-actions button:hover{background:var(--border);color:var(--text)}
.panel-actions button.lock-btn.active{color:var(--yellow);border-color:var(--yellow)}
.panel-actions button.comment-btn.active{color:var(--purple)}
.lock-badge{font-size:10px;color:var(--yellow);margin-left:4px;display:none}
.panel.locked .lock-badge{display:inline}
.chart-area{height:180px;position:relative;overflow:hidden}
.annotation-container{position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none}
.sticky-note{position:absolute;background:var(--yellow);color:#1a1a1a;padding:6px 8px;border-radius:4px;font-size:11px;max-width:180px;min-width:100px;box-shadow:var(--shadow);pointer-events:auto;cursor:move;z-index:10}
.sticky-note .note-author{font-weight:600;font-size:9px;margin-bottom:2px}
.sticky-note .note-text{font-size:10px;line-height:1.3}
.sticky-note .note-close{position:absolute;top:2px;right:4px;cursor:pointer;font-size:12px;color:rgba(0,0,0,0.4);line-height:1}
.sticky-note .note-close:hover{color:rgba(0,0,0,0.8)}
.cursor-overlay{position:fixed;pointer-events:none;z-index:9999}
.remote-cursor{position:fixed;width:8px;height:8px;border-radius:50%;pointer-events:none;z-index:9999;transition:left 0.08s linear,top 0.08s linear}
.remote-cursor::after{content:attr(data-label);position:absolute;left:10px;top:-4px;font-size:9px;background:inherit;color:#fff;padding:1px 4px;border-radius:3px;white-space:nowrap;opacity:0.9}
.filter-bar{display:flex;gap:8px;align-items:center;padding:8px 0;flex-wrap:wrap}
.filter-bar label{font-size:12px;color:var(--muted)}
.filter-bar select,.filter-bar input{padding:4px 8px;border-radius:4px;border:1px solid var(--border);background:var(--surface);color:var(--text);font-size:12px}
.filter-bar .follow-toggle{padding:4px 12px;border-radius:4px;border:1px solid var(--border);background:var(--surface);color:var(--text);cursor:pointer;font-size:11px;transition:all 0.15s}
.filter-bar .follow-toggle.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.filter-bar .follow-indicator{font-size:10px;color:var(--yellow)}
.stat-row{display:flex;gap:16px;margin-top:12px}
.stat{flex:1}
.stat-value{font-size:22px;font-weight:700}
.stat-label{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:0.5px}
.chat-panel{background:var(--surface);border-left:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden}
.chat-header{padding:12px 16px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;font-size:13px;font-weight:600}
.chat-header button{background:none;border:none;color:var(--muted);cursor:pointer;font-size:16px;padding:2px 6px;border-radius:4px}
.chat-header button:hover{background:var(--border);color:var(--text)}
.chat-messages{flex:1;overflow-y:auto;padding:8px 12px;display:flex;flex-direction:column;gap:6px}
.chat-msg{font-size:12px;line-height:1.4;padding:4px 8px;border-radius:6px;background:var(--bg)}
.chat-msg .msg-author{font-weight:600;font-size:10px;color:var(--accent)}
.chat-msg .msg-time{font-size:9px;color:var(--muted);float:right}
.chat-msg.system{background:transparent;font-style:italic;color:var(--muted);text-align:center;font-size:11px}
.chat-msg .msg-text{margin-top:1px}
.chat-input-area{padding:8px 12px;border-top:1px solid var(--border);display:flex;gap:8px}
.chat-input-area input{flex:1;padding:6px 10px;border-radius:6px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-size:12px;outline:none}
.chat-input-area input:focus{border-color:var(--accent)}
.chat-input-area button{padding:6px 14px;border-radius:6px;border:none;background:var(--accent);color:#fff;cursor:pointer;font-size:12px;font-weight:600}
.comment-thread{position:absolute;right:8px;top:40px;width:240px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--shadow);z-index:50;display:none}
.comment-thread.open{display:block}
.comment-thread-header{padding:8px 10px;border-bottom:1px solid var(--border);font-size:11px;font-weight:600;display:flex;justify-content:space-between}
.comment-thread-header button{background:none;border:none;color:var(--muted);cursor:pointer;font-size:14px}
.comment-list{max-height:200px;overflow-y:auto;padding:6px 10px}
.comment-item{font-size:11px;margin-bottom:6px;padding:4px 6px;background:var(--bg);border-radius:4px}
.comment-item .c-author{font-weight:600;font-size:9px;color:var(--accent)}
.comment-item .c-time{font-size:8px;color:var(--muted);float:right}
.comment-item .c-text{margin-top:1px}
.comment-input-area{padding:6px 10px;border-top:1px solid var(--border);display:flex;gap:6px}
.comment-input-area input{flex:1;padding:4px 8px;border-radius:4px;border:1px solid var(--border);background:var(--bg);color:var(--text);font-size:11px;outline:none}
.comment-input-area button{padding:4px 10px;border-radius:4px;border:none;background:var(--accent);color:#fff;cursor:pointer;font-size:11px}
.metric-card{padding:8px;background:var(--bg);border-radius:6px;margin-bottom:6px;cursor:pointer;transition:background 0.15s}
.metric-card:hover{background:var(--border)}
.metric-card .metric-name{font-size:11px;color:var(--muted)}
.metric-card .metric-val{font-size:16px;font-weight:600}
.annotation-btn{position:absolute;bottom:8px;right:8px;padding:4px 10px;border-radius:4px;border:1px solid var(--border);background:var(--surface);color:var(--muted);cursor:pointer;font-size:10px;z-index:5}
.annotation-btn:hover{color:var(--text);border-color:var(--accent)}
.annotation-btn.active{background:var(--yellow);color:#1a1a1a;border-color:var(--yellow)}
.tooltip{position:fixed;background:var(--surface);border:1px solid var(--border);border-radius:6px;padding:6px 10px;font-size:11px;box-shadow:var(--shadow);pointer-events:none;z-index:10000;display:none}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:10px 20px;font-size:13px;box-shadow:var(--shadow);z-index:99999;display:none;animation:toast-in 0.3s}
@keyframes toast-in{from{opacity:0;transform:translateX(-50%) translateY(20px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
.chart-svg{width:100%;height:100%}
.chart-svg line,.chart-svg path{transition:all 0.3s}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
</style>
</head>
<body>
<div class="layout" id="layout">
  <div class="topbar">
    <div class="logo">Canvas</div>
    <div class="presence-bar" id="presenceBar">
      <div id="presenceAvatars"></div>
      <span class="presence-more" id="presenceMore"></span>
    </div>
    <div class="topbar-actions">
      <button id="toggleChatBtn" title="Toggle chat sidebar">Chat</button>
      <button id="addAnnotationBtn" title="Add annotation mode">Annotate</button>
      <button id="leaveBtn" title="Leave session">Leave</button>
    </div>
  </div>
  <div class="dashboard" id="dashboard">
    <div class="filter-bar" id="filterBar">
      <label>Time range:</label>
      <select id="timeFilter">
        <option value="7d">Last 7 days</option>
        <option value="30d" selected>Last 30 days</option>
        <option value="90d">Last 90 days</option>
      </select>
      <label>Region:</label>
      <select id="regionFilter">
        <option value="all" selected>All regions</option>
        <option value="na">North America</option>
        <option value="eu">Europe</option>
        <option value="ap">Asia Pacific</option>
      </select>
      <label>Metric:</label>
      <select id="metricFilter">
        <option value="revenue" selected>Revenue</option>
        <option value="users">Active Users</option>
        <option value="conversion">Conversion</option>
      </select>
      <button class="follow-toggle" id="followToggle">Follow host</button>
      <span class="follow-indicator" id="followIndicator"></span>
    </div>
    <div class="panel-grid" id="panelGrid">
      <div class="panel" data-panel-id="revenue" id="panel-revenue">
        <div class="panel-header">
          <span class="panel-title">Revenue Trends</span>
          <div class="panel-actions">
            <span class="lock-badge">Locked</span>
            <button class="lock-btn" title="Lock/unlock panel">Lock</button>
            <button class="comment-btn" title="Comments">Comments</button>
          </div>
        </div>
        <div class="chart-area" id="chart-revenue"><canvas id="canvas-revenue" width="500" height="180"></canvas></div>
        <button class="annotation-btn" data-panel="revenue">+ Note</button>
      </div>
      <div class="panel" data-panel-id="users" id="panel-users">
        <div class="panel-header">
          <span class="panel-title">Active Users</span>
          <div class="panel-actions">
            <span class="lock-badge">Locked</span>
            <button class="lock-btn" title="Lock/unlock panel">Lock</button>
            <button class="comment-btn" title="Comments">Comments</button>
          </div>
        </div>
        <div class="chart-area" id="chart-users"><canvas id="canvas-users" width="500" height="180"></canvas></div>
        <button class="annotation-btn" data-panel="users">+ Note</button>
      </div>
      <div class="panel" data-panel-id="conversion" id="panel-conversion">
        <div class="panel-header">
          <span class="panel-title">Conversion Rate</span>
          <div class="panel-actions">
            <span class="lock-badge">Locked</span>
            <button class="lock-btn" title="Lock/unlock panel">Lock</button>
            <button class="comment-btn" title="Comments">Comments</button>
          </div>
        </div>
        <div class="chart-area" id="chart-conversion"><canvas id="canvas-conversion" width="500" height="180"></canvas></div>
        <button class="annotation-btn" data-panel="conversion">+ Note</button>
      </div>
      <div class="panel" data-panel-id="metrics" id="panel-metrics">
        <div class="panel-header">
          <span class="panel-title">Key Metrics</span>
          <div class="panel-actions">
            <span class="lock-badge">Locked</span>
            <button class="lock-btn" title="Lock/unlock panel">Lock</button>
            <button class="comment-btn" title="Comments">Comments</button>
          </div>
        </div>
        <div class="stat-row">
          <div class="stat"><div class="stat-value" id="stat-revenue">$--</div><div class="stat-label">Revenue</div></div>
          <div class="stat"><div class="stat-value" id="stat-users">--</div><div class="stat-label">Active Users</div></div>
          <div class="stat"><div class="stat-value" id="stat-conversion">--%</div><div class="stat-label">Conversion</div></div>
          <div class="stat"><div class="stat-value" id="stat-avgorder">$--</div><div class="stat-label">Avg Order</div></div>
        </div>
        <button class="annotation-btn" data-panel="metrics">+ Note</button>
      </div>
    </div>
  </div>
  <div class="chat-panel" id="chatPanel">
    <div class="chat-header">
      <span>Chat</span>
      <button id="closeChatBtn">&times;</button>
    </div>
    <div class="chat-messages" id="chatMessages"></div>
    <div class="chat-input-area">
      <input type="text" id="chatInput" placeholder="Type a message..." maxlength="500">
      <button id="chatSendBtn">Send</button>
    </div>
  </div>
</div>
<div class="cursor-overlay" id="cursorOverlay"></div>
<div class="tooltip" id="tooltip"></div>
<div class="toast" id="toast"></div>
<script>
// ============================================================
// Live Collaboration Canvas — WebSocket Real-time Dashboard
// ============================================================
const WS_URL = 'ws://localhost:8080/ws';
const USER_COLORS = ['#58a6ff','#3fb950','#d29922','#f85149','#bc8cff','#ff7b72','#79c0ff','#a5d6ff','#c9d1d9','#7ee787'];
const PRESENCE_UPDATE_MS = 50;
const CURSOR_BROADCAST_MS = 80;
let ws = null;
let reconnectTimer = null;
let connected = false;
let userId = 'user_' + Math.random().toString(36).slice(2, 8);
let userName = 'User_' + userId.slice(-4);
let userColor = USER_COLORS[Math.floor(Math.random() * USER_COLORS.length)];
let isHost = false;
let followMode = false;
let annotateMode = false;
let myCursor = {x:0, y:0, panel:null};
let remoteCursors = {};
let remoteUsers = {};
let panels = {};
let annotations = {};
let comments = {};
let locks = {};
let filterState = {time:'30d', region:'all', metric:'revenue'};
let messages = [];
let lastCursorSend = 0;
function getWsUrl(){return WS_URL}
function connect(){
  if(ws && (ws.readyState===WebSocket.OPEN||ws.readyState===WebSocket.CONNECTING))return;
  try{
    ws=new WebSocket(getWsUrl());
    ws.onopen=onOpen;
    ws.onclose=onClose;
    ws.onmessage=onMessage;
    ws.onerror=function(e){console.log('WS error:',e)}
  }catch(e){console.log('WS connection failed, running local-only mode');runLocalMode()}
}
function runLocalMode(){
  connected=true;
  addSystemMsg('Connected (local-only mode — no server)');
  // Simulate other users in local mode
  setTimeout(function(){
    addPresenceUser('demo_alice','Alice','#3fb950');
    addPresenceUser('demo_bob','Bob','#d29922');
    addSystemMsg('Alice joined the session');
    addSystemMsg('Bob joined the session');
    renderCharts();
  },300);
  renderCharts();
}
function onOpen(){
  connected=true;
  addSystemMsg('Connected to collaboration server');
  ws.send(JSON.stringify({type:'join',userId:userId,userName:userName,color:userColor}));
  renderCharts();
}
function onClose(){
  connected=false;
  addSystemMsg('Disconnected. Reconnecting in 3s...');
  if(reconnectTimer)clearTimeout(reconnectTimer);
  reconnectTimer=setTimeout(connect,3000);
}
function onMessage(e){
  try{
    var msg=JSON.parse(e.data);
    switch(msg.type){
      case 'welcome': handleWelcome(msg);break;
      case 'join': handleRemoteJoin(msg);break;
      case 'leave': handleRemoteLeave(msg);break;
      case 'cursor': handleRemoteCursor(msg);break;
      case 'annotation': handleRemoteAnnotation(msg);break;
      case 'delete_annotation': handleRemoteDeleteAnnotation(msg);break;
      case 'comment': handleRemoteComment(msg);break;
      case 'lock': handleRemoteLock(msg);break;
      case 'filter': handleRemoteFilter(msg);break;
      case 'chat': handleRemoteChat(msg);break;
      case 'state': handleStateSync(msg);break;
    }
  }catch(err){console.log('WS parse error:',err)}
}
function send(msg){if(ws&&ws.readyState===WebSocket.OPEN)ws.send(JSON.stringify(msg))}
// ---- Presence ----
function addPresenceUser(id,name,color){
  if(remoteUsers[id])return;
  remoteUsers[id]={id:id,name:name,color:color};
  renderPresence();
  renderRemoteCursors();
}
function removePresenceUser(id){
  delete remoteUsers[id];
  delete remoteCursors[id];
  renderPresence();
  renderRemoteCursors();
}
function renderPresence(){
  var container=document.getElementById('presenceAvatars');
  var more=document.getElementById('presenceMore');
  var selfAvatar=document.createElement('div');
  selfAvatar.className='avatar self';
  selfAvatar.style.background=userColor;
  selfAvatar.textContent=userName[0].toUpperCase();
  selfAvatar.title=userName+' (you)';
  var label=document.createElement('div');
  label.className='cursor-label';
  label.textContent=userName;
  selfAvatar.appendChild(label);
  var others=[];
  for(var k in remoteUsers)others.push(remoteUsers[k]);
  var maxShow=8;
  var shown=others.slice(0,maxShow);
  var html=selfAvatar.outerHTML;
  for(var i=0;i<shown.length;i++){
    var u=shown[i];
    var a=document.createElement('div');
    a.className='avatar';
    a.style.background=u.color;
    a.textContent=u.name[0].toUpperCase();
    a.title=u.name;
    var l=document.createElement('div');
    l.className='cursor-label';
    l.textContent=u.name;
    a.appendChild(l);
    html+=a.outerHTML;
  }
  container.innerHTML=html;
  more.textContent=others.length>maxShow?'+'+(others.length-maxShow):'';
}
function renderRemoteCursors(){
  var overlay=document.getElementById('cursorOverlay');
  overlay.innerHTML='';
  for(var id in remoteCursors){
    var c=remoteCursors[id];
    var u=remoteUsers[id];
    if(!u)continue;
    var el=document.createElement('div');
    el.className='remote-cursor';
    el.style.background=u.color;
    el.style.left=c.x+'px';
    el.style.top=c.y+'px';
    el.setAttribute('data-label',u.name);
    el.id='rc-'+id;
    overlay.appendChild(el);
  }
  // Remove stale cursor elements
  for(var id2 in remoteUsers){
    var el2=document.getElementById('rc-'+id2);
    if(el2 && !remoteCursors[id2])el2.remove();
  }
}
// ---- Handlers ----
function handleWelcome(msg){
  isHost=msg.isHost||false;
  userId=msg.userId||userId;
  if(msg.users){
    for(var i=0;i<msg.users.length;i++){
      var u=msg.users[i];
      if(u.id!==userId)addPresenceUser(u.id,u.name,u.color);
    }
  }
  if(msg.annotations){annotations=msg.annotations;renderAnnotations()}
  if(msg.comments){comments=msg.comments}
  if(msg.locks){locks=msg.locks;renderLocks()}
  if(msg.filterState){filterState=msg.filterState;syncFilterUI()}
  if(msg.messages){messages=msg.messages;renderChatMessages()}
  if(isHost){
    document.getElementById('followToggle').style.display='';
  }else{
    followMode=false;
    document.getElementById('followToggle').textContent='Follow host';
  }
  renderCharts();
}
function handleRemoteJoin(msg){
  if(msg.userId!==userId){
    addPresenceUser(msg.userId,msg.userName,msg.color);
    addSystemMsg(msg.userName+' joined the session');
  }
}
function handleRemoteLeave(msg){
  var u=remoteUsers[msg.userId];
  if(u)addSystemMsg(u.name+' left the session');
  removePresenceUser(msg.userId);
}
function handleRemoteCursor(msg){
  if(msg.userId!==userId){
    var now=Date.now();
    remoteCursors[msg.userId]=msg.cursor;
    renderRemoteCursors();
  }
}
function handleRemoteAnnotation(msg){
  if(!annotations[msg.panelId])annotations[msg.panelId]=[];
  annotations[msg.panelId].push(msg.annotation);
  renderAnnotations();
  addSystemMsg(msg.userName+' added a note on '+msg.panelId);
}
function handleRemoteDeleteAnnotation(msg){
  if(annotations[msg.panelId]){
    annotations[msg.panelId]=annotations[msg.panelId].filter(function(a){return a.id!==msg.annotationId});
    renderAnnotations();
  }
}
function handleRemoteComment(msg){
  if(!comments[msg.panelId])comments[msg.panelId]=[];
  comments[msg.panelId].push(msg.comment);
  var badge=document.querySelector('#panel-'+msg.panelId+' .comment-btn');
  if(badge)badge.textContent='Comments ('+comments[msg.panelId].length+')';
  var threads=document.querySelectorAll('.comment-thread[data-panel="'+msg.panelId+'"] .comment-list');
  if(threads.length)renderCommentThread(msg.panelId,threads[0]);
}
function handleRemoteLock(msg){
  if(msg.userId!==userId){
    locks[msg.panelId]=msg.locked?msg.userId:null;
    renderLocks();
    var panel=document.getElementById('panel-'+msg.panelId);
    if(panel){
      var lockBtn=panel.querySelector('.lock-btn');
      if(lockBtn)lockBtn.textContent=msg.locked?'Unlock':'Lock';
    }
    if(msg.locked){
      var u=remoteUsers[msg.userId];
      addSystemMsg((u?u.name:msg.userId)+' locked '+msg.panelId);
    }else{
      addSystemMsg(msg.panelId+' unlocked');
    }
  }
}
function handleRemoteFilter(msg){
  if(msg.userId!==userId){
    filterState=msg.filterState;
    syncFilterUI();
    renderCharts();
    if(followMode){
      var u=remoteUsers[msg.userId];
      addSystemMsg('View synced to '+(u?u.name:'host'));
    }
  }
}
function handleRemoteChat(msg){
  messages.push(msg);
  renderChatMessages();
  scrollChat();
  if(document.hidden){showToast('New message from '+msg.userName)}
}
function handleStateSync(msg){
  if(msg.annotations){annotations=msg.annotations;renderAnnotations()}
  if(msg.comments){comments=msg.comments}
  if(msg.locks){locks=msg.locks;renderLocks()}
}
// ---- Cursor tracking ----
document.addEventListener('mousemove',function(e){
  myCursor.x=e.clientX;
  myCursor.y=e.clientY;
  var panel=null;
  var el=e.target.closest('[data-panel-id]');
  if(el)panel=el.getAttribute('data-panel-id');
  myCursor.panel=panel;
  var now=Date.now();
  if(connected && now-lastCursorSend>CURSOR_BROADCAST_MS){
    lastCursorSend=now;
    send({type:'cursor',userId:userId,cursor:myCursor});
  }
});
// ---- Panel focus tracking ----
var focusedPanel=null;
document.addEventListener('mouseover',function(e){
  var panel=e.target.closest('[data-panel-id]');
  if(panel){
    var id=panel.getAttribute('data-panel-id');
    if(id!==focusedPanel){
      focusedPanel=id;
      document.querySelectorAll('.panel.focused').forEach(function(p){p.classList.remove('focused')});
      if(panel)panel.classList.add('focused');
    }
  }
});
// ---- Annotation mode ----
document.getElementById('addAnnotationBtn').addEventListener('click',function(){
  annotateMode=!annotateMode;
  this.classList.toggle('active',annotateMode);
  document.querySelectorAll('.annotation-btn').forEach(function(b){
    b.classList.toggle('active',annotateMode);
  });
  if(annotateMode)showToast('Click +Note on any panel to add a sticky note');
});
document.querySelectorAll('.annotation-btn').forEach(function(btn){
  btn.addEventListener('click',function(e){
    e.stopPropagation();
    var panelId=this.getAttribute('data-panel');
    var text=prompt('Enter annotation:');
    if(text && text.trim()){
      addAnnotation(panelId,text.trim());
      if(connected)send({type:'annotation',userId:userId,userName:userName,panelId:panelId,annotation:{id:Date.now().toString(),text:text,author:userName,x:120,y:60,color:userColor}});
    }
  });
});
function addAnnotation(panelId,text){
  if(!annotations[panelId])annotations[panelId]=[];
  annotations[panelId].push({id:Date.now().toString(),text:text,author:userName,x:80+Math.random()*100,y:20+Math.random()*80,color:userColor});
  renderAnnotations();
}
function renderAnnotations(){
  document.querySelectorAll('.annotation-container').forEach(function(c){c.remove()});
  for(var panelId in annotations){
    var panel=document.getElementById('panel-'+panelId);
    if(!panel)continue;
    var chartArea=panel.querySelector('.chart-area');
    if(!chartArea)continue;
    var container=document.createElement('div');
    container.className='annotation-container';
    annotations[panelId].forEach(function(a){
      var note=document.createElement('div');
      note.className='sticky-note';
      note.style.left=a.x+'px';
      note.style.top=a.y+'px';
      note.style.background=a.color||'#d29922';
      note.innerHTML='<div class="note-close" data-panel="'+panelId+'" data-id="'+a.id+'">&times;</div><div class="note-author">'+a.author+'</div><div class="note-text">'+a.text+'</div>';
      note.addEventListener('mousedown',function(e){
        if(e.target.classList.contains('note-close'))return;
        var startX=e.clientX,startY=e.clientY;
        var noteEl=this;
        var origX=parseInt(noteEl.style.left)||0;
        var origY=parseInt(noteEl.style.top)||0;
        function onMove(ev){
          noteEl.style.left=(origX+ev.clientX-startX)+'px';
          noteEl.style.top=(origY+ev.clientY-startY)+'px';
        }
        function onUp(){
          document.removeEventListener('mousemove',onMove);
          document.removeEventListener('mouseup',onUp);
          // Update annotation position
          var pid=noteEl.querySelector('.note-close').getAttribute('data-panel');
          var aid=noteEl.querySelector('.note-close').getAttribute('data-id');
          if(annotations[pid]){
            for(var i=0;i<annotations[pid].length;i++){
              if(annotations[pid][i].id===aid){
                annotations[pid][i].x=parseInt(noteEl.style.left)||0;
                annotations[pid][i].y=parseInt(noteEl.style.top)||0;
                break;
              }
            }
          }
          if(connected)send({type:'annotation_move',userId:userId,panelId:pid,annotationId:aid,x:parseInt(noteEl.style.left)||0,y:parseInt(noteEl.style.top)||0});
        }
        document.addEventListener('mousemove',onMove);
        document.addEventListener('mouseup',onUp);
      });
      container.appendChild(note);
    });
    chartArea.appendChild(container);
  }
  // Close buttons
  document.querySelectorAll('.note-close').forEach(function(el){
    el.addEventListener('click',function(e){
      e.stopPropagation();
      var panelId=this.getAttribute('data-panel');
      var id=this.getAttribute('data-id');
      if(annotations[panelId]){
        annotations[panelId]=annotations[panelId].filter(function(a){return a.id!==id});
        renderAnnotations();
        if(connected)send({type:'delete_annotation',userId:userId,panelId:panelId,annotationId:id});
      }
    });
  });
}
// ---- Panel lock ----
document.querySelectorAll('.lock-btn').forEach(function(btn){
  btn.addEventListener('click',function(){
    var panel=this.closest('[data-panel-id]');
    var panelId=panel.getAttribute('data-panel-id');
    var isLocked=!!locks[panelId];
    if(isLocked && locks[panelId]!==userId){
      showToast('Panel locked by another user');
      return;
    }
    locks[panelId]=isLocked?null:userId;
    renderLocks();
    this.textContent=isLocked?'Lock':'Unlock';
    if(connected)send({type:'lock',userId:userId,userName:userName,panelId:panelId,locked:!isLocked});
  });
});
function renderLocks(){
  document.querySelectorAll('.panel').forEach(function(p){
    var id=p.getAttribute('data-panel-id');
    if(locks[id]){
      p.classList.add('locked');
    }else{
      p.classList.remove('locked');
    }
  });
}
// ---- Comments ----
document.querySelectorAll('.comment-btn').forEach(function(btn){
  btn.addEventListener('click',function(){
    var panel=this.closest('[data-panel-id]');
    var panelId=panel.getAttribute('data-panel-id');
    var existing=panel.querySelector('.comment-thread');
    if(existing){
      existing.classList.toggle('open');
      return;
    }
    var thread=document.createElement('div');
    thread.className='comment-thread open';
    thread.setAttribute('data-panel',panelId);
    thread.innerHTML='<div class="comment-thread-header"><span>Comments</span><button class="close-thread">&times;</button></div><div class="comment-list"></div><div class="comment-input-area"><input type="text" placeholder="Add comment..." maxlength="300"><button>Post</button></div>';
    panel.appendChild(thread);
    var list=thread.querySelector('.comment-list');
    if(comments[panelId])renderCommentThread(panelId,list);
    thread.querySelector('.close-thread').addEventListener('click',function(){thread.classList.remove('open')});
    thread.querySelector('button').addEventListener('click',function(){
      var input=thread.querySelector('input');
      var text=input.value.trim();
      if(!text)return;
      if(!comments[panelId])comments[panelId]=[];
      var c={id:Date.now().toString(),text:text,author:userName,time:new Date().toISOString()};
      comments[panelId].push(c);
      renderCommentThread(panelId,list);
      btn.textContent='Comments ('+comments[panelId].length+')';
      input.value='';
      if(connected)send({type:'comment',userId:userId,userName:userName,panelId:panelId,comment:c});
    });
    thread.querySelector('input').addEventListener('keydown',function(e){
      if(e.key==='Enter')this.nextElementSibling.click();
    });
  });
});
function renderCommentThread(panelId,list){
  if(!comments[panelId])return;
  list.innerHTML='';
  comments[panelId].forEach(function(c){
    var div=document.createElement('div');
    div.className='comment-item';
    div.innerHTML='<span class="c-author">'+c.author+'</span><span class="c-time">'+formatTime(c.time)+'</span><div class="c-text">'+c.text+'</div>';
    list.appendChild(div);
  });
  list.scrollTop=list.scrollHeight;
}
function formatTime(iso){
  if(!iso)return '';
  var d=new Date(iso);
  return d.getHours().toString().padStart(2,'0')+':'+d.getMinutes().toString().padStart(2,'0');
}
// ---- Filters ----
document.querySelectorAll('#filterBar select').forEach(function(sel){
  sel.addEventListener('change',function(){
    filterState.time=document.getElementById('timeFilter').value;
    filterState.region=document.getElementById('regionFilter').value;
    filterState.metric=document.getElementById('metricFilter').value;
    if(connected)send({type:'filter',userId:userId,filterState:filterState,isHost:isHost});
    renderCharts();
  });
});
document.getElementById('followToggle').addEventListener('click',function(){
  if(isHost){
    var follow=this.textContent==='Stop sharing view';
    this.textContent=follow?'Share my view':'Stop sharing view';
    this.classList.toggle('active',!follow);
    document.getElementById('followIndicator').textContent=follow?'':'Sharing view with followers';
    showToast(follow?'Stopped sharing view':'Sharing your view with all participants');
    if(connected)send({type:'follow_toggle',userId:userId,active:!follow,isHost:isHost});
  }else{
    followMode=!followMode;
    this.textContent=followMode?'Unfollow host':'Follow host';
    this.classList.toggle('active',followMode);
    document.getElementById('followIndicator').textContent=followMode?'Following host view':'';
    showToast(followMode?'Following host view':'Stopped following');
    if(connected)send({type:'follow',userId:userId,active:followMode});
  }
});
function syncFilterUI(){
  document.getElementById('timeFilter').value=filterState.time||'30d';
  document.getElementById('regionFilter').value=filterState.region||'all';
  document.getElementById('metricFilter').value=filterState.metric||'revenue';
}
// ---- Charts ----
function generateData(metric,days){
  var data=[];
  var base=metric==='revenue'?45000:(metric==='users'?12000:3.2);
  var variance=metric==='revenue'?12000:(metric==='users'?3000:0.8);
  var trend=metric==='revenue'?200:(metric==='users'?50:0.01);
  for(var i=0;i<days;i++){
    var val=base+trend*i+Math.random()*variance-variance/2;
    if(metric==='conversion')val=Math.max(0.5,Math.min(8,val));
    data.push({label:'D'+(i+1),value:Math.round(val*100)/100});
  }
  return data;
}
var chartData={};
var chartDays=30;
function renderCharts(){
  var days=filterState.time==='7d'?7:(filterState.time==='30d'?30:90);
  chartDays=days;
  chartData.revenue=generateData('revenue',days);
  chartData.users=generateData('users',days);
  chartData.conversion=generateData('conversion',days);
  // Update stats
  var rev=chartData.revenue[chartData.revenue.length-1].value;
  var usr=chartData.users[chartData.users.length-1].value;
  var conv=chartData.conversion[chartData.conversion.length-1].value;
  document.getElementById('stat-revenue').textContent='$'+rev.toLocaleString('en-US',{maximumFractionDigits:0});
  document.getElementById('stat-users').textContent=Math.round(usr).toLocaleString();
  document.getElementById('stat-conversion').textContent=conv.toFixed(2)+'%';
  document.getElementById('stat-avgorder').textContent='$'+(rev/Math.max(usr,1)*100).toFixed(2);
  drawChart('canvas-revenue',chartData.revenue,'#58a6ff');
  drawChart('canvas-users',chartData.users,'#3fb950');
  drawChart('canvas-conversion',chartData.conversion,'#d29922');
}
function drawChart(canvasId,data,color){
  var canvas=document.getElementById(canvasId);
  if(!canvas)return;
  var rect=canvas.parentElement.getBoundingClientRect();
  canvas.width=rect.width||500;
  canvas.height=rect.height||180;
  var ctx=canvas.getContext('2d');
  var w=canvas.width,h=canvas.height;
  var pad={top:15,bottom:20,left:40,right:15};
  var cw=w-pad.left-pad.right;
  var ch=h-pad.top-pad.bottom;
  ctx.clearRect(0,0,w,h);
  ctx.fillStyle='#0d1117';
  ctx.fillRect(0,0,w,h);
  if(!data||data.length<2)return;
  var vals=data.map(function(d){return d.value});
  var min=Math.min.apply(null,vals);
  var max=Math.max.apply(null,vals);
  var range=max-min||1;
  // Grid lines
  ctx.strokeStyle='#21262d';
  ctx.lineWidth=1;
  for(var i=0;i<=4;i++){
    var y=pad.top+ch*(i/4);
    ctx.beginPath();
    ctx.moveTo(pad.left,y);
    ctx.lineTo(w-pad.right,y);
    ctx.stroke();
    var label=(max-(range*i/4)).toLocaleString('en-US',{maximumFractionDigits:0});
    ctx.fillStyle='#8b949e';
    ctx.font='9px sans-serif';
    ctx.textAlign='right';
    ctx.fillText(label,pad.left-4,y+3);
  }
  // Line
  ctx.beginPath();
  ctx.strokeStyle=color;
  ctx.lineWidth=2;
  ctx.lineJoin='round';
  ctx.lineCap='round';
  for(var i=0;i<data.length;i++){
    var x=pad.left+cw*(i/(data.length-1));
    var y=pad.top+ch-(data[i].value-min)/range*ch;
    if(i===0)ctx.moveTo(x,y);
    else ctx.lineTo(x,y);
  }
  ctx.stroke();
  // Fill
  var lastX=pad.left+cw;
  var lastY=pad.top+ch;
  ctx.lineTo(lastX,lastY);
  ctx.lineTo(pad.left,lastY);
  ctx.closePath();
  var grad=ctx.createLinearGradient(0,pad.top,0,pad.top+ch);
  grad.addColorStop(0,color+'40');
  grad.addColorStop(1,color+'05');
  ctx.fillStyle=grad;
  ctx.fill();
  // Dots on hover
  // Tooltip on click
  canvas.onclick=function(e){
    var r=this.getBoundingClientRect();
    var mx=e.clientX-r.left;
    var idx=Math.round((mx-pad.left)/cw*(data.length-1));
    idx=Math.max(0,Math.min(data.length-1,idx));
    var tooltip=document.getElementById('tooltip');
    tooltip.style.display='block';
    tooltip.style.left=(e.clientX+12)+'px';
    tooltip.style.top=(e.clientY-20)+'px';
    tooltip.innerHTML='<strong>'+data[idx].label+'</strong>: '+data[idx].value.toLocaleString('en-US',{maximumFractionDigits:2});
    setTimeout(function(){tooltip.style.display='none'},2000);
  };
}
// Resize handler
window.addEventListener('resize',function(){renderCharts()});
// ---- Chat ----
function addSystemMsg(text){
  messages.push({type:'system',text:text,time:new Date().toISOString(),userName:'System'});
  renderChatMessages();
  scrollChat();
}
function renderChatMessages(){
  var container=document.getElementById('chatMessages');
  container.innerHTML='';
  messages.forEach(function(m){
    var div=document.createElement('div');
    if(m.type==='system'){
      div.className='chat-msg system';
      div.textContent=m.text;
    }else{
      div.className='chat-msg';
      div.innerHTML='<span class="msg-author" style="color:'+(m.color||'var(--accent)')+'">'+m.userName+'</span><span class="msg-time">'+formatTime(m.time)+'</span><div class="msg-text">'+m.text+'</div>';
    }
    container.appendChild(div);
  });
}
function scrollChat(){
  var container=document.getElementById('chatMessages');
  container.scrollTop=container.scrollHeight;
}
document.getElementById('chatSendBtn').addEventListener('click',sendChat);
document.getElementById('chatInput').addEventListener('keydown',function(e){
  if(e.key==='Enter')sendChat();
});
function sendChat(){
  var input=document.getElementById('chatInput');
  var text=input.value.trim();
  if(!text)return;
  var msg={type:'chat',userId:userId,userName:userName,text:text,color:userColor,time:new Date().toISOString()};
  messages.push(msg);
  renderChatMessages();
  scrollChat();
  input.value='';
  if(connected)send(msg);
}
// ---- Toggle chat ----
document.getElementById('toggleChatBtn').addEventListener('click',function(){
  document.getElementById('layout').classList.toggle('chat-collapsed');
  this.classList.toggle('active');
  setTimeout(function(){renderCharts()},350);
});
document.getElementById('closeChatBtn').addEventListener('click',function(){
  document.getElementById('layout').classList.add('chat-collapsed');
  document.getElementById('toggleChatBtn').classList.remove('active');
  setTimeout(function(){renderCharts()},350);
});
// ---- Toast ----
function showToast(text){
  var t=document.getElementById('toast');
  t.textContent=text;
  t.style.display='block';
  setTimeout(function(){t.style.display='none'},3000);
}
// ---- Leave ----
document.getElementById('leaveBtn').addEventListener('click',function(){
  if(ws){send({type:'leave',userId:userId});ws.close()}
  showToast('Left session. Refresh to rejoin.');
});
// ---- Init ----
function init(){
  renderPresence();
  renderCharts();
  connect();
  // Periodic re-render
  setInterval(function(){if(!connected)return;send({type:'ping'})},30000);
}
// Override system msg to show in chat
var origAddSystemMsg=addSystemMsg;
addSystemMsg=function(text){
  origAddSystemMsg(text);
};
init();
</script>
</body>
</html>