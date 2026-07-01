```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge — Agent Lifecycle Timeline</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e14;color:#d4d7d9;font-family:system-ui,'Segoe UI',sans-serif;overflow-x:hidden}
#app{max-width:1400px;margin:0 auto;padding:20px}
h1{font-size:20px;font-weight:400;color:#8a9aa8;margin-bottom:4px}
h1 span{color:#e8c547;font-weight:600}
.sub{font-size:12px;color:#5c6a78;margin-bottom:20px}
#controls{display:flex;align-items:center;gap:12px;margin-bottom:16px;padding:12px 16px;background:#131a23;border-radius:8px;flex-wrap:wrap}
#controls button{background:#1e293b;border:1px solid #2a3a4d;color:#d4d7d9;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:13px;transition:.15s}
#controls button:hover{background:#2a3a4d;border-color:#e8c547}
#controls button.active{background:#e8c547;color:#0a0e14;border-color:#e8c547;font-weight:600}
#timeLabel{font-size:12px;color:#8a9aa8;min-width:140px;font-variant-numeric:tabular-nums}
#sliderWrap{flex:1;min-width:200px;position:relative}
#sliderWrap input[type=range]{width:100%;height:4px;-webkit-appearance:none;background:#2a3a4d;border-radius:2px;outline:none}
#sliderWrap input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;border-radius:50%;background:#e8c547;cursor:pointer;border:2px solid #0a0e14}
#stats{display:flex;gap:16px;font-size:12px;color:#5c6a78;margin-bottom:12px;flex-wrap:wrap}
#stats span{background:#131a23;padding:4px 10px;border-radius:4px}
#timelineWrap{overflow-x:auto;overflow-y:auto;max-height:calc(100vh - 220px);background:#0f151c;border-radius:8px;border:1px solid #1e293b;position:relative}
#timeline{display:block;min-width:100%}
.track-label{font-size:11px;fill:#8a9aa8;cursor:pointer}
.track-label:hover{fill:#e8c547}
.node{cursor:pointer;transition:opacity .15s}
.node:hover{opacity:1!important}
.node-label{font-size:9px;fill:#fff;text-anchor:middle;pointer-events:none;font-weight:600}
.tooltip{position:fixed;background:#1a2535;border:1px solid #2a3a4d;border-radius:8px;padding:12px 16px;font-size:12px;line-height:1.5;z-index:1000;max-width:340px;display:none;box-shadow:0 8px 24px rgba(0,0,0,.5)}
.tooltip.show{display:block}
.tooltip h3{color:#e8c547;font-size:14px;margin-bottom:4px;font-weight:600}
.tooltip .row{display:flex;justify-content:space-between;gap:16px;color:#b0bec5;margin:2px 0}
.tooltip .row .val{color:#d4d7d9;font-weight:500}
.tooltip .score{font-size:18px;font-weight:700;text-align:center;padding:6px 0;margin:6px 0;border-radius:4px}
.tooltip .score.gold{color:#e8c547}
.tooltip .score.amber{color:#d4a84b}
.tooltip .score.cool{color:#6b8fa0}
#legend{display:flex;gap:16px;font-size:11px;color:#8a9aa8;margin-top:12px;align-items:center}
#legend .dot{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:4px}
.dot.gold{background:#e8c547}
.dot.amber{background:#d4a84b}
.dot.cool{background:#5a7a8a}
#loading{text-align:center;padding:60px;color:#5c6a78}
#error{text-align:center;padding:40px;color:#e74c3c;display:none}
</style>
</head>
<body>
<div id="app">
  <h1><span>Styde Forge</span> — Agent Lifecycle Timeline</h1>
  <div class="sub">spawn → eval → improve → promote &middot; each track = one blueprint</div>
  <div id="stats"></div>
  <div id="controls">
    <button id="playBtn">▶ Play</button>
    <button id="resetViewBtn">⟲ Reset zoom</button>
    <span id="timeLabel">—</span>
    <div id="sliderWrap">
      <input type="range" id="scrubber" min="0" max="1000" value="0" step="1">
    </div>
  </div>
  <div id="legend">
    <span><span class="dot gold"></span>≥85 (production)</span>
    <span><span class="dot amber"></span>70–84</span>
    <span><span class="dot cool"></span>&lt;70</span>
    <span style="margin-left:auto;color:#5c6a78" id="eventCount">—</span>
  </div>
  <div id="timelineWrap">
    <svg id="timeline" xmlns="http://www.w3.org/2000/svg"></svg>
    <div id="loading">Loading state.yaml ...</div>
    <div id="error">Failed to load state.yaml. Open this file via a local HTTP server (python -m http.server) and ensure state.yaml is in the same directory.</div>
  </div>
  <div class="tooltip" id="tooltip"></div>
</div>
<script>
const MARGIN = { top: 20, right: 60, bottom: 20, left: 220 }
const TRACK_H = 36
const NODE_R = 7
const FONT_SIZE = 11
const MIN_TIMELINE_W = 1200
const svg = document.getElementById('timeline')
const scrubber = document.getElementById('scrubber')
const timeLabel = document.getElementById('timeLabel')
const playBtn = document.getElementById('playBtn')
const tooltip = document.getElementById('tooltip')
const loading = document.getElementById('loading')
const errorDiv = document.getElementById('error')
const statsDiv = document.getElementById('stats')
const eventCount = document.getElementById('eventCount')
let events = []
let blueprints = []
let tracks = {}
let timeMin = Infinity, timeMax = -Infinity
let timeRange = 0
let isPlaying = false
let playTimer = null
let currentFrame = 0
let animationId = null
function parseScore(detail) {
  const m = detail.match(/C:([\d.]+)/)
  if (m) return parseFloat(m[1])
  const m2 = detail.match(/(\d+[.]?\d*)\s*\/\s*100/)
  if (m2) return parseFloat(m2[1])
  const m3 = detail.match(/\(?(\d+[.]?\d)\)/)
  if (m3) return parseFloat(m3[1])
  const s = detail.match(/S:(\d+)/)
  const j = detail.match(/J:(\d+)/)
  if (s && j) return Math.round((parseInt(s[1]) + parseInt(j[1])) / 2 * 10) / 10
  return null
}
function scoreColor(score) {
  if (score === null) return '#5a7a8a'
  if (score >= 85) return '#e8c547'
  if (score >= 70) return '#d4a84b'
  return '#5a7a8a'
}
function scoreClass(score) {
  if (score === null) return 'cool'
  if (score >= 85) return 'gold'
  if (score >= 70) return 'amber'
  return 'cool'
}
function fmtTime(iso) {
  const d = new Date(iso)
  return d.toLocaleString('sv-SE', { month:'short', day:'2-digit', hour:'2-digit', minute:'2-digit' })
}
function fmtDateFull(iso) {
  const d = new Date(iso)
  return d.toLocaleString('sv-SE', { year:'numeric', month:'short', day:'2-digit', hour:'2-digit', minute:'2-digit', second:'2-digit' })
}
function parseStateYaml(text) {
  const lines = text.split('\n')
  const result = []
  let inActivity = false
  let inAgents = false
  let current = null
  let brace = 0
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    if (line.trim() === 'activity:') { inActivity = true; inAgents = false; continue }
    if (line.trim() === 'agents:') { inAgents = true; inActivity = false; continue }
    if (line.match(/^[a-z]/) && line.includes(':')) {
      if (line.startsWith('last_') || line.startsWith('total_') || line.startsWith('loop_') || line.startsWith('forge_') || line.startsWith('caveman_') || line.startsWith('hardware_') || line.startsWith('evaluations') || line.startsWith('blueprints') || line.startsWith('improvements') || line.startsWith('archive_entries')) {
        inActivity = false; inAgents = false
      }
    }
    if (!inActivity) continue
    if (line.startsWith('- action:')) {
      if (current) result.push(current)
      current = { action: line.split(':')[1].trim() }
    } else if (current) {
      const m = line.match(/^\s+(\w+):\s*(.+)/)
      if (m) {
        const key = m[1]
        let val = m[2].trim()
        if ((val.startsWith("'") && val.endsWith("'")) || (val.startsWith('"') && val.endsWith('"'))) val = val.slice(1,-1)
        if (key === 'id' || key === 'progress') val = parseInt(val)
        current[key] = val
      }
    }
  }
  if (current) result.push(current)
  const scoreKeys = ['S:', 'J:', 'C:']
  return result.filter(e => e.action && e.blueprint).map(e => {
    const score = parseScore(e.detail || '')
    return { ...e, score }
  })
}
function buildTimeline(data) {
  events = data.filter(e => e.timestamp)
  if (events.length === 0) return
  // sort by timestamp
  events.sort((a,b) => new Date(a.timestamp) - new Date(b.timestamp))
  // collect blueprints in order of first appearance
  const bpSet = new Set()
  blueprints = []
  for (const e of events) {
    if (!bpSet.has(e.blueprint)) {
      bpSet.add(e.blueprint)
      blueprints.push(e.blueprint)
    }
  }
  // time range
  timeMin = new Date(events[0].timestamp).getTime()
  timeMax = new Date(events[events.length-1].timestamp).getTime()
  timeRange = Math.max(timeMax - timeMin, 1)
  // index
  tracks = {}
  for (const bp of blueprints) {
    tracks[bp] = events.filter(e => e.blueprint === bp)
  }
  // set max on scrubber
  scrubber.max = events.length - 1
  render(events.length - 1)
  updateStats()
}
function render(frameIdx) {
  currentFrame = Math.min(frameIdx, events.length - 1)
  const visible = events.slice(0, currentFrame + 1)
  const currentTime = new Date(events[currentFrame].timestamp)
  // group visible by blueprint
  const visibleByBp = {}
  for (const e of visible) {
    if (!visibleByBp[e.blueprint]) visibleByBp[e.blueprint] = []
    visibleByBp[e.blueprint].push(e)
  }
  const visibleBps = Object.keys(visibleByBp)
  const totalH = MARGIN.top + visibleBps.length * TRACK_H + MARGIN.bottom
  // x scale: time
  const chartW = Math.max(MIN_TIMELINE_W, svg.parentElement.clientWidth - 10)
  const xScale = (t) => MARGIN.left + ((new Date(t).getTime() - timeMin) / timeRange) * (chartW - MARGIN.left - MARGIN.right)
  svg.setAttribute('width', chartW)
  svg.setAttribute('height', totalH)
  svg.innerHTML = ''
  // clip
  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs')
  const clip = document.createElementNS('http://www.w3.org/2000/svg', 'clipPath')
  clip.setAttribute('id', 'chartClip')
  const clipRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect')
  clipRect.setAttribute('x', MARGIN.left)
  clipRect.setAttribute('y', 0)
  clipRect.setAttribute('width', chartW - MARGIN.left - MARGIN.right + 10)
  clipRect.setAttribute('height', totalH)
  clip.appendChild(clipRect)
  defs.appendChild(clip)
  svg.appendChild(defs)
  const mainG = document.createElementNS('http://www.w3.org/2000/svg', 'g')
  mainG.setAttribute('clip-path', 'url(#chartClip)')
  svg.appendChild(mainG)
  // grid lines
  const gridCount = 8
  for (let i = 0; i <= gridCount; i++) {
    const t = timeMin + (timeRange / gridCount) * i
    const x = xScale(t)
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line')
    line.setAttribute('x1', x); line.setAttribute('y1', 0)
    line.setAttribute('x2', x); line.setAttribute('y2', totalH)
    line.setAttribute('stroke', '#1a2535')
    line.setAttribute('stroke-width', '1')
    mainG.appendChild(line)
    const lbl = document.createElementNS('http://www.w3.org/2000/svg', 'text')
    lbl.setAttribute('x', x); lbl.setAttribute('y', totalH - 4)
    lbl.setAttribute('fill', '#3a4a5a')
    lbl.setAttribute('font-size', '9px')
    lbl.setAttribute('text-anchor', 'middle')
    lbl.textContent = fmtTime(new Date(t).toISOString())
    mainG.appendChild(lbl)
  }
  // current time indicator
  const nowX = xScale(currentTime.toISOString())
  const nowLine = document.createElementNS('http://www.w3.org/2000/svg', 'line')
  nowLine.setAttribute('x1', nowX); nowLine.setAttribute('y1', 0)
  nowLine.setAttribute('x2', nowX); nowLine.setAttribute('y2', totalH)
  nowLine.setAttribute('stroke', '#e8c547')
  nowLine.setAttribute('stroke-width', '1.5')
  nowLine.setAttribute('stroke-dasharray', '4,3')
  nowLine.setAttribute('opacity', '0.7')
  mainG.appendChild(nowLine)
  // tracks
  visibleBps.forEach((bp, i) => {
    const y = MARGIN.top + i * TRACK_H
    const bpEvents = visibleByBp[bp]
    // track bg
    const bg = document.createElementNS('http://www.w3.org/2000/svg', 'rect')
    bg.setAttribute('x', MARGIN.left); bg.setAttribute('y', y)
    bg.setAttribute('width', chartW - MARGIN.left - MARGIN.right)
    bg.setAttribute('height', TRACK_H)
    bg.setAttribute('fill', i % 2 === 0 ? '#0f151c' : '#121a24')
    bg.setAttribute('rx', '2')
    mainG.appendChild(bg)
    // label
    const lbl = document.createElementNS('http://www.w3.org/2000/svg', 'text')
    lbl.setAttribute('x', MARGIN.left - 10)
    lbl.setAttribute('y', y + TRACK_H / 2 + 4)
    lbl.setAttribute('text-anchor', 'end')
    lbl.setAttribute('class', 'track-label')
    lbl.setAttribute('font-size', FONT_SIZE + 'px')
    const name = bp.length > 28 ? bp.slice(0, 26) + '…' : bp
    lbl.textContent = name
    lbl.setAttribute('data-bp', bp)
    lbl.addEventListener('click', () => {
      const idx = events.findIndex(e => e.blueprint === bp && e.timestamp)
      if (idx >= 0) { scrubber.value = idx; render(idx); updateTimeLabel(idx) }
    })
    mainG.appendChild(lbl)
    // connection line between nodes
    if (bpEvents.length > 1) {
      const sorted = [...bpEvents].sort((a,b) => new Date(a.timestamp) - new Date(b.timestamp))
      for (let j = 1; j < sorted.length; j++) {
        const x1 = xScale(sorted[j-1].timestamp)
        const x2 = xScale(sorted[j].timestamp)
        const conn = document.createElementNS('http://www.w3.org/2000/svg', 'line')
        conn.setAttribute('x1', x1); conn.setAttribute('y1', y + TRACK_H / 2)
        conn.setAttribute('x2', x2); conn.setAttribute('y2', y + TRACK_H / 2)
        conn.setAttribute('stroke', '#2a3a4d')
        conn.setAttribute('stroke-width', '1.5')
        conn.setAttribute('opacity', '0.5')
        mainG.appendChild(conn)
      }
    }
    // nodes
    bpEvents.forEach(e => {
      const cx = xScale(e.timestamp)
      const cy = y + TRACK_H / 2
      const sc = e.score
      const isComplete = e.status === 'complete'
      // outer ring for active/running
      if (e.status === 'running') {
        const ring = document.createElementNS('http://www.w3.org/2000/svg', 'circle')
        ring.setAttribute('cx', cx); ring.setAttribute('cy', cy)
        ring.setAttribute('r', NODE_R + 3)
        ring.setAttribute('fill', 'none')
        ring.setAttribute('stroke', '#e8c547')
        ring.setAttribute('stroke-width', '1.5')
        ring.setAttribute('stroke-dasharray', '3,2')
        ring.setAttribute('opacity', '0.6')
        mainG.appendChild(ring)
      }
      const scClass = scoreClass(sc)
      const color = scoreColor(sc)
      const node = document.createElementNS('http://www.w3.org/2000/svg', 'g')
      node.setAttribute('class', 'node')
      node.style.opacity = isComplete ? '0.85' : '1'
      // shape by action
      if (e.action === 'spawn') {
        const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect')
        rect.setAttribute('x', cx - 7); rect.setAttribute('y', cy - 7)
        rect.setAttribute('width', 14); rect.setAttribute('height', 14)
        rect.setAttribute('fill', color)
        rect.setAttribute('rx', '2')
        node.appendChild(rect)
      } else if (e.action === 'improve') {
        const tri = document.createElementNS('http://www.w3.org/2000/svg', 'polygon')
        const pts = `${cx},${cy-8} ${cx+7},${cy+5} ${cx-7},${cy+5}`
        tri.setAttribute('points', pts)
        tri.setAttribute('fill', color)
        node.appendChild(tri)
      } else {
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle')
        circle.setAttribute('cx', cx); circle.setAttribute('cy', cy)
        circle.setAttribute('r', NODE_R)
        circle.setAttribute('fill', color)
        node.appendChild(circle)
      }
      // if score is available, show it
      if (sc !== null && isComplete) {
        const lbl2 = document.createElementNS('http://www.w3.org/2000/svg', 'text')
        lbl2.setAttribute('x', cx)
        lbl2.setAttribute('y', cy + 3)
        lbl2.setAttribute('class', 'node-label')
        lbl2.setAttribute('font-size', '8px')
        lbl2.textContent = Math.round(sc)
        node.appendChild(lbl2)
      }
      node.addEventListener('click', (ev) => showTooltip(e, ev))
      node.addEventListener('mouseenter', (ev) => {
        node.style.opacity = '1'
        const sc2 = e.score
        const color2 = scoreColor(sc2)
        if (sc2 !== null) {
          const lbl2 = document.createElementNS('http://www.w3.org/2000/svg', 'text')
          lbl2.setAttribute('x', cx); lbl2.setAttribute('y', cy - NODE_R - 6)
          lbl2.setAttribute('text-anchor', 'middle')
          lbl2.setAttribute('fill', color2)
          lbl2.setAttribute('font-size', '10px')
          lbl2.setAttribute('font-weight', 'bold')
          lbl2.setAttribute('class', 'hover-score')
          lbl2.textContent = sc2.toFixed(1)
          node.appendChild(lbl2)
        }
      })
      node.addEventListener('mouseleave', () => {
        node.style.opacity = isComplete ? '0.85' : '1'
        const hs = node.querySelector('.hover-score')
        if (hs) hs.remove()
      })
      mainG.appendChild(node)
    })
  })
}
function showTooltip(e, ev) {
  const sc = e.score
  const scCls = scoreClass(sc)
  const color = scoreColor(sc)
  const scStr = sc !== null ? sc.toFixed(1) : '—'
  const detailStr = e.detail || '—'
  tooltip.innerHTML = `
    <h3>${e.blueprint}</h3>
    <div class="score ${scCls}">C: ${scStr}</div>
    <div class="row"><span>Action</span><span class="val">${e.action}</span></div>
    <div class="row"><span>Run ID</span><span class="val">${e.id}</span></div>
    <div class="row"><span>Status</span><span class="val">${e.status}</span></div>
    <div class="row"><span>Progress</span><span class="val">${e.progress}%</span></div>
    <div class="row"><span>Time</span><span class="val">${fmtDateFull(e.timestamp)}</span></div>
    <div style="margin-top:6px;padding-top:6px;border-top:1px solid #2a3a4d;font-size:11px;color:#8a9aa8;word-break:break-word">${detailStr.length > 120 ? detailStr.slice(0,120)+'…' : detailStr}</div>
  `
  tooltip.classList.add('show')
  let tx = ev.clientX + 12
  let ty = ev.clientY - 10
  const tw = tooltip.offsetWidth
  const th = tooltip.offsetHeight
  if (tx + tw > window.innerWidth - 10) tx = ev.clientX - tw - 12
  if (ty + th > window.innerHeight - 10) ty = window.innerHeight - th - 10
  if (ty < 10) ty = 10
  tooltip.style.left = tx + 'px'
  tooltip.style.top = ty + 'px'
}
function updateTimeLabel(idx) {
  if (idx < 0 || idx >= events.length) return
  const e = events[idx]
  const pct = currentFrame / (events.length - 1) * 100
  timeLabel.textContent = `${fmtDateFull(e.timestamp)}  (${Math.round(pct)}%)`
}
function updateStats() {
  const total = events.length
  const complete = events.filter(e => e.status === 'complete').length
  const running = events.filter(e => e.status === 'running').length
  const scored = events.filter(e => e.score !== null)
  const gold = scored.filter(e => e.score >= 85).length
  const amber = scored.filter(e => e.score >= 70 && e.score < 85).length
  const cool = scored.filter(e => e.score < 70).length
  const bps = blueprints.length
  const spawns = events.filter(e => e.action === 'spawn').length
  const evals2 = events.filter(e => e.action === 'eval').length
  const improves = events.filter(e => e.action === 'improve').length
  eventCount.textContent = `${total} events · ${bps} blueprints · ${spawns} spawn · ${evals2} eval · ${improves} improve`
  statsDiv.innerHTML = `
    <span>${total} events</span>
    <span>${bps} blueprints</span>
    <span>${complete} complete / ${running} running</span>
    <span>★ ${gold} gold</span>
    <span>◆ ${amber} amber</span>
    <span>○ ${cool} cool</span>
  `
}
function animate() {
  if (!isPlaying) return
  const next = currentFrame + 1
  if (next >= events.length) {
    isPlaying = false
    playBtn.textContent = '▶ Play'
    playBtn.classList.remove('active')
    return
  }
  scrubber.value = next
  render(next)
  updateTimeLabel(next)
  if (isPlaying) {
    animationId = requestAnimationFrame(animate)
  }
}
playBtn.addEventListener('click', () => {
  isPlaying = !isPlaying
  if (isPlaying) {
    if (currentFrame >= events.length - 1) { scrubber.value = 0; render(0); updateTimeLabel(0) }
    playBtn.textContent = '⏸ Pause'
    playBtn.classList.add('active')
    animationId = requestAnimationFrame(animate)
  } else {
    playBtn.textContent = '▶ Play'
    playBtn.classList.remove('active')
    if (animationId) cancelAnimationFrame(animationId)
  }
})
scrubber.addEventListener('input', () => {
  if (isPlaying) {
    isPlaying = false
    playBtn.textContent = '▶ Play'
    playBtn.classList.remove('active')
    if (animationId) cancelAnimationFrame(animationId)
  }
  const idx = parseInt(scrubber.value)
  render(idx)
  updateTimeLabel(idx)
})
document.addEventListener('click', (e) => {
  if (!tooltip.contains(e.target) && !e.target.closest('.node')) {
    tooltip.classList.remove('show')
  }
})
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') tooltip.classList.remove('show')
})
resetViewBtn.addEventListener('click', () => {
  scrubber.value = events.length - 1
  render(events.length - 1)
  updateTimeLabel(events.length - 1)
})
// load data
fetch('state.yaml')
  .then(r => {
    if (!r.ok) throw new Error('HTTP ' + r.status)
    return r.text()
  })
  .then(text => {
    loading.style.display = 'none'
    const data = parseStateYaml(text)
    if (data.length === 0) throw new Error('No events found')
    buildTimeline(data)
  })
  .catch(err => {
    loading.style.display = 'none'
    errorDiv.style.display = 'block'
    errorDiv.textContent = 'Failed to load state.yaml: ' + err.message + '. Make sure you are serving this page via a local HTTP server (python -m http.server) and state.yaml is in the same directory.'
  })
</script>
</body>
</html>
```
The HTML above is a self-contained Agent Lifecycle Timeline viewer.
Save it as `timeline.html` in E:\Stryde\_alpedal\styde-forge\, then serve with:
```
python -m http.server 8768
```
Open http://localhost:8768/timeline.html in your browser.
Features:
- Parses your 15K-line state.yaml live via fetch
- One horizontal track per blueprint (color-palette-originator, agent-lifecycle-timeline, aesthetic-style-composer, etc.)
- Nodes shaped by action: circle=eval, square=spawn, triangle=improve
- Color: gold ≥85, amber 70–84, cool <70; score number rendered inside each node
- Connection lines trace each blueprint's progression across time
- Drag scrubber to step through events in chronological order
- Play/pause auto-replays the full timeline from start to now
- Click any node for detail popup: run_id, action, score, status, timestamp, detail text
- Stats bar shows event counts, gold/amber/cool distribution
- Current time indicator line slides across as you scrub