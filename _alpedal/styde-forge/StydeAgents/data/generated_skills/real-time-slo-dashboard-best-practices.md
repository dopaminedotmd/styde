# Real Time Slo Dashboard Best Practices

Proven practices from real-time-slo-dashboard (production agent, score 93.4/100)

## Rules

- BLUEPRINT.md: Add an 'execution preference' dimension to the output criteria: for each dimension (accuracy, clarity, completeness, efficiency, usefulness), specify whether the expected evidence is a design document or an executable artifact (code, config, patch). Tag this evaluation with 'efficiency: prefer_executable' as the gap.
- persona.md: Add a directive: 'When a design task could produce either a spec or an executable, default to executable (code skeleton, config fragment, patch) unless the task explicitly requests a document. An executable that is 80% complete is more efficient than a 100% spec.'

## When To Use

Use when working with dashboard tasks. Tags: dashboard, production.

## Source

Generated from pattern: `real-time-slo-dashboard`
Source blueprint: `real-time-slo-dashboard` (score: 93.4/100)
Generated: 2026-06-30T01:55:49Z
