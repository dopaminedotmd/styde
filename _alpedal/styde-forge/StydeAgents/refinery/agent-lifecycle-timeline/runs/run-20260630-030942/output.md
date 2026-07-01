```html
<!DOCTYPE html>
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>Agent Lifecycle Timeline</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d1117;color:#e6edf3;font-family:system-ui,-apple-system,sans-serif;padding:20px;overflow-x:hidden}
h1{font-size:1.4rem;font-weight:500;margin:0 0 4px 0;color:#f0e6d0}
.sub{color:#8b949e;font-size:.85rem;margin-bottom:20px}
.controls{display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap}
.controls button{background:#1f2937;border:1px solid #30363d;color:#e6edf3;padding:6px 16px;border-radius:6px;cursor:pointer;font-size:.85rem}
.controls button:hover{background:#2d3748}
.controls button.active{background:#2563eb;border-color:#3b82f6}
.slider-container{flex:1;min-width:200px;display:flex;align-items:center;gap:10px}
.slider-container input{flex:1;accent-color:#f59e0b}
.slider-container label{font-size:.8rem;color:#8b949e;min-width:80px;text-align:right}
#timeline{overflow-x:auto;overflow-y:auto;max-height:80vh;position:relative;padding-bottom:20px}
#timeline svg{display:block;min-width:800px}
.node{cursor:pointer}
.node:hover{filter:brightness(1.3)}
.node-label{font-size:10px;fill:#8b949e;pointer-events:none}
.axis-label{fill:#8b949e;font-size:11px}
.tick text{fill:#6e7681;font-size:10px}
.tick line{stroke:#21262d;stroke-width:1}
.gridline{stroke:#161b22;stroke-width:1}
.popup{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#161b22;border:1px solid #30363d;border-radius:10px;padding:24px;z-index:1000;min-width:340px;max-width:460px;box-shadow:0 8px 32px rgba(0,0,0,.6)}
.popup.show{display:block}
.popup h2{font-size:1.1rem;margin-bottom:12px;color:#f0e6d0}
.popup .row{display:flex;justify-content:space-between;padding:4px 0;font-size:.85rem;border-bottom:1px solid #21262d}
.popup .row:last-child{border-bottom:none}
.popup .label{color:#8b949e}
.popup .value{color:#e6edf3;font-weight:500}
.popup .close{position:absolute;top:12px;right:14px;background:none;border:none;color:#8b949e;font-size:1.2rem;cursor:pointer}
.popup .close:hover{color:#e6edf3}
#overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:999}
#overlay.show{display:block}
.legend{display:flex;gap:16px;margin-bottom:14px;font-size:.8rem}
.legend span{display:flex;align-items:center;gap:6px}
.legend .dot{width:12px;height:12px;border-radius:50%;display:inline-block}
.stat-bar{display:flex;gap:16px;margin-bottom:14px;font-size:.8rem;color:#8b949e}
.stat-bar strong{color:#e6edf3}
</style>
<h1>Agent Lifecycle Timeline</h1>
<p class=sub>spawn to eval to improve to promote &mdash; each track is one blueprint</p>
<div class=controls>
  <button id=playBtn title="auto-play through timeline">Play</button>
  <button id=resetBtn title="reset to earliest event">Reset</button>
  <div class=slider-container>
    <label id=timeLabel>0 / 0</label>
    <input type=range id=timeSlider min=0 max=0 value=0 step=1>
  </div>
</div>
<div class=legend>
  <span><span class=dot style=background:#f59e0b></span> promoted (score 85+)</span>
  <span><span class=dot style=background:#d97706></span> eval (70-84)</span>
  <span><span class=dot style=background:#6b7280></span> spawn/below 70</span>
  <span><span class=dot style=background:#3b82f6></span> improved</span>
</div>
<div id=statBar class=stat-bar></div>
<div id=timeline>
  <svg id=tlSvg viewBox="0 0 1000 400"></svg>
</div>
<div id=overlay></div>
<div id=popup class=popup>
  <button class=close id=popupClose>&times;</button>
  <h2 id=popupTitle>Agent Details</h2>
  <div id=popupBody></div>
</div>
<script>
;(function(){
'use strict'
// ===== SAMPLE DATA =====
// In production this comes from parsing state.yaml via fetch('/state.yaml') then parseYAML()
// For the demo we embed representative forge data
const blueprints = [
  {name:'cli-agent', agents:[
    {id:'cli-v1.0-r1',ts:0,stage:'spawn',score:51,ver:'v1.0',run:1},
    {id:'cli-v1.1-r2',ts:1,stage:'eval',score:72,ver:'v1.1',run:2},
    {id:'cli-v1.2-r3',ts:2,stage:'eval',score:88,ver:'v1.2',run:3,promoted:true}
  ]},
  {name:'web-scraper',agents:[
    {id:'ws-v1.0-r1',ts:0,stage:'spawn',score:43,ver:'v1.0',run:1},
    {id:'ws-v1.1-r2',ts:2,stage:'eval',score:69,ver:'v1.1',run:2},
    {id:'ws-v1.2-r3',ts:4,stage:'eval',score:76,ver:'v1.2',run:3},
    {id:'ws-v1.3-r4',ts:5,stage:'improve',score:81,ver:'v1.3',run:4}
  ]},
  {name:'data-pipeline',agents:[
    {id:'dp-v1.0-r1',ts:1,stage:'spawn',score:39,ver:'v1.0',run:1},
    {id:'dp-v1.1-r2',ts:3,stage:'eval',score:65,ver:'v1.1',run:2},
    {id:'dp-v1.2-r3',ts:6,stage:'eval',score:91,ver:'v1.2',run:3,promoted:true}
  ]},
  {name:'api-builder',agents:[
    {id:'ab-v1.0-r1',ts:0,stage:'spawn',score:48,ver:'v1.0',run:1},
    {id:'ab-v1.1-r2',ts:1,stage:'eval',score:74,ver:'v1.1',run:2},
    {id:'ab-v1.2-r3',ts:3,stage:'improve',score:79,ver:'v1.2',run:3},
    {id:'ab-v1.3-r4',ts:4,stage:'eval',score:86,ver:'v1.3',run:4,promoted:true}
  ]},
  {name:'test-gen',agents:[
    {id:'tg-v1.0-r1',ts:0,stage:'spawn',score:35,ver:'v1.0',run:1},
    {id:'tg-v1.1-r2',ts:2,stage:'eval',score:58,ver:'v1.1',run:2}
  ]},
  {name:'doc-gen',agents:[
    {id:'dg-v1.0-r1',ts:1,stage:'spawn',score:44,ver:'v1.0',run:1},
    {id:'dg-v1.1-r2',ts:3,stage:'eval',score:67,ver:'v1.1',run:2},
    {id:'dg-v1.2-r3',ts:5,stage:'eval',score:73,ver:'v1.2',run:3},
    {id:'dg-v1.3-r4',ts:7,stage:'eval',score:82,ver:'v1.3',run:4}
  ]},
  {name:'config-agent',agents:[
    {id:'ca-v1.0-r1',ts:0,stage:'spawn',score:47,ver:'v1.0',run:1},
    {id:'ca-v1.1-r2',ts:1,stage:'improve',score:62,ver:'v1.1',run:2},
    {id:'ca-v1.2-r3',ts:2,stage:'eval',score:71,ver:'v1.2',run:3},
    {id:'ca-v1.3-r4',ts:4,stage:'eval',score:77,ver:'v1.3',run:4},
    {id:'ca-v1.4-r5',ts:5,stage:'improve',score:84,ver:'v1.4',run:5}
  ]},
  {name:'monitor',agents:[
    {id:'mo-v1.0-r1',ts:0,stage:'spawn',score:29,ver:'v1.0',run:1},
    {id:'mo-v1.1-r2',ts:2,stage:'eval',score:55,ver:'v1.1',run:2},
    {id:'mo-v1.2-r3',ts:6,stage:'eval',score:90,ver:'v1.2',run:3,promoted:true}
  ]}
]
// Flatten all events, assign global timestamps, sort
const allEvents = []
blueprints.forEach((bp,bi)=>{
  bp.agents.forEach(a=>{
    allEvents.push({bp:bp.name,bpIdx:bi,agent:a,tsGlobal:a.ts})
  })
})
allEvents.sort((a,b)=>a.tsGlobal-b.tsGlobal)
const maxTs = Math.max(0,...allEvents.map(e=>e.tsGlobal))
let currentTs = 0
const MARGIN_LEFT = 140
const MARGIN_TOP = 40
const ROW_HEIGHT = 36
const NODE_RADIUS = 10
const MIN_GAP = 40
// Build track positions
const trackPositions = {}
blueprints.forEach((bp,i)=>{
  trackPositions[bp.name] = MARGIN_TOP + i * ROW_HEIGHT
})
function getNodeColor(agent){
  if(agent.promoted) return '#f59e0b'
  if(agent.score >= 85) return '#f59e0b'
  if(agent.score >= 70) return '#d97706'
  if(agent.stage === 'spawn' || agent.score < 70) return '#6b7280'
  if(agent.stage === 'improve') return '#3b82f6'
  return '#6b7280'
}
function getNodeLabel(agent){
  let lbl = agent.ver + ' r' + agent.run
  lbl += ' ' + agent.score
  return lbl
}
function getTotalWidth(){
  if(allEvents.length < 2) return 600
  const range = maxTs || 1
  const spacing = Math.max(80, Math.min(160, 900 / range))
  return MARGIN_LEFT + (maxTs * spacing) + 80
}
function render(currentTick){
  let minW = getTotalWidth()
  const svg = document.getElementById('tlSvg')
  const allNodes = []
  // For each blueprint, find events up to currentTick
  const visible = {}
  blueprints.forEach(bp=>{visible[bp.name]=[]})
  allEvents.forEach(e=>{
    if(e.tsGlobal <= currentTick){
      visible[e.bp].push(e)
    }
  })
  // Determine visible blueprints
  const visibleBps = blueprints.filter(bp=>visible[bp.name].length > 0)
  const svgHeight = Math.max(300, MARGIN_TOP + visibleBps.length * ROW_HEIGHT + 40)
  // Compute x positions per blueprint based on event ordering
  const xPositions = {}
  visibleBps.forEach(bp=>{
    const events = visible[bp.name].sort((a,b)=>a.tsGlobal-b.tsGlobal)
    const range = maxTs || 1
    const spacing = Math.max(80, Math.min(160, Math.min(900,minW-180) / range))
    xPositions[bp.name] = {}
    events.forEach((e,i)=>{
      const prev = events[i-1]
      if(prev){
        const gap = (e.tsGlobal - prev.tsGlobal) * spacing
        const prevX = xPositions[bp.name][prev.agent.id]
        xPositions[bp.name][e.agent.id] = prevX + Math.max(MIN_GAP, gap)
      } else {
        xPositions[bp.name][e.agent.id] = MARGIN_LEFT + e.tsGlobal * spacing
      }
    })
  })
  let width = Math.max(minW, MARGIN_LEFT + 80)
  visibleBps.forEach(bp=>{
    const events = visible[bp.name].sort((a,b)=>a.tsGlobal-b.tsGlobal)
    if(events.length){
      const last = events[events.length-1]
      const lx = xPositions[bp.name][last.agent.id] || MARGIN_LEFT
      width = Math.max(width, lx + 120)
    }
  })
  width = Math.max(width, 800)
  svg.setAttribute('viewBox','0 0 '+width+' '+svgHeight)
  svg.setAttribute('width',width)
  svg.setAttribute('height',svgHeight)
  let html = ''
  // Grid lines
  html += '<g class=grid>'
  const gridInterval = Math.max(1, Math.floor(maxTs / 8) || 1)
  const range = maxTs || 1
  const spacing = Math.max(80, Math.min(160, Math.min(900,width-180) / range))
  for(let t=0; t<=maxTs; t+=gridInterval){
    const x = MARGIN_LEFT + t * spacing
    html += '<line class=gridline x1='+x+' y1='+MARGIN_TOP+' x2='+x+' y2='+(MARGIN_TOP+visibleBps.length*ROW_HEIGHT)+'/>'
    html += '<text class=tick x='+x+' y='+(MARGIN_TOP-10)+' text-anchor=middle>t'+t+'</text>'
  }
  html += '</g>'
  // Tracks and nodes
  visibleBps.forEach((bp,vi)=>{
    const y = MARGIN_TOP + vi * ROW_HEIGHT
    const events = visible[bp.name].sort((a,b)=>a.tsGlobal-b.tsGlobal)
    // Track bg
    html += '<rect x='+MARGIN_LEFT+' y='+(y-NODE_RADIUS-2)+' width='+(width-MARGIN_LEFT-40)+' height='+(ROW_HEIGHT-4)+' fill='+(vi%2===0?'#0d1117':'#111826')+' rx=4/>'
    // Track label
    html += '<text class=axis-label x='+(MARGIN_LEFT-10)+' y='+(y+4)+' text-anchor=end>'+bp.name+'</text>'
    // Connection line
    if(events.length > 1){
      const first = events[0]
      const last = events[events.length-1]
      const fx = xPositions[bp.name][first.agent.id] || MARGIN_LEFT
      const lx = xPositions[bp.name][last.agent.id] || MARGIN_LEFT
      html += '<line x1='+fx+' y1='+y+' x2='+lx+' y2='+y+' stroke=#30363d stroke-width=2 stroke-linecap=round/>'
    }
    // Nodes
    events.forEach(e=>{
      const x = xPositions[bp.name][e.agent.id] || MARGIN_LEFT
      const color = getNodeColor(e.agent)
      const cls = 'node'
      const dataId = e.agent.id.replace(/[^a-zA-Z0-9_-]/g,'_')
      let stroke = 'none'
      let strokeW = 0
      if(e.agent.promoted){
        stroke = '#fbbf24'
        strokeW = 3
      }
      html += '<circle class='+cls+' data-id='+dataId+' cx='+x+' cy='+y+' r='+NODE_RADIUS+' fill='+color+' stroke='+(stroke||'none')+' stroke-width='+strokeW+'/>'
      // Score label
      html += '<text class=node-label x='+x+' y='+(y+NODE_RADIUS+13)+' text-anchor=middle>'+e.agent.score+'</text>'
      allNodes.push({id:dataId,agent:e.agent,color,stroke})
    })
  })
  svg.innerHTML = html
  // Count stats
  const totalAgents = allEvents.length
  const promoted = allEvents.filter(e=>e.agent.promoted).length
  const active = allEvents.filter(e=>e.agent.score>=70 && !e.agent.promoted).length
  document.getElementById('statBar').innerHTML = 
    '<span><strong>'+totalAgents+'</strong> total agents</span>' +
    '<span><strong>'+promoted+'</strong> promoted</span>' +
    '<span><strong>'+active+'</strong> active (70+)</span>' +
    '<span>tick <strong>'+currentTick+'</strong>/'+maxTs+'</span>'
  // Attach click handlers via DOM events
  document.querySelectorAll('.node').forEach(el=>{
    el.addEventListener('click',function(e){
      const id = this.getAttribute('data-id')
      const found = allNodes.find(n=>n.id===id)
      if(found) showPopup(found.agent)
    })
  })
}
function showPopup(agent){
  const p = document.getElementById('popup')
  document.getElementById('overlay').classList.add('show')
  document.getElementById('popupTitle').textContent = 'Agent: '+agent.id
  document.getElementById('popupBody').innerHTML = 
    '<div class=row><span class=label>Run ID</span><span class=value>'+agent.id+'</span></div>' +
    '<div class=row><span class=label>Version</span><span class=value>'+agent.ver+'</span></div>' +
    '<div class=row><span class=label>Run</span><span class=value>#'+agent.run+'</span></div>' +
    '<div class=row><span class=label>Stage</span><span class=value>'+agent.stage+'</span></div>' +
    '<div class=row><span class=label>Score</span><span class=value>'+agent.score+'</span></div>' +
    (agent.promoted ? '<div class=row><span class=label>Promoted</span><span class=value style=color:#f59e0b>yes</span></div>' : '')
  p.classList.add('show')
}
// Controls
const slider = document.getElementById('timeSlider')
const timeLabel = document.getElementById('timeLabel')
slider.max = maxTs
slider.value = 0
slider.addEventListener('input',function(){
  currentTs = parseInt(this.value)
  timeLabel.textContent = currentTs + ' / ' + maxTs
  render(currentTs)
})
document.getElementById('playBtn').addEventListener('click',function(){
  if(this.classList.contains('active')){
    this.classList.remove('active')
    this.textContent = 'Play'
    return
  }
  this.classList.add('active')
  this.textContent = 'Pause'
  let tick = currentTs
  const interval = setInterval(()=>{
    if(!document.getElementById('playBtn').classList.contains('active')){
      clearInterval(interval)
      return
    }
    tick++
    if(tick > maxTs){
      tick = 0
    }
    currentTs = tick
    slider.value = tick
    timeLabel.textContent = tick + ' / ' + maxTs
    render(tick)
  }, 600)
})
document.getElementById('resetBtn').addEventListener('click',function(){
  document.getElementById('playBtn').classList.remove('active')
  document.getElementById('playBtn').textContent = 'Play'
  currentTs = 0
  slider.value = 0
  timeLabel.textContent = '0 / ' + maxTs
  render(0)
})
document.getElementById('popupClose').addEventListener('click',function(){
  document.getElementById('popup').classList.remove('show')
  document.getElementById('overlay').classList.remove('show')
})
document.getElementById('overlay').addEventListener('click',function(){
  document.getElementById('popup').classList.remove('show')
  this.classList.remove('show')
})
// Initial render
render(0)
})()
</script>
```