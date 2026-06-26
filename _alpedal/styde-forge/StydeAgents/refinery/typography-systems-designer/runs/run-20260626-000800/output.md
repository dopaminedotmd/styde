# Typography System — Stryde Forge

> **Generated:** 2026-06-26 00:08:00  
> **Designer:** Typography Systems Designer Agent  
> **Scale Ratio:** 1.25 (Major Third)  
> **Base Size:** 16px / 1rem  
> **Baseline Grid:** 4px unit (6 units per line = 24px base line-height)

---

## Table of Contents

1. [Design Rationale](#1-design-rationale)
2. [Font Pairing](#2-font-pairing)
3. [Modular Type Scale](#3-modular-type-scale)
4. [Variable Font Configuration](#4-variable-font-configuration)
5. [Vertical Rhythm & Baseline Grid](#5-vertical-rhythm--baseline-grid)
6. [Responsive Type with clamp()](#6-responsive-type-with-clamp)
7. [Complete CSS Design Tokens](#7-complete-css-design-tokens)
8. [Usage Examples](#8-usage-examples)
9. [Accessibility Notes](#9-accessibility-notes)

---

## 1. Design Rationale

### Why 1.25 (Major Third)?

The major third ratio (5:4) produces a type scale that is:

- **Musically harmonious** — derived from the 5:4 frequency ratio in just intonation
- **Visibly distinct** — each step is clearly larger than the last without being jarring
- **Practical** — yields clean pixel values at standard base sizes (16px → 20 → 25 → 31.25)
- **Web-native** — pairs naturally with `rem` units and clamp-based fluid sizing

### Why These Fonts?

| Role | Font | Rationale |
|------|------|-----------|
| **Display** | Fraunces | Variable serif with optical sizing, soft wedge serifs, works at large sizes and in text. Weight axis 100–900, plus Softness (SOFT) axis for warmth. |
| **Body** | Inter | Variable sans-serif optimized for screen legibility at small sizes. Weight axis 100–900. Excellent x-height. |
| **Mono** | JetBrains Mono | Variable monospace with coding ligatures. Weight axis 100–800. Tall x-height, distinct letterforms. |

### Font Stack Strategy

Every stack includes a critical-fallback pair and a generic family:

```
Display: 'Fraunces', 'Georgia', 'Times New Roman', serif
Body:    'Inter', 'system-ui', '-apple-system', 'Segoe UI', sans-serif
Mono:    'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace
```

---

## 2. Font Pairing

### 2.1 The Pairing

```
┌──────────────────────────────────────┐
│  DISPLAY — Fraunces (Variable Serif) │
│  • Headings h1–h3                    │
│  • Hero text                         │
│  • Pull quotes                       │
│  • Large numerals                    │
├──────────────────────────────────────┤
│  BODY — Inter (Variable Sans)        │
│  • Body copy                         │
│  • UI labels                         │
│  • Navigation                        │
│  • h4–h6 (sans-serif hierarchy)      │
├──────────────────────────────────────┤
│  MONO — JetBrains Mono (Variable)    │
│  • Code blocks                       │
│  • Inline code                       │
│  • Data tables                       │
│  • Technical specifications          │
└──────────────────────────────────────┘
```

### 2.2 Pairing Principles

1. **Contrast with purpose** — Serif display commands attention; sans body maximizes readability; mono signals "machine/math."
2. **Shared proportions** — All three have generous x-heights, making mixed-line usage coherent.
3. **Variable-first** — All three are variable fonts, enabling fine-tuned weight control without FOUT from multiple static files.
4. **Optical sizing** — Fraunces supports the `opsz` axis, automatically adjusting contrast and spacing for the rendered size.

### 2.3 @font-face Declarations

```css
/* Display — Fraunces (variable, 2 files: roman + italic) */
@font-face {
  font-family: 'Fraunces';
  src: url('/fonts/fraunces.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-stretch: 100% 120%;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Fraunces';
  src: url('/fonts/fraunces-italic.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-stretch: 100% 120%;
  font-style: italic;
  font-display: swap;
}

/* Body — Inter (variable, 2 files: roman + italic) */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-italic.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-style: italic;
  font-display: swap;
}

/* Mono — JetBrains Mono (variable, 2 files: roman + italic) */
@font-face {
  font-family: 'JetBrains Mono';
  src: url('/fonts/jetbrains-mono.woff2') format('woff2-variations');
  font-weight: 100 800;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'JetBrains Mono';
  src: url('/fonts/jetbrains-mono-italic.woff2') format('woff2-variations');
  font-weight: 100 800;
  font-style: italic;
  font-display: swap;
}
```

### 2.4 Google Fonts CDN Alternative

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,100..900,0..100;1,9..144,100..900,0..100&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap" rel="stylesheet">
```

---

## 3. Modular Type Scale

### 3.1 Scale Computation

**Base:** 16px (1rem) · **Ratio:** 1.25 (5/4)

| Step | Formula | px Value | rem Value | Name | Use |
|------|---------|----------|-----------|------|-----|
| -2 | 16 ÷ 1.25² | 10.24 | 0.64 | `--text-xs` | Fine print, captions |
| -1 | 16 ÷ 1.25 | 12.80 | 0.80 | `--text-sm` | Small body, labels |
| 0 | 16 × 1.25⁰ | 16.00 | 1.00 | `--text-base` | Body, paragraph |
| 1 | 16 × 1.25 | 20.00 | 1.25 | `--text-lg` | Lead, intro text |
| 2 | 16 × 1.25² | 25.00 | 1.563 | `--text-xl` | h4, card titles |
| 3 | 16 × 1.25³ | 31.25 | 1.953 | `--text-2xl` | h3, section heads |
| 4 | 16 × 1.25⁴ | 39.06 | 2.441 | `--text-3xl` | h2, page heads |
| 5 | 16 × 1.25⁵ | 48.83 | 3.052 | `--text-4xl` | h1, hero secondary |
| 6 | 16 × 1.25⁶ | 61.04 | 3.815 | `--text-5xl` | h1 hero primary |
| 7 | 16 × 1.25⁷ | 76.29 | 4.768 | `--text-6xl` | Super display |
| 8 | 16 × 1.25⁸ | 95.37 | 5.960 | `--text-7xl` | Mega display |

### 3.2 Scale Visual Reference

```
 95px ████████████████████████████████████████████████  --text-7xl
 76px ████████████████████████████████████████          --text-6xl
 61px ████████████████████████████████                  --text-5xl
 49px ████████████████████████████                      --text-4xl
 39px ████████████████████████                          --text-3xl
 31px ████████████████████                              --text-2xl
 25px ████████████████                                  --text-xl
 20px ████████████                                      --text-lg
 16px ██████████                                        --text-base
 13px ████████                                          --text-sm
 10px ██████                                            --text-xs
```

### 3.3 Line-Height Pairing

Each scale step receives a line-height that snaps to the 4px baseline grid:

| Step | fontSize (px) | line-height (px) | lh unitless | lh in rem | Baseline units |
|------|---------------|-------------------|-------------|-----------|----------------|
| xs | 10.24 | 16 | 1.5625 | 1.0 | 4 |
| sm | 12.80 | 20 | 1.5625 | 1.25 | 5 |
| base | 16.00 | 24 | 1.5 | 1.5 | 6 |
| lg | 20.00 | 28 | 1.4 | 1.75 | 7 |
| xl | 25.00 | 32 | 1.28 | 2.0 | 8 |
| 2xl | 31.25 | 40 | 1.28 | 2.5 | 10 |
| 3xl | 39.06 | 48 | 1.229 | 3.0 | 12 |
| 4xl | 48.83 | 56 | 1.147 | 3.5 | 14 |
| 5xl | 61.04 | 68 | 1.114 | 4.25 | 17 |
| 6xl | 76.29 | 84 | 1.101 | 5.25 | 21 |
| 7xl | 95.37 | 104 | 1.090 | 6.5 | 26 |

---

## 4. Variable Font Configuration

### 4.1 Available Axes

#### Fraunces (Display)

| Axis | Tag | Range | Description |
|------|-----|-------|-------------|
| Weight | `wght` | 100–900 | Thin (100) to Black (900) |
| Optical Size | `opsz` | 9–144 | Auto-adjusts contrast for rendered size |
| Softness | `SOFT` | 0–100 | 0 = crisp/sharp, 100 = soft/rounded |
| Width | `wdth` | 100–120 | Normal to slightly extended |

#### Inter (Body)

| Axis | Tag | Range | Description |
|------|-----|-------|-------------|
| Weight | `wght` | 100–900 | Thin (100) to Black (900) |
| Slant | `slnt` | 0–10° | Upright to oblique |

#### JetBrains Mono (Mono)

| Axis | Tag | Range | Description |
|------|-----|-------|-------------|
| Weight | `wght` | 100–800 | Thin (100) to ExtraBold (800) |
| Italic | `ital` | 0–1 | Upright (0) to Italic (1) |

### 4.2 Prescribed Settings

```css
/* ── Display: Fraunces ── */
/* Heading weight hierarchy */
--font-display-h1: "wght" 700, "opsz" 72, "SOFT" 10, "wdth" 105;
--font-display-h2: "wght" 600, "opsz" 48, "SOFT" 15, "wdth" 102;
--font-display-h3: "wght" 500, "opsz" 32, "SOFT" 20, "wdth" 100;
--font-display-quote: "wght" 350, "opsz" 24, "SOFT" 40, "wdth" 100;

/* ── Body: Inter ── */
--font-body-regular: "wght" 400;
--font-body-medium:  "wght" 500;
--font-body-semibold:"wght" 600;
--font-body-bold:    "wght" 700;
--font-body-caption: "wght" 400, "slnt" 3;  /* slight slant for captions */

/* ── Mono: JetBrains Mono ── */
--font-mono-regular: "wght" 400;
--font-mono-medium:  "wght" 500;
--font-mono-bold:    "wght" 700;
```

### 4.3 Optical Sizing Strategy

Fraunces `opsz` axis should track the rendered `font-size`:

```
opsz = clamp(9, font-size * 0.75, 144)
```

| Rendered size | opsz value | Effect |
|---------------|------------|--------|
| 16px (body) | 12 | Low contrast, wider spacing — readable at text sizes |
| 32px (h3) | 24 | Moderate contrast |
| 48px (h2) | 36 | Increased contrast, tighter spacing |
| 64px (h1) | 48 | High contrast, display-optimized |
| 96px (hero) | 72 | Maximum contrast, tight fit |

When using `clamp()` for fluid type, `opsz` should ALSO use clamp to track the current size:

```css
h1 {
  font-size: clamp(2.441rem, 1.5rem + 3.5vw, 5.96rem);
  font-variation-settings: "wght" 700, "opsz" calc(clamp(2.441rem, 1.5rem + 3.5vw, 5.96rem) * 0.75);
}
```

Unfortunately CSS `calc()` inside `font-variation-settings` has limited browser support. The practical approach is to set `opsz` to the mid-point of the expected size range, or use a JavaScript-driven approach. For the design token layer, we document the intent and provide JS polyfill guidance.

---

## 5. Vertical Rhythm & Baseline Grid

### 5.1 Grid Foundation

```
Base unit:  4px
Line height: 24px (6 units)
Baseline:    every 4th pixel vertically

 0px ─────────────────────────────── baseline
 4px ─
 8px ─
12px ─
16px ─
20px ─
24px ─────────────────────────────── baseline
28px ─
32px ─
36px ─
40px ─
44px ─
48px ─────────────────────────────── baseline
```

### 5.2 Spacing Scale

All spacing tokens are multiples of the 4px baseline unit:

| Token | Value | Units | Use |
|-------|-------|-------|-----|
| `--space-0` | 0 | 0 | No spacing |
| `--space-1` | 4px / 0.25rem | 1 | Inline gaps, icon padding |
| `--space-2` | 8px / 0.5rem | 2 | Tight padding, small gaps |
| `--space-3` | 12px / 0.75rem | 3 | Component padding |
| `--space-4` | 16px / 1.0rem | 4 | Standard gutters |
| `--space-5` | 20px / 1.25rem | 5 | Section padding |
| `--space-6` | 24px / 1.5rem | 6 | Block spacing = 1 line |
| `--space-8` | 32px / 2.0rem | 8 | Section gaps |
| `--space-10` | 40px / 2.5rem | 10 | Large section gaps |
| `--space-12` | 48px / 3.0rem | 12 | 2 lines |
| `--space-16` | 64px / 4.0rem | 16 | Major layout divisions |
| `--space-20` | 80px / 5.0rem | 20 | Hero sections |
| `--space-24` | 96px / 6.0rem | 24 | Page-level separators |

### 5.3 Flow Spacing (Lobotomized Owl)

Default spacing between block-level siblings snaps to the baseline:

```css
/* Every block element that follows another gets 1 baseline-unit of margin */
.flow > * + * {
  margin-block-start: var(--space-6); /* 24px = 1 line */
}

/* Smaller flow context (cards, sidebars) */
.flow-sm > * + * {
  margin-block-start: var(--space-4); /* 16px */
}

/* Larger flow context (article body) */
.flow-lg > * + * {
  margin-block-start: var(--space-8); /* 32px */
}
```

### 5.4 Headline-to-Body Spacing

Headings use `margin-block-end` that falls on the baseline:

| Context | After heading | Token |
|---------|---------------|-------|
| h1 → body | 24px (1 line) | `--space-6` |
| h2 → body | 20px | `--space-5` |
| h3 → body | 16px | `--space-4` |
| h4 → body | 12px | `--space-3` |
| h5 → body | 8px | `--space-2` |
| h6 → body | 8px | `--space-2` |

---

## 6. Responsive Type with clamp()

### 6.1 Fluid Scale Formula

Each scale step uses `clamp(min, preferred, max)` where:

- **min** = size at 360px viewport (small mobile)
- **preferred** = viewport-relative growth using `vw`
- **max** = size at 1440px viewport (large desktop)

The preferred value is calculated as:

```
preferred = min_rem + (max_rem - min_rem) * ((100vw - 22.5rem) / (90rem - 22.5rem))
```

...which simplifies to a `rem + vw` expression.

### 6.2 Fluid Scale Table

| Step | Min (360px) | Max (1440px) | clamp() Expression |
|------|-------------|--------------|--------------------|
| xs | 0.625rem (10px) | 0.75rem (12px) | `clamp(0.625rem, 0.583rem + 0.185vw, 0.75rem)` |
| sm | 0.75rem (12px) | 0.875rem (14px) | `clamp(0.75rem, 0.708rem + 0.185vw, 0.875rem)` |
| base | 1rem (16px) | 1.125rem (18px) | `clamp(1rem, 0.958rem + 0.185vw, 1.125rem)` |
| lg | 1.125rem (18px) | 1.375rem (22px) | `clamp(1.125rem, 1.042rem + 0.37vw, 1.375rem)` |
| xl | 1.25rem (20px) | 1.75rem (28px) | `clamp(1.25rem, 1.083rem + 0.741vw, 1.75rem)` |
| 2xl | 1.5rem (24px) | 2.25rem (36px) | `clamp(1.5rem, 1.25rem + 1.111vw, 2.25rem)` |
| 3xl | 1.875rem (30px) | 2.75rem (44px) | `clamp(1.875rem, 1.583rem + 1.296vw, 2.75rem)` |
| 4xl | 2.25rem (36px) | 3.5rem (56px) | `clamp(2.25rem, 1.833rem + 1.852vw, 3.5rem)` |
| 5xl | 2.75rem (44px) | 4.5rem (72px) | `clamp(2.75rem, 2.167rem + 2.593vw, 4.5rem)` |
| 6xl | 3.25rem (52px) | 5.5rem (88px) | `clamp(3.25rem, 2.5rem + 3.333vw, 5.5rem)` |
| 7xl | 4rem (64px) | 7rem (112px) | `clamp(4rem, 3rem + 4.444vw, 7rem)` |

### 6.3 Fluid Line-Height Strategy

Line-height should also adjust with viewport — tighter at large sizes, looser at small:

```css
/* Body text */
--lh-body: clamp(1.4, 0.8rem + 2vw, 1.6);

/* Headings — tighter as they grow */
--lh-heading: clamp(1.0, 0.8rem + 1.5vw, 1.25);
```

---

## 7. Complete CSS Design Tokens

### 7.1 Full Token System (`design-tokens.css`)

```css
/* ============================================================
   STRYDE FORGE — TYPOGRAPHY DESIGN TOKENS
   Scale: 1.25 (Major Third) | Base: 16px | Grid: 4px
   ============================================================ */

:root {
  /* ═══════════════════════════════════════════════════════════
     FONT FAMILIES
     ═══════════════════════════════════════════════════════════ */

  /* Primary font stacks */
  --font-display: 'Fraunces', 'Georgia', 'Times New Roman', serif;
  --font-body:    'Inter', 'system-ui', '-apple-system', 'Segoe UI',
                  'Roboto', 'Helvetica Neue', 'Arial', sans-serif;
  --font-mono:    'JetBrains Mono', 'Cascadia Code', 'Fira Code',
                  'Consolas', 'Monaco', 'Andale Mono', monospace;

  /* Functional aliases */
  --font-heading:   var(--font-display);
  --font-ui:        var(--font-body);
  --font-code:      var(--font-mono);
  --font-article:   var(--font-body);
  --font-caption:   var(--font-body);

  /* ═══════════════════════════════════════════════════════════
     FONT WEIGHTS (Variable-First)
     ═══════════════════════════════════════════════════════════ */

  --weight-thin:       100;
  --weight-extralight: 200;
  --weight-light:      300;
  --weight-normal:     400;
  --weight-medium:     500;
  --weight-semibold:   600;
  --weight-bold:       700;
  --weight-extrabold:  800;
  --weight-black:      900;

  /* ═══════════════════════════════════════════════════════════
     MODULAR TYPE SCALE — Static (px fallback + rem)
     ═══════════════════════════════════════════════════════════ */

  --text-xs:   0.64rem;   /* 10.24px  | Step -2 */
  --text-sm:   0.8rem;    /* 12.80px  | Step -1 */
  --text-base: 1rem;      /* 16.00px  | Step  0 */
  --text-lg:   1.25rem;   /* 20.00px  | Step  1 */
  --text-xl:   1.563rem;  /* 25.00px  | Step  2 */
  --text-2xl:  1.953rem;  /* 31.25px  | Step  3 */
  --text-3xl:  2.441rem;  /* 39.06px  | Step  4 */
  --text-4xl:  3.052rem;  /* 48.83px  | Step  5 */
  --text-5xl:  3.815rem;  /* 61.04px  | Step  6 */
  --text-6xl:  4.768rem;  /* 76.29px  | Step  7 */
  --text-7xl:  5.96rem;   /* 95.37px  | Step  8 */

  /* ═══════════════════════════════════════════════════════════
     FLUID TYPE SCALE — Responsive clamp() values
     ═══════════════════════════════════════════════════════════ */

  --text-fluid-xs:   clamp(0.625rem, 0.583rem + 0.185vw, 0.75rem);
  --text-fluid-sm:   clamp(0.75rem,  0.708rem + 0.185vw, 0.875rem);
  --text-fluid-base: clamp(1rem,     0.958rem + 0.185vw, 1.125rem);
  --text-fluid-lg:   clamp(1.125rem, 1.042rem + 0.37vw,  1.375rem);
  --text-fluid-xl:   clamp(1.25rem,  1.083rem + 0.741vw, 1.75rem);
  --text-fluid-2xl:  clamp(1.5rem,   1.25rem  + 1.111vw, 2.25rem);
  --text-fluid-3xl:  clamp(1.875rem, 1.583rem + 1.296vw, 2.75rem);
  --text-fluid-4xl:  clamp(2.25rem,  1.833rem + 1.852vw, 3.5rem);
  --text-fluid-5xl:  clamp(2.75rem,  2.167rem + 2.593vw, 4.5rem);
  --text-fluid-6xl:  clamp(3.25rem,  2.5rem   + 3.333vw, 5.5rem);
  --text-fluid-7xl:  clamp(4rem,     3rem     + 4.444vw, 7rem);

  /* ═══════════════════════════════════════════════════════════
     LINE HEIGHTS — Baseline-snapped
     ═══════════════════════════════════════════════════════════ */

  --leading-xs:    1;      /* 16px / 1 baseline unit */
  --leading-sm:    1.25;   /* 20px / 1.25 baseline units */
  --leading-base:  1.5;    /* 24px / 1.5 baseline units (default) */
  --leading-lg:    1.4;    /* 28px */
  --leading-xl:    1.28;   /* 32px */
  --leading-2xl:   1.28;   /* 40px */
  --leading-3xl:   1.229;  /* 48px */
  --leading-4xl:   1.147;  /* 56px */
  --leading-5xl:   1.114;  /* 68px */
  --leading-6xl:   1.101;  /* 84px */
  --leading-7xl:   1.09;   /* 104px */

  /* Fluid line-height tokens */
  --leading-fluid-body:    clamp(1.4, 0.6rem + 2vw, 1.6);
  --leading-fluid-heading: clamp(1.05, 0.7rem + 1.5vw, 1.2);
  --leading-fluid-display: clamp(1.0, 0.6rem + 1vw, 1.12);

  /* ═══════════════════════════════════════════════════════════
     LETTER SPACING
     ═══════════════════════════════════════════════════════════ */

  --tracking-tighter: -0.05em;
  --tracking-tight:   -0.025em;
  --tracking-normal:   0;
  --tracking-wide:     0.025em;
  --tracking-wider:    0.05em;
  --tracking-widest:   0.1em;

  /* Display text (large headings) benefits from tighter tracking */
  --tracking-display: -0.02em;
  /* Uppercase text benefits from wider tracking */
  --tracking-uppercase: 0.04em;

  /* ═══════════════════════════════════════════════════════════
     VERTICAL RHYTHM — Spacing Scale (4px baseline unit)
     ═══════════════════════════════════════════════════════════ */

  --space-0:  0;
  --space-1:  0.25rem;  /*   4px — 1 unit  */
  --space-2:  0.5rem;   /*   8px — 2 units */
  --space-3:  0.75rem;  /*  12px — 3 units */
  --space-4:  1rem;     /*  16px — 4 units */
  --space-5:  1.25rem;  /*  20px — 5 units */
  --space-6:  1.5rem;   /*  24px — 6 units (1 line) */
  --space-8:  2rem;     /*  32px — 8 units */
  --space-10: 2.5rem;   /*  40px — 10 units */
  --space-12: 3rem;     /*  48px — 12 units (2 lines) */
  --space-16: 4rem;     /*  64px — 16 units */
  --space-20: 5rem;     /*  80px — 20 units */
  --space-24: 6rem;     /*  96px — 24 units (4 lines) */
  --space-32: 8rem;     /* 128px — 32 units */
  --space-40: 10rem;    /* 160px — 40 units */

  /* Fluid spacing tokens */
  --space-fluid-section: clamp(3rem, 2rem + 4vw, 6rem);
  --space-fluid-block:   clamp(1.5rem, 1rem + 2vw, 3rem);

  /* ═══════════════════════════════════════════════════════════
     VARIABLE FONT SETTINGS — Prescribed axes
     ═══════════════════════════════════════════════════════════ */

  /* ── Fraunces (Display) ── */
  --fv-fraunces-h1:    "wght" 700, "opsz" 72, "SOFT" 10, "wdth" 105;
  --fv-fraunces-h2:    "wght" 600, "opsz" 48, "SOFT" 15, "wdth" 102;
  --fv-fraunces-h3:    "wght" 500, "opsz" 32, "SOFT" 20, "wdth" 100;
  --fv-fraunces-h4:    "wght" 450, "opsz" 24, "SOFT" 25, "wdth" 100;
  --fv-fraunces-quote: "wght" 350, "opsz" 24, "SOFT" 40, "wdth" 100;
  --fv-fraunces-caps:  "wght" 600, "opsz" 18, "SOFT" 5,  "wdth" 110;

  /* ── Inter (Body) ── */
  --fv-inter-regular:  "wght" 400;
  --fv-inter-medium:   "wght" 500;
  --fv-inter-semibold: "wght" 600;
  --fv-inter-bold:     "wght" 700;
  --fv-inter-caption:  "wght" 400, "slnt" 3;

  /* ── JetBrains Mono (Code) ── */
  --fv-mono-regular: "wght" 400;
  --fv-mono-medium:  "wght" 500;
  --fv-mono-bold:    "wght" 700;
  --fv-mono-code:    "wght" 400, "ital" 0;

  /* ═══════════════════════════════════════════════════════════
     FONT STYLE TOKENS
     ═══════════════════════════════════════════════════════════ */

  --style-normal:  normal;
  --style-italic:  italic;
  --style-oblique: oblique 10deg;

  /* ═══════════════════════════════════════════════════════════
     TEXT DECORATION
     ═══════════════════════════════════════════════════════════ */

  --decoration-none:        none;
  --decoration-underline:   underline;
  --decoration-line-through: line-through;

  --underline-offset: 0.15em;
  --underline-thickness: 0.08em;

  /* ═══════════════════════════════════════════════════════════
     MEASURE (Max inline length for readability)
     ═══════════════════════════════════════════════════════════ */

  --measure-narrow:  35ch;  /* Narrow columns, sidebars */
  --measure-base:    60ch;  /* Optimal body-copy width */
  --measure-wide:    75ch;  /* Comfortable maximum */
  --measure-full:    100%;  /* Full container width */

  /* ═══════════════════════════════════════════════════════════
     BASELINE GRID OVERLAY (debug mode)
     ═══════════════════════════════════════════════════════════ */

  --baseline-unit:  4px;
  --baseline-line:  24px;  /* 6 units */
  --baseline-color: rgba(255, 0, 255, 0.12);

  /* ═══════════════════════════════════════════════════════════
     TYPOGRAPHIC SCALE ALIASES (Semantic)
     ═══════════════════════════════════════════════════════════ */

  --text-caption:   var(--text-sm);
  --text-body:      var(--text-base);
  --text-lead:      var(--text-lg);
  --text-subtitle:  var(--text-xl);
  --text-h6:        var(--text-base);   /* h6 = body size, bold */
  --text-h5:        var(--text-lg);
  --text-h4:        var(--text-xl);
  --text-h3:        var(--text-2xl);
  --text-h2:        var(--text-3xl);
  --text-h1:        var(--text-5xl);
  --text-hero:      var(--text-7xl);
}
```

### 7.2 Typographic Utility Classes

```css
/* ============================================================
   TYPOGRAPHY UTILITY CLASSES
   ============================================================ */

/* ── Heading Resets (apply directly to h1–h6) ── */
h1, .h1 {
  font-family: var(--font-display);
  font-size: var(--text-fluid-5xl);
  font-weight: var(--weight-bold);
  font-variation-settings: var(--fv-fraunces-h1);
  line-height: var(--leading-fluid-display);
  letter-spacing: var(--tracking-display);
  max-width: var(--measure-wide);
}

h2, .h2 {
  font-family: var(--font-display);
  font-size: var(--text-fluid-3xl);
  font-weight: var(--weight-semibold);
  font-variation-settings: var(--fv-fraunces-h2);
  line-height: var(--leading-fluid-heading);
  letter-spacing: var(--tracking-tight);
  max-width: var(--measure-wide);
}

h3, .h3 {
  font-family: var(--font-display);
  font-size: var(--text-fluid-2xl);
  font-weight: var(--weight-medium);
  font-variation-settings: var(--fv-fraunces-h3);
  line-height: var(--leading-fluid-heading);
  letter-spacing: var(--tracking-tight);
}

h4, .h4 {
  font-family: var(--font-body);
  font-size: var(--text-fluid-xl);
  font-weight: var(--weight-semibold);
  font-variation-settings: var(--fv-inter-semibold);
  line-height: var(--leading-fluid-heading);
}

h5, .h5 {
  font-family: var(--font-body);
  font-size: var(--text-fluid-lg);
  font-weight: var(--weight-semibold);
  font-variation-settings: var(--fv-inter-semibold);
  line-height: var(--leading-fluid-body);
}

h6, .h6 {
  font-family: var(--font-body);
  font-size: var(--text-fluid-base);
  font-weight: var(--weight-bold);
  font-variation-settings: var(--fv-inter-bold);
  line-height: var(--leading-fluid-body);
  text-transform: uppercase;
  letter-spacing: var(--tracking-uppercase);
}

/* ── Body Copy ── */
body {
  font-family: var(--font-body);
  font-size: var(--text-fluid-base);
  font-weight: var(--weight-normal);
  font-variation-settings: var(--fv-inter-regular);
  line-height: var(--leading-fluid-body);
  color: var(--color-text, inherit);
}

/* ── Lead / Intro Paragraph ── */
.lead {
  font-size: var(--text-fluid-lg);
  font-weight: var(--weight-light);
  font-variation-settings: var(--fv-inter-caption);
  line-height: var(--leading-fluid-body);
  max-width: var(--measure-base);
}

/* ── Small / Caption ── */
small, .text-caption {
  font-size: var(--text-fluid-sm);
  font-weight: var(--weight-normal);
  line-height: var(--leading-sm);
}

/* ── Fine Print ── */
.text-fine {
  font-size: var(--text-fluid-xs);
  line-height: var(--leading-xs);
}

/* ── Code ── */
code, .code {
  font-family: var(--font-mono);
  font-size: 0.875em;
  font-variation-settings: var(--fv-mono-code);
  background: var(--color-code-bg, rgba(0, 0, 0, 0.05));
  padding: 0.15em 0.35em;
  border-radius: 0.25em;
}

pre {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-variation-settings: var(--fv-mono-regular);
  line-height: var(--leading-base);
  padding: var(--space-4);
  border-radius: 0.5rem;
  overflow-x: auto;
}

/* ── Blockquote ── */
blockquote {
  font-family: var(--font-display);
  font-size: var(--text-fluid-lg);
  font-weight: var(--weight-light);
  font-variation-settings: var(--fv-fraunces-quote);
  font-style: italic;
  line-height: var(--leading-fluid-body);
  max-width: var(--measure-narrow);
  padding-inline-start: var(--space-4);
  border-inline-start: 3px solid currentColor;
}

/* ── Pull Quote ── */
.pull-quote {
  font-family: var(--font-display);
  font-size: var(--text-fluid-2xl);
  font-weight: var(--weight-light);
  font-variation-settings: var(--fv-fraunces-quote);
  line-height: var(--leading-fluid-heading);
  max-width: var(--measure-narrow);
}

/* ── Uppercase Label ── */
.label {
  font-family: var(--font-body);
  font-size: var(--text-fluid-xs);
  font-weight: var(--weight-bold);
  font-variation-settings: var(--fv-inter-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-uppercase);
}

/* ── Baseline Grid Debug Overlay ── */
.baseline-debug {
  position: relative;
}

.baseline-debug::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  background-image:
    repeating-linear-gradient(
      to bottom,
      transparent,
      transparent calc(var(--baseline-line) - 1px),
      var(--baseline-color) calc(var(--baseline-line) - 1px),
      var(--baseline-color) var(--baseline-line)
    );
}
```

---

## 8. Usage Examples

### 8.1 HTML Head Setup

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Stryde Forge — Typography System</title>

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,100..900,0..100;1,9..144,100..900,0..100&family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap" rel="stylesheet">

  <!-- Design Tokens -->
  <link rel="stylesheet" href="/css/design-tokens.css">
  <link rel="stylesheet" href="/css/typography.css">
</head>
```

### 8.2 Article Page — Semantic HTML

```html
<article class="flow-lg" style="max-width: var(--measure-base); margin-inline: auto;">
  <h1>The Craft of Typographic Systems</h1>

  <p class="lead">
    A well-designed typographic system is not merely a collection of font sizes —
    it is a mathematical framework that creates harmony between text elements
    at every viewport size.
  </p>

  <p>
    The foundation of this system rests on the major third ratio (1.25), chosen
    for its clean geometric progression. Each step in the scale is 25% larger
    than the previous, creating a rhythm that feels both natural and deliberate.
  </p>

  <h2>Vertical Rhythm</h2>

  <p>
    Every line of text falls on a 4px baseline grid. This invisible structure
    ensures that text across columns aligns perfectly, creating a sense of
    order that readers perceive subconsciously.
  </p>

  <blockquote>
    Typography is the craft of endowing human language with a durable visual form.
    <cite>— Robert Bringhurst</cite>
  </blockquote>

  <h3>Responsive Scaling</h3>

  <p>
    All type sizes use <code>clamp()</code> to fluidly scale between mobile
    and desktop viewports. No breakpoints, no media queries — just smooth,
    continuous scaling that respects the type scale at every width.
  </p>

  <pre><code>/* Fluid base size */
font-size: clamp(1rem, 0.958rem + 0.185vw, 1.125rem);</code></pre>
</article>
```

### 8.3 Dashboard / UI Layout

```html
<nav style="font-family: var(--font-ui);">
  <span class="label">Navigation</span>
  <ul style="list-style: none; padding: 0;">
    <li><a href="#" style="font-weight: var(--weight-medium);">Dashboard</a></li>
    <li><a href="#">Settings</a></li>
    <li><a href="#">Analytics</a></li>
  </ul>
</nav>

<main style="font-family: var(--font-body);">
  <h3>Performance Metrics</h3>
  <table style="font-family: var(--font-mono); font-size: var(--text-sm);">
    <thead>
      <tr>
        <th class="label">Metric</th>
        <th class="label">Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>requests_per_sec</td>
        <td>12,847</td>
      </tr>
      <tr>
        <td>p99_latency_ms</td>
        <td>243.7</td>
      </tr>
    </tbody>
  </table>
</main>
```

### 8.4 Hero Section

```html
<section class="hero" style="
  padding-block: var(--space-fluid-section);
  text-align: center;
">
  <h1 style="
    font-size: var(--text-fluid-7xl);
    font-variation-settings: var(--fv-fraunces-h1);
    line-height: var(--leading-fluid-display);
  ">
    Stryde Forge
  </h1>

  <p class="lead" style="
    font-size: var(--text-fluid-2xl);
    font-weight: var(--weight-light);
    max-width: var(--measure-base);
    margin-inline: auto;
  ">
    A typographic framework built for precision, scale, and beauty.
  </p>
</section>
```

---

## 9. Accessibility Notes

### 9.1 Minimum Sizes

| Element | Minimum | Rationale |
|---------|---------|-----------|
| Body text | 16px (1rem) | WCAG does not mandate minimum, but 16px is the de facto standard; below 14px harms readability |
| Small/caption | 12px (0.75rem) | Absolute floor; never go below 12px for readable content |
| Input text | 16px (1rem) | Prevents iOS Safari zoom on focus |
| Touch targets | 44×44px | WCAG 2.5.5 Target Size (AAA) |

### 9.2 Contrast

- Body text on background must meet **AA contrast ratio (4.5:1)**
- Large text (≥24px or ≥18px bold) must meet **AA contrast ratio (3:1)**
- All text should meet **AAA (7:1)** where feasible

### 9.3 Relative Units

- All typography uses `rem` — respects user font-size preferences
- No `px` in production styles (tokens show px equivalents in comments only)
- `clamp()` with `vw` means zooming in also scales text appropriately

### 9.4 `prefers-reduced-motion`

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 9.5 Font Loading Strategy

- `font-display: swap` ensures text is visible immediately with fallback
- Inline critical CSS to minimize FOUT (Flash of Unstyled Text)
- Preload critical font files: `<link rel="preload" as="font" ...>`

---

## Appendix A: Scale Calculation Reference

```
Scale factor: 1.25 = 5/4

Step(n) = 16px × (1.25)^n

n = -2: 16 × (4/5)²   = 16 × 0.64  = 10.24
n = -1: 16 × (4/5)    = 16 × 0.80  = 12.80
n =  0: 16 × 1        = 16.00
n =  1: 16 × 1.25     = 20.00
n =  2: 16 × 1.5625   = 25.00
n =  3: 16 × 1.953125  = 31.25
n =  4: 16 × 2.441406  = 39.06
n =  5: 16 × 3.051758  = 48.83
n =  6: 16 × 3.814697  = 61.04
n =  7: 16 × 4.768372  = 76.29
n =  8: 16 × 5.960464  = 95.37
```

## Appendix B: Fluid clamp() Derivation

For a value that should be `min` at 360px (22.5rem) and `max` at 1440px (90rem):

```
clamp(min_rem, min_rem + (max_rem - min_rem) * (100vw - 22.5rem) / (90rem - 22.5rem), max_rem)

Simplified to: clamp(min_rem, [slope]rem + [intercept]vw, max_rem)

Where:
  slope = min_rem - (max_rem - min_rem) * 22.5 / (90 - 22.5)
  intercept = (max_rem - min_rem) * 100 / (90 - 22.5)
```

## Appendix C: File Structure

```
css/
├── design-tokens.css       ← All custom properties
├── typography.css          ← Element resets + utility classes
├── baseline-debug.css      ← Baseline grid overlay (dev only)
└── fonts/
    ├── fraunces.woff2
    ├── fraunces-italic.woff2
    ├── inter.woff2
    ├── inter-italic.woff2
    ├── jetbrains-mono.woff2
    └── jetbrains-mono-italic.woff2
```

---

*Styde Forge Typography System v1.0 — Generated 2026-06-26*
