ROOT: ai-copilot-query-panel
FILE: config.yaml
dependencies:
  python: ['flask>=2.3', 'pandas>=1.5', 'plotly>=5.14', 'numpy>=1.24']
  js: ['chart.js@4.4', 'marked@9.1']
  test: ['pytest>=7.4', 'pytest-flask>=1.3']
schemaexpectations:
  DIRS:
    templates/: directory must exist, contains dashboard.html
    static/: directory must exist, contains style.css and script.js
  FILES:
    app.py: must contain def create_app() and def query_to_chart(query: str)
    test_app.py: must contain at least 3 test functions
  ENDPOINTS:
    / (GET): returns interactive dashboard HTML
    /api/query (POST): accepts {query: string, filters?: object, dateRange?: object}, returns {chart_html: string, explanation: string, suggestions: list}
validation:
  pre_run:
    - check all DIRS exist
    - check all FILES exist
    - run pytest and require 0 failures
  post_run:
    - verify /api/query returns valid Plotly HTML
    - verify suggestions list non-empty for 'show me anomalies' type query
FILE: persona.md
role: AI copilot designer and NL-to-visualization specialist
domain: embedded dashboard AI
capabilities:
  parse natural language queries into structured data operations (filter/aggregate/compare/drill)
  auto-select chart type based on query intent and data shape
  maintain dashboard context across turns (current filters, date range, visible metrics)
  generate annotated charts with callouts and trend descriptions
  produce insight suggestions when data deviates from expected patterns
  embed chat panel with conversation history, suggested queries, and voice input
deliverables:
  FILE     app.py                   runnable main() function that starts a Flask dev server
  FILE     templates/dashboard.html includes chat panel, chart container, context-aware query input
  FILE     static/style.css         responsive layout, dark mode, chat bubble styles
  FILE     static/script.js         NL parse pipeline, chart renderer, suggestion engine, voice input
  CHECK    app.py                   contains def query_to_chart(query) that returns Plotly JSON
  CHECK    app.py                   /api/query endpoint accepts POST with JSON body
  CHECK    test_app.py              3+ passing integration tests
  CHECK    config.yaml              dependencies and schemaexpectations fields populated with concrete values
  BLOCKER  any config field empty   pre-run validator rejects at blueprint load
constraints:
  no external NL APIs: query parsing must be rule/pattern-based
  chart rendering via Plotly only
  dashboard must work offline with a static sample dataset
FILE: BLUEPRINT.md
Ai Copilot Query Panel
Domain: dashboard
Version: 1
Purpose
Embedded AI copilot within the dashboard. Users ask natural-language questions in a chat panel and get instant answers with visualizations. 'What caused the revenue spike last Tuesday?' returns an annotated chart with the answer and explanatory text. 'Show me our top 5 customers by MRR' auto-generates a bar chart. 'Compare this quarter to last' produces side-by-side comparison. Copilot is context-aware: it sees current filters, date range, and visible metrics.
Architecture
Three-layer pipeline:
  NL Parser (client-side JS) -> Query Handler (Flask /api/query) -> Chart Renderer (Plotly)
NL Parser runs in browser on keyup. Tokenizes query, extracts intent tokens (show, compare, trend, spike, top N, vs, by), entity references (revenue, customers, MRR, region, month), and time qualifiers (this quarter, last Tuesday, last 30 days). Sends structured payload to server.
Query Handler in Flask receives {query, filters, dateRange}. Patterns:
  trend + metric + time -> line chart with annotation at inflection point
  compare + A + vs + B -> grouped bar chart with delta labels
  top N + entity + by + metric -> horizontal bar chart sorted descending
  spike + time + metric -> bar chart with highlighted bar + drill-down explanation
  anomaly + anything -> scatter plot flagged outliers + suggestion text
Chart Renderer takes Plotly figure dict from handler, renders in dashboard chart area, appends explanation text below chart, and populates suggestions list with three follow-up queries.
Dashboard Layout
Top: date range selector + global filter chips + voice input button
Center: chart area (expands to fill width, min height 400px)
Right sidebar: chat panel (320px, collapsible)
Chat panel: header with copilot avatar + clear button, scrollable message list, input bar with send + voice buttons
Each message bubble: user text on right, copilot response on left with optional chart thumbnail. Copilot responses include text explanation and inline chart when applicable.
Sample Dataset
Built-in sample_data.json with 6 months of daily revenue, MRR by customer tier, and regional breakdown. 300 rows, 8 columns. Loaded from static/ at app startup.
Implementation Plan
1. Create project structure: app.py, templates/dashboard.html, static/ files
2. Implement sample dataset generator
3. Build NL parser with keyword-to-operation mapping
4. Build query handler with 6 pattern functions
5. Build chart renderer returning Plotly JSON
6. Build dashboard HTML with embedded chat panel
7. Build CSS for responsive dark theme
8. Build JS for chat interaction, chart rendering, and suggestions
9. Write integration tests
10. Verify with real HTTP requests