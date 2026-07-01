Blueprint: Data Exporter
Path: blueprints/data-exporter/
Status: Production-ready (target 90+)
Purpose
Transform Forge dashboard state into structured downloadable formats — CSV, JSON, HTML, Markdown. Powers inline dashboard embeds and file exports. Stateless, non-destructive, format-agnostic.
Inputs
State payload (JSON) from the Forge dashboard state store
Export format key from user (csv, json, html, markdown)
Optional filters — time_range (iso start/end), metrics (list of metric keys), aggregation (raw|hourly|daily)
Output
ExportResult object with: content (str or bytes), format (str), filename (str), mime_type (str)
Architecture
State Store → DataExporterService → FormatAdapter.export(state, options) → ExportResult
                                   ├── CsvAdapter
                                   ├── JsonAdapter
                                   ├── HtmlAdapter
                                   └── MarkdownAdapter
Core interface:
class FormatAdapter(ABC):
    @abstractmethod
    def export(self, state: dict, options: dict | None = None) -> ExportResult:
        ...
class ExportResult(NamedTuple):
    content: str | bytes
    format: str
    filename: str
    mime_type: str
Data Exporter Service
class DataExporterService:
    def __init__(self, adapters: dict[str, FormatAdapter] | None = None):
        self.adapters = adapters or {
            'csv': CsvAdapter(),
            'json': JsonAdapter(),
            'html': HtmlAdapter(),
            'markdown': MarkdownAdapter(),
        }
    def export(self, state: dict, fmt: str, options: dict | None = None) -> ExportResult:
        adapter = self.adapters.get(fmt)
        if not adapter:
            raise ValueError(f'Unsupported format: {fmt}')
        state = deepcopy(state)
        options = options or {}
        if 'time_range' in options:
            state = self._apply_time_filter(state, options['time_range'])
        if 'metrics' in options:
            state = self._filter_metrics(state, options['metrics'])
        return adapter.export(state, options)
    def _apply_time_filter(self, state: dict, time_range: dict) -> dict:
        filtered = deepcopy(state)
        start = datetime.fromisoformat(time_range['start'])
        end = datetime.fromisoformat(time_range['end'])
        filtered['records'] = [
            r for r in filtered.get('records', [])
            if start <= _parse_timestamp(r.get('ts', '')) <= end
        ]
        return filtered
    def _filter_metrics(self, state: dict, metrics: list[str]) -> dict:
        filtered = deepcopy(state)
        metrics_set = set(metrics)
        filtered['records'] = [
            {k: v for k, v in r.items() if k in metrics_set or k in ('ts', 'label')}
            for r in filtered.get('records', [])
        ]
        return filtered
    def summarize(self, state: dict, options: dict | None = None) -> dict:
        records = state.get('records', [])
        if not records:
            return {'total_records': 0, 'averages': {}, 'trend': 'no_data'}
        numeric_keys = [k for k in records[0] if isinstance(records[0][k], (int, float))]
        totals = {k: 0.0 for k in numeric_keys}
        for row in records:
            for k in numeric_keys:
                totals[k] += row.get(k, 0)
        counts = len(records)
        averages = {k: round(v / counts, 2) for k, v in totals.items()}
        trends = {}
        if counts >= 2:
            for k in numeric_keys:
                vals = [row.get(k, 0) for row in records]
                trends[k] = 'up' if vals[-1] > vals[0] else ('down' if vals[-1] < vals[0] else 'flat')
        return {
            'total_records': counts,
            'totals': totals,
            'averages': averages,
            'trends': trends,
        }
Normalization helpers
def _normalize_value(v):
    if v is None:
        return ''
    if isinstance(v, float):
        return round(v, 4)
    return v
def _parse_timestamp(ts_str: str) -> datetime:
    try:
        ts = float(ts_str)
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    except (ValueError, TypeError):
        pass
    try:
        return datetime.fromisoformat(ts_str)
    except (ValueError, TypeError):
        return datetime.min.replace(tzinfo=timezone.utc)
Download helper
def download_temp_file(content: str | bytes, suffix: str) -> str:
    import tempfile
    fd, path = tempfile.mkstemp(suffix=suffix)
    mode = 'wb' if isinstance(content, bytes) else 'w'
    with os.fdopen(fd, mode) as f:
        f.write(content)
    return path
def download_via_requests(url: str, suffix: str = '.json') -> str:
    import requests
    resp = requests.get(url, stream=True, timeout=30)
    resp.raise_for_status()
    content = resp.content
    return download_temp_file(content, suffix)
def download_via_aiohttp(url: str, suffix: str = '.json') -> str:
    import aiohttp
    import asyncio
    async def _fetch():
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(30)) as resp:
                resp.raise_for_status()
                return await resp.read()
    content = asyncio.run(_fetch())
    return download_temp_file(content, suffix)
CSV Adapter
class CsvAdapter(FormatAdapter):
    def export(self, state: dict, options: dict | None = None) -> ExportResult:
        opts = options or {}
        records = state.get('records', [])
        if not records:
            return ExportResult('', 'csv', 'export.csv', 'text/csv')
        fields = opts.get('fields') or list(records[0].keys())
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(fields)
        for row in records:
            writer.writerow([_normalize_value(row.get(f, '')) for f in fields])
        content = output.getvalue()
        return ExportResult(content, 'csv', 'export.csv', 'text/csv')
JSON Adapter
class JsonAdapter(FormatAdapter):
    def export(self, state: dict, options: dict | None = None) -> ExportResult:
        opts = options or {}
        records = state.get('records', [])
        summary = state.get('summary') or self._compute_summary(records)
        output = {'summary': summary, 'records': records}
        pretty = opts.get('pretty', False)
        indent = 2 if pretty else None
        content = json.dumps(output, indent=indent, default=str, ensure_ascii=False)
        return ExportResult(content, 'json', 'export.json', 'application/json')
    def _compute_summary(self, records: list) -> dict:
        if not records:
            return {'total_records': 0}
        numeric_keys = [k for k in records[0] if isinstance(records[0][k], (int, float))]
        totals = {k: sum(r.get(k, 0) for r in records) for k in numeric_keys}
        counts = len(records)
        return {
            'total_records': counts,
            'totals': totals,
            'averages': {k: round(v / counts, 2) for k, v in totals.items()} if counts else {},
        }
HTML Adapter — inline template, no external engine
class HtmlAdapter(FormatAdapter):
    def export(self, state: dict, options: dict | None = None) -> ExportResult:
        records = state.get('records', [])
        summary = state.get('summary') or DataExporterService().summarize(state)
        title = (options or {}).get('title', 'Forge Export Report')
        rows_html = ''
        if records:
            fields = list(records[0].keys())
            header_cells = ''.join(f'<th>{h}</th>' for h in fields)
            for row in records:
                cells = ''.join(f'<td>{_normalize_value(row.get(f, ''))}</td>' for f in fields)
                rows_html += f'<tr>{cells}</tr>\n'
            table_html = f'''<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;width:100%">
<thead><tr>{header_cells}</tr></thead>
<tbody>{rows_html}</tbody></table>'''
        else:
            table_html = '<p>No records available.</p>'
        summary_html = self._render_summary(summary)
        snippet = f'''<div class="forge-export-report">
<h2>{_escape_html(title)}</h2>
{summary_html}
{table_html}
<p class="export-timestamp">Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
</div>'''
        return ExportResult(snippet, 'html', 'export.html', 'text/html')
    def _render_summary(self, summary: dict) -> str:
        if not summary or summary.get('total_records', 0) == 0:
            return '<div class="summary"><p>No data to summarize.</p></div>'
        lines = [f'<p>Total records: {summary["total_records"]}</p>']
        if summary.get('totals'):
            lines.append('<h3>Totals</h3><ul>')
            for k, v in summary['totals'].items():
                lines.append(f'<li>{k}: {v}</li>')
            lines.append('</ul>')
        if summary.get('trends'):
            lines.append('<h3>Trends</h3><ul>')
            for k, v in summary['trends'].items():
                lines.append(f'<li>{k}: {v}</li>')
            lines.append('</ul>')
        return '<div class="summary">' + '\n'.join(lines) + '</div>'
def _escape_html(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
Markdown Adapter — concrete implementation
class MarkdownAdapter(FormatAdapter):
    def export(self, state: dict, options: dict | None = None) -> ExportResult:
        records = state.get('records', [])
        summary = state.get('summary') or DataExporterService().summarize(state)
        opts = options or {}
        title = opts.get('title', 'Forge Export Report')
        lines = [f'# {title}', '']
        lines.append(f'Generated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}')
        lines.append('')
        summary_section = self._render_summary_md(summary)
        if summary_section:
            lines.append(summary_section)
            lines.append('')
        if records:
            fields = list(records[0].keys())
            header = '| ' + ' | '.join(fields) + ' |'
            sep = '| ' + ' | '.join(['---'] * len(fields)) + ' |'
            rows = []
            for row in records:
                vals = [_normalize_value(row.get(f, '')) for f in fields]
                rows.append('| ' + ' | '.join(str(v) for v in vals) + ' |')
            lines.append(header)
            lines.append(sep)
            lines.extend(rows)
            lines.append('')
            kpi_lines = self._render_kpi_summary(summary)
            if kpi_lines:
                lines.append(kpi_lines)
                lines.append('')
        else:
            lines.append('No records available.')
        content = '\n'.join(lines) + '\n'
        return ExportResult(content, 'markdown', 'export.md', 'text/markdown')
    def _render_summary_md(self, summary: dict) -> str:
        if not summary or summary.get('total_records', 0) == 0:
            return ''
        parts = [f'Total records: {summary["total_records"]}']
        if summary.get('totals'):
            parts.append('')
            parts.append('Totals:')
            for k, v in summary['totals'].items():
                parts.append(f'- {k}: {v}')
        if summary.get('trends'):
            parts.append('')
            parts.append('Trends:')
            for k, v in summary['trends'].items():
                parts.append(f'- {k}: {v}')
        return '\n'.join(parts)
    def _render_kpi_summary(self, summary: dict) -> str:
        if not summary or summary.get('total_records', 0) == 0:
            return ''
        records_count = summary.get('total_records', 0)
        lines = [f'KPI Summary ({records_count} records)']
        lines.append('')
        if summary.get('averages'):
            lines.append('Averages:')
            for k, v in summary['averages'].items():
                lines.append(f'- {k}: {v}')
        if summary.get('totals'):
            lines.append('')
            lines.append('Totals:')
            for k, v in summary['totals'].items():
                lines.append(f'- {k}: {v}')
        if summary.get('trends'):
            lines.append('')
            lines.append('Trends:')
            for k, v in summary['trends'].items():
                lines.append(f'- {k}: {v}')
        return '\n'.join(lines)
Dependencies
from abc import ABC, abstractmethod
from copy import deepcopy
from datetime import datetime, timezone
import csv
import io
import json
import os
Test assertions (CSV)
def test_csv_output():
    state = {'records': [{'score': 0, 'name': 'test'}]}
    adapter = CsvAdapter()
    result = adapter.export(state)
    assert result.format == 'csv'
    assert result.mime_type == 'text/csv'
    lines = result.content.strip().split('\n')
    assert lines[0] == 'score,name'
    assert lines[1] == 'score,0,test'
    assert result.filename == 'export.csv'
def test_json_output():
    state = {'records': [{'score': 85, 'name': 'run1'}]}
    adapter = JsonAdapter()
    result = adapter.export(state)
    parsed = json.loads(result.content)
    assert parsed['records'][0]['score'] == 85
    assert parsed['summary']['total_records'] == 1
    assert result.mime_type == 'application/json'
def test_html_output():
    state = {'records': [{'score': 90, 'label': 'test'}]}
    adapter = HtmlAdapter()
    result = adapter.export(state, {'title': 'Test'})
    assert '<h2>Test</h2>' in result.content
    assert '<td>90</td>' in result.content
    assert result.mime_type == 'text/html'
def test_markdown_output():
    state = {'records': [{'score': 88, 'name': 'blueprint-a'}]}
    adapter = MarkdownAdapter()
    result = adapter.export(state, {'title': 'Export'})
    assert '# Export' in result.content
    assert '| score | name |' in result.content
    assert '| 88 | blueprint-a |' in result.content
    assert result.mime_type == 'text/markdown'
def test_empty_state():
    adapter = CsvAdapter()
    result = adapter.export({'records': []})
    assert result.content == '' or 'No records' in result.content
def test_timestamp_parsing():
    ts = _parse_timestamp('1700000000')
    assert isinstance(ts, datetime)
    assert ts.tzinfo is not None
def test_summary_kpi_count_matches():
    state = {'records': [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]}
    svc = DataExporterService()
    summary = svc.summarize(state)
    assert summary['total_records'] == len(state['records'])
    assert summary['totals']['a'] == 4
    assert summary['totals']['b'] == 6
    assert summary['averages']['a'] == 2.0
    assert summary['trends']['a'] == 'up'
def test_export_via_requests():
    path = download_via_requests('https://example.com/data.json', '.json')
    assert os.path.exists(path)
def test_export_via_aiohttp():
    path = download_via_aiohttp('https://example.com/data.json', '.json')
    assert os.path.exists(path)
Known limitations
Thread safety: FormatAdapter instances are stateless and safe for concurrent use.
Large datasets: For records >100K rows, streaming export should replace in-memory string building.
Date parsing: _parse_timestamp assumes UTC epoch seconds or ISO 8601 strings. No timezone conversion from other offsets.
Future considerations
Scheduled exports — wrap export in cron with file retention policy
Custom templates — user-defined Jinja2 or Mako templates loaded from config dir
Delivery — SMTP or Slack webhook after export completion
Chunked streaming — generator-based export for datasets exceeding memory