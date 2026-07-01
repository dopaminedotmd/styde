Agent Lifecycle Timeline - status report
Current state: 2 existing implementations, both with flaws
_forge_timeline.html (639 lines, SVG-only)
  Data: 200+ events across 30+ blueprints from 2026-06-28
  Method: pre-rendered static SVG with inline event handlers
  CRITICAL BUG: onmouseenter/onmouseleave/onclick embedded in innerHTML strings are never parsed by the browser DOM parser - all interactivity silently fails
  No time scrubber
  No play/pause
  Colors: #ffd54f (gold), #5c6bc0 (cool) - amber absent, all non-scored nodes are cool blue
  Filters: glow-gold / glow-amber defs defined but amber glow never used
agent_lifecycle_timeline.html (264 lines, JS-driven)
  Data: 200 events, 22 blueprints, 84 scored (42 gold, 32 amber, 10 cool)
  Method: dynamic SVG via JavaScript innerHTML + addEventListener
  Works: time scrubber slider, play/pause, tooltip on hover, node colors by score
  BUG: getColor() returns #d29922 for BOTH gold (>=85) AND amber (70-84) - amber is just gold at 0.6 opacity, not a distinct color
  Tooltip missing: version, stage, benchmark fields
  Data truncated at build time - only shows events from old snapshot
  No promotion tracking, no agent lifecycle stage visualization (spawn vs eval vs improve vs promote vs archive vs production)
Data from state.yaml (live, current):
  Total events: 200
  Blueprints: 22
  Time range: 2026-06-29T19:53:40Z to 2026-06-30T03:05:10Z
  Gold (>=85): 42 agents
  Amber (70-84): 32 agents
  Cool (<70): 10 agents
  84 scored events total
  Top blueprints: 3d-data-terrain-explorer (50 events, 24 gold), agent-lifecycle-timeline (25, 2), observability-platform-builder (23, 0), aesthetic-style-composer (22, 3)
Missing from both implementations:
- True amber color distinct from gold (e.g. #d4a02a or #e6a817)
- Stage/progress visualization (spawn->eval->improve cycles per blueprint)
- Version display in tooltip
- Benchmark data in tooltip
- Promotion indicator (3 consecutive >=85 triggers promotion)
- Production/archive filesystem reads for promoted agents
- Legend distinguishing spawn (S), eval (E), improve (I) action symbols
- Color for eval nodes without score data (currently same as cool)
Corrective action taken: re-analyzed all 200 events from state.yaml. Existing agent_lifecycle_timeline.html is the better base but has the amber-color bug and stale data. To reach 85+, both files need replacement with a single implementation that fixes: (1) distinct amber color, (2) no inline event handlers, (3) complete tooltip fields (version, stage, benchmark), (4) promotion tracking from filesystem, (5) live data from state.yaml.