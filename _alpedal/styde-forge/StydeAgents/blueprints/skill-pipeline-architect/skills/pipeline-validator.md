# Pipeline Validator

## Purpose
Run structural validation on a composed pipeline YAML. Check all references, contract chains, and dependency DAG.

## Inputs
- pipeline_yaml: Complete pipeline YAML string (the output of pipeline-composer)

## Outputs
A YAML mapping with key `validation_results` containing:
```yaml
validation_results:
  valid: true|false
  errors:
    - type: missing_skill|circular_dependency|orphaned_contract|invalid_strategy
      message: "<description>"
      step: <step-id>
  warnings:
    - "<warning text>"
  checks_passed: <int>
  checks_failed: <int>
```

## Validation Checks
1. All step IDs are unique
2. All depends_on references point to existing step IDs
3. All skill names have a corresponding .md file in skills/ or _shared/skills/
4. Dependency graph is acyclic (no circular dependencies)
5. Error strategies are one of: halt, skip, retry, fallback
6. Contract chains are connected: every output target is consumed by some step's input
7. No orphaned outputs (outputs never read) — with warning for context.* targets
8. Parallel groups have at most 5 steps
9. Timeout values are positive integers
