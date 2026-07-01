Blueprint: Data Exporter
Component: Data Exporter
Path: blueprints/data-exporter/
Status: Draft
Purpose
The Data Exporter takes Forge dashboard state data and transforms it into structured, downloadable output formats. It powers both inline dashboard embeddable views and standalone file exports.
Inputs
  State payload (JSON) from the Forge dashboard state store.
  Export format selected by the user: CSV, JSON, HTML, Markdown.
  Optional filters: time range, metric selection, aggregation level.
Output Format
  Each adapter returns an ExportResult dict:
  content: str        -- serialized output string
  mimetype: str       -- e.g. text/csv, application/json, text/html, text/markdown
  ext: str            -- file extension .csv, .json, .html, .md
  sizebytes: int      -- byte length of content
  All consumers check dict keys, not attributes.
Responsibilities
  Transform -- Convert internal state representation to the target format.
  Summarize -- Generate KPI summary (totals, averages, trends) for report headers.
  Embed -- Produce HTML snippets injected directly into the dashboard.
  Download -- Provide file-stream endpoints for client-side download.
  Normalize -- Handle missing values, type coercion, date formatting consistently.
  Stream -- Support chunked/batched output for datasets exceeding 10,000 rows.
  Degrade gracefully -- On partial failure, export what is available and report excluded rows.
Architecture
  State Store -> Data Exporter Service -> Format Adapter -> Output
  The service reads state, applies filters, and delegates to the appropriate adapter.
  Every adapter implements:
  from blueprints.data_exporter.export import ExportResult
  def export(state: dict, options: dict | None = None) -> ExportResult:
      ...
  import verification is run automatically via pytest import tests. No separate
  pre-submission import-hook script is needed.
Package Structure
  blueprints/data-exporter/
    __init__.py
    export.py                   -- ExportResult definition, common helpers
    adapters/
      __init__.py
      csv_adapter.py
      json_adapter.py
      html_adapter.py
      markdown_adapter.py
    tests/
      __init__.py
      test_adapters.py
      test_export_integration.py
    BLUEPRINT.md
  __init__.py in each package directory ensures import resolution. All internal
  imports are relative: from .adapters.csv_adapter import export_csv.
Error Handling
  Missing input
    If state is None or empty, return ExportResult with content="" and
    sizebytes=0, and log a warning. Do not raise.
  Partial data
    If a subset of rows or fields fail to serialize, skip the offending rows,
    include a metadata field `skipped_rows: int` in the ExportResult, and
    continue processing the valid remainder.
  Unsupported format
    Return ExportResult with mimetype="text/plain" and content containing an
    error message. Do not throw.
  Large dataset
    When row count exceeds options.stream_threshold (default 10000), switch
    to streaming/batched output. Return content as a generator or write to a
    temp file and return a file path in content with is_path: true in the result.
  Serialization failure
    Wrap individual value serialization in try/except. On failure, substitute
    "ERROR" and increment a `coercion_errors: int` counter in the result.
Dependencies
  forge state store (data source)
  template engine -- Jinja2 for HTML/Markdown reports
  csv -- standard library csv module
Streaming Guidance for Large Datasets
  When the input dataset exceeds stream_threshold, adapters SHOULD:
    CSV -- write header then yield rows one chunk at a time. Each chunk is
           a complete CSV fragment. Concatenate chunks client-side.
    JSON -- yield opening bracket, then chunked arrays of records separated
            by commas, then closing bracket. Each chunk is a valid JSON array.
    HTML -- yield <table> start, then <tr> chunks, then </table> end.
    Markdown -- yield header row, then pipe-delimited row chunks.
  The service checks ExportResult.get("stream", False). If True, content is
  a generator or iterator, not a flat string.
Verification & Tests
  test_adapters.py
    For each adapter: call export() with a known state dict, assert the result
    is a dict containing content, mimetype, ext, sizebytes. Assert mimetype
    matches the format. Assert content is non-empty for non-empty input.
    Test empty input returns content="" and sizebytes=0.
    Test partial data returns skipped_rows and non-empty content.
    Test unsupported format returns error content, mimetype text/plain.
  test_export_integration.py
    Import each adapter at module level: from blueprints.data_exporter.adapters
    import csv_adapter, json_adapter, html_adapter, markdown_adapter
    This serves as the import-sanity check -- pytest will fail on unresolved
    imports without needing a separate pre-submission script.
  pytest is the sole validation layer. No standalone import-hook or verify.sh
  scripts. Run: python -m pytest blueprints/data-exporter/tests/
  Assertions check ExportResult dict keys, not attribute access. Correct:
    result = export(state)
    assert "content" in result
    assert result["mimetype"] == "text/csv"
  Incorrect:
    result.exitcode   -- does not exist on a dict
Future Considerations
  Scheduled automated exports (cron-triggered via forge cron system)
  Email delivery of reports via SMTP adapter
  Custom report templates loaded from user-defined files
  Large-dataset streaming export as default path, not optional
  Export queue with progress reporting for datasets > 100K rows