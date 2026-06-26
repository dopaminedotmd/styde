BLUEPRINT.md
purpose: Generate production-ready clay-soft dashboard design specifications.
domain: frontend-design
version: 7
persona:
  You are a clay-soft interface designer. Rounded corners everywhere, soft extrusive shadows, warm pastels, tactile depth. Interfaces you want to touch. Playful but premium.
visual_constraints:
  bar_chart_8_bars:
    odd_bars_1_3_5_7: color_A
    even_bars_2_4_6_8: color_B
    gradient_blending_adjacent_bars: forbidden
  tooltip_trigger: bar_hover_only
    forbidden_zones: [axis_labels, axis_ticks, chart_title, chart_background]
    hover_zone: bar_rectangle
    hover_zone_width_max_px: 60
dom_budget:
  max_containers_per_view: 20
  max_unique_color_transitions_per_page: 6
  hover_zone_width_cap_px: 60
  max_nested_container_depth: 4
responsive_breakpoints:
  mobile_320_767:
    grid_columns: 1
    cards: stack_vertically
    charts: full_width
    pie_chart_diameter_px: 120
  tablet_768_1023:
    grid_columns: 2
    sidebar: icon_tray
    charts_span: 2
    pie_chart_diameter_px: 160
  desktop_1024_plus:
    grid_columns: 3
    sidebar: full
    charts_span: 3
    pie_chart_diameter_px: 200
exact_specs:
  pie_chart_diameter_desktop_px: 200
  pie_chart_diameter_tablet_px: 160
  pie_chart_diameter_mobile_px: 120
  card_padding_inner_px: 24
  card_gutter_outer_px: 16
  border_radius_cards_px: 16
  border_radius_buttons_px: 12
  border_radius_inputs_px: 8
  shadow_spread: "0 8px 32px rgba(0,0,0,0.08)"
completeness_checklist:
  typography:
    - font_stack_declared: required
    - scale_chain_h1_h6_declared: required
    - line_heights_per_level: required
    - letter_spacing_tracking_values: required
    - font_weight_mappings: required
  states:
    - loading_state_spec: required
    - empty_state_spec: required
    - error_state_spec: required
    - hover_state_transition_ms: required
    - active_pressed_state: required
    - disabled_state_opacity_or_color: required
  dark_mode:
    - color_tokens_for_dark_background: required
    - surface_elevation_shadows_in_dark: required
    - text_contrast_ratio_min_AA_on_dark: required
    - card_shadow_color_dark_mode: required
  focus_indicators:
    - focus_ring_style: required
    - focus_ring_offset: required
    - focus_ring_color_light_and_dark: required
    - focus_visible_vs_focus_any_behaviour: required
  animation:
    - transition_duration_ms_for_theme_toggle: required
    - card_enter_animation: optional
    - chart_animate_on_load: optional
  accessibility:
    - color_contrast_ratio_min: "4.5:1 text, 3:1 large text"
    - touch_target_min_size_px: 44
    - aria_patterns_for_dynamic_charts: recommended
  asset_delivery:
    - color_palette_export_hex: required
    - shadow_definitions_css: required
    - border_radius_tokens: required
    - spacing_scale: required
post_generation_review:
  step_1: scan_spec_against_checklist_above
  step_2: if_any_required_item_missing_mark_as_incomplete_and_readd
  step_3: verify_all_dom_budget_rules_are_satisfied
  step_4: verify_responsive_breakpoint_specs_exist_for_all_three_tiers
  step_5: confirm_no_self_evaluation_score_claims_in_output
  step_6: run_validation_gate_before_submit
self_evaluation_claims: forbidden
  reason: Prevents inflation that undermines objectivity per 20260626-183136 feedback
  replacement: Use objective output quality criteria and verifiable success metrics only
---
config.yaml
production_threshold_score: 85
validation_gates:
  format:
    enabled: true
    rule: output_must_be_valid_markdown_with_no_raw_yaml_leakage
    threshold: pass_fail
    enforcement: hard_block_on_failure
  language:
    enabled: true
    rule: all_design_specs_must_use_english
    enforcement: hard_block_on_failure
  completeness_checklist:
    enabled: true
    rule: mandatory_fields_above_must_be_present_in_final_spec
    min_field_coverage_percent: 100
    enforcement: hard_block_on_failure
  dom_budget_compliance:
    enabled: true
    max_containers_per_view: 20
    max_color_transitions_per_page: 6
    max_hover_zone_width_px: 60
    max_nested_depth: 4
    enforcement: soft_warning_recommend_refactor
  responsive_completeness:
    enabled: true
    required_breakpoints: [mobile_320_767, tablet_768_1023, desktop_1024_plus]
    each_breakpoint_must_include:
      - grid_columns
      - pie_chart_diameter_px
      - sidebar_behaviour
    enforcement: hard_block_on_failure
  accessibility_minimum:
    enabled: true
    contrast_ratio_min_text: "4.5:1"
    contrast_ratio_min_large_text: "3:1"
    touch_target_min_px: 44
    enforcement: soft_warning
  no_self_evaluation_scores:
    enabled: true
    rule: Spec_output_must_not_contain_self_assigned_quality_scores_or_estimated_composite_ranges
    enforcement: hard_block_on_failure
    remediation: Replace_any_score_claims_with_verifiable_objective_criteria_matching_the_completeness_checklist
production_checks:
  pre_submit:
    - name: format_validation
      command: parse_spec_as_valid_markdown_no_yaml_leakage
    - name: checklist_scan
      command: scan_output_against_completeness_checklist_generate_coverage_report
    - name: score_claim_scan
      command: regex_search_for_digital_score_patterns_reject_if_found
    - name: dom_budget_scan
      command: count_containers_color_transitions_hover_widths_nested_depth
  fail_action: return_to_phase_0_5_with_violations_list
scoring:
  compliance_weight: 0.25
  accuracy_weight: 0.25
  completeness_weight: 0.25
  consistency_weight: 0.25
  min_acceptable: 85