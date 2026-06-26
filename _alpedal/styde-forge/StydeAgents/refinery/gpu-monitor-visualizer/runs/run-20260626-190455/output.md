Blueprint: Gpu Monitor Visualizer v3
Domain: frontend | Version: 3 | Format: plaintext+yaml
Purpose
Six real-time GPU monitoring cards for Forge dashboard. One GPU per card. Metrics as visual art.
Glanceable status at 2m, deep diagnostics at 0.3m.
Layout
3x2 grid of GPU cards. 400x340px each. Dark theme (#0a0c10 base), accent colors driven by temperature gradient.
Header row: hostname + GPU count + refresh indicator (live dot pulsing every 2s).
Per-GPU Card Structure
Four vertical zones, 400px wide:
Zone 1: Identity + Overview (60px)
Left: GPU index badge — small pill, white text on temp-gradient background
Center: GPU name (e.g. "NVIDIA RTX 4090") in 12px semibold, #c0c4cc
Right: 4 status dots — Temp/Uti/Mem/Fan — green=nominal, amber=warn, red=critical
Zone 2: Temperature Heat-Map Core (140px)
Full-width graduated bar, 130px tall. Canvas-style gradient from left (coolest core) to right (hottest core).
8 vertical segments, each 16px wide, representing GPU hot-spot zones.
Segment color from blue (#00d4ff) → green (#00ff88) → yellow (#ffd000) → red (#ff3355) — interpolated by temp.
No labels on segments. Clean. Pure color.
Below bar: single row of 3 numbers — "Avg 67°C | Max 74°C | Mem 62°C" — 11px, #888
Zone 3: Utilization + Memory Bars (70px)
Two horizontal stacked bars, full width:
Utilization bar (28px height):
  Background: #1a1d24
  Fill: gradient #00ff88 → #00d4ff, width = util%
  Sparkline overlay: 1px white line, 60 data points, drawn into the bar's right 80%
  Text: "43%" at right edge of fill, 13px bold white
Memory bar (28px height):
  Background: #1a1d24
  Fill: gradient #8888ff → #ff88ff, width = vram_used/vram_total
  Two segments: Used (solid gradient) + Reserved (hatched overlay, 4px pattern)
  Text: "10.2/24 GB" at right edge, 11px #aaa
  Cache/swap fraction shown as thin sliver at bar end, 3px #ffd000
Zone 4: Fan + Power + Misc (70px)
Three mini-metrics side by side:
Fan: Circular arc gauge, 44px diameter. Arc sweeps from 7 o'clock to 5 o'clock. Fill angle = fan_speed%. Center text "45%". Stroke width 3px, color #00ff88.
Power: Vertical bar, 8px wide, 40px tall. Fill = power_draw/TDP. Color transitions green→yellow→red. Text below: "285W / 450W" 9px.
Voltage block: Two rows — "1.05V" + "PCIe 4.0 x16". 9px #777, right-aligned.
Palette
bg-deep:       #0a0c10
bg-card:       #111318
bg-bar-empty:  #1a1d24
text-primary:  #e8eaed
text-secondary:#888899
text-dim:      #555566
temp-cold:     #00d4ff
temp-nominal:  #00ff88
temp-warm:     #ffd000
temp-hot:      #ff3355
util-grad:     linear-gradient(90deg, #00ff88, #00d4ff)
mem-grad:      linear-gradient(90deg, #8888ff, #ff88ff)
accent-pulse:  #00ff88
Interaction
Hover on any GPU card: subtle glow border (#ffffff11, 4px spread), slight scale 1.01
Click GPU card: expands to full-width detail panel below the grid
Detail panel shows: per-core temp sparklines (last 60s), process list (top 5 by vram), clock speeds graph
Double-click: isolates single GPU to center of viewport, expands all metrics 2x
Responsive Breakpoints
>1400px: 3 columns, 2 rows
900-1400px: 2 columns, 3 rows
<900px: 1 column, scroll
Animation
Temperature segments: 300ms ease transition on color change
Sparklines: 500ms ease-in-out path transition on new data point
Fan gauge: 800ms spring animation on speed change
Status dots: 200ms ease color transition
All metrics update at 2s interval, synced to one RAF loop
Data-As-Art Principle
Every pixel carries signal. The temperature bar IS the thermal gradient — no chrome, no decorative borders. Sparkline IS the utilization fill, not an overlay. Color IS the warning state. Form follows data so tightly that removing any visual element destroys information. This is what makes it beautiful.
Specification Summary
Dimensions: 400x340px per card | 3x2 grid total ~1200x680px
Fonts: system-ui, 400/600 weight, sizes 9-13px
Radius: 8px card corners, 4px inner element corners
Spacing: 16px card padding, 8px inter-zone gap, 12px grid gap
Animations: 200-800ms ease transitions, single RAF loop
Refresh: 2000ms poll interval
Concision Constraint
This blueprint is the single authoritative spec. No YAML block repeats data already stated. No inline pixel dimensions on diagrams. No color prose in mockup descriptions — colors live in Palette above. Every sentence adds signal not present elsewhere. If a detail is derivable from the spec table, omit it from prose.