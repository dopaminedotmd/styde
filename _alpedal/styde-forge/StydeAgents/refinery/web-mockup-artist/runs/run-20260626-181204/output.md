Styde Forge Dashboard — Monitoring & Control Center
A standalone HTML mockup showing the forge dashboard within the styde.se ecosystem. Responsive, interactive, unique layout.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge — Dashboard</title>
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0b0d11;--surface:#12151c;--surface2:#1a1e29;--border:#262b39;--text:#d6dae5;--text-dim:#7b8194;--accent:#6c8cff;--accent-glow:rgba(108,140,255,0.15);--green:#4ade80;--yellow:#fbbf24;--red:#f87171;--cyan:#22d3ee;--purple:#a78bfa;--radius:10px;--radius-sm:6px;--shadow:0 4px 24px rgba(0,0,0,0.4)}
html{font-size:15px}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.5;min-height:100vh;display:flex;flex-direction:column}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
/* header */
.site-header{background:var(--surface);border-bottom:1px solid var(--border);padding:0 1.5rem;display:flex;align-items:center;height:56px;position:sticky;top:0;z-index:100}
.site-header .logo{display:flex;align-items:center;gap:10px;font-size:1.2rem;font-weight:700;letter-spacing:-0.3px}
.site-header .logo svg{width:28px;height:28px}
.site-header .logo span{background:linear-gradient(135deg,#6c8cff,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.header-right{margin-left:auto;display:flex;align-items:center;gap:1rem}
.status-indicator{display:flex;align-items:center;gap:6px;font-size:0.8rem;color:var(--text-dim)}
.status-dot{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 8px rgba(74,222,128,0.5);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}
.header-time{font-size:0.8rem;color:var(--text-dim);font-variant-numeric:tabular-nums}
.profile-avatar{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#6c8cff,#a78bfa);display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:600;cursor:pointer}
/* nav */
.main-nav{background:var(--surface2);border-bottom:1px solid var(--border);padding:0 1.5rem;display:flex;align-items:center;height:44px;overflow-x:auto;gap:2px}
.main-nav::-webkit-scrollbar{height:2px}
.main-nav button{background:none;border:none;color:var(--text-dim);padding:0 1rem;height:100%;font-size:0.85rem;cursor:pointer;white-space:nowrap;border-bottom:2px solid transparent;transition:all 0.15s;font-family:inherit}
.main-nav button:hover{color:var(--text);background:var(--accent-glow)}
.main-nav button.active{color:var(--accent);border-bottom-color:var(--accent)}
.hamburger{display:none;background:none;border:none;color:var(--text);font-size:1.4rem;cursor:pointer;padding:4px;line-height:1}
/* breadcrumbs */
.breadcrumbs{display:flex;align-items:center;gap:6px;padding:0.6rem 1.5rem;font-size:0.8rem;color:var(--text-dim)}
.breadcrumbs a{color:var(--text-dim)}
.breadcrumbs a:hover{color:var(--accent);text-decoration:none}
.breadcrumbs .sep{color:var(--border)}
/* layout */
.dashboard{flex:1;padding:1.5rem;max-width:1440px;margin:0 auto;width:100%}
.page-title{font-size:1.6rem;font-weight:700;margin-bottom:0.25rem}
.page-sub{color:var(--text-dim);font-size:0.9rem;margin-bottom:1.5rem}
/* grid */
.metrics-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-bottom:1.5rem}
.metric-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1rem;position:relative;overflow:hidden}
.metric-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--accent);opacity:0.5}
.metric-card .label{font-size:0.75rem;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px}
.metric-card .value{font-size:1.8rem;font-weight:700;letter-spacing:-0.5px}
.metric-card .change{font-size:0.8rem;margin-top:2px}
.change.up{color:var(--green)}
.change.down{color:var(--red)}
/* main content columns */
.content-row{display:grid;grid-template-columns:1fr 340px;gap:1.5rem;margin-bottom:1.5rem}
@media(max-width:900px){.content-row{grid-template-columns:1fr}}
/* agent status table */
.section-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden}
.section-header{display:flex;align-items:center;justify-content:space-between;padding:1rem 1.25rem;border-bottom:1px solid var(--border);cursor:pointer;user-select:none}
.section-header h2{font-size:0.95rem;font-weight:600}
.section-header .toggle-icon{color:var(--text-dim);transition:transform 0.2s;font-size:0.8rem}
.section-header.collapsed .toggle-icon{transform:rotate(-90deg)}
.section-body{padding:0;transition:max-height 0.3s ease;overflow:hidden}
.section-body.hidden{max-height:0;padding:0}
.agent-table{width:100%;border-collapse:collapse;font-size:0.85rem}
.agent-table th{text-align:left;padding:0.75rem 1.25rem;color:var(--text-dim);font-weight:500;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;border-bottom:1px solid var(--border);background:var(--surface2)}
.agent-table td{padding:0.7rem 1.25rem;border-bottom:1px solid var(--border)}
.agent-table tr:last-child td{border-bottom:none}
.agent-table tr:hover{background:var(--accent-glow)}
.status-badge{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:10px;font-size:0.75rem;font-weight:500}
.status-badge.online{background:rgba(74,222,128,0.12);color:var(--green)}
.status-badge.processing{background:rgba(251,191,36,0.12);color:var(--yellow)}
.status-badge.idle{background:rgba(123,129,148,0.12);color:var(--text-dim)}
.status-badge.error{background:rgba(248,113,113,0.12);color:var(--red)}
/* activity feed */
.activity-feed{padding:0.5rem 0}
.activity-item{display:flex;align-items:flex-start;gap:10px;padding:0.7rem 1.25rem;border-bottom:1px solid var(--border);font-size:0.85rem}
.activity-item:last-child{border-bottom:none}
.activity-dot{width:8px;height:8px;border-radius:50%;margin-top:5px;flex-shrink:0}
.activity-dot.info{background:var(--accent)}
.activity-dot.success{background:var(--green)}
.activity-dot.warn{background:var(--yellow)}
.activity-dot.error{background:var(--red)}
.activity-text{flex:1}
.activity-text .msg{color:var(--text)}
.activity-text .time{color:var(--text-dim);font-size:0.75rem;margin-top:1px}
/* GPU monitor */
.gpu-list{padding:0.5rem 0}
.gpu-item{padding:0.7rem 1.25rem;border-bottom:1px solid var(--border)}
.gpu-item:last-child{border-bottom:none}
.gpu-item .gpu-name{font-size:0.85rem;font-weight:500;margin-bottom:4px}
.gpu-item .gpu-name .gpu-id{color:var(--text-dim);font-weight:400}
.gpu-bar-wrap{display:flex;align-items:center;gap:8px}
.gpu-bar{flex:1;height:6px;background:var(--surface2);border-radius:3px;overflow:hidden}
.gpu-bar-fill{height:100%;border-radius:3px;transition:width 0.4s}
.gpu-bar-fill.low{background:var(--green)}
.gpu-bar-fill.med{background:var(--yellow)}
.gpu-bar-fill.high{background:var(--red)}
.gpu-pct{font-size:0.75rem;color:var(--text-dim);width:32px;text-align:right;font-variant-numeric:tabular-nums}
/* footer */
.site-footer{margin-top:auto;border-top:1px solid var(--border);background:var(--surface);padding:1rem 1.5rem;display:flex;align-items:center;justify-content:space-between;font-size:0.8rem;color:var(--text-dim);flex-wrap:wrap;gap:8px}
.site-footer .footer-links{display:flex;gap:1.5rem}
.site-footer .footer-links a{color:var(--text-dim)}
.site-footer .footer-links a:hover{color:var(--accent);text-decoration:none}
/* collapsible handler via CSS */
.section-body{max-height:2000px}
.section-body.hidden{max-height:0}
/* responsive */
@media(max-width:640px){
  .site-header{padding:0 1rem}
  .main-nav{gap:0}
  .main-nav button{padding:0 0.6rem;font-size:0.8rem}
  .hamburger{display:block}
  .nav-desktop{display:none}
  .nav-desktop.open{display:flex;flex-direction:column;position:absolute;top:100%;left:0;right:0;background:var(--surface2);border-bottom:1px solid var(--border);z-index:99;height:auto}
  .nav-desktop.open button{height:40px;border-bottom:1px solid var(--border);width:100%;text-align:left;padding:0 1rem}
  .dashboard{padding:1rem}
  .metrics-grid{grid-template-columns:repeat(2,1fr)}
  .page-title{font-size:1.3rem}
  .site-footer{flex-direction:column;align-items:flex-start;gap:6px}
}
@media(max-width:400px){
  .metrics-grid{grid-template-columns:1fr}
  .header-time,.status-indicator{display:none}
}
</style>
</head>
<body>
<header class="site-header">
  <div class="logo">
    <svg viewBox="0 0 28 28" fill="none">
      <rect x="2" y="2" width="10" height="10" rx="2" fill="#6c8cff" opacity="0.8"/>
      <rect x="16" y="2" width="10" height="10" rx="2" fill="#a78bfa" opacity="0.8"/>
      <rect x="2" y="16" width="10" height="10" rx="2" fill="#6c8cff" opacity="0.4"/>
      <rect x="16" y="16" width="10" height="10" rx="2" fill="#a78bfa" opacity="0.4"/>
      <line x1="12" y1="7" x2="16" y2="7" stroke="#d6dae5" stroke-width="1.5" opacity="0.3"/>
      <line x1="7" y1="12" x2="7" y2="16" stroke="#d6dae5" stroke-width="1.5" opacity="0.3"/>
    </svg>
    <span>styde</span>
  </div>
  <div class="header-right">
    <div class="status-indicator">
      <span class="status-dot"></span>
      <span>All systems nominal</span>
    </div>
    <span class="header-time" id="headerTime">--:--:--</span>
    <div class="profile-avatar" title="Pontus / Alpedal">PA</div>
  </div>
</header>
<nav class="main-nav">
  <button class="hamburger" id="hamburgerBtn" aria-label="Toggle navigation">&#9776;</button>
  <div class="nav-desktop" id="navDesktop">
    <button class="active">Forge</button>
    <button>Agents</button>
    <button>Training</button>
    <button>Datasets</button>
    <button>Models</button>
    <button>Monitoring</button>
    <button>Settings</button>
  </div>
</nav>
<div class="breadcrumbs">
  <a href="#">styde.se</a>
  <span class="sep">&#8250;</span>
  <a href="#">Forge</a>
  <span class="sep">&#8250;</span>
  <span>Dashboard</span>
</div>
<main class="dashboard">
  <h1 class="page-title">Forge Dashboard</h1>
  <p class="page-sub">Real-time overview of agent training, inference pipelines, and cluster health</p>
  <div class="metrics-grid">
    <div class="metric-card">
      <div class="label">Active Agents</div>
      <div class="value">14</div>
      <div class="change up">+2 in last hour</div>
    </div>
    <div class="metric-card">
      <div class="label">Pipelines Active</div>
      <div class="value">7</div>
      <div class="change up">3 queued</div>
    </div>
    <div class="metric-card">
      <div class="label">GPU Utilisation</div>
      <div class="value">68<span style="font-size:1rem">%</span></div>
      <div class="change up">+12% from idle</div>
    </div>
    <div class="metric-card">
      <div class="label">Tokens / min</div>
      <div class="value">2.4M</div>
      <div class="change down">-8% from peak</div>
    </div>
    <div class="metric-card">
      <div class="label">Avg Latency</div>
      <div class="value">312ms</div>
      <div class="change up">within SLA</div>
    </div>
    <div class="metric-card">
      <div class="label">Backlog</div>
      <div class="value">43</div>
      <div class="change" style="color:var(--yellow)">12 pending review</div>
    </div>
  </div>
  <div class="content-row">
    <!-- left column -->
    <div>
      <!-- Agent Status (collapsible) -->
      <div class="section-card" style="margin-bottom:1.5rem">
        <div class="section-header" onclick="toggleCollapse(this)" role="button" tabindex="0" onkeydown="if(event.key==='Enter')toggleCollapse(this)">
          <h2>Agent Status</h2>
          <span class="toggle-icon">&#9660;</span>
        </div>
        <div class="section-body">
          <table class="agent-table">
            <thead>
              <tr>
                <th>Agent</th>
                <th>Status</th>
                <th>Task</th>
                <th>Progress</th>
                <th>Uptime</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>hermes-core</td>
                <td><span class="status-badge online">&#9679; Online</span></td>
                <td>Idle</td>
                <td>—</td>
                <td>12h 34m</td>
              </tr>
              <tr>
                <td>refinery-alpha</td>
                <td><span class="status-badge processing">&#9679; Processing</span></td>
                <td>BP Refinement #47</td>
                <td>62%</td>
                <td>4h 12m</td>
              </tr>
              <tr>
                <td>production-beta</td>
                <td><span class="status-badge processing">&#9679; Processing</span></td>
                <td>Batch eval v2.3</td>
                <td>88%</td>
                <td>2h 55m</td>
              </tr>
              <tr>
                <td>scout-delta</td>
                <td><span class="status-badge idle">&#9679; Idle</span></td>
                <td>Awaiting dispatch</td>
                <td>—</td>
                <td>0h 08m</td>
              </tr>
              <tr>
                <td>guardian-epsilon</td>
                <td><span class="status-badge online">&#9679; Online</span></td>
                <td>Monitor loop</td>
                <td>—</td>
                <td>24h 01m</td>
              </tr>
              <tr>
                <td>weaver-gamma</td>
                <td><span class="status-badge error">&#9679; Error</span></td>
                <td>Prompt assembly</td>
                <td>—</td>
                <td>0h 03m</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!-- Activity Feed (collapsible) -->
      <div class="section-card">
        <div class="section-header" onclick="toggleCollapse(this)" role="button" tabindex="0" onkeydown="if(event.key==='Enter')toggleCollapse(this)">
          <h2>Activity Feed</h2>
          <span class="toggle-icon">&#9660;</span>
        </div>
        <div class="section-body">
          <div class="activity-feed">
            <div class="activity-item">
              <span class="activity-dot success"></span>
              <div class="activity-text">
                <div class="msg">refinery-alpha completed blueprint refinement — score 91.7</div>
                <div class="time">2 min ago</div>
              </div>
            </div>
            <div class="activity-item">
              <span class="activity-dot info"></span>
              <div class="activity-text">
                <div class="msg">production-beta dispatched on batch eval v2.3 (12 blueprints)</div>
                <div class="time">7 min ago</div>
              </div>
            </div>
            <div class="activity-item">
              <span class="activity-dot warn"></span>
              <div class="activity-text">
                <div class="msg">weaver-gamma error: prompt template mismatch in slot #4</div>
                <div class="time">11 min ago</div>
              </div>
            </div>
            <div class="activity-item">
              <span class="activity-dot success"></span>
              <div class="activity-text">
                <div class="msg">Batch training loop completed — 46 blueprints processed</div>
                <div class="time">23 min ago</div>
              </div>
            </div>
            <div class="activity-item">
              <span class="activity-dot info"></span>
              <div class="activity-text">
                <div class="msg">scout-delta: 3 new blueprint candidates detected in staging</div>
                <div class="time">35 min ago</div>
              </div>
            </div>
            <div class="activity-item">
              <span class="activity-dot info"></span>
              <div class="activity-text">
                <div class="msg">Dashboard refreshed — 7 active pipelines, GPU at 68%</div>
                <div class="time">1h 02m ago</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- right sidebar -->
    <div>
      <!-- GPU Monitor (collapsible) -->
      <div class="section-card" style="margin-bottom:1.5rem">
        <div class="section-header" onclick="toggleCollapse(this)" role="button" tabindex="0" onkeydown="if(event.key==='Enter')toggleCollapse(this)">
          <h2>GPU Monitor</h2>
          <span class="toggle-icon">&#9660;</span>
        </div>
        <div class="section-body">
          <div class="gpu-list">
            <div class="gpu-item">
              <div class="gpu-name">NVIDIA A100 <span class="gpu-id">#0</span></div>
              <div class="gpu-bar-wrap">
                <div class="gpu-bar"><div class="gpu-bar-fill med" style="width:72%"></div></div>
                <span class="gpu-pct">72%</span>
              </div>
            </div>
            <div class="gpu-item">
              <div class="gpu-name">NVIDIA A100 <span class="gpu-id">#1</span></div>
              <div class="gpu-bar-wrap">
                <div class="gpu-bar"><div class="gpu-bar-fill high" style="width:91%"></div></div>
                <span class="gpu-pct">91%</span>
              </div>
            </div>
            <div class="gpu-item">
              <div class="gpu-name">NVIDIA A100 <span class="gpu-id">#2</span></div>
              <div class="gpu-bar-wrap">
                <div class="gpu-bar"><div class="gpu-bar-fill low" style="width:34%"></div></div>
                <span class="gpu-pct">34%</span>
              </div>
            </div>
            <div class="gpu-item">
              <div class="gpu-name">NVIDIA A100 <span class="gpu-id">#3</span></div>
              <div class="gpu-bar-wrap">
                <div class="gpu-bar"><div class="gpu-bar-fill low" style="width:18%"></div></div>
                <span class="gpu-pct">18%</span>
              </div>
            </div>
            <div class="gpu-item">
              <div class="gpu-name">NVIDIA A100 <span class="gpu-id">#4</span></div>
              <div class="gpu-bar-wrap">
                <div class="gpu-bar"><div class="gpu-bar-fill med" style="width:55%"></div></div>
                <span class="gpu-pct">55%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- Quick Actions -->
      <div class="section-card">
        <div class="section-header" onclick="toggleCollapse(this)" role="button" tabindex="0" onkeydown="if(event.key==='Enter')toggleCollapse(this)">
          <h2>Quick Actions</h2>
          <span class="toggle-icon">&#9660;</span>
        </div>
        <div class="section-body" style="padding:0.75rem 1.25rem">
          <div style="display:flex;flex-direction:column;gap:8px">
            <button class="qa-btn" onclick="alert('Dispatch queued')" style="background:var(--accent);color:#fff;border:none;border-radius:var(--radius-sm);padding:10px;font-size:0.85rem;cursor:pointer;font-family:inherit;font-weight:500;transition:opacity 0.15s" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">Dispatch New Batch</button>
            <button class="qa-btn" onclick="alert('Cleanup initiated')" style="background:var(--surface2);color:var(--text);border:1px solid var(--border);border-radius:var(--radius-sm);padding:10px;font-size:0.85rem;cursor:pointer;font-family:inherit;font-weight:500;transition:all 0.15s" onmouseover="this.style.borderColor='var(--accent)'" onmouseout="this.style.borderColor='var(--border)'">Run Cleanup</button>
            <button class="qa-btn" onclick="alert('Report generated')" style="background:var(--surface2);color:var(--text);border:1px solid var(--border);border-radius:var(--radius-sm);padding:10px;font-size:0.85rem;cursor:pointer;font-family:inherit;font-weight:500;transition:all 0.15s" onmouseover="this.style.borderColor='var(--accent)'" onmouseout="this.style.borderColor='var(--border)'">Export Report</button>
            <button class="qa-btn" onclick="alert('Config panel opening')" style="background:var(--surface2);color:var(--text);border:1px solid var(--border);border-radius:var(--radius-sm);padding:10px;font-size:0.85rem;cursor:pointer;font-family:inherit;font-weight:500;transition:all 0.15s" onmouseover="this.style.borderColor='var(--accent)'" onmouseout="this.style.borderColor='var(--border)'">Configure Alerts</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</main>
<footer class="site-footer">
  <span>&copy; 2026 styde.se &mdash; Alpedal Labs</span>
  <div class="footer-links">
    <a href="#">Documentation</a>
    <a href="#">API</a>
    <a href="#">Status</a>
    <a href="#">Privacy</a>
    <a href="#">Contact</a>
  </div>
</footer>
<script>
(function(){
  // Live clock
  function updateClock(){
    var d=new Date();
    var h=String(d.getHours()).padStart(2,'0');
    var m=String(d.getMinutes()).padStart(2,'0');
    var s=String(d.getSeconds()).padStart(2,'0');
    var el=document.getElementById('headerTime');
    if(el) el.textContent=h+':'+m+':'+s;
  }
  updateClock();
  setInterval(updateClock,1000);
  // Collapse toggle
  window.toggleCollapse = function(header){
    var body=header.nextElementSibling;
    if(!body)return;
    header.classList.toggle('collapsed');
    body.classList.toggle('hidden');
  };
  // Hamburger menu (mobile)
  var hamburger=document.getElementById('hamburgerBtn');
  var navDesktop=document.getElementById('navDesktop');
  if(hamburger && navDesktop){
    hamburger.addEventListener('click',function(e){
      e.stopPropagation();
      navDesktop.classList.toggle('open');
    });
    document.addEventListener('click',function(e){
      if(!navDesktop.contains(e.target) && e.target!==hamburger){
        navDesktop.classList.remove('open');
      }
    });
  }
  // Nav button active state
  var navBtns=document.querySelectorAll('.nav-desktop button');
  for(var i=0;i<navBtns.length;i++){
    (function(btn){
      btn.addEventListener('click',function(){
        for(var j=0;j<navBtns.length;j++) navBtns[j].classList.remove('active');
        this.classList.add('active');
        if(window.innerWidth<=640){
          navDesktop.classList.remove('open');
        }
      });
    })(navBtns[i]);
  }
  // Simulated GPU and agent updates
  setInterval(function(){
    var fills=document.querySelectorAll('.gpu-bar-fill');
    for(var i=0;i<fills.length;i++){
      var pct=Math.floor(Math.random()*40)+60;
      if(pct>95)pct=95;
      fills[i].style.width=pct+'%';
      var parent=fills[i].parentElement;
      if(parent){
        var next=parent.nextElementSibling;
        if(next) next.textContent=pct+'%';
      }
      fills[i].className='gpu-bar-fill '+(pct<50?'low':pct<80?'med':'high');
    }
  },5000);
  // Simulated agent status flip
  setInterval(function(){
    var errRow=document.querySelector('.agent-table tbody tr:nth-child(6) .status-badge');
    if(errRow){
      var states=['online','processing','idle'];
      var r=states[Math.floor(Math.random()*states.length)];
      errRow.className='status-badge '+r;
      if(r==='online') errRow.innerHTML='&#9679; Online';
      else if(r==='processing') errRow.innerHTML='&#9679; Processing';
      else errRow.innerHTML='&#9679; Idle';
    }
  },8000);
})();
</script>
</body>
</html>
```