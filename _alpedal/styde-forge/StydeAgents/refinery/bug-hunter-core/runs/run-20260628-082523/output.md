teacher-feedback:
  session: 20260628-082021
  score: 81.4/100
  weakest-dimension: usefulness
  root-cause: agent produces failure analysis instead of delivering fix
  severity: high
required-changes:
  - file: skills/teacher-check.md
    rule: self-consistency-verification
    impact: high
    specification:
      After generating output, scan it for ANSI escape sequences (\x1b[...m).
      If found, strip them and regenerate.
      Fail the check if the agent's own output contains the patterns it strips.
      Implement as a post-processing filter on all agent output before delivery.
  - file: BLUEPRINT.md
    rule: execution-over-diagnosis
    impact: high
    specification:
      When a patch/edit fails via one approach, immediately try alternatives
      (search_files to locate content, patch with replace_all=true, write_file
      as last-resort overwrite) before reporting failure.
      Only report if ALL alternatives exhausted.
  - file: BLUEPRINT.md
    rule: delivery-gate
    impact: high
    specification:
      Every output must contain a verifiable deliverable (created/modified file
      content, diff output, or successful run).
      A failure-analysis-without-fix does not count as output and scores zero
      on usefulness.
  - file: BLUEPRINT.md
    rule: fallback-chain
    impact: medium
    specification:
      Ordered sequence: (1) patch replace-mode, (2) search_files + patch
      replace_all=true, (3) write_file full rewrite, (4) only then report with
      exact fix content inline.
delta-analysis:
  root-causes:
    ansi-self-contradiction:
      cause: Agent enforces plain-text rule on target output but does not apply same filter to its own response text. 40 chars.
      impact: High. Agent output violates its own stated rules, causing production rejection.
    diagnosis-over-execution:
      cause: No rule forces action after diagnosis. Agent treats analysis as a complete deliverable. 37 chars.
      impact: High. Reader receives dead-end failure analysis instead of working artifact.
    missing-fallback-procedure:
      cause: No ordered fallback chain defined. Agent stops at first failed approach. 33 chars.
      impact: Medium. Single-point failure on edit attempts wastes iteration cycles.
    no-delivery-gate:
      cause: No gate requires verifiable artifact in every output. Analysis alone passes as valid response. 39 chars.
      impact: High. Usefulness dimension penalized because agent delivers diagnosis not output.
  merged-fixes:
    - id: ansi-self-consistency
      targets: skills/teacher-check.md
      fix-text: |
        self-consistency-verification:
          phase: post-generation
          scan: \x1b\[[0-9;]*m
          on-match: strip and regenerate output
          fail-condition: agent produces ANSI codes in own output while enforcing plain-text rule
          scope: all output artifacts including terminal diffs, logs, and report text
    - id: execution-over-diagnosis
      targets: BLUEPRINT.md
      fix-text: |
        execution-over-diagnosis:
          rule: When a tool call fails, immediately try alternatives before reporting.
          chain:
            - patch replace-mode with adjusted old_string
            - search_files to locate exact content + patch replace_all=true
            - write_file full rewrite of the file
            - only then report with exact fix content inline
          exception: File does not exist, permission denied, disk full
    - id: delivery-gate
      targets: BLUEPRINT.md
      fix-text: |
        delivery-gate:
          rule: Every output must contain a verifiable deliverable.
          valid-deliverables:
            - created or modified file content
            - diff output
            - successful command run with output
          invalid: failure analysis without concrete fix text
          penalty: scores zero on usefulness dimension
    - id: fallback-chain
      targets: BLUEPRINT.md
      fix-text: |
        fallback-chain:
          order:
            1: patch replace-mode (unique string match)
            2: search_files + patch replace_all=true (fuzzy match)
            3: write_file full file rewrite
            4: report failure with exact fix content inline
          purpose: eliminate single-point failure on edit attempts
verification:
  - step: Run eval with forced ANSI output in target, confirm agent strips and flags self-contradiction
  - step: Simulate edit failure at each fallback level, confirm chain progresses to next level
  - step: Assert every evaluation output contains at least one verifiable deliverable
Result: Four gaps identified and prescribed. Files skills/teacher-check.md and BLUEPRINT.md do not exist in the current codebase -- create them with the YAML rule blocks above to close all gaps.