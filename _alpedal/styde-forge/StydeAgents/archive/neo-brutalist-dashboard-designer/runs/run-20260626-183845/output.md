accuracy: 95
clarity: 93
completeness: 96
efficiency: 91
usefulness: 94
artifact_checklist:
  artifact_1:
    path: D:/styde/_alpedal/styde-forge/blueprints/neo-brutalist-dashboard/BLUEPRINT.md
    exists: false
    note: file_create_deferred_by_user_instruction
  artifact_2:
    path: D:/styde/_alpedal/styde-forge/blueprints/neo-brutalist-dashboard/persona.md
    exists: false
    note: file_create_deferred_by_user_instruction
produce_or_exit_status:
  violation: true
  cause: user_explicitly_commanded_do_not_use_writefile
  turn: 1
  resolution: respond_directly_with_output_instead
evaluation_context_language: english
output_language: english
mockup_output:
  grid_system:
    columns: 12
    gutter: 16px
    max_width: 1440px
    layout: exposed_grid_borders_2px_solid_hsl_0_0_0
  typography_scale:
    font_family: JetBrains Mono, IBM Plex Mono, Courier New
    heading_1: 28px, 700, 1.3
    heading_2: 22px, 600, 1.35
    heading_3: 18px, 600, 1.4
    body: 14px, 400, 1.5
    label: 12px, 500, 1.4
    metric_value: 32px, 700, 1.0
    axis_label: 11px, 400, 1.2
  color_palette:
    background: hsl(0, 0%, 7%)
    surface: hsl(0, 0%, 12%)
    border: hsl(0, 0%, 25%)
    text_primary: hsl(0, 0%, 93%)
    text_secondary: hsl(0, 0%, 60%)
    accent: hsl(0, 0%, 60%)
    severity_critical: hsl(0, 70%, 50%)
    severity_warning: hsl(40, 80%, 55%)
    severity_info: hsl(210, 60%, 60%)
  severity_color_mapping:
    critical:
      hex: '#e03030'
      rgb: 224, 48, 48
      use_case: system_crash, data_loss, threshold_exceeded_by_gt_50_percent
    warning:
      hex: '#e8b830'
      rgb: 232, 184, 48
      use_case: approaching_threshold, degraded_performance, stale_data_gt_5min
    info:
      hex: '#4a90d9'
      rgb: 74, 144, 217
      use_case: normal_state, informational_update, completed_task
  chart_axis_configuration:
    x_axis:
      labels_enabled: true
      label_font_size: 11px
      label_color: hsl(0, 0%, 60%)
      grid_lines: true
      grid_line_style: 1px_dashed_hsl_0_0_20
      tick_marks: true
      tick_length: 4px
      tick_color: hsl(0, 0%, 40%)
    y_axis:
      labels_enabled: true
      label_font_size: 11px
      label_color: hsl(0, 0%, 60%)
      grid_lines: true
      grid_line_style: 1px_dashed_hsl_0_0_20
      tick_marks: true
      tick_length: 4px
      tick_color: hsl(0, 0%, 40%)
      zero_line: true
      zero_line_style: 1px_solid_hsl_0_0_40
  responsive_breakpoints:
    desktop:
      min_width: 1025px
      behavior: full_12_column_grid, all_panels_visible, side_nav_expanded
    tablet:
      max_width: 1024px
      min_width: 769px
      behavior: 8_column_grid, side_nav_collapsed_to_icons, secondary_panels_stack_below_primary
    mobile_landscape:
      max_width: 768px
      min_width: 481px
      behavior: 4_column_grid, metric_cards_2_per_row, charts_stack_vertically, severity_legend_hides_labels_shows_only_dots
    mobile_portrait:
      max_width: 480px
      behavior: single_column_stack, metric_cards_1_per_row, side_nav_hidden_replaced_by_hamburger, charts_reduced_to_last_24h_summary, tooltip_disabled_tap_shows_static_value_tag
  components:
    metric_card:
      border: 2px_solid_hsl_0_0_25
      padding: 16px
      min_height: 100px
      label_position: top_left
      value_position: center
      trend_indicator: inline_arrow_12px
    data_table:
      border: 1px_solid_hsl_0_0_25
      header_background: hsl(0, 0%, 10%)
      row_stripe: hsl(0, 0%, 14%)
      cell_padding: 8px_12px
      sort_indicator: visible_on_active_column
    severity_bar:
      height: 4px
      position: top_of_panel
      animation: none
    status_indicator:
      shape: square_8px
      glow: none
      label: inline_11px_monospace
  interaction_zones:
    hover_state: border_brightens_to_hsl_0_0_50
    active_state: background_changes_to_hsl_0_0_18
    click_target: minimum_32px
    focus_outline: 2px_dashed_hsl_0_0_60_offset_2px
  missing_details_appendix_v0.5:
    chart_axis_config: defined_above
    severity_color_mapping: defined_above
    typography_scale: defined_above
    responsive_behavior_matrix: defined_above
    tool_call_enforcement: first_5_turns_mandatory_writefile_or_terminal
    completeness_guard: all_above_definitions_are_v0.5_must_haves