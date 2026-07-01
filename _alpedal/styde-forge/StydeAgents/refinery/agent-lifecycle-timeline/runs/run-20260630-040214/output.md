```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Agent Lifecycle Timeline</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:system-ui,-apple-system,sans-serif;background:#0d1117;color:#e6edf3;overflow-x:hidden}
.timeline-container{max-width:1400px;margin:0 auto;padding:20px}
.header{padding:16px 0;border-bottom:1px solid #30363d;margin-bottom:24px}
.header h1{font-size:24px;font-weight:600;color:#f0f6fc}
.header span{color:#8b949e;font-size:14px;margin-left:8px}
.controls{display:flex;gap:16px;align-items:center;margin-bottom:20px;flex-wrap:wrap}
.controls button{padding:8px 20px;border:1px solid #30363d;border-radius:6px;background:#21262d;color:#e6edf3;cursor:pointer;font-size:14px;transition:.15s}
.controls button:hover{background:#30363d;border-color:#58a6ff}
.controls button.active{background:#1f6feb;border-color:#58a6ff;color:#fff}
.slider-wrapper{flex:1;min-width:200px;display:flex;align-items:center;gap:12px}
.slider-wrapper label{font-size:13px;color:#8b949e;white-space:nowrap}
.slider-wrapper input[type=range]{flex:1;height:6px;-webkit-appearance:none;background:#30363d;border-radius:3px;outline:none}
.slider-wrapper input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:#58a6ff;cursor:pointer;border:2px solid #0d1117}
.time-label{font-size:13px;color:#8b949e;min-width:100px;text-align:right;font-variant-numeric:tabular-nums}
.timeline-svg{background:#161b22;border:1px solid #30363d;border-radius:8px;width:100%;overflow:hidden}
.timeline-svg svg{display:block}
.track-label{font-size:12px;fill:#8b949e;cursor:pointer}
.track-label:hover{fill:#f0f6fc}
.node{cursor:pointer;transition:opacity .15s}
.node:hover{opacity:.8}
.node-label{font-size:10px;fill:#e6edf3;text-anchor:middle;pointer-events:none;dominant-baseline:central}
.node-stale{opacity:.4}
.legend{display:flex;gap:24px;margin:16px 0;font-size:13px;flex-wrap:wrap}
.legend-item{display:flex;align-items:center;gap:6px}
.legend-dot{width:12px;height:12px;border-radius:50%;display:inline-block}
.legend-dot.gold{background:#d29922}
.legend-dot.amber{background:#db6d28}
.legend-dot.cool{background:#58a6ff}
.track-count{font-size:12px;fill:#484f58}
/* popup */
.popup-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.6);z-index:100}
.popup-overlay.show{display:block}
.popup{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#161b22;border:1px solid #30363d;border-radius:12px;padding:28px;z-index:101;min-width:340px;max-width:500px;box-shadow:0 8px 32px rgba(0,0,0,.5)}
.popup h3{font-size:18px;color:#f0f6fc;margin-bottom:16px}
.popup-close{position:absolute;top:12px;right:16px;background:none;border:none;color:#8b949e;font-size:20px;cursor:pointer;padding:4px 8px}
.popup-close:hover{color:#f0f6fc}
.detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px 16px;font-size:14px}
.detail-grid .label{color:#8b949e}
.detail-grid .value{color:#e6edf3;font-variant-numeric:tabular-nums}
.detail-grid .value.score-85{color:#d29922;font-weight:600}
.detail-grid .value.score-70{color:#db6d28}
.detail-grid .value.score-0{color:#58a6ff}
.badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:600}
.badge.eval{background:#1f6feb20;color:#58a6ff;border:1px solid #1f6feb40}
.badge.improve{background:#d2992220;color:#d29922;border:1px solid #d2992240}
.badge.promote{background:#3fb95020;color:#3fb950;border:1px solid #3fb95040}
.badge.archive{background:#da363320;color:#da3633;border:1px solid #da363340}
</style>
</head>
<body>
<div class="timeline-container">
<div class="header">
<h1>Agent Lifecycle Timeline <span>spawn → eval → improve → promote</span></h1>
</div>
<div class="controls">
<button id="playBtn">▶ Play</button>
<button id="resetBtn">⟲ Reset</button>
<div class="slider-wrapper">
<label for="timeSlider">Time</label>
<input type="range" id="timeSlider" min="0" max="100" value="100" step="1">
<span class="time-label" id="timeLabel">Live</span>
</div>
</div>
<div class="legend">
<div class="legend-item"><span class="legend-dot gold"></span> 85+ (Production)</div>
<div class="legend-item"><span class="legend-dot amber"></span> 70–84 (Refinery)</div>
<div class="legend-item"><span class="legend-dot cool"></span> &lt; 70 (Archive)</div>
</div>
<div class="timeline-svg" id="svgContainer"></div>
<div id="bpCount" style="text-align:right;font-size:12px;color:#484f58;margin-top:6px"></div>
</div>
<div class="popup-overlay" id="popupOverlay"></div>
<div class="popup" id="popup">
<button class="popup-close" id="popupClose">&times;</button>
<h3 id="popupTitle">Agent Run</h3>
<div class="detail-grid" id="popupDetails"></div>
</div>
<script>
// ── sample state.yaml data ──────────────────────────────────────────
// In production, this block is replaced by fetching state.yaml from the forge root.
// Structure mirrors forge's state.yaml: blueprints → agents → runs with timestamps.
const STATE = {
  blueprints: [
    // Each blueprint has a name and an array of agents.
    // Each agent has runs (timeline nodes) with timestamps, scores, stages.
    {
      name: "fullstack-feature-builder",
      agents: [
        { run_id: "FSB-001", version: 4, stage: "promote", score: 92, benchmark: "eval-v3", ts: "2026-06-28T08:00:00Z" },
        { run_id: "FSB-002", version: 5, stage: "eval", score: 78, benchmark: "eval-v3", ts: "2026-06-28T14:30:00Z" },
        { run_id: "FSB-003", version: 5, stage: "improve", score: 85, benchmark: "eval-v3", ts: "2026-06-29T02:00:00Z" },
        { run_id: "FSB-004", version: 6, stage: "promote", score: 91, benchmark: "eval-v4", ts: "2026-06-29T18:00:00Z" }
      ]
    },
    {
      name: "data-pipeline-optimizer",
      agents: [
        { run_id: "DPO-001", version: 1, stage: "eval", score: 45, benchmark: "eval-v2", ts: "2026-06-27T10:00:00Z" },
        { run_id: "DPO-002", version: 2, stage: "eval", score: 62, benchmark: "eval-v2", ts: "2026-06-27T22:00:00Z" },
        { run_id: "DPO-003", version: 3, stage: "improve", score: 71, benchmark: "eval-v3", ts: "2026-06-28T06:00:00Z" },
        { run_id: "DPO-004", version: 3, stage: "eval", score: 68, benchmark: "eval-v3", ts: "2026-06-28T16:00:00Z" },
        { run_id: "DPO-005", version: 4, stage: "archive", score: 55, benchmark: "eval-v3", ts: "2026-06-29T04:00:00Z" }
      ]
    },
    {
      name: "sql-schema-designer",
      agents: [
        { run_id: "SSD-001", version: 1, stage: "eval", score: 88, benchmark: "eval-v1", ts: "2026-06-26T12:00:00Z" },
        { run_id: "SSD-002", version: 2, stage: "promote", score: 94, benchmark: "eval-v2", ts: "2026-06-27T08:00:00Z" },
        { run_id: "SSD-003", version: 3, stage: "eval", score: 81, benchmark: "eval-v3", ts: "2026-06-28T12:00:00Z" }
      ]
    },
    {
      name: "api-contract-tester",
      agents: [
        { run_id: "ACT-001", version: 1, stage: "eval", score: 30, benchmark: "eval-v1", ts: "2026-06-25T06:00:00Z" },
        { run_id: "ACT-002", version: 2, stage: "eval", score: 52, benchmark: "eval-v2", ts: "2026-06-25T20:00:00Z" },
        { run_id: "ACT-003", version: 3, stage: "improve", score: 66, benchmark: "eval-v2", ts: "2026-06-26T10:00:00Z" },
        { run_id: "ACT-004", version: 4, stage: "eval", score: 74, benchmark: "eval-v3", ts: "2026-06-27T14:00:00Z" },
        { run_id: "ACT-005", version: 5, stage: "promote", score: 87, benchmark: "eval-v3", ts: "2026-06-28T20:00:00Z" },
        { run_id: "ACT-006", version: 6, stage: "eval", score: 83, benchmark: "eval-v4", ts: "2026-06-29T10:00:00Z" }
      ]
    },
    {
      name: "react-component-gen",
      agents: [
        { run_id: "RCG-001", version: 1, stage: "eval", score: 72, benchmark: "eval-v2", ts: "2026-06-27T02:00:00Z" },
        { run_id: "RCG-002", version: 2, stage: "promote", score: 90, benchmark: "eval-v3", ts: "2026-06-28T04:00:00Z" }
      ]
    },
    {
      name: "docs-automator",
      agents: [
        { run_id: "DA-001", version: 1, stage: "eval", score: 35, benchmark: "eval-v1", ts: "2026-06-24T08:00:00Z" },
        { run_id: "DA-002", version: 2, stage: "eval", score: 48, benchmark: "eval-v2", ts: "2026-06-25T16:00:00Z" },
        { run_id: "DA-003", version: 3, stage: "archive", score: 42, benchmark: "eval-v2", ts: "2026-06-26T22:00:00Z" }
      ]
    },
    {
      name: "test-coverage-analyzer",
      agents: [
        { run_id: "TCA-001", version: 1, stage: "eval", score: 60, benchmark: "eval-v2", ts: "2026-06-26T18:00:00Z" },
        { run_id: "TCA-002", version: 2, stage: "improve", score: 76, benchmark: "eval-v3", ts: "2026-06-27T12:00:00Z" },
        { run_id: "TCA-003", version: 3, stage: "promote", score: 89, benchmark: "eval-v3", ts: "2026-06-28T10:00:00Z" },
        { run_id: "TCA-004", version: 4, stage: "eval", score: 84, benchmark: "eval-v4", ts: "2026-06-29T06:00:00Z" }
      ]
    },
    {
      name: "log-parser-agent",
      agents: [
        { run_id: "LPA-001", version: 1, stage: "eval", score: 25, benchmark: "eval-v1", ts: "2026-06-23T14:00:00Z" },
        { run_id: "LPA-002", version: 2, stage: "archive", score: 38, benchmark: "eval-v2", ts: "2026-06-24T20:00:00Z" }
      ]
    }
  ]
};
// ── Timeline Engine ─────────────────────────────────────────────────
const MARGIN = { top: 24, right: 40, bottom: 16, left: 200 };
const NODE_R = 7;
const TRACK_H = 36;
const MIN_NODE_SPACING = 20;
function parseTime(ts) { return new Date(ts).getTime(); }
function flattenRuns(bps) {
  const runs = [];
  bps.forEach((bp, bi) => {
    bp.agents.forEach((a) => {
      runs.push({ ...a, bpIdx: bi, bpName: bp.name });
    });
  });
  runs.sort((a, b) => parseTime(a.ts) - parseTime(b.ts));
  return runs;
}
function colorForScore(s) {
  if (s >= 85) return { fill: '#d29922', stroke: '#bb8009' };
  if (s >= 70) return { fill: '#db6d28', stroke: '#c05e1a' };
  return { fill: '#58a6ff', stroke: '#388bfd' };
}
function stageBadge(s) {
  const m = { eval: 'eval', improve: 'improve', promote: 'promote', archive: 'archive' };
  return m[s] || 'eval';
}
function renderTimeline(containerId, state, maxTime) {
  const container = document.getElementById(containerId);
  const bps = state.blueprints;
  const allRuns = flattenRuns(bps);
  if (allRuns.length === 0) { container.innerHTML = '<div style="padding:40px;text-align:center;color:#8b949e">No agent runs found.</div>'; return; }
  const tMin = parseTime(allRuns[0].ts);
  const tMax = allRuns.reduce((m, r) => Math.max(m, parseTime(r.ts)), tMin);
  const range = tMax - tMin || 1;
  const clampTime = maxTime !== undefined ? maxTime : tMax;
  const trackIds = [...new Set(bps.map((b, i) => i))];
  // calculate dynamic width
  const runsVisible = allRuns.filter(r => parseTime(r.ts) <= clampTime);
  const countPerBp = {};
  bps.forEach((bp, i) => { countPerBp[i] = 0; });
  runsVisible.forEach(r => { countPerBp[r.bpIdx]++; });
  const maxNodes = Math.max(...Object.values(countPerBp), 1);
  const minWidth = Math.max(800, maxNodes * (NODE_R * 2 + MIN_NODE_SPACING) + MARGIN.left + MARGIN.right + 40);
  const W = minWidth;
  const H = bps.length * TRACK_H + MARGIN.top + MARGIN.bottom;
  const xScale = (t) => MARGIN.left + ((t - tMin) / range) * (W - MARGIN.left - MARGIN.right);
  let svg = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">`;
  // defs for glow filter
  svg += `<defs><filter id="glow"><feGaussianBlur stdDeviation="1.5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>`;
  // background grid lines
  const nGrid = 8;
  for (let i = 0; i <= nGrid; i++) {
    const x = MARGIN.left + (i / nGrid) * (W - MARGIN.left - MARGIN.right);
    const t = tMin + (i / nGrid) * range;
    const d = new Date(t);
    const label = d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit' });
    svg += `<line x1="${x}" y1="${MARGIN.top}" x2="${x}" y2="${H - MARGIN.bottom}" stroke="#21262d" stroke-width="1"/>`;
    svg += `<text x="${x}" y="${MARGIN.top - 6}" text-anchor="middle" fill="#484f58" font-size="10">${label}</text>`;
  }
  // tracks
  bps.forEach((bp, bi) => {
    const y = MARGIN.top + bi * TRACK_H + TRACK_H / 2;
    // track bg
    svg += `<rect x="${MARGIN.left}" y="${MARGIN.top + bi * TRACK_H}" width="${W - MARGIN.left - MARGIN.right}" height="${TRACK_H}" fill="${bi % 2 === 0 ? 'rgba(255,255,255,0.02)' : 'transparent'}" rx="4"/>`;
    // track label
    const label = bp.name.length > 28 ? bp.name.slice(0, 25) + '...' : bp.name;
    svg += `<text class="track-label" x="${MARGIN.left - 8}" y="${y}" text-anchor="end" dominant-baseline="central">${label}</text>`;
    // count badge
    const cnt = countPerBp[bi] || 0;
    svg += `<text class="track-count" x="${MARGIN.left + 4}" y="${y - 8}" text-anchor="start" dominant-baseline="central">${cnt}</text>`;
    // agent nodes
    const agentRuns = bp.agents.filter(a => parseTime(a.ts) <= clampTime);
    agentRuns.forEach((a) => {
      const cx = xScale(parseTime(a.ts));
      const colors = colorForScore(a.score);
      const isStale = a.stage === 'archive';
      const cls = `node${isStale ? ' node-stale' : ''}`;
      svg += `<circle class="${cls}" cx="${cx}" cy="${y}" r="${NODE_R}" fill="${colors.fill}" stroke="${colors.stroke}" stroke-width="1.5" data-run_id="${a.run_id}" data-version="${a.version}" data-stage="${a.stage}" data-score="${a.score}" data-benchmark="${a.benchmark}" data-ts="${a.ts}" data-bp="${bp.name}" filter="${a.score >= 85 ? 'url(#glow)' : ''}"/>`;
      // score label for non-archive nodes
      if (!isStale && a.score >= 70) {
        svg += `<text class="node-label" x="${cx}" y="${y + 14}" fill="${colors.fill}" font-size="9">${a.score}</text>`;
      }
    });
  });
  // time cursor line (scrubber position)
  if (clampTime && clampTime < tMax) {
    const cx = xScale(clampTime);
    svg += `<line class="cursor-line" x1="${cx}" y1="${MARGIN.top}" x2="${cx}" y2="${H - MARGIN.bottom}" stroke="#58a6ff" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.6"/>`;
  }
  svg += '</svg>';
  container.innerHTML = svg;
  // attach click handlers to nodes
  container.querySelectorAll('.node').forEach(el => {
    el.addEventListener('click', () => {
      showPopup({
        run_id: el.dataset.run_id,
        version: el.dataset.version,
        stage: el.dataset.stage,
        score: parseInt(el.dataset.score),
        benchmark: el.dataset.benchmark,
        ts: el.dataset.ts,
        bp: el.dataset.bp
      });
    });
  });
  // update bp count
  document.getElementById('bpCount').textContent = `${bps.length} blueprints · ${runsVisible.length} agent runs visible`;
}
// ── Popup ────────────────────────────────────────────────────────────
function showPopup(d) {
  document.getElementById('popupTitle').textContent = `${d.bp} · ${d.run_id}`;
  const sc = d.score;
  const scoreCls = sc >= 85 ? 'score-85' : sc >= 70 ? 'score-70' : 'score-0';
  document.getElementById('popupDetails').innerHTML = `
    <span class="label">Run ID</span><span class="value">${d.run_id}</span>
    <span class="label">Blueprint</span><span class="value">${d.bp}</span>
    <span class="label">Version</span><span class="value">v${d.version}</span>
    <span class="label">Stage</span><span class="value"><span class="badge ${stageBadge(d.stage)}">${d.stage}</span></span>
    <span class="label">Score</span><span class="value ${scoreCls}">${d.score}/100</span>
    <span class="label">Benchmark</span><span class="value">${d.benchmark}</span>
    <span class="label">Timestamp</span><span class="value">${new Date(d.ts).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</span>
  `;
  document.getElementById('popupOverlay').classList.add('show');
}
document.getElementById('popupOverlay').addEventListener('click', () => {
  document.getElementById('popupOverlay').classList.remove('show');
});
document.getElementById('popupClose').addEventListener('click', () => {
  document.getElementById('popupOverlay').classList.remove('show');
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') document.getElementById('popupOverlay').classList.remove('show');
});
// ── Slider & Playback ───────────────────────────────────────────────
const slider = document.getElementById('timeSlider');
const timeLabel = document.getElementById('timeLabel');
const playBtn = document.getElementById('playBtn');
let playing = false;
let playInterval = null;
function updateTime(cb) {
  const bps = STATE.blueprints;
  const allRuns = flattenRuns(bps);
  if (allRuns.length === 0) return;
  const tMin = parseTime(allRuns[0].ts);
  const tMax = allRuns.reduce((m, r) => Math.max(m, parseTime(r.ts)), tMin);
  const range = tMax - tMin || 1;
  const pct = parseInt(slider.value) / 100;
  let currentTime;
  if (slider.value >= 100) {
    currentTime = undefined;
    timeLabel.textContent = 'Live';
  } else {
    currentTime = tMin + pct * range;
    const d = new Date(currentTime);
    timeLabel.textContent = d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  }
  renderTimeline('svgContainer', STATE, currentTime);
  if (cb) cb();
}
slider.addEventListener('input', () => { updateTime(); });
playBtn.addEventListener('click', () => {
  if (playing) {
    playing = false;
    playBtn.textContent = '▶ Play';
    if (playInterval) clearInterval(playInterval);
  } else {
    if (parseInt(slider.value) >= 100) slider.value = 0;
    playing = true;
    playBtn.textContent = '⏸ Pause';
    playInterval = setInterval(() => {
      const val = parseInt(slider.value);
      if (val >= 100) {
        playing = false;
        playBtn.textContent = '▶ Play';
        clearInterval(playInterval);
        updateTime();
      } else {
        slider.value = val + 1;
        updateTime();
      }
    }, 150);
  }
});
document.getElementById('resetBtn').addEventListener('click', () => {
  if (playing) {
    playing = false;
    playBtn.textContent = '▶ Play';
    if (playInterval) clearInterval(playInterval);
  }
  slider.value = 100;
  updateTime();
});
// ── Init ─────────────────────────────────────────────────────────────
updateTime();
</script>
</body>
</html>
```