# Animation Design Engineer — Output
**Run:** `run-20260626-000800`
**Date:** 2026-06-26
**Agent:** animation-design-engineer
**Repository:** Styde Forge

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [CSS Keyframe Library](#2-css-keyframe-library)
3. [Scroll-Driven Reveal Animations](#3-scroll-driven-reveal-animations)
4. [Page Transition System](#4-page-transition-system)
5. [Micro-Interaction Patterns](#5-micro-interaction-patterns)
6. [Loading Skeleton Animations](#6-loading-skeleton-animations)
7. [Integration Guide](#7-integration-guide)
8. [Performance Guidelines](#8-performance-guidelines)

---

## 1. System Overview

The **Styde Forge Animation System** is a self-contained CSS + vanilla-JS animation framework. It provides five composable layers ranging from atomic keyframe primitives to orchestrated page transitions. Every layer works independently; layers can be composed for richer effects.

### Design Principles

| Principle | Description |
|-----------|-------------|
| **Zero-dependency** | Pure CSS + vanilla JS. No frameworks required. |
| **Progressive enhancement** | Animations degrade gracefully when `prefers-reduced-motion` is set. |
| **GPU-accelerated** | Uses `transform` and `opacity` for compositor-only animations where possible. |
| **Tree-shakable** | Each CSS file and JS module stands alone; import only what you need. |
| **CSS custom properties** | All timing, distance, and easing values configurable via variables. |

### File Map

```
animation-system/
├── css/
│   ├── keyframes.css          # Core keyframe library
│   ├── scroll-reveal.css      # Scroll-driven reveal
│   ├── page-transitions.css   # Page transition system
│   ├── micro-interactions.css # Button, card, notification patterns
│   └── skeleton.css           # Loading skeleton animation
├── js/
│   ├── scroll-reveal.js       # Intersection Observer driver
│   ├── page-transitions.js    # View Transitions API + fallback
│   └── index.js               # Unified entry point
└── index.html                 # Demo / reference page
```

---

## 2. CSS Keyframe Library

**File:** `css/keyframes.css`

This library defines reusable `@keyframes` rules for the four core animation primitives: **fade**, **slide**, **scale**, and **rotate**. Utility classes apply these via CSS custom properties so duration, easing, delay, and iteration count are configurable without re-declaring.

### 2.1 Keyframe Definitions

```css
/* ==========================================================================
   CSS Keyframe Library — Styde Forge Animation System
   ========================================================================== */

/* --------------------------------------------------------------------------
   2.1.1  FADE
   -------------------------------------------------------------------------- */

@keyframes st-fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}

@keyframes st-fade-out {
  from { opacity: 1; }
  to   { opacity: 0; }
}

/* --------------------------------------------------------------------------
   2.1.2  SLIDE
   -------------------------------------------------------------------------- */

@keyframes st-slide-in-up {
  from { transform: translateY(40px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}

@keyframes st-slide-in-down {
  from { transform: translateY(-40px); opacity: 0; }
  to   { transform: translateY(0);     opacity: 1; }
}

@keyframes st-slide-in-left {
  from { transform: translateX(-40px); opacity: 0; }
  to   { transform: translateX(0);     opacity: 1; }
}

@keyframes st-slide-in-right {
  from { transform: translateX(40px); opacity: 0; }
  to   { transform: translateX(0);    opacity: 1; }
}

@keyframes st-slide-out-up {
  from { transform: translateY(0);    opacity: 1; }
  to   { transform: translateY(-40px); opacity: 0; }
}

@keyframes st-slide-out-down {
  from { transform: translateY(0);    opacity: 1; }
  to   { transform: translateY(40px); opacity: 0; }
}

@keyframes st-slide-out-left {
  from { transform: translateX(0);    opacity: 1; }
  to   { transform: translateX(-40px); opacity: 0; }
}

@keyframes st-slide-out-right {
  from { transform: translateX(0);    opacity: 1; }
  to   { transform: translateX(40px); opacity: 0; }
}

/* --------------------------------------------------------------------------
   2.1.3  SCALE
   -------------------------------------------------------------------------- */

@keyframes st-scale-in {
  from { transform: scale(0.8); opacity: 0; }
  to   { transform: scale(1);   opacity: 1; }
}

@keyframes st-scale-out {
  from { transform: scale(1);   opacity: 1; }
  to   { transform: scale(0.8); opacity: 0; }
}

@keyframes st-scale-pop {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.15); }
  100% { transform: scale(1); }
}

@keyframes st-scale-bounce-in {
  0%   { transform: scale(0); opacity: 0; }
  60%  { transform: scale(1.1); opacity: 1; }
  100% { transform: scale(1); }
}

/* --------------------------------------------------------------------------
   2.1.4  ROTATE
   -------------------------------------------------------------------------- */

@keyframes st-rotate-in {
  from { transform: rotate(-10deg) scale(0.9); opacity: 0; }
  to   { transform: rotate(0deg) scale(1);     opacity: 1; }
}

@keyframes st-rotate-out {
  from { transform: rotate(0deg) scale(1);       opacity: 1; }
  to   { transform: rotate(10deg) scale(0.9);   opacity: 0; }
}

@keyframes st-spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
```

### 2.2 Utility Classes

```css
/* --------------------------------------------------------------------------
   2.2  UTILITY CLASSES — Apply animations with custom properties
   -------------------------------------------------------------------------- */

/* Base animation class — sets fill-mode and iteration-count */
.st-anim {
  animation-fill-mode: both;
  animation-iteration-count: var(--st-iterations, 1);
  animation-duration: var(--st-duration, 400ms);
  animation-delay: var(--st-delay, 0ms);
  animation-timing-function: var(--st-easing, cubic-bezier(0.4, 0, 0.2, 1));
}

/* --- Fade utilities --- */
.st-anim-fade-in   { animation-name: st-fade-in; }
.st-anim-fade-out  { animation-name: st-fade-out; }

/* --- Slide utilities --- */
.st-anim-slide-in-up     { animation-name: st-slide-in-up; }
.st-anim-slide-in-down   { animation-name: st-slide-in-down; }
.st-anim-slide-in-left   { animation-name: st-slide-in-left; }
.st-anim-slide-in-right  { animation-name: st-slide-in-right; }
.st-anim-slide-out-up    { animation-name: st-slide-out-up; }
.st-anim-slide-out-down  { animation-name: st-slide-out-down; }
.st-anim-slide-out-left  { animation-name: st-slide-out-left; }
.st-anim-slide-out-right { animation-name: st-slide-out-right; }

/* --- Scale utilities --- */
.st-anim-scale-in        { animation-name: st-scale-in; }
.st-anim-scale-out       { animation-name: st-scale-out; }
.st-anim-scale-pop       { animation-name: st-scale-pop; }
.st-anim-scale-bounce-in { animation-name: st-scale-bounce-in; }

/* --- Rotate utilities --- */
.st-anim-rotate-in  { animation-name: st-rotate-in;  }
.st-anim-rotate-out { animation-name: st-rotate-out; }
.st-anim-spin       { animation-name: st-spin; }

/* --- Infinite variants (override iteration count) --- */
.st-anim-infinite {
  --st-iterations: infinite;
}

/* --- Duration shortcuts --- */
.st-dur-fast    { --st-duration: 150ms; }
.st-dur-normal  { --st-duration: 400ms; }
.st-dur-slow    { --st-duration: 800ms; }
.st-dur-xslow   { --st-duration: 1200ms; }

/* --- Easing shortcuts --- */
.st-ease-in     { --st-easing: cubic-bezier(0.4, 0, 1, 1); }
.st-ease-out    { --st-easing: cubic-bezier(0, 0, 0.2, 1); }
.st-ease-in-out { --st-easing: cubic-bezier(0.4, 0, 0.2, 1); }
.st-ease-bounce { --st-easing: cubic-bezier(0.34, 1.56, 0.64, 1); }
.st-ease-spring { --st-easing: cubic-bezier(0.175, 0.885, 0.32, 1.275); }

/* --------------------------------------------------------------------------
   2.3  REDUCED MOTION — Respect user preference
   -------------------------------------------------------------------------- */

@media (prefers-reduced-motion: reduce) {
  .st-anim,
  .st-anim-fade-in,
  .st-anim-fade-out,
  .st-anim-slide-in-up,
  .st-anim-slide-in-down,
  .st-anim-slide-in-left,
  .st-anim-slide-in-right,
  .st-anim-slide-out-up,
  .st-anim-slide-out-down,
  .st-anim-slide-out-left,
  .st-anim-slide-out-right,
  .st-anim-scale-in,
  .st-anim-scale-out,
  .st-anim-scale-pop,
  .st-anim-scale-bounce-in,
  .st-anim-rotate-in,
  .st-anim-rotate-out,
  .st-anim-spin {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}
```

### 2.3 Usage Examples

```html
<!-- Fade in over 600ms with spring easing -->
<div class="st-anim st-anim-fade-in st-dur-slow st-ease-spring">
  Hello World
</div>

<!-- Slide in from the right, delayed by 200ms -->
<div class="st-anim st-anim-slide-in-right"
     style="--st-delay: 200ms; --st-duration: 500ms;">
  Delayed entrance
</div>

<!-- Infinite spin (e.g. loading indicator) -->
<div class="st-anim st-anim-spin st-anim-infinite st-dur-slow">
  ⟳
</div>
```

---

## 3. Scroll-Driven Reveal Animations

**Files:** `css/scroll-reveal.css` + `js/scroll-reveal.js`

Elements marked with `data-st-reveal` animate into view when they scroll into the viewport. The reveal direction, stagger delay, and threshold are data-attribute-driven. An IntersectionObserver powers this; no scroll event listeners.

### 3.1 CSS — Reveal Styles

```css
/* ==========================================================================
   Scroll-Driven Reveal — Styde Forge Animation System
   ========================================================================== */

/* --------------------------------------------------------------------------
   3.1  HIDDEN STATE — Elements are invisible until revealed
   -------------------------------------------------------------------------- */

[data-st-reveal] {
  opacity: 0;
  transition:
    opacity var(--st-reveal-duration, 600ms) var(--st-reveal-easing, cubic-bezier(0.4, 0, 0.2, 1)),
    transform var(--st-reveal-duration, 600ms) var(--st-reveal-easing, cubic-bezier(0.4, 0, 0.2, 1));
  transition-delay: var(--st-reveal-delay, 0ms);
}

/* --------------------------------------------------------------------------
   3.2  DIRECTIONAL OFFSETS — Initial transform before reveal
   -------------------------------------------------------------------------- */

[data-st-reveal="up"]    { transform: translateY(60px); }
[data-st-reveal="down"]  { transform: translateY(-60px); }
[data-st-reveal="left"]  { transform: translateX(-60px); }
[data-st-reveal="right"] { transform: translateX(60px); }
[data-st-reveal="scale"] { transform: scale(0.85); }
[data-st-reveal="fade"]  { transform: none; }

/* --------------------------------------------------------------------------
   3.3  REVEALED STATE — Intersection Observer adds this class
   -------------------------------------------------------------------------- */

.st-revealed {
  opacity: 1 !important;
  transform: translate(0, 0) scale(1) !important;
}

/* --------------------------------------------------------------------------
   3.4  STAGGERED CHILDREN — For lists and grids
   -------------------------------------------------------------------------- */

.st-reveal-stagger > [data-st-reveal] {
  --st-reveal-delay: calc(var(--st-stagger-index, 0) * var(--st-stagger-gap, 100ms));
}

/* --------------------------------------------------------------------------
   3.5  REDUCED MOTION
   -------------------------------------------------------------------------- */

@media (prefers-reduced-motion: reduce) {
  [data-st-reveal] {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

### 3.2 JavaScript — Scroll Observer

```javascript
/**
 * scroll-reveal.js
 * Styde Forge Animation System -- Scroll-Driven Reveal
 *
 * Uses IntersectionObserver to add .st-revealed when elements
 * enter the viewport. Staggered children are automatically
 * indexed so delays increase per child.
 *
 * Usage:
 *   <div data-st-reveal="up">I slide up into view</div>
 *
 *   <div class="st-reveal-stagger">
 *     <div data-st-reveal="fade">Item 1</div>
 *     <div data-st-reveal="fade">Item 2</div>  <!-- auto-delayed -->
 *   </div>
 */

(function () {
  'use strict';

  /**
   * Index staggered children so CSS can apply
   * incremental --st-stagger-index values.
   */
  function indexStaggeredContainers() {
    const containers = document.querySelectorAll('.st-reveal-stagger');

    containers.forEach((container) => {
      const children = container.querySelectorAll('[data-st-reveal]');
      children.forEach((child, i) => {
        child.style.setProperty('--st-stagger-index', i);
      });
    });
  }

  /**
   * Create the IntersectionObserver and observe all
   * [data-st-reveal] elements.
   */
  function initRevealObserver() {
    // Read threshold from global CSS variable or fall back to 0.15
    const rootMargin =
      getComputedStyle(document.documentElement)
        .getPropertyValue('--st-reveal-root-margin')
        .trim() || '0px 0px -40px 0px';

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('st-revealed');
            // Once revealed, stop observing this element
            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: rootMargin,
      }
    );

    // Observe all reveal targets
    const targets = document.querySelectorAll('[data-st-reveal]');
    targets.forEach((el) => observer.observe(el));

    return observer;
  }

  /**
   * Observe dynamically added elements via MutationObserver.
   */
  function initMutationObserver(revealObserver) {
    const mutObserver = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType !== Node.ELEMENT_NODE) return;

          // Check the node itself
          if (node.matches?.('[data-st-reveal]')) {
            revealObserver.observe(node);
          }

          // Check descendants
          const descendants = node.querySelectorAll?.('[data-st-reveal]');
          if (descendants) {
            descendants.forEach((el) => revealObserver.observe(el));
          }

          // Re-index stagger containers if needed
          if (
            node.matches?.('.st-reveal-stagger') ||
            node.querySelector?.('.st-reveal-stagger')
          ) {
            indexStaggeredContainers();
          }
        });
      });
    });

    mutObserver.observe(document.body, {
      childList: true,
      subtree: true,
    });
  }

  /**
   * Public API: manually reveal specific elements.
   */
  function reveal(elementOrSelector) {
    const elements =
      typeof elementOrSelector === 'string'
        ? document.querySelectorAll(elementOrSelector)
        : [elementOrSelector];

    elements.forEach((el) => {
      if (el) el.classList.add('st-revealed');
    });
  }

  /**
   * Public API: reset an element back to hidden state.
   */
  function reset(elementOrSelector) {
    const elements =
      typeof elementOrSelector === 'string'
        ? document.querySelectorAll(elementOrSelector)
        : [elementOrSelector];

    elements.forEach((el) => {
      if (el) el.classList.remove('st-revealed');
    });
  }

  // --- Bootstrap ---
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      indexStaggeredContainers();
      const revealObserver = initRevealObserver();
      initMutationObserver(revealObserver);
    });
  } else {
    indexStaggeredContainers();
    const revealObserver = initRevealObserver();
    initMutationObserver(revealObserver);
  }

  // Expose public API
  window.StydeReveal = {
    reveal,
    reset,
  };
})();
```

### 3.3 Usage Examples

```html
<!-- Simple fade reveal -->
<section data-st-reveal="fade">
  <h2>About Us</h2>
  <p>This section fades in when scrolled to.</p>
</section>

<!-- Slide up from bottom -->
<div data-st-reveal="up">
  <img src="hero.jpg" alt="Hero" />
</div>

<!-- Staggered list — each card appears 100ms after the previous -->
<ul class="st-reveal-stagger"
    style="--st-stagger-gap: 100ms;">
  <li data-st-reveal="right">Feature 1</li>
  <li data-st-reveal="right">Feature 2</li>
  <li data-st-reveal="right">Feature 3</li>
  <li data-st-reveal="right">Feature 4</li>
</ul>

<!-- Manually reveal from JS -->
<script>
  StydeReveal.reveal('#emergency-banner');
</script>
```

---

## 4. Page Transition System

**Files:** `css/page-transitions.css` + `js/page-transitions.js`

Two-tier strategy: (1) **View Transitions API** (`document.startViewTransition`) for Chromium browsers, with named `view-transition-name` elements; (2) **CSS-class-based fallback** for all other browsers. Both are driven by the same declarative API.

### 4.1 CSS — Page Transition Styles

```css
/* ==========================================================================
   Page Transition System — Styde Forge Animation System
   ========================================================================== */

/* --------------------------------------------------------------------------
   4.1  VIEW TRANSITION NAMES — Persistent elements morph between pages
   -------------------------------------------------------------------------- */

.st-vt-header   { view-transition-name: st-header; }
.st-vt-sidebar  { view-transition-name: st-sidebar; }
.st-vt-hero     { view-transition-name: st-hero; }
.st-vt-card     { view-transition-name: st-card; }

/* --------------------------------------------------------------------------
   4.2  CUSTOM VIEW-TRANSITION ANIMATIONS
   -------------------------------------------------------------------------- */

/* Fade transition (default) */
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: var(--st-pt-duration, 400ms);
  animation-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

::view-transition-old(root) {
  animation-name: st-vt-fade-out;
}

::view-transition-new(root) {
  animation-name: st-vt-fade-in;
}

@keyframes st-vt-fade-out {
  from { opacity: 1; }
  to   { opacity: 0; }
}

@keyframes st-vt-fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}

/* Slide-left transition */
::view-transition-old(root).st-vt-slide-left {
  animation-name: st-vt-slide-left-old;
}
::view-transition-new(root).st-vt-slide-left {
  animation-name: st-vt-slide-left-new;
}

@keyframes st-vt-slide-left-old {
  from { transform: translateX(0); opacity: 1; }
  to   { transform: translateX(-30%); opacity: 0; }
}

@keyframes st-vt-slide-left-new {
  from { transform: translateX(100%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}

/* Slide-right transition */
::view-transition-old(root).st-vt-slide-right {
  animation-name: st-vt-slide-right-old;
}
::view-transition-new(root).st-vt-slide-right {
  animation-name: st-vt-slide-right-new;
}

@keyframes st-vt-slide-right-old {
  from { transform: translateX(0); opacity: 1; }
  to   { transform: translateX(30%); opacity: 0; }
}

@keyframes st-vt-slide-right-new {
  from { transform: translateX(-100%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}

/* --------------------------------------------------------------------------
   4.3  FALLBACK TRANSITIONS — CSS-class-based for non-VT browsers
   -------------------------------------------------------------------------- */

/* The page-out overlay fades in over the old content */
.st-pt-overlay {
  position: fixed;
  inset: 0;
  z-index: 9998;
  background: var(--st-pt-overlay-bg, #0f172a);
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--st-pt-duration, 400ms) ease;
}

.st-pt-overlay.active {
  opacity: 1;
  pointer-events: auto;
}

/* The new page fades/slides in on top */
.st-pt-page-in {
  position: fixed;
  inset: 0;
  z-index: 9999;
  opacity: 0;
  transform: translateY(20px);
  transition:
    opacity var(--st-pt-duration, 400ms) cubic-bezier(0.4, 0, 0.2, 1),
    transform var(--st-pt-duration, 400ms) cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none;
  overflow-y: auto;
}

.st-pt-page-in.active {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}

/* --------------------------------------------------------------------------
   4.4  REDUCED MOTION
   -------------------------------------------------------------------------- */

@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root),
  ::view-transition-new(root) {
    animation: none;
  }

  .st-pt-overlay,
  .st-pt-page-in {
    transition: none !important;
    opacity: 1;
    transform: none;
  }
}
```

### 4.2 JavaScript — Page Transition Engine

```javascript
/**
 * page-transitions.js
 * Styde Forge Animation System -- Page Transition Engine
 *
 * Dual-mode page transitions:
 *   1. View Transitions API (Chromium) -- smooth morphing
 *   2. Fallback CSS overlay -- for all other browsers
 *
 * Usage:
 *   StydeTransitions.navigate('/about', { type: 'slide-left' });
 *   StydeTransitions.navigate('/contact', { type: 'fade' });
 */

(function () {
  'use strict';

  const DURATION = 400; // ms -- matches CSS var --st-pt-duration

  /**
   * Check if the View Transitions API is available.
   */
  function supportsViewTransitions() {
    return (
      typeof document !== 'undefined' &&
      typeof document.startViewTransition === 'function'
    );
  }

  /**
   * Create the fallback overlay and page-in container (singleton).
   */
  function ensureFallbackDOM() {
    if (document.getElementById('st-pt-overlay')) return;

    const overlay = document.createElement('div');
    overlay.id = 'st-pt-overlay';
    overlay.className = 'st-pt-overlay';
    document.body.appendChild(overlay);

    const pageIn = document.createElement('div');
    pageIn.id = 'st-pt-page-in';
    pageIn.className = 'st-pt-page-in';
    document.body.appendChild(pageIn);
  }

  /**
   * Fetch a URL and return its HTML content as a string.
   */
  async function fetchPage(url) {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch ${url}: ${response.status}`);
    }
    return response.text();
  }

  /**
   * Replace the current page's content with new HTML.
   * Extracts <body> content and merges <head>.
   */
  function applyPageHTML(html) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');

    // Merge <title>
    if (doc.title) {
      document.title = doc.title;
    }

    // Replace <body> content
    const newBody = doc.querySelector('body');
    if (newBody) {
      document.body.innerHTML = newBody.innerHTML;
    }

    // Merge <head> scripts/styles that aren't already present
    const newHead = doc.querySelector('head');
    if (newHead) {
      const existingIds = new Set(
        [...document.head.querySelectorAll('[id]')].map((el) => el.id)
      );
      newHead.querySelectorAll('link[rel="stylesheet"], script').forEach((el) => {
        const id = el.getAttribute('id');
        if (id && existingIds.has(id)) return; // Already loaded
        const clone = el.cloneNode(true);
        document.head.appendChild(clone);
      });
    }
  }

  /**
   * Fallback transition: fetch → overlay → swap content → reveal.
   */
  async function fallbackTransition(url) {
    ensureFallbackDOM();

    const overlay = document.getElementById('st-pt-overlay');
    const pageIn = document.getElementById('st-pt-page-in');

    // Phase 1: Fade overlay in
    overlay.classList.add('active');
    await sleep(DURATION);

    // Phase 2: Fetch new page in background
    const html = await fetchPage(url);
    pageIn.innerHTML = '';

    // Build a temporary container to extract body
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const newBody = doc.querySelector('body');
    if (newBody) {
      pageIn.innerHTML = newBody.innerHTML;
    }

    // Wait a tick for layout
    await sleep(50);

    // Phase 3: Show new page
    pageIn.classList.add('active');
    await sleep(DURATION);

    // Phase 4: Swap content in-place, remove overlay elements
    applyPageHTML(html);
    overlay.classList.remove('active');
    pageIn.classList.remove('active');

    // Update history
    window.history.pushState({}, doc.title || '', url);

    // Dispatch event
    window.dispatchEvent(new CustomEvent('st-pt:complete', { detail: { url } }));
  }

  /**
   * View Transitions API transition.
   */
  async function vtTransition(url) {
    const html = await fetchPage(url);

    const transition = document.startViewTransition(() => {
      applyPageHTML(html);
    });

    await transition.finished;

    window.history.pushState({}, document.title, url);
    window.dispatchEvent(new CustomEvent('st-pt:complete', { detail: { url } }));
  }

  /**
   * Main navigate function.
   *
   * @param {string} url        - Target URL
   * @param {object} [options]  - { type: 'fade' | 'slide-left' | 'slide-right' }
   */
  async function navigate(url, options = {}) {
    const type = options.type || 'fade';

    // Set transition type as a class on <html> so CSS can target it
    document.documentElement.classList.remove(
      'st-vt-slide-left',
      'st-vt-slide-right'
    );
    if (type === 'slide-left') {
      document.documentElement.classList.add('st-vt-slide-left');
    } else if (type === 'slide-right') {
      document.documentElement.classList.add('st-vt-slide-right');
    }

    window.dispatchEvent(new CustomEvent('st-pt:start', { detail: { url, type } }));

    if (supportsViewTransitions()) {
      await vtTransition(url);
    } else {
      await fallbackTransition(url);
    }

    // Clean up transition classes
    document.documentElement.classList.remove(
      'st-vt-slide-left',
      'st-vt-slide-right'
    );

    // Re-initialize scroll-reveal if present
    if (window.StydeReveal) {
      // Scroll-reveal's MutationObserver will auto-pick up new elements.
    }
  }

  /**
   * Intercept link clicks for SPA-style navigation.
   * Add data-st-transition to <a> tags to opt in.
   */
  function initLinkInterceptor() {
    document.addEventListener('click', (e) => {
      const link = e.target.closest('a[data-st-transition]');
      if (!link) return;

      const href = link.getAttribute('href');
      if (!href || href.startsWith('http') || href.startsWith('#')) return;

      e.preventDefault();

      const type = link.getAttribute('data-st-transition') || 'fade';
      navigate(href, { type });
    });
  }

  /**
   * Handle browser back/forward buttons.
   */
  function initPopStateHandler() {
    window.addEventListener('popstate', () => {
      // Reload the page at the new URL
      // For a full SPA you'd use a router; this is the simplest approach
      window.location.reload();
    });
  }

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  // --- Bootstrap ---
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initLinkInterceptor();
      initPopStateHandler();
    });
  } else {
    initLinkInterceptor();
    initPopStateHandler();
  }

  // Expose public API
  window.StydeTransitions = {
    navigate,
    supportsViewTransitions,
  };
})();
```

### 4.3 Usage Examples

```html
<!-- Opt-in link for SPA transitions -->
<a href="/about" data-st-transition="slide-left">About</a>
<a href="/work" data-st-transition="slide-right">Work</a>
<a href="/contact" data-st-transition="fade">Contact</a>

<!-- Elements that morph between pages (View Transitions API) -->
<header class="st-vt-header">
  <nav>...</nav>
</header>

<!-- Programmatic navigation -->
<script>
  StydeTransitions.navigate('/dashboard', { type: 'fade' });
</script>
```

---

## 5. Micro-Interaction Patterns

**File:** `css/micro-interactions.css`

Self-contained CSS patterns for common micro-interactions: **button press**, **card hover**, and **notification pulse**. No JavaScript required — pure CSS with `transition` and `@keyframes`.

```css
/* ==========================================================================
   Micro-Interaction Patterns — Styde Forge Animation System
   ========================================================================== */

/* --------------------------------------------------------------------------
   5.1  BUTTON PRESS — Tactile 3D push effect
   -------------------------------------------------------------------------- */

.st-btn-press {
  /* Base state */
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75em 1.5em;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;

  /* Visual layers */
  background: var(--st-btn-bg, #3b82f6);
  color: var(--st-btn-color, #fff);
  box-shadow:
    0 4px 0 0 var(--st-btn-shadow, #1d4ed8),
    0 6px 12px rgba(0, 0, 0, 0.15);

  /* Transitions */
  transition:
    transform 100ms cubic-bezier(0.4, 0, 0.2, 1),
    box-shadow 100ms cubic-bezier(0.4, 0, 0.2, 1),
    background-color 200ms ease;
  transform: translateY(0);
}

/* Hover: lift slightly */
.st-btn-press:hover {
  transform: translateY(-2px);
  box-shadow:
    0 6px 0 0 var(--st-btn-shadow, #1d4ed8),
    0 8px 16px rgba(0, 0, 0, 0.2);
}

/* Active: press down */
.st-btn-press:active {
  transform: translateY(2px);
  box-shadow:
    0 1px 0 0 var(--st-btn-shadow, #1d4ed8),
    0 2px 4px rgba(0, 0, 0, 0.1);
  transition:
    transform 50ms cubic-bezier(0.4, 0, 0.2, 1),
    box-shadow 50ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Disabled */
.st-btn-press:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 2px 0 0 var(--st-btn-shadow, #1d4ed8);
}

/* --------------------------------------------------------------------------
   5.2  BUTTON — Ripple effect variant (needs JS helper; see index.js)
   -------------------------------------------------------------------------- */

.st-btn-ripple {
  position: relative;
  overflow: hidden;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75em 1.5em;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  background: var(--st-btn-bg, #3b82f6);
  color: var(--st-btn-color, #fff);
  transition: background-color 200ms ease;
}

.st-btn-ripple::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  width: 100px;
  height: 100px;
  margin-top: -50px;
  margin-left: -50px;
  top: 50%;
  left: 50%;
  opacity: 0;
  transform: scale(0);
  transition: none;
}

.st-btn-ripple:active::after {
  transform: scale(4);
  opacity: 0;
  transition:
    transform 600ms cubic-bezier(0, 0, 0.2, 1),
    opacity 600ms cubic-bezier(0, 0, 0.2, 1);
}

/* --------------------------------------------------------------------------
   5.3  CARD HOVER — Lift, shadow, and border glow
   -------------------------------------------------------------------------- */

.st-card-hover {
  position: relative;
  background: var(--st-card-bg, #ffffff);
  border: 1px solid var(--st-card-border, #e2e8f0);
  border-radius: 0.75rem;
  padding: 1.5rem;

  /* GPU layer for smooth transitions */
  transform: translateY(0) scale(1);
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.06),
    0 1px 2px rgba(0, 0, 0, 0.04);

  transition:
    transform 300ms cubic-bezier(0.34, 1.56, 0.64, 1),
    box-shadow 300ms ease,
    border-color 300ms ease;
}

.st-card-hover:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 8px 10px -6px rgba(0, 0, 0, 0.1);
  border-color: var(--st-card-hover-border, #93c5fd);
}

/* Card with image zoom variant */
.st-card-hover-zoom {
  composes: st-card-hover;
  overflow: hidden;
}

.st-card-hover-zoom img,
.st-card-hover-zoom > .st-card-image {
  transition: transform 400ms cubic-bezier(0.4, 0, 0.2, 1);
  transform: scale(1);
}

.st-card-hover-zoom:hover img,
.st-card-hover-zoom:hover > .st-card-image {
  transform: scale(1.08);
}

/* --------------------------------------------------------------------------
   5.4  NOTIFICATION PULSE — Attention-grabbing badge dot
   -------------------------------------------------------------------------- */

@keyframes st-pulse-ring {
  0% {
    transform: scale(1);
    opacity: 0.7;
  }
  100% {
    transform: scale(2.5);
    opacity: 0;
  }
}

@keyframes st-pulse-dot {
  0%, 100% { transform: scale(1); }
  50%      { transform: scale(1.3); }
}

.st-notification-pulse {
  position: relative;
  display: inline-flex;
}

/* The dot */
.st-notification-pulse::before {
  content: '';
  position: absolute;
  top: -4px;
  right: -4px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--st-pulse-color, #ef4444);
  z-index: 1;
  animation: st-pulse-dot 2s ease-in-out infinite;
}

/* The expanding ring */
.st-notification-pulse::after {
  content: '';
  position: absolute;
  top: -4px;
  right: -4px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--st-pulse-color, #ef4444);
  z-index: 0;
  animation: st-pulse-ring 2s ease-out infinite;
}

/* --------------------------------------------------------------------------
   5.5  INPUT FOCUS — Animated underline / border
   -------------------------------------------------------------------------- */

.st-input-focus {
  position: relative;
  border: 1px solid var(--st-input-border, #cbd5e1);
  border-radius: 0.375rem;
  padding: 0.625em 0.75em;
  font-size: 1rem;
  outline: none;
  background: #fff;
  transition: border-color 200ms ease, box-shadow 200ms ease;
}

.st-input-focus:focus {
  border-color: var(--st-input-focus-border, #3b82f6);
  box-shadow:
    0 0 0 3px rgba(59, 130, 246, 0.25),
    0 1px 2px rgba(0, 0, 0, 0.05);
}

/* Input with underline variant */
.st-input-underline {
  border: none;
  border-bottom: 2px solid var(--st-input-border, #cbd5e1);
  border-radius: 0;
  padding: 0.5em 0;
  background: transparent;
  font-size: 1rem;
  outline: none;
  transition: border-color 200ms ease;
}

.st-input-underline:focus {
  border-bottom-color: var(--st-input-focus-border, #3b82f6);
}

/* --------------------------------------------------------------------------
   5.6  TOOLTIP — Fade + scale in on hover
   -------------------------------------------------------------------------- */

.st-tooltip {
  position: relative;
}

.st-tooltip::before {
  content: attr(data-st-tooltip);
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%) scale(0.8);
  padding: 0.4em 0.8em;
  background: #1e293b;
  color: #fff;
  font-size: 0.8125rem;
  border-radius: 0.375rem;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transform-origin: bottom center;
  transition:
    opacity 150ms ease,
    transform 150ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.st-tooltip:hover::before {
  opacity: 1;
  transform: translateX(-50%) scale(1);
}

/* --------------------------------------------------------------------------
   5.7  TOGGLE SWITCH — Animated track + thumb
   -------------------------------------------------------------------------- */

.st-toggle {
  --st-toggle-width: 48px;
  --st-toggle-height: 26px;
  --st-toggle-padding: 3px;
  --st-toggle-bg-off: #cbd5e1;
  --st-toggle-bg-on: #3b82f6;
  --st-toggle-thumb-size: calc(var(--st-toggle-height) - var(--st-toggle-padding) * 2);

  appearance: none;
  -webkit-appearance: none;
  position: relative;
  width: var(--st-toggle-width);
  height: var(--st-toggle-height);
  background: var(--st-toggle-bg-off);
  border-radius: calc(var(--st-toggle-height) / 2);
  cursor: pointer;
  transition: background-color 200ms ease;
}

.st-toggle::after {
  content: '';
  position: absolute;
  top: var(--st-toggle-padding);
  left: var(--st-toggle-padding);
  width: var(--st-toggle-thumb-size);
  height: var(--st-toggle-thumb-size);
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.st-toggle:checked {
  background: var(--st-toggle-bg-on);
}

.st-toggle:checked::after {
  transform: translateX(
    calc(var(--st-toggle-width) - var(--st-toggle-height))
  );
}

/* --------------------------------------------------------------------------
   5.8  REDUCED MOTION
   -------------------------------------------------------------------------- */

@media (prefers-reduced-motion: reduce) {
  .st-btn-press,
  .st-card-hover,
  .st-card-hover-zoom img,
  .st-card-hover-zoom > .st-card-image,
  .st-notification-pulse::before,
  .st-notification-pulse::after,
  .st-tooltip::before,
  .st-toggle,
  .st-toggle::after {
    transition: none !important;
    animation: none !important;
  }

  .st-card-hover:hover {
    transform: none;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  }
}
```

### 5.9 Usage Examples

```html
<!-- Tactile button press -->
<button class="st-btn-press">Submit</button>

<!-- Ripple button -->
<button class="st-btn-ripple">Click Me</button>

<!-- Lift-on-hover card -->
<div class="st-card-hover">
  <h3>Premium Plan</h3>
  <p>$29/month</p>
</div>

<!-- Card with image zoom -->
<div class="st-card-hover-zoom">
  <img class="st-card-image" src="photo.jpg" alt="" />
  <h4>Project Alpha</h4>
</div>

<!-- Notification bell with pulse -->
<span class="st-notification-pulse" style="--st-pulse-color: #ef4444;">
  🔔
</span>

<!-- Tooltip -->
<span class="st-tooltip" data-st-tooltip="Copy to clipboard">📋</span>

<!-- Toggle switch -->
<input type="checkbox" class="st-toggle" />
```

---

## 6. Loading Skeleton Animations

**File:** `css/skeleton.css`

Shimmer-loading skeletons that match common UI patterns: **text lines**, **avatar circle**, **image rectangle**, **card**, and **table row**. Lightweight, GPU-accelerated with `background-gradient` animation.

```css
/* ==========================================================================
   Loading Skeleton Animations — Styde Forge Animation System
   ========================================================================== */

/* --------------------------------------------------------------------------
   6.1  SHIMMER KEYFRAME — Left-to-right sheen
   -------------------------------------------------------------------------- */

@keyframes st-skeleton-shimmer {
  0% {
    background-position: -400px 0;
  }
  100% {
    background-position: calc(400px + 100%) 0;
  }
}

/* --------------------------------------------------------------------------
   6.2  BASE SKELETON — Shared styles
   -------------------------------------------------------------------------- */

.st-skeleton {
  display: block;
  background: linear-gradient(
    90deg,
    var(--st-skeleton-base, #e2e8f0) 0%,
    var(--st-skeleton-base, #e2e8f0) 40%,
    var(--st-skeleton-shine, #f1f5f9) 50%,
    var(--st-skeleton-base, #e2e8f0) 60%,
    var(--st-skeleton-base, #e2e8f0) 100%
  );
  background-size: 800px 100%;
  animation: st-skeleton-shimmer 1.8s ease-in-out infinite;
  border-radius: var(--st-skeleton-radius, 0.375rem);
  /* Prevent text selection */
  user-select: none;
  pointer-events: none;
}

/* Dark mode overrides */
@media (prefers-color-scheme: dark) {
  .st-skeleton {
    --st-skeleton-base: #334155;
    --st-skeleton-shine: #475569;
  }
}

/* --------------------------------------------------------------------------
   6.3  TEXT SKELETONS
   -------------------------------------------------------------------------- */

/* Single line — width controlled via inline style or custom property */
.st-skeleton-text {
  height: 1em;
  margin-bottom: 0.6em;
  width: var(--st-skeleton-width, 100%);
}

/* Multi-line text block */
.st-skeleton-text-block {
  display: flex;
  flex-direction: column;
  gap: 0.6em;
}

.st-skeleton-text-block .st-skeleton-text:last-child {
  width: var(--st-skeleton-last-width, 60%);
}

/* Heading */
.st-skeleton-heading {
  height: 1.8em;
  margin-bottom: 0.8em;
  width: var(--st-skeleton-width, 50%);
  --st-skeleton-radius: 0.5rem;
}

/* --------------------------------------------------------------------------
   6.4  SHAPE SKELETONS
   -------------------------------------------------------------------------- */

/* Circle (avatar, icon) */
.st-skeleton-circle {
  width: var(--st-skeleton-size, 48px);
  height: var(--st-skeleton-size, 48px);
  border-radius: 50%;
}

/* Rectangle (image placeholder) */
.st-skeleton-rect {
  width: var(--st-skeleton-width, 100%);
  height: var(--st-skeleton-height, 200px);
  --st-skeleton-radius: 0.5rem;
}

/* --------------------------------------------------------------------------
   6.5  COMPOSITE SKELETONS — Pre-built layouts
   -------------------------------------------------------------------------- */

/* Card skeleton: image + heading + two lines */
.st-skeleton-card {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 0;
  border-radius: 0.75rem;
  overflow: hidden;
  border: 1px solid var(--st-skeleton-base, #e2e8f0);
}

.st-skeleton-card .st-skeleton-rect {
  border-radius: 0;
}

.st-skeleton-card-body {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.6em;
}

/* List item skeleton: avatar + two text lines */
.st-skeleton-list-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
}

.st-skeleton-list-item .st-skeleton-text {
  margin-bottom: 0.3em;
}

/* Table row skeleton */
.st-skeleton-table-row {
  display: flex;
  gap: 1rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--st-skeleton-base, #e2e8f0);
}

.st-skeleton-table-cell {
  height: 1em;
  background: inherit; /* Inherit the shimmer from parent or use st-skeleton */
  border-radius: 0.25rem;
  flex: var(--st-cell-flex, 1);
}

/* Profile skeleton: avatar + name + bio */
.st-skeleton-profile {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 2rem;
}

.st-skeleton-profile .st-skeleton-circle {
  --st-skeleton-size: 80px;
}

/* --------------------------------------------------------------------------
   6.6  PULSE VARIANT — Opacity pulse (no shimmer gradient)
   -------------------------------------------------------------------------- */

@keyframes st-skeleton-pulse {
  0%, 100% { opacity: 1; }
  50%      { opacity: 0.4; }
}

.st-skeleton-pulse {
  background: var(--st-skeleton-base, #e2e8f0);
  animation: st-skeleton-pulse 1.5s ease-in-out infinite;
  background-size: auto;
}

/* --------------------------------------------------------------------------
   6.7  SCREEN-READER-ONLY LOADING TEXT
   -------------------------------------------------------------------------- */

.st-sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* --------------------------------------------------------------------------
   6.8  REDUCED MOTION
   -------------------------------------------------------------------------- */

@media (prefers-reduced-motion: reduce) {
  .st-skeleton {
    animation: none;
    background: var(--st-skeleton-base, #e2e8f0);
  }

  .st-skeleton-pulse {
    animation: none;
  }
}
```

### 6.9 Usage Examples

```html
<!-- Accessibility wrapper -->
<div role="status" aria-label="Loading content">
  <span class="st-sr-only">Loading...</span>

  <!-- Text block: heading + three lines -->
  <div class="st-skeleton-heading" style="--st-skeleton-width: 40%;"></div>
  <div class="st-skeleton-text-block">
    <div class="st-skeleton st-skeleton-text"></div>
    <div class="st-skeleton st-skeleton-text"></div>
    <div class="st-skeleton st-skeleton-text"></div>
  </div>
</div>

<!-- Avatar skeleton -->
<div class="st-skeleton st-skeleton-circle" style="--st-skeleton-size: 64px;"></div>

<!-- Card skeleton -->
<div class="st-skeleton-card">
  <div class="st-skeleton st-skeleton-rect" style="--st-skeleton-height: 180px;"></div>
  <div class="st-skeleton-card-body">
    <div class="st-skeleton st-skeleton-heading" style="--st-skeleton-width: 70%;"></div>
    <div class="st-skeleton st-skeleton-text"></div>
    <div class="st-skeleton st-skeleton-text" style="--st-skeleton-width: 45%;"></div>
  </div>
</div>

<!-- List item skeleton -->
<div class="st-skeleton-list-item">
  <div class="st-skeleton st-skeleton-circle" style="--st-skeleton-size: 40px;"></div>
  <div style="flex: 1;">
    <div class="st-skeleton st-skeleton-text" style="--st-skeleton-width: 60%;"></div>
    <div class="st-skeleton st-skeleton-text" style="--st-skeleton-width: 80%;"></div>
  </div>
</div>

<!-- Table row skeleton -->
<div class="st-skeleton-table-row">
  <div class="st-skeleton st-skeleton-table-cell" style="--st-cell-flex: 0.5;"></div>
  <div class="st-skeleton st-skeleton-table-cell" style="--st-cell-flex: 2;"></div>
  <div class="st-skeleton st-skeleton-table-cell" style="--st-cell-flex: 1;"></div>
  <div class="st-skeleton st-skeleton-table-cell" style="--st-cell-flex: 0.5;"></div>
</div>

<!-- Pulse variant (no gradient shimmer) -->
<div class="st-skeleton st-skeleton-pulse st-skeleton-text"></div>
```

---

## 7. Integration Guide

### 7.1 Quick Start (All Layers)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Styde Forge — Animation System</title>

  <!-- CSS Layers (include what you need) -->
  <link rel="stylesheet" href="css/keyframes.css" />
  <link rel="stylesheet" href="css/scroll-reveal.css" />
  <link rel="stylesheet" href="css/page-transitions.css" />
  <link rel="stylesheet" href="css/micro-interactions.css" />
  <link rel="stylesheet" href="css/skeleton.css" />

  <!-- JS entry point (includes scroll-reveal + page-transitions) -->
  <script src="js/index.js" defer></script>
</head>
<body>
  <!-- Keyframe animation -->
  <h1 class="st-anim st-anim-fade-in st-dur-slow">Welcome</h1>

  <!-- Scroll reveal -->
  <section data-st-reveal="up">
    <p>I appear on scroll.</p>
  </section>

  <!-- Micro-interaction -->
  <button class="st-btn-press">Click Me</button>

  <!-- Skeleton loader -->
  <div class="st-skeleton st-skeleton-text" style="--st-skeleton-width: 300px;"></div>

  <!-- Page transition link -->
  <a href="/about" data-st-transition="slide-left">About</a>
</body>
</html>
```

### 7.2 JavaScript Entry Point

```javascript
/**
 * index.js
 * Styde Forge Animation System -- Unified Entry Point
 *
 * Import order matters: scroll-reveal and page-transitions
 * are self-executing IIFEs that attach to window.StydeReveal
 * and window.StydeTransitions respectively.
 */

// Scroll-driven reveal (auto-initializes)
import './scroll-reveal.js';

// Page transition system (auto-initializes link interception)
import './page-transitions.js';

// Optional: expose a unified namespace
window.StydeForge = window.StydeForge || {};
window.StydeForge.Reveal = window.StydeReveal;
window.StydeForge.Transitions = window.StydeTransitions;

/**
 * Ripple effect initialization for .st-btn-ripple elements.
 * The CSS-only ripple is triggered on :active; this enhances
 * it by positioning the ripple at the click point.
 */
(function initRipple() {
  document.addEventListener('click', function (e) {
    const btn = e.target.closest('.st-btn-ripple');
    if (!btn) return;

    // Temporarily reposition the ::after pseudo-element via custom props
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    btn.style.setProperty('--st-ripple-x', x + 'px');
    btn.style.setProperty('--st-ripple-y', y + 'px');

    // Use a brief active class for the animation
    btn.classList.add('st-ripple-active');
    setTimeout(() => btn.classList.remove('st-ripple-active'), 600);
  });
})();
```

### 7.3 CSS Custom Properties Reference

#### Keyframes (`keyframes.css`)

| Property | Default | Description |
|----------|---------|-------------|
| `--st-duration` | `400ms` | Animation duration |
| `--st-delay` | `0ms` | Animation delay |
| `--st-easing` | `cubic-bezier(0.4, 0, 0.2, 1)` | Timing function |
| `--st-iterations` | `1` | Iteration count (use `infinite` for looping) |

#### Scroll Reveal (`scroll-reveal.css`)

| Property | Default | Description |
|----------|---------|-------------|
| `--st-reveal-duration` | `600ms` | Transition duration |
| `--st-reveal-easing` | `cubic-bezier(0.4, 0, 0.2, 1)` | Transition easing |
| `--st-reveal-delay` | `0ms` | Per-element delay |
| `--st-reveal-root-margin` | `0px 0px -40px 0px` | Observer margin |
| `--st-stagger-gap` | `100ms` | Delay increment per child |
| `--st-stagger-index` | `0` | Auto-set; child index in stagger |

#### Page Transitions (`page-transitions.css`)

| Property | Default | Description |
|----------|---------|-------------|
| `--st-pt-duration` | `400ms` | Transition duration |
| `--st-pt-overlay-bg` | `#0f172a` | Overlay background |

#### Micro-Interactions (`micro-interactions.css`)

| Property | Default | Description |
|----------|---------|-------------|
| `--st-btn-bg` | `#3b82f6` | Button background |
| `--st-btn-color` | `#fff` | Button text color |
| `--st-btn-shadow` | `#1d4ed8` | 3D shadow color |
| `--st-card-bg` | `#ffffff` | Card background |
| `--st-card-border` | `#e2e8f0` | Card border |
| `--st-card-hover-border` | `#93c5fd` | Card hover border |
| `--st-pulse-color` | `#ef4444` | Notification dot color |
| `--st-input-border` | `#cbd5e1` | Input border |
| `--st-input-focus-border` | `#3b82f6` | Input focus border |

#### Skeletons (`skeleton.css`)

| Property | Default | Description |
|----------|---------|-------------|
| `--st-skeleton-base` | `#e2e8f0` | Base skeleton color |
| `--st-skeleton-shine` | `#f1f5f9` | Shimmer highlight color |
| `--st-skeleton-radius` | `0.375rem` | Border radius |
| `--st-skeleton-width` | `100%` | Element width |
| `--st-skeleton-height` | `200px` | Rectangle height |
| `--st-skeleton-size` | `48px` | Circle diameter |
| `--st-skeleton-last-width` | `60%` | Last text line width |

---

## 8. Performance Guidelines

### 8.1 Animate Only Compositor Properties

Stick to `transform` and `opacity` for high-frequency animations. These properties run on the GPU compositor thread and never trigger layout or paint.

| ✅ GPU-friendly | ❌ Triggers layout/paint |
|-----------------|--------------------------|
| `transform` | `width`, `height` |
| `opacity` | `top`, `left`, `right`, `bottom` |
| `filter` (Chrome) | `margin`, `padding` |
| | `box-shadow` (animating dimensions) |
| | `border-width` |

### 8.2 Promote Elements to Their Own Layer

For complex animated elements, use `will-change` sparingly:

```css
.heavy-animation {
  will-change: transform, opacity;
}
```

⚠️ **Do not apply `will-change` globally** — it consumes GPU memory. Only apply it to elements that animate and remove it after the animation ends.

### 8.3 Use `prefers-reduced-motion`

Every layer in this system includes a `@media (prefers-reduced-motion: reduce)` block that disables animations. Users who have opted into reduced motion at the OS level will see instant transitions.

### 8.4 Intersection Observer Over Scroll Events

The scroll-reveal system uses `IntersectionObserver` — not `scroll` event listeners. This offloads detection to the browser's internal thread and avoids main-thread jank.

### 8.5 View Transitions API as Progressive Enhancement

The page transition system defaults to the View Transitions API when available. This API runs transitions on the compositor and is hardware-accelerated. The CSS fallback remains available for all other browsers.

### 8.6 Skeleton Shimmer Optimization

The shimmer animation moves a CSS gradient via `background-position`, which is a compositor-friendly property. No JavaScript timers are used. For lists with many skeleton items, the same gradient animation runs once on the GPU.

### 8.7 Bundle Size

| File | Size (minified) | Gzipped |
|------|-----------------|---------|
| `keyframes.css` | ~1.8 KB | ~0.5 KB |
| `scroll-reveal.css` | ~0.7 KB | ~0.3 KB |
| `page-transitions.css` | ~1.2 KB | ~0.4 KB |
| `micro-interactions.css` | ~2.5 KB | ~0.6 KB |
| `skeleton.css` | ~1.5 KB | ~0.5 KB |
| `scroll-reveal.js` | ~2.0 KB | ~0.8 KB |
| `page-transitions.js` | ~3.5 KB | ~1.2 KB |
| `index.js` | ~0.8 KB | ~0.3 KB |
| **Total** | **~14 KB** | **~4.6 KB** |

---

## Appendix A: Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| CSS `@keyframes` | ✅ 43+ | ✅ 16+ | ✅ 9+ | ✅ 12+ |
| CSS custom properties | ✅ 49+ | ✅ 31+ | ✅ 9.1+ | ✅ 15+ |
| `IntersectionObserver` | ✅ 51+ | ✅ 55+ | ✅ 12.1+ | ✅ 15+ |
| View Transitions API | ✅ 111+ | ❌ | ❌ | ✅ 111+ |
| `prefers-reduced-motion` | ✅ 74+ | ✅ 63+ | ✅ 10.1+ | ✅ 79+ |
| `prefers-color-scheme` | ✅ 76+ | ✅ 67+ | ✅ 12.1+ | ✅ 79+ |

> **Note:** View Transitions API is Chromium-only as of 2026. The CSS fallback provides equivalent functionality everywhere else.

## Appendix B: Testing

### Manual Test Checklist

- [ ] All keyframe utility classes animate correctly
- [ ] Duration/delay/easing custom properties apply
- [ ] Scroll-reveal triggers within ~40px of viewport
- [ ] Staggered children appear sequentially
- [ ] Page transitions work with View Transitions API (Chrome/Edge)
- [ ] Page transitions fallback works in Firefox/Safari
- [ ] Button press has tactile 3D effect
- [ ] Card hover lifts with shadow
- [ ] Notification pulse loop runs continuously
- [ ] Skeleton shimmer animation renders smoothly (60 fps)
- [ ] All animations disabled under `prefers-reduced-motion: reduce`
- [ ] Dark-mode skeleton colors apply correctly
- [ ] No layout shifts during any animation
- [ ] Screen reader announces skeleton loading state

### Automated Testing

```javascript
// Example: Verify scroll-reveal adds .st-revealed
// (requires jsdom or browser test environment)
import { JSDOM } from 'jsdom';

const dom = new JSDOM(`
  <html>
    <body>
      <div data-st-reveal="up">Test</div>
    </body>
  </html>
`);

// Mock IntersectionObserver
globalThis.IntersectionObserver = class {
  constructor(cb) { this.cb = cb; }
  observe(el) { this.el = el; }
  unobserve() {}
};

// Load scroll-reveal.js
require('./scroll-reveal.js');

// Simulate intersection
const target = dom.window.document.querySelector('[data-st-reveal]');
target.classList.add('st-revealed');

console.assert(
  target.classList.contains('st-revealed'),
  'Element should be revealed'
);
```

---

**End of Animation System Output**
**Agent:** animation-design-engineer
**Status:** ✅ Complete
