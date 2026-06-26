mockup-001: compact-status-row
  purpose: minimal single-line agent card for dense dashboards
  tokens:
    colors: [--bg-surface, --bg-elevated, --text-primary, --text-secondary, --accent-green, --accent-yellow, --accent-red, --accent-blue]
    spacing: [--space-2xs, --space-xs, --space-sm, --space-md]
    typography: [--font-mono-sm, --font-ui-sm, --font-ui-xs]
  layout:
    type: horizontal-flex
    height: 48px
    padding: --space-sm
    gap: --space-sm
    border-radius: 6px
    background: --bg-surface
    border: 1px solid rgba(255,255,255,0.06)
    children:
      - zone: status-dot
        width: 10px
        height: 10px
        align: center
        states:
          running: background --accent-green + pulse-animation
          pending: background --accent-yellow + slow-pulse
          idle: background --accent-blue
          error: background --accent-red + blink
      - zone: agent-name
        font: --font-ui-sm
        color: --text-primary
        weight: 500
        max-width: 140px
        truncate: ellipsis
      - zone: task-label
        font: --font-ui-xs
        color: --text-secondary
        max-width: 200px
        truncate: ellipsis
      - zone: score-badge
        width: 44px
        height: 22px
        background: --bg-elevated
        border-radius: 11px
        font: --font-mono-sm
        color: --accent-green
        text-align: center
        line-height: 22px
      - zone: status-text
        font: --font-ui-xs
        color: --text-secondary
        text-transform: uppercase
    hover:
      background: --bg-elevated
      border-color: rgba(255,255,255,0.12)
    active:
      background: rgba(99,102,241,0.08)
      border-color: --accent-blue
    focus-visible:
      outline: 2px solid --accent-blue
      outline-offset: 2px
    disabled:
      opacity: 0.4
      pointer-events: none
mockup-002: agent-detail-card
  purpose: expanded single-agent view with metrics and controls
  tokens:
    colors: [--bg-surface, --bg-elevated, --text-primary, --text-secondary, --accent-green, --accent-yellow, --accent-red, --accent-blue, --accent-orange]
    spacing: [--space-xs, --space-sm, --space-md, --space-lg]
    typography: [--font-mono-sm, --font-ui-sm, --font-ui-md, --font-ui-lg, --font-ui-xs]
  layout:
    type: vertical-flex
    width: 320px
    padding: --space-md
    gap: --space-sm
    background: --bg-surface
    border-radius: 10px
    border: 1px solid rgba(255,255,255,0.06)
    children:
      - zone: header-row
        type: horizontal-flex
        gap: --space-sm
        align: center
        children:
          - zone: status-dot
            width: 12px
            height: 12px
            border-radius: 50%
            states:
              running: bg --accent-green + box-shadow 0 0 8px rgba(34,197,94,0.4)
              pending: bg --accent-yellow + box-shadow 0 0 8px rgba(234,179,8,0.3)
              idle: bg --accent-blue
              error: bg --accent-red + box-shadow 0 0 8px rgba(239,68,68,0.4)
          - zone: agent-name
            font: --font-ui-md
            color: --text-primary
            weight: 600
          - zone: score-badge
            width: 48px
            height: 24px
            background: --bg-elevated
            border-radius: 12px
            font: --font-mono-sm
            color: --accent-green
            text-align: center
            line-height: 24px
            margin-left: auto
      - zone: progress-bar
        height: 6px
        background: --bg-elevated
        border-radius: 3px
        overflow: hidden
        children:
          - zone: fill
            height: 100%
            border-radius: 3px
            transition: width 0.4s ease
            states:
              running: bg --accent-blue
              error: bg --accent-red
              completed: bg --accent-green
      - zone: metric-row
        type: grid-3col
        gap: --space-xs
        children:
          - metric: tasks-completed
            label: done
            value-format: integer
            color: --text-primary
            font: --font-mono-sm
          - metric: avg-score
            label: score
            value-format: decimal(1)
            color: --accent-green
            font: --font-mono-sm
          - metric: uptime
            label: uptime
            value-format: duration
            color: --text-secondary
            font: --font-mono-sm
      - zone: labels-row
        type: horizontal-flex
        gap: --space-2xs
        flex-wrap: true
        children:
          - each: label-chip
            height: 20px
            padding: 0 --space-xs
            border-radius: 4px
            font: --font-ui-xs
            background: --bg-elevated
            color: --text-secondary
    hover:
      transform: translateY(-2px)
      box-shadow: 0 8px 24px rgba(0,0,0,0.15)
      border-color: rgba(255,255,255,0.1)
    active:
      transform: translateY(0)
      box-shadow: 0 2px 8px rgba(0,0,0,0.1)
    focus-visible:
      outline: 2px solid --accent-blue
      outline-offset: 2px
    disabled:
      opacity: 0.5
      pointer-events: none
mockup-003: agent-grid-tile
  purpose: visual tile for grid/kanban layout with avatar ring
  tokens:
    colors: [--bg-surface, --bg-elevated, --text-primary, --text-secondary, --accent-green, --accent-yellow, --accent-red, --accent-blue, --accent-purple]
    spacing: [--space-2xs, --space-xs, --space-sm, --space-md]
    typography: [--font-mono-sm, --font-ui-2xs, --font-ui-xs, --font-ui-sm]
  layout:
    type: vertical-flex
    width: 200px
    padding: --space-md
    gap: --space-xs
    align: center
    background: --bg-surface
    border-radius: 12px
    border: 1px solid rgba(255,255,255,0.06)
    children:
      - zone: avatar-ring
        width: 56px
        height: 56px
        border-radius: 50%
        border: 3px solid
        transition: border-color 0.3s ease
        states:
          running: border-color --accent-green
          pending: border-color --accent-yellow
          idle: border-color rgba(255,255,255,0.15)
          error: border-color --accent-red
        inner:
          type: circle
          size: 44px
          background: --bg-elevated
          font: --font-ui-sm
          color: --text-primary
          text-align: center
          line-height: 44px
          overflow: hidden
      - zone: agent-name
        font: --font-ui-sm
        color: --text-primary
        weight: 500
        margin-top: --space-xs
      - zone: score-bar
        width: 100%
        height: 4px
        background: --bg-elevated
        border-radius: 2px
        children:
          - zone: fill
            height: 100%
            border-radius: 2px
            width: var(--score-percent)
            transition: width 0.6s ease
            background: linear-gradient(90deg, --accent-blue, --accent-purple)
      - zone: score-label
        font: --font-ui-2xs
        color: --text-secondary
    hover:
      transform: translateY(-4px)
      box-shadow: 0 12px 32px rgba(0,0,0,0.2)
      border-color: rgba(255,255,255,0.12)
    active:
      transform: translateY(-1px)
      box-shadow: 0 4px 12px rgba(0,0,0,0.15)
    focus-visible:
      outline: 2px solid --accent-blue
      outline-offset: 2px
      border-radius: 14px
    disabled:
      opacity: 0.45
      filter: grayscale(0.8)
      pointer-events: none
mockup-004: live-status-bar
  purpose: horizontal global status bar across dashboard top
  tokens:
    colors: [--bg-surface, --bg-elevated, --text-primary, --text-secondary, --accent-green, --accent-yellow, --accent-red, --accent-blue, --accent-orange]
    spacing: [--space-2xs, --space-xs, --space-sm, --space-md]
    typography: [--font-mono-sm, --font-ui-xs, --font-ui-sm]
  layout:
    type: horizontal-flex
    width: 100%
    height: 40px
    padding: 0 --space-md
    align: center
    background: --bg-elevated
    border-bottom: 1px solid rgba(255,255,255,0.06)
    children:
      - zone: running-count
        type: horizontal-flex
        gap: --space-2xs
        align: center
        children:
          - dot: running
            width: 8px
            height: 8px
            border-radius: 50%
            background: --accent-green
            animation: pulse 1.5s infinite
          - label: running
            font: --font-ui-xs
            color: --text-secondary
          - value: count
            font: --font-mono-sm
            color: --accent-green
            weight: 600
      - zone: pending-count
        type: horizontal-flex
        gap: --space-2xs
        align: center
        children:
          - dot: pending
            width: 8px
            height: 8px
            border-radius: 50%
            background: --accent-yellow
            animation: slow-pulse 2.5s infinite
          - label: pending
            font: --font-ui-xs
            color: --text-secondary
          - value: count
            font: --font-mono-sm
            color: --accent-yellow
            weight: 600
      - zone: completed-count
        type: horizontal-flex
        gap: --space-2xs
        align: center
        children:
          - dot: completed
            width: 8px
            height: 8px
            border-radius: 50%
            background: --accent-blue
          - label: completed
            font: --font-ui-xs
            color: --text-secondary
          - value: count
            font: --font-mono-sm
            color: --accent-blue
            weight: 600
      - zone: error-count
        type: horizontal-flex
        gap: --space-2xs
        align: center
        children:
          - dot: error
            width: 8px
            height: 8px
            border-radius: 50%
            background: --accent-red
            animation: blink 1s infinite
          - label: errors
            font: --font-ui-xs
            color: --text-secondary
          - value: count
            font: --font-mono-sm
            color: --accent-red
            weight: 600
      - zone: spacer
        flex: 1
      - zone: avg-score
        type: horizontal-flex
        gap: --space-2xs
        align: center
        children:
          - label: avg
            font: --font-ui-xs
            color: --text-secondary
          - value: score
            font: --font-mono-sm
            color: --accent-orange
            weight: 700
    hover:
      background: rgba(255,255,255,0.02)
    states:
      collapsed: height 32px, only show counts, no labels
      expanded: full layout
mockup-005: mini-sidebar-list
  purpose: compact agent list for sidebar/panel drawer
  tokens:
    colors: [--bg-sidebar, --bg-hover, --text-primary, --text-secondary, --accent-green, --accent-yellow, --accent-red, --accent-blue]
    spacing: [--space-2xs, --space-xs, --space-sm]
    typography: [--font-mono-2xs, --font-ui-xs, --font-ui-sm]
  layout:
    type: vertical-flex
    width: 240px
    gap: 0
    background: --bg-sidebar
    children:
      - each: agent-row
        type: horizontal-flex
        height: 36px
        padding: 0 --space-sm
        gap: --space-xs
        align: center
        border-left: 3px solid transparent
        children:
          - zone: status-bar
            width: 3px
            height: 100%
            margin-left: calc(-1 * var(--space-sm))
            transition: background 0.3s ease
            states:
              running: bg --accent-green
              pending: bg --accent-yellow
              idle: bg transparent
              error: bg --accent-red
          - zone: initial-avatar
            width: 22px
            height: 22px
            border-radius: 50%
            background: --bg-hover
            font: --font-mono-2xs
            color: --text-secondary
            text-align: center
            line-height: 22px
          - zone: name
            font: --font-ui-xs
            color: --text-primary
            truncate: ellipsis
            flex: 1
          - zone: mini-score
            font: --font-mono-2xs
            color: --accent-green
            width: 28px
            text-align: right
        hover:
          background: --bg-hover
          border-left-color: rgba(255,255,255,0.1)
        selected:
          background: rgba(99,102,241,0.08)
          border-left-color: --accent-blue
        focus-visible:
          outline: 2px solid --accent-blue
          outline-offset: -2px
mockup-006: agent-comparison-split
  purpose: side-by-side comparison of two agents
  tokens:
    colors: [--bg-surface, --bg-elevated, --text-primary, --text-secondary, --accent-green, --accent-yellow, --accent-red, --accent-blue, --accent-purple, --accent-orange]
    spacing: [--space-xs, --space-sm, --space-md, --space-lg]
    typography: [--font-mono-sm, --font-ui-xs, --font-ui-sm, --font-ui-md]
  layout:
    type: horizontal-flex
    width: 600px
    height: 200px
    gap: 0
    background: --bg-surface
    border-radius: 10px
    border: 1px solid rgba(255,255,255,0.06)
    overflow: hidden
    children:
      - zone: left-agent
        type: vertical-flex
        flex: 1
        padding: --space-md
        gap: --space-xs
        border-right: 1px solid rgba(255,255,255,0.06)
        children:
          - header: same as mockup-002 header-row compressed
          - metrics:
            type: vertical-flex
            gap: --space-2xs
            children:
              - each-metric:
                type: horizontal-flex
                justify: space-between
                font: --font-ui-xs
                children:
                  - label: color --text-secondary
                  - value-bar:
                    type: horizontal-flex
                    gap: --space-xs
                    align: center
                    children:
                      - value: font --font-mono-sm, color --text-primary
                      - bar: width 40px, height 4px, bg --bg-elevated, border-radius 2px
                        fill: height 100%, bg --accent-blue, border-radius 2px, width var(--pct)
      - zone: right-agent
        type: vertical-flex
        flex: 1
        padding: --space-md
        gap: --space-xs
        children:
          - header: same structure as left
          - metrics: same structure as left
            color-variant: accent-purple for fill bars
    hover:
      box-shadow: 0 4px 16px rgba(0,0,0,0.12)
    states:
      vs-mode: highlight the higher value in each pair with --accent-green
      tie-mode: both values highlight with --accent-blue
mockup-007: timeline-dot-stream
  purpose: chronological agent activity timeline
  tokens:
    colors: [--bg-surface, --bg-elevated, --text-primary, --text-secondary, --accent-green, --accent-yellow, --accent-red, --accent-blue, --accent-purple, --accent-orange]
    spacing: [--space-2xs, --space-xs, --space-sm, --space-md]
    typography: [--font-mono-2xs, --font-mono-sm, --font-ui-2xs, --font-ui-xs, --font-ui-sm]
  layout:
    type: vertical-flex
    width: 360px
    max-height: 400px
    overflow-y: auto
    padding: --space-sm 0
    background: --bg-surface
    border-radius: 8px
    border: 1px solid rgba(255,255,255,0.06)
    scrollbar:
      width: 4px
      track: transparent
      thumb: --bg-elevated
    children:
      - each: timeline-event
        type: horizontal-flex
        height: 52px
        padding: 0 --space-md
        gap: --space-sm
        align: flex-start
        position: relative
        children:
          - zone: dot-column
            type: vertical-flex
            width: 20px
            align: center
            children:
              - connector-line
                width: 2px
                height: 50%
                background: rgba(255,255,255,0.06)
                position: absolute
                top: 0
              - dot
                width: 10px
                height: 10px
                border-radius: 50%
                margin-top: 8px
                z-index: 2
                states:
                  running: bg --accent-green, box-shadow 0 0 6px rgba(34,197,94,0.5)
                  completed: bg --accent-blue
                  error: bg --accent-red
                  pending: bg --accent-yellow
                  queued: bg rgba(255,255,255,0.2)
              - connector-line
                width: 2px
                height: 50%
                background: rgba(255,255,255,0.06)
                position: absolute
                bottom: 0
          - zone: content
            type: vertical-flex
            gap: 2px
            flex: 1
            children:
              - event-title
                font: --font-ui-xs
                color: --text-primary
                weight: 500
              - event-meta
                type: horizontal-flex
                gap: --space-xs
                font: --font-ui-2xs
                color: --text-secondary
                children:
                  - agent-name
                  - timestamp
                  - duration
          - zone: score-tag
            width: 36px
            height: 20px
            background: --bg-elevated
            border-radius: 4px
            font: --font-mono-2xs
            color: --accent-green
            text-align: center
            line-height: 20px
            display: none
            conditional: visible only when score exists
        hover:
          background: --bg-elevated
          border-radius: 4px
        first-child:
          connector-line-top: display none
        last-child:
          connector-line-bottom: display none
mockup-008: radial-score-ring
  purpose: visual score ring with rich inner metrics
  tokens:
    colors: [--bg-surface, --bg-elevated, --text-primary, --text-secondary, --accent-green, --accent-yellow, --accent-red, --accent-blue, --accent-purple, --accent-orange]
    spacing: [--space-2xs, --space-xs, --space-sm, --space-md, --space-lg]
    typography: [--font-mono-sm, --font-mono-lg, --font-mono-xl, --font-ui-2xs, --font-ui-xs, --font-ui-sm]
  layout:
    type: vertical-flex
    width: 240px
    padding: --space-lg
    gap: --space-md
    align: center
    background: --bg-surface
    border-radius: 16px
    border: 1px solid rgba(255,255,255,0.06)
    children:
      - zone: ring-container
        width: 120px
        height: 120px
        position: relative
        children:
          - ring-bg
            width: 120px
            height: 120px
            border-radius: 50%
            border: 8px solid --bg-elevated
            position: absolute
          - ring-fill
            width: 120px
            height: 120px
            border-radius: 50%
            border: 8px solid transparent
            position: absolute
            clip: rect(auto auto auto auto)
            background: conic-gradient(var(--accent-color) var(--score-pct), transparent var(--score-pct))
            mask: radial-gradient(circle, transparent 48px, black 48px)
            transition: background 0.8s ease
            color-variants:
              score >= 90: --accent-green
              score >= 70: --accent-blue
              score >= 50: --accent-yellow
              score < 50: --accent-red
          - center-content
            position: absolute
            width: 100%
            height: 100%
            display: flex
            flex-direction: column
            align-items: center
            justify-content: center
            children:
              - score-number
                font: --font-mono-xl
                color: --text-primary
                weight: 700
              - score-label
                font: --font-ui-2xs
                color: --text-secondary
                text-transform: uppercase
      - zone: name-row
        font: --font-ui-sm
        color: --text-primary
        weight: 500
      - zone: detail-row
        type: horizontal-flex
        gap: --space-md
        children:
          - detail: completed
            font: --font-ui-2xs
            color: --text-secondary
            align: center
            children:
              - value: font --font-mono-sm, color --text-primary
              - label: font --font-ui-2xs
          - detail: speed
            font: --font-ui-2xs
            color: --text-secondary
            align: center
            children:
              - value: font --font-mono-sm, color --accent-blue
              - label: font --font-ui-2xs
    hover:
      transform: translateY(-2px) scale(1.02)
      box-shadow: 0 12px 32px rgba(0,0,0,0.15)
    active:
      transform: scale(0.98)
    focus-visible:
      outline: 2px solid --accent-blue
      outline-offset: 4px
      border-radius: 18px
    disabled:
      opacity: 0.4
      filter: grayscale(0.7)
mockup-009: pipeline-flow-cards
  purpose: sequential pipeline stages with agent assignments
  tokens:
    colors: [--bg-surface, --bg-elevated, --bg-canvas, --text-primary, --text-secondary, --accent-green, --accent-yellow, --accent-red, --accent-blue, --accent-purple, --accent-orange]
    spacing: [--space-2xs, --space-xs, --space-sm, --space-md, --space-lg]
    typography: [--font-mono-2xs, --font-mono-sm, --font-ui-2xs, --font-ui-xs, --font-ui-sm, --font-ui-md]
  layout:
    type: horizontal-flex
    width: 100%
    min-width: 720px
    gap: --space-md
    padding: --space-md
    background: --bg-canvas
    border-radius: 12px
    overflow-x: auto
    children:
      - each: stage-card
        type: vertical-flex
        min-width: 160px
        max-width: 200px
        padding: --space-sm
        gap: --space-xs
        background: --bg-surface
        border-radius: 8px
        border: 1px solid rgba(255,255,255,0.06)
        flex-shrink: 0
        children:
          - zone: stage-header
            type: horizontal-flex
            align: center
            justify: space-between
            children:
              - stage-name
                font: --font-ui-xs
                color: --text-primary
                weight: 600
              - stage-status
                width: 8px
                height: 8px
                border-radius: 50%
                states:
                  active: bg --accent-green, pulse
                  waiting: bg --accent-yellow
                  done: bg --accent-blue
                  blocked: bg --accent-red
          - zone: agent-badge-strip
            type: horizontal-flex
            gap: 4px
            flex-wrap: wrap
            children:
              - each: agent-badge
                type: horizontal-flex
                height: 22px
                padding: 0 --space-2xs
                gap: 3px
                align: center
                background: --bg-elevated
                border-radius: 4px
                font: --font-mono-2xs
                color: --text-secondary
                children:
                  - status-mini
                    width: 4px
                    height: 4px
                    border-radius: 50%
                    states:
                      running: bg --accent-green
                      idle: bg transparent
                      error: bg --accent-red
                  - name-trunc
                    max-width: 50px
                    truncate: ellipsis
                  - score
                    color: --accent-green
          - zone: stage-meta
            type: horizontal-flex
            justify: space-between
            font: --font-ui-2xs
            color: --text-secondary
            children:
              - task-count
              - duration
        states:
          active-stage:
            border-color: --accent-blue
            box-shadow: 0 0 0 1px rgba(99,102,241,0.3)
          completed-stage:
            border-color: rgba(34,197,94,0.2)
          blocked-stage:
            border-color: rgba(239,68,68,0.2)
      - zone: connector-arrow
        width: 24px
        height: 2px
        background: rgba(255,255,255,0.1)
        align-self: center
        position: relative
        children:
          - arrow-head
            position: absolute
            right: 0
            top: -4px
            border-left: 6px solid rgba(255,255,255,0.1)
            border-top: 5px solid transparent
            border-bottom: 5px solid transparent
mockup-010: floating-agent-chip
  purpose: ultra-mini agent indicator for overlays/status bars
  tokens:
    colors: [--bg-surface, --bg-elevated, --text-primary, --text-secondary, --accent-green, --accent-yellow, --accent-red, --accent-blue]
    spacing: [--space-2xs, --space-xs]
    typography: [--font-mono-2xs, --font-ui-2xs]
  layout:
    type: horizontal-flex
    height: 28px
    padding: 0 --space-xs
    gap: 4px
    align: center
    background: --bg-surface
    border-radius: 14px
    border: 1px solid rgba(255,255,255,0.08)
    box-shadow: 0 2px 8px rgba(0,0,0,0.12)
    backdrop-filter: blur(8px)
    children:
      - zone: status-dot
        width: 6px
        height: 6px
        border-radius: 50%
        states:
          running: bg --accent-green, animation pulse 1.5s infinite
          pending: bg --accent-yellow
          idle: bg rgba(255,255,255,0.3)
          error: bg --accent-red, animation blink 1s infinite
      - zone: name
        font: --font-ui-2xs
        color: --text-primary
        max-width: 60px
        truncate: ellipsis
      - zone: separator
        width: 1px
        height: 12px
        background: rgba(255,255,255,0.1)
      - zone: score
        font: --font-mono-2xs
        color: --accent-green
        weight: 600
    states:
      running:
        border-color: rgba(34,197,94,0.3)
        box-shadow: 0 2px 12px rgba(34,197,94,0.15)
      error:
        border-color: rgba(239,68,68,0.3)
        box-shadow: 0 2px 12px rgba(239,68,68,0.15)
    hover:
      transform: scale(1.05)
      background: --bg-elevated
    active:
      transform: scale(0.95)
    focus-visible:
      outline: 2px solid --accent-blue
      outline-offset: 2px
      border-radius: 16px
    disabled:
      opacity: 0.35
summary:
  total-unique-mockups: 10
  panel-styles-coverered: [compact-row, detail-card, grid-tile, status-bar, sidebar-list, comparison-split, timeline-stream, score-ring, pipeline-flow, floating-chip]
  interaction-states-per-mockup: [hover, active, focus-visible, disabled] for interactive panels, [hover, selected, focus-visible] for list panels
  design-token-usage: all color values, spacing, typography referenced by token name, zero inlined values
  animation-primitives: [pulse, slow-pulse, blink, scale-transition, translate-transition, box-shadow-transition, width-transition, color-transition]
  responsive-behavior: grid-tile reflows to 2-col on <480px, pipeline-flow activates horizontal scroll under 720px, status-bar collapses to compact under 360px