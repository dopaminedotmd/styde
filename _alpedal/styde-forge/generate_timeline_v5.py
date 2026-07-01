#!/usr/bin/env python
"""Generate agent lifecycle timeline HTML v5 - with all teacher feedback applied."""
import yaml, json, sys
from collections import defaultdict
from datetime import datetime

# === STEP 1: DATA-SOURCE VALIDATION (Teacher feedback: live data, no mocks) ===
try:
    with open('state.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
except FileNotFoundError:
    sys.exit('ERROR: state.yaml not found. No mock data fallback - file required.')
except Exception as e:
    sys.exit('ERROR: Failed to read state.yaml: ' + str(e))

agents = data.get('agents', [])
activity = data.get('activity', [])

if not agents:
    sys.exit('ERROR: state.yaml has empty agents list. No mock data fallback.')

# === STEP 2: VERIFICATION CHECKPOINT (Teacher feedback: prove real data flows) ===
total_agents = data.get('total_agents', 0)
all_blueprints = set(a.get('blueprint', 'unknown') for a in agents)
all_stages = defaultdict(int)
for a in agents:
    all_stages[a.get('stage', 'unknown')] += 1

# Extract scores from activity eval events
scores_raw = []
for a in activity:
    if a.get('action') == 'eval' and a.get('progress') == 100:
        detail = a.get('detail', '')
        if 'S:' in detail and 'C:' in detail:
            try:
                c = float(detail.split('C:')[1].split()[0].rstrip(','))
                scores_raw.append(c)
            except Exception:
                pass

# Timestamps for time span
all_ts = []
for a in activity:
    ts = a.get('timestamp', '')
    if ts:
        all_ts.append(ts)
for a in agents:
    ts = a.get('spawned_at', '') or a.get('timestamp', '')
    if ts:
        all_ts.append(ts)
all_ts.sort()

print('=== DATA VERIFICATION CHECKPOINT ===')
print('Agent records loaded: ' + str(len(agents)) + ' (state.yaml total_agents key: ' + str(total_agents) + ')')
print('Unique blueprints:    ' + str(len(all_blueprints)))
print('Activity events:      ' + str(len(activity)))
print('Scored evaluations:   ' + str(len(scores_raw)))
if scores_raw:
    above85 = sum(1 for s in scores_raw if s >= 85)
    print('Score range:          ' + str(min(scores_raw)) + ' - ' + str(max(scores_raw)))
    print('  >= 85 (promote):    ' + str(above85) + ' (' + str(round(100*above85/len(scores_raw), 1)) + '%)')
    print('  70-84:              ' + str(sum(1 for s in scores_raw if 70 <= s < 85)))
    print('  < 70:               ' + str(sum(1 for s in scores_raw if s < 70)))
print('Stage breakdown:      ' + str(dict(all_stages)))
print('  Production:         ' + str(all_stages.get('production', 0)))
print('  Refinery:           ' + str(all_stages.get('refinery', 0)))
print('  Archive:            ' + str(all_stages.get('archive', 0)))
if all_ts:
    print('Time span:            ' + all_ts[0][:10] + ' -> ' + all_ts[-1][:10])
    t1 = datetime.fromisoformat(all_ts[0].replace('Z',''))
    t2 = datetime.fromisoformat(all_ts[-1].replace('Z',''))
    print('Duration:             ' + str((t2-t1).days) + ' days')
print('=== VERIFICATION COMPLETE - proceeding to render ===')

# === STEP 3: BUILD EVENT DATA ===
bp_runs = defaultdict(list)
for a in agents:
    bp = a.get('blueprint', 'unknown')
    bp_runs[bp].append(a)
for bp in bp_runs:
    bp_runs[bp].sort(key=lambda x: x.get('spawned_at', x.get('run_id', '')))

# Extract eval scores per blueprint
bp_scores = defaultdict(list)
for a in activity:
    if a.get('action') == 'eval' and a.get('progress') == 100:
        detail = a.get('detail', '')
        if 'S:' in detail and 'C:' in detail:
            try:
                s = float(detail.split('S:')[1].split()[0].rstrip(','))
                bp_scores[a.get('blueprint', '')].append({
                    'score': s,
                    'ts': a.get('timestamp', ''),
                    'detail': detail,
                    'id': a.get('id', '')
                })
            except Exception:
                pass
for bp in bp_scores:
    bp_scores[bp].sort(key=lambda x: x['ts'])

all_events = []
for bp, runs in bp_runs.items():
    bp_score_list = bp_scores.get(bp, [])
    score_offset = max(0, len(runs) - len(bp_score_list))
    for i, r in enumerate(runs):
        ts = r.get('spawned_at', '')
        if not ts and 'run_id' in r:
            try:
                parts = r['run_id'].split('-')
                if len(parts) == 2 and len(parts[0]) == 8:
                    ts = parts[0][:4] + '-' + parts[0][4:6] + '-' + parts[0][6:8] + 'T' + parts[1][:2] + ':' + parts[1][2:4] + ':' + parts[1][4:6] + 'Z'
            except Exception:
                pass
        score = None
        sc_idx = i - score_offset
        if sc_idx >= 0 and sc_idx < len(bp_score_list):
            score = bp_score_list[sc_idx]['score']
        all_events.append({
            'blueprint': bp,
            'ts': ts,
            'run_id': r.get('run_id', ''),
            'iteration': r.get('iteration', 1),
            'stage': r.get('stage', 'refinery'),
            'status': r.get('status', ''),
            'score': score,
            'benchmark': r.get('benchmark', ''),
            'detail': r.get('spawned_at', '')
        })

all_events.sort(key=lambda e: e['ts'])
data_json = json.dumps(all_events)

valid_times = [e['ts'] for e in all_events if e['ts']]
if not valid_times:
    valid_times = ['2026-06-25T00:00:00Z']

scored_count = len(scores_raw)
promotable_count = sum(1 for s in scores_raw if s >= 85) if scores_raw else 0
promotable_pct = round(100 * promotable_count / len(scores_raw), 1) if scores_raw else 0
avg_score = round(sum(scores_raw) / len(scores_raw), 1) if scores_raw else 0
score_min = round(min(scores_raw), 1) if scores_raw else 0
score_max = round(max(scores_raw), 1) if scores_raw else 0
time_start = all_ts[0][:10] if all_ts else ''
time_end = all_ts[-1][:10] if all_ts else ''

stat_json = json.dumps({
    'total_agents': total_agents,
    'blueprint_count': len(all_blueprints),
    'run_count': len(agents),
    'production_count': all_stages.get('production', 0),
    'refinery_count': all_stages.get('refinery', 0),
    'archive_count': all_stages.get('archive', 0),
    'scored_count': scored_count,
    'promotable_count': promotable_count,
    'promotable_pct': promotable_pct,
    'avg_score': avg_score,
    'score_min': score_min,
    'score_max': score_max,
    'time_start': time_start,
    'time_end': time_end
})

# === STEP 4: RENDER HTML with summary-first, score range slider, search, stage filter ===
HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline v5</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0d1117;color:#e6edf3;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;overflow-x:hidden}
.header{padding:20px 30px;background:#161b22;border-bottom:1px solid #30363d;display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.header h1{font-size:22px;font-weight:600;color:#f0f6fc}
.header .stats{display:flex;gap:16px;font-size:13px;color:#8b949e;flex-wrap:wrap}
.header .stats span strong{color:#e6edf3}
.promotion-bar{display:flex;padding:0 30px 10px;gap:20px;flex-wrap:wrap}
.promotion-stat{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:8px 16px;min-width:100px;flex:1;text-align:center}
.promotion-stat .val{font-size:20px;font-weight:700;color:#f0f6fc}
.promotion-stat .label{font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px}
.promotion-stat .val.gold{color:#d29922}
.promotion-stat .val.green{color:#3fb950}
.promotion-stat .val.blue{color:#58a6ff}
.promotion-stat .val.red{color:#f85149}
.controls{display:flex;align-items:center;gap:12px;padding:12px 30px;background:#0d1117;border-bottom:1px solid #21262d;flex-wrap:wrap}
.controls label{font-size:12px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px}
.controls input[type=range]{width:200px;accent-color:#d29922;cursor:pointer}
.controls .time-display{font-size:13px;color:#e6edf3;font-family:monospace;min-width:160px}
.controls button{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px;font-weight:500}
.controls button:hover{background:#30363d}
.controls button.active{background:#1f6feb;border-color:#1f6feb;color:#fff}
.controls select{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:4px 8px;border-radius:6px;font-size:12px}
.controls input[type=text]{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:4px 8px;border-radius:6px;font-size:12px;width:160px}
.controls .score-range{display:flex;align-items:center;gap:6px}
.controls .score-range input[type=range]{width:100px}
.controls .score-range .val{font-size:11px;color:#e6edf3;font-family:monospace;min-width:24px;text-align:center}
.filter-count{font-size:11px;color:#8b949e;padding:0 4px}
.legend{display:flex;gap:16px;padding:8px 30px;font-size:11px;color:#8b949e;border-bottom:1px solid #21262d;flex-wrap:wrap}
.legend-item{display:flex;align-items:center;gap:5px}
.legend-dot{width:10px;height:10px;border-radius:50%;border:1px solid rgba(255,255,255,.15)}
.timeline-wrap{overflow:auto;max-height:calc(100vh - 240px);position:relative}
.timeline-svg{display:block;min-width:100%}
.tooltip{position:fixed;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px 20px;z-index:1000;max-width:400px;box-shadow:0 8px 24px rgba(0,0,0,.5);pointer-events:none;display:none;font-size:12px}
.tooltip h3{font-size:14px;font-weight:600;color:#f0f6fc;margin-bottom:8px}
.tooltip .row{display:flex;justify-content:space-between;gap:16px;padding:3px 0;border-bottom:1px solid #21262d}
.tooltip .row:last-child{border-bottom:none}
.tooltip .label{color:#8b949e}
.tooltip .value{color:#e6edf3;font-family:monospace;text-align:right}
.badge{display:inline-block;padding:1px 8px;border-radius:10px;font-size:11px;font-weight:600}
.badge-production{background:rgba(63,185,80,.15);color:#3fb950;border:1px solid rgba(63,185,80,.3)}
.badge-archive{background:rgba(139,148,158,.15);color:#8b949e;border:1px solid rgba(139,148,158,.3)}
.badge-refinery{background:rgba(88,166,255,.15);color:#58a6ff;border:1px solid rgba(88,166,255,.3)}
.empty-state{padding:60px;text-align:center;color:#8b949e;font-size:14px}
</style>
</head>
<body>

<div class="header">
  <h1>Agent Lifecycle Timeline v5</h1>
  <div class="stats">
    <span>Blueprints: <strong id="bp-count">0</strong></span>
    <span>Runs: <strong id="run-count">0</strong></span>
    <span>Production: <strong id="prod-count">0</strong></span>
    <span>Scored: <strong id="scored-count">0</strong></span>
    <span>Span: <strong id="time-span">...</strong></span>
  </div>
</div>

<div class="promotion-bar" id="promotion-bar">
  <div class="promotion-stat">
    <div class="val green" id="stat-promotable">--</div>
    <div class="label">Promotable (>=85)</div>
  </div>
  <div class="promotion-stat">
    <div class="val blue" id="stat-avg">--</div>
    <div class="label">Avg Score</div>
  </div>
  <div class="promotion-stat">
    <div class="val" id="stat-production">--</div>
    <div class="label">In Production</div>
  </div>
  <div class="promotion-stat">
    <div class="val gold" id="stat-refinery">--</div>
    <div class="label">In Refinery</div>
  </div>
  <div class="promotion-stat">
    <div class="val red" id="stat-archive">--</div>
    <div class="label">Archived</div>
  </div>
  <div class="promotion-stat">
    <div class="val" id="stat-total">--</div>
    <div class="label">Total Agents</div>
  </div>
</div>

<div class="controls">
  <label>Time</label>
  <input type="range" id="time-slider" min="0" max="100" value="100" step="1">
  <span class="time-display" id="time-display">All time</span>
  <button id="play-btn">Play</button>
  <button id="reset-btn">Reset</button>
  <label>Stage</label>
  <select id="stage-filter">
    <option value="all">All</option>
    <option value="production">Production</option>
    <option value="refinery">Refinery</option>
    <option value="archive">Archive</option>
  </select>
  <label>Search</label>
  <input type="text" id="search-input" placeholder="Blueprint name...">
  <label>Score</label>
  <div class="score-range">
    <span class="val" id="score-min-label">0</span>
    <input type="range" id="score-min-slider" min="0" max="100" value="0" step="1">
    <span class="val" id="score-max-label">100</span>
    <input type="range" id="score-max-slider" min="0" max="100" value="100" step="1">
  </div>
  <span class="filter-count" id="filter-count"></span>
</div>

<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:#3fb950"></div> Production</div>
  <div class="legend-item"><div class="legend-dot" style="background:#58a6ff"></div> Refinery</div>
  <div class="legend-item"><div class="legend-dot" style="background:#8b949e"></div> Archive</div>
  <div class="legend-item"><div class="legend-dot" style="background:#d29922"></div> Score 85+</div>
  <div class="legend-item"><div class="legend-dot" style="background:#db6d28"></div> Score 70-84</div>
  <div class="legend-item"><div class="legend-dot" style="background:#f85149"></div> Score below 70</div>
</div>

<div class="timeline-wrap" id="timeline-wrap">
  <div class="empty-state" id="empty-state">Loading timeline data...</div>
  <svg class="timeline-svg" id="timeline-svg"></svg>
</div>

<div class="tooltip" id="tooltip"></div>

<script>
var DATA = ''' + data_json + r''';
var STATS = ''' + stat_json + r''';

function init() {
  var blueprints = [...new Set(DATA.map(function(d) { return d.blueprint; }))].sort();
  var bpRuns = {};
  blueprints.forEach(function(bp) {
    bpRuns[bp] = DATA.filter(function(d) { return d.blueprint === bp; })
      .sort(function(a,b) { return (a.ts||'').localeCompare(b.ts||''); });
  });

  var allTimes = DATA.map(function(d) { return d.ts ? new Date(d.ts) : null; }).filter(function(t) { return t && !isNaN(t.getTime()); });
  if (allTimes.length === 0) allTimes = [new Date()];
  var tMin = new Date(Math.min.apply(null, allTimes));
  var tMax = new Date(Math.max.apply(null, allTimes));
  var tRange = tMax - tMin || 1;

  var prodCount = DATA.filter(function(d) { return d.stage === 'production'; }).length;
  var scoredCount = DATA.filter(function(d) { return d.score !== null; }).length;

  document.getElementById('bp-count').textContent = blueprints.length;
  document.getElementById('run-count').textContent = DATA.length;
  document.getElementById('prod-count').textContent = prodCount;
  document.getElementById('scored-count').textContent = scoredCount;
  document.getElementById('time-span').textContent = tMin.toLocaleDateString() + ' - ' + tMax.toLocaleDateString();

  // SUMMARY FIRST: populate promotion stats bar
  document.getElementById('stat-promotable').textContent = STATS.promotable_count + ' (' + STATS.promotable_pct + '%)';
  document.getElementById('stat-avg').textContent = STATS.avg_score;
  document.getElementById('stat-production').textContent = STATS.production_count;
  document.getElementById('stat-refinery').textContent = STATS.refinery_count;
  document.getElementById('stat-archive').textContent = STATS.archive_count;
  document.getElementById('stat-total').textContent = STATS.total_agents;

  var SVG_W = 2200;
  var LABEL_W = 240;
  var ROW_H = 26;
  var NODE_R = 5;
  var PAD_L = 20;
  var PAD_R = 60;
  var plotL = LABEL_W + 10;
  var plotR = SVG_W - PAD_R;
  var plotW = plotR - plotL;

  function tsToX(ts) {
    var t = new Date(ts).getTime();
    if (isNaN(t)) return plotL;
    var p = (t - tMin) / tRange;
    return plotL + p * plotW;
  }

  function nodeColor(ev) {
    var s = ev.score;
    var stage = ev.stage;
    if (s !== null) {
      if (s >= 85) return ['#d29922', '#b0881a'];
      if (s >= 70) return ['#db6d28', '#b85a1a'];
      return ['#f85149', '#da3633'];
    }
    if (stage === 'production') return ['#3fb950', '#2ea043'];
    if (stage === 'refinery') return ['#58a6ff', '#388bfd'];
    return ['#8b949e', '#6e7681'];
  }

  function getFilteredBlueprints() {
    var stageFilter = document.getElementById('stage-filter').value;
    var search = document.getElementById('search-input').value.toLowerCase();
    var scoreMin = parseInt(document.getElementById('score-min-slider').value);
    var scoreMax = parseInt(document.getElementById('score-max-slider').value);
    return blueprints.filter(function(bp) {
      if (search && bp.toLowerCase().indexOf(search) === -1) return false;
      if (stageFilter !== 'all' && !bpRuns[bp].some(function(r) { return r.stage === stageFilter; })) return false;
      // Score range filter: at least one run with score in range
      if (scoreMin > 0 || scoreMax < 100) {
        if (!bpRuns[bp].some(function(r) { return r.score !== null && r.score >= scoreMin && r.score <= scoreMax; })) return false;
      }
      return true;
    });
  }

  function showTooltip(ev, x, y) {
    var tip = document.getElementById('tooltip');
    var stage = ev.stage || 'unknown';
    var stageBadge = 'badge-' + stage;
    var scoreHtml = ev.score !== null ? '<div class="row"><span class="label">Score</span><span class="value">' + ev.score.toFixed(1) + '</span></div>' : '';
    var benchmarkHtml = ev.benchmark ? '<div class="row"><span class="label">Benchmark</span><span class="value">' + ev.benchmark + '</span></div>' : '';
    var iterationHtml = ev.iteration ? '<div class="row"><span class="label">Iteration</span><span class="value">' + ev.iteration + '</span></div>' : '';
    tip.innerHTML = 
      '<h3>' + ev.blueprint + '</h3>' +
      '<div><span class="badge ' + stageBadge + '">' + stage + '</span></div>' +
      '<div class="row"><span class="label">Run ID</span><span class="value">' + ev.run_id + '</span></div>' +
      iterationHtml +
      scoreHtml +
      benchmarkHtml +
      '<div class="row"><span class="label">Status</span><span class="value">' + (ev.status || 'unknown') + '</span></div>' +
      '<div class="row"><span class="label">Timestamp</span><span class="value">' + (ev.ts || '').split('T')[0] + '</span></div>';
    tip.style.display = 'block';
    var w = tip.offsetWidth || 380;
    var tipX = Math.min(x, window.innerWidth - w - 10);
    tipX = Math.max(10, tipX);
    var tipY = Math.min(y, window.innerHeight - 280);
    tipY = Math.max(10, tipY);
    tip.style.left = tipX + 'px';
    tip.style.top = tipY + 'px';
  }

  function hideTooltip() {
    document.getElementById('tooltip').style.display = 'none';
  }

  function render() {
    var slider = document.getElementById('time-slider');
    var sliderVal = parseInt(slider.value);
    var showAll = sliderVal >= 100;
    var cutTime = showAll ? tMax : new Date(tMin.getTime() + (tRange * sliderVal / 100));

    var filteredBps = getFilteredBlueprints();
    var visibleBps = filteredBps.filter(function(bp) {
      if (showAll) return true;
      return bpRuns[bp].some(function(r) { return r.ts && new Date(r.ts) <= cutTime; });
    });

    document.getElementById('filter-count').textContent = visibleBps.length + '/' + blueprints.length + ' BPs';

    if (visibleBps.length === 0) {
      document.getElementById('timeline-svg').style.display = 'none';
      document.getElementById('empty-state').style.display = 'block';
      return;
    }
    document.getElementById('timeline-svg').style.display = 'block';
    document.getElementById('empty-state').style.display = 'none';

    var h = visibleBps.length * ROW_H + 80;
    var svg = document.getElementById('timeline-svg');
    svg.setAttribute('width', SVG_W);
    svg.setAttribute('height', h);
    svg.setAttribute('viewBox', '0 0 ' + SVG_W + ' ' + h);

    var html = '<rect width="' + SVG_W + '" height="' + h + '" fill="#0d1117"/>';

    // Time axis
    var axisTicks = 10;
    html += '<line x1="' + plotL + '" y1="40" x2="' + plotR + '" y2="40" stroke="#30363d" stroke-width="1"/>';
    for (var i = 0; i <= axisTicks; i++) {
      var t = new Date(tMin.getTime() + (tRange * i / axisTicks));
      var x = plotL + (plotW * i / axisTicks);
      html += '<line x1="' + x + '" y1="38" x2="' + x + '" y2="42" stroke="#30363d" stroke-width="1"/>';
      html += '<text x="' + x + '" y="30" text-anchor="middle" fill="#8b949e" font-size="9" font-family="monospace">'
        + t.toLocaleDateString('en-US',{month:'short',day:'numeric',hour:'2-digit'}) + '</text>';
    }

    // Cutoff line
    if (!showAll) {
      var cutX = tsToX(cutTime.toISOString());
      html += '<line x1="' + cutX + '" y1="38" x2="' + cutX + '" y2="' + h + '" stroke="#d29922" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>';
    }

    // Rows
    visibleBps.forEach(function(bp, idx) {
      var y = 60 + idx * ROW_H;
      var runs = bpRuns[bp];

      if (idx % 2 === 0) {
        html += '<rect x="0" y="' + y + '" width="' + SVG_W + '" height="' + ROW_H + '" fill="#161b22" opacity="0.3"/>';
      }

      var label = bp.length > 32 ? bp.slice(0, 30) + '..' : bp;
      html += '<text x="10" y="' + (y + ROW_H * 0.65) + '" fill="#e6edf3" font-size="11" font-family="monospace">'
        + label.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') + '</text>';

      html += '<line x1="' + plotL + '" y1="' + (y + ROW_H/2) + '" x2="' + plotR + '" y2="' + (y + ROW_H/2) + '" stroke="#30363d" stroke-width="1" opacity="0.4"/>';

      runs.forEach(function(ev) {
        var cx = tsToX(ev.ts);
        if (cx < plotL || cx > plotR) return;
        if (!showAll && ev.ts && new Date(ev.ts) > cutTime) return;
        var nc = nodeColor(ev);
        var fill = nc[0], stroke = nc[1];
        var r = NODE_R + (ev.score !== null ? 2 : 0);
        var evIdx = DATA.indexOf(ev);
        html += '<circle class="node" cx="' + cx + '" cy="' + (y + ROW_H/2) + '" r="' + r + '" fill="' + fill + '" stroke="' + stroke + '" stroke-width="1" opacity="0.9"'
          + ' data-idx="' + evIdx + '" style="cursor:pointer"'
          + ' onmouseover="showTooltip(DATA[this.dataset.idx],event.clientX,event.clientY)"'
          + ' onmouseout="hideTooltip()"'
          + '/>';
      });

      // Sparkline of last 15 scores
      var scores = runs.map(function(r) { return r.score; }).filter(function(s) { return s !== null; });
      if (scores.length > 0) {
        var maxS = Math.max.apply(null, scores.concat([70]));
        var minS = Math.min.apply(null, scores.concat([0]));
        var sRange = maxS - minS || 1;
        var sparkX = plotR + 8;
        scores.slice(-15).forEach(function(s, si) {
          var barH = Math.max(2, (s - minS) / sRange * 12);
          var barColor = s >= 85 ? '#d29922' : s >= 70 ? '#db6d28' : '#f85149';
          html += '<rect x="' + (sparkX + si * 3) + '" y="' + (y + ROW_H/2 - barH) + '" width="2" height="' + barH + '" fill="' + barColor + '" opacity="0.7"/>';
        });
      }
    });

    svg.innerHTML = html;
  }

  // --- EVENT BINDING ---
  var slider = document.getElementById('time-slider');
  var timeDisplay = document.getElementById('time-display');

  function formatTimeDisplay() {
    var val = parseInt(slider.value);
    if (val >= 100) {
      timeDisplay.textContent = 'All time (' + DATA.length + ' runs)';
    } else {
      var t = new Date(tMin.getTime() + (tRange * val / 100));
      timeDisplay.textContent = t.toLocaleDateString('en-US',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'});
    }
  }

  slider.addEventListener('input', function() { formatTimeDisplay(); render(); });

  var playing = false;
  var playInterval = null;
  var playBtn = document.getElementById('play-btn');
  playBtn.addEventListener('click', function() {
    if (playing) {
      clearInterval(playInterval);
      playing = false;
      playBtn.textContent = 'Play';
      playBtn.classList.remove('active');
    } else {
      playing = true;
      playBtn.textContent = 'Pause';
      playBtn.classList.add('active');
      if (parseInt(slider.value) >= 100) slider.value = 0;
      playInterval = setInterval(function() {
        var val = parseInt(slider.value);
        if (val >= 100) {
          val = 0;
          clearInterval(playInterval);
          playing = false;
          playBtn.textContent = 'Play';
          playBtn.classList.remove('active');
        }
        slider.value = val + 1;
        formatTimeDisplay();
        render();
      }, 150);
    }
  });

  document.getElementById('reset-btn').addEventListener('click', function() {
    slider.value = 100;
    formatTimeDisplay();
    render();
    if (playing) {
      clearInterval(playInterval);
      playing = false;
      playBtn.textContent = 'Play';
      playBtn.classList.remove('active');
    }
  });

  document.getElementById('stage-filter').addEventListener('change', render);
  document.getElementById('search-input').addEventListener('input', render);

  // Score range slider handlers
  document.getElementById('score-min-slider').addEventListener('input', function() {
    var min = parseInt(document.getElementById('score-min-slider').value);
    var max = parseInt(document.getElementById('score-max-slider').value);
    if (min > max) document.getElementById('score-min-slider').value = max;
    document.getElementById('score-min-label').textContent = document.getElementById('score-min-slider').value;
    render();
  });
  document.getElementById('score-max-slider').addEventListener('input', function() {
    var min = parseInt(document.getElementById('score-min-slider').value);
    var max = parseInt(document.getElementById('score-max-slider').value);
    if (max < min) document.getElementById('score-max-slider').value = min;
    document.getElementById('score-max-label').textContent = document.getElementById('score-max-slider').value;
    render();
  });

  formatTimeDisplay();
  render();
}

document.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>'''

with open('agent-lifecycle-timeline-v5.html', 'w') as f:
    f.write(HTML)

print('Written ' + str(len(HTML)) + ' bytes to agent-lifecycle-timeline-v5.html')
print('Events: ' + str(len(all_events)) + ', Blueprints: ' + str(len(all_blueprints)))
