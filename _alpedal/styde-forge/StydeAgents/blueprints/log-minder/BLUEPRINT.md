# Log-Minder — Blueprint

## Purpose
Log-minder is a Forge dashboard blueprint that continuously monitors and classifies logs from across the Forge ecosystem — server logs, agent spawn logs, and evaluation logs — to surface actionable insights, group recurring issues, and detect anomalies.

## Source Logs
| Source | Description |
|---|---|
| **Server logs** | HTTP requests, authentication events, rate limiting, internal errors |
| **Agent spawn logs** | Agent lifecycle events — create, start, stop, crash, timeout |
| **Evaluation logs** | Eval run results, pass/fail counts, model responses, scoring errors |

## Classification
Every log line is tagged with one of three severity levels:

| Level | Meaning | Example |
|---|---|---|
| `ERROR` | Something broke — requires manual attention | 500 response, spawn failure, eval timeout |
| `WARN` | Unusual but non-critical — may need investigation | High latency, retry count exceeded, deprecation notice |
| `INFO` | Routine operational event | Request completed, agent spawned, eval started |

## Capabilities

### 1. Similar-Error Grouping
Log-minder clusters log entries with identical or near-identical messages/text, collapsing noise into repeat-count groups. Each group shows:
- Consolidated message (canonical form)
- First and last occurrence timestamp
- Total occurrence count
- List of trace IDs or agent IDs involved

### 2. Anomaly Detection
Two distinct anomaly signals are raised:

- **Unusual error patterns** — a new error type not seen in the baseline window (e.g., last 24 h) appears.
- **Frequency spikes** — an existing error class fires at >3× its rolling average rate within a 5-minute bucket.

Anomalies are surfaced as `WARN` or `ERROR` meta-events in the forge dashboard.

## Forge Integration
- Registers a `dashboard_panel` that displays a real-time log summary + anomaly feed.
- Exposes a `GET /logs/classify` endpoint returning structured JSON of recent classifications.
- All logic lives under `blueprints/log-minder/` — no changes to core Forge required.

## Config
See `config.yaml` for adjustable thresholds, polling intervals, and log sources.

## Dependencies
- Python 3.11+
- Forge runtime (`styde-forge`)
- `re`, `collections.Counter`, `datetime` (stdlib)
