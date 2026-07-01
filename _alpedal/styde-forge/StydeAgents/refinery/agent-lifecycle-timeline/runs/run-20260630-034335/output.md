```python
import json, re
with open('_timeline_data.json') as f:
    data = json.load(f)
# Build structured data: bp -> sorted events
all_bps = {}
for bp in data['bps']:
    name = bp['n']
    evts = []
    for e in bp['e']:
        if not e.get('t'):
            continue
        evts.append({
            't': e['t'],
            'id': e.get('id',''),
            'ty': e.get('ty',''),
            'sc': e.get('sc'),
            'st': e.get('st',''),
            'stt': e.get('stt',''),
            'it': e.get('it'),
            'bm': e.get('bm','')
        })
    evts.sort(key=lambda x: x['t'])
    all_bps[name] = evts
bp_names = sorted(all_bps.keys(), key=lambda n: max(
    (e['sc'] or 0 for e in all_bps[n]), default=0
), reverse=True)
# Compute time bounds
all_ts = [e['t'] for evts in all_bps.values() for e in evts]
min_t, max_t = min(all_ts), max(all_ts)
def ts_ms(ts):
    from datetime import datetime, timezone
    return int(datetime.fromisoformat(ts.replace('Z','+00:00')).timestamp() * 1000)
min_ms = ts_ms(min_t)
max_ms = ts_ms(max_t) - min_ms  # range in ms
# Build compact data for JSON embedding
compact_d = {
    'n': bp_names,
    'e': {n: [
        [ts_ms(e['t']) - min_ms, e['id'], e['ty'], e['sc'], e['st'], e['it'], e['bm']]
        for e in all_bps[n]
    ] for n in bp_names},
    'mi': min_ms,
    'mr': max_ms,
    'mt': min_t[:10],
    'xt': max_t[:10]
}
data_json = json.dumps(compact_d, separators=(',',':'))
HTML = r"""<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Agent Lifecycle Timeline - Styde Forge</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#0d1117;color:#c9d1d9;overflow-x:hidden}
.header{padding:20px 24px 10px;border-bottom:1px solid #30363d}
.header h1{font-size:20px;font-weight:600;color:#f0f6fc}
.header .meta{font-size:12px;color:#8b949e;margin-top:3px}
.legend{display:flex;gap:12px;padding:8px 24px;background:#0d1117;border-bottom:1px solid #21262d;font-size:11px;align-items:center;flex-wrap:wrap}
.legend-item{display:flex;align-items:center;gap:4px;color:#8b949e}
.dot{width:10px;height:10px;border-radius:50%;display:inline-block}
.dot.gold{background:#d29922}
.dot.amber{background:#bb8d1e}
.dot.cool{background:#58a6ff}
.dot.no-score{background:#484f58;opacity:.4}
.legend-shape{width:12px;height:12px;display:inline-block;vertical-align:middle}
.shape-spawn{width:0;height:0;border-left:6px solid transparent;border-right:6px solid transparent;border-bottom:8px solid #238636}
.shape-eval{border-radius:50%;background:#d29922}
.shape-improve{width:10px;height:10px;background:#58a6ff;transform:rotate(45deg)}
.shape-promote{width:10px;height:10px;background:#da3633;border-radius:2px;border:1px solid #ff7b72}
.shape-archive{width:10px;height:6px;background:#484f58;border-radius:1px}
.controls{display:flex;align-items:center;gap:10px;padding:10px 24px;border-bottom:1px solid #21262d;background:#161b22;flex-wrap:wrap}
.controls label{font-size:11px;color:#8b949e;text-transform:uppercase;letter-spacing:.4px;white-space:nowrap}
.controls input[type=range]{flex:1;min-width:140px;accent-color:#d29922;height:4px}
.time-display{font-size:11px;color:#c9d1d9;min-width:155px;font-family:"JetBrains Mono","Fira Code",monospace}
.btn{padding:4px 12px;border:1px solid #30363d;border-radius:4px;background:#21262d;color:#c9d1d9;font-size:11px;cursor:pointer;font-weight:500}
.btn:hover{background:#30363d}
.btn.active{background:#d29922;color:#0d1117;border-color:#d29922}
.btn-group{display:flex;gap:2px}
.timeline-wrap{overflow:auto;max-height:calc(100vh - 160px);padding:4px 24px 24px}
.track-label{font-size:10px;fill:#c9d1d9;font-family:monospace}
.axis-text{font-size:8px;fill:#8b949e;font-family:monospace}
.grid-line{stroke:#21262d;stroke-width:1}
.tick-line{stroke:#30363d;stroke-width:.5}
.node{cursor:pointer;transition:opacity .12s}
.node.dim{opacity:.08!important}
.node:hover{opacity:1!important}
#popup{display:none;position:fixed;background:#1c2128;border:1px solid #30363d;border-radius:8px;padding:14px 18px;z-index:1000;box-shadow:0 8px 32px rgba(0,0,0,.4);min-width:250px;max-width:360px}
#popup h3{font-size:13px;color:#f0f6fc;margin-bottom:6px;padding-right:18px}
#popup .row{display:flex;justify-content:space-between;padding:3px 0;font-size:12px;border-bottom:1px solid #21262d}
#popup .row:last-child{border-bottom:none}
#popup .label{color:#8b949e}
#popup .value{color:#f0f6fc;font-family:monospace;font-size:11px}
.pop-close{position:absolute;top:8px;right:10px;cursor:pointer;color:#8b949e;font-size:18px;line-height:1;background:none;border:none}
.pop-close:hover{color:#f0f6fc}
.stat-bar{font-size:11px;color:#484f58;padding:3px 24px;background:#0d1117;text-align:right;border-top:1px solid #21262d}
select{background:#21262d;color:#c9d1d9;border:1px solid #30363d;border-radius:4px;padding:3px 6px;font-size:11px}
</style>
</head>
<body>
<div class=header>
<h1>Agent Lifecycle Timeline</h1>
<div class=meta><span id=bpCount></span> blueprints | <span id=evCount></span> events | <span id=scCount></span> scored | <span id=timeRange></span></div>
</div>
<div class=legend>
<span class=legend-item><span class="dot gold"></span> 85+</span>
<span class=legend-item><span class="dot amber"></span> 70-84</span>
<span class=legend-item><span class="dot cool"></span> &lt;70</span>
<span class=legend-item><span class="dot no-score"></span> no score</span>
<span class=legend-item style=margin-left:10px><span class=legend-shape style=background:#238636;border-radius:2px></span> spawn</span>
<span class=legend-item><span class=legend-shape style=background:#d29922;border-radius:8px></span> eval</span>
<span class=legend-item><span class=legend-shape style=background:#58a6ff;transform:rotate(45deg);width:8px;height:8px></span> improve</span>
<span class=legend-item><span class=legend-shape style=background:#da3633;border-radius:2px;border:1px solid #ff7b72></span> promote</span>
<span class=legend-item><span class=legend-shape style=background:#484f58;border-radius:1px></span> archive</span>
</div>
<div class=controls>
<label>scrub</label>
<input type=range id=scrubber min=0 max=1000 value=0 step=1>
<span class=time-display id=timeDisplay></span>
<div class=btn-group>
<button class=btn id=playBtn>play</button>
<button class=btn id=resetBtn>end</button>
</div>
<label>bp</label>
<select id=bpFilter><option value=all>all</option></select>
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
<div class=timeline-wrap id=wrap><div id=timeline></div></div>
<div id=popup><button class=pop-close id=popClose>&times;</button><h3 id=popTitle></h3><div id=popBody></div></div>
<div class=stat-bar id=statBar></div>
<script>
var D=%DATA%;
var bpNames=D.n,evts=D.e,minMs=D.mi,rangeMs=D.mr,globalMin=minMs,globalMax=minMs+rangeMs;
var isPlay=false,playInt=null,curScrub=0,allNodes=[];
function tsAbs(rel){return new Date(minMs+rel);}
function tsRel(d){return d.getTime()-minMs;}
function pct(t){return t/rangeMs;}
function nodeColor(sc,ty){
  if(sc===null||sc===undefined)return '#484f58';
  if(sc>=85)return '#d29922';
  if(sc>=70)return '#bb8d1e';
  return '#58a6ff';
}
function nodeOpacity(sc,ty){
  if(sc===null||sc===undefined)return.35;
  if(sc>=85)return 1;
  if(sc>=70)return.65;
  return.45;
}
function nodeRadius(sc,ty){
  if(ty==='spawn')return 4;
  if(ty==='improve')return 3.5;
  if(ty==='promote')return 5;
  if(ty==='archive')return 2.5;
  if(sc===null||sc===undefined)return 4;
  if(sc>=90)return 8;
  if(sc>=80)return 6.5;
  return Math.max(3.5,Math.min(7,sc/14));
}
function shapePath(cx,cy,ty,r){
  if(ty==='spawn'){
    var t=r*1.3;
    return 'M'+cx+','+(cy-t)+'L'+(cx+t)+','+(cy+t)+'L'+(cx-t)+','+(cy+t)+'Z';
  }
  if(ty==='improve'){
    var s=r*1.1;
    return 'M'+cx+','+(cy-s)+'L'+(cx+s)+','+cy+'L'+cx+','+(cy+s)+'L'+(cx-s)+','+cy+'Z';
  }
  if(ty==='promote'){
    return null;
  }
  if(ty==='archive'){
    return 'M'+(cx-3)+','+(cy-2)+'h6v4h-6Z';
  }
  return null;
}
function render(){
  var sv=parseInt(document.getElementById('scrubber').value);
  var cutT=minMs+rangeMs*(sv/1000);
  var bpf=document.getElementById('bpFilter').value;
  var sf=document.getElementById('stageFilter').value;
  var vis=bpf==='all'?bpNames:[bpf];
  if(sf!=='all')vis=vis.filter(function(n){for(var i=0;i<evts[n].length;i++)if(evts[n][i][2]===sf)return true;return false;});
  var n=vis.length,ML=200,MT=22,TH=22,TG=2,PAD=50;
  var totalH=MT+n*(TH+TG)+30;
  var totalW=ML+2200;
  var pl=ML,pr=totalW-PAD,pw=pr-pl;
  var s='<svg class=tsvg width='+totalW+' height='+totalH+' viewBox="0 0 '+totalW+' '+totalH+'"><rect width='+totalW+' height='+totalH+' fill=#0d1117/>';
  // Axis ticks - 6 evenly spaced
  var ni=6;
  var tm=new Date(globalMin);
  tm.setHours(0,0,0,0);
  for(var i=0;i<=ni;i++){
    var t=globalMin+(rangeMs*i/ni);
    var x=pl+(t-globalMin)/rangeMs*pw;
    s+='<line class=grid-line x1='+x+' y1='+(MT-6)+' x2='+x+' y2='+(totalH-12)+'/>';
    var d=new Date(t);
    s+='<text class=axis-text x='+x+' y='+(MT-10)+' text-anchor=middle>'+d.toISOString().slice(11,19)+'</text>';
  }
  s+='<text class=axis-text x='+pl+' y='+(MT-10)+' text-anchor=start>'+new Date(globalMin).toISOString().slice(0,10)+'</text>';
  s+='<text class=axis-text x='+pr+' y='+(MT-10)+' text-anchor=end>'+new Date(globalMax).toISOString().slice(0,10)+'</text>';
  // Scrubber line
  var sx=pl+(cutT-globalMin)/rangeMs*pw;
  s+='<line x1='+sx+' y1='+(MT-6)+' x2='+sx+' y2='+(totalH-12)+' stroke=#d29922 stroke-width=1.5 stroke-dasharray=4,3 opacity=.5/>';
  allNodes=[];
  for(var i=0;i<n;i++){
    var bp=vis[i],y0=MT+i*(TH+TG);
    var bg=i%2===0?'#0d1117':'#161b2233';
    s+='<rect x='+(pl-6)+' y='+y0+' width='+(pw+12)+' height='+TH+' fill='+bg+' rx=2/>';
    var lb=bp.length>32?bp.slice(0,29)+'...':bp;
    s+='<text class=track-label x='+(ML-10)+' y='+(y0+TH/2+1)+' text-anchor=end>'+lb+'</text>';
    var ev=evts[bp]||[];
    // Filter visible events up to cutT
    var fv=ev.filter(function(e){return minMs+e[0]<=cutT;});
    // Connection line between events
    var pts=[];
    for(var j=0;j<fv.length;j++){
      var x=pl+(e[0])/rangeMs*pw;
      pts.push(x);
    }
    if(pts.length>=2){
      var pd='';
      for(var j=0;j<pts.length;j++)pd+=(j===0?'M':'L')+pts[j]+','+(y0+TH/2);
      s+='<path d='+pd+' stroke=#30363d stroke-width=1 fill=none opacity=.3/>';
    }
    for(var j=0;j<fv.length;j++){
      var e=fv[j],x=pl+e[0]/rangeMs*pw,y=y0+TH/2;
      var sc=e[3],ty=e[2],id=e[1];
      var nd={
        bp:bp,id:id,ty:ty,sc:sc,st:e[4],it:e[5],bm:e[6],
        ts:new Date(minMs+e[0]).toISOString()
      };
      var idx=allNodes.push(nd)-1;
      var c=nodeColor(sc,ty),o=nodeOpacity(sc,ty),r=nodeRadius(sc,ty);
      var di=ty==='promote'?'data-fill='+c+' data-r='+r:'';
      var shape=shapePath(x,y,ty,r);
      var esc=bp.replace(/'/g,"\\'");
      if(shape){
        s+='<path class=node d='+shape+' fill='+c+' opacity='+o+' data-i='+idx+' data-bp='+esc+'/>';
      }else{
        s+='<circle class=node cx='+x+' cy='+y+' r='+r+' fill='+c+' opacity='+o+' stroke='+(ty==='promote'?'#ff7b72':'none')+' stroke-width='+(ty==='promote'?1:0)+' data-i='+idx+' data-bp='+esc+'/>';
      }
      // Score label for high scorers
      if(sc!==null&&sc!==undefined&&sc>=80){
        s+='<text x='+x+' y='+(y+r+8)+' text-anchor=middle fill='+c+' font-size=6 font-family=monospace opacity='+o+'>'+sc+'</text>';
      }
    }
  }
  s+='</svg>';
  document.getElementById('timeline').innerHTML=s;
  // Attach event listeners to nodes
  var ns=document.querySelectorAll('.node');
  for(var i=0;i<ns.length;i++){
    (function(el){
      var bp=el.getAttribute('data-bp');
      el.addEventListener('click',function(evt){
        evt.stopPropagation();
        var idx=parseInt(el.getAttribute('data-i'));
        showPopup(idx,el);
      });
      el.addEventListener('mouseenter',function(){
        var ns2=document.querySelectorAll('.node');
        for(var j=0;j<ns2.length;j++)ns2[j].classList.toggle('dim',ns2[j].getAttribute('data-bp')!==bp);
      });
      el.addEventListener('mouseleave',function(){
        var ns2=document.querySelectorAll('.node');
        for(var j=0;j<ns2.length;j++)ns2[j].classList.remove('dim');
      });
    })(ns[i]);
  }
  var d2=new Date(cutT);
  document.getElementById('statBar').textContent=vis.length+' bps | cut '+d2.toISOString().slice(0,19).replace('T',' ');
}
function showPopup(idx,el){
  var nd=allNodes[idx];
  if(!nd)return;
  document.getElementById('popTitle').textContent=nd.bp;
  var rows=[
    {l:'Run ID',v:nd.id},
    {l:'Action',v:nd.ty},
    {l:'Stage',v:nd.st||'-'},
    {l:'Timestamp',v:nd.ts.slice(0,19).replace('T',' ')}
  ];
  if(nd.sc!==null&&nd.sc!==undefined)rows.push({l:'Score',v:nd.sc});
  if(nd.it!==null&&nd.it!==undefined)rows.push({l:'Iteration',v:nd.it});
  if(nd.bm)rows.push({l:'Benchmark',v:nd.bm});
  var h='';
  for(var i=0;i<rows.length;i++)h+='<div class=row><span class=label>'+rows[i].l+'</span><span class=value>'+(rows[i].v||'')+'</span></div>';
  document.getElementById('popBody').innerHTML=h;
  var pop=document.getElementById('popup');
  pop.style.display='block';
  if(el){
    var r=el.getBoundingClientRect(),l=r.right+12,t=r.top;
    if(l+360>window.innerWidth)l=r.left-300;
    if(t+300>window.innerHeight)t=window.innerHeight-300;
    if(t<10)t=10;
    pop.style.left=l+'px';pop.style.top=t+'px';
  }
}
function init(){
  var te=0,sc=0;
  for(var i=0;i<bpNames.length;i++){
    var ev=evts[bpNames[i]];
    for(var j=0;j<ev.length;j++){
      te++;
      if(ev[j][3]!==null&&ev[j][3]!==undefined)sc++;
    }
  }
  document.getElementById('bpCount').textContent=bpNames.length;
  document.getElementById('evCount').textContent=te;
  document.getElementById('scCount').textContent=sc;
  document.getElementById('timeRange').textContent=new Date(globalMin).toISOString().slice(0,19).replace('T',' ')+' to '+new Date(globalMax).toISOString().slice(0,19).replace('T',' ');
  // Populate filter dropdown
  var sel=document.getElementById('bpFilter');
  for(var i=0;i<bpNames.length;i++){
    var bp=bpNames[i],ev=evts[bp],ec=0,best=0;
    for(var j=0;j<ev.length;j++){if(ev[j][3]!==null){ec++;if(ev[j][3]>best)best=ev[j][3];}}
    var opt=document.createElement('option');
    opt.value=bp;opt.textContent=bp+(ec?' ('+ec+' evals, best '+best+')':'');
    sel.appendChild(opt);
  }
  updDisp();
  render();
}
function updDisp(){
  var pct2=curScrub/1000,t=minMs+rangeMs*pct2;
  document.getElementById('timeDisplay').textContent=new Date(t).toISOString().slice(0,19).replace('T',' ');
}
// Event listeners
document.getElementById('scrubber').addEventListener('input',function(){
  curScrub=parseInt(this.value);updDisp();render();
});
document.getElementById('playBtn').addEventListener('click',function(){
  isPlay=!isPlay;this.textContent=isPlay?'pause':'play';this.classList.toggle('active',isPlay);
  if(isPlay){
    if(curScrub>=1000){curScrub=0;document.getElementById('scrubber').value=0;updDisp();render();}
    var self=this;
    playInt=setInterval(function(){
      curScrub+=3;if(curScrub>1000){curScrub=1000;self.textContent='play';self.classList.remove('active');clearInterval(playInt);isPlay=false;}
      document.getElementById('scrubber').value=curScrub;updDisp();render();
    },70);
  }else clearInterval(playInt);
});
document.getElementById('resetBtn').addEventListener('click',function(){
  if(isPlay){clearInterval(playInt);isPlay=false;document.getElementById('playBtn').textContent='play';document.getElementById('playBtn').classList.remove('active');}
  curScrub=1000;document.getElementById('scrubber').value=1000;updDisp();render();
});
document.getElementById('bpFilter').addEventListener('change',render);
document.getElementById('stageFilter').addEventListener('change',render);
document.getElementById('popClose').addEventListener('click',function(){document.getElementById('popup').style.display='none';});
document.addEventListener('click',function(e){
  if(!e.target.closest('#popup')&&!e.target.closest('.node'))document.getElementById('popup').style.display='none';
});
document.addEventListener('keydown',function(e){
  if(e.key===' '||e.key==='Space'){e.preventDefault();document.getElementById('playBtn').click();}
  if(e.key==='Escape')document.getElementById('popup').style.display='none';
});
init();
</script>
</body>
</html>"""
HTML = HTML.replace('%DATA%', data_json)
with open('_timeline_output.html', 'w', encoding='utf-8') as f:
    f.write(HTML)
size = len(HTML.encode('utf-8'))
print(f'Written: _timeline_output.html ({size/1024:.0f} KB)')
# Validate
m = re.search(r'var D=({.*?});', HTML, re.DOTALL)
if m:
    parsed = json.loads(m.group(1))
    nbps = len(parsed['n'])
    nevt = sum(len(v) for v in parsed['e'].values())
    nsc = sum(1 for v in parsed['e'].values() for e in v if e[3] is not None)
    print(f'Data valid: {nbps} blueprints, {nevt} events, {nsc} scored')
else:
    print('ERROR: data not found in HTML')
```