Agent Status Panel — Fas 0.5 Mockup
AGENT CARD (compact, 280px wide, single column)
+----------------------------------------+
| [icon] Agent Name            [status]  |
| Role: Blueprint Designer               |
| Score: 87.4/100  [=========>--] 87%    |
| Runs: 12 active | 3 pending | 45 done  |
| Health: [green] Operational            |
| Last: 2m ago    Next: in 14s          |
+----------------------------------------+
Status indicators (16x16 dot, left of name):
  green-filled #22c55e — running, healthy, recent activity <5m
  yellow-pulse #eab308 — pending, queued, or evaluating
  red-flash #ef4444 — error, stuck, or crashed >3 consecutive fails
  gray-dim #6b7280 — idle, completed, no pending work
  blue-ring #3b82f6 — training, generating, in-progress action
Score bar gradient:
  <50: red to amber
  50-69: amber to yellow
  70-84: yellow to green
  85+: green to emerald with sparkle #22c55e-#10b981
AGENT LIST VIEW (full-width rows)
| Icon | Name            | Score | Status    | Active | Pending | Done | Health     | Next Action     |
|------|-----------------|-------|-----------|--------|---------|------|------------|-----------------|
| [G]  | Blueprint Gen   | 91.2  | running   | 8      | 2       | 134  | excellent  | validate in 3s  |
| [Y]  | Feedback Eval   | 67.5  | evaluating| 3      | 7       | 89   | degraded   | awaiting input  |
| [R]  | Cache Migrator  | 0.0   | stuck     | 1      | 0       | 12   | critical   | manual fix req  |
| [B]  | Metrics Aggr    | 94.8  | idle      | 0      | 0       | 203  | excellent  | scheduled 12:00 |
Column widths: icon 40px, name 180px, score 80px, status 100px, active 60px, pending 60px, done 60px, health 100px, next action 140px.
Status color bar on left edge of row — 4px solid matching indicator color.
AGENT GRID (3-column dashboard tile)
+-------------------+-------------------+-------------------+
| Blueprint Gen     | Feedback Eval     | Cache Migrator    |
| Score 91.2        | Score 67.5        | Score 0.0         |
| [=====-] active 8 | [===----] active 3| [-------] stuck   |
| Health: excellent | Health: degraded  | Health: critical  |
| + Recent activity | + No recent eval  | ! Needs attention |
+-------------------+-------------------+-------------------+
Tile sizes: 320x180px, 8px rounded corners, 1px border matching status color at 30% opacity.
HEALTH BREAKDOWN PANEL (expandable detail)
Agent: Blueprint Gen
  Accuracy:   91/100 [=========-]  strong
  Completeness: 78/100 [=======---]  needs edge cases
  Consistency: 95/100 [==========]  excellent
  Usefulness:  84/100 [========- ]  good
  Latency:     240ms avg         [green]
  Error Rate:  1.2% last 50 runs [green]
  Stall Count: 0                 [green]
  Recovery:    automatic         [green]
RUN QUEUE (mini timeline, right sidebar)
+12:05:23  validate-output  completed  0.4s
+12:05:27  generate-spec    running    2.1s
+12:05:31  check-constraints pending
+12:05:40  report-metrics   pending
Line height 24px, timestamp in gray, action in white, status dot prefix.
STACKING CONTEXT (depth layers, back to front):
1. Grid background — dark #0f172a
2. Agent cards — surface #1e293b with status edge glow
3. Health bars — colored fill with animated pulse on active agents
4. Status indicators — top layer, z-index always above card content
5. Expand/hover overlays — glass #1e293bee, blur 8px, above all cards