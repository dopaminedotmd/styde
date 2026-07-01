```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-yaml/4.1.0/js-yaml.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0d1117; color: #e6edf3; overflow: hidden; }
#app { display: flex; flex-direction: column; height: 100vh; }
header { padding: 16px 24px; background: #161b22; border-bottom: 1px solid #30363d; display: flex; align-items: center; gap: 16px; }
header h1 { font-size: 18px; font-weight: 600; color: #f0f6fc; }
header .subtitle { font-size: 13px; color: #8b949e; margin-left: auto; }
#controls { display: flex; align-items: center; gap: 12px; padding: 8px 24px; background: #161b22; border-bottom: 1px solid #30363d; flex-shrink: 0; }
#controls button { background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 500; }
#controls button:hover { background: #30363d; }
#controls button.active { background: #1f6feb; border-color: #1f6feb; color: #fff; }
#scrub-container { flex: 1; display: flex; align-items: center; gap: 10px; }
#scrub-container label { font-size: 12px; color: #8b949e; white-space: nowrap; }
#scrubber { flex: 1; accent-color: #58a6ff; height: 6px; cursor: pointer; }
#time-display { font-size: 12px; color: #8b949e; font-family: monospace; min-width: 160px; text-align: center; }
.legend { display: flex; gap: 16px; margin-left: auto; align-items: center; }
.legend-item { display: flex; align-items: center; gap: 5px; font-size: 11px; color: #8b949e; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; }
#canvas-wrap { flex: 1; overflow: auto; position: relative; }
svg { width: 100%; min-height: 100%; display: block; }
.track-label { font-size: 12px; fill: #8b949e; cursor: pointer; }
.track-label:hover { fill: #f0f6fc; }
.node { cursor: pointer; transition: r 0.15s ease; }
.node:hover { stroke: #fff; stroke-width: 2.5; }
.node.gold { fill: #ffd700; }
.node.amber { fill: #d29922; }
.node.cool { fill: #58a6ff; }
.node.gray { fill: #484f58; }
.node.running { fill: #3fb950; opacity: 0.7; }
.node.spawn { fill: #8b949e; }
.node.improve { fill: #a371f7; }
#tooltip { display: none; position: fixed; background: #1c2128; border: 1px solid #30363d; border-radius: 8px; padding: 14px 18px; font-size: 13px; line-height: 1.5; max-width: 360px; box-shadow: 0 8px 24px rgba(0,0,0,0.4); z-index: 1000; pointer-events: none; }
#tooltip h3 { font-size: 14px; font-weight: 600; margin-bottom: 6px; color: #f0f6fc; }
#tooltip .row { display: flex; justify-content: space-between; gap: 20px; padding: 2px 0; }
#tooltip .label { color: #8b949e; }
#tooltip .value { font-weight: 500; color: #e6edf3; }
#tooltip .score-high { color: #ffd700; }
#tooltip .score-mid { color: #d29922; }
#tooltip .score-low { color: #58a6ff; }
#loading { display: flex; align-items: center; justify-content: center; height: 100vh; flex-direction: column; gap: 16px; }
#loading .spinner { width: 40px; height: 40px; border: 3px solid #30363d; border-top-color: #58a6ff; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
#loading p { color: #8b949e; font-size: 14px; }
#error { display: none; align-items: center; justify-content: center; height: 100vh; flex-direction: column; gap: 12px; color: #f85149; }
#error p { font-size: 14px; }
</style>
</head>
<body>
<div id="loading"><div class="spinner"></div><p>Loading state.yaml...</p></div>
<div id="error"><h2>Failed to load state.yaml</h2><p id="error-msg"></p></div>
<div id="app" style="display:none">
  <header>
    <h1>Agent Lifecycle Timeline</h1>
    <span class="subtitle"><span id="bp-count">0</span> blueprints | <span id="entry-count">0</span> events</span>
  </header>
  <div id="controls">
    <button id="play-btn" title="Play/pause auto-scrub">Play</button>
    <div id="scrub-container">
      <label>Time:</label>
      <input type="range" id="scrubber" min="0" max="100" value="100">
      <span id="time-display">all events</span>
    </div>
    <div class="legend">
      <span class="legend-item"><span class="legend-dot" style="background:#ffd700"></span>85+</span>
      <span class="legend-item"><span class="legend-dot" style="background:#d29922"></span>70-84</span>
      <span class="legend-item"><span class="legend-dot" style="background:#58a6ff"></span>&lt;70</span>
      <span class="legend-item"><span class="legend-dot" style="background:#a371f7"></span>improve</span>
      <span class="legend-item"><span class="legend-dot" style="background:#3fb950"></span>running</span>
    </div>
  </div>
  <div id="canvas-wrap">
    <svg id="timeline-svg" viewBox="0 0 1200 600"></svg>
  </div>
</div>
<div id="tooltip"></div>
<script>
(async function() {
  let data, entries, blueprints;
  let playing = false;
  let playInterval = null;
  try {
    const resp = await fetch('state.yaml');
    if (!resp.ok) throw new Error('HTTP ' + resp.status);
    const yamlText = await resp.text();
    const parsed = jsyaml.load(yamlText);
    entries = (parsed && parsed.activity) || [];
  } catch(e) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('error').style.display = 'flex';
    document.getElementById('error-msg').textContent = e.message || String(e);
    return;
  }
  // Parse each entry
  function parseDetail(detail) {
    const result = { s: null, j: null, c: null, text: detail };
    if (!detail) return result;
    const sMatch = detail.match(/S:(\d+(?:\.\d+)?)/);
    const jMatch = detail.match(/J:(\d+(?:\.\d+)?)/);
    const cMatch = detail.match(/C:(\d+(?:\.\d+)?)/);
    if (sMatch) result.s = parseFloat(sMatch[1]);
    if (jMatch) result.j = parseFloat(jMatch[1]);
    if (cMatch) result.c = parseFloat(cMatch[1]);
    return result;
  }
  entries = entries.filter(e => e && e.blueprint && e.timestamp).map(e => ({
    ...e,
    parsed: parseDetail(e.detail),
    time: new Date(e.timestamp)
  }));
  // Group by blueprint
  const bpMap = new Map();
  for (const e of entries) {
    if (!bpMap.has(e.blueprint)) bpMap.set(e.blueprint, []);
    bpMap.get(e.blueprint).push(e);
  }
  blueprints = Array.from(bpMap.entries())
    .map(([name, evts]) => ({
      name,
      entries: evts.sort((a,b) => a.time - b.time)
    }))
    .sort((a,b) => b.entries.length - a.entries.length);
  document.getElementById('bp-count').textContent = blueprints.length;
  document.getElementById('entry-count').textContent = entries.length;
  // Time range
  const allTimes = entries.map(e => e.time).filter(t => !isNaN(t.getTime()));
  if (allTimes.length === 0) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('error').style.display = 'flex';
    document.getElementById('error-msg').textContent = 'No valid timestamps found';
    return;
  }
  const tMin = new Date(Math.min(...allTimes));
  const tMax = new Date(Math.max(...allTimes));
  const tRange = tMax - tMin;
  function formatTime(t) {
    const d = new Date(t);
    return d.toISOString().replace('T',' ').slice(0,16);
  }
  function formatTimeShort(t) {
    const d = new Date(t);
    const month = String(d.getUTCMonth()+1).padStart(2,'0');
    const day = String(d.getUTCDate()).padStart(2,'0');
    const h = String(d.getUTCHours()).padStart(2,'0');
    const m = String(d.getUTCMinutes()).padStart(2,'0');
    return `${month}/${day} ${h}:${m}`;
  }
  // Layout constants
  const MARGIN = { top: 30, bottom: 40, left: 220, right: 40 };
  const TRACK_H = 30;
  const TRACK_PAD = 8;
  const NODE_MIN_R = 6;
  const NODE_MAX_R = 14;
  function getNodeRadius(e, allBpEntries) {
    // Bigger for eval with score, smaller for spawn/improve
    if (e.action === 'eval' && e.parsed.c !== null) {
      const c = e.parsed.c;
      return NODE_MIN_R + (c / 100) * (NODE_MAX_R - NODE_MIN_R);
    }
    return 7;
  }
  function getNodeClass(e) {
    if (e.status === 'running') return 'running';
    if (e.action === 'improve') return 'improve';
    if (e.action === 'spawn') return 'spawn';
    if (e.parsed.c !== null) {
      if (e.parsed.c >= 85) return 'gold';
      if (e.parsed.c >= 70) return 'amber';
      return 'cool';
    }
    return 'gray';
  }
  function getNodeTooltip(e) {
    let html = `<h3>${e.blueprint}</h3>`;
    html += `<div class="row"><span class="label">Action</span><span class="value">${e.action}</span></div>`;
    html += `<div class="row"><span class="label">ID</span><span class="value">${e.id}</span></div>`;
    html += `<div class="row"><span class="label">Time</span><span class="value">${formatTime(e.time)}</span></div>`;
    html += `<div class="row"><span class="label">Status</span><span class="value">${e.status}</span></div>`;
    html += `<div class="row"><span class="label">Progress</span><span class="value">${e.progress}%</span></div>`;
    if (e.parsed.c !== null) {
      const cls = e.parsed.c >= 85 ? 'score-high' : e.parsed.c >= 70 ? 'score-mid' : 'score-low';
      html += `<div class="row"><span class="label">Composite</span><span class="value ${cls}">${e.parsed.c.toFixed(1)}</span></div>`;
    }
    if (e.parsed.s !== null) {
      html += `<div class="row"><span class="label">S Score</span><span class="value">${e.parsed.s.toFixed(1)}</span></div>`;
    }
    if (e.parsed.j !== null) {
      html += `<div class="row"><span class="label">J Score</span><span class="value">${e.parsed.j.toFixed(1)}</span></div>`;
    }
    if (e.detail && !e.detail.startsWith('S:') && !e.detail.startsWith('iter')) {
      const short = e.detail.length > 50 ? e.detail.slice(0,50)+'...' : e.detail;
      html += `<div class="row"><span class="label">Detail</span><span class="value">${short}</span></div>`;
    }
    return html;
  }
  function render(scrubValue) {
    const svg = document.getElementById('timeline-svg');
    const W = 1200, H = Math.max(600, MARGIN.top + MARGIN.bottom + blueprints.length * (TRACK_H + TRACK_PAD));
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    // Time window based on scrubber (0-100, where 100 = all events)
    const cutoff = tMin.getTime() + (scrubValue / 100) * tRange;
    const showAll = scrubValue >= 99.9;
    // Filter visible entries
    let visibleEntries = [];
    const visibleByBp = new Map();
    for (const bp of blueprints) {
      const vis = bp.entries.filter(e => showAll || e.time.getTime() <= cutoff);
      if (vis.length > 0) {
        visibleByBp.set(bp.name, vis);
        visibleEntries = visibleEntries.concat(vis);
      }
    }
    // Update time display
    document.getElementById('time-display').textContent =
      showAll ? 'all events' : `until ${formatTimeShort(cutoff)}` + ` (${visibleEntries.length}/${entries.length})`;
    // Build visible blueprint list (preserving order)
    const visibleBpList = blueprints.filter(bp => visibleByBp.has(bp.name));
    // Y positions
    const yPositions = new Map();
    visibleBpList.forEach((bp, i) => {
      yPositions.set(bp.name, MARGIN.top + i * (TRACK_H + TRACK_PAD) + TRACK_H/2);
    });
    const plotW = W - MARGIN.left - MARGIN.right;
    const plotH = H - MARGIN.top - MARGIN.bottom;
    // Time to X
    function timeToX(t) {
      const p = (t.getTime() - tMin.getTime()) / tRange;
      return MARGIN.left + p * plotW;
    }
    let html = '';
    // Background grid
    html += `<rect x="${MARGIN.left}" y="${MARGIN.top}" width="${plotW}" height="${plotH}" fill="none" stroke="#21262d" stroke-width="1"/>`;
    // Hour gridlines
    const hourMs = 3600000;
    const startHour = new Date(Math.floor(tMin.getTime() / hourMs) * hourMs);
    const endHour = new Date(Math.ceil(tMax.getTime() / hourMs) * hourMs);
    let gridX = startHour.getTime();
    const gridLines = [];
    while (gridX <= endHour.getTime()) {
      const gx = timeToX(new Date(gridX));
      if (gx >= MARGIN.left && gx <= MARGIN.left + plotW) {
        gridLines.push({ x: gx, time: new Date(gridX) });
      }
      gridX += hourMs;
    }
    for (const gl of gridLines) {
      html += `<line x1="${gl.x}" y1="${MARGIN.top}" x2="${gl.x}" y2="${MARGIN.top+plotH}" stroke="#21262d" stroke-width="1"/>`;
      html += `<text x="${gl.x}" y="${H - 15}" text-anchor="middle" fill="#484f58" font-size="10">${formatTimeShort(gl.time)}</text>`;
    }
    // Scrub indicator line
    if (!showAll) {
      const sx = timeToX(new Date(cutoff));
      html += `<line x1="${sx}" y1="${MARGIN.top}" x2="${sx}" y2="${MARGIN.top+plotH}" stroke="#f85149" stroke-width="2" stroke-dasharray="4,3"/>`;
    }
    // Rows (alternating backgrounds)
    visibleBpList.forEach((bp, i) => {
      const y = yPositions.get(bp.name);
      const rowY = y - TRACK_H/2;
      if (i % 2 === 0) {
        html += `<rect x="${MARGIN.left}" y="${rowY}" width="${plotW}" height="${TRACK_H}" fill="#161b22" opacity="0.4"/>`;
      }
      // Track line
      html += `<line x1="${MARGIN.left}" y1="${y}" x2="${MARGIN.left+plotW}" y2="${y}" stroke="#30363d" stroke-width="1"/>`;
      // Blueprint label
      const label = bp.name.replace(/-/g, ' ');
      const labelY = y + 4;
      html += `<text x="${MARGIN.left - 12}" y="${labelY}" text-anchor="end" class="track-label" font-size="11" font-weight="500">${label}</text>`;
    });
    // Nodes
    const nodes = [];
    for (const bp of visibleBpList) {
      const y = yPositions.get(bp.name);
      const bpEntries = visibleByBp.get(bp.name);
      for (const e of bpEntries) {
        const x = timeToX(e.time);
        const r = getNodeRadius(e, bpEntries);
        const cls = getNodeClass(e);
        const idx = nodes.length;
        const aid = `node-${idx}`;
        html += `<circle id="${aid}" class="node ${cls}" cx="${x}" cy="${y}" r="${r}" data-idx="${idx}"/>`;
        nodes.push(e);
      }
    }
    // Node labels for eval with score
    for (const bp of visibleBpList) {
      const y = yPositions.get(bp.name);
      const bpEntries = visibleByBp.get(bp.name);
      for (const e of bpEntries) {
        if (e.action === 'eval' && e.parsed.c !== null && e.parsed.c >= 85) {
          const x = timeToX(e.time);
          html += `<text x="${x}" y="${y - 14}" text-anchor="middle" fill="#ffd700" font-size="9" font-weight="600">${e.parsed.c.toFixed(1)}</text>`;
        }
      }
    }
    svg.innerHTML = html;
    // Attach tooltip events
    for (let i = 0; i < nodes.length; i++) {
      const el = document.getElementById(`node-${i}`);
      if (!el) continue;
      const e = nodes[i];
      el.addEventListener('mouseenter', function(ev) {
        const tip = document.getElementById('tooltip');
        tip.innerHTML = getNodeTooltip(e);
        tip.style.display = 'block';
        positionTooltip(ev);
      });
      el.addEventListener('mousemove', function(ev) {
        positionTooltip(ev);
      });
      el.addEventListener('mouseleave', function() {
        document.getElementById('tooltip').style.display = 'none';
      });
    }
  }
  function positionTooltip(ev) {
    const tip = document.getElementById('tooltip');
    let x = ev.clientX + 14;
    let y = ev.clientY - 10;
    const rect = tip.getBoundingClientRect();
    if (x + rect.width > window.innerWidth - 10) x = ev.clientX - rect.width - 14;
    if (y + rect.height > window.innerHeight - 10) y = ev.clientY - rect.height - 10;
    if (y < 10) y = 10;
    tip.style.left = x + 'px';
    tip.style.top = y + 'px';
  }
  // Initial full render
  render(100);
  // Scrubber
  const scrubber = document.getElementById('scrubber');
  scrubber.addEventListener('input', function() {
    if (playing) { togglePlay(); }
    render(parseFloat(this.value));
  });
  // Play/Pause
  function togglePlay() {
    playing = !playing;
    document.getElementById('play-btn').textContent = playing ? 'Pause' : 'Play';
    document.getElementById('play-btn').classList.toggle('active', playing);
    if (playing) {
      const step = 0.5;
      playInterval = setInterval(() => {
        let val = parseFloat(scrubber.value) + step;
        if (val > 100) {
          val = 0;
        }
        scrubber.value = val;
        render(val);
      }, 100);
    } else {
      clearInterval(playInterval);
      playInterval = null;
    }
  }
  document.getElementById('play-btn').addEventListener('click', togglePlay);
  // Show the app
  document.getElementById('loading').style.display = 'none';
  document.getElementById('app').style.display = 'flex';
  // Handle resize - re-render on scrub
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => render(parseFloat(scrubber.value)), 200);
  });
})();
</script>
</body>
</html>
```
This is a self-contained HTML file. Save it as `timeline.html` in `E:\Stryde\_alpedal\styde-forge\` alongside `state.yaml`, then open it in a browser.
How it works:
- Fetches `state.yaml` from the same directory, parses with js-yaml CDN
- 21 blueprints as horizontal tracks, 200 events laid out by timestamp
- Gold circles = composite score >= 85, amber = 70-84, cool blue = < 70
- Purple circles = improve steps, green = running, gray = spawn
- Labels overlaid on gold nodes showing the exact score
- Scrubber slider at top: drag left to filter events by time window; play button auto-animates from first to last event
- Click any node for a detail popup (score breakdown, ID, timestamp, status, progress)
- Hourly gridlines on the X axis for temporal reference