SVG saved to E:/Stryde/_alpedal/styde-forge/timeline.svg
52 000 chars, 1200x812px, dark theme
Data: 200 events across 21 blueprints from 20:15 to 03:44 UTC (7.5h)
Everything is baked from state.yaml - no fabrication.
Panel layout:
21 horizontal tracks, one per blueprint, sorted chronologically by first event
Each track shows:
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 812" style="background:#1a1a2e;font-family:monospace">
<defs><style>.tt { font-size:11px; fill:#ccc; }</style></defs>
Title + timerange at top
8 time markers (20:15 21:11 22:07 23:03 00:00 00:56 01:52 02:48 03:44)
Blueprint rows with alternating background (#222240 / #1e1e38)
Nodes:
  circle gold #FFB800 = eval self-score >=85
  circle amber #D4944C = eval 70-84
  circle blue #5A8FBF = eval <70 or no score
  diamond #888 = spawn
  rounded rect #666 = improve
Connector lines between first/last event per BP
Every node has <title> tooltip with Run#, blueprint, action, scores, timestamp
Legend at bottom
Scrubber bar with draggable gold thumb + Play button
Key observations visible in the timeline:
- 3d-data-terrain-explorer: dense cluster of 30 events early on (20:15-20:37), all gold 95+ scores, clearly a well-performing high-volume blueprint
- agent-lifecycle-timeline: spans whole timeline, 42 events, mixed scores from 10 to 92, most activity in the last hour 03:00-03:44
- observability-platform-builder: tight burst 22:32-22:54, 23 events, consistent 79 composite scores - stuck just under promotion threshold
- aesthetic-style-composer: two distinct clusters (early 20:41, late 02:00-03:22)
- agent-promotion-evaluator: early cluster 20:55-21:27 with gold 88-93 scores, then a single eval at 02:50
- sprint-coach: two clusters (22:03-22:52 and 03:14-03:32) with gold 86-92 in both
- Several BPs with single events (web-component-builder, live-collaboration-canvas, caveman-mode-enforcer, prompt-injection-defender) - early spawns that never completed