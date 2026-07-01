<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-yaml/4.1.0/js-yaml.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0d1117;color:#c9d1d9;padding:20px;min-height:100vh}
#app{max-width:1400px;margin:0 auto}
h1{font-size:20px;font-weight:600;margin-bottom:4px;color:#f0f6fc}
.sub{font-size:13px;color:#8b949e;margin-bottom:20px}
.toolbar{display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap}
.btn{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:13px}
.btn:hover{background:#30363d}
.btn:disabled{opacity:0.5;cursor:default}
.btn-primary{background:#238636;border-color:#2ea043;color:#fff}
.btn-primary:hover{background:#2ea043}
#controls{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
#scrubber{flex:1;min-width:200px;accent-color:#d29922}
#timeLabel{font-size:12px;color:#8b949e;min-width:100px;font-variant-numeric:tabular-nums}
#legend{display:flex;gap:16px;font-size:12px;color:#8b949e;margin-bottom:12px}
.legend-item{display:flex;align-items:center;gap:4px}
.legend-dot{width:10px;height:10px;border-radius:50%;display:inline-block}
#svg-container{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;overflow-x:auto;min-height:300px}
#timeline-svg{width:100%;min-width:800px}
.node{cursor:pointer;transition:r 0.15s,stroke-width 0.15s}
.node:hover{r:8;stroke-width:3}
.node-detail{fill:#c9d1d9;font-size:11px}
.track-label{font-size:12px;fill:#8b949e}
.axis-label{font-size:10px;fill:#484f58}
.axis-tick{stroke:#30363d;stroke-width:1}
#detail-popup{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:#161b22;border:1px solid #30363d;border-radius:12px;padding:24px;min-width:340px;max-width:480px;z-index:100;box-shadow:0 16px 48px rgba(0,0,0,0.6)}
#detail-popup.show{display:block}
#overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:99}
#overlay.show{display:block}
#detail-popup h2{font-size:16px;margin-bottom:12px;color:#f0f6fc}
.detail-row{display:flex;justify-content:space-between;padding:4px 0;font-size:13px;border-bottom:1px solid #21262d}
.detail-row:last-child{border-bottom:none}
.detail-label{color:#8b949e}
.detail-value{color:#c9d1d9;font-variant-numeric:tabular-nums}
.close-btn{position:absolute;top:12px;right:12px;background:none;border:none;color:#8b949e;font-size:18px;cursor:pointer;padding:4px 8px}
.close-btn:hover{color:#f0f6fc}
.file-hint{text-align:center;padding:60px 20px;color:#8b949e}
.file-hint svg{margin-bottom:12px;opacity:0.4}
.file-hint p{font-size:14px;margin-top:8px}
.badge{display:inline-block;padding:1px 8px;border-radius:10px;font-size:11px;font-weight:600}
.badge-gold{background:rgba(210,153,34,0.2);color:#d29922;border:1px solid rgba(210,153,34,0.4)}
.badge-amber{background:rgba(203,145,47,0.2);color:#cb912f;border:1px solid rgba(203,145,47,0.4)}
.badge-cool{background:rgba(88,166,255,0.15);color:#58a6ff;border:1px solid rgba(88,166,255,0.3)}
#stats{display:flex;gap:20px;font-size:12px;color:#8b949e;margin-bottom:12px;flex-wrap:wrap}
.stat span{color:#f0f6fc;font-weight:600}
</style>
</head>
<body>
<div id="app">
<h1>Agent Lifecycle Timeline</h1>
<p class="sub">Interactive timeline of agent spawn, eval, improve, and promote cycles</p>
<div id="legend">
<span class="legend-item"><span class="legend-dot" style="background:#d29922"></span> 85+ (Promotable)</span>
<span class="legend-item"><span class="legend-dot" style="background:#cb912f"></span> 70-84</span>
<span class="legend-item"><span class="legend-dot" style="background:#58a6ff"></span> Below 70</span>
</div>
<div class="toolbar">
<div id="stats"></div>
</div>
<div class="toolbar">
<button class="btn" id="loadBtn">Choose state.yaml</button>
<input type="file" id="fileInput" accept=".yaml,.yml" style="display:none">
<div id="controls">
<button class="btn" id="playBtn" disabled>Play</button>
<button class="btn" id="resetBtn" disabled>Reset</button>
<input type="range" id="scrubber" min="0" max="100" value="0" disabled>
<span id="timeLabel">No data loaded</span>
</div>
</div>
<div id="svg-container">
<svg id="timeline-svg" viewBox="0 0 800 300"></svg>
<div class="file-hint" id="emptyHint">
<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
<p>Load a state.yaml file to visualize agent timelines</p>
</div>
</div>
</div>
<div id="overlay"></div>
<div id="detail-popup">
<button class="close-btn" id="closePopup">&times;</button>
<h2 id="popup-title">Agent Run Detail</h2>
<div id="popup-body"></div>
</div>
<script>
const state = {
  data: null,
  blueprints: [],
  allEvents: [],
  currentIndex: 0,
  isPlaying: false,
  playInterval: null,
  timelineSvg: null
};
const COLORS = {
  hot: '#d29922',
  amber: '#cb912f',
  cool: '#58a6ff'
};
function getColor(score) {
  if (score === null || score === undefined || score === 'N/A') return '#484f58';
  const s = Number(score);
  if (s >= 85) return COLORS.hot;
  if (s >= 70) return COLORS.amber;
  return COLORS.cool;
}
function getBadgeClass(score) {
  if (score === null || score === undefined || score === 'N/A') return 'badge-cool';
  const s = Number(score);
  if (s >= 85) return 'badge-gold';
  if (s >= 70) return 'badge-amber';
  return 'badge-cool';
}
document.getElementById('loadBtn').addEventListener('click', () => {
  document.getElementById('fileInput').click();
});
document.getElementById('fileInput').addEventListener('change', function(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(evt) {
    try {
      const parsed = jsyaml.load(evt.target.result);
      loadData(parsed);
    } catch(err) {
      alert('Failed to parse YAML: ' + err.message);
    }
  };
  reader.readAsText(file);
});
function loadData(parsed) {
  state.data = parsed;
  state.blueprints = [];
  state.allEvents = [];
  const agents = parsed.agents || parsed;
  const bpNames = Object.keys(agents);
  state.blueprints = bpNames.sort();
  let tsMin = Infinity, tsMax = -Infinity;
  bpNames.forEach(bp => {
    const runs = agents[bp];
    if (!Array.isArray(runs)) return;
    const events = runs.map((r, idx) => {
      const ts = r.timestamp || r.ts || r.time || (Date.now() - (bpNames.indexOf(bp) * 60000 + idx * 5000));
      const tsNum = Number(ts) || Date.parse(ts) || Date.now();
      const score = r.score !== undefined ? r.score : (r.eval && r.eval.score);
      return {
        blueprint: bp,
        run_id: r.run_id || r.id || `${bp}-run-${idx}`,
        version: r.version || r.v || idx + 1,
        stage: r.stage || r.stage_name || 'eval',
        score: score !== undefined ? Number(score) : 'N/A',
        benchmark: r.benchmark || r.test_name || r.eval?.benchmark || '',
        cycle: r.cycle || r.iteration || idx,
        timestamp: tsNum,
        raw: r
      };
    });
    events.sort((a, b) => a.timestamp - b.timestamp);
    events.forEach((e, i) => { e._index = i; });
    if (events.length > 0) {
      tsMin = Math.min(tsMin, events[0].timestamp);
      tsMax = Math.max(tsMax, events[events.length - 1].timestamp);
    }
    state.allEvents.push(...events);
  });
  if (state.allEvents.length === 0) {
    document.getElementById('emptyHint').style.display = 'block';
    return;
  }
  state.allEvents.sort((a, b) => a.timestamp - b.timestamp);
  if (tsMin === Infinity) { tsMin = Date.now() - 3600000; tsMax = Date.now(); }
  if (tsMin === tsMax) { tsMin -= 60000; tsMax += 60000; }
  state.tsMin = tsMin;
  state.tsMax = tsMax;
  state.tsRange = tsMax - tsMin || 1;
  document.getElementById('emptyHint').style.display = 'none';
  document.getElementById('playBtn').disabled = false;
  document.getElementById('resetBtn').disabled = false;
  document.getElementById('scrubber').disabled = false;
  renderStats();
  renderTimeline();
}
function renderStats() {
  const bpCount = state.blueprints.length;
  const eventCount = state.allEvents.length;
  const goldCount = state.allEvents.filter(e => e.score !== 'N/A' && Number(e.score) >= 85).length;
  const amberCount = state.allEvents.filter(e => e.score !== 'N/A' && Number(e.score) >= 70 && Number(e.score) < 85).length;
  document.getElementById('stats').innerHTML =
    `<span class="stat"><span>${bpCount}</span> blueprints</span>` +
    `<span class="stat"><span>${eventCount}</span> runs</span>` +
    `<span class="stat"><span style="color:#d29922">${goldCount}</span> elite</span>` +
    `<span class="stat"><span style="color:#cb912f">${amberCount}</span> developing</span>`;
}
function renderTimeline() {
  const bpCount = state.blueprints.length;
  const events = state.allEvents;
  if (!events.length) return;
  const margin = { top: 30, right: 60, bottom: 40, left: 160 };
  const width = 800;
  const rowHeight = 38;
  const nodeR = 5;
  const height = Math.max(300, margin.top + margin.bottom + bpCount * rowHeight + 20);
  const svg = document.getElementById('timeline-svg');
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
  const plotW = width - margin.left - margin.right;
  const plotH = height - margin.top - margin.bottom;
  function xPos(ts) {
    return margin.left + ((ts - state.tsMin) / state.tsRange) * plotW;
  }
  function yPos(bpIdx) {
    return margin.top + bpIdx * rowHeight + rowHeight / 2;
  }
  let html = '';
  /* background */
  html += `<rect width="${width}" height="${height}" fill="transparent"/>`;
  /* time axis */
  const tickCount = Math.min(8, Math.max(3, Math.floor(plotW / 100)));
  for (let i = 0; i <= tickCount; i++) {
    const frac = i / tickCount;
    const x = margin.left + frac * plotW;
    const ts = state.tsMin + frac * state.tsRange;
    const label = new Date(ts).toLocaleTimeString();
    html += `<line class="axis-tick" x1="${x}" y1="${margin.top - 8}" x2="${x}" y2="${margin.top + plotH + 4}"/>`;
    html += `<text class="axis-label" x="${x}" y="${margin.top + plotH + 16}" text-anchor="middle">${label}</text>`;
  }
  /* track lines + labels */
  state.blueprints.forEach((bp, idx) => {
    const y = yPos(idx);
    html += `<line x1="${margin.left}" y1="${y}" x2="${margin.left + plotW}" y2="${y}" stroke="#21262d" stroke-width="1"/>`;
    const label = bp.length > 28 ? bp.slice(0, 25) + '...' : bp;
    html += `<text class="track-label" x="${margin.left - 8}" y="${y + 4}" text-anchor="end">${label}</text>`;
  });
  /* current time line */
  const scrubbed = document.getElementById('scrubber').value / 100;
  const currentTs = state.tsMin + scrubbed * state.tsRange;
  const cx = xPos(currentTs);
  html += `<line id="scrubber-line" x1="${cx}" y1="${margin.top - 8}" x2="${cx}" y2="${margin.top + plotH + 4}" stroke="#d29922" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.7"/>`;
  /* event nodes */
  events.forEach(evt => {
    const bpIdx = state.blueprints.indexOf(evt.blueprint);
    if (bpIdx === -1) return;
    const x = xPos(evt.timestamp);
    const y = yPos(bpIdx);
    const color = getColor(evt.score);
    const visible = evt.timestamp <= currentTs;
    const opacity = visible ? 1 : 0.15;
    const stageIcons = { spawn: 'S', eval: 'E', improve: 'I', promote: 'P' };
    const icon = stageIcons[evt.stage.toLowerCase()] || 'R';
    const scoreStr = evt.score === 'N/A' ? '--' : evt.score;
    html += `<g class="node-group" opacity="${opacity}">`;
    html += `<circle class="node" cx="${x}" cy="${y}" r="${nodeR}" fill="${color}" stroke="${color}" stroke-width="1.5" data-run-id="${evt.run_id}" data-blueprint="${evt.blueprint}" data-score="${evt.score}" data-stage="${evt.stage}" data-version="${evt.version}" data-benchmark="${evt.benchmark}" data-timestamp="${evt.timestamp}"/>`;
    html += `<text class="node-detail" x="${x}" y="${y + 3}" text-anchor="middle" fill="#0d1117" font-size="8" font-weight="bold">${icon}</text>`;
    html += `</g>`;
  });
  /* promote markers */
  events.filter(e => e.stage.toLowerCase() === 'promote').forEach(evt => {
    const bpIdx = state.blueprints.indexOf(evt.blueprint);
    if (bpIdx === -1) return;
    const x = xPos(evt.timestamp);
    const y = yPos(bpIdx);
    const visible = evt.timestamp <= currentTs;
    if (!visible) return;
    html += `<polygon points="${x},${y - 12} ${x - 5},${y - 7} ${x + 5},${y - 7}" fill="#238636" opacity="0.8"/>`;
  });
  svg.innerHTML = html;
  /* attach click listeners */
  svg.querySelectorAll('.node').forEach(el => {
    el.addEventListener('click', function() {
      showDetail(this.dataset);
    });
  });
}
function showDetail(data) {
  const ts = Number(data.timestamp);
  const timeStr = new Date(ts).toLocaleString();
  const scoreStr = data.score === 'N/A' ? 'N/A' : data.score;
  const badgeClass = getBadgeClass(data.score);
  const badgeLabel = scoreStr === 'N/A' ? 'Unknown' : (Number(scoreStr) >= 85 ? 'Elite' : Number(scoreStr) >= 70 ? 'Developing' : 'Learning');
  document.getElementById('popup-title').textContent = data.blueprint;
  document.getElementById('popup-body').innerHTML =
    `<div class="detail-row"><span class="detail-label">Run ID</span><span class="detail-value">${data.runId}</span></div>` +
    `<div class="detail-row"><span class="detail-label">Version</span><span class="detail-value">${data.version}</span></div>` +
    `<div class="detail-row"><span class="detail-label">Stage</span><span class="detail-value">${data.stage}</span></div>` +
    `<div class="detail-row"><span class="detail-label">Score</span><span class="detail-value"><span class="badge ${badgeClass}">${scoreStr} — ${badgeLabel}</span></span></div>` +
    `<div class="detail-row"><span class="detail-label">Benchmark</span><span class="detail-value">${data.benchmark || '—'}</span></div>` +
    `<div class="detail-row"><span class="detail-label">Timestamp</span><span class="detail-value">${timeStr}</span></div>`;
  document.getElementById('detail-popup').classList.add('show');
  document.getElementById('overlay').classList.add('show');
}
document.getElementById('closePopup').addEventListener('click', closeDetail);
document.getElementById('overlay').addEventListener('click', closeDetail);
function closeDetail() {
  document.getElementById('detail-popup').classList.remove('show');
  document.getElementById('overlay').classList.remove('show');
}
document.getElementById('scrubber').addEventListener('input', function() {
  if (state.isPlaying) return;
  state.currentIndex = Number(this.value);
  updateTimeLabel();
  renderTimeline();
});
document.getElementById('playBtn').addEventListener('click', function() {
  if (state.isPlaying) {
    stopPlay();
  } else {
    startPlay();
  }
});
document.getElementById('resetBtn').addEventListener('click', function() {
  stopPlay();
  document.getElementById('scrubber').value = 0;
  state.currentIndex = 0;
  updateTimeLabel();
  renderTimeline();
});
function startPlay() {
  state.isPlaying = true;
  document.getElementById('playBtn').textContent = 'Pause';
  state.playInterval = setInterval(() => {
    const scrubber = document.getElementById('scrubber');
    let val = Number(scrubber.value) + 1;
    if (val > 100) {
      stopPlay();
      document.getElementById('playBtn').textContent = 'Replay';
      return;
    }
    scrubber.value = val;
    state.currentIndex = val;
    updateTimeLabel();
    renderTimeline();
  }, 120);
}
function stopPlay() {
  state.isPlaying = false;
  clearInterval(state.playInterval);
  state.playInterval = null;
  document.getElementById('playBtn').textContent = 'Play';
}
function updateTimeLabel() {
  const frac = state.currentIndex / 100;
  const ts = state.tsMin + frac * state.tsRange;
  const label = new Date(ts).toLocaleTimeString();
  const visible = state.allEvents.filter(e => e.timestamp <= ts).length;
  const total = state.allEvents.length;
  document.getElementById('timeLabel').textContent = `${label} — ${visible}/${total} events`;
}
</script>
</body>
</html>