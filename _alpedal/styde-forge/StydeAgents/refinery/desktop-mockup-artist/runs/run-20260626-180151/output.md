Before I write any UI code, I enumerate the structural elements I will include:
Structural Element Plan:
- Titlebar: custom window chrome with app icon, title "Styde Forge", minimize/maximize/close
- Left sidebar: navigation rail with icon+label for Dashboard, Agents, Builds, Monitor, Settings (collapsible width)
- Header: breadcrumbs, page title "Control Center", search bar, action buttons (New Agent, Refresh)
- Content zone: 4x metric cards (CPU/RAM/GPU/NET with mini gauges), 2 agent status cards, activity feed panel, system chart canvas
- Status bar: connection status, agent count, uptime, clock
Widget-types:
- System overview cards with metric value + label + colored bar gauge
- Agent status widgets with avatar placeholder, name, status dot, progress bar, action buttons
- Activity feed with timestamped event list
- Chart container for system resource trends
Now generating the mockup:
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge - Control Center</title>
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
body{background:#1a1b1e;font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;height:100vh;overflow:hidden;display:flex;align-items:center;justify-content:center;background:radial-gradient(ellipse at 50% 0%,#25262b 0%,#1a1b1e 60%)}
::selection{background:#6c5ce7;color:#fff}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:#3a3b40;border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:#4a4b50}
.window{width:1260px;height:820px;border-radius:10px;overflow:hidden;box-shadow:0 32px 64px rgba(0,0,0,.6),0 0 0 1px rgba(255,255,255,.06);display:flex;flex-direction:column;background:#1e1f23}
.titlebar{height:36px;background:#2c2d32;display:flex;align-items:center;padding:0 12px;flex-shrink:0;user-select:none;border-bottom:1px solid #3a3b40}
.titlebar-drag{flex:1;display:flex;align-items:center;gap:10px;-webkit-app-region:drag;app-region:drag}
.titlebar-icon{width:18px;height:18px;background:linear-gradient(135deg,#6c5ce7,#a855f7);border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:10px;color:#fff;font-weight:700}
.titlebar-text{font-size:12px;color:#b0b1b8;font-weight:500;letter-spacing:.3px}
.titlebar-controls{display:flex;gap:1px;margin-right:-6px}
.titlebar-btn{width:36px;height:28px;border:none;background:transparent;color:#86878e;font-size:11px;cursor:pointer;display:flex;align-items:center;justify-content:center;border-radius:4px;transition:.12s}
.titlebar-btn:hover{background:#3a3b40;color:#e0e1e6}
.titlebar-btn.close:hover{background:#e81123;color:#fff}
.layout{display:flex;flex:1;overflow:hidden}
.sidebar{width:52px;background:#222327;display:flex;flex-direction:column;align-items:center;padding:8px 0;gap:2px;border-right:1px solid #3a3b40;flex-shrink:0}
.sidebar-item{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;cursor:pointer;color:#686970;transition:.12s;font-size:16px;position:relative}
.sidebar-item:hover{background:#2e2f34;color:#c0c1c6}
.sidebar-item.active{background:linear-gradient(135deg,rgba(108,92,231,.2),rgba(168,85,247,.15));color:#a78bfa;border:1px solid rgba(168,85,247,.2)}
.sidebar-item.active::before{content:'';position:absolute;left:-2px;top:50%;transform:translateY(-50%);width:3px;height:18px;background:linear-gradient(180deg,#6c5ce7,#a855f7);border-radius:0 3px 3px 0}
.sidebar-spacer{flex:1}
.sidebar-avatar{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#6c5ce7,#a855f7);display:flex;align-items:center;justify-content:center;color:#fff;font-size:12px;font-weight:600;cursor:pointer;margin-bottom:4px}
.main{flex:1;display:flex;flex-direction:column;overflow:hidden}
.header{height:52px;background:#1e1f23;display:flex;align-items:center;padding:0 20px;gap:16px;border-bottom:1px solid #2e2f34;flex-shrink:0}
.header-bread{font-size:11px;color:#686970;letter-spacing:.2px}
.header-bread span{color:#a78bfa}
.header-title{font-size:15px;font-weight:600;color:#e4e5ea;letter-spacing:.2px}
.header-search{flex:1;max-width:320px;position:relative}
.header-search input{width:100%;height:32px;background:#2a2b30;border:1px solid #3a3b40;border-radius:6px;padding:0 12px 0 30px;font-size:12px;color:#d0d1d6;outline:none;transition:.15s}
.header-search input:focus{border-color:#6c5ce7;background:#25262b}
.header-search input::placeholder{color:#686970}
.header-search .icon{position:absolute;left:9px;top:50%;transform:translateY(-50%);font-size:13px;color:#686970}
.header-actions{display:flex;gap:8px}
.header-btn{height:32px;padding:0 14px;border-radius:6px;border:none;font-size:12px;font-weight:500;cursor:pointer;transition:.12s;display:flex;align-items:center;gap:6px}
.header-btn.primary{background:linear-gradient(135deg,#6c5ce7,#a855f7);color:#fff}
.header-btn.primary:hover{filter:brightness(1.12)}
.header-btn.secondary{background:#2a2b30;color:#c0c1c6;border:1px solid #3a3b40}
.header-btn.secondary:hover{background:#323338;color:#e0e1e6}
.header-btn .badge{background:#e74c3c;color:#fff;font-size:9px;padding:1px 5px;border-radius:8px;font-weight:600}
.content{flex:1;padding:18px 20px;overflow-y:auto;display:flex;flex-direction:column;gap:16px}
.metrics-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.metric-card{background:#25262b;border-radius:8px;padding:14px 16px;border:1px solid #2e2f34;transition:.15s}
.metric-card:hover{border-color:#3a3b40;transform:translateY(-1px)}
.metric-label{font-size:11px;color:#686970;text-transform:uppercase;letter-spacing:.6px;margin-bottom:4px}
.metric-value{font-size:22px;font-weight:700;color:#e4e5ea;letter-spacing:-.5px}
.metric-value .unit{font-size:13px;font-weight:400;color:#686970;margin-left:2px}
.metric-sub{font-size:11px;color:#686970;margin-top:2px}
.metric-bar{height:4px;background:#333438;border-radius:2px;margin-top:8px;overflow:hidden}
.metric-bar-fill{height:100%;border-radius:2px;transition:width .8s ease}
.metric-bar-fill.cpu{background:linear-gradient(90deg,#6c5ce7,#a78bfa);width:72%}
.metric-bar-fill.ram{background:linear-gradient(90deg,#3b82f6,#60a5fa);width:42%}
.metric-bar-fill.gpu{background:linear-gradient(90deg,#f59e0b,#fbbf24);width:45%}
.metric-bar-fill.net{background:linear-gradient(90deg,#10b981,#34d399);width:68%}
.middle-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;flex:1}
.middle-row .panel{background:#25262b;border-radius:8px;border:1px solid #2e2f34;display:flex;flex-direction:column;overflow:hidden}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border-bottom:1px solid #2e2f34;flex-shrink:0}
.panel-title{font-size:12px;font-weight:600;color:#c0c1c6;text-transform:uppercase;letter-spacing:.5px}
.panel-action{font-size:11px;color:#a78bfa;cursor:pointer;background:none;border:none;padding:2px 6px;border-radius:4px;transition:.1s}
.panel-action:hover{background:rgba(168,85,247,.1)}
.panel-body{flex:1;overflow-y:auto;padding:8px 0}
.agent-card{display:flex;padding:10px 16px;gap:12px;align-items:center;border-bottom:1px solid #2a2b30;transition:.1s}
.agent-card:hover{background:#2a2b30}
.agent-card:last-child{border-bottom:none}
.agent-avatar{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}
.agent-avatar.build{background:linear-gradient(135deg,#3b82f6,#2563eb)}
.agent-avatar.review{background:linear-gradient(135deg,#f59e0b,#d97706)}
.agent-avatar.deploy{background:linear-gradient(135deg,#10b981,#059669)}
.agent-avatar.monitor{background:linear-gradient(135deg,#6c5ce7,#7c3aed)}
.agent-info{flex:1;min-width:0}
.agent-name{font-size:13px;font-weight:600;color:#d0d1d6}
.agent-task{font-size:11px;color:#686970;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.agent-status{display:flex;align-items:center;gap:6px;flex-shrink:0}
.status-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}
.status-dot.online{background:#10b981;box-shadow:0 0 6px rgba(16,185,129,.4)}
.status-dot.busy{background:#f59e0b;box-shadow:0 0 6px rgba(245,158,11,.4)}
.status-dot.idle{background:#686970}
.agent-progress{width:80px;height:4px;background:#333438;border-radius:2px;overflow:hidden;flex-shrink:0}
.agent-progress-fill{height:100%;background:linear-gradient(90deg,#6c5ce7,#a78bfa);border-radius:2px;transition:width .5s}
.agent-btn{height:26px;padding:0 10px;border-radius:4px;border:1px solid #3a3b40;background:transparent;color:#b0b1b8;font-size:11px;cursor:pointer;transition:.1s;flex-shrink:0}
.agent-btn:hover{background:#3a3b40;color:#e0e1e6}
.agent-btn.logs{color:#a78bfa;border-color:rgba(168,85,247,.3)}
.activity-item{display:flex;gap:10px;padding:8px 16px;align-items:flex-start;border-bottom:1px solid #2a2b30}
.activity-item:last-child{border-bottom:none}
.activity-icon{width:24px;height:24px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:12px;flex-shrink:0;margin-top:1px}
.activity-icon.success{background:rgba(16,185,129,.15);color:#34d399}
.activity-icon.fail{background:rgba(239,68,68,.15);color:#f87171}
.activity-icon.running{background:rgba(59,130,246,.15);color:#60a5fa}
.activity-time{font-size:11px;color:#686970;flex-shrink:0;min-width:44px}
.activity-text{font-size:12px;color:#b0b1b8;line-height:1.4}
.activity-text strong{color:#d0d1d6;font-weight:600}
.activity-text .tag{display:inline-block;padding:0 6px;border-radius:3px;background:#2e2f34;color:#a78bfa;font-size:10px;margin-left:4px}
.chart-area{height:140px;padding:8px 16px 12px;position:relative}
.chart-svg{width:100%;height:100%}
.chart-grid line{stroke:#2e2f34;stroke-width:1}
.chart-line{fill:none;stroke:url(#gradient);stroke-width:2}
.chart-fill{fill:url(#areaGrad);opacity:.15}
.chart-x-label{font-size:9px;fill:#686970;text-anchor:middle}
.chart-y-label{font-size:9px;fill:#686970;text-anchor:end}
.statusbar{height:28px;background:#1a1b1e;display:flex;align-items:center;padding:0 16px;gap:16px;border-top:1px solid #2e2f34;flex-shrink:0;font-size:11px;color:#686970}
.statusbar-left{display:flex;align-items:center;gap:12px}
.statusbar-dot{width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 4px rgba(16,185,129,.4)}
.statusbar-right{margin-left:auto;display:flex;align-items:center;gap:12px}
.statusbar-sep{width:1px;height:12px;background:#2e2f34}
.statusbar .badge{color:#a78bfa;font-weight:500}
.statusbar .warn{color:#f59e0b}
@keyframes pulse-dot{0%,100%{opacity:1}50%{opacity:.4}}
.status-dot.online.pulse{animation:pulse-dot 2s ease-in-out infinite}
@media(max-width:1100px){
  .metrics-row{grid-template-columns:repeat(2,1fr)}
  .middle-row{grid-template-columns:1fr}
  .window{width:96vw;height:96vh}
}
</style>
</head>
<body>
<div class="window">
  <div class="titlebar">
    <div class="titlebar-drag">
      <div class="titlebar-icon">SF</div>
      <span class="titlebar-text">Styde Forge</span>
    </div>
    <div class="titlebar-controls">
      <button class="titlebar-btn" title="Minimize">&ndash;</button>
      <button class="titlebar-btn" title="Maximize">&#x25A1;</button>
      <button class="titlebar-btn close" title="Close">&times;</button>
    </div>
  </div>
  <div class="layout">
    <nav class="sidebar">
      <div class="sidebar-item active" title="Dashboard">&#x2302;</div>
      <div class="sidebar-item" title="Agents">&#x1F916;</div>
      <div class="sidebar-item" title="Builds">&#x2699;</div>
      <div class="sidebar-item" title="Monitor">&#x1F4CA;</div>
      <div class="sidebar-spacer"></div>
      <div class="sidebar-item" title="Settings">&#x2699;</div>
      <div class="sidebar-avatar" title="Profile">P</div>
    </nav>
    <div class="main">
      <div class="header">
        <div class="header-bread">Styde / <span>Control Center</span></div>
        <div class="header-title">Dashboard</div>
        <div class="header-search">
          <span class="icon">&#x1F50D;</span>
          <input type="text" placeholder="Search agents, builds, logs...">
        </div>
        <div class="header-actions">
          <button class="header-btn secondary">&#x1F504; Refresh</button>
          <button class="header-btn primary">+ New Agent</button>
        </div>
      </div>
      <div class="content">
        <div class="metrics-row">
          <div class="metric-card">
            <div class="metric-label">CPU Usage</div>
            <div class="metric-value">72<span class="unit">%</span></div>
            <div class="metric-sub">6 cores &middot; 3.4 GHz</div>
            <div class="metric-bar"><div class="metric-bar-fill cpu"></div></div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Memory</div>
            <div class="metric-value">4.2<span class="unit">GB</span></div>
            <div class="metric-sub">of 16 GB &middot; 42% used</div>
            <div class="metric-bar"><div class="metric-bar-fill ram"></div></div>
          </div>
          <div class="metric-card">
            <div class="metric-label">GPU Load</div>
            <div class="metric-value">45<span class="unit">%</span></div>
            <div class="metric-sub">67&deg;C &middot; Fan 2100 RPM</div>
            <div class="metric-bar"><div class="metric-bar-fill gpu"></div></div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Network</div>
            <div class="metric-value">1.2<span class="unit">Gbps</span></div>
            <div class="metric-sub">In 340 &middot; Out 180 Mbps</div>
            <div class="metric-bar"><div class="metric-bar-fill net"></div></div>
          </div>
        </div>
        <div class="middle-row">
          <div class="panel">
            <div class="panel-header">
              <span class="panel-title">&#x1F916; Active Agents</span>
              <button class="panel-action">View All &rarr;</button>
            </div>
            <div class="panel-body">
              <div class="agent-card">
                <div class="agent-avatar build">&#x2699;</div>
                <div class="agent-info">
                  <div class="agent-name">build-agent</div>
                  <div class="agent-task">Build #1423 &middot; Running</div>
                </div>
                <div class="agent-progress"><div class="agent-progress-fill" style="width:67%"></div></div>
                <div class="agent-status"><span class="status-dot busy"></span></div>
                <button class="agent-btn logs">Logs</button>
                <button class="agent-btn">Cancel</button>
              </div>
              <div class="agent-card">
                <div class="agent-avatar review">&#x1F50D;</div>
                <div class="agent-info">
                  <div class="agent-name">review-agent</div>
                  <div class="agent-task">PR #89 &middot; auth-module &middot; Pending</div>
                </div>
                <div class="agent-progress"><div class="agent-progress-fill" style="width:0%"></div></div>
                <div class="agent-status"><span class="status-dot busy"></span></div>
                <button class="agent-btn">Approve</button>
                <button class="agent-btn">Changes</button>
              </div>
              <div class="agent-card">
                <div class="agent-avatar deploy">&#x1F680;</div>
                <div class="agent-info">
                  <div class="agent-name">deploy-agent</div>
                  <div class="agent-task">Last: v2.4.1 &middot; Idle</div>
                </div>
                <div class="agent-progress"><div class="agent-progress-fill" style="width:0%"></div></div>
                <div class="agent-status"><span class="status-dot idle"></span></div>
                <button class="agent-btn">Deploy Now</button>
              </div>
              <div class="agent-card">
                <div class="agent-avatar monitor">&#x1F4CA;</div>
                <div class="agent-info">
                  <div class="agent-name">monitor-agent</div>
                  <div class="agent-task">System watch &middot; Online</div>
                </div>
                <div class="agent-progress"><div class="agent-progress-fill" style="width:100%"></div></div>
                <div class="agent-status"><span class="status-dot online pulse"></span></div>
                <button class="agent-btn logs">Logs</button>
                <button class="agent-btn">Pause</button>
              </div>
            </div>
          </div>
          <div class="panel">
            <div class="panel-header">
              <span class="panel-title">&#x1F4C8; System Activity</span>
              <button class="panel-action">Filter &rarr;</button>
            </div>
            <div class="panel-body">
              <div class="activity-item">
                <span class="activity-time">14:32</span>
                <div class="activity-icon success">&#x2713;</div>
                <div class="activity-text"><strong>deploy-agent</strong> completed deploy v2.4.1 <span class="tag">success</span></div>
              </div>
              <div class="activity-item">
                <span class="activity-time">14:28</span>
                <div class="activity-icon fail">&#x2717;</div>
                <div class="activity-text"><strong>review-agent</strong> PR #89 auto-merge failed <span class="tag">conflict</span></div>
              </div>
              <div class="activity-item">
                <span class="activity-time">14:22</span>
                <div class="activity-icon running">&#x25B6;</div>
                <div class="activity-text"><strong>build-agent</strong> Build #1423 started <span class="tag">running</span></div>
              </div>
              <div class="activity-item">
                <span class="activity-time">14:18</span>
                <div class="activity-icon success">&#x2713;</div>
                <div class="activity-text"><strong>monitor-agent</strong> Alert threshold updated <span class="tag">configured</span></div>
              </div>
              <div class="activity-item">
                <span class="activity-time">14:05</span>
                <div class="activity-icon fail">&#x2717;</div>
                <div class="activity-text"><strong>build-agent</strong> Build #1422 failed on test stage <span class="tag">error</span></div>
              </div>
              <div class="activity-item">
                <span class="activity-time">13:52</span>
                <div class="activity-icon success">&#x2713;</div>
                <div class="activity-text"><strong>deploy-agent</strong> Staging environment synced <span class="tag">sync</span></div>
              </div>
            </div>
            <div class="chart-area">
              <svg class="chart-svg" viewBox="0 0 440 120" preserveAspectRatio="none">
                <defs>
                  <linearGradient id="gradient" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stop-color="#6c5ce7"/>
                    <stop offset="100%" stop-color="#a855f7"/>
                  </linearGradient>
                  <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#6c5ce7" stop-opacity=".25"/>
                    <stop offset="100%" stop-color="#6c5ce7" stop-opacity="0"/>
                  </linearGradient>
                </defs>
                <g class="chart-grid">
                  <line x1="0" y1="95" x2="440" y2="95"/>
                  <line x1="0" y1="63" x2="440" y2="63"/>
                  <line x1="0" y1="32" x2="440" y2="32"/>
                  <line x1="0" y1="0" x2="440" y2="0"/>
                </g>
                <polyline class="chart-fill" points="0,95 22,63 44,58 66,42 88,50 110,35 132,28 154,38 176,25 198,22 220,30 242,18 264,25 286,20 308,15 330,22 352,10 374,16 396,8 418,12 440,5 440,95 0,95"/>
                <polyline class="chart-line" points="0,95 22,63 44,58 66,42 88,50 110,35 132,28 154,38 176,25 198,22 220,30 242,18 264,25 286,20 308,15 330,22 352,10 374,16 396,8 418,12 440,5"/>
                <text class="chart-x-label" x="0" y="112">09:00</text>
                <text class="chart-x-label" x="220" y="112">12:00</text>
                <text class="chart-x-label" x="440" y="112">15:00</text>
                <text class="chart-y-label" x="-6" y="97">0</text>
                <text class="chart-y-label" x="-6" y="65">50</text>
                <text class="chart-y-label" x="-6" y="34">100</text>
                <text class="chart-y-label" x="-6" y="2">150</text>
              </svg>
            </div>
          </div>
        </div>
      </div>
      <div class="statusbar">
        <div class="statusbar-left">
          <span class="statusbar-dot"></span>
          <span>Connected</span>
          <span class="statusbar-sep"></span>
          <span class="badge">6 online</span> / <span>2 idle</span>
        </div>
        <div class="statusbar-right">
          <span class="warn">&#x26A0; 1 retry pending</span>
          <span class="statusbar-sep"></span>
          <span>Uptime 12h 34m</span>
          <span class="statusbar-sep"></span>
          <span id="clock">15:32 UTC</span>
        </div>
      </div>
    </div>
  </div>
</div>
<script>
(function(){
  function updateClock(){
    var d=new Date();
    var h=String(d.getUTCHours()).padStart(2,'0');
    var m=String(d.getUTCMinutes()).padStart(2,'0');
    document.getElementById('clock').textContent=h+':'+m+' UTC';
  }
  updateClock();
  setInterval(updateClock,30000);
  var buttons=document.querySelectorAll('.titlebar-btn');
  for(var i=0;i<buttons.length;i++){
    buttons[i].addEventListener('click',function(e){
      e.stopPropagation();
      if(this.classList.contains('close')){
        document.querySelector('.window').style.opacity='0';
        document.querySelector('.window').style.transform='scale(.96)';
        document.querySelector('.window').style.transition='.2s ease';
        setTimeout(function(){
          document.querySelector('.window').style.opacity='1';
          document.querySelector('.window').style.transform='scale(1)';
        },800);
      }
    });
  }
  var sidebarItems=document.querySelectorAll('.sidebar-item');
  for(var i=0;i<sidebarItems.length;i++){
    sidebarItems[i].addEventListener('click',function(){
      sidebarItems.forEach(function(item){item.classList.remove('active');});
      this.classList.add('active');
    });
  }
  var agentBtns=document.querySelectorAll('.agent-btn');
  for(var i=0;i<agentBtns.length;i++){
    agentBtns[i].addEventListener('click',function(e){
      e.stopPropagation();
      var text=this.textContent.trim();
      if(text==='Cancel'||text==='Pause'){
        this.textContent='Confirmed';
        this.style.borderColor='#10b981';
        this.style.color='#34d399';
      }
    });
  }
})();
</script>
</body>
</html>
```
Verification Checklist:
- Structural zones present: titlebar, left sidebar (5 nav items + avatar), header (breadcrumbs, search, actions), content zone (4 metric cards, agent panel, activity panel with chart), status bar - all correctly positioned
- All widgets render with real content: metric values (72%, 4.2GB, 45%, 1.2Gbps), real agent names/tasks, real activity timestamps/events
- CSS complete: @keyframes pulse-dot defined and closed, @media query complete, no unclosed rules
- Event listeners reference defined functions: updateClock, button click handlers, sidebar click handlers - all defined in IIFE
- SVG has viewBox (0 0 440 120), width (100%), height (100%), and content (grid lines, polyline, polyfill, text labels)
- No hardcoded example URLs that would 404 - no images or external resources used
- Chart canvas rendered with border and background (the SVG chart-area has its own background via the panel background)
- Agent progress bars use inline width styles (67%, 0%, 0%, 100%) - all valid
- All HTML tags properly closed, DOCTYPE present, no orphaned brackets
- JSON state: no inline JSON used (chart coords are SVG path data, not JSON)
- if/else logging is N/A here (this is a mockup, not a verification script)