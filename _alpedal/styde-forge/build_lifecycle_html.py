#!/usr/bin/env python3
"""
Build agent-lifecycle-timeline.html from _timeline_data.json.
Injects structured JSON data into the template placeholders.
"""
import json, re, sys
from datetime import datetime

SRC = '_timeline_data.json'
TEMPLATE = 'agent-lifecycle-timeline.html'

with open(SRC) as f:
    raw = json.load(f)

# Separate activity events (with 'action' field) and state records (agents.yaml data)
activity = [ev for ev in raw if 'action' in ev]
state = [ev for ev in raw if 'action' not in ev]

# Build records: one per meaningful event
records = []

# 1. Activity events: spawn, eval, improve
for ev in activity:
    ts = ev.get('timestamp', '')
    blueprint = ev.get('blueprint', '')
    action = ev.get('action', '')
    detail = ev.get('detail', '')
    eid = ev.get('id', '')

    score = None
    if 'S:' in detail:
        try:
            score = float(detail.split('S:')[1].split()[0].rstrip(','))
        except (ValueError, IndexError):
            pass

    records.append({
        'blueprint': blueprint,
        'ts': ts,
        'action': action,
        'detail': detail,
        'run_id': str(eid),
        'stage': action,  # treat activity action as stage for coloring
        'iteration': '',
        'status': ev.get('status', ''),
        'benchmark': '',
        'score': score,
        'diagnosis': '',
        'summary': ''
    })

# 2. State records: each represents a run (spawned_at as timestamp)
for s in state:
    blueprint = s.get('blueprint', '')
    ts = s.get('spawned_at') or s.get('timestamp', '')
    run_id = s.get('run_id', '')
    stage = s.get('stage', '')
    iteration = s.get('iteration', '')
    status = s.get('status', '')
    benchmark = s.get('benchmark', '')
    diagnosis = s.get('diagnosis', '')
    summary = s.get('summary', '')

    if not ts:
        continue

    records.append({
        'blueprint': blueprint,
        'ts': ts,
        'action': 'run',
        'detail': '',
        'run_id': run_id,
        'stage': stage,
        'iteration': str(iteration) if iteration is not None else '',
        'status': status,
        'benchmark': benchmark,
        'score': None,
        'diagnosis': diagnosis,
        'summary': (summary or '')[:200]
    })

# Sort by timestamp
records.sort(key=lambda r: r['ts'])

# Read template and inject
with open(TEMPLATE) as f:
    html = f.read()

json_str = json.dumps(records, ensure_ascii=False, default=str)
html = html.replace('%TIMELINE_DATA%', json_str)

with open(TEMPLATE, 'w') as f:
    f.write(html)

print(f'Injected {len(records)} records into {TEMPLATE}')
print(f'  {len(activity)} activity events')
print(f'  {len(state)} state records')
print(f'  Blueprints: {len(set(r["blueprint"] for r in records))}')
print(f'  Time range: {records[0]["ts"]} -> {records[-1]["ts"]}')
