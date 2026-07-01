Mockup-1: Agent List View (8 agents visible)
```
AGENT STATUS DASHBOARD          Updated: 28 Jun 2026 14:03 UTC
ID  NAME             STATUS  HEALTH  SCORE  TASKS         UPTIME
--  ----             ------  ------  -----  -----         ------
A1  Hermes-Main      RUN     █████   97.2   12/12 done    14d 6h
A2  Claude-Dev       RUN     ████░   84.5   4/6 run       2d 11h
A3  GPT-Forge        BLOCK   ██░░░   62.1   1/8 queue     0d 9h
A4  Mistral-Code     IDLE    █████   99.8   0/0 idle      7d 0h
A5  DeepSeek-R1      RUN     ████░   88.3   7/9 run       5d 3h
A6  Gemini-Analyze   FAIL    █░░░░   41.0   0/3 stuck     0d 1h
A7  Llama-Critic     PEND    ████░   81.7   0/2 pend      3d 8h
A8  Qwen-Fast        RUN     █████   95.1   9/9 done      1d 4h
AGGREGATE           ACTIVE 8  MEAN 81.2  TASKS 33/43  SYSTEM OK
```
Mockup-2: Grid Card View (4 agents, landscape)
```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Hermes-Main      │  │ Claude-Dev       │  │ GPT-Forge        │  │ Mistral-Code     │
│ RUN              │  │ RUN              │  │ BLOCK            │  │ IDLE             │
│ ████████████ 97.2│  │ ████████░░░ 84.5│  │ ████░░░░░░░ 62.1│  │ ████████████ 99.8│
│ 12/12 done       │  │ 4/6 ████████░░  │  │ 1/8 ██░░░░░░░░  │  │ 0/0 —            │
│ [HEALTH] █████   │  │ [HEALTH] ████░   │  │ [HEALTH] ██░░░  │  │ [HEALTH] █████   │
│ uptime 14d 6h    │  │ uptime 2d 11h   │  │ uptime 0d 9h    │  │ uptime 7d 0h     │
│ last: spec v3    │  │ last: eval t2    │  │ last: prompt q  │  │ last: —          │
│ next: review 4a  │  │ next: code gen   │  │ next: retry(3)  │  │ next: —          │
└──────────────────┘  └──────────────────┘  └──────────────────┘  └──────────────────┘
```
Mockup-3: Single Agent Detail Panel (expanded)
```
AGENT: Hermes-Main               ID: A1    MODEL: deepseek-v4-flash
STATUS: ███ RUNNING              HEALTH: █████ 97.2/100
METRICS
  score        97.2 ━━━━━━━━━━━━━━━━━━━━ 99.8 peak
  accuracy     94.1 ━━━━━━━━━━━━━━━━━    96.0 peak
  efficiency   89.4 ━━━━━━━━━━━━━━━      92.1 peak
  usefulness   99.0 ━━━━━━━━━━━━━━━━━━━  99.8 peak
  clarity      91.6 ━━━━━━━━━━━━━━━━━    94.4 peak
TASK QUEUE                          HISTORY (last 10)
  done  spec-generation (14m ago)      ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
  done  code-review (9m ago)           │98│97│96│99│97│98│95│96│97│99│
  done  test-suite (4m ago)            ├──┼──┼──┼──┼──┼──┼──┼──┼──┼──┤
  run   mockup-design (─)              │14│13│12│11│10│ 9│ 8│ 7│ 6│ 5│
  pend  deploy-check                   └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘
  pend  user-feedback                   [5m] each bar
PERF: cpu 23%  mem 1.2G  tokens 142k  latency 0.8s
```
Mockup-4: Multi-Agent Comparison Panel
```
COMPARE: 4 agents selected                 Filter: all profiles
METRIC         HERMES  CLAUDE  MISTRAL  DEEPSEEK   BEST       WORST
------         ------  ------  -------  --------   ----       -----
SCORE          97.2    84.5    99.8     88.3       Mistral    Claude
ACCURACY       94.1    81.8    96.2     86.1       Mistral    Claude
EFFICIENCY     89.4    79.2    95.0     82.7       Mistral    Claude
USEFULNESS     99.0    86.0    100.0    90.1       Mistral    Claude
CLARITY        91.6    80.5    92.4     85.9       Mistral    Claude
TASKS DONE     12      4       0        7          Hermes     Mistral
UPTIME         14d     2d      7d       5d         Hermes     Claude
HEALTH         5.0     4.2     5.0      4.5        tie        Claude
COMPOSITE RANK    2nd     4th     1st      3rd      Mistral    Claude
```
Mockup-5: Agent Health Timeline (last 24 hours)
```
AGENT HEALTH WATCH            Scope: all agents       Refresh: 30s
HERMES    ████████████████████████████████████████  100% ok
CLAUDE    ████████████████████████░░██████████████   92% ok
MISTRAL   ████████████████████████████████████████  100% ok
DEEPSEEK  ████████████████████████████████████████  100% ok
GPT       ████████░░░░████░░░░░░░░████████████████   67% ok
LLAMA     ████████████████████████████████████████  100% ok
QEN       ████████████████████████████████████████  100% ok
                                                     12:00  18:00  00:00  06:00
                                                      ▄▄▄▄▄  ▄▄▄▄▄  ▄▄▄▄▄  ▄▄▄▄▄
EVENTS
  02:14  GPT-Forge   BLOCK   prompt queue full (retry 3/5)
  06:03  Claude-Dev  WARN    eval timeout -> retry
  11:40  Hermes-Main PASS    spec-v3 verified (score 97.2)
  13:22  Mistral     PASS    idle -> standby mode
```
Design tokens:
```
health-bar:   █████ = 90-100  ████░ = 70-89  ██░░░ = 50-69  █░░░░ = 0-49
status-icon:  RUN=RUN  IDLE=IDLE  BLOCK=BLOCK  FAIL=FAIL  PEND=PEND
score-bar:    fill █ = remaining  ░ = unused, 12 chars wide
timeline-bar: █ = uptime tick  ░ = downtime tick, 1 char = 15 min
metric-bar:   ━ = filled to current value  ─ = unfilled, 20 chars wide
heatmap:      █ = 95+  ▆ = 85-94  ▄ = 70-84  ░ = <70, 1 char = 1 tick
border:       ┌─┐│└┘ for cards  ─── for separators  │ for columns
```
States: show all 4 quadrants of agent lifecycle (healthy-running, degraded-running, blocked, idle) plus 2 boundary states (failed, pending). Each mockup covers a distinct information density tier: list (compact), grid (medium), detail (dense), compare (tabular), timeline (trend).