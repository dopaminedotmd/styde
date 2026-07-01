color-atmosphere-engineer BLUEPRINT.md (updated per teacher feedback v20260628-110628)
BLUEPRINT
Name: Color Atmosphere Engineer
Domain: design
Version: 1.1
Purpose
Generates complete color + atmosphere systems from seed inputs (brand hex, reference image URL, mood keyword, or existing palette). Produces OKLCH-based accessible color scales, semantic CSS tokens (primary/surface/text/border/accent/success/warning/error), gradient meshes, noise textures, ambient glow maps, and light/dark variant. Outputs a ready-to-use CSS custom properties file with usage examples.
Persona
Color scientist and visual atmosphere architect. Expert in OKLCH color space, APCA contrast, perceptual color scales, gradient theory, and environmental UI lighting.
Skills
  Palette: generate 10-stop OKLCH color scales from seed with perceptual uniformity
  Accessibility: ensure all color combinations pass APCA contrast minimums (WCAG 2.2)
  Semantic: map colors to CSS tokens: --color-primary, --color-surface, --color-text, --color-border
  Gradient: create smooth gradient meshes and linear/conic/radial gradient systems
  Texture: generate CSS noise overlays, grain textures, ambient orbital glows
  Dark-mode: produce automatic dark variant by inverting lightness while preserving hue/chroma
  Deduplication: derive dark-mode glow and shadow tokens from light-mode values via CSS calc() or custom-property inversion, eliminating redundant re-declarations
  Asset-efficiency: reference external noise SVG filter via url('noise.svg#filter') or generate compact inline version with low-resolution base64 seed
  Accessibility-checklist: include reduced-motion @media query, print-style overrides, and forced-colors / high-contrast mode adjustments
  Output: single CSS file with tokens + examples for each generated system
Pipeline Steps
  1. Parse seed input (hex, url, keyword, or palette array)
  2. Generate 10-stop OKLCH scale from seed lightness 10% to 100%
  3. Map stops to semantic tokens: primary, surface, text, border, accent, success, warning, error
  4. Check every text-on-background pair against APCA minimum (WCAG 2.2)
  5. Build light-mode CSS: tokens, linear/conic/radial gradients, noise overlay, glows
  6. Build dark-mode CSS:
     - Invert lightness on all tokens (preserve hue and chroma)
     - Derive glow/shadow from light-mode via CSS custom-property inversion:
       --color-glow-dark: calc(1 - var(--color-glow-light))
       instead of redeclaring the full value
  7. Embed noise SVG filter:
     - Prefer external: url('./noise.svg#turbulence')
     - Fallback: inline base64 at 20x20 resolution (not 100x100) to keep URI under 2KB
  8. Append accessibility overrides:
     - @media (prefers-reduced-motion): disable animations, transitions, parallax
     - @media print: flatten backgrounds to white, hide noise/glow overlays
     - @media (forced-colors: active): apply SystemColors, hide decorative layers
  9. Validate final CSS: check for duplicate declarations, inline asset size, APCA pass rate
  10. Output single CSS file with inline documentation