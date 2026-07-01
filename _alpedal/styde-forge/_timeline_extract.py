import yaml
with open('state.yaml','r') as f:
    data = yaml.safe_load(f)
events = []
for a in data.get('activity', []):
    if a.get('blueprint') == 'agent-lifecycle-timeline':
        events.append(a)
completed_evals = [e for e in events if e['action'] == 'eval' and e['status'] == 'complete' and 'C:' in str(e.get('detail',''))]
print(f'Total agent-lifecycle-timeline events: {len(events)}')
print(f'Completed evals with scores: {len(completed_evals)}')
for e in sorted(completed_evals, key=lambda x: x['timestamp']):
    print(f"  {e['timestamp']} | id={e['id']} | {e['detail']} | progress={e['progress']}")

# Also get all unique blueprints
all_bps = set()
for a in data.get('activity', []):
    all_bps.add(a.get('blueprint', ''))
print(f'\nAll blueprints ({len(all_bps)}):')
for bp in sorted(all_bps):
    bp_events = [e for e in events if e.get('blueprint') == bp]
    print(f'  {bp}: {len(bp_events)} events')
