---
name: css-token-architecture
description: >-
  Mandates CSS custom properties for all colors, typography, and spacing in
  dashboard mockups. Enforces a single style block or external stylesheet,
  forbids redundant font-weight declarations, and requires semantic color
  tokens over raw hex values.
license: MIT
metadata:
  author: styde-forge
  version: 1.0.0
compatibility: Vanilla CSS, any frontend framework
---

# /css-token-architecture -- Design Token System for Dashboard Mockups

You produce HTML/CSS dashboard mockups. Every pixel of styling must flow through a token system defined in a single :root block. Raw values in selectors are forbidden outside of one-off breakpoint overrides.

## Trigger
Activate on every dashboard mockup. Always. This is not optional.

## Core Pattern: Token Definition Block

At the top of every style block, declare all tokens:

```css
:root {
  /* Colors */
  --color-bg: #0f0f1a;
  --color-surface: #1a1a2e;
  --color-metric-primary: #ffffff;
  --color-metric-secondary: #a0a0b8;
  --color-headline: #ffffff;
  --color-accent: #6c63ff;
  --color-positive: #00c853;
  --color-negative: #ff5252;
  --color-neutral: #ffd740;

  /* Typography */
  --font-family-display: 'Playfair Display', 'Georgia', serif;
  --font-family-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --font-family-sans: 'Inter', 'Segoe UI', sans-serif;
  --font-size-hero: clamp(2.5rem, 6vw, 5rem);
  --font-size-headline: clamp(1.5rem, 3vw, 2.5rem);
  --font-size-metric: clamp(1rem, 2vw, 1.5rem);
  --font-size-label: 0.85rem;
  --font-size-delta: 0.75rem;
  --font-weight-bold: 700;
  --font-weight-semibold: 600;
  --font-weight-regular: 400;
  --line-height-tight: 1.1;
  --line-height-normal: 1.5;

  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  --space-xl: 4rem;
  --gap-grid: 1.5rem;
}
```

## Rules

1. One style block per file. No inline styles except for JS-driven dynamic values (chart data points, live counters, timestamps). Inline styles for layout, color, or typography are forbidden.

2. Every font-weight value must come from a custom property. Literal `font-weight: 700` or `font-weight: bold` in a selector is a violation. Use `font-weight: var(--font-weight-bold)`.

3. Color tokens must be semantic (e.g., `--color-metric-primary`), not descriptive (`--color-white`). This lets the theme swap without changing selectors.

4. No CSS rule may set both font-size and font-weight without also referencing at least one spacing token in the same selector group. This prevents orphaned typography declarations.

5. Container width/max-width must use a custom property or a named CSS Grid template area — never a raw percentage in the selector.

6. All gap, margin, and padding values in layout rules must come from the spacing token scale. The only exception is a one-off margin for breakpoint adjustments, which must be commented with the reason.

## Common Violations

```
/* VIOLATION: raw hex, no variable */
.card { background: #1a1a2e; }

/* CORRECT */
.card { background: var(--color-surface); }

/* VIOLATION: hardcoded font-weight */
.metric { font-weight: bold; }

/* CORRECT */
.metric { font-weight: var(--font-weight-bold); }

/* VIOLATION: inline style for static color */
<div style="color: #ffffff">

/* CORRECT */
<div class="metric-value">

/* VIOLATION: raw percentage width */
.widget { width: 66%; }

/* CORRECT — use Grid template areas or a spacing token */
.widget { width: calc(100% - var(--space-lg)); }
```

## Checklist
- [ ] Single :root block defines all colors, typography, spacing tokens
- [ ] Every selector uses `var(--token-name)` for color, font-weight, spacing
- [ ] No inline styles for static values
- [ ] No redundant font-weight declarations (same weight on same hierarchy level)
- [ ] All color names are semantic, not descriptive
- [ ] Layout uses CSS Grid with named template areas
- [ ] Font sizes use clamp() for responsive scale where appropriate
