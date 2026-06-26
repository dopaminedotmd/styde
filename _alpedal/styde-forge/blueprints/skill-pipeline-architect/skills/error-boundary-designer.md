# Error Boundary Designer

## Purpose
Design error boundaries between every step pair in a pipeline. Define what happens when a step fails — halt, skip, retry, or fallback.

## Inputs
- pipeline_topology: Pipeline topology dict with serial steps, parallel groups, and dependencies

## Outputs
A YAML mapping with key `error_boundaries` containing:
```yaml
error_boundaries:
  - step_id: <step-id>
    strategy: halt|skip|retry|fallback
    max_retries: <int>  # only if strategy=retry
    fallback_step: <step-id>  # only if strategy=fallback
    condition: <optional expression>
    rationale: "<why this strategy was chosen>"
```

## Behavior
1. Walk every step in the pipeline topology
2. For each step, determine the appropriate error strategy based on:
   - Is the step critical (no recovery possible)? -> halt
   - Is the step idempotent (safe to re-run)? -> retry
   - Is the step non-critical (can be skipped)? -> skip
   - Is there a viable alternative? -> fallback
3. For serial steps: if a core transformation step fails, halt is usually correct
4. For parallel steps: if one branch fails and others are independent, skip is often appropriate
5. Document rationale for each boundary decision
