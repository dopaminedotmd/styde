#!/usr/bin/env python3
import yaml, json, math
from datetime import datetime, timezone
from collections import defaultdict

def parse_ts(s):
    return datetime.strptime(s.replace('Z',''), '%Y-%m-%dT%H:%M:%S')

with open('state.yaml') as f:
    data = yaml.safe_load(f)

events = [e for e in data.get('activity', []) if e.get('blueprint') == 'agent-lifecycle-timeline']
events.sort(key=lambda e: parse_ts(e['timestamp']))

agents = defaultdict(list)
for e in events:
    agents[e['id']].append(e)

agent_order = sorted(agents.keys(), key=lambda aid: min(parse_ts(e['timestamp']) for e in agents[aid]))

t_min = parse_ts(events[0]['timestamp'])
t_max = parse_ts(events[-1]['timestamp'])
span_sec = (t_max - t_min).total_seconds()
if span_sec < 1:
    span_sec = 1

agent_nodes = {}
for aid in agent_order:
    nodes = []
    for e in agents[aid]:
        ts = parse_ts(e['timestamp'])
        comp = e.get('composite')
        action = e['action']
        detail = str(e.get('detail',''))
        status = e.get('status','')
        pct = (ts - t_min).total_seconds() / span_sec * 100
        s_val = None
        j_val = None
        if 'S:' in detail and 'J:' in detail:
            try:
                s_val = float(detail.split('S:')[1].split()[0])
                j_val = float(detail.split('J:')[1].split()[0])
            except:
                pass
        nodes.append({
            'ts': ts.strftime('%H:%M:%S'),
            'pct': pct,
            'action': action,
            'score': comp,
            's_score': s_val,
            'j_score': j_val,
            'detail': detail[:120],
            'status': status,
            'id': aid,
        })
    agent_nodes[aid] = nodes

AGENT_H = 36
TOP_MARGIN = 120
LEFT_MARGIN = 80
RIGHT_MARGIN = 40
TIMELINE_H = len(agent_order) * AGENT_H + TOP_MARGIN + 60
TIMELINE_W = 1100

def score_color(s):
    if s is None:
        return '#94a3b8'
    if s >= 85:
        return '#f59e0b'
    if s >= 70:
        return '#d97706'
    return '#6366f1'

def action_color(action):
    return {'spawn': '#22c55e', 'eval': '#3b82f6', 'improve': '#a855f7'}.get(action, '#94a3b8')

# Build SVG as list of lines to avoid f-string nesting issues
svg_lines = []
def emit(line):
    svg_lines.append(line)

W = TIMELINE_W
H = TIMELINE_H

emit('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" style="background:#0f172a;font-family:system-ui,sans-serif;width:100%%;height:auto;max-width:%dpx">' % (W, H, W))
emit('<defs>')
emit('<filter id="glowGold"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
emit('<filter id="glowAmber"><feGaussianBlur stdDeviation="2" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
emit('<linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%%" stop-color="#1e293b"/><stop offset="100%%" stop-color="#0f172a"/></linearGradient>')
emit('</defs>')
emit('<rect width="%d" height="%d" fill="url(#bgGrad)" rx="12"/>' % (W, H))
emit('<text x="40" y="40" fill="#f8fafc" font-size="20" font-weight="700">agent-lifecycle-timeline Agent Lifecycle Timeline</text>')
emit('<text x="40" y="62" fill="#94a3b8" font-size="13">%d agents | %d events | %s - %s UTC</text>' % (len(agent_order), len(events), t_min.strftime("%b %d %H:%M"), t_max.strftime("%H:%M")))

# Legend
lx = 40
legends = [
    ('#f59e0b', '>=85 hot gold'),
    ('#d97706', '70-84 amber'),
    ('#6366f1', '<70 cool'),
    ('#22c55e', 'spawn'),
    ('#3b82f6', 'eval'),
    ('#a855f7', 'improve'),
]
for color, label in legends:
    emit('<rect x="%d" y="76" width="10" height="10" fill="%s" rx="2"/>' % (lx, color))
    emit('<text x="%d" y="85" fill="#94a3b8" font-size="11">%s</text>' % (lx + 16, label))
    lx += 95

# Timeline bar
bar_y = TOP_MARGIN - 20
emit('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#475569" stroke-width="2"/>' % (LEFT_MARGIN, bar_y, W - RIGHT_MARGIN, bar_y))

# Time ticks every 30 min
tick_interval = 1800
t_sec = int(t_min.timestamp())
t_end = int(t_max.timestamp())
first_tick = (t_sec // tick_interval) * tick_interval
for tt in range(first_tick, t_end + tick_interval, tick_interval):
    dt = datetime.fromtimestamp(tt, tz=timezone.utc).replace(tzinfo=None)
    if dt < t_min:
        continue
    pct = (dt - t_min).total_seconds() / span_sec * 100
    x = LEFT_MARGIN + pct * (W - LEFT_MARGIN - RIGHT_MARGIN) / 100
    emit('<line x1="%f" y1="%d" x2="%f" y2="%d" stroke="#64748b" stroke-width="1.5"/>' % (x, bar_y - 4, x, bar_y + 4))
    emit('<text x="%f" y="%d" fill="#64748b" font-size="10" text-anchor="middle">%s</text>' % (x, bar_y + 18, dt.strftime("%H:%M")))

# Agent tracks
for idx, aid in enumerate(agent_order):
    y = TOP_MARGIN + idx * AGENT_H + 10
    nodes = agent_nodes[aid]
    emit('<text x="%d" y="%d" fill="#94a3b8" font-size="12" text-anchor="end" font-weight="500">#%d</text>' % (LEFT_MARGIN - 12, y + 4, aid))
    emit('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#1e293b" stroke-width="1" stroke-dasharray="4,2"/>' % (LEFT_MARGIN, y, W - RIGHT_MARGIN, y))

    # Cluster close nodes
    sorted_nodes = sorted(nodes, key=lambda n: n['pct'])
    clusters = []
    cur = [sorted_nodes[0]] if sorted_nodes else []
    for n in sorted_nodes[1:]:
        if n['pct'] - cur[-1]['pct'] <= 12:
            cur.append(n)
        else:
            clusters.append(cur)
            cur = [n]
    if cur:
        clusters.append(cur)

    for cluster in clusters:
        if len(cluster) == 1:
            n = cluster[0]
            x = LEFT_MARGIN + n['pct'] * (W - LEFT_MARGIN - RIGHT_MARGIN) / 100
            color = score_color(n['score']) if n['score'] is not None else action_color(n['action'])
            opacity = '0.5' if n['status'] == 'running' else '1'
            tip = 'Agent #%d | %s | %s | Score: %s' % (n['id'], n['ts'], n['action'], n['score'] if n['score'] is not None else 'N/A')
            if n['action'] in ('spawn', 'eval'):
                emit('<circle cx="%f" cy="%d" r="8" fill="%s" opacity="%s" style="cursor:pointer"><title>%s</title></circle>' % (x, y, color, opacity, tip))
            else:
                emit('<rect x="%f" y="%d" width="10" height="10" fill="%s" opacity="%s" rx="2" style="cursor:pointer"><title>%s</title></rect>' % (x - 5, y - 5, color, opacity, tip))
        else:
            for i, n in enumerate(cluster):
                x = LEFT_MARGIN + n['pct'] * (W - LEFT_MARGIN - RIGHT_MARGIN) / 100
                color = score_color(n['score']) if n['score'] is not None else action_color(n['action'])
                opacity = '0.5' if n['status'] == 'running' else '1'
                dy = -8 + i * 4 if len(cluster) > 2 else -4 + i * 8
                tip = 'Agent #%d | %s | %s | Score: %s' % (n['id'], n['ts'], n['action'], n['score'] if n['score'] is not None else 'N/A')
                emit('<circle cx="%f" cy="%d" r="6" fill="%s" opacity="%s" style="cursor:pointer"><title>%s</title></circle>' % (x, y + dy, color, opacity, tip))

    # Mini sparkline for scored agents
    scored = [n for n in nodes if n['score'] is not None]
    if len(scored) >= 2:
        pts = []
        for n in scored:
            x = LEFT_MARGIN + n['pct'] * (W - LEFT_MARGIN - RIGHT_MARGIN) / 100
            sy = y - (n['score'] / 100) * 18
            pts.append('%f,%f' % (x, sy))
        emit('<polyline points="%s" fill="none" stroke="#f59e0b" stroke-width="1" opacity="0.3"/>' % ' '.join(pts))

# Footer
fy = TOP_MARGIN + len(agent_order) * AGENT_H + 25
spawned = sum(1 for e in events if e['action'] == 'spawn')
evalled = sum(1 for e in events if e['action'] == 'eval')
improved = sum(1 for e in events if e['action'] == 'improve')
scores = [e.get('composite') for e in events if e.get('composite') is not None]
avg = sum(scores)/len(scores) if scores else 0
best = max(scores) if scores else 0
running_count = sum(1 for e in events if e['status'] == 'running')
emit('<text x="40" y="%d" fill="#64748b" font-size="12">%d spawns | %d evals | %d improves | avg score %.1f | best %.1f | %d agents</text>' % (fy, spawned, evalled, improved, avg, best, len(agent_order)))
emit('<text x="%d" y="%d" fill="#f59e0b" font-size="12" text-anchor="end">%d running / %d agents</text>' % (W - 40, fy, running_count, len(agent_order)))
emit('</svg>')

svg_content = '\n'.join(svg_lines)

# Full HTML wrapper
html_parts = []
html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0f1a;display:flex;flex-direction:column;align-items:center;padding:20px;font-family:system-ui,sans-serif}
svg{border-radius:12px;box-shadow:0 4px 24px rgba(0,0,0,0.4)}
.controls{display:flex;align-items:center;gap:16px;margin:16px 0;padding:12px 24px;background:#1e293b;border-radius:8px;width:100%;max-width:%dpx}
.controls button{background:#334155;color:#f8fafc;border:none;padding:6px 16px;border-radius:6px;cursor:pointer;font-size:13px;transition:background 0.2s}
.controls button:hover{background:#475569}
.controls input[type=range]{flex:1;accent-color:#f59e0b;height:4px;cursor:pointer}
.controls .time-label{color:#94a3b8;font-size:12px;white-space:nowrap;min-width:100px;text-align:center}
.popup{display:none;position:fixed;top:50%%;left:50%%;transform:translate(-50%%,-50%%);background:#1e293b;border:1px solid #334155;border-radius:12px;padding:24px;z-index:1000;min-width:320px;max-width:480px;box-shadow:0 8px 40px rgba(0,0,0,0.6);color:#f8fafc}
.popup h3{font-size:16px;margin-bottom:8px;color:#f59e0b}
.popup table{width:100%%;border-collapse:collapse;font-size:13px}
.popup td{padding:4px 8px;border-bottom:1px solid #334155}
.popup td:first-child{color:#64748b;width:90px}
.popup .close{float:right;background:#334155;border:none;color:#f8fafc;padding:4px 12px;border-radius:4px;cursor:pointer;font-size:12px}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:999}
</style>
</head>
<body>
''' % TIMELINE_W)

html_parts.append(svg_content)

html_parts.append('''
<div class="controls">
  <button id="playBtn">▶ Play</button>
  <button id="resetBtn">↺ Reset</button>
  <input type="range" id="scrubber" min="0" max="100" value="100" step="0.1">
  <span class="time-label" id="timeLabel">100% - end</span>
</div>
<div class="overlay" id="overlay"></div>
<div class="popup" id="popup">
  <button class="close" onclick="closePopup()">&#10005;</button>
  <h3 id="popupTitle">Agent Detail</h3>
  <table><tbody id="popupBody"></tbody></table>
</div>

<script>
var svg = document.querySelector('svg');
var scrubber = document.getElementById('scrubber');
var timeLabel = document.getElementById('timeLabel');
var playBtn = document.getElementById('playBtn');
var playing = false;
var timer = null;

var titles = svg.querySelectorAll('title');
var nodeData = [];
for (var i = 0; i < titles.length; i++) {
  var t = titles[i];
  var parent = t.parentElement;
  var x = parseFloat(parent.getAttribute('cx') || parent.getAttribute('x')) || 0;
  var op = parent.getAttribute('opacity') || '1';
  nodeData.push({ text: t.textContent, x: x, el: parent, origOpacity: op });
}
nodeData.sort(function(a, b) { return a.x - b.x; });

var trackLines = svg.querySelectorAll('line[stroke-dasharray]');
var lineEls = [];
for (var i = 0; i < trackLines.length; i++) { lineEls.push(trackLines[i]); }

var minX = 80;
var maxX = 1060;
if (trackLines.length > 0) {
  minX = parseFloat(trackLines[0].getAttribute('x1')) || 80;
  maxX = parseFloat(trackLines[0].getAttribute('x2')) || 1060;
}

function applyScrubber(val) {
  var pct = parseFloat(val);
  var cutoffX = minX + (maxX - minX) * pct / 100;
  for (var i = 0; i < nodeData.length; i++) {
    var d = nodeData[i];
    if (d.x <= cutoffX + 2) {
      d.el.style.opacity = d.origOpacity;
      d.el.style.display = '';
    } else {
      d.el.style.opacity = '0.08';
      d.el.style.display = '';
    }
  }
  // update tracks
  for (var i = 0; i < lineEls.length; i++) {
    lineEls[i].style.opacity = '0.2';
  }
  var shown = {};
  for (var i = 0; i < nodeData.length; i++) {
    var d = nodeData[i];
    if (d.x <= cutoffX + 2) {
      var cy = parseFloat(d.el.getAttribute('cy') || d.el.getAttribute('y')) || 0;
      for (var j = 0; j < lineEls.length; j++) {
        var ly = parseFloat(lineEls[j].getAttribute('y1')) || 0;
        if (Math.abs(cy - ly) < 18) {
          lineEls[j].style.opacity = '1';
        }
      }
    }
  }
  // time label
  var last = null;
  for (var i = 0; i < nodeData.length; i++) {
    if (nodeData[i].x <= cutoffX + 2) { last = nodeData[i]; }
  }
  if (last) {
    var parts = last.text.split('|');
    var ts = (parts[1] || '').trim();
    timeLabel.textContent = pct.toFixed(0) + '% - ' + ts;
  } else {
    timeLabel.textContent = pct.toFixed(0) + '% - start';
  }
}

scrubber.addEventListener('input', function() { applyScrubber(scrubber.value); });

function togglePlay() {
  if (playing) {
    clearInterval(timer);
    playing = false;
    playBtn.textContent = '▶ Play';
  } else {
    var val = parseFloat(scrubber.value);
    if (val >= 99) val = 0;
    playing = true;
    playBtn.textContent = '⏸ Pause';
    timer = setInterval(function() {
      var v = parseFloat(scrubber.value) + 0.5;
      if (v > 100) {
        v = 100;
        clearInterval(timer);
        playing = false;
        playBtn.textContent = '▶ Play';
      }
      scrubber.value = v;
      applyScrubber(v);
    }, 100);
  }
}

playBtn.addEventListener('click', togglePlay);

document.getElementById('resetBtn').addEventListener('click', function() {
  scrubber.value = 100;
  applyScrubber(100);
  if (playing) togglePlay();
});

function showPopup(text) {
  var parts = text.split('|');
  document.getElementById('popupTitle').textContent = parts[0] || 'Agent';
  var rows = '';
  for (var i = 1; i < parts.length; i++) {
    var p = parts[i].trim();
    var kv = p.split(':');
    var key = kv[0] + ':';
    var val = kv.slice(1).join(':');
    rows += '<tr><td>' + key + '</td><td>' + val + '</td></tr>';
  }
  document.getElementById('popupBody').innerHTML = rows;
  document.getElementById('popup').style.display = 'block';
  document.getElementById('overlay').style.display = 'block';
}

function closePopup() {
  document.getElementById('popup').style.display = 'none';
  document.getElementById('overlay').style.display = 'none';
}

svg.addEventListener('click', function(e) {
  var target = e.target.closest('circle') || e.target.closest('rect');
  if (target) {
    var t = target.querySelector('title');
    if (t) { showPopup(t.textContent); }
  }
});

document.getElementById('overlay').addEventListener('click', closePopup);

applyScrubber(100);
</script>
</body>
</html>''')

result = '\n'.join(html_parts)
with open('agent-lifecycle-timeline.html', 'w', encoding='utf-8') as f:
    f.write(result)
print('Generated: agent-lifecycle-timeline.html (%d bytes)' % len(result))
