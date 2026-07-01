Agent Lifecycle Timeline v8 regenerated.
Output: E:\Stryde\_alpedal\styde-forge\agent-lifecycle-timeline-v8.html (318KB)
Data from state.yaml:
- 979 events across 95 blueprints
- 108 eval, 57 spawn, 814 improve
- Timespan: 2026-06-26T06:35 to 2026-06-30T04:37
- 11 promoted >= 85 / 95 blueprints
- Score range: 14.0 - 93.6
Generator: _build_timeline_v8.py (840 lines)
Reads state.yaml LIVE, outputs self-contained HTML with:
- Executive summary with stats grid
- Interactive SVG timeline: one horizontal track per blueprint
- Nodes colored by score: gold 85+, amber 70-84, cool <70
- Spawn=diamond, eval=circle, improve=square
- Time scrubber with play/pause auto-replay
- Click node: detail popup with run_id, version, stage, score, benchmark, source line
- Score trend arrows (up/down)
- Inter-run bezier connection edges (green=improving, blue=declining)
- Promotion threshold markers (85+)
- Blueprint filter dropdown
- Debounced resize handler
Open file:///E:/Stryde/_alpedal/styde-forge/agent-lifecycle-timeline-v8.html in browser.
To refresh with latest data: python _build_timeline_v8.py