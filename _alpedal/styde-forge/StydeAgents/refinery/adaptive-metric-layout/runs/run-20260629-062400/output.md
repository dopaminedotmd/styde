<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--surface:#1a1d27;--surface2:#222533;--border:#2a2d3a;
  --text:#e1e3eb;--text2:#8b8fa3;--accent:#6c8cff;--accent2:#4a6cf7;
  --up:#34d399;--down:#f87171;--warn:#fbbf24;
  --radius:10px;--gap:12px;--header-h:52px;
}
body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}
#app{max-width:1400px;margin:0 auto;padding:16px}
header{display:flex;align-items:center;justify-content:space-between;height:var(--header-h);margin-bottom:16px;padding:0 4px}
header h1{font-size:1.3rem;font-weight:600;letter-spacing:-0.3px}
.header-stats{display:flex;gap:18px;font-size:0.82rem;color:var(--text2)}
.header-stats span strong{color:var(--text);font-weight:600}
#dashboard-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--gap);margin-bottom:16px}
#collapsed-section{border-top:1px solid var(--border);padding-top:14px;display:none}
#collapsed-section.visible{display:block}
#collapsed-section h3{font-size:0.85rem;color:var(--text2);margin-bottom:10px;cursor:pointer;user-select:none}
#collapsed-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px}
.panel{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px 16px;cursor:grab;transition:box-shadow 0.2s,border-color 0.2s,transform 0.15s;position:relative;user-select:none}
.panel:hover{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.panel.dragging{opacity:0.4;border-style:dashed}
.panel.drop-target{border-color:var(--accent2);box-shadow:0 0 12px rgba(108,140,255,0.25)}
.panel.size-large{grid-column:span 2}
.panel.size-normal{grid-column:span 1}
.panel.size-compact{grid-column:span 1;padding:10px 14px}
.panel.size-collapsed{display:none}
.panel.locked .lock-indicator{opacity:1}
.panel.locked{cursor:default}
.panel-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:6px}
.panel-label{font-size:0.78rem;color:var(--text2);text-transform:uppercase;letter-spacing:0.4px;display:flex;align-items:center;gap:6px}
.panel-icon{font-size:1rem}
.panel-controls{display:flex;gap:4px;align-items:center}
.panel-controls button{background:none;border:none;color:var(--text2);cursor:pointer;padding:3px 5px;border-radius:4px;font-size:0.75rem;line-height:1;transition:color 0.15s,background 0.15s}
.panel-controls button:hover{color:var(--text);background:var(--surface2)}
.lock-indicator{opacity:0.25;font-size:0.7rem;transition:opacity 0.2s}
.panel-value{font-size:2rem;font-weight:700;letter-spacing:-0.5px;line-height:1.1}
.panel-unit{font-size:0.85rem;font-weight:400;color:var(--text2);margin-left:3px}
.panel-trend{font-size:0.8rem;margin-top:4px;display:flex;align-items:center;gap:4px}
.panel-trend.up{color:var(--up)}.panel-trend.down{color:var(--down)}
.panel-spark{height:32px;margin-top:8px;display:flex;align-items:flex-end;gap:2px}
.panel-spark .bar{flex:1;background:var(--accent);border-radius:2px 2px 0 0;min-height:2px;opacity:0.7;transition:height 0.4s}
.size-compact .panel-value{font-size:1.3rem}
.size-compact .panel-spark{height:20px;margin-top:4px}
.collapsed-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:10px 13px;cursor:pointer;transition:border-color 0.15s;display:flex;align-items:center;gap:8px}
.collapsed-card:hover{border-color:var(--accent)}
.collapsed-card .cc-icon{font-size:1rem}
.collapsed-card .cc-label{font-size:0.75rem;color:var(--text2)}
.collapsed-card .cc-value{font-size:1rem;font-weight:600;margin-left:auto}
.ghost{position:fixed;pointer-events:none;z-index:9999;opacity:0.8;transform:scale(1.02);box-shadow:0 8px 32px rgba(0,0,0,0.5);border:1.5px solid var(--accent);border-radius:var(--radius);background:var(--surface)}
</style>
</head>
<body>
<div id="app">
<header>
<h1>Adaptive Dashboard</h1>
<div class="header-stats">
<span>Recomputes: <strong id="recompute-count">0</strong></span>
<span>Panels: <strong id="panel-count">0</strong></span>
<span>Data source: <strong id="source-label">mock-seeded</strong></span>
</div>
</header>
<div id="dashboard-grid"></div>
<div id="collapsed-section"><h3 id="collapsed-toggle">More panels ▸</h3><div id="collapsed-grid"></div></div>
</div>
<script>
/* ================================================================
   SEEDED RNG — deterministic mock data
   ================================================================ */
const SeededRNG = (()=>{
  function mulberry32(a){return()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
  let rng=mulberry32(42)
  return{seed(s){rng=mulberry32(s)},next(){return rng()},int(min,max){return Math.floor(rng()*(max-min+1))+min}}
})()
/* ================================================================
   MOCK DATA LAYER — deterministic data source interface
   ================================================================ */
const MockDataLayer = (()=>{
  const PANEL_DEFS=[
    {id:'cpu',label:'CPU Usage',unit:'%',icon:'⚙️',base:45,swing:30},
    {id:'memory',label:'Memory',unit:'GB',icon:'🧠',base:12,swing:4},
    {id:'disk',label:'Disk I/O',unit:'MB/s',icon:'💾',base:80,swing:60},
    {id:'network',label:'Network',unit:'Mbps',icon:'🌐',base:200,swing:150},
    {id:'requests',label:'Requests',unit:'/s',icon:'📡',base:1200,swing:800},
    {id:'latency',label:'Latency',unit:'ms',icon:'⏱️',base:45,swing:30},
    {id:'errors',label:'Error Rate',unit:'%',icon:'🚨',base:0.5,swing:0.8},
    {id:'users',label:'Active Users',unit:'',icon:'👥',base:340,swing:120},
    {id:'cache',label:'Cache Hit',unit:'%',icon:'📦',base:82,swing:15},
    {id:'queue',label:'Queue Depth',unit:'',icon:'📋',base:18,swing:25}
  ]
  function buildSpark(base,swing,points){
    const arr=[];let v=base
    for(let i=0;i<points;i++){v+=SeededRNG.next()*swing-swing/2;arr.push(Math.max(0,Math.round(v)))}
    return arr
  }
  let fetchCount=0
  return{
    async fetchMetrics(){
      fetchCount++
      SeededRNG.seed(42+fetchCount*7)
      return PANEL_DEFS.map(d=>{
        const value=Math.round((d.base+SeededRNG.next()*d.swing-d.swing/2)*10)/10
        const prevValue=Math.round((d.base+SeededRNG.next()*d.swing-d.swing/2)*10)/10
        const trend=value>prevValue*1.02?'up':value<prevValue*0.98?'down':'flat'
        return{id:d.id,label:d.label,unit:d.unit,icon:d.icon,value,trend,
          history:buildSpark(d.base,d.swing,12)}
      })
    },
    getPanelDefs(){return PANEL_DEFS}
  }
})()
/* ================================================================
   PERSISTENCE LAYER — localStorage save/restore
   ================================================================ */
const PersistenceLayer = (()=>{
  const KEY='adaptive-dashboard-v2'
  return{
    save(state){
      try{localStorage.setItem(KEY,JSON.stringify(state))}catch(e){/* quota exceeded, ignore */}
    },
    load(){
      try{const raw=localStorage.getItem(KEY);return raw?JSON.parse(raw):null}catch(e){return null}
    }
  }
})()
/* ================================================================
   ATTENTION TRACKER — logs view duration, interactions per panel
   ================================================================ */
const AttentionTracker = (()=>{
  let records={}
  const NOW=()=>Date.now()
  function ensure(id){
    if(!records[id])records[id]={interactions:0,totalDuration:0,lastInteraction:0}
    return records[id]
  }
  let viewTimers={}
  return{
    startView(panelId){
      viewTimers[panelId]=NOW()
    },
    endView(panelId){
      if(viewTimers[panelId]){
        const dur=(NOW()-viewTimers[panelId])/1000
        ensure(panelId).totalDuration+=dur
        delete viewTimers[panelId]
      }
    },
    recordInteraction(panelId){
      const r=ensure(panelId);r.interactions++;r.lastInteraction=NOW()
    },
    getRecords(){return records},
    hydrate(saved){if(saved)records=saved},
    serialize(){return JSON.parse(JSON.stringify(records))}
  }
})()
/* ================================================================
   PANEL SCORER — composite attention metric
   ================================================================ */
const PanelScorer = {
  score(records,panelId){
    const r=records[panelId]
    if(!r)return 0
    const hoursSince=(Date.now()-r.lastInteraction)/(1000*60*60)
    const recency=1/(1+hoursSince*0.3)
    return r.interactions*r.totalDuration*recency
  },
  rank(records,panelIds){
    const scored=panelIds.map(id=>({id,score:this.score(records,id)}))
    scored.sort((a,b)=>b.score-a.score)
    return scored
  }
}
/* ================================================================
   DRAG HANDLER — cloneNode ghost, pointer tracking, single render
   ================================================================ */
const DragHandler = (()=>{
  let ghost=null,sourcePanel=null,sourceId=null,targetId=null
  let gridEl=null,onReorder=null,offsetX=0,offsetY=0,origRect=null
  function createGhost(el,rect){
    const g=el.cloneNode(true)
    g.classList.add('ghost')
    g.style.width=rect.width+'px'
    g.style.height=rect.height+'px'
    g.style.left=rect.left+'px'
    g.style.top=rect.top+'px'
    return g
  }
  function findDropTarget(x,y){
    const panels=[...gridEl.querySelectorAll('.panel:not(.dragging):not(.size-collapsed)')]
    for(const p of panels){
      const r=p.getBoundingClientRect()
      if(x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom)return p
    }
    return null
  }
  function onPointerMove(e){
    if(!ghost||!sourcePanel)return
    ghost.style.left=(e.clientX-offsetX)+'px'
    ghost.style.top=(e.clientY-offsetY)+'px'
    const target=findDropTarget(e.clientX,e.clientY)
    gridEl.querySelectorAll('.drop-target').forEach(p=>p.classList.remove('drop-target'))
    targetId=null
    if(target&&target!==sourcePanel){
      target.classList.add('drop-target')
      targetId=target.dataset.panelId
    }
  }
  function onPointerUp(e){
    if(!ghost||!sourcePanel)return
    ghost.remove();ghost=null
    document.removeEventListener('pointermove',onPointerMove)
    document.removeEventListener('pointerup',onPointerUp)
    sourcePanel.classList.remove('dragging')
    gridEl.querySelectorAll('.drop-target').forEach(p=>p.classList.remove('drop-target'))
    if(targetId&&targetId!==sourceId&&onReorder){
      onReorder(sourceId,targetId)
    }
    sourcePanel=null;sourceId=null;targetId=null;origRect=null
  }
  return{
    init(grid,reorderFn){gridEl=grid;onReorder=reorderFn},
    start(panelEl,e){
      if(panelEl.classList.contains('locked'))return
      sourcePanel=panelEl;sourceId=panelEl.dataset.panelId
      const rect=panelEl.getBoundingClientRect();origRect=rect
      offsetX=e.clientX-rect.left;offsetY=e.clientY-rect.top
      ghost=createGhost(panelEl,rect)
      document.body.appendChild(ghost)
      panelEl.classList.add('dragging')
      document.addEventListener('pointermove',onPointerMove)
      document.addEventListener('pointerup',onPointerUp)
    }
  }
})()
/* ================================================================
   RENDERER — targeted DOM patching, no full-container rebuilds
   ================================================================ */
const Renderer = (()=>{
  const gridEl=document.getElementById('dashboard-grid')
  const collapsedGrid=document.getElementById('collapsed-grid')
  const collapsedSection=document.getElementById('collapsed-section')
  const collapsedToggle=document.getElementById('collapsed-toggle')
  let collapsedOpen=false
  collapsedToggle.addEventListener('click',()=>{
    collapsedOpen=!collapsedOpen
    collapsedToggle.textContent=collapsedOpen?'More panels ▾':'More panels ▸'
    collapsedGrid.style.display=collapsedOpen?'grid':'none'
  })
  collapsedGrid.style.display='none'
  function panelHTML(p){return`<div class="panel-header"><span class="panel-label"><span class="panel-icon">${p.icon}</span>${p.label}</span><span class="panel-controls"><span class="lock-indicator" title="Locked">🔒</span><button class="btn-lock" title="Toggle lock">🔓</button><button class="btn-collapse" title="Collapse">─</button></span></div><div class="panel-value">${p.value}<span class="panel-unit">${p.unit}</span></div><div class="panel-trend ${p.trend}">${p.trend==='up'?'▲':p.trend==='down'?'▼':'─'} ${p.trend==='up'?'Rising':p.trend==='down'?'Falling':'Stable'}</div><div class="panel-spark">${p.history.map(h=>{const max=Math.max(...p.history,1);return`<span class="bar" style="height:${(h/max)*100}%"></span>`}).join('')}</div>`}
  function createPanelElement(panel,rank){
    const el=document.createElement('div')
    el.className=`panel size-${panel.size}`
    if(panel.locked)el.classList.add('locked')
    el.dataset.panelId=panel.id
    el.innerHTML=panelHTML(panel)
    el.addEventListener('pointerdown',e=>{DragHandler.start(el,e)})
    el.addEventListener('pointerenter',()=>AttentionTracker.startView(panel.id))
    el.addEventListener('pointerleave',()=>AttentionTracker.endView(panel.id))
    el.addEventListener('click',e=>{
      if(e.target.closest('button'))return
      AttentionTracker.recordInteraction(panel.id)
    })
    const lockBtn=el.querySelector('.btn-lock')
    lockBtn.addEventListener('click',e=>{
      e.stopPropagation()
      panel.locked=!panel.locked
      if(panel.locked){el.classList.add('locked');lockBtn.textContent='🔒'}
      else{el.classList.remove('locked');lockBtn.textContent='🔓'}
      AttentionTracker.recordInteraction(panel.id)
    })
    const collapseBtn=el.querySelector('.btn-collapse')
    collapseBtn.addEventListener('click',e=>{
      e.stopPropagation()
      panel.collapsed=!panel.collapsed
      AttentionTracker.recordInteraction(panel.id)
    })
    return el
  }
  function createCollapsedCard(panel){
    const el=document.createElement('div')
    el.className='collapsed-card'
    el.innerHTML=`<span class="cc-icon">${panel.icon}</span><span class="cc-label">${panel.label}</span><span class="cc-value">${panel.value}${panel.unit}</span>`
    el.addEventListener('click',()=>{
      panel.collapsed=false
      AttentionTracker.recordInteraction(panel.id)
    })
    return el
  }
  const panelElements=new Map()
  function updateValue(el,panel){
    const valEl=el.querySelector('.panel-value')
    if(valEl){
      const current=valEl.childNodes[0]
      if(current&&current.nodeType===3&&current.textContent.trim()!==String(panel.value)){
        current.textContent=panel.value
      }
    }
    const trendEl=el.querySelector('.panel-trend')
    if(trendEl){
      trendEl.className=`panel-trend ${panel.trend}`
      trendEl.innerHTML=`${panel.trend==='up'?'▲':panel.trend==='down'?'▼':'─'} ${panel.trend==='up'?'Rising':panel.trend==='down'?'Falling':'Stable'}`
    }
    const spark=el.querySelector('.panel-spark')
    if(spark&&panel.history){
      const bars=spark.querySelectorAll('.bar')
      const max=Math.max(...panel.history,1)
      panel.history.forEach((h,i)=>{
        if(bars[i])bars[i].style.height=(h/max)*100+'%'
      })
    }
  }
  return{
    fullRender(panels){
      panelElements.clear()
      gridEl.textContent=''
      collapsedGrid.textContent=''
      let anyCollapsed=false
      panels.forEach(p=>{
        if(p.size==='collapsed'){
          anyCollapsed=true
          collapsedGrid.appendChild(createCollapsedCard(p))
        }else{
          const el=createPanelElement(p,p.score)
          panelElements.set(p.id,el)
          gridEl.appendChild(el)
        }
      })
      if(anyCollapsed)collapsedSection.classList.add('visible')
      else collapsedSection.classList.remove('visible')
      document.getElementById('panel-count').textContent=panels.length
    },
    targetedUpdate(panels){
      const panelMap=new Map(panels.map(p=>[p.id,p]))
      const existingIds=new Set([...gridEl.querySelectorAll('.panel')].map(el=>el.dataset.panelId))
      const newIds=new Set(panels.filter(p=>p.size!=='collapsed').map(p=>p.id))
      if(existingIds.size!==newIds.size||![...existingIds].every(id=>newIds.has(id))){
        this.fullRender(panels)
        return
      }
      panels.forEach(p=>{
        if(p.size==='collapsed')return
        const el=panelElements.get(p.id)
        if(!el)return
        updateValue(el,p)
        const sizeClass=[...el.classList].find(c=>c.startsWith('size-'))
        const targetSize=`size-${p.size}`
        if(sizeClass&&sizeClass!==targetSize){
          el.classList.remove(sizeClass)
          el.classList.add(targetSize)
        }
        if(p.locked&&!el.classList.contains('locked'))el.classList.add('locked')
        if(!p.locked&&el.classList.contains('locked'))el.classList.remove('locked')
      })
      collapsedGrid.textContent=''
      let anyCollapsed=false
      panels.forEach(p=>{
        if(p.size==='collapsed'){
          anyCollapsed=true
          collapsedGrid.appendChild(createCollapsedCard(p))
        }
      })
      if(anyCollapsed)collapsedSection.classList.add('visible')
      else collapsedSection.classList.remove('visible')
    },
    reorderDOM(orderedIds){
      const fragment=document.createDocumentFragment()
      orderedIds.forEach(id=>{
        const el=panelElements.get(id)
        if(el)fragment.appendChild(el)
      })
      gridEl.appendChild(fragment)
    }
  }
})()
/* ================================================================
   LAYOUT ENGINE — rank, assign sizes, determine order
   ================================================================ */
const LayoutEngine = (()=>{
  function assignSize(rankIndex,total,locked){
    if(locked)return'normal'
    if(rankIndex<3)return'large'
    if(rankIndex<6)return'normal'
    if(rankIndex<8)return'compact'
    return'collapsed'
  }
  return{
    compute(panels,records){
      const scored=PanelScorer.rank(records,panels.map(p=>p.id))
      const scoreMap=new Map(scored.map(s=>[s.id,s.score]))
      const result=panels.map((p,i)=>{
        const rank=scored.findIndex(s=>s.id===p.id)
        const size=assignSize(rank,panels.length,p.locked)
        return{...p,score:scoreMap.get(p.id)||0,rank,size}
      })
      result.sort((a,b)=>{
        if(a.locked&&!b.locked)return -1
        if(!a.locked&&b.locked)return 1
        return a.rank-b.rank
      })
      return result
    }
  }
})()
/* ================================================================
   MAIN APP — orchestrator
   ================================================================ */
const App = (()=>{
  let panels=[]
  let recomputeCount=0
  const recomputeEl=document.getElementById('recompute-count')
  function incRecompute(){
    recomputeCount++
    recomputeEl.textContent=recomputeCount
  }
  function reorderPanels(sourceId,targetId){
    const srcIdx=panels.findIndex(p=>p.id===sourceId)
    const tgtIdx=panels.findIndex(p=>p.id===targetId)
    if(srcIdx===-1||tgtIdx===-1)return
    const [moved]=panels.splice(srcIdx,1)
    panels.splice(tgtIdx,0,moved)
    const orderedIds=panels.filter(p=>p.size!=='collapsed').map(p=>p.id)
    Renderer.reorderDOM(orderedIds)
    incRecompute()
    PersistenceLayer.save({panels:panels.map(p=>({id:p.id,locked:p.locked,collapsed:p.collapsed})),records:AttentionTracker.serialize()})
  }
  async function recompute(initial=false){
    if(initial)return
    const metrics=await MockDataLayer.fetchMetrics()
    const records=AttentionTracker.getRecords()
    const merged=panels.map(p=>{
      const m=metrics.find(m=>m.id===p.id)
      if(m)return{...p,value:m.value,trend:m.trend,history:m.history,icon:m.icon,unit:m.unit}
      return p
    })
    panels=LayoutEngine.compute(merged,records)
    Renderer.targetedUpdate(panels)
    incRecompute()
    PersistenceLayer.save({panels:panels.map(p=>({id:p.id,locked:p.locked,collapsed:p.collapsed})),records:AttentionTracker.serialize()})
  }
  async function init(){
    DragHandler.init(document.getElementById('dashboard-grid'),reorderPanels)
    const saved=PersistenceLayer.load()
    if(saved&&saved.records)AttentionTracker.hydrate(saved.records)
    const metrics=await MockDataLayer.fetchMetrics()
    const defs=MockDataLayer.getPanelDefs()
    panels=defs.map(d=>{
      const m=metrics.find(m=>m.id===d.id)
      return{id:d.id,label:d.label,icon:m?m.icon:d.icon,unit:m?m.unit:d.unit,
        value:m?m.value:0,trend:m?m.trend:'flat',history:m?m.history:[],
        score:0,rank:0,size:'normal',locked:false,collapsed:false}
    })
    if(saved&&saved.panels){
      const savedMap=new Map(saved.panels.map(p=>[p.id,p]))
      panels.forEach(p=>{
        const s=savedMap.get(p.id)
        if(s){p.locked=s.locked||false;p.collapsed=s.collapsed||false}
      })
    }
    const records=AttentionTracker.getRecords()
    panels=LayoutEngine.compute(panels,records)
    Renderer.fullRender(panels)
    incRecompute()
    setInterval(recompute,8000)
    document.getElementById('source-label').textContent='mock-seeded'
  }
  init().catch(console.error)
  return{recompute}
})()
</script>
</body>
</html>