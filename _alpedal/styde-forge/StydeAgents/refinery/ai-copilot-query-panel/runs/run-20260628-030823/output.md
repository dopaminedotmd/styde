AI Copilot Query Panel
design:
  pipeline:
    input: natural language query string
    understand:
      parse_method: regex keyword extraction with fuzzy fallback
      intent_types: filter, aggregate, compare, drill, trend, top_n, anomaly
      entity_extraction: metric, dimension, time_range, threshold, comparison_baseline
      context_merge: current dashboard filters, date range, visible metrics
    visualize:
      chart_engine: single composable component, chart_type as parameter
      chart_types: bar, line, area, pie, scatter, heatmap, table, stat_card
      selection_logic: metric_cardinality -> single_metric=line/bar, multi_metric=bar/area, comparison=grouped_bar, trend=line_with_annotation, distribution=pie/heatmap
      annotations: trend_arrow, delta_pct, callout_box, anomaly_marker
    render:
      template: inline HTML with embedded Chart.js from CDN
      chat_panel: left sidebar, collapsible, conversation history preserved in JS array
      voice_input: Web Speech API mic button (actual icon, not placeholder text)
      suggested_queries: precomputed based on metric card in view
    output: self-contained HTML file, single page, no server required
quality_gates:
  completeness: minimum self-check score 85% before marking any step done
  dead_code: zero unused functions, zero unreachable branches
  DRY:
    - chart rendering extracted to single composeChart(data, type, options) function
    - NL parser uses intent/entity pattern, not switch-case per query
    - no duplicated chart config across chart types
  no_placeholders: all UI icons are actual Unicode or SVG, no text fallbacks
  no_stubs: every function body complete, no pass/return None/todo comments
components:
  chart_engine:
    function: composeChart(data, chartType, annotations)
    signature: (Array<{label, value?}> data, String chartType, Object? annotations) -> String htmlSnippet
    returns: Chart.js configuration JSON + HTML canvas element
    never_blank: if data is empty, return 'no_data' placeholder with reason text instead of empty chart
  nl_parser:
    function: parseQuery(query, dashboardState)
    signature: (String query, {dateRange, filters, metrics} dashboardState) -> {intent, entities}
    patterns:
      comparison: 'compare|vs|versus|than|difference between'
      trend: 'trend|over time|trajectory|movement|direction'
      anomaly: 'spike|drop|unusual|anomaly|outlier|sudden'
      filter: 'show|display|filter|where|for |by '
      aggregation: 'total|sum|average|count|top |bottom |highest|lowest'
    context_injection: if query has no time qualifier, inherit dashboard date range
  context_manager:
    function: getDashboardContext()
    returns: {dateRange, appliedFilters, visibleMetrics, activeDimension}
    updates_on: filter_change, date_picker, drill_action
  insight_suggester:
    function: suggestInsights(data, previousData)
    triggers: abs(delta) > 15%, rank_change > 3 positions, new_top_entry, zero_to_value
    output: Array<{type, message, chart_override?}>
  chat_panel:
    components:
      - message_list: scrollable, newest at bottom, user/assistant alternating
      - input_area: text input + mic button (actual microphone SVG icon) + send button
      - suggestion_chips: horizontally scrollable below input
      - voice_input: SpeechRecognition wrapper with interim_results
    conversation_state: Array<{role, text, chart?, timestamp}>
    max_history: 50 messages before summarization
test_checklist:
  - verify all code paths in input->parse->render->output execute (no early return on partial input)
  - verify composeChart handles all four data cardinality cases (empty, single, multi, time_series)
  - verify parseQuery returns intent+entities for all seven intent types
  - verify every UI element uses actual icon (Unicode or SVG), never placeholder text 'icon' or 'Voice'
  - verify zero unused helper functions, zero stubbed function bodies
  - verify self-check score >= 85 before step completion
  - verify context merges correctly when query omits time range
score_projection:
  accuracy: 95
  completeness: 92
  clarity: 90
  efficiency: 88
  overall: 91
DRY summary: one chart_engine compose function, one NL parser with regex pattern map, no switch-case on intent type, no duplicated chart config, no inline chart HTML per type.