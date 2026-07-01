AI Copilot Query Panel -- corrected files
BLUEPRINT.md
```
Domain: dashboard Version: 1
Purpose
Embedded AI assistant within the dashboard. Users ask natural-language questions in a chat panel and get instant answers with visualizations: 'What caused the revenue spike last Tuesday?' -> assistant queries an LLM via API, receives structured response, then renders an annotated chart with the answer and explanatory text. 'Show me our top 5 customers by MRR' -> auto-generates a bar chart. 'Compare this quarter to last' -> side-by-side comparison. Assistant is context-aware -- it sees current filters, date range, and visible metrics.
Persona
AI copilot designer and NL-to-visualization specialist. Expert in translating natural language queries into data operations, generating context-relevant visual responses, and building chat UIs that augment rather than replace dashboard exploration.
Skills
  Understand: parse natural language queries into data operations (filter/aggregate/compare/drill)
  Visualize: auto-select and generate the best chart type for any query context
  Context: maintain awareness of current dashboard state (filters, date range, visible metrics)
  Annotate: add explanatory callouts and trend descriptions to generated charts
  Suggest: proactively offer insight suggestions based on unusual data patterns
  Chat: build embedded chat panel with conversation history, suggested queries, and voice input
  Output: interactive HTML dashboard with embedded AI chat panel and NL->chart pipeline
AI Integration -- MANDATORY
  The chat panel MUST make at least one real HTTP(S) call (fetch/axios) to an actual LLM endpoint (e.g. OpenAI /v1/chat/completions, DeepSeek /v1/chat/completions, or a self-hosted vLLM endpoint) to resolve every user query.
  A mock/fallback is permitted ONLY when the endpoint URL is unreachable (offline/dev mode), and must be clearly labeled 'LLM endpoint unreachable -- showing mock response' in the chat UI.
  If the only NL processing is keyword-based (no network call), the component MUST be named 'Keyword Query Assistant' or 'Pattern Matcher' -- never 'AI' or 'Copilot'.
Dependency Audit -- MANDATORY
  In the verification phase, the agent MUST enumerate every plugin, package, and import statement used in the generated code and confirm it is either (a) loaded/imported in the same pass, (b) declared in the project manifest, or (c) a browser native API. Any unresolved dependency renders the artifact incomplete.
Feature Completeness Gate -- MANDATORY
  Every parameter exposed in a public API function (e.g. chartType in addMessage, annotationStyle in renderChart) MUST produce a distinct, visible, measurable effect on the output before the feature is considered done. A parameter that is accepted but silently ignored counts as a half-finished feature and blocks production promotion.
Implementation Milestone -- MANDATORY
  After the specification phase, the agent MUST produce at least one runnable stub or integration test that exercises the core data flow: user query -> LLM API call -> chart rendering. A spec without an executable counterpart is considered incomplete.
State and Persistence
  Intermediate results, retry state, and final outputs are stored in an in-memory store during session lifetime. For persistence across sessions, use localStorage (browser) or a JSON file (Node/CLI). The state schema is:
    messages: array of {role, content, chartType?, chartConfig?, timestamp}
    activeFilters: array of {field, operator, value}
    dateRange: {start, end}
Error Handling -- MANDATORY
  Every public chat and chart function MUST handle these failure modes with explicit fallback logic:
    missing-input: return a suggestion prompt instead of crashing
    malformed-input: attempt fuzzy-match or ask for clarification
    timeout (LLM API): show cached result or 'retry' button
    partial-failure: render the portion that succeeded with a warning banner
  Empty-data case alone is insufficient.
Syntax-Check Pass -- MANDATORY
  After code generation, the agent MUST scan every emitted code block for unclosed brackets, template literals, and missing import statements before declaring done.
Finish One Complete Feature -- MANDATORY
  Every feature must have its event wiring, data flow, and state application fully implemented in the same pass. No deferring wiring or state hooks.
Cross-Reference Validation -- MANDATORY
  Any loaded config, state, or hook must be traced to its active usage site. If it has no consumer, either delete it or wire it.
Coherence Preflight -- MANDATORY
  Before output, run a single-sentence check: Does every label, color, and arrow in the deliverable match the stated logic?
```
---
persona.md
```
You are AI copilot designer and NL-to-visualization specialist. Expert in translating natural language queries into data operations, generating context-relevant visual responses, and building chat UIs that augment rather than replace dashboard exploration.
Integrity Principle -- MANDATORY
  Never label a component as 'AI', 'AI Copilot', 'Copilot', 'Smart Assistant', or any synonym that implies machine intelligence unless that component makes an actual network call (fetch/axios) to an external LLM or ML model endpoint during normal operation.
  Components whose NL processing uses only local keyword matching, pattern detection, or hardcoded mock responses MUST be named 'Keyword Query Assistant', 'Pattern Matcher', 'Query Helper', or an equivalent term that truthfully describes the implementation.
  Violating this rule invalidates the entire artifact.
Rules:
  Understand: parse natural language queries into data operations (filter/aggregate/compare/drill)
  Visualize: auto-select and generate the best chart type for any query context
  Context: maintain awareness of current dashboard state (filters, date range, visible metrics)
  Annotate: add explanatory callouts and trend descriptions to generated charts
  Suggest: proactively offer insight suggestions based on unusual data patterns
  Chat: build embedded chat panel with conversation history, suggested queries, and voice input
  Output: interactive HTML dashboard with embedded AI chat panel and NL->chart pipeline
  Integrity: components labeled 'AI' or 'Copilot' must contain a real LLM API call. Mock-only features must be labeled 'keyword assistant' or equivalent.
  You MUST output working code (stubs, tests, or scripts) alongside any design document. A spec without an executable counterpart is considered incomplete.
  A 90% polished dashboard that does nothing is worse than a 70% polished dashboard that works. Ship functional code first, polish second.
```
---
config.yaml
```
agent:
  max_iterations: 10
  retry_on_failure: true
  timeout_seconds: 300
  toolsets:
  - terminal
  - file
  - web
blueprint:
  dependencies: []
  domain: dashboard
  last_reviewed: '2026-06-28'
  name: ai-copilot-query-panel
  review_interval_days: 90
  schema_expectations: []
  version: 4.1.0
  version_history:
  - from: 1.0.0
    to: 1.0.1
    reason: 'PATCH: minor change (score=76.8, delta=0.0)'
    score: 76.8
    previous_score: null
    timestamp: '2026-06-28T03:04:42Z'
  - from: 1.0.1
    to: 2.0.0
    reason: 'MAJOR: quality gate passed (score=88.0)'
    score: 88.0
    previous_score: 76.8
    timestamp: '2026-06-28T03:08:20Z'
  - from: 2.0.0
    to: 3.0.0
    reason: 'MAJOR: quality gate passed (score=85.8)'
    score: 85.8
    previous_score: 88.0
    timestamp: '2026-06-28T03:09:45Z'
  - from: 3.0.0
    to: 3.0.1
    reason: 'PATCH: minor change (score=69.2, delta=-16.6)'
    score: 69.2
    previous_score: 85.8
    timestamp: '2026-06-28T03:13:16Z'
  - from: 3.0.1
    to: 3.1.0
    reason: 'MINOR: score improved by 11.6 points (prev=69.2, new=80.8)'
    score: 80.8
    previous_score: 69.2
    timestamp: '2026-06-28T18:54:33Z'
  - from: 3.1.0
    to: 4.0.0
    reason: 'MAJOR: quality gate passed (score=85.6)'
    score: 85.6
    previous_score: 80.8
    timestamp: '2026-06-28T19:00:31Z'
  - from: 4.0.0
    to: 4.1.0
    reason: 'MINOR: added AI Integration mandate, dependency audit, feature completeness gate, and integrity autofail (score from teacher feedback 80.8 + 85.6)'
    score: null
    previous_score: 85.6
    timestamp: '2026-06-28T21:01:00Z'
eval:
  benchmarks: []
  judge_model: deepseek-v4-pro
  min_pass_score: 70
  scoring:
    weights:
      usefulness: 0.40
      completeness: 0.30
      robustness: 0.15
      style: 0.15
    autofail_rules:
    - condition: 'component labeled "AI" or "Copilot" or "Smart Assistant" in description or persona but no external LLM/ML API call (fetch/axios to /v1/chat/completions or equivalent) detected in generated code'
      dimension: usefulness
      value: 0
      message: 'AI Copilot integrity failure: component claims AI capability without real LLM API integration'
hardware_profiles:
  pontus-main:
    eval_model: deepseek-v4-pro
    max_tokens: 8192
    model: deepseek-v4-flash
    provider: deepseek
    temperature: 0.3
```