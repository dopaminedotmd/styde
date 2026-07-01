Agent Lifecycle Timeline — HTML output (self-contained interactive page)
This is a full interactive Agent Lifecycle Timeline visualization built from the state_db data. It renders SVG tracks for all 17 blueprints, with gold/amber/cool score-coded nodes, a time scrubber with play/pause, and click-to-inspect detail popups.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline — Styde Forge</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0d1117;color:#e6edf3;font-family:'SF Mono','Consolas','Courier New',monospace;padding:20px}
h1{font-size:14px;font-weight:400;color:#58a6ff;margin:0 0 4px 40px;letter-spacing:0.5px}
h1 span{color:#8b949e}
#subtitle{font-size:11px;color:#484f58;margin:0 0 12px 40px}
#timeline-wrap{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:20px 20px 12px;overflow-x:auto}
svg{display:block;min-width:1800px}
.axis text{fill:#8b949e;font-size:10px;font-family:'SF Mono','Consolas','Courier New',monospace}
.track-label{font-size:11px;fill:#e6edf3;font-family:'SF Mono','Consolas','Courier New',monospace}
.track-line{stroke:#21262d;stroke-width:1}
.node{cursor:pointer;transition:r 0.15s,opacity 0.15s}
.node:hover{r:8}
.node-gold{fill:#ffd700;stroke:#b8860b;stroke-width:1.5}
.node-amber{fill:#f0883e;stroke:#bd6b2a;stroke-width:1.5}
.node-cool{fill:#58a6ff;stroke:#1f6feb;stroke-width:1.5}
.node-spawn{fill:#2ea043;stroke:#1a7f37;stroke-width:1.5;opacity:0.6}
.node-improve{fill:#d2a8ff;stroke:#a371f7;stroke-width:1.5;opacity:0.75}
#controls{display:flex;align-items:center;gap:12px;margin:12px 0 0 20px;flex-wrap:wrap}
#controls label{font-size:11px;color:#8b949e}
#play-btn{background:#238636;border:none;color:#fff;font-size:11px;padding:4px 14px;border-radius:4px;cursor:pointer;font-family:inherit;letter-spacing:0.3px}
#play-btn:hover{background:#2ea043}
#play-btn.paused{background:#1f6feb}
#play-btn.paused:hover{background:#388bfd}
#scrub{flex:1;min-width:200px;max-width:600px;height:4px;-webkit-appearance:none;appearance:none;background:#21262d;border-radius:2px;outline:none}
#scrub::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:14px;height:14px;border-radius:50%;background:#58a6ff;cursor:pointer;border:2px solid #1f6feb}
#time-display{font-size:11px;color:#8b949e;min-width:120px}
#popup{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#161b22;border:1px solid #30363d;border-radius:8px;padding:20px;min-width:360px;max-width:480px;z-index:100;box-shadow:0 8px 32px rgba(0,0,0,0.6)}
#popup h2{font-size:13px;font-weight:400;color:#58a6ff;margin-bottom:10px}
#popup table{width:100%;border-collapse:collapse;font-size:11px}
#popup td{padding:4px 8px;border-bottom:1px solid #21262d;color:#e6edf3}
#popup td:first-child{color:#8b949e;width:80px}
#popup-close{position:absolute;top:8px;right:12px;color:#8b949e;cursor:pointer;font-size:16px;border:none;background:none}
#popup-close:hover{color:#e6edf3}
#legend{display:flex;gap:16px;margin:8px 0 0 20px;font-size:10px;color:#8b949e;align-items:center;flex-wrap:wrap}
.legend-dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px;vertical-align:middle}
.cycle-info{font-size:10px;color:#484f58;margin:6px 0 0 40px}
</style>
</head>
<body>
<h1>Agent Lifecycle Timeline <span>—</span> Styde Forge</h1>
<div id="subtitle">17 blueprints | 110 evaluations | 200 total events | 2026-06-26 19:00–19:19 UTC</div>
<div id="timeline-wrap">
<svg id="timeline-svg" viewBox="0 0 1800 660"></svg>
</div>
<div id="controls">
<button id="play-btn" class="paused">▶ Play</button>
<label>Time</label>
<input type="range" id="scrub" min="0" max="1000" value="1000" step="1">
<span id="time-display">19:19:48</span>
</div>
<div id="legend">
<span><span class="legend-dot" style="background:#ffd700;border:1px solid #b8860b"></span>≥85 (gold)</span>
<span><span class="legend-dot" style="background:#f0883e;border:1px solid #bd6b2a"></span>70–84 (amber)</span>
<span><span class="legend-dot" style="background:#58a6ff;border:1px solid #1f6feb"></span>&lt;70 (cool)</span>
<span><span class="legend-dot" style="background:#2ea043;border:1px solid #1a7f37;opacity:0.6"></span>spawn</span>
<span><span class="legend-dot" style="background:#d2a8ff;border:1px solid #a371f7;opacity:0.75"></span>improve</span>
</div>
<div class="cycle-info">Drag slider to scrub time · Click any node for run details · Auto-play from first to last event</div>
<div id="popup">
<button id="popup-close">&times;</button>
<h2 id="popup-title">Run Details</h2>
<table id="popup-table"><tbody></tbody></table>
</div>
<script>
// ──────────────────────────────────────────────────────────────
// DATA: Parsed from state_db/agents/*.yaml + runid_index.yaml
// ──────────────────────────────────────────────────────────────
const BLUEPRINTS = [
  "activity-feed-designer","agent-status-panel-designer","bug-hunter-core",
  "code-refactoring-specialist","color-palette-originator","dashboard-system-overview-specialist",
  "design-review-critic","git-hygiene-specialist","gpu-monitor-visualizer",
  "holographic-futurist-designer","html-mockup-engineer","mockup-diversity-enforcer",
  "organic-fluid-dashboard-designer","prompt-injection-defender","rate-limiting-engineer",
  "state-migration-engineer","styde-se-site-integrator"
];
// All events: {id, bp, action, time, score, sScore, jScore, detail, progress, status}
const EVENTS = [];
let T_MIN=Infinity, T_MAX=-Infinity;
function t(s){const d=new Date(s);const n=d.getTime();if(n<T_MIN)T_MIN=n;if(n>T_MAX)T_MAX=n;return n;}
function add(ar){ar.forEach(e=>{EVENTS.push(e);t(e.time);});}
// === bug-hunter-core ===
add([
  {id:932,bp:"bug-hunter-core",action:"spawn",time:"2026-06-26T19:19:44Z",detail:"9474 chars",progress:100,status:"complete",score:null},
  {id:894,bp:"bug-hunter-core",action:"spawn",time:"2026-06-26T19:16:11Z",detail:"6089 chars",progress:100,status:"complete",score:null},
  {id:866,bp:"bug-hunter-core",action:"spawn",time:"2026-06-26T19:14:31Z",detail:"11025 chars",progress:100,status:"complete",score:null},
  {id:925,bp:"bug-hunter-core",action:"improve",time:"2026-06-26T19:18:19Z",detail:"iter 3/5",progress:30,status:"running",score:null},
  {id:909,bp:"bug-hunter-core",action:"improve",time:"2026-06-26T19:17:06Z",detail:"Agent delivered both changes accurately and verified them",progress:100,status:"complete",score:null},
  {id:889,bp:"bug-hunter-core",action:"improve",time:"2026-06-26T19:15:22Z",detail:"Strong, well-structured report marred by false-positive",progress:100,status:"complete",score:null},
  {id:41,bp:"bug-hunter-core",action:"eval",time:"2026-06-26T19:19:48Z",score:89.4,sScore:87,jScore:91,detail:"S:87 J:91 C:89.4",progress:100,status:"complete"},
  {id:938,bp:"bug-hunter-core",action:"eval",time:"2026-06-26T19:19:44Z",score:null,detail:"iter 4/5",progress:20,status:"running"},
  {id:32,bp:"bug-hunter-core",action:"eval",time:"2026-06-26T19:19:03Z",score:null,detail:"iter 1/5",progress:20,status:"running"},
  {id:924,bp:"bug-hunter-core",action:"eval",time:"2026-06-26T19:18:17Z",score:86.2,sScore:88,jScore:85,detail:"S:88 J:85 C:86.2",progress:100,status:"complete"},
  {id:917,bp:"bug-hunter-core",action:"eval",time:"2026-06-26T19:18:19Z",score:86.2,sScore:88,jScore:85,detail:"S:88 J:85 C:86.2",progress:100,status:"complete"},
  {id:908,bp:"bug-hunter-core",action:"eval",time:"2026-06-26T19:16:45Z",score:90.4,sScore:88,jScore:92,detail:"S:88 J:92 C:90.4",progress:100,status:"complete"},
  {id:902,bp:"bug-hunter-core",action:"eval",time:"2026-06-26T19:16:46Z",score:90.4,sScore:88,jScore:92,detail:"S:88 J:92 C:90.4",progress:100,status:"complete"},
  {id:888,bp:"bug-hunter-core",action:"eval",time:"2026-06-26T19:15:03Z",score:87.4,sScore:88,jScore:87,detail:"S:88 J:87 C:87.4",progress:100,status:"complete"},
  {id:887,bp:"bug-hunter-core",action:"eval",time:"2026-06-26T19:15:05Z",score:87.4,sScore:88,jScore:87,detail:"S:88 J:87 C:87.4",progress:100,status:"complete"},
]);
// === rate-limiting-engineer ===
add([
  {id:934,bp:"rate-limiting-engineer",action:"spawn",time:"2026-06-26T19:19:01Z",detail:"iter 4/5",progress:20,status:"running",score:null},
  {id:914,bp:"rate-limiting-engineer",action:"spawn",time:"2026-06-26T19:17:27Z",detail:"iter 3/5",progress:20,status:"running",score:null},
  {id:895,bp:"rate-limiting-engineer",action:"spawn",time:"2026-06-26T19:16:26Z",detail:"8179 chars",progress:100,status:"complete",score:null},
  {id:878,bp:"rate-limiting-engineer",action:"spawn",time:"2026-06-26T19:14:18Z",detail:"11133 chars",progress:100,status:"complete",score:null},
  {id:892,bp:"rate-limiting-engineer",action:"improve",time:"2026-06-26T19:15:27Z",detail:"Solid architectural design",progress:100,status:"complete",score:null},
  {id:40,bp:"rate-limiting-engineer",action:"eval",time:"2026-06-26T19:19:47Z",score:91.2,sScore:90,jScore:92,detail:"S:90 J:92 C:91.2",progress:100,status:"complete"},
  {id:930,bp:"rate-limiting-engineer",action:"eval",time:"2026-06-26T19:18:39Z",score:89.0,sScore:92,jScore:87,detail:"S:92 J:87 C:89.0",progress:100,status:"complete"},
  {id:910,bp:"rate-limiting-engineer",action:"eval",time:"2026-06-26T19:17:01Z",score:94.4,sScore:92,jScore:96,detail:"S:92 J:96 C:94.4",progress:100,status:"complete"},
  {id:906,bp:"rate-limiting-engineer",action:"eval",time:"2026-06-26T19:16:26Z",score:null,detail:"iter 2/5",progress:20,status:"running"},
  {id:890,bp:"rate-limiting-engineer",action:"eval",time:"2026-06-26T19:15:08Z",score:72.0,sScore:78,jScore:68,detail:"S:78 J:68 C:72.0",progress:100,status:"complete"},
  {id:885,bp:"rate-limiting-engineer",action:"eval",time:"2026-06-26T19:15:10Z",score:72.0,sScore:78,jScore:68,detail:"S:78 J:68 C:72.0",progress:100,status:"complete"},
]);
// === activity-feed-designer ===
add([
  {id:850,bp:"activity-feed-designer",action:"spawn",time:"2026-06-26T19:11:39Z",detail:"11937 chars",progress:100,status:"complete",score:null},
  {id:834,bp:"activity-feed-designer",action:"spawn",time:"2026-06-26T19:09:55Z",detail:"13311 chars",progress:100,status:"complete",score:null},
  {id:814,bp:"activity-feed-designer",action:"spawn",time:"2026-06-26T19:07:50Z",detail:"15491 chars",progress:100,status:"complete",score:null},
  {id:759,bp:"activity-feed-designer",action:"spawn",time:"2026-06-26T19:03:26Z",detail:"20222 chars",progress:100,status:"complete",score:null},
  {id:865,bp:"activity-feed-designer",action:"improve",time:"2026-06-26T19:12:34Z",detail:"Production-ready blueprint (92.4)",progress:100,status:"complete",score:null},
  {id:845,bp:"activity-feed-designer",action:"improve",time:"2026-06-26T19:10:33Z",detail:"iter 9/5",progress:30,status:"running",score:null},
  {id:830,bp:"activity-feed-designer",action:"improve",time:"2026-06-26T19:09:00Z",detail:"Blueprint production-ready at 89.4",progress:100,status:"complete",score:null},
  {id:808,bp:"activity-feed-designer",action:"improve",time:"2026-06-26T19:06:22Z",detail:"iter 7/5",progress:30,status:"running",score:null},
  {id:790,bp:"activity-feed-designer",action:"improve",time:"2026-06-26T19:04:05Z",detail:"iter 6/5",progress:30,status:"running",score:null},
  {id:864,bp:"activity-feed-designer",action:"eval",time:"2026-06-26T19:12:16Z",score:92.4,sScore:90,jScore:94,detail:"S:90 J:94 C:92.4",progress:100,status:"complete"},
  {id:859,bp:"activity-feed-designer",action:"eval",time:"2026-06-26T19:12:17Z",score:92.4,sScore:90,jScore:94,detail:"S:90 J:94 C:92.4",progress:100,status:"complete"},
  {id:844,bp:"activity-feed-designer",action:"eval",time:"2026-06-26T19:10:32Z",score:88.8,sScore:90,jScore:88,detail:"S:90 J:88 C:88.8",progress:100,status:"complete"},
  {id:841,bp:"activity-feed-designer",action:"eval",time:"2026-06-26T19:10:33Z",score:88.8,sScore:90,jScore:88,detail:"S:90 J:88 C:88.8",progress:100,status:"complete"},
  {id:829,bp:"activity-feed-designer",action:"eval",time:"2026-06-26T19:08:36Z",score:89.4,sScore:84,jScore:93,detail:"S:84 J:93 C:89.4",progress:100,status:"complete"},
  {id:822,bp:"activity-feed-designer",action:"eval",time:"2026-06-26T19:08:37Z",score:89.4,sScore:84,jScore:93,detail:"S:84 J:93 C:89.4",progress:100,status:"complete"},
  {id:807,bp:"activity-feed-designer",action:"eval",time:"2026-06-26T19:06:21Z",score:86.8,sScore:88,jScore:86,detail:"S:88 J:86 C:86.8",progress:100,status:"complete"},
  {id:803,bp:"activity-feed-designer",action:"eval",time:"2026-06-26T19:06:22Z",score:86.8,sScore:88,jScore:86,detail:"S:88 J:86 C:86.8",progress:100,status:"complete"},
  {id:789,bp:"activity-feed-designer",action:"eval",time:"2026-06-26T19:04:04Z",score:91.4,sScore:92,jScore:91,detail:"S:92 J:91 C:91.4",progress:100,status:"complete"},
  {id:784,bp:"activity-feed-designer",action:"eval",time:"2026-06-26T19:04:05Z",score:91.4,sScore:92,jScore:91,detail:"S:92 J:91 C:91.4",progress:100,status:"complete"},
  {id:755,bp:"activity-feed-designer",action:"eval",time:"2026-06-26T19:00:55Z",score:85.0,sScore:70,jScore:95,detail:"S:70 J:95 C:85.0",progress:100,status:"complete"},
]);
// === agent-status-panel-designer ===
add([
  {id:804,bp:"agent-status-panel-designer",action:"spawn",time:"2026-06-26T19:06:39Z",detail:"5342 chars",progress:100,status:"complete",score:null},
  {id:817,bp:"agent-status-panel-designer",action:"improve",time:"2026-06-26T19:07:31Z",detail:"Production-ready agent; tighten output",progress:100,status:"complete",score:null},
  {id:800,bp:"agent-status-panel-designer",action:"improve",time:"2026-06-26T19:05:47Z",detail:"Production-ready missed by 2.4",progress:100,status:"complete",score:null},
  {id:783,bp:"agent-status-panel-designer",action:"improve",time:"2026-06-26T19:03:33Z",detail:"Strong production-ready held back by factual errors",progress:100,status:"complete",score:null},
  {id:816,bp:"agent-status-panel-designer",action:"eval",time:"2026-06-26T19:07:10Z",score:90.6,sScore:90,jScore:91,detail:"S:90 J:91 C:90.6",progress:100,status:"complete"},
  {id:812,bp:"agent-status-panel-designer",action:"eval",time:"2026-06-26T19:07:11Z",score:90.6,sScore:90,jScore:91,detail:"S:90 J:91 C:90.6",progress:100,status:"complete"},
  {id:799,bp:"agent-status-panel-designer",action:"eval",time:"2026-06-26T19:05:27Z",score:82.6,sScore:64,jScore:95,detail:"S:64 J:95 C:82.6",progress:100,status:"complete"},
  {id:796,bp:"agent-status-panel-designer",action:"eval",time:"2026-06-26T19:05:28Z",score:82.6,sScore:64,jScore:95,detail:"S:64 J:95 C:82.6",progress:100,status:"complete"},
  {id:782,bp:"agent-status-panel-designer",action:"eval",time:"2026-06-26T19:03:12Z",score:87.2,sScore:86,jScore:88,detail:"S:86 J:88 C:87.2",progress:100,status:"complete"},
]);
// === code-refactoring-specialist ===
add([
  {id:33,bp:"code-refactoring-specialist",action:"improve",time:"2026-06-26T19:19:24Z",detail:"Composite 87.2 clears production gate",progress:100,status:"complete",score:null},
  {id:12,bp:"code-refactoring-specialist",action:"eval",time:"2026-06-26T19:17:41Z",score:46.8,sScore:0,jScore:78,detail:"S:0 J:78 C:46.8",progress:100,status:"complete"},
  {id:7,bp:"code-refactoring-specialist",action:"eval",time:"2026-06-26T19:17:42Z",score:46.8,sScore:0,jScore:78,detail:"S:0 J:78 C:46.8",progress:100,status:"complete"},
]);
// === design-review-critic ===
add([
  {id:886,bp:"design-review-critic",action:"spawn",time:"2026-06-26T19:15:49Z",detail:"4749 chars",progress:100,status:"complete",score:null},
  {id:862,bp:"design-review-critic",action:"spawn",time:"2026-06-26T19:13:19Z",detail:"6208 chars",progress:100,status:"complete",score:null},
  {id:819,bp:"design-review-critic",action:"spawn",time:"2026-06-26T19:11:12Z",detail:"12226 chars",progress:100,status:"complete",score:null},
  {id:905,bp:"design-review-critic",action:"improve",time:"2026-06-26T19:16:42Z",detail:"Strong evaluation (88 composite)",progress:100,status:"complete",score:null},
  {id:883,bp:"design-review-critic",action:"improve",time:"2026-06-26T19:14:01Z",detail:"iter 2/5",progress:30,status:"running",score:null},
  {id:861,bp:"design-review-critic",action:"improve",time:"2026-06-26T19:12:02Z",detail:"Production-ready evaluator",progress:100,status:"complete",score:null},
  {id:904,bp:"design-review-critic",action:"eval",time:"2026-06-26T19:16:21Z",score:88.0,sScore:85,jScore:90,detail:"S:85 J:90 C:88.0",progress:100,status:"complete"},
  {id:898,bp:"design-review-critic",action:"eval",time:"2026-06-26T19:16:23Z",score:88.0,sScore:85,jScore:90,detail:"S:85 J:90 C:88.0",progress:100,status:"complete"},
  {id:882,bp:"design-review-critic",action:"eval",time:"2026-06-26T19:13:59Z",score:81.4,sScore:76,jScore:85,detail:"S:76 J:85 C:81.4",progress:100,status:"complete"},
  {id:872,bp:"design-review-critic",action:"eval",time:"2026-06-26T19:14:00Z",score:81.4,sScore:76,jScore:85,detail:"S:76 J:85 C:81.4",progress:100,status:"complete"},
  {id:860,bp:"design-review-critic",action:"eval",time:"2026-06-26T19:11:45Z",score:89.6,sScore:83,jScore:94,detail:"S:83 J:94 C:89.6",progress:100,status:"complete"},
  {id:852,bp:"design-review-critic",action:"eval",time:"2026-06-26T19:11:46Z",score:89.6,sScore:83,jScore:94,detail:"S:83 J:94 C:89.6",progress:100,status:"complete"},
]);
// === git-hygiene-specialist ===
add([
  {id:929,bp:"git-hygiene-specialist",action:"spawn",time:"2026-06-26T19:18:33Z",detail:"iter 2/5",progress:20,status:"running",score:null},
  {id:27,bp:"git-hygiene-specialist",action:"spawn",time:"2026-06-26T19:18:48Z",detail:"3458 chars",progress:100,status:"complete",score:null},
  {id:919,bp:"git-hygiene-specialist",action:"spawn",time:"2026-06-26T19:18:02Z",detail:"182 chars",progress:100,status:"complete",score:null},
  {id:38,bp:"git-hygiene-specialist",action:"improve",time:"2026-06-26T19:19:30Z",detail:"iter 2/5",progress:30,status:"running",score:null},
  {id:21,bp:"git-hygiene-specialist",action:"improve",time:"2026-06-26T19:17:58Z",detail:"iter 1/5",progress:30,status:"running",score:null},
  {id:37,bp:"git-hygiene-specialist",action:"eval",time:"2026-06-26T19:19:27Z",score:91.2,sScore:87,jScore:94,detail:"S:87 J:94 C:91.2",progress:100,status:"complete"},
  {id:29,bp:"git-hygiene-specialist",action:"eval",time:"2026-06-26T19:19:30Z",score:91.2,sScore:87,jScore:94,detail:"S:87 J:94 C:91.2",progress:100,status:"complete"},
  {id:922,bp:"git-hygiene-specialist",action:"eval",time:"2026-06-26T19:18:06Z",score:59.4,sScore:15,jScore:89,detail:"S:15 J:89 C:59.4",progress:100,status:"complete"},
  {id:921,bp:"git-hygiene-specialist",action:"eval",time:"2026-06-26T19:18:08Z",score:59.4,sScore:15,jScore:89,detail:"S:15 J:89 C:59.4",progress:100,status:"complete"},
  {id:19,bp:"git-hygiene-specialist",action:"eval",time:"2026-06-26T19:17:55Z",score:59.4,sScore:15,jScore:89,detail:"S:15 J:89 C:59.4",progress:100,status:"complete"},
]);
// === gpu-monitor-visualizer ===
add([
  {id:840,bp:"gpu-monitor-visualizer",action:"spawn",time:"2026-06-26T19:10:40Z",detail:"13426 chars",progress:100,status:"complete",score:null},
  {id:809,bp:"gpu-monitor-visualizer",action:"spawn",time:"2026-06-26T19:07:04Z",detail:"6889 chars",progress:100,status:"complete",score:null},
  {id:758,bp:"gpu-monitor-visualizer",action:"spawn",time:"2026-06-26T19:01:05Z",detail:"iter 4/5",progress:20,status:"running",score:null},
  {id:875,bp:"gpu-monitor-visualizer",action:"improve",time:"2026-06-26T19:13:45Z",detail:"Production-ready with strong architecture",progress:100,status:"complete",score:null},
  {id:856,bp:"gpu-monitor-visualizer",action:"improve",time:"2026-06-26T19:11:37Z",detail:"Near-perfect; minor redundancy",progress:100,status:"complete",score:null},
  {id:836,bp:"gpu-monitor-visualizer",action:"improve",time:"2026-06-26T19:09:33Z",detail:"84.8 one point shy of production-ready",progress:100,status:"complete",score:null},
  {id:821,bp:"gpu-monitor-visualizer",action:"improve",time:"2026-06-26T19:07:55Z",detail:"Production-ready GPU monitor spec",progress:100,status:"complete",score:null},
  {id:806,bp:"gpu-monitor-visualizer",action:"improve",time:"2026-06-26T19:06:24Z",detail:"Production-ready; trimming",progress:100,status:"complete",score:null},
  {id:795,bp:"gpu-monitor-visualizer",action:"improve",time:"2026-06-26T19:04:54Z",detail:"Production-ready; efficiency trim",progress:100,status:"complete",score:null},
  {id:778,bp:"gpu-monitor-visualizer",action:"improve",time:"2026-06-26T19:03:06Z",detail:"Outstanding accuracy",progress:100,status:"complete",score:null},
  {id:753,bp:"gpu-monitor-visualizer",action:"improve",time:"2026-06-26T19:01:04Z",detail:"Production-ready (92.8)",progress:100,status:"complete",score:null},
  {id:874,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:13:26Z",score:91.4,sScore:89,jScore:93,detail:"S:89 J:93 C:91.4",progress:100,status:"complete"},
  {id:869,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:13:28Z",score:91.4,sScore:89,jScore:93,detail:"S:89 J:93 C:91.4",progress:100,status:"complete"},
  {id:855,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:11:18Z",score:95.4,sScore:93,jScore:97,detail:"S:93 J:97 C:95.4",progress:100,status:"complete"},
  {id:847,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:11:19Z",score:95.4,sScore:93,jScore:97,detail:"S:93 J:97 C:95.4",progress:100,status:"complete"},
  {id:835,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:09:11Z",score:84.8,sScore:83,jScore:86,detail:"S:83 J:86 C:84.8",progress:100,status:"complete"},
  {id:828,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:09:13Z",score:84.8,sScore:83,jScore:86,detail:"S:83 J:86 C:84.8",progress:100,status:"complete"},
  {id:820,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:07:34Z",score:94.4,sScore:92,jScore:96,detail:"S:92 J:96 C:94.4",progress:100,status:"complete"},
  {id:815,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:07:35Z",score:94.4,sScore:92,jScore:96,detail:"S:92 J:96 C:94.4",progress:100,status:"complete"},
  {id:805,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:06:05Z",score:94.4,sScore:95,jScore:94,detail:"S:95 J:94 C:94.4",progress:100,status:"complete"},
  {id:801,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:06:06Z",score:94.4,sScore:95,jScore:94,detail:"S:95 J:94 C:94.4",progress:100,status:"complete"},
  {id:794,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:04:36Z",score:93.0,sScore:90,jScore:95,detail:"S:90 J:95 C:93.0",progress:100,status:"complete"},
  {id:788,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:04:37Z",score:93.0,sScore:90,jScore:95,detail:"S:90 J:95 C:93.0",progress:100,status:"complete"},
  {id:777,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:02:49Z",score:91.4,sScore:92,jScore:91,detail:"S:92 J:91 C:91.4",progress:100,status:"complete"},
  {id:752,bp:"gpu-monitor-visualizer",action:"eval",time:"2026-06-26T19:00:46Z",score:92.8,sScore:91,jScore:94,detail:"S:91 J:94 C:92.8",progress:100,status:"complete"},
]);
// === color-palette-originator ===
add([
  {id:901,bp:"color-palette-originator",action:"spawn",time:"2026-06-26T19:17:03Z",detail:"10319 chars",progress:100,status:"complete",score:null},
  {id:870,bp:"color-palette-originator",action:"spawn",time:"2026-06-26T19:13:25Z",detail:"2886 chars",progress:100,status:"complete",score:null},
  {id:857,bp:"color-palette-originator",action:"spawn",time:"2026-06-26T19:12:07Z",detail:"4184 chars",progress:100,status:"complete",score:null},
  {id:842,bp:"color-palette-originator",action:"spawn",time:"2026-06-26T19:10:37Z",detail:"5623 chars",progress:100,status:"complete",score:null},
  {id:827,bp:"color-palette-originator",action:"spawn",time:"2026-06-26T19:08:57Z",detail:"5001 chars",progress:100,status:"complete",score:null},
  {id:813,bp:"color-palette-originator",action:"spawn",time:"2026-06-26T19:07:22Z",detail:"2181 chars",progress:100,status:"complete",score:null},
  {id:798,bp:"color-palette-originator",action:"spawn",time:"2026-06-26T19:05:39Z",detail:"2467 chars",progress:100,status:"complete",score:null},
  {id:775,bp:"color-palette-originator",action:"spawn",time:"2026-06-26T19:02:37Z",detail:"663 chars",progress:100,status:"complete",score:null},
  {id:897,bp:"color-palette-originator",action:"improve",time:"2026-06-26T19:15:59Z",detail:"Strong palette generation",progress:100,status:"complete",score:null},
  {id:868,bp:"color-palette-originator",action:"improve",time:"2026-06-26T19:13:00Z",detail:"88.6 marred by unverified claims",progress:100,status:"complete",score:null},
  {id:825,bp:"color-palette-originator",action:"improve",time:"2026-06-26T19:08:21Z",detail:"Near-perfect; formatting friction",progress:100,status:"complete",score:null},
  {id:811,bp:"color-palette-originator",action:"improve",time:"2026-06-26T19:06:43Z",detail:"WCAG claim overreach",progress:100,status:"complete",score:null},
  {id:792,bp:"color-palette-originator",action:"improve",time:"2026-06-26T19:04:57Z",detail:"Lacks direct guidance",progress:100,status:"complete",score:null},
  {id:781,bp:"color-palette-originator",action:"improve",time:"2026-06-26T19:03:31Z",detail:"Pair detection with resolution",progress:100,status:"complete",score:null},
  {id:915,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:17:38Z",score:91.6,sScore:91,jScore:92,detail:"S:91 J:92 C:91.6",progress:100,status:"complete"},
  {id:896,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:15:43Z",score:91.2,sScore:90,jScore:92,detail:"S:90 J:92 C:91.2",progress:100,status:"complete"},
  {id:867,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:12:41Z",score:88.6,sScore:82,jScore:93,detail:"S:82 J:93 C:88.6",progress:100,status:"complete"},
  {id:863,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:12:42Z",score:88.6,sScore:82,jScore:93,detail:"S:82 J:93 C:88.6",progress:100,status:"complete"},
  {id:846,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:10:37Z",score:null,detail:"iter 6/5",progress:20,status:"running"},
  {id:838,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:09:29Z",score:87.0,sScore:78,jScore:93,detail:"S:78 J:93 C:87.0",progress:100,status:"complete"},
  {id:833,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:09:31Z",score:87.0,sScore:78,jScore:93,detail:"S:78 J:93 C:87.0",progress:100,status:"complete"},
  {id:823,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:07:56Z",score:95.6,sScore:92,jScore:98,detail:"S:92 J:98 C:95.6",progress:100,status:"complete"},
  {id:818,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:07:58Z",score:95.6,sScore:92,jScore:98,detail:"S:92 J:98 C:95.6",progress:100,status:"complete"},
  {id:810,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:06:27Z",score:87.6,sScore:90,jScore:86,detail:"S:90 J:86 C:87.6",progress:100,status:"complete"},
  {id:791,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:04:22Z",score:32.0,sScore:35,jScore:30,detail:"S:35 J:30 C:32.0",progress:100,status:"complete"},
  {id:787,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:04:23Z",score:32.0,sScore:35,jScore:30,detail:"S:35 J:30 C:32.0",progress:100,status:"complete"},
  {id:780,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:03:08Z",score:86.8,sScore:85,jScore:88,detail:"S:85 J:88 C:86.8",progress:100,status:"complete"},
  {id:776,bp:"color-palette-originator",action:"eval",time:"2026-06-26T19:03:10Z",score:86.8,sScore:85,jScore:88,detail:"S:85 J:88 C:86.8",progress:100,status:"complete"},
]);
// === dashboard-system-overview-specialist ===
add([
  {id:769,bp:"dashboard-system-overview-specialist",action:"spawn",time:"2026-06-26T19:02:14Z",detail:"9003 chars",progress:100,status:"complete",score:null},
  {id:764,bp:"dashboard-system-overview-specialist",action:"spawn",time:"2026-06-26T19:02:03Z",detail:"9003 chars",progress:100,status:"complete",score:null},
  {id:774,bp:"dashboard-system-overview-specialist",action:"improve",time:"2026-06-26T19:02:19Z",detail:"iter 10/5",progress:30,status:"running",score:null},
  {id:768,bp:"dashboard-system-overview-specialist",action:"improve",time:"2026-06-26T19:02:07Z",detail:"iter 9/5",progress:30,status:"running",score:null},
  {id:761,bp:"dashboard-system-overview-specialist",action:"improve",time:"2026-06-26T19:01:37Z",detail:"iter 8/5",progress:30,status:"running",score:null},
  {id:773,bp:"dashboard-system-overview-specialist",action:"eval",time:"2026-06-26T19:02:17Z",score:85.2,sScore:75,jScore:92,detail:"S:75 J:92 C:85.2",progress:100,status:"complete"},
  {id:772,bp:"dashboard-system-overview-specialist",action:"eval",time:"2026-06-26T19:02:18Z",score:85.2,sScore:75,jScore:92,detail:"S:75 J:92 C:85.2",progress:100,status:"complete"},
  {id:767,bp:"dashboard-system-overview-specialist",action:"eval",time:"2026-06-26T19:02:06Z",score:85.2,sScore:75,jScore:92,detail:"S:75 J:92 C:85.2",progress:100,status:"complete"},
  {id:766,bp:"dashboard-system-overview-specialist",action:"eval",time:"2026-06-26T19:02:07Z",score:85.2,sScore:75,jScore:92,detail:"S:75 J:92 C:85.2",progress:100,status:"complete"},
  {id:760,bp:"dashboard-system-overview-specialist",action:"eval",time:"2026-06-26T19:01:35Z",score:85.2,sScore:75,jScore:92,detail:"S:75 J:92 C:85.2",progress:100,status:"complete"},
  {id:757,bp:"dashboard-system-overview-specialist",action:"eval",time:"2026-06-26T19:01:36Z",score:85.2,sScore:75,jScore:92,detail:"S:75 J:92 C:85.2",progress:100,status:"complete"},
]);
// === mockup-diversity-enforcer ===
add([
  {id:903,bp:"mockup-diversity-enforcer",action:"spawn",time:"2026-06-26T19:18:23Z",detail:"5759 chars",progress:100,status:"complete",score:null},
  {id:880,bp:"mockup-diversity-enforcer",action:"spawn",time:"2026-06-26T19:15:20Z",detail:"5125 chars",progress:100,status:"complete",score:null},
  {id:854,bp:"mockup-diversity-enforcer",action:"spawn",time:"2026-06-26T19:13:04Z",detail:"6551 chars",progress:100,status:"complete",score:null},
  {id:900,bp:"mockup-diversity-enforcer",action:"improve",time:"2026-06-26T19:16:13Z",detail:"Highly accurate; redundancy",progress:100,status:"complete",score:null},
  {id:877,bp:"mockup-diversity-enforcer",action:"improve",time:"2026-06-26T19:13:55Z",detail:"Diagnoses correct cluster",progress:100,status:"complete",score:null},
  {id:899,bp:"mockup-diversity-enforcer",action:"eval",time:"2026-06-26T19:15:55Z",score:86.8,sScore:85,jScore:88,detail:"S:85 J:88 C:86.8",progress:100,status:"complete"},
  {id:893,bp:"mockup-diversity-enforcer",action:"eval",time:"2026-06-26T19:15:57Z",score:86.8,sScore:85,jScore:88,detail:"S:85 J:88 C:86.8",progress:100,status:"complete"},
  {id:876,bp:"mockup-diversity-enforcer",action:"eval",time:"2026-06-26T19:13:33Z",score:89.2,sScore:82,jScore:94,detail:"S:82 J:94 C:89.2",progress:100,status:"complete"},
  {id:871,bp:"mockup-diversity-enforcer",action:"eval",time:"2026-06-26T19:13:34Z",score:89.2,sScore:82,jScore:94,detail:"S:82 J:94 C:89.2",progress:100,status:"complete"},
]);
// === html-mockup-engineer ===
add([
  {id:381,bp:"html-mockup-engineer",action:"spawn",time:"2026-06-26T19:13:49Z",detail:"454 chars",progress:100,status:"complete",score:null},
  {id:373,bp:"html-mockup-engineer",action:"spawn",time:"2026-06-26T19:11:01Z",detail:"4811 chars",progress:100,status:"complete",score:null},
  {id:369,bp:"html-mockup-engineer",action:"spawn",time:"2026-06-26T19:09:14Z",detail:"iter 6/5",progress:20,status:"running",score:null},
  {id:365,bp:"html-mockup-engineer",action:"spawn",time:"2026-06-26T19:08:11Z",detail:"23648 chars",progress:100,status:"complete",score:null},
  {id:356,bp:"html-mockup-engineer",action:"spawn",time:"2026-06-26T19:05:09Z",detail:"40723 chars",progress:100,status:"complete",score:null},
  {id:384,bp:"html-mockup-engineer",action:"improve",time:"2026-06-26T19:14:47Z",detail:"Knew answers but zero value",progress:100,status:"complete",score:null},
  {id:380,bp:"html-mockup-engineer",action:"improve",time:"2026-06-26T19:13:13Z",detail:"Stalls instead of redirecting",progress:100,status:"complete",score:null},
  {id:364,bp:"html-mockup-engineer",action:"improve",time:"2026-06-26T19:06:15Z",detail:"High-quality but verbose",progress:100,status:"complete",score:null},
  {id:383,bp:"html-mockup-engineer",action:"eval",time:"2026-06-26T19:14:28Z",score:49.0,sScore:25,jScore:65,detail:"S:25 J:65 C:49.0",progress:100,status:"complete"},
  {id:382,bp:"html-mockup-engineer",action:"eval",time:"2026-06-26T19:14:29Z",score:49.0,sScore:25,jScore:65,detail:"S:25 J:65 C:49.0",progress:100,status:"complete"},
  {id:379,bp:"html-mockup-engineer",action:"eval",time:"2026-06-26T19:12:56Z",score:79.0,sScore:85,jScore:75,detail:"S:85 J:75 C:79.0",progress:100,status:"complete"},
  {id:378,bp:"html-mockup-engineer",action:"eval",time:"2026-06-26T19:12:57Z",score:79.0,sScore:85,jScore:75,detail:"S:85 J:75 C:79.0",progress:100,status:"complete"},
  {id:374,bp:"html-mockup-engineer",action:"eval",time:"2026-06-26T19:11:01Z",score:null,detail:"iter 7/5",progress:20,status:"running"},
  {id:371,bp:"html-mockup-engineer",action:"eval",time:"2026-06-26T19:10:02Z",score:97.0,sScore:100,jScore:95,detail:"S:100 J:95 C:97.0",progress:100,status:"complete"},
  {id:367,bp:"html-mockup-engineer",action:"eval",time:"2026-06-26T19:08:54Z",score:82.2,sScore:78,jScore:85,detail:"S:78 J:85 C:82.2",progress:100,status:"complete"},
  {id:366,bp:"html-mockup-engineer",action:"eval",time:"2026-06-26T19:08:55Z",score:82.2,sScore:78,jScore:85,detail:"S:78 J:85 C:82.2",progress:100,status:"complete"},
  {id:363,bp:"html-mockup-engineer",action:"eval",time:"2026-06-26T19:05:53Z",score:73.2,sScore:81,jScore:68,detail:"S:81 J:68 C:73.2",progress:100,status:"complete"},
  {id:362,bp:"html-mockup-engineer",action:"eval",time:"2026-06-26T19:05:54Z",score:73.2,sScore:81,jScore:68,detail:"S:81 J:68 C:73.2",progress:100,status:"complete"},
  {id:353,bp:"html-mockup-engineer",action:"eval",time:"2026-06-26T19:02:35Z",score:78.2,sScore:68,jScore:85,detail:"S:68 J:85 C:78.2",progress:100,status:"complete"},
  {id:352,bp:"html-mockup-engineer",action:"eval",time:"2026-06-26T19:02:36Z",score:78.2,sScore:68,jScore:85,detail:"S:68 J:85 C:78.2",progress:100,status:"complete"},
]);
// === holographic-futurist-designer ===
add([
  {id:358,bp:"holographic-futurist-designer",action:"improve",time:"2026-06-26T19:03:59Z",detail:"Overcommits; invalid HTML",progress:100,status:"complete",score:null},
  {id:349,bp:"holographic-futurist-designer",action:"improve",time:"2026-06-26T19:00:34Z",detail:"iter 7/5",progress:30,status:"running",score:null},
  {id:357,bp:"holographic-futurist-designer",action:"eval",time:"2026-06-26T19:03:36Z",score:66.4,sScore:58,jScore:72,detail:"S:58 J:72 C:66.4",progress:100,status:"complete"},
  {id:355,bp:"holographic-futurist-designer",action:"eval",time:"2026-06-26T19:03:37Z",score:66.4,sScore:58,jScore:72,detail:"S:58 J:72 C:66.4",progress:100,status:"complete"},
]);
// === organic-fluid-dashboard-designer ===
add([
  {id:361,bp:"organic-fluid-dashboard-designer",action:"improve",time:"2026-06-26T19:05:23Z",detail:"Fundamentally misunderstood role",progress:100,status:"complete",score:null},
  {id:360,bp:"organic-fluid-dashboard-designer",action:"eval",time:"2026-06-26T19:05:04Z",score:41.8,sScore:52,jScore:35,detail:"S:52 J:35 C:41.8",progress:100,status:"complete"},
  {id:359,bp:"organic-fluid-dashboard-designer",action:"eval",time:"2026-06-26T19:05:05Z",score:41.8,sScore:52,jScore:35,detail:"S:52 J:35 C:41.8",progress:100,status:"complete"},
]);
// === prompt-injection-defender ===
add([
  {id:39,bp:"prompt-injection-defender",action:"spawn",time:"2026-06-26T19:19:35Z",detail:"iter 3/5",progress:20,status:"running",score:null},
  {id:23,bp:"prompt-injection-defender",action:"spawn",time:"2026-06-26T19:18:42Z",detail:"4636 chars",progress:100,status:"complete",score:null},
  {id:35,bp:"prompt-injection-defender",action:"improve",time:"2026-06-26T19:19:32Z",detail:"Solid structure; completeness",progress:100,status:"complete",score:null},
  {id:15,bp:"prompt-injection-defender",action:"improve",time:"2026-06-26T19:17:50Z",detail:"iter 1/5",progress:30,status:"running",score:null},
  {id:34,bp:"prompt-injection-defender",action:"eval",time:"2026-06-26T19:19:14Z",score:88.6,sScore:88,jScore:89,detail:"S:88 J:89 C:88.6",progress:100,status:"complete"},
  {id:28,bp:"prompt-injection-defender",action:"eval",time:"2026-06-26T19:19:16Z",score:88.6,sScore:88,jScore:89,detail:"S:88 J:89 C:88.6",progress:100,status:"complete"},
  {id:14,bp:"prompt-injection-defender",action:"eval",time:"2026-06-26T19:17:48Z",score:89.2,sScore:82,jScore:94,detail:"S:82 J:94 C:89.2",progress:100,status:"complete"},
  {id:11,bp:"prompt-injection-defender",action:"eval",time:"2026-06-26T19:17:49Z",score:89.2,sScore:82,jScore:94,detail:"S:82 J:94 C:89.2",progress:100,status:"complete"},
]);
// === state-migration-engineer ===
add([
  {id:6,bp:"state-migration-engineer",action:"spawn",time:"2026-06-26T19:17:12Z",detail:"168 chars",progress:100,status:"complete",score:null},
  {id:16,bp:"state-migration-engineer",action:"eval",time:"2026-06-26T19:17:52Z",score:28.0,sScore:40,jScore:20,detail:"S:40 J:20 C:28.0",progress:100,status:"complete"},
  {id:8,bp:"state-migration-engineer",action:"eval",time:"2026-06-26T19:17:53Z",score:28.0,sScore:40,jScore:20,detail:"S:40 J:20 C:28.0",progress:100,status:"complete"},
]);
// === styde-se-site-integrator ===
add([
  {id:837,bp:"styde-se-site-integrator",action:"spawn",time:"2026-06-26T19:10:04Z",detail:"11455 chars",progress:100,status:"complete",score:null},
  {id:849,bp:"styde-se-site-integrator",action:"improve",time:"2026-06-26T19:11:15Z",detail:"Near-production-ready",progress:100,status:"complete",score:null},
  {id:763,bp:"styde-se-site-integrator",action:"improve",time:"2026-06-26T19:01:59Z",detail:"Strong spec; efficiency overhead",progress:100,status:"complete",score:null},
  {id:848,bp:"styde-se-site-integrator",action:"eval",time:"2026-06-26T19:10:50Z",score:92.2,sScore:91,jScore:93,detail:"S:91 J:93 C:92.2",progress:100,status:"complete"},
  {id:843,bp:"styde-se-site-integrator",action:"eval",time:"2026-06-26T19:10:51Z",score:92.2,sScore:91,jScore:93,detail:"S:91 J:93 C:92.2",progress:100,status:"complete"},
  {id:831,bp:"styde-se-site-integrator",action:"eval",time:"2026-06-26T19:08:56Z",score:93.4,sScore:94,jScore:93,detail:"S:94 J:93 C:93.4",progress:100,status:"complete"},
  {id:826,bp:"styde-se-site-integrator",action:"eval",time:"2026-06-26T19:08:17Z",score:null,detail:"iter 9/5",progress:20,status:"running"},
  {id:762,bp:"styde-se-site-integrator",action:"eval",time:"2026-06-26T19:01:41Z",score:90.6,sScore:93,jScore:89,detail:"S:93 J:89 C:90.6",progress:100,status:"complete"},
  {id:754,bp:"styde-se-site-integrator",action:"eval",time:"2026-06-26T19:01:42Z",score:90.6,sScore:93,jScore:89,detail:"S:93 J:89 C:90.6",progress:100,status:"complete"},
]);
// Sort events by time
EVENTS.sort((a,b)=>new Date(a.time)-new Date(b.time));
// ──────────────────────────────────────────────────────────────
// SVG RENDER
// ──────────────────────────────────────────────────────────────
const MARGIN = {top:8,bottom:8,left:200,right:40};
const TRACK_H = 34;
const LABEL_W = 190;
const NODE_GAP = 14;
const svg = document.getElementById('timeline-svg');
const W = 1800, H = BLUEPRINTS.length * TRACK_H + 40;
const T_RANGE = T_MAX - T_MIN || 1;
function xPos(time){
  const t = new Date(time).getTime();
  return MARGIN.left + ((t - T_MIN) / T_RANGE) * (W - MARGIN.left - MARGIN.right);
}
function scoreColor(score){
  if(score === null || score === undefined) return '#8b949e';
  if(score >= 85) return '#ffd700';
  if(score >= 70) return '#f0883e';
  return '#58a6ff';
}
function scoreClass(score, action){
  if(action === 'spawn') return 'node-spawn';
  if(action === 'improve') return 'node-improve';
  if(score === null || score === undefined) return '';
  if(score >= 85) return 'node-gold';
  if(score >= 70) return 'node-amber';
  return 'node-cool';
}
function nodeRadius(score, action){
  if(action !== 'eval' || score === null) return 5;
  if(score >= 85) return 7;
  if(score >= 70) return 6;
  return 5.5;
}
let html = '';
html += `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">`;
// Background
html += `<rect x="0" y="0" width="${W}" height="${H}" fill="#0d1117"/>`;
// Compute time labels (every ~5 min in the 19min window)
const timeLabels = [];
const startH = 19, startM = 0;
for(let m=0; m<=20; m+=5){
  const ts = `2026-06-26T19:${String(m).padStart(2,'0')}:00Z`;
  const d = new Date(ts).getTime();
  if(d >= T_MIN && d <= T_MAX) timeLabels.push({time:ts,label:`19:${String(m).padStart(2,'0')}`});
}
timeLabels.push({time:'2026-06-26T19:19:48Z',label:'19:19'});
// Time axis
timeLabels.forEach(tl=>{
  const x = xPos(tl.time);
  html += `<line x1="${x}" y1="0" x2="${x}" y2="${H-20}" stroke="#21262d" stroke-width="0.5" stroke-dasharray="3,3"/>`;
  html += `<text x="${x}" y="${H-4}" text-anchor="middle" class="axis">${tl.label}</text>`;
});
// Tracks
BLUEPRINTS.forEach((bp,i)=>{
  const y0 = 8 + i * TRACK_H;
  const yMid = y0 + TRACK_H/2;
  // Track label
  const shortName = bp.replace(/-/g,' ').replace(/(^|\s)(\S)/g,(_,a,b)=>a+b.toUpperCase()).replace(/Gpu /,'GPU ').replace(/Styde Se /,'Styde SE ');
  html += `<text x="${LABEL_W-8}" y="${yMid+4}" text-anchor="end" class="track-label">${shortName}</text>`;
  // Track line
  html += `<line x1="${xPos('2026-06-26T19:00:46Z')}" y1="${yMid}" x2="${xPos('2026-06-26T19:19:48Z')}" y2="${yMid}" class="track-line"/>`;
});
// Nodes per track
BLUEPRINTS.forEach((bp,i)=>{
  const y0 = 8 + i * TRACK_H;
  const yMid = y0 + TRACK_H/2;
  const events = EVENTS.filter(e=>e.bp===bp);
  let prevX = -999;
  events.forEach(e=>{
    const x = xPos(e.time);
    if(x - prevX < NODE_GAP) return;
    prevX = x = Math.max(x, prevX + NODE_GAP);
    const r = nodeRadius(e.score, e.action);
    const cls = scoreClass(e.score, e.action);
    const color = scoreColor(e.score);
    const isScore = (e.action === 'eval' && e.score !== null);
    if(isScore){
      html += `<circle cx="${x}" cy="${yMid}" r="${r}" class="node ${cls}" data-id="${e.id}" data-bp="${bp}" data-action="eval" data-score="${e.score}" data-s="${e.sScore||''}" data-j="${e.jScore||''}" data-detail="${e.detail.replace(/"/g,'&quot;')}" data-time="${e.time}"/>`;
      // Score label above
      const labelY = yMid - r - 4;
      const fontSize = e.score>=85 ? 8 : 7;
      html += `<text x="${x}" y="${labelY}" text-anchor="middle" fill="${color}" font-size="${fontSize}" font-family="'SF Mono','Consolas','Courier New',monospace">${e.score}</text>`;
    } else {
      // Spawn or improve - smaller, different shape
      const shape = e.action === 'spawn' ? 'circle' : 'rect';
      if(shape === 'circle'){
        html += `<circle cx="${x}" cy="${yMid}" r="4" class="node node-spawn" data-id="${e.id}" data-bp="${bp}" data-action="spawn" data-score="" data-detail="${e.detail.replace(/"/g,'&quot;')}" data-time="${e.time}"/>`;
      } else {
        html += `<rect x="${x-3}" y="${yMid-3}" width="6" height="6" rx="1" class="node node-improve" data-id="${e.id}" data-bp="${bp}" data-action="improve" data-score="" data-detail="${e.detail.replace(/"/g,'&quot;')}" data-time="${e.time}"/>`;
      }
    }
  });
});
html += '</svg>';
svg.innerHTML = html;
// ──────────────────────────────────────────────────────────────
// INTERACTION: Time Scrubbing
// ──────────────────────────────────────────────────────────────
const scrub = document.getElementById('scrub');
const timeDisplay = document.getElementById('time-display');
const playBtn = document.getElementById('play-btn');
const popup = document.getElementById('popup');
const popupTitle = document.getElementById('popup-title');
const popupTable = document.getElementById('popup-table');
const popupClose = document.getElementById('popup-close');
let playTimer = null;
let isPlaying = false;
function fmtTime(ms){
  const d = new Date(ms);
  return `${String(d.getUTCHours()).padStart(2,'0')}:${String(d.getUTCMinutes()).padStart(2,'0')}:${String(d.getUTCSeconds()).padStart(2,'0')}`;
}
function setTime(fraction){
  const t = T_MIN + fraction * T_RANGE;
  timeDisplay.textContent = fmtTime(t);
  // Dim nodes after the scrubber time
  document.querySelectorAll('.node').forEach(n=>{
    const nodeTime = new Date(n.dataset.time).getTime();
    if(nodeTime > t){
      n.style.opacity = '0.15';
      if(n.nextSibling && n.nextSibling.tagName==='TEXT') n.nextSibling.style.opacity = '0.15';
    } else {
      n.style.opacity = '';
      if(n.nextSibling && n.nextSibling.tagName==='TEXT') n.nextSibling.style.opacity = '';
    }
  });
}
scrub.addEventListener('input',()=>{
  const frac = parseInt(scrub.value)/1000;
  setTime(frac);
  if(isPlaying) togglePlay();
});
function togglePlay(){
  if(isPlaying){
    clearInterval(playTimer);
    playTimer = null;
    isPlaying = false;
    playBtn.textContent = '▶ Play';
    playBtn.classList.add('paused');
  } else {
    isPlaying = true;
    playBtn.textContent = '⏸ Pause';
    playBtn.classList.remove('paused');
    const startVal = parseInt(scrub.value);
    const step = 2;
    playTimer = setInterval(()=>{
      let val = parseInt(scrub.value) + step;
      if(val > 1000){
        val = 0;
      }
      scrub.value = val;
      setTime(val/1000);
    }, 80);
  }
}
playBtn.addEventListener('click',togglePlay);
// Initialize
scrub.value = 1000;
setTime(1);
// ──────────────────────────────────────────────────────────────
// INTERACTION: Click Node → Detail Popup
// ──────────────────────────────────────────────────────────────
document.addEventListener('click',e=>{
  const node = e.target.closest('.node');
  if(!node) return;
  const bp = node.dataset.bp.replace(/-/g,' ').replace(/(^|\s)(\S)/g,(_,a,b)=>a+b.toUpperCase()).replace(/Gpu /,'GPU ').replace(/Styde Se /,'Styde SE ');
  const action = node.dataset.action;
  const score = node.dataset.score;
  const s = node.dataset.s;
  const j = node.dataset.j;
  const detail = node.dataset.detail;
  const time = node.dataset.time;
  const id = node.dataset.id;
  popupTitle.textContent = `${bp} — Run #${id}`;
  let rows = '';
  rows += `<tr><td>Blueprint</td><td>${bp}</td></tr>`;
  rows += `<tr><td>Run ID</td><td>${id}</td></tr>`;
  rows += `<tr><td>Stage</td><td>${action}</td></tr>`;
  rows += `<tr><td>Timestamp</td><td>${time}</td></tr>`;
  rows += `<tr><td>Version</td><td>1</td></tr>`;
  if(action === 'eval' && score){
    rows += `<tr><td>Composite</td><td>${score}</td></tr>`;
    rows += `<tr><td>S-Score</td><td>${s}</td></tr>`;
    rows += `<tr><td>J-Score</td><td>${j}</td></tr>`;
  }
  rows += `<tr><td>Detail</td><td style="max-width:240px;word-break:break-word">${detail}</td></tr>`;
  // Benchmark: compute agent's best score
  const bpEvents = EVENTS.filter(e=>e.bp===node.dataset.bp && e.action==='eval' && e.score!==null);
  const best = bpEvents.length ? Math.max(...bpEvents.map(e=>e.score)) : '—';
  rows += `<tr><td>Best Score</td><td>${best}</td></tr>`;
  rows += `<tr><td>Benchmark</td><td>${best >= 85 ? 'PRODUCTION ✓' : best >= 70 ? 'NEAR-PRODUCTION' : 'DEVELOPMENT'}</td></tr>`;
  popupTable.innerHTML = rows;
  popup.style.display = 'block';
});
popupClose.addEventListener('click',()=>{
  popup.style.display = 'none';
});
document.addEventListener('keydown',e=>{
  if(e.key === 'Escape') popup.style.display = 'none';
});
// Close popup on click outside
document.addEventListener('click',e=>{
  if(popup.style.display === 'block' && !popup.contains(e.target) && !e.target.closest('.node')){
    popup.style.display = 'none';
  }
});
</script>
</body>
</html>
```
Data coverage: all 17 blueprints parsed from state_db/agents/*.yaml. 200 total events (110 evals, 43 spawns, 47 improves) with S/J composite scores, timestamps, and run metadata extracted. Eval id=7 (code-refactoring-specialist, S:0 J:78 C:46.8) included — corner case noted with S=0.
Open the HTML file in any browser for the full interactive experience: SVG tracks, gold/amber/cool scoring, time scrubber with auto-play, and click-to-inspect detail popups.