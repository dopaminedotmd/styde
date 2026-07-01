State loaded. Export format not specified. Defaulting to JSON.
data-exporter/status:
  component: Data Exporter
  status: draft
  format: JSON
  output:
adapters:
  - csv: ready
  - json: ready
  - html: ready
  - markdown: ready
missing:
  - input state payload (required)
  - export format selection (default: json)
  - filters: none
action required:
  Provide state payload to produce output.