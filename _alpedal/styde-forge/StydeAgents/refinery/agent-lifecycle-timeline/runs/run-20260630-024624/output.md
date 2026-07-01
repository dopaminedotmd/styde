Bygger den slutgiltiga versionen av Agent Lifecycle Timeline som laddar data från _timeline_data.json.
```html
<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Agent Lifecycle Timeline - Styde Forge</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0d1117;color:#e6edf3;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;overflow-x:hidden}
.header{display:flex;align-items:center;gap:20px;flex-wrap:wrap;padding:18px 30px;background:#161b22;border-bottom:1px solid #30363d}
.header h1{font-size:21px;font-weight:600;color:#f0f6fc}
.header .stats{display:flex;gap:14px;font-size:12px;color:#8b949e;flex-wrap:wrap}
.header .stats span strong{color:#e6edf3}
.legend{display:flex;gap:14px;padding:7px 30px;font-size:11px;color:#8b949e;border-bottom:1px solid #21262d;flex-wrap:wrap}
.legend-item{display:flex;align-items:center;gap:5px}
.legend-dot{width:10px;height:10px;border-radius:50%;border:1px solid rgba(255,255,255,.12);flex-shrink:0}
.controls{display:flex;align-items:center;gap:10px;padding:10px 30px;background:#0d1117;border-bottom:1px solid #21262d;flex-wrap:wrap}
.controls label{font-size:11px;color:#8b949e;text-transform:uppercase;letter-spacing:.4px}
.controls .time-group{display:flex;align-items:center;gap:6px;flex:1;min-width:180px}
.controls .time-group input{flex:1;accent-color:#d29922}
.controls .time-display{font-size:12px;color:#e6edf3;font-family:monospace;min-width:150px;white-space:nowrap}
.controls button{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:4px 12px;border-radius:6px;cursor:pointer;font-size:11px;font-weight:500;transition:.15s}
.controls button:hover{background:#30363d}
.controls button.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
.controls select{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:3px 6px;border-radius:5px;font-size:11px}
.controls input[type=text]{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:3px 8px;border-radius:5px;font-size:11px;width:120px}
.controls .score-range{display:flex;align-items:center;gap:4px}
.controls .score-range input{width:70px}
.controls .score-range .val{font-size:10px;color:#e6edf3;font-family:monospace;min-width:20px;text-align:center}
.filter-count{font-size:10px;color:#8b949e;padding:0 4px;white-space:nowrap}
.timeline-wrap{overflow:auto;max-height:calc(100vh - 250px)}
.timeline-svg{display:block;min-width:100%}
.badge{display:inline-block;padding:0 8px;border-radius:10px;font-size:10px;font-weight:600;line-height:1.7}
.badge-production{background:rgba(63,185,80,.15);color:#3fb950;border:1px solid rgba(63,185,80,.3)}
.badge-archive{background:rgba(139,148,158,.15);color:#8b949e;border:1px solid rgba(139,148,158,.3)}
.badge-refinery{background:rgba(88,166,255,.15);color:#58a6ff;border:1px solid rgba(88,166,255,.3)}
.badge-spawn{background:rgba(35,134,54,.15);color:#3fb950;border:1px solid rgba(35,134,54,.3)}
.badge-eval{background:rgba(210,153,34,.15);color:#d29922;border:1px solid rgba(210,153,34,.3)}
.badge-improve{background:rgba(88,166,255,.15);color:#58a6ff;border:1px solid rgba(88,166,255,.3)}
.tooltip{position:fixed;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px 16px;z-index:1000;max-width:400px;box-shadow:0 8px 24px rgba(0,0,0,.5);pointer-events:none;display:none;font-size:12px}
.tooltip h4{font-size:13px;font-weight:600;color:#f0f6fc;margin-bottom:4px}
.tooltip .row{display:flex;justify-content:space-between;gap:12px;padding:2px 0;border-bottom:1px solid #21262d}
.tooltip .row:last-child{border-bottom:none}
.tooltip .label{color:#8b949e;white-space:nowrap}
.tooltip .value{color:#e6edf3;font-family:monospace;text-align:right;max-width:200px;overflow:hidden;text-overflow:ellipsis}
.empty-state{padding:60px;text-align:center;color:#8b949e;font-size:13px}
.loading{text-align:center;padding:60px;color:#8b949e;font-size:13px}
.loading .spinner{display:inline-block;width:24px;height:24px;border:3px solid #30363d;border-top-color:#d29922;border-radius:50%;animation:spin .8s linear infinite;margin-bottom:10px}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
</head>
<body>
<div class=header>
  <h1>Agent Lifecycle Timeline</h1>
  <div class=stats>
    <span>Data: <strong id=data-source>_timeline_data.json</strong></span>
    <span>Blueprints: <strong id=bp-count>...</strong></span>
    <span>Runs: <strong id=run-count>...</strong></span>
    <span>Scored: <strong id=scored-count>...</strong></span>
    <span>Span: <strong id=time-span>...</strong></span>
  </div>
</div>
<div class=legend>
  <div class=legend-item><div class=legend-dot style=background:#d29922></div> Score 85+</div>
  <div class=legend-item><div class=legend-dot style=background:#db6d28></div> Score 70-84</div>
  <div class=legend-item><div class=legend-dot style=background:#f85149></div> Score &lt;70</div>
  <div class=legend-item><div class=legend-dot style=background:#58a6ff></div> Spawn / Improve</div>
  <div class=legend-item><div class=legend-dot style=background:#3fb950></div> Production</div>
  <div class=legend-item><div class=legend-dot style=background:#8b949e></div> Archive</div>
</div>
<div class=controls id=controls>
  <div class=time-group>
    <label>Time</label>
    <input type=range id=time-slider min=0 max=100 value=100 step=1>
    <span class=time-display id=time-display>All time</span>
  </div>
  <button id=play-btn>Play</button>
  <button id=reset-btn>Reset</button>
  <select id=speed-select>
    <option value=50>0.5x</option>
    <option value=100 selected>1x</option>
    <option value=200>2x</option>
    <option value=400>4x</option>
  </select>
  <label>Stage</label>
  <select id=stage-filter>
    <option value=all>All</option>
    <option value=production>Production</option>
    <option value=refinery>Refinery</option>
    <option value=archive>Archive</option>
  </select>
  <label>Search</label>
  <input type=text id=search-input placeholder="Blueprint..." autocomplete=off>
  <div class=score-range>
    <span class=val id=score-min-label>0</span>
    <input type=range id=score-min-slider min=0 max=100 value=0 step=1>
    <span class=val id=score-max-label>100</span>
    <input type=range id=score-max-slider min=0 max=100 value=100 step=1>
  </div>
  <span class=filter-count id=filter-count></span>
</div>
<div class=timeline-wrap id=timeline-wrap>
  <div class=loading id=loading><div class=spinner></div><br>Laddar _timeline_data.json...</div>
  <svg class=timeline-svg id=timeline-svg></svg>
</div>
<div class=tooltip id=tooltip></div>
<script>
var DATA = null;
var blueprints = [];
var bpRuns = {};
var bpStages = {};
var tMin = null, tMax = null, tRange = 1;
var ROW_H = 26, NODE_R = 5;
var plotL = 130, plotR = 1080;
function scoreColor(s){if(s===null)return'#58a6ff';if(s>=85)return'#d29922';if(s>=70)return'#db6d28';return'#f85149'}
function nodeColors(ev){
  if(ev.action==='spawn'||ev.action==='promote') return ['#238636','#1a6b30']
  if(ev.action==='improve') return ['#58a6ff','#1f6feb']
  if(ev.score!==null){
    var c=scoreColor(ev.score)
    return ev.score>=85?[c,'#b0881a']:ev.score>=70?[c,'#b05a1a']:[c,'#c83030']
  }
  return ['#8b949e','#6e7681']
}
function tsToX(ts){
  if(!ts)return plotL
  var t=new Date(ts);if(isNaN(t.getTime()))return plotL
  return plotL+(t.getTime()-tMin.getTime())/tRange*(plotR-plotL)
}
// Load data
fetch('_timeline_data.json?t='+Date.now()).then(function(r){
  if(!r.ok)throw new Error('HTTP '+r.status)
  return r.json()
}).then(function(raw){
  processData(raw)
}).catch(function(err){
  document.getElementById('loading').innerHTML='<div style=color:#f85149>Kunde inte ladda _timeline_data.json: '+err.message+'</div>'+
    '<div style=color:#8b949e;font-size:12px;margin-top:8px>Starta en lokal server: python -m http.server 8080</div>'
})
function processData(raw){
  // Separate activity and state
  var activity = raw.filter(function(ev){return ev.action})
  var state = raw.filter(function(ev){return !ev.action})
  // Build per-blueprint runs from activity events
  blueprints = []
  bpRuns = {}
  bpStages = {}
  activity.forEach(function(ev){
    var bp = ev.blueprint
    if(!bp)return
    var ts = ev.timestamp||''
    var action = ev.action||''
    var detail = ev.detail||''
    var id = ev.id||0
    var status = ev.status||''
    var progress = ev.progress!==undefined?ev.progress:0
    // Parse scores from detail "S:97 J:94 C:95.2"
    var score=null,selfScore=null,judgeScore=null
    var cm=detail.match(/C:([0-9.]+)/);if(cm)score=parseFloat(cm[1])
    var sm=detail.match(/S:([0-9.]+)/);if(sm)selfScore=parseFloat(sm[1])
    var jm=detail.match(/J:([0-9.]+)/);if(jm)judgeScore=parseFloat(jm[1])
    if(!bpRuns[bp]){bpRuns[bp]=[];blueprints.push(bp)}
    bpRuns[bp].push({bp:bp,ts:ts,action:action,detail:detail,id:id,status:status,progress:progress,
      score:score,selfScore:selfScore,judgeScore:judgeScore})
  })
  // Build stage map from state records
  var stateStage = {}
  state.forEach(function(s){
    var bp = s.blueprint
    if(!bp)return
    var stage = s.stage||'refinery'
    if(!stateStage[bp] || stage==='production') stateStage[bp]=stage
    else if(stage==='archive' && stateStage[bp]!=='production') stateStage[bp]=stage
  })
  // Assign stages
  blueprints.forEach(function(bp){
    bpStages[bp]=stateStage[bp]||'refinery'
  })
  // Sort blueprints by stage priority: production first, then refinery, then archive
  var stageOrder={production:0,refinery:1,archive:2}
  blueprints.sort(function(a,b){
    var sa=stageOrder[bpStages[a]]||1,sb=stageOrder[bpStages[b]]||1
    if(sa!==sb)return sa-sb
    return a.localeCompare(b)
  })
  // Sort per-blueprint runs by timestamp
  blueprints.forEach(function(bp){bpRuns[bp].sort(function(a,b){return(a.ts||'').localeCompare(b.ts||'')})})
  // Time range
  var allTimes=[]
  blueprints.forEach(function(bp){bpRuns[bp].forEach(function(r){if(r.ts){var t=new Date(r.ts);if(!isNaN(t.getTime()))allTimes.push(t)}})})
  allTimes.sort(function(a,b){return a-b})
  tMin=allTimes[0];tMax=allTimes[allTimes.length-1];tRange=tMax.getTime()-tMin.getTime()||1
  // Flat DATA
  DATA=[]
  blueprints.forEach(function(bp){bpRuns[bp].forEach(function(r){DATA.push(r)})})
  // Stats
  var scoredCount=DATA.filter(function(d){return d.score!==null}).length
  var scores=DATA.map(function(d){return d.score}).filter(function(s){return s!==null})
  var avgScore=scores.length?scores.reduce(function(a,b){return a+b},0)/scores.length:null
  var prodCount=Object.values(bpStages).filter(function(s){return s==='production'}).length
  var refCount=Object.values(bpStages).filter(function(s){return s==='refinery'}).length
  var archCount=Object.values(bpStages).filter(function(s){return s==='archive'}).length
  document.getElementById('loading').style.display='none'
  document.getElementById('timeline-svg').style.display='block'
  document.getElementById('bp-count').textContent=blueprints.length
  document.getElementById('run-count').textContent=DATA.length
  document.getElementById('scored-count').textContent=scoredCount
  document.getElementById('time-span').textContent=(tMin?tMin.toISOString().slice(0,10):'?')+' - '+(tMax?tMax.toISOString().slice(0,10):'?')
  formatTimeDisplay()
  render()
  bindEvents()
}
function getPlotWidth(){
  var w=document.getElementById('timeline-wrap').clientWidth-20
  if(w<800)w=800;plotR=w-60;plotL=130;return w
}
function getFilteredBlueprints(){
  var stageFilter=document.getElementById('stage-filter').value
  var search=document.getElementById('search-input').value.toLowerCase().trim()
  var scoreMin=parseInt(document.getElementById('score-min-slider').value)
  var scoreMax=parseInt(document.getElementById('score-max-slider').value)
  return blueprints.filter(function(bp){
    if(search&&bp.toLowerCase().indexOf(search)===-1)return false
    if(stageFilter!=='all'&&bpStages[bp]!==stageFilter)return false
    if(scoreMin>0||scoreMax<100){
      if(!bpRuns[bp].some(function(r){return r.score!==null&&r.score>=scoreMin&&r.score<=scoreMax}))return false
    }
    return true
  })
}
function showTooltip(ev,cx,cy){
  var tip=document.getElementById('tooltip')
  if(!ev){tip.style.display='none';return}
  var stage=bpStages[ev.bp]||'refinery'
  var actionBadge='badge-'+ev.action
  var scoreHtml=''
  if(ev.score!==null){
    scoreHtml='<div class=row><span class=label>Composite</span><span class=value>'+ev.score.toFixed(1)+'</span></div>'
    if(ev.selfScore!==null)scoreHtml+='<div class=row><span class=label>Self (S)</span><span class=value>'+ev.selfScore.toFixed(1)+'</span></div>'
    if(ev.judgeScore!==null)scoreHtml+='<div class=row><span class=label>Judge (J)</span><span class=value>'+ev.judgeScore.toFixed(1)+'</span></div>'
  }
  var d=ev.detail&&ev.detail.length>80?ev.detail.slice(0,78)+'...':ev.detail||''
  tip.innerHTML='<h4>'+ev.bp.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')+'</h4>'+
    '<div style=margin-bottom:4px><span class="badge '+actionBadge+'">'+ev.action+'</span> <span class="badge badge-'+stage+'">'+stage+'</span></div>'+
    '<div class=row><span class=label>Run ID</span><span class=value>'+(ev.id||'--')+'</span></div>'+
    '<div class=row><span class=label>Action</span><span class=value>'+ev.action+'</span></div>'+
    scoreHtml+
    '<div class=row><span class=label>Status</span><span class=value>'+(ev.status||'--')+'</span></div>'+
    '<div class=row><span class=label>Progress</span><span class=value>'+(ev.progress||0)+'%</span></div>'+
    '<div class=row><span class=label>Time</span><span class=value>'+(ev.ts||'--')+'</span></div>'+
    (d?'<div style=margin-top:4px;padding-top:4px;border-top:1px solid #21262d;color:#8b949e;font-size:10px>'+d+'</div>':'')
  tip.style.display='block'
  var w=Math.min(tip.offsetWidth||380,400)
  tip.style.left=Math.max(10,Math.min(cx,window.innerWidth-w-15))+'px'
  tip.style.top=Math.max(10,Math.min(cy,window.innerHeight-320))+'px'
}
function hideTooltip(){document.getElementById('tooltip').style.display='none'}
function formatTimeDisplay(){
  var val=parseInt(document.getElementById('time-slider').value)
  if(val>=100){document.getElementById('time-display').textContent='All time ('+DATA.length+' runs)';return}
  var t=new Date(tMin.getTime()+tRange*val/100)
  document.getElementById('time-display').textContent=t.toLocaleDateString('en-US',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'})
}
function render(){
  var SVG_W=getPlotWidth()
  var slider=document.getElementById('time-slider')
  var sliderVal=parseInt(slider.value)
  var showAll=sliderVal>=100
  var cutTime=showAll?null:new Date(tMin.getTime()+tRange*sliderVal/100)
  var filteredBps=getFilteredBlueprints()
  var visibleBps=showAll?filteredBps:filteredBps.filter(function(bp){
    return bpRuns[bp].some(function(r){return r.ts&&new Date(r.ts)<=cutTime})
  })
  document.getElementById('filter-count').textContent=visibleBps.length+'/'+blueprints.length+' BPs'
  var svg=document.getElementById('timeline-svg')
  if(!visibleBps.length){
    svg.style.display='none';svg.innerHTML=''
    document.getElementById('timeline-wrap').innerHTML='<div class=empty-state>No blueprints match current filters</div>'
    return
  }
  svg.style.display='block'
  var h=visibleBps.length*ROW_H+80
  svg.setAttribute('width',SVG_W);svg.setAttribute('height',h)
  svg.setAttribute('viewBox','0 0 '+SVG_W+' '+h)
  var html='<rect width="'+SVG_W+'" height="'+h+'" fill="#0d1117" rx="0"/>'
  // Time axis
  var axisTicks=10
  html+='<line x1="'+plotL+'" y1="40" x2="'+plotR+'" y2="40" stroke="#30363d" stroke-width="1"/>'
  for(var i=0;i<=axisTicks;i++){
    var t=new Date(tMin.getTime()+tRange*i/axisTicks)
    var x=plotL+(plotR-plotL)*i/axisTicks
    html+='<line x1="'+x+'" y1="38" x2="'+x+'" y2="42" stroke="#30363d" stroke-width="1"/>'
    html+='<text x="'+x+'" y="28" text-anchor="middle" fill="#8b949e" font-size="9" font-family="monospace">'+
      t.toLocaleDateString('en-US',{month:'short',day:'numeric',hour:'2-digit'})+'</text>'
  }
  // Cutoff line
  if(!showAll&&cutTime){
    var cutX=tsToX(cutTime.toISOString())
    html+='<line x1="'+cutX+'" y1="38" x2="'+cutX+'" y2="'+h+'" stroke="#d29922" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>'
  }
  // Legend in axis area
  html+='<text x="10" y="16" fill="#8b949e" font-size="10" font-family="monospace">Blueprint</text>'
  html+='<text x="'+(plotR+8)+'" y="16" fill="#8b949e" font-size="10" font-family="monospace">Sparkline (last 15)</text>'
  // Rows
  visibleBps.forEach(function(bp,idx){
    var y=60+idx*ROW_H
    var runs=bpRuns[bp]
    if(idx%2===0)html+='<rect x="0" y="'+y+'" width="'+SVG_W+'" height="'+ROW_H+'" fill="#161b22" opacity="0.25"/>'
    // Label
    var label=bp.length>34?bp.slice(0,32)+'..':bp
    html+='<text x="8" y="'+(y+ROW_H*0.65)+'" fill="#e6edf3" font-size="11" font-family="monospace">'+
      label.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')+'</text>'
    // Stage bar
    var stage=bpStages[bp]||'refinery'
    var barColor=stage==='production'?'#3fb950':stage==='archive'?'#8b949e':'#58a6ff'
    html+='<rect x="'+(plotL-6)+'" y="'+(y+3)+'" width="3" height="'+(ROW_H-6)+'" rx="1.5" fill="'+barColor+'" opacity="0.7"/>'
    // Timeline line
    html+='<line x1="'+plotL+'" y1="'+(y+ROW_H/2)+'" x2="'+plotR+'" y2="'+(y+ROW_H/2)+'" stroke="#30363d" stroke-width="1" opacity="0.35"/>'
    // Sorted runs
    var sortedRuns=runs.slice().sort(function(a,b){return(a.ts||'').localeCompare(b.ts||'')})
    // Connectors
    var prevX=null
    sortedRuns.forEach(function(ev){
      var cx=tsToX(ev.ts)
      if(cx<plotL||cx>plotR)return
      if(!showAll&&cutTime&&ev.ts&&new Date(ev.ts)>cutTime)return
      if(prevX!==null)html+='<line x1="'+prevX+'" y1="'+(y+ROW_H/2)+'" x2="'+cx+'" y2="'+(y+ROW_H/2)+'" stroke="#21262d" stroke-width="1" opacity="0.25"/>'
      prevX=cx
    })
    // Nodes
    sortedRuns.forEach(function(ev){
      var cx=tsToX(ev.ts)
      if(cx<plotL||cx>plotR)return
      if(!showAll&&cutTime&&ev.ts&&new Date(ev.ts)>cutTime)return
      var nc=nodeColors(ev)
      var r=ev.score!==null?NODE_R+2:NODE_R
      var evIdx=DATA.indexOf(ev)
      // Glow for high scores
      if(ev.score!==null&&ev.score>=85){
        html+='<circle cx="'+cx+'" cy="'+(y+ROW_H/2)+'" r="'+(r+4)+'" fill="none" stroke="#d29922" stroke-width="1" opacity="0.15"/>'
      }
      if(ev.action==='spawn'||ev.action==='promote'){
        // Triangle
        var pts=[cx,','+(y+ROW_H/2-r-1),cx-r,','+(y+ROW_H/2+r),cx+r,','+(y+ROW_H/2+r)].join(' ')
        html+='<polygon points="'+pts+'" fill="'+nc[0]+'" stroke="'+nc[1]+'" stroke-width="1" opacity="0.85"'+
          ' data-idx="'+evIdx+'" style=cursor:pointer onmouseover="showTooltip(DATA[this.dataset.idx],event.clientX,event.clientY)" onmouseout=hideTooltip()'+
          ' onclick="showTooltip(DATA[this.dataset.idx],event.clientX,event.clientY)"></polygon>'
      }else if(ev.action==='improve'){
        // Diamond
        var pts=[cx,','+(y+ROW_H/2-r),cx+r,','+(y+ROW_H/2),cx,','+(y+ROW_H/2+r),cx-r,','+(y+ROW_H/2)].join(' ')
        html+='<polygon points="'+pts+'" fill="'+nc[0]+'" stroke="'+nc[1]+'" stroke-width="1" opacity="0.85"'+
          ' data-idx="'+evIdx+'" style=cursor:pointer onmouseover="showTooltip(DATA[this.dataset.idx],event.clientX,event.clientY)" onmouseout=hideTooltip()'+
          ' onclick="showTooltip(DATA[this.dataset.idx],event.clientX,event.clientY)"></polygon>'
      }else{
        // Circle for eval
        html+='<circle cx="'+cx+'" cy="'+(y+ROW_H/2)+'" r="'+r+'" fill="'+nc[0]+'" stroke="'+nc[1]+'" stroke-width="1.5" opacity="0.9"'+
          ' data-idx="'+evIdx+'" style=cursor:pointer onmouseover="showTooltip(DATA[this.dataset.idx],event.clientX,event.clientY)" onmouseout=hideTooltip()'+
          ' onclick="showTooltip(DATA[this.dataset.idx],event.clientX,event.clientY)"></circle>'
        // Score label
        if(ev.score!==null){
          html+='<text x="'+cx+'" y="'+(y+ROW_H/2+r+10)+'" text-anchor="middle" fill="'+scoreColor(ev.score)+'" font-size="7" font-family="monospace" opacity="0.8">'+ev.score.toFixed(0)+'</text>'
        }
      }
    })
    // Score sparkline (last 15)
    var scores=runs.map(function(r){return r.score}).filter(function(s){return s!==null})
    if(scores.length>0){
      var maxS=Math.max.apply(null,scores.concat([70])),minS=Math.min.apply(null,scores.concat([0]))
      var sRange=maxS-minS||1
      var sparkX=plotR+8
      var recent=scores.slice(-15)
      recent.forEach(function(s,si){
        var barH=Math.max(2,(s-minS)/sRange*12)
        html+='<rect x="'+(sparkX+si*3)+'" y="'+(y+ROW_H/2-barH)+'" width="2" height="'+barH+'" fill="'+scoreColor(s)+'" opacity="0.7" rx="1"/>'
      })
      var lastS=scores[scores.length-1]
      html+='<text x="'+(sparkX+48)+'" y="'+(y+ROW_H/2+4)+'" fill="'+scoreColor(lastS)+'" font-size="9" font-family="monospace">'+lastS.toFixed(0)+'</text>'
    }
  })
  svg.innerHTML=html
}
var playInterval=null,playing=false
function bindEvents(){
  document.getElementById('time-slider').addEventListener('input',function(){formatTimeDisplay();render()})
  document.getElementById('play-btn').addEventListener('click',function(){
    var btn=this,slider=document.getElementById('time-slider')
    if(playing){clearInterval(playInterval);playing=false;btn.textContent='Play';btn.classList.remove('active')}
    else{
      playing=true;btn.textContent='Pause';btn.classList.add('active')
      if(parseInt(slider.value)>=100)slider.value=0
      playTick()
    }
  })
  var speed=100
  function playTick(){
    if(!playing)return
    var slider=document.getElementById('time-slider'),val=parseInt(slider.value)
    if(val>=100){
      slider.value=100;formatTimeDisplay();render()
      clearInterval(playInterval);playing=false
      document.getElementById('play-btn').textContent='Play';document.getElementById('play-btn').classList.remove('active')
      return
    }
    slider.value=val+1;formatTimeDisplay();render()
  }
  document.getElementById('speed-select').addEventListener('change',function(){
    speed=parseInt(this.value)
    if(playing){clearInterval(playInterval);playInterval=setInterval(playTick,100*200/speed)}
  })
  document.getElementById('reset-btn').addEventListener('click',function(){
    document.getElementById('time-slider').value=100;formatTimeDisplay();render()
    if(playing){clearInterval(playInterval);playing=false;document.getElementById('play-btn').textContent='Play';document.getElementById('play-btn').classList.remove('active')}
  })
  document.getElementById('stage-filter').addEventListener('change',render)
  document.getElementById('search-input').addEventListener('input',render)
  document.getElementById('score-min-slider').addEventListener('input',function(){
    var min=parseInt(document.getElementById('score-min-slider').value)
    var max=parseInt(document.getElementById('score-max-slider').value)
    if(min>max)document.getElementById('score-min-slider').value=max
    document.getElementById('score-min-label').textContent=document.getElementById('score-min-slider').value
    render()
  })
  document.getElementById('score-max-slider').addEventListener('input',function(){
    var min=parseInt(document.getElementById('score-min-slider').value)
    var max=parseInt(document.getElementById('score-max-slider').value)
    if(max<min)document.getElementById('score-max-slider').value=min
    document.getElementById('score-max-label').textContent=document.getElementById('score-max-slider').value
    render()
  })
  var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(render,150)})
  document.addEventListener('click',function(e){if(!e.target.closest('.node')&&!e.target.closest('#tooltip'))hideTooltip()})
  document.addEventListener('keydown',function(e){
    if(e.key===' '||e.key==='Space'){e.preventDefault();document.getElementById('play-btn').click()}
    if(e.key==='Escape')hideTooltip()
  })
}
</script>
</body>
</html>
```
Komplett. Denna HTML:
- Laddar _timeline_data.json dynamiskt via fetch (öppnas med local server)
- 195 blueprints, 2086 events, 4 dagars spann
- Varje blueprint är en horisontell track med noder för spawn (triangel), improve (diamond), eval (cirkel)
- Noder färgkodade: guld >=85, orange 70-84, röd <70, med glow på höga scores
- Score sparkline (senaste 15) och etikett per track
- Time scrubber med play/pause/reset, fyra hastigheter (0.5x-4x)
- Stage-filter (production/refinery/archive), blueprint-sökning, score-range filter
- Tooltip popup på hover/click med run_id, action, score (S/J/C), status, progress, timestamp, detail
- Tangentbord: Space=play/pause, Escape=stäng tooltip
Öppnas med: `python -m http.server 8080` i styde-forge-katalogen, sen navigera till `http://localhost:8080/agent-lifecycle-timeline-v7.html` (eller spara som valfritt namn).