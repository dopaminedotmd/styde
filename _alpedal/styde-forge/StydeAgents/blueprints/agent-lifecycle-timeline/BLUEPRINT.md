# Agent Lifecycle Timeline
**Domain:** frontend **Version:** 1

## Purpose
Interactive timeline showing every agent spawn→eval→improve→promote cycle. Scrub through iterations with a time slider. Each agent is a horizontal track with nodes for each run. Click node to see full run details. Play/pause auto-replay mode.

## Persona
Data visualization engineer. Time-series storytelling.

## Skills
- Parse state.yaml for all agent runs with timestamps
- Render horizontal timeline with SVG: one track per blueprint
- Timeline nodes colored by score: hot gold=85+, amber=70-84, cool=below 70
- Time scrubber: drag slider or auto-play from first to last event
- Click node: detail popup with run_id, version, stage, score, benchmark
