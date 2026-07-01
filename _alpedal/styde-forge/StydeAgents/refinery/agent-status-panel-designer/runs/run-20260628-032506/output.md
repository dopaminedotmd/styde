agent_status_panel_mockup:
  version: 2
  format: html+css+inline_svg
  panel_spec:
    layout: horizontal_card_grid
    columns: 3
    max_agents_shown: 9
    card_height: 180px
    card_width: 320px
  agent_card:
    structure:
      - zone: avatar_ring
        position: top_left
        size: 44px
        style: circular_progress_ring
        content: agent_initial
      - zone: name_and_role
        position: top_center
        content: [agent_name, agent_role]
      - zone: score_badge
        position: top_right
        content: overall_score
        color_by_score:
          threshold_ge: 85: #00e676
          threshold_ge: 70: #ffd54f
          default: #ff5252
      - zone: status_indicator
        position: below_avatar
        states:
          running: {icon: pulse_dot, color: '#4fc3f7', label: Running}
          idle: {icon: steady_dot, color: '#9e9e9e', label: Idle}
          pending: {icon: ring_dot, color: '#ffb74d', label: Pending}
          completed: {icon: check_dot, color: '#66bb6a', label: Completed}
          error: {icon: exclamation_dot, color: '#ef5350', label: Error}
      - zone: health_bar
        position: below_name
        metric: session_health
        range: [0, 100]
        color: gradient from '#ff5252' to '#4fc3f7'
      - zone: counters
        position: bottom_row
        layout: row_3_equal
        items:
          - metric: tasks_running
            icon: play_arrow
            color: '#4fc3f7'
          - metric: tasks_completed
            icon: check
            color: '#66bb6a'
          - metric: tasks_pending
            icon: schedule
            color: '#ffb74d'
  score_display:
    type: numeric_badge
    size: large
    show_decimal: true
    decimal_places: 1
    animation: count_up_on_update
  health_bar_style:
    height: 4px
    border_radius: 2px
    background: rgba(255,255,255,0.08)
    fill: solid
    gradient_stops:
      - color: '#ff5252'
        position: 0
      - color: '#ffd54f'
        position: 50
      - color: '#4fc3f7'
        position: 100
  color_scheme:
    card_bg: rgba(18, 22, 33, 0.95)
    card_border: rgba(255, 255, 255, 0.06)
    card_border_hover: rgba(79, 195, 247, 0.4)
    text_primary: rgba(255, 255, 255, 0.92)
    text_secondary: rgba(255, 255, 255, 0.55)
    text_muted: rgba(255, 255, 255, 0.3)
    accent_blue: '#4fc3f7'
    accent_green: '#66bb6a'
    accent_amber: '#ffb74d'
    accent_red: '#ef5350'
    accent_purple: '#b39ddb'
  responsive_breakpoints:
    - screen_width_min: 1200
      columns: 3
      card_width: 320px
    - screen_width_min: 768
      columns: 2
      card_width: 280px
    - screen_width_min: 0
      columns: 1
      card_width: 100%
  interaction_states:
    idle: {transform: none, transition: 200ms}
    hover: {transform: translateY(-2px), box_shadow: '0 8px 24px rgba(0,0,0,0.3)'}
    selected: {border_color: '#4fc3f7', border_width: 2px}
  sample_data:
    - agent: Hermes-Core
      role: primary orchestrator
      score: 94.2
      status: running
      health: 88
      counters: {running: 3, completed: 27, pending: 1}
    - agent: Teacher
      role: evaluation engine
      score: 91.7
      status: idle
      health: 95
      counters: {running: 0, completed: 142, pending: 0}
    - agent: Forge-Daemon
      role: blueprint compiler
      score: 87.3
      status: running
      health: 76
      counters: {running: 2, completed: 89, pending: 4}
    - agent: Plan-Reviewer
      role: prompt validator
      score: 82.9
      status: pending
      health: 100
      counters: {running: 0, completed: 56, pending: 12}
    - agent: Codex-Connector
      role: sandbox bridge
      score: 73.5
      status: error
      health: 34
      counters: {running: 1, completed: 23, pending: 7}
  rendering_notes:
    - avatar_ring uses conic-gradient to show score as a percentage ring
    - status_indicator uses inline svg circle elements, no external icon deps
    - health_bar is a flat div with gradient fill, css-only
    - counters use inline svg icons (material-like, 16x16 viewbox)
    - card uses css grid for zone placement, no js framework
    - transitions are css-only, :hover pseudo-class
    - browsers: chrome 90+, firefox 88+, safari 14+