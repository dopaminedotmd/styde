Task: manual benchmark for Dependency Mapper
analysis:
  domain: planning
  input: teacher feedback on eval accuracy (score 89/100)
  weakest_dimension: accuracy
  cause: unverified exit criteria claims without source references
dependency_graph:
  - id: A
    name: adopt accuracy evidence rule in BLUEPRINT.md
    depends_on: []
    effort: low
    impact: high
  - id: B
    name: add verification instruction to persona.md
    depends_on: [A]
    effort: low
    impact: medium
  - id: C
    name: set precision threshold in config.yaml
    depends_on: [A, B]
    effort: low
    impact: medium
  - id: D
    name: run eval with updated config
    depends_on: [C]
    effort: medium
    impact: high
  - id: E
    name: verify exit criteria anchor to source lines
    depends_on: [D]
    effort: medium
    impact: high
critical_path: A -> B -> C -> D -> E
critical_path_length: 5 nodes
estimated_total_effort: low (all file edits are single-rule additions)
bottlenecks:
  - node: A
    reason: evidence rule is prerequisite to all downstream changes; if poorly scoped it breaks B, C, D, E
  - node: C
    reason: config threshold must be calibrated — too strict rejects valid runs, too loose misses the accuracy fix
risks:
  - id: R1
    description: threshold in config.yaml set too high (e.g. accuracy > 95) rejects borderline runs
    likelihood: medium
    severity: medium
    mitigation: set accuracy >= 85 with UNKNOWN exit criteria cap at 20%, not both simultaneously
  - id: R2
    description: persona.md instruction conflicts with existing agent guidelines
    likelihood: low
    severity: low
    mitigation: review persona.md for contradictory clauses before edit
  - id: R3
    description: source-anchored evidence rule slows eval output
    likelihood: medium
    severity: low
    mitigation: allow brief source references — file:line or grep — not full content dumps
schedule_optimization:
  order: [A, B, C, D, E]
  parallelism_possible:
    - A and B: yes (independent edits to different files)
    - after C: D and E serial (config then run)
  recommended_start: A and B in parallel, then C, then D, then E
exit_criteria_verification:
  - file: BLUEPRINT.md
    claim: evidence rule added
    verification: read BLUEPRINT.md line count and confirm rule text
    file_lines_reference_needed: yes
  - file: persona.md
    claim: verification instruction added
    verification: read persona.md line count and confirm rule text
    file_lines_reference_needed: yes
  - file: config.yaml
    claim: precision threshold set
    verification: read config.yaml line count and confirm threshold values
    file_lines_reference_needed: yes
accuracy_improvement_prediction:
  before: 89.0
  after_estimated: 94-96
  rationale: source-anchored evidence eliminates unverifiable UNKNOWN claims which caused the accuracy deficit; remaining margin is natural variation in eval prompts