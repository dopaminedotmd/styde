import yaml, re, json
from datetime import datetime
from collections import defaultdict

with open('state.yaml', 'r') as f:
    data = yaml.safe_load(f)

events = data.get('activity', [])
bp_events = [e for e in events if e.get('blueprint') == 'agent-lifecycle-timeline' and e.get('action') in ('spawn', 'eval', 'improve')]

def extract_score(e):
    detail = e.get('detail', '')
    m = re.search(r'C:(\d+\.?\d*)', detail)
    if m:
        return float(m.group(1))
    return None

for e in bp_events:
    e['composite'] = extract_score(e)

bp_events.sort(key=lambda e: e.get('timestamp', ''))

by_id = defaultdict(list)
for e in bp_events:
    by_id[e.get('id')].append(e)

agent_ids = sorted(by_id.keys())
num_agents = len(agent_ids)

all_ts = [datetime.fromisoformat(e['timestamp'].replace('Z','+00:00')) for e in bp_events if e.get('timestamp')]
t_min = min(all_ts)
t_max = max(all_ts)
t_range_sec = (t_max - t_min).total_seconds()

nodes = []
for idx, aid in enumerate(agent_ids):
    runs = by_id[aid]
    y_pos = idx * 40 + 60
    for run in runs:
        ts = datetime.fromisoformat(run['timestamp'].replace('Z','+00:00'))
        x_ratio = (ts - t_min).total_seconds() / t_range_sec if t_range_sec > 0 else 0.5
        x_pos = 100 + x_ratio * 700
        score = run['composite']
        action = run['action']

        if score is not None:
            if score >= 85:
                color = '#FFD700'
                text_color = '#000'
            elif score >= 70:
                color = '#E8913A'
                text_color = '#fff'
            else:
                color = '#4A90D9'
                text_color = '#fff'
        else:
            if action == 'spawn':
                color = '#555'
                text_color = '#fff'
            elif action == 'improve':
                color = '#777'
                text_color = '#fff'
            else:
                color = '#666'
                text_color = '#fff'

        detail = run.get('detail', '')
        detail_short = detail[:60] + '...' if len(detail) > 60 else detail

        node = {
            'id': aid,
            'action': action,
            'score': score,
            'x': round(x_pos, 1),
            'y': y_pos,
            'color': color,
            'text_color': text_color,
            'timestamp': ts.strftime('%H:%M:%S'),
            'detail': detail_short,
            'detail_full': detail,
            'progress': run.get('progress', ''),
            'status': run.get('status', '')
        }
        nodes.append(node)

nodes_json = json.dumps(nodes)

svg_height = 60 + num_agents * 40 + 40

agent_labels = '\n'.join(
    f'<text x="20" y="{idx * 40 + 65}" fill="#666" font-size="11" font-family="monospace">{aid}</text>'
    for idx, aid in enumerate(agent_ids)
)

track_lines = '\n'.join(
    f'<line x1="95" y1="{idx * 40 + 60}" x2="805" y2="{idx * 40 + 60}" stroke="#222" stroke-width="1"/>'
    for idx, aid in enumerate(agent_ids)
)

node_elements = []
for i, n in enumerate(nodes):
    radius = 6 if n['score'] is not None else 4
    glow = ' filter="url(#glow)"' if n['score'] is not None and n['score'] >= 85 else ''
    stroke = '#fff' if n['score'] is not None and n['score'] >= 85 else 'transparent'
    circle = f'<circle id="n-{n["id"]}-{i}" cx="{n["x"]}" cy="{n["y"]}" r="{radius}" fill="{n["color"]}" stroke="{stroke}" stroke-width="1"{glow} onclick="showPopup({json.dumps(n)})" style="cursor:pointer;"/>'
    if n['score'] is not None:
        label = f'<text x="{n["x"]}" y="{n["y"] - 10}" fill="{n["text_color"]}" font-size="9" text-anchor="middle" font-weight="bold" onclick="showPopup({json.dumps(n)})" style="cursor:pointer;">{n["score"]}</text>'
    else:
        label = f'<text x="{n["x"]}" y="{n["y"] - 9}" fill="#666" font-size="8" text-anchor="middle" onclick="showPopup({json.dumps(n)})" style="cursor:pointer;">{n["action"][0].upper()}</text>'
    node_elements.append(circle)
    node_elements.append(label)

node_svg = '\n'.join(node_elements)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #1a1a2e; color: #eee; font-family: 'Segoe UI', system-ui, sans-serif; overflow-x: hidden; }}
h1 {{ font-size: 16px; font-weight: 400; color: #aaa; padding: 16px 24px 4px; }}
h1 strong {{ color: #FFD700; font-weight: 600; }}
.sub {{ font-size: 12px; color: #666; padding: 0 24px 16px; }}
#container {{ position: relative; width: 900px; margin: 0 auto; }}
#timeline-svg {{ width: 100%; display: block; }}
#controls {{ display: flex; align-items: center; gap: 12px; padding: 12px 24px; background: #16213e; border-radius: 8px; margin: 8px 24px; }}
#controls button {{ background: #0f3460; color: #fff; border: none; padding: 6px 16px; border-radius: 4px; cursor: pointer; font-size: 13px; }}
#controls button:hover {{ background: #1a5276; }}
#controls button.active {{ background: #e94560; }}
#slider {{ flex: 1; accent-color: #FFD700; }}
#time-label {{ font-size: 12px; color: #888; min-width: 80px; text-align: center; font-family: monospace; }}
#popup {{ display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #16213e; border: 1px solid #333; border-radius: 12px; padding: 24px; z-index: 100; min-width: 320px; max-width: 500px; box-shadow: 0 8px 40px rgba(0,0,0,0.6); }}
#popup h2 {{ font-size: 18px; margin-bottom: 12px; }}
#popup table {{ width: 100%; border-collapse: collapse; }}
#popup td {{ padding: 4px 8px; font-size: 13px; }}
#popup td:first-child {{ color: #888; width: 80px; }}
#popup .close {{ float: right; cursor: pointer; color: #e94560; font-size: 20px; }}
#overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 99; }}
.legend {{ display: flex; gap: 20px; padding: 8px 24px; font-size: 11px; color: #888; }}
.legend-item {{ display: flex; align-items: center; gap: 4px; }}
.legend-dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}
</style>
</head>
<body>

<h1>agent-lifecycle-timeline <strong>Agent Lifecycle Timeline</strong></h1>
<div class="sub">{len(nodes)} events across {num_agents} agents | {t_min.strftime("%H:%M")} &ndash; {t_max.strftime("%H:%M")} UTC</div>

<div class="legend">
  <span class="legend-item"><span class="legend-dot" style="background:#FFD700"></span> 85+ (gold/production)</span>
  <span class="legend-item"><span class="legend-dot" style="background:#E8913A"></span> 70-84 (amber)</span>
  <span class="legend-item"><span class="legend-dot" style="background:#4A90D9"></span> &lt;70 (cool)</span>
  <span class="legend-item"><span class="legend-dot" style="background:#555"></span> spawn</span>
  <span class="legend-item"><span class="legend-dot" style="background:#777"></span> improve</span>
</div>

<div id="container">
<svg id="timeline-svg" viewBox="0 0 900 {svg_height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="900" height="{svg_height}" fill="#1a1a2e"/>
  <line x1="100" y1="{50 + num_agents * 40 + 10}" x2="800" y2="{50 + num_agents * 40 + 10}" stroke="#333" stroke-width="1"/>
  <text x="100" y="{50 + num_agents * 40 + 30}" fill="#555" font-size="10">{t_min.strftime("%H:%M")}</text>
  <text x="450" y="{50 + num_agents * 40 + 30}" fill="#555" font-size="10" text-anchor="middle">{t_min.strftime("%b %d")}</text>
  <text x="800" y="{50 + num_agents * 40 + 30}" fill="#555" font-size="10" text-anchor="end">{t_max.strftime("%H:%M")}</text>
  {agent_labels}
  {track_lines}
  {node_svg}
  <line id="scrubber" x1="100" y1="40" x2="100" y2="{50 + num_agents * 40}" stroke="#e94560" stroke-width="1" stroke-dasharray="3,3" opacity="0.6"/>
</svg>
</div>

<div id="controls">
  <button id="play-btn" onclick="togglePlay()">Play</button>
  <input type="range" id="slider" min="0" max="1000" value="0" oninput="scrub(this.value/1000)">
  <span id="time-label">{t_min.strftime("%H:%M:%S")}</span>
</div>

<div id="overlay" onclick="hidePopup()"></div>
<div id="popup">
  <span class="close" onclick="hidePopup()">&times;</span>
  <h2 id="pop-title">Agent #</h2>
  <table>
    <tr><td>Action</td><td id="pop-action"></td></tr>
    <tr><td>Score</td><td id="pop-score"></td></tr>
    <tr><td>Time</td><td id="pop-time"></td></tr>
    <tr><td>Progress</td><td id="pop-progress"></td></tr>
    <tr><td>Status</td><td id="pop-status"></td></tr>
  </table>
  <div id="pop-detail" style="margin-top:8px;padding:8px;background:#0f3460;border-radius:6px;font-size:12px;color:#ccc;"></div>
</div>

<script>
var nodes = {nodes_json};
var tMin = "{t_min.strftime('%H:%M:%S')}";
var tMax = "{t_max.strftime('%H:%M:%S')}";

function timeToSec(t) {{
  var p = t.split(':');
  return parseInt(p[0])*3600 + parseInt(p[1])*60 + parseInt(p[2]);
}}
var minSec = timeToSec(tMin);
var maxSec = timeToSec(tMax);
var rangeSec = maxSec - minSec || 1;

function secToTime(s) {{
  var h = String(Math.floor(s/3600) % 24).padStart(2,'0');
  var m = String(Math.floor((s%3600)/60)).padStart(2,'0');
  var sec = String(Math.floor(s%60)).padStart(2,'0');
  return h+':'+m+':'+sec;
}}

var isPlaying = false;
var intervalId = null;

function scrub(ratio) {{
  ratio = Math.max(0, Math.min(1, ratio));
  var x = 100 + ratio * 700;
  document.getElementById('scrubber').setAttribute('x1', x);
  document.getElementById('scrubber').setAttribute('x2', x);
  var currentSec = minSec + ratio * rangeSec;
  document.getElementById('time-label').textContent = secToTime(currentSec);

  var tolerance = 0.02;
  var circles = document.querySelectorAll('circle[id^="n-"]');
  for (var i = 0; i < circles.length; i++) {{
    var cx = parseFloat(circles[i].getAttribute('cx'));
    circles[i].setAttribute('opacity', Math.abs(cx - x) / 700 < tolerance ? '1' : '0.3');
  }}
}}

function showPopup(n) {{
  document.getElementById('pop-title').textContent = 'Agent #' + n.id + ' - ' + n.action.charAt(0).toUpperCase() + n.action.slice(1);
  document.getElementById('pop-action').textContent = n.action;
  document.getElementById('pop-score').textContent = n.score !== null ? n.score.toFixed(1) : 'N/A';
  document.getElementById('pop-time').textContent = n.timestamp;
  document.getElementById('pop-progress').textContent = n.progress + '%';
  document.getElementById('pop-status').textContent = n.status;
  document.getElementById('pop-detail').textContent = n.detail_full;
  document.getElementById('popup').style.display = 'block';
  document.getElementById('overlay').style.display = 'block';
}}

function hidePopup() {{
  document.getElementById('popup').style.display = 'none';
  document.getElementById('overlay').style.display = 'none';
}}

function togglePlay() {{
  isPlaying = !isPlaying;
  document.getElementById('play-btn').textContent = isPlaying ? 'Pause' : 'Play';
  document.getElementById('play-btn').classList.toggle('active', isPlaying);
  if (isPlaying) {{
    var slider = document.getElementById('slider');
    intervalId = setInterval(function() {{
      var val = parseFloat(slider.value);
      val += 3;
      if (val > 1000) {{
        val = 0;
      }}
      slider.value = val;
      scrub(val / 1000);
    }}, 50);
  }} else {{
    clearInterval(intervalId);
  }}
}}

scrub(0);
</script>
</body>
</html>'''

with open('agent-lifecycle-timeline.html', 'w', encoding='utf-8') as f:
    f.write(html)

import os
size_kb = os.path.getsize('agent-lifecycle-timeline.html') / 1024
print(f'Written: agent-lifecycle-timeline.html ({size_kb:.0f}KB)')
print(f'Agents: {num_agents}, Events: {len(nodes)}')
print(f'Time range: {t_min} to {t_max}')
print(f'Gold (85+): {sum(1 for n in nodes if n["score"] is not None and n["score"] >= 85)}')
print(f'Amber (70-84): {sum(1 for n in nodes if n["score"] is not None and 70 <= n["score"] < 85)}')
print(f'Cool (<70): {sum(1 for n in nodes if n["score"] is not None and n["score"] < 70)}')
