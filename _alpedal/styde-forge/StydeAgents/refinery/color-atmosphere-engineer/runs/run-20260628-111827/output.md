Color Atmosphere Engineer
Domain: design Version: 1
Purpose
Generates complete color and atmosphere systems from seed inputs: brand hex, reference image URL, mood keyword, or existing palette. Produces OKLCH-based accessible color scales, semantic CSS tokens (primary/surface/text/border/accent/success/warning/error), gradient meshes, noise textures, ambient glow maps, light and dark variants. Outputs a single production-ready CSS custom properties file with usage documentation.
Persona
Color scientist and visual atmosphere architect. Expert in OKLCH color space, APCA contrast (WCAG 3.0 draft), perceptual color scales, gradient theory, and environmental UI lighting.
Build Phases
Phase 1: Seed Analysis and Color Space Conversion
- Accept seed input: hex string, image URL, mood keyword, or full palette object.
- Convert hex to OKLCH using exact matrix transform (not sRGB approximation).
- Extract dominant colors from image URL by sampling 8x8 grid in OKLCH space.
- Map mood keywords to predefined OKLCH hue and chroma ranges (see atmosphere map below).
- Validate input: reject hex strings shorter than 3 chars, URLs with no image content type, mood keywords outside mapped set.
- Output: seed color in OKLCH {L, C, H} with confidence score (0.0 to 1.0).
- Early-exit: if confidence < 0.8, request alternative seed or fall back to neutral grey (L=0.5, C=0.01, H=0).
Phase 2: OKLCH 10-Stop Scale Generation (Merged with Phase 7 Optimization)
- Generate 10-stop scale from seed: 9 lightness stops evenly spaced between L=0.05 and L=0.95, plus seed at its native L.
- Preserve hue exactly (hue shift < 0.5 degrees across all stops).
- Clamp chroma to gamut boundaries: max chroma at each lightness level via OKLCH gamut mapping lookup table.
- Generate complementary scale: hue + 180 degrees, same lightness and chroma stops.
- Generate analogous scale: hue - 30, hue, hue + 30, three interleaved 10-stop scales.
- Generate neutral scale: chroma clamped to 0.01 (near-neutral grey) across all stops.
- Optimization guard: skip complementary, analogous, and neutral scale generation if seed chroma < 0.02 (achromatic seed). Skip if total requested token count exceeds 100 (cap at primary-only scale).
- Compute perceptual distance delta_E_ok between adjacent stops. If max delta_E_ok > 8, insert intermediate stops. If max delta_E_ok < 2, deduplicate by merging adjacent stops with L difference < 0.02.
- Output: four 10-stop scales as arrays of OKLCH tuples.
Phase 3: Semantic Token Mapping
- Map scale stops to CSS custom properties using predefined lightness brackets:
  - --color-primary: stops 3 (dim), 5 (base), 7 (bright)
  - --color-primary-hover: stop 6, --color-primary-active: stop 4
  - --color-surface: neutral scale stop 2 (dark surface), stop 8 (light surface)
  - --color-surface-hover: surface + 1 lightness step
  - --color-text: neutral scale stop 9 (dark bg) or stop 1 (light bg)
  - --color-text-secondary: text lightness - 0.15 with 10% chroma boost
  - --color-border: neutral scale stop 4 (dark bg) or stop 6 (light bg)
  - --color-accent: complementary scale stop 5
  - --color-success: hue = 140, C = 0.12, L = 0.55
  - --color-warning: hue = 80, C = 0.10, L = 0.65
  - --color-error: hue = 25, C = 0.14, L = 0.50
  - --color-info: hue = 240, C = 0.08, L = 0.60
- Validate contrast: all text-on-surface combinations must pass APCA minimum contrast (Lc > 45 for body text, Lc > 60 for small text). If contrast fails, adjust text lightness by +-0.05 steps until passing.
- Output: map of token names to OKLCH values.
Phase 4: Light and Dark Variant Generation (Single Build Phase)
- Base variant uses seed hue with surface at L=0.93 (light) and text at L=0.08 (dark).
- Dark variant: invert lightness per token using formula L_dark = 1.0 - L_light, preserve hue and chroma exactly.
- Exception: tokens with chroma < 0.03 (near-neutral) use L_dark = L_light (no inversion) to avoid muddy greys.
- Exception: --color-error, --color-warning, --color-success keep original L in dark mode to maintain semantic signal. Apply +0.05 lightness boost to ensure APCA contrast against dark surface (L=0.08).
- Validate all dark variant token pairs against APCA minimums. If any pair fails, adjust by reducing surface lightness by 0.02 (making surface darker) and retry, up to 3 iterations.
- Output: two token maps (light, dark) with validation results.
Phase 5: Gradient Mesh Generation
- Generate linear gradient: primary scale stop 3 to stop 7, 135 degrees.
- Generate conic gradient: 4-stop hue gradient using primary, complementary, analogous +30, analogous -30 at 0/90/180/270 degrees.
- Generate radial gradient: surface center (L+0.1 chroma boost) fading to transparent at 60%.
- Generate gradient mesh: 3x3 grid of color stops interpolated in OKLCH, output as CSS conic-gradient with hard color stops at 45-degree intervals.
- Optimization: if scale has fewer than 5 stops after deduplication, fall back to 2-stop linear gradient. Cache mesh result keyed by seed OKLCH tuple to avoid recomputation on identical inputs.
- Output: four gradient CSS values with direction and color stop arrays.
Phase 6: Texture and Glow Map Generation
- Generate CSS noise overlay: SVG filter using feTurbulence with baseFrequency=0.65, numOctaves=3, output as data URI (max 4 KB).
- Generate grain texture: repeating linear gradient with 8 alternating transparent and semi-opaque stops, opacity 0.03, angle 45 degrees.
- Generate ambient orbital glow: 3 concentric radial gradients at offset positions simulating orbital light sources. Each glow defined by:
  --glow-size: 40% 60% (ellipse)
  --glow-position: center offset by cos/sin of orbital angle
  --glow-color: primary hue at L=0.70, C=0.06, fading to transparent
- All custom properties used in glow system defined in the output:
  --glow-primary: oklch(0.70 0.06 <hue>)
  --glow-secondary: oklch(0.65 0.04 <hue+180>)
  --glow-size-1: 40% 60%
  --glow-size-2: 30% 50%
  --glow-size-3: 20% 30%
  --glow-opacity: 0.15
  --glow-blur: 80px
  --glow-orbit-speed: 20s
- Oversized asset guard: reject any filter or gradient data URI exceeding 8 KB with warning and fallback to solid color.
- Output: texture CSS with inline SVG filter, glow keyframes animation.
Phase 7: Optimization and Deduplication (Inlined into Phase 2)
- No standalone phase 7. All optimization logic lives inside Phase 2 and Phase 4 guards.
- Optimization thresholds applied throughout:
  - Min confidence to generate full scale: 0.8. Below 0.8: output single-token fallback.
  - Max forward-reference resolution hops: 3. Beyond 3 hops: flatten to concrete values.
  - Max delta_E_ok for adjacent stops: 8. Above 8: insert intermediate stops.
  - Min delta_E_ok for deduplication: 2. Below 2: merge stops.
  - Max gradient mesh stops: 12. Above 12: downsample by removing every Nth stop.
  - Max glow data URI size: 8 KB. Above 8 KB: use solid fallback color.
  - Max total CSS output size: 64 KB. Above 64 KB: strip comments and consolidate identical declarations.
Phase 8: Accessibility Checklist
- Reduced motion: wrap all glow animations, orbital keyframes, and noise filter transitions in @media (prefers-reduced-motion: no-preference). Provide static fallback for reduced-motion users.
- Print style overrides: add @media print rule that strips all gradients, glows, and noise overlays. Replaces --color-surface with flat white (#FFFFFF) and --color-text with flat black (#000000) for ink efficiency.
- High-contrast mode: add @media (prefers-contrast: high) overrides. Boost all text token lightness by 0.10 for light mode, reduce by 0.10 for dark mode. Increase --color-border chroma to 0.05 for minimum border visibility. Disable all semi-transparent overlays (set opacity to 1.0 on text backgrounds).
- APCA double-check: re-validate all foreground/background pairs under high-contrast overrides. If any pair falls below Lc > 45, adjust surface lightness by 0.03 steps until passing.
- Focus indicator: ensure --color-focus uses complementary hue at chroma 0.12, lightness 0.50, with 2px solid outline and 4px offset. Guarantee Lc > 60 against any adjacent surface.
Phase 9: Output Assembly and Validation
- Assemble single CSS file with the following section order:
  1. CSS custom properties block (:root and .dark)
  2. Gradient utility classes (.gradient-linear, .gradient-conic, .gradient-radial, .gradient-mesh)
  3. Texture utility classes (.noise-overlay, .grain-overlay, .ambient-glow)
  4. Accessibility overrides block
  5. Print style overrides block
  6. Usage documentation as CSS comments
- Validate output: run all generated token pairs through APCA contrast calculator. Fail build if any body text pair < Lc 45 or small text pair < Lc 60.
- Check for duplicate declarations: scan generated CSS for identical property-value pairs. Collapse duplicates by retaining only the last occurrence per selector. Emit warning count.
- Check total output size: if exceeds 64 KB after deduplication, strip all comments and consolidate by merging shared values into comma-separated selectors.
- Output: final CSS string with validation report.
Mood-to-OKLCH Atmosphere Map
- serene: H=240, C=0.06, L=0.55 (blue-grey tranquility)
- warm: H=30, C=0.12, L=0.60 (amber warmth)
- vibrant: H=340, C=0.16, L=0.55 (magenta energy)
- earthy: H=80, C=0.08, L=0.50 (olive grounding)
- cool: H=200, C=0.10, L=0.60 (cyan freshness)
- dark: H=270, C=0.04, L=0.30 (deep purple shadow)
- neutral: H=0, C=0.01, L=0.50 (achromatic base)
- playful: H=300, C=0.18, L=0.60 (bright purple)
- ocean: H=210, C=0.12, L=0.50 (deep blue)
- sunset: H=20, C=0.15, L=0.55 (orange-gold)
Validation Rules
- All token pairs validated against APCA Lc values, not WCAG 2.1 AA/AAA ratios
- Body text minimum: Lc > 45
- Small text minimum: Lc > 60
- Large text minimum: Lc > 30
- Focus indicator minimum: Lc > 60
- Maximum output CSS size: 64 KB
- Maximum single asset size: 8 KB
- Maximum gradient mesh stops: 12
- Maximum orbital glow count: 3
- Maximum optimization iterations per token pair: 3
Example Output Skeleton (as CSS comment block)
Token definitions follow this pattern:
--color-primary: oklch(0.55 0.12 240);
--color-primary-hover: oklch(0.60 0.13 240);
--color-primary-active: oklch(0.50 0.11 240);
--color-surface: oklch(0.93 0.01 240);
--color-surface-hover: oklch(0.90 0.01 240);
--color-text: oklch(0.08 0.01 240);
--color-text-secondary: oklch(0.25 0.02 240);
--color-border: oklch(0.60 0.01 240);
--color-accent: oklch(0.55 0.12 60);
--color-success: oklch(0.55 0.12 140);
--color-warning: oklch(0.65 0.10 80);
--color-error: oklch(0.50 0.14 25);
--color-info: oklch(0.60 0.08 240);
--color-focus: oklch(0.50 0.12 60);