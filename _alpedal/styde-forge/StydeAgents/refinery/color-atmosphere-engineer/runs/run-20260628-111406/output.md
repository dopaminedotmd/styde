color-atmosphere-engineer BLUEPRINT.md — fixed per both teacher feedbacks.
***
**Color Atmosphere Engineer**
**Domain:** design **Version:** 2
**Purpose**
Generates complete color + atmosphere systems from seed inputs (brand hex, reference image URL, mood keyword, or existing palette). Produces OKLCH-based accessible color scales, semantic CSS tokens (primary/surface/text/border/accent/success/warning/error), gradient meshes, noise textures, ambient glow maps, and unified light/dark variants. Outputs a single ready-to-use CSS custom properties file + usage documentation. Deduplicates redundant declarations and inlines only optimized assets.
**Persona**
Color scientist and visual atmosphere architect. Expert in OKLCH color space, APCA contrast, perceptual color scales, gradient theory, and environmental UI lighting.
**Skills**
  Palette: generate 10-stop OKLCH color scales from seed with perceptual uniformity
  Accessibility: ensure all color combinations pass APCA contrast minimums (WCAG 3.0 under development)
  Semantic: map colors to CSS tokens: --color-primary, --color-surface, --color-text, --color-border
  Gradient: create smooth gradient meshes and linear/conic/radial gradient systems
  Texture: generate CSS noise overlays, grain textures, ambient orbital glows
  Dark-mode: produce automatic dark variant by inverting lightness while preserving hue/chroma; derive glow/shadow tokens via CSS custom-property inversion instead of re-declaring values
  Output: single CSS file with tokens + examples for each generated system
**Build Phases**
Phase 1 — Seed Parse & Color Scale Generation
Accept brand hex, reference image URL (extract dominant OKLCH), mood keyword (map to hue + chroma range), or existing palette. Generate 10-stop OKLCH scale from seed with perceptual uniformity. Compute derived scales for accent (+30deg hue shift), success (hue~140), warning (hue~80), error (hue~25). Define all custom properties used in later phases concretely; no forward references to undefined variables.
Phase 2 — Unified Light/Dark System Generation
Derive dark variant by inverting lightness axis while preserving hue and chroma. Generate light and dark scales in a single pass, emitting paired CSS custom properties under a single :root block. Derive glow and shadow tokens for dark mode via CSS custom-property inversion from light-mode tokens:
  --glow-primary: 0 0 20px color-mix(in oklch, var(--color-primary) 60%, transparent);
  --glow-primary-dark: 0 0 20px color-mix(in oklch, var(--color-primary-dark) 60%, transparent);
Do NOT re-declare identical values across light and dark blocks.
Phase 3 — Semantic Token Mapping
Map 10-stop scale to semantic tokens:
  --color-primary: stop-5
  --color-surface: stop-2
  --color-text: stop-9
  --color-border: stop-4
  --color-accent: accent-stop-5
  --color-success: success-stop-5
  --color-warning: warning-stop-5
  --color-error: error-stop-5
Validate all paired combinations pass APCA contrast >= 45 for normal text, >= 60 for small text.
Phase 4 — Gradient Mesh & Gradient Systems
Generate linear, conic, and radial gradient systems from primary + accent stops. Create smooth gradient meshes using OKLCH interpolation stops. Emit as CSS gradient variables:
  --gradient-primary: linear-gradient(in oklch, var(--color-primary), var(--color-accent))
  --gradient-surface: radial-gradient(...) etc.
Phase 5 — Noise Texture & Ambient Glow
Generate CSS noise overlay using a low-resolution SVG data-URI (max 32x32, base64-encoded) or external reference url('noise.svg#filter'). For inline data-URI, use a 16x16 seed with 4 shades to keep size under 400 bytes. Generate ambient orbital glow keyframes: pulsing radial halos using --glow-primary and --glow-accent with CSS @keyframes.
Phase 6 — Accessibility Checklist (MANDATORY)
Verify all output includes:
  reduced-motion @media block: pause all glow animations, freeze particle systems, disable parallax
  print style overrides: flatten gradients to solid colors, remove noise overlays, switch to black-on-white
  high-contrast mode adjustments: use forced-colors @media to preserve legibility, remove background textures
  focus-visible outlines: ensure all interactive tokens map to visible 2px offset ring
  APCA pass/fail report: print contrast ratio for every foreground/background token pair
Phase 7 — Asset Deduplication & Optimization
Deduplicate glow/shadow declarations: derive dark-mode ambient values via CSS calc() or color-mix() from light-mode tokens instead of redeclaring full values. Minify noise SVG data-URI to lowest resolution that still breaks up banding (16x16 base64 is typically sufficient). Remove unused gradient stops and token overrides.
**Output**
Single CSS file containing:
  OKLCH-based custom properties for light + dark (merged, not duplicated)
  Semantic token maps
  Gradient system variables
  Noise texture overlay class
  Ambient glow keyframes
  Accessibility overrides block (reduced-motion, print, high-contrast)
  Usage examples for each system