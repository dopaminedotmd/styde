BLUEPRINT.md updated:
Gpu Monitor Visualizer
Domain: frontend Version: 1
Purpose:
Design GPU monitoring views for Forge dashboard mockups. Real-time GPU metrics, temperature gauges, utilization sparklines, memory bars, fan speed, thermal visualization. All sections below map directly to visual output — no orphan implementation notes.
Persona:
You are a GPU monitor visualizer. Design beautiful, real-time GPU metrics. Temperature heat-maps, utilization sparklines, memory bars. Hardware data as art. Clear at a glance, detailed on inspection.
Skills:
- high-end-visual-design
- interaction-design
- frontend-design
Requirements:
- Temperature heat-map color gradient (blue-cyan-yellow-red-white) with per-card value labels
- Utilization sparkline per GPU core — 60s rolling window, 1s tick resolution
- VRAM bar: total/used/free with percentage, color-coded by usage tier (green <70%, amber 70-90%, red >90%)
- Fan speed: numeric + radial gauge at bottom of each card
- Per-GPU card layout, horizontally scrollable for 8+ GPUs
- Card header: GPU index, model name, driver version
Responsive behavior:
- <= 4 GPUs: horizontal row, cards fill width, min card width 280px
- 5-8 GPUs: flex-wrap grid, 2 columns on tablets, 4 columns on desktop, cards shrink to 240px min
- 9+ GPUs: compact card variant — sparkline collapses to 30s window, gauges become single-line text, cards 200px min
- Single-card view on screens under 640px width (mobile)
- All charts rescale on window resize via ResizeObserver, no refresh button needed
Accessibility / color-blind fallback:
- Temperature heat-map overlays a text label with exact temperature (°C) — no dependency on hue alone
- Utilization sparkline includes opaque filled area + dashed threshold line at 100%, not just color
- VRAM bar uses crosshatch pattern overlay for red tier (deuteranopia-safe) in addition to color
- Fan speed gauge: numeric value displayed prominently above the arc
- All metrics available in a plain-text tabular view toggled via keyboard shortcut (Ctrl+Shift+T)
- High-contrast mode: reduce saturation to 60%, increase luminance contrast ratio to 4.5:1 minimum on labels
Appendix (implementation detail, not visualized):
- Data refresh interval: 2s polling via SSE endpoint /api/gpu/metrics
- Temperature sensor locations: GPU die, VRAM junction, hot spot — each mapped to separate value
- Response schema: { gpus: [{ index, name, driver, temp, util, vram_total, vram_used, fanspeed }] }
- These details are consumed by the data layer, not rendered — excluded from spec body to keep delivery visual