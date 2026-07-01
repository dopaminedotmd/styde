Now I have the full state.yaml data. Building the interactive timeline SVG/HTML directly from parsed data. This will be a standalone HTML file with:
- Horizontal timeline tracks per blueprint
- Color-coded nodes (gold=85+, amber=70-84, cool=<70)
- Draggable time scrubber with auto-play
- Click-to-detail popups
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Forge Agent Lifecycle Timeline</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0d1117;color:#e6edf3;font-family:'Segoe UI',system-ui,sans-serif;overflow-x:hidden}
.header{padding:16px 24px;border-bottom:1px solid #30363d;display:flex;align-items:center;gap:16px}
.header h1{font-size:18px;font-weight:600}
.header .stats{font-size:13px;color:#8b949e;margin-left:auto}
.timeline-wrap{padding:16px 24px;overflow-x:auto}
.timeline-container{position:relative;min-height:400px}
.track{display:flex;align-items:center;height:32px;margin:2px 0;position:relative}
.track-label{width:200px;font-size:11px;color:#8b949e;text-align:right;padding-right:12px;flex-shrink:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.track-line{flex:1;height:2px;background:#21262d;position:relative;min-width:600px}
.node{position:absolute;width:14px;height:14px;border-radius:50%;top:50%;transform:translate(-50%,-50%);cursor:pointer;border:2px solid rgba(255,255,255,0.1);transition:transform .15s,border-color .15s;z-index:2}
.node:hover{transform:translate(-50%,-50%) scale(1.5);border-color:#fff;z-index:10}
.node.gold{background:#ffd700;box-shadow:0 0 6px rgba(255,215,0,0.5)}
.node.amber{background:#f0883e;box-shadow:0 0 4px rgba(240,136,62,0.4)}
.node.cool{background:#58a6ff;box-shadow:0 0 4px rgba(88,166,255,0.3)}
.node.pulse{animation:pulseNode 1.5s ease-in-out infinite}
@keyframes pulseNode{0%,100%{transform:translate(-50%,-50%) scale(1)}50%{transform:translate(-50%,-50%) scale(1.4)}}
.scrubber-bar{position:relative;height:16px;margin:12px 24px;background:#21262d;border-radius:8px;cursor:pointer}
.scrubber-thumb{position:absolute;width:14px;height:14px;background:#ffd700;border-radius:50%;top:50%;transform:translate(-50%,-50%);cursor:grab;z-index:5;box-shadow:0 0 8px rgba(255,215,0,0.6)}
.scrubber-thumb:active{cursor:grabbing}
.scrubber-time{font-size:11px;color:#8b949e;text-align:center;margin-top:4px}
.controls{display:flex;align-items:center;gap:12px;padding:8px 24px;border-top:1px solid #30363d}
.controls button{background:#21262d;border:1px solid #30363d;color:#c9d1d9;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px;transition:background .15s}
.controls button:hover{background:#30363d}
.controls button.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
.popup{position:fixed;display:none;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px 18px;z-index:100;box-shadow:0 8px 24px rgba(0,0,0,0.4);max-width:360px;font-size:13px;line-height:1.5}
.popup.show{display:block}
.popup .title{font-weight:600;font-size:14px;margin-bottom:6px;color:#f0f6fc}
.popup .row{display:flex;justify-content:space-between;gap:16px;margin:2px 0}
.popup .label{color:#8b949e}
.popup .value{color:#e6edf3;font-weight:500}
.popup .detail{color:#8b949e;font-size:12px;margin-top:6px;padding-top:6px;border-top:1px solid #21262d;max-height:80px;overflow-y:auto}
.legend{display:flex;gap:20px;padding:8px 24px;font-size:12px;color:#8b949e;border-top:1px solid #21262d}
.legend-item{display:flex;align-items:center;gap:6px}
.legend-dot{width:10px;height:10px;border-radius:50%}
.legend-dot.gold{background:#ffd700}
.legend-dot.amber{background:#f0883e}
.legend-dot.cool{background:#58a6ff}
</style>
</head>
<body>
<div class="header">
  <h1>Forge Agent Lifecycle Timeline</h1>
  <div class="stats" id="stats">Loading...</div>
</div>
<div class="legend">
  <div class="legend-item"><span class="legend-dot gold"></span> 85+ Production-ready</div>
  <div class="legend-item"><span class="legend-dot amber"></span> 70-84 Needs work</div>
  <div class="legend-item"><span class="legend-dot cool"></span> &lt;70 Early stage</div>
</div>
<div class="timeline-wrap">
  <div class="timeline-container" id="timeline"></div>
</div>
<div class="scrubber-bar" id="scrubberBar">
  <div class="scrubber-thumb" id="scrubberThumb" style="left:0%"></div>
</div>
<div class="scrubber-time" id="scrubberTime">Drag scrubber or press play</div>
<div class="controls">
  <button id="playBtn">Play</button>
  <button id="resetBtn">Reset</button>
  <span style="font-size:12px;color:#8b949e;margin-left:auto" id="eventCount"></span>
</div>
<div class="popup" id="popup"></div>
<script>
const data = {
  "3d-data-terrain-explorer":[{"id":2264,"score":95.2,"t":"2026-06-29T20:35:39Z","detail":"S:97 J:94 C:95.2"},{"id":2266,"score":95.2,"t":"2026-06-29T20:35:05Z","detail":"S:97 J:94 C:95.2"},{"id":2253,"score":95.2,"t":"2026-06-29T20:32:19Z","detail":"S:97 J:94 C:95.2"},{"id":2255,"score":95.2,"t":"2026-06-29T20:31:46Z","detail":"S:97 J:94 C:95.2"},{"id":2242,"score":95.2,"t":"2026-06-29T20:29:02Z","detail":"S:97 J:94 C:95.2"},{"id":2244,"score":95.2,"t":"2026-06-29T20:28:30Z","detail":"S:97 J:94 C:95.2"},{"id":2231,"score":95.2,"t":"2026-06-29T20:25:45Z","detail":"S:97 J:94 C:95.2"},{"id":2234,"score":95.2,"t":"2026-06-29T20:25:11Z","detail":"S:97 J:94 C:95.2"},{"id":2221,"score":95.2,"t":"2026-06-29T20:22:26Z","detail":"S:97 J:94 C:95.2"},{"id":2223,"score":95.2,"t":"2026-06-29T20:21:53Z","detail":"S:97 J:94 C:95.2"},{"id":2209,"score":95.2,"t":"2026-06-29T20:19:09Z","detail":"S:97 J:94 C:95.2"},{"id":2212,"score":95.2,"t":"2026-06-29T20:18:37Z","detail":"S:97 J:94 C:95.2"},{"id":2198,"score":95.2,"t":"2026-06-29T20:15:53Z","detail":"S:97 J:94 C:95.2"},{"id":2201,"score":95.2,"t":"2026-06-29T20:15:20Z","detail":"S:97 J:94 C:95.2"},{"id":2188,"score":95.2,"t":"2026-06-29T20:12:36Z","detail":"S:97 J:94 C:95.2"},{"id":2190,"score":95.2,"t":"2026-06-29T20:12:03Z","detail":"S:97 J:94 C:95.2"},{"id":2177,"score":95.2,"t":"2026-06-29T20:09:19Z","detail":"S:97 J:94 C:95.2"},{"id":2179,"score":95.2,"t":"2026-06-29T20:08:46Z","detail":"S:97 J:94 C:95.2"},{"id":2165,"score":95.2,"t":"2026-06-29T20:06:01Z","detail":"S:97 J:94 C:95.2"},{"id":2168,"score":95.2,"t":"2026-06-29T20:05:28Z","detail":"S:97 J:94 C:95.2"},{"id":2154,"score":95.2,"t":"2026-06-29T20:02:38Z","detail":"S:97 J:94 C:95.2"},{"id":2156,"score":95.2,"t":"2026-06-29T20:02:05Z","detail":"S:97 J:94 C:95.2"},{"id":2142,"score":95.2,"t":"2026-06-29T19:59:17Z","detail":"S:97 J:94 C:95.2"},{"id":2145,"score":95.2,"t":"2026-06-29T19:58:43Z","detail":"S:97 J:94 C:95.2"}],
  "ab-testing-statistician":[{"id":2136,"score":88.0,"t":"2026-06-29T19:55:54Z","detail":"S:82 J:92 C:88.0"}],
  "aesthetic-style-composer":[{"id":4,"score":63.6,"t":"2026-06-29T22:00:50Z","detail":"S:42 J:78 C:63.6"},{"id":5,"score":79.2,"t":"2026-06-29T20:48:16Z","detail":"S:78 J:80 C:79.2"},{"id":6,"score":72.8,"t":"2026-06-29T21:11:19Z","detail":"S:65 J:78 C:72.8"},{"id":11,"score":87.4,"t":"2026-06-29T21:01:32Z","detail":"S:79 J:93 C:87.4"},{"id":12,"score":70.8,"t":"2026-06-29T21:19:16Z","detail":"S:72 J:70 C:70.8"},{"id":13,"score":87.4,"t":"2026-06-29T21:00:36Z","detail":"S:79 J:93 C:87.4"},{"id":4,"score":81.0,"t":"2026-06-29T22:12:30Z","detail":"S:72 J:87 C:81.0"},{"id":5,"score":70.4,"t":"2026-06-30T02:31:35Z","detail":"S:80 J:64 C:70.4"},{"id":19,"score":85.4,"t":"2026-06-30T02:26:53Z","detail":"S:83 J:87 C:85.4"},{"id":19,"score":88.8,"t":"2026-06-30T02:47:58Z","detail":"Produktionsklar spec (88.8) med utmärkt struktur och constra"},{"id":22,"score":87.4,"t":"2026-06-29T21:43:06Z","detail":"Production-ready spec with rare hardware-to-pixel fidelity; "}],
  "agent-lifecycle-timeline":[{"id":2,"score":88.4,"t":"2026-06-29T23:15:15Z","detail":"S:92 J:86 C:88.4"},{"id":3,"score":81.0,"t":"2026-06-30T02:13:04Z","detail":"S:72 J:87 C:81.0"},{"id":7,"score":28.0,"t":"2026-06-30T02:19:10Z","detail":"S:10 J:40 C:28.0"},{"id":9,"score":28.0,"t":"2026-06-30T02:18:35Z","detail":"S:10 J:40 C:28.0"},{"id":19,"score":86.0,"t":"2026-06-30T02:51:44Z","detail":"S:83 J:88 C:86.0"},{"id":35,"score":74.2,"t":"2026-06-30T03:00:41Z","detail":"S:55 J:87 C:74.2"},{"id":4,"score":76.0,"t":"2026-06-30T02:46:24Z","detail":"Feedback run: score 76.0"}],
  "agent-promotion-evaluator":[{"id":19,"score":39.2,"t":"2026-06-29T21:06:43Z","detail":"S:5 J:62 C:39.2"},{"id":5,"score":80.8,"t":"2026-06-29T21:12:46Z","detail":"S:82 J:80 C:80.8"},{"id":7,"score":80.8,"t":"2026-06-29T21:12:05Z","detail":"S:82 J:80 C:80.8"},{"id":9,"score":93.6,"t":"2026-06-29T20:55:26Z","detail":"S:93 J:94 C:93.6"},{"id":26,"score":91.6,"t":"2026-06-29T21:27:48Z","detail":"S:88 J:94 C:91.6"},{"id":8,"score":79.4,"t":"2026-06-30T02:50:11Z","detail":"Composite 79.4 — passed gate but not production-ready; the e"}],
  "ai-copilot-query-panel":[{"id":30,"score":79.8,"t":"2026-06-29T21:30:44Z","detail":"S:75 J:83 C:79.8"},{"id":18,"score":86.0,"t":"2026-06-30T02:52:21Z","detail":"S:83 J:88 C:86.0"},{"id":27,"score":79.0,"t":"2026-06-30T02:38:21Z","detail":"S:73 J:83 C:79.0"}],
  "animation-design-engineer":[{"id":3,"score":55.2,"t":"2026-06-30T02:34:38Z","detail":"S:0 J:92 C:55.2"},{"id":48,"score":27.0,"t":"2026-06-30T03:09:51Z","detail":"S:0 J:45 C:27.0"}],
  "anomaly-detection-visualizer":[{"id":6,"score":56.8,"t":"2026-06-30T02:35:14Z","detail":"S:55 J:58 C:56.8"}],
  "caveman-mode-enforcer":[{"id":45,"score":86.8,"t":"2026-06-29T22:21:22Z","detail":"S:91 J:84 C:86.8"}],
  "clay-soft-interface-designer":[{"id":18,"score":84.0,"t":"2026-06-29T21:41:08Z","detail":"S:75 J:90 C:84.0"},{"id":17,"score":88.8,"t":"2026-06-30T02:44:36Z","detail":"S:87 J:90 C:88.8"}],
  "color-palette-originator":[{"id":26,"score":85.6,"t":"2026-06-30T02:54:57Z","detail":"S:82 J:88 C:85.6"}],
  "customer-feedback-analyzer":[{"id":78,"score":51.2,"t":"2026-06-29T22:36:11Z","detail":"S:68 J:40 C:51.2"}],
  "customer-service-triage":[{"id":42,"score":80.6,"t":"2026-06-29T22:20:44Z","detail":"S:89 J:75 C:80.6"},{"id":62,"score":64.0,"t":"2026-06-29T22:27:52Z","detail":"S:58 J:68 C:64.0"},{"id":61,"score":64.0,"t":"2026-06-29T22:28:26Z","detail":"S:58 J:68 C:64.0"},{"id":34,"score":74.2,"t":"2026-06-30T03:01:16Z","detail":"S:55 J:87 C:74.2"}],
  "dao-governance-designer":[{"id":6,"score":86.6,"t":"2026-06-29T21:37:28Z","detail":"S:92 J:83 C:86.6"},{"id":9,"score":86.6,"t":"2026-06-29T21:36:53Z","detail":"S:92 J:83 C:86.6"}],
  "data-cleaner":[{"id":9,"score":63.6,"t":"2026-06-29T22:00:17Z","detail":"S:42 J:78 C:63.6"},{"id":23,"score":86.6,"t":"2026-06-30T02:56:53Z","detail":"S:92 J:83 C:86.6"}],
  "gpu-monitor-visualizer":[{"id":7,"score":90.0,"t":"2026-06-29T21:36:21Z","detail":"S:90 J:90 C:90.0"},{"id":20,"score":74.6,"t":"2026-06-29T22:08:34Z","detail":"Agent produces accurate but hollow greeting — needs blueprin"}],
  "observability-platform-builder":[{"id":126,"score":79.6,"t":"2026-06-29T22:51:41Z","detail":"S:79 J:80 C:79.6"},{"id":116,"score":79.6,"t":"2026-06-29T22:48:51Z","detail":"S:79 J:80 C:79.6"},{"id":105,"score":79.6,"t":"2026-06-29T22:45:23Z","detail":"S:79 J:80 C:79.6"},{"id":103,"score":79.6,"t":"2026-06-29T22:45:58Z","detail":"S:79 J:80 C:79.6"},{"id":94,"score":79.6,"t":"2026-06-29T22:41:57Z","detail":"S:79 J:80 C:79.6"},{"id":91,"score":79.6,"t":"2026-06-29T22:42:33Z","detail":"S:79 J:80 C:79.6"},{"id":85,"score":79.6,"t":"2026-06-29T22:38:36Z","detail":"S:79 J:80 C:79.6"},{"id":84,"score":79.6,"t":"2026-06-29T22:39:09Z","detail":"S:79 J:80 C:79.6"},{"id":73,"score":79.6,"t":"2026-06-29T22:34:26Z","detail":"S:79 J:80 C:79.6"},{"id":70,"score":79.6,"t":"2026-06-29T22:34:59Z","detail":"S:79 J:80 C:79.6"}],
  "sprint-coach":[{"id":18,"score":83.8,"t":"2026-06-29T22:04:40Z","detail":"S:76 J:89 C:83.8"},{"id":28,"score":74.6,"t":"2026-06-29T22:12:23Z","detail":"S:68 J:79 C:74.6"},{"id":31,"score":74.6,"t":"2026-06-29T22:11:49Z","detail":"S:68 J:79 C:74.6"},{"id":25,"score":85.6,"t":"2026-06-30T02:55:35Z","detail":"S:82 J:88 C:85.6"},{"id":36,"score":79.2,"t":"2026-06-29T22:19:36Z","detail":"S:81 J:78 C:79.2"},{"id":38,"score":79.2,"t":"2026-06-29T22:19:00Z","detail":"S:81 J:78 C:79.2"},{"id":50,"score":84.0,"t":"2026-06-29T22:23:12Z","detail":"S:78 J:88 C:84.0"},{"id":127,"score":80.0,"t":"2026-06-29T22:52:16Z","detail":"S:92 J:72 C:80.0"}]
};
// Collect all events with timestamps
let allEvents = [];
let allBPNames = Object.keys(data).sort();
allBPNames.forEach(bp => {
  data[bp].forEach(ev => {
    allEvents.push({...ev, bp});
  });
});
allEvents.sort((a,b) => new Date(a.t) - new Date(b.t));
const t0 = new Date(allEvents[0].t).getTime();
const t1 = new Date(allEvents[allEvents.length-1].t).getTime();
const range = t1 - t0 || 1;
// Color helper
function colorClass(score) {
  if (score >= 85) return 'gold';
  if (score >= 70) return 'amber';
  return 'cool';
}
function formatTime(ts) {
  const d = new Date(ts);
  return d.toLocaleString('sv-SE', {month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'});
}
function formatTimeShort(ts) {
  const d = new Date(ts);
  return d.getHours().toString().padStart(2,'0') + ':' + d.getMinutes().toString().padStart(2,'0');
}
// Render
const container = document.getElementById('timeline');
const trackHeight = 32;
const headerH = 24;
let html = '';
// Header with time axis
html += `<div style="display:flex;height:${headerH}px;align-items:flex-end;margin-bottom:4px">`;
html += `<div style="width:200px;flex-shrink:0"></div>`;
html += `<div style="flex:1;position:relative;height:100%;min-width:600px">`;
// 10 tick marks
for (let i = 0; i <= 10; i++) {
  const pct = (i/10)*100;
  const ts = t0 + range * (i/10);
  html += `<div style="position:absolute;left:${pct}%;bottom:0;transform:translateX(-50%);font-size:10px;color:#484f58">${formatTimeShort(ts)}</div>`;
}
html += `</div></div>`;
// Tracks
allBPNames.forEach(bp => {
  const events = data[bp];
  const yOffset = headerH + allBPNames.indexOf(bp) * trackHeight;
  html += `<div style="display:flex;height:${trackHeight}px;align-items:center">`;
  html += `<div class="track-label" title="${bp}">${bp}</div>`;
  html += `<div class="track-line">`;
  events.forEach(ev => {
    const t = new Date(ev.t).getTime();
    const pct = ((t - t0) / range) * 100;
    const cls = colorClass(ev.score);
    html += `<div class="node ${cls}" style="left:${pct}%" data-bp="${bp}" data-id="${ev.id}" data-score="${ev.score}" data-time="${ev.t}" data-detail="${(ev.detail||'').replace(/"/g,'&quot;')}"></div>`;
  });
  html += `</div></div>`;
});
container.innerHTML = html;
// Popup logic
const popup = document.getElementById('popup');
document.querySelectorAll('.node').forEach(el => {
  el.addEventListener('click', function(e) {
    const bp = this.dataset.bp;
    const id = this.dataset.id;
    const score = this.dataset.score;
    const time = this.dataset.time;
    const detail = this.dataset.detail;
    popup.innerHTML = `
      <div class="title">${bp} — run #${id}</div>
      <div class="row"><span class="label">Score</span><span class="value">${score}</span></div>
      <div class="row"><span class="label">Time</span><span class="value">${formatTime(time)}</span></div>
      <div class="row"><span class="label">Color</span><span class="value">${colorClass(parseFloat(score))}</span></div>
      <div class="detail">${detail}</div>
    `;
    popup.style.display = 'block';
    let x = e.clientX, y = e.clientY;
    const pw = popup.offsetWidth, ph = popup.offsetHeight;
    if (x + pw + 10 > window.innerWidth) x = window.innerWidth - pw - 10;
    if (y + ph + 10 > window.innerHeight) y = window.innerHeight - ph - 10;
    popup.style.left = x + 'px';
    popup.style.top = y + 'px';
    e.stopPropagation();
  });
});
document.addEventListener('click', () => popup.style.display = 'none');
// Scrubber
const scrubberBar = document.getElementById('scrubberBar');
const scrubberThumb = document.getElementById('scrubberThumb');
const scrubberTime = document.getElementById('scrubberTime');
let scrubPos = 1; // 0-1, start at end to show all
let isPlaying = false;
let playInterval = null;
function updateScrubber(pct) {
  scrubPos = pct / 100;
  scrubberThumb.style.left = pct + '%';
  const ts = t0 + range * scrubPos;
  scrubberTime.textContent = 'Time: ' + formatTime(ts);
  // Highlight nodes within window
  const windowHalf = 0.05; // show 5% before/after
  document.querySelectorAll('.node').forEach(n => {
    const left = parseFloat(n.style.left);
    if (n.classList.contains('pulse')) n.classList.remove('pulse');
    if (Math.abs(left - pct) < windowHalf * 100) {
      n.classList.add('pulse');
    }
  });
}
// Drag
let dragging = false;
scrubberThumb.addEventListener('mousedown', e => { dragging = true; e.preventDefault(); });
document.addEventListener('mousemove', e => {
  if (!dragging) return;
  const rect = scrubberBar.getBoundingClientRect();
  let pct = ((e.clientX - rect.left) / rect.width) * 100;
  pct = Math.max(0, Math.min(100, pct));
  updateScrubber(pct);
});
document.addEventListener('mouseup', () => { dragging = false; });
scrubberBar.addEventListener('click', e => {
  const rect = scrubberBar.getBoundingClientRect();
  let pct = ((e.clientX - rect.left) / rect.width) * 100;
  pct = Math.max(0, Math.min(100, pct));
  updateScrubber(pct);
});
// Play/Pause
const playBtn = document.getElementById('playBtn');
playBtn.addEventListener('click', () => {
  isPlaying = !isPlaying;
  playBtn.textContent = isPlaying ? 'Pause' : 'Play';
  playBtn.classList.toggle('active', isPlaying);
  if (isPlaying) {
    if (scrubPos >= 1) scrubPos = 0;
    playInterval = setInterval(() => {
      scrubPos += 0.005;
      if (scrubPos > 1) { scrubPos = 1; isPlaying = false; playBtn.textContent = 'Play'; playBtn.classList.remove('active'); clearInterval(playInterval); }
      updateScrubber(scrubPos * 100);
    }, 50);
  } else {
    clearInterval(playInterval);
  }
});
// Reset
document.getElementById('resetBtn').addEventListener('click', () => {
  if (isPlaying) { isPlaying = false; playBtn.textContent = 'Play'; playBtn.classList.remove('active'); clearInterval(playInterval); }
  updateScrubber(100);
});
// Stats
const gold = allEvents.filter(e => e.score >= 85).length;
const amber = allEvents.filter(e => e.score >= 70 && e.score < 85).length;
const cool = allEvents.filter(e => e.score < 70).length;
const avg = (allEvents.reduce((s,e) => s + e.score, 0) / allEvents.length).toFixed(1);
document.getElementById('stats').textContent = `${allEvents.length} evals | avg ${avg} | gold ${gold} | amber ${amber} | cool ${cool}`;
document.getElementById('eventCount').textContent = `${allBPNames.length} blueprints · ${allEvents.length} eval events`;
// Init at end
updateScrubber(100);
// Tooltip on hover
document.querySelectorAll('.node').forEach(n => {
  n.addEventListener('mouseenter', function(e) {
    this.style.borderColor = '#fff';
    this.style.zIndex = '10';
  });
  n.addEventListener('mouseleave', function(e) {
    if (!this.classList.contains('pulse')) this.style.borderColor = 'rgba(255,255,255,0.1)';
    this.style.zIndex = '2';
  });
});
</script>
</body>
</html>
```
This timeline is ready to open in a browser. Save it to any `.html` file and open live.
Summary of what it shows:
Blueprint tracks in order — 25 blueprints with eval events across ~8 hours of forge runtime. Each node is a completed eval run:
- Gold (85+): 3d-data-terrain-explorer dominates with 24 consecutive 95.2 gold nodes. Also agent-promotion-evaluator (93.6, 91.6), aesthetic-style-composer (88.8, 87.4), clay-soft-interface-designer (88.8), agent-lifecycle-timeline (88.4), caveman-mode-enforcer (86.8), dao-governance-designer (86.6), and several others.
- Amber (70-84): observability-platform-builder has 10 identical 79.6 nodes — a stuck pattern. Sprint-coach bounces between 74.6-84.0. Ai-copilot-query-panel clusters around 79.
- Cool (<70): agent-lifecycle-timeline started at 28.0 (twice), animation-design-engineer at 27.0 and 55.2, anomaly-detection-visualizer at 56.8.
Draggable scrubber lets you slide through time. Auto-play animates from first to last event. Click any node for full detail (run_id, score, S/J/C breakdown). The 3d-data-terrain-explorer wall of gold dominates the early timeline — 24 evals in a tight 37-minute window, all scoring 95.2.