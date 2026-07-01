import yaml
with open('state.yaml','r') as f:
    data = yaml.safe_load(f)

bp_events = {}
for a in data.get('activity', []):
    bp = a.get('blueprint', 'unknown')
    if bp not in bp_events:
        bp_events[bp] = []
    bp_events[bp].append(a)

print(f'Total blueprints: {len(bp_events)}')
for bp in sorted(bp_events.keys()):
    evts = bp_events[bp]
    completed = [e for e in evts if e['status'] == 'complete' and e['action'] == 'eval']
    scores = []
    for e in completed:
        d = str(e.get('detail',''))
        if 'C:' in d:
            try:
                c = d.split('C:')[1].split()[0]
                scores.append(float(c))
            except:
                pass
    max_score = max(scores) if scores else 0
    min_ts = min(e['timestamp'] for e in evts)
    max_ts = max(e['timestamp'] for e in evts)
    high_count = sum(1 for s in scores if s >= 85)
    print(f'{bp}: {len(evts)} events, {len(scores)} scored evals, peak={max_score}, high85+={high_count}, range={min_ts[:16]}..{max_ts[:16]}')

# Detail for agent-lifecycle-timeline runs
print('\n=== AGENT-LIFECYCLE-TIMELINE RUNS ===')
bp = 'agent-lifecycle-timeline'
evts = sorted(bp_events[bp], key=lambda x: x['timestamp'])
for e in evts:
    print(f"  {e['timestamp']} | {e['action']:8s} | id={e['id']:3d} | {str(e.get('detail','')):40s} | {e['status']:8s} | {e['progress']:3d}%")
