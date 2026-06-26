config.yaml:
chart-generator:
  version: 1.0
  engine: forge-blueprint
  output-format:
    - svg
    - chartjs-config
  chart-types:
    score-history:
      type: line
      series: multi
      x-axis: time
      y-axis: score
      y-range: [0, 100]
      legend: per-agent
    agent-distribution:
      type: donut
      segment-sort: descending
      start-angle: 0
    timeline:
      type: horizontal-bar
      orientation: horizontal
      axis: task-duration
    gpu-sparkline:
      type: sparkline
      axes: false
      labels: false
      grid: false
  defaults:
    width: 400
    height: 200
    theme: light
    show-legend: true
  dependencies:
    svg-mode: none
    chartjs-mode: chart.js-v4
  error-handling:
    invalid-input: placeholder-svg
    purity: enforced
  palette:
    light:
      background: "#ffffff"
      text: "#1a1a1a"
      grid: "#e5e5e5"
      series:
        - "#4e79a7"
        - "#f28e2b"
        - "#e15759"
        - "#76b7b2"
        - "#59a14f"
        - "#edc948"
    dark:
      background: "#1a1a2e"
      text: "#e0e0e0"
      grid: "#2d2d44"
      series:
        - "#86b7e0"
        - "#f9b56c"
        - "#f47a7a"
        - "#8cd4cb"
        - "#7fc96e"
        - "#f2df7a"