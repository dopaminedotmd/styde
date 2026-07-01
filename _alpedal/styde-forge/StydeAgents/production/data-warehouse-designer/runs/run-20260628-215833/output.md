action: analyze-feedback
source:
  - run-20260628-214524
  - run-20260628-214717
  - T.md:normalize-yaml-indent
composite-score: 90.3
findings:
  - dimension: efficiency
    score: low-80s
    cause: blueprint explains principles at length but lacks executable dbt/SQL examples
    fix:
      - replace execution-principles prose with 3-4 runnable dbt/SQL snippets
      - consolidate principles into compact table (principle | one-liner | where-applied)
  - dimension: completeness
    score: mid-80s
    cause: stg SQL, source YAML, dbtproject.yml contain placeholders/ellipsis; SCD macro has literal '...'
    fix:
      - add required-artifacts checklist to blueprint prompt
      - create verify-artifacts skill that greps for '...' 'TODO' 'stub' pre-submission
  - dimension: formatting
    score: 95
    cause: T.md star schema example has mixed indentation
    fix: normalize to consistent 2-space throughout
changes-proposed:
  - file: BLUEPRINT.md
    changes:
      - strip redundant execution-principles prose blocks
      - add compact table: principle | one-liner | where-applied
      - add 3-4 runnable snippets (incremental model, dbt test, custom macro, source freshness)
      - add required-artifacts checklist section
  - file: T.md
    changes:
      - normalize star-schema YAML example to consistent 2-space indent
  - file: skills/verify-artifacts/skill.md (new)
    content: pre-submission grep for '...' 'TODO' 'stub'; check each file path in spec is non-empty valid syntax
priority-order:
  1. T.md: normalize YAML indent (low impact, quick fix)
  2. BLUEPRINT.md: replace prose with executable snippets + table (high impact)
  3. BLUEPRINT.md: add required-artifacts checklist (high impact)
  4. skills/: create verify-artifacts (medium impact)