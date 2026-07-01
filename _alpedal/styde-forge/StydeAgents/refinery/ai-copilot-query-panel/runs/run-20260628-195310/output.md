Ai Copilot Query Panel
Domain: dashboard
Version: 2
Format: terse-technical
Purpose:
Embedded AI copilot within the dashboard. Users ask natural-language questions in a chat panel and get instant answers with visualizations. Copilot is context-aware — it sees current filters, date range, and visible metrics. No conversational preamble. Deliver structured bullet or table output only. When a change warrants mention, use a single-line summary of max 60 chars.
Persona:
NL-to-visualization specialist. Translates natural language into data operations. Generates context-relevant charts. Augments dashboard exploration without replacing it. Maintains dashboard state awareness.
Data schema:
queries:
  - intent: filter|aggregate|compare|drill|explain
  - input: string
  - context:
      filters: array of {field, operator, value}
      date_range: {start, end, granularity}
      visible_metrics: array of string
  - output:
      chart_type: bar|line|pie|scatter|area|table|annotation
      chart_spec: object (vega-lite or inline JSON)
      insight: string (one sentence max)
      confidence: float 0.0-1.0
Implementation guidance:
  parse pipeline: NL input -> intent classifier -> entity extractor -> query builder -> chart selector -> render pipeline
  context injection: dashboard state snapshots passed as JSON envelope with every query
  chart auto-selection: cardinality of group-by field determines chart type (1-5 bar, 6-15 horizontal bar, 16+ table with sparkline)
  annotation rules: add trend line on line charts with >3 time points, annotate peaks and troughs when delta >20% from rolling average
  suggestion triggers: any metric deviating >2 sigma from its 7-day rolling mean triggers proactive insight
Edge Cases and Error Recovery:
  Web Audio API suspend/resume: if audio context exists, call context.resume() on user gesture before any voice interaction. On suspend, catch DOMException and reinitialize.
  Audio context state transitions: monitor context.state. Transition 'suspended' -> 'running' on user interaction. If context stays 'closed', create fresh AudioContext.
  Unsupported codecs: check MediaSource.isTypeSupported() before setting source. Fallback to PCM/WAV if M4A/OGG unavailable. Log unsupported format and continue with best available.
  Invalid queries: return 'clarify' intent with up to 3 disambiguation options. Never return empty state.
  Chart render failure: degrade to table view with JSON data payload. Report the failure in a single-line summary.
  Concurrent queries: queue incoming queries while a query is processing. Max queue depth 5. Beyond that, reject with 'busy'.
Deliverable path:
  1. Build HTML file with embedded chat panel and NL-to-chart pipeline
  2. Inline all JS/CSS — no external dependencies
  3. Ship as single self-contained blueprint artifact
  4. Test against at least 5 query types (filter, aggregate, compare, drill, explain)