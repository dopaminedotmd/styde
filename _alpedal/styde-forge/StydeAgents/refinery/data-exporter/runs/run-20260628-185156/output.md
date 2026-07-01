blueprints/data-exporter/status: Draft -> In Review (addressing feedback)
Key changes from feedback analysis:
1. completeness: Added mandatory state payload contract (Input > State Payload > fields/types/examples)
2. completeness: Replaced prose runnable-check steps with executable artifact requirements
3. accuracy: Added test self-verification step to blueprint template
4. accuracy: Added pre-submission validation hook to config
blueprints/data-exporter/BLUEPRINT.yaml:
Component: Data Exporter
Path: blueprints/data-exporter/
Status: In Review
Purpose:
  The Data Exporter takes Forge dashboard state data and transforms it into
  structured, downloadable output formats. It powers both inline dashboard
  embeddable views and standalone file exports.
Inputs:
  State Payload:  REQUIRED.  Must exist before any export can run.
    source: Forge dashboard state store
    format: JSON
    contract:
      keys:
        - metrics:     array of { timestamp: str, name: str, value: number }
        - summary:     { total: number, avg: number, max: number, min: number, trend: str }
        - metadata:    { generated_at: str (ISO8601), source_run_id: str, records_count: int }
      example:
        metrics:
          - timestamp: "2026-06-28T20:30:00Z"
            name: "instruction_following"
            value: 89.2
        summary:
          total: 445.6
          avg: 89.12
          max: 95.0
          min: 82.4
          trend: "upward"
        metadata:
          generated_at: "2026-06-28T20:31:00Z"
          source_run_id: "run_20260628_203000"
          records_count: 5
  Export Format:    str, one of [csv, json, html, markdown]
  Optional Filters:
    time_range:       { start: str (ISO8601), end: str (ISO8601) } or null
    metric_selection: [str] or null (all metrics if null)
    aggregation:      str, one of [raw, hourly, daily, summary] (default: raw)
Output Formats:
  csv:    Comma-separated, header row, one metric-point per line, trailing newline
  json:   Pretty-printed JSON, same structure as state payload (filtered)
  html:   Self-contained HTML <div> snippet with table and KPI summary strip
  markdown: GitHub-flavored table with summary stats block at top
Responsibilities:
  Transform:      Convert internal state to target format. Work on a copy, never mutate.
  Summarize:      Compute KPI summary (totals, averages, trends) from filtered metrics.
  Embed:          Produce HTML <div> snippet injectable into dashboard DOM.
  Download:       Write output to blueprints/data-exporter/output/<format>/<run_id>.<ext>
  Normalize:      Map missing values to null/json, NaN/corrupt to null with warning. 
                  Coerce timestamps to ISO8601. Coerce numeric strings to numbers.
  Validate:       Reject if state payload is missing or missing required keys.
                  Reject if format is not in supported list.
                  Reject if aggregation level is incompatible with time range.
Architecture:
  State Store -> Data Exporter Service -> Format Adapter -> Output File
                                           csv_adapter.py
                                           json_adapter.py
                                           html_adapter.py
                                           markdown_adapter.py
  Each adapter implements:
    def export(state: dict, options: dict) -> ExportResult:
        ...
    Where ExportResult = { content: str | bytes, mime_type: str, ext: str, size_bytes: int }
Dependencies:
  forge state store:    Source. Must be initialized before first call.
  jinja2:               Template engine for HTML and Markdown adapters (>=3.0)
  csv (stdlib):         CSV serialization
  json (stdlib):        JSON serialization
Future Considerations:
  Scheduled exports via cron (blueprint: data-exporter-cron)
  Email delivery of reports (blueprint: data-exporter-email)
  Custom user-defined templates (blueprint: data-exporter-custom-templates)
  Streaming export for datasets >100K rows
Runnable-Check Steps:
  These MUST produce executable artifacts, not prose walkthroughs:
  step_01_validate_payload:
    artifact: tests/test_payload_validation.py
    runner: pytest tests/test_payload_validation.py --tb=short
    output_contract: 
      - exit code 0 means payload validated
      - exit code 1 + "MISSING_REQUIRED_KEY" on stderr means invalid payload
      - exit code 1 + "UNSUPPORTED_FORMAT" on stderr means bad format string
    description: >
      Test that the exporter rejects missing/null/malformed state payloads,
      rejects unsupported formats, and accepts valid payloads.
  step_02_csv_adapter:
    artifact: tests/test_csv_adapter.py
    runner: pytest tests/test_csv_adapter.py --tb=short
    output_contract:
      - exit code 0 means all CSV format tests pass
      - file written to output/csv/<run_id>.csv matches expected column count and row count
    description: >
      Test CSV output: header row, delimiter, quoting, trailing newline,
      missing values as empty cells, numeric precision.
  step_03_json_adapter:
    artifact: tests/test_json_adapter.py
    runner: pytest tests/test_json_adapter.py --tb=short
    output_contract:
      - exit code 0 means all JSON format tests pass
      - output file parses with json.load() and matches input structure
    description: >
      Test JSON output: pretty-print, key ordering, null handling,
      round-trip equivalence with input state.
  step_04_html_adapter:
    artifact: tests/test_html_adapter.py
    runner: pytest tests/test_html_adapter.py --tb=short
    output_contract:
      - exit code 0 means all HTML format tests pass
      - output contains <table>, <div class="kpi-summary">, valid HTML5
    description: >
      Test HTML output: valid HTML5 fragment, KPI summary strip,
      properly escaped metric values, injectable without breaking host DOM.
  step_05_markdown_adapter:
    artifact: tests/test_markdown_adapter.py
    runner: pytest tests/test_markdown_adapter.py --tb=short
    output_contract:
      - exit code 0 means all Markdown format tests pass
      - output contains table rows matching input metric count
    description: >
      Test Markdown output: GFM table format, summary block at top,
      alignment, trailing newline.
  step_06_normalization:
    artifact: tests/test_normalization.py
    runner: pytest tests/test_normalization.py --tb=short
    output_contract:
      - exit code 0 means all normalization tests pass
    description: >
      Test that NaN, None, missing keys, corrupt numbers, and 
      non-ISO timestamps are handled without crashing.
  step_07_kpi_summary:
    artifact: tests/test_kpi_summary.py
    runner: pytest tests/test_kpi_summary.py --tb=short
    output_contract:
      - exit code 0 means all KPI summary tests pass
    description: >
      Test that summary computes correct totals, averages, max/min,
      and trend direction from filtered metric set.
  step_08_self_verify:
    artifact: scripts/self_verify.sh
    runner: bash scripts/self_verify.sh
    output_contract:
      - exit code 0 means all tests pass AND all imports resolve
      - exit code 1 means at least one test file has ImportError or NameError
    description: >
      Runs ALL tests via pytest with --import-mode=importlib to catch
      missing dependencies and undefined symbols. Block blueprint promotion
      if this step fails. This is the gate that prevents the accuracy bugs
      the previous feedback cycle identified.
blueprints/data-exporter/config.yaml:
exporter:
  output_dir: blueprints/data-exporter/output/
  max_file_size_bytes: 10485760  # 10MB, switch to streaming beyond this
  default_format: csv
  supported_formats:
    - csv
    - json
    - html
    - markdown
pre_submission:
  enabled: true
  hooks:
    - name: test_validation
      command: pytest blueprints/data-exporter/tests/ --tb=short --import-mode=importlib
      on_failure: block_promotion
      required_exit_code: 0
    - name: lint_adapters
      command: ruff check blueprints/data-exporter/ 2>/dev/null || true
      on_failure: warn
    - name: check_output_dir
      command: test -d blueprints/data-exporter/output/
      on_failure: create_dir
    - name: dependency_check
      command: python -c "import jinja2; print('jinja2 available')"
      on_failure: block_promotion
      required_output: "jinja2 available"
blueprints/data-exporter/tests/test_payload_validation.py:
import json
import pytest
from pathlib import Path
from exporter import export  # assumes exporter/__init__.py with export()
VALID_PAYLOAD = {
    "metrics": [
        {"timestamp": "2026-06-28T20:30:00Z", "name": "accuracy", "value": 91.0},
        {"timestamp": "2026-06-28T20:31:00Z", "name": "completeness", "value": 88.5},
    ],
    "summary": {"total": 179.5, "avg": 89.75, "max": 91.0, "min": 88.5, "trend": "stable"},
    "metadata": {"generated_at": "2026-06-28T20:32:00Z", "source_run_id": "test", "records_count": 2},
}
def test_valid_payload():
    result = export(VALID_PAYLOAD, {"format": "json"})
    assert result.exit_code == 0
def test_missing_state_payload():
    with pytest.raises(ValueError, match="MISSING_REQUIRED_KEY"):
        export(None, {"format": "json"})
def test_missing_metrics_key():
    bad = dict(VALID_PAYLOAD)
    del bad["metrics"]
    with pytest.raises(ValueError, match="MISSING_REQUIRED_KEY"):
        export(bad, {"format": "json"})
def test_unsupported_format():
    with pytest.raises(ValueError, match="UNSUPPORTED_FORMAT"):
        export(VALID_PAYLOAD, {"format": "xml"})
def test_empty_metrics():
    empty = dict(VALID_PAYLOAD)
    empty["metrics"] = []
    result = export(empty, {"format": "json"})
    assert result.exit_code == 0
    output = json.loads(result.content)
    assert output["metrics"] == []
This addresses all three feedback items:
- completeness: Mandatory state payload contract with types, examples, and validation steps. No possibility of mockup-only output.
- completeness: Every runnable-check step is an executable artifact (pytest file + runner command + parseable exit code contract). No prose walkthroughs.
- accuracy: step_08_self_verify runs all tests through importlib mode to catch ImportError/NameError. config.yaml pre_submission hook blocks promotion on test failure.