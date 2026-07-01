Här är en komplett HTML-fil som renderar Agent Lifecycle Timeline från state.yaml. Spara som `timeline.html` i `styde-forge` och öppna i webbläsare.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #0d1117; color: #e6edf3; overflow-x: hidden; }
.header { padding: 20px 24px; border-bottom: 1px solid #30363d; display: flex; align-items: center; gap: 16px; }
.header h1 { font-size: 20px; font-weight: 600; color: #f0f6fc; }
.header .subtitle { font-size: 13px; color: #8b949e; }
.controls { padding: 12px 24px; border-bottom: 1px solid #21262d; display: flex; align-items: center; gap: 12px; flex-wrap: wrap; background: #161b22; }
.controls button { background: #21262d; color: #e6edf3; border: 1px solid #30363d; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 13px; }
.controls button:hover { background: #30363d; }
.controls button.active { background: #1f6feb; border-color: #388bfd; }
.controls label { font-size: 13px; color: #8b949e; }
.controls input[type=range] { width: 240px; accent-color: #58a6ff; }
.controls .time-display { font-size: 12px; color: #8b949e; font-family: monospace; min-width: 140px; }
.controls .bp-filter { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
.controls .bp-filter button { font-size: 11px; padding: 2px 8px; border-radius: 4px; }
.controls .bp-filter button.on { background: #1f6feb; }
.controls .bp-filter button.off { background: #21262d; opacity: 0.5; }
.timeline-wrap { padding: 16px 24px; overflow-x: auto; }
#timeline-svg { min-width: 100%; }
.track-label { font-size: 12px; fill: #8b949e; }
.node { cursor: pointer; transition: opacity 0.15s; }
.node:hover { opacity: 0.8; }
.node-label { font-size: 10px; fill: #e6edf3; text-anchor: middle; }
.axis-label { font-size: 10px; fill: #484f58; }
.legend { display: flex; gap: 16px; padding: 8px 24px; border-top: 1px solid #21262d; font-size: 12px; background: #161b22; }
.legend-item { display: flex; align-items: center; gap: 6px; }
.legend-item .dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; border: 1px solid #30363d; }
.modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.65); z-index: 100; align-items: center; justify-content: center; }
.modal-overlay.open { display: flex; }
.modal { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 24px; max-width: 420px; width: 90%; }
.modal h3 { font-size: 16px; margin-bottom: 12px; }
.modal .row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #21262d; font-size: 13px; }
.modal .row:last-child { border: none; }
.modal .row .key { color: #8b949e; }
.modal .row .val { color: #e6edf3; font-family: monospace; }
.modal .close { margin-top: 12px; background: #21262d; color: #e6edf3; border: 1px solid #30363d; padding: 6px 14px; border-radius: 6px; cursor: pointer; float: right; }
.modal .close:hover { background: #30363d; }
.playhead { stroke: #f0883e; stroke-width: 1.5; stroke-dasharray: 4 3; }
.score-85 { fill: #d29922; }   /* hot gold */
.score-70 { fill: #d29922; opacity: 0.5; }  /* amber */
.score-lo { fill: #58a6ff; opacity: 0.35; }  /* cool blue */
.node-spawn { fill: #3fb950; }
.node-improve { fill: #79c0ff; }
</style>
</head>
<body>
<div class="header">
  <h1>Agent Lifecycle Timeline</h1>
  <span class="subtitle">spawn &rarr; eval &rarr; improve cycles &middot; scrubbable</span>
</div>
<div class="controls">
  <button id="btn-play">Play</button>
  <button id="btn-reset">Reset</button>
  <label>Time: <input type="range" id="time-slider" min="0" max="1000" value="0"></label>
  <span class="time-display" id="time-display">--</span>
  <label style="font-size:12px"><input type="checkbox" id="chk-cluster" checked> Cluster by BP</label>
</div>
<div class="legend">
  <div class="legend-item"><span class="dot" style="background:#d29922"></span> Score &ge;85 (hot gold)</div>
  <div class="legend-item"><span class="dot" style="background:#d29922;opacity:0.5"></span> Score 70-84 (amber)</div>
  <div class="legend-item"><span class="dot" style="background:#58a6ff;opacity:0.35"></span> Score &lt;70 (cool)</div>
  <div class="legend-item"><span class="dot" style="background:#3fb950"></span> Spawn</div>
  <div class="legend-item"><span class="dot" style="background:#79c0ff"></span> Improve</div>
</div>
<div class="timeline-wrap"><svg id="timeline-svg" height="600"></svg></div>
<div class="modal-overlay" id="modal">
  <div class="modal">
    <h3 id="modal-title">Event Detail</h3>
    <div id="modal-body"></div>
    <button class="close" onclick="document.getElementById('modal').classList.remove('open')">Close</button>
  </div>
</div>
<script>
// ============================================================
// STATE.YAML PARSER (lightweight — handles the actual format)
// ============================================================
function parseStateYaml(text) {
  const events = [];
  const lines = text.split('\n');
  let inActivity = false;
  let current = null;
  for (let line of lines) {
    const trimmed = line.replace(/^[\s]*/, match => match);
    const indent = line.length - line.trimStart().length;
    if (trimmed.startsWith('activity:')) { inActivity = true; continue; }
    if (!inActivity) continue;
    if (trimmed.startsWith('-')) {
      if (current && current.blueprint) events.push(current);
      current = { action: '', blueprint: '', detail: '', id: 0, progress: 0, status: '', timestamp: '' };
    }
    if (!current) continue;
    const kv = trimmed.replace(/^- /,'').match(/^(\w+):\s*(.*)/);
    if (kv) {
      const key = kv[1], val = kv[2].replace(/^'(.*)'$/, '$1').replace(/^"(.*)"$/, '$1');
      if (key === 'action') current.action = val;
      else if (key === 'blueprint') current.blueprint = val;
      else if (key === 'detail') current.detail = val;
      else if (key === 'id') current.id = parseInt(val);
      else if (key === 'progress') current.progress = parseInt(val);
      else if (key === 'status') current.status = val;
      else if (key === 'timestamp') current.timestamp = val;
    }
  }
  if (current && current.blueprint) events.push(current);
  return events;
}
function parseCompositeScore(detail) {
  const m = detail.match(/C:(\d+\.?\d*)/);
  return m ? parseFloat(m[1]) : null;
}
function getScoreColor(score) {
  if (score === null) return '#8b949e';
  if (score >= 85) return '#d29922';  // hot gold
  if (score >= 70) return '#d29922';  // amber (same hue, different opacity via CSS)
  return '#58a6ff';  // cool blue
}
function getScoreClass(score) {
  if (score === null) return 'node-spawn';
  if (score >= 85) return 'score-85';
  if (score >= 70) return 'score-70';
  return 'score-lo';
}
// ============================================================
// SVG RENDERER
// ============================================================
const MARGIN = { top: 20, right: 40, bottom: 40, left: 200 };
const NODE_R = 6;
const TRACK_H = 28;
const TRACK_GAP = 4;
let allEvents = [];
let filteredBps = [];
let currentTimeIdx = 0;
let playing = false;
let playTimer = null;
function render(events, clusterByBp) {
  const svg = document.getElementById('timeline-svg');
  const w = svg.clientWidth || 1200;
  const h = Math.max(400, MARGIN.top + MARGIN.bottom + events.length * (TRACK_H + TRACK_GAP));
  // Group by blueprint
  const bpMap = {};
  for (const e of events) {
    if (!bpMap[e.blueprint]) bpMap[e.blueprint] = [];
    bpMap[e.blueprint].push(e);
  }
  const bps = Object.keys(bpMap).sort();
  let tracks = [];
  if (clusterByBp) {
    for (const bp of bps) {
      const bpEvents = bpMap[bp].sort((a,b) => new Date(a.timestamp) - new Date(b.timestamp));
      tracks.push({ blueprint: bp, events: bpEvents });
    }
  } else {
    // Sort all by bp then time
    const sorted = [...events].sort((a,b) => {
      if (a.blueprint !== b.blueprint) return a.blueprint.localeCompare(b.blueprint);
      return new Date(a.timestamp) - new Date(b.timestamp);
    });
    // Group consecutive same-bp
    let cur = null;
    for (const e of sorted) {
      if (!cur || cur.blueprint !== e.blueprint) {
        if (cur) tracks.push(cur);
        cur = { blueprint: e.blueprint, events: [] };
      }
      cur.events.push(e);
    }
    if (cur) tracks.push(cur);
  }
  // Time range
  let minT = Infinity, maxT = -Infinity;
  for (const e of events) {
    const t = new Date(e.timestamp).getTime();
    if (t < minT) minT = t;
    if (t > maxT) maxT = t;
  }
  const range = maxT - minT || 1;
  const plotLeft = MARGIN.left;
  const plotWidth = w - MARGIN.left - MARGIN.right;
  const trackAreaH = tracks.length * (TRACK_H + TRACK_GAP);
  svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
  svg.setAttribute('height', h);
  svg.innerHTML = '';
  // Clip
  const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
  defs.innerHTML = `<clipPath id="plot-clip"><rect x="${plotLeft}" y="0" width="${plotWidth}" height="${h}"/></clipPath>`;
  svg.appendChild(defs);
  // Background
  const bg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
  bg.setAttribute('width', w); bg.setAttribute('height', h); bg.setAttribute('fill', '#0d1117');
  svg.appendChild(bg);
  // Plot group
  const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g.setAttribute('clip-path', 'url(#plot-clip)');
  svg.appendChild(g);
  // Grid lines (time axis)
  const nTicks = 8;
  for (let i = 0; i <= nTicks; i++) {
    const frac = i / nTicks;
    const x = plotLeft + frac * plotWidth;
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', x); line.setAttribute('y1', 0);
    line.setAttribute('x2', x); line.setAttribute('y2', h);
    line.setAttribute('stroke', '#21262d'); line.setAttribute('stroke-width', '0.5');
    g.appendChild(line);
    const lbl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    lbl.setAttribute('x', x); lbl.setAttribute('y', h - 6);
    lbl.setAttribute('text-anchor', 'middle');
    lbl.setAttribute('class', 'axis-label');
    const dt = new Date(minT + frac * range);
    lbl.textContent = dt.toLocaleString('sv-SE', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    g.appendChild(lbl);
  }
  // Playhead
  const playhead = document.createElementNS('http://www.w3.org/2000/svg', 'line');
  playhead.setAttribute('class', 'playhead');
  playhead.setAttribute('y1', '0');
  playhead.setAttribute('y2', h - MARGIN.bottom);
  g.appendChild(playhead);
  // Tracks
  const playheadX = plotLeft + (currentTimeIdx / Math.max(events.length-1,1)) * plotWidth;
  for (let ti = 0; ti < tracks.length; ti++) {
    const track = tracks[ti];
    const y = MARGIN.top + ti * (TRACK_H + TRACK_GAP);
    // Track bg
    const trackBg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    trackBg.setAttribute('x', plotLeft); trackBg.setAttribute('y', y);
    trackBg.setAttribute('width', plotWidth); trackBg.setAttribute('height', TRACK_H);
    trackBg.setAttribute('fill', ti % 2 === 0 ? '#0d1117' : '#161b22');
    g.appendChild(trackBg);
    // Label
    const lbl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    lbl.setAttribute('x', plotLeft - 8); lbl.setAttribute('y', y + TRACK_H / 2 + 4);
    lbl.setAttribute('text-anchor', 'end'); lbl.setAttribute('class', 'track-label');
    lbl.textContent = track.blueprint.length > 28 ? track.blueprint.slice(0,25) + '...' : track.blueprint;
    svg.appendChild(lbl);
    // Connector line
    const sortedEv = track.events.sort((a,b) => new Date(a.timestamp) - new Date(b.timestamp));
    if (sortedEv.length > 1) {
      let prevX = null;
      for (const e of sortedEv) {
        const t = new Date(e.timestamp).getTime();
        const x = plotLeft + ((t - minT) / range) * plotWidth;
        if (prevX !== null) {
          const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          line.setAttribute('x1', prevX); line.setAttribute('y1', y + TRACK_H/2);
          line.setAttribute('x2', x); line.setAttribute('y2', y + TRACK_H/2);
          line.setAttribute('stroke', '#30363d'); line.setAttribute('stroke-width', '1');
          g.appendChild(line);
        }
        prevX = x;
      }
    }
    // Nodes
    for (const e of sortedEv) {
      const t = new Date(e.timestamp).getTime();
      const x = plotLeft + ((t - minT) / range) * plotWidth;
      const composite = parseCompositeScore(e.detail);
      const nodeClass = composite !== null ? getScoreClass(composite) : (e.action === 'spawn' ? 'node-spawn' : 'node-improve');
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', x); circle.setAttribute('cy', y + TRACK_H/2);
      circle.setAttribute('r', NODE_R);
      circle.setAttribute('class', `node ${nodeClass}`);
      circle.style.stroke = nodeClass === 'score-70' ? '#d29922' : 'none';
      circle.style.strokeWidth = nodeClass === 'score-70' ? '1.5' : '0';
      circle.dataset.evtIdx = allEvents.indexOf(e);
      circle.addEventListener('click', () => showDetail(e));
      g.appendChild(circle);
      // Score label for eval events
      if (composite !== null) {
        const lbl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        lbl.setAttribute('x', x); lbl.setAttribute('y', y + TRACK_H/2 - 10);
        lbl.setAttribute('class', 'node-label');
        lbl.setAttribute('font-size', '9');
        lbl.textContent = composite.toFixed(1);
        g.appendChild(lbl);
      }
    }
  }
  // Group separator lines
  if (clusterByBp) {
    for (let ti = 1; ti < tracks.length; ti++) {
      const y = MARGIN.top + ti * (TRACK_H + TRACK_GAP) - TRACK_GAP/2;
      const sep = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      sep.setAttribute('x1', plotLeft); sep.setAttribute('y1', y);
      sep.setAttribute('x2', plotLeft + plotWidth); sep.setAttribute('y2', y);
      sep.setAttribute('stroke', '#21262d'); sep.setAttribute('stroke-width', '0.5');
      g.appendChild(sep);
    }
  }
  // Update playhead position
  playhead.setAttribute('x1', playheadX);
  playhead.setAttribute('x2', playheadX);
  // Update slider max & display
  const slider = document.getElementById('time-slider');
  slider.max = Math.max(events.length - 1, 0);
  const disp = document.getElementById('time-display');
  if (events[currentTimeIdx]) {
    disp.textContent = events[currentTimeIdx].timestamp + ' [' + (currentTimeIdx+1) + '/' + events.length + ']';
  } else {
    disp.textContent = '--';
  }
}
// ============================================================
// DETAIL POPUP
// ============================================================
function showDetail(e) {
  document.getElementById('modal-title').textContent = e.blueprint + ' — ' + e.action;
  const body = document.getElementById('modal-body');
  const composite = parseCompositeScore(e.detail);
  body.innerHTML = `
    <div class="row"><span class="key">Action</span><span class="val">${e.action}</span></div>
    <div class="row"><span class="key">Blueprint</span><span class="val">${e.blueprint}</span></div>
    <div class="row"><span class="key">Run ID</span><span class="val">${e.id}</span></div>
    <div class="row"><span class="key">Version</span><span class="val">${e.detail.match(/iter (\d+)\/\d+/) ? 'Iter ' + e.detail.match(/iter (\d+)\/\d+/)[1] : '-'}</span></div>
    <div class="row"><span class="key">Stage</span><span class="val">${e.status}</span></div>
    <div class="row"><span class="key">Composite Score</span><span class="val">${composite !== null ? composite.toFixed(1) : '-'}</span></div>
    <div class="row"><span class="key">Progress</span><span class="val">${e.progress}%</span></div>
    <div class="row"><span class="key">Timestamp</span><span class="val">${e.timestamp}</span></div>
    <div class="row"><span class="key">Detail</span><span class="val" style="font-size:11px;max-width:240px;word-break:break-word">${e.detail}</span></div>
  `;
  document.getElementById('modal').classList.add('open');
}
// ============================================================
// TIME SCRUBBER
// ============================================================
function updateTime(idx) {
  currentTimeIdx = Math.max(0, Math.min(idx, allEvents.length - 1));
  document.getElementById('time-slider').value = currentTimeIdx;
  // Re-render with current filter
  const cluster = document.getElementById('chk-cluster').checked;
  const cutoff = currentTimeIdx;
  const visible = allEvents.slice(0, cutoff + 1);
  render(visible, cluster);
}
document.getElementById('time-slider').addEventListener('input', function() {
  if (playing) { playing = false; clearInterval(playTimer); document.getElementById('btn-play').textContent = 'Play'; }
  updateTime(parseInt(this.value));
});
document.getElementById('btn-play').addEventListener('click', function() {
  playing = !playing;
  this.textContent = playing ? 'Pause' : 'Play';
  if (playing) {
    if (currentTimeIdx >= allEvents.length - 1) updateTime(0);
    playTimer = setInterval(() => {
      if (currentTimeIdx >= allEvents.length - 1) { playing = false; clearInterval(playTimer); document.getElementById('btn-play').textContent = 'Play'; }
      updateTime(currentTimeIdx + 1);
    }, 200);
  } else {
    clearInterval(playTimer);
  }
});
document.getElementById('btn-reset').addEventListener('click', function() {
  if (playing) { playing = false; clearInterval(playTimer); document.getElementById('btn-play').textContent = 'Play'; }
  updateTime(allEvents.length - 1);
});
document.getElementById('chk-cluster').addEventListener('change', function() {
  const cluster = this.checked;
  const visible = allEvents.slice(0, currentTimeIdx + 1);
  render(visible, cluster);
});
// ============================================================
// BOOT
// ============================================================
fetch('state.yaml')
  .then(r => r.text())
  .then(text => {
    allEvents = parseStateYaml(text);
    // Filter: only eval events with composite scores + spawn + improve
    allEvents = allEvents.filter(e => {
      if (e.action === 'eval' && e.status === 'complete' && parseCompositeScore(e.detail) !== null) return true;
      if (e.action === 'spawn' && e.status === 'complete') return true;
      if (e.action === 'improve' && e.status === 'complete') return true;
      return false;
    });
    // Sort by timestamp
    allEvents.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
    currentTimeIdx = allEvents.length - 1;
    document.getElementById('time-slider').max = Math.max(allEvents.length - 1, 0);
    const cluster = document.getElementById('chk-cluster').checked;
    render(allEvents, cluster);
  })
  .catch(err => {
    document.getElementById('timeline-svg').innerHTML = `<text x="20" y="40" fill="#f85149" font-size="14">Error loading state.yaml: ${err.message}</text>`;
  });
</script>
</body>
</html>
```
Klistra in ovanstående i `timeline.html`, lägg bredvid `state.yaml`, öppna i webbläsare. Laddar YAML från disk via fetch, parsa händelser, renderar SVG-spår per blueprint med färgkodade noder (guld >=85, amber 70-84, blå <70). Time scrubber med play/pause och auto-replay. Klicka nod för detaljpopup med run_id, version, stage, score, benchmark.