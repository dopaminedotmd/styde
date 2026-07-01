Data parsed from state.yaml: 22 blueprints, 200 events, 87 eval scores.
Time range: 2026-06-29T19:49 to 2026-06-30T02:47
AGENT LIFECYCLE TIMELINE
Scale: each column ~6 min
Legend: G=Gold>=85, A=Amber 70-84, C=Cool<70, S=Spawn, I=Improve
19:50       20:20       20:50       21:20       21:50       22:20       22:50       23:20       23:50       00:20        01:00        01:40        02:20
3d-data-terrain-explorer
  G95 G95 I S G95 G95 I S G95 G95 I S G95 G95 I S G95 G95 I S G95 ... (50 events, best 95.2)
agent-promotion-evaluator
  G94 A81 A81 I S S G92 I I                                               (12 events, best 93.6)
gpu-monitor-visualizer
  G90                                                                      (2 events, best 90.0)
agent-lifecycle-timeline
  S S G88 I S S A81 C28 C28 I S S                                        (21 events, best 88.4)
ab-testing-statistician
  G88 G88 I S G88 G88 I S                                                 (10 events, best 88.0)
aesthetic-style-composer
  A79 I G87 G87 A73 A71 I S A81 A81 S G85 G85 I I A70                     (22 events, best 87.4)
caveman-mode-enforcer
  G87                                                                      (1 event, best 86.8)
dao-governance-designer
  S G87 G87 I                                                              (4 events, best 86.6)
sprint-coach
  A84 A75 A75 A79 A79 I A84 I S A80 I A79                                 (14 events, best 84.0)
data-cleaner
  S A84 C64 I                                                              (5 events, best 84.0)
clay-soft-interface-designer
  A84 S                                                                    (3 events, best 84.0)
customer-service-triage
  A83 I S A81 S C64 C64 I                                                  (9 events, best 83.0)
ai-copilot-query-panel
  A80 S C58 A79 S A81 A81 I                                                (8 events, best 81.0)
observability-platform-builder
  S A80 A80 S A80 A80 I S A80 A80 I S A80 A80 I S A80 I S A80 S           (23 events, best 79.6)
anomaly-detection-visualizer
  S S S C57                                                                (5 events, best 56.8)
animation-design-engineer
  S C55 I                                                                  (3 events, best 55.2)
customer-feedback-analyzer
  C51 I                                                                    (2 events, best 51.2)
color-palette-originator
  S                                                                        (1 event, no score)
web-component-builder
  S                                                                        (1 event, no score)
live-collaboration-canvas
  S                                                                        (1 event, no score)
prompt-injection-defender
  S                                                                        (1 event, no score)
web-security-engineer
  S S                                                                      (2 events, no score)
SUMMARY
  Blueprints: 22
  Total events: 200
  Eval scores: 87
  Gold >=85: 41 (47.1%)
  Amber 70-84: 35 (40.2%)
  Cool <70: 11 (12.6%)
  Average score of evals: 79.4
  Highest: 95.2 (3d-data-terrain-explorer, 24 gold runs)
  Lowest: 28.0 (agent-lifecycle-timeline)
TOP 5 BLUEPRINTS BY AGENT QUALITY
  1. 3d-data-terrain-explorer    95.2 - 24 gold agents, dominant
  2. agent-promotion-evaluator   93.6 - strong, 2 gold
  3. gpu-monitor-visualizer      90.0 - single gold agent
  4. agent-lifecycle-timeline    88.4 - 1 gold, 1 amber
  5. ab-testing-statistician     88.0 - 6 consecutive gold
BLUEPRINTS WITH NO SCORE YET
  color-palette-originator, web-component-builder, live-collaboration-canvas
  prompt-injection-defender, web-security-engineer - all stuck at spawn
The complete interactive HTML version (time scrubber, SVG tracks, clickable nodes, auto-play) has already been written to:
  E:\Stryde\_alpedal\styde-forge\agent_lifecycle_timeline.html (264 lines)
  E:\Stryde\_alpedal\styde-forge\_forge_timeline.html (639 lines, static SVG)
Rebuild command: python build_timeline.py > agent_lifecycle_timeline.html