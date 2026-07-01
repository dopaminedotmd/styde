import re, json
from collections import defaultdict, Counter

with open('state.yaml', encoding='utf-8') as f:
    text = f.read()

# Find all activity list entries
entries = []
# Each entry: starts with '  - action:' or '- action:'
pattern = r'(?m)^\s*-\s+action:\s*(\S+)\s*\n(?:\s+blueprint:\s*(\S+)\s*\n)?(?:\s+detail:\s*(.*?)\s*\n)?(?:\s+id:\s*(\d+)\s*\n)?(?:\s+progress:\s*(\d+)\s*\n)?(?:\s+status:\s*(\S+)\s*\n)?(?:\s+timestamp:\s*[\"\']?(.*?)[\"\']?\s*\n?)?'

for m in re.finditer(pattern, text):
    ts = (m.group(7) or '').strip().strip("'\"")
    entries.append({
        'action': m.group(1),
        'blueprint': m.group(2) or '',
        'detail': (m.group(3) or '').strip().strip("'\""),
        'id': m.group(4) or '',
        'progress': m.group(5) or '',
        'status': m.group(6) or '',
        'timestamp': ts
    })

print(f'Total entries: {len(entries)}')

action_counts = Counter(e['action'] for e in entries)
print('Actions:', dict(action_counts))

bp_counts = Counter(e['blueprint'] for e in entries if e['blueprint'])
print(f'Blueprints: {len(bp_counts)}')
for bp, cnt in bp_counts.most_common(10):
    print(f'  {bp}: {cnt}')

scored = [e for e in entries if 'S:' in e['detail']]
print(f'\nScored entries: {len(scored)}')

# Find min/max timestamp
times = [e['timestamp'] for e in entries if e['timestamp']]
times.sort()
if times:
    print(f'Time range: {times[0][:16]} to {times[-1][:16]}')

# Per-blueprint timeline data
bp_data = defaultdict(list)
for e in entries:
    bp = e['blueprint'] or 'unknown'
    bp_data[bp].append(e)

# Output as JSON for consumption
output = []
for bp, evts in sorted(bp_data.items()):
    evts_sorted = sorted(evts, key=lambda x: x['timestamp'] or '')
    for e in evts_sorted:
        # Extract score
        m_score = re.search(r'S:([\d.]+)\s+J:([\d.]+)\s+C:([\d.]+)', e['detail'])
        s = None
        if m_score:
            s = {'S': float(m_score.group(1)), 'J': float(m_score.group(2)), 'C': float(m_score.group(3))}
        output.append({
            'bp': bp,
            'action': e['action'],
            'id': e['id'],
            'ts': e['timestamp'],
            'status': e['status'],
            'progress': e['progress'],
            'score': s,
            'detail_preview': e['detail'][:80]
        })

with open('_timeline_data.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=1)

print(f'\nWritten {len(output)} events to _timeline_data.json')
