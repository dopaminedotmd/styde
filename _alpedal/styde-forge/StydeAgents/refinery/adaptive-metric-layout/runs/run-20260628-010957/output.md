I will output one complete HTML file directly to the terminal.
```html
<!DOCTYPE html>
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Adaptive Metric Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box}
body{font-family:system-ui,-apple-system,sans-serif;background:#0f1117;color:#e4e6ed;margin:0;padding:20px;min-height:100vh}
h1{font-size:1.4rem;font-weight:500;margin:0 0 8px 0;color:#c8cbd6}
h2{font-size:0.75rem;font-weight:500;margin:0 0 4px 0;color:#888b98;letter-spacing:0.5px;text-transform:uppercase}
.dashboard{max-width:1400px;margin:0 auto}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px}
.header-controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.phase-badge{font-size:0.7rem;padding:3px 10px;border-radius:4px;background:#1e2039;color:#818cf8;border:1px solid #2e3059}
.btn{font-size:0.75rem;padding:4px 12px;border-radius:4px;border:1px solid #2e3059;background:#1e2039;color:#b0b3c1;cursor:pointer}
.btn:hover{background:#2e3059}
.btn.active{background:#2e3a6f;border-color:#4a5a9f;color:#c8d0ff}
.btn.primary{background:#4f46e5;border-color:#6366f1;color:#fff}
.btn.primary:hover{background:#6366f1}
.reset-btn{font-size:0.7rem;padding:2px 8px;border-radius:3px;border:1px solid #3a2020;background:#2a1010;color:#f87171;cursor:pointer}
.reset-btn:hover{background:#3a2020}
.grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));transition:grid-template-columns 0.3s,grid-template-rows 0.3s;position:relative}
.panel{position:relative;background:#15171f;border-radius:8px;border:1px solid #24263a;overflow:hidden;transition:all 0.4s cubic-bezier(0.34,1.56,0.64,1);display:flex;flex-direction:column}
.panel.dragging{opacity:0.85;z-index:1000;box-shadow:0 8px 32px rgba(0,0,0,0.5);transform:scale(1.02)}
.panel.locked{border-color:#4f46e5}
.panel.compact{height:52px;overflow:hidden}
.panel.compact .panel-body{display:none}
.panel.compact .panel-header{cursor:pointer}
.panel.compact .panel-title{font-size:0.75rem}
.panel.mini{height:40px}
.panel.mini .panel-header{padding:6px 10px}
.panel.mini .panel-title{font-size:0.7rem;max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.panel-header{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;background:#191b26;user-select:none;border-bottom:1px solid #24263a;gap:6px;min-height:36px}
.panel-header-left{display:flex;align-items:center;gap:6px;min-width:0}
.panel-title{font-size:0.8rem;font-weight:500;color:#c8cbd6;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.panel-usage{font-size:0.6rem;padding:1px 5px;border-radius:3px;background:#1a1d30;color:#6b7fd4;white-space:nowrap}
.panel-usage.high{background:#1a2d1a;color:#6bd46b}
.panel-usage.medium{background:#2d2d1a;color:#d4c46b}
.panel-usage.low{background:#2d1a1a;color:#d46b6b}
.panel-controls{display:flex;gap:4px;align-items:center;flex-shrink:0}
.panel-btn{font-size:0.65rem;padding:1px 6px;border-radius:3px;border:none;background:transparent;color:#6b7089;cursor:pointer;line-height:1.4}
.panel-btn:hover{background:#2a2d42;color:#c8cbd6}
.panel-btn.locked{color:#4f46e5}
.panel-btn.drag-handle{cursor:grab;font-size:0.7rem}
.panel-btn.drag-handle:active{cursor:grabbing}
.panel-btn.minimize-btn{font-size:0.7rem}
.panel-body{padding:10px 12px;flex:1;display:flex;flex-direction:column;gap:8px;min-height:80px}
.metric-value{font-size:1.6rem;font-weight:600;color:#e4e6ed;line-height:1.1}
.metric-label{font-size:0.7rem;color:#6b7089}
.metric-bar{height:4px;border-radius:2px;background:#24263a;overflow:hidden;margin-top:4px}
.metric-bar-fill{height:100%;border-radius:2px;transition:width 0.6s ease}
.metric-row{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.sparkline{height:28px;width:100%;overflow:hidden;margin-top:4px}
.chart-bar{display:flex;align-items:flex-end;gap:2px;height:24px}
.chart-bar-item{flex:1;border-radius:1px;min-height:2px;transition:height 0.3s ease}
.panel-footer{font-size:0.6rem;padding:4px 12px;color:#4a4d5e;display:flex;justify-content:space-between;border-top:1px solid #1e2039}
.tag{display:inline-block;font-size:0.6rem;padding:1px 5px;border-radius:3px;background:#1e2039;color:#6b7fd4;margin-right:3px}
.drop-zone{position:absolute;inset:0;pointer-events:none;z-index:999;border-radius:8px;transition:all 0.2s}
.drop-zone.active{background:rgba(79,70,229,0.06);border:2px dashed #4f46e5;pointer-events:auto}
.rank-badge{font-size:0.6rem;padding:1px 5px;border-radius:3px;background:#1e2039;color:#6b7fd4}
.hidden{display:none!important}
.empty-state{padding:40px 20px;text-align:center;color:#4a4d5e;font-size:0.85rem}
.session-summary{display:flex;gap:16px;font-size:0.7rem;color:#6b7089;flex-wrap:wrap}
.session-summary span{white-space:nowrap}
.overlay{position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:10000;display:flex;align-items:center;justify-content:center}
.overlay-content{background:#1a1c29;border:1px solid #2e3059;border-radius:8px;padding:20px;min-width:300px;max-width:90vw}
.overlay-content h3{font-size:0.9rem;margin:0 0 12px 0;color:#c8cbd6}
.overlay-content label{display:block;font-size:0.75rem;color:#888b98;margin-bottom:4px}
.overlay-content select,.overlay-content input{width:100%;padding:6px 8px;border-radius:4px;border:1px solid #2e3059;background:#0f1117;color:#e4e6ed;font-size:0.8rem;margin-bottom:10px}
.overlay-actions{display:flex;gap:8px;justify-content:flex-end;margin-top:12px}
@media(max-width:600px){.grid{grid-template-columns:1fr!important}}@media(min-width:1200px){.grid{grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}}
</style>
<div class=dashboard>
<div class=header>
  <div>
    <h1>Adaptive Metric Dashboard</h1>
    <div class=session-summary>
      <span>sessions: <strong id=sessionCount>0</strong></span>
      <span>total views: <strong id=totalViews>0</strong></span>
      <span>layout age: <strong id=layoutAge>0m</strong></span>
      <span>mode: <span id=modeIndicator>learning</span></span>
    </div>
  </div>
  <div class=header-controls>
    <button class="btn primary" id=resetDataBtn>reset data</button>
    <button class=btn id=compactAllBtn>compact all</button>
    <button class=btn id=expandAllBtn>expand all</button>
    <span class=phase-badge id=phaseBadge>phase: learning</span>
  </div>
</div>
<div id=grid class=grid></div>
<div id=emptyState class="empty-state hidden">No panels configured. Add panels to begin tracking usage.</div>
</div>
<script>
(function(){
const STORAGE_KEY='adaptive_dashboard_v1';
const MIN_VIEW_MS=800;
const RECENCY_HALF_LIFE_HOURS=4;
const MAX_LAYOUT_ATTEMPTS=5;
const DEFAULT_PANELS=[
  {id:'cpu',title:'CPU Usage',type:'gauge',color:'#6366f1',range:[0,100],unit:'%'},
  {id:'memory',title:'Memory',type:'gauge',color:'#22c55e',range:[0,32],unit:'GB'},
  {id:'requests',title:'Requests/min',type:'sparkline',color:'#f59e0b',range:[0,2000],unit:'r/m'},
  {id:'latency',title:'Latency p99',type:'bar',color:'#ef4444',range:[0,500],unit:'ms'},
  {id:'errors',title:'Error Rate',type:'bar',color:'#ec4899',range:[0,5],unit:'%'},
  {id:'disk',title:'Disk I/O',type:'gauge',color:'#8b5cf6',range:[0,500],unit:'MB/s'},
  {id:'network',title:'Network In/Out',type:'double',color:'#14b8a6',unit:'Mbps'},
  {id:'containers',title:'Container Status',type:'status',color:'#06b6d4',max:20},
  {id:'cache',title:'Cache Hit Ratio',type:'gauge',color:'#84cc16',range:[0,100],unit:'%'},
  {id:'db',title:'DB Connections',type:'gauge',color:'#f97316',range:[0,200],unit:'conn'},
];
class AdaptiveDashboard{
  constructor(){
    this.state=this._loadState();
    this.panels=[];
    this.dragData=null;
    this.viewTimers=new Map();
    this.learningPhase=true;
    this.layoutInterval=null;
    this.phaseChangePending=false;
    this._init();
  }
  _init(){
    this._ensurePanels();
    this.panels=this._resolvePanelOrder();
    this._mergeOverrides();
    this._setupGrid();
    this._render();
    this._startViewTracking();
    this._startAdaptiveLoop();
    this._updateSummary();
    this._updatePhase();
  }
  _loadState(){
    try{
      const raw=localStorage.getItem(STORAGE_KEY);
      if(raw){
        const parsed=JSON.parse(raw);
        if(parsed&&typeof parsed==='object'&&parsed.version){
          return parsed;
        }
      }
    }catch(e){/* corrupt data, reset */}
    return this._freshState();
  }
  _freshState(){
    return{
      version:1,
      sessionCount:0,
      views:{},
      layout:[],
      locks:{},
      overrides:{},
      created:Date.now(),
      lastLayout:Date.now()
    };
  }
  _ensurePanels(){
    if(!this.state.layout||this.state.layout.length===0){
      this.state.layout=DEFAULT_PANELS.map(p=>({
        id:p.id,
        order:DEFAULT_PANELS.indexOf(p),
        compact:false,
        mini:false,
        locked:false
      }));
    }
    const existingIds=new Set(this.state.layout.map(l=>l.id));
    DEFAULT_PANELS.forEach(p=>{
      if(!existingIds.has(p.id)){
        this.state.layout.push({id:p.id,order:this.state.layout.length,compact:false,mini:false,locked:false});
      }
    });
    this.state.layout.forEach(l=>{if(l.locked===undefined)l.locked=false});
  }
  _resolvePanelOrder(){
    const panelMap=new Map();
    DEFAULT_PANELS.forEach(p=>panelMap.set(p.id,{...p}));
    const resolved=[];
    const ordered=this.state.layout.slice().sort((a,b)=>a.order-b.order);
    ordered.forEach(entry=>{
      const def=panelMap.get(entry.id);
      if(def){
        resolved.push({
          ...def,
          compact:entry.compact||false,
          mini:entry.mini||false,
          locked:entry.locked||false,
          overridePos:this.state.overrides[entry.id],
          order:entry.order
        });
        panelMap.delete(entry.id);
      }
    });
    panelMap.forEach(def=>{
      resolved.push({
        ...def,
        compact:false,mini:false,locked:false,
        overridePos:this.state.overrides[def.id],
        order:resolved.length
      });
      this.state.layout.push({id:def.id,order:resolved.length,compact:false,mini:false,locked:false});
    });
    return resolved;
  }
  _mergeOverrides(){
    this.panels.forEach(p=>{
      if(p.overridePos!==undefined){
        p.order=p.overridePos;
      }
    });
  }
  _setupGrid(){
    this.grid=document.getElementById('grid');
    this.emptyState=document.getElementById('emptyState');
  }
  _render(){
    this.grid.innerHTML='';
    if(this.panels.length===0){
      this.emptyState.classList.remove('hidden');
      return;
    }
    this.emptyState.classList.add('hidden');
    const sorted=this._getDisplayOrder();
    sorted.forEach((panel,i)=>{
      const el=this._createPanelElement(panel);
      el.dataset.panelId=panel.id;
      el.dataset.order=i;
      this.grid.appendChild(el);
    });
    this._applyLayout(sorted);
  }
  _getDisplayOrder(){
    const sorted=[...this.panels].sort((a,b)=>{
      if(a.locked!==b.locked)return a.locked?-1:1;
      return a.order-b.order;
    });
    const ranked=this._rankPanels(sorted);
    const locked=sorted.filter(p=>p.locked);
    const unlocked=sorted.filter(p=>!p.locked);
    const rankedUnlocked=[...unlocked].sort((a,b)=>{
      const sa=ranked.get(a.id)||0;
      const sb=ranked.get(b.id)||0;
      return sb-sa;
    });
    return[...locked,...rankedUnlocked];
  }
  _rankPanels(panels){
    const scores=new Map();
    const now=Date.now();
    panels.forEach(p=>{
      const v=this.state.views[p.id];
      if(!v||v.count===0){
        scores.set(p.id,0);
        return;
      }
      const frequency=v.count/(Math.max(1,(now-v.firstSeen)/60000));
      const duration=v.totalDuration/1000;
      const hoursSinceLast=(now-(v.lastSeen||v.firstSeen))/3600000;
      const recency=Math.exp(-hoursSinceLast/RECENCY_HALF_LIFE_HOURS);
      const score=frequency*duration*recency;
      scores.set(p.id,score);
    });
    return scores;
  }
  _createPanelElement(panel){
    const div=document.createElement('div');
    div.className='panel';
    if(panel.locked)div.classList.add('locked');
    if(panel.compact){
      div.classList.add('compact');
      if(panel.mini)div.classList.add('mini');
    }
    div.draggable=false;
    div.innerHTML=this._panelHTML(panel);
    this._attachPanelEvents(div,panel);
    this._renderPanelBody(div,panel);
    return div;
  }
  _panelHTML(panel){
    const v=this.state.views[panel.id]||{count:0,totalDuration:0};
    const usageClass=v.count>100?'high':v.count>20?'medium':'low';
    return `
      <div class=panel-header>
        <div class=panel-header-left>
          <span class="panel-btn drag-handle" data-action=drag>:::</span>
          <span class=panel-title>${panel.title}</span>
          <span class="panel-usage ${usageClass}">${v.count} views</span>
        </div>
        <div class=panel-controls>
          <span class=rank-badge>#${panel.order+1}</span>
          <button class="panel-btn minimize-btn" data-action=minimize title=toggle>_</button>
          <button class="panel-btn ${panel.locked?'locked':''}" data-action=lock title=lock>${panel.locked?'&#128274;':'&#128275;'}</button>
          <button class=panel-btn data-action=settings title=settings>&#9881;</button>
        </div>
      </div>
      <div class=panel-body></div>
      <div class=panel-footer>
        <span>${panel.type}</span>
        <span>views:${v.count} | ${Math.round(v.totalDuration/1000)}s</span>
      </div>`;
  }
  _renderPanelBody(el,panel){
    const body=el.querySelector('.panel-body');
    if(!body||panel.compact)return;
    const v=Math.random();
    switch(panel.type){
      case'gauge':this._renderGauge(body,panel);break;
      case'sparkline':this._renderSparkline(body,panel);break;
      case'bar':this._renderBar(body,panel);break;
      case'double':this._renderDouble(body,panel);break;
      case'status':this._renderStatus(body,panel);break;
      default:this._renderGauge(body,panel);
    }
  }
  _renderGauge(body,panel){
    const val=panel.range[0]+Math.random()*(panel.range[1]-panel.range[0]);
    const pct=(val-panel.range[0])/(panel.range[1]-panel.range[0])*100;
    body.innerHTML=`
      <div class=metric-row>
        <span class=metric-value>${val.toFixed(1)}</span>
        <span class=metric-label>${panel.unit||''}</span>
      </div>
      <div class=metric-label>${panel.title}</div>
      <div class=metric-bar><div class=metric-bar-fill style=width:${pct}%;background:${panel.color}></div></div>
      <div style=display:flex;justify-content:space-between;font-size:0.6rem;color:#4a4d5e>
        <span>${panel.range[0]}</span><span>${panel.range[1]}</span>
      </div>`;
  }
  _renderSparkline(body,panel){
    const vals=Array.from({length:20},()=>panel.range[0]+Math.random()*(panel.range[1]-panel.range[0]));
    const max=Math.max(...vals,1);
    body.innerHTML=`
      <div style=display:flex;justify-content:space-between;align-items:baseline>
        <span class=metric-value>${vals[vals.length-1].toFixed(0)}</span>
        <span class=metric-label>${panel.unit||''} (current)</span>
      </div>
      <div class=sparkline>
        <div class=chart-bar>
          ${vals.map(v=>`<div class=chart-bar-item style=height:${(v/max*100).toFixed(0)}%;background:${panel.color}></div>`).join('')}
        </div>
      </div>
      <div class=metric-label>last 20 samples &middot; avg ${(vals.reduce((a,b)=>a+b,0)/vals.length).toFixed(0)}</div>`;
  }
  _renderBar(body,panel){
    const val=panel.range[0]+Math.random()*(panel.range[1]-panel.range[0]);
    const pct=val/panel.range[1]*100;
    body.innerHTML=`
      <div class=metric-row>
        <span class=metric-value>${val.toFixed(1)}</span>
        <span class=metric-label>${panel.unit||''}</span>
      </div>
      <div class=metric-bar><div class=metric-bar-fill style=width:${Math.min(pct,100)}%;background:${panel.color}></div></div>
      <div class=metric-label>threshold: ${panel.range[1]}${panel.unit||''}</div>`;
  }
  _renderDouble(body,panel){
    const inVal=100+Math.random()*400;
    const outVal=50+Math.random()*200;
    body.innerHTML=`
      <div class=metric-row>
        <span class=metric-value>${inVal.toFixed(0)}</span>
        <span class=metric-label>in (${panel.unit||''})</span>
      </div>
      <div class=metric-bar><div class=metric-bar-fill style=width:${Math.min(inVal/8,100)}%;background:#22c55e></div></div>
      <div class=metric-row style=margin-top:4px>
        <span class=metric-value>${outVal.toFixed(0)}</span>
        <span class=metric-label>out (${panel.unit||''})</span>
      </div>
      <div class=metric-bar><div class=metric-bar-fill style=width:${Math.min(outVal/6,100)}%;background:#6366f1></div></div>`;
  }
  _renderStatus(body,panel){
    const running=Math.floor(Math.random()*panel.max);
    const stopped=panel.max-running;
    body.innerHTML=`
      <div class=metric-row>
        <span class=metric-value>${running}</span>
        <span class=metric-label>running</span>
        <span style=color:#ef4444>${stopped}</span>
        <span class=metric-label>stopped</span>
      </div>
      <div class=metric-bar>
        <div class=metric-bar-fill style=width:${(running/panel.max*100).toFixed(0)}%;background:#22c55e;display:inline-block>
        </div><div class=metric-bar-fill style=width:${(stopped/panel.max*100).toFixed(0)}%;background:#ef4444;display:inline-block>
        </div>
      </div>
      <div style=display:flex;gap:4px;flex-wrap:wrap;margin-top:4px>
        ${Array.from({length:panel.max},(_,i)=>`<span style=display:inline-block;width:8px;height:8px;border-radius:2px;background:${i<running?'#22c55e':'#ef4444'}></span>`).join('')}
      </div>`;
  }
  _attachPanelEvents(el,panel){
    const header=el.querySelector('.panel-header');
    const minimizeBtn=el.querySelector('[data-action=minimize]');
    const lockBtn=el.querySelector('[data-action=lock]');
    const settingsBtn=el.querySelector('[data-action=settings]');
    const dragHandle=el.querySelector('[data-action=drag]');
    minimizeBtn&&minimizeBtn.addEventListener('click',e=>{
      e.stopPropagation();
      this._toggleCompact(panel.id);
    });
    lockBtn&&lockBtn.addEventListener('click',e=>{
      e.stopPropagation();
      this._toggleLock(panel.id);
    });
    settingsBtn&&settingsBtn.addEventListener('click',e=>{
      e.stopPropagation();
      this._showSettingsOverlay(panel.id);
    });
    dragHandle&&dragHandle.addEventListener('mousedown',e=>{
      e.preventDefault();
      this._startDrag(e,panel.id,el);
    });
    dragHandle&&dragHandle.addEventListener('touchstart',e=>{
      e.preventDefault();
      const touch=e.touches[0];
      this._startDrag({clientX:touch.clientX,clientY:touch.clientY,target:e.target,preventDefault:()=>{}},panel.id,el);
    },{passive:false});
    el.addEventListener('mouseenter',()=>this._onViewStart(panel.id));
    el.addEventListener('mouseleave',()=>this._onViewEnd(panel.id));
  }
  _onViewStart(panelId){
    if(this.viewTimers.has(panelId)){
      clearTimeout(this.viewTimers.get(panelId).timer);
    }
    const entry={start:Date.now(),timer:null};
    this.viewTimers.set(panelId,entry);
  }
  _onViewEnd(panelId){
    const entry=this.viewTimers.get(panelId);
    if(!entry)return;
    const elapsed=Date.now()-entry.start;
    if(elapsed>=MIN_VIEW_MS){
      this._recordView(panelId,elapsed);
    }else{
      entry.timer=setTimeout(()=>{
        this._recordView(panelId,MIN_VIEW_MS);
      },MIN_VIEW_MS-elapsed);
    }
    this.viewTimers.delete(panelId);
  }
  _recordView(panelId,duration){
    if(!this.state.views[panelId]){
      this.state.views[panelId]={count:0,totalDuration:0,firstSeen:Date.now(),lastSeen:Date.now()};
    }
    const v=this.state.views[panelId];
    v.count++;
    v.totalDuration+=duration;
    v.lastSeen=Date.now();
    this._saveState();
    this._updatePhase();
    this._updateSummary();
    this._refreshUsageBadges();
  }
  _toggleCompact(panelId){
    const entry=this.state.layout.find(l=>l.id===panelId);
    if(!entry)return;
    if(!entry.compact){
      entry.compact=true;
      entry.mini=false;
    }else if(!entry.mini){
      entry.mini=true;
    }else{
      entry.compact=false;
      entry.mini=false;
    }
    this._saveState();
    this._reconcilePanels();
    this._render();
    this._updateSummary();
  }
  _toggleLock(panelId){
    const entry=this.state.layout.find(l=>l.id===panelId);
    if(!entry)return;
    entry.locked=!entry.locked;
    this._saveState();
    this._reconcilePanels();
    this._render();
  }
  _showSettingsOverlay(panelId){
    const panel=this.panels.find(p=>p.id===panelId);
    if(!panel)return;
    const overlay=document.createElement('div');
    overlay.className='overlay';
    overlay.innerHTML=`
      <div class=overlay-content>
        <h3>Panel Settings: ${panel.title}</h3>
        <label>Position</label>
        <input type=number id=posInput min=0 max=${this.panels.length-1} value=${panel.order}>
        <label>Display Mode</label>
        <select id=modeSelect>
          <option value=normal ${!panel.compact?'selected':''}>Normal</option>
          <option value=compact ${panel.compact&&!panel.mini?'selected':''}>Compact</option>
          <option value=mini ${panel.mini?'selected':''}>Mini</option>
        </select>
        <label>Lock Position</label>
        <select id=lockSelect>
          <option value=false ${!panel.locked?'selected':''}>Off</option>
          <option value=true ${panel.locked?'selected':''}>On</option>
        </select>
        <div class=overlay-actions>
          <button class=btn id=overlayCancel>Cancel</button>
          <button class="btn primary" id=overlayApply>Apply</button>
        </div>
      </div>`;
    document.body.appendChild(overlay);
    overlay.querySelector('#overlayCancel').onclick=()=>overlay.remove();
    overlay.querySelector('#overlayApply').onclick=()=>{
      const pos=parseInt(overlay.querySelector('#posInput').value);
      const mode=overlay.querySelector('#modeSelect').value;
      const lock=overlay.querySelector('#lockSelect').value==='true';
      const entry=this.state.layout.find(l=>l.id===panelId);
      if(entry){
        if(!isNaN(pos)&&pos>=0){
          entry.order=pos;
          this.state.overrides[panelId]=pos;
        }
        entry.compact=mode==='compact'||mode==='mini';
        entry.mini=mode==='mini';
        entry.locked=lock;
      }
      this._saveState();
      this._reconcilePanels();
      this._render();
      overlay.remove();
    };
  }
  _startDrag(e,panelId,el){
    this.dragData={panelId,el,startX:e.clientX,startY:e.clientY,startOrder:parseInt(el.dataset.order)};
    el.classList.add('dragging');
    const onMove=(ev)=>{
      if(!this.dragData)return;
      const dx=ev.clientX-this.dragData.startX;
      const dy=ev.clientY-this.dragData.startY;
      el.style.transform=`translate(${dx}px,${dy}px)`;
      this._updateDropZones(ev.clientX,ev.clientY,panelId);
    };
    const onUp=(ev)=>{
      if(!this.dragData)return;
      el.classList.remove('dragging');
      el.style.transform='';
      this._commitDrop(ev.clientX,ev.clientY,panelId);
      this._clearDropZones();
      document.removeEventListener('mousemove',onMove);
      document.removeEventListener('mouseup',onUp);
      document.removeEventListener('touchmove',onMove);
      document.removeEventListener('touchend',onUp);
      this.dragData=null;
    };
    document.addEventListener('mousemove',onMove);
    document.addEventListener('mouseup',onUp);
    document.addEventListener('touchmove',onMove,{passive:true});
    document.addEventListener('touchend',onUp);
  }
  _updateDropZones(cx,cy,sourceId){
    const items=this.grid.querySelectorAll('.panel');
    items.forEach(el=>{
      if(el.dataset.panelId===sourceId)return;
      const rect=el.getBoundingClientRect();
      const dz=el.querySelector('.drop-zone')||(()=>{
        const d=document.createElement('div');d.className='drop-zone';el.appendChild(d);return d;
      })();
      const inZone=cx>=rect.left&&cx<=rect.right&&cy>=rect.top&&cy<=rect.bottom;
      dz.classList.toggle('active',inZone);
    });
  }
  _clearDropZones(){
    this.grid.querySelectorAll('.drop-zone').forEach(d=>d.remove());
  }
  _commitDrop(cx,cy,sourceId){
    const items=this.grid.querySelectorAll('.panel');
    let targetId=null;
    items.forEach(el=>{
      if(el.dataset.panelId===sourceId)return;
      const rect=el.getBoundingClientRect();
      if(cx>=rect.left&&cx<=rect.right&&cy>=rect.top&&cy<=rect.bottom){
        targetId=el.dataset.panelId;
      }
    });
    if(targetId&&targetId!==sourceId){
      const sourceEntry=this.state.layout.find(l=>l.id===sourceId);
      const targetEntry=this.state.layout.find(l=>l.id===targetId);
      if(sourceEntry&&targetEntry){
        const temp=sourceEntry.order;
        sourceEntry.order=targetEntry.order;
        targetEntry.order=temp;
        this.state.overrides[sourceId]=sourceEntry.order;
        this.state.overrides[targetId]=targetEntry.order;
        this._saveState();
        this._reconcilePanels();
        this._render();
      }
    }
  }
  _startViewTracking(){
    const observer=new IntersectionObserver((entries)=>{
      entries.forEach(entry=>{
        const panelId=entry.target.closest('[data-panel-id]')?.dataset.panelId;
        if(!panelId)return;
        if(entry.isIntersecting){
          this._onViewStart(panelId);
        }else{
          this._onViewEnd(panelId);
        }
      });
    },{threshold:0.3});
    const startObserving=()=>{
      this.grid.querySelectorAll('.panel').forEach(el=>observer.observe(el));
    };
    startObserving();
    const renderObserver=new MutationObserver(startObserving);
    renderObserver.observe(this.grid,{childList:true});
  }
  _startAdaptiveLoop(){
    this._runAdaptiveLayout();
    this.layoutInterval=setInterval(()=>this._runAdaptiveLayout(),15000);
  }
  _runAdaptiveLayout(){
    if(this.learningPhase&&this._hasEnoughData()){
      this.learningPhase=false;
      this.phaseChangePending=true;
    }
    if(!this.learningPhase||this.phaseChangePending){
      const changed=this._reorderByRank();
      if(changed){
        this._saveState();
        this._render();
        this._updatePhase();
        this._updateSummary();
      }
    }
    this._autoCompact();
    this._refreshUsageBadges();
    this.state.lastLayout=Date.now();
    this._saveState();
  }
  _hasEnoughData(){
    const viewCounts=Object.values(this.state.views).map(v=>v.count);
    const total=viewCounts.reduce((a,b)=>a+b,0);
    return total>=20&&viewCounts.length>=3;
  }
  _reorderByRank(){
    const unlocked=this.panels.filter(p=>!p.locked);
    const lockedPanels=this.panels.filter(p=>p.locked);
    if(unlocked.length<2)return false;
    const ranked=this._rankPanels(unlocked);
    const sorted=[...unlocked].sort((a,b)=>(ranked.get(b.id)||0)-(ranked.get(a.id)||0));
    let changed=false;
    sorted.forEach((panel,idx)=>{
      const entry=this.state.layout.find(l=>l.id===panel.id);
      if(entry&&!entry.locked&&entry.order!==idx){
        const oldOrder=entry.order;
        entry.order=idx;
        const displaced=this.state.layout.find(l=>l.order===idx&&l.id!==panel.id);
        if(displaced&&!displaced.locked){
          displaced.order=oldOrder;
        }
        changed=true;
      }
    });
    return changed;
  }
  _autoCompact(){
    if(!this.learningPhase){
      const scores=this._rankPanels(this.panels.filter(p=>!p.locked&&!p.compact));
      const sorted=[...this.panels].filter(p=>!p.locked).sort((a,b)=>(scores.get(b.id)||0)-(scores.get(a.id)||0));
      const bottomHalf=sorted.slice(Math.floor(sorted.length/2));
      bottomHalf.forEach(p=>{
        const entry=this.state.layout.find(l=>l.id===p.id);
        if(entry&&!entry.locked&&!entry.compact&&(scores.get(p.id)||0)<1){
          entry.compact=true;
        }
      });
      const topHalf=sorted.slice(0,Math.floor(sorted.length/2));
      topHalf.forEach(p=>{
        const entry=this.state.layout.find(l=>l.id===p.id);
        if(entry&&entry.compact&&(scores.get(p.id)||0)>=5){
          entry.compact=false;
          entry.mini=false;
        }
      });
    }
  }
  _applyLayout(sorted){
    const containerWidth=this.grid.clientWidth||800;
    const cols=Math.min(sorted.length,containerWidth<600?1:containerWidth<900?2:3);
    this.grid.style.gridTemplateColumns=`repeat(${cols},1fr)`;
    sorted.forEach((panel,i)=>{
      const col=i%cols;
      const row=Math.floor(i/cols);
      const el=this.grid.querySelector(`[data-panel-id="${panel.id}"]`);
      if(!el)return;
      const rankFromTop=i;
      const isLarge=rankFromTop<2;
      const isTiny=rankFromTop>=sorted.length-1;
      if(isLarge&&!panel.locked){
        el.style.gridColumn=`span ${Math.min(cols,2)}`;
        el.style.gridRow='auto';
      }else if(isTiny&&!panel.locked){
        el.style.gridColumn='span 1';
        el.style.minHeight='0';
      }else{
        el.style.gridColumn='span 1';
        el.style.gridRow='auto';
      }
    });
  }
  _refreshUsageBadges(){
    this.grid.querySelectorAll('.panel').forEach(el=>{
      const panelId=el.dataset.panelId;
      if(!panelId)return;
      const v=this.state.views[panelId]||{count:0};
      const badge=el.querySelector('.panel-usage');
      if(badge){
        badge.textContent=`${v.count} views`;
        badge.className=`panel-usage ${v.count>100?'high':v.count>20?'medium':'low'}`;
      }
      const rankBadge=el.querySelector('.rank-badge');
      const panelDef=this.panels.find(p=>p.id===panelId);
      if(rankBadge&&panelDef){
        rankBadge.textContent=`#${panelDef.order+1}`;
      }
      const footer=el.querySelector('.panel-footer span:last-child');
      if(footer){
        footer.textContent=`views:${v.count} | ${Math.round(v.totalDuration/1000)}s`;
      }
    });
  }
  _reconcilePanels(){
    this.panels=this._resolvePanelOrder();
    this._mergeOverrides();
  }
  _updateSummary(){
    const total=Object.values(this.state.views).reduce((s,v)=>s+v.count,0);
    document.getElementById('sessionCount').textContent=this.state.sessionCount;
    document.getElementById('totalViews').textContent=total;
    const ageMin=Math.round((Date.now()-this.state.created)/60000);
    document.getElementById('layoutAge').textContent=ageMin+'m';
  }
  _updatePhase(){
    const badge=document.getElementById('phaseBadge');
    const indicator=document.getElementById('modeIndicator');
    if(this.learningPhase){
      badge.textContent='phase: learning (collecting data)';
      indicator.textContent='learning';
    }else{
      badge.textContent='phase: adaptive (auto-layout active)';
      indicator.textContent='adaptive';
    }
  }
  _saveState(){
    try{
      this.state.sessionCount++;
      localStorage.setItem(STORAGE_KEY,JSON.stringify(this.state));
    }catch(e){/* storage full */}
  }
  resetData(){
    this.state=this._freshState();
    this.learningPhase=true;
    this.phaseChangePending=false;
    this._ensurePanels();
    this._reconcilePanels();
    this._render();
    this._updateSummary();
    this._updatePhase();
    this._saveState();
  }
  compactAll(){
    this.panels.forEach(p=>{
      const entry=this.state.layout.find(l=>l.id===p.id);
      if(entry&&!entry.locked){
        entry.compact=true;
        entry.mini=false;
      }
    });
    this._saveState();
    this._reconcilePanels();
    this._render();
  }
  expandAll(){
    this.panels.forEach(p=>{
      const entry=this.state.layout.find(l=>l.id===p.id);
      if(entry&&!entry.locked){
        entry.compact=false;
        entry.mini=false;
      }
    });
    this._saveState();
    this._reconcilePanels();
    this._render();
  }
}
const dash=new AdaptiveDashboard();
document.getElementById('resetDataBtn').addEventListener('click',()=>dash.resetData());
document.getElementById('compactAllBtn').addEventListener('click',()=>dash.compactAll());
document.getElementById('expandAllBtn').addEventListener('click',()=>dash.expandAll());
})();
</script>
```