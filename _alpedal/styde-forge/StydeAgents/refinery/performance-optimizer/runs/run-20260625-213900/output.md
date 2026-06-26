# Web Performance Optimization Guide

> **Author:** Performance Optimizer Agent  
> **Run:** `run-20260625-213900`  
> **Target Stack:** Next.js (App Router) / Vite + React  
> **Last Updated:** June 2026

---

## Table of Contents

1. [Core Web Vitals: Measurement & Improvement](#1-core-web-vitals-measurement--improvement)
   - [1.1 Largest Contentful Paint (LCP)](#11-largest-contentful-paint-lcp)
   - [1.2 Interaction to Next Paint (INP)](#12-interaction-to-next-paint-inp)
   - [1.3 Cumulative Layout Shift (CLS)](#13-cumulative-layout-shift-cls)
   - [1.4 Monitoring & Measurement Toolchain](#14-monitoring--measurement-toolchain)
2. [JavaScript Bundle Optimization](#2-javascript-bundle-optimization)
   - [2.1 Code Splitting](#21-code-splitting)
   - [2.2 Tree Shaking](#22-tree-shaking)
   - [2.3 Lazy Loading](#23-lazy-loading)
3. [Image Optimization](#3-image-optimization)
   - [3.1 Modern Formats: WebP & AVIF](#31-modern-formats-webp--avif)
   - [3.2 Responsive Images with `srcset` & `<picture>`](#32-responsive-images-with-srcset--picture)
   - [3.3 Image Lazy Loading](#33-image-lazy-loading)
4. [Caching Strategies](#4-caching-strategies)
   - [4.1 Browser Cache](#41-browser-cache)
   - [4.2 CDN Caching](#42-cdn-caching)
   - [4.3 API & Data Caching](#43-api--data-caching)
5. [Font Loading Optimization](#5-font-loading-optimization)
6. [Performance Budget Template](#6-performance-budget-template)
7. [Appendix: Quick-Reference Checklists](#7-appendix-quick-reference-checklists)

---

## 1. Core Web Vitals: Measurement & Improvement

Core Web Vitals are the unified signals Google uses to quantify real-world user experience. The three pillars:

| Metric | What It Measures | "Good" Threshold |
|--------|-----------------|-------------------|
| **LCP** | Loading — when the largest content element becomes visible | ≤ 2.5 s |
| **INP** | Interactivity — the worst-case latency of a user interaction | ≤ 200 ms |
| **CLS** | Visual stability — how much the page layout shifts unexpectedly | ≤ 0.1 |

---

### 1.1 Largest Contentful Paint (LCP)

#### What triggers LCP?

The browser considers these elements as LCP candidates (largest one wins):
- `<img>` elements
- `<image>` inside `<svg>`
- `<video>` poster images
- Elements with CSS `background-image: url(...)`
- Block-level text nodes inside a containing block

#### Measurement — RUM (Real User Monitoring)

```js
// web-vitals library — the gold standard
import {onLCP} from 'web-vitals';

onLCP((metric) => {
  // Send to your analytics endpoint
  analytics.track('web_vital', {
    name: 'LCP',
    value: metric.value,
    rating: metric.rating,     // 'good' | 'needs-improvement' | 'poor'
    delta: metric.delta,
    id: metric.id,
    entries: metric.entries,   // raw PerformanceEntry objects
  });
});
```

#### Measurement — Lab (Synthetic)

```bash
# Lighthouse CLI audit
npx lighthouse https://example.com --view --preset=desktop

# Chrome DevTools: Performance panel → record a reload
# Use "Web Vitals" overlay in the timeline
```

#### LCP Sub-Parts Breakdown

LCP = **TTFB** + **Resource Load Delay** + **Resource Load Duration** + **Element Render Delay**

| Phase | What Happens | Fix |
|-------|-------------|-----|
| TTFB | Server response time | CDN, edge rendering, serverless |
| Load Delay | Time before browser discovers the LCP resource | Preload, no lazy-load on LCP |
| Load Duration | Network download time | Compress, modern formats, CDN |
| Render Delay | Time from download to paint | Avoid render-blocking CSS/JS |

#### LCP Improvement Strategies

**Strategy 1: Eliminate render-blocking resources**

```html
<!-- Inline critical CSS, defer the rest -->
<head>
  <style>
    /* Critical-path CSS: above-the-fold styles */
    .hero { ... }
    nav { ... }
  </style>
  <link rel="preload" href="/styles/full.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="/styles/full.css"></noscript>
</head>
```

**Strategy 2: Preload the LCP image**

```html
<!-- Tell the browser to fetch the hero image ASAP -->
<link rel="preload" as="image" href="/hero-desktop.webp" 
      imagesrcset="/hero-640.webp 640w, /hero-1080.webp 1080w, /hero-1920.webp 1920w"
      imagesizes="100vw"
      fetchpriority="high">
```

**Strategy 3: Priority Hints**

```html
<!-- Signal to the browser this is the most important image -->
<img src="hero.webp" fetchpriority="high" loading="eager" alt="Hero">
```

**Strategy 4: Next.js App Router — ensure LCP image is not lazy-loaded**

```tsx
// ❌ Bad: LCP image lazy-loaded by default in Next.js
import Image from 'next/image';
<Image src="/hero.jpg" width={1920} height={1080} alt="Hero" />

// ✅ Good: Explicitly set priority and disable lazy loading
<Image 
  src="/hero.jpg" 
  width={1920} 
  height={1080} 
  alt="Hero"
  priority           // = loading="eager" + fetchpriority="high" + preload
  sizes="100vw"
/>
```

---

### 1.2 Interaction to Next Paint (INP)

INP replaced FID in March 2024. It measures the latency of **all** interactions (click, tap, keypress) and reports the **worst one** (or close to it — typically the 98th percentile).

#### Measurement

```js
import {onINP} from 'web-vitals';

onINP((metric) => {
  console.log(`INP: ${metric.value}ms — rating: ${metric.rating}`);
  // metric.entries contains the individual event entries
  // metric.attribution gives you the interaction target info (Chrome only)
});
```

#### Understanding Long Tasks

INP is driven by **long tasks** (>50 ms) on the main thread. The browser can't respond to user input while the main thread is blocked.

```
User clicks ──┐
              │ [ Input Delay: waiting for main thread ]
              │ [ Processing Time: event handlers run     ]
              │ [ Presentation Delay: next frame painted  ]
              └──> INP = sum of the above
```

#### INP Improvement Strategies

**Strategy 1: Break up long tasks with `scheduler.yield()` or `setTimeout`**

```js
// ❌ Bad: one monolithic 200ms task
function processLargeDataset(items) {
  items.forEach(item => heavyTransform(item));
  updateUI();
}

// ✅ Good: yield to the browser every 50ms
async function processLargeDataset(items) {
  for (let i = 0; i < items.length; i++) {
    heavyTransform(items[i]);
    if (i % 5 === 0) {
      // Yield to the main thread
      await new Promise(resolve => setTimeout(resolve, 0));
      // Or use the newer scheduler API:
      // await scheduler.yield();
    }
  }
  updateUI();
}
```

**Strategy 2: Use `scheduler.postTask()` (Chrome)**

```js
// Schedule work with explicit priorities
scheduler.postTask(() => updateCriticalUI(), { priority: 'user-blocking' });
scheduler.postTask(() => fetchRecommendations(), { priority: 'background' });
```

**Strategy 3: Debounce / throttle expensive event handlers**

```js
// Debounce: wait until user stops
function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// Throttle: fire at most once per interval
function throttle(fn, limit) {
  let inThrottle = false;
  return (...args) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// Usage
input.addEventListener('input', debounce(handleSearch, 300));
```

**Strategy 4: Web Workers for heavy computation**

```js
// main.js
const worker = new Worker('/workers/data-processor.js');
worker.postMessage(largeArray);
worker.onmessage = (e) => {
  const result = e.data;
  updateUI(result);  // lightweight DOM update
};

// workers/data-processor.js
self.onmessage = (e) => {
  const result = e.data.map(expensiveOperation);
  self.postMessage(result);
};
```

**Strategy 5: `useDeferredValue` / `useTransition` in React**

```tsx
import { useState, useDeferredValue, useTransition } from 'react';

// Approach A: useDeferredValue — defer re-render of expensive list
function SearchPage() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  
  return (
    <>
      <input 
        value={query} 
        onChange={e => setQuery(e.target.value)} 
        placeholder="Search..."
      />
      {/* This re-renders with lower priority */}
      <ExpensiveSearchResults query={deferredQuery} />
    </>
  );
}

// Approach B: useTransition — mark state update as non-urgent
function TabSwitcher() {
  const [tab, setTab] = useState('home');
  const [isPending, startTransition] = useTransition();
  
  const handleTabChange = (newTab) => {
    startTransition(() => setTab(newTab));
  };
  
  return (
    <>
      <TabBar onTabChange={handleTabChange} />
      {isPending && <Spinner />}
      <TabContent tab={tab} />
    </>
  );
}
```

---

### 1.3 Cumulative Layout Shift (CLS)

CLS measures **unexpected** layout shifts during the page lifecycle. A layout shift occurs when a visible element changes its start position between frames.

```
CLS Score = impact fraction × distance fraction

Impact fraction: what % of the viewport was affected?
Distance fraction: how far did the element move (as % of viewport)?
```

#### Measurement

```js
import {onCLS} from 'web-vitals';

onCLS((metric) => {
  console.log(`CLS: ${metric.value} — rating: ${metric.rating}`);
  // metric.entries contains LayoutShift entries with attribution
});
```

#### Common CLS Culprits

| Cause | Fix |
|-------|-----|
| Images without dimensions | Always set `width`/`height` or `aspect-ratio` |
| Dynamically injected content (ads, embeds) | Reserve space with `min-height` |
| Web fonts causing FOIT/FOUT | Use `font-display: swap` + reserve space |
| Late-loading CSS | Inline critical CSS |
| Animations using `top`/`left` | Use `transform` instead |

#### CLS Fixes

**Fix 1: Always reserve space for images**

```css
/* Reserve aspect ratio so the browser knows the height up front */
img {
  max-width: 100%;
  height: auto;
  aspect-ratio: attr(width) / attr(height);
}
```

```html
<!-- Explicit dimensions on every image -->
<img src="photo.jpg" width="800" height="600" alt="..." loading="lazy">

<!-- Next.js Image automatically reserves space -->
<Image src="/photo.jpg" width={800} height={600} alt="..." />
<!-- Or use fill with a sized container -->
<div style={{ position: 'relative', width: '100%', aspectRatio: '4/3' }}>
  <Image src="/photo.jpg" fill alt="..." />
</div>
```

**Fix 2: Reserve space for embeds/iframes/ad slots**

```css
.ad-slot {
  min-height: 250px;  /* Reserve space before ad loads */
  background: #f0f0f0;
}
.ad-slot:empty::after {
  content: "Advertisement";
  display: flex;
  align-items: center;
  justify-content: center;
  height: 250px;
  color: #999;
}
```

**Fix 3: Font loading — prevent layout shift**

```css
/* Reserve fallback font metrics using size-adjust */
@font-face {
  font-family: 'MyWebFont';
  src: url('/fonts/myfont.woff2') format('woff2');
  font-display: swap;
}

/* Match fallback font metrics to web font */
body {
  font-family: 'MyWebFont', 'Fallback Font', sans-serif;
}

/* CSS font-size-adjust to match x-height */
body {
  font-size-adjust: 0.5;  /* Ratio of x-height to font-size */
}
```

**Fix 4: Animate with `transform`, not layout properties**

```css
/* ❌ Bad: triggers layout recalculation */
.modal {
  transition: top 0.3s;
  top: 100%;
}
.modal.open { top: 0; }

/* ✅ Good: GPU-composited, no layout shift */
.modal {
  transition: transform 0.3s;
  transform: translateY(100%);
}
.modal.open { transform: translateY(0); }
```

---

### 1.4 Monitoring & Measurement Toolchain

#### Lab Data (Synthetic Testing)

| Tool | Use Case |
|------|----------|
| **Lighthouse** | Page-level audit during CI or dev |
| **Chrome DevTools Performance Panel** | Deep-dive into individual page loads |
| **WebPageTest** | Multi-location, multi-device testing |
| **PageSpeed Insights** | Combines lab + CrUX field data |

**Lighthouse CI — automated performance gates:**

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [pull_request]
jobs:
  lhci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci && npm run build
      - run: |
          npm install -g @lhci/cli
          lhci autorun --collect.url=http://localhost:3000 \
            --upload.target=temporary-public-storage \
            --assert.preset=lighthouse:recommended
```

**Lighthouse CI assert config (`.lighthouserc.js`):**

```js
module.exports = {
  ci: {
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        // Custom thresholds
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'interactive': ['warn', { maxNumericValue: 3500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['warn', { maxNumericValue: 300 }],
        // Bundle size checks
        'resource-summary:script:size': ['error', { maxNumericValue: 300 * 1024 }],
        'resource-summary:stylesheet:size': ['warn', { maxNumericValue: 80 * 1024 }],
      },
    },
  },
};
```

#### Field Data (RUM)

**web-vitals + custom analytics:**

```js
// analytics.js
import {onCLS, onINP, onLCP, onFCP, onTTFB} from 'web-vitals';

function sendToAnalytics({name, value, rating, delta, id}) {
  // Batch and send to your analytics backend
  navigator.sendBeacon(
    '/api/vitals',
    JSON.stringify({
      name,
      value: Math.round(value),
      rating,
      delta: Math.round(delta),
      id,
      page: location.pathname,
      timestamp: Date.now(),
    })
  );
}

onCLS(sendToAnalytics);
onINP(sendToAnalytics);
onLCP(sendToAnalytics);
onFCP(sendToAnalytics);
onTTFB(sendToAnalytics);
```

**Vercel Analytics / Next.js Speed Insights (zero-config):**

```tsx
// app/layout.tsx
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  );
}
```

---

## 2. JavaScript Bundle Optimization

### 2.1 Code Splitting

Code splitting breaks your JS bundle into smaller chunks loaded on demand. This reduces the initial payload.

#### Dynamic `import()` — the foundation

```js
// ❌ Static import — always in the main bundle
import HeavyChart from './components/HeavyChart';

// ✅ Dynamic import — loaded only when needed
const HeavyChart = await import('./components/HeavyChart');
```

#### React `lazy()` + `Suspense`

```tsx
import { lazy, Suspense } from 'react';

// Route-level code splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));
const Analytics = lazy(() => import('./pages/Analytics'));

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/analytics" element={<Analytics />} />
      </Routes>
    </Suspense>
  );
}
```

#### Component-level splitting — only load below the fold

```tsx
import { lazy, Suspense } from 'react';

// Heavy component that's not in the initial viewport
const InteractiveMap = lazy(() => import('./InteractiveMap'));
const VideoPlayer = lazy(() => import('./VideoPlayer'));

function HomePage() {
  return (
    <div>
      <HeroSection />
      <Suspense fallback={<div className="h-[600px] bg-gray-100 animate-pulse" />}>
        <InteractiveMap />
      </Suspense>
      <Testimonials />
      <Suspense fallback={<div className="aspect-video bg-gray-100" />}>
        <VideoPlayer src="/promo.mp4" />
      </Suspense>
    </div>
  );
}
```

#### Next.js App Router — native code splitting

```tsx
// Next.js automatically code-splits by route segment.
// Each page.tsx / layout.tsx gets its own chunk.

// For component-level splitting within a page:
import dynamic from 'next/dynamic';

const HeavyCalendar = dynamic(() => import('./HeavyCalendar'), {
  loading: () => <CalendarSkeleton />,
  ssr: false,  // Skip SSR if the component uses browser APIs
});

export default function Page() {
  return (
    <div>
      <h1>My Page</h1>
      <HeavyCalendar />
    </div>
  );
}
```

#### Vite — manual chunk splitting via `rollupOptions`

```js
// vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Separate large dependencies into dedicated chunks
          vendor: ['react', 'react-dom'],
          charts: ['d3', 'recharts'],
          editor: ['@tiptap/react', 'prosemirror-state', 'prosemirror-view'],
        },
      },
    },
  },
});
```

**Vite chunk splitting strategy — by import origin:**

```js
// vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          // Group node_modules by package
          if (id.includes('node_modules')) {
            if (id.includes('react-dom') || id.includes('react/')) return 'react';
            if (id.includes('lodash')) return 'lodash';
            if (id.includes('d3')) return 'd3';
            return 'vendor';  // everything else
          }
        },
      },
    },
  },
});
```

---

### 2.2 Tree Shaking

Tree shaking removes dead (unused) code from the final bundle. It relies on ES module static analysis.

#### Prerequisites for effective tree shaking

1. **Use ES module syntax** (`import`/`export`), not CommonJS (`require`/`module.exports`)
2. **Avoid side effects** in module top-level scope
3. **Mark modules as side-effect-free** in `package.json`

#### Enabling tree shaking

```json
// package.json — mark the entire package as side-effect-free
{
  "name": "my-lib",
  "sideEffects": false
}

// Or whitelist files that DO have side effects
{
  "name": "my-lib",
  "sideEffects": [
    "*.css",
    "*.scss",
    "./src/polyfills.js"
  ]
}
```

#### Import only what you need

```js
// ❌ Bad: imports entire library (even with tree shaking, often includes more)
import _ from 'lodash';
_.debounce(fn, 300);

// ✅ Good: import only the function needed
import debounce from 'lodash/debounce';
debounce(fn, 300);

// ✅ Better: use native alternatives or smaller libraries
// Instead of lodash, use native or micro-libraries
const debounce = (fn, ms) => {
  let timer;
  return (...args) => { clearTimeout(timer); timer = setTimeout(fn, ms, ...args); };
};

// ❌ Bad: barrel exports can defeat tree shaking
export * from './components/Button';
export * from './components/Modal';

// ✅ Good: named exports
export { Button } from './components/Button';
export { Modal } from './components/Modal';
```

#### Vite tree-shaking config

```js
// vite.config.js — Vite uses Rollup+esbuild, tree-shaking is on by default
// But you can tune it:
export default defineConfig({
  build: {
    // Ensure we can analyze side effects
    rollupOptions: {
      treeshake: {
        preset: 'recommended',     // or 'smallest' | 'safest'
        moduleSideEffects: true,   // respect package.json sideEffects
      },
    },
    // Minification with Terser (more aggressive) vs esbuild (faster)
    minify: 'terser',              // terser removes more dead code
    terserOptions: {
      compress: {
        drop_console: true,        // strip console.log in production
        drop_debugger: true,
        pure_funcs: ['console.debug'], // strip specific calls
      },
    },
  },
});
```

#### Next.js tree shaking

Next.js uses webpack (or Turbopack) — tree shaking is on by default. Optimize further:

```js
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: [
      // Next.js can optimize barrel imports for these packages
      'lucide-react',
      '@heroicons/react',
      'date-fns',
      'lodash-es',
    ],
  },
};
```

#### Bundle analysis — find what's bloating your bundle

```bash
# Next.js — built-in analyzer
ANALYZE=true next build

# Vite — rollup-plugin-visualizer
npm install -D rollup-plugin-visualizer
```

```js
// vite.config.js
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    visualizer({
      filename: 'stats.html',
      open: true,
      gzipSize: true,
      brotliSize: true,
    }),
  ],
});
```

---

### 2.3 Lazy Loading

Beyond code splitting, lazy loading defers non-critical resources until they're needed.

#### Lazy load images (native)

```html
<img src="photo.jpg" loading="lazy" alt="..." />
```

#### Lazy load iframes

```html
<iframe src="https://example.com" loading="lazy" title="Embedded content"></iframe>
```

#### Lazy load videos

```html
<!-- Don't autoplay; use poster image + preload="none" -->
<video poster="thumbnail.jpg" preload="none" controls width="640" height="360">
  <source src="video.mp4" type="video/mp4">
</video>
```

#### Intersection Observer — DIY lazy loading

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.srcset = img.dataset.srcset;
      observer.unobserve(img);
    }
  });
}, {
  rootMargin: '200px',  // Start loading 200px before visible
});

document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));
```

#### Next.js — lazy load client components

```tsx
// Only load this component when it scrolls into view
'use client';

import { useEffect, useRef, useState } from 'react';

function LazySection({ children }) {
  const ref = useRef(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setIsVisible(true); },
      { rootMargin: '200px' }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return <div ref={ref}>{isVisible ? children : <div style={{ minHeight: '400px' }} />}</div>;
}
```

#### Module preload — speed up subsequent navigations

```html
<!-- Preload chunks for likely next pages -->
<link rel="modulepreload" href="/assets/dashboard-BzF8GpXw.js">
<link rel="modulepreload" href="/assets/settings-Ck9LmNoP.js">
```

---

## 3. Image Optimization

Images are typically the largest payload on a web page. Optimizing them is the single highest-impact performance win.

### 3.1 Modern Formats: WebP & AVIF

| Format | Compression vs JPEG | Browser Support | Best For |
|--------|-------------------|----------------|-----------|
| **JPEG** | Baseline | Universal | Photographs (fallback) |
| **WebP** | 25-35% smaller | 97%+ global | Photographs, UI images |
| **AVIF** | 50% smaller | 93%+ global | Photographs, HDR, transparency |
| **PNG** | Baseline | Universal | Simple graphics (fallback) |

#### Server-side auto-conversion

```bash
# Sharp — the fastest Node.js image processing library
npm install sharp
```

```js
// image-processor.js — build-time or on-demand conversion
import sharp from 'sharp';

async function optimizeImage(inputPath, outputDir) {
  // Generate multiple formats
  await sharp(inputPath)
    .resize(1920)
    .avif({ quality: 50 })
    .toFile(`${outputDir}/hero-1920.avif`);

  await sharp(inputPath)
    .resize(1920)
    .webp({ quality: 75 })
    .toFile(`${outputDir}/hero-1920.webp`);

  await sharp(inputPath)
    .resize(1920)
    .jpeg({ quality: 80, progressive: true })
    .toFile(`${outputDir}/hero-1920.jpg`);
}
```

#### Next.js Image — automatic optimization

```tsx
// Next.js optimizes images on-demand via its image optimization API
// Configurable in next.config.js:

module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],  // Serve AVIF first, WebP fallback
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    minimumCacheTTL: 60,  // Cache optimized images for 60s
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
      },
    ],
  },
};
```

#### Vite — imagemin plugin for build-time optimization

```bash
npm install -D vite-plugin-imagemin
```

```js
// vite.config.js
import viteImagemin from 'vite-plugin-imagemin';

export default defineConfig({
  plugins: [
    viteImagemin({
      gifsicle: { optimizationLevel: 3 },
      mozjpeg: { quality: 80, progressive: true },
      optipng: { optimizationLevel: 5 },
      webp: { quality: 75 },
    }),
  ],
});
```

---

### 3.2 Responsive Images with `srcset` & `<picture>`

#### Resolution switching (`srcset` + `sizes`)

```html
<!-- Browser picks the best image based on viewport width -->
<img
  src="photo-800.jpg"
  srcset="
    photo-400.jpg   400w,
    photo-800.jpg   800w,
    photo-1200.jpg 1200w,
    photo-1920.jpg 1920w
  "
  sizes="
    (max-width: 640px) 100vw,
    (max-width: 1024px) 50vw,
    33vw
  "
  alt="Responsive photo"
  width="1920"
  height="1080"
  loading="lazy"
>
```

#### Art direction (`<picture>` element)

```html
<!-- Different crops/ratios for different screen sizes -->
<picture>
  <source media="(max-width: 640px)" srcset="hero-mobile.webp" type="image/webp">
  <source media="(max-width: 640px)" srcset="hero-mobile.jpg">
  <source media="(max-width: 1200px)" srcset="hero-tablet.webp" type="image/webp">
  <source media="(max-width: 1200px)" srcset="hero-tablet.jpg">
  <source srcset="hero-desktop.webp" type="image/webp">
  <img src="hero-desktop.jpg" alt="Hero image" fetchpriority="high">
</picture>
```

#### Next.js — responsive images with `sizes` and `fill`

```tsx
// Fixed dimensions — Next.js auto-generates srcset
<Image src="/photo.jpg" width={800} height={600} alt="..." />

// Fill mode — for images with unknown/custom sizes
<div style={{ position: 'relative', aspectRatio: '16/9' }}>
  <Image
    src="/photo.jpg"
    fill
    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    alt="..."
    style={{ objectFit: 'cover' }}
  />
</div>
```

#### Generate responsive image sizes at build time

```js
// scripts/generate-responsive-images.js
import sharp from 'sharp';
import { glob } from 'glob';

const WIDTHS = [400, 800, 1200, 1920];
const INPUT = 'public/images/originals';
const OUTPUT = 'public/images/optimized';

async function generateResponsiveImages() {
  const files = await glob(`${INPUT}/*.{jpg,jpeg,png}`);

  for (const file of files) {
    const name = file.split('/').pop().replace(/\.[^.]+$/, '');

    for (const width of WIDTHS) {
      await sharp(file)
        .resize(width)
        .webp({ quality: 75 })
        .toFile(`${OUTPUT}/${name}-${width}.webp`);

      await sharp(file)
        .resize(width)
        .avif({ quality: 50 })
        .toFile(`${OUTPUT}/${name}-${width}.avif`);
    }
  }
  console.log(`Generated responsive images for ${files.length} files.`);
}

generateResponsiveImages();
```

---

### 3.3 Image Lazy Loading

Three tiers: **native** (simplest), **Intersection Observer** (most control), **framework-level** (Next.js built-in).

#### Tier 1: Native lazy loading (all modern browsers)

```html
<img src="photo.jpg" loading="lazy" alt="..." decoding="async">
<!-- decoding="async" lets the browser decode off the main thread -->
```

#### Tier 2: Intersection Observer with blur-up placeholder

```html
<img
  src="data:image/webp;base64,UklGRiIAAABXRUJQ..."  <!-- 20px blur placeholder -->
  data-src="photo-full.webp"
  class="lazy"
  alt="..."
>
```

```css
.lazy { filter: blur(20px); transition: filter 0.3s; }
.lazy.loaded { filter: blur(0); }
```

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.onload = () => img.classList.add('loaded');
      observer.unobserve(img);
    }
  });
}, { rootMargin: '300px' }); // Start loading 300px before viewport
```

#### Tier 3: Next.js — built-in lazy loading

```tsx
// Next.js Image: lazy loading by default (except when priority is set)
<Image src="/below-fold.jpg" width={800} height={600} alt="..." />
// This automatically gets loading="lazy" and a blur-up placeholder
// if you configure placeholder="blur" with a static import:

import belowFoldImg from '@/public/below-fold.jpg';
<Image
  src={belowFoldImg}
  alt="..."
  placeholder="blur"    // Next.js generates a tiny blur data URL at build time
/>
```

---

## 4. Caching Strategies

### 4.1 Browser Cache

#### Cache-Control headers — the foundation

```
# Static assets with content hashes — cache aggressively
Cache-Control: public, max-age=31536000, immutable

# HTML — revalidate often
Cache-Control: public, max-age=0, must-revalidate

# API responses — short TTL
Cache-Control: public, max-age=60, stale-while-revalidate=300
```

#### Cache-Control directives explained

| Directive | Meaning |
|-----------|---------|
| `public` | Can be cached by browsers and CDNs |
| `private` | Only browser cache (not CDN) |
| `max-age=N` | Cache for N seconds |
| `immutable` | Don't revalidate during max-age |
| `must-revalidate` | Must check with origin after expiry |
| `stale-while-revalidate=N` | Serve stale for N seconds while revalidating in background |
| `no-cache` | Always revalidate (but can store) |
| `no-store` | Never store |

#### Next.js — Cache-Control per route

```tsx
// App Router: set headers in layout or page
export const dynamic = 'force-static';  // static generation
export const revalidate = 3600;          // ISR: revalidate every hour

// Or set custom Cache-Control headers
export async function generateMetadata() {
  return {
    other: {
      'Cache-Control': 'public, max-age=3600, stale-while-revalidate=86400',
    },
  };
}
```

```js
// next.config.js — static asset headers
module.exports = {
  async headers() {
    return [
      {
        source: '/_next/static/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/fonts/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ];
  },
};
```

#### Vite — cache-friendly file naming

```js
// vite.config.js — Vite already uses content hashes by default
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        // Ensure content-hashed filenames for long-term caching
        entryFileNames: 'assets/[name]-[hash].js',
        chunkFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash][extname]',
      },
    },
  },
});
```

#### Service Worker — advanced browser caching

```js
// sw.js — Cache-first strategy for static assets
const CACHE_NAME = 'app-v2';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) =>
      cache.addAll([
        '/',
        '/styles/main.css',
        '/scripts/app.js',
      ])
    )
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => {
      // Cache-first: return cached, fall back to network
      return cached || fetch(event.request).then((response) => {
        return caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, response.clone());
          return response;
        });
      });
    })
  );
});
```

---

### 4.2 CDN Caching

#### CDN Cache Strategy Matrix

| Content Type | Cache Duration | Purge Strategy |
|-------------|---------------|----------------|
| HTML pages | 0 – 5 min | Purge on deploy |
| CSS/JS (hashed) | 1 year | Never purge (new hash = new URL) |
| Images | 1 year | Purge on update |
| API responses | 1 – 60 min | Stale-while-revalidate |
| Fonts | 1 year | Purge on update |

#### Vercel Edge Cache (Next.js)

```tsx
// App Router — control edge caching
export const runtime = 'edge';  // Run at the edge

// Cache a route for 1 hour at the edge
export const revalidate = 3600;

// Stale-while-revalidate pattern
export async function GET() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 },
  });
  return Response.json(data);
}
```

```js
// next.config.js
module.exports = {
  // Cache-Control for static outputs
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'CDN-Cache-Control',
            value: 'public, max-age=60, stale-while-revalidate=300',
          },
        ],
      },
    ];
  },
};
```

#### Cloudflare / Generic CDN — Cache Rules

```
# Example: Cloudflare Cache Rules
URL pattern: example.com/static/*
  → Cache: Eligible for Cache
  → Edge TTL: 30 days
  → Browser TTL: 1 year

URL pattern: example.com/api/*
  → Cache: Eligible for Cache
  → Edge TTL: 5 minutes
  → Respect Origin Headers: Yes
```

#### Surrogate Keys for targeted purge

```http
# Origin sends a Surrogate-Key header
Surrogate-Key: post-123 category-tech

# CDN can purge all content tagged with post-123
# Without invalidating the entire cache
```

---

### 4.3 API & Data Caching

#### Client-side data caching

**React Query / TanStack Query:**

```tsx
import { QueryClient, QueryClientProvider, useQuery } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,      // 5 min before considered stale
      gcTime: 30 * 60 * 1000,         // 30 min garbage collection (formerly cacheTime)
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});

function ProductList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['products'],
    queryFn: () => fetch('/api/products').then(r => r.json()),
    staleTime: 10 * 60 * 1000,        // Override: 10 min stale time
  });

  if (isLoading) return <Skeleton />;
  if (error) return <Error message={error.message} />;
  return <ProductGrid products={data} />;
}
```

**SWR (Next.js ecosystem):**

```tsx
import useSWR from 'swr';

const fetcher = (url) => fetch(url).then(r => r.json());

function ProfilePage() {
  const { data, error, isLoading, mutate } = useSWR('/api/user', fetcher, {
    revalidateOnFocus: false,
    dedupingInterval: 60000,     // Dedupe requests within 60s
    revalidateIfStale: true,
  });

  return <Profile user={data} />;
}

// Preload data for a likely navigation
import { preload } from 'swr';
preload('/api/products', fetcher);
```

#### Server-side caching

**Next.js — Incremental Static Regeneration (ISR):**

```tsx
// Rebuild this page at most once every 60 seconds
export const revalidate = 60;

export default async function BlogPost({ params }) {
  const post = await fetch(`https://cms.example.com/posts/${params.slug}`, {
    next: { revalidate: 3600 },  // Cache fetch for 1 hour
  }).then(r => r.json());

  return <article>{post.content}</article>;
}
```

**Next.js — `unstable_cache` (App Router):**

```tsx
import { unstable_cache } from 'next/cache';

const getProducts = unstable_cache(
  async (category) => {
    const res = await fetch(`https://api.example.com/products?cat=${category}`);
    return res.json();
  },
  ['products'],       // Cache key
  { revalidate: 300 } // 5 min
);

export default async function ProductsPage({ params }) {
  const products = await getProducts(params.category);
  return <ProductList products={products} />;
}
```

**Redis / Upstash — global cache layer:**

```ts
// lib/cache.ts
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_URL!,
  token: process.env.UPSTASH_REDIS_TOKEN!,
});

export async function cachedFetch<T>(
  key: string,
  fn: () => Promise<T>,
  ttlSeconds: number = 300
): Promise<T> {
  const cached = await redis.get<T>(key);
  if (cached) return cached;

  const fresh = await fn();
  await redis.set(key, fresh, { ex: ttlSeconds });
  return fresh;
}

// Usage
const products = await cachedFetch(
  'products:featured',
  () => fetch('https://api.example.com/products/featured').then(r => r.json()),
  600 // 10 min TTL
);
```

---

## 5. Font Loading Optimization

Web fonts are a top offender for both LCP and CLS. The key principle: **show text immediately, swap fonts later, and minimize the layout shift when the swap happens.**

### The Font Loading Timeline

```
1. Browser discovers @font-face → starts downloading font
2. While downloading → shows invisible text (FOIT) or fallback font (FOUT)
3. Font loads → swaps to web font → POTENTIAL LAYOUT SHIFT (CLS!)
```

### Strategy 1: `font-display` — the single most important CSS property

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-var.woff2') format('woff2-variations'),
       url('/fonts/inter-regular.woff2') format('woff2');
  font-display: swap;         /* Show fallback immediately, swap later */
  font-weight: 100 900;
  font-style: normal;
}
```

| `font-display` Value | Block Period | Swap Period | Best For |
|---------------------|-------------|-------------|----------|
| `swap` | 0 ms | ∞ | Body text, UI (recommended) |
| `optional` | ~100 ms | 0 ms | Icons, decorative |
| `block` | ~3 s | ∞ | Brand-critical headings |
| `fallback` | ~100 ms | ~3 s | Compromise |
| `auto` | Browser default | Browser default | Default |

### Strategy 2: Subset fonts to reduce file size

```bash
# Use glyphhanger or a subsetting tool to include only needed characters
# For Latin-only sites, strip Cyrillic, CJK, etc.
npx glyphhanger --subset=*.woff2 --formats=woff2
```

```css
/* Instead of one massive font file, use unicode-range to split */
@font-face {
  font-family: 'MyFont';
  src: url('/fonts/myfont-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF; /* Latin */
  font-display: swap;
}
@font-face {
  font-family: 'MyFont';
  src: url('/fonts/myfont-latin-ext.woff2') format('woff2');
  unicode-range: U+0100-024F; /* Latin Extended */
  font-display: swap;
}
```

### Strategy 3: Preload critical fonts

```html
<!-- Preload the most important font file as early as possible -->
<link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
```

**Next.js — font optimization built in:**

```tsx
// app/layout.tsx — Next.js auto-optimizes Google Fonts
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',   // CSS variable for Tailwind etc.
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
```

```tsx
// Local fonts — Next.js self-hosts and optimizes
import localFont from 'next/font/local';

const myFont = localFont({
  src: [
    {
      path: '../public/fonts/myfont-regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../public/fonts/myfont-bold.woff2',
      weight: '700',
      style: 'normal',
    },
  ],
  display: 'swap',
  preload: true,
  variable: '--font-custom',
});
```

### Strategy 4: Match fallback font metrics to prevent CLS

```css
/* Use size-adjust, ascent-override, descent-override to align fallback */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-var.woff2') format('woff2-variations');
  font-display: swap;
}

/* Define a fallback that matches Inter's metrics */
@font-face {
  font-family: 'Inter Fallback';
  src: local('Arial');
  size-adjust: 105%;        /* Scale Arial to match Inter's advance width */
  ascent-override: 90%;     /* Match Inter's ascender */
  descent-override: 25%;    /* Match Inter's descender */
  line-gap-override: 0%;
}

body {
  font-family: 'Inter', 'Inter Fallback', sans-serif;
}
```

**Automated metric matching tool:**

```js
// scripts/match-font-metrics.js
// Use Capsize to generate fallback font metrics automatically
import { preconnect, createFontStack } from '@capsizecss/core';
import interMetrics from '@capsizecss/metrics/inter';
import arialMetrics from '@capsizecss/metrics/arial';

const { fontFaces, fontFamily } = createFontStack(
  [interMetrics, arialMetrics],
  { fontFaceFormat: 'styleString' }
);

// Output:
// @font-face { font-family: "Inter Fallback"; src: local("Arial"); size-adjust: ...; }
console.log(fontFaces);
```

### Strategy 5: Self-host fonts (don't use Google Fonts CDN)

```bash
# Use google-webfonts-helper to download and self-host
# https://gwfh.mranftl.com/

# Avoid the extra DNS lookup + TLS handshake for fonts.googleapis.com
# Self-hosting with preload is consistently faster
```

### Strategy 6: Use variable fonts

```css
/* One file instead of 4-6 weight files */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}
```

---

## 6. Performance Budget Template

A performance budget is a set of limits that the team agrees to not exceed. Enforce it in CI.

### Budget Template

```json
{
  "name": "Web Performance Budget — Q3 2026",
  "version": "1.0.0",
  "owner": "Frontend Team",
  "lastUpdated": "2026-06-25",

  "milestones": {
    "target": "All pages < 3s on 4G mobile",
    "stretch": "All pages < 2s on 4G mobile"
  },

  "metrics": {
    "coreWebVitals": {
      "LCP": { "good": 2500, "needsImprovement": 4000, "unit": "ms" },
      "INP": { "good": 200, "needsImprovement": 500, "unit": "ms" },
      "CLS": { "good": 0.1, "needsImprovement": 0.25, "unit": "score" },
      "TTFB": { "good": 800, "needsImprovement": 1800, "unit": "ms" },
      "FCP": { "good": 1800, "needsImprovement": 3000, "unit": "ms" }
    },

    "resourceBudgets": {
      "totalPageWeight": { "budget": 1000, "unit": "KB", "network": "4G" },
      "javaScript": {
        "initial": { "budget": 200, "unit": "KB", "network": "4G" },
        "totalPage": { "budget": 500, "unit": "KB", "network": "4G" },
        "mainThread": { "budget": 3000, "unit": "ms" }
      },
      "css": {
        "initial": { "budget": 80, "unit": "KB", "network": "4G" },
        "totalPage": { "budget": 200, "unit": "KB", "network": "4G" }
      },
      "fonts": {
        "total": { "budget": 150, "unit": "KB", "network": "4G" },
        "perFont": { "budget": 50, "unit": "KB", "network": "4G" }
      },
      "images": {
        "hero": { "budget": 100, "unit": "KB" },
        "thumbnail": { "budget": 20, "unit": "KB" },
        "perPage": { "budget": 1000, "unit": "KB" }
      },
      "thirdParty": {
        "total": { "budget": 250, "unit": "KB", "network": "4G" },
        "requests": { "budget": 10, "unit": "count" }
      }
    },

    "requestBudgets": {
      "totalRequests": { "budget": 50, "unit": "count" },
      "javaScriptRequests": { "budget": 10, "unit": "count" },
      "cssRequests": { "budget": 3, "unit": "count" },
      "fontRequests": { "budget": 3, "unit": "count" },
      "imageRequests": { "budget": 20, "unit": "count" }
    },

    "lighthouseScores": {
      "performance": { "budget": 90, "unit": "score" },
      "accessibility": { "budget": 90, "unit": "score" },
      "bestPractices": { "budget": 90, "unit": "score" },
      "seo": { "budget": 90, "unit": "score" }
    }
  },

  "pageSpecificBudgets": {
    "homepage": {
      "LCP": { "budget": 2000, "unit": "ms" },
      "totalPageWeight": { "budget": 800, "unit": "KB" },
      "notes": "Most trafficked page — strictest budget"
    },
    "productPage": {
      "totalPageWeight": { "budget": 1200, "unit": "KB" },
      "thirdParty": { "budget": 200, "unit": "KB" },
      "notes": "Likely has analytics, product images, recommendations"
    },
    "blogPost": {
      "totalPageWeight": { "budget": 600, "unit": "KB" },
      "notes": "Should be lightweight; mostly text"
    }
  }
}
```

### CI Enforcement — Lighthouse Budget

```js
// .lighthouserc.js — matches the budget above
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/', 'http://localhost:3000/products', 'http://localhost:3000/blog'],
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        // Core Web Vitals
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'interactive': ['error', { maxNumericValue: 3500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 300 }],

        // Resource budgets (in bytes)
        'resource-summary:script:size': ['error', { maxNumericValue: 500 * 1024 }],
        'resource-summary:stylesheet:size': ['error', { maxNumericValue: 80 * 1024 }],
        'resource-summary:font:size': ['error', { maxNumericValue: 150 * 1024 }],
        'resource-summary:image:size': ['error', { maxNumericValue: 1000 * 1024 }],

        // Request counts
        'resource-summary:script:count': ['warn', { maxNumericValue: 10 }],
        'resource-summary:stylesheet:count': ['warn', { maxNumericValue: 3 }],
        'resource-summary:font:count': ['warn', { maxNumericValue: 3 }],

        // Scores
        'categories:performance': ['error', { minScore: 0.90 }],
        'categories:accessibility': ['error', { minScore: 0.90 }],
      },
    },
  },
};
```

### Webpack Bundle Budget (alternative for Vite/Next.js webpack configs)

```js
// next.config.js — if using webpack (not Turbopack)
module.exports = {
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.performance = {
        maxAssetSize: 250 * 1024,        // 250 KB per asset
        maxEntrypointSize: 300 * 1024,   // 300 KB per entry point
        hints: 'error',                   // Fail the build
        assetFilter: (assetFilename) => {
          return !/\.(map|gz|br)$/.test(assetFilename);
        },
      };
    }
    return config;
  },
};
```

---

## 7. Appendix: Quick-Reference Checklists

### LCP Optimization Checklist

- [ ] LCP image uses `fetchpriority="high"` and is NOT lazy-loaded
- [ ] Critical CSS is inlined; non-critical CSS is deferred
- [ ] Render-blocking JS is deferred or async
- [ ] Server response time (TTFB) < 800 ms
- [ ] LCP resource is preloaded with `<link rel="preload">`
- [ ] Text is visible during webfont load (`font-display: swap`)
- [ ] CDN is enabled for static assets

### INP Optimization Checklist

- [ ] No single task blocks the main thread > 50 ms
- [ ] Expensive event handlers are debounced or throttled
- [ ] Heavy computation runs in Web Workers
- [ ] React: `useTransition` / `useDeferredValue` for expensive updates
- [ ] `requestAnimationFrame` for visual updates, not layout reads
- [ ] Third-party scripts are deferred or loaded after interaction

### CLS Optimization Checklist

- [ ] All `<img>` elements have explicit `width` and `height` or `aspect-ratio`
- [ ] Ad slots / embeds have reserved space (`min-height`)
- [ ] Web fonts use `font-display: swap` + fallback metric matching
- [ ] Animations use `transform` and `opacity` only (GPU-composited)
- [ ] Dynamically inserted content is added below the fold or in reserved space
- [ ] No layout shifts caused by late-loading CSS

### Bundle Size Checklist

- [ ] Routes are code-split (dynamic imports)
- [ ] Heavy components are lazy-loaded below the fold
- [ ] Tree shaking is verified (no barrel imports, ESM only)
- [ ] `package.json` has `"sideEffects": false` (or proper whitelist)
- [ ] Bundle analyzer run — no unexpected large dependencies
- [ ] Total JS < 200 KB (compressed) for initial load
- [ ] Dead code elimination confirmed (Terser with `drop_console` in prod)

### Image Checklist

- [ ] Images served in WebP (with AVIF for modern browsers)
- [ ] Responsive `srcset` with multiple widths
- [ ] Images below the fold use `loading="lazy"`
- [ ] LCP image explicitly marked `priority` (Next.js) or `fetchpriority="high"`
- [ ] Build-time image optimization pipeline in place
- [ ] Proper `sizes` attribute for responsive images
- [ ] Placeholder/blur-up strategy for lazy-loaded images

### Caching Checklist

- [ ] Static assets (hashed JS/CSS) have `max-age=31536000, immutable`
- [ ] HTML has short cache with revalidation: `max-age=0, must-revalidate`
- [ ] API responses use `stale-while-revalidate`
- [ ] CDN is configured with appropriate TTLs per content type
- [ ] Service Worker or Cache API for offline-critical assets
- [ ] Build outputs use content hashes in filenames

---

## References & Further Reading

- [Web Vitals — web.dev](https://web.dev/vitals/)
- [Largest Contentful Paint (LCP) — web.dev](https://web.dev/lcp/)
- [Interaction to Next Paint (INP) — web.dev](https://web.dev/inp/)
- [Cumulative Layout Shift (CLS) — web.dev](https://web.dev/cls/)
- [Next.js Image Optimization Docs](https://nextjs.org/docs/app/building-your-application/optimizing/images)
- [Vite Build Optimizations](https://vitejs.dev/guide/build.html)
- [web-vitals NPM Package](https://github.com/GoogleChrome/web-vitals)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [Capsize — Font Metric Matching](https://seek-oss.github.io/capsize/)
- [webpagetest.org](https://www.webpagetest.org/)

---

*Generated by Performance Optimizer Agent — Run `run-20260625-213900`*
