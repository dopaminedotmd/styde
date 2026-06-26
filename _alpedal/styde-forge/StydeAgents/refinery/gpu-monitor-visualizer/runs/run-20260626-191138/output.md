blueprint: gpu-monitor-visualizer
domain: frontend
version: 2
overview:
  purpose: Design GPU monitoring views for Forge dashboard mockups. Real-time GPU metrics, temperature gauges, utilization sparklines, memory bars, fan speed, thermal visualization.
  persona: You are a GPU monitor visualizer. Design beautiful, real-time GPU metrics. Temperature heat-maps, utilization sparklines, memory bars. Hardware data as art. Clear at a glance, detailed on inspection.
skills:
  - high-end-visual-design
  - interaction-design
  - frontend-design
  - real-time-data-visualization
  - accessibility-engineering
  - responsive-layout-design
data-flow-architecture:
  transport-layer:
    real-time-metrics:
      protocol: WebSocket
      rationale: Bidirectional low-latency push. Sub-100ms delivery for GPU temp, util, VRAM, fan, clock. SSE is unidirectional-only and adds reconnect complexity for the same perf profile. WebSocket wins for bidirectional metrics stream.
      endpoint: ws://<host>:<port>/ws/gpu/metrics
      payload-schema:
        type: object
        properties:
          gpuIndex: integer
          temperatureC: number
          utilizationPct: number
          vramUsedMb: number
          vramTotalMb: number
          fanSpeedPct: number
          clockCoreMhz: number
          clockMemoryMhz: number
          powerDrawW: number
          timestamp: integer
        required: [gpuIndex, temperatureC, utilizationPct, vramUsedMb, vramTotalMb, timestamp]
    config-history:
      protocol: REST (HTTP/2)
      rationale: Request-response suitable for polling config snapshots and historical log queries. No need for persistent stream.
      endpoints:
        - method: GET
          path: /api/gpu/list
          description: Enumerate detected GPUs with metadata (name, driver, pciBus)
          response:
            type: array
            items:
              type: object
              properties:
                gpuIndex: integer
                name: string
                driverVersion: string
                pciBus: string
                vramTotalMb: number
        - method: GET
          path: /api/gpu/{gpuIndex}/history
          description: Time-series history for sparkline and chart rendering
          query-params:
            - name: span
              type: string
              enum: [5m, 15m, 1h, 6h, 24h]
              default: 5m
            - name: resolution
              type: integer
              description: Sampling interval in seconds
              default: 1
          response:
            type: object
            properties:
              gpuIndex: integer
              span: string
              resolution: integer
              series:
                type: array
                items:
                  type: object
                  properties:
                    ts: integer
                    temperatureC: number
                    utilizationPct: number
                    vramUsedMb: number
        - method: GET
          path: /api/gpu/{gpuIndex}/config
          description: Per-GPU display configuration (thresholds, alerts)
          response:
            type: object
            properties:
              gpuIndex: integer
              tempWarning: number
              tempCritical: number
              utilWarning: number
              vramWarningPct: number
              pollingIntervalMs: integer
  metric-pipeline-sequence:
    step-1: Client opens WebSocket to /ws/gpu/metrics
    step-2: Server pushes metrics every 500ms as JSON frame
    step-3: Client receives frame -> validate schema -> update Reactive GPU state dictionary keyed by gpuIndex
    step-4: Per-component subscriptions fire:
      GpuTemperatureGauge: subscribes to gpuState.temperatureC, maps to color heat-index and gauge needle angle
      GpuUtilSparkline: pushes newest utilizationPct onto 120-sample ring buffer at 500ms interval, triggers re-render of SVG path
      VramBar: reads vramUsedMb / vramTotalMb -> calculates fill ratio, updates bar width + color
      FanSpeedIndicator: reads fanSpeedPct -> drives tachometer arc and label
      ClockDisplay: reads clockCoreMhz + clockMemoryMhz -> updates numeric readout
    step-5: On connect, client fetches GET /api/gpu/list to populate GPU selector and metadata badges
    step-6: On GPU selection change, client fetches GET /api/gpu/{gpuIndex}/history?span=5m&resolution=1 to backfill sparkline initial data
    step-7: Client also fetches GET /api/gpu/{gpuIndex}/config to apply user thresholds and polling preferences
  sparkline-window-resolved:
    server-push-interval: 500ms
    sparkline-ring-buffer-size: 120 samples
    effective-window: 60 seconds of data (120 samples * 500ms = 60s)
    downsampling-strategy: None. Server pushes at 500ms, client keeps full 120-sample native resolution. No aggregation or decimation needed. The earlier 60-point-at-1s reference was pre-v2; aligned to 120-point-at-500ms for higher fidelity with zero aliasing.
responsive-breakpoints:
  - breakpoint: sm
    min-width: 0px
    columns: 1
    gauge-size: compact (120px)
    sparkline-visible: false
    metric-labels: inline
  - breakpoint: md
    min-width: 640px
    columns: 2
    gauge-size: standard (160px)
    sparkline-visible: true
    metric-labels: stacked
  - breakpoint: lg
    min-width: 1024px
    columns: 3
    gauge-size: expanded (200px)
    sparkline-visible: true
    metric-labels: stacked
  - breakpoint: xl
    min-width: 1440px
    columns: 4
    gauge-size: expanded (240px)
    sparkline-visible: true
    metric-labels: stacked
component-summary:
  - component: GpuTemperatureGauge
    description: Radial gauge displaying current GPU temperature with color-coded arc
    states:
      loading: Skeleton circular placeholder with pulsing animation. Arc segments rendered as 4 translucent grey arcs with no angle. Tooltip hidden.
      error: Gauge shows red arc at 0% angle with ! icon center. Tooltip reads "Disconnected. Last data: <relative-time>". Reconnect button below gauge. After 3 failed reconnect attempts, shows static "GPU offline" badge.
      empty: No GPU detected. Gauge shows dimmed zero-state ring with thermometer icon inside. Text: "No GPU sensor found. Waiting for hardware...". Auto-hides after 30s if no GPU appears, collapses to badge-only.
    loading: skeleton circular placeholder, pulsing translucency, no arc angle
    error: red arc 0%, exclamation icon, last-data timestamp, reconnect button, 3-strike offline badge
    empty: dimmed zero-state ring, thermometer icon, "No GPU sensor found" text, auto-collapse to badge after 30s
  - component: GpuUtilSparkline
    description: SVG sparkline line chart showing utilization % over rolling 60-second window
    states:
      loading: Flat grey line at 0% with 3 animated shimmer dots moving along baseline. No fill area. Y-axis labels hidden.
      error: Sparkline frozen at last known path, overlaid with red dashed line at 0%. Tooltip: "Stale data. Last update <relative-time>". Single-click sparkline triggers re-fetch of history endpoint.
      empty: No sparkline path rendered. Baseline grey line only. Text: "Awaiting utilization data". Auto-fills from history backfill once GPU selected.
    loading: flat grey baseline, 3 shimmer dots animating, axis hidden
    error: frozen path + red dashed overlay, stale-data tooltip, click-to-refresh
    empty: baseline only, awaiting-data text, auto-fill from history backfill
  - component: VramBar
    description: Horizontal stacked bar showing VRAM used vs total with color gradient fill
    states:
      loading: Grey bar outline with pulsing 50% fill. No label digits (Mb/Mb shows ---/---). No color gradient.
      error: Bar shows 0% with red left edge border. Total capacity shown dimly. Tooltip: "VRAM sensor unreachable". Retry indicator dot beside bar.
      empty: Bar rendered at 0% with faint dashed outline. Text "0 MB / ---" with total unknown until GPU selected. Capability icon in gray.
    loading: pulsing 50% grey fill, ---/--- label, no gradient
    error: 0% red border, dim total, unreachable tooltip, retry dot
    empty: 0% dashed outline, 0 MB / --- label, gray icon
  - component: FanSpeedIndicator
    description: Tachometer-style arc gauge for fan RPM/speed percentage
    states:
      loading: Arc drawn as full circle in dim grey with no needle. RPM readout shows "--- RPM". No speed bar.
      error: Needle stuck at 0, arc red tint. Text: "Fan sensor error". Blinking warning triangle.
      empty: Arc absent entirely. "Fan: N/A" text. Hidden on passive-cooled GPUs.
    loading: grey full-circle arc, --- RPM, no needle
    error: needle at 0, red tint, fan sensor error text, blinking triangle
    empty: arc removed, N/A label, hidden on passive-cooled systems
  - component: ClockDisplay
    description: Numeric readout for core clock and memory clock in MHz
    states:
      loading: "--- / --- MHz" with monospace font in dim grey. Decimal dots flicker on last digit position.
      error: "ERR / ERR" in red monospace. Tooltip: "Clock sensor disconnected". Does not retry automatically past 10s.
      empty: "0 / 0 MHz" in faint grey. Hidden entirely if no GPU selected.
    loading: ---/--- MHz dim monospace, flickering dots
    error: ERR/ERR red, disconnected tooltip, 10s timeout
    empty: 0/0 MHz faint, hidden on no-GPU state
  - component: ThermalMapView
    description: Grid or heatmap overlay showing temperature deltas across GPU die zones (if multi-sensor data available)
    states:
      loading: Grey 3x3 block grid with no color fill. Pulsing checkerboard pattern. No legend.
      error: Entire grid rendered in flat red. Tooltip: "Thermal sensor array unavailable on this GPU". Collapsed to text-only badge after 5s.
      empty: Grid rendered in uniform blue (idle temp) with all cells at same value. Legend shows single entry. No hotspot visualization.
    loading: grey 3x3 checkerboard pulsing, no legend
    error: flat red grid, sensor-unavailable message, collapse to badge
    empty: uniform blue grid, single legend entry, no hotspots
accessibility:
  color-contrast:
    temperature-thresholds:
      safe: 35C-60C -> green (#22c55e) on dark bg (#1a1a2e) ratio 5.2:1 PASS AA
      warm: 61C-75C -> amber (#f59e0b) on dark bg (#1a1a2e) ratio 6.8:1 PASS AA
      hot: 76C-85C -> orange (#ea580c) on dark bg (#1a1a2e) ratio 5.5:1 PASS AA
      critical: 86C+ -> red (#ef4444) on dark bg (#1a1a2e) ratio 5.7:1 PASS AA
      stroke-weights: Minimum 3px for color-only indicators. Where color alone carries meaning (threshold arcs, heatmap cells), add pattern overlay or text annotation as secondary channel.
  screen-reader-labels:
    real-time-charts:
      - GpuTemperatureGauge: aria-label="GPU {index} temperature {value} degrees {status}" aria-live="polite" role="progressbar" aria-valuenow={temp} aria-valuemin="0" aria-valuemax="120"
      - GpuUtilSparkline: aria-label="GPU {index} utilization sparkline. Last {value} percent. {direction}" role="img" aria-describedby="sparkline-{index}-desc"
      - VramBar: aria-label="GPU {index} VRAM {used} of {total} megabytes, {percent} percent used" role="progressbar" aria-valuenow={used} aria-valuemin="0" aria-valuemax={total}
      - FanSpeedIndicator: aria-label="GPU {index} fan speed {value} percent" role="meter" aria-valuenow={value} aria-valuemin="0" aria-valuemax="100"
      - ClockDisplay: aria-label="GPU {index} core clock {core} megahertz, memory clock {memory} megahertz" role="status"
      - ThermalMapView: aria-label="GPU {index} thermal map. Hotspot at zone {zone}, {value} degrees" role="img" aria-describedby="thermal-{index}-legend"
    update-frequency: Screen reader updates debounced to max 1 announcement per 3 seconds per component, to avoid aria-live flooding.
  keyboard-navigation:
    - All interactive controls focusable via Tab in logical DOM order
    - Sparklines and gauges receive focus only if they expose a tooltip or click action
    - Space/Enter activates reconnect button, toggles GPU selector, expands detail panels
    - Arrow keys navigate GPU grid cells in desktop layout
    - Escape closes any open tooltip or detail overlay
    - Focus indicator: 2px solid cyan (#06b6d4) outline with 4px offset, visible on all focusable elements
gpu-index-resolution:
  rule: gpuIndex is defined exactly once under the WebSocket payload schema and REST endpoint path params. It is NOT listed on individual component props tables because each component receives the full gpu state object keyed by gpuIndex from the parent container. Components consume gpuIndex implicitly via subscription filter, not as a prop. Parent container (GpuDashboardGrid) receives the gpuIndex array from GET /api/gpu/list and distributes sub-components per GPU instance. No duplication.
design-notes:
  palette: Dark theme baseline (#0f0f23 body, #1a1a2e card, #e2e8f0 primary text). Accent colors driven by data values, not theme tokens. Chart colors follow temperature heat-index from blue (cold) through green (safe), amber (warm), red (hot).
  animation: Metrics animate at 60fps via requestAnimationFrame. WebSocket frames apply to intermediate state immediately; visual interpolation uses spring physics (stiffness 180, damping 12) for gauge needle and bar width. Sparkline path transitions with d3 shape-tweening over 300ms.
  multi-gpu: Grid renders N columns of GPU cards up to the xl breakpoint limit. If more GPUs than columns, wraps to next row. Each card is an independent component tree with its own WebSocket subscription filter.
  empty-dashboard: When no GPU detected anywhere, the entire dashboard collapses to a single centered "No GPU Hardware Detected" hero panel with a pulsing scan icon and "Checking for hardware..." auto-retry message every 10 seconds. All sub-components remain mounted but in empty state with visibility: hidden on their parent card wrapper.