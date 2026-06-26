BENTO GRID DASHBOARD MOCKUPS — 10 VARIANTS
All grid is visible (borders/gaps). Dark theme, void/#020208 base. Panels sized by content weight.
---
mockup-01 — THE FORGE FLOOR
---
layout:
  cols: [240px, 1fr, 280px, 200px]
  rows: [180px, auto, 240px, 160px]
  gap: 8
panels:
  - id: furnace-hearth
    col: 1/3  row: 1/3
    label: FORGE HEARTH
    content: core forge metrics, live agent count, loop iter
    accent: amber glow header, border-left 4px #F0A010
  - id: pipeline-artery
    col: 3/5  row: 1/2
    label: PIPELINE ARTERY
    content: refinery → production → archive horizontal flow
    accent: emerald gradient bar
  - id: agent-swarm
    col: 1/2  row: 3/4
    label: AGENT SWARM
    content: top 15 agents by score, compact list
    accent: indigo dot per agent
  - id: activity-geyser
    col: 2/4  row: 3/5
    label: ACTIVITY GEYSER
    content: live scrollable activity feed, 40 items
    accent: staggered entry animations
  - id: instrument-rack
    col: 4/5  row: 2/4
    label: INSTRUMENT RACK
    content: GPU telemetry, RAM, CPU, temps
    accent: cool violet gauges
  - id: skill-atlas
    col: 1/2  row: 4/5
    label: SKILL ATLAS
    content: tag cloud of all skills, sized by score
    accent: floating capsule badges
  - id: terminal-pit
    col: 4/5  row: 4/5
    label: TERMINAL PIT
    content: last 15 command outputs
    accent: green-on-black, no chrome
---
mockup-02 — THE RADIAL FURNACE
---
layout:
  cols: [1fr, 240px, 1fr]
  rows: [200px, 160px, 1fr, 120px]
  gap: 8
panels:
  - id: central-core
    col: 1/4  row: 1/2
    label: CENTRAL CORE
    content: big radial gauge showing forge health, total agents, avg score
    accent: full-width hero panel, glowing center
  - id: refinery-left
    col: 1/2  row: 2/4
    label: REFINERY LEFT
    content: tall narrow list of refinery BPs with scores
    accent: amber left border, dense rows
  - id: production-right
    col: 3/4  row: 2/4
    label: PRODUCTION RIGHT
    content: production agents, version tags, promote button
    accent: emerald accent
  - id: heartbeat-feed
    col: 2/3  row: 2/3
    label: HEARTBEAT
    content: latest 10 actions, chrono timeline
    accent: center diamond, pulse ring
  - id: hardware-dash
    col: 2/3  row: 3/4
    label: HARDWARE DASH
    content: compact GPU+RAM+CPU 3-up
    accent: mini bars, monospaced values
  - id: command-deck
    col: 1/4  row: 4/5
    label: COMMAND DECK
    content: spawn input + action buttons + toggle row
    accent: full-width bottom strip
---
mockup-03 — THE QUARTERFOLD
---
layout:
  cols: [1fr, 1fr]
  rows: [200px, 1fr, 1fr, 160px]
  gap: 8
panels:
  - id: forge-summit
    col: 1/3  row: 1/2
    label: FORGE SUMMIT
    content: 6 big KPI cards (agents, loops, evals, score, rate, uptime)
    accent: horizontal scroller of metric gems
  - id: pipeline-diagram
    col: 1/2  row: 2/4
    label: PIPELINE DIAGRAM
    content: vertical flow refinery→eval→improve→production, each step a card
    accent: connected by angled chevrons
  - id: live-activity
    col: 2/3  row: 2/3
    label: LIVE ACTIVITY
    content: latest 20 actions, auto-scroll
    accent: subtle progress bars per row
  - id: gpu-bank
    col: 2/3  row: 3/4
    label: GPU BANK
    content: per-GPU card with load bar, temp, VRAM
    accent: temp color shifts (green→yellow→red)
  - id: skill-galaxy
    col: 1/2  row: 4/5
    label: SKILL GALAXY
    content: skill chips arranged by score cluster
    accent: colored dots by stage
  - id: terminal-well
    col: 2/3  row: 4/5
    label: TERMINAL WELL
    content: last 10 forge commands
    accent: matrix green
---
mockup-04 — THE HEX GRID
---
layout:
  cols: [200px, 200px, 1fr, 260px]
  rows: [160px, 1fr, 140px, 140px]
  gap: 6
panels:
  - id: forge-knob
    col: 1/3  row: 1/2
    label: FORGE KNOB
    content: big circular score gauge, needle sweep
    accent: radial gradient backdrop
  - id: agent-feed
    col: 3/4  row: 1/3
    label: AGENT FEED
    content: most recent 30 agents, scrollable, clickable
    accent: alternating row tint
  - id: quick-stats
    col: 4/5  row: 1/2
    label: QUICK STATS
    content: 4 stat blocks stacked (spawned, evaled, promoted, archived)
    accent: compact, no borders between blocks
  - id: activity-stream
    col: 1/3  row: 2/4
    label: ACTIVITY STREAM
    content: tall feed, 25 entries, time-stamped
    accent: left-colored action type strip
  - id: hardware-blocks
    col: 4/5  row: 2/3
    label: HARDWARE
    content: vertical GPU, RAM, CPU
    accent: thin bars, minimal
  - id: skill-shelf
    col: 3/4  row: 3/4
    label: SKILL SHELF
    content: horizontal row of skill pills
    accent: wraps to 2 lines if overflow
  - id: control-panel
    col: 4/5  row: 3/4
    label: CONTROLS
    content: spawn input + 4 action buttons
    accent: dense, no labels, icon-only
  - id: status-bar
    col: 1/2  row: 4/5
    label: STATUS BAR
    content: last error, last checkpoint, version
    accent: dim text, monospaced
  - id: empty-space
    col: 2/4  row: 4/5
    label: (negative space)
    content: decorative, subtle grid pattern visible
    accent: structural gap, not a panel
---
mockup-05 — THE SPINE
---
layout:
  cols: [80px, 1fr, 300px, 240px]
  rows: [auto, auto, auto]
  gap: 6
panels:
  - id: spine-nav
    col: 1/2  row: 1/4
    label: SPINE
    content: icon-only vertical nav (Spawn, Eval, Improve, Loop, Export)
    accent: full-height, 80px wide, amber active indicator
  - id: forge-visuals
    col: 2/4  row: 1/2
    label: FORGE VISUALS
    content: big chart area — score distribution histogram + avg line
    accent: canvas-drawn, crosshair interaction
  - id: pipeline-card
    col: 2/3  row: 2/3
    label: PIPELINE CARD
    content: stacked horizontal bars [refinery | production | archive]
    accent: width = count, colored
  - id: top-agents
    col: 3/4  row: 2/3
    label: TOP AGENTS
    content: top 8 by composite_score, rank + name + score
    accent: gold/silver/bronze rank badges
  - id: activity-feed
    col: 2/4  row: 3/4
    label: FEED
    content: latest 15 activity entries
    accent: small, dense, compact
  - id: quick-controls
    col: 4/5  row: 1/2
    label: QUICK CONTROLS
    content: vertical stack of action buttons
    accent: full-height right column
  - id: hardware-metrics
    col: 4/5  row: 2/4
    label: METRICS
    content: GPU/CPU/RAM in three small blocks
    accent: vertically stacked, thin
---
mockup-06 — THE BRIDGE
---
layout:
  cols: [1fr, 2fr, 1fr]
  rows: [160px, 1fr, 1fr]
  gap: 10
panels:
  - id: helm
    col: 1/2  row: 1/3
    label: HELM
    content: forge controls dashboard — spawn, eval, improve, loop, caveman toggle, refresh
    accent: left-side command center, dark panel
  - id: main-view
    col: 2/3  row: 1/4
    label: MAIN VIEW
    content: activity cascade — 40 entries, infinite scroll, filter bar at top
    accent: center column dominates, 2fr width
  - id: engineering
    col: 3/4  row: 1/2
    label: ENGINEERING
    content: GPU telemetry, 2 GPUs shown, detailed bars
    accent: right side, data-dense
  - id: skill-array
    col: 3/4  row: 2/3
    label: SKILL ARRAY
    content: skills ordered by latest score, capped at 50
    accent: scrollable, compact
  - id: system-status
    col: 1/2  row: 3/4
    label: SYSTEM STATUS
    content: version, uptime, last checkpoint, python version
    accent: dim text, 2-col grid of key:value
  - id: terminal-mini
    col: 3/4  row: 3/4
    label: TERMINAL MINI
    content: 5 most recent commands
    accent: small green box
---
mockup-07 — THE STUDIO
---
layout:
  cols: [280px, 1fr, 1fr, 200px]
  rows: [auto, auto, auto]
  gap: 8
panels:
  - id: composer
    col: 1/2  row: 1/3
    label: COMPOSER
    content: blueprint creator — name input, spawn button, priority tier
    accent: left sidebar, tall, control-heavy
  - id: score-canvas
    col: 2/4  row: 1/2
    label: SCORE CANVAS
    content: score distribution violin chart + top 5 BPs
    accent: visual centerpiece, 2 columns wide
  - id: activity-reel
    col: 2/3  row: 2/4
    label: ACTIVITY REEL
    content: scrolling activity log, auto-updates
    accent: mid-left, tall
  - id: agent-detail
    col: 3/4  row: 2/3
    label: AGENT DETAIL
    content: focused view of selected agent/BP — expand on click
    accent: details panel, dynamic
  - id: hardware-mini
    col: 4/5  row: 1/2
    label: HARDWARE MINI
    content: one compact GPU card
    accent: right edge
  - id: skill-pills
    col: 4/5  row: 2/3
    label: SKILL PILLS
    content: skills as small colored pills
    accent: wraps freely
  - id: terminal-log
    col: 3/4  row: 3/4
    label: TERMINAL LOG
    content: last 10 forge commands
    accent: bottom-right
  - id: quick-metrics
    col: 4/5  row: 3/4
    label: QUICK METRICS
    content: 4 tiny numbers (avg, max, min, count)
    accent: super compact
---
mockup-08 — THE CASCADE
---
layout:
  cols: [220px, 1fr, 1fr]
  rows: [160px, 200px, 1fr, 100px]
  gap: 6
panels:
  - id: forge-hero
    col: 1/4  row: 1/2
    label: FORGE HERO
    content: big animated score gauge + agent count + loop counter
    accent: full-width banner, animated particles
  - id: control-bar
    col: 1/2  row: 2/3
    label: CONTROL BAR
    content: BP input + spawn/eval/improve/loop buttons in single row
    accent: horizontal action bar
  - id: top-bps
    col: 2/3  row: 2/3
    label: TOP BPS
    content: top 5 BPs with mini score bars
    accent: horizontal, side by side
  - id: hardware-cluster
    col: 3/4  row: 2/3
    label: HARDWARE CLUSTER
    content: 3 mini gauges (GPU/RAM/CPU) in a row
    accent: small, horizontal
  - id: agent-ocean
    col: 1/3  row: 3/4
    label: AGENT OCEAN
    content: all agents in a scrollable grid, 4-column card layout
    accent: 2-column wide, main content
  - id: activity-side
    col: 3/4  row: 3/4
    label: ACTIVITY SIDE
    content: latest 15 actions
    accent: right column, scrollable
  - id: foot-strip
    col: 1/4  row: 4/5
    label: FOOT STRIP
    content: version, uptime, terminal preview, skill count
    accent: full-width bottom, monospaced
---
mockup-09 — THE LOOM
---
layout:
  cols: [1fr, 260px, 260px]
  rows: [180px, 1fr, 1fr]
  gap: 10
panels:
  - id: forge-weave
    col: 1/2  row: 1/2
    label: FORGE WEAVE
    content: big 2x2 grid of 4 key metrics (agents, evals, loops, avg score)
    accent: large numbers, no labels visible until hover
  - id: live-spindle
    col: 1/2  row: 2/4
    label: LIVE SPINDLE
    content: activity feed — vertical timeline with dots + time
    accent: left column timeline, full height
  - id: pipeline-bobbin
    col: 2/4  row: 1/2
    label: PIPELINE BOBBIN
    content: horizontal pipeline: refinery → eval → improve → production
    accent: 2-col top right, flow arrows
  - id: gpu-thread
    col: 2/3  row: 2/3
    label: GPU THREAD
    content: GPU details, per-GPU breakdown
    accent: mid-right
  - id: skill-shuttle
    col: 3/4  row: 2/3
    label: SKILL SHUTTLE
    content: skills as woven tag cloud
    accent: varied font sizes by score
  - id: control-loom
    col: 2/3  row: 3/4
    label: CONTROL LOOM
    content: spawn input + 2 action buttons
    accent: compact bottom
  - id: terminal-shuttle
    col: 3/4  row: 3/4
    label: TERMINAL SHUTTLE
    content: last 8 commands
    accent: bottom right
---
mockup-10 — THE CORE DUMP
---
layout:
  cols: [1fr, 2fr, 1fr]
  rows: [auto, auto, auto]
  gap: 8
panels:
  - id: left-rail
    col: 1/2  row: 1/4
    label: LEFT RAIL
    content: vertical stack — forge vitals (top), controls (mid), hardware (bottom)
    accent: single panel, 3 internal sections with thin dividers
  - id: center-stage
    col: 2/3  row: 1/4
    label: CENTER STAGE
    content: big activity cascade, 50 entries, filter tabs (all/spawn/eval/improve)
    accent: 2fr, main content area, full height
  - id: right-rail-top
    col: 3/4  row: 1/2
    label: RIGHT RAIL TOP
    content: top 5 BPs by score + promote-to-production button
    accent: action-oriented
  - id: right-rail-mid
    col: 3/4  row: 2/3
    label: RIGHT RAIL MID
    content: skill collection, search input at top
    accent: searchable, scrollable
  - id: right-rail-bottom
    col: 3/4  row: 3/4
    label: RIGHT RAIL BOTTOM
    content: forge terminal, last 10 commands
    accent: bottom dock
---
RECOMMENDATION: mockup-01 (THE FORGE FLOOR) — most balanced asymmetry. 5-column grid with varied spans. Uses negative space as structural element. Panels sized by data density. Best ratio of information density to visual breathing room.