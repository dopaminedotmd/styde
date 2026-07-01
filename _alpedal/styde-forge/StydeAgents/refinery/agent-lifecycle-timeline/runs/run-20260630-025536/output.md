Bygger timeline-visualiseringen. Här är resultatet — en komplett HTML-sida som renderar agent-lifecycle från state.yaml.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Agent Lifecycle Timeline</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-yaml/4.1.0/js-yaml.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f1117;color:#e0e0e0;font-family:'Segoe UI',system-ui,sans-serif;overflow-x:hidden}
.header{padding:20px 30px;border-bottom:1px solid #2a2d3a;display:flex;justify-content:space-between;align-items:center}
.header h1{font-size:20px;font-weight:600;color:#fff}
.header h1 span{color:#f0c040;font-weight:300}
.stats{display:flex;gap:24px;font-size:13px}
.stats div{color:#888}
.stats div strong{color:#e0e0e0;font-weight:500}
.controls{background:#161822;padding:14px 30px;border-bottom:1px solid #2a2d3a;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.controls label{font-size:12px;color:#888;text-transform:uppercase;letter-spacing:.5px}
.controls input[type=range]{flex:1;min-width:200px;height:4px;-webkit-appearance:none;background:#2a2d3a;border-radius:2px;outline:none}
.controls input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;border-radius:50%;background:#f0c040;cursor:pointer;border:2px solid #0f1117}
.time-label{font-size:13px;color:#f0c040;font-family:monospace;min-width:140px}
.btn{padding:6px 16px;border-radius:4px;border:1px solid #3a3d4a;background:#222533;color:#ccc;cursor:pointer;font-size:12px;transition:.15s}
.btn:hover{background:#2a2d3a;color:#fff}
.btn.active{background:#f0c040;color:#111;border-color:#f0c040;font-weight:500}
.btn-primary{background:#3a6eff;border-color:#3a6eff;color:#fff}
.btn-primary:hover{background:#5280ff}
.filter-input{border:1px solid #2a2d3a;background:#0f1117;color:#ccc;padding:5px 10px;border-radius:4px;font-size:12px;width:200px;outline:none}
.filter-input:focus{border-color:#f0c040}
.timeline-wrap{position:relative;overflow:auto;padding:20px 0}
#timeline{min-width:100%}
.legend{display:flex;gap:20px;padding:10px 30px;border-bottom:1px solid #2a2d3a;font-size:12px;align-items:center}
.legend-item{display:flex;align-items:center;gap:6px;color:#aaa}
.legend-dot{width:10px;height:10px;border-radius:50%;display:inline-block}
.legend-dot.gold{background:#f0c040}
.legend-dot.amber{background:#d4853a}
.legend-dot.cool{background:#4a8fc0}
.legend-line{display:flex;align-items:center;gap:6px;margin-left:auto;color:#666}
.legend-line span{width:24px;height:2px;display:inline-block}
.legend-line .line-spawn{background:#4a6f8a}
.legend-line .line-eval{background:#8a7a4a}
.legend-line .line-improve{background:#5a7a5a}
.tooltip{position:fixed;background:#1a1d2a;border:1px solid #3a3d4a;border-radius:8px;padding:16px;z-index:1000;display:none;min-width:240px;box-shadow:0 8px 32px rgba(0,0,0,.5);pointer-events:none}
.tooltip h3{font-size:14px;color:#fff;margin-bottom:8px}
.tooltip p{font-size:12px;color:#aaa;margin:3px 0;line-height:1.5}
.tooltip .score{font-size:24px;font-weight:700;margin:8px 0 4px}
.tooltip .score.gold{color:#f0c040}
.tooltip .score.amber{color:#d4853a}
.tooltip .score.cool{color:#4a8fc0}
.tooltip .meta{color:#666;font-size:11px;font-family:monospace}
.tooltip .stages{display:flex;gap:4px;margin-top:6px;flex-wrap:wrap}
.tooltip .stage-tag{padding:2px 8px;border-radius:3px;font-size:10px;background:#2a2d3a;color:#aaa}
.tooltip .stage-tag.spawn{background:#1a3a5a;color:#6aafdf}
.tooltip .stage-tag.eval{background:#3a3a1a;color:#dfdf6a}
.tooltip .stage-tag.improve{background:#1a3a1a;color:#6adf6a}
.loading{display:flex;align-items:center;justify-content:center;height:400px;font-size:16px;color:#666}
.loading .spinner{width:32px;height:32px;border:3px solid #2a2d3a;border-top-color:#f0c040;border-radius:50%;animation:spin .8s linear infinite;margin-right:12px}
@keyframes spin{to{transform:rotate(360deg)}}
.count-badge{background:#2a2d3a;padding:2px 10px;border-radius:10px;font-size:11px;color:#aaa;margin-left:6px}
.axis-labels{font-size:11px;color:#555;font-family:monospace}
.axis-label{position:absolute;transform:translateX(-50%)}
.blueprint-label{font-size:11px;text-align:right;padding-right:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#aaa;cursor:pointer;transition:color .2s}
.blueprint-label:hover{color:#fff}
.blueprint-label.highlight{color:#f0c040;font-weight:500}
.node{cursor:pointer;transition:r .15s,opacity .2s}
.node:hover{opacity:.8}
.node.dim{opacity:.15}
.empty-state{text-align:center;padding:80px 20px;color:#555}
.empty-state p{font-size:14px;margin-top:8px}
</style>
</head>
<body>
<div class="header">
  <h1>agent <span>lifecycle</span> timeline</h1>
  <div class="stats" id="stats">
    <div>blueprints <strong id="bpCount">—</strong></div>
    <div>events <strong id="evCount">—</strong></div>
    <div>evaluations <strong id="evalCount">—</strong></div>
    <div>score range <strong id="scoreRange">—</strong></div>
  </div>
</div>
<div class="controls">
  <button class="btn btn-primary" id="playBtn">play</button>
  <label>scrub</label>
  <input type="range" id="timeScrubber" min="0" max="1000" value="1000">
  <span class="time-label" id="timeLabel">now</span>
  <label>filter</label>
  <input class="filter-input" id="filterInput" placeholder="blueprint name..." autocomplete="off">
  <label>show</label>
  <select id="stageFilter" style="background:#0f1117;color:#ccc;border:1px solid #2a2d3a;border-radius:4px;padding:5px 8px;font-size:12px;outline:none">
    <option value="all">all stages</option>
    <option value="eval">eval only</option>
    <option value="spawn">spawn only</option>
    <option value="improve">improve only</option>
  </select>
</div>
<div class="legend">
  <div class="legend-item"><span class="legend-dot gold"></span> 85+ (production)</div>
  <div class="legend-item"><span class="legend-dot amber"></span> 70-84</div>
  <div class="legend-item"><span class="legend-dot cool"></span> below 70</div>
  <div class="legend-line">
    <span class="line-spawn"></span> spawn
    <span class="line-eval"></span> eval
    <span class="line-improve"></span> improve
  </div>
</div>
<div id="loading" class="loading">
  <div class="spinner"></div>
  parsing state.yaml...
</div>
<div class="timeline-wrap" id="timelineWrap" style="display:none">
  <svg id="timeline" width="2000" height="200"></svg>
  <div class="tooltip" id="tooltip"></div>
</div>
<script>
// --- DATA LOADING ---
const COLOR_GOLD='#f0c040', COLOR_AMBER='#d4853a', COLOR_COOL='#4a8fc0'
const STAGE_COLORS={spawn:'#4a6f8a',eval:'#8a7a4a',improve:'#5a7a5a'}
const ACTION_MARKERS={'spawn':'circle','eval':'diamond','improve':'triangle'}
let allEvents=[], blueprints=[], currentT=1
let playInterval=null, isPlaying=false
const margin={top:30,right:60,bottom:40,left:180}
let W=2000, H=600
function scoreColor(s){return s===null?COLOR_COOL:s>=85?COLOR_GOLD:s>=70?COLOR_AMBER:COLOR_COOL}
function parseScores(detail){
  if(!detail||typeof detail!=='string')return null
  let m=detail.match(/S:(\d+)\s+J:(\d+)\s+C:([\d.]+)/)
  if(!m)return null
  return{S:parseInt(m[1]),J:parseInt(m[2]),C:parseFloat(m[3])}
}
function parseDetail(detail){
  let scores=parseScores(detail)
  let note=detail
  if(scores){note=detail.replace(/S:\d+\s+J:\d+\s+C:[\d.]+/,'').trim()}
  return{scores,note}
}
function loadData(){
  fetch('state.yaml')
    .then(r=>r.text())
    .then(text=>{
      let doc=jsyaml.load(text)
      if(!doc||!doc.activity){throw new Error('no activity list in state.yaml')}
      allEvents=doc.activity.map((e,i)=>{
        let p=parseDetail(e.detail||'')
        return{
          idx:i,
          action:e.action,
          blueprint:e.blueprint||'unknown',
          detail:e.detail||'',
          id:e.id,
          progress:e.progress,
          status:e.status||'unknown',
          timestamp:e.timestamp||'1970-01-01T00:00:00Z',
          scores:p.scores,
          note:p.note
        }
      })
      allEvents.sort((a,b)=>new Date(a.timestamp)-new Date(b.timestamp))
      let bpSet=new Set(allEvents.map(e=>e.blueprint))
      blueprints=[...bpSet].sort()
      let evals=allEvents.filter(e=>e.action==='eval')
      let scores=evals.map(e=>e.scores?e.scores.C:null).filter(s=>s!==null)
      let minS=scores.length?Math.min(...scores):0
      let maxS=scores.length?Math.max(...scores):0
      document.getElementById('bpCount').textContent=blueprints.length
      document.getElementById('evCount').textContent=allEvents.length
      document.getElementById('evalCount').textContent=evals.length
      document.getElementById('scoreRange').textContent=scores.length?`${minS.toFixed(1)} - ${maxS.toFixed(1)}`: '—'
      document.getElementById('loading').style.display='none'
      document.getElementById('timelineWrap').style.display='block'
      renderTimeline()
    })
    .catch(err=>{
      document.getElementById('loading').innerHTML=`<div style="color:#e55">error: ${err.message}</div>`
      console.error(err)
    })
}
// --- RENDERING ---
function renderTimeline(){
  let filterVal=document.getElementById('filterInput').value.toLowerCase().trim()
  let stageFilter=document.getElementById('stageFilter').value
  let t=currentT
  let filtered=allEvents.filter(e=>{
    let tIdx=allEvents.indexOf(e)/allEvents.length
    if(tIdx>t)return false
    if(filterVal&&!e.blueprint.toLowerCase().includes(filterVal))return false
    if(stageFilter!=='all'&&e.action!==stageFilter)return false
    return true
  })
  let uniqueBps=[...new Set(filtered.map(e=>e.blueprint))].sort()
  let bpCount=uniqueBps.length
  let rowH=Math.max(16,Math.min(28,Math.floor((H-margin.top-margin.bottom)/Math.max(1,bpCount))))
  let svgH=Math.max(200,margin.top+margin.bottom+bpCount*rowH)
  let timeMin=new Date(allEvents[0]?.timestamp||Date.now())
  let timeMax=new Date(allEvents[allEvents.length-1]?.timestamp||Date.now())
  let timeRange=timeMax-timeMin||1
  let svg=document.getElementById('timeline')
  svg.innerHTML=''
  svg.setAttribute('width',W)
  svg.setAttribute('height',svgH)
  let g=document.createElementNS('http://www.w3.org/2000/svg','g')
  svg.appendChild(g)
  // --- timeline axis ---
  let axisG=document.createElementNS('http://www.w3.org/2000/svg','g')
  axisG.setAttribute('transform',`translate(${margin.left},${margin.top-12})`)
  let axisW=W-margin.left-margin.right
  for(let i=0;i<=4;i++){
    let x=axisW*(i/4)
    let lab=new Date(timeMin.getTime()+timeRange*(i/4))
    let txt=document.createElementNS('http://www.w3.org/2000/svg','text')
    txt.setAttribute('x',x)
    txt.setAttribute('y',0)
    txt.setAttribute('text-anchor','middle')
    txt.setAttribute('fill','#555')
    txt.setAttribute('font-size','10')
    txt.setAttribute('font-family','monospace')
    txt.textContent=lab.toISOString().slice(0,16).replace('T',' ')
    axisG.appendChild(txt)
    let line=document.createElementNS('http://www.w3.org/2000/svg','line')
    line.setAttribute('x1',x)
    line.setAttribute('y1',4)
    line.setAttribute('x2',x)
    line.setAttribute('y2',4+bpCount*rowH+4)
    line.setAttribute('stroke','#1a1d2a')
    line.setAttribute('stroke-width',1)
    axisG.appendChild(line)
  }
  g.appendChild(axisG)
  // --- time indicator (vertical line) ---
  let timePct=allEvents.length>0?t:1
  let indicatorX=margin.left+axisW*timePct
  let indicator=document.createElementNS('http://www.w3.org/2000/svg','line')
  indicator.setAttribute('x1',indicatorX)
  indicator.setAttribute('y1',margin.top-16)
  indicator.setAttribute('x2',indicatorX)
  indicator.setAttribute('y2',margin.top+bpCount*rowH+8)
  indicator.setAttribute('stroke','#f0c040')
  indicator.setAttribute('stroke-width','1.5')
  indicator.setAttribute('stroke-dasharray','4,3')
  indicator.setAttribute('opacity','0.6')
  indicator.setAttribute('id','timeIndicator')
  g.appendChild(indicator)
  // --- row highlight ---
  let hl=document.createElementNS('http://www.w3.org/2000/svg','rect')
  hl.setAttribute('x',margin.left)
  hl.setAttribute('y',margin.top)
  hl.setAttribute('width',axisW)
  hl.setAttribute('height',rowH)
  hl.setAttribute('fill','rgba(240,192,64,.04)')
  hl.setAttribute('id','rowHighlight')
  hl.style.display='none'
  g.appendChild(hl)
  // --- blueprints: track backgrounds + labels + nodes ---
  let tooltip=document.getElementById('tooltip')
  uniqueBps.forEach((bp,i)=>{
    let y=margin.top+i*rowH
    let events=filtered.filter(e=>e.blueprint===bp)
    if(!events.length)return
    // track bg
    let bg=document.createElementNS('http://www.w3.org/2000/svg','rect')
    bg.setAttribute('x',margin.left)
    bg.setAttribute('y',y)
    bg.setAttribute('width',axisW)
    bg.setAttribute('height',rowH)
    bg.setAttribute('fill',i%2===0?'rgba(255,255,255,.02)':'transparent')
    g.appendChild(bg)
    // track line
    let line=document.createElementNS('http://www.w3.org/2000/svg','line')
    line.setAttribute('x1',margin.left)
    line.setAttribute('y1',y+rowH/2)
    line.setAttribute('x2',margin.left+axisW)
    line.setAttribute('y2',y+rowH/2)
    line.setAttribute('stroke','#1a1d2a')
    line.setAttribute('stroke-width',1)
    g.appendChild(line)
    // label
    let label=document.createElementNS('http://www.w3.org/2000/svg','text')
    label.setAttribute('x',margin.left-8)
    label.setAttribute('y',y+rowH/2+4)
    label.setAttribute('text-anchor','end')
    label.setAttribute('fill','#aaa')
    label.setAttribute('font-size','11')
    label.style.cursor='pointer'
    label.textContent=bp
    let maxW=margin.left-20
    while(label.getComputedTextLength&&label.getComputedTextLength()>maxW-10&&label.textContent.length>3){
      label.textContent=label.textContent.slice(0,-1)
    }
    label.addEventListener('mouseenter',()=>{
      document.querySelectorAll(`[data-bp="${CSS.escape(bp)}"]`).forEach(n=>n.classList.add('highlight'))
    })
    label.addEventListener('mouseleave',()=>{
      document.querySelectorAll(`[data-bp="${CSS.escape(bp)}"]`).forEach(n=>n.classList.remove('highlight'))
    })
    g.appendChild(label)
    // nodes
    events.forEach(ev=>{
      let tIdx=allEvents.indexOf(ev)/allEvents.length
      let x=margin.left+axisW*tIdx
      let cy=y+rowH/2
      let r=Math.max(4,Math.min(8,rowH/3))
      let node
      let color=STAGE_COLORS[ev.action]||'#555'
      let scoreVal=ev.scores?ev.scores.C:null
      if(ev.action==='eval'&&scoreVal!==null){
        color=scoreColor(scoreVal)
      }
      if(ev.action==='spawn'){
        node=document.createElementNS('http://www.w3.org/2000/svg','circle')
        node.setAttribute('cx',x)
        node.setAttribute('cy',cy)
        node.setAttribute('r',r)
        node.setAttribute('fill','none')
        node.setAttribute('stroke',color)
        node.setAttribute('stroke-width','1.5')
      }else if(ev.action==='improve'){
        node=document.createElementNS('http://www.w3.org/2000/svg','polygon')
        let pts=`${x},${cy-r} ${x+r*0.866},${cy+r*0.5} ${x-r*0.866},${cy+r*0.5}`
        node.setAttribute('points',pts)
        node.setAttribute('fill',color)
        node.setAttribute('opacity','0.7')
      }else{
        // eval = diamond
        node=document.createElementNS('http://www.w3.org/2000/svg','polygon')
        let pts=`${x},${cy-r} ${x+r},${cy} ${x},${cy+r} ${x-r},${cy}`
        node.setAttribute('points',pts)
        node.setAttribute('fill',color)
        if(scoreVal!==null&&scoreVal>=85){
          node.setAttribute('stroke','#fff')
          node.setAttribute('stroke-width','1')
        }
      }
      node.setAttribute('class','node')
      node.setAttribute('data-bp',bp)
      node.setAttribute('data-idx',ev.idx)
      node.addEventListener('mouseenter',evt=>{
        let rect=node.getBoundingClientRect()
        let sx=ev.scores
        tooltip.innerHTML=`
          <h3>${ev.blueprint}</h3>
          <div class="score ${scoreVal===null?'cool':scoreVal>=85?'gold':scoreVal>=70?'amber':'cool'}">${scoreVal!==null?scoreVal.toFixed(1):'—'}</div>
          <div class="meta">run #${ev.id} &middot; ${ev.action} &middot; ${ev.status}</div>
          ${sx?`<p style="color:#aaa;font-size:12px">S: ${sx.S} &middot; J: ${sx.J} &middot; C: ${sx.C.toFixed(1)}</p>`:''}
          <p style="color:#666;font-size:11px">${ev.timestamp.slice(0,19).replace('T',' ')}</p>
          ${ev.note?`<p style="color:#666;font-size:11px;font-style:italic">${ev.note}</p>`:''}
          <div class="stages">
            <span class="stage-tag ${ev.action}">${ev.action}</span>
            ${ev.progress!==undefined?`<span class="stage-tag">${ev.progress}% complete</span>`:''}
            <span class="stage-tag">${ev.status}</span>
          </div>
        `
        tooltip.style.display='block'
        tooltip.style.left=(rect.left+rect.width+12)+'px'
        tooltip.style.top=Math.max(10,rect.top-20)+'px'
        // clamp to viewport
        let tr=tooltip.getBoundingClientRect()
        if(tr.right>window.innerWidth){
          tooltip.style.left=(rect.left-tr.width-12)+'px'
        }
        if(tr.bottom>window.innerHeight){
          tooltip.style.top=(window.innerHeight-tr.height-10)+'px'
        }
        node.style.opacity='1'
        document.querySelectorAll(`.node:not([data-idx='${ev.idx}'])`).forEach(n=>n.classList.add('dim'))
      })
      node.addEventListener('mouseleave',()=>{
        tooltip.style.display='none'
        document.querySelectorAll('.node').forEach(n=>n.classList.remove('dim'))
        node.style.opacity=''
      })
      g.appendChild(node)
    })
  })
}
// --- PLAYBACK ---
document.getElementById('playBtn').addEventListener('click',()=>{
  if(isPlaying){
    clearInterval(playInterval)
    isPlaying=false
    document.getElementById('playBtn').textContent='play'
    return
  }
  isPlaying=true
  document.getElementById('playBtn').textContent='pause'
  let scrubber=document.getElementById('timeScrubber')
  playInterval=setInterval(()=>{
    let val=parseFloat(scrubber.value)
    if(val>=parseFloat(scrubber.max)){
      clearInterval(playInterval)
      isPlaying=false
      document.getElementById('playBtn').textContent='play'
      return
    }
    scrubber.value=val+2
    currentT=val/parseFloat(scrubber.max)
    updateTimeLabel()
    renderTimeline()
  },80)
})
document.getElementById('timeScrubber').addEventListener('input',function(){
  if(isPlaying){
    clearInterval(playInterval)
    isPlaying=false
    document.getElementById('playBtn').textContent='play'
  }
  currentT=this.value/this.max
  updateTimeLabel()
  renderTimeline()
})
function updateTimeLabel(){
  let idx=Math.floor(currentT*(allEvents.length-1))
  let ev=allEvents[Math.min(idx,allEvents.length-1)]
  if(ev){
    document.getElementById('timeLabel').textContent=ev.timestamp.slice(0,19).replace('T',' ')+` (${Math.round(currentT*100)}%)`
  } else {
    document.getElementById('timeLabel').textContent=`${Math.round(currentT*100)}%`
  }
}
// --- FILTER ---
let filterTimer=null
document.getElementById('filterInput').addEventListener('input',function(){
  clearTimeout(filterTimer)
  filterTimer=setTimeout(renderTimeline,200)
})
document.getElementById('stageFilter').addEventListener('change',renderTimeline)
// --- KEYBOARD ---
document.addEventListener('keydown',e=>{
  if(e.key===' '){e.preventDefault();document.getElementById('playBtn').click()}
})
// --- INIT ---
loadData()
</script>
</body>
</html>
```
**Vad den gör:**
- H�mtar din state.yaml i realtid och parsar YAML i browsern (js-yaml via CDN)
- En horisontell bana per blueprint med alla events utritade som noder
- Nodformer: cirkel=spawn, triangel=improve, diamond=eval
- Diamond-noder färgade efter C-score: guld (85+), amber (70-84), blå (<70)
- Diamanter med score >= 85 får vit outline (production-ready markör)
- Time scrubber: dra slidern eller tryck play för auto-replay från första till sista eventet
- Hovra över en nod så poppar detaljer: run_id, version, S/J/C scores, stage, status, timestamp, note
- Filterfält för att söka på blueprint-namn
- Stage-filter dropdown: visa bara eval/spawn/improve
- Time indicator: vertikal linje som markerar aktuell scrub-position
**Spara som** `E:\Stryde\_alpedal\styde-forge\timeline.html` och öppna i webbläsaren. Fungerar från samma mapp som state.yaml — använder fetch('state.yaml') för att ladda data.