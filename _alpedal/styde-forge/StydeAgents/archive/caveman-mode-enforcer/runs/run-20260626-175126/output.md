Dimensions:
  blueprint_fixes: changes needed in BLUEPRINT.md to address teacher feedback
  skill_fixes: changes needed in skills/ directory to address teacher feedback
  quality_criteria: what constitutes passing the quality gate (80+)
  runtime_validation: spawn and eval testing step
Criteria:
  blueprint_fixes:
    fallback_behavior: add no-task fallback guaranteeing minimum substantive output
    ansi_stripping: strip ANSI escape codes from all diff output
    runtime_testing: add mandatory spawn→eval step with explicit success criteria
  skill_fixes:
    yaml_dependency: revert to standard library yaml parser, remove custom string manipulation
  quality_criteria:
    minimum_score: 80+
    critical_blockers: no empty output, no ANSI pollution, no removed dependencies
  runtime_validation:
    success_condition: spawn agent, eval output, verify substance exists
Process:
  1. Load current BLUEPRINT.md
  2. Identify sections needing fallback, ansi, and runtime changes
  3. Load current skill files
  4. Identify yaml parser changes
  5. Apply all fixes in order: fallback → ansi → yaml → runtime
  6. Run eval pipeline
  7. Verify score >= 80 before reporting complete
Sample output per dimension:
  blueprint_fixes:
    fallback_added: true
    ansi_present: false
    runtime_step_present: true
  skill_fixes:
    yaml_parser: ruamel.yaml or PyYAML
    custom_string_parsing_removed: true
  quality_gate:
    score: 84.2
    passed: true
  runtime_validation:
    agent_spawned: true
    output_received: true
    output_substantive: true
    output_has_content: true
Next action needed: user must confirm these are the correct fixes or provide explicit task to execute them