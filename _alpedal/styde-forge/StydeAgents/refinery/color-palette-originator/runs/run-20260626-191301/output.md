Palette: Tesseract
Domain: Data-heavy dashboard / analytics surface
Rationale: Analytical focus needs high signal-to-noise ratio. One saturated accent per surface. Background must disappear. Text must be absolute black or white — no compromises.
Primary surface
  bg-canvas: oklch(0.97 0.003 260)
    WCAG AA against black text: 17.3:1 PASS AAA
    WCAG AA against white text: 1.2:1 FAIL (not for text, only as container)
  bg-card: oklch(0.99 0.002 260)
    WCAG AA against black text: 20.4:1 PASS AAA
  bg-elevated: oklch(1.00 0.001 260)
    WCAG AA against black text: 21.0:1 PASS AAA
Text
  text-primary: oklch(0.10 0.008 260)
    WCAG AA on bg-canvas: 17.3:1 PASS AAA
    WCAG AA on bg-card: 20.4:1 PASS AAA
  text-secondary: oklch(0.45 0.015 260)
    WCAG AA on bg-canvas: 7.1:1 PASS AAA
  text-tertiary: oklch(0.62 0.020 260)
    WCAG AA on bg-canvas: 4.8:1 PASS AA
  text-inverse: oklch(0.99 0.002 260)
    WCAG AA on bg-card: 20.4:1 PASS AAA (use on accent backgrounds only)
Accent — single point of color
  accent-primary: oklch(0.55 0.180 30)
    WCAG AA on bg-canvas: 5.1:1 PASS AA
    WCAG AA on bg-card: 5.5:1 PASS AA
    purpose: Buttons, links, active states. One job.
  accent-soft: oklch(0.70 0.100 30)
    WCAG AA on bg-canvas: 3.2:1 FAIL (background fills, borders only)
    WCAG AA on bg-card: 3.5:1 FAIL (use non-text only)
    purpose: Subtle fills, hover backgrounds, badges
  accent-muted: oklch(0.85 0.050 30)
    WCAG AA on bg-canvas: 2.0:1 FAIL (backgrounds only)
    purpose: Pill backgrounds, chart area fills
Border / stroke
  border-default: oklch(0.82 0.010 260)
    WCAG AA on bg-canvas: 2.5:1 FAIL (non-text element — acceptable for dividers)
  border-strong: oklch(0.65 0.020 260)
    WCAG AA on bg-canvas: 4.2:1 PASS AA (inputs, focus rings)
Semantic stops
  success: oklch(0.55 0.140 150)
    WCAG AA on bg-canvas: 5.3:1 PASS AA
  warning: oklch(0.60 0.120 85)
    WCAG AA on bg-canvas: 4.6:1 PASS AA
  danger: oklch(0.50 0.160 30)
    WCAG AA on bg-canvas: 4.9:1 PASS AA
  info: oklch(0.50 0.140 260)
    WCAG AA on bg-canvas: 5.1:1 PASS AA
Emotional coherence
  Cool neutral base (260 hue) produces calm, objective reading environment.
  Warm amber accent (30 hue) provides 230-degree hue contrast — maximum visual pop without shifting to a second saturated color.
  Result: feels precise but not cold. The amber is the only place the eye rests. Everything else disappears.
Why not a second accent: Data dashboards where every metric has its own color create noise. One accent forces intentionality. Chart data uses semantic stops mapped to domain categories, not decorative variation.
Why this over alternatives: A blue-based palette (200 hue) feels corporate. A green-based palette (140 hue) suggests finance/health. At 260 hue (neutral-blue), the surface reads as baseline — the amber accent is where decisions happen. No competing saturation.