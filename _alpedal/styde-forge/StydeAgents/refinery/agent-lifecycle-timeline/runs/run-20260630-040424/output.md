Blueprint: agent-lifecycle-timeline
Persona: data-visualization-engineer / time-series-storyteller
Version: 1
Input source: state.yaml
Parse: extract every agent run with run_id, blueprint_name, timestamp, version, stage, score, benchmark
Output: SVG timeline
Layout:
  SVG viewBox: 0 0 1200 (height dynamic: 60px per track + 40px header)
  X-axis: linear time scale, min=first timestamp, max=last timestamp
  Y-axis: one horizontal track per unique blueprint_name, evenly spaced
Nodes:
  shape: circle, radius=8
  position: x mapped to timestamp, y centered on blueprint track
  fill:
    score >= 85: #FFD700 (hot gold)
    score >= 70 and < 85: #FF8C00 (amber)
    score < 70: #4682B4 (cool steel blue)
  stroke: #333, width=1
  title attribute: run_id
Time scrubber:
  element: HTML input type=range
  min: epoch_ms(first_timestamp)
  max: epoch_ms(last_timestamp)
  step: 1000
  oninput: filter visible nodes to those with timestamp <= scrubber value
  autoplay button: setInterval advancing scrubber at 2x speed, play/pause toggle
Click handler:
  target: circle node
  behavior: show detail popup (div overlay or SVG foreignObject)
  fields:
    run_id: string
    blueprint: string
    version: string
    stage: string
    score: number
    benchmark: string
Data pipeline:
  read_file(path='state.yaml') -> parse YAML -> flatten into event list -> sort by timestamp -> render SVG + scrubber controls
Constraints:
  one track per blueprint, not per agent instance
  agents on same blueprint share same track, ordered left-to-right by timestamp
  no track for blueprints with zero runs
  empty state: display 'No agent lifecycle data found in state.yaml' centered in SVG