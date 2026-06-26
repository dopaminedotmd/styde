# Skill Pipeline Architect
Domain: skills-opt Version: 2

## Purpose
Architects skill pipelines for Styde Forge. Multi-skill workflows, state passing, error boundaries between skills.
Designs, validates, and integration-tests pipelines that compose multiple Hermes skills into robust multi-step workflows.

## Persona
Skill pipeline architect. Expert in composing skills into robust multi-step workflows.

## Pipeline
This blueprint defines a 6-step pipeline (plus 2 parallel substeps): analyze skills -> design pipeline -> design error boundaries + state contracts (parallel) -> compose pipeline -> validate -> integration test.

## Skills
- skill-analyzer: Parse and analyze skill files from a blueprint's skills/ directory
- pipeline-designer: Design pipeline topology from skill definitions and dependencies
- error-boundary-designer: Define error strategies (halt/skip/retry/fallback) between steps
- state-contract-designer: Define typed data contracts between steps
- pipeline-composer: Merge topology, errors, and contracts into a complete pipeline.yaml
- pipeline-validator: Structural validation of pipeline DAG, references, and contract integrity
- pipeline-tester: Integration test pipelines using stub agents to verify state flow and error handling

## State Contract
Key                          Produced By              Consumed By             Format
skills_analyzed              analyze-skills            design-pipeline          yaml
pipeline_design              design-pipeline           error-boundary-designer  yaml
pipeline_design              design-pipeline           state-contract-designer  yaml
error_boundaries             error-boundary-designer   compose-pipeline         yaml
state_contracts              state-contract-designer   compose-pipeline         yaml
composed_pipeline            compose-pipeline          validate-pipeline        yaml
validation_results           validate-pipeline         integration-test         yaml
test_results                 integration-test          (final output)           yaml

## Error Boundaries
Step                        Strategy      Max Retries   Fallback         Rationale
analyze-skills              halt          0             -                Cannot design pipeline without skill analysis
design-pipeline             halt          0             -                Topology is core to all downstream steps
design-error-boundaries     skip          0             -                Non-critical: pipeline can run without explicit boundaries
design-state-contracts      retry         2             -                State contracts are important but retryable
compose-pipeline            halt          0             -                No valid pipeline without composition
validate-pipeline           halt          0             -                Pipeline must be valid before testing
integration-test            retry         1             validate-pipeline Tests may transiently fail; fall back to re-validate
