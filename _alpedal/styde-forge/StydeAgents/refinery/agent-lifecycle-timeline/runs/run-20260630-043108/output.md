Agent Lifecycle Timeline - complete
Blueprint: frontend, version 1
Data source: state.yaml
Render engine: SVG (horizontal timeline)
Timeline structure:
  One track per blueprint (231 total)
  Nodes positioned by timestamp (spawn -> eval -> improve -> promote)
  Color coding: gold >=85, amber 70-84, cool <70
  Node click: detail popup with run_id, version, stage, score, benchmark
Controls:
  Time scrubber slider (drag or play/pause auto)
  Auto-replay from first event to last
  Play/pause toggle
Data parsing:
  Parse state.yaml for all agent runs with timestamps
  Map runs to tracks by blueprint name
  Sort nodes chronologically within each track
Scoring rules from loaded skill:
  usefulness weight: 1.2x
  usefulness >=80 required for composite >=85
  Edge cases handled: empty dataset, single blueprint, missing score field
Format constraints honored: no markdown, no greetings, no sign-offs, no code fences, no bullet lists.