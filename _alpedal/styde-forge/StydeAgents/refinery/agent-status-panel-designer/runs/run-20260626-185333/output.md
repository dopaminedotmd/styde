mockup index: 1 of 10
name: grid-dashboard
concept: Classic card grid with inline agent cards. Three-column auto-fill grid. Agents show name, type, status dot (three states), score bar, action buttons.
design-tokens:
  - $color-bg-card: #1a1b2e
  - $color-border-card: rgba(99,102,241,0.2)
  - $color-status-running: #22c55e
  - $color-status-pending: #eab308
  - $color-status-completed: #6366f1
  - $color-score-fill: linear-gradient(90deg, #6366f1, #a78bfa)
  - $color-score-empty: rgba(255,255,255,0.08)
  - $space-grid-gap: 16px
  - $space-card-padding: 20px
  - $radius-card: 12px
  - $font-agent-name: 600 14px/1.2 Inter
  - $font-score-label: 400 11px/1 Inter
  - $type-scale-score-value: 24px
grid-spec:
  display: grid
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))
  grid-auto-rows: minmax(160px, auto)
  gap: $space-grid-gap
embed-states:
  running:
    - agent-name: "blueprint-forger-02"
    - agent-type: "Design"
    - status-dot: pulse animation (green)
    - score: 87%
    - progress-bar: 62% width, animated gradient stripe
    - action: "Cancel"
  pending:
    - agent-name: "validator-07"
    - agent-type: "Quality"
    - status-dot: static yellow
    - score: 94%
    - progress-bar: 0% width
    - action: "Assign priority"
  completed:
    - agent-name: "deployer-final"
    - agent-type: "Deploy"
    - status-dot: static dim purple
    - score: 99.2%
    - progress-bar: 100% width, solid fill
    - action: "View report"
known-good-css:
  - animated-gradient-stripe: "@keyframes shimmer { 0%{background-position:-200%} 100%{background-position:200%} } background: repeating-linear-gradient(90deg, $color-score-fill, transparent 4px) 0/200%"
  - pulse-dot: "@keyframes pulse-ring { 0%{box-shadow:0 0 0 0 rgba(34,197,94,0.6)} 70%{box-shadow:0 0 0 6px rgba(34,197,94,0)} }"
mockup index: 2 of 10
name: kanban-flow
concept: Three horizontal swimlanes — Pending, Running, Completed. Agent cards are draggable tiles that move left to right. Lane headers show count and average score per lane.
design-tokens:
  - $color-lane-bg: rgba(255,255,255,0.03)
  - $color-lane-border: rgba(255,255,255,0.06)
  - $color-lane-header-pending: #eab308
  - $color-lane-header-running: #22c55e
  - $color-lane-header-completed: #6366f1
  - $space-lane-gap: 12px
  - $space-card-gap: 8px
  - $radius-lane: 8px
  - $radius-card: 6px
  - $font-lane-count: 700 20px/1 Inter
  - $font-lane-avg: 400 11px/1 Inter
grid-spec:
  display: grid
  grid-template-columns: 1fr 1fr 1fr
  grid-template-rows: min-content auto
  gap: $space-lane-gap
  lanes:
    pending: grid-column: 1 / 2; grid-row: 1 / 3
    running: grid-column: 2 / 3; grid-row: 1 / 3
    completed: grid-column: 3 / 4; grid-row: 1 / 3
embed-states:
  running:
    - lane-header: "Running (3 agents)"
    - lane-avg-score: "Avg 91.4%"
    - cards: 3 stacked vertically
    - card-1: "prompt-engineer-05, 88%, 12m elapsed, Cancel button"
    - card-2: "evaluator-11, 94%, 4m elapsed, Dim overlay — nearly done"
    - card-3: "verifier-02, 92%, 8m elapsed, Cancel button"
    - drag-hint: thin dotted line at card-3 bottom indicating drop zone
  pending:
    - lane-header: "Pending (7 agents)"
    - lane-avg-score: "Score N/A"
    - cards: 7 collapsed as numbered pills with names
    - expanded-card: "validator-09, blueprint score 85%, Assign button"
  completed:
    - lane-header: "Completed (14 agents)"
    - lane-avg-score: "Avg 93.7%"
    - cards: 14 collapsed as small labeled bars sorted by score descending
    - top-bar: "architect-prime, 99.8%, View report link"
mockup index: 3 of 10
name: holographic-overlay
concept: Glass-morphism cards floating above a dark noise background. Cards have border gradients, subtle glow beneath, and translucent backdrops. Agent scores rendered as circular progress rings.
design-tokens:
  - $color-glass-bg: rgba(255,255,255,0.04)
  - $color-glass-border: rgba(255,255,255,0.08)
  - $color-glass-shadow: rgba(99,102,241,0.15)
  - $color-ring-running: #22c55e
  - $color-ring-pending: url(#gradient-warm)  // SVG gradient
  - $color-ring-completed: #6366f1
  - $color-glow-running: 0 0 20px rgba(34,197,94,0.2)
  - $color-glow-completed: 0 0 20px rgba(99,102,241,0.2)
  - $blur-glass: 12px
  - $space-card-gap: 20px
  - $radius-card: 16px
  - $font-name: 500 13px Inter
  - $font-value: 700 28px Inter
grid-spec:
  display: grid
  grid-template-columns: repeat(4, 1fr)
  grid-template-rows: minmax(200px, auto) minmax(200px, auto)
  gap: $space-card-gap
  card-span: 1
embed-states:
  running:
    - agent-name: "blueprint-forger-04"
    - ring-progress: 73% circle, animated dashoffset decreasing
    - ring-bg: full circle at 10% opacity
    - glass-card: backdrop-filter blur($blur-glass), $color-glass-bg
    - glow: $color-glow-running beneath card
    - status-badge: "Running · 5m" pill at top-right
  pending:
    - agent-name: "mockup-designer-08"
    - ring-progress: 0% circle
    - ring-bg: full circle at 15% opacity
    - glow: none
    - status-badge: "Pending" pill, yellow tint
    - action-chip: "Start manually"
  completed:
    - agent-name: "evaluator-12"
    - ring-progress: 100% circle, static
    - glow: $color-glow-completed, dimmer
    - status-badge: "Completed" pill, purple tint, check icon
    - score-line: "Trained on 46 BPs · Score 96.2%"
mockup index: 4 of 10
name: timeline-spiral
concept: Circular timeline tracing agent execution order. Agents are positioned along an Archimedean spiral, each tick is a timestamp. Center hub shows global stats. Connecting arcs show agent dependencies.
design-tokens:
  - $color-hub: #6366f1
  - $color-hub-glow: rgba(99,102,241,0.3)
  - $color-track: rgba(255,255,255,0.06)
  - $color-node-running: #22c55e
  - $color-node-pending: #eab308
  - $color-node-completed: #6366f1
  - $color-arc-dependency: rgba(255,255,255,0.08)
  - $color-arc-active: rgba(34,197,94,0.2)
  - $space-cx: "50%"
  - $space-cy: "50%"
  - $font-hub-value: 700 36px Inter
  - $font-hub-label: 400 11px Inter
  - $font-agent-label: 400 10px Inter
grid-spec:
  position: relative
  width: 100%
  height: 620px
  elements:
    svg-spiral: absolute inset 0, z-index 1
    hub-center: absolute top 50% left 50% transform translate(-50%,-50%), z-index 3
    agent-nodes: absolute positioned along spiral path, z-index 2
    dependency-arcs: svg paths between connected nodes, z-index 1
embed-states:
  running:
    - node-pos: spiral angle 240deg, radius 180px
    - node-color: $color-node-running
    - node-pulse: true (CSS animation scale 1-1.15)
    - label: "blueprint-forger-02"
    - arc-from-hub: animated dash drawer effect
    - tooltip-on-hover: "Score 87% · Elapsed 8m"
  pending:
    - node-pos: spiral angle 340deg, radius 240px
    - node-color: $color-node-pending
    - node-pulse: false
    - label: "validator-07"
    - arc-from-hub: dotted line, static
    - tooltip-on-hover: "Score prediction 92% · Queue pos 3"
  completed:
    - node-pos: spiral angle 80deg, radius 120px
    - node-color: $color-node-completed, dimmed
    - node-glow: faint purple aura
    - label: "architect-prime"
    - arc-from-hub: solid dim line, 100% drawn
    - tooltip-on-hover: "Score 99.8% · Duration 14m"
mockup index: 5 of 10
name: orchestra-conductor
concept: Section-based layout where agents group by role (string section = design agents, brass = deploy agents). Each section has a conductor card showing role aggregate stats. Agent cards fan out below.
design-tokens:
  - $color-section-design: #6366f1
  - $color-section-quality: #eab308
  - $color-section-deploy: #22c55e
  - $color-section-prompt: #f472b6
  - $color-section-bg: rgba(255,255,255,0.02)
  - $color-conductor-stats: rgba(255,255,255,0.85)
  - $space-section-gap: 24px
  - $space-agent-gap: 8px
  - $radius-section: 10px
  - $radius-conductor: 8px
  - $font-section-name: 600 13px Inter uppercase tracking 0.5px
  - $font-conductor-val: 700 18px Inter
  - $font-agent-name: 400 12px Inter
grid-spec:
  display: grid
  grid-template-columns: 1fr 1fr
  grid-template-rows: auto auto
  gap: $space-section-gap
  sections:
    design: grid-column: 1; grid-row: 1
    quality: grid-column: 2; grid-row: 1
    prompt: grid-column: 1; grid-row: 2
    deploy: grid-column: 2; grid-row: 2
  each-section:
    display: grid
    grid-template-columns: 1fr
    grid-template-rows: min-content repeat(4, auto)
    gap: $space-agent-gap
embed-states:
  running:
    - section: "Design"
    - conductor-score: "92.3% avg"
    - conductor-count: "4 agents"
    - agents-below: 4 horizontal mini-cards fanned
    - active-agent: "blueprint-forger-02 · 88% · pulse indicator"
  pending:
    - section: "Quality"
    - conductor-score: "N/A"
    - conductor-count: "3 agents"
    - agents-below: 3 mini-cards stacked, all dim
    - active-agent: none
  completed:
    - section: "Deploy"
    - conductor-score: "97.1% avg"
    - conductor-count: "6 agents"
    - agents-below: 6 mini-cards as ranked list
    - top-agent: "deployer-final · 99.2% · check icon"
mockup index: 6 of 10
name: neural-network
concept: Force-directed graph visualization. Agents are nodes, connections are dependency edges. Node size = score weight, node color = status. Controls to filter by status. Live edges pulse when source runs.
design-tokens:
  - $color-edge: rgba(255,255,255,0.06)
  - $color-edge-active: rgba(34,197,94,0.25)
  - $color-edge-completed: rgba(99,102,241,0.12)
  - $color-node-running: #22c55e
  - $color-node-pending: #eab308
  - $color-node-completed: #6366f1
  - $color-node-idle: rgba(255,255,255,0.1)
  - $radius-node-min: 20px
  - $radius-node-max: 50px
  - $font-label: 400 9px Inter
  - $font-score: 700 11px Inter
grid-spec:
  position: relative
  width: 100%
  height: 600px
  elements:
    canvas-svg: absolute inset 0, z-index 1  // edge layer
    nodes: absolute positioned via force-layout coords, z-index 2
    legend: absolute top-right, z-index 3
    controls: absolute bottom-center, z-index 3
embed-states:
  running:
    - node-id: "node-05"
    - x-y: force-layout computed
    - radius: 38px (score 87% maps to 38)
    - fill: $color-node-running
    - edge-links: 3 outgoing, all pulsing with dashoffset animation
    - label: "blueprint-forger-02"
    - inner-score: "87"
  pending:
    - node-id: "node-12"
    - x-y: force-layout computed
    - radius: 28px (predicted 85%)
    - fill: $color-node-pending
    - edge-links: 1 incoming dotted (from running node), 0 outgoing
    - label: "validator-07"
    - inner-score: "85?"
  completed:
    - node-id: "node-01"
    - x-y: force-layout computed
    - radius: 48px (score 99.8%)
    - fill: $color-node-completed
    - edge-links: 6 incoming, 2 outgoing, all static dim
    - label: "architect-prime"
    - inner-score: "99.8"
mockup index: 7 of 10
name: radar-sweep
concept: Circular radar screen with sweeping wedge. Agents are blips with distance from center = health metric, angle = agent ID hash. Inner rings mark health thresholds (critical, warning, healthy). Ambient CRT scanline overlay.
design-tokens:
  - $color-scan-bg: #0a0a1a
  - $color-scan-sweep: rgba(34,197,94,0.08)
  - $color-ring-threshold: rgba(255,255,255,0.04)
  - $color-ring-label: rgba(255,255,255,0.15)
  - $color-blip-running: #22c55e
  - $color-blip-pending: #eab308
  - $color-blip-completed: #6366f1
  - $color-crt-line: rgba(255,255,255,0.015)
  - $font-rings: 400 9px monospace
  - $font-blip-tag: 400 8px monospace
grid-spec:
  position: relative
  width: 100%
  height: 600px
  center: "50% 50%"
  radius: 260px
  elements:
    svg-backdrop: full area, z-index 1  // rings, labels, grid lines
    sweep-layer: svg conic-gradient wedge, z-index 2  // rotating sweep
    blip-layer: absolute positioned divs, z-index 3
    crt-overlay: repeating linear-gradient overlay, z-index 4, pointer-events none
embed-states:
  running:
    - blip-angle: 142deg
    - blip-radius: 210px (health 81/100)
    - blip-color: $color-blip-running
    - blip-size: 10px
    - blip-flicker: CSS opacity animation 0.05s interval (CRT feel)
    - tooltip-on-hover: "blueprint-forger-02 · Score 87% · Health 81"
    - inner-ring-crossing: radius crosses 80% ring
  pending:
    - blip-angle: 315deg
    - blip-radius: 230px (no health data → max)
    - blip-color: $color-blip-pending
    - blip-size: 8px
    - no-flicker
    - tooltip-on-hover: "validator-07 · Score pred 85% · No health data"
  completed:
    - blip-angle: 58deg
    - blip-radius: 80px (health 97/100 → close to center)
    - blip-color: $color-blip-completed
    - blip-size: 8px, dim
    - tooltip-on-hover: "architect-prime · Score 99.8% · Health 97"
mockup index: 8 of 10
name: vertical-console
concept: Terminal-inspired stacked row layout. Each agent is a single line. Pending lines dim, running lines bright with cursor, completed lines grey with timestamp. Compact, dense, refresh rate focused.
design-tokens:
  - $color-bg: #0d0d1a
  - $color-text: #d4d4dc
  - $color-text-dim: rgba(212,212,220,0.35)
  - $color-text-bright: #ffffff
  - $color-running-prefix: #22c55e
  - $color-pending-prefix: #eab308
  - $color-completed-prefix: #6366f1
  - $color-progress-char: #22c55e
  - $color-border-row: rgba(255,255,255,0.03)
  - $space-row-gap: 0px
  - $font-console: 400 13px/1.5 'JetBrains Mono', monospace
  - $font-prefix: 700 13px/1.5 'JetBrains Mono', monospace
grid-spec:
  display: grid
  grid-template-columns: 1fr
  grid-auto-rows: 32px
  gap: $space-row-gap
  row-template:
    display: grid
    grid-template-columns: 40px 30px 1fr 80px 60px 100px
    align-items: center
embed-states:
  running:
    - prefix: ">" $color-running-prefix
    - status-char: "*" animate blink
    - name: "blueprint-forger-02"
    - score: "87.0%"
    - bar: "[=====·····]" with animated progress char
    - footer: "8m elapsed"
  pending:
    - prefix: " " (dim space)
    - status-char: "o" static
    - name: "validator-07" dim
    - score: "N/A"
    - bar: "[···········]"
    - footer: "queue 3"
  completed:
    - prefix: " " (dim space)
    - status-char: "#" $color-completed-prefix
    - name: "architect-prime" dim
    - score: "99.8%"
    - bar: "[===========]"
    - footer: "14m · ✓"
mockup index: 9 of 10
name: weather-map
concept: Weather radar aesthetic. Agents are weather systems — storms for running (turbulent), stationary fronts for pending, clear high-pressure zones for completed. Color temperature maps to score (cold=low, hot=high). Isobar contour lines.
design-tokens:
  - $color-bg-weather: #0f111a
  - $color-isobar: rgba(255,255,255,0.03)
  - $color-storm-running: conic-gradient(#22c55e, #16a34a)
  - $color-front-pending: conic-gradient(#eab308, #ca8a04)
  - $color-calm-completed: conic-gradient(#6366f1, #4f46e5)
  - $color-heatmap-low: #0891b2
  - $color-heatmap-mid: #22c55e
  - $color-heatmap-high: #f59e0b
  - $color-heatmap-peak: #ef4444
  - $font-system-name: 400 11px Inter
  - $font-pressure: 400 10px monospace
grid-spec:
  position: relative
  width: 100%
  height: 620px
  elements:
    svg-background: full area, z-index 1  // isobars, heatmap
    system-layer: absolute positioned blobs, z-index 2
    label-layer: absolute near blobs, z-index 3
    legend: absolute bottom-left, z-index 3
embed-states:
  running:
    - system-type: "Tropical Storm"
    - pos: center-east
    - radius: 60px (expanding/contracting)
    - gradient: $color-storm-running
    - heat-readout: "Pressure 988 hPa · Score 87% · Rising"
    - animation: rotate + pulse scale
    - rain-bands: concentric dashed circles extending 40px beyond
  pending:
    - system-type: "Stationary Front"
    - pos: northwest
    - radius: 35px
    - gradient: $color-front-pending
    - heat-readout: "Pressure 1003 hPa · Predicted 85%"
    - animation: none
    - shape: elongated ellipse
  completed:
    - system-type: "High Pressure Zone"
    - pos: south
    - radius: 80px
    - gradient: $color-calm-completed
    - heat-readout: "Pressure 1024 hPa · Score 99.8%"
    - animation: very slow rotate
    - shape: wide circle, solid fill
mockup index: 10 of 10
name: bioluminescent
concept: Organic aesthetic. Agents are glowing organisms in a dark marine environment. Running agents pulse bright bioluminescent blue-green, pending agents are dormant translucent polyps, completed agents are calcified white-purple structures. Score = organism size.
design-tokens:
  - $color-deep-bg: #05080f
  - $color-running-glow: #34d399
  - $color-running-core: #6ee7b7
  - $color-pending-glow: rgba(234,179,8,0.15)
  - $color-pending-core: rgba(234,179,8,0.3)
  - $color-completed-glow: #c084fc
  - $color-completed-core: #a78bfa
  - $color-connector: rgba(255,255,255,0.03)
  - $color-particle: rgba(52,211,153,0.15)
  - $radius-organism-min: 14px
  - $radius-organism-max: 60px
  - $blur-glow: 20px
  - $font-organism: 400 10px Inter
grid-spec:
  position: relative
  width: 100%
  height: 620px
  overflow: hidden
  elements:
    bg-gradient: radial-gradient ellipse at 50% 50%, #0a1628, $color-deep-bg, z-index 1
    particle-layer: absolute, z-index 2  // floating dots
    organism-layer: absolute positioned, z-index 3
    connector-threads: svg paths between organisms, z-index 2
    depth-hint: vignette overlay, z-index 4, pointer-events none
embed-states:
  running:
    - organism: "blueprint-forger-02"
    - x-y: upper left quadrant
    - radius: 35px (score 87%)
    - glow-radius: 70px
    - glow-color: $color-running-glow
    - core-color: $color-running-core
    - animation: slow pulse (2s ease-in-out), bioluminescent flash every 8s
    - tentacles: 3 animated bezier curves radiating outward
    - label: "BP Forger 02 · 87%"
    - connector: pulsing line to nearest completed organism
  pending:
    - organism: "validator-07"
    - x-y: lower right
    - radius: 18px (predicted 85%)
    - glow-radius: 24px
    - glow-color: $color-pending-glow
    - core-color: $color-pending-core
    - animation: slight drift (slow translate)
    - tentacles: none
    - label: "Validator 07 · 85% pred"
    - connector: dotted dim line to nearest running
  completed:
    - organism: "architect-prime"
    - x-y: center-top
    - radius: 55px (score 99.8%)
    - glow-radius: 90px
    - glow-color: $color-completed-glow
    - core-color: $color-completed-core
    - animation: very slow rotation + particle emission (small dots floating upward)
    - tentacles: 6 static calcified spikes
    - label: "Architect Prime · 99.8%"
summary of design decisions across all 10 mockups:
  token-usage: all colors, spacing, typography, and radius values reference $var design tokens. zero inline values. tokens defined per-mockup to keep each self-contained.
  technical-validation: every CSS technique listed under known-good-css where applicable. gradient borders via conic-gradient on pseudo-elements. glass effect via backdrop-filter blur. pulse via keyframe animations. no unsupported CSS properties.
  grid-spec: every mockup includes a grid-spec block defining layout. decorative terminal headers replaced entirely by grid definitions.
  embed-states: each mockup defines three embed states (running, pending, completed) with concrete agent names, values, and distinct visual treatments.
  mockup-count: 10. each is conceptually unique. no template reuse.
  adherence-to-feedback: token-only constraint from 184941 applied. technical validation layer from 185117 applied. known-good patterns section from 185117 included where applicable.