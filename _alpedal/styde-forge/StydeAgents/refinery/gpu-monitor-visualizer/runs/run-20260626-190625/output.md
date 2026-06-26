GPU Monitor Visualizer — Design Mockup
gpu-monitor:
  philosophy: data-as-art — every pixel carries signal, color is temperature, motion is utilization
  layout: horizontal band spanning full dashboard width, 4 GPU cards in row
  breakpoint: 4 cards at 1400px+, 2 cards at 900px, 1 card below
gpu-card:
  width: 1/4 of viewport minus gutter
  height: 380px
  background: okhsl(240 8% 8%) with subtle gradient edge glow
  border: 1px okhsl(240 10% 15%)
  border-radius: 12px
  padding: 16px
  structure:
    - header row: GPU index + model name + health dot
    - thermal ring: circular temperature gauge (outer ring)
    - center: utilization sparkline (SVG path, 60 data points)
    - bottom row: VRAM bar + fan speed arc
thermal-ring:
  type: circular gradient gauge, 240 degrees arc
  radius: 64px
  stroke-width: 8px
  color-scale:
    0-40C: okhsl(140 70% 50%) — cool green
    40-55C: okhsl(80 80% 50%) — warm green
    55-65C: okhsl(50 90% 55%) — yellow
    65-75C: okhsl(30 95% 55%) — orange
    75-85C: okhsl(10 90% 55%) — red
    85-100C: okhsl(340 95% 55%) — magenta warning
  implementation: conic-gradient with hard color stops, rotation transforms
  inner-text: temperature in celsius, font-size 24px, weight 600
  glow: outer ring glow matches current color at 30% opacity
utilization-sparkline:
  type: SVG polyline, 60 data points (2 seconds at 30fps)
  width: 100% of card inner width
  height: 48px
  line-color: okhsl(var(--util-hue) 80% 60%) — hue maps to type
  compute: okhsl(270 80% 60%) — purple
  memory: okhsl(200 80% 60%) — blue
  encoder: okhsl(40 80% 60%) — amber
  fill: gradient below line to transparent
  animation: CSS animate stroke-dashoffset over 1s on data update
  overlay: horizontal reference lines at 25/50/75/100% at 10% opacity
vram-bar:
  type: horizontal stacked bar
  height: 12px
  border-radius: 6px
  background: okhsl(240 5% 15%)
  segments:
    - used: width via CSS var(--vram-used-%), okhsl(200 70% 55%)
    - reserved: width via --vram-reserved-%, okhsl(200 40% 35%)
    - free: remaining, no fill
  animation: width transitions at 300ms ease
  label: "XX.X / XX.X GB" right-aligned, font-size 11px, opacity 0.7
fan-speed-arc:
  type: small radial arc, 180 degrees
  radius: 24px
  stroke-width: 4px
  color: okhsl(180 50% 50%) at 0-40%, okhsl(40 70% 55%) at 40-70%, okhsl(10 80% 55%) above 70%
  dasharray: speed percentage of circumference
  center-text: rpm in thousands (e.g. "2.4k"), font-size 10px
power-draw:
  type: horizontal micro-bar below fan arc
  height: 4px
  width: 48px
  color: okhsl(30 90% 60%)
  label: "XXXW" beside bar, font-size 10px
health-dot:
  type: 8px circle
  color:
    ok: okhsl(140 70% 50%) — pulsing at 2s interval with 0.6-1.0 opacity
    warning: okhsl(50 90% 55%) — pulsing at 1s interval
    critical: okhsl(10 90% 55%) — pulsing at 0.5s interval
header-row:
  layout: flex, space-between
  gpu-index: "GPU 0", font-size 14px, weight 600, white
  model-name: "RTX 4090", font-size 11px, opacity 0.5
  health-dot: right-aligned
layout-grid:
  type: CSS Grid, grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))
  gap: 12px
  padding: 16px
  overflow-x: auto
  scrollbar: thin, transparent track, okhsl(240 10% 30%) thumb
interaction:
  hover: card elevates (translateY -2px, shadow deepens, border brightens 20%)
  click: expands card to full-width detail view with historical 5-minute charts
  detail-view:
    - 5-minute utilization line chart (300 data points at 1Hz)
    - temperature history overlay (same timespan, right axis)
    - VRAM allocation breakdown per-process
    - fan speed + power draw dual axis chart
  update-frequency: 1 second polling, CSS transition on all changing values at 500ms ease
color-palette:
  background: okhsl(240 12% 6%)
  card-bg: okhsl(240 8% 10%)
  text-primary: okhsl(0 0% 95%)
  text-secondary: okhsl(0 0% 60%)
  accent: okhsl(180 80% 50%) — cyan accent for borders, highlights
  thermal-green: okhsl(140 70% 50%)
  thermal-yellow: okhsl(50 90% 55%)
  thermal-orange: okhsl(30 95% 55%)
  thermal-red: okhsl(10 90% 55%)
  thermal-magenta: okhsl(340 95% 55%)
typography:
  font-family: 'Inter', system-ui, sans-serif
  weights: 400 for labels, 500 for values, 600 for headers
  sizing:
    - gpu-index: 14px semibold
    - temperature: 24px semibold
    - utilization-label: 11px regular
    - vram-label: 11px regular
    - fan-speed: 10px regular
micro-animations:
  - temperature change: color transitions at 500ms ease (prevents flicker)
  - sparkline points: new point fades in at right edge, old scrolls left
  - VRAM bar: width animates 300ms ease
  - health dot: persistent subtle pulse at 2s when healthy
  - card entry: staggered fade-in-up at 100ms delay per card
empty-state:
  - no GPUs detected: 120px GPU icon (silhouette) at 30% opacity
  - text: "No GPU hardware detected" centered below
  - polling indicator: pulsing dot at bottom, "Waiting for NVIDIA driver..."
error-state:
  - driver failure: card turns okhsl(10 30% 15%) background
  - icon: warning triangle at top-right
  - message: "GPU driver not responding — last reading [timestamp]"
  - retry button: 80px wide, "Retry", okhsl(10 80% 55%) border, transparent bg
loading-state:
  - skeleton cards: same dimensions, no content
  - shimmer: linear gradient sweep at 45deg, okhsl(240 8% 10%) to okhsl(240 8% 14%) to okhsl(240 8% 10%)
  - animation: 1.5s infinite translateX sweep
accessibility:
  - aria-labels on all gauges (e.g. "GPU 0 temperature: 62 degrees Celsius")
  - role="img" on sparklines with aria-label describing trend
  - prefers-reduced-motion: disable all animations except color transitions
  - color-independent indicators: texture patterns alongside color on thermal ring for color-blind users
component-tree:
  GpuMonitorGrid
    ├── GpuCard (×N)
    │   ├── CardHeader
    │   │   ├── GpuIndexLabel
    │   │   ├── ModelName
    │   │   └── HealthStatusDot
    │   ├── ThermalRingGauge
    │   │   ├── ConicGradientRing
    │   │   └── TemperatureValue
    │   ├── UtilizationSparkline
    │   │   ├── SvgPolyline
    │   │   └── ReferenceLines
    │   └── MetricsBar
    │       ├── VramBar (stacked)
    │       ├── FanSpeedArc
    │       └── PowerDrawIndicator
    └── DetailOverlay (on expand)
        ├── HistoryLineChart
        ├── TemperatureOverlay
        ├── ProcessBreakdown
        └── DualAxisFooter
data-model:
  gpuMetrics:
    - index: integer
    - name: string
    - temperature: float (Celsius)
    - utilization: float (0-100%)
    - vramTotal: float (GB)
    - vramUsed: float (GB)
    - vramReserved: float (GB)
    - fanSpeed: integer (RPM)
    - powerDraw: float (Watts)
    - powerLimit: float (Watts)
    - encoderUtil: float (0-100%)
    - decoderUtil: float (0-100%)
    - memoryUtil: float (0-100%)
    - health: enum(ok, warning, critical)
    - history: array of {timestamp, temp, util, vramUsed} (last 300 entries)