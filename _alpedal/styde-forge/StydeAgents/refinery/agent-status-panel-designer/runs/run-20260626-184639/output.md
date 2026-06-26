--- AGENT STATUS PANEL ---
Forge Dashboard Component
Design Spec v1 -- 2026-06-26
CORE LAYOUT
Top: 3 stat cards (running / pending / completed) in a row
Middle: Agent grid or compact list (toggleable)
Each agent card: status dot, name, current task, score bar, mini health widget
Bottom: System-wide health bar + resource usage mini-graph
COLOR SCHEME
Background: #0f1117
Card bg: #1a1d27
Border: #2a2d3a
Text primary: #e4e6ef
Text secondary: #7e8299
Accent green (active): #50cd89
Accent blue (pending): #7239ea
Accent amber (queued): #ffa800
Accent red (error): #f1416c
Score fill: gradient #50cd89 -> #7239ea
Health bar fill: green/yellow/red thin strip
--- STAT CARDS ROW ---
+------------------+  +-------------------+  +-------------------+
| [green dot]       |  | [blue dot]        |  | [amber dot]       |
| RUNNING           |  | PENDING           |  | COMPLETED         |
| 12                |  | 8                 |  | 347               |
| agents active now |  | in queue          |  | last 24h          |
+------------------+  +-------------------+  +-------------------+
Large digit (48px) left-aligned under label. Small descriptor text in secondary color.
--- AGENT CARD (compact list view) ---
[green] agent-refinery      refine BLUEPRINT_42.md   [=========80%===] 8.5/10  [###--] mem: 240MB
[green] agent-production    generate component       [=====50%=======] 7.2/10  [#####] mem: 480MB
[blue]  agent-evaluator     awaiting task...         [pending         ] ---/10  [----] mem: 0MB
[amber] agent-designer      draft sketch v3           [==========95%==] 9.1/10  [###--] mem: 190MB
[red]   agent-validator     FAILED: validation err   [XX--------------] ---/10  [!!!--] mem: 0MB
Status dot color + unicode glyph:
  green circle = running
  blue square = pending
  amber diamond = queued
  red X = error/failed
  grey dash = idle
Score bar: unicode block characters [=====--] filled = score out of 10
Health mini-bar: 5 chars [#####] [###--] [#----]
  each char = 20% health segment
  green block = healthy, yellow = degraded, red = critical
--- AGENT CARD (grid view) ---
+---------------------------+
| [green]                   |
| agent-refinery            |
| refine BLUEPRINT_42.md   |
|                           |
| SCORE      HEALTH  STATUS |
| 8.5/10     [#####] ALIVE  |
|                           |
| mem: 240MB | runtime: 14m |
| +---- progress bar ----+ |
+---------------------------+
Grid: 2-3 columns, cards sized ~320px wide. Hover shows expanded info.
--- SYSTEM HEALTH BAR ---
Bottom of panel:
Overall Health: [=========--------] 62%
CPU: [####------] 42%  |  MEM: [########--] 78%  |  AGENTS: [#########-] 92% stable
Thin horizontal bars (2px height). Percentage right-aligned.
--- SCORE TYPES ---
quality_score: float 0.0-10.0 (from eval pipeline)
task_progress: int 0-100%
health_score: computed from error rate + response time + memory trend
status_badge: alive | degraded | critical | idle | queued
--- INTERACTIONS ---
Click agent card -> opens detailed agent view (separate panel, not covered here)
Toggle button top-right: [grid view] / [list view]
Filter dropdown: all | running | pending | completed | error
Sort: by score | by name | by runtime
Auto-refresh: checkbox, 5s default
--- RESPONSIVE BREAKPOINTS ---
>=1200px: 3-column grid
>=768px: 2-column grid
<768px: single column list
--- DELIVERY NOTES ---
This design is for mockups stage (Fas 0.5). Next step: implement as HTML/CSS component on Forge dashboard :8765. Wire up to real agent data from forge.py eval pipeline. No templates. Unique animated pulse on active agents.