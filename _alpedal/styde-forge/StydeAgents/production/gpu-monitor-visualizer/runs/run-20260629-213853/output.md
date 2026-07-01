BLUEPRINT: Gpu Monitor Visualizer
Version: 1
Domain: frontend
Purpose:
Design GPU monitoring views for Forge dashboard mockups. Real-time GPU metrics with temperature heat-maps, utilization sparklines, memory bars, fan speed curves, and thermal zone visualization. Hardware data rendered as art — glanceable at distance, detailed on hover.
Layout: Full-width vitals bar + grid of metric cards + per-GPU expand panel
--- VITALS BAR (always visible, top strip) ---
gpu_count: 4
thermal_aggregate: heat-gradient strip per GPU
  format: [GPU_0 ████████████████ 72C]  [GPU_1 ████████████████ 68C]  [GPU_2 ████████████████ 81C]  [GPU_3 ████████████████ 65C]
  color_map: <60C=cyan, 60-70C=green, 70-80C=yellow, 80-85C=orange, >85C=red
  width: 12px per degree block (each block = 1C)
  length: proportional to current temp + 10C headroom
utilization_avg: sparkline across all GPUs over last 60s
  line_color: per-GPU color (GPU_0=#00ff88, GPU_1=#ffaa00, GPU_2=#ff4488, GPU_3=#44aaff)
  height: 24px
  width: 120px
vram_total: stacked horizontal bar
  total: 96GB / 128GB
  per GPU: colored segments with gaps
  bar_height: 8px
  label: compact side text
--- METRIC GRID (2x2 or 4x1 depending on screen width) ---
Each GPU card has:
CARD HEADER:
  gpu_label: GPU 0 — NVIDIA RTX 5090
  icon: thermal/gaming/compute badge
  dropdown: select GPU from N available
  timestamp: last updated 2.3s ago
CARD BODY — four quadrants:
QUADRANT 1: TEMPERATURE HEAT-MAP (top-left, dominant)
  representation: thermal camera style gradient rectangle
  dimensions: 240x120px
  gradient: per-sensor hot spots mapped to gaussian blur overlay
    core_temp: center hotspot at current temp color
    memory_temp: lower-right hotspot
    hotspot_temp: upper-left hotspot
    vram_temp: lower-left hotspot
  overlay: 5x5 grid of sensor points, each rendered as radial gradient circle
    radius: 12px
    opacity: 0.6-1.0 based on proximity to sensor hot
  label: floating temp readout in center "72C"
  color_scale: inferno colormap (dark purple->bright yellow->white)
    stops: [0, 0.25, 0.5, 0.75, 1.0]
    colors: ["#0d0887", "#46039f", "#9e2c9e", "#f48849", "#fef0d2"]
  gauge_ring: circular gauge around heat-map
    arc: 270 degrees
    thickness: 6px
    value: current temp mapped to arc
    min: 30C
    max: 100C
    target: 83C (throttle threshold as tick mark)
QUADRANT 2: UTILIZATION SPARKLINES (top-right)
  render: three stacked mini-sparklines with area fill
  dimensions: 200x90px
  lines:
    - core_util: % over last 120s
      color: #00ff88
      fill: yes, gradient to transparent at 50% opacity
      current_marker: circle dot at latest value
      label: "Core 87%"
    - memory_util: % over last 120s
      color: #44aaff
      fill: yes
      label: "Mem 34%"
    - pcie_util: % over last 120s
      color: #aa88ff
      fill: yes
      label: "PCIe 22%"
  x_axis: time ticks at 30s intervals
  y_axis: 0-100% with horizontal reference lines at 25, 50, 75
  animation: lines draw left-to-right in 600ms on mount, then scroll smoothly
QUADRANT 3: VRAM & MEMORY BARS (bottom-left)
  render: vertical stacked bar + horizontal detail bars
  dimensions: 200x90px
  main_bar: vertical, 100px tall, 16px wide
    segments:
      - used: 22GB (#ff4488)
      - cache: 8GB (#ffaa00)
      - reserved: 2GB (#8866ff)
      - free: 32GB (#1a1a2e)
    width: proportional to total percentage
    label: "Used 22/64 GB"
  detail_bars: horizontal, mini
    - bar: bandwidth (GB/s)
      color: gradient from #0055ff to #00ffaa
      value: 584 GB/s out of 960 GB/s
    - bar: vram_temp
      color: orange-to-red gradient
      value: 68C
    - bar: pcie_bw
      color: purple
      value: Gen5 x16
QUADRANT 4: FAN & POWER (bottom-right)
  render: fan speed radial array + power gauge
  fans:
    count: 3
    layout: arc along 180 degrees at bottom
    each fan:
      radius: 14px
      blade_count: 7
      rotation_speed: proportional to RPM value (0-3000 RPM mapped to deg/s)
      color_per_ring:
        inner: base color at 30% opacity
        outer: base color at 100% opacity
      label: "F1 1800 RPM"
    animation: continuous rotation, speed synced to live RPM
    hover: tooltip with RPM, PWM%, bearing temp
  power_gauge: horizontal segmented bar below fans
    total: 350W
    used: 287W
    segments:
      - core: 200W (#ff4488)
      - memory: 45W (#44aaff)
      - aux: 42W (#8866ff)
    overdraw_zone: >100% power limit in red stripes
    label: "287W / 350W  PL 100%"
    limit_indicator: vertical line at power limit (105% = dotted)
--- EXPAND PANEL (click GPU card header to expand) ---
DETAIL SECTION 1: THERMAL ZONE MAP
  render: 3D-ish GPU die layout with per-zone temperature
  zones:
    - core (die center)
    - memory_controller
    - cache_sram
    - pcie_phy
    - display_engine
    - video_encode
    - video_decode
    - tensors (tensor cores region)
  each_zone:
    shape: polygon approximating physical die position
    color: thermal gradient based on current temp
    label: zone name + temp
  layout: PCB outline in dark charcoal, die area highlighted
  scale: matches die layout of NVIDIA GB202 / AD102
DETAIL SECTION 2: CLOCK GRAPHS
  render: dual-line chart
  dimensions: full width card
  lines:
    - core_clock: MHz over last 300s
      color: cyan
    - mem_clock: MHz over last 300s
      color: magenta
  y_axis: dual (left=core, right=mem)
  reference_lines: base clock, boost clock, max allowed
  shading: voltage/freq curve region
DETAIL SECTION 3: VOLTAGE & CURRENT
  render: horizontal gauge cluster
  rails:
    - vcore: 0.985V
      range: 0.7-1.1V
    - vmem: 1.35V
      range: 1.0-1.5V
    - vaux: 1.8V
      range: 1.5-2.0V
  each: segmented gauge bar with current value marker
DETAIL SECTION 4: PROCESS LIST
  render: compact table
  columns: PID, Process Name, VRAM Used, Core Util %, Compute Cap
  max_rows: 15 with scroll
  highlight: self (Forge) row in accent color
--- INTERACTION SPEC ---
hover_card: any metric card shows expanded title + min/max/avg for last 5min
click_gpu: opens expand panel for that GPU
click_metric: isolates that metric to full-width chart
drag_reorder: metric cards draggable within grid
right_click: context menu (export snapshot, reset sparkline, log to file)
keyboard:
  Tab/Shift+Tab: navigate between GPU cards
  Space: toggle expand panel
  R: reset all sparklines
  numbers 1-4: jump to GPU card N
--- COLOR PALETTE ---
background: "#0a0a14" (deep space)
surface: "#12121e" (card bg)
surface_alt: "#1a1a2e" (alt row)
border: "#2a2a3e"
text_primary: "#e0e0ff"
text_secondary: "#8888aa"
text_muted: "#555577"
accent_gpu0: "#00ff88"
accent_gpu1: "#ffaa00"
accent_gpu2: "#ff4488"
accent_gpu3: "#44aaff"
thermal_inferno: ["#0d0887", "#46039f", "#9e2c9e", "#f48849", "#fef0d2"]
thermal_heat: ["#000000", "#ff0000", "#ffff00", "#ffffff"]
utilization_gradient: "#00ff88" -> "rgba(0,255,136,0.1)"
memory_gradient: "#44aaff" -> "rgba(68,170,255,0.1)"
danger: "#ff2244"
warning: "#ffaa00"
success: "#00ff88"
info: "#44aaff"
--- DATA FLOW ---
source: WebSocket /api/v1/gpu/stream
message: JSON per GPU, 500ms interval
payload:
  gpu_index: int
  name: string
  temperature: { core, memory, hotspot, vram, avg }
  utilization: { core, memory, pcie, decoder, encoder }
  clocks: { core, memory, boost }
  vram: { total, used, cache, reserved, free }
  power: { core, memory, aux, total, limit, draw }
  fans: [ { rpm, pwm, bearing_temp } ]
  processes: [ { pid, name, vram, util, capability } ]
  voltage: { vcore, vmem, vaux }
  throttle: { is_throttling, reason, since_timestamp }
cache: ring buffer per metric per GPU, 600 entries (5 min at 500ms)
aggregation: min, max, avg, p50, p95, p99 per window
--- RESPONSIVE BREAKPOINTS ---
wide (>1400px): 4-column grid, vitals bar sidecar
normal (1000-1400px): 2x2 grid, vitals on top
tablet (600-1000px): 4x1 stack, vitals collapsed to single line
mobile (<600px): single card, swap to auto-scroll through GPUs
--- PERFORMANCE BUDGETS ---
first_paint: <100ms
fps: 60fps sustained
memory: <50MB heap
ws_messages: <5000/min per connection
canvas_redraw: <8ms per frame
--- RENDERING TECHNIQUE ---
Primary: HTML5 Canvas for heatmaps, sparklines, fan animations
Secondary: SVG for static elements (labels, grids, card frames)
Fallback: DOM-based rendering when Canvas not available
Blend mode: "screen" for overlay highlights, "normal" for base
Anti-alias: enabled for all curve rendering
Resolution: devicePixelRatio-aware (2x for retina)