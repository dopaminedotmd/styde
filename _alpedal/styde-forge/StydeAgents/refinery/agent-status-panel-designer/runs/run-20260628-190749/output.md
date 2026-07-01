agent-status-panel v1
layout: single-screen-dashboard
format: compact-grid
state: live-preview
AGENT STATUS PANEL
```
┌─────────────────────────────────────────────────────────────────────────────┐
│  AGENT STATUS  ──  12 active  │  3 pending  │  47 completed today          │
│  ▲ 1 failing  ◆ 8 healthy  ▼ 2 degraded                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  AGENT              SCORE    STATUS      RUNTIME    LAST RUN        HEALTH  │
│  ─────────────────────────────────────────────────────────────────────────  │
│  teacher-v4         92.4  ◆  processing   1m 12s    now              ● ● ●  │
│  writer-muse        89.8  ◆  processing   3m 04s    2s ago           ● ● ●  │
│  validator-phi      87.1  ■  pending      0m 00s    —                ● ● ◌  │
│  reviewer-alpha     91.0  ◆  completed    2m 31s    14s ago          ● ● ●  │
│  critic-omega       76.3  ⚠  completed    1m 54s    3m ago           ● ◌ ◌  │
│  summarizer-beta    94.7  ■  queued       0m 00s    —                ● ● ●  │
│  debugger-gamma     68.2  ✕  error        0m 48s    1m ago           ◌ ◌ ◌  │
│  planner-delta      85.5  ◆  processing   4m 12s    now              ● ● ●  │
│  coder-epsilon      83.0  ■  pending      0m 00s    —                ● ● ◌  │
│  tester-zeta        90.1  ◆  completed    0m 23s    45s ago          ● ● ●  │
│  architect-eta      79.4  ◆  completed    2m 09s    8m ago           ● ◌ ◌  │
│  orchestrator-theta   —  ◆  idle          12m 44s   12m ago          ● ● ●  │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ▲  TOP PERFORMERS                      ▼  NEEDS ATTENTION                  │
│  summarizer-beta  94.7  ●●●             debugger-gamma  68.2  ◌◌◌ ✕ error │
│  teacher-v4       92.4  ●●●             critic-omega    76.3  ◌◌◌           │
│  reviewer-alpha   91.0  ●●●             architect-eta   79.4  ◌◌◌           │
└─────────────────────────────────────────────────────────────────────────────┘
```
STATES & INDICATORS
status:
  processing: ◆  (animated dot, pulsing)
  completed:  ◆  (static dot, dim 30s after finish)
  pending:    ■  (square, queued)
  queued:     ■  (square, waiting)
  error:      ✕  (red cross)
  idle:       ◆  (static dot, dimmed)
health-dots: ● ● ●  (3-dot bar, green/gray)
  ● = healthy metric (latency, accuracy, throughput each green)
  ◌ = degraded metric (yellow or timeout)
  3 dots = 3 health dimensions
health-dimensions:
  - response-latency   (green <2s, yellow 2-5s, red >5s)
  - output-quality     (green >80, yellow 60-80, red <60)
  - run-stability      (green <2% error rate, yellow 2-10%, red >10%)
SCORE COLOR CODING
score-colors:
  threshold:
    - min: 90  color: bright-green  label: excellent
    - min: 80  color: green         label: good
    - min: 70  color: yellow        label: acceptable
    - min: 0   color: red           label: failing
PANEL BEHAVIOR
auto-refresh: 5s
sort-order: status then score descending
  processing first
  completed (recent first)
  queued/pending
  idle
  error last (always visible at bottom)
row-count: 12 visible, scroll remainder
click-action: opens agent-detail-panel (separate mockup)
error-persist: error rows stay visible until acknowledged or agent re-runs successfully
idle-timeout: agents idle >10m dim to 40% opacity
LAYOUT SPEC
header-bar:
  height: 3 lines
  content: summary counts + health bar
table-section:
  min-height: 14 rows
  border: compact (┌ ┐ └ ┘ ─ │)
  column-gap: 2 spaces
  columns: agent-name(18) score(6) status(12) runtime(8) last-run(12) health(9)
footer-quadrants:
  left: top-3 performers
  right: bottom-3 / needs-attention
ACCESSIBILITY
color-not-sole-indicator: true
  health dots shown as ●◌◌ but also spelled 'latency: ok | quality: warn | stability: fail' on hover
  status uses shape ◆ ■ ✕ not just color
RESPONSIVE BREAKPOINTS
breakpoints:
  wide (>1200px): full grid, 12 rows, footer quadrants visible
  medium (800-1200px): 8 rows, footer stacked vertically
  narrow (<800px): 6 rows, compact header, footer hidden (expandable)
DESIGN RATIONALE
compact-borders-justification: 5+ panels visible in mockup suite, single-panel deep-dives would use verbose ascii borders. efficiency vs readability tradeoff favors compact here because this panel lives alongside agent-detail, run-history, and composition-graph mockups in the same viewport.
build-guidance:
  implement-as: single html file with css grid + js polling
  data-source: /api/agents/status (json)
  refresh: setInterval 5000ms, fade-transition on score changes
  health-calculation: 3-dimension check on last 10 runs per agent
  priority-implementation: error highlighting > score colors > sort order > auto-refresh