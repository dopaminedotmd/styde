import yaml, re
from datetime import datetime

with open('state.yaml') as f:
    data = yaml.safe_load(f)

activity = data.get('activity', [])
bp_events = {}
for a in activity:
    bp = a.get('blueprint', 'unknown')
    if bp not in bp_events:
        bp_events[bp] = []
    score = None
    m = re.search(r'C:([\d.]+)', str(a.get('detail','')))
    if m:
        try: score = float(m.group(1))
        except: pass
    bp_events[bp].append({'ts':a.get('timestamp',''),'id':a.get('id',''),'action':a.get('action',''),'score':score})

bps_sorted = sorted(bp_events.items(), key=lambda x: len(x[1]), reverse=True)
all_ts = [a.get('timestamp','') for a in activity]
all_ts = [t for t in all_ts if t]
if not all_ts:
    print('No timestamps found')
    exit()

t0 = datetime.fromisoformat(min(all_ts).replace('Z','+00:00'))
tN = datetime.fromisoformat(max(all_ts).replace('Z','+00:00'))
span = (tN - t0).total_seconds()
W = 80

print('TIMELINE: %s to %s | %d events, %d BPs' % (t0.strftime('%m-%d %H:%M'), tN.strftime('%m-%d %H:%M'), len(activity), len(bp_events)))
print('@=gold>=85  #=amber70-84  o=cool<70  S=spawn  E=eval  I=improve')
print()

for bp_name, evts in bps_sorted[:25]:
    evts.sort(key=lambda x: x['ts'])
    line = ['.'] * W
    for e in evts:
        if not e['ts']:
            continue
        t = datetime.fromisoformat(e['ts'].replace('Z','+00:00'))
        pos = int((t - t0).total_seconds() / span * (W-1)) if span > 0 else 0
        pos = min(W-1, max(0, pos))
        if e['action'] == 'eval' and e['score'] is not None:
            if e['score'] >= 85:
                line[pos] = '@'
            elif e['score'] >= 70:
                line[pos] = '#'
            else:
                line[pos] = 'o'
        else:
            line[pos] = e['action'][0].upper()
    scored = [e['score'] for e in evts if e['score'] is not None]
    best = 'best=%d' % max(scored) if scored else 'no sc'
    label = bp_name[:40].ljust(42)
    print(label + ' ' + best + ' |' + ''.join(line) + '|')
