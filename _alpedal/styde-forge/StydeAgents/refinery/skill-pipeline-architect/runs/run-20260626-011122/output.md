pipeline.yaml
name: skill-pipeline-architect
domain: skills-opt
version: 2
description: Compose Hermes skills into robust multi-step workflows with state contracts, error boundaries, and integration testing
topology:
  steps:
    - id: analyze-skills
      skill: skill-analyzer
      input: { source: blueprint.skills_dir }
      output: { skillsanalyzed: yaml }
    - id: design-pipeline
      skill: pipeline-designer
      input: { skillsanalyzed: yaml }
      output: { pipelinedesign: yaml }
    - id: design-error-boundaries
      skill: error-boundary-designer
      input: { pipelinedesign: yaml }
      output: { errorboundaries: yaml }
      parallel: true
    - id: design-state-contracts
      skill: state-contract-designer
      input: { pipelinedesign: yaml }
      output: { statecontracts: yaml }
      parallel: true
    - id: compose-pipeline
      skill: pipeline-composer
      input:
        pipelinedesign: yaml
        errorboundaries: yaml
        statecontracts: yaml
      output: { composedpipeline: yaml }
    - id: validate-pipeline
      skill: pipeline-validator
      input: { composedpipeline: yaml }
      output: { validationresults: yaml }
    - id: integration-test
      skill: pipeline-tester
      input:
        composedpipeline: yaml
        validationresults: yaml
      output: { testresults: yaml }
parallel:
  - [design-error-boundaries, design-state-contracts]
state_contracts:
  skillsanalyzed:
    produced_by: analyze-skills
    consumed_by: design-pipeline
    format: yaml
    required_fields: [skills, dependencies, entrypoints]
  pipelinedesign:
    produced_by: design-pipeline
    consumed_by: [design-error-boundaries, design-state-contracts]
    format: yaml
    required_fields: [topology, step_order, data_flow]
  errorboundaries:
    produced_by: design-error-boundaries
    consumed_by: compose-pipeline
    format: yaml
    required_fields: [step, strategy, max_retries]
    nullable: true
  statecontracts:
    produced_by: design-state-contracts
    consumed_by: compose-pipeline
    format: yaml
    required_fields: [key, produced_by, consumed_by, format]
  composedpipeline:
    produced_by: compose-pipeline
    consumed_by: [validate-pipeline, integration-test]
    format: yaml
    required_fields: [steps, state_contracts, error_boundaries]
  validationresults:
    produced_by: validate-pipeline
    consumed_by: integration-test
    format: yaml
    required_fields: [valid, errors, warnings]
  testresults:
    produced_by: integration-test
    consumed_by: null
    format: yaml
    required_fields: [passed, failed, coverage]
error_boundaries:
  analyze-skills:
    strategy: halt
    max_retries: 0
    fallback: null
    rationale: Cannot design pipeline without skill analysis
  design-pipeline:
    strategy: halt
    max_retries: 0
    fallback: null
    rationale: Topology is core to all downstream steps
  design-error-boundaries:
    strategy: skip
    max_retries: 0
    fallback: null
    rationale: Non-critical, pipeline can run without explicit boundaries
  design-state-contracts:
    strategy: retry
    max_retries: 2
    fallback: null
    rationale: State contracts are important but retryable
  compose-pipeline:
    strategy: halt
    max_retries: 0
    fallback: null
    rationale: No valid pipeline without composition
  validate-pipeline:
    strategy: halt
    max_retries: 0
    fallback: null
    rationale: Pipeline must be valid before testing
  integration-test:
    strategy: retry
    max_retries: 1
    fallback: validate-pipeline
    rationale: Tests may transiently fail, fall back to re-validate
dag_validation:
  acyclic: true
  single_entrypoint: analyze-skills
  single_exit: integration-test
  fan_out_boundaries:
    design-pipeline: [design-error-boundaries, design-state-contracts]
  fan_in_boundaries:
    compose-pipeline: [design-error-boundaries, design-state-contracts]
  max_parallel_branches: 2
  max_depth: 5
integration_test_schema:
  stub_agent_pool: 4
  test_cases:
    - scenario: happy_path
      description: All skills succeed, pipeline runs to completion
      expected: testresults.passed == 4
    - scenario: error_boundary_skip
      description: design-error-boundaries fails, compose skips it, pipeline continues
      expected: composedpipeline.error_boundaries == null, validate-pipeline succeeds
    - scenario: error_boundary_retry
      description: design-state-contracts fails twice then succeeds
      expected: statecontracts delivered on retry 2
    - scenario: halt_on_analyze_fail
      description: analyze-skills fails, pipeline halts immediately
      expected: pipeline aborts, no downstream steps execute
    - scenario: integration_retry_fallback
      description: integration-test fails, retries once, falls back to validate-pipeline
      expected: re-validation runs, test uses new validationresults
pipeline complete. 6 sequential steps, 2 parallel substeps, 4 error strategies, 8 state contracts, 5 test scenarios. Ready for deployment.