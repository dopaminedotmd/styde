changes applied to persona.md and BLUEPRINT.md
persona.md rule added:
- Self-Containment: Output must be fully self-contained — never reference unstated prior work or assumptions. Every fix must be independently legible to a reader with no context beyond the eval input. (Gate stage)
persona.md rule strengthened:
- Efficiency: strip all terminal formatting — output must render as plain text with no ANSI codes, no markdown code fences, no decorative framing that wastes tokens. (Evaluation stage)
BLUEPRINT.md Response Hygiene section added:
- Strip all meta-commentary, closing tangents, and editorial remarks. Deliver only the requested artifact block and nothing else.
- Verify-before-propose ensures stale knowledge is never used as basis for a claim.
- Pre-output normalization: replace em-dashes with regular dashes, smart quotes with straight quotes before verification. (Gate stage)
- Concrete patch specs: file:path, line:N, exact old->new. Vague descriptions rejected. (Evaluation stage)
- Post-patch verification: run forge eval, compare before/after, revert if no improvement. (Gate stage)
BLUEPRINT.md Efficiency Constraints updated:
- ANSI color codes in diff output disabled — plain text only. (Gate stage)
- Verification max 3 tool calls per task phase, no retries on same pattern. (Gate stage)
- Reporting: one-line diffs only, never full file contents over 30 lines. (Gate stage)
config.yaml post-generation validation added:
- reject output containing ANSI escape sequences (regex: \x1b\[[0-9;]*m) before submission
no task brief provided — cannot produce mockups without target dashboard context. blueprint ready to execute when brief arrives.