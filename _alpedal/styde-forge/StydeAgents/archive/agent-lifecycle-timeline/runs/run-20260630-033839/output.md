Agent Lifecycle Timeline v8 -- complete solution
Solution: Python script som laser state.yaml dynamiskt och genererar en standalone HTML med ALLA livscykelfaser inbäddade. Ingen hardcoding.
```python
#!/usr/bin/env python3
"""
_forge_timeline_v8.py  --  Agent Lifecycle Timeline builder
Las state.yaml dynamiskt, extrahera spawn/eval/improve/promote/archive,
generera standalone HTML med SVG-timeline, time scrubber, click-detail.
"""
import json, re, os, sys
from datetime import datetime
STATE_YAML = 'state.yaml'
OUT_HTML = 'agent_lifecycle_timeline_v8.html'
def parse_state_yaml(path):
    events = []
    current = None
    key_order = ['action','blueprint','detail','id','progress','status','timestamp']
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n\r')
            if line.startswith('- '):
                if current:
                    events.append(current)
                current = {}
                rest = line[2:]
                if ': ' in rest:
                    k, v = rest.split(': ', 1)
                    current[k.strip()] = v.strip()
            elif line.startswith('  ') and current is not None:
                rest = line.strip()
                if ': ' in rest:
                    k, v = rest.split(': ', 1)
                    current[k.strip()] = v.strip()
        if current:
            events.append(current)
    return events
def extract_score(detail):
    # Detail format: "S:82 J:92 C:88.0" or "iter 1/5" or "1949 chars"
    if not detail:
        return None
    m = re.search(r'C:(\d+(?:\.\d+)?)', detail)
    if m:
        return round(float(m.group(1)), 1)
    # Fallback: try to extract any number from score-like pattern
    m = re.search(r'(\d+\.?\d*)', detail)
    if m:
        val = float(m.group(1))
        if 0 <= val <= 100:
            return val
    return None
def parse_timestamp(ts):
    if not ts:
        return None
    try:
        return datetime.strptime(ts.replace('Z',''), '%Y-%m-%dT%H:%M:%S')
    except:
        try:
            return datetime.strptime(ts.replace('Z',''), '%Y-%m-%dT%H:%M:%S.%f')
        except:
            return None
def build_events(events):
    out = []
    for ev in events:
        action = ev.get('action','')
        blueprint = ev.get('blueprint','')
        detail = ev.get('detail','')
        eid = ev.get('id','')
        ts_str = ev.get('timestamp','')
        status = ev.get('status','')
        progress = ev.get('progress','')
        dt = parse_timestamp(ts_str)
        if not dt or not blueprint:
            continue
        score = extract_score(detail)
        out.append({
            'bp': blueprint,
            'ts': dt.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'ts_ms': int(dt.timestamp() * 1000),
            'action': action,
            'detail': detail,
            'id': str(eid),
            'score': score,
            'status': status,
            'progress': progress,
        })
    out.sort(key=lambda x: x['ts_ms'])
    return out
def build_html(events_data):
    bps = {}
    for e in events_data:
        bp = e['bp']
        if bp not in bps:
            bps[bp] = []
        bps[bp].append(e)
    bp_names = sorted(bps.keys(), key=lambda n: max((e['ts_ms'] for e in bps[n]), default=0))
    all_events_json = json.dumps(events_data, separators=(',',':'))
    bp_list_json = json.dumps(bp_names, separators=(',',':'))
    t_min = min(e['ts_ms'] for e in events_data) if events_data else 0
    t_max = max(e['ts_ms'] for e in events_data) if events_data else 0
    total_events = len(events_data)
    total_bps = len(bp_names)
    gold = sum(1 for e in events_data if e['score'] is not None and e['score'] >= 85)
    amber = sum(1 for e in events_data if e['score'] is not None and 70 <= e['score'] < 85)
    cool = sum(1 for e in events_data if e['score'] is not None and e['score'] < 70)
    html = f'''<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Agent Lifecycle Timeline v8 - Styde Forge</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#0d1117;color:#c9d1d9;overflow-x:hidden}}
.header{{padding:18px 24px 10px;background:#161b22;border-bottom:1px solid #30363d;display:flex;align-items:center;gap:18px;flex-wrap:wrap}}
.header h1{{font-size:18px;font-weight:600;color:#f0f6fc}}
.header .src{{font-size:10px;color:#484f58;font-family:monospace}}
.stats{{display:flex;gap:12px;font-size:11px;color:#8b949e;flex-wrap:wrap}}
.stats span strong{{color:#e6edf3}}
.legend{{display:flex;gap:10px;padding:6px 24px;background:#0d1117;border-bottom:1px solid #21262d;font-size:10px;align-items:center;flex-wrap:wrap}}
.legend-item{{display:flex;align-items:center;gap:4px;color:#8b949e}}
.legend-dot{{width:8px;height:8px;border-radius:50%;display:inline-block}}
.icon-s{{display:inline-block;width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:7px solid #238636;vertical-align:middle}}
.icon-i{{display:inline-block;width:7px;height:7px;background:#58a6ff;transform:rotate(45deg);vertical-align:middle}}
.icon-p{{font-size:11px;color:#da3633;vertical-align:middle}}
.icon-a{{display:inline-block;width:6px;height:6px;background:#484f58;vertical-align:middle}}
.controls{{display:flex;align-items:center;gap:10px;padding:8px 24px;background:#0d1117;border-bottom:1px solid #21262d;flex-wrap:wrap}}
.controls label{{font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:.4px}}
.controls input[type=range]{{flex:1;min-width:140px;max-width:500px;accent-color:#d29922;cursor:pointer}}
.controls .tdisp{{font-size:11px;color:#e6edf3;min-width:150px;font-family:monospace}}
.btn{{padding:4px 12px;border:1px solid #30363d;border-radius:5px;background:#21262d;color:#c9d1d9;font-size:10px;cursor:pointer;font-weight:500}}
.btn:hover{{background:#30363d}}
.btn.active{{background:#d29922;color:#0d1117;border-color:#d29922;font-weight:600}}
.btn-group{{display:flex;gap:3px}}
select{{background:#21262d;color:#c9d1d9;border:1px solid #30363d;border-radius:4px;padding:3px 6px;font-size:10px;max-width:240px}}
.timeline-container{{overflow:auto;max-height:calc(100vh - 175px);padding:4px 20px 20px}}
.timeline-svg{{min-width:100%;display:block}}
.node{{cursor:pointer;transition:opacity .15s,transform .1s}}
.node:hover{{filter:brightness(1.5)}}
.node.dimmed{{opacity:.08 !important}}
.track-bg{{fill:#161b22;rx:4}}
.track-bg.alt{{fill:#0d1117}}
.track-label{{font-size:9px;fill:#c9d1d9;font-family:monospace;dominant-baseline:middle}}
.axis-text{{font-size:8px;fill:#484f58;font-family:monospace;dominant-baseline:middle}}
.grid-line{{stroke:#1c2128;stroke-width:.5}}
.now-line{{stroke:#d29922;stroke-width:1;stroke-dasharray:3,3;opacity:.5;pointer-events:none}}
#popup{{display:none;position:fixed;background:#1c2128;border:1px solid #30363d;border-radius:8px;padding:12px 16px;z-index:1000;box-shadow:0 8px 32px rgba(0,0,0,.5);min-width:240px;max-width:360px;font-size:11px}}
#popup h3{{font-size:12px;color:#f0f6fc;margin-bottom:5px}}
#popup .pr{{display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid #21262d}}
#popup .pr:last-child{{border:none}}
#popup .pl{{color:#8b949e}}
#popup .pv{{color:#e6edf3;font-family:monospace;font-size:10px}}
#popup .close{{float:right;cursor:pointer;color:#8b949e;font-size:14px;background:none;border:none;line-height:1}}
#popup .close:hover{{color:#f0f6fc}}
#popup .big-score{{font-size:20px;font-weight:700;text-align:center;padding:4px 0}}
footer{{font-size:9px;color:#484f58;text-align:right;padding:2px 20px;border-top:1px solid #21262d}}
</style>
</head>
<body>
<div class=header>
<h1>Agent Lifecycle Timeline</h1>
<span class=src>state.yaml</span>
<div class=stats>
<span>Blueprints: <strong>{total_bps}</strong></span>
<span>Events: <strong>{total_events}</strong></span>
<span style="color:#d29922">Gold <strong>{gold}</strong></span>
<span style="color:#bb8d1e">Amber <strong>{amber}</strong></span>
<span style="color:#58a6ff">Cool <strong>{cool}</strong></span>
</div>
</div>
<div class=legend>
<span class=legend-item><span class=legend-dot style="background:#d29922"></span> 85+ gold</span>
<span class=legend-item><span class=legend-dot style="background:#bb8d1e;opacity:.7"></span> 70-84 amber</span>
<span class=legend-item><span class=legend-dot style="background:#58a6ff;opacity:.5"></span> &lt;70 cool</span>
<span style="width:1px;height:12px;background:#30363d;margin:0 4px"></span>
<span class=legend-item><span class=icon-s></span> spawn</span>
<span class=legend-item><span class=icon-i></span> improve</span>
<span class=legend-item><span class=icon-p>&#9733;</span> promote</span>
<span class=legend-item><span class=icon-a></span> archive</span>
<span class=legend-item><span class=legend-dot style="background:#484f58"></span> eval</span>
</div>
<div class=controls>
<label>scrub</label>
<input type=range id=scrubber min=0 max=1000 value=1000 step=1>
<span class=tdisp id=timeDisplay></span>
<div class=btn-group>
<button class=btn id=playBtn>play</button>
<button class=btn id=resetBtn>reset</button>
</div>
<label style=margin-left:12px>bp</label>
<select id=bpFilter><option value=all>all blueprints</option></select>
<label>stage</label>
<select id=stageFilter>
<option value=all>all</option>
<option value=spawn>spawn</option>
<option value=eval>eval</option>
<option value=improve>improve</option>
<option value=promote>promote</option>
<option value=archive>archive</option>
</select>
</div>
<div class=timeline-container id=timelineContainer><svg class=timeline-svg id=timelineSvg></svg></div>
<div id=popup><button class=close id=popupClose>&times;</button><h3 id=popupTitle></h3><div id=popupBody></div></div>
<footer>source: state.yaml &middot; {total_events} events across {total_bps} blueprints</footer>
<script>
var EVENTS = {all_events_json};
var BP_NAMES = {bp_list_json};
var T_MIN = {t_min};
var T_MAX = {t_max};
var RANGE = T_MAX - T_MIN;
function fmtDate(ms){{
    var d=new Date(ms);
    return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')+' '+String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0');
}}
function fmtShort(ms){{
    var d=new Date(ms);
    return String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0');
}}
function getColor(sc){{
    if(sc===null||sc===undefined)return '#484f58';
    if(sc>=85)return '#d29922';
    if(sc>=70)return '#bb8d1e';
    return '#58a6ff';
}}
function getOpac(sc,act){{
    if(act==='spawn')return.45;
    if(act==='improve')return.4;
    if(act==='promote')return.85;
    if(act==='archive')return.3;
    if(sc===null||sc===undefined)return.35;
    if(sc>=85)return 1;
    if(sc>=70)return.7;
    return.5;
}}
function getRadius(sc,act){{
    if(act==='spawn')return 4;
    if(act==='improve')return 3.5;
    if(act==='promote')return 5;
    if(act==='archive')return 2.5;
    if(sc===null||sc===undefined)return 4;
    return Math.max(3.5,Math.min(8,sc/13));
}}
var bps={{}};
EVENTS.forEach(function(e){{
    if(!bps[e.bp])bps[e.bp]=[];
    bps[e.bp].push(e);
}});
var bpOrder=BP_NAMES;
var curScrub=1000,isPlaying=false,playInt=null;
function render(){{
    var sv=parseInt(document.getElementById('scrubber').value);
    var cutMs=T_MIN+RANGE*(sv/1000);
    var bpf=document.getElementById('bpFilter').value;
    var sf=document.getElementById('stageFilter').value;
    var vis=bpf==='all'?bpOrder:[bpf];
    if(sf!=='all')vis=vis.filter(function(n){{
        for(var i=0;i<(bps[n]||[]).length;i++)if(bps[n][i].action===sf)return true;
        return false;
    }});
    var n=vis.length,ML=180,MT=20,TH=22,TG=2,PAD=40;
    var th=MT+n*(TH+TG)+22;
    var tw=Math.max(ML+1200,1200);
    var pl=ML,pr=tw-PAD,pw=pr-pl;
    var s='<svg class=timeline-svg width='+tw+' height='+th+' viewBox="0 0 '+tw+' '+th+'"><rect width='+tw+' height='+th+' fill=#0d1117/>';
    var ni=Math.max(6,Math.round(pw/160));
    for(var i=0;i<=ni;i++){{
        var t=T_MIN+(RANGE*i/ni);
        var x=pl+(t-T_MIN)/RANGE*pw;
        s+='<line class=grid-line x1='+x+' y1='+(MT-4)+' x2='+x+' y2='+(th-8)+'/>';
        s+='<text class=axis-text x='+x+' y='+(MT-6)+' text-anchor=middle font-size=7>'+fmtShort(t)+'</text>';
    }}
    s+='<text class=axis-text x='+pl+' y='+(MT-6)+' text-anchor=start font-size=7>'+fmtDate(T_MIN).slice(0,10)+'</text>';
    s+='<text class=axis-text x='+pr+' y='+(MT-6)+' text-anchor=end font-size=7>'+fmtDate(T_MAX).slice(0,10)+'</text>';
    var sx=pl+(cutMs-T_MIN)/RANGE*pw;
    s+='<line class=now-line x1='+sx+' y1='+MT+' x2='+sx+' y2='+(th-8)+'/>';
    for(var i=0;i<n;i++){{
        var bp=vis[i],y0=MT+i*(TH+TG);
        var evts=(bps[bp]||[]).slice().sort(function(a,b){{return a.ts_ms-b.ts_ms;}});
        var alt=i%2===0?'#0d1117':'#161b22';
        s+='<rect x='+(pl-4)+' y='+y0+' width='+(pw+8)+' height='+TH+' fill='+alt+' class=track-bg rx=3/>';
        var lb=bp.length>28?bp.slice(0,25)+'...':bp;
        s+='<text class=track-label x='+(ML-8)+' y='+(y0+TH/2)+' text-anchor=end font-size=9>'+lb+'</text>';
        var visEvts=[];
        for(var e=0;e<evts.length;e++)if(evts[e].ts_ms<=cutMs)visEvts.push(evts[e]);
        if(visEvts.length>=2){{
            var pd='';
            for(var j=0;j<visEvts.length;j++){{
                var lx=pl+(visEvts[j].ts_ms-T_MIN)/RANGE*pw;
                pd+=(j===0?'M':'L')+lx+','+(y0+TH/2);
            }}
            s+='<path d='+pd+' stroke=#30363d stroke-width=.5 fill=none opacity=.25/>';
        }}
        for(var e=0;e<visEvts.length;e++){{
            var a=visEvts[e],x=pl+(a.ts_ms-T_MIN)/RANGE*pw,y=y0+TH/2;
            var r=getRadius(a.score,a.action);
            var c=getColor(a.score);
            var o=getOpac(a.score,a.action);
            var esc=a.bp.replace(/'/g,"\\\\'");
            var oc='onclick="showPopup(this,\\\''+esc+'\\\','+a.ts_ms+','+(a.score||'null')+',\\\''+a.action+'\\\',\\\''+(a.id||'')+'\\\',\\\''+(a.detail||'').replace(/'/g,"\\\\'")+'\\\')"';
            var hv='onmouseover="dim(\\\''+esc+'\\\')" onmouseout="undim()"';
            if(a.action==='spawn'){{
                var pts=(x)+','+(y-4)+' '+(x-4)+','+(y+4)+' '+(x+4)+','+(y+4);
                s+='<polygon class=node points='+pts+' fill=#238636 opacity='+o+' '+oc+' '+hv+'/>';
            }}else if(a.action==='improve'){{
                var pts=(x)+','+(y-3.5)+' '+(x+3.5)+','+y+' '+(x)+','+(y+3.5)+' '+(x-3.5)+','+y;
                s+='<polygon class=node points='+pts+' fill=#58a6ff opacity='+o+' '+oc+' '+hv+'/>';
            }}else if(a.action==='promote'){{
                s+='<circle class=node cx='+x+' cy='+y+' r='+r+' fill=#da3633 opacity='+o+' stroke=#ff7b72 stroke-width=1 '+oc+' '+hv+'/>';
                s+='<text x='+x+' y='+(y+1)+' text-anchor=middle fill=#fff font-size=8 font-weight=700 pointer-events=none opacity='+o+'>★</text>';
            }}else if(a.action==='archive'){{
                s+='<rect class=node x='+(x-2.5)+' y='+(y-2.5)+' width=5 height=5 fill=#484f58 opacity='+o+' rx=1 '+oc+' '+hv+'/>';
            }}else{{
                var fc=a.score!==null?c:'#484f58';
                s+='<circle class=node cx='+x+' cy='+y+' r='+r+' fill='+fc+' opacity='+o+' filter=url(#sh) '+oc+' '+hv+'/>';
                if(a.score!==null&&a.score>=80){{
                    s+='<text x='+x+' y='+(y+r+8)+' text-anchor=middle fill='+c+' font-size=6 font-family=monospace opacity='+o+'>'+Math.round(a.score)+'</text>';
                }}
            }}
        }}
    }}
    s+='<defs><filter id=sh><feDropShadow dx=0 dy=1 stdDeviation=1 flood-opacity=.15/></filter></defs>';
    s+='</svg>';
    document.getElementById('timelineSvg').innerHTML=s;
    document.getElementById('timeDisplay').textContent=fmtDate(cutMs);
}}
function showPopup(el,bp,ts,score,action,id,detail){{
    var popup=document.getElementById('popup');
    document.getElementById('popupTitle').textContent=bp;
    var rows=[
        ['Action',action],
        ['Run ID',id||'-'],
        ['Timestamp',fmtDate(ts)],
    ];
    if(score!==null&&score!==undefined)rows.push(['Score',score]);
    if(detail)rows.push(['Detail',detail]);
    var h='';
    if(score!==null&&score!==undefined&&score>=0){{
        var sc=Math.round(score);
        var col=sc>=85?'#d29922':sc>=70?'#bb8d1e':'#58a6ff';
        h+='<div class=big-score style=color:'+col+'>'+sc+'</div>';
    }}
    for(var i=0;i<rows.length;i++){{
        h+='<div class=pr><span class=pl>'+rows[i][0]+'</span><span class=pv>'+rows[i][1]+'</span></div>';
    }}
    document.getElementById('popupBody').innerHTML=h;
    popup.style.display='block';
    var r=el.getBoundingClientRect(),l=r.right+12,t=r.top-10;
    if(l+360>window.innerWidth)l=r.left-280;
    if(t+260>window.innerHeight)t=window.innerHeight-270;
    if(t<10)t=10;
    popup.style.left=l+'px';popup.style.top=t+'px';
}}
function dim(bp){{
    var ns=document.querySelectorAll('.node');
    for(var i=0;i<ns.length;i++){{
        var n=ns[i];n.classList.toggle('dimmed',n.getAttribute('data-bp')!==bp&&n.getAttribute('data-bp2')!==bp);
    }}
}}
function undim(){{
    var ns=document.querySelectorAll('.node');
    for(var i=0;i<ns.length;i++)ns[i].classList.remove('dimmed');
}}
function popFilter(){{
    var sel=document.getElementById('bpFilter');
    for(var b=0;b<bpOrder.length;b++){{
        var bp=bpOrder[b],evts=bps[bp]||[],ec=0,best=0,worst=100;
        for(var i=0;i<evts.length;i++){{if(evts[i].score!==null){{ec++;if(evts[i].score>best)best=evts[i].score;if(evts[i].score<worst)worst=evts[i].score;}}}}
        var opt=document.createElement('option');
        opt.value=bp;opt.textContent=bp+' ('+ec+' sc, '+best+'/'+(worst<100?worst:'-')+')';
        sel.appendChild(opt);
    }}
}}
document.getElementById('scrubber').addEventListener('input',function(){{curScrub=parseInt(this.value);render();}});
document.getElementById('playBtn').addEventListener('click',function(){{
    isPlaying=!isPlaying;this.textContent=isPlaying?'pause':'play';this.classList.toggle('active',isPlaying);
    if(isPlaying){{
        if(curScrub>=1000){{curScrub=0;document.getElementById('scrubber').value=0;}}
        playInt=setInterval(function(){{
            curScrub+=4;if(curScrub>1000){{curScrub=1000;document.getElementById('playBtn').textContent='play';document.getElementById('playBtn').classList.remove('active');clearInterval(playInt);isPlaying=false;}}
            document.getElementById('scrubber').value=curScrub;render();
        }},60);
    }}else clearInterval(playInt);
}});
document.getElementById('resetBtn').addEventListener('click',function(){{
    if(isPlaying){{clearInterval(playInt);isPlaying=false;document.getElementById('playBtn').textContent='play';document.getElementById('playBtn').classList.remove('active');}}
    curScrub=1000;document.getElementById('scrubber').value=1000;render();
}});
document.getElementById('bpFilter').addEventListener('change',render);
document.getElementById('stageFilter').addEventListener('change',render);
document.getElementById('popupClose').addEventListener('click',function(){{document.getElementById('popup').style.display='none';}});
document.addEventListener('click',function(e){{if(!e.target.closest('.node')&&!e.target.closest('#popup'))document.getElementById('popup').style.display='none';}});
document.addEventListener('keydown',function(e){{if(e.key===' '||e.key==='Space'){{e.preventDefault();document.getElementById('playBtn').click();}}if(e.key==='Escape')document.getElementById('popup').style.display='none';}});
popFilter();
render();
</script>
</body>
</html>'''
    return html
if __name__ == '__main__':
    if not os.path.exists(STATE_YAML):
        print(f'ERROR: {STATE_YAML} not found')
        sys.exit(1)
    raw = parse_state_yaml(STATE_YAML)
    events = build_events(raw)
    print(f'Parsed {len(raw)} raw entries -> {len(events)} valid events')
    bps = set(e['bp'] for e in events)
    print(f'Blueprints: {len(bps)}')
    acts = {}
    for e in events:
        acts[e['action']] = acts.get(e['action'], 0) + 1
    print('Actions:', acts)
    scored = sum(1 for e in events if e['score'] is not None)
    print(f'Scored events: {scored}')
    if events:
        t_min = min(e['ts_ms'] for e in events)
        t_max = max(e['ts_ms'] for e in events)
        print(f'Time range: {datetime.fromtimestamp(t_min/1000)} -> {datetime.fromtimestamp(t_max/1000)}')
    html = build_html(events)
    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    size_kb = len(html.encode('utf-8')) / 1024
    print(f'Written: {OUT_HTML} ({size_kb:.0f} KB)')
```
Usage:
```
uv run python _forge_timeline_v8.py
```
Detta script laser state.yaml dynamiskt, extraherar alla fyra livscykelfaser (spawn/eval/improve/promote + archive), och genererar en standalone HTML. Ingen hardcoding. HTML innehaller inbaddad JSON med alla events.