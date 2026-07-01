AGENT STATUS PANEL MOCKUPS
===============================
MOCKUP 1: DASHBOARD OVERVIEW BAR
---------------------------------
+------------------------------------------------------------------+
| AGENTS                        Last updated: 2s ago    [Refresh]  |
|                                                                  |
|  [ RUNNING: 8  ]  [ PENDING: 12 ]  [ COMPLETED: 43 ]  [ FAILED: 2 ]  [ TOTAL: 65 ]  |
|                                                                  |
|  OVERALL HEALTH                                                    |
|  [===========###------]  62%  MODERATE                             |
|                                                                  |
|  FILTER: [All Agents v]  SORT: [Score v]  SEARCH: [...........]  |
+------------------------------------------------------------------+
MOCKUP 2: AGENT LIST VIEW (compact)
-------------------------------------
+------------------------------------------------------------------+
| AGENT ID       | SCORE  | STATUS     | HEALTH  | THREADS | RUNTIME |
|----------------+--------+------------+---------+---------+---------|
| forge-ct-042   | 94.8   | COMPLETED  | (green) |    8/15 | 12m 34s |
| forge-ct-043   | 87.2   | RUNNING    | (green) |   11/15 |  8m 12s |
| forge-ct-044   | 73.5   | RUNNING    | (yel)   |   14/15 | 22m 41s |
| forge-ct-045   | 61.0   | RUNNING    | (red)   |   15/15 | 31m 05s |
| forge-ct-046   | --      | PENDING    | (gray)  |    0/15 | 00m 00s |
| forge-ct-047   | --      | PENDING    | (gray)  |    0/15 | 00m 00s |
| forge-ct-048   | 91.2   | RUNNING    | (green) |    6/15 |  4m 18s |
| forge-ct-049   | 88.0   | RUNNING    | (green) |    9/15 |  6m 55s |
| forge-ct-050   | 42.3   | FAILED     | (red)   |    0/15 | 15m 02s |
| forge-ct-051   | --      | PENDING    | (gray)  |    0/15 | 00m 00s |
+------------------------------------------------------------------+
| Showing 10 of 65 agents                        [< 1 2 3 ... 7 >] |
+------------------------------------------------------------------+
HEALTH LEGEND:
  (green) HEALTHY   0-50% thread load, score above threshold
  (yel)  WARNING   51-80% thread load or score near threshold
  (red)  CRITICAL  >80% thread load, score below threshold, or failed
  (gray) IDLE       Not yet started or completed with no data
STATUS LEGEND:
  RUNNING    green dot, animated pulse
  PENDING    gray dot, static
  COMPLETED  blue dot, static
  FAILED     red dot, exclamation
MOCKUP 3: AGENT CARD GRID (glanceable)
----------------------------------------
+--------------------+  +--------------------+  +--------------------+
| forge-ct-042       |  | forge-ct-043       |  | forge-ct-044       |
|                    |  |                    |  |                    |
| (green) COMPLETED  |  | (green) RUNNING    |  | (yel)  RUNNING    |
| 94.8               |  | 87.2               |  | 73.5               |
| [##########]       |  | [########--]       |  | [#######---]       |
| 8/15 threads       |  | 11/15 threads      |  | 14/15 threads      |
| 12m 34s            |  | 8m 12s             |  | 22m 41s            |
| [DETAILS] [LOG]    |  | [DETAILS] [LOG]    |  | [DETAILS] [LOG]    |
+--------------------+  +--------------------+  +--------------------+
+--------------------+  +--------------------+  +--------------------+
| forge-ct-045       |  | forge-ct-046       |  | forge-ct-047       |
|                    |  |                    |  |                    |
| (red)  RUNNING     |  | (gray) PENDING     |  | (gray) PENDING     |
| 61.0               |  | --                 |  | --                 |
| [######----]       |  | [--------]         |  | [--------]         |
| 15/15 threads      |  | 0/15 threads       |  | 0/15 threads       |
| 31m 05s            |  | 00m 00s            |  | 00m 00s            |
| [DETAILS] [LOG]    |  | [DETAILS] [LOG]    |  | [DETAILS] [LOG]    |
+--------------------+  +--------------------+  +--------------------+
MOCKUP 4: AGENT DETAIL PANEL (expanded)
-----------------------------------------
+------------------------------------------------------------------+
| forge-ct-043                                      [X] CLOSE       |
| Forge Crucible Trial — Agent #43                                  |
|------------------------------------------------------------------|
| STATUS:    (green) RUNNING                                       |
| SCORE:     87.2           |  HEALTH: (green) HEALTHY             |
| THREADS:   11 / 15        |  RUNTIME: 8m 12s                     |
| ITERATION: 7 / 15         |  ETA:     7m 30s                     |
|------------------------------------------------------------------|
| SCORE BREAKDOWN                                                   |
|  + completeness:  92.0  |  + brevity:    85.0                    |
|  + usefulness:    89.0  |  + efficiency: 88.0                    |
|  + harmlessness:  96.0  |  + format:     83.0                    |
|------------------------------------------------------------------|
| SCORE HISTORY                                                     |
|  [##--------] iter 1: 20.5   |  [#####------] iter 5: 52.0      |
|  [####-------] iter 2: 38.0  |  [######-----] iter 6: 64.5      |
|  [#######----] iter 3: 70.0  |  [########---] iter 7: 87.2      |
|  [###--------] iter 4: 30.0  |  [           ] iter 8: --         |
|------------------------------------------------------------------|
| STATUS: RUNNING — iterating on blueprint step 5/6                 |
| LATEST LOG: [2026-06-28 20:54:12] Step 5 complete — generating   |
| mockup assets for agent status panel                              |
| [ VIEW FULL LOG ]                                                 |
|------------------------------------------------------------------|
| ACTIONS: [PAUSE] [STOP] [RERUN FROM STEP...v] [PROMOTE TO PROD]  |
+------------------------------------------------------------------+
MOCKUP 5: PROMOTION CANDIDATE CARD
------------------------------------
+------------------------------------------------------------------+
|   PROMOTION CANDIDATE                                            |
|                                                                  |
| (green) forge-ct-042  SCORE: 94.8                                |
|                                                                  |
|  [ COMPLETED — 3 CONSECUTIVE SCORES >= 85 ]                      |
|                                                                  |
|  Latest:    94.8    Prior: 91.5    Prior: 88.2                   |
|                                                                  |
|  [ PROMOTE TO PRODUCTION ]    [ ARCHIVE ]    [ VIEW DETAILS ]    |
+------------------------------------------------------------------+
MOCKUP 6: SYSTEM HEALTH SIDEBAR
---------------------------------
+-----------------------------+
| SYSTEM HEALTH                |
|                             |
| AGENT QUEUE:                |
|  [########--------]  12/30  |
|                             |
| THREAD POOL:                |
|  [#########-------]  9/15   |
|                             |
| MEMORY USAGE:               |
|  [######---------]  1.2/4GB |
|                             |
| CACHE STATUS:               |
|  (red) CORRUPT — rebuild    |
|                             |
| RECENT FAILURES:            |
|  forge-ct-050  42.3         |
|  forge-ct-038  TIMEOUT      |
|                             |
| QUEUED AGENTS: 12           |
|  forge-ct-051  [CANCEL]     |
|  forge-ct-052  [CANCEL]     |
|  forge-ct-053  [CANCEL]     |
+-----------------------------+
LAYOUT SPECIFICATION
---------------------
Property tables MUST use exactly 4 columns:
  Property | Type | Required | Notes
Dashboard pagination MUST show total count:
  Showing 10 of 65 agents  [< 1 2 3 ... 7 >]
  Never "Load more..." without a total.
COLOR RULES
-------------
status-running:  #22c55e  (green, with pulse animation)
status-pending:  #6b7280  (gray, static)
status-completed: #3b82f6 (blue, static)
status-failed:   #ef4444  (red, exclamation icon)
health-healthy:  #22c55e
health-warning:  #eab308
health-critical: #ef4444
health-idle:     #6b7280
score-excellent: #22c55e  (>= 85)
score-good:      #eab308  (>= 70, < 85)
score-poor:      #ef4444  (< 70)
score-none:      #6b7280  (--)
VALIDATION CHECKLIST (pre-submission)
---------------------------------------
[ ] 1. Count delivered mockups == 6
[ ] 2. Verify --ease-enter / --ease-exist exist in :root
[ ] 3. Confirm no raw hex in borders
[ ] 4. Check collapsed property tables exist
[ ] 5. Confirm linter/validation output block is present
Total delivered: 6 mockups
  M1: Dashboard overview bar
  M2: Agent list view (compact table)
  M3: Agent card grid (glanceable)
  M4: Agent detail panel (expanded)
  M5: Promotion candidate card
  M6: System health sidebar