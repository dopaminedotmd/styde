<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--surface2:#22263a;--border:#2a2e3f;
  --text:#e1e4ed;--text2:#8b90a5;--accent:#6366f1;--accent2:#818cf8;
  --rank1:#10b981;--rank2:#f59e0b;--rank3:#ef4444;--rank4:#6b7280;
  --compact-scale:0.45;--transition:0.35s cubic-bezier(0.4,0,0.2,1);
}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px}
header{display:flex;justify-content:space-between;align-items:center;padding:12px 20px;background:var(--surface);border-radius:12px;margin-bottom:16px;border:1px solid var(--border)}
header h1{font-size:1.25rem;font-weight:600;letter-spacing:-0.02em}
.controls{display:flex;gap:8px;align-items:center}
.btn{padding:6px 14px;border-radius:8px;border:1px solid var(--border);background:var(--surface2);color:var(--text);cursor:pointer;font-size:0.8rem;transition:all var(--transition);white-space:nowrap}
.btn:hover{background:var(--border)}
.btn.accent{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.accent:hover{background:var(--accent2)}
.btn.danger{background:transparent;border-color:#ef4444;color:#ef4444}
.btn.danger:hover{background:#ef444422}
.badge{padding:3px 8px;border-radius:6px;font-size:0.7rem;font-weight:600;background:var(--surface2);color:var(--text2)}
.badge.hot{background:#ef444422;color:#ef4444}
.badge.warm{background:#f59e0b22;color:#f59e0b}
.badge.cold{background:#6b728022;color:#6b7280}
.stats-bar{display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap}
.stat-card{flex:1;min-width:140px;background:var(--surface);border-radius:10px;padding:14px 16px;border:1px solid var(--border);transition:all var(--transition)}
.stat-card:hover{border-color:var(--accent)}
.stat-label{font-size:0.7rem;color:var(--text2);text-transform:uppercase;letter-spacing:0.05em;margin-bottom:4px}
.stat-value{font-size:1.5rem;font-weight:700;letter-spacing:-0.02em}
.dashboard{display:grid;grid-template-columns:repeat(6,1fr);grid-auto-rows:180px;gap:12px;transition:all var(--transition)}
.panel{background:var(--surface);border-radius:12px;border:1px solid var(--border);padding:16px;display:flex;flex-direction:column;position:relative;overflow:hidden;transition:all var(--transition);cursor:grab;min-height:0}
.panel:active{cursor:grabbing}
.panel.compact{grid-column:span 1;grid-row:span 1;padding:10px;font-size:0.75rem}
.panel.compact .panel-body{display:none}
.panel.compact .panel-preview{display:flex}
.panel.compact .panel-title{font-size:0.7rem}
.panel.large{grid-column:span 2;grid-row:span 2}
.panel.medium{grid-column:span 1;grid-row:span 1}
.panel.wide{grid-column:span 2;grid-row:span 1}
.panel.locked{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.panel.locked::after{content:'LOCKED';position:absolute;top:6px;right:6px;font-size:0.55rem;padding:2px 6px;border-radius:4px;background:var(--accent);color:#fff;letter-spacing:0.05em}
.panel-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;flex-shrink:0}
.panel-title{font-size:0.85rem;font-weight:600;letter-spacing:-0.01em}
.panel-rank{font-size:0.6rem;padding:2px 6px;border-radius:4px;font-weight:700}
.panel-rank.r1{background:var(--rank1);color:#000}
.panel-rank.r2{background:var(--rank2);color:#000}
.panel-rank.r3{background:var(--rank3);color:#fff}
.panel-rank.r4{background:var(--rank4);color:#fff}
.panel-actions{display:flex;gap:4px;flex-shrink:0}
.panel-actions button{width:22px;height:22px;border-radius:5px;border:1px solid transparent;background:transparent;color:var(--text2);cursor:pointer;font-size:0.65rem;display:flex;align-items:center;justify-content:center;transition:all 0.15s}
.panel-actions button:hover{background:var(--surface2);color:var(--text)}
.panel-actions button.pin-btn.locked{color:var(--accent);background:var(--accent)22;border-color:var(--accent)}
.panel-body{flex:1;display:flex;flex-direction:column;justify-content:center;min-height:0;overflow:hidden}
.panel-preview{display:none;font-size:0.65rem;color:var(--text2)}
.metric-big{font-size:2rem;font-weight:800;letter-spacing:-0.03em;line-height:1}
.metric-trend{font-size:0.75rem;margin-top:4px}
.metric-trend.up{color:var(--rank1)}
.metric-trend.down{color:var(--rank3)}
.metric-trend.flat{color:var(--text2)}
.chart-mini{flex:1;display:flex;align-items:flex-end;gap:3px;padding-top:8px}
.chart-bar{flex:1;border-radius:3px 3px 0 0;min-height:4px;transition:height 0.5s}
.sparkline{width:100%;height:40px;margin-top:8px}
.heatmap-dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin:1px}
.heat-row{display:flex;gap:2px;flex-wrap:wrap;margin-top:auto;padding-top:6px}
.activity-line{font-size:0.72rem;padding:4px 0;border-bottom:1px solid var(--border);color:var(--text2)}
.activity-line:last-child{border-bottom:none}
.activity-time{color:var(--accent2);font-size:0.6rem;margin-right:6px}
.status-dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:6px}
.status-dot.ok{background:var(--rank1)}
.status-dot.warn{background:var(--rank2)}
.status-dot.err{background:var(--rank3)}
.toast{position:fixed;bottom:20px;right:20px;background:var(--surface);border:1px solid var(--border);padding:10px 18px;border-radius:10px;font-size:0.8rem;z-index:100;opacity:0;transform:translateY(10px);transition:all 0.3s;pointer-events:none}
.toast.show{opacity:1;transform:translateY(0)}
.attention-heatmap{position:absolute;inset:0;border-radius:12px;pointer-events:none;opacity:0;transition:opacity 0.5s}
.attention-indicator{position:absolute;top:0;left:0;height:3px;border-radius:0;transition:width 0.3s;background:var(--accent)}
@media(max-width:900px){.dashboard{grid-template-columns:repeat(3,1fr)}}
@media(max-width:500px){.dashboard{grid-template-columns:repeat(2,1fr)}}
</style>
</head>
<body>
<header>
  <h1>Adaptive Dashboard</h1>
  <div class="controls">
    <span id="global-score" class="badge">Score: --</span>
    <button class="btn accent" onclick="Dashboard.autoArrange()" title="Auto-arrange by attention rank">Auto-Arrange</button>
    <button class="btn" onclick="Dashboard.resetTracking()" title="Reset all tracking data">Reset Tracking</button>
    <button class="btn danger" onclick="Dashboard.nuke()" title="Clear all stored data">Nuke Data</button>
  </div>
</header>
<div class="stats-bar">
  <div class="stat-card">
    <div class="stat-label">Total Interactions</div>
    <div class="stat-value" id="stat-total">0</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Top Panel</div>
    <div class="stat-value" id="stat-top" style="font-size:1rem">--</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Locked Panels</div>
    <div class="stat-value" id="stat-locked">0</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Compact Panels</div>
    <div class="stat-value" id="stat-compact">0</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Session Duration</div>
    <div class="stat-value" id="stat-duration">0s</div>
  </div>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="toast" id="toast"></div>
<script>
const Dashboard = {
  panels:[
    {id:'revenue',title:'Revenue',type:'metric',value:48200,trend:+12.5,unit:'$',decimals:0,color:'#10b981'},
    {id:'users',title:'Active Users',type:'metric',value:1847,trend:+8.3,unit:'',decimals:0,color:'#6366f1'},
    {id:'conversion',title:'Conversion Rate',type:'metric',value:3.82,trend:-0.4,unit:'%',decimals:2,color:'#f59e0b'},
    {id:'server',title:'Server Status',type:'status',status:'ok',uptime:'99.97%',latency:'24ms'},
    {id:'activity',title:'Recent Activity',type:'feed',entries:[
      {time:'2m ago',msg:'Deploy v2.4.1 to production'},
      {time:'15m ago',msg:'New user signup: enterprise plan'},
      {time:'42m ago',msg:'API rate limit warning resolved'},
      {time:'1h ago',msg:'Database backup completed'},
      {time:'2h ago',msg:'SSL certificate renewed'}
    ]},
    {id:'health',title:'System Health',type:'health',cpu:34,mem:62,disk:48,reqs:1240},
    {id:'retention',title:'User Retention',type:'chart',data:[82,78,85,80,88,83,90,87,92,89,94,91],labels:'weekly'},
    {id:'errors',title:'Error Rate',type:'metric',value:0.12,trend:-0.03,unit:'%',decimals:2,color:'#ef4444'},
    {id:'latency',title:'P95 Latency',type:'metric',value:187,trend:-15,unit:'ms',decimals:0,color:'#8b5cf6'}
  ],
  init(){
    this.loadState();
    this.render();
    this.startSessionTimer();
    this.setupIntersectionObserver();
    this.renderStats();
    if(!this._autoArrangeTimer) this._autoArrangeTimer = setInterval(()=>this.autoArrange(),30000);
  },
  loadState(){
    try{
      const raw = localStorage.getItem('adaptive_dashboard_state');
      if(raw){
        const s = JSON.parse(raw);
        this.panels = s.panels || this.panels;
        this.locks = s.locks || {};
        this.tracking = s.tracking || this.initTracking();
      }else{
        this.locks = {};
        this.tracking = this.initTracking();
      }
    }catch(e){
      this.locks = {};
      this.tracking = this.initTracking();
    }
  },
  initTracking(){
    const t = {};
    this.panels.forEach(p=>{
      t[p.id] = {
        views:0,
        interactions:0,
        totalDuration:0,
        lastInteraction:0,
        score:0,
        history:[]
      };
    });
    return t;
  },
  saveState(){
    try{
      localStorage.setItem('adaptive_dashboard_state',JSON.stringify({
        panels:this.panels,
        locks:this.locks,
        tracking:this.tracking
      }));
    }catch(e){}
  },
  startSessionTimer(){
    this._startTime = Date.now();
    setInterval(()=>{
      const elapsed = Math.floor((Date.now()-this._startTime)/1000);
      document.getElementById('stat-duration').textContent = elapsed+'s';
    },1000);
  },
  setupIntersectionObserver(){
    this._viewTimers = {};
    this._observer = new IntersectionObserver((entries)=>{
      entries.forEach(e=>{
        const pid = e.target.dataset.panelId;
        if(e.isIntersecting){
          this._viewTimers[pid] = Date.now();
          this.track(pid,'view');
        }else if(this._viewTimers[pid]){
          const duration = Date.now()-this._viewTimers[pid];
          this.tracking[pid].totalDuration += duration;
          delete this._viewTimers[pid];
          this.recalcScores();
          this.saveState();
        }
      });
    },{threshold:0.3});
  },
  track(panelId,eventType){
    if(!this.tracking[panelId]) return;
    const t = this.tracking[panelId];
    t.interactions++;
    t.lastInteraction = Date.now();
    if(eventType==='view') t.views++;
    t.history.push({type:eventType,ts:Date.now()});
    if(t.history.length > 200) t.history = t.history.slice(-200);
    this.recalcScores();
    this.saveState();
    this.renderStats();
    const el = document.querySelector(`[data-panel-id="${panelId}"]`);
    if(el) this.updateAttentionIndicator(el,panelId);
  },
  recalcScores(){
    const now = Date.now();
    const HOUR = 3600000;
    const DAY = 86400000;
    Object.keys(this.tracking).forEach(pid=>{
      const t = this.tracking[pid];
      const freq = t.interactions || 0;
      const durSec = (t.totalDuration || 0)/1000;
      const recencyHours = Math.max(0.1,(now-(t.lastInteraction||now-DAY))/HOUR);
      const recencyFactor = Math.exp(-recencyHours/24);
      t.score = (freq*1.0 + durSec*0.5) * (0.3+0.7*recencyFactor);
      t.score = Math.round(t.score*100)/100;
    });
  },
  getRank(panelId){
    const sorted = Object.entries(this.tracking).sort((a,b)=>b[1].score-a[1].score);
    const idx = sorted.findIndex(([id])=>id===panelId);
    return idx+1;
  },
  getPanelSize(rank,totalPanels){
    const ratio = rank/totalPanels;
    if(ratio<=0.22) return 'large';
    if(ratio<=0.44) return 'wide';
    if(ratio<=0.75) return 'medium';
    return 'compact';
  },
  autoArrange(){
    this.recalcScores();
    const sorted = Object.entries(this.tracking)
      .filter(([id])=>!this.locks[id])
      .sort((a,b)=>b[1].score-a[1].score);
    const lockedPanels = Object.keys(this.locks).filter(id=>this.locks[id]);
    const totalUnlocked = sorted.length;
    sorted.forEach(([panelId,tdata],idx)=>{
      this.panels.find(p=>p.id===panelId)._rank = idx+1;
    });
    lockedPanels.forEach(id=>{
      const p = this.panels.find(p=>p.id===id);
      if(p) p._rank = p._rank || 999;
    });
    this.render();
    this.toast('Layout auto-arranged by attention rank');
    this.saveState();
  },
  toggleLock(panelId){
    this.locks[panelId] = !this.locks[panelId];
    if(!this.locks[panelId]) delete this.locks[panelId];
    this.track(panelId,'lock');
    this.render();
    this.renderStats();
    this.saveState();
    this.toast(this.locks[panelId]?'Panel locked':'Panel unlocked');
  },
  resetTracking(){
    this.tracking = this.initTracking();
    this.locks = {};
    this.render();
    this.renderStats();
    this.saveState();
    this.toast('Tracking data reset');
  },
  nuke(){
    localStorage.removeItem('adaptive_dashboard_state');
    this.locks = {};
    this.tracking = this.initTracking();
    this.render();
    this.renderStats();
    this.saveState();
    this.toast('All data nuked');
  },
  toast(msg){
    const el = document.getElementById('toast');
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(()=>el.classList.remove('show'),1800);
  },
  updateAttentionIndicator(el,panelId){
    const t = this.tracking[panelId];
    const maxScore = Math.max(...Object.values(this.tracking).map(t=>t.score),1);
    const pct = Math.min(100,(t.score/maxScore)*100);
    let ind = el.querySelector('.attention-indicator');
    if(!ind){
      ind = document.createElement('div');
      ind.className = 'attention-indicator';
      el.appendChild(ind);
    }
    ind.style.width = pct+'%';
    const colors = ['#6b7280','#f59e0b','#10b981','#6366f1'];
    const ci = Math.min(3,Math.floor(pct/25));
    ind.style.background = colors[ci];
  },
  getHeatmapClass(score,maxScore){
    const pct = score/maxScore;
    if(pct>0.7) return 'hot';
    if(pct>0.3) return 'warm';
    return 'cold';
  },
  renderStats(){
    const total = Object.values(this.tracking).reduce((s,t)=>s+t.interactions,0);
    const topPanel = Object.entries(this.tracking).sort((a,b)=>b[1].score-a[1].score)[0];
    document.getElementById('stat-total').textContent = total;
    document.getElementById('stat-top').textContent = topPanel?this.panels.find(p=>p.id===topPanel[0])?.title:'--';
    document.getElementById('stat-locked').textContent = Object.values(this.locks).filter(Boolean).length;
    document.getElementById('stat-compact').textContent = Object.entries(this.tracking)
      .filter(([id,t])=>this.getPanelSize(this.getRank(id),this.panels.length)==='compact').length;
  },
  render(){
    const container = document.getElementById('dashboard');
    const totalPanels = this.panels.length;
    this.recalcScores();
    const maxScore = Math.max(...Object.values(this.tracking).map(t=>t.score),1);
    let html = '';
    this.panels.forEach(panel=>{
      const tdata = this.tracking[panel.id] || {score:0,interactions:0,views:0,totalDuration:0};
      const rank = this.getRank(panel.id);
      const size = this.getPanelSize(rank,totalPanels);
      const locked = !!this.locks[panel.id];
      const heatClass = tdata.interactions>0?this.getHeatmapClass(tdata.score,maxScore):'';
      const rankClass = rank<=2?'r1':rank<=4?'r2':rank<=6?'r3':'r4';
      const pctScore = maxScore>0?Math.round((tdata.score/maxScore)*100):0;
      html += `<div class="panel ${size}${locked?' locked':''}" data-panel-id="${panel.id}" 
        onclick="Dashboard.track('${panel.id}','click')"
        onmouseenter="Dashboard.track('${panel.id}','hover')">
        <div class="panel-header">
          <div><span class="panel-title">${panel.title}</span> <span class="panel-rank ${rankClass}">#${rank}</span></div>
          <div class="panel-actions">
            <span class="badge ${heatClass}" title="Score: ${tdata.score}">${pctScore}%</span>
            <button class="pin-btn${locked?' locked':''}" onclick="event.stopPropagation();Dashboard.toggleLock('${panel.id}')" title="${locked?'Unlock':'Lock'} position">${locked?'&#128274;':'&#128275;'}</button>
          </div>
        </div>
        <div class="panel-body">${this.renderPanelBody(panel,size)}</div>
        <div class="panel-preview">${this.renderPreview(panel,tdata)}</div>
        <div class="attention-indicator" style="width:${pctScore}%"></div>
      </div>`;
    });
    container.innerHTML = html;
    container.querySelectorAll('[data-panel-id]').forEach(el=>{
      const pid = el.dataset.panelId;
      if(this._observer) this._observer.observe(el);
      this.updateAttentionIndicator(el,pid);
    });
  },
  renderPanelBody(panel,size){
    if(size==='compact') return '';
    switch(panel.type){
      case 'metric':
        const v = panel.value.toLocaleString(undefined,{minimumFractionDigits:panel.decimals,maximumFractionDigits:panel.decimals});
        const trendIcon = panel.trend>0?'&#9650;':panel.trend<0?'&#9660;':'&#9644;';
        const trendClass = panel.trend>0?'up':panel.trend<0?'down':'flat';
        return `<div class="metric-big">${panel.unit}${v}</div>
          <div class="metric-trend ${trendClass}">${trendIcon} ${Math.abs(panel.trend)}%</div>`;
      case 'status':
        const sc = panel.status==='ok'?'ok':panel.status==='warn'?'warn':'err';
        return `<div style="font-size:1.2rem;margin-bottom:6px"><span class="status-dot ${sc}"></span>${panel.status.toUpperCase()}</div>
          <div style="font-size:0.75rem;color:var(--text2)">Uptime: ${panel.uptime}</div>
          <div style="font-size:0.75rem;color:var(--text2)">Latency: ${panel.latency}</div>`;
      case 'feed':
        return panel.entries.slice(0,size==='large'?5:3).map(e=>
          `<div class="activity-line"><span class="activity-time">${e.time}</span>${e.msg}</div>`
        ).join('');
      case 'health':
        const bars = [
          {label:'CPU',val:panel.cpu,color:'#6366f1'},
          {label:'MEM',val:panel.mem,color:'#10b981'},
          {label:'DISK',val:panel.disk,color:'#f59e0b'}
        ];
        return bars.map(b=>`<div style="margin-bottom:6px">
          <div style="display:flex;justify-content:space-between;font-size:0.7rem;margin-bottom:2px"><span>${b.label}</span><span>${b.val}%</span></div>
          <div style="height:6px;background:var(--surface2);border-radius:3px;overflow:hidden">
            <div style="height:100%;width:${b.val}%;background:${b.color};border-radius:3px;transition:width 0.5s"></div>
          </div>
        </div>`).join('')+`<div style="font-size:0.7rem;color:var(--text2);margin-top:auto">${panel.reqs} req/min</div>`;
      case 'chart':
        const max = Math.max(...panel.data);
        const bars = panel.data.map((d,i)=>`<div class="chart-bar" style="height:${(d/max)*100}%;background:var(--accent);opacity:${0.4+(d/max)*0.6}" title="Week ${i+1}: ${d}%"></div>`).join('');
        return `<div style="font-size:0.7rem;color:var(--text2);margin-bottom:4px">${panel.labels} retention %</div>
          <div class="chart-mini">${bars}</div>`;
      default: return '';
    }
  },
  renderPreview(panel,tdata){
    const score = tdata.score||0;
    const views = tdata.views||0;
    const dur = Math.round((tdata.totalDuration||0)/1000);
    switch(panel.type){
      case 'metric': return `${panel.unit}${panel.value.toLocaleString()} ${panel.trend>0?'+':''}${panel.trend}% | Score:${score.toFixed(1)}`;
      case 'status': return `${panel.status.toUpperCase()} | Up:${panel.uptime}`;
      case 'feed': return `${panel.entries.length} events | Last: ${panel.entries[0]?.time}`;
      case 'health': return `CPU:${panel.cpu}% MEM:${panel.mem}% | ${panel.reqs} req/m`;
      case 'chart': return `Avg: ${Math.round(panel.data.reduce((a,b)=>a+b,0)/panel.data.length)}% | Views:${views}`;
      default: return `Views:${views} | ${dur}s viewed`;
    }
  }
};
document.addEventListener('DOMContentLoaded',()=>Dashboard.init());
let dragState = null;
document.addEventListener('dragstart',function(e){
  const panel = e.target.closest('.panel');
  if(!panel||Dashboard.locks[panel.dataset.panelId]){e.preventDefault();return;}
  dragState = {id:panel.dataset.panelId,el:panel};
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain',panel.dataset.panelId);
  setTimeout(()=>panel.style.opacity='0.4',0);
});
document.addEventListener('dragover',function(e){e.preventDefault();e.dataTransfer.dropEffect='move';});
document.addEventListener('drop',function(e){
  e.preventDefault();
  const target = e.target.closest('.panel');
  if(!target||!dragState||target.dataset.panelId===dragState.id) return;
  const fromIdx = Dashboard.panels.findIndex(p=>p.id===dragState.id);
  const toIdx = Dashboard.panels.findIndex(p=>p.id===target.dataset.panelId);
  if(fromIdx<0||toIdx<0) return;
  const [moved] = Dashboard.panels.splice(fromIdx,1);
  Dashboard.panels.splice(toIdx,0,moved);
  Dashboard.locks[dragState.id] = true;
  Dashboard.render();
  Dashboard.saveState();
  Dashboard.toast('Panel moved & locked');
  dragState = null;
});
document.addEventListener('dragend',function(){
  if(dragState?.el) dragState.el.style.opacity='1';
  dragState = null;
});
</script>
</body>
</html>