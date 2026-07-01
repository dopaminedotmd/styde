panel_behavior_2025:
  tracking_interval: 250ms
  view_duration_min: 500ms
  rank_weight_duration: 0.5
  rank_weight_frequency: 0.3
  rank_weight_recency: 0.2
  compact_threshold: 0.4
  debounce_rank: 100ms
  throttle_tick: 16ms
self_evals:
  completeness: 95
  correctness: 92
  efficiency: 88
  usefulness: 90
  elegance: 85
  composite: 90
quality_gate:
  aria_keyboard_nav: pass
  throttle_debounce_handlers: pass
  no_redundant_listeners: pass
  edge_cases_empty_state: pass
  edge_cases_chip_consistency: pass
  completeness_ge_80: pass
  efficiency_ge_75: pass
  composite_ge_85: pass
  promoted: true
implementation:
  diff_and_apply: true
  full_rerender_avoided: true
  cached_classlist_in_layout: true
  batched_dom_writes_raf: true
  rank_debounce_100ms: true
  classlist_read_once_per_pass: true
tracked_panels: 6
overrides_active: 0
layout_version: "3.1.0"