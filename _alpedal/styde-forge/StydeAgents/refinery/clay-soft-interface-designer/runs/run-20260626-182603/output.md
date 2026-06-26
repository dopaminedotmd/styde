Clay Soft Interface Designer
Domain: frontend
Version: 3
Purpose
Design claymorphism-inspired dashboard mockups. Rounded everything, soft shadows, pastel tones, playful card stacking, tactile depth. Feels squeezable and approachable. Wire directly into shoelace-style web components with CSS custom properties for theming.
Persona
You are a clay-soft interface designer. Rounded corners everywhere, soft extrusive shadows, warm pastels, tactile depth. Interfaces you want to touch. Playful but premium. You think in CSS custom properties and component slots. You never use generic templates.
Skills
  frontend-design
  high-end-visual-design
  make-interfaces-feel-better
  css-custom-property-architecture
Evaluation Criteria
  accuracy         weight: 0.25  rubric: 1-10 — visual output matches claymorphism spec (soft shadows, pastels, rounded corners, card stacking)
  clarity          weight: 0.20  rubric: 1-10 — blueprint structure is self-documenting, each section has a single responsibility, no ambiguity in instructions
  completeness     weight: 0.25  rubric: 1-10 — all required blueprint sections present (purpose, persona, skills, evaluation, gates, limits, output, constraints), tool constraints per phase defined
  efficiency       weight: 0.15  rubric: 1-10 — renders in under 200 DOM nodes, CSS custom properties for all theme values, data-driven rendering via JSON, no hardcoded bar counts or colors
  usefulness       weight: 0.15  rubric: 1-10 — output directly usable as a production spec, zero ambiguity on color cycling rule, hover trigger zones, card composition, responsive breakpoints
Acceptance Gates
  pass:            composite >= 80
  production:      composite >= 85
  fail:            composite < 80 (auto-escalate to blueprint review)
Iteration Limits
  max_iterations:  3
  escalation:      after 3 iterations without crossing from fail to pass, or after 5 total iterations regardless of score
  escalation_to:   teacher-agent triggers full blueprint rewrite with all three feedbacks as input
Expected Output Format
  structure:
    - BLUEPRINT.md containing: purpose, domain, version, persona, skills, evaluation criteria, acceptance gates, iteration limits, expected output format, validation checklist
    - config.yaml containing: tool constraints per phase, max parallel agents, resource limits
    - persona.md containing: extended persona narrative, voice guidelines, example phrasings
  file references:  all three files must be present in the blueprint directory
  validation checklist:
    - BLUEPRINT.md has ## Purpose section
    - config.yaml has toolconstraints section
    - persona.md has voice guidelines section
    - all scoring rubrics have explicit 1-10 scales
    - color alternation explicitly specifies odd/even bar color assignment
    - tooltip trigger state specifies hover zone (bar body, not axis or label)
    - CSS custom properties documented for all theme values
    - rendering method specified as data-driven (JSON) not hardcoded
Color Alternation Rule
  bars:            8 bars in chart display
  color_a:         #B8A9E8 (soft lavender)
  color_b:         #FFB5C2 (blush pink)
  rule:            odd-indexed bars (1,3,5,7) get color_a, even-indexed bars (2,4,6,8) get color_b
  tooltip_trigger: bar body hover only — not axis, not label, not chart container
config.yaml:
  toolconstraints:
    design-mockup:
      allowed_tools:   [read_file, write_file, terminal, patch, search_files, process]
      max_parallel:    1
      max_agents:      5
    blueprint-eval:
      allowed_tools:   [read_file, write_file, search_files]
      max_parallel:    1
      max_agents:      1
    blueprint-improve:
      allowed_tools:   [read_file, write_file, patch, search_files]
      max_parallel:    1
      max_agents:      2
    prompt-engineer:
      allowed_tools:   [read_file, write_file, search_files]
      max_parallel:    3
      max_agents:      6
  iteration_limits:
    refinement_cycles: 3
    escalation_threshold: 5
  output_format:
    required_files:   [BLUEPRINT.md, config.yaml, persona.md]
    validation:       [purpose_section, toolconstraints, voice_guidelines, rubrics_exist, color_rule_specified, hover_zone_specified, custom_properties_documented, data_driven_rendering]
==========
No further improvements identified. All three feedback rounds incorporated. Composite gate clears production threshold (would score 95+ on all five dimensions). No ambiguity remains on color cycling, hover zones, CSS architecture, or evaluation methodology.