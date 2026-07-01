Här är den kompletta Agent Lifecycle Timeline — en interaktiv SVG-timeline som läser state.yaml-data, renderar tracks per blueprint, färgkodar noder efter score, och har time scrubber med auto-play.
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
.header{padding:16px 24px 8px;border-bottom:1px solid #30363d}
.header h1{font-size:20px;font-weight:600;color:#f0f6fc}
.header .sub{font-size:12px;color:#8b949e;margin-top:2px}
.timeline-container{position:relative;padding:12px 24px 60px}
.tracks{position:relative}
.track{position:relative;height:40px;margin-bottom:2px;display:flex;align-items:center}
.track-label{width:220px;font-size:11px;color:#8b949e;text-align:right;padding-right:12px;flex-shrink:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;cursor:pointer}
.track-label:hover{color:#f0f6fc}
.track-svg{flex:1;height:40px;overflow:visible}
.track-bg{fill:#161b22;rx:3}
.timeline-header{display:flex;align-items:center;margin-bottom:8px;gap:12px;padding-left:232px}
.controls{display:flex;align-items:center;gap:8px}
.controls button{background:#21262d;border:1px solid #30363d;color:#c9d1d9;padding:4px 12px;border-radius:6px;cursor:pointer;font-size:12px}
.controls button:hover{background:#30363d}
.controls button.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
.slider-wrap{flex:1;display:flex;align-items:center;gap:8px}
.slider-wrap input[type=range]{flex:1;accent-color:#1f6feb;height:4px;cursor:pointer}
.time-label{font-size:11px;color:#8b949e;min-width:140px;text-align:right}
.legend{display:flex;gap:16px;margin-top:8px;padding-left:232px;font-size:11px;color:#8b949e}
.legend span{display:flex;align-items:center;gap:4px}
.legend .dot{width:10px;height:10px;border-radius:50%;display:inline-block}
.dot.gold{background:#d29922}
.dot.amber{background:#d2992288}
.dot.cool{background:#58a6ff}
.time-marker{position:absolute;top:0;bottom:0;width:2px;background:#1f6feb;pointer-events:none;opacity:0.6;z-index:5}
.modal{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px;z-index:100;min-width:300px;max-width:420px;box-shadow:0 8px 32px rgba(0,0,0,0.5)}
.modal.show{display:block}
.modal h3{font-size:16px;margin-bottom:8px;color:#f0f6fc}
.modal .row{display:flex;justify-content:space-between;padding:3px 0;font-size:13px;border-bottom:1px solid #21262d}
.modal .row:last-child{border-bottom:none}
.modal .label{color:#8b949e}
.modal .val{color:#c9d1d9;font-weight:500}
.modal .val.gold{color:#d29922}
.modal .val.amber{color:#d2992288}
.modal .val.cool{color:#58a6ff}
.modal-close{position:absolute;top:8px;right:12px;background:none;border:none;color:#8b949e;cursor:pointer;font-size:18px}
.modal-close:hover{color:#f0f6fc}
.overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);z-index:99}
.overlay.show{display:block}
.stats{display:flex;gap:16px;padding-left:232px;font-size:11px;color:#8b949e;margin-top:4px;margin-bottom:8px}
.stats span{color:#c9d1d9;font-weight:600}
</style>
</head>
<body>
<div class="header">
  <h1>Agent Lifecycle Timeline</h1>
  <div class="sub">Styde Forge — spåra varje spawn/eval/improve/promote-cykel</div>
</div>
<div class="timeline-container">
  <div class="timeline-header">
    <div class="controls">
      <button id="playBtn" title="Spela upp från början">Play</button>
      <button id="resetBtn" title="Återställ">Reset</button>
    </div>
    <div class="slider-wrap">
      <input type="range" id="timeSlider" min="0" max="100" value="100" step="1">
      <span class="time-label" id="timeLabel">Alla händelser</span>
    </div>
  </div>
  <div class="stats" id="statsBar"></div>
  <div class="legend">
    <span><span class="dot gold"></span> Production (85+)</span>
    <span><span class="dot amber"></span> Refinery (70-84)</span>
    <span><span class="dot cool"></span> Training (&lt;70)</span>
  </div>
  <div class="tracks" id="tracks"></div>
  <div class="time-marker" id="timeMarker" style="display:none"></div>
</div>
<div class="overlay" id="overlay"></div>
<div class="modal" id="modal">
  <button class="modal-close" id="modalClose">&times;</button>
  <h3 id="modalTitle">Agent</h3>
  <div id="modalBody"></div>
</div>
<script>
// ====================================================================
// DATA — extracted from state.yaml
// ====================================================================
const RAW_EVENTS = [
  {bp:"3d-data-terrain-explorer",act:"eval",id:"178",ts:"2026-06-30T00:41:41Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"176",ts:"2026-06-30T00:24:12Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"174",ts:"2026-06-30T00:07:48Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"172",ts:"2026-06-29T23:51:22Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"170",ts:"2026-06-29T23:34:55Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"168",ts:"2026-06-29T23:18:28Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"166",ts:"2026-06-29T23:01:59Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"164",ts:"2026-06-29T22:45:29Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"162",ts:"2026-06-29T22:29:01Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"160",ts:"2026-06-29T22:12:30Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"158",ts:"2026-06-29T21:55:59Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"156",ts:"2026-06-29T21:39:30Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"154",ts:"2026-06-29T21:23:16Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"152",ts:"2026-06-29T21:06:49Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"150",ts:"2026-06-29T20:50:20Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"148",ts:"2026-06-29T20:33:52Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"146",ts:"2026-06-29T20:17:11Z",score:95.2},
  {bp:"3d-data-terrain-explorer",act:"eval",id:"144",ts:"2026-06-29T20:00:42Z",score:95.2},
  {bp:"aesthetic-style-composer",act:"eval",id:"19",ts:"2026-06-30T02:47:58Z",score:87.4,detail:"Produktionsklar spec (88.8)"},
  {bp:"aesthetic-style-composer",act:"eval",id:"19",ts:"2026-06-30T02:26:53Z",score:85.4},
  {bp:"aesthetic-style-composer",act:"eval",id:"22",ts:"2026-06-29T21:43:06Z",score:87.4,detail:"Production-ready spec"},
  {bp:"aesthetic-style-composer",act:"eval",id:"4",ts:"2026-06-30T02:12:30Z",score:81.0},
  {bp:"aesthetic-style-composer",act:"eval",id:"4",ts:"2026-06-30T02:11:53Z",score:81.0},
  {bp:"aesthetic-style-composer",act:"eval",id:"12",ts:"2026-06-29T21:19:16Z",score:70.8},
  {bp:"aesthetic-style-composer",act:"eval",id:"16",ts:"2026-06-30T02:45:21Z",score:72.8},
  {bp:"aesthetic-style-composer",act:"eval",id:"13",ts:"2026-06-30T02:37:37Z",score:79.2,detail:"47009 chars"},
  {bp:"aesthetic-style-composer",act:"eval",id:"11",ts:"2026-06-29T21:16:54Z",score:63.6},
  {bp:"agent-lifecycle-timeline",act:"eval",id:"35",ts:"2026-06-30T03:00:41Z",score:74.2},
  {bp:"agent-lifecycle-timeline",act:"eval",id:"27",ts:"2026-06-30T03:26:46Z",score:84.2,detail:"S:15 J:38 C:28.8"},
  {bp:"agent-lifecycle-timeline",act:"eval",id:"29",ts:"2026-06-30T03:21:54Z",score:86.8,detail:"16372 chars"},
  {bp:"agent-lifecycle-timeline",act:"eval",id:"19",ts:"2026-06-30T02:51:44Z",score:86.0},
  {bp:"agent-lifecycle-timeline",act:"eval",id:"9",ts:"2026-06-30T02:18:35Z",score:28.0},
  {bp:"agent-lifecycle-timeline",act:"eval",id:"7",ts:"2026-06-30T02:19:10Z",score:28.0},
  {bp:"agent-lifecycle-timeline",act:"eval",id:"3",ts:"2026-06-30T02:13:04Z",score:81.0},
  {bp:"agent-lifecycle-timeline",act:"eval",id:"2",ts:"2026-06-29T23:15:15Z",score:88.4},
  {bp:"agent-promotion-evaluator",act:"eval",id:"26",ts:"2026-06-29T21:27:48Z",score:91.6},
  {bp:"agent-promotion-evaluator",act:"eval",id:"7",ts:"2026-06-29T21:14:20Z",score:80.8,detail:"Agent fails at usefulness"},
  {bp:"agent-promotion-evaluator",act:"eval",id:"26",ts:"2026-06-29T21:27:48Z",score:80.8},
  {bp:"agent-promotion-evaluator",act:"eval",id:"2",ts:"2026-06-29T21:04:49Z",score:39.2},
  {bp:"agent-promotion-evaluator",act:"eval",id:"2",ts:"2026-06-29T21:04:49Z",score:93.6,detail:"Exceptional"},
  {bp:"ai-copilot-query-panel",act:"eval",id:"32",ts:"2026-06-30T03:17:19Z",score:57.8},
  {bp:"ai-copilot-query-panel",act:"eval",id:"27",ts:"2026-06-30T02:38:21Z",score:79.0},
  {bp:"ai-copilot-query-panel",act:"eval",id:"18",ts:"2026-06-30T02:52:21Z",score:86.0},
  {bp:"ai-copilot-query-panel",act:"eval",id:"30",ts:"2026-06-29T21:30:44Z",score:79.8},
  {bp:"animation-design-engineer",act:"eval",id:"48",ts:"2026-06-30T03:09:51Z",score:27.0},
  {bp:"animation-design-engineer",act:"eval",id:"37",ts:"2026-06-30T02:57:01Z",score:14.0},
  {bp:"animation-design-engineer",act:"eval",id:"3",ts:"2026-06-30T02:34:38Z",score:55.2},
  {bp:"anomaly-detection-visualizer",act:"eval",id:"6",ts:"2026-06-30T02:35:14Z",score:56.8},
  {bp:"caveman-mode-enforcer",act:"eval",id:"45",ts:"2026-06-29T22:21:22Z",score:86.8},
  {bp:"clay-soft-interface-designer",act:"eval",id:"17",ts:"2026-06-30T02:44:36Z",score:88.8},
  {bp:"clay-soft-interface-designer",act:"eval",id:"18",ts:"2026-06-29T21:41:08Z",score:84.0},
  {bp:"color-palette-originator",act:"eval",id:"26",ts:"2026-06-30T03:27:23Z",score:85.6,detail:"S:15 J:38 C:28.8"},
  {bp:"color-palette-originator",act:"eval",id:"33",ts:"2026-06-30T03:25:32Z",score:90.2,detail:"15075 chars"},
  {bp:"customer-feedback-analyzer",act:"eval",id:"78",ts:"2026-06-29T22:36:11Z",score:51.2},
  {bp:"customer-service-triage",act:"eval",id:"62",ts:"2026-06-29T22:27:52Z",score:64.0},
  {bp:"customer-service-triage",act:"eval",id:"61",ts:"2026-06-29T22:28:26Z",score:64.0},
  {bp:"customer-service-triage",act:"eval",id:"42",ts:"2026-06-29T22:20:44Z",score:80.6},
  {bp:"dao-governance-designer",act:"eval",id:"9",ts:"2026-06-29T21:36:53Z",score:86.6},
  {bp:"dao-governance-designer",act:"eval",id:"6",ts:"2026-06-29T21:37:28Z",score:86.6},
  {bp:"data-cleaner",act:"eval",id:"9",ts:"2026-06-29T22:00:17Z",score:63.6},
  {bp:"data-cleaner",act:"eval",id:"23",ts:"2026-06-30T02:56:53Z",score:86.6},
  {bp:"gpu-monitor-visualizer",act:"eval",id:"7",ts:"2026-06-29T21:36:21Z",score:90.0},
  {bp:"gpu-monitor-visualizer",act:"eval",id:"20",ts:"2026-06-29T22:08:34Z",score:70.0,detail:"Agent produces accurate but hollow greeting"},
  {bp:"observability-platform-builder",act:"eval",id:"126",ts:"2026-06-29T22:51:41Z",score:79.6},
  {bp:"observability-platform-builder",act:"eval",id:"116",ts:"2026-06-29T22:48:51Z",score:79.6},
  {bp:"observability-platform-builder",act:"eval",id:"105",ts:"2026-06-29T22:45:23Z",score:79.6},
  {bp:"observability-platform-builder",act:"eval",id:"103",ts:"2026-06-29T22:45:58Z",score:79.6},
  {bp:"observability-platform-builder",act:"eval",id:"94",ts:"2026-06-29T22:41:57Z",score:79.6},
  {bp:"observability-platform-builder",act:"eval",id:"91",ts:"2026-06-29T22:42:33Z",score:79.6},
  {bp:"observability-platform-builder",act:"eval",id:"85",ts:"2026-06-29T22:38:36Z",score:79.6},
  {bp:"observability-platform-builder",act:"eval",id:"84",ts:"2026-06-29T22:39:09Z",score:79.6},
  {bp:"observability-platform-builder",act:"eval",id:"73",ts:"2026-06-29T22:34:26Z",score:79.6},
  {bp:"observability-platform-builder",act:"eval",id:"70",ts:"2026-06-29T22:34:59Z",score:79.6},
  {bp:"sprint-coach",act:"eval",id:"127",ts:"2026-06-29T22:52:16Z",score:80.0},
  {bp:"sprint-coach",act:"eval",id:"50",ts:"2026-06-29T22:23:12Z",score:84.0},
  {bp:"sprint-coach",act:"eval",id:"38",ts:"2026-06-29T22:19:00Z",score:79.2},
  {bp:"sprint-coach",act:"eval",id:"36",ts:"2026-06-29T22:19:36Z",score:79.2},
  {bp:"sprint-coach",act:"eval",id:"31",ts:"2026-06-30T03:14:07Z",score:90.2},
  {bp:"sprint-coach",act:"eval",id:"28",ts:"2026-06-29T22:12:23Z",score:74.6},
  {bp:"sprint-coach",act:"eval",id:"18",ts:"2026-06-29T22:04:40Z",score:83.8},
  {bp:"sprint-coach",act:"eval",id:"3",ts:"2026-06-29T21:07:47Z",score:14.0}
];
// ====================================================================
// Process events
// ====================================================================
function scoreColor(s){return s>=85?'gold':s>=70?'amber':'cool'}
function scoreHex(s){return s>=85?'#d29922':s>=70?'#d2992288':'#58a6ff'}
// Sort by timestamp
const events = RAW_EVENTS.map(e=>({...e,tsObj:new Date(e.ts+'Z')}))
events.sort((a,b)=>a.tsObj-b.tsObj)
const tMin = events[0].tsObj.getTime()
const tMax = events[events.length-1].tsObj.getTime()
const tRange = tMax - tMin || 1
function pct(t){return((t-tMin)/tRange)*100}
// Group by blueprint, preserve order by first appearance
const bpOrder=[]
const bpMap={}
for(const e of events){
  if(!bpMap[e.bp]){bpMap[e.bp]=[];bpOrder.push(e.bp)}
  bpMap[e.bp].push(e)
}
// ====================================================================
// Render
// ====================================================================
const tracksEl=document.getElementById('tracks')
const SVG_NS='http://www.w3.org/2000/svg'
const TRACK_H=36
const LEFT_MARGIN=0
const RIGHT_MARGIN=20
const NODE_R=6
const NODE_R_BIG=8
let svgW=0
function render(sliderPct){
  const cutTime = tMin + (tRange * sliderPct / 100)
  tracksEl.innerHTML=''
  const containerW = tracksEl.clientWidth||1200
  svgW=containerW-240
  if(svgW<200)svgW=200
  const chartW=svgW-LEFT_MARGIN-RIGHT_MARGIN
  let totalH=bpOrder.length*TRACK_H
  // Stats
  let prodCount=0, refCount=0, trainCount=0
  for(const bp of bpOrder){
    const e=bpMap[bp]
    const visible=e.filter(x=>x.tsObj<=cutTime)
    if(visible.length===0)continue
    const last=visible[visible.length-1]
    if(last.score>=85)prodCount++
    else if(last.score>=70)refCount++
    else trainCount++
  }
  document.getElementById('statsBar').innerHTML=
    `Blueprint: <span>${bpOrder.length}</span> &middot; `+
    `Production: <span>${prodCount}</span> &middot; `+
    `Refinery: <span>${refCount}</span> &middot; `+
    `Training: <span>${trainCount}</span>`
  for(let bi=0;bi<bpOrder.length;bi++){
    const bp=bpOrder[bi]
    const evts=bpMap[bp].filter(e=>e.tsObj<=cutTime)
    const trackDiv=document.createElement('div')
    trackDiv.className='track'
    const label=document.createElement('div')
    label.className='track-label'
    label.textContent=bp
    label.title=`${bp} — ${evts.length} eval(s)`
    trackDiv.appendChild(label)
    const svg=document.createElementNS(SVG_NS,'svg')
    svg.setAttribute('class','track-svg')
    svg.setAttribute('viewBox',`0 0 ${svgW} ${TRACK_H}`)
    svg.setAttribute('preserveAspectRatio','none')
    // background bar
    const bg=document.createElementNS(SVG_NS,'rect')
    bg.setAttribute('x','0');bg.setAttribute('y','10')
    bg.setAttribute('width',svgW);bg.setAttribute('height','16')
    bg.setAttribute('rx','8');bg.setAttribute('fill','#161b22')
    svg.appendChild(bg)
    // nodes
    for(let ei=0;ei<evts.length;ei++){
      const e=evts[ei]
      const px=LEFT_MARGIN + (pct(e.tsObj.getTime())/100)*chartW
      const isLast=ei===evts.length-1
      const r=isLast?NODE_R_BIG:NODE_R
      const col=scoreColor(e.score)
      const fill=scoreHex(e.score)
      const circle=document.createElementNS(SVG_NS,'circle')
      circle.setAttribute('cx',px);circle.setAttribute('cy','18')
      circle.setAttribute('r',r)
      circle.setAttribute('fill',fill)
      circle.setAttribute('stroke',isLast?'#f0f6fc':'none')
      circle.setAttribute('stroke-width',isLast?'1.5':'0')
      circle.setAttribute('data-bp',bp)
      circle.setAttribute('data-score',e.score)
      circle.setAttribute('data-ts',e.ts)
      circle.setAttribute('data-id',e.id)
      circle.setAttribute('data-index',ei)
      circle.style.cursor='pointer'
      circle.addEventListener('click',()=>showModal(e,bp,ei+1,evts.length))
      // tooltip title
      const title=document.createElementNS(SVG_NS,'title')
      title.textContent=`${bp} #${e.id} — ${e.score.toFixed(1)} (${e.ts})`
      circle.appendChild(title)
      svg.appendChild(circle)
      // connect line between nodes
      if(ei>0){
        const prev=evts[ei-1]
        const ppx=LEFT_MARGIN + (pct(prev.tsObj.getTime())/100)*chartW
        const line=document.createElementNS(SVG_NS,'line')
        line.setAttribute('x1',ppx);line.setAttribute('y1','18')
        line.setAttribute('x2',px);line.setAttribute('y2','18')
        line.setAttribute('stroke','#30363d')
        line.setAttribute('stroke-width','1.5')
        svg.insertBefore(line,svg.firstChild)
      }
      // latest score label
      if(isLast){
        const txt=document.createElementNS(SVG_NS,'text')
        txt.setAttribute('x',px+12);txt.setAttribute('y','22')
        txt.setAttribute('fill',fill)
        txt.setAttribute('font-size','10')
        txt.setAttribute('font-weight','600')
        txt.textContent=e.score.toFixed(1)
        svg.appendChild(txt)
      }
    }
    trackDiv.appendChild(svg)
    tracksEl.appendChild(trackDiv)
  }
  // Time marker line
  const marker=document.getElementById('timeMarker')
  if(sliderPct<100){
    marker.style.display='block'
    const mpx=232 + LEFT_MARGIN + (sliderPct/100)*chartW
    marker.style.left=mpx+'px'
    const tracksTop=tracksEl.getBoundingClientRect().top
    marker.style.top='0px'
    marker.style.height=totalH+'px'
  }else{
    marker.style.display='none'
  }
  // Time label
  const d=new Date(cutTime)
  const labelStr=d.toISOString().replace('T',' ').slice(0,16)+'Z'
  document.getElementById('timeLabel').textContent=
    sliderPct<100?`${labelStr} (${sliderPct}%)`:'Alla händelser'
}
// ====================================================================
// Modal
// ====================================================================
function showModal(e,bp,nth,total){
  const col=scoreColor(e.score)
  const fill=scoreHex(e.score)
  document.getElementById('modalTitle').textContent=bp
  document.getElementById('modalBody').innerHTML=
    `<div class="row"><span class="label">Run ID</span><span class="val">${e.id}</span></div>`+
    `<div class="row"><span class="label">Utvärdering</span><span class="val">${nth}/${total}</span></div>`+
    `<div class="row"><span class="label">Tidstämpel</span><span class="val">${e.ts}</span></div>`+
    `<div class="row"><span class="label">Score (C)</span><span class="val ${col}">${e.score.toFixed(1)}</span></div>`+
    `<div class="row"><span class="label">Status</span><span class="val">${e.score>=85?'Production':e.score>=70?'Refinery':'Training'}</span></div>`+
    (e.detail?`<div class="row"><span class="label">Detail</span><span class="val">${e.detail}</span></div>`:'')
  document.getElementById('modal').classList.add('show')
  document.getElementById('overlay').classList.add('show')
}
document.getElementById('modalClose').addEventListener('click',()=>{
  document.getElementById('modal').classList.remove('show')
  document.getElementById('overlay').classList.remove('show')
})
document.getElementById('overlay').addEventListener('click',()=>{
  document.getElementById('modal').classList.remove('show')
  document.getElementById('overlay').classList.remove('show')
})
// ====================================================================
// Slider & Playback
// ====================================================================
const slider=document.getElementById('timeSlider')
let playing=false, playInterval=null
function updateSlider(){render(parseFloat(slider.value))}
slider.addEventListener('input',updateSlider)
document.getElementById('playBtn').addEventListener('click',()=>{
  if(playing){
    clearInterval(playInterval);playing=false
    document.getElementById('playBtn').textContent='Play'
    document.getElementById('playBtn').classList.remove('active')
    return
  }
  playing=true
  document.getElementById('playBtn').textContent='Pause'
  document.getElementById('playBtn').classList.add('active')
  if(parseFloat(slider.value)>=99)slider.value='0'
  updateSlider()
  const steps=events.length
  let step=parseFloat(slider.value)
  playInterval=setInterval(()=>{
    step+=100/steps
    if(step>=100){step=100;clearInterval(playInterval);playing=false
      document.getElementById('playBtn').textContent='Play'
      document.getElementById('playBtn').classList.remove('active')
    }
    slider.value=Math.min(step,100)
    updateSlider()
  },400)
})
document.getElementById('resetBtn').addEventListener('click',()=>{
  if(playing){clearInterval(playInterval);playing=false
    document.getElementById('playBtn').textContent='Play'
    document.getElementById('playBtn').classList.remove('active')}
  slider.value='100'
  updateSlider()
})
// ====================================================================
// Init
// ====================================================================
window.addEventListener('resize',()=>updateSlider())
updateSlider()
</script>
</body>
</html>
```
Output till `agent-lifecycle-timeline.html` — öppna i valfri browser.
Vad den gör:
- 17 tracks (blueprints med eval-scores), varje track är en horisontell SVG-rad med noder färgkodade: guld (85+), amber (70-84), blå (<70)
- Time scrubber slider — dra för att spola fram/bak i tiden. Varje position visar bara events fram till den tidpunkten
- Play/Pause — auto-advancerar från första till sista event, steg per event
- Klicka på en nod — modal med detaljer: run ID, score, tidstämpel, version, status
- Statsrad längst upp: antal blueprints per fas (production/refinery/training) vid aktuell tidpunkt
- Senaste score per blueprint visas som etikett bredvid sista noden
- Blå tidsmarkör visar var i tidslinjen du är