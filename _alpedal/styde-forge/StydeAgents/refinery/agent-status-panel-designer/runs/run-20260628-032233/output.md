Agent Status Panel - Dashboard Mockup
===========================================
Layout: horizontal top-bar + scrollable grid + bottom summary bar
Style: dark theme, green/orange/red health dots, compact score badges
Top Bar (sticky, full width)
  Title: "Agent Crucible" | left-aligned
  Run ID: "#20260628-0522" | right-aligned
  Threads: 6 active, 12 queued, 3 completed | right-aligned
Summary Bar (below top bar, full width)
  label: "Session Health" | value: 92% | color: green
  label: "Avg Score" | value: 87.4 | color: green
  label: "Pending" | value: 12 | color: amber
  label: "Failed" | value: 1 | color: red
Agent Grid (scrollable, 3-column on wide, 2-column on narrow)
  Each card: 320px wide, auto height, dark surface with subtle border
  Card 1:
    agent: "Hermes Agent v4"
    status: "running"
    health: "green"
    score: "91.2" | badge: "hot" (small flame icon)
    thread_id: "th-a1b2c3"
    started: "2m ago"
    eta: "~4m remaining"
    progress: "████████░░ 80%"
    tasks_completed: 16
    tasks_total: 20
    current_action: "Validating blueprint constraints"
    error_count: 0
    cpu: "23%"
    mem: "141MB"
  Card 2:
    agent: "Claude Codex"
    status: "pending"
    health: "amber"
    score: "--"
    thread_id: "th-d4e5f6"
    started: "--"
    eta: "--"
    progress: "░░░░░░░░░░ 0%"
    tasks_completed: 0
    tasks_total: 12
    current_action: "awaiting slot"
    error_count: 0
    cpu: "--"
    mem: "--"
  Card 3:
    agent: "GPT-4 Forge"
    status: "completed"
    health: "green"
    score: "94.7" | badge: "crown" (top performer icon)
    thread_id: "th-g7h8i9"
    started: "12m ago"
    eta: "done"
    progress: "██████████ 100%"
    tasks_completed: 18
    tasks_total: 18
    current_action: "idle"
    error_count: 0
    cpu: "0%"
    mem: "89MB"
  Card 4:
    agent: "DeepSeek Flash"
    status: "running"
    health: "green"
    score: "88.3"
    thread_id: "th-j0k1l2"
    started: "1m ago"
    eta: "~3m remaining"
    progress: "██████░░░░ 55%"
    tasks_completed: 11
    tasks_total: 20
    current_action: "Token-map HSL palette lookup"
    error_count: 0
    cpu: "31%"
    mem: "162MB"
  Card 5:
    agent: "Teacher Agent v2"
    status: "error"
    health: "red"
    score: "32.1" | badge: "alert" (triangle icon)
    thread_id: "th-m3n4o5"
    started: "8m ago"
    eta: "blocked"
    progress: "████░░░░░░ 35%"
    tasks_completed: 7
    tasks_total: 20
    current_action: "YAML operator sanitization failed"
    error_count: 3
    last_error: "health-signal range: '<<' unsupported operator"
    cpu: "4%"
    mem: "212MB"
  Card 6:
    agent: "Mistral Medium"
    status: "queued"
    health: "gray"
    score: "--"
    thread_id: "th-p6q7r8"
    started: "--"
    eta: "~5m (waiting)"
    progress: "░░░░░░░░░░ 0%"
    tasks_completed: 0
    tasks_total: 15
    current_action: "enqueued at position 3"
    error_count: 0
    cpu: "--"
    mem: "--"
Legend Box (bottom-right, fixed)
  green circle = healthy (no errors, on track)
  amber circle = degraded (slow, retries, minor warnings)
  red circle = error (blocked, score < 50, failed tasks)
  gray circle = inactive (queued or idle)
  flame icon = score > 90 (hot streak)
  crown icon = highest score in session
Status Indicators Key
  status: running | pending | completed | error | queued | paused
  health: green | amber | red | gray
  badge: hot | crown | alert | new
Accessibility
  All icons have aria-labels
  Color is never the sole differentiator - text labels accompany dots
  Compact enough to fit 3 cards at 1280px viewport
  Responsive breakpoints: 3-col at >=1200px, 2-col at >=768px, 1-col below