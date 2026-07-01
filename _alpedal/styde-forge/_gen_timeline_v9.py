import yaml, json, sys, math
from datetime import datetime, timezone
from collections import defaultdict

with open('state.yaml') as f:
    data = yaml.safe_load(f)

events_raw = data.get('activity', [])

# Group by blueprint
bp_events = defaultdict(list)
for e in events_raw:
    bp = e.get('blueprint', 'unknown')
    ts = e.get('timestamp', '')
    if not ts:
        continue
    action = e.get('action', '')
    pid = e.get('id', '')
    detail = e.get('detail', '')
    progress = e.get('progress', 0)
    status = e.get('status', '')

    # Parse composite score from detail like "S:91 J:93 C:92.2"
    score = -1
    import re
    m = re.search(r'C:([\d.]+)', str(detail))
    if m:
        score = float(m.group(1))

    bp_events[bp].append({
        'ts': ts,
        'action': action,
        'id': str(pid),
        'detail': str(detail),
        'score': score,
        'status': status,
        'progress': progress
    })

# Sort blueprints by max score descending
bp_order = sorted(bp_events.keys(), key=lambda b: max(
    (e['score'] for e in bp_events[b] if e['score'] >= 0), default=-1
), reverse=True)

# Collect all timestamps and normalize
all_ts = []
for b, evts in bp_events.items():
    for e in evts:
        try:
            all_ts.append(datetime.fromisoformat(e['ts'].replace('Z', '+00:00')))
        except:
            pass
all_ts.sort()
t_start = all_ts[0]
t_end = all_ts[-1]
total_span = (t_end - t_start).total_seconds()

def ts_to_pct(ts_str):
    try:
        d = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        return (d - t_start).total_seconds() / total_span if total_span > 0 else 0
    except:
        return 0

def color_for_score(s):
    if s >= 85: return '#d29922'
    if s >= 70: return '#bb8d1e'
    return '#58a6ff'

def opacity_for_score(s, status):
    if status == 'running': return 0.35
    if s >= 85: return 1.0
    if s >= 70: return 0.7
    if s < 0: return 0.35
    return 0.5

def radius_for(action, score):
    if action == 'spawn': return 4
    if action == 'improve': return 4
    if score >= 0: return max(4, min(9, score / 12))
    return 5

# JSON data for embedding
events_compact = []
for bp in bp_order:
    for e in bp_events[bp]:
        events_compact.append([
            bp,
            e['ts'],
            e['id'],
            e['action'],
            e['score'],
            e['status'],
            e['detail'][:80]
        ])

data_json = json.dumps(events_compact, separators=(',', ':'))

n = len(bp_order)
ML = 220
MT = 45
TH = 26
TG = 4
PAD = 60
tw = ML + 1800
sy = MT + n * (TH + TG)
ph = n * (TH + TG)
th = MT + ph + 130

total_events = len(events_compact)
scored = sum(1 for e in events_compact if e[4] >= 0)

html = '''<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Agent Lifecycle Timeline - Styde Forge v9</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#0d1117;color:#c9d1d9;overflow-x:hidden}
.header{padding:18px 24px 8px;border-bottom:1px solid #30363d}
.header h1{font-size:18px;font-weight:600;color:#f0f6fc}
.header .meta{font-size:11px;color:#8b949e;margin-top:2px}
.legend{display:flex;gap:12px;padding:6px 24px;background:#0d1117;border-bottom:1px solid #21262d;font-size:11px;align-items:center;flex-wrap:wrap}
.legend-item{display:flex;align-items:center;gap:4px;color:#8b949e}
.legend-dot{width:10px;height:10px;border-radius:50%}
.legend-dot.gold{background:#d29922}
.legend-dot.amber{background:#bb8d1e;opacity:.65}
.legend-dot.cool{background:#58a6ff;opacity:.5}
.legend-icon{width:10px;height:10px;border-radius:2px;display:inline-block}
.legend-icon.spawn{background:#238636}
.legend-icon.eval{background:#d29922}
.legend-icon.improve{background:#58a6ff}
.controls{display:flex;align-items:center;gap:10px;padding:8px 24px;border-bottom:1px solid #21262d;background:#161b22;flex-wrap:wrap}
.controls label{font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:.3px}
.controls input[type=range]{flex:1;min-width:140px;accent-color:#d29922;height:4px}
.controls .time-display{font-size:11px;color:#c9d1d9;min-width:150px;font-family:"JetBrains Mono","Fira Code",monospace}
.btn{padding:4px 12px;border:1px solid #30363d;border-radius:4px;background:#21262d;color:#c9d1d9;font-size:10px;cursor:pointer;font-weight:500;line-height:1.4}
.btn:hover{background:#30363d}
.btn.active{background:#d29922;color:#0d1117;border-color:#d29922}
.btn-group{display:flex;gap:3px}
.timeline-wrap{overflow-x:auto;overflow-y:auto;max-height:calc(100vh - 155px);padding:4px 24px 16px;background:#0d1117}
.timeline-svg{min-width:100%;display:block}
.node{cursor:pointer;transition:r .08s,opacity .1s}
.node.dimmed{opacity:.12!important}
.node:hover{opacity:1!important;filter:brightness(1.3)}
.track-label text{font-size:10px;fill:#c9d1d9;dominant-baseline:middle;font-family:monospace}
.axis-text{font-size:9px;fill:#8b949e;font-family:"JetBrains Mono",monospace}
.grid-line{stroke:#21262d;stroke-width:1}
#popup{display:none;position:fixed;background:#1c2128;border:1px solid #30363d;border-radius:8px;padding:12px 16px;z-index:1000;box-shadow:0 8px 32px rgba(0,0,0,.5);min-width:240px;max-width:360px;font-size:11px}
#popup h3{font-size:12px;color:#f0f6fc;margin-bottom:5px;padding-right:16px}
#popup .row{display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px solid #21262d}
#popup .row:last-child{border-bottom:none}
#popup .label{color:#8b949e}
#popup .value{color:#f0f6fc;font-family:"JetBrains Mono",monospace;font-size:10px}
#popup .close{position:absolute;top:8px;right:12px;cursor:pointer;color:#8b949e;font-size:14px;background:none;border:none;line-height:1}
#popup .close:hover{color:#f0f6fc}
.stat-bar{font-size:10px;color:#484f58;padding:2px 24px;background:#0d1117;text-align:right;border-top:1px solid #21262d;font-family:monospace}
.bp-filter{background:#21262d;color:#c9d1d9;border:1px solid #30363d;border-radius:4px;padding:3px 5px;font-size:10px;min-width:140px;max-width:240px}
.score-label{font-size:7px;font-family:monospace;text-anchor:middle}
</style>
</head>
<body>
<div class=header>
<h1>Agent Lifecycle Timeline</h1>
<div class=meta><span id=bpCount>'''+str(n)+'''</span> blueprints | <span id=eventCount>'''+str(total_events)+'''</span> events | <span id=scoreCount>'''+str(scored)+'''</span> scored | '''+t_start.strftime('%Y-%m-%d %H:%M')+''' to '''+t_end.strftime('%Y-%m-%d %H:%M')+'''</div>
</div>
<div class=legend>
<div class=legend-item><span class=legend-dot gold></span> 85+ hot</div>
<div class=legend-item><span class=legend-dot amber></span> 70-84 amber</div>
<div class=legend-item><span class=legend-dot cool></span> &lt;70 cool</div>
<div class=legend-item style=margin-left:8px><span class=legend-icon spawn></span> spawn</div>
<div class=legend-item><span class=legend-icon eval></span> eval</div>
<div class=legend-item><span class=legend-icon improve></span> improve</div>
</div>
<div class=controls>
<label>scrub</label>
<input type=range id=scrubber min=0 max=1000 value=1000 step=1>
<span class=time-display id=timeDisplay></span>
<div class=btn-group>
<button class=btn id=playBtn>play</button>
<button class=btn id=resetBtn>reset</button>
</div>
<label style=margin-left:10px>blueprint</label>
<select id=bpFilter class=bp-filter><option value=all>all blueprints</option></select>
</div>
<div class=timeline-wrap><div id=timeline></div></div>
<div id=popup><button class=close id=popupClose>&times;</button><h3 id=popupTitle>detail</h3><div id=popupBody></div></div>
<div class=stat-bar id=statBar></div>
<script>
var EV='''+data_json+''';
var minT='''+str(int(t_start.timestamp()*1000))+''',maxT='''+str(int(t_end.timestamp()*1000))+''',span=maxT-minT;
var allBps={},bpNames=[];
var isPlaying=false,playInt=null,curScrub=1000;

function init(){
  var raw=JSON.parse(EV);
  for(var i=0;i<raw.length;i++){
    var e=raw[i],nm=e[0];
    if(!allBps[nm])allBps[nm]=[];
    allBps[nm].push({ts:e[1],id:e[2],act:e[3],sc:e[4],st:e[5],det:e[6]});
  }
  bpNames=Object.keys(allBps);
  popFilter();
  updDisp();
  render();
}

function color(sc){
  if(sc<0)return('#484f58');
  if(sc>=85)return('#d29922');
  if(sc>=70)return('#bb8d1e');
  return('#58a6ff');
}
function opac(sc,st){
  if(st==='running')return.35;
  if(sc>=85)return 1;
  if(sc>=70)return.7;
  if(sc<0)return.35;
  return.5;
}
function rad(sc,act){
  if(act==='spawn'||act==='improve')return 4;
  if(sc<0)return 5;
  return Math.max(4,Math.min(9,sc/12));
}

function normT(ts){
  return(new Date(ts).getTime()-minT)/span;
}

function render(){
  var sv=parseInt(document.getElementById('scrubber').value);
  var ct=minT+span*(sv/1000);
  var bpf=document.getElementById('bpFilter').value;
  var vis=bpf==='all'?bpNames:[bpf];
  var n=vis.length;
  var MT='''+str(MT)+''',TH='''+str(TH)+''',TG='''+str(TG)+''',pl='''+str(ML)+''',pr='''+str(ML+1800)+''',pw='''+str(1800)+''';
  var sy='''+str(sy)+''';
  var s='<svg class=timeline-svg width='''+str(tw)+''' height='''+str(sy+16)+''' viewBox=\"0 0 '''+str(tw)+' '+str(sy+16)+'''\" xmlns=http://www.w3.org/2000/svg><defs><filter id=sh><feDropShadow dx=0 dy=1 stdDeviation=1.5 flood-opacity=.25/></filter><linearGradient id=bg x1=0 x2=0 y1=0 y2=1><stop offset=0% stop-color=#0d1117/><stop offset=100% stop-color=#161b22/></linearGradient></defs><rect width='''+str(tw)+' y=0 height='+str(sy+16)+''' fill=url(#bg)/>';

  // title
  s+='<text x='''+str(ML+900)+''' y=18 fill=#f0f6fc font-size=13 font-weight=600 text-anchor=middle font-family=monospace>AGENT LIFECYCLE TIMELINE</text>';
  s+='<text x='''+str(ML+900)+''' y=32 fill=#8b949e font-size=9 text-anchor=middle>'+n+' blueprints | scrub at '+(new Date(ct)).toISOString().slice(0,19).replace('T',' ')+'</text>';

  // time axis
  var ni=10;
  for(var i=0;i<=ni;i++){
    var t=minT+span*(i/ni);
    var x=pl+(i/ni)*pw;
    s+='<line class=grid-line x1='+x+' y1='+MT+' x2='+x+' y2='+sy+' stroke-dasharray=2,3 opacity=.3/>';
    var d=new Date(t);
    s+='<text class=axis-text x='+x+' y='+(MT-10)+' text-anchor=middle>'+('0'+d.getHours()).slice(-2)+':'+('0'+d.getMinutes()).slice(-2)+'</text>';
  }

  // scrub line
  var sx=pl+(ct-minT)/span*pw;
  s+='<line x1='+sx+' y1='+MT+' x2='+sx+' y2='+sy+' stroke=#e94560 stroke-width=1.5 stroke-dasharray=4,2 opacity=.6/>';

  // per blueprints
  for(var i=0;i<n;i++){
    var bp=vis[i],y0=MT+i*(TH+TG);
    var evts=allBps[bp].slice().sort(function(a,b){return new Date(a.ts)-new Date(b.ts);});
    var bg=i%2===0?'#0d1117':'#161b2244';
    s+='<rect x='+(pl-4)+' y='+y0+' width='+(pw+8)+' height='+TH+' fill='+bg+' rx=2/>';

    // label
    var lb=bp.length>28?bp.slice(0,25)+'...':bp;
    s+='<text class=track-label x='+(ML-10)+' y='+(y0+TH/2)+' text-anchor=end>'+lb+'</text>';

    // filter by scrub time
    var ft=[];
    for(var e=0;e<evts.length;e++)if(new Date(evts[e].ts).getTime()<=ct)ft.push(evts[e]);

    // connection lines
    var lts=[];
    for(var e=0;e<ft.length;e++)lts.push(new Date(ft[e].ts).getTime());
    lts.sort(function(a,b){return a-b;});
    if(lts.length>=2){
      var pd='';
      for(var j=0;j<lts.length;j++){var lx=pl+(lts[j]-minT)/span*pw;pd+=(j===0?'M':'L')+lx+','+(y0+TH/2);}
      s+='<path d='+pd+' stroke=#30363d stroke-width=1 fill=none opacity=.25/>';
    }

    // nodes
    for(var e=0;e<ft.length;e++){
      var a=ft[e],t=new Date(a.ts).getTime(),x=pl+(t-minT)/span*pw,y=y0+TH/2;
      var r=rad(a.sc,a.act),c=color(a.sc),o=opac(a.sc,a.st);
      var esc=bp.replace(/'/g,"\\'");
      var oc='onclick=\"pop(\\''+esc+'\\','+a.id+')\"';
      var hv='onmouseover=\"dim(\\''+esc+'\\')\" onmouseout=\"undim()\"';

      if(a.act==='spawn'){
        var pts=(x)+','+(y-r-1)+' '+(x-r+1)+','+(y+r-1)+' '+(x+r-1)+','+(y+r-1);
        s+='<polygon class=node points='+pts+' fill=#238636 opacity=.5 '+oc+' '+hv+' data-bp='+esc+'/>';
      }else if(a.act==='improve'){
        var pts=(x)+','+(y-r)+' '+(x+r)+','+y+' '+(x)+','+(y+r)+' '+(x-r)+','+y;
        s+='<polygon class=node points='+pts+' fill=#58a6ff opacity=.4 '+oc+' '+hv+' data-bp='+esc+'/>';
      }else{
        s+='<circle class=node cx='+x+' cy='+y+' r='+r+' fill='+c+' opacity='+o+' filter=url(#sh) '+oc+' '+hv+' data-bp='+esc+'/>';
        if(a.sc>=80){
          s+='<text class=score-label x='+x+' y='+(y+r+8)+' fill='+c+' opacity='+o+'>'+a.sc+'</text>';
        }
      }
    }
  }
  s+='</svg>';
  document.getElementById('timeline').innerHTML=s;
  var d2=new Date(ct);
  document.getElementById('statBar').textContent='showing '+n+' bps | cut at '+d2.toISOString().slice(0,19).replace('T',' ');
}

function dim(bp){
  var ns=document.querySelectorAll('.node');
  for(var i=0;i<ns.length;i++){
    var n=ns[i];
    n.classList.toggle('dimmed',n.getAttribute('data-bp')!==bp);
  }
}
function undim(){
  var ns=document.querySelectorAll('.node');
  for(var i=0;i<ns.length;i++)ns[i].classList.remove('dimmed');
}

function pop(bp,id){
  var evts=allBps[bp]||[],a=null;
  for(var i=0;i<evts.length;i++)if(evts[i].id==id){a=evts[i];break;}
  if(!a)return;
  document.getElementById('popupTitle').textContent=bp;
  var rows=[
    {l:'Run ID',v:a.id},
    {l:'Action',v:a.act},
    {l:'Status',v:a.st},
    {l:'Timestamp',v:a.ts}
  ];
  if(a.sc>=0)rows.push({l:'Score',v:a.sc});
  if(a.det)rows.push({l:'Detail',v:a.det.slice(0,60)});
  var h='';
  for(var i=0;i<rows.length;i++){
    h+='<div class=row><span class=label>'+rows[i].l+'</span><span class=value>'+(rows[i].v||'-')+'</span></div>';
  }
  document.getElementById('popupBody').innerHTML=h;
  var popup=document.getElementById('popup');
  popup.style.display='block';
  var r=event.target.getBoundingClientRect?event.target.getBoundingClientRect():{right:window.innerWidth/2,top:100};
  var l=r.right+12,t=r.top-10;
  if(l+360>window.innerWidth)l=r.left-300;
  if(t<10)t=10;
  if(t+250>window.innerHeight)t=window.innerHeight-260;
  popup.style.left=l+'px';popup.style.top=t+'px';
}

function popFilter(){
  var sel=document.getElementById('bpFilter');
  for(var b=0;b<bpNames.length;b++){
    var bp=bpNames[b],evts=allBps[bp],ec=0,best=0,worst=100;
    for(var i=0;i<evts.length;i++){if(evts[i].sc>=0){ec++;if(evts[i].sc>best)best=evts[i].sc;if(evts[i].sc<worst)worst=evts[i].sc;}}
    if(ec===0){best='-';worst='-';}
    var opt=document.createElement('option');
    opt.value=bp;opt.textContent=bp+' ('+ec+' evals, '+best+'/'+worst+')';
    sel.appendChild(opt);
  }
}

function updDisp(){
  var pct=curScrub/1000,t=minT+span*pct;
  document.getElementById('timeDisplay').textContent=(new Date(t)).toISOString().slice(0,19).replace('T',' ');
}

document.getElementById('scrubber').addEventListener('input',function(){curScrub=parseInt(this.value);updDisp();render();});
document.getElementById('playBtn').addEventListener('click',function(){
  isPlaying=!isPlaying;this.textContent=isPlaying?'pause':'play';this.classList.toggle('active',isPlaying);
  if(isPlaying){
    if(curScrub>=1000){curScrub=0;document.getElementById('scrubber').value=0;updDisp();render();}
    playInt=setInterval(function(){
      curScrub+=2;if(curScrub>1000){curScrub=1000;document.getElementById('playBtn').textContent='play';document.getElementById('playBtn').classList.remove('active');clearInterval(playInt);isPlaying=false;}
      document.getElementById('scrubber').value=curScrub;updDisp();render();
    },50);
  }else clearInterval(playInt);
});
document.getElementById('resetBtn').addEventListener('click',function(){
  if(isPlaying){clearInterval(playInt);isPlaying=false;document.getElementById('playBtn').textContent='play';document.getElementById('playBtn').classList.remove('active');}
  curScrub=1000;document.getElementById('scrubber').value=1000;updDisp();render();
});
document.getElementById('bpFilter').addEventListener('change',render);
document.getElementById('popupClose').addEventListener('click',function(){document.getElementById('popup').style.display='none';});
document.addEventListener('click',function(e){
  if(!e.target.closest('.node')&&!e.target.closest('#popup')&&!e.target.closest('#playBtn')&&!e.target.closest('#resetBtn')&&!e.target.closest('#bpFilter'))
    document.getElementById('popup').style.display='none';
});
document.addEventListener('keydown',function(e){
  if(e.key===' '||e.key==='Space'){e.preventDefault();document.getElementById('playBtn').click();}
  if(e.key==='Escape')document.getElementById('popup').style.display='none';
});
init();
</script>
</body>
</html>'''

with open('agent-lifecycle-timeline-v9.html', 'w', encoding='utf-8') as f:
    f.write(html)

size = len(html.encode('utf-8'))
print(f'Written: agent-lifecycle-timeline-v9.html ({size/1024:.0f} KB)')
print(f'Data: {total_events} events from {n} blueprints ({scored} scored)')
print(f'Range: {t_start} to {t_end}')
