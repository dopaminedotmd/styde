Refined blueprint incorporating both feedback rounds:
Agent Lifecycle Timeline
Domain: frontend
Version: 2
Purpose
Interactive timeline showing every agent spawn to eval to improve to promote cycle. Scrub through iterations with a time slider. Each agent is a horizontal track with nodes for each run. Click node to see full run details. Play/pause auto-replay mode.
Persona
Data visualization engineer. Time-series storytelling.
Skills
  Parse state.yaml for all agent runs with timestamps
  Render horizontal timeline with SVG: one track per blueprint
  Timeline nodes colored by score: hot gold=85+, amber=70-84, cool=below 70
  Time scrubber: drag slider or auto-play from first to last event
  Click node: detail popup with run_id, version, stage, score, benchmark
==== CHANGES INCORPORATED FROM TEACHER FEEDBACK ====
Clarity fix (from 20260628-181739):
  Rule: summary-first output
    Before any raw data or SVG rendering, emit a concise human-readable summary:
      pass/fail count
      key metrics
      top issues
    Keep raw terminal dumps in a collapsible section or separate output block.
    Impact: high
Completeness fix (from 20260629-230922):
  Phase order:
    Step 1: Parse state.yaml from target forge directory
    Step 2: Validate at least 1 real agent exists. Fail fast if file missing or empty. No mock data fallback.
    Step 3: Emit verification checkpoint to stdout: number of agents loaded, score range, date span
    Step 4: Render timeline using only live data
  Acceptance criteria for filtering and zoom:
    agent name/ID search box
    score range slider (min-max)
    time window zoom (independent from scrubber, adjustable viewport)
    List these as explicit deliverables in output
==== OUTPUT CONTRACT ====
On every run, emit:
phase: verify
  agents_loaded: <count>
  score_min: <float>
  score_max: <float>
  date_earliest: <timestamp>
  date_latest: <timestamp>
phase: summary
  total_nodes: <count>
  promoted: <count>
  archived: <count>
  in_progress: <count>
  top_issues: <array of strings>
phase: render
  timeline_type: svg_horizontal
  tracks: <count>
  color_map:
    gold: score >= 85
    amber: score 70-84
    cool: score < 70
  interactivity:
    - scrubber_drag
    - auto_play
    - node_click_detail
    - agent_search
    - score_filter
    - time_zoom