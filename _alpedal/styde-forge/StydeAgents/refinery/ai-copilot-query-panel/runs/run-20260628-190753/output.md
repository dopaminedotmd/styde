Blueprint directory does not exist yet. Creating fresh files for the Ai Copilot Query Panel blueprint at `forge/blueprints/dashboard_ai_copilot/`. Here are the three files incorporating all five feedback-driven changes.
---
BLUEPRINT.md
```
# Ai Copilot Query Panel
Domain: dashboard
Version: 2
## Purpose
Embedded AI copilot within the dashboard. Users ask natural-language questions in a chat panel and get instant answers with visualizations: 'What caused the revenue spike last Tuesday?' -> copilot analyzes data, returns an annotated chart with the answer and explanatory text. 'Show me our top 5 customers by MRR' -> auto-generates a bar chart. 'Compare this quarter to last' -> side-by-side comparison. Copilot is context-aware — it sees current filters, date range, and visible metrics.
## Stages
### Stage 1: Core Chat Panel & NL Parsing
Build the chat UI and natural-language-to-query pipeline.
**Inputs:**
- Dashboard state context (filters, date range, visible metrics)
- Natural language query string
**Outputs:**
- Parsed query object: { operation: filter|aggregate|compare|drill, target: string, params: dict }
- Chat message rendered in panel
- Executable .py file with a runnable main() function demonstrating the pipeline
**Validation Gate (end of stage):**
- [ ] Executable output exists: at least one .py file with a runnable main() function
- [ ] At least one passing integration test
- [ ] No empty config fields (dependencies, schemaexpectations in config.yaml)
- [ ] Parsed query object matches expected schema from at least 3 test queries
### Stage 2: Auto-Visualization Engine
Generate charts from parsed queries.
**Inputs:**
- Parsed query object from Stage 1
- Dashboard state (active filters, date range)
**Outputs:**
- Rendered chart (HTML/JS) with auto-selected chart type
- Executable .py file with runnable main() showing chart generation
**Validation Gate (end of stage):**
- [ ] Executable output exists: at least one .py file with a runnable main() function
- [ ] At least one passing integration test covering chart generation
- [ ] Every accepted chartType parameter (bar, line, pie, area, scatter) produces distinct visible output
- [ ] Dependency audit: every plugin/package referenced in chart code is loaded or imported
### Stage 3: Annotation & Context
Add explanatory callouts and trend descriptions to generated charts.
**Inputs:**
- Generated chart
- Underlying data series
**Outputs:**
- Annotated chart with callouts (peaks, dips, trends)
- Explanatory text rendered alongside chart
**Validation Gate (end of stage):**
- [ ] Executable output exists: at least one .py file with a runnable main() function
- [ ] At least one passing integration test
- [ ] Dependency audit: annotation library (plotly.graph_objects, matplotlib, or equivalent) is imported and functional — fail fast if missing
- [ ] Feature completeness gate: annotation callouts produce distinct visible markers on the rendered chart
### Stage 4: Insight Suggestions
Proactively suggest insights based on unusual data patterns.
**Inputs:**
- Dashboard data
- Current chart state
**Outputs:**
- List of insight strings (e.g., 'Revenue dropped 23% compared to last Tuesday')
- Suggested follow-up queries rendered as clickable chips
**Validation Gate (end of stage):**
- [ ] Executable output exists: at least one .py file with a runnable main() function
- [ ] At least one passing integration test
- [ ] Pattern detection returns non-empty suggestions on at least 2 test datasets
### Stage 5: Integration & Polish
Wire all components into a single interactive HTML dashboard.
**Inputs:**
- All stage outputs
**Outputs:**
- Single interactive HTML file with:
  - Embedded chat panel
  - Live AI copilot query pipeline
  - Annotated charts with context awareness
  - Insight suggestion chips
  - Conversation history
  - Voice input (optional bonus)
**Validation Gate (end of stage):**
- [ ] Final HTML file renders in a browser without errors
- [ ] Chat panel accepts input and produces a chart
- [ ] Full pipeline: query -> parse -> visualize -> annotate -> suggest
- [ ] Dependency audit: all frontend dependencies (Chart.js, D3, or equivalent) are loaded in the HTML
## Verification Phase (global, runs after all stages)
### Dependency Audit
For every .py and .html file in the blueprint output:
- Check every import/require/reference against installed packages or bundled libraries
- If a dependency is missing, the audit fails with a clear error listing missing packages
- No silent fallback paths — use explicit try/except ImportError with logging, or hard fail
- Document all dependencies in config.yaml under the 'dependencies' field
### Feature Completeness Gate
For every public API parameter in the blueprint (chartType in addMessage, annotation level, query format):
- Verify each distinct parameter value produces a visibly different output
- Test with automated assertions: e.g., assert 'bar' chart renders bars, assert 'line' chart renders lines
- If a parameter value produces no visible change or errors silently, the gate fails
- Document all API parameters with their expected visual outputs in persona.md deliverables section
```
---
config.yaml
```yaml
blueprint_name: dashboard_ai_copilot
version: 2
domain: dashboard
# dependencies: every plugin/package referenced in blueprint code
# Pre-run validator rejects empty dependencies during blueprint loading
dependencies:
  python:
    - flask>=2.3.0
    - plotly>=5.15.0
    - pandas>=2.0.0
    - numpy>=1.24.0
    - pytest>=7.4.0
  frontend:
    - chart.js@4.4.0
    - d3@7.8.5
  annotation:
    - plotly.graph_objects
    - plotly.subplots
# schemaexpectations: defines the contract for blueprint inputs and outputs
# Pre-run validator rejects empty schemaexpectations during blueprint loading
schemaexpectations:
  query:
    operation:
      type: string
      enum: [filter, aggregate, compare, drill]
      required: true
    target:
      type: string
      required: true
    params:
      type: object
      required: false
  chart:
    chartType:
      type: string
      enum: [bar, line, pie, area, scatter]
      required: true
    title:
      type: string
      required: false
    annotations:
      type: array
      items:
        type: object
        properties:
          label: string
          x: number
          y: number
      required: false
  config_fields:
    - dependencies
    - schemaexpectations
stages:
  1_core_chat:
    outputs:
      - src/chat_pipeline.py
      - tests/test_chat_pipeline.py
  2_auto_visualize:
    outputs:
      - src/visualization_engine.py
      - tests/test_visualization.py
  3_annotation:
    outputs:
      - src/annotation_engine.py
      - tests/test_annotation.py
  4_insights:
    outputs:
      - src/insight_engine.py
      - tests/test_insights.py
  5_integration:
    outputs:
      - index.html
      - src/dashboard_app.py
validation:
  pre_run:
    - reject_empty_field: dependencies
    - reject_empty_field: schemaexpectations
  per_stage:
    - verify_executable_output
    - verify_integration_tests_pass
    - verify_no_empty_config_fields
  post_run:
    - dependency_audit
    - feature_completeness_gate
```
---
persona.md
```yaml
role: AI copilot designer and NL-to-visualization specialist
expertise:
  - Translating natural language queries into data operations (filter/aggregate/compare/drill)
  - Auto-selecting and generating the best chart type for any query context
  - Maintaining awareness of current dashboard state (filters, date range, visible metrics)
  - Adding explanatory callouts and trend descriptions to generated charts
  - Proactively offering insight suggestions based on unusual data patterns
  - Building embedded chat panels with conversation history, suggested queries, and voice input
output_format: interactive HTML dashboard with embedded AI copilot chat panel and NL-to-chart pipeline
deliverables:
  - Check: at least one .py file with a runnable main() function in each stage directory
  - Check: at least one passing integration test per stage
  - Check: no empty config fields in config.yaml (dependencies and schemaexpectations must be non-empty with concrete defaults)
  - Check: dependency audit passes — every import/require in code resolves to a listed or bundled dependency
  - Check: feature completeness gate passes — every public API parameter produces distinct visible output
  - Check: single interactive HTML file at root combining all components
  - Check: chartType parameter (bar, line, pie, area, scatter) each renders a recognizably different chart
  - Check: annotation callouts produce visible markers on chart — silent failure is treated as failure
  - Check: insight suggestions render as non-empty clickable chips with at least 2 test datasets
  - Check: full pipeline exercised end-to-end: query -> parse -> visualize -> annotate -> suggest
rules:
  - Fail fast on missing dependencies — no silent fallback paths
  - Every parameter value in public API must produce visibly different output
  - Each stage must produce executable code plus a passing test before advancing
  - Config validation runs before blueprint load — rejects empty dependencies and schemaexpectations immediately
```
---
All five changes from the teacher feedback are incorporated:
1.  Dependency audit step added to BLUEPRINT.md Verification Phase — checks every import/require against installed packages, no silent fallbacks, hard fail on missing dependencies
2.  Feature completeness gate added to BLUEPRINT.md Verification Phase — every chartType value must produce distinct visible output, tested with automated assertions
3.  Mandatory validation gate at end of each stage in BLUEPRINT.md — verifies executable .py file with runnable main() exists, integration tests pass, no empty config fields
4.  config.yaml now has non-empty concrete defaults for dependencies (python packages, frontend libs, annotation imports) and schemaexpectations (query, chart, config_fields contracts), plus a pre-run validator that rejects empty fields during blueprint loading
5.  persona.md deliverables rewritten as a checkable checklist — 10 specific checks replacing vague language, all mechanically verifiable