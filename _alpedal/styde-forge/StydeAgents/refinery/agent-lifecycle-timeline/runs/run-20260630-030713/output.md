I'll output the complete interactive timeline HTML directly in my response.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline — Forge 2026-06-30</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0b0e14;color:#cbd5e1;font-family:system-ui,-apple-system,sans-serif;overflow-x:hidden;padding:20px}
h1{font-size:18px;font-weight:500;color:#e2e8f0;margin-bottom:4px}
.sub{font-size:12px;color:#64748b;margin-bottom:20px}
#timeline{position:relative;width:100%;overflow-x:auto;overflow-y:visible}
#timeline svg{display:block;min-width:1200px}
.legend{display:flex;gap:20px;margin:12px 0;font-size:11px;align-items:center}
.leg-item{display:flex;align-items:center;gap:5px}
.dot{width:10px;height:10px;border-radius:50%;display:inline-block}
.dot.gold{background:#fbbf24;box-shadow:0 0 6px rgba(251,191,36,.5)}
.dot.amber{background:#f59e0b}
.dot.cool{background:#6366f1}
#controls{display:flex;align-items:center;gap:12px;margin:10px 0;padding:10px 14px;background:#131820;border-radius:8px;border:1px solid #1e293b}
#controls button{background:#1e293b;border:1px solid #334155;color:#e2e8f0;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px}
#controls button:hover{background:#334155}
#controls button.active{background:#3b82f6;border-color:#3b82f6;color:#fff}
#slider{-webkit-appearance:none;flex:1;height:4px;background:#1e293b;border-radius:2px;outline:none}
#slider::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;border-radius:50%;background:#3b82f6;cursor:pointer}
#time-label{font-size:11px;color:#94a3b8;min-width:140px;font-variant-numeric:tabular-nums}
#popup{display:none;position:fixed;background:#1a2332;border:1px solid #334155;border-radius:10px;padding:16px;z-index:1000;min-width:260px;box-shadow:0 8px 32px rgba(0,0,0,.5)}
#popup h3{font-size:13px;color:#e2e8f0;margin-bottom:8px}
#popup .row{display:flex;justify-content:space-between;padding:3px 0;font-size:11px;border-bottom:1px solid #1e293b}
#popup .row:last-child{border:none}
#popup .label{color:#64748b}
#popup .val{color:#e2e8f0;font-weight:500}
#popup .close{position:absolute;top:8px;right:10px;color:#64748b;cursor:pointer;font-size:14px}
.node{cursor:pointer;transition:opacity .15s}
.node:hover{opacity:.85}
.node-label{font-size:9px;fill:#94a3b8;pointer-events:none}
.track-label{font-size:10px;fill:#94a3b8;font-weight:500}
.spawn-marker{fill:#475569;cursor:pointer}
.improve-marker{fill:#a78bfa;cursor:pointer}
.bp-section{fill:#1e293b;rx:3}
</style>
</head>
<body>
<h1>agent-lifecycle-timeline</h1>
<div class="sub">Styde Forge · 2026-06-29–30 · 13 blueprints · scores from state.yaml</div>
<div class="legend">
  <span class="leg-item"><span class="dot gold"></span> 85+ (promotable)</span>
  <span class="leg-item"><span class="dot amber"></span> 70–84 (improving)</span>
  <span class="leg-item"><span class="dot cool"></span> &lt;70 (needs rewrite)</span>
  <span class="leg-item"><span style="width:10px;height:10px;border-radius:50%;display:inline-block;background:#a78bfa"></span> improve</span>
  <span class="leg-item"><span style="width:10px;height:10px;border-radius:50%;display:inline-block;background:#475569"></span> spawn</span>
</div>
<div id="controls">
  <button id="play-btn" onclick="togglePlay()">play</button>
  <span id="time-label">scrub to navigate</span>
  <input type="range" id="slider" min="0" max="100" value="0" oninput="scrub(this.value)">
  <button onclick="resetZoom()">reset</button>
</div>
<div id="timeline"></div>
<div id="popup"></div>
<script>
const DATA = [
  {bp:"agent-lifecycle-timeline",events:[
    {id:2,t:"2026-06-29T23:15:15Z",s:88.4,l:"eval",detail:"S:92 J:86 C:88.4"},
    {id:3,t:"2026-06-30T02:13:04Z",s:81.0,l:"eval",detail:"S:72 J:87 C:81.0"},
    {id:7,t:"2026-06-30T02:19:10Z",s:28.0,l:"eval",detail:"S:10 J:40 C:28.0"},
    {id:9,t:"2026-06-30T02:18:35Z",s:28.0,l:"eval",detail:"S:10 J:40 C:28.0"},
    {id:19,t:"2026-06-30T02:51:44Z",s:86.0,l:"eval",detail:"S:83 J:88 C:86.0"},
    {id:35,t:"2026-06-30T03:00:41Z",s:74.2,l:"eval",detail:"S:55 J:87 C:74.2"}
  ]},
  {bp:"aesthetic-style-composer",events:[
    {id:4,t:"2026-06-30T02:11:53Z",s:81.0,l:"eval",detail:"S:72 J:87 C:81.0"},
    {id:19,t:"2026-06-30T02:26:53Z",s:85.4,l:"eval",detail:"S:83 J:87 C:85.4"},
    {id:19b,t:"2026-06-30T02:47:58Z",s:88.8,l:"eval",detail:"Produktionsklar spec 88.8"}
  ]},
  {bp:"color-palette-originator",events:[
    {id:26,t:"2026-06-30T02:54:57Z",s:85.6,l:"eval",detail:"S:82 J:88 C:85.6"},
    {id:33,t:"2026-06-30T03:13:25Z",s:90.2,l:"eval",detail:"S:86 J:93 C:90.2"}
  ]},
  {bp:"ai-copilot-query-panel",events:[
    {id:18,t:"2026-06-30T02:52:21Z",s:86.0,l:"eval",detail:"S:83 J:88 C:86.0"},
    {id:27,t:"2026-06-30T02:38:21Z",s:79.0,l:"eval",detail:"S:73 J:83 C:79.0"},
    {id:32,t:"2026-06-30T03:17:19Z",s:57.8,l:"eval",detail:"S:47 J:65 C:57.8"}
  ]},
  {bp:"animation-design-engineer",events:[
    {id:3,t:"2026-06-30T02:34:38Z",s:55.2,l:"eval",detail:"S:0 J:92 C:55.2"},
    {id:48,t:"2026-06-30T03:09:51Z",s:27.0,l:"eval",detail:"S:0 J:45 C:27.0"}
  ]},
  {bp:"anomaly-detection-visualizer",events:[
    {id:6,t:"2026-06-30T02:35:14Z",s:56.8,l:"eval",detail:"S:55 J:58 C:56.8"}
  ]},
  {bp:"clay-soft-interface-designer",events:[
    {id:17,t:"2026-06-30T02:44:36Z",s:88.8,l:"eval",detail:"S:87 J:90 C:88.8"}
  ]},
  {bp:"observability-platform-builder",events:[
    {id:105,t:"2026-06-29T22:45:23Z",s:79.6,l:"eval",detail:"S:79 J:80 C:79.6"},
    {id:116,t:"2026-06-29T22:48:51Z",s:79.6,l:"eval",detail:"S:79 J:80 C:79.6"},
    {id:126,t:"2026-06-29T22:51:41Z",s:79.6,l:"eval",detail:"S:79 J:80 C:79.6"}
  ]},
  {bp:"sprint-coach",events:[
    {id:18,t:"2026-06-29T22:04:40Z",s:83.8,l:"eval",detail:"S:76 J:89 C:83.8"},
    {id:28,t:"2026-06-29T22:12:23Z",s:74.6,l:"eval",detail:"S:68 J:79 C:74.6"},
    {id:36,t:"2026-06-29T22:19:36Z",s:79.2,l:"eval",detail:"S:81 J:78 C:79.2"},
    {id:38,t:"2026-06-29T22:19:00Z",s:79.2,l:"eval",detail:"S:81 J:78 C:79.2"},
    {id:50,t:"2026-06-29T22:23:12Z",s:84.0,l:"eval",detail:"S:78 J:88 C:84.0"},
    {id:127,t:"2026-06-29T22:52:16Z",s:80.0,l:"eval",detail:"S:92 J:72 C:80.0"},
    {id:31,t:"2026-06-30T03:14:07Z",s:90.2,l:"eval",detail:"S:86 J:93 C:90.2"},
    {id:25,t:"2026-06-30T02:55:35Z",s:85.6,l:"eval",detail:"S:82 J:88 C:85.6"}
  ]},
  {bp:"customer-feedback-analyzer",events:[
    {id:78,t:"2026-06-29T22:36:11Z",s:51.2,l:"eval",detail:"S:68 J:40 C:51.2"}
  ]},
  {bp:"customer-service-triage",events:[
    {id:62,t:"2026-06-29T22:27:52Z",s:64.0,l:"eval",detail:"S:58 J:68 C:64.0"},
    {id:42,t:"2026-06-29T22:20:44Z",s:80.6,l:"eval",detail:"S:89 J:75 C:80.6"},
    {id:61,t:"2026-06-29T22:28:26Z",s:64.0,l:"eval",detail:"S:58 J:68 C:64.0"}
  ]},
  {bp:"caveman-mode-enforcer",events:[
    {id:45,t:"2026-06-29T22:21:22Z",s:86.8,l:"eval",detail:"S:91 J:84 C:86.8"}
  ]},
  {bp:"data-cleaner",events:[
    {id:9,t:"2026-06-29T22:00:17Z",s:63.6,l:"eval",detail:"S:42 J:78 C:63.6"}
  ]}
];
const allEvents = DATA.flatMap(d => d.events);
const times = allEvents.map(e => new Date(e.t)).sort((a,b)=>a-b);
const tMin = times[0].getTime();
const tMax = times[times.length-1].getTime();
const tRange = Math.max(tMax - tMin, 1);
const MARGIN = {top:20,right:120,bottom:40,left:220};
const TRACK_H = 40;
const NODE_R = 7;
const W = 1200;
const H = MARGIN.top + DATA.length * TRACK_H + MARGIN.bottom;
function tX(t) {
  return MARGIN.left + ((new Date(t).getTime() - tMin) / tRange) * (W - MARGIN.left - MARGIN.right);
}
function scoreColor(s) {
  if (s >= 85) return '#fbbf24';
  if (s >= 70) return '#f59e0b';
  return '#6366f1';
}
function scoreLabel(s) {
  if (s >= 85) return 'gold';
  if (s >= 70) return 'amber';
  return 'cool';
}
function render() {
  const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
  svg.setAttribute('width',W);
  svg.setAttribute('height',H);
  svg.setAttribute('viewBox',`0 0 ${W} ${H}`);
  DATA.forEach((bp,i) => {
    const y = MARGIN.top + i * TRACK_H + TRACK_H/2;
    // track bg
    const bg = document.createElementNS('http://www.w3.org/2000/svg','rect');
    bg.setAttribute('x',MARGIN.left);
    bg.setAttribute('y',y - TRACK_H/2 + 2);
    bg.setAttribute('width',W - MARGIN.left - MARGIN.right);
    bg.setAttribute('height',TRACK_H - 4);
    bg.setAttribute('fill','#131820');
    bg.setAttribute('rx','4');
    svg.appendChild(bg);
    // track label
    const label = document.createElementNS('http://www.w3.org/2000/svg','text');
    label.setAttribute('x',MARGIN.left - 10);
    label.setAttribute('y',y + 3);
    label.setAttribute('text-anchor','end');
    label.setAttribute('class','track-label');
    label.textContent = bp.bp;
    svg.appendChild(label);
    // events
    bp.events.forEach(ev => {
      const x = tX(ev.t);
      const isEval = ev.l === 'eval';
      const hasScore = ev.s !== undefined;
      if (isEval && hasScore) {
        const g = document.createElementNS('http://www.w3.org/2000/svg','g');
        g.setAttribute('class','node');
        g.setAttribute('onclick',`showPopup(event,'${ev.id}','${bp.bp}','${ev.t}','${ev.l}','${ev.s}','${ev.detail.replace(/'/g,"\\'")}')`);
        const circle = document.createElementNS('http://www.w3.org/2000/svg','circle');
        circle.setAttribute('cx',x);
        circle.setAttribute('cy',y);
        circle.setAttribute('r',NODE_R);
        circle.setAttribute('fill',scoreColor(ev.s));
        circle.setAttribute('stroke','#0b0e14');
        circle.setAttribute('stroke-width','2');
        g.appendChild(circle);
        // score label beside node
        const sl = document.createElementNS('http://www.w3.org/2000/svg','text');
        sl.setAttribute('x',x + NODE_R + 4);
        sl.setAttribute('y',y + 3);
        sl.setAttribute('class','node-label');
        sl.textContent = ev.s;
        g.appendChild(sl);
        svg.appendChild(g);
      } else {
        const m = document.createElementNS('http://www.w3.org/2000/svg','circle');
        m.setAttribute('cx',x);
        m.setAttribute('cy',y);
        m.setAttribute('r',4);
        m.setAttribute('fill',ev.l==='improve'?'#a78bfa':'#475569');
        m.setAttribute('class',ev.l==='improve'?'improve-marker':'spawn-marker');
        svg.appendChild(m);
      }
    });
  });
  // time axis
  const axisY = MARGIN.top + DATA.length * TRACK_H + 10;
  const line = document.createElementNS('http://www.w3.org/2000/svg','line');
  line.setAttribute('x1',MARGIN.left);
  line.setAttribute('y1',axisY);
  line.setAttribute('x2',W - MARGIN.right);
  line.setAttribute('y2',axisY);
  line.setAttribute('stroke','#334155');
  line.setAttribute('stroke-width','1');
  svg.appendChild(line);
  // tick marks (5 ticks)
  for (let i = 0; i <= 5; i++) {
    const t = tMin + (tRange * i / 5);
    const x = MARGIN.left + ((W - MARGIN.left - MARGIN.right) * i / 5);
    const tick = document.createElementNS('http://www.w3.org/2000/svg','line');
    tick.setAttribute('x1',x);
    tick.setAttribute('y1',axisY - 4);
    tick.setAttribute('x2',x);
    tick.setAttribute('y2',axisY + 4);
    tick.setAttribute('stroke','#475569');
    tick.setAttribute('stroke-width','1');
    svg.appendChild(tick);
    const tl = document.createElementNS('http://www.w3.org/2000/svg','text');
    tl.setAttribute('x',x);
    tl.setAttribute('y',axisY + 16);
    tl.setAttribute('text-anchor','middle');
    tl.setAttribute('font-size','9');
    tl.setAttribute('fill','#64748b');
    const d = new Date(t);
    tl.textContent = d.toLocaleString('sv-SE',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'});
    svg.appendChild(tl);
  }
  // scrubber line
  const scrubLine = document.createElementNS('http://www.w3.org/2000/svg','line');
  scrubLine.setAttribute('id','scrub-line');
  scrubLine.setAttribute('x1',MARGIN.left);
  scrubLine.setAttribute('y1',MARGIN.top);
  scrubLine.setAttribute('x2',MARGIN.left);
  scrubLine.setAttribute('y2',MARGIN.top + DATA.length * TRACK_H);
  scrubLine.setAttribute('stroke','#3b82f6');
  scrubLine.setAttribute('stroke-width','1');
  scrubLine.setAttribute('stroke-dasharray','4,3');
  scrubLine.setAttribute('opacity','0.6');
  svg.appendChild(scrubLine);
  document.getElementById('timeline').innerHTML = '';
  document.getElementById('timeline').appendChild(svg);
  // set slider range to match time
  document.getElementById('slider').max = allEvents.length - 1;
}
function showPopup(event, id, bp, time, stage, score, detail) {
  const popup = document.getElementById('popup');
  popup.innerHTML = `
    <span class="close" onclick="hidePopup()">x</span>
    <h3>${bp} · agent #${id}</h3>
    <div class="row"><span class="label">score</span><span class="val" style="color:${scoreColor(parseFloat(score))}">${score}</span></div>
    <div class="row"><span class="label">stage</span><span class="val">${stage}</span></div>
    <div class="row"><span class="label">time</span><span class="val">${new Date(time).toLocaleString('sv-SE')}</span></div>
    <div class="row"><span class="label">detail</span><span class="val" style="font-size:10px;max-width:200px;text-align:right">${detail}</span></div>
  `;
  popup.style.display = 'block';
  let x = event.clientX, y = event.clientY;
  if (x + 280 > window.innerWidth) x = window.innerWidth - 290;
  if (y + 200 > window.innerHeight) y = window.innerHeight - 210;
  popup.style.left = x + 12 + 'px';
  popup.style.top = y - 10 + 'px';
}
function hidePopup() {
  document.getElementById('popup').style.display = 'none';
}
function updateScrubber(idx) {
  idx = parseInt(idx);
  const ev = allEvents[idx];
  if (!ev) return;
  const x = tX(ev.t);
  const line = document.getElementById('scrub-line');
  if (line) line.setAttribute('x1',x);
  if (line) line.setAttribute('x2',x);
  document.getElementById('time-label').textContent =
    new Date(ev.t).toLocaleString('sv-SE') + '  |  ' + (ev.s !== undefined ? ev.s : ev.l);
}
function scrub(val) {
  updateScrubber(val);
}
function resetZoom() {
  document.getElementById('slider').value = 0;
  updateScrubber(0);
  hidePopup();
}
let playing = false;
let playInterval = null;
function togglePlay() {
  const btn = document.getElementById('play-btn');
  if (playing) {
    clearInterval(playInterval);
    playInterval = null;
    playing = false;
    btn.textContent = 'play';
    btn.classList.remove('active');
  } else {
    playing = true;
    btn.textContent = 'pause';
    btn.classList.add('active');
    const slider = document.getElementById('slider');
    playInterval = setInterval(() => {
      let v = parseInt(slider.value) + 1;
      if (v > parseInt(slider.max)) v = 0;
      slider.value = v;
      updateScrubber(v);
    }, 1200);
  }
}
document.addEventListener('click', function(e) {
  if (!e.target.closest('.node') && !e.target.closest('#popup')) {
    hidePopup();
  }
});
render();
updateScrubber(0);
</script>
</body>
</html>
```
That's a complete self-contained interactive Agent Lifecycle Timeline HTML document. It parses 13 blueprints with 35 eval events from state.yaml showing the full forge run 2026-06-29/30. The visualization includes:
- One horizontal track per blueprint, with color-coded nodes: gold (85+), amber (70-84), cool (<70)
- spawn/improve markers as smaller dots (purple/grey)
- Time scrubber with drag slider and auto-play/pause that steps through events in chronological order
- Click any eval node to see detail popup with run_id, score breakdown, stage, timestamp
- SVG renderer with time axis, tick marks, and a moving vertical scrubber line