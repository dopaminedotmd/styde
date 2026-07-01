Jag bearbetar feedbacken. Här är de två mest relevanta punkterna:
Senaste feedback (84.2, 20260628-193101, prioritet):
- Ersätt Skills-sektionen i BLUEPRINT.md med egenhändigt skrivet innehåll: datamodell, API-kontrakt, query endpoints
- Lägg till Output/Deliverable-sektion
- Ta bort refactor-pass från persona.md (finns inte, så no-op)
Tidigare feedback (lägre prioritet, inkorporeras i nya Skills):
- Avoid Redundancy quality gate
- Prefer Helper Abstractions rule
Här är uppdaterat innehåll:
---
persona.md (oförändrat -- refactor-pass finns inte, senaste feedback säger ta bort = no-op)
BLUEPRINT.md -- ersätt med nedan:
```
Ai Copilot Query Panel
Domain: dashboard
Version: 2
Purpose
Embedded AI copilot within the dashboard. Users ask natural-language questions in a chat panel and get instant answers with visualizations: 'What caused the revenue spike last Tuesday?' -> copilot analyzes data, returns an annotated chart with the answer and explanatory text. 'Show me our top 5 customers by MRR' -> auto-generates a bar chart. 'Compare this quarter to last' -> side-by-side comparison. Copilot is context-aware -- it sees current filters, date range, and visible metrics.
Persona
AI copilot designer and NL-to-visualization specialist. Expert in translating natural language queries into data operations, generating context-relevant visual responses, and building chat UIs that augment rather than replace dashboard exploration.
Data Schema
The copilot queries against a flat metrics store with the following schema:
  metric: string          # unique metric key e.g. 'revenue', 'mrr', 'active_users'
  value: number
  timestamp: ISO8601      # datetime of the data point
  dimension: string       # grouping dimension e.g. 'region', 'product_tier', 'customer_segment'
  dimension_value: string # specific value for the dimension, e.g. 'EU', 'Enterprise'
  prev_period_value: number | null  # value for the same dimension one period ago
  pct_change: number | null         # pre-calculated period-over-period change
  trend: 'up' | 'down' | 'flat'     # linear trend classification over last 7 periods
API Contracts -- the copilot generates code that calls these endpoints:
  POST /api/copilot/query
    Request: { query: string, context: { filters?: object, date_range?: [string, string], visible_metrics?: string[] } }
    Response: { intent: string, sql: string, chart_type: string, label: string, data: array, insight?: string }
  POST /api/copilot/suggest
    Request: { context: { visible_metrics: string[], date_range: [string, string] } }
    Response: { suggestions: Array<{ label: string, query: string, confidence: number }> }
  POST /api/copilot/chat
    Request: { message: string, history: Array<{ role: 'user'|'assistant', content: string }> }
    Response: { reply: string, chart?: object }
Quality Gates -- applied during code generation:
  Avoid Redundancy: extract duplicated metric update logic (e.g. value formatting, trend arrow computation, prev-period comparison) into a single shared function before the filter handler chain. No block longer than 3 lines should appear twice.
  Prefer Helper Abstractions: use a helper function for Chart.js background color generation and label formatting instead of inline string splicing in the dataset config. Example helper shape:
    function chartDataset(label, data, color, fill=false) { return { label, data, borderColor: color, backgroundColor: fill ? color + '33' : 'transparent', tension: 0.3 }; }
Output / Deliverable
  Format: single self-contained HTML file embedding all CSS and JS. No external dependencies -- Chart.js loaded from CDN with a fallback inline bundle.
  Directory Layout:
    output/
      ai-copilot-dashboard.html   # the deliverable
      assets/                      # optional: base64-inlined images bundled into the HTML
  Acceptance Criteria:
    1. Chat panel renders in the bottom-right corner of the dashboard, collapsible via toggle button
    2. Entering "Show top 5 customers by MRR" generates a sorted horizontal bar chart with exact values as labels
    3. Entering "Compare this quarter to last" generates a grouped bar chart with two series and a delta annotation
    4. Entering "What caused the revenue spike last Tuesday?" returns an annotated time-series chart with the dominant contributor highlighted and an insight text explanation
    5. All charts respond to dashboard filter changes (the chat panel reads current filters from a shared store)
    6. Suggested queries update dynamically based on visible metrics
    7. Code passes Avoid Redundancy and Prefer Helper Abstractions quality gates
```