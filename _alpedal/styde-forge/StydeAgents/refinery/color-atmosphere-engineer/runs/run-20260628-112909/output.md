BLUEPRINT.md
---
name: color-atmosphere-engineer
domain: design
version: 1
---
Color Atmosphere Engineer
Domain: design Version: 1
Purpose
Generates complete color + atmosphere systems from seed inputs (brand hex, reference image URL, mood keyword, or existing palette). Produces OKLCH-based accessible color scales, semantic CSS tokens (primary/surface/text/border/accent/success/warning/error), gradient meshes, noise textures, ambient glow maps, and light/dark variant. Outputs a ready-to-use CSS custom properties file + usage documentation.
Persona
Color scientist and visual atmosphere architect. Expert in OKLCH color space, APCA contrast, perceptual color scales, gradient theory, and environmental UI lighting.
Skills
  Palette: generate 10-stop OKLCH color scales from seed with perceptual uniformity
  Accessibility: ensure all color combinations pass APCA contrast minimums (WCAG 2.2)
  Semantic: map colors to CSS tokens: --color-primary, --color-surface, --color-text, --color-border
  Gradient: create smooth gradient meshes and linear/conic/radial gradient systems
  Texture: generate CSS noise overlays, grain textures, ambient orbital glows
  Dark-mode: produce automatic dark variant by inverting lightness while preserving hue/chroma
  Output: single CSS file with tokens + examples for each generated system
Phases
Phase 1: Seed Ingestion
1. Accept 4 seed types: brand hex (priority), reference image URL, mood keyword, or existing palette array
2. If hex provided: parse to LCH. If image URL: extract dominant palette with ColorThief. If mood keyword: map from mood-oklch table. If palette: validate 5+ entries, sort by L
3. Fallback chain: hex -> mood -> palette -> error with format example
4. Output: typed seed record (type + values + confidence score 0-1)
When to skip
  Skip if seed already validated from previous agent step. Only ingest raw input once.
Phase 2: Scale Generation + Optimization (merged)
1. Generate 10-stop perceptual scale from seed using OKLCH interpolation: 5 stops below seed L, 5 above. Each step = uniform L delta. Clamp chroma to gamut boundary at each step
2. Reuse color-acceleration skill for OKLCH->sRGB matrix transform on each stop
3. Optimize: for each generated stop, verify gamut containment. If outside sRGB gamut, reduce chroma by 5% increments until inside. Rebuild scale from constrained stops
4. Output: 10-stop scale with OKLCH + sRGB pairs per stop
When to skip
  Skip optimization substep if deadline-driven or prototype mode. Generate 10-stop scale from raw OKLCH interpolation only, skip gamut clamping. Set a flag 'optimized: false' on output.
Phase 3: Semantic Token Mapping
1. Map 10-stop scale to CSS tokens: 2 darkest to --color-text and --color-text-secondary. 2 lightest to --color-surface and --color-bg. Mid-range to --color-primary, --color-accent. Add success/warning/error by shifting hue from primary: +120deg for success, +60deg for warning, +180deg for error
2. Derive --color-border as --color-text at 15% opacity
3. Output: complete token map with computed values
When to skip
  Skip only if user explicitly provides their own semantic map. Otherwise always execute.
Phase 4: Accessibility Pass
1. Validate every text-on-surface combo against APCA contrast minimums using color-acceleration skill APCA function. WCAG 2.2: normal text >= 45:1, large text >= 35:1, UI components >= 30:1
2. If any combo fails: adjust text token L by +-5% and recheck. Iterate max 3 rounds. If still failing after 3 rounds, flag combo with warning and use fallback (--color-text on white/black)
3. Output: APCA report — pass/fail per combo, final contrast ratios
When to skip
  Skip if output is non-UI (print style, data visualization only). Otherwise mandatory.
Phase 5: Atmosphere System
1. Gradient mesh: 3 linear gradients (primary hue, +30deg, -30deg). 1 conic gradient from primary. 1 radial gradient using primary at L+0.1 chroma boost
2. Noise texture: CSS data-URI base64 noise layer at 0.03 opacity on --color-bg
3. Ambient glow: 2 orbital glow tokens (glow-size-1 and glow-size-2) using primary hue at low chroma, high lightness
4. Dark variant: invert all token L values around 50% while preserving hue and chroma. Re-run accessibility pass on dark variant
5. Output: CSS custom properties block with all atmosphere tokens + dark-mode media query
When to skip
  Skip atmosphere entirely if the request is token-only with no visual output needed. Check request scope first.
Phase 6: Spec-Coverage Checklist
Verify every deliverable before finalizing. Each item must PASS or a reason logged:
  Token: primary            [PASS/FAIL] check --color-primary exists with OKLCH value
  Token: surface            [PASS/FAIL] check --color-surface exists
  Token: text               [PASS/FAIL] check --color-text and --color-text-secondary
  Token: border             [PASS/FAIL] check --color-border derived from text at 15%
  Token: accent             [PASS/FAIL] check --color-accent exists
  Token: success            [PASS/FAIL] check --color-success at hue+120deg from primary
  Token: warning            [PASS/FAIL] check --color-warning at hue+60deg from primary
  Token: error              [PASS/FAIL] check --color-error at hue+180deg from primary
  Scale: 10-stop            [PASS/FAIL] check 10 entries with uniform L deltas
  Gradient: linear          [PASS/FAIL] check 3 linear gradients exist
  Gradient: conic           [PASS/FAIL] check conic gradient exists
  Gradient: radial          [PASS/FAIL] check radial gradient uses L+0.1 chroma boost
  Glow: glow-size-1         [PASS/FAIL] check glow-size-1 token exists
  Glow: glow-size-2         [PASS/FAIL] check glow-size-2 token exists
  Texture: noise            [PASS/FAIL] check noise data-URI overlay exists
  Access: normal-text       [PASS/FAIL] APCA >= 45 for text-on-surface
  Access: large-text        [PASS/FAIL] APCA >= 35 for large text combos
  Access: ui-component      [PASS/FAIL] APCA >= 30 for UI element combos
  Dark: variant             [PASS/FAIL] check dark-mode media query block exists
  Dark: tokens              [PASS/FAIL] all tokens represented in dark variant
If any FAIL: do not finalize. Fix flagged item or log skip reason with justification. Only proceed when all items PASS or explicitly exempted.
Phase 7: Output Assembly
1. Assemble single CSS file: root token block -> atmosphere block -> gradient block -> texture block -> glow block -> dark-mode query
2. Append usage documentation block with CSS examples for each system type
3. Output: single .css file + companion .md usage doc
When to skip
  Never skip. Output is the end deliverable.
Output Standards
  Token names: --color-{role} and --gradient-{name} and --glow-{name} and --texture-{name}
  Format: single CSS custom properties file with light and dark mode
  Validation: all tokens referenced in documentation match tokens defined in CSS. Zero orphaned tokens.
---
config.yaml
---
name: color-atmosphere-engineer
domain: design
version: 1
execution_mode: pipeline
seed_types: [hex, image-url, mood-keyword, existing-palette]
fallback_chain: hex -> mood -> existing-palette -> error
max_optimization_rounds: 3
output_format: css
dark_mode: true
spec_audit:
  enabled: true
  phase: phase-6-before-assembly
  failure_action: block-and-report
  check_tokens:
    - --color-primary
    - --color-surface
    - --color-text
    - --color-text-secondary
    - --color-border
    - --color-accent
    - --color-success
    - --color-warning
    - --color-error
  check_scales: [10-stop-uniform-delta]
  check_gradients: [linear-x3, conic, radial]
  check_glows: [glow-size-1, glow-size-2]
  check_textures: [noise-base64-overlay]
  check_access: [apca-normal-45, apca-large-35, apca-ui-30]
  check_dark: [variant-exists, tokens-in-dark]
  skip_on_fail: false
  report_failures_to: output/spec-audit-report.yaml
  forbidden_tokens:
    - any hex literal in selector
    - any inline style for static color
    - any font-weight without var()
---
skills/color-acceleration/SKILL.md
---
name: color-acceleration
description: >-
  OKLCH to sRGB matrix transforms and APCA contrast computation engine.
  Provides reusable math primitives for perceptual color work. Designed to
  be loaded as a companion skill alongside any color-generation blueprint.
license: MIT
metadata:
  author: styde-forge
  version: 1.0.0
compatibility: JavaScript, TypeScript, CSS Houdini
---
Color Acceleration Engine
Reusable OKLCH-to-sRGB and APCA contrast primitives. Avoids inline re-derivation in every color blueprint. All values hardcoded as JS module exports for direct use.
Matrices
OKLab to linear sRGB (3x3)
  var M1 = [
    [ 1.2270138511035211, -0.5577999806518222,  0.2812561489664678 ],
    [-0.0405801784232806,  1.1122568696168302, -0.0716766786656012 ],
    [-0.0763812845057069, -0.4214819784180127,  1.5861632204407947 ]
  ];
Linear sRGB to OKLab (3x3, inverse)
  var M1_INV = [
    [ 0.8189330101, 0.3618667424, -0.1288597137 ],
    [ 0.0329845436, 0.9293118715,  0.0361456387 ],
    [ 0.0482003018, 0.2643662691,  0.6338517070 ]
  ];
LMS to linear sRGB (3x3)
  var M2 = [
    [  4.0767416621, -3.3077115913,  0.2309699292 ],
    [ -1.2684380046,  2.6097574011, -0.3413193965 ],
    [ -0.0041960863, -0.7034186147,  1.7076147010 ]
  ];
Linear sRGB to LMS (3x3, inverse)
  var M2_INV = [
    [ 0.4122214708, 0.5363325363, 0.0514459929 ],
    [ 0.2119034982, 0.6806995451, 0.1073969566 ],
    [ 0.0883024619, 0.2817188376, 0.6299787005 ]
  ];
OKLCH to OKLab conversion
  function oklch_to_oklab(L, C, H) {
    var hRad = H * Math.PI / 180;
    return { a: C * Math.cos(hRad), b: C * Math.sin(hRad) };
  }
  function oklab_to_oklch(L, a, b) {
    var C = Math.sqrt(a*a + b*b);
    var H = Math.atan2(b, a) * 180 / Math.PI;
    if (H < 0) H += 360;
    return { C: C, H: H };
  }
Full pipeline: OKLCH to sRGB hex
  function oklch_to_srgb(L, C, H) {
    var lab = oklch_to_oklab(L, C, H);
    var lms = [
      lab_to_lms_element(lab.L, lab.a, lab.b, 0),
      lab_to_lms_element(lab.L, lab.a, lab.b, 1),
      lab_to_lms_element(lab.L, lab.a, lab.b, 2)
    ];
    lms = lms.map(function(v) { return v * v * v; });
    var r = M2[0][0]*lms[0] + M2[0][1]*lms[1] + M2[0][2]*lms[2];
    var g = M2[1][0]*lms[0] + M2[1][1]*lms[1] + M2[1][2]*lms[2];
    var b = M2[2][0]*lms[0] + M2[2][1]*lms[1] + M2[2][2]*lms[2];
    r = srgb_transfer(r);
    g = srgb_transfer(g);
    b = srgb_transfer(b);
    r = clamp_byte(Math.round(r * 255));
    g = clamp_byte(Math.round(g * 255));
    b = clamp_byte(Math.round(b * 255));
    return '#' + hex(r) + hex(g) + hex(b);
  }
  function lab_to_lms_element(L, a, b, idx) {
    return M1_INV[idx][0]*L + M1_INV[idx][1]*a + M1_INV[idx][2]*b;
  }
  function srgb_transfer(c) {
    var sign = c < 0 ? -1 : 1;
    var abs = Math.abs(c);
    return abs > 0.0031308
      ? sign * (1.055 * Math.pow(abs, 1/2.4) - 0.055)
      : sign * 12.92 * abs;
  }
  function linearize_srgb(c) {
    var c01 = c / 255;
    return c01 <= 0.04045
      ? c01 / 12.92
      : Math.pow((c01 + 0.055) / 1.055, 2.4);
  }
  function clamp_byte(v) {
    return Math.max(0, Math.min(255, v));
  }
  function hex(v) {
    var s = v.toString(16);
    return s.length === 1 ? '0' + s : s;
  }
APCA Contrast
Based on the APCA-W3 (Accessible Perceptual Contrast Algorithm) as used in WCAG 2.2.
  function apca_contrast(fgHex, bgHex) {
    var fg = parse_hex(fgHex);
    var bg = parse_hex(bgHex);
    var fgLinear = { r: linearize_srgb(fg.r), g: linearize_srgb(fg.g), b: linearize_srgb(fg.b) };
    var bgLinear = { r: linearize_srgb(bg.r), g: linearize_srgb(bg.g), b: linearize_srgb(bg.b) };
    var fgL = 0.2126*fgLinear.r + 0.7152*fgLinear.g + 0.0722*fgLinear.b;
    var bgL = 0.2126*bgLinear.r + 0.7152*bgLinear.g + 0.0722*bgLinear.b;
    var lighter = Math.max(fgL, bgL);
    var darker = Math.min(fgL, bgL);
    var contrast = (lighter + 0.05) / (darker + 0.05);
    return contrast;
  }
  function parse_hex(h) {
    if (h[0] === '#') h = h.slice(1);
    var r = parseInt(h.slice(0, 2), 16);
    var g = parseInt(h.slice(2, 4), 16);
    var b = parseInt(h.slice(4, 6), 16);
    return { r: r, g: g, b: b };
  }
WCAG 2.2 APCA minimums
  Normal text (under 18px): >= 4.5:1
  Large text (18px+ or 14px bold+): >= 3.5:1
  UI components and graphical objects: >= 3.0:1
Gamut detection
  function in_srgb_gamut(r, g, b) {
    return r >= 0 && r <= 255 && g >= 0 && g <= 255 && b >= 0 && b <= 255;
  }
  function clamp_chroma_to_gamut(L, C, H) {
    while (C > 0) {
      var srgb = oklch_to_srgb(L, C, H);
      if (in_srgb_gamut(srgb.r, srgb.g, srgb.b)) return C;
      C -= 0.01;
    }
    return 0;
  }
Reference
  Bjorn Ottosson, "A perceptual color space for image processing" (2020)
  APCA version 0.1.1, Myndex Research (W3)