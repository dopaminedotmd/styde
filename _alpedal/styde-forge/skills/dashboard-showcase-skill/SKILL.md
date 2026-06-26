# Dashboard Showcase Skill

Proven output template for multi-mockup delivery. Enforces readability and structure when presenting N distinct design artifacts.

## Template

```
[ARTIFACT N: Label]
[1-2 sentence description of what this mockup demonstrates]

--- Display artifact (HTML/CSS content) ---

---
Commentary: what design territory this explores, unique visual choices, what makes it distinct from other artifacts.

[ARTIFACT N+1: Label]
...
```

## Closing Summary Table

| # | Variant | Theme | What Makes It Unique |
|---|---------|-------|---------------------|
| 1 | Label   | Core visual philosophy | Key differentiator |

## Rules

1. Every artifact gets a numbered label and a 1-2 sentence description.
2. Separator (---) with commentary between every artifact.
3. Closing summary table always renders last, even if truncation is needed.
4. If character budget runs low: truncate from the middle of artifacts (cut tail sections before code blocks), never strip the summary.
5. No two artifacts may share the same primary color, font stack, or card layout pattern.
6. Use CSS class-based styling — no inline styles except dynamic JS values.
7. Maximum one nested wrapper div per section.
