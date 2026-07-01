blueprint:
  name: Data Exporter
  path: blueprints/data-exporter/
  status: Draft
  purpose: Transform Forge dashboard state into structured downloadable output formats
  inputs:
    - name: state
      type: JSON
      source: Forge dashboard state store
    - name: format
      type: string
      values: [CSV, JSON, HTML, Markdown]
    - name: filters
      type: object
      optional: true
      fields: [time_range, metric_selection, aggregation_level]
  output_formats:
    CSV: spreadsheet import raw data
    JSON: programmatic consumption API
    HTML: in-dashboard embeddable report
    Markdown: summary documentation README
  architecture:
    State_Store: data source
    Data_Exporter_Service: reads state applies filters delegates to adapter
    Format_Adapter: common interface export(state options) -> Output
    Adapters: [CSV, JSON, HTML, Markdown]
  dependencies:
    - Forge state store
    - Template engine for HTML/Markdown
    - CSV serialization library
  future:
    - Scheduled automated exports
    - Email delivery
    - Custom report templates
    - Large-dataset streaming