changes:
  - file: BLUEPRINT.md
    changes:
      - Section: routeorder method area
        action: add schemas
        detail: Define Venue and VenueRouting pydantic schemas above routeorder() with explicit cross-references to parameter types in the method signature
        impact: medium
      - Section: before implementation
        action: add edge case validation paragraph
        detail: >
          List specific invariants to check: total slices never zero, remainder not
          double-counted, quantity not overshoot target. Require one-line assertion
          or proof per invariant before code.
        impact: high
      - Section: after implementation
        action: add self-verify step
        detail: >
          Require 2-3 smoke cases (e.g. qty < slices, qty % slices != 0, qty == 0)
          with confirmed output totals matching input quantity before deliverable.
        impact: medium
  - file: persona.md
    changes:
      - action: append rule
        detail: >
          When blueprint specifies completeness tiers (85/90/95+), agent MUST provide
          sample I/O for every tier above 85. Never stop at descriptions without examples.
        impact: low
      - action: append constraint
        detail: >
          Before finalizing any quantitative solution, identify at least two edge cases
          and assert they produce correct totals.
        impact: medium
summary:
  current_composite: 81.0
  target: 85.0
  gap: 4.0
  critical_path:
    - edge_case_validation: high impact, addresses root cause of accuracy deficit
    - self_verify_step: medium impact, closes verification gap
    - schema_definitions: medium impact, fixes structural incompleteness
  risk:
    - Without invariant assertions, agents produce structurally correct code with
      silent arithmetic bugs (off-by-one, double-count, slice overshoot)
    - Without self-verify, correctness is assumed rather than demonstrated