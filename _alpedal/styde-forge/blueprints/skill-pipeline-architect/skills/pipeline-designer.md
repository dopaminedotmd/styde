# Pipeline Designer

## Purpose
Design pipeline topology from skill definitions. Determine step ordering, parallel groups, and state flow between skills.

## Inputs
- skill_definitions: List of analyzed skill objects with name, inputs, outputs, dependencies

## Outputs
A YAML mapping with key `pipeline_design` containing:
```yaml
pipeline_design:
  topology:
    serial: [<step-ids in order>]
    parallel_groups:
      - id: group-1
        steps: [<step-ids that run concurrently>]
  state_flow:
    - from: <step-id>
      to: <step-id>
      keys: [<data keys transferred>]
```

## Behavior
1. Inspect skill dependencies to determine ordering
2. Skills with no inter-dependency can run in parallel
3. Skills with data dependencies must run in serial (order by dependency chain)
4. Design state flow between each connected pair
5. Return complete topology as YAML

## Rules
- A skill that depends on another's output must come after it
- Independent skills at the same depth are candidates for parallel groups
- The topology must be a directed acyclic graph (DAG)
- Maximum parallel group size: 5 (concurrency limit)
