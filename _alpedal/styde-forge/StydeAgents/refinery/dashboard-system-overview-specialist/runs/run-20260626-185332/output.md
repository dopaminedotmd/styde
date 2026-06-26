panel_spec:
  id: system-overview
  label: System Overview
  version: 2
layout_spec:
  panel_height: 380px
  tokenized_spacing:
    cell_size: var(--space-md)
    gap: var(--space-xs)
    padding: var(--space-sm)
  sub_panels:
    - id: resource-gauges
      label: Resource Gauges
      rows: 4
      row_height: var(--space-md)
      gap: var(--space-xs)
      computed: 4 * 44px + 3 * 8px = 200px
    - id: active-processes
      label: Active Processes
      rows: 3
      row_height: var(--space-md)
      gap: var(--space-xs)
      computed: 3 * 44px + 2 * 8px = 148px
    - id: health-indicators
      label: Health Indicators
      rows: 1
      row_height: var(--space-md)
      computed: 44px
layout_validation:
  sub_total: 200px + 148px + 44px = 392px
  gaps_between: 2 * var(--space-xs) = 16px
  padding: 2 * var(--space-sm) = 16px
  total: 392px + 16px + 16px = 424px
  note: exceeds 380px cap by 44px — reduce resource-gauges to 3 rows (156px) for total=156+148+44+16+16=380px exactly
resource_gauges:
  - id: gpu-util
    label: GPU Util
    type: radial-gauge
    range: 0-100
    unit: "%"
    thresholds:
      warn: 80
      crit: 95
    css_token: --color-gpu
    aria_label: GPU utilization gauge, {value} percent
  - id: gpu-mem
    label: GPU Mem
    type: radial-gauge
    range: 0-100
    unit: "%"
    thresholds:
      warn: 85
      crit: 95
    css_token: --color-gpu-mem
    aria_label: GPU memory gauge, {value} percent
  - id: cpu-load
    label: CPU Load
    type: radial-gauge
    range: 0-100
    unit: "%"
    thresholds:
      warn: 75
      crit: 90
    css_token: --color-cpu
    aria_label: CPU load gauge, {value} percent
  - id: mem-load
    label: Memory
    type: radial-gauge
    range: 0-100
    unit: "%"
    thresholds:
      warn: 80
      crit: 90
    css_token: --color-memory
    aria_label: Memory usage gauge, {value} percent
active_processes:
  - name: forge-worker-01
    pid: 1823
    status: running
    cpu: 12.4
    mem: 1.2
    uptime: 4h32m
  - name: forge-worker-02
    pid: 1891
    status: running
    cpu: 8.7
    mem: 0.9
    uptime: 4h30m
  - name: dashboard-server
    pid: 1702
    status: running
    cpu: 3.1
    mem: 0.4
    uptime: 4h35m
health_indicators:
  uptime:
    value: 4h35m
    label: Uptime
    icon: clock
  temperature:
    value: 68
    unit: "°C"
    label: Temp
    icon: thermometer
    threshold_crit: 85
  process_count:
    value: 3
    label: Active
    icon: layers
responsive:
  breakpoints:
    - min_width: 0px
      columns: 1
    - min_width: 768px
      columns: 2
    - min_width: 1200px
      columns: 3
accessibility:
  - focus_indicators: 2px outline offset 2px on all interactive elements
  - aria_labels on all gauges using template strings
  - color_not_sole_indicator: add text labels beneath each gauge
  - reduced_motion: respect prefers-reduced-motion, disable gauge animations
dark_mode:
  tokens:
    bg_panel: var(--color-surface-2)
    gauge_track: var(--color-surface-3)
    text_primary: var(--color-text-primary)
    text_dim: var(--color-text-dim)
    border: var(--color-border)
  note: all gauge colors (--color-gpu, --color-cpu, etc.) invert automatically via CSS color-mix or data-theme attribute