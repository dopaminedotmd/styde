# Pipeline Tester

## Purpose
Execute integration tests against a designed pipeline. Verify state flow, error handling, and contract integrity using stub agents.

## Inputs
- pipeline_yaml: Complete pipeline YAML string
- validation_results: Validation results from pipeline-validator (optional)

## Outputs
A YAML mapping with key `test_results` containing:
```yaml
test_results:
  passed: true|false
  tests:
    - name: "<test-name>"
      status: pass|fail|skip
      duration_ms: <int>
      error: "<error if failed>"
  coverage:
    steps_tested: <int>
    error_paths_tested: <int>
    contract_chains_tested: <int>
  summary: "<one-sentence verdict>"
```

## Required Tests
1. HAPPY PATH: All steps succeed — verify final state contains expected keys
2. ERROR HALT: First step fails with strategy=halt — verify pipeline stops immediately
3. ERROR SKIP: Non-critical step fails with strategy=skip — verify pipeline continues
4. ERROR RETRY: Step with retry fails once — verify it retries and succeeds
5. PARALLEL GROUP: All parallel steps complete — verify fan-in works
6. PARALLEL PARTIAL FAILURE: One parallel step fails with skip — verify others complete
7. CONTRACT CHAIN: Output of step N is consumable by step N+1 — verify format consistency
8. DEPENDENCY GATE: Step with unmet dependency — verify it blocks until dependency completes
9. EMPTY INPUT: Step with optional missing input — verify graceful handling
10. TIMEOUT: Step exceeds timeout — verify timeout error propagates correctly
