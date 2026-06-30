# Algo Execution Engine Best Practices

Proven practices from algo-execution-engine (production agent, score 94.8/100)

## Rules

- BLUEPRINT.md: Refactor `_allocate_by_score` to compute total inverse-weight in a single O(n) pass, then allocate proportionally.
- BLUEPRINT.md: Populate `venuebreakdown` dict by grouping score slices per venue instead of returning an empty placeholder.
- BLUEPRINT.md: Add an inline comment or docstring in `smartrouteorder` explaining the clarity-gate refactoring and why line count was reduced.

## When To Use

Use when working with day-trading tasks. Tags: day-trading, production.

## Source

Generated from pattern: `algo-execution-engine`
Source blueprint: `algo-execution-engine` (score: 94.8/100)
Generated: 2026-06-30T01:55:48Z
