```html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Agent Lifecycle Timeline</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0d1117;color:#c9d1d9;height:100vh;display:flex;flex-direction:column}
#header{display:flex;align-items:center;justify-content:space-between;padding:12px 24px;background:#161b22;border-bottom:1px solid #30363d;flex-shrink:0}
#header h1{font-size:18px;font-weight:600;color:#f0f6fc}
#header .sub{font-size:12px;color:#8b949e;margin-left:12px}
#status{display:flex;align-items:center;gap:8px;font-size:13px}
#status .dot{width:8px;height:8px;border-radius:50%;display:inline-block}
#status .dot.green{background:#3fb950}
#status .dot.yellow{background:#d29922}
#status .dot.red{background:#f85149}
#main{flex:1;display:flex;flex-direction:column;overflow:hidden}
#canvas-wrap{flex:1;overflow:auto;padding:16px 24px;position:relative}
#timeline-svg{width:100%;min-height:400px;display:block}
#controls{flex-shrink:0;background:#161b22;border-top:1px solid #30363d;padding:12px 24px;display:flex;align-items:center;gap:16px}
#scrub-wrap{flex:1;display:flex;align-items:center;gap:12px}
#scrub-wrap label{font-size:12px;color:#8b949e;white-space:nowrap}
#scrubber{flex:1;-webkit-appearance:none;appearance:none;height:4px;border-radius:2px;background:#30363d;outline:none;cursor:pointer}
#scrubber::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:14px;height:14px;border-radius:50%;background:#58a6ff;border:2px solid #1f6feb;cursor:pointer}
#scrubber::-moz-range-thumb{width:14px;height:14px;border-radius:50%;background:#58a6ff;border:2px solid #1f6feb;cursor:pointer}
#time-display{font-size:12px;color:#8b949e;min-width:160px;text-align:right;font-variant-numeric:tabular-nums}
#btn-play{background:none;border:1px solid #30363d;color:#c9d1d9;padding:4px 12px;border-radius:6px;cursor:pointer;font-size:13px;line-height:1.5}
#btn-play:hover{background:#21262d;border-color:#8b949e}
#btn-play.playing{background:#1f6feb;border-color:#1f6feb;color:#fff}
#legend{display:flex;gap:16px;align-items:center;font-size:11px;color:#8b949e}
#legend .swatch{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:4px;vertical-align:middle}
#legend .swatch.gold{background:#d29922}
#legend .swatch.amber{background:#d29922;opacity:.6}
#legend .swatch.cool{background:#58a6ff;opacity:.5}
#legend .swatch.stage-p{background:#3fb950}
#legend .swatch.stage-a{background:#f0883e}
#legend .swatch.stage-r{background:#8b949e}
#legend .swatch.stage-z{background:#f85149}
/* popup */
#popup{display:none;position:fixed;background:#1c2128;border:1px solid #30363d;border-radius:8px;padding:16px 20px;box-shadow:0 8px 24px rgba(0,0,0,.4);z-index:1000;min-width:280px;max-width:360px}
#popup.show{display:block}
#popup .close{float:right;background:none;border:none;color:#8b949e;cursor:pointer;font-size:16px;line-height:1}
#popup .close:hover{color:#f0f6fc}
#popup h3{font-size:14px;font-weight:600;color:#f0f6fc;margin-bottom:8px}
#popup table{width:100%;border-collapse:collapse;font-size:12px}
#popup td{padding:3px 6px;border-bottom:1px solid #21262d}
#popup td:first-child{color:#8b949e;width:80px}
#popup td:last-child{color:#c9d1d9;font-weight:500}
#popup .score-badge{display:inline-block;padding:1px 6px;border-radius:3px;font-size:11px;font-weight:600}
#popup .score-badge.gold{background:#d29922;color:#0d1117}
#popup .score-badge.amber{background:#d29922;color:#0d1117}
#popup .score-badge.cool{background:#58a6ff;color:#0d1117}
#popup .progress-bar{height:4px;border-radius:2px;background:#30363d;margin-top:6px;overflow:hidden}
#popup .progress-bar .fill{height:100%;border-radius:2px;transition:width .3s}
#loading{display:flex;align-items:center;justify-content:center;height:200px;flex-direction:column;gap:12px;color:#8b949e}
#loading .spinner{width:32px;height:32px;border:3px solid #30363d;border-top-color:#58a6ff;border-radius:50%;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
#error{display:none;align-items:center;justify-content:center;height:200px;flex-direction:column;gap:8px;color:#f85149}
#drop-zone{display:none;position:absolute;inset:0;background:rgba(13,17,23,.9);border:2px dashed #58a6ff;border-radius:8px;align-items:center;justify-content:center;flex-direction:column;gap:8px;z-index:500;color:#58a6ff;font-size:16px}
#drop-zone.show{display:flex}
#counts{font-size:12px;color:#8b949e;display:flex;gap:16px}
#counts span{white-space:nowrap}
#counts .num{color:#f0f6fc;font-weight:600}
.axis-label{fill:#8b949e;font-size:11px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
.track-label{fill:#f0f6fc;font-size:12px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;cursor:pointer}
.track-label:hover{fill:#58a6ff}
.node{cursor:pointer;transition:opacity .15s}
.node:hover{opacity:.8}
.node-label{font-size:10px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;text-anchor:middle;pointer-events:none}
.node-outline{fill:none;stroke:#30363d;stroke-width:1.5}
.grid-line{stroke:#21262d;stroke-width:1;stroke-dasharray:4,4}
.playhead{stroke:#f85149;stroke-width:2;pointer-events:none;transition:transform .1s}
</style>
</head>
<body>
<div id=header>
<div style=display:flex;align-items:center;gap:8px>
<h1>Agent Lifecycle Timeline</h1>
<span class=sub id=counts>blueprints: <span class=num id=count-bp>—</span> agents: <span class=num id=count-ag>—</span> runs: <span class=num id=count-run>—</span></span>
</div>
<div id=status>
<span class=dot id=status-dot></span>
<span id=status-text>laddar...</span>
</div>
</div>
<div id=main>
<div id=canvas-wrap>
<div id=loading>
<div class=spinner></div>
<span>Läser state.yaml...</span>
</div>
<div id=error>
<svg width=24 height=24 viewBox="0 0 24 24" fill=none stroke=currentColor stroke-width=2><circle cx=12 cy=12 r=10/><line x1=15 y1=9 x2=9 y2=15/><line x1=9 y1=9 x2=15 y2=15/></svg>
<span id=error-text></span>
</div>
<svg id=timeline-svg></svg>
<div id=drop-zone>
<svg width=48 height=48 viewBox="0 0 24 24" fill=none stroke=currentColor stroke-width=1.5><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1=12 y1=3 x2=12 y2=15/></svg>
<span>Släpp state.yaml här</span>
</div>
</div>
<div id=controls>
<div id=legend>
<span><span class=swatch gold></span>≥85 (produktion)</span>
<span><span class=swatch amber></span>70–84</span>
<span><span class=swatch cool></span>&lt;70</span>
</div>
<button id=btn-play title=Spela upp▶</button>
<div id=scrub-wrap>
<label for=scrubber>tid</label>
<input type=range id=scrubber min=0 max=100 value=0 step=1>
<span id=time-display>—</span>
</div>
</div>
</div>
<div id=popup>
<button class=close id=popup-close>✕</button>
<h3 id=popup-title></h3>
<table id=popup-body></table>
<div class=progress-bar><div class=fill id=popup-bar style=width:0%></div></div>
</div>
<script>
(function(){
const D=document;
const SVG=D.getElementById('timeline-svg');
const scrub=D.getElementById('scrubber');
const timeDisplay=D.getElementById('time-display');
const btnPlay=D.getElementById('btn-play');
const popup=D.getElementById('popup');
const popupTitle=D.getElementById('popup-title');
const popupBody=D.getElementById('popup-body');
const popupBar=D.getElementById('popup-bar');
const popupClose=D.getElementById('popup-close');
const statusDot=D.getElementById('status-dot');
const statusText=D.getElementById('status-text');
const loadingEl=D.getElementById('loading');
const errorEl=D.getElementById('error');
const errorText=D.getElementById('error-text');
const dropZone=D.getElementById('drop-zone');
const countBp=D.getElementById('count-bp');
const countAg=D.getElementById('count-ag');
const countRun=D.getElementById('count-run');
let state=null,blueprints=[],agents=[],runs=[];
let minT=Infinity,maxT=-Infinity;
let playing=false,playTimer=null;
let svgW=900,svgH=400;
const PAD=80,TRACK_H=48,TRACK_GAP=4,NODE_R=10;
popupClose.onclick=()=>popup.classList.remove('show');
D.addEventListener('click',e=>{if(!popup.contains(e.target)&&e.target.tagName!=='circle'&&e.target.tagName!=='text')popup.classList.remove('show')});
function setStatus(text,cls){statusText.textContent=text;statusDot.className='dot '+(cls||'yellow')}
function showError(msg){errorText.textContent=msg;errorEl.style.display='flex';loadingEl.style.display='none';setStatus('fel','red')}
function formatDate(ts){
  if(!ts)return'—';
  try{
    const d=new Date(ts);
    if(isNaN(d.getTime()))return ts;
    return d.toLocaleString('sv-SE',{year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit'});
  }catch(e){return ts}
}
function fmtShort(ts){
  if(!ts)return'—';
  try{
    const d=new Date(ts);
    if(isNaN(d.getTime()))return ts;
    return d.toLocaleDateString('sv-SE',{day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'});
  }catch(e){return ts}
}
// minimal YAML parser for the forge state.yaml format
function parseForgeYaml(text){
  const result={blueprints:{}};
  let currentBP=null,currentAgent=null,currentVer=null;
  const lines=text.split('\n');
  let i=0;
  function indent(s){let m=s.match(/^(\s*)/);return m?m[1].length:0}
  for(;i<lines.length;i++){
    const raw=lines[i];
    const trimmed=raw.trim();
    if(!trimmed||trimmed.startsWith('#'))continue;
    if(trimmed.startsWith('- '))continue;
    // skip list items
    if(/^-\s/.test(trimmed))continue;
    const id=indent(raw);
    const m=trimmed.match(/^([^:]+):\s*(.*)$/);
    if(!m)continue;
    const key=m[1].trim();
    let val=m[2].trim();
    if(id===0&&key==='blueprints'){
      // enter blueprints block
      continue;
    }
    if(id===2&&currentBP&&!currentAgent&&!currentVer){
      // blueprint level key
      if(val===''||val==='{}'||val==='{}}'){
        // enter agent if next line has key
        // read ahead
        continue;
      }
      // check if next line is indented further - if so, this is an agent name
      if(i+1<lines.length&&indent(lines[i+1])>id){
        currentAgent=key;
        if(!result.blueprints[currentBP].agents[currentAgent]){
          result.blueprints[currentBP].agents[currentAgent]={versions:{}};
        }
        continue;
      }
      continue;
    }
    // detect blueprint names at indent 2
    if(id===2&&!currentBP&&!currentAgent){
      // check context: we're under blueprints
      // check prev line
      let prevLine=i>0?lines[i-1].trim():'';
      if(prevLine==='blueprints:'||prevLine==='blueprints'||(i>1&&indent(lines[i-1])===0&&lines[i-1].trim()==='blueprints:')){
        currentBP=key;
        if(!result.blueprints[currentBP])result.blueprints[currentBP]={agents:{}};
        continue;
      }
      // check if we're still in blueprint section
      if(currentBP&&!val){
        // new blueprint
        currentBP=key;
        if(!result.blueprints[currentBP])result.blueprints[currentBP]={agents:{}};
        continue;
      }
    }
    // heuristic: if indent 2 and no val and we have a currentBP, it's an agent
    if(id===2&&currentBP&&!val){
      // could be agent name
      const nextLine=i+1<lines.length?lines[i+1]:'';
      if(nextLine&&indent(nextLine)>2){
        currentAgent=key;
        if(!result.blueprints[currentBP].agents[currentAgent]){
          result.blueprints[currentBP].agents[currentAgent]={versions:{}};
        }
        continue;
      }
    }
    // detect agent at indent 4
    if(id>=4&&currentBP&&!val){
      // lookahead: if next line is indented further, it's an agent key
      const nextLine=i+1<lines.length?lines[i+1]:'';
      if(nextLine&&indent(nextLine)>id){
        currentAgent=key;
        if(!result.blueprints[currentBP].agents[currentAgent]){
          result.blueprints[currentBP].agents[currentAgent]={versions:{}};
        }
        continue;
      }
    }
    // version numbers at indent 6/8
    if(id>=6&&currentBP&&currentAgent&&!val&&/^\d+$/.test(key)){
      currentVer=key;
      if(!result.blueprints[currentBP].agents[currentAgent].versions[currentVer]){
        result.blueprints[currentBP].agents[currentAgent].versions[currentVer]={};
      }
      continue;
    }
    // fields inside version (indent 8/10)
    if(id>=8&&currentBP&&currentAgent&&currentVer){
      const ver=result.blueprints[currentBP].agents[currentAgent].versions[currentVer];
      if(key==='stage')ver.stage=val;
      else if(key==='run_id')ver.run_id=val;
      else if(key==='created_at')ver.created_at=val;
      else if(key==='updated_at')ver.updated_at=val;
      else if(key==='score'||key==='scores'||key==='eval_score')ver.score=parseFloat(val)||0;
      else if(key==='composite'||key==='composite_score')ver.composite=parseFloat(val)||0;
      else if(key==='teacher_score')ver.teacher_score=parseFloat(val)||0;
      else if(key==='benchmark')ver.benchmark=val;
      else if(/^agent_version|version$/.test(key)&&!/^\d+$/.test(val))ver.agent_version=val;
      else if(key==='model')ver.model=val;
      else ver[key]=val;
      continue;
    }
    // if we see indent 0, reset nesting for blueprint context
    if(id===0&&key!=='blueprints'){
      if(currentBP){
        // check if this key is under a different root
        // reset
      }
    }
  }
  // second pass: more robust parsing using indentation tree
  // This first pass catches the basic structure
  return result;
}
function parseYamlRobust(text){
  const result={blueprints:{}};
  const lines=text.split('\n');
  const stack=[{name:'root',children:{},indent:-1}];
  let lastObj=result;
  function getParent(id){
    while(stack.length>1&&stack[stack.length-1].indent>=id)stack.pop();
    return stack[stack.length-1];
  }
  for(let i=0;i<lines.length;i++){
    const raw=lines[i];
    const trimmed=raw.trim();
    if(!trimmed||trimmed.startsWith('#')||trimmed.startsWith('---'))continue;
    const id=indent(raw);
    const m=trimmed.match(/^([^#:]+?):\s*(.*?)$/);
    if(!m)continue;
    const key=m[1].trim();
    let val=m[2].trim();
    // strip quotes
    if((val.startsWith('"')&&val.endsWith('"'))||(val.startsWith("'")&&val.endsWith("'"))){
      val=val.slice(1,-1);
    }
    const parent=stack[stack.length-1];
    const isScalar=val!==''&&val!=='{}'&&val!=='{}}'&&val!=='[]';
    const nextLine=i+1<lines.length?lines[i+1]:'';
    const hasChildren=nextLine&&indent(nextLine)>id;
    if(hasChildren){
      const node={children:{}};
      parent.children[key]=node;
      stack.push({name:key,children:node.children,indent:id});
    }else if(isScalar){
      parent.children[key]=val;
    }else{
      parent.children[key]={};
    }
  }
  // convert stack tree to our format
  function walk(node,bp,agent,ver){
    if(typeof node==='string')return;
    if(node.children){
      for(const k of Object.keys(node.children)){
        const v=node.children[k];
        // blueprint root: keys under blueprints
        if(k==='blueprints')continue;
        if(!bp&&!agent&&!ver){
          // try to determine what k is based on context
          // look at parent context
          continue;
        }
        if(bp&&!agent&&!ver){
          // agent or bp-level field
          if(typeof v==='object'&&!Array.isArray(v)){
            result.blueprints[bp].agents[k]={versions:{}};
            walk(v,bp,k,null);
          }else{
            result.blueprints[bp][k]=v;
          }
        }else if(bp&&agent&&!ver){
          if(/^\d+$/.test(k)){
            result.blueprints[bp].agents[agent].versions[k]={};
            walk(v,bp,agent,k);
          }else if(typeof v==='object'){
            result.blueprints[bp].agents[agent][k]=v;
          }else{
            result.blueprints[bp].agents[agent][k]=v;
          }
        }else if(bp&&agent&&ver){
          const o=result.blueprints[bp].agents[agent].versions[ver];
          if(k==='score'||k==='eval_score'||k==='composite'||k==='composite_score')o.score=parseFloat(v)||0;
          else if(k==='stage')o.stage=String(v);
          else if(k==='run_id')o.run_id=String(v);
          else if(k==='created_at')o.created_at=String(v);
          else if(k==='updated_at')o.updated_at=String(v);
          else if(k==='teacher_score')o.teacher_score=parseFloat(v)||0;
          else if(k==='benchmark')o.benchmark=String(v);
          else if(k==='model')o.model=String(v);
          else o[k]=v;
        }
      }
    }
  }
  // manually find blueprints section
  let inBp=false;
  let currentBpName=null;
  let currentAgName=null;
  let currentVerName=null;
  for(let i=0;i<lines.length;i++){
    const raw=lines[i];
    const trimmed=raw.trim();
    if(!trimmed||trimmed.startsWith('#')||trimmed.startsWith('---'))continue;
    const id=indent(raw);
    const m=trimmed.match(/^([^#:]+?):\s*(.*?)$/);
    if(!m)continue;
    const key=m[1].trim();
    let val=m[2].trim();
    if((val.startsWith('"')&&val.endsWith('"'))||(val.startsWith("'")&&val.endsWith("'")))val=val.slice(1,-1);
    if(id===0&&key==='blueprints'){inBp=true;continue}
    if(id===0&&key!=='blueprints'){inBp=false;continue}
    if(!inBp)continue;
    const nextLine=i+1<lines.length?lines[i+1]:'';
    const hasChildren=nextLine&&indent(nextLine)>id;
    if(id===2){
      // blueprint name
      currentBpName=key;
      if(!result.blueprints[currentBpName])result.blueprints[currentBpName]={agents:{}};
      result.blueprints[currentBpName]._name=key;
      currentAgName=null;currentVerName=null;
      // check if next line has a scalar field instead of agent
    }else if(id>2&&currentBpName){
      // could be agent name or field
      if(hasChildren||(!val&&hasChildren)){
        currentAgName=key;
        if(!result.blueprints[currentBpName].agents[currentAgName]){
          result.blueprints[currentBpName].agents[currentAgName]={versions:{}};
        }
        currentVerName=null;
      }else if(id>=6&&currentAgName&&/^\d+$/.test(key)){
        currentVerName=key;
        if(!result.blueprints[currentBpName].agents[currentAgName].versions[currentVerName]){
          result.blueprints[currentBpName].agents[currentAgName].versions[currentVerName]={};
        }
      }else if(id>=8&&currentAgName&&currentVerName){
        const o=result.blueprints[currentBpName].agents[currentAgName].versions[currentVerName];
        if(key==='score'||key==='eval_score'||key==='composite'||key==='composite_score')o.score=parseFloat(val)||0;
        else if(key==='stage')o.stage=String(val);
        else if(key==='run_id')o.run_id=String(val);
        else if(key==='created_at')o.created_at=String(val);
        else if(key==='updated_at')o.updated_at=String(val);
        else if(key==='teacher_score')o.teacher_score=parseFloat(val)||0;
        else if(key==='benchmark')o.benchmark=String(val);
        else if(key==='model')o.model=String(val);
        else o[key]=val;
      }else if(currentAgName&&!currentVerName){
        // field at agent level
        const ag=result.blueprints[currentBpName].agents[currentAgName];
        ag[key]=val;
      }
    }
  }
  return result;
}
function indent(s){let m=s.match(/^(\s*)/);return m?m[1].length:0}
function scoreColor(s){
  const sc=parseFloat(s);
  if(isNaN(sc))return'#8b949e';
  if(sc>=85)return'#d29922';
  if(sc>=70)return'#cc8833';
  return'#58a6ff';
}
function scoreClass(s){
  const sc=parseFloat(s);
  if(isNaN(sc))return'cool';
  if(sc>=85)return'gold';
  if(sc>=70)return'amber';
  return'cool';
}
function flattenState(data){
  const bps=[],ags=[],rns=[];
  for(const bpName of Object.keys(data.blueprints||{})){
    const bp=data.blueprints[bpName];
    if(!bp||!bp.agents)continue;
    bps.push(bpName);
    for(const agName of Object.keys(bp.agents)){
      const ag=bp.agents[agName];
      if(!ag||!ag.versions)continue;
      ags.push({blueprint:bpName,name:agName});
      for(const ver of Object.keys(ag.versions)){
        const v=ag.versions[ver];
        if(!v)continue;
        const ts=v.created_at||v.updated_at;
        if(ts){
          const d=new Date(ts);
          if(!isNaN(d.getTime())){
            if(d<minT)minT=d;
            if(d>maxT)maxT=d;
          }
        }
        rns.push({
          blueprint:bpName,
          agent:agName,
          version:ver,
          run_id:v.run_id,
          stage:v.stage||'refinery',
          score:parseFloat(v.score)||0,
          composite:parseFloat(v.composite)||v.score,
          benchmark:v.benchmark,
          model:v.model,
          times:ts,
          created_at:v.created_at,
          updated_at:v.updated_at
        });
      }
    }
  }
  return {blueprints:bps,agents:ags,runs:rns};
}
function renderTimeline(timePos){
  // timePos: 0..1 fraction through the timeline
  const wrap=D.getElementById('canvas-wrap');
  const rect=wrap.getBoundingClientRect();
  svgW=Math.max(rect.width-40,600);
  svgH=Math.max(blueprints.length*(TRACK_H+TRACK_GAP)+PAD+60,300);
  SVG.setAttribute('viewBox',`0 0 ${svgW} ${svgH}`);
  SVG.setAttribute('width','100%');
  SVG.setAttribute('height',svgH);
  const timeRange=maxT-minT||1;
  const cutTime=minT+timeRange*timePos;
  const x0=PAD+20;
  const x1=svgW-40;
  const timeW=x1-x0;
  let html='';
  // grid lines
  const numGrid=Math.min(10,Math.ceil(timeRange/60000));
  for(let i=0;i<=numGrid;i++){
    const f=i/numGrid;
    const x=x0+f*timeW;
    const t=new Date(minT+f*timeRange);
    html+=`<line class=grid-line x1=${x} y1=${PAD-20} x2=${x} y2=${svgH-20}/>`;
    html+=`<text class=axis-label x=${x} y=${PAD-25} text-anchor=middle>${fmtShort(t)}</text>`;
  }
  // tracks per blueprint
  const sortedBps=[...blueprints].sort((a,b)=>a.localeCompare(b));
  const bpMap={};
  sortedBps.forEach((bp,i)=>{bpMap[bp]=i});
  // playhead
  const playheadX=x0+timeW*timePos;
  html+=`<line class=playhead x1=${playheadX} y1=${PAD-20} x2=${playheadX} y2=${svgH-20}/>`;
  sortedBps.forEach((bpName,i)=>{
    const yBase=PAD+i*(TRACK_H+TRACK_GAP);
    const midY=yBase+TRACK_H/2;
    // track bg
    html+=`<rect x=${x0-4} y=${yBase} width=${timeW+8} height=${TRACK_H} fill=${i%2===0?'#161b22':'#0d1117'} rx=4/>`;
    // label
    const shortName=bpName.length>25?bpName.slice(0,22)+'...':bpName;
    html+=`<text class=track-label x=${x0-12} y=${midY+4} text-anchor=end>${shortName.replace(/&/g,'&amp;').replace(/</g,'&lt;')}</text>`;
    // filter runs visible at this time position
    const bpRuns=runs.filter(r=>r.blueprint===bpName);
    let visibleNodes=0;
    bpRuns.forEach(r=>{
      const ts=r.created_at||r.updated_at;
      if(!ts)return;
      const d=new Date(ts);
      if(isNaN(d.getTime()))return;
      // only show if within cut time
      if(d>cutTime)return;
      visibleNodes++;
      const f=(d-minT)/timeRange;
      const cx=x0+f*timeW;
      const cy=midY;
      const col=scoreColor(r.score);
      const cls=scoreClass(r.score);
      const rad=Math.max(NODE_R-2,Math.min(NODE_R+4,NODE_R+r.score/30));
      const title=`${r.agent} v${r.version} (${r.score})`;
      html+=`<circle class=node data-bp='${bpName.replace(/'/g,"\\'")}' data-ag='${r.agent.replace(/'/g,"\\'")}' data-ver='${r.version}' cx=${cx} cy=${cy} r=${rad} fill=${col} stroke=${col} stroke-width=2 opacity=.85/>`;
      html+=`<circle class=node-outline cx=${cx} cy=${cy} r=${rad+2}/>`;
      // show score label if space
      if(timeW>300){
        html+=`<text class=node-label fill=${col==='#58a6ff'?'#fff':'#0d1117'} x=${cx} y=${cy+3.5} font-weight=600>${r.score}</text>`;
      }
    });
  });
  // axis label
  html+=`<text class=axis-label x=${x0+timeW/2} y=${svgH-6} text-anchor=middle>tid →</text>`;
  SVG.innerHTML=html;
  // event delegation for click
  SVG.querySelectorAll('.node').forEach(el=>{
    el.addEventListener('click',function(e){
      e.stopPropagation();
      const bp=this.dataset.bp;
      const ag=this.dataset.ag;
      const ver=this.dataset.ver;
      const r=runs.find(x=>x.blueprint===bp&&x.agent===ag&&x.version===ver);
      if(!r)return;
      showPopup(e,r);
    });
  });
  // update counts
  const visibleCount=runs.filter(r=>{
    const ts=r.created_at||r.updated_at;
    if(!ts)return false;
    return new Date(ts)<=cutTime;
  }).length;
}
function showPopup(e,run){
  const rect=e.target.getBoundingClientRect();
  popupTitle.textContent=`${run.blueprint} / ${run.agent} v${run.version}`;
  const s=parseFloat(run.score)||0;
  const cls=scoreClass(s);
  const html=`<tr><td>Score</td><td><span class="score-badge ${cls}">${s}</span></td></tr>
<tr><td>Stage</td><td>${run.stage||'—'}</td></tr>
<tr><td>Run ID</td><td style=font-size:10px;font-family:monospace>${run.run_id||'—'}</td></tr>
<tr><td>Skapad</td><td>${formatDate(run.created_at)}</td></tr>
<tr><td>Uppdaterad</td><td>${formatDate(run.updated_at)}</td></tr>
<tr><td>Benchmark</td><td>${run.benchmark||'—'}</td></tr>
<tr><td>Model</td><td>${run.model||'—'}</td></tr>`;
  popupBody.innerHTML=html;
  popupBar.style.width=(s||0)+'%';
  popupBar.style.background=scoreColor(s);
  popup.style.left=Math.min(rect.left+20,window.innerWidth-380)+'px';
  popup.style.top=Math.max(10,Math.min(rect.top-20,window.innerHeight-320))+'px';
  popup.classList.add('show');
}
function onData(data){
  loadingEl.style.display='none';
  errorEl.style.display='none';
  const parsed=parseYamlRobust(data);
  const flat=flattenState(parsed);
  blueprints=flat.blueprints;
  agents=flat.agents;
  runs=flat.runs;
  if(runs.length===0){
    showError('Inga agent-runs hittades i state.yaml. Kontrollera formatet.');
    return;
  }
  countBp.textContent=blueprints.length;
  countAg.textContent=agents.length;
  countRun.textContent=runs.length;
  setStatus(`${runs.length} runs, ${blueprints.length} blueprints`,'green');
  // sort runs by time
  runs.sort((a,b)=>{
    const ta=a.created_at||a.updated_at||'';
    const tb=b.created_at||b.updated_at||'';
    return ta.localeCompare(tb);
  });
  // set scrubber max
  scrub.max=100;
  scrub.value=0;
  renderTimeline(0);
  updateTimeDisplay(0);
}
function updateTimeDisplay(f){
  const t=new Date(minT+(maxT-minT)*f);
  timeDisplay.textContent=t.toLocaleString('sv-SE',{
    year:'numeric',month:'2-digit',day:'2-digit',
    hour:'2-digit',minute:'2-digit',second:'2-digit'
  });
}
function onScrub(){
  const f=parseInt(scrub.value)/100;
  renderTimeline(f);
  updateTimeDisplay(f);
}
scrub.addEventListener('input',onScrub);
btnPlay.onclick=function(){
  playing=!playing;
  btnPlay.textContent=playing?'⏸':'▶';
  btnPlay.classList.toggle('playing',playing);
  if(playing){
    if(parseInt(scrub.value)>=100)scrub.value=0;
    playTimer=setInterval(()=>{
      let v=parseInt(scrub.value)+1;
      if(v>100){v=100;playing=false;btnPlay.textContent='▶';btnPlay.classList.remove('playing');clearInterval(playTimer)}
      scrub.value=v;
      onScrub();
    },120);
  }else{
    clearInterval(playTimer);
  }
};
function loadStateYaml(){
  fetch('state.yaml')
    .then(r=>{
      if(!r.ok)throw new Error(`HTTP ${r.status}: ${r.statusText}`);
      return r.text();
    })
    .then(text=>{
      onData(text);
    })
    .catch(err=>{
      // try GET with ?t param for cache busting
      fetch('state.yaml?'+Date.now())
        .then(r=>{
          if(!r.ok)throw new Error(`HTTP ${r.status}`);
          return r.text();
        })
        .then(text=>onData(text))
        .catch(err2=>{
          showError('Kunde inte ladda state.yaml. Dra & släpp filen här istället. ('+err.message+')');
          dropZone.classList.add('show');
        });
    });
}
// drag and drop support
let dragCounter=0;
D.addEventListener('dragover',e=>{e.preventDefault();e.dataTransfer.dropEffect='copy';dropZone.classList.add('show')});
D.addEventListener('dragleave',e=>{e.preventDefault();dragCounter--;if(dragCounter<=0){dropZone.classList.remove('show');dragCounter=0}});
D.addEventListener('dragenter',e=>{e.preventDefault();dragCounter++});
D.addEventListener('drop',e=>{
  e.preventDefault();
  dropZone.classList.remove('show');
  dragCounter=0;
  const file=e.dataTransfer.files[0];
  if(!file)return;
  const reader=new FileReader();
  reader.onload=function(ev){
    onData(ev.target.result);
  };
  reader.onerror=function(){showError('Kunde inte läsa filen.');};
  reader.readAsText(file);
});
// init
loadStateYaml();
// resize handler
let resizeTimer;
window.addEventListener('resize',()=>{
  clearTimeout(resizeTimer);
  resizeTimer=setTimeout(()=>{
    const f=parseInt(scrub.value)/100;
    renderTimeline(f);
  },150);
});
})();
</script>
</body>
</html>
```