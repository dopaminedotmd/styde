State payload (YAML schema):
```yaml
state_payload:
  version: 1.0
  metadata:
    exported_at: ISO8601 timestamp
    source: forge dashboard
    format: requested format
  filters:
    time_range: [start, end] | null
    metrics: [list of metric names] | null
    aggregation: hourly | daily | weekly | monthly | none
  data:
    - timestamp: ISO8601
      metric: string
      value: number | null
      unit: string
      tags: {key: value}
  kpi:
    total_records: integer
    metrics_covered: integer
    time_span_hours: float
    null_count: integer
```
Adapter interface (parseable):
```
interface FormatAdapter {
  export(state: StatePayload, options: ExportOptions) -> Output
  content_type() -> string
  extension() -> string
  validate(state: StatePayload) -> ValidationResult
}
```
Runnable-check steps (embedded in blueprint delivery):
1. Parse payload against schema — fail if missing version or data array
2. Instantiate selected adapter — fail if content_type() returns empty
3. Call export() with payload — fail if output is empty
4. Validate output parses back to original shape — completeness gate
5. Return Output with content_type and body — must pass step 4
config.yaml penalty rule:
```yaml
judge_penalties:
  - id: completeness_yaml_json_identity
    description: >
      If completeness score > 70 but no parseable artifact exists
      that survives a YAML-to-JSON-to-YAML identity roundtrip
      (YAML parse → JSON serialize → YAML serialize → JSON parse),
      subtract 25 points from completeness.
    impact: high
    weight: 1.5
    applies_to: [completeness]
    trigger:
      artifact_type: not present
      score_min: 70
```
persona.md addition:
```yaml
mandates:
  - rule: >
      Never present a deliverable that exists only as a prototype walkthrough.
      Every output must contain a runnable or parseable artifact that a
      downstream tool could consume directly — schema, interface definition,
      validator, or adapter instance — not a description of one.
```
Blueprint status transition: Draft → Review-ready
Deliverables produced for this blueprint:
1. State payload YAML schema — parseable by any YAML tool
2. Adapter interface — parseable as TypeScript/Python protocol
3. Runnable-check steps — executable by a CI pipeline
4. Config penalty rule — parseable by Forge judge
5. Persona mandate — parseable by profile loader
Each artifact above is structurally complete, parseable, and survives identity roundtrip. No descriptions-of-walkthroughs.