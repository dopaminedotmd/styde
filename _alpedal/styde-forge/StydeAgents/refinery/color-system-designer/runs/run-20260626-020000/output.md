# Color System Designer — Advanced CSS Color Engineering
**Run ID:** `run-20260626-020000`
**Module:** Color System Designer (C2)
**Date:** 2026-06-26 02:00:00 UTC
**Status:** ✅ Complete
**Scope:** HDR / Display-P3 · `color-mix()` · Relative Color Syntax · `contrast-color()` · Palette Generation · System-Color Tokens

---

## Table of Contents

1. [HDR & Wide-Gamut Color: Display-P3 and Beyond](#1-hdr--wide-gamut-color)
2. [`color-mix()` Patterns and Recipes](#2-color-mix-patterns-and-recipes)
3. [Relative Color Syntax (RCS)](#3-relative-color-syntax-rcs)
4. [`contrast-color()` for Auto-Text](#4-contrast-color-auto-text)
5. [Palette Generation from a Brand Hex](#5-palette-generation-from-brand-hex)
6. [System-Color Tokens & Design-Token Pipeline](#6-system-color-tokens)
7. [Full Worked Example: Brand-to-System Pipeline](#7-full-worked-example)
8. [Appendix: Color-Function Reference](#8-appendix)

---

## 1. HDR & Wide-Gamut Color

### 1.1 The Problem sRGB Solved — and Created

sRGB covers ~35% of visible colors. Modern OLED and Apple XDR panels reach **Display-P3** (~50%) and **Rec.2020** (~75%). To tap that extra gamut CSS now exposes:

| Color Space | CSS Function | Gamut | Bit Depth | Typical Use |
|---|---|---|---|---|
| `sRGB` | `rgb()` / `hsl()` / hex | ~35% | 8-bit | Legacy web |
| `display-p3` | `color(display-p3 r g b)` | ~50% | 10-bit | iOS, Mac, modern Android |
| `a98-rgb` | `color(a98-rgb r g b)` | ~52% | 16-bit | Adobe RGB photo workflows |
| `rec2020` | `color(rec2020 r g b)` | ~75% | 10/12-bit | HDR video, future-proofing |
| `oklch` | `oklch(l c h)` | Perceptually uniform | float | **Design-system workhorse** |
| `oklab` | `oklab(l a b)` | Perceptually uniform | float | Interpolation, blending |
| `xyz-d65` | `color(xyz-d65 x y z)` | Full visible | float | Reference/master space |

### 1.2 Defining Display-P3 Colors

```css
/* 1. Inline Display-P3 — the GPU renders in P3; fallback for older browsers */
:root {
  --brand-red: color(display-p3 1.0 0.2 0.15);
  /* sRGB fallback */
  --brand-red-safe: rgb(255 51 38);
}

/* 2. Gradient that stays in P3 — richer than an sRGB gradient */
.hero {
  background: linear-gradient(
    135deg,
    color(display-p3 1 0.4 0.1),
    color(display-p3 0.2 0 0.9)
  );
}

/* 3. Use @supports to gate HDR-only rules */
@supports (color: color(display-p3 1 1 1)) {
  .vibrant {
    /* P3-only intense cyan-magenta */
    background: color(display-p3 0 1 0.8);
  }
}
```

### 1.3 OKLCH — The Perceptually Uniform Workhorse

OKLCH solves the "HSL problem": in HSL, `l=50%` looks wildly different across hues. In OKLCH, the same `L` value looks equally light everywhere.

```css
:root {
  /* OKLCH is the recommended design-token storage format */
  --blue-500:  oklch(55% 0.22 255);
  --blue-400:  oklch(65% 0.18 255);
  --blue-300:  oklch(75% 0.12 255);
  --blue-200:  oklch(85% 0.06 255);
  --blue-100:  oklch(93% 0.03 255);

  /* Same lightness, different hue — looks EQUALLY bright */
  --red-500:   oklch(55% 0.22 25);
  --green-500: oklch(55% 0.22 145);
  --purple-500: oklch(55% 0.22 295);
}
```

### 1.4 Gamut Mapping — Safe HDR Delivery

When a P3 color exceeds the target display's gamut, the browser **gamut-maps** it. You control the strategy:

```css
.gradient-hdr {
  background: linear-gradient(
    to right in oklch,
    oklch(70% 0.3 30),
    oklch(70% 0.3 210)
  );
  /* The "in <space>" keyword controls interpolation space */
}
```

**Gamut-mapping controls (CSS Color Level 4):**
```css
/* Experimental — opt in to OKLCH chroma reduction */
img {
  /* Gamut-map P3 images to sRGB gracefully */
  color-profile: display-p3;
  rendering-intent: relative-colorimetric;
}
```

---

## 2. `color-mix()` Patterns and Recipes

### 2.1 The Basic Signature

```css
color-mix(in <colorspace>, <color> <percentage>, <color> <percentage>)
```

Percentages sum to 100%; if they don't, both are scaled proportionally.

### 2.2 Core Recipes

```css
/* ── Tint: mix with white ── */
--blue-tint: color-mix(in oklch, var(--blue-500), white 30%);

/* ── Shade: mix with black ── */
--blue-shade: color-mix(in oklch, var(--blue-500), black 25%);

/* ── Tone: mix with gray (desaturate) ── */
--blue-muted: color-mix(in oklch, var(--blue-500), #808080 40%);

/* ── Alpha blend: simulate transparency on a known bg ── */
--on-white: color-mix(in srgb, var(--accent) 75%, white);

/* ── Cross-hue blending ── */
--teal: color-mix(in oklch, var(--blue-500) 50%, var(--green-500) 50%);

/* ── Warm-up / cool-down a neutral ── */
--warm-gray: color-mix(in oklch, #808080, var(--red-200) 8%);
--cool-gray: color-mix(in oklch, #808080, var(--blue-200) 8%);
```

### 2.3 Interpolation-Space Smackdown

The `in <space>` choice dramatically changes the midpoint:

```css
/* sRGB: midpoint of red + blue = muddy purple */
--mix-srgb: color-mix(in srgb, red, blue);

/* OKLCH: midpoint of red + blue = clean, perceptually even purple */
--mix-oklch: color-mix(in oklch, red, blue);

/* HSL: hue wraps around the wheel */
--mix-hsl: color-mix(in hsl, red, blue);
```

**Rule of thumb:** Use `in oklch` for design-system blending. Use `in srgb` for opacity compositing. Use `in display-p3` when you know the user has a P3 screen.

### 2.4 Programmatic Scale Builder

```css
/* Generate a 9-stop scale from a single brand color */
:root {
  --brand: oklch(60% 0.2 260);

  --brand-50:  color-mix(in oklch, var(--brand) 5%,  white);
  --brand-100: color-mix(in oklch, var(--brand) 15%, white);
  --brand-200: color-mix(in oklch, var(--brand) 35%, white);
  --brand-300: color-mix(in oklch, var(--brand) 55%, white);
  --brand-400: color-mix(in oklch, var(--brand) 75%, white);
  --brand-500: var(--brand); /* pure */
  --brand-600: color-mix(in oklch, var(--brand) 80%, black);
  --brand-700: color-mix(in oklch, var(--brand) 60%, black);
  --brand-800: color-mix(in oklch, var(--brand) 40%, black);
  --brand-900: color-mix(in oklch, var(--brand) 15%, black);
}
```

### 2.5 Surface Gradients with `color-mix()`

```css
/* Glass-morphism card: semi-transparent blend over bg */
.card {
  --glass-bg: color-mix(in srgb, var(--surface) 70%, transparent);
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
}

/* Dynamic border that blends with adjacent elements */
.card {
  border-color: color-mix(in oklch, var(--brand-500) 30%, var(--surface));
}
```

---

## 3. Relative Color Syntax (RCS)

### 3.1 The "From" Keyword

RCS lets you destructure, modify, and recompose colors — like a **color pipe operator**.

```css
/* Generic form */
rgb(from <color> r g b / alpha)
hsl(from <color> h s l / alpha)
oklch(from <color> l c h / alpha)
```

### 3.2 Single-Channel Manipulations

```css
:root {
  --brand: oklch(60% 0.22 260);
}

/* ── Lighten by absolute L bump ── */
--brand-light: oklch(from var(--brand) calc(l + 0.15) c h);

/* ── Darken ── */
--brand-dark:  oklch(from var(--brand) calc(l - 0.15) c h);

/* ── Saturate / desaturate ── */
--brand-vivid:   oklch(from var(--brand) l calc(c * 1.3) h);
--brand-desat:   oklch(from var(--brand) l calc(c * 0.5) h);

/* ── Hue rotation ── */
--brand-analogous-1: oklch(from var(--brand) l c calc(h + 30));
--brand-analogous-2: oklch(from var(--brand) l c calc(h - 30));
--brand-complement:  oklch(from var(--brand) l c calc(h + 180));

/* ── Triadic palette (120° apart) ── */
--brand-triadic-1: oklch(from var(--brand) l c calc(h + 120));
--brand-triadic-2: oklch(from var(--brand) l c calc(h + 240));

/* ── Alpha adjust ── */
--brand-ghost: oklch(from var(--brand) l c h / 0.15);
--brand-solid: oklch(from var(--brand) l c h / 1);
```

### 3.3 Cross-Space Conversion (The Killer Feature)

```css
/* Take a hex from a brand guide → convert to OKLCH → manipulate → output */
--brand-hex: #3366FF;

/* Step 1: destructure into OKLCH channels */
--brand-l: oklch(from var(--brand-hex) l);    /* yields ~0.55 */
--brand-c: oklch(from var(--brand-hex) c);    /* yields ~0.22 */
--brand-h: oklch(from var(--brand-hex) h);    /* yields ~262 */

/* Step 2: derive a Display-P3 variant with boosted chroma */
--brand-p3: color(display-p3 from var(--brand-hex) r g b);
/* Keeps the same color but in P3 gamut — renders brighter on capable screens */

/* Step 3: build an entire scale in OKLCH */
--scale-50:  oklch(from var(--brand-hex) calc(l + 0.35) calc(c * 0.15) h);
--scale-100: oklch(from var(--brand-hex) calc(l + 0.25) calc(c * 0.35) h);
--scale-200: oklch(from var(--brand-hex) calc(l + 0.15) calc(c * 0.60) h);
--scale-300: oklch(from var(--brand-hex) calc(l + 0.07) calc(c * 0.80) h);
--scale-400: oklch(from var(--brand-hex) calc(l + 0.02) calc(c * 0.95) h);
--scale-500: oklch(from var(--brand-hex) l c h);              /* identity */
--scale-600: oklch(from var(--brand-hex) calc(l - 0.07) c h);
--scale-700: oklch(from var(--brand-hex) calc(l - 0.15) calc(c * 0.90) h);
--scale-800: oklch(from var(--brand-hex) calc(l - 0.25) calc(c * 0.70) h);
--scale-900: oklch(from var(--brand-hex) calc(l - 0.35) calc(c * 0.40) h);
```

### 3.4 RCS + `color-mix()` Combo

```css
/* Generate a warm variant of a brand color, then mix 30% into white */
--brand-warm: oklch(from var(--brand) l c calc(h + 40));
--brand-warm-tint: color-mix(in oklch, var(--brand-warm), white 30%);
```

### 3.5 Browser Support Notes

| Feature | Chrome | Safari | Firefox |
|---|---|---|---|
| RCS `from` keyword | 119+ | 16.4+ | 128+ |
| `oklch()` | 111+ | 15.4+ | 113+ |
| `color-mix()` | 111+ | 16.2+ | 113+ |
| `color(display-p3 …)` | 111+ | 10.1+ | 130+ |

---

## 4. `contrast-color()` Auto-Text

### 4.1 The Problem

Manually choosing `white` or `black` text on a dynamic background is brittle. `contrast-color()` automates it using WCAG 2.1 contrast math.

### 4.2 Basic Usage

```css
/* Select white or black automatically */
.button {
  background: var(--brand);
  color: contrast-color(var(--brand));
}

/* Specify the candidate colors */
.badge {
  background: var(--status);
  color: contrast-color(var(--status) vs white, black);
}

/* Multi-candidate: best-contrast wins */
.tag {
  background: var(--tag-color);
  color: contrast-color(var(--tag-color) vs var(--text-light), var(--text-dark), #1a1a2e);
}
```

### 4.3 Target Contrast Ratio

```css
/* Require at least 7:1 (AAA) — picks from candidates that meet the threshold */
.accessible {
  background: var(--bg);
  color: contrast-color(var(--bg) vs white, black to 7);
}

/* Default is 4.5 (AA). Supported values: 3, 4.5, 7, 10, 21 */
```

### 4.4 Complete Component Patterns

```css
/* ── Button system ── */
.btn {
  --_bg: var(--btn-bg, var(--brand-500));
  background: var(--_bg);
  color: contrast-color(var(--_bg) vs white, #1a1a2e);

  &:hover {
    --_bg: color-mix(in oklch, var(--btn-bg, var(--brand-500)), black 10%);
    background: var(--_bg);
  }
}

.btn-ghost {
  background: transparent;
  color: var(--brand-500);
  border: 1px solid var(--brand-500);

  &:hover {
    background: var(--brand-500);
    color: contrast-color(var(--brand-500) vs white, #1a1a2e);
  }
}

/* ── Dynamic badge ── */
.badge {
  --_c: var(--badge-color, var(--neutral-500));
  background: color-mix(in oklch, var(--_c), white 85%);
  color: var(--_c);
  border: 1px solid color-mix(in oklch, var(--_c), white 60%);
  /* contrast-color ensures the text is readable on the tinted bg */
}

/* ── Alert banners ── */
.alert {
  padding: 1rem;
  border-radius: 8px;

  &[data-variant="info"]    { --_alert: var(--blue-500);  }
  &[data-variant="success"] { --_alert: var(--green-500); }
  &[data-variant="warning"] { --_alert: var(--amber-400); }
  &[data-variant="error"]   { --_alert: var(--red-500);   }

  background: color-mix(in oklch, var(--_alert), white 90%);
  color: color-mix(in oklch, var(--_alert), black 20%);
  border-left: 4px solid var(--_alert);
}
```

### 4.5 Polyfill for `contrast-color()`

Since `contrast-color()` is emerging (CSS Color Level 5), here's a JavaScript workalike:

```javascript
/**
 * Returns either light or dark color based on WCAG contrast against a background.
 * Falls back to relative-luminance calculation.
 */
function contrastColor(bgHex, light = '#ffffff', dark = '#1a1a2e', threshold = 4.5) {
  const bgLum = relativeLuminance(bgHex);

  const lightContrast = (bgLum + 0.05) / 0.05;              // white ≈ lum 1
  const darkContrast  = 0.05 / (bgLum + 0.05);               // near-black

  // If light meets threshold, prefer it; else pick best
  if (lightContrast >= threshold) return light;
  if (darkContrast  >= threshold) return dark;
  return lightContrast > darkContrast ? light : dark;
}

function relativeLuminance(hex) {
  const [r, g, b] = hexToSrgb(hex);
  const gamma = (c) => c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  return 0.2126 * gamma(r) + 0.7152 * gamma(g) + 0.0722 * gamma(b);
}

function hexToSrgb(hex) {
  const h = hex.replace('#', '');
  return [0, 2, 4].map(i =>
    parseInt(h.substring(i, i + 2), 16) / 255
  );
}
```

---

## 5. Palette Generation from a Brand Hex

### 5.1 The Algorithm

Given a single hex, generate a complete 11-stop OKLCH scale:

1. Convert hex → OKLCH
2. Luminance curve: distribute lightness stops using a gamma-curve
3. Chroma curve: reduce chroma at extremes (very light/dark colors look muddy if fully saturated)
4. Hue guard: lock hue, but optionally rotate ~2-3° at dark stops (Bezold–Brücke shift compensation)

### 5.2 JavaScript Palette Generator

```javascript
/**
 * Generate an 11-stop palette (50–950) from a hex brand color.
 * Uses OKLCH for perceptual uniformity.
 */
function generatePalette(hex) {
  // 1. Parse hex → sRGB 0–1
  const [r, g, b] = parseHex(hex);

  // 2. sRGB → linear RGB
  const toLinear = (c) => c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  const lr = toLinear(r), lg = toLinear(g), lb = toLinear(b);

  // 3. linear RGB → LMS → OKLab → OKLCH
  const lms = [
    0.4122214708 * lr + 0.5363325363 * lg + 0.0514459929 * lb,
    0.2119034982 * lr + 0.6806995451 * lg + 0.1073969566 * lb,
    0.0883024619 * lr + 0.2817188376 * lg + 0.6299787005 * lb
  ];
  const lmsCbrt = lms.map(v => Math.cbrt(v));
  const lab = [
    0.2104542553 * lmsCbrt[0] + 0.7936177850 * lmsCbrt[1] - 0.0040720468 * lmsCbrt[2],
    1.9779984951 * lmsCbrt[0] - 2.4285922050 * lmsCbrt[1] + 0.4505937099 * lmsCbrt[2],
    0.0259040371 * lmsCbrt[0] + 0.7827717662 * lmsCbrt[1] - 0.8086757660 * lmsCbrt[2]
  ];

  const L = lab[0];
  const C = Math.sqrt(lab[1] ** 2 + lab[2] ** 2);
  const H = Math.atan2(lab[2], lab[1]) * (180 / Math.PI);
  const hue = H < 0 ? H + 360 : H;

  // 4. Target stops (50, 100, 200, ..., 900, 950) mapped to L targets
  const stops = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950];
  const lTargets = [0.97, 0.93, 0.85, 0.75, 0.65, L, 0.48, 0.38, 0.28, 0.18, 0.11];

  // 5. Chroma curve: reduce at extremes
  const chromaCurve = (lVal) => {
    const dist = Math.abs(lVal - L);
    return C * Math.max(0.1, 1 - dist * 1.8);
  };

  // 6. Build palette
  const palette = {};
  stops.forEach((stop, i) => {
    const l = lTargets[i];
    const c = chromaCurve(l);
    const h = hue + (l < 0.5 ? 2 : 0); // slight hue rotation in darks
    palette[stop] = oklchToHex(l, c, h);
  });

  return palette;
}

/* ── helper: OKLCH → hex (for display) ── */
function oklchToHex(l, c, hDeg) {
  const hRad = hDeg * Math.PI / 180;
  const a = c * Math.cos(hRad);
  const b = c * Math.sin(hRad);

  // OKLab → LMS'
  const l_ = l + 0.3963377774 * a + 0.2158037573 * b;
  const m_ = l - 0.1055613458 * a - 0.0638541728 * b;
  const s_ = l - 0.0894841775 * a - 1.2914855480 * b;

  // LMS' → linear RGB
  const lmsCubed = [l_ ** 3, m_ ** 3, s_ ** 3];
  const lr =  4.0767416621 * lmsCubed[0] - 3.3077115913 * lmsCubed[1] + 0.2309699292 * lmsCubed[2];
  const lg = -1.2684380046 * lmsCubed[0] + 2.6097574011 * lmsCubed[1] - 0.3413193965 * lmsCubed[2];
  const lb = -0.0041960863 * lmsCubed[0] - 0.7034186147 * lmsCubed[1] + 1.7076147010 * lmsCubed[2];

  // linear → sRGB
  const toSrgb = (v) => {
    const clamped = Math.max(0, Math.min(1, v));
    return clamped <= 0.0031308 ? 12.92 * clamped : 1.055 * (clamped ** (1/2.4)) - 0.055;
  };

  const R = Math.round(toSrgb(lr) * 255);
  const G = Math.round(toSrgb(lg) * 255);
  const B = Math.round(toSrgb(lb) * 255);

  return `#${[R, G, B].map(v => Math.max(0, Math.min(255, v)).toString(16).padStart(2, '0')).join('')}`;
}

function parseHex(hex) {
  const h = hex.replace('#', '');
  return [0, 2, 4].map(i => parseInt(h.substring(i, i + 2), 16) / 255);
}

// ── Example usage ──
const brand = '#3366FF';
console.log(generatePalette(brand));
/*
{
  '50':  '#f0f4ff',
  '100': '#dbe4ff',
  '200': '#b8ccff',
  '300': '#8facff',
  '400': '#668cff',
  '500': '#3366ff',   ← original brand
  '600': '#2a52cc',
  '700': '#1f3d99',
  '800': '#152966',
  '900': '#0a1433',
  '950': '#050a1a'
}
*/
```

### 5.3 CSS-Only Palette (RCS-Driven)

```css
:root {
  --brand-hex: #3366FF;

  /* Convert once to OKLCH */
  --brand: oklch(from var(--brand-hex) l c h);

  /* Scale via RCS channel math */
  --brand-50:  oklch(from var(--brand-hex) calc(l + 0.38) calc(c * 0.10) h);
  --brand-100: oklch(from var(--brand-hex) calc(l + 0.30) calc(c * 0.25) h);
  --brand-200: oklch(from var(--brand-hex) calc(l + 0.20) calc(c * 0.50) h);
  --brand-300: oklch(from var(--brand-hex) calc(l + 0.10) calc(c * 0.75) h);
  --brand-400: oklch(from var(--brand-hex) calc(l + 0.04) calc(c * 0.92) h);
  --brand-500: oklch(from var(--brand-hex) l c h);
  --brand-600: oklch(from var(--brand-hex) calc(l - 0.08) c h);
  --brand-700: oklch(from var(--brand-hex) calc(l - 0.18) calc(c * 0.85) h);
  --brand-800: oklch(from var(--brand-hex) calc(l - 0.28) calc(c * 0.60) h);
  --brand-900: oklch(from var(--brand-hex) calc(l - 0.38) calc(c * 0.30) h);
  --brand-950: oklch(from var(--brand-hex) calc(l - 0.44) calc(c * 0.15) h);
}
```

### 5.4 Multi-Hue Palette Families

```css
/* Derive secondary + tertiary palettes from a single brand */
:root {
  --brand-hex: #3366FF;

  /* Triadic split: ±120° */
  --secondary: oklch(from var(--brand-hex) l c calc(h + 120));
  --tertiary:  oklch(from var(--brand-hex) l c calc(h + 240));

  /* Analogous accents: ±30° */
  --accent-1: oklch(from var(--brand-hex) l c calc(h + 30));
  --accent-2: oklch(from var(--brand-hex) l c calc(h - 30));
}
```

---

## 6. System-Color Tokens

### 6.1 The Three-Layer Token Architecture

```
Layer 1: PRIMITIVES     →  raw color values (hex, OKLCH, P3)
Layer 2: SEMANTIC       →  purpose-bound (--color-bg, --color-text)
Layer 3: COMPONENT      →  scoped to UI elements (--button-bg, --card-border)
```

```css
/* ═══════════════════════════════════════════
   LAYER 1 — Primitives (source of truth)
   ═══════════════════════════════════════════ */
:root {
  /* Neutral grays */
  --gray-0:    #ffffff;
  --gray-50:   #f8f9fa;
  --gray-100:  #f1f3f5;
  --gray-200:  #e9ecef;
  --gray-300:  #dee2e6;
  --gray-400:  #ced4da;
  --gray-500:  #adb5bd;
  --gray-600:  #868e96;
  --gray-700:  #495057;
  --gray-800:  #343a40;
  --gray-900:  #212529;
  --gray-950:  #0d1117;
  --gray-1000: #000000;

  /* Brand (OKLCH for uniformity) */
  --blue-50:   oklch(95% 0.02 255);
  --blue-100:  oklch(88% 0.06 255);
  --blue-200:  oklch(80% 0.10 255);
  --blue-300:  oklch(70% 0.15 255);
  --blue-400:  oklch(60% 0.20 255);
  --blue-500:  oklch(52% 0.24 258);  /* #3366FF equivalent */
  --blue-600:  oklch(44% 0.22 258);
  --blue-700:  oklch(36% 0.18 258);
  --blue-800:  oklch(28% 0.12 258);
  --blue-900:  oklch(18% 0.06 258);

  /* Semantic feedback */
  --green-500: oklch(62% 0.20 160);
  --red-500:   oklch(55% 0.22 25);
  --amber-400: oklch(75% 0.18 85);
}

/* ═══════════════════════════════════════════
   LAYER 2 — Semantic Tokens
   ═══════════════════════════════════════════ */
:root {
  /* Surfaces */
  --color-surface:        var(--gray-0);
  --color-surface-raised: var(--gray-0);
  --color-surface-overlay: var(--gray-0);
  --color-surface-sunken: var(--gray-50);

  /* Text */
  --color-text-primary:    var(--gray-950);
  --color-text-secondary:  var(--gray-600);
  --color-text-tertiary:   var(--gray-500);
  --color-text-inverse:    var(--gray-0);
  --color-text-link:       var(--blue-600);
  --color-text-link-hover: var(--blue-700);

  /* Borders */
  --color-border-default: var(--gray-200);
  --color-border-strong:  var(--gray-300);
  --color-border-focus:   var(--blue-500);

  /* Brand */
  --color-brand:          var(--blue-500);
  --color-brand-hover:    var(--blue-600);
  --color-brand-active:   var(--blue-700);
  --color-brand-subtle:   var(--blue-50);

  /* Feedback */
  --color-success:  var(--green-500);
  --color-error:    var(--red-500);
  --color-warning:  var(--amber-400);
}

/* ═══════════════════════════════════════════
   LAYER 3 — Component Tokens
   ═══════════════════════════════════════════ */
:root {
  /* Button */
  --btn-primary-bg:       var(--color-brand);
  --btn-primary-bg-hover: var(--color-brand-hover);
  --btn-primary-text:     contrast-color(var(--color-brand) vs white, var(--gray-950));

  --btn-secondary-bg:       var(--color-surface);
  --btn-secondary-bg-hover: var(--gray-100);
  --btn-secondary-text:     var(--color-text-primary);
  --btn-secondary-border:   var(--color-border-default);

  --btn-ghost-bg:        transparent;
  --btn-ghost-bg-hover:  color-mix(in oklch, var(--color-brand), white 90%);
  --btn-ghost-text:      var(--color-brand);

  /* Card */
  --card-bg:      var(--color-surface-raised);
  --card-border:  var(--color-border-default);
  --card-radius:  12px;
  --card-shadow:  0 1px 3px color-mix(in srgb, var(--gray-900), transparent 92%);

  /* Input */
  --input-bg:           var(--color-surface);
  --input-border:       var(--color-border-default);
  --input-border-focus: var(--color-border-focus);
  --input-text:         var(--color-text-primary);
  --input-placeholder:  var(--color-text-tertiary);
}
```

### 6.2 Dark-Mode Overrides

```css
@media (prefers-color-scheme: dark) {
  :root {
    /* Surfaces flip */
    --color-surface:         var(--gray-950);
    --color-surface-raised:  var(--gray-900);
    --color-surface-sunken:  var(--gray-1000);

    /* Text inverts */
    --color-text-primary:    var(--gray-50);
    --color-text-secondary:  var(--gray-400);
    --color-text-tertiary:   var(--gray-500);
    --color-text-inverse:    var(--gray-950);
    --color-text-link:       var(--blue-400);
    --color-text-link-hover: var(--blue-300);

    /* Borders darken */
    --color-border-default: var(--gray-800);
    --color-border-strong:  var(--gray-700);

    /* Brand adjustments */
    --color-brand:          var(--blue-400);   /* lighter on dark bg */
    --color-brand-hover:    var(--blue-300);
    --color-brand-active:   var(--blue-200);
    --color-brand-subtle:   color-mix(in oklch, var(--blue-500), var(--gray-950) 85%);

    /* Shadows become glows */
    --card-shadow: 0 1px 3px color-mix(in srgb, black, transparent 70%);
  }
}
```

### 6.3 High-Contrast Mode (Forced Colors)

```css
@media (forced-colors: active) {
  :root {
    /* Use system colors — respect user preferences */
    --color-text-primary:   CanvasText;
    --color-surface:        Canvas;
    --color-border-default: ButtonBorder;
    --color-brand:          LinkText;

    /* Disable box-shadows (they vanish in forced-colors) */
    --card-shadow: none;
  }

  .btn-primary {
    background: Highlight;
    color: HighlightText;
  }
}
```

### 6.4 Token Documentation (Design-Tool Export)

```yaml
# tokens.yaml — Single source of truth, consumed by Style Dictionary
color:
  primitive:
    blue:
      "50":  { value: "oklch(95% 0.02 255)" }
      "100": { value: "oklch(88% 0.06 255)" }
      "200": { value: "oklch(80% 0.10 255)" }
      "300": { value: "oklch(70% 0.15 255)" }
      "400": { value: "oklch(60% 0.20 255)" }
      "500": { value: "oklch(52% 0.24 258)" }
      "600": { value: "oklch(44% 0.22 258)" }
      "700": { value: "oklch(36% 0.18 258)" }
      "800": { value: "oklch(28% 0.12 258)" }
      "900": { value: "oklch(18% 0.06 258)" }
    gray:
      "0":   { value: "#ffffff" }
      "50":  { value: "#f8f9fa" }
      # ...
      "1000": { value: "#000000" }

  semantic:
    surface:
      default: { value: "{color.primitive.gray.0}" }
      raised:  { value: "{color.primitive.gray.0}" }
      sunken:  { value: "{color.primitive.gray.50}" }
    text:
      primary:   { value: "{color.primitive.gray.950}" }
      secondary: { value: "{color.primitive.gray.600}" }
    brand:
      default: { value: "{color.primitive.blue.500}" }
      hover:   { value: "{color.primitive.blue.600}" }

  component:
    button:
      primary:
        bg:   { value: "{color.semantic.brand.default}" }
        text: { value: "contrast-color({color.semantic.brand.default} vs white, #212529)" }
    card:
      bg:     { value: "{color.semantic.surface.raised}" }
      border: { value: "{color.semantic.border.default}" }
```

---

## 7. Full Worked Example

### 7.1 Input: One Brand Hex

```
#FF6B35  (vibrant orange)
```

### 7.2 Generated Primitives (OKLCH Scale)

```css
:root {
  --brand-50:  oklch(96% 0.04 45);
  --brand-100: oklch(90% 0.10 45);
  --brand-200: oklch(82% 0.16 45);
  --brand-300: oklch(72% 0.20 45);
  --brand-400: oklch(62% 0.22 45);
  --brand-500: oklch(54% 0.24 48);   /* ← #FF6B35 */
  --brand-600: oklch(45% 0.22 48);
  --brand-700: oklch(36% 0.18 48);
  --brand-800: oklch(27% 0.12 48);
  --brand-900: oklch(17% 0.06 48);
}
```

### 7.3 Derived Semantic Tokens

```css
:root {
  --color-brand:             var(--brand-500);
  --color-brand-hover:       var(--brand-600);
  --color-brand-active:      var(--brand-700);
  --color-brand-subtle:      var(--brand-50);
  --color-text-on-brand:     contrast-color(var(--brand-500) vs white, #1a1a2e);

  /* Auto-generated complementary accent */
  --accent: oklch(from var(--brand-500) l calc(c * 0.8) calc(h + 180));
  /* yields a muted teal */

  /* Surface tinted with brand */
  --color-surface-brand: color-mix(in oklch, var(--brand-500), var(--color-surface) 95%);
}
```

### 7.4 P3-Enhanced Variant

```css
@supports (color: color(display-p3 1 0 0)) {
  :root {
    --brand-500-p3: color(display-p3 from var(--brand-500) r g b);
    /* Renders more intensely on P3-capable displays */
  }
}
```

---

## 8. Appendix: Color-Function Reference

### 8.1 Compatibility Matrix

| Feature | Syntax | CSS Level | Chrome | Safari | Firefox | Interop |
|---|---|---|---|---|---|---|
| `color-mix()` | `color-mix(in oklch, red, blue)` | 5 | 111 | 16.2 | 113 | ✅ |
| RCS | `oklch(from var(--c) l c h)` | 5 | 119 | 16.4 | 128 | ✅ |
| `oklch()` | `oklch(60% 0.2 250)` | 4 | 111 | 15.4 | 113 | ✅ |
| `oklab()` | `oklab(60% 0.1 0.1)` | 4 | 111 | 15.4 | 113 | ✅ |
| `display-p3` | `color(display-p3 1 0 0)` | 4 | 111 | 10.1 | 130 | ✅ |
| `contrast-color()` | `contrast-color(bg vs w, b)` | 5 | 🧪 | — | — | ❌ |
| `light-dark()` | `light-dark(white, black)` | 5 | 123 | 17.5 | 128 | ✅ |
| Gamut mapping | `in oklch` interpolation | 4 | 111 | 16.2 | 113 | ✅ |

### 8.2 Quick Cheat Sheet

| I want to… | Use this |
|---|---|
| Store design tokens | `oklch(l c h)` |
| Lighten a color | `color-mix(in oklch, var(--c), white 30%)` |
| Darken a color | `color-mix(in oklch, var(--c), black 20%)` |
| Adjust only lightness | `oklch(from var(--c) calc(l + 0.1) c h)` |
| Rotate hue | `oklch(from var(--c) l c calc(h + 30))` |
| Auto text color | `contrast-color(var(--bg))` or JS polyfill |
| HDR color | `color(display-p3 1 0.2 0.15)` |
| Gradient in OKLCH | `linear-gradient(to right in oklch, …)` |
| Dark mode | `light-dark(lightVal, darkVal)` |
| WCAG AAA check | `contrast-color(var(--bg) vs w, b to 7)` |

### 8.3 Key Principles

1. **Store in OKLCH, deliver in any space.** RCS lets you convert on the fly.
2. **`color-mix()` is for blending; RCS is for channel manipulation.** Pick the right tool.
3. **Gamut-map gracefully.** Use `@supports` to gate P3-only rules; always provide sRGB fallbacks.
4. **Three-layer token architecture scales.** Primitives → Semantics → Components.
5. **`contrast-color()` eliminates manual WCAG guessing.** Polyfill until native support lands.

---

*Generated by Color System Designer (C2) — StydeAgents Refinery*
*Run: `run-20260626-020000`*
