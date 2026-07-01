Agent Status Panel Dashboard v1
Design mockup for Forge crucible dashboard
```
  FORGE AGENT STATUS  [4 active | 2 idle | 1 error]   last scan: 3s ago
  ┌─────────────────────────────────────────────────────────────────────┐
  │ AGENT           SCORE  STATUS  ITER  HEALTH  RUNTIME   OUTPUT      │
  ├─────────────────────────────────────────────────────────────────────┤
  │ teacher-alpha    92.4  RUNNING  7/15  ●●●●○   14m 23s  lesson-07   │
  │ mentor-bravo     87.1  PENDING  3/15  ●●●○○    8m 01s  rubric-03   │
  │ critic-charlie   45.0  ERROR   12/15  ●○○○○   22m 47s  crash-log   │
  │ builder-delta    90.8  COMPLETE 15/15 ●●●●○   19m 32s  blueprint   │
  │ analyst-echo     73.4  RUNNING  9/15  ●●●○○   11m 18s  review-06   │
  │ scanner-foxtrot  68.2  PENDING  0/15  ●●○○○    0m 00s  —           │
  │ tester-golf      91.0  COMPLETE 15/15 ●●●●○   17m 44s  coverage    │
  │ fixer-hotel      82.7  RUNNING  6/15  ●●●●○   13m 09s  patch-02    │
  └─────────────────────────────────────────────────────────────────────┘
  HEALTH KEY: ● active  ◐ degraded  ○ down
  STATUS KEY: RUNNING  PENDING  COMPLETE  ERROR  IDLE  QUEUED
```
Compact variant for 5+ agents in limited width:
```
  FORGE AGENT STATUS  [4/1/1/2]  5s
  ┌────────────────────────────────────────────┐
  │ AGENT       S R I H  AGENT       S R I H  │
  ├────────────────────────────────────────────┤
  │ teacher     92 07 ●  scanner     68 00 ◐  │
  │ mentor      87 03 ◐  tester-g    91 15 ●  │
  │ critic      45 12 ○  fixer-h     82 06 ●  │
  │ builder     90 15 ●  analyst     73 09 ●  │
  └────────────────────────────────────────────┘
```
Status distribution bar for dashboard header:
```
  AGENT HEALTH:  ●●●●●●●○○○  70% healthy
  STATUS:  RUNNING[3] PENDING[2] COMPLETE[2] ERROR[1]
```
Design principles:
1. Score column is first data field after name — the primary metric
2. Health dots use fixed 5-wide format: ●●●●● active, ●●●○○ degraded, ●○○○○ critical, ○○○○○ down
3. Status column uses VISIBLE COLOR-BLOCKED labels — RUNNING green, PENDING yellow, COMPLETE blue, ERROR red, IDLE gray, QUEUED cyan
4. Runtime column shows mm:ss precision only — hh:mm:ss is too wide, truncate at 60m to 1h+
5. Output column shows the current/last deliverable name — truncated to 12 chars with ellipsis if longer
6. Iteration column shows n/15 to give completion sense without separate progress bar
7. Table header is present at all times — never omit column labels
8. Last scan timestamp top-right — stale data indicator, if >30s flag with WARN text
Empty state:
```
  FORGE AGENT STATUS  [0 active | 0 pending]
  ┌──────────────────────────────────────────────┐
  │ No agents running. Launch a forge run to     │
  │ populate the status board.                    │
  │                                              │
  │  [Launch Run]  [Schedule Batch]              │
  └──────────────────────────────────────────────┘
```
Error detail state (popup below affected row):
```
  │ critic-charlie   45.0  ERROR   12/15  ●○○○○   22m 47s  crash-log   │
  │   ⚠ TypeError: agent.critic._eval_round() arg 3 — missing rubric  │
  │   Suggested fix: check eval-cache or re-run with --rebuild-indexes│
```
This design meets Fas 0.5 mockup specification. Ready for distillation into HTML prototype or CLI dashboard.