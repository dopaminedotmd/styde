Mockups: 10
mockup_01_classic_hud:
  layout: four-column grid
  row_1:
    - cpu_gauge: semicircular, 0-100%, gradient blue-to-cyan, 70% fill
    - gpu_gauge: semicircular, 0-100%, gradient green-to-yellow, 92% fill  
    - mem_gauge: semicircular, 0-128GB, 64GB fill, gradient purple-to-pink
    - disk_gauge: semicircular, 0-4TB, 2.1TB fill, gradient orange-to-red
  row_2:
    - uptime: 14d 6h 32m, green dot pulse
    - active_processes: 47, sparkline mini
    - temp: 68C, yellow warning
    - power: 450W, white
  row_3:
    - process_list: scrollable, top 5 by GPU%
    - columns: PID | NAME | GPU% | MEM | TIME
mockup_02_hex_grid:
  layout: honeycomb 2x3 + 1x2
  cells:
    - hex_1: CPU, fill_to_center 70%, core temp inside, ripple animation
    - hex_2: GPU, fill_to_center 92%, hotspot temp, glow orange
    - hex_3: RAM, fill_to_center 50%, frequency label
    - hex_4: VRAM, fill_to_center 85%, 20GB/24GB
    - hex_5: DISK, fill_to_center 52%, IO queue dot
    - hex_6: NET, fill_to_center 12%, up/down arrows
    - hex_7: UPTIME, clock icon, 14d6h
    - hex_8: POWER, 450W, efficiency %
mockup_03_terminal_hud:
  layout: monospace dark screen, green-on-black
  content:
    - header: === SYSTEM OVERVIEW === [14:32:18 UTC]
    - line_1: CPU | ████████░░ 70% | 48C | 3.2GHz
    - line_2: GPU | █████████░ 92% | 68C | 1980MHz
    - line_3: RAM | █████░░░░░ 50% | 64/128GB | 3200MT/s
    - line_4: VRAM| ████████░░ 85% | 20/24GB | HBM2e
    - line_5: DSK | █████░░░░░ 52% | R:142MB W:89MB
    - line_6: NET | █░░░░░░░░░ 12% | ↓:45Mbps ↑:12Mbps
    - line_7: UP  | 14d 6h 32m | PROC:47 | LOAD:2.3
    - divider: ─────────────────────────────────
    - footer: [PID]    NAME         GPU%   MEM   STATE
    - procs:  2304    comfyui       87%   4.2G   RUN
    - procs:  1892    python        63%   1.8G   RUN
    - procs:  3101    chrome        12%   2.1G   SLEEP
mockup_04_radial_sweep:
  layout: four large semicircular gauges stacked 2x2
  gauge_props:
    - arc_width: 12px
    - sweep_angle: 180
    - animated_fill: true
    - glow: true
  gauge_1: CPU | 70% | arc color #00d4ff | inner label "Cores: 8/16"
  gauge_2: GPU | 92% | arc color #ff6b35 | inner label "1.98GHz / 68C"
  gauge_3: MEM | 50% | arc color #a855f7 | inner label "64/128GB"
  gauge_4: VRAM | 85% | arc color #22c55e | inner label "20/24GB"
  center_decor:
    - mini_bar_cpu_per_core: 8 bars vertical
    - mini_bar_gpu_mem_freq: sparkline last 60s
mockup_05_pill_ribbon:
  layout: vertical stack of pill gauges
  each_pill:
    - type: horizontal rounded bar full width
    - height: 32px
    - has_label_left, value_right, mini_sparkline_rightmost
    - gradient_fill: true
  pills_top_to_bottom:
    - CPU: 70%, sparkline up-trend, gradient cyan-blue
    - GPU: 92%, sparkline plateau, gradient orange-red
    - RAM: 50%, sparkline steady, gradient violet-pink
    - VRAM: 85%, sparkline rising, gradient green-emerald
    - DISK IO: 52%, sparkline erratic, gradient amber
    - NET: 12%, sparkline flat, gradient slate
  below_pills:
    - uptime: 14d 6h | processes: 47 | temp: 68C | power: 450W
    - format: small text, dimmed label, bright value
mockup_06_glow_cards:
  layout: 2x4 card grid
  card_props:
    - bg: glassmorphism blur 12px
    - border: 1px rgba white 0.1
    - glow_hover: dropshadow colored 0 0 20px
  cards:
    - cpu: label "CPU", value "70%", detail "48C | 3.2GHz", glow blue
    - gpu: label "GPU", value "92%", detail "68C | 1980MHz", glow orange
    - ram: label "RAM", value "64GB", detail "50% | 3200MT/s", glow purple
    - vram: label "VRAM", value "20GB", detail "85% | HBM2e", glow green
    - disk: label "DISK", value "2.1TB", detail "52% | IO: 2.3ms", glow amber
    - net: label "NET", value "12Mbps", detail "12% | ↓45↑12", glow cyan
    - uptime: label "UPTIME", value "14d 6h", detail "Since Jun 12", glow white
    - procs: label "PROCESSES", value "47", detail "3 active GPU", glow pink
  pulse: cards with value > 80% get border glow animation
mockup_07_strip_metrics:
  layout: ultra-thin horizontal strips, full width
  strip_props:
    - height: 20px
    - bar_thickness: 4px
    - label_left: 80px fixed width
    - value_right: 50px fixed width
    - bar stretch: remaining width, colored
  strips:
    - CPU | ████████████████░░░░░░ | 70%
    - GPU | ████████████████████░░ | 92%
    - RAM | ██████████░░░░░░░░░░░░ | 50%
    - VRM | █████████████████░░░░░ | 85%
    - DSK | ██████████░░░░░░░░░░░░ | 52%
    - NET | ██░░░░░░░░░░░░░░░░░░░░ | 12%
  footer_strip:
    - layout: same width, 4 equal cells
    - uptime: 14d 6h
    - processes: 47
    - temp: 68C
    - power: 450W
mockup_08_radar_sunburst:
  layout: central radar chart, orbiting metric nodes
  center:
    - type: radar chart, 6 axes
    - axes: CPU | GPU | RAM | VRAM | DISK | NET
    - filled_area: gradient from center
    - opacity: 0.6
    - scale: 0-100%
  orbiting:
    - nodes float around radar, connected by dashed lines
    - each node shows: metric name + value
    - node_cpu: 70%, near top
    - node_gpu: 92%, near top-right, pulsing
    - node_ram: 50%, near right
    - node_vram: 85%, near bottom-right
    - node_disk: 52%, near bottom
    - node_net: 12%, near bottom-left
  orbital_info:
    - outer ring: uptime = 14d 6h, inner ring: temp = 68C
    - particles orbit along ring lines
mockup_09_vertical_meter:
  layout: single column, each metric is vertical bar cluster
  meter_props:
    - bar_width: 24px
    - bar_height: 120px
    - filled_from_bottom: gradient
    - cap: rounded
    - margin: 8px
  cluster_1_cpu:
    - label: CPU
    - value: 70%
    - bars: [70, 65, 72, 68, 80, 15, 5, 2] per-core usage
    - color: cyan gradient
  cluster_2_gpu:
    - label: GPU
    - value: 92%
    - bars: [92, 87, 95, 90] per-GPU-unit
    - color: orange gradient
    - annotation: hotspot 71C
  cluster_3_mem:
    - label: MEM
    - value: 64GB
    - stacked_bar: [used=64, free=64] 128GB total
    - color: purple gradient
  cluster_4_vram:
    - label: VRAM
    - value: 20GB
    - stacked_bar: [used=20, free=4] 24GB total
    - color: green gradient
  bottom_info:
    - horizontal bar for temperature: 68C from 0-100C
    - horizontal bar for power: 450W from 0-1000W
mockup_10_dashboard_overview_hub:
  layout: full panel, left 60% gauges, right 40% process alerter
  left_gauges:
    - type: compact donut charts, 4 in 2x2
    - each donut: radius 48px, arc 270 degrees, thickness 8px
    - donut_cpu: 70%, cyan, center text "CPU"
    - donut_gpu: 92%, orange-red, center text "GPU"  
    - donut_ram: 50%, violet, center text "RAM"
    - donut_vrm: 85%, emerald, center text "VRAM"
    - below_donuts: horizontal bar for DISK IO + NET + TEMP
    - format: mini bar + label + value per row
  right_panel:
    - header: ACTIVE PROCESSES
    - list: 4 items, each expandable
    - process_1: [PID 2304] ComfyUI | GPU 87% | 4.2G
    - process_1_detail: path /workspace/comfy | since 6h ago | priority high
    - process_2: [PID 1892] python train.py | GPU 63% | 1.8G
    - process_2_detail: path /workspace/train | since 2h ago | priority mid
    - process_3: [PID 3101] Chrome | GPU 12% | 2.1G
    - process_4: [PID 4096] Hermes Agent | GPU 5% | 0.8G
    - bottom_right: alert area, flash when any metric > 90%
    - alert_now: GPU at 92% - HIGH