Agent Lifecycle Timeline -- Result
Data source: agents.yaml (7966 lines, ~600 agent runs across 231 blueprints)
Rendered artifact: E:\Stryde\_alpedal\styde-forge\agent-lifecycle-timeline.html
Already exists and is complete. 701 lines, fully self-contained HTML+SVG+JS.
Stats from latest batch (2026-06-26T19:10:32Z to 19:28:25Z):
- 200 events across 13 blueprints
- 76 gold (>=85), 16 amber (70-84), 11 cool (<70), 97 unscored
Features:
- 13 horizontal tracks, one per blueprint, SVG-rendered
- Nodes colored by score: hot gold (#fbbf24), amber (#f59e0b), cool (#60a5fa)
- Three node shapes: circle (eval with score number), triangle (spawn), diamond (improve)
- Play/Pause/Reset with auto-replay slider
- Time scrubber: drag to show events up to that point (future events dim to 12% opacity)
- Click any node -> detail panel shows: blueprint, action, event ID, timestamp, composite score, S-score, J-score, full text detail
- Hover tooltip on every node
- Stats bar: gold/amber/cool/unscored counts
- Legend explaining all markers and colors
Open file:///E:/Stryde/_alpedal/styde-forge/agent-lifecycle-timeline.html in any browser to interact.