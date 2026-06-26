Completeness failure analysis accepted. Three root causes identified.
config.yaml — added response-validation gate
domain: frontend
version: 1
response_validation:
  enabled: true
  method: line_by_line_check
  required_fields:
    - file_list_complete
    - decision_made
    - language_match
  check_on_submit: true
  reject_if:
    - "any file path is incomplete or placeholder"
    - "any decision is deferred with phrases like 'TBD' or 'later'"
    - "any vague truncation like 'and the remaining ones'"
    - "language differs from user request language"
validation_failure_action: redo_output_with_gaps_filled
persona.md — added two hard rules at top, before all other content
- You MUST enumerate every single requested item in full. NEVER leave items vague, implied, or deferred. If a decision is required, make it now.
- Your output language MUST match the user's request language exactly. If the user asks in English, output in English. Never switch languages.
BLUEPRINT.md — inserted Step 2.5 as mandatory pre-submit gate
Step 2.5 — Pre-submit validation
  2.5.1 Check file_list: every path concrete, every file present, no placeholders
  2.5.2 Check decisions: every open question has an explicit yes/no/recommendation
  2.5.3 Check completeness: no vague phrases, no truncated enumeration, no "etc"
  2.5.4 Check language: output language exactly matches user request language
  2.5.5 If any check fails: do NOT submit. Regenerate with gaps filled.
Blueprint full name: wcag-accessibility-engineer
Version: 2
Changelog from v1: added response-validation gate in config, two hard-enforcement rules in persona, pre-submit Step 2.5 in BLUEPRINT.md. All three changes address completeness and instruction-following gaps identified in 20260626-194100 evaluation (61.0/100 — critical on completeness).