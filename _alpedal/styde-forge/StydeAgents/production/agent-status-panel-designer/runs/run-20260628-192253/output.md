Agent Status Panel — Fas 0.5 Mockup
=== LAYOUT: Overview Bar ===
Agent Status Panel
[master header bar]
  ALL AGENTS    FILTER: All | Active | Idle | Faulted    [Refresh] [Auto-refresh: on]
  Summary counters row:
  [12 Running]   [4 Pending]   [28 Idle]   [3 Faulted]   [2 Completed]
  Bulk action: [Stop Selected] [Restart Selected] [Archive Completed]
=== LAYOUT: Agent Cards Grid ===
Responsive grid, 3 columns at 1200px, 2 at 768px, 1 at 480px
Each card:
+------------------------------------------------------+
| [status dot] agent-voice-v3     [STOP] [RESTART]     |
| IDLE since 2026-06-28 21:00:01                       |
|                                                       |
| Score trajectory:  92  89  91  94  88  [sparkline]    |
| Current score: 88/100                                 |
|                                                       |
| Run count:  47   |   Uptime: 12h 31m                 |
| Last task:  summarize-transcript-9a2f                 |
| Next task:  (in queue: 3 ahead)                       |
|                                                       |
| Health bar: [████████░░░░░░] 67%                      |
+------------------------------------------------------+
=== STATUS DOT COLOR LEGEND ===
green:  Running          -- pulse animation (slow glow)
yellow: Pending/Queued   -- static  
blue:   Idle             -- static
red:    Faulted/Errored  -- blink animation
gray:   Completed/Stopped -- dimmed
white:  Unknown          -- question mark overlay
=== CARD STATES ===
STATE: Running
  [glowing green dot] agent-code-reviewer
  RUNNING  (task 4/12 — lint-check-services)
  Current score: 84/100  trending: up +3
  ETA: 45s remaining
  Health: [████████░░] 78%
STATE: Faulted
  [blinking red dot] agent-deployment-v2
  FAULTED since 2026-06-28 20:47:02
  Last error: Connection timeout (retry 3/3)  stacktrace available
  Score before fault: 72/100
  Actions: [VIEW LOGS] [RESTART] [PROMOTE BACKUP] [ARCHIVE]
STATE: Pending
  [yellow dot] agent-dataset-validator
  PENDING — waiting for resource: GPU queue (2 ahead)
  Estimated start: ~2 min
  Priority: medium
  Score from last run: 91/100
STATE: Completed
  [gray dot with checkmark] agent-benchmark-suite
  COMPLETED - 2026-06-28 19:32:14
  Final score: 95/100  high score: 97/100
  Duration: 23m 41s
  Output: 12 test cases passed, 0 failed
  [VIEW REPORT] [ARCHIVE] [RERUN]
=== FILTERED VIEW: Production Agents ===
Tab: Production
  agent-prod-v1      green   score: 92   health: 89%   uptime: 6d 14h
  agent-prod-v2      green   score: 94   health: 91%   uptime: 6d 14h
  agent-prod-v3      yellow  score: 78   health: 62%   uptime: 6d 14h  (pending review)
  [PROMOTE v3 to production] button only visible when agent is staged
=== FILTERED VIEW: Staging Agents ===
Tab: Staging
  agent-staging-b7f2  green   score: 87   runs: 3/3 passes
  agent-staging-c11a  red     score: 41   runs: 0/3 passes  (auto-archived)
  agent-staging-d403  yellow  score: 73   runs: 2/3 passes  (needs 1 more pass)
=== EXPANDED DETAIL VIEW (click card) ===
DETAIL: agent-voice-v3
  Status:       IDLE
  Score:        88/100 (trend: stable)
  Peak score:   94 at run #23
  Total runs:   47
  Last run:     summarize-transcript-9a2f (score 88, 45s)
  Next run:     (queued: 3 ahead)
  Uptime:       12h 31m
  Health:       67%  [metrics breakdown]
  SCORE HISTORY:
  Run  #44: 92
  Run  #45: 89
  Run  #46: 91
  Run  #47: 88
  [sparkline chart]
  PROMOTION STATUS:
  Staging:     passed (3 consecutive >=85)
  Production:  not promoted — run #47 scored 88, needs 3 consecutive >=85, currently 1/3
  ETA:         2 more scoring runs at >=85 to qualify
  ERRORS (last 5):
  2026-06-28 19:02  task-timeout  (auto-retry, resolved)
  2026-06-28 14:30  nil-response  (cache miss, resolved)
  2026-06-27 22:15  connection-refused  (host down, resolved)
=== METRICS PANEL (summary strip at top) ===
  AGENT METRICS                    LAST HOUR      LAST 24H      ALL TIME
  Total agents                     49             49            231
  Active (running + pending)       16             24            -
  Faulted                          3              5             12
  Completed                        2              18            1,847
  Avg score                       87.2           85.1          81.4
  Avg health                      72%            68%           -
  Total promotion candidates      4              9             38
  Auto-archived                   0              3             19
=== RESPONSIVE BREAKPOINTS ===
Desktop (>=1200px):
  3-column grid, full detail on card click, sticky metrics bar
Tablet (768-1199px):
  2-column grid, condensed cards (hide run count, last/next task)
Mobile (480-767px):
  1-column grid, flat list, only status dot + agent name + score, swipe for actions
Narrow (<480px):
  single-line rows, no cards, horizontal scroll on score sparkline