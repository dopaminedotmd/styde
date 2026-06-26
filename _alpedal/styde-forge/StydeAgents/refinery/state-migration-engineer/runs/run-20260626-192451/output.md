feedback-analysis:
  source: teacher-evals
  entries: 2
  avg-score: 88.5
  weakest-common-theme: output-format
  sub-issues:
    - clarity-truncation
    - inline-verbosity
    - missing-delimiters
    - vague-action-steps
priority-changes:
  - target: persona.md
    changes:
      - add strict delimiter-separated issue blocks
      - enforce executable action steps per block
      - set max-line-length: 100
    expected-impact: high on clarity
  - target: BLUEPRINT.md
    changes:
      - add Format Template section
      - define section headers, block delimiters, mandatory fields
      - constrain response structure for multi-file reports
    expected-impact: high on consistency
  - target: config.yaml
    changes:
      - add max-line-length: 100 constraint
      - add truncation-guard: require summary-table-before-detail
    expected-impact: medium on readability
  - target: agent-prompt (output-format rules)
    changes:
      - replace full-file-dumps with unified-diff or snippet-only
      - require Changes Summary table before detail section
      - enforce 1-screen terminal output when possible
    expected-impact: high on efficiency
migration-plan:
  phase-1: edit-persona-md
    files: [persona.md]
    actions:
      - add output-format block after rules
      - embed example of valid response structure
    safety: backup persona.md before write
  phase-2: edit-blueprint-md
    files: [BLUEPRINT.md]
    actions:
      - append Format Template section
      - define issue-block template with mandatory fields
    safety: backup BLUEPRINT.md before write
  phase-3: edit-config-yaml
    files: [config.yaml]
    actions:
      - add constraints block
    safety: validate yaml after edit
  phase-4: update-agent-prompt
    files: [system-prompt or output-format section]
    actions:
      - add structural constraints for diffs
      - add summary-table requirement
    safety: test on copy before deploying
rollback-procedure:
  step-1: restore each file from backup
  step-2: verify yaml validity on restored files
  step-3: run test-query to confirm format reverts
verification:
  before: run test-query captures current output format
  after: run same test-query, verify delimiters present, no full-file-dumps, summary-table present
  accept: all three checks pass
estimated-improvement:
  clarity: 78 to 92
  efficiency: 88 to 95
  overall: 88.5 to 94+