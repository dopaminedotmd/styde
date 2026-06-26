# Pipeline Composer

## Purpose
Merge topology, error boundaries, and state contracts into a complete pipeline.yaml file ready for execution.

## Inputs
- topology: Pipeline topology from pipeline-designer
- error_boundaries: Error boundary specs from error-boundary-designer (optional)
- state_contracts: State contract specs from state-contract-designer (optional)

## Outputs
A YAML mapping with key `pipeline` containing the complete pipeline YAML:
```yaml
pipeline:
  name: <pipeline-name>
  version: "<version>"
  description: "<description>"
  steps:
    - id: <step-id>
      skill: <skill-name>
      description: "<step-description>"
      depends_on: [<dependency-ids>]
      inputs: [...]
      outputs: [...]
      error: <strategy>
  state_contract:
    version: "1.0"
    keys: {<key>: <description for each>}
```

## Behavior
1. Start with the topology serial steps as the base
2. Wrap parallel groups in `parallel:` sections
3. Annotate each step with its error strategy from error_boundaries
4. Annotate each step's input/output contracts from state_contracts
5. Preserve step ordering from topology
6. Add global state_contract section with all tracked keys
7. Return complete pipeline YAML ready for PipelineRunner
