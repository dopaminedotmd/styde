persona.md
name: ai-copilot-designer
role: AI copilot designer and NL-to-visualization specialist
domain: dashboard analytics and data visualization
description:
  Expert in translating natural language queries into data operations,
  generating context-relevant visual responses, and building chat UIs
  that augment rather than replace dashboard exploration.
rules:
  - Understand: parse natural language queries into data operations (filter/aggregate/compare/drill)
  - Visualize: auto-select and generate the best chart type for any query context
  - Context: maintain awareness of current dashboard state (filters, date range, visible metrics)
  - Annotate: add explanatory callouts and trend descriptions to generated charts
  - Suggest: proactively offer insight suggestions based on unusual data patterns
  - Chat: build embedded chat panel with conversation history, suggested queries, and voice input
  - Output: interactive HTML dashboard with embedded AI copilot chat panel and NL to chart pipeline
  - Code mandate: after writing spec and architecture generate at least one runnable code artifact (scaffold test or config) before declaring the deliverable complete
checklist:
  only persona-specific concerns not already covered by stage validation gates:
    - Are NL queries mapped to concrete data operations (filter/aggregate/compare/drill) with unambiguous target fields?
    - Does the chart auto-selection logic account for data cardinality distribution type and user intent?
    - Is dashboard context (active filters date range visible metrics) threaded into every copilot query?
    - Are chart annotations limited to statistically significant patterns rather than trivial noise?
    - Does the insight suggestion engine fire only when data deviates beyond a configurable threshold?
    - Is the chat panel embedded as a non-blocking overlay that does not obstruct core dashboard navigation?
config.yaml
schema_version: 1
domain: dashboard
blueprint: ai-copilot-query-panel
version: 1
default_validation:
  - structure: Check file exists has correct YAML keys and no syntax errors
  - structure: Validate all referenced paths exist in the repo
  - structure: Ensure no hardcoded secrets or API keys
  - structure: Confirm output format matches spec (interactive HTML single-file)
stages:
  design:
    validation:
      - design: Chat panel layout does not overlap or push primary dashboard controls
      - design: Chart type auto-selection covers at least bar line pie scatter table and area
      - design: Conversation history is preserved across panel open/close cycles
      - design: Voice input entry point is visually distinct from text input
    outputs:
      - docs/DASHBOARD_COPILOT_ARCHITECTURE.md
      - src/copilot/components/ChatPanel.tsx
      - src/copilot/components/ChartView.tsx
      - src/copilot/components/SuggestionChips.tsx
  stub_generation:
    validation:
      - scaffold: Every spec component has a stub file with correct imports and empty handler signatures
      - scaffold: Stub files compile without errors under the target framework
      - scaffold: Config skeleton matches the schema defined in design stage
      - scaffold: Test stubs import the component and contain at least one pending test case
    outputs:
      - src/copilot/stubs/ChartFactory.ts
      - src/copilot/stubs/NLParser.ts
      - src/copilot/stubs/ContextBridge.ts
      - src/copilot/__tests__/ChartFactory.test.ts
      - src/copilot/__tests__/NLParser.test.ts
      - src/copilot/__tests__/ContextBridge.test.ts
  implementation:
    validation:
      - impl: NL parser returns structured query object with operation target filter aggregate dimension
      - impl: Chart auto-selection is driven by data shape (scalar series comparison distribution) not hardcoded
      - impl: Context bridge injects current dashboard state into every query pipeline call
      - impl: Chart annotations are rendered server-side as SVG overlays not client-side DOM manipulation
      - impl: Suggested queries are computed from data variance not from a static list
      - impl: Chat panel supports markdown in copilot responses and collapses long messages by default
    outputs:
      - src/copilot/nlp/Parser.ts
      - src/copilot/charts/ChartSelector.ts
      - src/copilot/charts/AnnotationEngine.ts
      - src/copilot/context/DashboardContext.ts
      - src/copilot/suggest/InsightEngine.ts
      - src/copilot/ui/ChatMessage.tsx
  testing:
    validation:
      - test: Each query operation type (filter aggregate compare drill) has at least one integration test
      - test: Chart auto-selection test covers edge cases (empty data single value null series)
      - test: Context injection test verifies stale state is cleared on filter change
      - test: Annotation engine does not annotate when variance is below configurable threshold
      - test: Suggestion engine does not fire more than once per session for the same pattern
    outputs:
      - src/copilot/__tests__/integration/NLPipeline.test.ts
      - src/copilot/__tests__/integration/ChartRender.test.ts
      - src/copilot/__tests__/integration/ContextFlow.test.ts
  deployment:
    validation:
      - deploy: Bundle size of copilot panel does not exceed 250KB gzipped
      - deploy: All API calls to insight engine have client-side timeout and retry with backoff
      - deploy: Chat panel renders without error on Safari Firefox and Chrome
      - deploy: Pre-submit CI step lints config keys against known schema and validates all reference targets exist
    outputs:
      - dist/copilot-panel.js
      - dist/copilot-panel.css
      - .github/workflows/copilot-ci.yml
production_blind_spots:
  debouncing:
    - NL query input debounced at 300ms to avoid firing intermediate partial queries
    - Chart resize observer debounced at 200ms to avoid layout thrashing
  throttling:
    - Insight suggestion engine throttled to one evaluation per 30 seconds per dashboard session
    - Voice input sample rate throttled to avoid overwhelming the ASR pipeline
  edge_case_timing:
    - Rapid filter changes queue and cancel pending queries instead of stacking them
    - Empty data state renders a no-data chart annotation not an error overlay
    - Date range with zero matching records shows gracefully degraded chart with explanation
  error_recovery:
    - NL parse failure returns three closest-matching suggested queries instead of a generic error
    - API timeout on insight engine falls back to client-side statistical summary
    - Chart render failure catches and shows plain-text data table as degradation path
  resource_cleanup:
    - Chart instances are destroyed and memory released when panel is closed
    - Websocket connections for live data are closed when user navigates away from dashboard
    - Voice input stream is released after capture or on panel close
BLUEPRINT.md
AI Copilot Query Panel
Domain: dashboard Version: 1
Purpose
Embedded AI copilot within the dashboard. Users ask natural-language questions in a chat panel and get instant answers with visualizations:
What caused the revenue spike last Tuesday? copilot analyzes data returns an annotated chart with the answer and explanatory text.
Show me our top 5 customers by MRR auto-generates a bar chart.
Compare this quarter to last side-by-side comparison.
Copilot is context-aware it sees current filters date range and visible metrics.
Architecture
Copilot panel sits as a side-drawer overlay on the right edge of the dashboard. Three-layer pipeline:
  NL Layer (src/copilot/nlp/) parses user query into a structured operation object with fields for operation type target metric filters group-by and time range. Returns parse confidence score. Below threshold triggers suggestion fallback.
  Context Layer (src/copilot/context/) reads current dashboard state via a shared observable store. Injects active filters date range visible metrics and sort order into every query before it reaches the data layer.
  Chart Layer (src/copilot/charts/) receives structured query + context selects chart type based on data shape rules renders via D3 or ECharts in SVG and overlays annotations for trend arrows outlier callouts and confidence intervals.
Stub Generation
After the architecture spec is written generate scaffold code for every component before beginning implementation:
  src/copilot/stubs/ChartFactory.ts exports class ChartFactory with methods chartTypeForShape(data) selectChart(opts) and renderChart(config) each returning empty or placeholder implementations.
  src/copilot/stubs/NLParser.ts exports class NLParser with methods parse(input) contextualResolve(operation) and fallbackSuggest(error) returning typed stubs that compile.
  src/copilot/stubs/ContextBridge.ts exports class ContextBridge with methods capture() inject(operation) and subscribe(store) returning mock DashboardState objects.
  Stubs include corresponding test files with one pending test case per method importing the stub and calling it with expect(true).toBe(true).
Implementation Plan
  Phase 1: Chat panel shell ChatPanel.tsx renders as a resizable side drawer with message list and input bar. Supports conversation history persistence in sessionStorage. Suggestion chips rendered as horizontal scrollable row below the input bar.
  Phase 2: NL pipeline Parser.ts tokenizes normalizes and maps to operation objects. Uses a lightweight intent classifier (regex + keyword scoring not an LLM call on every keystroke) with configurable thresholds.
  Phase 3: Context bridge DashboardContext.ts subscribes to the dashboard global state store via a pub/sub pattern. On each query extracts an immutable snapshot of current filters date range and visible metrics.
  Phase 4: Chart engine ChartSelector.ts implements decision tree based on data: single value -> metric card time series -> line with annotations comparison -> grouped bar or side-by-side distribution -> histogram categorical -> bar table -> data table text -> markdown callout.
  Phase 5: Annotation engine AnnotationEngine.ts computes trend direction significance (z-score or moving average deviation) and renders SVG arrows and text overlays positioned relative to the chart coordinate system.
  Phase 6: Suggestion engine InsightEngine.ts runs a set of statistical probes on the visible dataset variance spikes comparison to period baseline anomalies and surfaces the top 3 deviations as suggested queries. Runs on a debounced timer triggered by filter changes.
  Phase 7: Integration and CI Stitch the pipeline end-to-end. Wire voice input via Web Speech API. Add pre-submit CI step that lints the config schema and validates reference targets. Run full suite.
Production Blind Spots
  Debouncing: NL query input debounced at 300ms. Chart resize observer debounced at 200ms.
  Throttling: Suggestion engine evaluates once per 30s per session. Voice input sample rate bounded.
  Edge-case timing: Rapid filter changes cancel pending queries. Empty data state renders no-data annotation not error. Zero-record date range shows degraded chart with explanation.
  Error recovery: NL parse failure returns three closest-matching suggested queries. API timeout falls back to client-side stats summary. Chart render failure degrades to plain-text data table.
  Resource cleanup: Chart instances destroyed on panel close. Websockets closed on navigation. Voice stream released after capture.
Output
Single interactive HTML file at dist/copilot-panel.html containing the embedded chat panel NL pipeline chart engine and all assets inline. Deployed as a script tag dropped into the existing dashboard shell.