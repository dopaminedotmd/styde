import json
import html as html_mod

with open('E:/Stryde/_alpedal/styde-forge/_timeline_events.json') as f:
    data = json.load(f)

bps = data['bp_order']
events = data['events']
t_min = events[-1]['ts']
t_max = events[0]['ts']

# Count stats
scored = [e for e in events if e['score'] > 0]
gold = sum(1 for e in scored if e['score'] >= 85)
amber = sum(1 for e in scored if 70 <= e['score'] < 85)
cool = sum(1 for e in scored if e['score'] < 70)

def js_str(s):
    return json.dumps(s)

t_min_iso = t_min
t_max_iso = t_max
events_json = json.dumps(events)
bps_json = json.dumps(bps)

html_out = f'''<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Lifecycle Timeline</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0d1117;color:#e6edf3;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;overflow-x:hidden}}
.header{{padding:18px 24px;background:#161b22;border-bottom:1px solid #30363d;display:flex;align-items:center;gap:16px;flex-wrap:wrap}}
.header h1{{font-size:20px;font-weight:600;color:#f0f6fc}}
.header .stats{{display:flex;gap:14px;font-size:12px;color:#8b949e}}
.header .stats span strong{{color:#e6edf3}}
.controls{{display:flex;align-items:center;gap:10px;padding:10px 24px;background:#0d1117;border-bottom:1px solid #21262d;flex-wrap:wrap}}
.controls label{{font-size:11px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px}}
.controls input[type=range]{{width:320px;accent-color:#d29922;cursor:pointer}}
.controls .time-display{{font-size:12px;color:#e6edf3;font-family:monospace;min-width:160px}}
.controls button{{background:#21262d;color:#c9d1d9;border:1px solid #30363d;padding:5px 12px;border-radius:6px;cursor:pointer;font-size:11px;font-weight:500}}
.controls button:hover{{background:#30363d}}
.controls button.active{{background:#1f6feb;border-color:#1f6feb;color:#fff}}
.controls .legend{{display:flex;gap:14px;margin-left:auto;font-size:11px;color:#8b949e}}
.controls .legend .dot{{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px;vertical-align:middle}}
.timeline-container{{padding:16px 24px;overflow-x:auto;max-height:calc(100vh - 140px);overflow-y:auto}}
.timeline-svg{{display:block;margin:0 auto}}
.track-label{{font-size:11px;fill:#e6edf3;font-family:monospace;dominant-baseline:central}}
.track-line{{stroke:#21262d;stroke-width:1}}
.node{{cursor:pointer;transition:r .15s,opacity .15s}}
.node:hover{{filter:brightness(1.4) brightness(1.3)}}
.action-icon{{font-size:9px;fill:#8b949e;font-family:monospace;pointer-events:none;dominant-baseline:central;user-select:none}}
.tick-label{{font-size:9px;fill:#484f58;font-family:monospace;dominant-baseline:central}}
.tick-line{{stroke:#1c2128;stroke-width:0.5}}
#tooltip{{position:fixed;display:none;background:#1c2128;border:1px solid #30363d;border-radius:8px;padding:12px 16px;font-size:12px;z-index:1000;max-width:340px;box-shadow:0 8px 24px rgba(0,0,0,.4)}}
#tooltip .tt-title{{font-weight:600;color:#f0f6fc;margin-bottom:4px;font-size:13px}}
#tooltip .tt-row{{display:flex;justify-content:space-between;gap:12px;padding:2px 0;color:#8b949e}}
#tooltip .tt-row .tt-val{{color:#e6edf3;font-family:monospace}}
#tooltip .tt-score{{font-size:22px;font-weight:700;text-align:center;padding:6px 0}}
.no-data{{text-align:center;padding:60px 20px;color:#484f58;font-size:14px}}
.now-line{{stroke:#f85149;stroke-width:1.5;stroke-dasharray:4,3;pointer-events:none}}
.promotion-marker{{fill:#3fb950;opacity:0.7;pointer-events:none}}
.consecutive-badge{{font-size:8px;fill:#3fb950;font-family:monospace;pointer-events:none;dominant-baseline:central}}
</style>
</head>
<body>
<div class="header">
  <h1>Agent Lifecycle Timeline</h1>
  <div class="stats">
    <span>Blueprint: <strong>{len(bps)}</strong></span>
    <span>Events: <strong>{len(events)}</strong></span>
    <span>Gold: <strong style="color:#d29922">{gold}</strong> Amber: <strong style="color:#d3883e">{amber}</strong> Cool: <strong style="color:#8b949e">{cool}</strong></span>
  </div>
</div>
<div class="controls">
  <label>Tidsreglage</label>
  <input type="range" id="timeSlider" min="0" max="100" value="100" step="1">
  <button id="playBtn">Spela</button>
  <button id="resetBtn">Aterstaell</button>
  <span class="time-display" id="timeDisplay">2026-06-29 20:29 -> 2026-06-30 04:18</span>
  <div class="legend">
    <span><span class="dot" style="background:#d29922"></span>Guld 85+</span>
    <span><span class="dot" style="background:#d3883e"></span>Bärnsten 70-84</span>
    <span><span class="dot" style="background:#8b949e"></span>Kall <70</span>
    <span><span class="dot" style="background:#3fb950"></span>Utbildad</span>
  </div>
</div>
<div class="timeline-container" id="timelineContainer">
  <svg class="timeline-svg" id="timelineSvg"></svg>
</div>
<div id="tooltip"></div>
<script>
var EVENTS = {events_json};
var TOP_BPS = {bps_json};
var T_MIN = {js_str(t_min_iso)};
var T_MAX = {js_str(t_max_iso)};

function timeMs(t){{return t?new Date(t).getTime():0}}
var t0 = timeMs(T_MIN);
var t1 = timeMs(T_MAX);
var rangeMs = t1 - t0 || 1;

function fmtTime(t){{
  var d = new Date(t);
  return d.toLocaleString('sv',{{hour:'2-digit',minute:'2-digit',day:'numeric',month:'short'}});
}}

function fmtShort(t){{
  var d = new Date(t);
  return (d.getHours()+'').padStart(2,'0')+':'+(d.getMinutes()+'').padStart(2,'0');
}}

function color(score){{
  if(score===null||score===undefined||score<0) return '#30363d';
  if(score>=85) return '#d29922';
  if(score>=70) return '#d3883e';
  return '#8b949e';
}}

function opacity(score){{
  if(score===null||score===undefined||score<0) return 0.35;
  if(score>=85) return 1;
  if(score>=70) return 0.85;
  return 0.6;
}}

function actionChar(a){{
  switch(a){{
    case'spawn':return'S';case'eval':return'E';case'improve':return'I';
    default:return'?';
  }}
}}

// Pre-index events per blueprint for O(n) rendering
var BP_EVENTS = {{}};
for(var i=0;i<EVENTS.length;i++){{
  var e = EVENTS[i];
  if(!BP_EVENTS[e.bp]) BP_EVENTS[e.bp] = [];
  BP_EVENTS[e.bp].push(e);
}}

var ROW_PAD = 28;
var LABEL_W = 200;
var ML = LABEL_W + 16;
var MR = 40;
var SVG_PAD = 16;
var playing = false;
var sliderVal = 100;

function build(){{
  var container = document.getElementById('timelineContainer');
  var svg = document.getElementById('timelineSvg');
  var cw = container.clientWidth - 32;
  var aw = cw - ML - MR;
  if(aw<100) aw=100;
  var h = TOP_BPS.length * ROW_PAD + SVG_PAD*2;
  var cl = ML;
  var cr = ML + aw;

  svg.setAttribute('width',cw);
  svg.setAttribute('height',h);
  svg.setAttribute('viewBox','0 0 '+cw+' '+h);

  var ratio = sliderVal/100;
  var cutoffMs = t0 + rangeMs*ratio;
  var html = '';

  // Ticks
  var ticks = 8;
  var step = rangeMs/ticks;
  for(var i=0;i<=ticks;i++){{
    var t = t0 + i*step;
    var x = cl + (t-t0)/rangeMs*aw;
    html += '<line x1="'+x+'" y1="18" x2="'+x+'" y2="'+(h-8)+'" class="tick-line"/>';
    html += '<text x="'+x+'" y="13" class="tick-label" text-anchor="middle">'+fmtShort(new Date(t).toISOString())+'</text>';
  }}

  // Now line
  var nowX = cl + (cutoffMs-t0)/rangeMs*aw;
  html += '<line x1="'+nowX+'" y1="18" x2="'+nowX+'" y2="'+(h-8)+'" class="now-line"/>';

  // Tracks
  for(var b=0;b<TOP_BPS.length;b++){{
    var bp = TOP_BPS[b];
    var y = SVG_PAD + b*ROW_PAD + 12;
    var label = bp.length>27 ? bp.substring(0,25)+'..' : bp;

    html += '<text x="8" y="'+y+'" class="track-label">'+label+'</text>';
    html += '<line x1="'+cl+'" y1="'+y+'" x2="'+cr+'" y2="'+y+'" class="track-line"/>';

    var bpEvents = BP_EVENTS[bp];
    if(!bpEvents) continue;

    // Track consecutive promotions (3+ scores >=85)
    var consCount = 0;
    for(var ei=0;ei<bpEvents.length;ei++){{
      var e = bpEvents[ei];
      if(e.action !== 'eval') continue;
      if(e.score >= 85) consCount++; else consCount=0;
      if(consCount >= 3) break;
    }}
    if(consCount >= 3){{
      var pmX = cr + 6;
      html += '<circle cx="'+pmX+'" cy="'+y+'" r="5" class="promotion-marker"/>';
      html += '<text x="'+(pmX+8)+'" y="'+y+'" class="consecutive-badge">P</text>';
    }}

    for(var ei=0;ei<bpEvents.length;ei++){{
      var e = bpEvents[ei];
      var tMs = timeMs(e.ts);
      if(tMs > cutoffMs) continue;

      var x = cl + (tMs-t0)/rangeMs*aw;
      var col = color(e.score);
      var op = opacity(e.score);
      var r = (e.score>0) ? 7 : 4.5;
      var det = (e.detail||'').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
      var scDisplay = (e.score>0) ? e.score : 'N/A';

      html += '<circle cx="'+x+'" cy="'+y+'" r="'+r+'" fill="'+col+'" opacity="'+op+'" class="node"';
      html += ' data-bp="'+bp+'" data-action="'+e.action+'" data-detail="'+det+'"';
      html += ' data-score="'+scDisplay+'" data-ts="'+e.ts+'" data-id="'+e.id+'"';
      html += ' onmouseenter="showTip(event,this)" onmouseleave="hideTip()" onclick="showTip(event,this)"/>';

      if(e.score<=0 || e.score===null){{
        html += '<text x="'+x+'" y="'+(y+1)+'" class="action-icon" text-anchor="middle">'+actionChar(e.action)+'</text>';
      }}
    }}
  }}

  svg.innerHTML = html;
}}

function showTip(ev,el){{
  var tip = document.getElementById('tooltip');
  var bp = el.getAttribute('data-bp');
  var action = el.getAttribute('data-action');
  var detail = el.getAttribute('data-detail');
  var score = el.getAttribute('data-score');
  var ts = el.getAttribute('data-ts');
  var id = el.getAttribute('data-id');

  var sc = '';
  if(score!=='N/A'){{
    var sv = parseFloat(score);
    if(sv>=85) sc = 'color:#d29922';
    else if(sv>=70) sc = 'color:#d3883e';
    else sc = 'color:#8b949e';
  }}
  var sHtml = '';
  if(score!=='N/A') sHtml = '<div class="tt-score" style="'+sc+'">'+score+'</div>';

  tip.style.display = 'block';
  tip.innerHTML = '<div class="tt-title">'+bp+'</div>'+sHtml+
    '<div class="tt-row"><span>Action</span><span class="tt-val">'+action.toUpperCase()+'</span></div>'+
    '<div class="tt-row"><span>Event ID</span><span class="tt-val">#'+id+'</span></div>'+
    '<div class="tt-row"><span>Time</span><span class="tt-val">'+fmtTime(ts)+'</span></div>'+
    '<div class="tt-row"><span>Detail</span><span class="tt-val">'+detail+'</span></div>';

  var x = ev.clientX+14, y = ev.clientY+6;
  var r = tip.getBoundingClientRect();
  if(x+r.width > window.innerWidth) x = ev.clientX-r.width-14;
  if(y+r.height > window.innerHeight) y = ev.clientY-r.height-6;
  tip.style.left = x+'px';
  tip.style.top = y+'px';
}}

function hideTip(){{ document.getElementById('tooltip').style.display='none' }}

function updateSlider(val){{
  sliderVal = parseInt(val);
  document.getElementById('timeSlider').value = sliderVal;
  var t = new Date(t0 + rangeMs*(sliderVal/100));
  document.getElementById('timeDisplay').textContent = fmtShort(T_MIN)+' -> '+fmtShort(t.toISOString());
  build();
}}

function togglePlay(){{
  playing = !playing;
  document.getElementById('playBtn').textContent = playing ? 'Pausa' : 'Spela';
  document.getElementById('playBtn').classList.toggle('active',playing);
  if(playing){{
    (function step(){{
      if(!playing) return;
      var v = parseInt(document.getElementById('timeSlider').value);
      v += 1;
      if(v>100){{ v=100; playing=false; document.getElementById('playBtn').textContent='Spela'; document.getElementById('playBtn').classList.remove('active'); }}
      updateSlider(v);
      if(playing) setTimeout(step,70);
    }})();
  }}
}}

function resetFn(){{
  playing = false;
  document.getElementById('playBtn').textContent = 'Spela';
  document.getElementById('playBtn').classList.remove('active');
  updateSlider(100);
}}

function keyNav(e){{
  if(e.key==='ArrowRight'){{ var v=parseInt(document.getElementById('timeSlider').value)+3; if(v>100)v=100; updateSlider(v); }}
  if(e.key==='ArrowLeft'){{ var v=parseInt(document.getElementById('timeSlider').value)-3; if(v<0)v=0; updateSlider(v); }}
  if(e.key===' '||e.key==='Space'){{ e.preventDefault(); togglePlay(); }}
}}

document.addEventListener('DOMContentLoaded',function(){{
  document.getElementById('timeSlider').addEventListener('input',function(e){{ updateSlider(e.target.value) }});
  document.getElementById('playBtn').addEventListener('click',togglePlay);
  document.getElementById('resetBtn').addEventListener('click',resetFn);
  document.addEventListener('keydown',keyNav);
  updateSlider(100);
}});
window.addEventListener('resize',build);
</script>
</body>
</html>'''

with open('E:/Stryde/_alpedal/styde-forge/agent_lifecycle_timeline.html', 'w', encoding='utf-8') as f:
    f.write(html_out)

print(f'Written {len(html_out)} bytes to agent_lifecycle_timeline.html')
print(f'Stats: {len(bps)} blueprints, {len(events)} events, {gold} gold, {amber} amber, {cool} cool')
