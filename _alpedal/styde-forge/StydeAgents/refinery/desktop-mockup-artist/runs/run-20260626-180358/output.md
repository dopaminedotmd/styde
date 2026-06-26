DESKTOP MOCKUP: Styde Forge Command Center
Layout: System Dashboard (Layout 1 from Blueprint)
Zones: titlebar, sidebar, header, content(4 metric cards + activity feed + 2 panels), statusbar
CSS: custom properties for all colors/spacing/typography
JS: const/let, arrow functions, template literals, no var, no function keyword
<!DOCTYPE html>
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Styde Forge Command Center</title>
<style>
:root {
  --bg-surface: #1e1e2e;
  --bg-mica: #252540;
  --bg-card: #2a2a3e;
  --bg-hover: #32324a;
  --bg-sidebar: #1a1a2a;
  --bg-titlebar: #16162a;
  --text-primary: #e0e0f0;
  --text-secondary: #9494b8;
  --text-muted: #6a6a88;
  --accent: #7c5cfc;
  --accent-hover: #9b7eff;
  --accent-dim: #5a3cc8;
  --green: #4ade80;
  --yellow: #facc15;
  --red: #f87171;
  --cyan: #22d3ee;
  --orange: #fb923c;
  --radius: 6px;
  --radius-lg: 10px;
  --shadow: 0 4px 24px rgba(0,0,0,.5);
  --shadow-sm: 0 2px 8px rgba(0,0,0,.35);
  --font: 'Segoe UI Variable','Segoe UI',-apple-system,system-ui,sans-serif;
  --title-h: 32px;
  --sidebar-w: 52px;
  --sidebar-exp: 200px;
  --status-h: 28px;
  --pad: 16px;
  --gap: 12px;
}
*,::before,::after{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;overflow:hidden;font-family:var(--font);background:var(--bg-surface);color:var(--text-primary);-webkit-font-smoothing:antialiased}
body{display:flex;flex-direction:column}
/* TITLEBAR */
.titlebar{height:var(--title-h);background:var(--bg-titlebar);display:flex;align-items:center;padding:0 12px;flex-shrink:0;gap:8px;user-select:none;-webkit-app-region:drag;border-bottom:1px solid rgba(255,255,255,.06)}
.titlebar-drag{flex:1;display:flex;align-items:center;gap:8px}
.titlebar-icon{width:16px;height:16px;background:var(--accent);border-radius:3px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:10px;color:#fff;font-weight:700}
.titlebar-title{font-size:12px;font-weight:600;color:var(--text-secondary);letter-spacing:.3px}
.titlebar-controls{display:flex;gap:2px;-webkit-app-region:no-drag}
.titlebar-btn{width:36px;height:24px;border:none;background:0 0;color:var(--text-secondary);font-size:11px;cursor:pointer;display:flex;align-items:center;justify-content:center;border-radius:4px;transition:all .15s}
.titlebar-btn:hover{background:rgba(255,255,255,.1);color:var(--text-primary)}
.titlebar-btn.close:hover{background:var(--red);color:#fff}
/* LAYOUT */
.layout{display:flex;flex:1;overflow:hidden}
.sidebar{width:var(--sidebar-w);background:var(--bg-sidebar);flex-shrink:0;display:flex;flex-direction:column;align-items:center;padding:8px 0;gap:4px;border-right:1px solid rgba(255,255,255,.06);transition:width .2s}
.sidebar.expanded{width:var(--sidebar-exp)}
.sidebar-item{width:40px;height:40px;border-radius:var(--radius);display:flex;align-items:center;justify-content:center;color:var(--text-muted);cursor:pointer;transition:all .15s;font-size:18px;position:relative;flex-shrink:0}
.sidebar-item:hover{background:var(--bg-hover);color:var(--text-primary)}
.sidebar-item.active{background:var(--accent-dim);color:var(--accent-hover);box-shadow:inset 0 0 0 1px var(--accent)}
.sidebar-item .label{display:none}
.sidebar.expanded .sidebar-item{width:100%;justify-content:flex-start;padding:0 14px;gap:10px;border-radius:0;font-size:14px}
.sidebar.expanded .sidebar-item .label{display:inline}
.sidebar-spacer{flex:1}
.sidebar-bottom{display:flex;flex-direction:column;align-items:center;gap:4px;padding-bottom:8px}
.sidebar.expanded .sidebar-bottom{align-items:stretch;padding:0 8px}
/* MAIN */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;background:var(--bg-mica)}
.header{display:flex;align-items:center;padding:12px var(--pad);gap:12px;flex-shrink:0;border-bottom:1px solid rgba(255,255,255,.05)}
.header-left{display:flex;align-items:center;gap:10px;flex:1}
.header-title{font-size:15px;font-weight:600;color:var(--text-primary)}
.header-badge{font-size:11px;padding:2px 8px;border-radius:10px;background:var(--accent-dim);color:var(--accent-hover)}
.search-box{display:flex;align-items:center;gap:6px;background:var(--bg-card);border:1px solid rgba(255,255,255,.08);border-radius:20px;padding:4px 14px;width:200px;transition:all .2s}
.search-box:focus-within{border-color:var(--accent);width:240px;box-shadow:0 0 0 2px rgba(124,92,252,.2)}
.search-box input{background:0 0;border:none;outline:none;color:var(--text-primary);font-size:13px;width:100%;font-family:var(--font)}
.search-box input::placeholder{color:var(--text-muted)}
.search-icon{color:var(--text-muted);font-size:13px}
.header-actions{display:flex;align-items:center;gap:6px}
.icon-btn{width:32px;height:32px;border:none;background:0 0;color:var(--text-secondary);border-radius:var(--radius);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;transition:all .15s}
.icon-btn:hover{background:var(--bg-hover);color:var(--text-primary)}
.avatar{width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--cyan));display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff;cursor:pointer}
/* CONTENT */
.content{flex:1;overflow-y:auto;padding:var(--pad);display:flex;flex-direction:column;gap:var(--gap)}
.content::-webkit-scrollbar{width:6px}
.content::-webkit-scrollbar-track{background:0 0}
.content::-webkit-scrollbar-thumb{background:rgba(255,255,255,.12);border-radius:3px}
.content::-webkit-scrollbar-thumb:hover{background:rgba(255,255,255,.2)}
/* METRIC GRID */
.metric-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--gap)}
.metric-card{background:var(--bg-card);border-radius:var(--radius-lg);padding:14px 16px;border:1px solid rgba(255,255,255,.06);transition:all .2s;cursor:default}
.metric-card:hover{transform:translateY(-1px);border-color:rgba(255,255,255,.12);box-shadow:var(--shadow-sm)}
.metric-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.metric-label{font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px}
.metric-icon{font-size:16px;opacity:.6}
.metric-value{font-size:22px;font-weight:700;color:var(--text-primary);margin-bottom:2px}
.metric-bar{height:4px;background:rgba(255,255,255,.08);border-radius:2px;overflow:hidden;margin-bottom:4px}
.metric-fill{height:100%;border-radius:2px;transition:width .6s ease}
.metric-fill.cpu{background:linear-gradient(90deg,var(--green),var(--yellow))}
.metric-fill.ram{background:linear-gradient(90deg,var(--accent),var(--cyan))}
.metric-fill.gpu{background:linear-gradient(90deg,var(--cyan),var(--accent))}
.metric-fill.net{background:linear-gradient(90deg,var(--orange),var(--yellow))}
.metric-sub{font-size:11px;color:var(--text-muted);display:flex;justify-content:space-between}
.metric-trend{font-size:11px}
.metric-trend.up{color:var(--green)}
.metric-trend.down{color:var(--red)}
/* TWO-COLUMN */
.cols2{display:grid;grid-template-columns:1.4fr 1fr;gap:var(--gap);flex:1;min-height:0}
.panel{background:var(--bg-card);border-radius:var(--radius-lg);border:1px solid rgba(255,255,255,.06);display:flex;flex-direction:column;overflow:hidden}
.panel-header{display:flex;align-items:center;justify-content:space-between;padding:12px 14px;border-bottom:1px solid rgba(255,255,255,.06);flex-shrink:0}
.panel-title{font-size:12px;font-weight:600;color:var(--text-primary);text-transform:uppercase;letter-spacing:.4px}
.panel-action{font-size:11px;color:var(--accent-hover);cursor:pointer;border:none;background:0 0;font-family:var(--font);padding:2px 6px;border-radius:4px;transition:all .15s}
.panel-action:hover{background:rgba(124,92,252,.15)}
.panel-body{padding:8px;flex:1;overflow-y:auto}
.panel-body::-webkit-scrollbar{width:4px}
.panel-body::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:2px}
/* ACTIVITY FEED */
.activity-item{display:flex;align-items:flex-start;gap:10px;padding:8px 6px;border-radius:var(--radius);cursor:default;transition:background .15s}
.activity-item:hover{background:var(--bg-hover)}
.activity-dot{width:8px;height:8px;border-radius:50%;margin-top:5px;flex-shrink:0}
.activity-dot.green{background:var(--green);box-shadow:0 0 6px var(--green)}
.activity-dot.red{background:var(--red);box-shadow:0 0 6px var(--red)}
.activity-dot.yellow{background:var(--yellow);box-shadow:0 0 6px var(--yellow)}
.activity-dot.blue{background:var(--cyan);box-shadow:0 0 6px var(--cyan)}
.activity-content{flex:1;min-width:0}
.activity-line{font-size:13px;color:var(--text-primary);line-height:1.4}
.activity-line strong{color:var(--accent-hover);font-weight:600}
.activity-meta{font-size:11px;color:var(--text-muted);margin-top:2px;display:flex;gap:8px}
.activity-icon{font-size:14px;width:20px;text-align:center;margin-top:3px}
/* GPU MONITOR */
.gauge-container{display:flex;flex-direction:column;gap:10px;padding:6px}
.gauge-item{display:flex;align-items:center;gap:10px}
.gauge-label{width:50px;font-size:12px;color:var(--text-secondary);flex-shrink:0}
.gauge-track{flex:1;height:22px;background:rgba(255,255,255,.06);border-radius:4px;overflow:hidden;position:relative}
.gauge-fill{height:100%;border-radius:4px;transition:width .8s ease;display:flex;align-items:center;padding:0 8px;font-size:10px;font-weight:600;color:#fff;justify-content:flex-end;min-width:30px}
.gauge-fill.temp{background:linear-gradient(90deg,var(--green),var(--yellow),var(--red))}
.gauge-fill.mem{background:linear-gradient(90deg,var(--accent),var(--cyan))}
.gauge-fill.fan{background:linear-gradient(90deg,var(--cyan),var(--accent))}
.gauge-value{font-size:12px;font-weight:600;color:var(--text-primary);width:40px;text-align:right;flex-shrink:0}
.gauge-sub{font-size:10px;color:var(--text-muted);display:block;margin-top:1px}
/* STATUS BAR */
.statusbar{height:var(--status-h);background:var(--bg-sidebar);display:flex;align-items:center;padding:0 14px;gap:16px;flex-shrink:0;font-size:11px;color:var(--text-muted);border-top:1px solid rgba(255,255,255,.06)}
.statusbar-dot{width:6px;height:6px;border-radius:50%;background:var(--green);box-shadow:0 0 4px var(--green);flex-shrink:0}
.statusbar-left{display:flex;align-items:center;gap:8px;flex:1}
.statusbar-right{display:flex;align-items:center;gap:12px}
.statusbar-item{display:flex;align-items:center;gap:4px}
.statusbar-badge{background:rgba(248,113,113,.2);color:var(--red);padding:1px 6px;border-radius:8px;font-size:10px;font-weight:600}
/* SMALL GAUGES BOTTOM */
.small-gauges{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:4px}
.small-gauge{background:rgba(255,255,255,.03);border-radius:var(--radius);padding:10px 12px}
.small-gauge-header{display:flex;justify-content:space-between;font-size:11px;color:var(--text-muted);margin-bottom:6px}
.small-gauge-track{height:6px;background:rgba(255,255,255,.06);border-radius:3px;overflow:hidden;margin-bottom:4px}
.small-gauge-fill{height:100%;border-radius:3px}
.small-gauge-fill.gpu-temp{background:linear-gradient(90deg,var(--green),var(--yellow),var(--red));width:67%}
.small-gauge-fill.gpu-mem{background:linear-gradient(90deg,var(--accent),var(--cyan));width:42%}
</style>
</head>
<body>
<div class=titlebar>
  <div class=titlebar-drag>
    <div class=titlebar-icon>S</div>
    <span class=titlebar-title>Styde Forge Command Center</span>
  </div>
  <div class=titlebar-controls>
    <button class=titlebar-btn aria-label=Minimize>&#x2014;</button>
    <button class=titlebar-btn aria-label=Maximize>&#x25A1;</button>
    <button class="titlebar-btn close" aria-label=Close>&#x2715;</button>
  </div>
</div>
<div class=layout>
  <div class=sidebar id=sidebar>
    <div class="sidebar-item active" data-label="Dashboard">&#x2302;</div>
    <div class=sidebar-item data-label="Agents">&#x2699;</div>
    <div class=sidebar-item data-label="Builds">&#x2692;</div>
    <div class=sidebar-item data-label="Monitor">&#x25C9;</div>
    <div class=sidebar-item data-label="Logs">&#x2630;</div>
    <div class=sidebar-spacer></div>
    <div class=sidebar-bottom>
      <div class=sidebar-item data-label="Settings">&#x2699;</div>
      <div class=sidebar-item data-label="Collapse" id=sidebarToggle>&#x25B6;</div>
    </div>
  </div>
  <div class=main>
    <div class=header>
      <div class=header-left>
        <span class=header-title>Dashboard</span>
        <span class=header-badge>v2.4.1</span>
        <div class=search-box>
          <span class=search-icon>&#x1F50D;</span>
          <input type=text placeholder="Search commands, agents, logs..." aria-label=Search>
        </div>
      </div>
      <div class=header-actions>
        <button class=icon-btn aria-label=Notifications>&#x1F514;</button>
        <button class=icon-btn aria-label=Add>&#x2795;</button>
        <div class=avatar>PA</div>
      </div>
    </div>
    <div class=content>
      <div class=metric-grid>
        <div class=metric-card>
          <div class=metric-top>
            <span class=metric-label>CPU</span>
            <span class=metric-icon>&#x1F5A5;</span>
          </div>
          <div class=metric-value>72%</div>
          <div class=metric-bar><div class="metric-fill cpu" style=width:72%></div></div>
          <div class=metric-sub><span>3.6 GHz</span><span class="metric-trend up">&#x2191; 8%</span></div>
        </div>
        <div class=metric-card>
          <div class=metric-top>
            <span class=metric-label>Memory</span>
            <span class=metric-icon>&#x1F4BE;</span>
          </div>
          <div class=metric-value>4.2 GB</div>
          <div class=metric-bar><div class="metric-fill ram" style=width:52%></div></div>
          <div class=metric-sub><span>8.0 GB total</span><span class="metric-trend up">&#x2191; 3%</span></div>
        </div>
        <div class=metric-card>
          <div class=metric-top>
            <span class=metric-label>GPU</span>
            <span class=metric-icon>&#x26A1;</span>
          </div>
          <div class=metric-value>45%</div>
          <div class=metric-bar><div class="metric-fill gpu" style=width:45%></div></div>
          <div class=metric-sub><span>67&#xB0;C / 2100 RPM</span><span class="metric-trend down">&#x2193; 2%</span></div>
        </div>
        <div class=metric-card>
          <div class=metric-top>
            <span class=metric-label>Network</span>
            <span class=metric-icon>&#x1F310;</span>
          </div>
          <div class=metric-value>1.2 Gbps</div>
          <div class=metric-bar><div class="metric-fill net" style=width:40%></div></div>
          <div class=metric-sub><span>Down: 850 Mbps</span><span class="metric-trend up">&#x2191; 12%</span></div>
        </div>
      </div>
      <div class=cols2>
        <div class=panel>
          <div class=panel-header>
            <span class=panel-title>Agent Activity Feed</span>
            <button class=panel-action>Clear all</button>
          </div>
          <div class=panel-body>
            <div class=activity-item>
              <span class=activity-icon>&#x2705;</span>
              <div class=activity-dot green></div>
              <div class=activity-content>
                <div class=activity-line><strong>Deploy-agent</strong> completed build #1423</div>
                <div class=activity-meta><span>14:32:18</span><span>2m ago</span></div>
              </div>
            </div>
            <div class=activity-item>
              <span class=activity-icon>&#x274C;</span>
              <div class=activity-dot red></div>
              <div class=activity-content>
                <div class=activity-line><strong>Review-agent</strong> PR #89 auth-module failed checks</div>
                <div class=activity-meta><span>14:28:04</span><span>6m ago</span></div>
              </div>
            </div>
            <div class=activity-item>
              <span class=activity-icon>&#x25B6;</span>
              <div class=activity-dot yellow></div>
              <div class=activity-content>
                <div class=activity-line><strong>Build-agent</strong> running build #1424 <em>in progress</em></div>
                <div class=activity-meta><span>14:22:47</span><span>11m ago</span></div>
              </div>
            </div>
            <div class=activity-item>
              <span class=activity-icon>&#x2705;</span>
              <div class=activity-dot green></div>
              <div class=activity-content>
                <div class=activity-line><strong>Test-agent</strong> passed all 342 tests (suite: api-v2)</div>
                <div class=activity-meta><span>14:18:30</span><span>15m ago</span></div>
              </div>
            </div>
            <div class=activity-item>
              <span class=activity-icon>&#x1F504;</span>
              <div class=activity-dot blue></div>
              <div class=activity-content>
                <div class=activity-line><strong>Index-agent</strong> reindexed 12,450 documents</div>
                <div class=activity-meta><span>14:10:12</span><span>23m ago</span></div>
              </div>
            </div>
          </div>
        </div>
        <div class=panel>
          <div class=panel-header>
            <span class=panel-title>GPU Monitor &amp; Memory</span>
            <button class=panel-action>Details</button>
          </div>
          <div class=panel-body>
            <div class=gauge-container>
              <div class=gauge-item>
                <span class=gauge-label>Temp</span>
                <div class=gauge-track><div class="gauge-fill temp" style=width:67%>67&#xB0;C</div></div>
                <span class=gauge-value>67&#xB0;</span>
              </div>
              <div class=gauge-item>
                <span class=gauge-label>Memory</span>
                <div class=gauge-track><div class="gauge-fill mem" style=width:42%>4.2GB</div></div>
                <span class=gauge-value>42%</span>
              </div>
              <div class=gauge-item>
                <span class=gauge-label>Fan</span>
                <div class=gauge-track><div class="gauge-fill fan" style=width:64%>2100</div></div>
                <span class=gauge-value>2100</span>
              </div>
            </div>
            <div class=small-gauges>
              <div class=small-gauge>
                <div class=small-gauge-header><span>GPU Core</span><span>1.68 GHz</span></div>
                <div class=small-gauge-track><div class="small-gauge-fill gpu-temp"></div></div>
                <div style="font-size:10px;color:var(--text-muted)">67% utilization</div>
              </div>
              <div class=small-gauge>
                <div class=small-gauge-header><span>VRAM</span><span>4.2 / 10 GB</span></div>
                <div class=small-gauge-track><div class="small-gauge-fill gpu-mem"></div></div>
                <div style="font-size:10px;color:var(--text-muted)">42% allocated</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class=statusbar>
      <div class=statusbar-left>
        <span class=statusbar-dot></span>
        <span>Connected</span>
        <span style="color:var(--text-muted)">|</span>
        <span>Uptime: 12h 34m</span>
      </div>
      <div class=statusbar-right>
        <span class=statusbar-item>&#x1F916; Agents: <strong style=color:var(--green)>6</strong> online / 2 idle</span>
        <span class=statusbar-item>&#x1F4CB; Queue: <strong>3</strong></span>
        <span class=statusbar-item><span class=statusbar-badge>&#x26A0; 1 retry</span></span>
        <span style=color:var(--text-muted)>|</span>
        <span>26 Jun 2026 20:04</span>
      </div>
    </div>
  </div>
</div>
<script>
const sidebar=document.getElementById('sidebar');
const toggleBtn=document.getElementById('sidebarToggle');
toggleBtn.addEventListener('click',()=>{
  const expanded=sidebar.classList.toggle('expanded');
  toggleBtn.innerHTML=expanded?'&#x25C0;':'&#x25B6;';
});
document.querySelectorAll('.sidebar-item[data-label]').forEach(el=>{
  el.addEventListener('click',function(){
    document.querySelectorAll('.sidebar-item.active').forEach(a=>a.classList.remove('active'));
    this.classList.add('active');
  });
});
document.querySelectorAll('.titlebar-btn').forEach(btn=>{
  btn.addEventListener('click',function(e){
    e.stopPropagation();
    const label=this.getAttribute('aria-label');
    if(label==='Close'){
      document.body.style.opacity='0';
      document.body.style.transition='opacity .3s';
      setTimeout(()=>{
        const overlay=document.createElement('div');
        overlay.style.cssText='position:fixed;inset:0;background:#1a1a1a;display:flex;align-items:center;justify-content:center;font-family:var(--font);color:#888;font-size:14px;z-index:9999';
        overlay.textContent='Application closed. Reload the page to restart.';
        document.body.innerHTML='';
        document.body.appendChild(overlay);
      },350);
    }else if(label==='Maximize'){
      const layout=document.querySelector('.layout');
      const isFull=layout.style.flex==='1 1 100vh';
      layout.style.flex=isFull?'':'1 1 100vh';
    }
  });
});
const searchInput=document.querySelector('.search-box input');
if(searchInput){
  searchInput.addEventListener('keydown',e=>{
    if(e.key==='Escape')searchInput.blur();
  });
}
const now=new Date();
const timeStr=String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0');
const clockSpan=document.querySelector('.statusbar-right span:last-child');
if(clockSpan){
  const d=String(now.getDate()).padStart(2,'0');
  const months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  clockSpan.textContent=d+' '+months[now.getMonth()]+' '+now.getFullYear()+' '+timeStr;
}
setInterval(()=>{
  const metricValues=document.querySelectorAll('.metric-value');
  const cpuVal=metricValues[0];
  const memVal=metricValues[1];
  const gpuVal=metricValues[2];
  const netVal=metricValues[3];
  if(cpuVal){
    const newCpu=Math.floor(45+Math.random()*35);
    cpuVal.textContent=newCpu+'%';
    const fill=cpuVal.closest('.metric-card').querySelector('.metric-fill');
    if(fill)fill.style.width=newCpu+'%';
  }
  if(gpuVal){
    const newGpu=Math.floor(25+Math.random()*40);
    gpuVal.textContent=newGpu+'%';
    const fill=gpuVal.closest('.metric-card').querySelector('.metric-fill');
    if(fill)fill.style.width=newGpu+'%';
  }
  if(netVal){
    const speeds=['1.2','0.8','0.6','0.9','1.1','1.4','1.0','0.7','1.3'];
    const sp=speeds[Math.floor(Math.random()*speeds.length)];
    netVal.textContent=sp+' Gbps';
    const fill=netVal.closest('.metric-card').querySelector('.metric-fill');
    if(fill){
      const pct=Math.round(parseFloat(sp)*70);
      fill.style.width=Math.min(pct,98)+'%';
    }
  }
},3000);
console.log('Styde Forge Command Center initialized');
console.log('Zones present: titlebar, sidebar, header, content (4 metric cards + activity feed + GPU monitor), statusbar');
</script>
</body>
</html>