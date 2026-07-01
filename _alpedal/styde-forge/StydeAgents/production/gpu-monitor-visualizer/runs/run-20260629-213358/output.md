BLUEPRINT
Blueprint: Gpu Monitor Visualizer
Domain: frontend
Version: 2
Purpose
Real-time GPU metrics dashboard for Forge monitoring. Temperature heat-maps, utilization sparklines, VRAM bars, fan curves, clock speeds. Hardware telemetry rendered as data-art — glanceable at distance, detailed on inspection.
Persona
GPU monitor visualizer. Design beautiful, real-time GPU metrics. Temperature heat-maps, utilization sparklines, memory bars. Hardware data as art. Clear at a glance, detailed on inspection.
Skills
  high-end-visual-design
  interaction-design
  frontend-design
  data-visualization
Architecture
Component tree:
  GpuDashboard
    GpuCard (one per GPU) [n=1-8, responsive grid]
      GpuHeader [name, index, model, driver version]
      ThermalMap [grid layout, per-sensor temps]
      UtilizationSparkline [last 60s, multi-line: core/mem/enc/dec]
      VramBar [used/total, color-coded bands]
      FanGauge [rpm + percentage, radial]
      ClockDisplay [core/mem/boost clocks, MHz]
      PowerMeter [watts, TBP percentage]
      GpuControls [refresh rate toggle, alert thresholds]
    SummaryBar
      AggregateUtilization [avg/max across all GPUs]
      TotalPower [sum, thermal ceiling indicator]
      AlertBadge [critical/warning count, click to focus]
Data flow:
  WebSocket -> pulse buffer (60 entries per metric) -> component props
  Pulse interval: 1s default, configurable 0.5-10s
  Buffer: ring buffer, drops oldest on overflow
  Aggregation: client-side reduce for summary stats
Responsive breakpoints:
  breakpoint: 320px | columns: 1 | card layout: stacked full-width
  breakpoint: 640px | columns: 2 | card layout: 2-col grid, compact gauges
  breakpoint: 1024px | columns: 3 | card layout: 3-col grid, expanded sparklines
  breakpoint: 1440px | columns: 4 | card layout: 4-col grid, full detail
  breakpoint: 1920px | columns: 6 | card layout: 6-col grid, side-by-side metrics
Props definition:
GpuDashboard
  gpus: GPUData[] — required, array of GPU telemetry objects
  refreshInterval: number — default 1000ms
  maxHistory: number — default 60, pulse buffer depth
  theme: 'dark' | 'light' — default 'dark'
  alertThresholds: AlertConfig — optional, per-metric warning/critical levels
  onGpuFocus: (index: number) => void — optional, focus callback
  className: string — optional, CSS class override
GPUData
  index: number — gpu ordinal
  model: string — GPU model name
  driver: string — driver version string
  temperature: SensorReading[] — per-sensor temps (core, memory, hotspot, vrm)
  utilization: UtilizationSnapshot — core/mem/enc/dec percentages
  vram: MemoryBand — used, total, reserved
  fans: FanState[] — per-fan rpm and percentage
  clocks: ClockSnapshot — core, memory, boost in MHz
  power: PowerReading — watts, total board power limit, percentage
  pcie: PcieLink — generation, lanes, throughput
AlertConfig
  tempWarning: number — default 85 C
  tempCritical: number — default 95 C
  utilWarning: number — default 95%
  vramWarning: number — default 90%
  powerWarning: number — default 90%
No props are inherited from parent. All props are defined under their definitive section above.
Component summary table:
  GpuDashboard — container, layout orchestration, pulse subscription — props: gpus, refreshInterval, maxHistory, theme, alertThresholds, onGpuFocus, className
  GpuCard — single GPU card, metric grid — props: gpu (GPUData), theme, alertThresholds
  GpuHeader — GPU label + status indicator — props: name, index, model, driver
  ThermalMap — heat-map grid per sensor position — props: sensors (SensorReading[]), theme
  UtilizationSparkline — multi-line sparkline last N pulses — props: history (UtilizationSnapshot[]), theme
  VramBar — horizontal bar with color bands — props: used, total, reserved, theme
  FanGauge — radial gauge per fan — props: fan (FanState), theme
  ClockDisplay — numeric clock values — props: clocks (ClockSnapshot), theme
  PowerMeter — bar + percentage — props: watts, tbp, theme
  GpuControls — user controls — props: refreshRate, onRefreshChange, thresholds, onThresholdChange
  SummaryBar — aggregate row — props: allGpus (GPUData[]), alertThresholds
  AggregateUtilization — avg/max across GPUs — props: gpus (GPUData[])
  TotalPower — sum + ceiling — props: gpus (GPUData[]), thermalCeiling (number)
  AlertBadge — alert count + click-to-focus — props: alerts (Alert[]), onAlertClick
Error Boundaries & Resilience
  GpuCardErrorBoundary — wraps each GpuCard, catches render errors, shows fallback card with GPU index and last-known-good snapshot. Reset on new data pulse.
  DashboardErrorBoundary — wraps entire grid, catches fatal errors, shows degraded mode with static summary only.
  WebSocket reconnection: exponential backoff with jitter. Initial delay 1s, multiplier 2, max delay 30s, jitter factor 0.3. Max retries: 10 before persistent error state. On reconnect, request full state then resume incremental pulses.
  Stale data detection: if no pulse received for 2x refreshInterval, show warning badge on card. After 5x interval without data, show "Disconnected" overlay.
  Fallback UI: GpuCard renders skeleton shimmer on first load before first pulse arrives. Error card shows GPU index, last temperature reading (if any), and retry button.
Performance Budgets
  Initial load JS: under 80KB gzipped (no chart library — hand-rolled SVG sparklines and bars)
  TTI: under 1.5s on mid-range device
  FCP: under 800ms
  LCP: under 2s
  Component render budgets (per frame at 60fps):
    GpuCard: under 2ms
    ThermalMap: under 1ms (canvas fallback if sensor count > 12)
    UtilizationSparkline: under 1ms (SVG path recompute, skip paint if data unchanged)
    VramBar: under 0.5ms
  Pulse processing: under 4ms total for 8 GPUs (60-entry buffer update + reduce)
  Memory: under 10MB for full buffer at 8 GPUs x 60 pulses
  Bundle size budget per component (min+gzip): GpuDashboard 2KB, GpuCard 3KB, ThermalMap 4KB, UtilizationSparkline 3KB, VramBar 1KB, FanGauge 2KB, ClockDisplay 1KB, PowerMeter 1KB, SummaryBar 2KB
Authentication & Security
  Auth flow: WebSocket connection requires JWT token in connection parameters. Token obtained via OAuth2 implicit flow or bearer token from parent dashboard. Token refresh: silent refresh via iframe postMessage before expiry. Session expiry: disconnect gracefully, show re-auth prompt in SummaryBar.
  API request signing: all REST polling fallback requests signed with HMAC-SHA256 using per-session key exchanged during WebSocket handshake. Timestamp + nonce in header to prevent replay.
  CORS: configured for same-origin by default. Cross-origin whitelist configurable via allowedOrigins prop. No wildcard.
  Input sanitization: all GPU model names, driver strings, and sensor labels run through DOMPurify before rendering. Numeric metrics validated client-side (0-100 for percentages, 0-2000 for MHz, checked for NaN/Infinity). Invalid values render '--' instead of crashing.
  Data isolation: per-tab session scoping. Multiple dashboard tabs receive only their authorized GPU subset. No cross-tab data leakage.