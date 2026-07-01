#!/usr/bin/env python3
"""Generate Agent Lifecycle Timeline HTML from state.yaml"""
import yaml, json, re, sys
from collections import defaultdict
from datetime import datetime

def parse_state(path='state.yaml'):
    with open(path) as f:
        data = yaml.safe_load(f)
    activities = data.get('activity', [])
    rows = []
    for a in activities:
        bp = a.get('blueprint', '?')
        action = a.get('action', '?')
        detail = a.get('detail', '')
        ts = a.get('timestamp', '')
        aid = a.get('id', 0)
        status = a.get('status', '')
        score = None
        m = re.search(r'C:([\d.]+)', detail)
        if m:
            score = float(m.group(1))
        rows.append({
            'bp': bp, 'action': action, 'id': aid,
            'ts': ts, 'detail': detail, 'status': status,
            'score': score
        })
    rows.sort(key=lambda r: r['ts'])
    return rows

def color_for_bp(idx):
    palette = [
        '#e06b6b','#6ba3e0','#6be0b8','#e0c46b','#b86be0',
        '#e06ba0','#6bd4e0','#8be06b','#e0a06b','#6b6be0',
        '#e06b6b','#6be0a8','#a86be0','#6bc8e0','#d46be0',
        '#e0c06b','#6be0d4','#e08b6b','#8b6be0','#6be08b',
        '#e06b8b','#6be0c0','#b8e06b','#b06be0','#e0b06b',
        '#6b6be0','#6be0e0','#e06be0','#8be0a0','#a0e06b'
    ]
    return palette[idx % len(palette)]

def score_color(s):
    if s is None: return '#30363d'
    if s >= 85: return '#ffb347'
    if s >= 70: return '#d29922'
    return '#58a6ff'

def score_label(s):
    if s is None: return '?'
    return f'{s:.1f}'

def action_icon(a):
    return {'spawn': '\u25b7', 'eval': '\u25c9', 'improve': '\u2699'}.get(a, '\u25cf')

def generate_html(rows):
    by_bp = defaultdict(list)
    for r in rows:
        by_bp[r['bp']].append(r)
    bp_order = sorted(by_bp.keys(), key=lambda b: len(by_bp[b]), reverse=True)

    t_min = rows[0]['ts']
    t_max = rows[-1]['ts']
    try:
        dt_min = datetime.fromisoformat(t_min.replace('Z','+00:00'))
        dt_max = datetime.fromisoformat(t_max.replace('Z','+00:00'))
        total_secs = (dt_max - dt_min).total_seconds()
    except:
        total_secs = 1

    # Layout
    track_h = 28
    margin_l = 260
    margin_r = 40
    timeline_w = 1400
    node_r = 7
    header_h = 50

    n_tracks = len(bp_order)
    svg_h = header_h + n_tracks * track_h + 40

    def x_pos(ts):
        try:
            dt = datetime.fromisoformat(ts.replace('Z','+00:00'))
            frac = (dt - dt_min).total_seconds() / total_secs if total_secs > 0 else 0
        except:
            frac = 0.5
        return margin_l + frac * timeline_w

    # Build BP lookup
    bp_list = []
    for i, bp in enumerate(bp_order):
        bp_list.append([bp, color_for_bp(i), len(by_bp[bp])])

    events_list = []
    for r in rows:
        events_list.append([r['bp'], r['action'], r['id'], r['ts'], r['detail'], r['score']])

    # Generate tracks
    tracks_svg = ''
    for i, bp in enumerate(bp_order):
        y = header_h + i * track_h + track_h // 2
        # Track bg
        bg = '#161b22' if i % 2 == 0 else '#0d1117'
        tracks_svg += f'<rect x="{margin_l}" y="{y - track_h//2}" width="{timeline_w}" height="{track_h}" fill="{bg}" rx="2"/>\n'
        # Label
        label = bp[:30] + '...' if len(bp) > 30 else bp
        tracks_svg += f'<text x="{margin_l - 8}" y="{y + 4}" text-anchor="end" font-size="11" fill="#8b949e" font-family="monospace">{label}</text>\n'
        # Nodes
        for r in by_bp[bp]:
            x = x_pos(r['ts'])
            c = score_color(r['score'])
            sc = score_label(r['score'])
            tracks_svg += f'<circle cx="{x}" cy="{y}" r="{node_r}" fill="{c}" stroke="#0d1117" stroke-width="1.5" class="evt" data-bp="{r["bp"]}" data-action="{r["action"]}" data-id="{r["id"]}" data-ts="{r["ts"]}" data-detail="{r["detail"]}" data-score="{sc}" style="cursor:pointer;transition:r .15s" onmouseenter="this.setAttribute(\'r\',{node_r+3})" onmouseleave="this.setAttribute(\'r\',{node_r})" onclick="showDetail(event,this)"/>\n'

    # Time axis
    axis_svg = ''
    n_ticks = 8
    for i in range(n_ticks + 1):
        frac = i / n_ticks
        x = margin_l + frac * timeline_w
        try:
            dt = dt_min + (dt_max - dt_min) * frac
            label = dt.strftime('%H:%M')
        except:
            label = ''
        axis_svg += f'<line x1="{x}" y1="{header_h - 20}" x2="{x}" y2="{header_h - 12}" stroke="#30363d" stroke-width="1"/>\n'
        axis_svg += f'<text x="{x}" y="{header_h - 28}" text-anchor="middle" font-size="9" fill="#484f58" font-family="monospace">{label}</text>\n'

    # Marker line for scrubber
    scrub_line_id = 'scrubLine'

    svg = f'''<svg width="{margin_l + timeline_w + margin_r}" height="{svg_h}" xmlns="http://www.w3.org/2000/svg" style="min-width:{margin_l + timeline_w + margin_r}px;background:#0d1117;border-radius:8px">
<style>
.evt{{transition:r .12s,opacity .3s}}
.evt.adim{{opacity:.2}}
</style>
<rect width="100%" height="100%" fill="#0d1117"/>
{axis_svg}
<line x1="{margin_l}" y1="{header_h-12}" x2="{margin_l+timeline_w}" y2="{header_h-12}" stroke="#30363d" stroke-width="1"/>
<line id="{scrub_line_id}" x1="{margin_l}" y1="0" x2="{margin_l}" y2="{svg_h}" stroke="#1f6feb" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.6"/>
{tracks_svg}
</svg>'''

    # Events as JSON
    events_json = json.dumps(events_list)
    bp_json = json.dumps(bp_list)
    t_min_json = json.dumps(t_min)
    t_max_json = json.dumps(t_max)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Agent Lifecycle Timeline</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0d1117;color:#c9d1d9;font-family:'Segoe UI','SF Pro',system-ui,sans-serif;overflow-x:hidden}}
h1{{font-size:1.1rem;font-weight:500;color:#f0f6fc;letter-spacing:.02em}}
.header{{padding:16px 24px;border-bottom:1px solid #30363d;display:flex;align-items:center;gap:16px}}
.header small{{color:#8b949e;font-size:.75rem}}
.controls{{padding:12px 24px;border-bottom:1px solid #21262d;display:flex;align-items:center;gap:12px;flex-wrap:wrap}}
.btn{{background:#21262d;border:1px solid #30363d;color:#c9d1d9;padding:6px 16px;border-radius:6px;cursor:pointer;font-size:.8rem;transition:all .15s}}
.btn:hover{{background:#30363d}}
.btn.active{{background:#1f6feb;border-color:#1f6feb;color:#fff}}
.timeline-wrap{{overflow-x:auto;overflow-y:auto;max-height:calc(100vh - 160px);padding:8px 0}}
.timeline-wrap svg{{display:block;margin:0 auto}}
.tooltip{{display:none;position:fixed;background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px 18px;box-shadow:0 8px 24px rgba(0,0,0,.4);z-index:1000;min-width:220px;font-size:.8rem;line-height:1.5}}
.tooltip.show{{display:block}}
.tooltip h3{{font-size:.85rem;color:#f0f6fc;margin-bottom:8px}}
.tooltip .row{{display:flex;justify-content:space-between;padding:2px 0;color:#8b949e}}
.tooltip .row .val{{color:#c9d1d9;font-weight:500}}
.tooltip .score-big{{font-size:1.5rem;font-weight:700;text-align:center;padding:8px 0 4px}}
.tooltip .action-badge{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:.7rem;font-weight:600;text-transform:uppercase;margin-bottom:6px}}
.legend{{display:flex;gap:16px;align-items:center;font-size:.75rem;color:#8b949e;padding:8px 24px;border-bottom:1px solid #21262d;flex-wrap:wrap}}
.legend-dot{{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:4px}}
.legend-item{{display:flex;align-items:center;gap:4px}}
.stats{{padding:12px 24px;border-bottom:1px solid #21262d;display:flex;gap:20px;font-size:.75rem;color:#8b949e}}
.stats span strong{{color:#c9d1d9;font-weight:500}}
</style>
</head>
<body>

<div class="header">
  <h1>&#9729; Agent Lifecycle Timeline</h1>
  <small>Styde Forge &middot; {len(rows)} events across {len(bp_order)} blueprints</small>
</div>

<div class="legend">
  <span class="legend-item"><span class="legend-dot" style="background:#ffb347"></span> 85+ hot/gold</span>
  <span class="legend-item"><span class="legend-dot" style="background:#d29922"></span> 70-84 amber</span>
  <span class="legend-item"><span class="legend-dot" style="background:#58a6ff"></span> &lt;70 cool</span>
  <span class="legend-item"><span class="legend-dot" style="background:#30363d;border:2px solid #8b949e"></span> no score</span>
  <span style="margin-left:auto;font-size:.7rem;color:#484f58">click any node for detail</span>
</div>

<div class="stats">
  <span>Range: <strong>{t_min[:16]} &rarr; {t_max[:16]}</strong></span>
  <span>Spawns: <strong>{sum(1 for r in rows if r['action']=='spawn')}</strong></span>
  <span>Evals: <strong>{sum(1 for r in rows if r['action']=='eval')}</strong></span>
  <span>Improves: <strong>{sum(1 for r in rows if r['action']=='improve')}</strong></span>
  <span>Scored: <strong>{sum(1 for r in rows if r['score'] is not None)}</strong></span>
</div>

<div class="controls">
  <button class="btn active" id="btnPlay">&#9654; Play</button>
  <button class="btn" id="btnReset">&#8635; Reset</button>
  <span style="color:#8b949e;font-size:.8rem">Scrub:</span>
  <span id="timeDisplay" style="color:#c9d1d9;font-size:.8rem;font-family:monospace;min-width:70px">--:--:--</span>
  <input type="range" id="scrubber" style="flex:1;min-width:150px;max-width:400px;accent-color:#1f6feb" value="100" min="0" max="100">
  <span style="color:#8b949e;font-size:.7rem" id="eventCount">{len(rows)}/{len(rows)}</span>
</div>

<div class="timeline-wrap" id="timelineWrap">
{svg}
</div>

<div class="tooltip" id="tooltip"></div>

<script>
(function() {{
const events = {events_json};
const bpColors = {bp_json};
const tMin = {t_min_json};
const tMax = {t_max_json};

const scrubber = document.getElementById('scrubber');
const timeDisplay = document.getElementById('timeDisplay');
const eventCount = document.getElementById('eventCount');
const btnPlay = document.getElementById('btnPlay');
const btnReset = document.getElementById('btnReset');
const tooltip = document.getElementById('tooltip');
const timelineWrap = document.getElementById('timelineWrap');
const svg = timelineWrap.querySelector('svg');
if (!svg) return;

const scrubLine = document.getElementById('scrubLine');
const allEvents = svg.querySelectorAll('.evt');
let playing = false;
let playTimer = null;

function timestampToMs(ts) {{
  return new Date(ts.replace('Z','+00:00').replace(' ','T')).getTime();
}}

const minMs = timestampToMs(tMin);
const maxMs = timestampToMs(tMax);
const rangeMs = maxMs - minMs || 1;

function clamp(v, lo, hi) {{ return Math.min(hi, Math.max(lo, v)); }}

function setScrub(frac) {{
  frac = clamp(frac, 0, 1);
  scrubber.value = frac * 100;

  // position line
  const svgW = svg.viewBox ? parseFloat(svg.viewBox.baseVal.width) : svg.getBoundingClientRect().width;
  // Find the timeline geometry from the SVG
  // The time axis starts at x=260 and spans 1400px (we hardcode this from generation)
  const marginL = 260;
  const tw = 1400;
  // But we might need to read from the actual svg, let's compute from known coords
  // We'll use the first time-axis tick
  const x = marginL + frac * tw;
  scrubLine.setAttribute('x1', x);
  scrubLine.setAttribute('x2', x);

  // time label
  const ms = minMs + frac * rangeMs;
  const d = new Date(ms);
  timeDisplay.textContent = d.toTimeString().slice(0,8);

  // dim events after the scrub point
  let visible = 0;
  allEvents.forEach(el => {{
    const cx = parseFloat(el.getAttribute('cx'));
    if (cx <= x + 7) {{ el.classList.remove('adim'); visible++; }}
    else {{ el.classList.add('adim'); }}
  }});
  eventCount.textContent = visible + '/' + allEvents.length;
}}

function resetView() {{
  setScrub(1.0);
}}

function play() {{
  if (playing) {{
    playing = false;
    btnPlay.textContent = '\u25b6 Play';
    btnPlay.classList.remove('active');
    if (playTimer) {{ clearInterval(playTimer); playTimer = null; }}
    return;
  }}
  playing = true;
  btnPlay.textContent = '\u23f8 Pause';
  btnPlay.classList.add('active');

  let frac = parseFloat(scrubber.value) / 100;
  const step = 0.003;

  playTimer = setInterval(() => {{
    frac += step;
    if (frac >= 1.0) {{
      frac = 1.0;
      setScrub(frac);
      // stop at end
      playing = false;
      btnPlay.textContent = '\u25b6 Play';
      btnPlay.classList.remove('active');
      clearInterval(playTimer);
      playTimer = null;
      return;
    }}
    setScrub(frac);
  }}, 40);
}}

scrubber.addEventListener('input', function() {{
  const frac = parseFloat(this.value) / 100;
  setScrub(frac);
  if (playing) {{
    playing = false;
    btnPlay.textContent = '\u25b6 Play';
    btnPlay.classList.remove('active');
    if (playTimer) {{ clearInterval(playTimer); playTimer = null; }}
  }}
}});

btnPlay.addEventListener('click', play);
btnReset.addEventListener('click', resetView);

function showDetail(evt, el) {{
  const bp = el.getAttribute('data-bp');
  const action = el.getAttribute('data-action');
  const id = el.getAttribute('data-id');
  const ts = el.getAttribute('data-ts');
  const detail = el.getAttribute('data-detail');
  const score = el.getAttribute('data-score');

  const actionColors = {{spawn:'#238636', eval:'#1f6feb', improve:'#9e6a03'}};
  const ac = actionColors[action] || '#30363d';

  let detailShort = detail;
  if (detail && detail.length > 60) detailShort = detail.slice(0,58) + '...';

  tooltip.innerHTML =
    '<div class="action-badge" style="background:' + ac + '">' + action + ' #' + id + '</div>' +
    '<h3>' + bp.slice(0,40) + '</h3>' +
    '<div class="row"><span>Score</span><span class="val" style="color:' + (parseFloat(score)>=85?'#ffb347':parseFloat(score)>=70?'#d29922':'#58a6ff') + '">' + score + '</span></div>' +
    '<div class="row"><span>Time</span><span class="val">' + ts.slice(0,19).replace('T',' ') + '</span></div>' +
    (detailShort ? '<div class="row" style="margin-top:6px;border-top:1px solid #21262d;padding-top:6px;flex-direction:column;gap:2px"><span style="color:#484f58;font-size:.7rem">Detail</span><span class="val" style="font-size:.73rem;word-break:break-word">' + detailShort + '</span></div>' : '');

  // position
  let tx = evt.clientX + 14;
  let ty = evt.clientY - 10;
  if (tx + 240 > window.innerWidth) tx = evt.clientX - 240;
  if (ty + 200 > window.innerHeight) ty = window.innerHeight - 210;
  if (ty < 10) ty = 10;
  tooltip.style.left = tx + 'px';
  tooltip.style.top = ty + 'px';
  tooltip.classList.add('show');
}}

document.addEventListener('click', function(evt) {{
  if (!evt.target.classList.contains('evt')) {{
    tooltip.classList.remove('show');
  }}
}});

// Init
resetView();
}})();
</script>

</body>
</html>'''

    return html

if __name__ == '__main__':
    rows = parse_state('state.yaml')
    html = generate_html(rows)
    outpath = '99_DASHBOARD/timeline_agent-lifecycle-timeline.html'
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Written {len(html)} bytes to {outpath}')
    print(f'{len(rows)} events, {len(set(r["bp"] for r in rows))} blueprints')
    print(f'Open in browser to view timeline')
