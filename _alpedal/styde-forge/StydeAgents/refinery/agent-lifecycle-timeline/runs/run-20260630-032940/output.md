<!-- Agent Lifecycle Timeline -- real forge state data -->
<!-- 105 eval events, 18 blueprints, 2026-06-29T20:08 to 2026-06-30T03:31 -->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge -- Agent Lifecycle Timeline</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;background:#0d1117;color:#e6edf3;padding:16px}
h1{font-size:1.2rem;margin-bottom:4px;color:#f0f6fc}
.sub{color:#8b949e;font-size:.85rem;margin-bottom:20px}
.controls{display:flex;align-items:center;gap:12px;margin-bottom:12px;flex-wrap:wrap}
.controls button{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:.8rem}
.controls button:hover{background:#30363d}
.controls button.active{background:#1f6feb;border-color:#388bfd;color:#fff}
#scrubber{flex:1;min-width:120px;accent-color:#1f6feb}
#timeLabel{font-size:.75rem;color:#8b949e;min-width:140px;font-family:monospace}
.timeline-wrap{position:relative;overflow-x:auto;overflow-y:auto;max-height:85vh;border:1px solid #21262d;border-radius:8px;background:#161b22}
#timeline{display:block}
.track-label{font-size:.7rem;fill:#8b949e;font-family:monospace}
.node{cursor:pointer;transition:r .15s,opacity .3s}
.node:hover{opacity:1!important;r:6}
.node.gold{fill:#ffd700;stroke:#b8860b;stroke-width:1.5}
.node.amber{fill:#ff8c00;stroke:#cc7000;stroke-width:1}
.node.cool{fill:#58a6ff;stroke:#1f6feb;stroke-width:1}
.node.running{fill:#21262d;stroke:#484f58;stroke-width:1;stroke-dasharray:3 2}
#popup{display:none;position:fixed;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px 18px;box-shadow:0 8px 24px rgba(0,0,0,.4);z-index:1000;max-width:340px;font-size:.8rem;line-height:1.5}
#popup h3{color:#f0f6fc;margin-bottom:6px;font-size:.9rem}
#popup .row{display:flex;justify-content:space-between;gap:12px;padding:2px 0;border-bottom:1px solid #21262d}
#popup .row:last-child{border:none}
#popup .label{color:#8b949e}
#popup .val{color:#e6edf3;font-weight:500}
#popup .close{float:right;cursor:pointer;color:#8b949e;font-size:1.1rem;line-height:1;margin:-4px -4px 4px 4px}
#popup .close:hover{color:#f85149}
.legend{display:flex;gap:16px;margin:10px 0 14px;font-size:.7rem;flex-wrap:wrap}
.legend-item{display:flex;align-items:center;gap:5px;color:#8b949e}
.legend-dot{width:10px;height:10px;border-radius:50%;display:inline-block}
.legend-dot.gold{background:#ffd700}
.legend-dot.amber{background:#ff8c00}
.legend-dot.cool{background:#58a6ff}
.legend-dot.running{background:#21262d;border:1px dashed #484f58}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px;margin-bottom:12px}
.stat-card{background:#161b22;border:1px solid #21262d;border-radius:6px;padding:8px 12px;text-align:center}
.stat-card .num{font-size:1.3rem;font-weight:600;color:#f0f6fc}
.stat-card .desc{font-size:.65rem;color:#8b949e;margin-top:2px}
.time-indicator{font-size:.65rem;fill:#484f58;font-family:monospace}
</style>
</head>
<body>
<h1>Styde Forge Agent Lifecycle Timeline</h1>
<div class="sub">Real forge state data from state.yaml (2026-06-29T20:08 through 2026-06-30T03:31)</div>
<div class="stats" id="stats"></div>
<div class="controls">
  <button id="playBtn" title="Auto-play through time">Play</button>
  <button id="resetBtn" title="Reset to full view">Reset</button>
  <span style="color:#8b949e;font-size:.7rem">Scrub:</span>
  <input type="range" id="scrubber" min="0" max="100" value="100">
  <span id="timeLabel">all events</span>
</div>
<div class="legend">
  <span class="legend-item"><span class="legend-dot gold"></span> 85+ (gold)</span>
  <span class="legend-item"><span class="legend-dot amber"></span> 70-84 (amber)</span>
  <span class="legend-item"><span class="legend-dot cool"></span> below 70 (cool)</span>
  <span class="legend-item"><span class="legend-dot running"></span> Incomplete/running</span>
</div>
<div class="timeline-wrap" id="timelineWrap">
  <svg id="timeline"></svg>
</div>
<div id="popup">
  <span class="close" onclick="closePopup()">&times;</span>
  <h3 id="popTitle"></h3>
  <div id="popBody"></div>
</div>
<script>
// DATA: 105 eval events from 18 blueprints (parsed from state.yaml)
const EVALS = [
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:08:46Z", s:97, c:95.2, id:2179, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:12:03Z", s:97, c:95.2, id:2190, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:12:36Z", s:97, c:95.2, id:2188, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:15:20Z", s:97, c:95.2, id:2201, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:15:53Z", s:97, c:95.2, id:2198, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:18:37Z", s:97, c:95.2, id:2212, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:19:09Z", s:97, c:95.2, id:2209, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:21:53Z", s:97, c:95.2, id:2223, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:22:26Z", s:97, c:95.2, id:2221, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:25:11Z", s:97, c:95.2, id:2234, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:25:45Z", s:97, c:95.2, id:2231, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:28:30Z", s:97, c:95.2, id:2244, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:29:02Z", s:97, c:95.2, id:2242, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:31:46Z", s:97, c:95.2, id:2255, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:32:19Z", s:97, c:95.2, id:2253, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:35:05Z", s:97, c:95.2, id:2266, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:35:39Z", s:97, c:95.2, id:2264, detail:"S:97 J:94 C:95.2"},
{bp:"3d-data-terrain-explorer", ts:"2026-06-29T20:37:50Z", s:null, c:null, id:2275, detail:"iter 1/5"},
{bp:"aesthetic-style-composer", ts:"2026-06-29T20:41:36Z", s:null, c:null, id:4, detail:"iter 1/5"},
{bp:"aesthetic-style-composer", ts:"2026-06-29T20:48:16Z", s:78, c:79.2, id:5, detail:"S:78 J:80 C:79.2"},
{bp:"agent-promotion-evaluator", ts:"2026-06-29T20:55:26Z", s:93, c:93.6, id:9, detail:"S:93 J:94 C:93.6"},
{bp:"aesthetic-style-composer", ts:"2026-06-29T21:00:36Z", s:79, c:87.4, id:13, detail:"S:79 J:93 C:87.4"},
{bp:"aesthetic-style-composer", ts:"2026-06-29T21:01:32Z", s:79, c:87.4, id:11, detail:"S:79 J:93 C:87.4"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-29T21:02:28Z", s:null, c:null, id:15, detail:"iter 1/5"},
{bp:"agent-promotion-evaluator", ts:"2026-06-29T21:04:58Z", s:null, c:null, id:16, detail:"iter 1/5"},
{bp:"agent-promotion-evaluator", ts:"2026-06-29T21:06:43Z", s:5, c:39.2, id:19, detail:"S:5 J:62 C:39.2"},
{bp:"aesthetic-style-composer", ts:"2026-06-29T21:11:19Z", s:65, c:72.8, id:6, detail:"S:65 J:78 C:72.8"},
{bp:"agent-promotion-evaluator", ts:"2026-06-29T21:12:05Z", s:82, c:80.8, id:7, detail:"S:82 J:80 C:80.8"},
{bp:"agent-promotion-evaluator", ts:"2026-06-29T21:12:46Z", s:82, c:80.8, id:5, detail:"S:82 J:80 C:80.8"},
{bp:"aesthetic-style-composer", ts:"2026-06-29T21:19:16Z", s:72, c:70.8, id:12, detail:"S:72 J:70 C:70.8"},
{bp:"agent-promotion-evaluator", ts:"2026-06-29T21:27:48Z", s:88, c:91.6, id:26, detail:"S:88 J:94 C:91.6"},
{bp:"ai-copilot-query-panel", ts:"2026-06-29T21:30:44Z", s:75, c:79.8, id:30, detail:"S:75 J:83 C:79.8"},
{bp:"gpu-monitor-visualizer", ts:"2026-06-29T21:36:21Z", s:90, c:90.0, id:7, detail:"S:90 J:90 C:90.0"},
{bp:"dao-governance-designer", ts:"2026-06-29T21:36:53Z", s:92, c:86.6, id:9, detail:"S:92 J:83 C:86.6"},
{bp:"dao-governance-designer", ts:"2026-06-29T21:37:28Z", s:92, c:86.6, id:6, detail:"S:92 J:83 C:86.6"},
{bp:"clay-soft-interface-designer", ts:"2026-06-29T21:41:08Z", s:75, c:84.0, id:18, detail:"S:75 J:90 C:84.0"},
{bp:"aesthetic-style-composer", ts:"2026-06-29T21:43:06Z", s:null, c:null, id:22, detail:"Production-ready spec"},
{bp:"web-security-engineer", ts:"2026-06-29T21:44:59Z", s:null, c:null, id:28, detail:"iter 1/5"},
{bp:"data-cleaner", ts:"2026-06-29T21:48:22Z", s:null, c:null, id:30, detail:"iter 1/5"},
{bp:"data-cleaner", ts:"2026-06-29T22:00:17Z", s:42, c:63.6, id:9, detail:"S:42 J:78 C:63.6"},
{bp:"aesthetic-style-composer", ts:"2026-06-29T22:00:50Z", s:42, c:63.6, id:4, detail:"S:42 J:78 C:63.6"},
{bp:"sprint-coach", ts:"2026-06-29T22:03:33Z", s:null, c:null, id:17, detail:"iter 1/5"},
{bp:"sprint-coach", ts:"2026-06-29T22:04:40Z", s:76, c:83.8, id:18, detail:"S:76 J:89 C:83.8"},
{bp:"gpu-monitor-visualizer", ts:"2026-06-29T22:08:34Z", s:null, c:null, id:20, detail:"hollow greeting"},
{bp:"sprint-coach", ts:"2026-06-29T22:19:36Z", s:81, c:79.2, id:36, detail:"S:81 J:78 C:79.2"},
{bp:"customer-service-triage", ts:"2026-06-29T22:20:44Z", s:89, c:80.6, id:42, detail:"S:89 J:75 C:80.6"},
{bp:"caveman-mode-enforcer", ts:"2026-06-29T22:21:22Z", s:91, c:86.8, id:45, detail:"S:91 J:84 C:86.8"},
{bp:"sprint-coach", ts:"2026-06-29T22:23:12Z", s:78, c:84.0, id:50, detail:"S:78 J:88 C:84.0"},
{bp:"customer-service-triage", ts:"2026-06-29T22:27:52Z", s:58, c:64.0, id:62, detail:"S:58 J:68 C:64.0"},
{bp:"customer-service-triage", ts:"2026-06-29T22:28:26Z", s:58, c:64.0, id:61, detail:"S:58 J:68 C:64.0"},
{bp:"observability-platform-builder", ts:"2026-06-29T22:34:26Z", s:79, c:79.6, id:73, detail:"S:79 J:80 C:79.6"},
{bp:"observability-platform-builder", ts:"2026-06-29T22:34:59Z", s:79, c:79.6, id:70, detail:"S:79 J:80 C:79.6"},
{bp:"sprint-coach", ts:"2026-06-29T22:35:37Z", s:null, c:null, id:77, detail:"iter 1/5"},
{bp:"customer-feedback-analyzer", ts:"2026-06-29T22:36:11Z", s:68, c:51.2, id:78, detail:"S:68 J:40 C:51.2"},
{bp:"observability-platform-builder", ts:"2026-06-29T22:38:36Z", s:79, c:79.6, id:85, detail:"S:79 J:80 C:79.6"},
{bp:"observability-platform-builder", ts:"2026-06-29T22:39:09Z", s:79, c:79.6, id:84, detail:"S:79 J:80 C:79.6"},
{bp:"observability-platform-builder", ts:"2026-06-29T22:41:57Z", s:79, c:79.6, id:94, detail:"S:79 J:80 C:79.6"},
{bp:"observability-platform-builder", ts:"2026-06-29T22:42:33Z", s:79, c:79.6, id:91, detail:"S:79 J:80 C:79.6"},
{bp:"observability-platform-builder", ts:"2026-06-29T22:45:23Z", s:79, c:79.6, id:105, detail:"S:79 J:80 C:79.6"},
{bp:"observability-platform-builder", ts:"2026-06-29T22:45:58Z", s:79, c:79.6, id:103, detail:"S:79 J:80 C:79.6"},
{bp:"observability-platform-builder", ts:"2026-06-29T22:48:51Z", s:79, c:79.6, id:116, detail:"S:79 J:80 C:79.6"},
{bp:"observability-platform-builder", ts:"2026-06-29T22:51:07Z", s:null, c:null, id:123, detail:"iter 1/5"},
{bp:"observability-platform-builder", ts:"2026-06-29T22:51:41Z", s:79, c:79.6, id:126, detail:"S:79 J:80 C:79.6"},
{bp:"sprint-coach", ts:"2026-06-29T22:52:16Z", s:92, c:80.0, id:127, detail:"S:92 J:72 C:80.0"},
{bp:"observability-platform-builder", ts:"2026-06-29T22:54:29Z", s:null, c:null, id:134, detail:"iter 1/5"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-29T23:15:15Z", s:92, c:88.4, id:2, detail:"S:92 J:86 C:88.4"},
{bp:"anomaly-detection-visualizer", ts:"2026-06-29T23:24:37Z", s:null, c:null, id:2, detail:"iter 1/5"},
{bp:"aesthetic-style-composer", ts:"2026-06-30T02:11:53Z", s:72, c:81.0, id:4, detail:"S:72 J:87 C:81.0"},
{bp:"aesthetic-style-composer", ts:"2026-06-30T02:12:30Z", s:72, c:81.0, id:4, detail:"S:72 J:87 C:81.0"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T02:13:04Z", s:72, c:81.0, id:3, detail:"S:72 J:87 C:81.0"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T02:15:21Z", s:null, c:null, id:7, detail:"iter 1/5"},
{bp:"clay-soft-interface-designer", ts:"2026-06-30T02:17:56Z", s:null, c:null, id:6, detail:"66617 chars"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T02:18:35Z", s:10, c:28.0, id:9, detail:"S:10 J:40 C:28.0"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T02:19:10Z", s:10, c:28.0, id:7, detail:"S:10 J:40 C:28.0"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T02:23:45Z", s:null, c:null, id:15, detail:"iter 1/5"},
{bp:"aesthetic-style-composer", ts:"2026-06-30T02:26:53Z", s:83, c:85.4, id:19, detail:"S:83 J:87 C:85.4"},
{bp:"customer-service-triage", ts:"2026-06-30T02:32:54Z", s:null, c:null, id:22, detail:"20677 chars"},
{bp:"animation-design-engineer", ts:"2026-06-30T02:34:38Z", s:0, c:55.2, id:3, detail:"S:0 J:92 C:55.2"},
{bp:"anomaly-detection-visualizer", ts:"2026-06-30T02:35:14Z", s:55, c:56.8, id:6, detail:"S:55 J:58 C:56.8"},
{bp:"aesthetic-style-composer", ts:"2026-06-30T02:37:37Z", s:null, c:null, id:13, detail:"47009 chars"},
{bp:"ai-copilot-query-panel", ts:"2026-06-30T02:38:21Z", s:73, c:79.0, id:27, detail:"S:73 J:83 C:79.0"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T02:43:08Z", s:null, c:null, id:13, detail:"iter 1/5"},
{bp:"clay-soft-interface-designer", ts:"2026-06-30T02:44:36Z", s:87, c:88.8, id:17, detail:"S:87 J:90 C:88.8"},
{bp:"aesthetic-style-composer", ts:"2026-06-30T02:45:21Z", s:null, c:null, id:16, detail:"verification plus explicit"},
{bp:"aesthetic-style-composer", ts:"2026-06-30T02:47:58Z", s:null, c:null, id:19, detail:"Produktionsklar spec (88.8)"},
{bp:"agent-promotion-evaluator", ts:"2026-06-30T02:50:11Z", s:null, c:null, id:8, detail:"Composite 79.4 -- gate pass"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T02:51:44Z", s:83, c:86.0, id:19, detail:"S:83 J:88 C:86.0"},
{bp:"ai-copilot-query-panel", ts:"2026-06-30T02:52:21Z", s:83, c:86.0, id:18, detail:"S:83 J:88 C:86.0"},
{bp:"customer-service-triage", ts:"2026-06-30T02:54:08Z", s:null, c:null, id:33, detail:"764 chars"},
{bp:"color-palette-originator", ts:"2026-06-30T02:54:57Z", s:82, c:85.6, id:26, detail:"S:82 J:88 C:85.6"},
{bp:"data-cleaner", ts:"2026-06-30T02:56:53Z", s:92, c:86.6, id:23, detail:"S:92 J:83 C:86.6"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T03:00:41Z", s:55, c:74.2, id:35, detail:"S:55 J:87 C:74.2"},
{bp:"animation-design-engineer", ts:"2026-06-30T03:09:51Z", s:0, c:27.0, id:48, detail:"S:0 J:45 C:27.0"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T03:11:58Z", s:null, c:null, id:22, detail:"iter 1/5"},
{bp:"color-palette-originator", ts:"2026-06-30T03:13:25Z", s:86, c:90.2, id:33, detail:"S:86 J:93 C:90.2"},
{bp:"sprint-coach", ts:"2026-06-30T03:14:07Z", s:86, c:90.2, id:31, detail:"S:86 J:93 C:90.2"},
{bp:"ai-copilot-query-panel", ts:"2026-06-30T03:17:19Z", s:47, c:57.8, id:32, detail:"S:47 J:65 C:57.8"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T03:23:10Z", s:null, c:null, id:6, detail:"iter 1/5"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T03:24:34Z", s:null, c:null, id:10, detail:"15596 chars"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T03:25:49Z", s:79, c:86.8, id:31, detail:"S:79 J:92 C:86.8"},
{bp:"animation-design-engineer", ts:"2026-06-30T03:26:45Z", s:5, c:14.0, id:39, detail:"S:5 J:20 C:14.0"},
{bp:"sprint-coach", ts:"2026-06-30T03:27:21Z", s:5, c:14.0, id:38, detail:"S:5 J:20 C:14.0"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T03:28:56Z", s:83, c:84.2, id:35, detail:"S:83 J:85 C:84.2"},
{bp:"sprint-coach", ts:"2026-06-30T03:29:47Z", s:null, c:null, id:28, detail:"failed to produce deliverable"},
{bp:"agent-lifecycle-timeline", ts:"2026-06-30T03:31:07Z", s:55, c:71.2, id:7, detail:"S:55 J:82 C:71.2"}
];
// Group by blueprint
const blueprints = [...new Set(EVALS.map(e=>e.bp))].sort();
const bpGroups = {};
blueprints.forEach(b=>bpGroups[b]=EVALS.filter(e=>e.bp===b));
// Time range
const times = EVALS.filter(e=>e.ts).map(e=>new Date(e.ts).getTime());
const tMin = Math.min(...times);
const tMax = Math.max(...times);
const tRange = tMax-tMin || 1;
// Build SVG
const TRACK_H = 24;
const LABEL_W = 220;
const PAD_L = LABEL_W + 10;
const PAD_R = 40;
const NODE_R = 4;
const VIS_W = 1400;
const H = blueprints.length * TRACK_H + 30;
function render(scrubPct) {
  const svg = document.getElementById('timeline');
  const cutoff = tMin + (tRange * scrubPct / 100);
  let html = `<svg width="${VIS_W}" height="${H}" viewBox="0 0 ${VIS_W} ${H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#161b22"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
  </defs>
  <rect width="${VIS_W}" height="${H}" fill="url(#bgGrad)"/>
  <line x1="${PAD_L-5}" y1="0" x2="${PAD_L-5}" y2="${H}" stroke="#21262d" stroke-width="1"/>
  <line x1="${VIS_W-PAD_R+5}" y1="0" x2="${VIS_W-PAD_R+5}" y2="${H}" stroke="#21262d" stroke-width="1"/>`;
  // Time indicators every ~2 hours
  const stepSecs = 7200;
  for(let t=tMin; t<=tMax; t+=stepSecs*1000) {
    const x = PAD_L + ((t-tMin)/tRange)*(VIS_W-PAD_L-PAD_R);
    const d = new Date(t);
    const label = d.getUTCHours().toString().padStart(2,'0') + ':' + d.getUTCMinutes().toString().padStart(2,'0');
    html += `<text x="${x}" y="${H-4}" text-anchor="middle" class="time-indicator">${label}</text>`;
    html += `<line x1="${x}" y1="0" x2="${x}" y2="${H-14}" stroke="#21262d" stroke-width="0.5" stroke-dasharray="3 3"/>`;
  }
  // Timeline baseline
  html += `<line x1="${PAD_L}" y1="0" x2="${VIS_W-PAD_R}" y2="0" stroke="#30363d" stroke-width="0.5"/>`;
  blueprints.forEach((bp, i) => {
    const y = i*TRACK_H + 18;
    const evals = bpGroups[bp];
    const activeEvals = evals.filter(e => e.ts && new Date(e.ts).getTime() <= cutoff);
    const inactiveEvals = evals.filter(e => e.ts && new Date(e.ts).getTime() > cutoff);
    // Track line
    html += `<line x1="${PAD_L}" y1="${y}" x2="${VIS_W-PAD_R}" y2="${y}" stroke="#21262d" stroke-width="1"/>`;
    // Label
    const label = bp.length > 28 ? bp.slice(0,25)+'...' : bp;
    html += `<text x="${PAD_L-8}" y="${y+4}" text-anchor="end" class="track-label">${label}</text>`;
    // Inactive nodes (dimmed)
    inactiveEvals.forEach(e => {
      const ex = PAD_L + ((new Date(e.ts).getTime()-tMin)/tRange)*(VIS_W-PAD_L-PAD_R);
      let cls = 'cool';
      if(e.s !== null) cls = e.s >= 85 ? 'gold' : e.s >= 70 ? 'amber' : 'cool';
      else cls = 'running';
      html += `<circle class="node ${cls}" cx="${ex}" cy="${y}" r="${NODE_R-1}" opacity="0.15" onclick="showPopup('${bp}',${e.id})"/>`;
    });
    // Active nodes (full opacity)
    activeEvals.forEach(e => {
      const ex = PAD_L + ((new Date(e.ts).getTime()-tMin)/tRange)*(VIS_W-PAD_L-PAD_R);
      let cls = 'cool';
      if(e.s !== null) cls = e.s >= 85 ? 'gold' : e.s >= 70 ? 'amber' : 'cool';
      else cls = 'running';
      html += `<circle class="node ${cls}" cx="${ex}" cy="${y}" r="${NODE_R}" onclick="showPopup('${bp.replace(/'/g,"\\'")}',${e.id},${e.s},${e.c},'${e.ts}','${e.detail.replace(/'/g,"\\'")}')"/>`;
    });
  });
  // Scrubber line
  const sx = PAD_L + (scrubPct/100)*(VIS_W-PAD_L-PAD_R);
  html += `<line x1="${sx}" y1="0" x2="${sx}" y2="${H-14}" stroke="#1f6feb" stroke-width="1.5" stroke-dasharray="4 2" opacity="0.7"/>`;
  html += `<circle cx="${sx}" cy="0" r="3" fill="#1f6feb"/>`;
  html += '</svg>';
  svg.innerHTML = html;
}
// Popup
function showPopup(bp, id, s, c, ts, detail) {
  const pop = document.getElementById('popup');
  document.getElementById('popTitle').textContent = bp + ' (agent #' + id + ')';
  let body = `<div class="row"><span class="label">Score (S)</span><span class="val">${s !== null && s !== undefined ? s : 'N/A'}</span></div>`;
  body += `<div class="row"><span class="label">Composite</span><span class="val">${c !== null && c !== undefined ? c : 'N/A'}</span></div>`;
  body += `<div class="row"><span class="label">Timestamp</span><span class="val" style="font-size:.7rem;font-family:monospace">${ts || 'N/A'}</span></div>`;
  body += `<div class="row"><span class="label">Status</span><span class="val">${s !== null && s !== undefined ? 'Complete' : 'Incomplete'}</span></div>`;
  body += `<div style="margin-top:6px;color:#8b949e;font-size:.7rem;word-break:break-all">${detail || ''}</div>`;
  document.getElementById('popBody').innerHTML = body;
  pop.style.display = 'block';
  pop.style.left = Math.min(event.clientX + 10, window.innerWidth - 360) + 'px';
  pop.style.top = Math.min(event.clientY - 10, window.innerHeight - 220) + 'px';
}
function closePopup() { document.getElementById('popup').style.display = 'none'; }
document.addEventListener('click', function(e) {
  if(!e.target.closest('#popup') && !e.target.closest('.node')) closePopup();
});
// Stats
function renderStats() {
  const scored = EVALS.filter(e=>e.s!==null);
  const gold = scored.filter(e=>e.s>=85).length;
  const amber = scored.filter(e=>e.s>=70&&e.s<85).length;
  const cool = scored.filter(e=>e.s<70).length;
  const cHigh = Math.max(...scored.map(e=>e.c));
  const avgC = (scored.reduce((a,e)=>a+e.c,0)/scored.length).toFixed(1);
  document.getElementById('stats').innerHTML = `
    <div class="stat-card"><div class="num">${EVALS.length}</div><div class="desc">Total evals</div></div>
    <div class="stat-card"><div class="num">${blueprints.length}</div><div class="desc">Blueprints</div></div>
    <div class="stat-card"><div class="num" style="color:#ffd700">${gold}</div><div class="desc">Gold (85+)</div></div>
    <div class="stat-card"><div class="num" style="color:#ff8c00">${amber}</div><div class="desc">Amber (70-84)</div></div>
    <div class="stat-card"><div class="num" style="color:#58a6ff">${cool}</div><div class="desc">Cool (<70)</div></div>
    <div class="stat-card"><div class="num" style="color:#3fb950">${avgC}</div><div class="desc">Avg composite</div></div>
    <div class="stat-card"><div class="num" style="color:#ffd700">${cHigh}</div><div class="desc">Best composite</div></div>
  `;
}
// Controls
let playing = false;
let playInterval = null;
document.getElementById('playBtn').addEventListener('click', function() {
  playing = !playing;
  this.textContent = playing ? 'Pause' : 'Play';
  this.classList.toggle('active');
  if(playing) {
    const scrub = document.getElementById('scrubber');
    playInterval = setInterval(() => {
      let v = parseInt(scrub.value) + 1;
      if(v > 100) { v = 0; }
      scrub.value = v;
      scrub.dispatchEvent(new Event('input'));
    }, 150);
  } else {
    clearInterval(playInterval);
  }
});
document.getElementById('resetBtn').addEventListener('click', function() {
  if(playing) { document.getElementById('playBtn').click(); }
  document.getElementById('scrubber').value = 100;
  document.getElementById('scrubber').dispatchEvent(new Event('input'));
});
document.getElementById('scrubber').addEventListener('input', function() {
  const v = parseInt(this.value);
  render(v);
  if(v >= 100) {
    document.getElementById('timeLabel').textContent = 'all events';
  } else {
    const pct = v;
    document.getElementById('timeLabel').textContent = `showing ~${pct}% of timeline`;
  }
});
// Init
renderStats();
render(100);
document.getElementById('scrubber').value = 100;
</script>
</body>
</html>