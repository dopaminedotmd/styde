import yaml, re
from datetime import datetime

with open('state.yaml') as f:
    data = yaml.safe_load(f)

activity = data.get('activity', [])
bp_agents = {}
for a in activity:
    bp = a.get('blueprint', 'unknown')
    if bp not in bp_agents:
        bp_agents[bp] = []
    bp_agents[bp].append(a)

bps_out = []
all_events = []
for bp, evts in bp_agents.items():
    be = []
    for a in evts:
        ts = a.get('timestamp','')
        score = None
        m = re.search(r'C:([\d.]+)', a.get('detail',''))
        if m:
            try: score = float(m.group(1))
            except: pass
        e = {'ts':ts, 'id':str(a.get('id','')), 'action':a.get('action',''), 'score':score}
        be.append(e)
        all_events.append({'bp':bp, **e})
    be.sort(key=lambda x: x['ts'])
    bps_out.append({'n':bp, 'e':be})

bps_out.sort(key=lambda x: len(x['e']), reverse=True)
all_events.sort(key=lambda x: x['ts'])

t0 = datetime.fromisoformat(all_events[0]['ts'].replace('Z','+00:00'))
tN = datetime.fromisoformat(all_events[-1]['ts'].replace('Z','+00:00'))
span_s = (tN - t0).total_seconds()

def ts_to_x(ts, width=80):
    t = datetime.fromisoformat(ts.replace('Z','+00:00'))
    frac = (t - t0).total_seconds() / span_s if span_s > 0 else 0
    return min(width-1, max(0, round(frac * (width-1))))

print('AGENT LIFECYCLE TIMELINE')
print(f'{len(bps_out)} blueprints | {len(all_events)} events')
print(f'{t0.strftime("%Y-%m-%d %H:%M")} to {tN.strftime("%Y-%m-%d %H:%M")}')
print()

# Legend
print('LEGEND:  @=gold(85+)  O=amber(70-84)  o=cool(<70)  ^=spawn  D=improve')
print()

# Time axis
axis_width = 78
tick_count = 8
ticks = []
for i in range(tick_count+1):
    tick_ts = t0.timestamp() + (span_s * i / tick_count)
    tick_dt = datetime.fromtimestamp(tick_ts)
    ticks.append(tick_dt.strftime('%H:%M'))

axis_line = '|'
for i in range(tick_count+1):
    x = round(i * axis_width / tick_count)
    while len(axis_line) <= x:
        axis_line += '-'
    axis_line = axis_line[:x] + '|' + axis_line[x+1:]
while len(axis_line) < axis_width + 2:
    axis_line += '-'
axis_line += '|'

# Time labels
label_line = ' ' * (axis_width + 2)
for i, t in enumerate(ticks):
    x = round(i * axis_width / tick_count)
    label_line = label_line[:x] + t + label_line[x+len(t):]

print(label_line)
print(axis_line)
print()

# Per-track timeline
for bp_data in bps_out[:20]:
    bp = bp_data['n']
    evts = bp_data['e']
    markers = [' '] * axis_width
    for e in evts:
        x = ts_to_x(e['ts'], axis_width)
        sc = e['score']
        if e['action'] == 'spawn':
            markers[x] = '^'
        elif e['action'] == 'improve':
            markers[x] = 'D'
        else:
            if sc is not None and sc >= 85:
                markers[x] = '@'
            elif sc is not None and sc >= 70:
                markers[x] = 'O'
            elif sc is not None:
                markers[x] = 'o'
            else:
                markers[x] = '.'
    sc_vals = [e['score'] for e in evts if e['score'] is not None]
    best = f'best={max(sc_vals):.0f}' if sc_vals else 'no scores'
    label = bp[:38] + ' ' * max(0, 40 - len(bp[:38]))
    marker_str = '|' + ''.join(markers) + '|'
    print(f'{label} {best:12s} {marker_str}')

print()
print('SCORE DISTRIBUTION:')
for bp_data in bps_out[:20]:
    bp = bp_data['n']
    scores = [e['score'] for e in bp_data['e'] if e['score'] is not None]
    if not scores:
        continue
    gold = len([s for s in scores if s >= 85])
    amber = len([s for s in scores if 70 <= s < 85])
    cool = len([s for s in scores if s < 70])
    bar = '@'*gold + 'O'*amber + 'o'*cool
    print(f'  {bp[:38]:38s} |{bar}')
