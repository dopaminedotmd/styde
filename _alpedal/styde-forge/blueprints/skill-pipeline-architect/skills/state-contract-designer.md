# State Contract Designer

## Purpose
Design explicit state contracts between pipeline steps. Define data keys, formats, and validation rules for cross-step communication.

## Inputs
- pipeline_topology: Pipeline topology dict with serial steps, parallel groups, and dependencies

## Outputs
A YAML mapping with key `state_contracts` containing:
```yaml
state_contracts:
  - from: <step-id>
    to: <step-id>
    contracts:
      - key: <data-key>
        source_format: yaml|text|json
        target_format: yaml|text|json
        required: true|false
        schema:
          # optional field-level type hints
          type: string|number|list|dict
  global:
    - key: <shared-context-key>
      description: "<what this key holds>"
      produced_by: [<step-ids>]
      consumed_by: [<step-ids>]
```

## Behavior
1. For each edge in the pipeline topology (from -> to), produce a contract
2. Each contract specifies:
   - The key being passed
   - Source format (what the producing step outputs)
   - Target format (what the consuming step expects)
   - Whether the data is required
   - Optional schema validation hints
3. Track global context keys across all steps
4. Warn on format mismatches (e.g., step A outputs JSON but step B expects YAML)
