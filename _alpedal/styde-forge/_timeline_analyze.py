import yaml, re, json

with open('E:/Stryde/_alpedal/styde-forge/state.yaml') as f:
    data = yaml.safe_load(f)

activity = data.get('activity', [])
bp_agents = {}
for a in activity:
    bp = a.get('blueprint', 'unknown')
    if bp not in bp_agents:
        bp_agents[bp] = []
    bp_agents[bp].append(a)

total_evts = len(activity)
total_bps = len(bp_agents)

sorted_bps = sorted(bp_agents.items(), key=lambda x: len(x[1]), reverse=True)

all_events = []
for bp, evts in sorted_bps:
    for a in evts:
        ts = a.get('timestamp', '')
        score = None
        detail = a.get('detail', '')
        m = re.search(r'C:([\d.]+)', detail)
        if m:
            try:
                score = round(float(m.group(1)), 1)
            except:
                pass
        all_events.append({
            'bp': bp,
            'ts': ts,
            'id': a.get('id', ''),
            'action': a.get('action', ''),
            'score': score,
            'stage': 'refinery',
            'detail': detail[:80]
        })

all_events.sort(key=lambda e: e['ts'])

scored = [e for e in all_events if e['score'] is not None]
gold = [e for e in scored if e['score'] >= 85]
amber = [e for e in scored if e['score'] >= 70 and e['score'] < 85]
cool = [e for e in scored if e['score'] < 70]

actions = {}
for e in all_events:
    act = e['action']
    actions[act] = actions.get(act, 0) + 1

print('AGENT LIFECYCLE TIMELINE ANALYSIS')
print('='*60)
print(f'Blueprints: {total_bps}')
print(f'Total events: {total_evts}')
print(f'Scored evals: {len(scored)}')
print(f'  Gold (85+): {len(gold)}')
print(f'  Amber (70-84): {len(amber)}')
print(f'  Cool (<70): {len(cool)}')
print(f'Time range: {all_events[0]["ts"]} to {all_events[-1]["ts"]}')
print()
print('Events by action:')
for a, c in sorted(actions.items(), key=lambda x: -x[1]):
    print(f'  {a}: {c}')
print()
print('Top blueprints by event count:')
for i, (bp, evts) in enumerate(sorted_bps[:30]):
    scores = []
    for a in evts:
        m = re.search(r'C:([\d.]+)', a.get('detail',''))
        if m:
            try:
                scores.append(float(m.group(1)))
            except:
                pass
    best = max(scores) if scores else '-'
    print(f'  {i+1:2d}. {bp}')
    print(f'      events={len(evts)}  best={best}')
print()
print('Timeline event data (first 50 events):')
for e in all_events[:50]:
    score_str = f'{e["score"]:5.1f}' if e['score'] is not None else '  N/A'
    print(f'  {e["ts"]} | {e["action"]:8s} | {score_str} | {e["bp"][:35]:35s} | #{e["id"]}')

print()
print('Timeline event data (last 20 events):')
for e in all_events[-20:]:
    score_str = f'{e["score"]:5.1f}' if e['score'] is not None else '  N/A'
    print(f'  {e["ts"]} | {e["action"]:8s} | {score_str} | {e["bp"][:35]:35s} | #{e["id"]}')

# Generate compact timeline data for visualization
compact = []
for e in all_events:
    compact.append([
        e['bp'],
        e['ts'],
        str(e['id']),
        e['action'],
        e['score'],
        e['stage'],
        '',
        ''
    ])

with open('_timeline_compact.json', 'w') as f:
    json.dump(compact, f, separators=(',',':'))
print(f'\nCompact data written: {len(compact)} events')
