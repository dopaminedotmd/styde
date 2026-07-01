```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0f1117;--surface:#1a1d27;--surface2:#23273a;--border:#2d3248;--text:#e4e6f0;--text2:#8b8fa3;--accent:#6c5ce7;--accent2:#00cec9;--danger:#ff6b6b;--success:#2ecc71;--radius:10px;--shadow:0 4px 24px rgba(0,0,0,.4);--transition:all .3s cubic-bezier(.4,0,.2,1)}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px}
.toolbar{display:flex;align-items:center;gap:16px;padding:12px 20px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);margin-bottom:16px;flex-wrap:wrap}
.toolbar h1{font-size:18px;font-weight:600;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.toolbar .badge{font-size:11px;color:var(--text2);background:var(--surface2);padding:2px 10px;border-radius:20px;border:1px solid var(--border)}
.toolbar .spacer{flex:1}
.toolbar button{padding:6px 14px;border-radius:6px;border:1px solid var(--border);background:var(--surface2);color:var(--text);cursor:pointer;font-size:12px;transition:var(--transition)}
.toolbar button:hover{background:var(--accent);border-color:var(--accent);color:#fff}
.toolbar button.active{background:var(--accent);border-color:var(--accent);color:#fff}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;transition:var(--transition)}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:var(--transition);position:relative;display:flex;flex-direction:column}
.panel:hover{border-color:var(--accent)}
.panel.dragging{opacity:.5;transform:scale(.97)}
.panel.compact{grid-column:span 1;max-height:52px;overflow:hidden}
.panel.compact .panel-body{display:none}
.panel.compact .panel-header{cursor:pointer}
.panel.locked{border-left:3px solid var(--danger)}
.panel.locked .lock-btn{background:var(--danger);color:#fff;border-color:var(--danger)}
.panel-header{display:flex;align-items:center;gap:8px;padding:10px 14px;background:var(--surface2);border-bottom:1px solid var(--border);cursor:grab;user-select:none;min-height:44px}
.panel-header:active{cursor:grabbing}
.panel-title{font-size:13px;font-weight:600;flex:1;display:flex;align-items:center;gap:6px}
.panel-title .indicator{width:8px;height:8px;border-radius:50%;display:inline-block}
.panel-title .indicator.high{background:var(--success)}
.panel-title .indicator.med{background:var(--accent2)}
.panel-title .indicator.low{background:var(--text2)}
.panel-controls{display:flex;gap:4px}
.panel-controls button{width:26px;height:26px;border-radius:5px;border:1px solid var(--border);background:transparent;color:var(--text2);cursor:pointer;font-size:11px;display:flex;align-items:center;justify-content:center;transition:var(--transition)}
.panel-controls button:hover{background:var(--surface);color:var(--text)}
.panel-controls .lock-btn:hover{color:var(--danger);border-color:var(--danger)}
.panel-controls .collapse-btn:hover{color:var(--accent2);border-color:var(--accent2)}
.panel-body{padding:14px;flex:1;min-height:100px}
.panel-body canvas,.panel-body .chart-placeholder{width:100%;height:120px;background:var(--surface2);border-radius:6px;display:flex;align-items:center;justify-content:center;color:var(--text2);font-size:12px}
.panel-body .stat-row{display:flex;justify-content:space-between;padding:4px 0;font-size:12px;border-bottom:1px solid var(--border)}
.panel-body .stat-row .label{color:var(--text2)}
.panel-body .stat-row .value{font-weight:600}
.panel-body .mini-preview{display:flex;gap:8px;align-items:center;font-size:11px;color:var(--text2);padding:4px 0}
.panel-body .mini-preview .mini-val{font-weight:600;color:var(--text);font-size:14px}
.rank-badge{position:absolute;top:8px;right:8px;background:var(--accent);color:#fff;font-size:10px;padding:1px 7px;border-radius:10px;font-weight:700;opacity:.7}
.drop-zone{border:2px dashed var(--accent);border-radius:var(--radius);background:rgba(108,92,231,.08);min-height:60px;display:flex;align-items:center;justify-content:center;color:var(--accent);font-size:13px;transition:var(--transition);opacity:0;pointer-events:none}
.drop-zone.active{opacity:1;min-height:80px;margin-bottom:14px}
.overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.6);z-index:100;display:none;align-items:center;justify-content:center}
.overlay.active{display:flex}
.overlay-content{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px;min-width:340px;max-width:480px;max-height:70vh;overflow-y:auto}
.overlay-content h2{font-size:16px;margin-bottom:16px}
.stats-table{width:100%;border-collapse:collapse;font-size:12px}
.stats-table th{text-align:left;padding:6px 8px;background:var(--surface2);color:var(--text2);font-weight:500;border-bottom:1px solid var(--border)}
.stats-table td{padding:6px 8px;border-bottom:1px solid var(--border)}
.stats-table tr:hover td{background:var(--surface2)}
.attention-bar{height:4px;border-radius:2px;background:var(--border);overflow:hidden;margin-top:2px}
.attention-bar .fill{height:100%;border-radius:2px;background:linear-gradient(90deg,var(--accent2),var(--accent));transition:width .6s ease}
@media(max-width:700px){.grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="toolbar">
  <h1>Adaptive Metric Layout</h1>
  <span class="badge">v1</span>
  <span class="spacer"></span>
  <span style="font-size:12px;color:var(--text2)" id="adaptCount">adapts: 0</span>
  <button onclick="toggleOverlay()">stats</button>
  <button onclick="resetAdaptation()">reset</button>
  <button id="autoAdaptBtn" class="active" onclick="toggleAutoAdapt()">auto</button>
</div>
<div class="grid" id="dashboardGrid"></div>
<div class="overlay" id="statsOverlay">
  <div class="overlay-content">
    <h2>Panel Attention Metrics</h2>
    <table class="stats-table">
      <thead><tr><th>panel</th><th>views</th><th>clicks</th><th>avg s</th><th>score</th><th>rank</th></tr></thead>
      <tbody id="statsBody"></tbody>
    </table>
    <br>
    <button onclick="toggleOverlay()" style="padding:6px 14px;border-radius:6px;border:1px solid var(--border);background:var(--surface2);color:var(--text);cursor:pointer;font-size:12px">close</button>
  </div>
</div>
<script>
// ─── DATA ───────────────────────────────────────────────────────────────────
const PANEL_DEFS = [
  {id:'revenue',    title:'Revenue',       indicator:'high', chart:true,  stats:{label:'MTD',val:'$284.6K'}, extra:'MoM +12.4%'},
  {id:'users',      title:'Active Users',   indicator:'high', chart:true,  stats:{label:'today',val:'18,432'}, extra:'+842 vs yesterday'},
  {id:'conversion', title:'Conversion',     indicator:'med',  chart:true,  stats:{label:'rate',val:'3.87%'}, extra:'+0.21pp'},
  {id:'retention',  title:'Retention',      indicator:'med',  chart:false, stats:{label:'d30',val:'68.2%'},  extra:'cohort: May'},
  {id:'traffic',    title:'Traffic Sources',indicator:'med',  chart:true,  stats:{label:'top',val:'organic'}, extra:'42% share'},
  {id:'errors',     title:'Error Rate',     indicator:'low',  chart:false, stats:{label:'5min',val:'0.23%'}, extra:'p99 1.2%'},
  {id:'latency',    title:'Latency p95',    indicator:'low',  chart:false, stats:{label:'avg',val:'214ms'},  extra:'p99 890ms'},
  {id:'sessions',   title:'Sessions',       indicator:'low',  chart:true,  stats:{label:'avg/usr',val:'4.7'}, extra:'duration 12m'},
];
// ─── TRACKING ───────────────────────────────────────────────────────────────
const STORAGE_KEY = 'adaptive_layout_v1';
function loadState(){
  try{
    const raw=localStorage.getItem(STORAGE_KEY);
    return raw?JSON.parse(raw):null;
  }catch{return null}
}
function saveState(){
  const data={
    tracking,
    positions:panels.map(p=>p.id),
    overrides:panels.reduce((a,p)=>{if(p.locked||p.customPos!==null)a[p.id]={locked:p.locked,pos:p.customPos};return a},{})
  };
  try{localStorage.setItem(STORAGE_KEY,JSON.stringify(data))}catch{}
}
let tracking = loadState()?.tracking || {};
PANEL_DEFS.forEach(d=>{
  if(!tracking[d.id]) tracking[d.id]={views:0,clicks:0,totalDuration:0,entries:0,compactCount:0};
});
function recordView(id){
  tracking[id].views++;
  tracking[id].entries++;
  tracking[id].lastEntry=performance.now();
  scheduleSave();
}
function recordClick(id){
  tracking[id].clicks++;
  scheduleSave();
}
function recordDuration(id){
  const t=tracking[id];
  if(t.lastEntry){const elapsed=(performance.now()-t.lastEntry)/1000;t.totalDuration+=elapsed;t.lastEntry=null;}
}
function recordCompact(id,compact){
  tracking[id].compactCount+=compact?1:0;
  scheduleSave();
}
let _saveTimer;
function scheduleSave(){clearTimeout(_saveTimer);_saveTimer=setTimeout(saveState,500);}
function attentionScore(id){
  const t=tracking[id];
  if(!t||t.views===0)return 0;
  const freq=t.views;
  const avgDur=t.totalDuration/Math.max(t.entries,1);
  const recency=1;
  return freq*Math.min(avgDur,30)*recency;
}
// ─── STATE ──────────────────────────────────────────────────────────────────
let panels = [];
let adaptCount = 0;
let autoAdapt = true;
let dragSrc=null;
function buildPanels(){
  const saved=loadState();
  const savedOverrides=saved?.overrides||{};
  const savedPos=saved?.positions||[];
  let defs=[...PANEL_DEFS];
  if(savedPos.length){
    const posMap={};
    savedPos.forEach((id,i)=>posMap[id]=i);
    defs.sort((a,b)=>(posMap[a.id]??99)-(posMap[b.id]??99));
  }
  panels=defs.map((d,i)=>{
    const ov=savedOverrides[d.id];
    return{
      ...d,
      compact:i>=5,
      locked:ov?.locked||false,
      customPos:ov?.pos??null,
      rank:i,
    };
  });
  recomputeRanks();
  render();
}
function recomputeRanks(){
  const scored=panels.map(p=>({id:p.id,score:attentionScore(p.id)}));
  scored.sort((a,b)=>b.score-a.score);
  const rankMap={};
  scored.forEach((s,i)=>rankMap[s.id]=i);
  panels.forEach(p=>p.rank=rankMap[p.id]??99);
}
// ─── RENDER ─────────────────────────────────────────────────────────────────
function render(){
  const grid=document.getElementById('dashboardGrid');
  grid.innerHTML='';
  const sorted=[...panels].sort((a,b)=>{
    if(a.locked&&b.locked)return 0;
    if(a.locked)return -1;
    if(b.locked)return 1;
    const pa=a.customPos!==null?a.customPos:99;
    const pb=b.customPos!==null?b.customPos:99;
    if(pa!==pb)return pa-pb;
    return a.rank-b.rank;
  });
  sorted.forEach((p,i)=>{
    const card=document.createElement('div');
    card.className='panel'+(p.compact?' compact':'')+(p.locked?' locked':'');
    card.dataset.id=p.id;
    card.draggable=!p.locked;
    card.innerHTML=`
      <div class="panel-header">
        <div class="panel-title">
          <span class="indicator ${p.indicator}"></span>
          ${p.title}
        </div>
        <div class="panel-controls">
          <button class="lock-btn" onclick="toggleLock('${p.id}')" title="lock position">&#x1F512;</button>
          <button class="collapse-btn" onclick="toggleCompact('${p.id}')" title="collapse">${p.compact?'&#x25B2;':'&#x25BC;'}</button>
        </div>
      </div>
      <div class="panel-body">
        ${p.compact?`<div class="mini-preview"><span class="mini-val">${p.stats.value}</span> ${p.stats.label} &middot; ${p.extra}</div>`
          :`<div class="stat-row"><span class="label">${p.stats.label}</span><span class="value">${p.stats.value}</span></div>
            <div class="stat-row"><span class="label">trend</span><span class="value">${p.extra}</span></div>
            <div class="attention-bar"><div class="fill" style="width:${Math.min(100,attentionScore(p.id)/5)}%"></div></div>
            ${p.chart?`<canvas id="chart-${p.id}" width="400" height="100"></canvas>`:''}
            <div style="font-size:10px;color:var(--text2);margin-top:6px">rank #${p.rank+1} &middot; score ${attentionScore(p.id).toFixed(1)}</div>`
        }
      </div>
    `;
    // drag events
    card.addEventListener('dragstart',(e)=>{
      if(p.locked){e.preventDefault();return}
      dragSrc=p.id;
      card.classList.add('dragging');
      e.dataTransfer.effectAllowed='move';
    });
    card.addEventListener('dragend',()=>{
      card.classList.remove('dragging');
    });
    card.addEventListener('dragover',(e)=>{
      e.preventDefault();
      if(p.locked||p.id===dragSrc)return;
      e.dataTransfer.dropEffect='move';
    });
    card.addEventListener('drop',(e)=>{
      e.preventDefault();
      if(p.locked||!dragSrc||dragSrc===p.id)return;
      swapPanels(dragSrc,p.id);
      dragSrc=null;
    });
    // tracking
    card.addEventListener('mouseenter',()=>recordView(p.id));
    card.addEventListener('click',()=>recordClick(p.id));
    card.addEventListener('mouseleave',()=>recordDuration(p.id));
    card.addEventListener('transitionend',()=>{
      if(p.compact&&!card.classList.contains('compact'))recordCompact(p.id,false);
      else if(!p.compact&&card.classList.contains('compact'))recordCompact(p.id,true);
    });
    grid.appendChild(card);
  });
  // mini charts
  sorted.filter(p=>p.chart).forEach(p=>{
    requestAnimationFrame(()=>drawMiniChart(p.id));
  });
  document.getElementById('adaptCount').textContent=`adapts: ${adaptCount}`;
  saveState();
}
function drawMiniChart(id){
  const canvas=document.getElementById('chart-'+id);
  if(!canvas)return;
  const ctx=canvas.getContext('2d');
  const w=canvas.width=canvas.clientWidth*2||800;
  const h=canvas.height=canvas.clientHeight*2||200;
  ctx.clearRect(0,0,w,h);
  const data=Array.from({length:30},()=>Math.random()*50+10);
  const colors={revenue:'#6c5ce7',users:'#00cec9',conversion:'#2ecc71',traffic:'#fdcb6e',sessions:'#e17055'};
  const color=colors[id]||'#6c5ce7';
  ctx.strokeStyle=color;
  ctx.lineWidth=3;
  ctx.beginPath();
  const pw=w/(data.length-1);
  data.forEach((v,i)=>{
    const x=i*pw;
    const y=h-(v/60)*h;
    i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
  });
  ctx.stroke();
  // fill
  ctx.lineTo((data.length-1)*pw,h);
  ctx.lineTo(0,h);
  ctx.closePath();
  const grad=ctx.createLinearGradient(0,0,0,h);
  grad.addColorStop(0,color+'44');
  grad.addColorStop(1,color+'00');
  ctx.fillStyle=grad;
  ctx.fill();
}
// ─── ACTIONS ────────────────────────────────────────────────────────────────
function toggleLock(id){
  const p=panels.find(x=>x.id===id);
  if(!p)return;
  p.locked=!p.locked;
  if(!p.locked)p.customPos=null;
  render();
}
function toggleCompact(id){
  const p=panels.find(x=>x.id===id);
  if(!p)return;
  p.compact=!p.compact;
  render();
}
function swapPanels(a,b){
  const pa=panels.find(x=>x.id===a);
  const pb=panels.find(x=>x.id===b);
  if(!pa||!pb)return;
  if(pa.locked||pb.locked)return;
  const tmp=pa.customPos??pa.rank;
  pa.customPos=pb.customPos??pb.rank;
  pb.customPos=tmp;
  render();
}
function toggleOverlay(){
  const ov=document.getElementById('statsOverlay');
  ov.classList.toggle('active');
  if(ov.classList.contains('active')){
    const body=document.getElementById('statsBody');
    const scored=panels.map(p=>({...p,score:attentionScore(p.id)}));
    scored.sort((a,b)=>b.score-a.score);
    body.innerHTML=scored.map(p=>`
      <tr>
        <td>${p.title}</td>
        <td>${tracking[p.id].views}</td>
        <td>${tracking[p.id].clicks}</td>
        <td>${(tracking[p.id].totalDuration/Math.max(tracking[p.id].entries,1)).toFixed(1)}</td>
        <td>${p.score.toFixed(1)}</td>
        <td>#${p.rank+1}</td>
      </tr>
    `).join('');
  }
}
function resetAdaptation(){
  localStorage.removeItem(STORAGE_KEY);
  PANEL_DEFS.forEach(d=>{tracking[d.id]={views:0,clicks:0,totalDuration:0,entries:0,compactCount:0};});
  panels.forEach((p,i)=>{p.compact=i>=5;p.locked=false;p.customPos=null;p.rank=i;});
  adaptCount=0;
  render();
}
function toggleAutoAdapt(){
  autoAdapt=!autoAdapt;
  document.getElementById('autoAdaptBtn').classList.toggle('active');
}
// ─── ADAPTATION LOOP ────────────────────────────────────────────────────────
function adapt(){
  if(!autoAdapt)return;
  recomputeRanks();
  const scored=panels.map(p=>({id:p.id,score:attentionScore(p.id),rank:p.rank,compact:p.compact,locked:p.locked}));
  scored.sort((a,b)=>b.score-a.score);
  let changed=false;
  scored.forEach((s,i)=>{
    const p=panels.find(x=>x.id===s.id);
    if(!p||p.locked)return;
    // top 2 -> expanded, bottom 2 -> compact
    const shouldCompact=i>=scored.length-2;
    if(i<2&&p.compact){p.compact=false;changed=true;}
    else if(i>=2&&i<scored.length-2){
      // middle: leave as is unless score dropped below threshold
      if(s.score<2&&!p.compact){p.compact=true;changed=true;}
    }
    if(shouldCompact&&!p.compact){p.compact=true;changed=true;}
  });
  if(changed){
    adaptCount++;
    render();
  }
}
// run adaptation every 5s
setInterval(adapt,5000);
// -- keyboard shortcuts
document.addEventListener('keydown',e=>{
  if(e.key==='s'&&!e.ctrlKey){toggleOverlay();e.preventDefault()}
  if(e.key==='r'&&!e.ctrlKey){resetAdaptation();e.preventDefault()}
});
// ─── INIT ───────────────────────────────────────────────────────────────────
buildPanels();
</script>
</body>
</html>
```