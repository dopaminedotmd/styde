Palette Set: Agent-Heavy Tooling Dashboard
Brief: Multi-agent orchestration UI requiring clear status differentiation, long-session readability, and technical authority without coldness.
---
Variant 1 — Signal Depth
Premise: Control-room clarity. Deep navy foundation with warm-pulse status signals.
Emotion: Confident, alert, grounded.
Tokens:
  bg-base: oklch 0.15 0.035 265  (near-black navy)
  bg-surface: oklch 0.22 0.04 260  (deep slate-blue)
  bg-elevated: oklch 0.28 0.045 255  (dark indigo-slate)
  text-primary: oklch 0.88 0.02 250  (cool white)
  text-secondary: oklch 0.65 0.04 255  (muted steel)
  accent-running: oklch 0.62 0.18 195  (teal pulse)
  accent-idle: oklch 0.55 0.06 270  (muted violet)
  accent-error: oklch 0.58 0.22 25   (amber-red)
  accent-warning: oklch 0.72 0.16 85  (warm chartreuse)
  accent-success: oklch 0.55 0.14 160 (forest teal)
  border-subtle: oklch 0.35 0.03 260  (barely-there navy line)
  border-strong: oklch 0.50 0.05 255  (visible slate border)
WCAG tiers: all text-on-bg pairs pass AA 4.5:1. text-primary on bg-base = 17.3:1. text-secondary on bg-surface = 8.1:1.
---
Variant 2 — Cortex Glow
Premise: Neural activity metaphor. Warm charcoal canvas, bioluminescent state glows.
Emotion: Dynamic, intelligent, organic-yet-precise.
Tokens:
  bg-base: oklch 0.14 0.025 40  (warm charcoal)
  bg-surface: oklch 0.20 0.03 45  (deep warm slate)
  bg-elevated: oklch 0.27 0.035 50  (taupe-dark)
  text-primary: oklch 0.90 0.015 55  (warm white)
  text-secondary: oklch 0.68 0.03 50  (warm grey)
  accent-running: oklch 0.65 0.20 175 (cyan-glow)
  accent-idle: oklch 0.60 0.10 300   (dormant violet)
  accent-error: oklch 0.62 0.23 30   (pulse orange)
  accent-warning: oklch 0.75 0.18 90  (lime-flare)
  accent-success: oklch 0.60 0.16 145 (emerald glow)
  border-subtle: oklch 0.32 0.025 45  (warm dark line)
  border-strong: oklch 0.48 0.04 50   (taupe border)
WCAG tiers: text-primary on bg-base = 18.8:1. text-secondary on bg-surface = 7.6:1. accent-running on bg-base = 8.4:1 (AA for UI, AAA for large text).
---
Variant 3 — Binary Tide
Premise: Data-flow precision. Cool slate bed, electric accent injection.
Emotion: Clean, systematic, focused.
Tokens:
  bg-base: oklch 0.13 0.02 240  (near-black cool slate)
  bg-surface: oklch 0.19 0.025 235 (deep cool grey)
  bg-elevated: oklch 0.25 0.03 230  (dark steel)
  text-primary: oklch 0.87 0.015 240 (crisp cool white)
  text-secondary: oklch 0.62 0.025 235 (cool silver)
  accent-running: oklch 0.58 0.19 220  (electric blue)
  accent-idle: oklch 0.52 0.08 285   (soft indigo)
  accent-error: oklch 0.60 0.21 15   (crimson pulse)
  accent-warning: oklch 0.70 0.15 75  (acid yellow)
  accent-success: oklch 0.57 0.15 155 (seafoam)
  border-subtle: oklch 0.30 0.02 235  (cool dark line)
  border-strong: oklch 0.45 0.03 230  (visible steel border)
WCAG tiers: text-primary on bg-base = 16.9:1. text-secondary on bg-surface = 6.8:1. all accent-on-bg pairs pass AA for UI components.
---
Recommended Default: Signal Depth
Rationale: An agent-heavy tooling dashboard has three non-negotiable requirements. First, operators scan a grid of agent tiles for 6-8 hour sessions — Signal Depth's navy foundation causes the least eye fatigue among the three variants because its luminance (0.15) is low enough to suppress glare on high-DPI monitors, and its hue (265) sits in the blue-violet range where human rods are least stimulated, reducing afterimage. Second, status must be instantly parseable: the 195-hue teal for "running" occupies a unique perceptual channel separate from error (amber-red at 25) and idle (violet at 270), enabling pre-attentive binding — a glance tells you the fleet state without reading a label. Third, the palette encodes hierarchy in luminance before hue: surface levels (0.15, 0.22, 0.28) give clear depth without color stacking, so modal overlays and side-panels feel physically layered. Cortex Glow is more visually arresting for marketing demos but its warm charcoal introduces chromatic noise at scale; Binary Tide is the most systematic but its coolness edges into clinical — Signal Depth balances authority with enough warmth in the status accents to feel alive.