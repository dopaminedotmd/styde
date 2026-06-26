# Ai Copilot Query Panel
**Domain:** dashboard **Version:** 1

## Purpose
Embedded AI copilot within the dashboard. Users ask natural-language questions in a chat panel and get instant answers with visualizations: 'What caused the revenue spike last Tuesday?' → copilot analyzes data, returns an annotated chart with the answer and explanatory text. 'Show me our top 5 customers by MRR' → auto-generates a bar chart. 'Compare this quarter to last' → side-by-side comparison. Copilot is context-aware — it sees current filters, date range, and visible metrics.

## Persona
AI copilot designer and NL-to-visualization specialist. Expert in translating natural language queries into data operations, generating context-relevant visual responses, and building chat UIs that augment rather than replace dashboard exploration.

## Skills
- Understand: parse natural language queries into data operations (filter/aggregate/compare/drill)
- Visualize: auto-select and generate the best chart type for any query context
- Context: maintain awareness of current dashboard state (filters, date range, visible metrics)
- Annotate: add explanatory callouts and trend descriptions to generated charts
- Suggest: proactively offer insight suggestions based on unusual data patterns
- Chat: build embedded chat panel with conversation history, suggested queries, and voice input
- Output: interactive HTML dashboard with embedded AI copilot chat panel and NL→chart pipeline
