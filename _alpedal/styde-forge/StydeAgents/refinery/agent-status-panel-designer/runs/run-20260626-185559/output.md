agents-status-panel-designer v1
10 mockups
---
mockup-01: shell-grid compact
layout: grid
grid-template-columns: repeat(3, 1fr)
gap: 6px
background: #0a0e14
token:
  --cell-bg: #121620
  --cell-border: #1e293b
  --dot-running: #22c55e
  --dot-pending: #facc15
  --dot-completed: #3b82f6
  --dot-error: #ef4444
  --text-dim: #64748b
  --text-bright: #e2e8f0
  --score-green: #4ade80
  --score-yellow: #fbbf24
  --score-red: #fb7185
states:
  idle: cell-border dim, text-dim, no dot
  running: cell-border green-pulse, dot-running pulsing, score-green
  pending: cell-border yellow, dot-pending static, score-yellow
  completed: cell-border blue, dot-completed static, score-green
  error: cell-border red, dot-error blink, score-red
format:
  each cell: agent-name on line 1, status-dot + score on line 2, task-count on line 3
  line-separator: single space
  no borders between lines within one cell
validation:
  --dot-running pulse uses css animation with opacity keyframes, no box-shadow
  --cell-border green-pulse uses animation: border-pulse 2s ease-in-out infinite
  @keyframes border-pulse { 0%,100% { border-color: #1e293b } 50% { border-color: #22c55e } }
  all keyframes defined before usage, no shorthand fallback issues
---
mockup-02: card-deck with progress-rings
layout: grid
grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))
gap: 16px
background: #0f1117
token:
  --card-bg: #1a1d27
  --card-radius: 12px
  --card-shadow: 0 4px 24px rgba(0,0,0,0.3)
  --ring-size: 48px
  --ring-stroke: 4px
  --ring-track: #2a2d3a
  --ring-fill-running: #22c55e
  --ring-fill-pending: #facc15
  --ring-fill-completed: #3b82f6
  --ring-fill-error: #ef4444
  --ring-animation: stroke-dashoffset 1.5s ease-in-out
  --text-name: #f1f5f9
  --text-meta: #94a3b8
  --score-font: monospace 1.4rem
states:
  idle: ring-track full, no fill, card-shadow dim
  running: ring-fill animating stroke-dashoffset, card-shadow green-glow
  pending: ring-fill static at 30%, card-shadow yellow-tint
  completed: ring-fill static at 100%, card-shadow blue-glow
  error: ring-fill red, ring-stroke width 6px, card-border red
format:
  top row: agent-name aligned left, score aligned right
  mid row: progress-ring centered, task-count below ring
  bottom row: status-text (running/pending/completed/error/idle) with time-elapsed
  ring technique: svg circle with stroke-dasharray and stroke-dashoffset, conic-gradient is not used because border-radius breaks border-image
validation:
  progress-ring uses SVG circle element not CSS conic-gradient
  conic-gradient approach was rejected by earlier audit for compatibility
  SVG circle: cx=24 cy=24 r=20 stroke-width=4 stroke-dasharray=125.6
  stroke-dashoffset maps to completion percentage: (1 - pct) * 125.6
  card-shadow green-glow uses box-shadow with rgba(34,197,94,0.25) spread 12px
  no filter:drop-shadow used for glow because cross-browser inconsistencies on Firefox
---
mockup-03: horizontal-bar dashboard
layout: flex column
gap: 8px
background: #0b0e14
token:
  --bar-bg: #1a1f2b
  --bar-height: 36px
  --bar-radius: 6px
  --bar-fill-running: linear-gradient(90deg, #22c55e, #4ade80)
  --bar-fill-pending: linear-gradient(90deg, #facc15, #fde047)
  --bar-fill-completed: linear-gradient(90deg, #3b82f6, #60a5fa)
  --bar-fill-error: linear-gradient(90deg, #ef4444, #f87171)
  --bar-fill-idle: #2a2f3d
  --label-width: 120px
  --stat-color: #94a3b8
  --score-badge-bg: #1e293b
states:
  idle: bar-fill-idle at 0% width, label dim
  running: bar-fill animating width from current to target, label bright
  pending: bar-fill 5% width, label yellow
  completed: bar-fill 100% width, label bright
  error: bar-fill red 70% width, label red-bright
format:
  each row: label in left column, bar in right column
  inside bar: percentage text aligned right with 8px padding
  score badge at far right of bar
  row hover: bar-bg lightens by 8%, cursor pointer
  aggregated header row: total agents, running count, pending count, completed count, average score
validation:
  gradient bar uses background-image linear-gradient not border-image
  width transition uses transition: width 0.6s cubic-bezier(0.4,0,0.2,1)
  width is set via inline style style="width: {pct}%"
  animation uses requestAnimationFrame not css animation for smooth progress
  label column uses text-overflow ellipsis for long agent names
---
mockup-04: orbital hub-and-satellite
layout: css position relative with absolute satellites
center: hub-circle diameter 120px
satellites: 8 agents max, evenly spaced on orbital radius 200px
background: #080b12
token:
  --hub-bg: radial-gradient(circle, #1e293b, #0f172a)
  --hub-text: #f1f5f9
  --hub-size: 120px
  --orbit-radius: 200px
  --satellite-size: 48px
  --satellite-running: #22c55e border
  --satellite-pending: #facc15 border
  --satellite-completed: #3b82f6 border
  --satellite-error: #ef4444 border
  --satellite-idle: #475569 border
  --connector-line: #1e293b 1px
  --glow-running: 0 0 12px rgba(34,197,94,0.4)
  --glow-error: 0 0 16px rgba(239,68,68,0.5)
states:
  hub shows aggregate: X running, Y pending, Z completed, avg-score center
  each satellite: agent initial, tooltip on hover, pulse-ring around running agents
  running: satellite-border green, glow running, satellite rotates slowly (animation: orbit-spin 20s linear infinite)
  pending: satellite-border yellow, no glow, static position
  completed: satellite-border blue, subtle ring, static
  error: satellite-border red, glow error, bounce animation
  idle: satellite-border gray, no effects, opacity 0.6
format:
  hub center: outer ring shows total agents, inner shows avg score
  satellite: letter-in-circle, border-color = status
  connector: line from hub edge to satellite center, opacity 0.3
  running agents have a dashed second orbit ring at +10px
  error agents get a triangle warning icon overlaying their circle
validation:
  orbit positioning uses transform: rotate(angle) translateX(200px) rotate(-angle)
  this avoids manual top/left calculation per agent
  animation orbit-spin rotates the whole satellite group, but individual satellites counter-rotate to keep text upright
  satellite counter-rotation: .satellite { animation: inherit } .satellite-text { animation: counter-spin 20s linear infinite }
  hub radial-gradient uses background-image not background shorthand to avoid old safari issues
  tooltip on hover uses title attribute HTML attribute, not css-only pseudo-element (accessibility)
---
mockup-05: kanban-column flow
layout: grid grid-template-columns: 4fr 1fr 1fr
columns: running | pending | completed | error
background: #0d1117
token:
  --col-bg: #161b22
  --col-header-bg: #1c2333
  --col-radius: 8px
  --card-bg: #1c2333
  --card-border: #30363d
  --card-radius: 6px
  --card-shadow: 0 1px 4px rgba(0,0,0,0.2)
  --running-indicator: #22c55e
  --pending-indicator: #facc15
  --completed-indicator: #3b82f6
  --error-indicator: #ef4444
  --col-header-text: #e6edf3
  --col-count-bg: #21262d
states:
  running column: agents with green indicator dot, show progress bar per card
  pending column: agents with yellow dot, no progress bar, show queue position
  completed column: agents with blue dot, show score, show completion time
  error column: agents with red dot, show error count, show last-error-time
  idle: agents not displayed in any column (filter toggle)
format per card:
  first line: agent-name with status dot inline
  second line: score-badge + task-count
  third line: time-elapsed (running) or queue-position (pending) or completed-at (completed) or error-message (error truncated 30 chars)
  fourth line (optional): actions button row
  card hover: card-border lightens, card-shadow elevates to 0 4px 12px rgba(0,0,0,0.3)
  column header: column-name + count badge
  column empty state: dashed border, faded text "no agents"
validation:
  card-shadow elevation uses transition on box-shadow, no transform: translateY to avoid layout recalculation
  count badge uses inline-flex with min-width 20px, height 20px, border-radius 9999px
  columns scroll independently with overflow-y auto and custom scrollbar styling
  drag-and-drop is visual only for mockup — no JS required for static preview
  error-message truncation uses text-overflow: ellipsis with white-space: nowrap and overflow: hidden
---
mockup-06: terminal-tui minimal
layout: grid grid-template-columns: 1fr 1fr 2fr
columns: agent | status | details
background: #0a0a0a
token:
  --tui-bg: #0a0a0a
  --tui-text: #c0c0c0
  --tui-bright: #ffffff
  --tui-green: #33ff33
  --tui-yellow: #ffff33
  --tui-blue: #33aaff
  --tui-red: #ff3333
  --tui-dim: #555555
  --tui-border: #222222
  --tui-cursor-blink: animation cursor-blink 1s step-end infinite
states:
  running: bright green text, cursor-blink adjacent line
  pending: yellow text, no cursor
  completed: blue text, dim
  error: red text, bold
  idle: gray text, dim
format:
  header row: AGENT, STATUS, SCORE, TASKS with tui-dim border-bottom
  each agent row: fixed-width columns using whitespace padding (monospace font)
  column widths: agent 18ch, status 10ch, score 6ch, tasks 8ch
  footer row: totals with tui-bright
  running indicator: green dot ascii `o` before agent name
  pending indicator: yellow dot ascii `~`
  completed indicator: blue dot ascii `*`
  error indicator: red dot ascii `!`
  idle: gray dot ascii `-`
  selected agent row (hover): tui-bg lightens to #141414, subtle underline
validation:
  no CSS animations except cursor-blink
  all effects are color changes and static layout
  monospace font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace
  column alignment uses tabular-nums font-variant for score column
  hover uses :hover pseudo-class background-color change only
  no transitions or transforms needed
---
mockup-07: gauge-panel array
layout: grid grid-template-columns: repeat(4, 1fr)
gap: 20px
max-columns: 4, wrap to next row
background: #0e1118
token:
  --gauge-bg: #161c26
  --gauge-radius: 60px
  --gauge-stroke-width: 6px
  --gauge-track: #262d3d
  --gauge-fill-running: #22c55e
  --gauge-fill-pending: #facc15
  --gauge-fill-completed: #3b82f6
  --gauge-fill-error: #ef4444
  --gauge-fill-idle: #475569
  --gauge-needle: #e2e8f0
  --gauge-needle-width: 2px
  --gauge-label: #94a3b8
  --gauge-value: #f1f5f9
  --scope-size: 140px
states:
  idle: gauge-track only, no fill, needle at 0, value dim
  running: gauge-fill arcs from 0 to current-progress, needle follows, value bright green
  pending: gauge-fill at 25% yellow, needle at 25%, value yellow
  completed: gauge-fill at 100% blue, needle at 100%, value bright blue
  error: gauge-fill at current-red, needle at current, value red bold, gauge-fill stroke-width doubles
format:
  gauge rendered as SVG arc: center 70 70, radius 55, stroke-width 6
  arc drawn with stroke-dasharray 345.6, stroke-dashoffset = (1 - pct) * 345.6
  needle line: from center (70,70) angled by pct * 360 degrees
  rotation: transform rotate(deg 70 70)
  below gauge: agent-name truncated 12ch
  below name: score as 2-digit number
  running gauge: arc animates using transition on stroke-dashoffset 0.8s ease
  gauge color transitions use transition: stroke 0.4s ease
validation:
  gauge uses svg not canvas, not conic-gradient background
  stroke-dasharray for full arc at r=55: 2 * pi * 55 = 345.6
  needle rotation uses transform origin 70 70
  SVG viewBox=0 0 140 140 preserveAspectRatio=xMidYMid meet
  transition on SVG attributes works in all modern browsers
  no requestAnimationFrame needed, pure CSS transitions on SVG stroke-dashoffset and stroke
---
mockup-08: pulse-wave timeline
layout: flex column
gap: 4px
background: #0a0d14
token:
  --wave-bg: #11151f
  --wave-line: #1e293b
  --wave-active: #22c55e
  --wave-pending: #facc15
  --wave-completed: #3b82f6
  --wave-error: #ef4444
  --wave-amplitude: 20px
  --wave-frequency: 4s
  --wave-height: 40px
  --dot-size: 8px
  --label-width: 100px
  --timestamp-color: #64748b
states:
  idle: flat line, no dot, label dim
  running: sine wave animating horizontally, green dot pulsing at right edge, label bright
  pending: flat line with gentle bump shape, yellow dot static, label yellow
  completed: flat line fading from blue to dim, blue dot at end, label bright blue
  error: jagged spike pattern (sawtooth), red dot blinking, label red bold
format:
  each row: label column 100px | wave area flex-grow 1 | timestamp column 80px
  wave area: SVG path drawn horizontally
  running wave: pathMath = sine function with animation via stroke-dashoffset
    pathData: M 0 20 Q 20 0, 40 20 T 80 20 T 120 20 ... for 200px
    animation: stroke-dashoffset from 200 to 0 over wave-frequency
  pending wave: single Gaussian bump using cubic bezier
    pathData: M 0 20 C 40 20, 60 0, 80 20 C 100 40, 120 20, 140 20
  completed wave: straight line at baseline, dot at right
    pathData: M 0 20 L 200 20
  error wave: sawtooth pattern using L segments
    pathData: M 0 20 L 10 0 L 20 40 L 30 0 L 40 40 L 50 20
  right side of wave area: status dot (dot-size)
validation:
  SVG path animation uses stroke-dasharray + stroke-dashoffset + animation
  sine wave is pre-computed points not JS-generated for static mockup
  wave-height fixed at 40px, SVG viewBox="0 0 200 40"
  pulse dot uses animation: pulse-opacity 1.5s ease-in-out infinite
  @keyframes pulse-opacity { 0%,100% { opacity: 1 } 50% { opacity: 0.3 } }
  sawtooth pattern is static SVG — no animation needed for error state
---
mockup-09: stacked-layer visualization
layout: css position relative stacking overlapping panels
layer-order: background agents (completed) -> mid agents (running) -> top agents (pending/error)
background: #0b0f17
token:
  --layer-bg: #141a26
  --layer-active-bg: #1a2236
  --layer-offset-x: 12px
  --layer-offset-y: 8px
  --layer-scale: 0.97
  --layer-z-base: 1
  --layer-z-increment: 2
  --stack-max: 5
  --border-completed: #3b82f6 40
  --border-running: #22c55e
  --border-pending: #facc15
  --border-error: #ef4444
  --border-idle: #334155
  --score-size: 32px
  --name-size: 14px
states:
  completed: stacked at bottom layers, scaled down layer-scale, faded opacity 0.5, blue border-left 3px
  running: mid layers, full scale, bright, green border, z-index higher
  pending: near-top layers, slightly right offset, yellow border, opacity 0.9
  error: top layer, pushed rightmost offset, red border, opacity 1.0, slight rotate 1deg
  idle: bottom-most, opacity 0.3, no border, half width
format:
  each layer card: width 280px, height 80px
  card content: agent-name at top-left, score ring at top-right, status text bottom-left, elapsed-time bottom-right
  layer offset formula: nth-layer translates (n * layer-offset-x)px right and (n * layer-offset-y)px down
  layer scale formula: nth-layer scales by pow(layer-scale, n)
  hover on any layer: brings that layer to front with z-index 100, shifts it left to x=0, full opacity
  hover transition: all 0.3s cubic-bezier(0.4,0,0.2,1)
  top agent: most visible, shows full detail with score ring and status
validation:
  layer stacking uses z-index not translateZ to avoid 3d rendering quirks in Chrome
  layer offset uses translateX and translateY on the card element
  scale uses transform: scale(num) with transform-origin: top left
  hover reset uses transform: translate(0, 0) scale(1) on the hovered element, all others shift further
  max 5 visible layers; additional agents shown as +N overflow badge
  overflow badge: circle 24px with +N text, bottom-right of stack
  no filter:blur for background layers, only opacity to avoid GPU compositing on large stacks
---
mockup-10: split-view master-detail
layout: grid grid-template-columns: 1fr 2fr
gap: 0
background: #0c101a
token:
  --master-bg: #111721
  --master-width: 360px
  --master-item-bg: #161d2b
  --master-item-hover: #1c2436
  --master-item-active: #1f2a40
  --master-radius: 6px
  --detail-bg: #0c101a
  --detail-header-bg: #111721
  --divider-color: #1e293b
  --divider-width: 1px
  --accent-running: #22c55e
  --accent-pending: #facc15
  --accent-completed: #3b82f6
  --accent-error: #ef4444
  --accent-idle: #475569
states:
  master-item states:
    idle: master-item-bg, dot gray, no badge
    running: master-item-active (if selected) or master-item-hover (if hovered), green dot, running badge
    pending: yellow dot, queue badge
    completed: blue dot, check badge
    error: red dot, exclamation badge, bg red tint
  detail-panel states:
    header: agent-name, status-bar, total score
    body: recent-tasks column, stats-grid column
    footer: actions bar
format master list:
  scrollable column with overflow-y auto
  each item: status-dot (8px circle) | agent-name (truncated 20ch) | score (aligned right) | running-indicator (pulsing dot if running)
  active item: left border 3px solid accent-color, background master-item-active
  item height: 56px, padding 12px 16px
  divider between master and detail: 1px solid divider-color
format detail panel:
  top section: large agent-name (1.2rem), status text, elapsed time
  mid-left section: stats grid 2x2 — active-time, tasks-total, success-rate, avg-score
  mid-right section: mini-timeline of recent activity (last 5 events)
  bottom section: action buttons — view-logs, restart, config, details
  empty detail state (no agent selected): centered text "Select an agent to view details" with dim opacity
  error state in detail: alert banner at top with error message, truncated 2 lines
validation:
  master-detail layout uses css grid with fixed first column width: grid-template-columns: 360px 1fr
  scroll on master only: overflow-y: auto, max-height: calc(100vh - header-height)
  divider is a border-right on master column, not a separate element
  detail-panel stats grid uses sub-grid or nested grid grid-template-columns: 1fr 1fr
  mini-timeline uses vertical layout with left-edge connector line and dots for each event
  timeline dot colors match event type: task-complete=blue, task-start=green, error=red
  no overflow issues: both columns have overflow hidden for content that exceeds bounds
  action buttons use inline-flex with gap 8px, no wrapping
---
summary table
mockup | layout-scheme | primary-visual | best-for | complexity
01 | compact grid | colored dots + border pulse | dense dashboards, ops views | low
02 | card grid | SVG progress rings | per-agent detail | medium
03 | flex column | horizontal gradient bars | aggregate overview | low
04 | orbital position | hub + satellite circles | novel UIs, demos | high
05 | kanban grid | column-based flow | pipeline tracking | medium
06 | fixed-width table | ASCII monospace | terminal UIs, logs | low
07 | grid of SVG arcs | circular gauges | performance metrics | medium
08 | flex + SVG paths | pulse waveform | timeline awareness | medium
09 | absolute stack | overlapping layers | space-constrained | high
10 | split grid | master list + detail panel | deep inspection | medium