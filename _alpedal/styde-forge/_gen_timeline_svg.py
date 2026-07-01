import json, html, sys
from datetime import datetime

with open('_timeline_events.json') as f:
    data = json.load(f)

events = data['events']
bp_order = data['bp_order']
bp_y = data['bp_y']

ts_all = sorted(set(e['ts'] for e in events if 'ts' in e))
t_start, t_end = ts_all[0], ts_all[-1]

def to_mins(ts):
    d = datetime.fromisoformat(ts.replace('Z','+00:00'))
    base = datetime.fromisoformat(t_start.replace('Z','+00:00'))
    return (d - base).total_seconds() / 60.0

total_min = to_mins(t_end) or 1

def sc(s):
    if s >= 85: return '#FFD700'
    if s >= 70: return '#FF8C00'
    return '#4A90D9'

rows = len(bp_order)
ml, mr, mt, mb = 200, 40, 50, 100
pw, ph = 1000, rows * 30 + 10
sw, sh = ml + pw + mr, mt + ph + mb

out = []
def L(s): out.append(s)

L('<?xml version="1.0" encoding="UTF-8"?>')
L(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {sw} {sh}" style="background:#1a1a2e;font-family:monospace">')
L('<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#16213e"/><stop offset="100%" stop-color="#1a1a2e"/></linearGradient></defs>')
L(f'<rect width="{sw}" height="{sh}" fill="url(#bg)"/>')
L(f'<text x="{ml+pw//2}" y="25" fill="#e0e0e0" font-size="16" text-anchor="middle" font-weight="bold">AGENT LIFECYCLE TIMELINE</text>')
L(f'<text x="{ml+pw//2}" y="42" fill="#888" font-size="11" text-anchor="middle">{t_start[:10]} to {t_end[:10]} | {len(events)} events across {len(bp_order)} blueprints</text>')

# tracks and labels
for i, bp in enumerate(bp_order):
    y = mt + i * 30 + 15
    label = bp[:28] + '..' if len(bp) > 30 else bp
    L(f'<text x="{ml-8}" y="{y}" fill="#aaa" font-size="10" text-anchor="end">{html.escape(label)}</text>')
    L(f'<line x1="{ml}" y1="{y}" x2="{ml+pw}" y2="{y}" stroke="#2a2a4e" stroke-width="1"/>')

# time grid lines
for h in range(0, int(total_min) + 10, 30):
    if h > total_min: break
    x = ml + (h / total_min) * pw
    L(f'<line x1="{x}" y1="{mt}" x2="{x}" y2="{mt+ph}" stroke="#2a2a4e" stroke-width="0.5" stroke-dasharray="2,3"/>')

# group events by bp
nodes = {}
for e in events:
    bp = e['bp']
    if bp not in nodes: nodes[bp] = []
    nodes[bp].append(e)

# draw nodes
for bp in bp_order:
    evts = nodes.get(bp, [])
    evts.sort(key=lambda x: x['ts'])
    y = mt + bp_y[bp] * 30 + 15
    for e in evts:
        x = ml + (to_mins(e['ts']) / total_min) * pw
        s = e.get('score', -1)
        r = 6 if e.get('action') == 'eval' else (5 if e.get('action') == 'improve' else 4 if e.get('action') == 'spawn' else 8)
        col = sc(s) if s >= 0 else '#666'
        op = 0.4 if e.get('status') == 'running' else 0.9
        meta = f'BP:{html.escape(bp)}|ID:{e["id"]}|{e.get("action","")}|Score:{s:.1f}|{e.get("status","")}'
        if e.get('detail'):
            meta += f'|{html.escape(e["detail"][:60])}'
        L(f'<circle cx="{x:.1f}" cy="{y}" r="{r}" fill="{col}" opacity="{op}" stroke="#fff" stroke-width="0.5" data-tip="{meta}" onmouseover="showTip(evt,this)" onmouseout="hideTip()" style="cursor:pointer"/>')

# legend
lx, ly = ml, mt + ph + 15
items = [('#FFD700','Score 85+'),('#FF8C00','Score 70-84'),('#4A90D9','Score <70'),('#666','No score')]
for col, label in items:
    L(f'<circle cx="{lx}" cy="{ly}" r="6" fill="{col}" stroke="#fff" stroke-width="0.5"/>')
    L(f'<text x="{lx+12}" y="{ly+4}" fill="#aaa" font-size="10">{label}</text>')
    lx += 115
# running
L(f'<circle cx="{lx}" cy="{ly}" r="6" fill="#666" opacity="0.4" stroke="#fff" stroke-width="0.5"/>')
L(f'<text x="{lx+12}" y="{ly+4}" fill="#aaa" font-size="10">Running</text>')

# time slider
sly = mt + ph + 50
L(f'<text x="{ml}" y="{sly-8}" fill="#888" font-size="9">Scrub:</text>')
L(f'<line x1="{ml}" y1="{sly}" x2="{ml+pw}" y2="{sly}" stroke="#444" stroke-width="2"/>')
L(f'<circle id="scrubber" cx="{ml}" cy="{sly}" r="7" fill="#e94560" stroke="#fff" stroke-width="1.5" style="cursor:ew-resize"/>')
L(f'<text id="ts_label" x="{ml}" y="{sly+20}" fill="#888" font-size="9">{t_start[:16]}</text>')
L(f'<rect id="playBtn" x="{ml+pw-60}" y="{sly-15}" width="50" height="22" rx="4" fill="#e94560" style="cursor:pointer" onclick="togglePlay()"/>')
L(f'<text x="{ml+pw-35}" y="{sly+1}" fill="#fff" font-size="11" text-anchor="middle" style="pointer-events:none">PLAY</text>')

# tooltip foreignObject
L(f'<foreignObject id="tooltip" x="0" y="0" width="400" height="120" style="display:none"><div xmlns="http://www.w3.org/1999/xhtml" style="background:#0f3460;color:#e0e0e0;padding:8px;border:1px solid #e94560;border-radius:4px;font-size:11px;font-family:monospace;white-space:pre"></div></foreignObject>')

# JS
L('<script type="text/javascript"><![CDATA[')
L(f'var ml={ml},pw={pw};')
L('var scr=document.getElementById("scrubber");')
L('var tsl=document.getElementById("ts_label");')
L('var tl=document.getElementById("tooltip");')
L('var pb=document.getElementById("playBtn");')
L('var playing=false,animId=null;')
L('var svgEl=document.querySelector("svg");')
L('function showTip(evt,el){')
L('  var tip=el.getAttribute("data-tip");')
L('  if(!tip)return;')
L('  var parts=tip.split("|");')
L("  tl.innerHTML='<div xmlns=\"http://www.w3.org/1999/xhtml\" style=\"background:#0f3460;color:#e0e0e0;padding:10px;border:1px solid #e94560;border-radius:4px;font-size:12px;font-family:monospace;white-space:pre;line-height:1.5\">'+parts.join('<br/>')+'</div>';")
L('  tl.style.display="block";')
L('  var cx=parseFloat(el.getAttribute("cx"))+20;')
L('  var cy=parseFloat(el.getAttribute("cy"))+20;')
L('  tl.setAttribute("x",Math.min(cx,svgEl.clientWidth-410));')
L('  tl.setAttribute("y",Math.min(cy,svgEl.clientHeight-130));')
L('}')
L('function hideTip(){tl.style.display="none";}')
L('function updateScrub(x){')
L(f'  x=Math.max(ml,Math.min(x,ml+pw));')
L('  scr.setAttribute("cx",x);')
L('  var p=(x-ml)/pw;')
L('  var all=document.querySelectorAll("circle[data-tip]");')
L('  all.forEach(function(c){')
L('    var cx=parseFloat(c.getAttribute("cx"));')
L('    c.style.display=cx<=x?"":"none";')
L('  });')
L('}')
L('scr.addEventListener("mousedown",function(e){e.preventDefault();function mv(ev){updateScrub(ev.clientX);}function up(){document.removeEventListener("mousemove",mv);document.removeEventListener("mouseup",up);}document.addEventListener("mousemove",mv);document.addEventListener("mouseup",up);});')
L('function togglePlay(){')
L('  playing=!playing;')
L('  pb.textContent=playing?"STOP":"PLAY";')
L('  if(playing){')
L('    var startX=parseFloat(scr.getAttribute("cx"));')
L(f'    var endX=ml+pw;')
L('    var dur=15000;')
L('    var t0=null;')
L('    function step(ts){')
L('      if(!t0)t0=ts;')
L('      var frac=Math.min((ts-t0)/dur,1);')
L('      var x=startX+(endX-startX)*frac;')
L('      scr.setAttribute("cx",x);')
L('      updateScrub(x);')
L('      if(frac<1)animId=requestAnimationFrame(step);')
L('      else togglePlay();')
L('    }')
L('    animId=requestAnimationFrame(step);')
L('  }else{if(animId)cancelAnimationFrame(animId);}')
L('}')
L(']]></script>')
L('</svg>')

sys.stdout.write('\n'.join(out))
