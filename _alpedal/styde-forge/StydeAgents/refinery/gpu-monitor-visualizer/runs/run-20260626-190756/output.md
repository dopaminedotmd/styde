BLUEPRINT:GpuMonitorVisualizer Design Spec v2
Domain: frontend Version: 2
=== STRUCTURE ===
1. Data Model (tables)
2. Layout Grid (breakpoint-aware)
3. Component Library (tables, max 3 sentences per animation)
4. Color System (single source)
5. Interactions & States (tables)
6. Responsiveness (breakpoint rules)
7. Appendix: Deep-dive animation curves (only if needed)
=== DATA MODEL ===
Metric | Unit | Range | Update Interval | Visual Treatment
GPU Temp | C | 0-105 | 500ms | Heat-map gradient, radial gauge
GPU Util | % | 0-100 | 500ms | Sparkline + bar, fill-to-empty
VRAM Total | GB | 0-24 | 1s | Stacked horizontal bar
VRAM Used | GB | 0-24 | 1s | Stacked fill within total
Fan Speed | RPM | 0-6000 | 2s | Arc gauge + numeric
Power Draw | W | 0-450 | 1s | Meter bar with TDP marker
Clock Core | MHz | 0-3000 | 1s | Trend line + current value
Clock Mem | MHz | 0-2000 | 1s | Trend line + current value
PCIe Gen | - | 1-5 | 5s | Badge
Driver Ver | - | - | on change | Label
=== COLOR SYSTEM (palette ref only) ===
cold: hsl(210,80%,50%)   - idle/cool GPU
warm: hsl(30,90%,55%)    - moderate load
hot: hsl(0,85%,55%)      - thermal throttle threshold
danger: hsl(350,95%,45%) - critical (over 95C)
bg: hsl(220,15%,8%)      - dashboard base
card: hsl(220,12%,14%)   - widget surface
text-primary: hsl(0,0%,92%)
text-secondary: hsl(0,0%,60%)
glow-hot: hsla(0,80%,50%,0.15)  - backdrop glow on hot cards
glow-normal: hsla(210,80%,50%,0.08)
Rule: reference above names only. No hex repeat in zone descriptions.
=== LAYOUT GRID ===
Breakpoint | Columns | Gutter | Widget Density
sm (0-639px) | 2 | 8px | 1-2 metrics per widget
md (640-1023px) | 3 | 12px | 2-3 metrics per widget
lg (1024-1439px) | 4 | 16px | 3-4 metrics per widget
xl (1440px+) | 6 | 20px | 4-6 metrics per widget
=== WIDGET COMPONENTS ===
Name | Type | Data Bound | Size (cells) | States
TempCard | radial-gauge + heat-map | GPU Temp | 1x1 (sm), 2x1 (lg+) | idle, active, critical, transition (300ms)
UtilSpark | sparkline + fill-bar | GPU Util | 2x1 | idle, spiking, flatline, transition (200ms)
VramBar | stacked-horizontal | VRAM Used + Total | 2x1 | normal, near-full (>90%), full
FanArc | arc-gauge + RPM label | Fan Speed | 1x1 | stopped, normal, max
PowerMeter | bar + TDP threshold | Power Draw | 2x1 | under-TDP, at-TDP, over-TDP (flash)
ClockTrend | trend-line + dual-value | Clock Core + Mem | 2x1 | stable, boosting, throttling
PcieBadge | icon + gen label | PCIe Gen | 1x1 | active, idle
DriverLabel | text | Driver Ver | 1x1 | current, outdated
State descriptions max 3 sentences each. Rationale for non-obvious choices only.
=== INTERACTIONS ===
Trigger | Response | Duration | Easing
hover widget | subtle scale(1.02) + glow-hot overlay | 200ms | ease-out
click widget | expand to detail overlay (full viewport) | 350ms | cubic-bezier(0.16,1,0.3,1)
metric threshold breach | widget border flash (hot->card) | 600ms pulse | steps(2)
resize viewport | reflow grid with column count transition | 300ms | ease-in-out
idle > 30s | reduce opacity to 0.3 on stable data | 500ms | ease
=== HISTORICAL SPARKLINE RULES ===
window: 60 data points per metric (60s at 1s interval)
rendering: Canvas2D, not SVG (perf > 60fps with 12 concurrent sparklines)
line color: gradient from cold to hot based on last-value position in range
tooltip: cursor-following, shows value + timestamp, fade-in 100ms
=== RESPONSIVENESS ===
sm: single-column stack, widgets full-width, tap-to-expand (no hover)
md: 2-3 column grid, compact widget labels, hover enabled
lg: 4-column grid, full labels, all hover/click interactions active
xl: 6-column grid, optional pinned heat-map spanning 2x2 cells
=== ANIMATION CONCISION ===
Each animation described in table row above. Max 3 sentences per animation. No philosophical rationale. Data-model-first ordering.
=== APPENDIX (deep-dive, only if queried) ===
easing curves: all custom cubic-bezier defined in CSS custom properties
--ease-smooth: cubic-bezier(0.16, 1, 0.3, 1)
--ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1)
render approach: double-buffered canvas for sparklines, CSS transitions for widget hover/expand, requestAnimationFrame for gauge animation. No setInterval for visual updates — use requestAnimationFrame with timestamp delta.