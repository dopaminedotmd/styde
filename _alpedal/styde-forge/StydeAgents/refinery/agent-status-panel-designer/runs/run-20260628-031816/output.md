design-mockups-forge-dashboard:
mockup-1:
  title: Agent Status Grid
  layout-strategy: css-grid
  grid-columns: 3
  grid-gap: 16
  layout-rules:
    strategy: flex
    container-width: full
    container-padding: 24
    grid-template-columns: repeat(3, 1fr)
    max-width: 1280
    centered: true
  design-tokens:
    color-primary: '#6366F1'
    color-success: '#22C55E'
    color-warning: '#F59E0B'
    color-danger: '#EF4444'
    color-bg-card: '#1E1E2E'
    color-bg-surface: '#181825'
    color-text-primary: '#CDD6F4'
    color-text-secondary: '#A6ADC8'
    color-text-muted: '#6C7086'
    color-border: '#313244'
    spacing-unit: 8
    radius-card: 12
    radius-badge: 6
    radius-bar: 4
    font-family: "'Inter', system-ui, sans-serif"
    font-size-sm: 12
    font-size-base: 14
    font-size-lg: 18
    font-size-xl: 24
    font-weight-normal: 400
    font-weight-medium: 500
    font-weight-bold: 600
    shadow-card: '0 2px 8px rgba(0,0,0,0.3)'
    shadow-hover: '0 4px 16px rgba(0,0,0,0.4)'
    transition-speed: 200
mockup-2: health-breakdown
  layout-strategy: absolute
  layout-rules:
    strategy: absolute-positioning
    container-width: full
    container-height: 240
    container-padding: 24
    background: color-bg-card
    border-radius: radius-card
    border: 1px solid color-border
  visualspecs:
    section-bar-chart:
      type: horizontal-stacked-bar
      y-offset: 48
      x-start: 24
      width: calc(100% - 48)
      bar-height: 28
      bar-gap: 12
      bar-count: 8
      bar-radius: 6
      labels:
        y-offset: 14
        x-offset-left: 0
        font-size: font-size-sm
        color: color-text-primary
        font-weight: font-weight-medium
      segments:
        healthy:
          color: color-success
          min-width: 0
        degraded:
          color: color-warning
          min-width: 0
        down:
          color: color-danger
          min-width: 0
      thresholds:
        warning-at: 70
        critical-at: 40
      color-stop-positions:
        - stop: 0
          color: color-danger
        - stop: 40
          color: color-warning
        - stop: 70
          color: color-success
          blend: true
    section-summary-strip:
      type: horizontal-metric-row
      y-offset: 12
      x-start: 24
      spacing: 32
      metrics:
        - label: Active
          value-color: color-success
          font-size: font-size-lg
          font-weight: font-weight-bold
        - label: Degraded
          value-color: color-warning
          font-size: font-size-lg
          font-weight: font-weight-bold
        - label: Down
          value-color: color-danger
          font-size: font-size-lg
          font-weight: font-weight-bold
        - label: Total
          value-color: color-text-primary
          font-size: font-size-lg
          font-weight: font-weight-bold
    section-label-column:
      y-offset: 48
      x-start: 24
      width: 160
      line-height: 40
      text-align: right
      font-size: font-size-sm
      color: color-text-primary
      font-weight: font-weight-medium
    grid-alignment:
      baseline-grid: 8
      bar-align: left
      label-align: right
      value-align: left
      group-gap: 16
mockup-3: task-log-panel
  layout-strategy: absolute
  layout-rules:
    strategy: absolute-positioning
    container-width: full
    container-height: 320
    container-padding: 24
    background: color-bg-card
    border-radius: radius-card
    border: 1px solid color-border
  visualspecs:
    section-header:
      y-offset: 0
      height: 40
      title:
        x: 0
        y: 8
        font-size: font-size-lg
        font-weight: font-weight-bold
        color: color-text-primary
      filter-controls:
        x: calc(100% - 240)
        y: 4
        width: 220
        height: 32
        radius: radius-badge
        background: color-bg-surface
        padding-horizontal: 8
    section-log-entries:
      y-offset: 52
      entry-height: 48
      entry-gap: 4
      max-entries: 5
      border-bottom: 1px solid color-border
      padding-left: 0
      padding-right: 0
      columns:
        - name: status-icon
          width: 32
          alignment: center
        - name: agent-name
          width: 140
          alignment: left
          font-weight: font-weight-medium
        - name: task-description
          width: auto
          alignment: left
          color: color-text-secondary
          truncate: true
        - name: duration
          width: 72
          alignment: right
          font-size: font-size-sm
          color: color-text-muted
    section-status-dot-spec:
      type: inline-svg-circle
      radius: 5
      fill-by-status:
        running: color-success
        pending: color-warning
        completed: color-text-muted
        failed: color-danger
      pulse-animation:
        running: true
        speed: 1500
      label-offset:
        x: 12
        y: 4
      font-size: font-size-sm
      color: color-text-primary
    section-progress-bar-entry:
      type: horizontal-bar-timeline
      height: 6
      radius: radius-bar
      background: color-bg-surface
      fill: color-primary
      y-offset: 6
      label-offset:
        x: 48
        y: -4
mockup-4: agent-status-card
  layout-strategy: flex
  layout-rules:
    strategy: flex-column
    padding: 16
    gap: 12
    background: color-bg-card
    border-radius: radius-card
    border: 1px solid color-border
    shadow: shadow-card
    hover-shadow: shadow-hover
    transition: transition-speed
  visualspecs:
    section-agent-header:
      type: flex-row
      gap: 12
      align-items: center
      avatar:
        width: 36
        height: 36
        radius: 50pct
        border: 2px solid color-primary
      agent-name:
        font-size: font-size-base
        font-weight: font-weight-bold
        color: color-text-primary
      status-badge:
        height: 22
        padding-horizontal: 8
        radius: radius-badge
        font-size: font-size-sm
        font-weight: font-weight-medium
        background-by-status:
          running: 'rgba(34,197,94,0.15)'
          pending: 'rgba(245,158,11,0.15)'
          completed: 'rgba(108,112,134,0.15)'
          failed: 'rgba(239,68,68,0.15)'
        color-by-status:
          running: color-success
          pending: color-warning
          completed: color-text-muted
          failed: color-danger
    section-score-ring:
      type: svg-conic-ring
      width: 64
      height: 64
      stroke-width: 5
      radius: 27
      center: 32
      fill-color: none
      track-color: color-bg-surface
      progress-color: color-primary
      label:
        font-size: font-size-lg
        font-weight: font-weight-bold
        color: color-text-primary
        y-offset: 4
    section-metrics-row:
      type: flex-row
      gap: 8
      justify: space-between
      metric-item:
        type: flex-column
        gap: 2
        align: center
        label:
          font-size: font-size-sm
          color: color-text-muted
        value:
          font-size: font-size-base
          font-weight: font-weight-bold
          color: color-text-primary
      metrics:
        - label: tasks
          key: task-count
        - label: score
          key: composite-score
          color: color-primary
        - label: health
          key: health-pct
          color-by-range:
            - min: 90
              color: color-success
            - min: 60
              color: color-warning
            - min: 0
              color: color-danger
mockup-5: diff-bar-visual
  layout-strategy: absolute
  layout-rules:
    strategy: absolute-positioning
    container-width: full
    container-height: 80
    container-padding: 16 24
    background: color-bg-surface
    border-radius: radius-card
    border: 1px solid color-border
  visualspecs:
    section-diff-bar:
      type: horizontal-segmented-bar
      y-offset: 28
      x-start: 0
      width: full
      height: 12
      radius: radius-bar
      background: color-border
      segments:
        - color: color-success
          label: improvement
          weight-key: score-up
        - color: color-danger
          label: regression
          weight-key: score-down
        - color: color-text-muted
          label: unchanged
          weight-key: score-stable
      color-stop-positions:
        - threshold: 0
          color: color-danger
        - threshold: 40
          color: color-warning
        - threshold: 70
          color: color-success
          blend: true
      threshold-labels:
        font-size: 10
        color: color-text-muted
        offset-y: 20
        position: below-bar
      label-offset-rules:
        segment-label:
          y: -18
          font-size: font-size-sm
          font-weight: font-weight-medium
          color: color-text-secondary
        value-label:
          y: -18
          x: auto
          font-size: font-size-sm
          font-weight: font-weight-bold
          color: color-text-primary
    section-summary-line:
      type: text-row
      y-offset: 4
      spacing: 16
      items:
        - text: +12
          color: color-success
          font-weight: font-weight-bold
          font-size: font-size-base
        - text: from last run
          color: color-text-muted
          font-size: font-size-sm
component-hierarchy:
  agent-status-grid: mockup-1
  children:
    - agent-status-card: mockup-4
    - health-breakdown: mockup-2
    - task-log-panel: mockup-3
    - diff-bar-visual: mockup-5
interaction-spec:
  hover-state-card:
    shadow: shadow-hover
    border-color: color-primary
    transform: translateY(-2)
    transition: 200ms ease
  click-state-card:
    transform: translateY(0)
    border-color: color-primary
    shadow: shadow-card
  status-dot-pulse:
    running:
      animation: pulse 1.5s infinite
      keyframes:
        from: opacity 1.0
        to: opacity 0.4
  score-ring-animation:
    type: conic-grow
    duration: 800
    easing: ease-out
    start-angle: -90
  live-filter:
    type: debounced-input
    delay: 300
    target: task-log-entries
    match-fields:
      - agent-name
      - task-description
    reset-on-empty: true
design-principles:
  glanceable: true
  color-constrained: true
  status-first: true
  progressive-disclosure: true
  dark-theme: true
  responsive-grid: collapse to single-column below 768px
  score-prominence: composite score is primary visual anchor on each card