Panel 1: Agent Grid Overview
+------------------+------------------+------------------+
| AGENT: teacher   | AGENT: coder     | AGENT: evaluator |
| SCORE: 92.4      | SCORE: 87.1      | SCORE: 74.5      |
| STATUS: running  | STATUS: idle     | STATUS: error    |
| RUN: 14          | RUN: 9           | RUN: 22          |
| DUR: 2m34s       | DUR: 0m12s       | DUR: 17m08s      |
| [=====O===] 52%  | [==========] 100%| [!!]            |
+------------------+------------------+------------------+
| AGENT: writer    | AGENT: archiver  | AGENT: planner   |
| SCORE: 88.9      | SCORE: --        | SCORE: 79.2      |
| STATUS: pending  | STATUS: blocked  | STATUS: running  |
| RUN: 7           | RUN: 3           | RUN: 31          |
| DUR: 1m01s       | DUR: 4m55s       | DUR: 8m12s       |
| [=====     ] 45% | [@@@] dep:forge  | [========O ] 89% |
+------------------+------------------+------------------+
Panel 2: Collapsed Single Agent Card
AGENT: teacher (92.4)
STATUS: running  RUN: 14  DUR: 2m34s  PROGRESS: 52%
[=========O=========================================]
  active skill: evaluate-answer | current: step 3/6
Panel 3: Expanded Agent Detail
AGENT: teacher                        SCORE: 92.4  PEAK: 94.8
STATUS: running (2m34s)            RUN #: 14/231  DUR: 2m34s
PHASE: evaluate      STEP: 3 of 6      SUB: 12 of 45
PROGRESS
[===============O===========================] 52%
  prompt generation  [DONE]   36/36
  evaluation phase   [ACTIVE] 12/45
  score aggregation  [WAIT]   0/1
  archive            [WAIT]   0/1
RECENT OUTPUT
  line 12: Score 94/100 for answer #47
  line 13: Evaluating answer #48...
  line 14: Score 89/100 for answer #48
HEALTH METRICS
  avg score:      92.4  | trend: +1.2
  completion:%   100%   | errors: 0
  latency p50:   1.2s  | p95: 3.8s
  throughput:    14/min | tokens: 12.4k
ACTIONS [start] [stop] [reset] [view logs] [archive]
Panel 4: Status Indicators Legend
ICON   LABEL      MEANING
[RUN]  running    agent is actively processing
[IDL]  idle       agent ready, no current work
[PND]  pending    agent queued, waiting for slot
[BLK]  blocked    agent waiting on dependency
[ERR]  error      agent failed with recoverable error
[CRS]  crashed    agent failed unrecoverably
[DN]   done       agent completed successfully
[ARC]  archived   agent retired from active roster
Panel 5: Health Dashboard Bar
ALL AGENTS  [12 running] [3 idle] [2 pending] [1 blocked] [1 error]
SCORE DISTRIBUTION
  90-100:  |||| (4)
  80-89:   ||||| (5)
  70-79:   ||| (3)
  <70:     | (1)
SYSTEM HEALTH
  queue depth: 2  | avg latency: 2.1s | error rate: 1.2%
  tokens used: 847k of 2M quota | throughput: 112 req/min
Panel 6: Linter / Validation Output Block
VALIDATION: agent_status_panel_design_v1
  STRUCTURAL INTEGRITY
    [PASS] 6 mockup panels present
    [PASS] status indicator legend covers 8 states
    [PASS] health dashboard includes score distribution
    [PASS] expanded detail includes health metrics + actions
  FORMAT CONSISTENCY
    [PASS] no markdown formatting used
    [PASS] panel delimiters symmetrical (max 84 chars wide)
    [PASS] agent cards aligned in 3-column grid
  COMPLETENESS
    [PASS] collapsed and expanded view variants both included
    [PASS] linter/validation section self-referenced
    [PASS] no placeholder text or TBD markers
RESULT: ALL CHECKS PASSED | STYLE: caveman-ultra | VERSION: fas-0.5