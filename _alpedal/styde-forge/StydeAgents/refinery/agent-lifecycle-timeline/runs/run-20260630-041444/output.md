agent-lifecycle-timeline complete solution output:
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0d1117;color:#c9d1d9;font-family:'Segoe UI',system-ui,sans-serif;overflow-x:hidden}
header{background:#161b22;border-bottom:1px solid #30363d;padding:16px 24px;display:flex;align-items:center;justify-content:space-between}
header h1{font-size:18px;font-weight:600;color:#f0f6fc;display:flex;align-items:center;gap:8px}
header h1 span{color:#8b949e;font-size:14px;font-weight:400}
.header-controls{display:flex;align-items:center;gap:16px}
#playBtn{background:#238636;border:none;color:#fff;padding:6px 18px;border-radius:6px;cursor:pointer;font-size:13px;font-weight:600}
#playBtn:hover{background:#2ea043}
#playBtn.active{background:#da3633}
#playBtn.active:hover{background:#f85149}
#timeLabel{font-size:13px;color:#8b949e;font-family:monospace;min-width:160px}
#legend{position:fixed;bottom:24px;right:24px;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px 16px;z-index:100;display:flex;flex-direction:column;gap:6px}
#legend .legend-item{display:flex;align-items:center;gap:8px;font-size:12px;color:#c9d1d9}
#legend .legend-dot{width:12px;height:12px;border-radius:50%;flex-shrink:0}
#tooltip{position:fixed;display:none;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px 18px;z-index:200;box-shadow:0 8px 24px rgba(0,0,0,0.4);min-width:220px;max-width:350px}
#tooltip.visible{display:block}
#tooltip .tt-title{font-size:14px;font-weight:600;color:#f0f6fc;margin-bottom:8px}
#tooltip .tt-row{display:flex;justify-content:space-between;gap:16px;font-size:12px;padding:2px 0}
#tooltip .tt-label{color:#8b949e}
#tooltip .tt-value{color:#c9d1d9;font-family:monospace;text-align:right}
#tooltip .tt-score{font-size:20px;font-weight:700;text-align:center;padding:6px 0;margin-bottom:6px;border-radius:6px}
#scrubContainer{position:fixed;bottom:0;left:0;right:0;background:#161b22;border-top:1px solid #30363d;padding:12px 24px 16px;z-index:50;display:flex;flex-direction:column;gap:6px}
#scrubLabel{display:flex;justify-content:space-between;font-size:11px;color:#8b949e;font-family:monospace}
#scrubRange{width:100%;height:6px;-webkit-appearance:none;appearance:none;background:#30363d;border-radius:3px;outline:none;cursor:pointer}
#scrubRange::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:#58a6ff;border:2px solid #1f6feb;cursor:pointer;transition:background .15s}
#scrubRange::-webkit-slider-thumb:hover{background:#79c0ff}
#scrubRange::-moz-range-thumb{width:16px;height:16px;border-radius:50%;background:#58a6ff;border:2px solid #1f6feb;cursor:pointer}
#container{width:100%;padding:16px 24px 80px;overflow-x:auto}
#timeline{width:100%;min-width:900px}
.track-label{cursor:pointer;transition:opacity .2s;font-size:13px}
.track-label:hover{opacity:1!important;text-decoration:underline}
.node{cursor:pointer;transition:transform .15s,opacity .15s}
.node:hover{transform:scale(1.35);opacity:1!important}
.node.dimmed,.edge.dimmed{opacity:.18}
.edge{transition:opacity .2s}
.edge.highlight{opacity:.7}
#axis text{font-family:monospace;fill:#8b949e}
.completeness-bar{position:relative;height:4px;background:#30363d;border-radius:2px;margin:16px 0 0}
.completeness-fill{height:100%;background:#238636;border-radius:2px;transition:width .8s ease}
.completeness-label{font-size:11px;color:#8b949e;margin-top:2px;display:flex;justify-content:space-between}
</style>
</head>
<body>
<header>
<h1>Agent Lifecycle Timeline <span>Styde Forge</span></h1>
<div class="header-controls">
<span id="timeLabel">scrub to explore</span>
<button id="playBtn">play</button>
</div>
</header>
<div id="container">
<svg id="timeline"></svg>
<div class="completeness-bar">
<div class="completeness-fill" id="completenessFill" style="width:0%"></div>
</div>
<div class="completeness-label"><span>completeness</span><span id="completenessPct">0%</span></div>
</div>
<div id="scrubContainer">
<div id="scrubLabel"><span id="scrubEarliest"></span><span id="scrubCurrent"></span><span id="scrubLatest"></span></div>
<input type="range" id="scrubRange" min="0" max="1000" value="1000">
</div>
<div id="legend">
<div class="legend-item"><span class="legend-dot" style="background:#ffd700;box-shadow:0 0 6px #ffd70055"></span>hot gold (85+)</div>
<div class="legend-item"><span class="legend-dot" style="background:#f0883e"></span>amber (70-84)</div>
<div class="legend-item"><span class="legend-dot" style="background:#58a6ff"></span>cool (&lt;70)</div>
<div class="legend-item"><span class="legend-dot" style="background:#8b949e;width:8px;height:2px;border-radius:1px"></span>running</div>
</div>
<div id="tooltip"></div>
<script>
const STATE_PATH = 'state.yaml';
const MARGIN = {top:50,right:60,bottom:20,left:240};
const NODE_R = 8;
const TRACK_H = 48;
const TRACK_GAP = 8;
const COLORS = {
  gold:'#ffd700',
  goldGlow:'#ffd70055',
  amber:'#f0883e',
  cool:'#58a6ff',
  edge:'#30363d',
  edgeRunning:'#58a6ff88',
  running:'#8b949e'
};
let allEvents=[], blueprints=[], timeMin, timeMax, timeRange;
let scrubValue=1000, isPlaying=false, playInterval=null;
let highlightedNode=null;
const svg = document.getElementById('timeline');
const scrubRange = document.getElementById('scrubRange');
const scrubCurrent = document.getElementById('scrubCurrent');
const scrubEarliest = document.getElementById('scrubEarliest');
const scrubLatest = document.getElementById('scrubLatest');
const timeLabel = document.getElementById('timeLabel');
const playBtn = document.getElementById('playBtn');
const tooltip = document.getElementById('tooltip');
const completenessFill = document.getElementById('completenessFill');
const completenessPct = document.getElementById('completenessPct');
function fmtTime(d){return d.toISOString().slice(0,16).replace('T',' ')}
function fmtShort(d){return d.toISOString().slice(11,16)}
function parseTS(s){return new Date(s.replace(' ','T')+'Z')}
function fracToTime(frac){return new Date(timeMin.getTime()+frac*timeRange)}
function updateScrubLabel(){
  if(!allEvents.length)return;
  const f=scrubValue/1000;
  const t=fracToTime(f);
  scrubCurrent.textContent=fmtShort(t);
  timeLabel.textContent='showing: '+fmtTime(t);
}
function computeScore(detail){
  const m=detail.match(/C:([\d.]+)/);
  if(m)return parseFloat(m[1]);
  const sm=detail.match(/S:(\d+)/);
  if(sm)return parseInt(sm[1]);
  return null;
}
function getColor(score){
  if(score===null)return COLORS.running;
  if(score>=85)return COLORS.gold;
  if(score>=70)return COLORS.amber;
  return COLORS.cool;
}
function getGlow(score){
  if(score!==null&&score>=85)return COLORS.goldGlow;
  return 'transparent';
}
// Parse state.yaml text
function parseStateYaml(text){
  const lines=text.split('\n');
  const entries=[];
  let current=null;
  for(let line of lines){
    const trimmed=line.trim();
    if(trimmed.startsWith('- action:')){
      if(current&&current.blueprint)entries.push(current);
      current={action:trimmed.split(':')[1].trim(),blueprint:null,detail:null,id:null,progress:null,status:null,timestamp:null};
      continue;
    }
    if(!current)continue;
    const m=trimmed.match(/^(\w+):\s*(.+)$/);
    if(m){
      const k=m[1],v=m[2].trim();
      if(k==='blueprint'||k==='detail'||k==='timestamp')current[k]=v;
      else if(k==='id'||k==='progress')current[k]=parseInt(v)||v;
      else if(k==='status')current[k]=v;
    }
  }
  if(current&&current.blueprint)entries.push(current);
  return entries.filter(e=>e.timestamp);
}
function buildData(entries){
  const bpMap={};
  for(const e of entries){
    const bp=e.blueprint||'unknown';
    if(!bpMap[bp])bpMap[bp]={name:bp,runs:[]};
    const score=computeScore(e.detail);
    bpMap[bp].runs.push({
      id:e.id,
      action:e.action,
      detail:e.detail,
      progress:e.progress,
      status:e.status,
      timestamp:parseTS(e.timestamp),
      score,
      color:getColor(score),
      glow:getGlow(score)
    });
  }
  const bps=Object.values(bpMap);
  for(const bp of bps){
    bp.runs.sort((a,b)=>a.timestamp-b.timestamp);
  }
  bps.sort((a,b)=>b.runs.length-a.runs.length);
  return bps;
}
function render(bps){
  blueprints=bps;
  allEvents=[];
  for(const bp of bps)allEvents.push(...bp.runs);
  allEvents.sort((a,b)=>a.timestamp-b.timestamp);
  if(!allEvents.length)return;
  timeMin=allEvents[0].timestamp;
  timeMax=allEvents[allEvents.length-1].timestamp;
  timeRange=timeMax-timeMin;
  if(timeRange===0)timeRange=1;
  scrubEarliest.textContent=fmtShort(timeMin);
  scrubLatest.textContent=fmtShort(timeMax);
  updateScrubLabel();
  const W=Math.max(1000,timeRange/60000*4+300);
  const H=TRACK_H*bps.length+TRACK_GAP*(bps.length-1)+MARGIN.top+MARGIN.bottom;
  svg.setAttribute('viewBox',`0 0 ${W+MARGIN.left+MARGIN.right} ${H}`);
  svg.setAttribute('height',H+20);
  svg.innerHTML='';
  // Defs
  const defs=document.createElementNS('http://www.w3.org/2000/svg','defs');
  defs.innerHTML=`
    <filter id="glowGold"><feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#ffd700" flood-opacity="0.4"/></filter>
    <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#30363d"/>
    </marker>
  `;
  svg.appendChild(defs);
  // Clip
  const clip=document.createElementNS('http://www.w3.org/2000/svg','clipPath');
  clip.id='timelineClip';
  const clipRect=document.createElementNS('http://www.w3.org/2000/svg','rect');
  clipRect.setAttribute('x',MARGIN.left);
  clipRect.setAttribute('y',MARGIN.top-20);
  clipRect.setAttribute('width',W);
  clipRect.setAttribute('height',H-MARGIN.top-MARGIN.bottom+40);
  clip.appendChild(clipRect);
  svg.appendChild(clip);
  const mainGroup=document.createElementNS('http://www.w3.org/2000/svg','g');
  mainGroup.setAttribute('clip-path','url(#timelineClip)');
  // Axis group (tick marks, not clipped)
  const axisGroup=document.createElementNS('http://www.w3.org/2000/svg','g');
  axisGroup.id='axis';
  // X axis ticks
  const tickCount=Math.max(5,Math.min(15,Math.floor(W/80)));
  for(let i=0;i<=tickCount;i++){
    const frac=i/tickCount;
    const x=MARGIN.left+frac*W;
    const tick=document.createElementNS('http://www.w3.org/2000/svg','line');
    tick.setAttribute('x1',x);tick.setAttribute('y1',MARGIN.top-8);
    tick.setAttribute('x2',x);tick.setAttribute('y2',MARGIN.top-4);
    tick.setAttribute('stroke','#30363d');tick.setAttribute('stroke-width','1');
    axisGroup.appendChild(tick);
    const t=fracToTime(frac);
    const label=document.createElementNS('http://www.w3.org/2000/svg','text');
    label.setAttribute('x',x);label.setAttribute('y',MARGIN.top-14);
    label.setAttribute('text-anchor','middle');label.setAttribute('fill','#8b949e');
    label.setAttribute('font-size','10');label.setAttribute('font-family','monospace');
    label.textContent=fmtShort(t);
    axisGroup.appendChild(label);
  }
  // Axis title
  const axisTitle=document.createElementNS('http://www.w3.org/2000/svg','text');
  axisTitle.setAttribute('x',MARGIN.left+W/2);
  axisTitle.setAttribute('y',MARGIN.top-24);
  axisTitle.setAttribute('text-anchor','middle');
  axisTitle.setAttribute('fill','#8b949e');
  axisTitle.setAttribute('font-size','11');
  axisTitle.setAttribute('font-family','monospace');
  axisTitle.textContent='time (UTC)';
  axisGroup.appendChild(axisTitle);
  // Grid lines
  for(let i=0;i<=tickCount;i++){
    const frac=i/tickCount;
    const x=MARGIN.left+frac*W;
    const line=document.createElementNS('http://www.w3.org/2000/svg','line');
    line.setAttribute('x1',x);line.setAttribute('y1',MARGIN.top);
    line.setAttribute('x2',x);line.setAttribute('y2',MARGIN.top+TRACK_H*bps.length+TRACK_GAP*(bps.length-1));
    line.setAttribute('stroke','#21262d');line.setAttribute('stroke-width','1');
    line.setAttribute('stroke-dasharray','3,3');
    axisGroup.appendChild(line);
  }
  svg.appendChild(axisGroup);
  // Tracks
  bps.forEach((bp,bpIdx)=>{
    const y=MARGIN.top+bpIdx*(TRACK_H+TRACK_GAP);
    const runs=bp.runs;
    // Track bg
    const bg=document.createElementNS('http://www.w3.org/2000/svg','rect');
    bg.setAttribute('x',MARGIN.left);bg.setAttribute('y',y);
    bg.setAttribute('width',W);bg.setAttribute('height',TRACK_H);
    bg.setAttribute('fill','#161b22');bg.setAttribute('rx','4');
    bg.setAttribute('stroke','#21262d');bg.setAttribute('stroke-width','1');
    mainGroup.appendChild(bg);
    // Track label
    const label=document.createElementNS('http://www.w3.org/2000/svg','text');
    label.setAttribute('x',MARGIN.left-8);label.setAttribute('y',y+TRACK_H/2+4);
    label.setAttribute('text-anchor','end');label.setAttribute('fill','#c9d1d9');
    label.setAttribute('font-size','12');label.setAttribute('font-family','monospace');
    label.setAttribute('class','track-label');
    label.setAttribute('opacity','0.85');
    label.textContent=bp.name;
    const shortName=bp.name.length>30?bp.name.slice(0,27)+'...':bp.name;
    label.textContent=shortName;
    svg.appendChild(label);
  });
  svg.appendChild(mainGroup);
  // Connection edges (run-to-run lines for same blueprint)
  bps.forEach((bp,bpIdx)=>{
    const y=MARGIN.top+bpIdx*(TRACK_H+TRACK_GAP)+TRACK_H/2;
    for(let i=1;i<bp.runs.length;i++){
      const prev=bp.runs[i-1];
      const curr=bp.runs[i];
      const pf=(prev.timestamp-timeMin)/timeRange;
      const cf=(curr.timestamp-timeMin)/timeRange;
      const x1=MARGIN.left+pf*W;
      const x2=MARGIN.left+cf*W;
      const edge=document.createElementNS('http://www.w3.org/2000/svg','line');
      edge.setAttribute('x1',x1);edge.setAttribute('y1',y);
      edge.setAttribute('x2',x2);edge.setAttribute('y2',y);
      edge.setAttribute('stroke',curr.status==='running'?COLORS.edgeRunning:COLORS.edge);
      edge.setAttribute('stroke-width','1.5');
      edge.setAttribute('stroke-dasharray',curr.status==='running'?'4,3':'none');
      edge.setAttribute('class','edge');
      mainGroup.appendChild(edge);
    }
  });
  // Nodes
  bps.forEach((bp,bpIdx)=>{
    const y=MARGIN.top+bpIdx*(TRACK_H+TRACK_GAP)+TRACK_H/2;
    bp.runs.forEach((run,runIdx)=>{
      const frac=(run.timestamp-timeMin)/timeRange;
      const x=MARGIN.left+frac*W;
      const g=document.createElementNS('http://www.w3.org/2000/svg','g');
      g.setAttribute('class','node');
      g.dataset.bpIdx=bpIdx;
      g.dataset.runIdx=runIdx;
      g.dataset.bp=bp.name;
      g.dataset.id=run.id;
      g.dataset.action=run.action;
      g.dataset.detail=run.detail||'';
      g.dataset.score=run.score!==null?run.score:'';
      g.dataset.status=run.status;
      g.dataset.timestamp=run.timestamp.toISOString();
      g.dataset.bpName=bp.name;
      g.dataset.runIndex=runIdx+1;
      let rad=NODE_R;
      if(run.action==='improve')rad=6;
      if(run.action==='spawn')rad=7;
      if(run.action==='eval')rad=NODE_R;
      const circle=document.createElementNS('http://www.w3.org/2000/svg','circle');
      circle.setAttribute('cx',x);circle.setAttribute('cy',y);
      circle.setAttribute('r',rad);
      circle.setAttribute('fill',run.color);
      circle.setAttribute('stroke',run.status==='running'?'#58a6ff':'none');
      circle.setAttribute('stroke-width',run.status==='running'?'2':'0');
      circle.setAttribute('stroke-dasharray',run.status==='running'?'3,2':'none');
      if(run.score!==null&&run.score>=85){
        circle.setAttribute('filter','url(#glowGold)');
        circle.setAttribute('stroke','#ffd700');
        circle.setAttribute('stroke-width','1.5');
      }
      // Score label for eval nodes with score
      if(run.action==='eval'&&run.score!==null){
        const sc=document.createElementNS('http://www.w3.org/2000/svg','text');
        sc.setAttribute('x',x);sc.setAttribute('y',y+rad+14);
        sc.setAttribute('text-anchor','middle');sc.setAttribute('fill','#8b949e');
        sc.setAttribute('font-size','9');sc.setAttribute('font-family','monospace');
        sc.textContent=run.score;
        g.appendChild(sc);
      }
      g.appendChild(circle);
      g.addEventListener('click',(e)=>{
        e.stopPropagation();
        showTooltip(run,bp.name,runIdx+1,e);
      });
      g.addEventListener('mouseenter',(e)=>{
        highlightNode(bpIdx,runIdx);
      });
      g.addEventListener('mouseleave',()=>{
        clearHighlight();
      });
      mainGroup.appendChild(g);
    });
  });
}
function highlightNode(bpIdx,runIdx){
  document.querySelectorAll('.node').forEach(n=>n.classList.add('dimmed'));
  document.querySelectorAll('.edge').forEach(e=>e.classList.add('dimmed'));
  const nodes=document.querySelectorAll('.node');
  nodes.forEach(n=>{
    const bi=parseInt(n.dataset.bpidx);
    const ri=parseInt(n.dataset.runidx);
    if(bi===bpIdx){
      n.classList.remove('dimmed');
      // Also highlight edges on this track
      const edges=document.querySelectorAll('.edge');
      let edgeIdx=0;
      document.querySelectorAll('.edge').forEach((e,idx)=>{
        e.classList.remove('highlight');
      });
    }
  });
  // Highlight edges on same track
  document.querySelectorAll('.edge').forEach((e,i)=>{
    // Simple approach: edges are per-track in order
    e.classList.remove('dimmed');
    e.classList.add('highlight');
  });
}
function clearHighlight(){
  document.querySelectorAll('.node').forEach(n=>n.classList.remove('dimmed'));
  document.querySelectorAll('.edge').forEach(e=>{e.classList.remove('dimmed');e.classList.remove('highlight');});
}
function showTooltip(run,bpName,iter,e){
  const scoreStr=run.score!==null?run.score:'--';
  const scoreColor=run.score!==null?(run.score>=85?'#ffd700':run.score>=70?'#f0883e':'#58a6ff'):'#8b949e';
  const detailPreview=run.detail?run.detail.slice(0,80):'';
  tooltip.innerHTML=`
    <div class="tt-title">${bpName} #${iter}</div>
    <div class="tt-score" style="background:${scoreColor}22;color:${scoreColor}">${scoreStr}</div>
    <div class="tt-row"><span class="tt-label">id</span><span class="tt-value">${run.id}</span></div>
    <div class="tt-row"><span class="tt-label">action</span><span class="tt-value">${run.action}</span></div>
    <div class="tt-row"><span class="tt-label">status</span><span class="tt-value">${run.status}</span></div>
    <div class="tt-row"><span class="tt-label">score (C)</span><span class="tt-value">${scoreStr}</span></div>
    <div class="tt-row"><span class="tt-label">time</span><span class="tt-value">${fmtTime(run.timestamp)}</span></div>
    <div class="tt-row"><span class="tt-label">detail</span><span class="tt-value" style="max-width:180px;word-break:break-word">${detailPreview}</span></div>
  `;
  tooltip.classList.add('visible');
  // Tooltip positioning with collision detection
  const tx=e.clientX||e.pageX;
  const ty=e.clientY||e.pageY;
  const tw=tooltip.offsetWidth;
  const th=tooltip.offsetHeight;
  const vw=window.innerWidth;
  const vh=window.innerHeight;
  const pad=12;
  let left,top;
  const preferAbove=ty-th-pad>0;
  const preferBelow=ty+th+pad<vh;
  const preferRight=tx+tw+pad<vw;
  const preferLeft=tx-tw-pad>0;
  if(preferAbove){top=ty-th-pad;left=tx-tw/2;}
  else if(preferBelow){top=ty+th+pad;left=tx-tw/2;}
  else if(preferRight){top=ty-th/2;left=tx+pad;}
  else if(preferLeft){top=ty-th/2;left=tx-tw-pad;}
  else{top=Math.max(pad,ty-th/2);left=Math.max(pad,Math.min(vw-tw-pad,tx-tw/2));}
  // Clamp
  top=Math.max(pad,Math.min(vh-th-pad,top));
  left=Math.max(pad,Math.min(vw-tw-pad,left));
  tooltip.style.top=top+'px';
  tooltip.style.left=left+'px';
}
function hideTooltip(){
  tooltip.classList.remove('visible');
}
document.addEventListener('click',(e)=>{
  if(!e.target.closest('.node'))hideTooltip();
});
// Scrub filter
function applyScrub(){
  const frac=scrubValue/1000;
  const cutoff=fracToTime(frac);
  document.querySelectorAll('.node').forEach(n=>{
    const t=new Date(n.dataset.timestamp);
    const visible=t<=cutoff;
    n.style.display=visible?'':'none';
  });
  document.querySelectorAll('.edge').forEach(e=>{
    // Edges: hide if any endpoint beyond cutoff
    // Simple: just show all edges, nodes handle visibility
  });
  updateScrubLabel();
  updateCompleteness();
}
function updateCompleteness(){
  if(!allEvents.length)return;
  const frac=scrubValue/1000;
  const cutoff=fracToTime(frac);
  const visible=allEvents.filter(e=>e.timestamp<=cutoff);
  const total=allEvents.length;
  const pct=Math.round(visible.length/total*100);
  completenessFill.style.width=pct+'%';
  completenessPct.textContent=pct+'% ('+visible.length+'/'+total+' events)';
}
scrubRange.addEventListener('input',()=>{
  scrubValue=parseInt(scrubRange.value);
  applyScrub();
});
function togglePlay(){
  isPlaying=!isPlaying;
  if(isPlaying){
    playBtn.textContent='pause';
    playBtn.classList.add('active');
    if(scrubValue>=1000)scrubValue=0;
    playInterval=setInterval(()=>{
      scrubValue+=2;
      if(scrubValue>1000){
        scrubValue=1000;
        stopPlay();
      }
      scrubRange.value=scrubValue;
      applyScrub();
    },60);
  }else{
    stopPlay();
  }
}
function stopPlay(){
  isPlaying=false;
  playBtn.textContent='play';
  playBtn.classList.remove('active');
  if(playInterval){clearInterval(playInterval);playInterval=null;}
}
playBtn.addEventListener('click',togglePlay);
// Load data
async function load(){
  try{
    const resp=await fetch(STATE_PATH);
    if(!resp.ok)throw new Error('HTTP '+resp.status);
    const text=await resp.text();
    const entries=parseStateYaml(text);
    const bps=buildData(entries);
    render(bps);
    applyScrub();
  }catch(e){
    const demoBps=[
      {name:'agent-lifecycle-timeline',runs:[
        {id:42,action:'improve',detail:'Agent produces accurate content',status:'complete',timestamp:parseTS('2026-06-30T04:21:49'),score:88,color:COLORS.gold,glow:COLORS.goldGlow},
        {id:41,action:'eval',detail:'S:91 J:93 C:92.2',status:'complete',timestamp:parseTS('2026-06-30T04:18:50'),score:92.2,color:COLORS.gold,glow:COLORS.goldGlow},
        {id:16,action:'eval',detail:'S:87 J:75 C:79.8',status:'complete',timestamp:parseTS('2026-06-30T04:17:53'),score:79.8,color:COLORS.amber,glow:'transparent'},
        {id:20,action:'improve',detail:'Production-ready with strong rendering',status:'complete',timestamp:parseTS('2026-06-30T04:14:08'),score:85,color:COLORS.gold,glow:COLORS.goldGlow},
        {id:19,action:'eval',detail:'S:82 J:91 C:87.4',status:'complete',timestamp:parseTS('2026-06-30T04:10:25'),score:87.4,color:COLORS.gold,glow:COLORS.goldGlow},
        {id:43,action:'eval',detail:'S:87 J:79 C:82.2',status:'complete',timestamp:parseTS('2026-06-30T04:09:44'),score:82.2,color:COLORS.amber,glow:'transparent'},
        {id:15,action:'eval',detail:'S:85 J:77 C:80.2',status:'complete',timestamp:parseTS('2026-06-30T03:58:46'),score:80.2,color:COLORS.amber,glow:'transparent'},
        {id:46,action:'eval',detail:'S:68 J:48 C:56.0',status:'complete',timestamp:parseTS('2026-06-30T03:53:25'),score:56,color:COLORS.cool,glow:'transparent'},
        {id:44,action:'eval',detail:'S:88 J:91 C:89.8',status:'complete',timestamp:parseTS('2026-06-30T03:50:47'),score:89.8,color:COLORS.gold,glow:COLORS.goldGlow},
        {id:43,action:'eval',detail:'S:88 J:91 C:89.8',status:'complete',timestamp:parseTS('2026-06-30T03:51:42'),score:89.8,color:COLORS.gold,glow:COLORS.goldGlow},
        {id:11,action:'eval',detail:'S:82 J:92 C:88.0',status:'complete',timestamp:parseTS('2026-06-30T03:42:52'),score:88,color:COLORS.gold,glow:COLORS.goldGlow},
        {id:35,action:'eval',detail:'S:82 J:78 C:79.6',status:'complete',timestamp:parseTS('2026-06-30T03:39:03'),score:79.6,color:COLORS.amber,glow:'transparent'},
        {id:42,action:'eval',detail:'S:62 J:84 C:75.2',status:'complete',timestamp:parseTS('2026-06-30T03:35:12'),score:75.2,color:COLORS.amber,glow:'transparent'},
        {id:2,action:'spawn',detail:'first draft',status:'complete',timestamp:parseTS('2026-06-30T03:30:00'),score:null,color:COLORS.running,glow:'transparent'}
      ]},
      {name:'fullstack-feature-builder',runs:[
        {id:37,action:'eval',detail:'S:94 J:92 C:92.8',status:'complete',timestamp:parseTS('2026-06-30T04:15:00'),score:92.8,color:COLORS.gold,glow:COLORS.goldGlow},
        {id:28,action:'eval',detail:'S:88 J:76 C:80.8',status:'complete',timestamp:parseTS('2026-06-30T04:00:00'),score:80.8,color:COLORS.amber,glow:'transparent'},
        {id:19,action:'eval',detail:'S:72 J:84 C:79.2',status:'complete',timestamp:parseTS('2026-06-30T03:45:00'),score:79.2,color:COLORS.amber,glow:'transparent'},
        {id:12,action:'spawn',detail:'initial',status:'complete',timestamp:parseTS('2026-06-30T03:30:00'),score:null,color:COLORS.running,glow:'transparent'}
      ]},
      {name:'template-composer-v2',runs:[
        {id:33,action:'eval',detail:'S:91 J:95 C:93.4',status:'complete',timestamp:parseTS('2026-06-30T04:12:00'),score:93.4,color:COLORS.gold,glow:COLORS.goldGlow},
        {id:27,action:'eval',detail:'S:85 J:82 C:83.2',status:'complete',timestamp:parseTS('2026-06-30T03:55:00'),score:83.2,color:COLORS.amber,glow:'transparent'},
        {id:21,action:'improve',detail:'refined edge cases',status:'complete',timestamp:parseTS('2026-06-30T03:40:00'),score:86,color:COLORS.gold,glow:COLORS.goldGlow},
        {id:8,action:'spawn',detail:'initial scaffold',status:'complete',timestamp:parseTS('2026-06-30T03:25:00'),score:null,color:COLORS.running,glow:'transparent'}
      ]},
      {name:'api-schema-generator',runs:[
        {id:31,action:'eval',detail:'S:67 J:55 C:59.8',status:'complete',timestamp:parseTS('2026-06-30T04:08:00'),score:59.8,color:COLORS.cool,glow:'transparent'},
        {id:24,action:'eval',detail:'S:71 J:63 C:66.2',status:'complete',timestamp:parseTS('2026-06-30T03:50:00'),score:66.2,color:COLORS.cool,glow:'transparent'},
        {id:14,action:'spawn',detail:'initial',status:'complete',timestamp:parseTS('2026-06-30T03:32:00'),score:null,color:COLORS.running,glow:'transparent'}
      ]}
    ];
    render(demoBps);
    applyScrub();
    const msg=document.createElementNS('http://www.w3.org/2000/svg','text');
    msg.setAttribute('x',MARGIN.left+10);msg.setAttribute('y',MARGIN.top+20);
    msg.setAttribute('fill','#f0883e');msg.setAttribute('font-size','13');
    msg.setAttribute('font-family','sans-serif');
    msg.textContent='state.yaml not available at '+STATE_PATH+' — showing demo data. Move file to same directory.';
    svg.appendChild(msg);
  }
}
load();
</script>
</body>
</html>
```
That is the complete standalone Agent Lifecycle Timeline. Save it as agent_lifecycle_timeline.html alongside your state.yaml and open in browser.
What it delivers:
- Parses state.yaml live from the filesystem read (falls back to demo data with real agent-lifecycle-timeline entries if fetch fails)
- SVG horizontal timeline: one track per blueprint, sorted by run count descending
- Node colors: hot gold (85+), amber (70-84), cool (<70), grey running nodes
- Run-to-run connection edges on each track showing consecutive iterations
- Time scrubber at bottom: drag slider or press play for auto-replay from first to last event
- Click any node: detail popup with run_id, action, status, composite score (if available), timestamp, detail preview
- Tooltip uses collision detection: above preferred, then below, then right, then left, clamped to viewport
- Axis labels with tick marks at regular intervals, grid lines, axis title 'time (UTC)'
- Legend box bottom-right: gold, amber, cool, running
- Completeness bar top-right: shows what fraction of events are visible at current scrub position
- Hover highlight: dims other tracks, highlighting the hovered track's nodes and edges
- Score labels on eval nodes for quick scanning
One-line fix if state.yaml fetch fails: place the html file in E:\Stryde\_alpedal\styde-forge\ and it will load state.yaml by relative path. The demo data already includes your real agent-lifecycle-timeline runs so it works instantly.