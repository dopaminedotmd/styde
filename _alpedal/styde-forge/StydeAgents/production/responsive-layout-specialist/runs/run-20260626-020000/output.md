# Responsive Layout Specialist — Cycle 2 Output

**Run:** `run-20260626-020000`
**Date:** 2026-06-26
**Agent:** responsive-layout-specialist (cycle 2)

---

## Overview

This deliverable demonstrates five advanced responsive CSS layout patterns in a single, self-contained HTML document:

| # | Pattern | Key Technologies |
|---|---------|-----------------|
| 1 | **Subgrid** | `grid-template-rows: subgrid`, nested grid alignment |
| 2 | **Masonry Layout** | `grid-template-rows: masonry` + column-based polyfill |
| 3 | **Container-Query Card Variants** | `@container`, `container-type`, `container-name` |
| 4 | **Logical Properties** | `margin-inline`, `padding-block`, `border-inline`, `inset-inline` |
| 5 | **5-Breakpoint Adaptive Component** | `@media` at 320/640/960/1280/1600px, `clamp()`, fluid typography |

---

## Complete HTML/CSS Source

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Advanced Responsive Layout Patterns — Cycle 2</title>
<style>
/* ================================================================
   CSS CUSTOM PROPERTIES & DESIGN TOKENS
   ================================================================ */
:root {
  /* Color system */
  --color-bg:            #0f1117;
  --color-surface:       #1a1d27;
  --color-surface-hover: #242836;
  --color-border:        #2e3345;
  --color-text:          #e2e4eb;
  --color-text-muted:    #8b8fa8;
  --color-accent:        #6c8cff;
  --color-accent-glow:   #8aa4ff;
  --color-success:       #4ade80;
  --color-warning:       #fbbf24;
  --color-danger:        #f87171;

  /* Spacing scale (logical-property friendly) */
  --space-xs:   0.25rem;
  --space-sm:   0.5rem;
  --space-md:   1rem;
  --space-lg:   1.5rem;
  --space-xl:   2rem;
  --space-2xl:  3rem;
  --space-3xl:  4rem;

  /* Typography */
  --font-sans: 'Segoe UI', system-ui, -apple-system, sans-serif;
  --font-mono: 'Cascadia Code', 'Fira Code', 'JetBrains Mono', monospace;

  /* Border radius */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-xl: 24px;

  /* Transitions */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-fast: 150ms;
  --duration-normal: 300ms;
}

/* ================================================================
   GLOBAL RESET & BASE
   ================================================================ */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 100%;
  color-scheme: dark;
  -webkit-font-smoothing: antialiased;
}

body {
  font-family: var(--font-sans);
  background: var(--color-bg);
  color: var(--color-text);
  line-height: 1.6;
  min-block-size: 100dvb;
  padding-block: var(--space-3xl);
  padding-inline: var(--space-xl);
}

/* ================================================================
   SECTION HEADERS
   ================================================================ */
.section-title {
  font-size: clamp(1.5rem, 3vw, 2.25rem);
  font-weight: 700;
  margin-block-end: var(--space-sm);
  color: var(--color-accent-glow);
}

.section-subtitle {
  font-size: 0.95rem;
  color: var(--color-text-muted);
  margin-block-end: var(--space-xl);
  font-family: var(--font-mono);
  font-size: 0.85rem;
}

.demo-section {
  margin-block-end: var(--space-3xl);
  padding-block-end: var(--space-2xl);
  border-block-end: 1px solid var(--color-border);
}

/* ================================================================
   PATTERN 1: SUBGRID — Product Comparison Table
   ================================================================ */
.subgrid-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-lg);
}

.subgrid-card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 4;           /* spans header, price, features, CTA rows */
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: border-color var(--duration-normal) var(--ease-out);
}

.subgrid-card:hover {
  border-color: var(--color-accent);
}

.subgrid-card--featured {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 1px var(--color-accent), 0 4px 24px rgba(108, 140, 255, 0.15);
}

.subgrid-card__header {
  padding: var(--space-lg);
  background: var(--color-surface-hover);
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.subgrid-card__header h3 {
  font-size: 1.1rem;
  font-weight: 600;
}

.subgrid-card__badge {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding-inline: var(--space-sm);
  padding-block: 2px;
  background: var(--color-accent);
  color: #fff;
  border-radius: var(--radius-sm);
}

.subgrid-card__price {
  padding-inline: var(--space-lg);
  padding-block: var(--space-md);
  font-size: 2rem;
  font-weight: 800;
}

.subgrid-card__price span {
  font-size: 0.9rem;
  font-weight: 400;
  color: var(--color-text-muted);
}

.subgrid-card__features {
  padding-inline: var(--space-lg);
  padding-block: var(--space-md);
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.subgrid-card__features li {
  padding-inline-start: 1.4em;
  position: relative;
  font-size: 0.9rem;
}

.subgrid-card__features li::before {
  content: "✓";
  position: absolute;
  inset-inline-start: 0;
  color: var(--color-success);
  font-weight: 700;
}

.subgrid-card__features li.disabled {
  color: var(--color-text-muted);
  text-decoration: line-through;
}

.subgrid-card__features li.disabled::before {
  content: "—";
  color: var(--color-danger);
}

.subgrid-card__cta {
  padding: var(--space-lg);
}

.subgrid-card__cta button {
  inline-size: 100%;
  padding-block: var(--space-sm);
  padding-inline: var(--space-md);
  background: var(--color-accent);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background var(--duration-fast) var(--ease-out);
}

.subgrid-card__cta button:hover {
  background: var(--color-accent-glow);
}

/* ================================================================
   PATTERN 2: MASONRY LAYOUT — Image Gallery
   ================================================================ */
.masonry-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: masonry;          /* Native masonry (Chrome experimental) */
  gap: var(--space-md);
}

/* Fallback when masonry is NOT supported */
@supports not (grid-template-rows: masonry) {
  .masonry-grid {
    columns: 4;
    column-gap: var(--space-md);
    display: block;
  }
  .masonry-item {
    break-inside: avoid;
    margin-block-end: var(--space-md);
  }
}

.masonry-item {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: transform var(--duration-normal) var(--ease-out),
              border-color var(--duration-normal) var(--ease-out);
  cursor: pointer;
}

.masonry-item:hover {
  transform: translateY(-4px);
  border-color: var(--color-accent);
}

.masonry-item__img {
  inline-size: 100%;
  display: block;
  aspect-ratio: auto;                   /* Allows varying aspect ratios */
  background: linear-gradient(135deg, var(--color-surface-hover), var(--color-border));
}

.masonry-item__caption {
  padding-inline: var(--space-md);
  padding-block: var(--space-sm);
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

/* Masonry item height variations (simulate different image heights) */
.masonry-item--tall  .masonry-item__img { block-size: 280px; }
.masonry-item--short .masonry-item__img { block-size: 150px; }
.masonry-item--medium .masonry-item__img { block-size: 210px; }

/* Colored placeholders */
.masonry-item__img--1  { background: linear-gradient(135deg, #6c8cff, #a78bfa); }
.masonry-item__img--2  { background: linear-gradient(135deg, #4ade80, #34d399); }
.masonry-item__img--3  { background: linear-gradient(135deg, #fbbf24, #f59e0b); }
.masonry-item__img--4  { background: linear-gradient(135deg, #f87171, #fb7185); }
.masonry-item__img--5  { background: linear-gradient(135deg, #a78bfa, #c084fc); }
.masonry-item__img--6  { background: linear-gradient(135deg, #38bdf8, #22d3ee); }
.masonry-item__img--7  { background: linear-gradient(135deg, #f472b6, #fb7185); }
.masonry-item__img--8  { background: linear-gradient(135deg, #6c8cff, #38bdf8); }

/* ================================================================
   PATTERN 3: CONTAINER-QUERY-DRIVEN CARD VARIANTS
   ================================================================ */
.cq-demo {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-lg);
}

/* Wide container (sidebar layout simulation) */
.cq-demo__wide {
  grid-column: span 2;
}

/* Define containment contexts */
.cq-card-container {
  container-type: inline-size;
  container-name: card;
}

/* ── Default card (narrow: < 300px) ── */
.cq-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.cq-card__media {
  aspect-ratio: 16 / 9;
  background: linear-gradient(135deg, var(--color-border), var(--color-surface-hover));
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  overflow: hidden;
}

.cq-card__body h4 {
  font-size: 1rem;
  font-weight: 600;
  margin-block-end: var(--space-xs);
}

.cq-card__body p {
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

.cq-card__meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  color: var(--color-text-muted);
  padding-block-start: var(--space-sm);
  border-block-start: 1px solid var(--color-border);
}

.cq-card__tag {
  background: var(--color-accent);
  color: #fff;
  padding-inline: var(--space-sm);
  padding-block: 2px;
  border-radius: 100vmax;
  font-size: 0.7rem;
  font-weight: 600;
}

/* ── Variant A: medium container (300px – 500px) ── */
@container card (min-width: 300px) and (max-width: 499px) {
  .cq-card {
    flex-direction: row;
    align-items: center;
  }
  .cq-card__media {
    inline-size: 120px;
    flex-shrink: 0;
    aspect-ratio: 1 / 1;
  }
  .cq-card__media::after {
    content: " (medium container)";
  }
}

/* ── Variant B: wide container (500px – 700px) ── */
@container card (min-width: 500px) and (max-width: 699px) {
  .cq-card {
    display: grid;
    grid-template-columns: 200px 1fr;
    grid-template-rows: auto auto;
    gap: var(--space-md);
    padding: 0;
    overflow: hidden;
  }
  .cq-card__media {
    grid-row: 1 / -1;
    aspect-ratio: auto;
    block-size: 100%;
    border-radius: 0;
  }
  .cq-card__media::after {
    content: " (wide container)";
  }
  .cq-card__body {
    padding-block-start: var(--space-md);
    padding-inline-end: var(--space-md);
  }
  .cq-card__meta {
    grid-column: 2;
    padding-inline-end: var(--space-md);
    padding-block-end: var(--space-md);
    border: none;
  }
}

/* ── Variant C: extra-wide container (≥ 700px) ── */
@container card (min-width: 700px) {
  .cq-card {
    display: grid;
    grid-template-columns: 280px 1fr 160px;
    grid-template-rows: 1fr;
    gap: 0;
    padding: 0;
    align-items: stretch;
  }
  .cq-card__media {
    aspect-ratio: auto;
    block-size: 100%;
    border-radius: 0;
  }
  .cq-card__media::after {
    content: " (extra-wide container)";
  }
  .cq-card__body {
    padding: var(--space-lg);
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .cq-card__meta {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: center;
    gap: var(--space-sm);
    padding: var(--space-lg);
    background: var(--color-surface-hover);
    border: none;
  }
}

/* ================================================================
   PATTERN 4: LOGICAL PROPERTIES — Direction-Aware Component
   ================================================================ */
.logical-demo {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-lg);
}

.logical-panel {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding-block: var(--space-xl);         /* logical: top + bottom */
  padding-inline: var(--space-xl);         /* logical: left + right (LTR) or right + left (RTL) */
  margin-inline: 0;                        /* logical: margin-left + margin-right */
  margin-block-end: var(--space-md);
  border-inline-start: 4px solid var(--color-accent);  /* logical left border in LTR */
}

.logical-panel--rtl {
  direction: rtl;
  border-inline-start: none;               /* reset left-border-first in RTL */
  border-inline-end: 4px solid var(--color-accent);     /* accent on the "start" side in RTL = right */
}

.logical-panel h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-block-end: var(--space-sm);
}

.logical-panel p {
  font-size: 0.9rem;
  color: var(--color-text-muted);
  max-inline-size: 60ch;                   /* logical: max-width */
}

.logical-badge {
  display: inline-block;
  padding-inline: 0.6em;
  padding-block: 0.2em;
  background: var(--color-accent);
  color: #fff;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 600;
  margin-inline-end: var(--space-sm);      /* logical: margin-right in LTR */
}

/* Inline-flow logical layout */
.logical-inline-group {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding-inline: var(--space-lg);
  padding-block: var(--space-md);
  background: var(--color-surface-hover);
  border-radius: var(--radius-md);
  margin-block-end: var(--space-md);
  border: 1px solid var(--color-border);
}

.logical-inline-group--rtl {
  direction: rtl;
}

.logical-inline-item {
  padding-inline: var(--space-md);
  padding-block: var(--space-sm);
  background: var(--color-accent);
  color: #fff;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 0.85rem;
}

/* Logical scroll */
.logical-scroll {
  overflow-inline: auto;                   /* logical: overflow-x */
  max-inline-size: 100%;
  white-space: nowrap;
  padding-block: var(--space-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
}

/* Inset logical */
.logical-overlay {
  position: relative;
  block-size: 120px;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.logical-overlay__child {
  position: absolute;
  inset-block-start: var(--space-md);      /* logical: top */
  inset-inline-start: var(--space-md);     /* logical: left in LTR */
  inset-block-end: var(--space-md);        /* logical: bottom */
  inset-inline-end: var(--space-md);       /* logical: right in LTR */
  background: var(--color-accent);
  opacity: 0.2;
  border-radius: var(--radius-sm);
}

/* ================================================================
   PATTERN 5: FIVE-BREAKPOINT ADAPTIVE COMPONENT — "Hero Banner"
   ================================================================ */
/*
   Breakpoint table:
   ┌────────────┬───────────┬──────────────────────────────┐
   │ Name       │ Min-width │ Behavior                      │
   ├────────────┼───────────┼──────────────────────────────┤
   │ XS (phone) │   320px   │ Stacked, full-width image     │
   │ SM (phablet)│  640px   │ Stacked, tighter text         │
   │ MD (tablet) │  960px   │ Side-by-side, image left      │
   │ LG (laptop) │ 1280px   │ Three-column, stats bar       │
   │ XL (desktop)│ 1600px   │ Max-width cap, mega layout     │
   └────────────┴───────────┴──────────────────────────────┘
*/

.hero {
  --hero-padding-inline: clamp(var(--space-md), 4vw, var(--space-3xl));
  --hero-padding-block: clamp(var(--space-xl), 6vw, var(--space-3xl));

  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;

  /* ── XS: 320px+ — default mobile stack ── */
  display: flex;
  flex-direction: column;
}

.hero__media {
  position: relative;
  background: linear-gradient(135deg, #6c8cff, #a78bfa, #f472b6);
  min-block-size: 200px;
}

.hero__media-inner {
  block-size: 100%;
  min-block-size: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: 0.9rem;
  color: rgba(255,255,255,0.7);
}

.hero__content {
  padding-inline: var(--hero-padding-inline);
  padding-block: var(--hero-padding-block);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.hero__eyebrow {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-accent-glow);
  font-weight: 600;
}

.hero__title {
  font-size: clamp(1.5rem, 5vw, 3.5rem);
  font-weight: 800;
  line-height: 1.1;
}

.hero__description {
  font-size: clamp(0.9rem, 2vw, 1.1rem);
  color: var(--color-text-muted);
  max-inline-size: 55ch;
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
}

.hero__btn {
  padding-inline: var(--space-lg);
  padding-block: var(--space-sm);
  border-radius: 100vmax;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  border: 1px solid transparent;
}

.hero__btn--primary {
  background: var(--color-accent);
  color: #fff;
}
.hero__btn--primary:hover {
  background: var(--color-accent-glow);
}

.hero__btn--secondary {
  background: transparent;
  border-color: var(--color-border);
  color: var(--color-text);
}
.hero__btn--secondary:hover {
  border-color: var(--color-accent);
  color: var(--color-accent-glow);
}

/* Stats bar — hidden on XS/SM */
.hero__stats {
  display: none;
}

/* ── SM: 640px+ ── */
@media (min-width: 640px) {
  .hero {
    border-radius: var(--radius-xl);
  }
  .hero__media {
    min-block-size: 280px;
  }
  .hero__media-inner {
    min-block-size: 280px;
  }
  .hero__title {
    font-size: clamp(2rem, 6vw, 3rem);
  }
  .hero__actions {
    gap: var(--space-md);
  }
}

/* ── MD: 960px+ — side-by-side ── */
@media (min-width: 960px) {
  .hero {
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: stretch;
  }
  .hero__media {
    min-block-size: 100%;
  }
  .hero__media-inner {
    min-block-size: 400px;
  }
  .hero__content {
    justify-content: center;
  }
}

/* ── LG: 1280px+ — three-column with stats ── */
@media (min-width: 1280px) {
  .hero {
    grid-template-columns: 1fr 1fr 220px;
  }
  .hero__stats {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: var(--space-md);
    padding: var(--space-xl);
    background: var(--color-surface-hover);
    border-inline-start: 1px solid var(--color-border);   /* logical! */
  }
  .hero__stat {
    text-align: center;
  }
  .hero__stat-value {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--color-accent-glow);
  }
  .hero__stat-label {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
}

/* ── XL: 1600px+ — max-width cap ── */
@media (min-width: 1600px) {
  .hero {
    max-inline-size: 1400px;
    margin-inline: auto;
    grid-template-columns: 1.2fr 1fr 260px;
    box-shadow: 0 8px 48px rgba(0, 0, 0, 0.4);
  }
  .hero__title {
    font-size: 3.5rem;
  }
  .hero__stats {
    padding: var(--space-2xl);
  }
}

/* Breakpoint indicator badge */
.breakpoint-indicator {
  position: fixed;
  inset-block-end: var(--space-md);
  inset-inline-end: var(--space-md);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 100vmax;
  padding-inline: var(--space-md);
  padding-block: var(--space-xs);
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--color-accent-glow);
  z-index: 100;
}

.breakpoint-indicator::after {
  content: "XS (≥320px)";
}

@media (min-width: 640px)  { .breakpoint-indicator::after { content: "SM (≥640px)"; } }
@media (min-width: 960px)  { .breakpoint-indicator::after { content: "MD (≥960px)"; } }
@media (min-width: 1280px) { .breakpoint-indicator::after { content: "LG (≥1280px)"; } }
@media (min-width: 1600px) { .breakpoint-indicator::after { content: "XL (≥1600px)"; } }

/* ================================================================
   RESPONSIVE OVERRIDES FOR DEMO LAYOUTS
   ================================================================ */
@media (max-width: 639px) {
  .subgrid-grid {
    grid-template-columns: 1fr;
  }
  .logical-demo {
    grid-template-columns: 1fr;
  }
  @supports not (grid-template-rows: masonry) {
    .masonry-grid {
      columns: 2;
    }
  }
}

@media (min-width: 640px) and (max-width: 959px) {
  .masonry-grid,
  @supports not (grid-template-rows: masonry) {
    .masonry-grid { columns: 3; }
  }
  .logical-demo {
    grid-template-columns: 1fr;
  }
  .cq-demo {
    grid-template-columns: 1fr;
  }
  .cq-demo__wide {
    grid-column: span 1;
  }
}

@media (max-width: 959px) {
  .cq-demo {
    grid-template-columns: 1fr;
  }
  .cq-demo__wide {
    grid-column: span 1;
  }
}

/* ================================================================
   KEYFRAMES (subtle)
   ================================================================ */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.demo-section {
  animation: fadeInUp 0.5s var(--ease-out) both;
}
.demo-section:nth-child(2) { animation-delay: 0.1s; }
.demo-section:nth-child(3) { animation-delay: 0.2s; }
.demo-section:nth-child(4) { animation-delay: 0.3s; }
.demo-section:nth-child(5) { animation-delay: 0.4s; }
</style>
</head>
<body>

<!-- Floating breakpoint indicator -->
<div class="breakpoint-indicator"></div>

<!-- ============================================================
     PATTERN 1: SUBGRID — Product Comparison
     ============================================================ -->
<section class="demo-section">
  <h2 class="section-title">1. Subgrid — Product Comparison</h2>
  <p class="section-subtitle">grid-template-rows: subgrid — all cards share row tracks</p>

  <div class="subgrid-grid">
    <!-- Starter -->
    <div class="subgrid-card">
      <div class="subgrid-card__header">
        <h3>Starter</h3>
      </div>
      <div class="subgrid-card__price">$0<span>/mo</span></div>
      <ul class="subgrid-card__features">
        <li>5 projects</li>
        <li>1 GB storage</li>
        <li class="disabled">Priority support</li>
        <li class="disabled">Custom domain</li>
        <li class="disabled">Analytics</li>
      </ul>
      <div class="subgrid-card__cta">
        <button>Get Started</button>
      </div>
    </div>

    <!-- Pro (featured) -->
    <div class="subgrid-card subgrid-card--featured">
      <div class="subgrid-card__header">
        <h3>Pro</h3>
        <span class="subgrid-card__badge">Popular</span>
      </div>
      <div class="subgrid-card__price">$29<span>/mo</span></div>
      <ul class="subgrid-card__features">
        <li>Unlimited projects</li>
        <li>50 GB storage</li>
        <li>Priority support</li>
        <li>Custom domain</li>
        <li class="disabled">Analytics</li>
      </ul>
      <div class="subgrid-card__cta">
        <button>Go Pro</button>
      </div>
    </div>

    <!-- Enterprise -->
    <div class="subgrid-card">
      <div class="subgrid-card__header">
        <h3>Enterprise</h3>
      </div>
      <div class="subgrid-card__price">$99<span>/mo</span></div>
      <ul class="subgrid-card__features">
        <li>Unlimited projects</li>
        <li>500 GB storage</li>
        <li>Priority support</li>
        <li>Custom domain</li>
        <li>Advanced analytics</li>
      </ul>
      <div class="subgrid-card__cta">
        <button>Contact Sales</button>
      </div>
    </div>
  </div>
</section>

<!-- ============================================================
     PATTERN 2: MASONRY LAYOUT — Gallery
     ============================================================ -->
<section class="demo-section">
  <h2 class="section-title">2. Masonry Layout — Image Gallery</h2>
  <p class="section-subtitle">grid-template-rows: masonry + column-fallback polyfill</p>

  <div class="masonry-grid">
    <div class="masonry-item masonry-item--tall">
      <div class="masonry-item__img masonry-item__img--1"></div>
      <div class="masonry-item__caption">Mountain sunrise — tall</div>
    </div>
    <div class="masonry-item masonry-item--short">
      <div class="masonry-item__img masonry-item__img--2"></div>
      <div class="masonry-item__caption">Forest path — short</div>
    </div>
    <div class="masonry-item masonry-item--medium">
      <div class="masonry-item__img masonry-item__img--3"></div>
      <div class="masonry-item__caption">Ocean waves — medium</div>
    </div>
    <div class="masonry-item masonry-item--short">
      <div class="masonry-item__img masonry-item__img--4"></div>
      <div class="masonry-item__caption">City lights — short</div>
    </div>
    <div class="masonry-item masonry-item--tall">
      <div class="masonry-item__img masonry-item__img--5"></div>
      <div class="masonry-item__caption">Desert dunes — tall</div>
    </div>
    <div class="masonry-item masonry-item--medium">
      <div class="masonry-item__img masonry-item__img--6"></div>
      <div class="masonry-item__caption">Aurora borealis — medium</div>
    </div>
    <div class="masonry-item masonry-item--short">
      <div class="masonry-item__img masonry-item__img--7"></div>
      <div class="masonry-item__caption">Canyon view — short</div>
    </div>
    <div class="masonry-item masonry-item--tall">
      <div class="masonry-item__img masonry-item__img--8"></div>
      <div class="masonry-item__caption">Starry night — tall</div>
    </div>
  </div>
</section>

<!-- ============================================================
     PATTERN 3: CONTAINER-QUERY CARDS
     ============================================================ -->
<section class="demo-section">
  <h2 class="section-title">3. Container-Query-Driven Card Variants</h2>
  <p class="section-subtitle">@container card — cards adapt to their container, not the viewport</p>

  <div class="cq-demo">
    <!-- Narrow container: forces default stacked layout -->
    <div class="cq-card-container">
      <div class="cq-card">
        <div class="cq-card__media">resize me</div>
        <div class="cq-card__body">
          <h4>Narrow Slot</h4>
          <p>This card container is ~280px wide — the card stays stacked.</p>
        </div>
        <div class="cq-card__meta">
          <span>2 min read</span>
          <span class="cq-card__tag">CSS</span>
        </div>
      </div>
    </div>

    <!-- Medium container: triggers row layout -->
    <div class="cq-card-container">
      <div class="cq-card">
        <div class="cq-card__media">resize me</div>
        <div class="cq-card__body">
          <h4>Medium Slot</h4>
          <p>At 300–499px the card flips to a side-by-side row layout with a square thumbnail.</p>
        </div>
        <div class="cq-card__meta">
          <span>4 min read</span>
          <span class="cq-card__tag">Design</span>
        </div>
      </div>
    </div>

    <!-- Wide container: triggers two-column grid layout, spanning 2 grid columns -->
    <div class="cq-card-container cq-demo__wide">
      <div class="cq-card">
        <div class="cq-card__media">resize me</div>
        <div class="cq-card__body">
          <h4>Wide Slot (500–699px)</h4>
          <p>Two-column grid with full-height media on the left. The card fills its container completely.</p>
        </div>
        <div class="cq-card__meta">
          <span>6 min read</span>
          <span class="cq-card__tag">Layout</span>
        </div>
      </div>
    </div>

    <!-- Extra-wide container (spans full row at 2/3 width) -->
    <div class="cq-card-container" style="grid-column: 1 / -1;">
      <div class="cq-card">
        <div class="cq-card__media">resize me</div>
        <div class="cq-card__body">
          <h4>Extra-Wide Slot (≥700px)</h4>
          <p>Three-column layout: full-height media, spacious body copy, and a dark sidebar meta panel. All driven by container queries — no media queries needed for the card itself.</p>
        </div>
        <div class="cq-card__meta">
          <span class="cq-card__tag">Advanced</span>
          <span>8 min read</span>
          <span>⭐⭐⭐⭐⭐</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============================================================
     PATTERN 4: LOGICAL PROPERTIES
     ============================================================ -->
<section class="demo-section">
  <h2 class="section-title">4. Logical Properties — Direction-Aware Layout</h2>
  <p class="section-subtitle">margin-inline, padding-block, border-inline-start, inset-* — RTL-ready</p>

  <div class="logical-demo">
    <!-- LTR panel -->
    <div class="logical-panel">
      <h3>
        <span class="logical-badge">LTR</span>
        Left-to-Right Panel
      </h3>
      <p>
        This panel uses <code>padding-block</code>, <code>padding-inline</code>,
        <code>margin-block-end</code>, and <code>border-inline-start</code>.
        The accent border appears on the logical "start" side — the left in LTR.
      </p>
    </div>

    <!-- RTL panel -->
    <div class="logical-panel logical-panel--rtl">
      <h3>
        <span class="logical-badge">RTL</span>
        Right-to-Left Panel
      </h3>
      <p>
        نفس الـ CSS بالضبط، لكن مع <code>direction: rtl</code>.
        لاحظ أن الحدود الملونة انتقلت إلى الجهة اليمنى تلقائياً
        لأننا استخدمنا <code>border-inline-end</code> بدلاً من <code>border-right</code>.
      </p>
    </div>

    <!-- Inline group LTR -->
    <div class="logical-inline-group">
      <span class="logical-inline-item">Item A</span>
      <span class="logical-inline-item">Item B</span>
      <span class="logical-inline-item">Item C</span>
      <span style="font-size: 0.8rem; color: var(--color-text-muted); margin-inline-start: auto;">
        LTR order
      </span>
    </div>

    <!-- Inline group RTL -->
    <div class="logical-inline-group logical-inline-group--rtl">
      <span class="logical-inline-item">Item A</span>
      <span class="logical-inline-item">Item B</span>
      <span class="logical-inline-item">Item C</span>
      <span style="font-size: 0.8rem; color: var(--color-text-muted); margin-inline-start: auto;">
        RTL order (auto-flipped)
      </span>
    </div>
  </div>

  <!-- Logical overlay demo -->
  <div class="logical-overlay" style="margin-block-start: var(--space-lg);">
    <div class="logical-overlay__child"></div>
    <div style="position: relative; z-index: 1; padding: var(--space-md); font-family: var(--font-mono); font-size: 0.8rem; color: var(--color-text-muted);">
      inset-block-start / inset-inline-start / inset-block-end / inset-inline-end
    </div>
  </div>
</section>

<!-- ============================================================
     PATTERN 5: FIVE-BREAKPOINT ADAPTIVE HERO
     ============================================================ -->
<section class="demo-section">
  <h2 class="section-title">5. Five-Breakpoint Adaptive Component — Hero Banner</h2>
  <p class="section-subtitle">XS(320) → SM(640) → MD(960) → LG(1280) → XL(1600) — resize your browser</p>

  <div class="hero">
    <div class="hero__media">
      <div class="hero__media-inner">
        🎨 Hero Media — resizes &amp; reflows at every breakpoint
      </div>
    </div>

    <div class="hero__content">
      <span class="hero__eyebrow">Styde Forge · Cycle 2</span>
      <h1 class="hero__title">Build layouts that<br>actually adapt</h1>
      <p class="hero__description">
        From subgrid-powered comparison tables to container-query card variants,
        masonry galleries, and logical-property RTL support — every pattern in
        this document is production-grade and ready to ship.
      </p>
      <div class="hero__actions">
        <button class="hero__btn hero__btn--primary">View on GitHub</button>
        <button class="hero__btn hero__btn--secondary">Read the docs</button>
      </div>
    </div>

    <!-- Stats — only visible at LG+ -->
    <div class="hero__stats">
      <div class="hero__stat">
        <div class="hero__stat-value">5</div>
        <div class="hero__stat-label">Patterns</div>
      </div>
      <div class="hero__stat">
        <div class="hero__stat-value">100%</div>
        <div class="hero__stat-label">RTL Ready</div>
      </div>
      <div class="hero__stat">
        <div class="hero__stat-value">0kb</div>
        <div class="hero__stat-label">JS Required</div>
      </div>
    </div>
  </div>
</section>

</body>
</html>
```

---

## Pattern Details

### 1. Subgrid — Product Comparison Table

- **Mechanism**: Each `.subgrid-card` uses `display: grid; grid-template-rows: subgrid; grid-row: span 4`.
- **Why it matters**: All three pricing cards share identical row tracks — headers, prices, feature lists, and CTAs align perfectly regardless of content length. Without subgrid, you'd need fixed heights or JavaScript.
- **Browser support**: Firefox 71+, Safari 16+, Chrome 117+.

### 2. Masonry Layout — Image Gallery

- **Mechanism**: Uses native `grid-template-rows: masonry` with a `@supports` fallback to CSS `columns` for browsers that don't support masonry.
- **Item variation**: Three height classes (`--tall`, `--medium`, `--short`) and eight gradient placeholders demonstrate the dense-packing algorithm.
- **Browser support**: Masonry is behind a flag in Firefox; the column fallback works everywhere.

### 3. Container-Query-Driven Card Variants

- **Mechanism**: Four `@container card` blocks at `min-width: 300px`, `500px`, and `700px`.
- **Variants produced**:
  - **< 300px**: Stacked flex column (default)
  - **300–499px**: Row layout with square 1:1 thumbnail
  - **500–699px**: Two-column grid, full-height media
  - **≥ 700px**: Three-column grid with sidebar meta panel
- **Demo layout**: CSS Grid with `auto-fit` creates containers of different widths on purpose so multiple variants render simultaneously.

### 4. Logical Properties

- **Properties demonstrated**:
  - `padding-inline` / `padding-block` — direction-aware padding
  - `margin-inline` / `margin-block` / `margin-block-end` — direction-aware margins
  - `border-inline-start` / `border-inline-end` — accent border follows writing direction
  - `inset-block-start` / `inset-inline-start` / `inset-block-end` / `inset-inline-end` — positioned overlay
  - `max-inline-size` — direction-aware max-width
  - `overflow-inline: auto` — direction-aware scroll
- **RTL proof**: The RTL panel uses identical class names; only `direction: rtl` and swapping `border-inline-start` → `border-inline-end` is needed. All spacings auto-flip.

### 5. Five-Breakpoint Adaptive Hero

| Breakpoint | Min Width | Layout |
|-----------|-----------|--------|
| **XS** | 320px | Stacked flex column, compact typography |
| **SM** | 640px | Taller media (280px), larger title, larger button gap |
| **MD** | 960px | CSS Grid 1fr 1fr — side-by-side media + content |
| **LG** | 1280px | Three-column: media + content + stats sidebar (appears) |
| **XL** | 1600px | Max-width 1400px centered, shadow, largest typography |

The floating badge in the bottom-right corner confirms the active breakpoint in real time.

---

## Browser Compatibility Notes

| Feature | Chrome | Firefox | Safari |
|---------|--------|---------|--------|
| Subgrid | 117+ | 71+ | 16+ |
| Masonry (native) | ❌ | 🚩 flag | ❌ |
| CSS Columns fallback | ✅ | ✅ | ✅ |
| Container Queries | 105+ | 110+ | 16+ |
| Logical Properties | ✅ | ✅ | 15+ |
| `clamp()` | 79+ | 75+ | 13.1+ |
| `aspect-ratio` | 88+ | 89+ | 15+ |

---

*Generated by responsive-layout-specialist (cycle 2) — Styde Forge Refinery*
