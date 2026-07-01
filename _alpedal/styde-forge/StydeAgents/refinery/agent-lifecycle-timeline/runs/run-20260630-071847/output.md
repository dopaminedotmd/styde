Din maskin har slut på sidväxlingsminne (WinError 1455, cygheap fork failures). Inga verktyg fungerar — read_file, search_files, terminal, write_file slår alla fel. Hård blockerare: sidfilen är för liten och Windows kan inte allokera mer virtuellt minne.
Jag har byggt det fullständiga timeline-verktyget. Här är HTML-koden — spara som `timeline.html` och öppna i en browser (ingen server krävs):
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge - Agent Lifecycle Timeline</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; overflow-x: hidden; }
.header { padding: 20px 30px; background: #161b22; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; }
.header h1 { font-size: 20px; font-weight: 600; color: #f0f6fc; }
.stats { display: flex; gap: 24px; font-size: 13px; }
.stat { display: flex; align-items: center; gap: 6px; }
.stat-value { font-weight: 700; font-variant-numeric: tabular-nums; }
.stat-hot { color: #ffd700; } .stat-amber { color: #d29922; } .stat-cool { color: #58a6ff; }
.controls { padding: 12px 30px; background: #161b22; border-bottom: 1px solid #30363d; display: flex; align-items: center; gap: 16px; }
.controls button { background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 6px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; }
.controls button:hover { background: #30363d; }
.controls button.active { background: #1f6feb; border-color: #1f6feb; color: #fff; }
.timeline-container { padding: 20px 30px; overflow-x: auto; }
.timeline-svg { min-width: 100%; }
.track-label { font-size: 12px; fill: #8b949e; }
.axis-label { font-size: 11px; fill: #484f58; }
.tooltip { display: none; position: fixed; background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; font-size: 13px; min-width: 280px; z-index: 1000; box-shadow: 0 8px 24px rgba(0,0,0,0.4); }
.tooltip.show { display: block; }
.tooltip h3 { font-size: 14px; margin-bottom: 8px; color: #f0f6fc; }
.tooltip .row { display: flex; justify-content: space-between; padding: 3px 0; border-bottom: 1px solid #21262d; }
.tooltip .row:last-child { border: none; }
.tooltip .label { color: #8b949e; }
.tooltip .value { font-weight: 600; }
.legend { display: flex; gap: 20px; padding: 0 30px 16px; font-size: 12px; }
.legend-item { display: flex; align-items: center; gap: 6px; }
.legend-dot { width: 12px; height: 12px; border-radius: 50%; }
.time-display { font-family: monospace; font-size: 13px; color: #8b949e; }
.speed-select { background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
</style>
</head>
<body>
<div class="header">
  <h1>Agent Lifecycle Timeline</h1>
  <div class="stats">
    <div class="stat"><span>Blueprints</span><span class="stat-value" id="bpCount">0</span></div>
    <div class="stat"><span>Agents</span><span class="stat-value" id="agentCount">0</span></div>
    <div class="stat"><span>Promoted</span><span class="stat-value stat-hot" id="promotedCount">0</span></div>
    <div class="stat"><span>Time range</span><span class="stat-value" id="timeRange">-</span></div>
  </div>
</div>
<div class="controls">
  <button id="playBtn" onclick="togglePlay()">Play</button>
  <button onclick="resetView()">Reset</button>
  <input type="range" id="timeSlider" min="0" max="100" value="100" style="flex:1; max-width:600px" oninput="updateSlider(this.value)">
  <span class="time-display" id="timeDisplay">-</span>
  <select class="speed-select" id="speedSelect">
    <option value="2000">0.5x</option>
    <option value="1000" selected>1x</option>
    <option value="400">2x</option>
    <option value="150">4x</option>
  </select>
</div>
<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:#ffd700"></div> Production (85+)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#d29922"></div> Refinery (70-84)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#58a6ff"></div> Below 70</div>
  <div class="legend-item"><div class="legend-dot" style="background:#30363d;border:2px dashed #484f58"></div> In progress</div>
</div>
<div class="timeline-container" id="timelineContainer">
  <svg class="timeline-svg" id="timelineSvg" height="400"></svg>
</div>
<div class="tooltip" id="tooltip"></div>
<script>
// ===== DATA =====
// Production: replace with fetch('/state.yaml') + js-yaml parse
// For the demo, embedded sample data matching Styde Forge structure:
const BLUEPRINT_DATA = [
  { name: "module-blueprint", agents: [
    { run_id: "mod-001", time: "2026-06-28T08:00:00Z", stage: "spawn", score: null, version: 1, benchmark: "mod-v1" },
    { run_id: "mod-002", time: "2026-06-28T09:30:00Z", stage: "eval", score: 62, version: 1, benchmark: "mod-v1-eval" },
    { run_id: "mod-003", time: "2026-06-28T11:00:00Z", stage: "improve", score: 71, version: 2, benchmark: "mod-v2" },
    { run_id: "mod-004", time: "2026-06-28T13:00:00Z", stage: "eval", score: 78, version: 2, benchmark: "mod-v2-eval" },
    { run_id: "mod-005", time: "2026-06-29T06:00:00Z", stage: "improve", score: 86, version: 3, benchmark: "mod-v3" },
    { run_id: "mod-006", time: "2026-06-29T08:00:00Z", stage: "eval", score: 88, version: 3, benchmark: "mod-v3-eval" },
    { run_id: "mod-007", time: "2026-06-29T10:00:00Z", stage: "promote", score: 88, version: 3, benchmark: "mod-v3-prod" }
  ]},
  { name: "skill-installer", agents: [
    { run_id: "skl-001", time: "2026-06-28T08:15:00Z", stage: "spawn", score: null, version: 1, benchmark: "skl-v1" },
    { run_id: "skl-002", time: "2026-06-28T10:00:00Z", stage: "eval", score: 45, version: 1, benchmark: "skl-v1-eval" },
    { run_id: "skl-003", time: "2026-06-28T12:30:00Z", stage: "improve", score: 67, version: 2, benchmark: "skl-v2" },
    { run_id: "skl-004", time: "2026-06-29T07:00:00Z", stage: "eval", score: 73, version: 2, benchmark: "skl-v2-eval" },
    { run_id: "skl-005", time: "2026-06-29T09:30:00Z", stage: "improve", score: 82, version: 3, benchmark: "skl-v3" },
    { run_id: "skl-006", time: "2026-06-30T01:00:00Z", stage: "eval", score: 91, version: 3, benchmark: "skl-v3-eval" },
    { run_id: "skl-007", time: "2026-06-30T02:00:00Z", stage: "promote", score: 91, version: 3, benchmark: "skl-v3-prod" }
  ]},
  { name: "fullstack-feature-builder", agents: [
    { run_id: "fsb-001", time: "2026-06-28T10:00:00Z", stage: "spawn", score: null, version: 1, benchmark: "fsb-v1" },
    { run_id: "fsb-002", time: "2026-06-28T14:00:00Z", stage: "eval", score: 55, version: 1, benchmark: "fsb-v1-eval" },
    { run_id: "fsb-003", time: "2026-06-29T05:00:00Z", stage: "improve", score: 74, version: 2, benchmark: "fsb-v2" },
    { run_id: "fsb-004", time: "2026-06-29T08:30:00Z", stage: "eval", score: 80, version: 2, benchmark: "fsb-v2-eval" },
    { run_id: "fsb-005", time: "2026-06-29T11:00:00Z", stage: "improve", score: 87, version: 3, benchmark: "fsb-v3" },
    { run_id: "fsb-006", time: "2026-06-29T13:00:00Z", stage: "eval", score: 90, version: 3, benchmark: "fsb-v3-eval" },
    { run_id: "fsb-007", time: "2026-06-29T14:00:00Z", stage: "promote", score: 90, version: 3, benchmark: "fsb-v3-prod" }
  ]},
  { name: "caveman-ultra", agents: [
    { run_id: "cav-001", time: "2026-06-28T11:00:00Z", stage: "spawn", score: null, version: 1, benchmark: "cav-v1" },
    { run_id: "cav-002", time: "2026-06-28T15:00:00Z", stage: "eval", score: 40, version: 1, benchmark: "cav-v1-eval" },
    { run_id: "cav-003", time: "2026-06-29T06:30:00Z", stage: "improve", score: 58, version: 2, benchmark: "cav-v2" },
    { run_id: "cav-004", time: "2026-06-29T10:00:00Z", stage: "eval", score: 63, version: 2, benchmark: "cav-v2-eval" },
    { run_id: "cav-005", time: "2026-06-29T14:30:00Z", stage: "archive", score: 63, version: 2, benchmark: "cav-v2-archive" }
  ]},
  { name: "command-center", agents: [
    { run_id: "cmd-001", time: "2026-06-28T09:00:00Z", stage: "spawn", score: null, version: 1, benchmark: "cmd-v1" },
    { run_id: "cmd-002", time: "2026-06-28T12:00:00Z", stage: "eval", score: 68, version: 1, benchmark: "cmd-v1-eval" },
    { run_id: "cmd-003", time: "2026-06-28T16:00:00Z", stage: "improve", score: 76, version: 2, benchmark: "cmd-v2" },
    { run_id: "cmd-004", time: "2026-06-29T09:00:00Z", stage: "eval", score: 83, version: 2, benchmark: "cmd-v2-eval" },
    { run_id: "cmd-005", time: "2026-06-29T12:00:00Z", stage: "improve", score: 89, version: 3, benchmark: "cmd-v3" },
    { run_id: "cmd-006", time: "2026-06-29T15:00:00Z", stage: "eval", score: 92, version: 3, benchmark: "cmd-v3-eval" },
    { run_id: "cmd-007", time: "2026-06-30T00:30:00Z", stage: "promote", score: 92, version: 3, benchmark: "cmd-v3-prod" }
  ]},
  { name: "dashboard-8767", agents: [
    { run_id: "dsh-001", time: "2026-06-28T09:30:00Z", stage: "spawn", score: null, version: 1, benchmark: "dsh-v1" },
    { run_id: "dsh-002", time: "2026-06-28T13:00:00Z", stage: "eval", score: 70, version: 1, benchmark: "dsh-v1-eval" },
    { run_id: "dsh-003", time: "2026-06-29T08:00:00Z", stage: "improve", score: 81, version: 2, benchmark: "dsh-v2" },
    { run_id: "dsh-004", time: "2026-06-29T11:30:00Z", stage: "eval", score: 87, version: 2, benchmark: "dsh-v2-eval" },
    { run_id: "dsh-005", time: "2026-06-30T01:30:00Z", stage: "promote", score: 87, version: 2, benchmark: "dsh-v2-prod" }
  ]}
];
// ===== STATE =====
let data = BLUEPRINT_DATA;
let allAgents = data.flatMap(bp => bp.agents.filter(a => a.time));
let playing = false;
let playInterval = null;
let minTime = new Date(Math.min(...allAgents.map(a => new Date(a.time))));
let maxTime = new Date(Math.max(...allAgents.map(a => new Date(a.time))));
let timeSpan = maxTime - minTime;
let currentMaxTime = new Date(maxTime);
if (timeSpan === 0) timeSpan = 3600000;
function getTimePosition(t) {
  return ((new Date(t) - minTime) / timeSpan) * 100;
}
function getNodeColor(agent) {
  if (agent.score === null || agent.score === undefined) return '#30363d';
  if (agent.score >= 85) return '#ffd700';
  if (agent.score >= 70) return '#d29922';
  return '#58a6ff';
}
function getNodeRadius(agent) {
  if (agent.stage === 'promote' || agent.stage === 'production') return 8;
  if (agent.stage === 'spawn' || agent.stage === 'archive') return 5;
  return 6;
}
function getStageShape(stage) {
  switch(stage) {
    case 'spawn': return 'diamond';
    case 'eval': case 'improve': return 'circle';
    case 'promote': case 'production': return 'star';
    case 'archive': return 'x';
    default: return 'circle';
  }
}
function render() {
  const svg = document.getElementById('timelineSvg');
  const container = document.getElementById('timelineContainer');
  const padding = { top: 30, right: 80, bottom: 20, left: 200 };
  const trackHeight = 52;
  const bpCount = data.length;
  const totalHeight = Math.max(bpCount * trackHeight + padding.top + padding.bottom, 300);
  const totalWidth = Math.max(container.clientWidth - 40, 900);
  let html = '<svg width="' + totalWidth + '" height="' + totalHeight + '" style="overflow:visible">';
  // Axis line
  html += '<line x1="' + padding.left + '" y1="' + (padding.top - 10) + '" x2="' + (totalWidth - padding.right) + '" y2="' + (padding.top - 10) + '" stroke="#30363d" stroke-width="1"/>';
  // Time labels
  const steps = 6;
  for (let i = 0; i <= steps; i++) {
    let pct = i / steps;
    let t = new Date(minTime.getTime() + timeSpan * pct);
    let x = padding.left + pct * (totalWidth - padding.left - padding.right);
    let label = t.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit' });
    html += '<text x="' + x + '" y="' + (padding.top - 16) + '" text-anchor="middle" class="axis-label">' + label + '</text>';
    html += '<line x1="' + x + '" y1="' + (padding.top - 6) + '" x2="' + x + '" y2="' + (padding.top - 4) + '" stroke="#484f58" stroke-width="1"/>';
    if (i > 0) {
      html += '<line x1="' + x + '" y1="' + (padding.top - 4) + '" x2="' + x + '" y2="' + (totalHeight - padding.bottom) + '" stroke="#21262d" stroke-width="1" stroke-dasharray="3,3"/>';
    }
  }
  // Tracks
  data.forEach((bp, idx) => {
    const y = padding.top + idx * trackHeight + 10;
    const labelY = y + trackHeight / 2;
    html += '<text x="8" y="' + (labelY + 4) + '" class="track-label" dominant-baseline="middle">' + bp.name + '</text>';
    html += '<line x1="' + padding.left + '" y1="' + labelY + '" x2="' + (totalWidth - padding.right) + '" y2="' + labelY + '" stroke="#21262d" stroke-width="1"/>';
    const visibleAgents = bp.agents.filter(a => a.time && new Date(a.time) <= currentMaxTime);
    const ordered = [...visibleAgents].sort((a, b) => new Date(a.time) - new Date(b.time));
    // Connectors
    for (let i = 1; i < ordered.length; i++) {
      let x1 = padding.left + (getTimePosition(ordered[i-1].time) / 100) * (totalWidth - padding.left - padding.right);
      let x2 = padding.left + (getTimePosition(ordered[i].time) / 100) * (totalWidth - padding.left - padding.right);
      html += '<line x1="' + x1 + '" y1="' + labelY + '" x2="' + x2 + '" y2="' + labelY + '" stroke="#30363d" stroke-width="1.5" stroke-dasharray="4,2"/>';
    }
    // Nodes
    ordered.forEach(agent => {
      let pct = getTimePosition(agent.time) / 100;
      let cx = padding.left + pct * (totalWidth - padding.left - padding.right);
      let cy = labelY;
      let r = getNodeRadius(agent);
      let color = getNodeColor(agent);
      let shape = getStageShape(agent.stage);
      let attrs = ' cursor="pointer" data-bp="' + idx + '" data-agent="' + agent.run_id + '"';
      if (shape === 'diamond') {
        let pts = (cx) + ',' + (cy-r) + ' ' + (cx+r*0.7) + ',' + (cy) + ' ' + (cx) + ',' + (cy+r) + ' ' + (cx-r*0.7) + ',' + (cy);
        html += '<polygon points="' + pts + '" fill="' + color + '"' + attrs + '/>';
      } else if (shape === 'star') {
        let pts = '';
        for (let j = 0; j < 10; j++) {
          let angle = (j * Math.PI / 5) - Math.PI / 2;
          let rad = j % 2 === 0 ? r : r * 0.45;
          pts += (j === 0 ? '' : ' ') + (cx + rad * Math.cos(angle)) + ',' + (cy + rad * Math.sin(angle));
        }
        html += '<polygon points="' + pts + '" fill="' + color + '" stroke="#fff" stroke-width="1.5"' + attrs + '/>';
      } else if (shape === 'x') {
        html += '<line x1="' + (cx-r) + '" y1="' + (cy-r) + '" x2="' + (cx+r) + '" y2="' + (cy+r) + '" stroke="' + color + '" stroke-width="2.5"' + attrs + '/>';
        html += '<line x1="' + (cx+r) + '" y1="' + (cy-r) + '" x2="' + (cx-r) + '" y2="' + (cy+r) + '" stroke="' + color + '" stroke-width="2.5"' + attrs + '/>';
      } else {
        html += '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="' + color + '"' + attrs + '/>';
      }
    });
  });
  // Scrubber line
  let scrubPct = (currentMaxTime - minTime) / timeSpan;
  let scrubX = padding.left + scrubPct * (totalWidth - padding.left - padding.right);
  html += '<line x1="' + scrubX + '" y1="' + (padding.top - 10) + '" x2="' + scrubX + '" y2="' + (totalHeight - padding.bottom) + '" stroke="#1f6feb" stroke-width="1.5" stroke-dasharray="4,3" id="scrubLine"/>';
  html += '</svg>';
  svg.outerHTML = html;
  // Bind clicks
  document.querySelectorAll('[data-agent]').forEach(el => {
    el.addEventListener('click', function(e) {
      let bp = data[parseInt(this.dataset.bp)];
      let agent = bp.agents.find(a => a.run_id === this.dataset.agent);
      if (!agent) return;
      let tooltip = document.getElementById('tooltip');
      let scoreText = agent.score !== null ? agent.score + '/100' : 'Pending';
      let scoreClass = agent.score >= 85 ? 'stat-hot' : agent.score >= 70 ? 'stat-amber' : '';
      tooltip.innerHTML = '<h3>' + agent.run_id + ' - ' + bp.name + '</h3>'
        + '<div class="row"><span class="label">Stage</span><span class="value">' + agent.stage + '</span></div>'
        + '<div class="row"><span class="label">Version</span><span class="value">v' + agent.version + '</span></div>'
        + '<div class="row"><span class="label">Score</span><span class="value ' + scoreClass + '">' + scoreText + '</span></div>'
        + '<div class="row"><span class="label">Benchmark</span><span class="value" style="font-family:monospace;font-size:12px">' + agent.benchmark + '</span></div>'
        + '<div class="row"><span class="label">Time</span><span class="value">' + new Date(agent.time).toLocaleString('en-US',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}) + '</span></div>';
      tooltip.style.display = 'block';
      tooltip.style.left = Math.min(e.clientX + 12, window.innerWidth - 310) + 'px';
      tooltip.style.top = Math.min(e.clientY + 12, window.innerHeight - 200) + 'px';
    });
    el.addEventListener('mouseenter', function() { this.style.filter = 'brightness(1.3)'; });
    el.addEventListener('mouseleave', function() { this.style.filter = 'none'; });
  });
  // Stats
  document.getElementById('bpCount').textContent = data.length;
  document.getElementById('agentCount').textContent = allAgents.length;
  document.getElementById('promotedCount').textContent = allAgents.filter(a => a.stage === 'promote' || a.stage === 'production').length;
  document.getElementById('timeRange').textContent =
    minTime.toLocaleDateString('en-US',{month:'short',day:'numeric',hour:'2-digit'}) + ' - '
    + maxTime.toLocaleDateString('en-US',{month:'short',day:'numeric',hour:'2-digit'});
  document.getElementById('timeDisplay').textContent = currentMaxTime.toLocaleString('en-US',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'});
  document.getElementById('timeSlider').value = ((currentMaxTime - minTime) / timeSpan) * 100;
}
document.addEventListener('click', function(e) {
  if (!e.target.closest('[data-agent]') && !e.target.closest('.tooltip')) {
    document.getElementById('tooltip').style.display = 'none';
  }
});
function updateSlider(val) {
  currentMaxTime = new Date(minTime.getTime() + timeSpan * (val / 100));
  render();
}
function togglePlay() {
  playing = !playing;
  document.getElementById('playBtn').textContent = playing ? 'Pause' : 'Play';
  document.getElementById('playBtn').classList.toggle('active', playing);
  if (playing) {
    let speed = parseInt(document.getElementById('speedSelect').value);
    playInterval = setInterval(() => {
      let pct = (currentMaxTime - minTime) / timeSpan + 0.015;
      if (pct >= 1) pct = 0;
      currentMaxTime = new Date(minTime.getTime() + timeSpan * pct);
      render();
    }, speed);
  } else {
    clearInterval(playInterval);
  }
}
function resetView() {
  if (playing) togglePlay();
  currentMaxTime = new Date(maxTime);
  render();
}
document.getElementById('speedSelect').addEventListener('change', function() {
  if (playing) {
    clearInterval(playInterval);
    playInterval = setInterval(() => {
      let pct = (currentMaxTime - minTime) / timeSpan + 0.015;
      if (pct >= 1) pct = 0;
      currentMaxTime = new Date(minTime.getTime() + timeSpan * pct);
      render();
    }, parseInt(this.value));
  }
});
window.addEventListener('resize', () => render());
render();
</script>
</body>
</html>
```
Spara som `timeline.html` och öppna direkt i webbläsaren. Allt är standalone — ingen server, inga dependencies.
Funktioner:
- SVG horisontell timeline, en track per blueprint
- Noder färgade: guld 85+, amber 70-84, blå under 70
- Diamant=spawn, cirkel=eval/improve, stjärna=promote, kryss=archived
- Time slider: dra eller auto-play (4 hastigheter)
- Klicka på nod: tooltip med run_id, version, stage, score, benchmark
- Anslutningslinjer mellan successiva agents per blueprint
- Scrubber line som följer aktuell tid
För att ladda riktig data från state.yaml, ersätt `BLUEPRINT_DATA` med:
```js
fetch('state.yaml')
  .then(r => r.text())
  .then(yamlText => {
    // använd js-yaml-biblioteket, eller inline-parser
    BLUEPRINT_DATA = jsyaml.load(yamlText);
    render();
  });
```
Åtgärda sidväxlingsproblemet först (öka virtuellt minne i Windows eller starta om) så kan jag skriva filen direkt och fortsätta.
⚠️ File-mutation verifier: 1 file(s) were NOT modified this turn despite any wording above that may suggest otherwise. Run `git status` or `read_file` to confirm.
  • `E:\Stryde\_alpedal\styde-forge\timeline.html` — [write_file] Failed to write file: 0 [main] bash (69904) child_copy: cygheap read copy failed, 0x0..0x80000A510, done 0, windows pid 69904, Win32 error 299 0 [main] bash 124280 dofork: child -…