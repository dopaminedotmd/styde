<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--surface2:#222636;--border:#2d3148;
  --text:#c9d1d9;--text2:#8b949e;--accent:#58a6ff;--accent2:#3fb950;
  --warn:#d29922;--danger:#f85149;--panel-gap:12px;--radius:8px;
  --transition:0.3s cubic-bezier(0.4,0,0.2,1);
}
body{background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,sans-serif;min-height:100vh;padding:16px}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px}
.header h1{font-size:1.4rem;font-weight:600;color:var(--text)}
.controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.btn{background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.82rem;transition:var(--transition);white-space:nowrap}
.btn:hover{background:var(--border);border-color:var(--accent)}
.btn.active{background:var(--accent);color:#000;border-color:var(--accent)}
.badge{background:var(--surface2);border:1px solid var(--border);padding:4px 10px;border-radius:12px;font-size:0.75rem;color:var(--text2)}
.dashboard{
  display:grid;grid-template-columns:repeat(4,1fr);
  grid-auto-rows:minmax(140px,auto);gap:var(--panel-gap);
  transition:var(--transition);
}
.panel{
  background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:14px;display:flex;flex-direction:column;gap:8px;
  transition:all var(--transition);position:relative;overflow:hidden;
  min-height:140px;
}
.panel.large{grid-column:span 2;grid-row:span 2}
.panel.medium{grid-column:span 1;grid-row:span 1}
.panel.small{grid-column:span 1;grid-row:span 1;min-height:100px;padding:10px}
.panel.compact{grid-column:span 1;grid-row:span 1;min-height:52px;padding:8px 12px;flex-direction:row;align-items:center;gap:8px}
.panel.compact .panel-body,.panel.compact .panel-footer{display:none}
.panel.compact .panel-metric-preview{display:block;font-size:0.8rem;color:var(--text2)}
.panel.locked{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.panel.locked::after{content:'LOCKED';position:absolute;top:4px;right:36px;font-size:0.6rem;color:var(--accent);font-weight:700;letter-spacing:1px;opacity:0.7}
.panel-header{display:flex;justify-content:space-between;align-items:center;gap:6px}
.panel-title{font-weight:600;font-size:0.9rem;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-actions{display:flex;gap:4px;flex-shrink:0}
.panel-actions button{background:none;border:none;color:var(--text2);cursor:pointer;padding:2px 6px;border-radius:4px;font-size:0.75rem;transition:var(--transition);line-height:1}
.panel-actions button:hover{background:var(--surface2);color:var(--text)}
.panel-actions button.locked-btn{color:var(--accent)}
.panel-body{flex:1;display:flex;align-items:center;justify-content:center;min-height:60px}
.metric-value{font-size:2.2rem;font-weight:700;color:var(--accent2);line-height:1}
.metric-unit{font-size:0.8rem;color:var(--text2);margin-left:4px}
.metric-sub{font-size:0.75rem;color:var(--text2);margin-top:2px}
.sparkline{display:flex;align-items:flex-end;gap:2px;height:40px;width:100%}
.sparkline-bar{flex:1;background:var(--accent);border-radius:2px 2px 0 0;min-height:2px;transition:height 0.5s}
.sparkline-bar.warn{background:var(--warn)}
.sparkline-bar.danger{background:var(--danger)}
.heatmap-indicator{display:flex;gap:4px;align-items:center}
.heatmap-dot{width:8px;height:8px;border-radius:50%}
.heatmap-dot.cold{background:var(--border)}
.heatmap-dot.warm{background:var(--warn)}
.heatmap-dot.hot{background:var(--danger)}
.panel-footer{display:flex;justify-content:space-between;align-items:center;font-size:0.7rem;color:var(--text2);margin-top:auto}
.panel-metric-preview{display:none}
.score-badge{font-size:0.65rem;padding:2px 6px;border-radius:8px;background:var(--surface2)}
.rank-indicator{position:absolute;top:8px;left:8px;font-size:0.6rem;color:var(--text2);opacity:0.5;font-weight:700}
.toast{position:fixed;bottom:20px;right:20px;background:var(--surface2);border:1px solid var(--border);padding:10px 16px;border-radius:var(--radius);font-size:0.8rem;z-index:100;animation:slideIn 0.3s ease,slideOut 0.3s ease 1.7s forwards;pointer-events:none}
@keyframes slideIn{from{transform:translateY(20px);opacity:0}to{transform:translateY(0);opacity:1}}
@keyframes slideOut{from{transform:translateY(0);opacity:1}to{transform:translateY(20px);opacity:0}}
@media(max-width:900px){.dashboard{grid-template-columns:repeat(2,1fr)}.panel.large{grid-column:span 2}}
@media(max-width:500px){.dashboard{grid-template-columns:1fr}.panel.large{grid-column:span 1}}
</style>
</head>
<body>
<div class="header">
  <h1>Adaptive Metric Layout</h1>
  <div class="controls">
    <span class="badge" id="session-time">Session: 0s</span>
    <button class="btn" id="btn-reset" title="Reset all tracking data">Reset Tracking</button>
    <button class="btn" id="btn-force-layout" title="Force immediate relayout">Apply Layout</button>
    <button class="btn" id="btn-auto" title="Toggle auto-layout" class="active">Auto: ON</button>
  </div>
</div>
<div class="dashboard" id="dashboard">
  <div class="panel" data-panel-id="cpu">
    <div class="panel-header">
      <span class="panel-title">CPU Usage</span>
      <div class="panel-actions">
        <button class="lock-btn" data-action="lock" title="Lock position">&#128274;</button>
        <button data-action="collapse" title="Collapse/Expand">&#9660;</button>
      </div>
    </div>
    <div class="panel-body">
      <div>
        <div class="metric-value">47<span class="metric-unit">%</span></div>
        <div class="metric-sub">4 cores active</div>
        <div class="sparkline" id="spark-cpu"></div>
      </div>
    </div>
    <div class="panel-footer"><span>View: 0s</span><span>Score: 0</span></div>
    <div class="panel-metric-preview">CPU: 47%</div>
  </div>
  <div class="panel" data-panel-id="memory">
    <div class="panel-header">
      <span class="panel-title">Memory</span>
      <div class="panel-actions">
        <button class="lock-btn" data-action="lock" title="Lock position">&#128274;</button>
        <button data-action="collapse" title="Collapse/Expand">&#9660;</button>
      </div>
    </div>
    <div class="panel-body">
      <div>
        <div class="metric-value">8.2<span class="metric-unit">GB</span></div>
        <div class="metric-sub">of 16 GB (51%)</div>
        <div class="sparkline" id="spark-memory"></div>
      </div>
    </div>
    <div class="panel-footer"><span>View: 0s</span><span>Score: 0</span></div>
    <div class="panel-metric-preview">Mem: 8.2/16GB</div>
  </div>
  <div class="panel" data-panel-id="network">
    <div class="panel-header">
      <span class="panel-title">Network I/O</span>
      <div class="panel-actions">
        <button class="lock-btn" data-action="lock" title="Lock position">&#128274;</button>
        <button data-action="collapse" title="Collapse/Expand">&#9660;</button>
      </div>
    </div>
    <div class="panel-body">
      <div>
        <div class="metric-value">3.1<span class="metric-unit">MB/s</span></div>
        <div class="metric-sub">TX: 1.2 | RX: 1.9 MB/s</div>
        <div class="sparkline" id="spark-network"></div>
      </div>
    </div>
    <div class="panel-footer"><span>View: 0s</span><span>Score: 0</span></div>
    <div class="panel-metric-preview">Net: 3.1MB/s</div>
  </div>
  <div class="panel" data-panel-id="disk">
    <div class="panel-header">
      <span class="panel-title">Disk I/O</span>
      <div class="panel-actions">
        <button class="lock-btn" data-action="lock" title="Lock position">&#128274;</button>
        <button data-action="collapse" title="Collapse/Expand">&#9660;</button>
      </div>
    </div>
    <div class="panel-body">
      <div>
        <div class="metric-value">128<span class="metric-unit">IOPS</span></div>
        <div class="metric-sub">Read: 89 | Write: 39</div>
        <div class="sparkline" id="spark-disk"></div>
      </div>
    </div>
    <div class="panel-footer"><span>View: 0s</span><span>Score: 0</span></div>
    <div class="panel-metric-preview">Disk: 128 IOPS</div>
  </div>
  <div class="panel" data-panel-id="requests">
    <div class="panel-header">
      <span class="panel-title">Requests/sec</span>
      <div class="panel-actions">
        <button class="lock-btn" data-action="lock" title="Lock position">&#128274;</button>
        <button data-action="collapse" title="Collapse/Expand">&#9660;</button>
      </div>
    </div>
    <div class="panel-body">
      <div>
        <div class="metric-value">2.4<span class="metric-unit">k</span></div>
        <div class="metric-sub">Avg latency: 42ms</div>
        <div class="sparkline" id="spark-requests"></div>
      </div>
    </div>
    <div class="panel-footer"><span>View: 0s</span><span>Score: 0</span></div>
    <div class="panel-metric-preview">Req: 2.4k/s</div>
  </div>
  <div class="panel" data-panel-id="errors">
    <div class="panel-header">
      <span class="panel-title">Error Rate</span>
      <div class="panel-actions">
        <button class="lock-btn" data-action="lock" title="Lock position">&#128274;</button>
        <button data-action="collapse" title="Collapse/Expand">&#9660;</button>
      </div>
    </div>
    <div class="panel-body">
      <div>
        <div class="metric-value" style="color:var(--danger)">0.12<span class="metric-unit">%</span></div>
        <div class="metric-sub">12 errors this hour</div>
        <div class="sparkline" id="spark-errors"></div>
      </div>
    </div>
    <div class="panel-footer"><span>View: 0s</span><span>Score: 0</span></div>
    <div class="panel-metric-preview">Err: 0.12%</div>
  </div>
  <div class="panel" data-panel-id="users">
    <div class="panel-header">
      <span class="panel-title">Active Users</span>
      <div class="panel-actions">
        <button class="lock-btn" data-action="lock" title="Lock position">&#128274;</button>
        <button data-action="collapse" title="Collapse/Expand">&#9660;</button>
      </div>
    </div>
    <div class="panel-body">
      <div>
        <div class="metric-value">847</div>
        <div class="metric-sub">+12 this minute</div>
        <div class="sparkline" id="spark-users"></div>
      </div>
    </div>
    <div class="panel-footer"><span>View: 0s</span><span>Score: 0</span></div>
    <div class="panel-metric-preview">Users: 847</div>
  </div>
  <div class="panel" data-panel-id="cache">
    <div class="panel-header">
      <span class="panel-title">Cache Hit Ratio</span>
      <div class="panel-actions">
        <button class="lock-btn" data-action="lock" title="Lock position">&#128274;</button>
        <button data-action="collapse" title="Collapse/Expand">&#9660;</button>
      </div>
    </div>
    <div class="panel-body">
      <div>
        <div class="metric-value">94.7<span class="metric-unit">%</span></div>
        <div class="metric-sub">Hit: 18.9k | Miss: 1.1k</div>
        <div class="sparkline" id="spark-cache"></div>
      </div>
    </div>
    <div class="panel-footer"><span>View: 0s</span><span>Score: 0</span></div>
    <div class="panel-metric-preview">Cache: 94.7%</div>
  </div>
</div>
<script>
(function(){
'use strict';
const LS_KEY = 'adaptive_metric_layout_v1';
const COMPACT_THRESHOLD = 0.15;
const LARGE_THRESHOLD = 0.7;
const RECENCY_HALFLIFE_HOURS = 24;
const DURATION_WEIGHT = 0.3;
const INTERACTION_WEIGHT = 1.0;
const dashboard = document.getElementById('dashboard');
const sessionTimeEl = document.getElementById('session-time');
const btnReset = document.getElementById('btn-reset');
const btnForceLayout = document.getElementById('btn-force-layout');
const btnAuto = document.getElementById('btn-auto');
let autoLayoutEnabled = true;
let sessionStart = Date.now();
function toast(msg){
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 2000);
}
function generateSparkline(panelId){
  const container = document.getElementById('spark-' + panelId);
  if(!container) return;
  container.innerHTML = '';
  const bars = 12;
  for(let i = 0; i < bars; i++){
    const bar = document.createElement('div');
    bar.className = 'sparkline-bar';
    const h = 15 + Math.random() * 70;
    bar.style.height = h + '%';
    if(h > 75) bar.classList.add('danger');
    else if(h > 55) bar.classList.add('warn');
    container.appendChild(bar);
  }
}
document.querySelectorAll('.panel').forEach(p => generateSparkline(p.dataset.panelId));
setInterval(() => {
  document.querySelectorAll('.panel').forEach(p => generateSparkline(p.dataset.panelId));
}, 5000);
class Dashboard {
  constructor(){
    this.panels = new Map();
    this.observer = null;
    this.visibilityTimers = new Map();
    this.initialized = false;
  }
  init(){
    if(this.initialized) return;
    this.initialized = true;
    const saved = this.restore();
    const panelEls = document.querySelectorAll('.panel[data-panel-id]');
    panelEls.forEach(el => {
      const id = el.dataset.panelId;
      const savedData = saved[id] || {};
      const data = {
        id,
        el,
        viewDuration: savedData.viewDuration || 0,
        interactions: savedData.interactions || 0,
        lastInteraction: savedData.lastInteraction || Date.now(),
        locked: savedData.locked || false,
        collapsed: savedData.collapsed || false,
        manualOrder: savedData.manualOrder || null,
        visible: false,
        visibleSince: null
      };
      this.panels.set(id, data);
      if(data.locked){
        el.classList.add('locked');
        const lockBtn = el.querySelector('.lock-btn');
        if(lockBtn) lockBtn.classList.add('locked-btn');
      }
      if(data.collapsed){
        el.classList.add('compact');
      }
      el.addEventListener('click', (e) => {
        if(e.target.closest('button')) return;
        this.trackInteraction(id);
      });
      el.addEventListener('mouseenter', () => {
        this.trackInteraction(id);
      });
      const lockBtn = el.querySelector('[data-action="lock"]');
      if(lockBtn){
        lockBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          this.toggleLock(id);
        });
      }
      const collapseBtn = el.querySelector('[data-action="collapse"]');
      if(collapseBtn){
        collapseBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          this.toggleCollapse(id);
        });
      }
    });
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const id = entry.target.dataset.panelId;
        const data = this.panels.get(id);
        if(!data) return;
        const now = Date.now();
        if(entry.isIntersecting && !data.visible){
          data.visible = true;
          data.visibleSince = now;
        } else if(!entry.isIntersecting && data.visible){
          data.visible = false;
          if(data.visibleSince){
            data.viewDuration += (now - data.visibleSince) / 1000;
            data.visibleSince = null;
          }
          this.persist();
        }
      });
    }, { threshold: 0.5 });
    panelEls.forEach(el => this.observer.observe(el));
    this.applyLayout();
    this.updateAllFooters();
    this.persist();
    setInterval(() => this.updateSessionTime(), 1000);
    setInterval(() => this.applyLayout(), 30000);
    window.addEventListener('beforeunload', () => {
      this.panels.forEach(data => {
        if(data.visible && data.visibleSince){
          data.viewDuration += (Date.now() - data.visibleSince) / 1000;
          data.visibleSince = null;
        }
      });
      this.persist();
    });
    console.assert(this.observer !== null, 'Dashboard.init: IntersectionObserver initialized');
    console.assert(this.panels.size > 0, 'Dashboard.init: panels tracked');
    console.assert(this.initialized === true, 'Dashboard.init: bootstrap complete');
    console.log('Dashboard.init: adaptive layout engine active, tracking', this.panels.size, 'panels');
  }
  trackInteraction(panelId){
    const data = this.panels.get(panelId);
    if(!data) return;
    data.interactions++;
    data.lastInteraction = Date.now();
    this.updateFooter(panelId);
    this.persist();
    this.applyLayout();
  }
  toggleLock(panelId){
    const data = this.panels.get(panelId);
    if(!data) return;
    data.locked = !data.locked;
    const el = data.el;
    const lockBtn = el.querySelector('.lock-btn');
    if(data.locked){
      el.classList.add('locked');
      if(lockBtn) lockBtn.classList.add('locked-btn');
      toast(panelId + ': position locked');
    } else {
      el.classList.remove('locked');
      if(lockBtn) lockBtn.classList.remove('locked-btn');
      toast(panelId + ': auto-layout restored');
    }
    this.persist();
    this.applyLayout();
  }
  toggleCollapse(panelId){
    const data = this.panels.get(panelId);
    if(!data) return;
    data.collapsed = !data.collapsed;
    if(data.collapsed){
      data.el.classList.add('compact');
    } else {
      data.el.classList.remove('compact');
    }
    this.persist();
    this.applyLayout();
  }
  computeScore(data){
    const now = Date.now();
    const hoursSince = (now - data.lastInteraction) / (1000 * 60 * 60);
    const recency = Math.pow(0.5, hoursSince / RECENCY_HALFLIFE_HOURS);
    const score = (data.interactions * INTERACTION_WEIGHT + data.viewDuration * DURATION_WEIGHT) * recency;
    return Math.max(score, 0.001);
  }
  rankPanels(){
    const scored = [];
    this.panels.forEach(data => {
      scored.push({ id: data.id, score: this.computeScore(data), locked: data.locked, data });
    });
    scored.sort((a, b) => b.score - a.score);
    return scored;
  }
  applyLayout(){
    if(!autoLayoutEnabled) return;
    const ranked = this.rankPanels();
    const maxScore = ranked.length > 0 ? Math.max(...ranked.map(r => r.score)) : 1;
    const container = document.getElementById('dashboard');
    const children = Array.from(container.children);
    const sizeClasses = ['large', 'medium', 'small', 'compact'];
    ranked.forEach((item, index) => {
      const el = item.data.el;
      if(!el) return;
      sizeClasses.forEach(c => el.classList.remove(c));
      if(item.data.collapsed){
        el.classList.add('compact');
      } else if(item.locked){
        el.classList.add('medium');
      } else {
        const ratio = maxScore > 0 ? item.score / maxScore : 0;
        if(ratio >= LARGE_THRESHOLD) el.classList.add('large');
        else if(ratio >= COMPACT_THRESHOLD) el.classList.add('medium');
        else if(ratio >= COMPACT_THRESHOLD * 0.5) el.classList.add('small');
        else el.classList.add('compact');
      }
      el.style.order = item.locked ? (item.data.manualOrder !== null ? item.data.manualOrder : index) : index;
    });
    this.updateAllFooters();
  }
  updateFooter(panelId){
    const data = this.panels.get(panelId);
    if(!data) return;
    const score = this.computeScore(data);
    const el = data.el;
    const footer = el.querySelector('.panel-footer');
    if(footer){
      const viewPart = footer.querySelector('span:first-child');
      const scorePart = footer.querySelector('span:last-child');
      if(viewPart) viewPart.textContent = 'View: ' + Math.round(data.viewDuration) + 's';
      if(scorePart) scorePart.textContent = 'Score: ' + score.toFixed(1);
    }
    const preview = el.querySelector('.panel-metric-preview');
    if(preview && data.collapsed){
      preview.style.display = 'block';
    }
  }
  updateAllFooters(){
    this.panels.forEach((data, id) => this.updateFooter(id));
  }
  persist(){
    const state = {};
    this.panels.forEach((data, id) => {
      state[id] = {
        viewDuration: data.viewDuration,
        interactions: data.interactions,
        lastInteraction: data.lastInteraction,
        locked: data.locked,
        collapsed: data.collapsed,
        manualOrder: data.manualOrder
      };
    });
    try {
      localStorage.setItem(LS_KEY, JSON.stringify(state));
    } catch(e){}
  }
  restore(){
    try {
      const raw = localStorage.getItem(LS_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch(e){ return {}; }
  }
  reset(){
    this.panels.forEach(data => {
      data.viewDuration = 0;
      data.interactions = 0;
      data.lastInteraction = Date.now();
      data.locked = false;
      data.collapsed = false;
      data.manualOrder = null;
      data.el.classList.remove('locked', 'compact', 'large', 'medium', 'small');
      const lockBtn = data.el.querySelector('.lock-btn');
      if(lockBtn) lockBtn.classList.remove('locked-btn');
    });
    this.persist();
    this.applyLayout();
    toast('Tracking data reset');
  }
  updateSessionTime(){
    const elapsed = Math.floor((Date.now() - sessionStart) / 1000);
    const m = Math.floor(elapsed / 60);
    const s = elapsed % 60;
    sessionTimeEl.textContent = 'Session: ' + m + 'm ' + s + 's';
  }
}
const app = new Dashboard();
app.init();
btnReset.addEventListener('click', () => app.reset());
btnForceLayout.addEventListener('click', () => { app.applyLayout(); toast('Layout applied'); });
btnAuto.addEventListener('click', () => {
  autoLayoutEnabled = !autoLayoutEnabled;
  btnAuto.textContent = 'Auto: ' + (autoLayoutEnabled ? 'ON' : 'OFF');
  btnAuto.classList.toggle('active', autoLayoutEnabled);
  if(autoLayoutEnabled) app.applyLayout();
  toast('Auto-layout: ' + (autoLayoutEnabled ? 'enabled' : 'disabled'));
});
btnAuto.classList.add('active');
console.assert(typeof app.init === 'function', 'Dashboard.init exists');
console.assert(app.initialized === true, 'Dashboard.init() was called and completed');
console.assert(app.observer !== null, 'IntersectionObserver wired');
console.assert(app.panels.size === 8, 'All 8 panels tracked');
})();
</script>
</body>
</html>