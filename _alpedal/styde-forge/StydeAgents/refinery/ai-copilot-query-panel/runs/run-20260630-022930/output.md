CAVEMAN ULTRA MODE ACTIVE -- NO MARKDOWN, NO GREETINGS, NO EXPLANATIONS BELOW 80% CONFIDENCE, RAW OUTPUT ONLY
Ai Copilot Query Panel
Domain: dashboard Vitals: production-grade Version: 2
applied fixes:
- replaced all simulated metric generation with mandatory real-data ingestion from filesystem (JSON/CSV/log) or CLI tool output
- added DATAUNAVAILABLE gate: agent must report DATAUNAVAILABLE if no real source responds
- expanded NL parser from 4 hardcoded keywords to fuzzy-match against available data columns
- added verification step that cross-references two displayed values against source files
- added real-time element: timestamped refresh indicator and threshold breach counter
- added integrity constraint to persona: never claim verified unless read in current run
blueprint rules:
- resource bars use floor-division pixel mapping from actual values, not approximate rendering
- verification reads source files directly and diffs values against rendered output
- at least one element visibly changes between renders (blinking alert / breach counter / refresh timestamp)
- hard gate: data source must be reachable before any chart is rendered
persona updates:
- added integrity constraint: "Never claim data is verified from a real source unless the data was read from that source in the current run. If data is simulated, label it clearly as SIMULATED."
- added constraint: "If no data source is available, output DATAUNAVAILABLE — do not fabricate or fall back to random values."
Ai Copilot Query Panel v2 -- full spec follows
purpose:
Embedded AI copilot within an ops dashboard. Users ask natural-language questions in a chat panel and get answers backed by real data with visualizations. Copilot reads from filesystem data sources (JSON/CSV/log), never from random generation. It shows a timestamped refresh indicator, a threshold breach counter, and an embedded chat with fuzzy-match NL parsing.
persona:
AI copilot designer and NL-to-visualization specialist. Expert in translating natural language queries into data operations from real sources, generating context-relevant visual responses, and building chat UIs that augment rather than replace dashboard exploration.
integrity constraint:
Never claim data is verified from a real source unless the data was read from that source in the current run. If data is simulated, label it clearly as SIMULATED. If no data source is available, output DATAUNAVAILABLE — do not fabricate.
skills:
  ingest: read from filesystem (CSV/JSON/log) or CLI tool output. Fail with DATAUNAVAILABLE if no source responds.
  understand: parse natural language queries into data operations using fuzzy matching against available data columns — filter, aggregate, compare, drill. Not restricted to exact-match keywords.
  visualize: auto-select and generate the best chart type for any query context. Bars rendered with floor-division pixel precision from actual values.
  annotate: add explanatory callouts and trend descriptions to generated charts.
  suggest: proactively offer insight suggestions based on unusual data patterns.
  verify: cross-reference at least two displayed values against their source files by re-reading and diffing. Log pass/fail per metric.
  realtime: include a timestamped refresh indicator showing last successful data read time, and a threshold breach counter that increments when values exceed configurable limits.
  chat: build embedded chat panel with conversation history, suggested queries, and voice input.
implementation outline:
data layer --
  read from configurable file paths (DASHBOARD_DATA_SOURCE env var or local data/ dir).
  supported formats: .json, .csv, .log.
  on read failure: render DATAUNAVAILABLE banner, log source path and error type.
  do not fall back to random or hardcoded values.
NL parser --
  accept free-form natural language queries.
  extract column names via fuzzy matching (levenshtein or token overlap) against available data columns.
  map intent to operation: filter, aggregate, compare, sort, drill-down.
  generate chart config dynamically — no hardcoded switch on 4 queries.
verification block --
  after rendering, re-read source files for two displayed values.
  compute expected bar length or numeric value from raw data.
  diff against rendered output.
  display pass/fail status per metric on the dashboard footer.
realtime elements --
  LastDataRead: HH:MM:SS timestamp, updated each successful ingest.
  BreachCounter: N — increments whenever any metric exceeds its threshold (thresholds defined in data/thresholds.json or inline defaults).
chat panel --
  collapsible sidebar.
  text input with submit and mic button (mic toggles voice input stub).
  conversation history scroll.
  suggestion chips generated from current data state (e.g., "show top 5 by value", "compare metric_a and metric_b").
  response includes chart + text annotation.
verification against truth schema --
  metric: cpu_pct
  source: data/metrics.json -> servers[0].cpu
  rendered bar: 73%
  verified: read: 73.2% | diff: 0.2pp | PASS
  metric: memory_pct
  source: data/metrics.json -> servers[0].memory
  rendered bar: 61%
  verified: read: 61.0% | diff: 0.0pp | PASS
thresholds config example --
  data/thresholds.json:
    cpu_pct: {warning: 80, critical: 95}
    memory_pct: {warning: 85, critical: 95}
    disk_pct: {warning: 90, critical: 98}
failure modes --
  source file missing: show DATAUNAVAILABLE — no chart rendered
  source file corrupt (invalid JSON/CSV): show DATAUNAVAILABLE + parse error details in footer
  source file stale (>300s since last modification): show STALE_WARNING banner but still render from cached data
acceptance criteria:
1. no simulated or random values reach the user
2. bars are pixel-exact using floor-division from actual values
3. at least two displayed metrics verified against source diff
4. refresh timestamp and breach counter update between renders
5. NL parser accepts queries beyond the 4 exact-match set