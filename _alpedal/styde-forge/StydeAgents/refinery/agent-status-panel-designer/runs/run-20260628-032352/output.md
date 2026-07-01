YAML
agent_status_panel:
  version: 0.5
layout:
  type: dashboard_grid
  container: full_width_card
  header:
    - metric_bar: [running: 3, pending: 7, completed: 142, failed: 2, total_sessions: 154]
    - refresh_interval: 5s
    - search_filter: text_input
    - group_dropdown: [all, running only, failed only, pending only]
  agent_cards:
    columns: 3
    breakpoints:
      - width: 1200 -> columns: 3
      - width: 800  -> columns: 2
      - width: 480  -> columns: 1
    card_spec:
      background: dark_surface_bg
      border_radius: 12px
      padding: 16px
      status_indicator:
        - type: dot
          states:
            running:  #00ff88 with pulse animation, 2s cycle
            pending:  #ffaa00 steady
            completed: #4488ff steady
            failed:    #ff3355 steady
            idle:      #666666 steady
      row_1:
        - agent_name: text_medium_bold
        - status_dot
        - score_badge:
            value: 85-100 -> #00ff88 bg
            value: 70-84  -> #44bbff bg
            value: 50-69  -> #ffaa00 bg
            value: 0-49   -> #ff3355 bg
          format: circle 32px, white text, font-weight 700
      row_2:
        - task_badge: top_task_name
        - duration: [current_run_time or last_run_duration, format HH:MM:SS]
      row_3:
        - progress_bar:
            type: thin 4px
            color: matches score_badge color
            label: step_x_of_y
            show_percent: true
      row_4:
        - metric_row:
            label: eval
            value: eval_score_numeric
            label: speed
            value: avg_response_ms
            label: sessions
            value: session_count
      row_5:
        - action_buttons:
            inspect: icon_eye -> opens detail modal
            restart: icon_rotate_cw -> triggers restart
            kill: icon_x_square -> confirmation dialog
      hover_state:
        background: slightly_lighter_surface
        transform: translateY(-2px)
        box_shadow: soft_glow matching status color
status_indicators:
  running:
    icon: filled_circle
    color: '#00ff88'
    animation: pulse 2s infinite
    label: RUNNING
  pending:
    icon: filled_circle
    color: '#ffaa00'
    animation: none
    label: PENDING
  completed:
    icon: filled_circle
    color: '#4488ff'
    animation: none
    label: COMPLETED
  failed:
    icon: filled_circle
    color: '#ff3355'
    animation: none
    label: FAILED
  idle:
    icon: outlined_circle
    color: '#666666'
    animation: none
    label: IDLE
score_badge:
  thresholds:
    excellent:
      range: 85-100
      bg: '#00ff88'
      label: Excellent
    good:
      range: 70-84
      bg: '#44bbff'
      label: Good
    fair:
      range: 50-69
      bg: '#ffaa00'
      label: Fair
    poor:
      range: 0-49
      bg: '#ff3355'
      label: Poor
health_summary_bar:
  position: below_header, above_grid
  layout: horizontal_flex, space-evenly
  items:
    - label: Overall Health
      value: aggregate_health_percent
      color: gradient from status thresholds
      format: gauge dial, 80px diameter
    - label: Avg Score
      value: aggregate_score
      format: large_number with +/- trend arrow
    - label: Agents Online
      value: count_running / total_agents
      format: fraction with sparkline
    - label: Throughput
      value: tasks_completed_last_5min
      format: number with mini_bar_chart
    - label: Error Rate
      value: failed / total_sessions * 100
      format: percentage, red if > 5%
empty_state:
  when: no agents running
  content: icon_robot_sleeping
  text: No active agents. Start a forge run to populate this panel.
  action_button: Start New Forge Run
responsiveness:
  mobile: stack to single column, hide action buttons behind overflow menu
  tablet: 2-column grid, show only icon buttons
  desktop: full 3-column grid with all details
states:
  loading: skeleton placeholders, 3 card silhouettes with shimmer animation
  error: red banner 'Failed to load agent status. Retry in 5s...' with retry button
  partial: gray banner 'Some agents unreachable. Showing cached data.' with staleness indicator
data_fetch:
  endpoint: /api/v1/agent-status
  polling: 5s interval
  cache: 30s local staleness before showing stale indicator
  fallback: last_cached_state if server unreachable
END