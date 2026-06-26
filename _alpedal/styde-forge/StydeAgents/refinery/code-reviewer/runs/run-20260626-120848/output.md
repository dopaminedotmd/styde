No code was provided to review. The task input is empty.
required_input: code_to_review
missing_fields: ["code"]
instruction_to_user: Provide the source code file(s) or code snippet to review.
partial_deliverable:
  known:
    - Reviewer persona loaded: senior developer, security-auditor style
    - Blueprint domain: coding, version 1
    - Skills available: bug detection, OWASP scanning, style compliance, performance analysis, edge case analysis
  missing:
    - code: The source code to analyze is absent from the task input
    - language: Unknown (affects skill selection)
    - file_count: Unknown
    - review_scoping_filters: None requested
  estimated_without_input:
    - review_depth: Full line-by-line, all categories (bugs, security, style, performance)
    - output_format: severity-grouped list (CRITICAL, MAJOR, MINOR) with line numbers and fix suggestions
    - coverage: 100% of provided code once supplied
  next_steps:
    - Provide the code as a string, file path, or pasted block
    - Optionally specify a language or review focus to narrow scope
No code. No review possible. Deliverable is diagnostic of missing input.