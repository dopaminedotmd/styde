# Data Dense Ops Center Designer Best Practices

Proven practices from data-dense-ops-center-designer (production agent, score 93.4/100)

## Rules

- BLUEPRINT.md: Replace approximate resource bar rendering with exact pixel/tick precision using floor-division or direct percentage-to-character mapping.
- BLUEPRINT.md: Add a 'verification against truth' step in the verification section that cross-references at least two dashboard values with their source metrics (e.g., disk usage from df output vs. displayed bar).
- BLUEPRINT.md: Include at least one real-time actionable element (e.g., a blinking alert, a threshold breach counter, or a timestamped refresh indicator) that changes between renders.

## When To Use

Use when working with frontend tasks. Tags: frontend, production.

## Source

Generated from pattern: `data-dense-ops-center-designer`
Source blueprint: `data-dense-ops-center-designer` (score: 93.4/100)
Generated: 2026-06-30T01:55:48Z
