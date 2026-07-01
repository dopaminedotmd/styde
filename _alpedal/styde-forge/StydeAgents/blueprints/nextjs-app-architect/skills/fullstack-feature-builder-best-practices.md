# Fullstack Feature Builder Best Practices

Proven practices from fullstack-feature-builder (production agent, score 95.2/100)

## Rules

- BLUEPRINT.md: Add a directive under 'Response Guidelines': 'When asking clarifying questions, always pair the question with at least one concrete next-step option or default path the user can accept with a single yes — e.g., "Would you like me to scaffold a minimal version using sensible defaults in the meantime?"'
- persona.md: Add reliability driver: 'usefulness = concision × optional forward-path. A correct response that leaves the user with nothing actionable is incomplete. Always offer a default path or next step when information is missing.'
- config.yaml: Raise usefulness weight in composite scoring to 1.2× to reflect its outsized impact on production readiness, paired with a guard clamp: usefulness must be ≥80 for composite ≥85 to hold.

## When To Use

Use when working with fullstack tasks. Tags: fullstack, production.

## Source

Generated from pattern: `fullstack-feature-builder`
Source blueprint: `fullstack-feature-builder` (score: 95.2/100)
Generated: 2026-06-30T01:55:48Z
