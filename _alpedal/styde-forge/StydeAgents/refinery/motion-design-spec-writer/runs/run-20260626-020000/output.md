# Motion Design Specification — Advanced Motion System
**Run ID:** `run-20260626-020000`
**Agent:** `motion-design-spec-writer` (c2)
**Date:** 2026-06-26 02:00 UTC
**Status:** Complete

---

## 1. Executive Overview

This document defines an advanced, framework-agnostic motion design system for modern web applications. It covers four pillars: **spring-based physics**, **timeline orchestration**, **entrance/exit coordinated sequences**, **shared element transitions**, and **framework-specific motion tokens** for React, Vue, and Svelte. The system is designed for 60 fps fluidity, accessibility compliance (`prefers-reduced-motion`), and ergonomic developer experience across all three frameworks.

---

## 2. Spring Physics Engine

### 2.1 Core Spring Model

The spring simulation models a damped harmonic oscillator parameterised by three values:

| Parameter | Symbol | Unit | Description |
|---|---|---|---|
| **Stiffness** | `k` (or `stiffness`) | N/m (abstract) | Resistance to displacement. Higher = snappier, faster settling. Typical range: 50–800. |
| **Damping** | `c` (or `damping`) | N·s/m (abstract) | Energy dissipation. Higher = less overshoot, slower approach. Typical range: 5–50. |
| **Mass** | `m` (or `mass`) | kg (abstract) | Inertia. Heavier objects accelerate slower. Default: `1`. Typical range: 0.5–5. |

The equation of motion:

```
m · x''(t) + c · x'(t) + k · x(t) = 0
```

Solved numerically via semi-implicit Euler integration at 60 Hz.

### 2.2 Damping Regimes

| Regime | Condition | Behaviour |
|---|---|---|
| **Underdamped** | `c² < 4mk` | Oscillates, overshoots target. Bouncy springs. |
| **Critically Damped** | `c² = 4mk` | Fastest settling without oscillation. |
| **Overdamped** | `c² > 4mk` | No oscillation; sluggish return to equilibrium. |

**Critical damping coefficient:** `c_critical = 2 · sqrt(m · k)`

### 2.3 Predefined Presets

```yaml
presets:
  gentle:
    stiffness: 120
    damping: 14
    mass: 1
    description: "Subtle hover/active states, micro-interactions"

  snappy:
    stiffness: 300
    damping: 20
    mass: 1
    description: "Modal dialogs, popovers, quick reveals"

  bouncy:
    stiffness: 500
    damping: 10
    mass: 1
    description: "Notification badges, celebratory animations, playful UIs"

  heavy:
    stiffness: 400
    damping: 30
    mass: 3
    description: "Page transitions, hero elements, deliberate weight"

  wobbly:
    stiffness: 180
    damping: 8
    mass: 1
    description: "Drag-release, elastic lists, physics-informed gestures"
```

### 2.4 Spring Function Signature

```
spring({
  from: number,         // initial value
  to: number,           // target value
  stiffness?: number,   // default: 170
  damping?: number,     // default: 26
  mass?: number,        // default: 1
  velocity?: number,    // initial velocity (default: 0)
  precision?: number,   // rest delta threshold (default: 0.01)
  onUpdate: (value: number, velocity: number) => void,
  onComplete?: () => void,
}): { stop: () => void }
```

### 2.5 Multi-Dimensional Springs

Springs operate per-axis. For composable interpolations (e.g. position + opacity + scale), run independent springs in parallel, synchronising their `onUpdate` callbacks:

```
multiSpring({
  properties: {
    x: { from: 0, to: 100, stiffness: 300, damping: 20 },
    y: { from: 0, to: 50,  stiffness: 300, damping: 20 },
    opacity: { from: 0, to: 1, stiffness: 200, damping: 24 },
  },
  onUpdate: (state: { x: number, y: number, opacity: number }) => void,
  onComplete?: () => void,
}): { stop: () => void }
```

---

## 3. Timeline Orchestration

### 3.1 Timeline Model

A **Timeline** is a directed acyclic graph (DAG) of animation segments. Each segment has a start offset, duration, and optional easing. Segments can be sequenced, overlapped, or gapped.

```
Timeline
├── Segment A: t=0ms      duration=300ms   [header slides in]
├── Segment B: t=200ms    duration=250ms   [subtitle fades in]     // overlaps A by 100ms
├── Segment C: t=300ms    duration=400ms   [cards stagger in]      // starts when A ends
└── Segment D: t=550ms    duration=200ms   [CTA button bounces]    // starts 50ms after B
```

### 3.2 Timeline API

```
createTimeline({
  segments: TimelineSegment[],
  direction?: 'forward' | 'reverse',
  loop?: boolean,
}): Timeline

interface TimelineSegment {
  id: string;
  at: number;              // absolute start time (ms)
  duration: number;        // ms
  easing?: EasingFunction;
  animate: (progress: number) => void;  // 0..1
  onStart?: () => void;
  onComplete?: () => void;
}
```

### 3.3 Execution Phases

| Phase | Description |
|---|---|
| `idle` | Timeline created, not yet started. |
| `playing` | Forward playback active. |
| `paused` | Paused mid-sequence; resumable. |
| `reversing` | Playing backward toward `idle`. |
| `completed` | Forward playback finished; not looping. |

### 3.4 Orchestration Patterns

#### 3.4.1 Staggered Stagger (Nested Staggering)

```
// Parent timeline with overlapping child timelines
// Each row's items stagger, and rows themselves stagger
const master = createTimeline({ segments: [
  { at: 0,    duration: 500, animate: row1 },
  { at: 100,  duration: 500, animate: row2 },  // 100ms row stagger
  { at: 200,  duration: 500, animate: row3 },
]});

// Inside row1/row2/row3: per-item stagger (50ms each)
```

#### 3.4.2 Scroll-Linked Timeline

```
const scrollTimeline = createScrollTimeline({
  source: scrollContainer,
  axis: 'y',
  segments: [
    { at: '0%',  atRelative: '0%',  animate: parallaxBack },
    { at: '20%', atRelative: '80%', animate: fadeInHero },
  ],
});
```

#### 3.4.3 Reverse-on-Exit

When a user navigates away or closes a modal, run the timeline in reverse:

```
timeline.reverse();  // plays all segments backward from their end times
```

---

## 4. Entrance & Exit Coordinated Sequences

### 4.1 Staged Entrance Protocol

Every view has a defined **entrance stage** and **exit stage**. Stages are composed of atomic keyframe sets:

```
ViewLifecycle = {
  mount:   EntranceSequence,
  unmount: ExitSequence,
}
```

### 4.2 Entrance Sequence Model

```
{
  "entrance": {
    "stages": [
      {
        "name": "container-appear",
        "type": "spring",
        "targets": [".view-container"],
        "properties": { "opacity": [0, 1], "scale": [0.96, 1] },
        "spring": "snappy",
        "duration_estimate_ms": 400
      },
      {
        "name": "header-slide",
        "type": "spring",
        "targets": [".view-header"],
        "properties": { "translateY": [-30, 0], "opacity": [0, 1] },
        "delay": 100,
        "spring": "gentle"
      },
      {
        "name": "content-stagger",
        "type": "stagger",
        "targets": [".card-item"],
        "stagger_delay": 60,
        "properties": { "translateY": [20, 0], "opacity": [0, 1] },
        "spring": "snappy"
      }
    ]
  }
}
```

### 4.3 Exit Sequence Model (Reverse)

Exits are the entrance reversed, optionally accelerated:

```
{
  "exit": {
    "stages": [
      {
        "name": "content-stagger-reverse",
        "type": "stagger-reverse",
        "targets": [".card-item"],
        "stagger_delay": 40,            // faster exit
        "properties": { "translateY": [0, 20], "opacity": [1, 0] },
        "spring": "snappy"
      },
      {
        "name": "container-shrink",
        "type": "spring",
        "targets": [".view-container"],
        "properties": { "opacity": [1, 0], "scale": [1, 0.98] },
        "delay": 0,
        "spring": { "stiffness": 400, "damping": 25 }  // snappier exit spring
      }
    ]
  }
}
```

### 4.4 Coordination Rules

1. **No overlap between mount and unmount sequences.** Mount must complete before unmount begins.
2. **Exit starts immediately on navigation trigger.** No delay on exit.
3. **Entrance waits until DOM is measured.** Use `requestAnimationFrame` double-rAF pattern for initial state capture.
4. **Stagger children inherit parent direction.** Reversing the parent reverses stagger order automatically.
5. **Interruptible.** Any in-progress entrance can be cancelled by an exit trigger (cleanup + immediate exit start).

### 4.5 Stagger Direction Matrix

| Layout | Forward Stagger | Reverse Stagger |
|---|---|---|
| Vertical list | Top → Bottom | Bottom → Top |
| Horizontal list | Left → Right | Right → Left |
| Grid | Row-major, L→R then T→B | Col-major reverse, B→T then R→L |
| Radial | Clockwise from 12 o'clock | Counter-clockwise from last |

---

## 5. Shared Element Transitions

### 5.1 Concept

A **shared element** is a UI piece that persists across two views — e.g. a product image expanding from a list card into a detail hero. The motion system morphs its **position**, **size**, and **style** between the old and new layouts seamlessly.

### 5.2 The Morph Lifecycle

```
View A (source)                          View B (destination)
┌─────────────────┐                      ┌─────────────────────┐
│  ┌───────────┐  │                      │  ┌───────────────┐  │
│  │  shared   │  │  ─── morph ───────▶  │  │    shared     │  │
│  │  element  │  │      animation       │  │   element     │  │
│  └───────────┘  │                      │  │  (expanded)   │  │
│                 │                      │  └───────────────┘  │
└─────────────────┘                      └─────────────────────┘
```

Steps:
1. **Capture** source element's bounding rect + computed styles (on exit trigger).
2. **Hide** source and destination elements.
3. **Create clone** positioned absolutely at source rect, styled like source.
4. **Animate clone** from source rect/style → destination rect/style using spring physics.
5. **Reveal destination** element on animation complete.
6. **Remove clone.**

### 5.3 Shared Element Spec

```yaml
shared_elements:
  - id: "product-image-42"
    source:
      view: "product-list"
      selector: "[data-shared='product-image-42']"
    destination:
      view: "product-detail"
      selector: "[data-shared='product-image-42']"
    morph_properties:
      - property: "bounds"         # x, y, width, height
        spring: "snappy"
      - property: "border-radius"
        from_calc: "current"
        to_calc: "destination"
        spring: "gentle"
      - property: "opacity"
        from: 1
        to: 1
        spring: "gentle"
    z_index: 1000
    clone_class: "shared-element-clone"
```

### 5.4 Multiple Shared Elements

When multiple elements share across views, coordinate them:

```
shared_element_group:
  stagger_delay: 80           # stagger start times
  spring: "snappy"
  elements:
    - id: "hero-image"
    - id: "title-text"
    - id: "price-tag"
```

The group captures all rects together, then animates with 80ms stagger between each.

### 5.5 Edge Cases

| Scenario | Resolution |
|---|---|
| Element not in destination | Fade out clone to `opacity: 0` over 200ms |
| Element not in source | Fade in from `opacity: 0` + slight scale-up |
| Scroll position differs | Compensate clone position by scroll delta |
| `display: none` in source | Use `getBoundingClientRect()` before DOM mutation; fallback to `visibility: hidden` trick |
| Resize during morph | Re-capture destination rect on `resize`; smoothly re-target spring on next frame |

---

## 6. Motion Tokens — Framework Implementations

Motion tokens are framework-specific primitives that expose the spring engine, timeline, entrance/exit sequences, and shared element transitions as idiomatic APIs.

### 6.1 Token Map

| Capability | React | Vue 3 | Svelte |
|---|---|---|---|
| Spring (single value) | `useSpring(value, config)` | `v-spring:prop="config"` | `$spring(value, config)` |
| Multi-spring | `useMultiSpring(values)` | `v-multi-spring="values"` | `$multiSpring(values)` |
| Timeline | `useTimeline(segments)` | `useTimeline(segments)` | `$timeline(segments)` |
| Entrance/Exit | `<AnimatePresence>` | `<TransitionGroup>` + directives | `{#key}` + `transition:` |
| Shared element | `<SharedElement id="...">` | `<SharedElement id="...">` | `<SharedElement id="...">` |

---

### 6.2 React Implementation

#### 6.2.1 `useSpring` Hook

```tsx
import { useSpring, SpringPreset } from '@stryde/motion-react';

function AnimatedCard() {
  const scale = useSpring(1, {
    stiffness: 300,
    damping: 20,
    mass: 1,
  });

  // Or use a preset:
  const opacity = useSpring(1, { preset: SpringPreset.Snappy });

  return (
    <motion.div
      style={{
        transform: `scale(${scale.value})`,
        opacity: opacity.value,
      }}
      onMouseEnter={() => { scale.set(1.05); opacity.set(0.9); }}
      onMouseLeave={() => { scale.set(1); opacity.set(1); }}
    >
      <p>Hover me</p>
    </motion.div>
  );
}
```

#### 6.2.2 `useTimeline` Hook

```tsx
import { useTimeline } from '@stryde/motion-react';

function ProductHero() {
  const { play, reverse, progress } = useTimeline([
    {
      id: 'header',
      at: 0,
      duration: 400,
      animate: (p) => headerSpring.set(p),
    },
    {
      id: 'subtitle',
      at: 200,
      duration: 300,
      animate: (p) => subtitleSpring.set(p),
    },
    {
      id: 'cards',
      at: 300,
      duration: 500,
      stagger: { count: 4, delay: 80 },
      animate: (p, index) => cardSprings[index].set(p),
    },
  ]);

  useEffect(() => { play(); }, []);

  return (/* ... */);
}
```

#### 6.2.3 `<AnimatePresence>` — Entrance/Exit

```tsx
import { AnimatePresence, motion } from '@stryde/motion-react';

function RouteSwitch({ route }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={route}
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -30 }}
        transition={{ type: 'spring', stiffness: 250, damping: 22 }}
      >
        <RouteContent route={route} />
      </motion.div>
    </AnimatePresence>
  );
}
```

#### 6.2.4 `<SharedElement>`

```tsx
import { SharedElement, SharedElementGroup } from '@stryde/motion-react';

function ProductList() {
  return (
    <SharedElementGroup id="product-gallery">
      {products.map((p) => (
        <Link to={`/product/${p.id}`} key={p.id}>
          <SharedElement id={`product-${p.id}`}>
            <img src={p.thumb} alt={p.name} />
          </SharedElement>
        </Link>
      ))}
    </SharedElementGroup>
  );
}

function ProductDetail() {
  return (
    <SharedElement id={`product-${product.id}`}>
      <img src={product.fullImage} alt={product.name} />
    </SharedElement>
  );
}
```

#### 6.2.5 Motion Token Utilities (React)

```tsx
// Stagger children manually
import { staggerChildren } from '@stryde/motion-react';

const items = useMemo(() =>
  staggerChildren(data.length, { delay: 60, direction: 'forward' }),
  [data.length]
);

// Reduced motion
import { useReducedMotion } from '@stryde/motion-react';

function AccessibleSpring() {
  const prefersReduced = useReducedMotion();
  const config = prefersReduced
    ? { stiffness: 800, damping: 50, mass: 1 }  // near-instant
    : { stiffness: 170, damping: 26, mass: 1 };

  const x = useSpring(0, config);
  // ...
}
```

---

### 6.3 Vue 3 Implementation

#### 6.3.1 `v-spring` Directive

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { vSpring } from '@stryde/motion-vue';

const isOpen = ref(false);
const springConfig = { stiffness: 300, damping: 20 };
</script>

<template>
  <div
    v-spring:scale="[isOpen ? 1.05 : 1, springConfig]"
    v-spring:opacity="[isOpen ? 0.9 : 1, springConfig]"
    @mouseenter="isOpen = true"
    @mouseleave="isOpen = false"
  >
    <p>Hover me</p>
  </div>
</template>
```

#### 6.3.2 `useSpring` Composable

```vue
<script setup lang="ts">
import { useSpring, SpringPreset } from '@stryde/motion-vue';

const { value: scaleValue, set: setScale } = useSpring(1, {
  preset: SpringPreset.Snappy,
});
</script>

<template>
  <div :style="{ transform: `scale(${scaleValue})` }">
    <!-- content -->
  </div>
</template>
```

#### 6.3.3 `useTimeline` Composable

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useTimeline } from '@stryde/motion-vue';

const headerOpacity = ref(0);
const subtitleOpacity = ref(0);

const timeline = useTimeline([
  {
    id: 'header',
    at: 0,
    duration: 400,
    animate: (p) => { headerOpacity.value = p; },
  },
  {
    id: 'subtitle',
    at: 200,
    duration: 300,
    animate: (p) => { subtitleOpacity.value = p; },
  },
]);

onMounted(() => timeline.play());
</script>
```

#### 6.3.4 `<TransitionGroup>` — Entrance/Exit

```vue
<template>
  <TransitionGroup
    name="list"
    tag="ul"
    :css="false"
    @enter="onEnter"
    @leave="onLeave"
  >
    <li v-for="item in items" :key="item.id" :data-index="item.index">
      {{ item.text }}
    </li>
  </TransitionGroup>
</template>

<script setup lang="ts">
import { spring } from '@stryde/motion-vue';

function onEnter(el: Element, done: () => void) {
  const index = Number((el as HTMLElement).dataset.index);
  spring({
    from: 0,
    to: 1,
    stiffness: 250,
    damping: 22,
    onUpdate: (v) => {
      (el as HTMLElement).style.opacity = String(v);
      (el as HTMLElement).style.transform = `translateY(${(1 - v) * 20}px)`;
    },
    onComplete: done,
  });
}

function onLeave(el: Element, done: () => void) {
  spring({
    from: 1,
    to: 0,
    stiffness: 350,
    damping: 28,
    onUpdate: (v) => {
      (el as HTMLElement).style.opacity = String(v);
      (el as HTMLElement).style.transform = `translateY(${(1 - v) * -15}px)`;
    },
    onComplete: done,
  });
}
</script>
```

#### 6.3.5 `<SharedElement>` Component

```vue
<!-- In ProductList.vue -->
<template>
  <SharedElementGroup id="gallery">
    <RouterLink v-for="p in products" :key="p.id" :to="`/product/${p.id}`">
      <SharedElement :id="`product-${p.id}`">
        <img :src="p.thumb" :alt="p.name" />
      </SharedElement>
    </RouterLink>
  </SharedElementGroup>
</template>

<!-- In ProductDetail.vue -->
<template>
  <SharedElement :id="`product-${product.id}`">
    <img :src="product.fullImage" :alt="product.name" />
  </SharedElement>
</template>

<script setup lang="ts">
import { SharedElement, SharedElementGroup } from '@stryde/motion-vue';
</script>
```

#### 6.3.6 Motion Tokens (Vue)

```ts
// Composable for reduced motion
import { useReducedMotion } from '@stryde/motion-vue';

const prefersReduced = useReducedMotion();

const springConfig = computed(() =>
  prefersReduced.value
    ? { stiffness: 800, damping: 50 }
    : { stiffness: 170, damping: 26 }
);

// Stagger helper
import { createStagger } from '@stryde/motion-vue';

const stagger = createStagger(items.value.length, { delay: 60 });
// stagger[i] = i * 60
```

---

### 6.4 Svelte Implementation

#### 6.4.1 `$spring` Rune

```svelte
<script lang="ts">
  import { spring, SpringPreset } from '@stryde/motion-svelte';

  let hovered = $state(false);

  const scale = spring(() => hovered ? 1.05 : 1, {
    stiffness: 300,
    damping: 20,
  });

  const opacity = spring(() => hovered ? 0.9 : 1, {
    preset: SpringPreset.Snappy,
  });
</script>

<div
  style="transform: scale({scale.current}); opacity: {opacity.current}"
  onmouseenter={() => hovered = true}
  onmouseleave={() => hovered = false}
>
  <p>Hover me</p>
</div>
```

#### 6.4.2 `$multiSpring` Rune

```svelte
<script lang="ts">
  import { multiSpring } from '@stryde/motion-svelte';

  let revealed = $state(false);

  const motion = multiSpring(() => ({
    x: revealed ? 0 : -50,
    opacity: revealed ? 1 : 0,
    scale: revealed ? 1 : 0.9,
  }), {
    stiffness: 250,
    damping: 22,
  });
</script>

<div
  style="transform: translateX({motion.current.x}px) scale({motion.current.scale}); opacity: {motion.current.opacity}"
>
  <!-- content -->
</div>
```

#### 6.4.3 `$timeline` Rune

```svelte
<script lang="ts">
  import { timeline, onMount } from '@stryde/motion-svelte';

  let headerP = $state(0);
  let subtitleP = $state(0);

  const tl = timeline([
    {
      id: 'header',
      at: 0,
      duration: 400,
      animate: (p) => { headerP = p; },
    },
    {
      id: 'subtitle',
      at: 200,
      duration: 300,
      animate: (p) => { subtitleP = p; },
    },
    {
      id: 'cards',
      at: 300,
      duration: 500,
      stagger: { count: 4, delay: 80 },
      animate: (p, i) => { cardP[i] = p; },
    },
  ]);

  onMount(() => tl.play());

  const cardP = $state(Array(4).fill(0));
</script>
```

#### 6.4.4 Svelte `transition:` — Entrance/Exit

```svelte
<script lang="ts">
  import { springTransition } from '@stryde/motion-svelte';

  // Spring-based transition function
  const slideFade = springTransition({
    stiffness: 250,
    damping: 22,
    enter: (node, { duration = 400 }) => ({
      duration,
      css: (t) => `
        opacity: ${t};
        transform: translateY(${(1 - t) * 20}px);
      `,
    }),
    exit: (node, { duration = 300 }) => ({
      duration,
      css: (t) => `
        opacity: ${t};
        transform: translateY(${(1 - t) * -15}px);
      `,
    }),
  });

  let items = $state([...]);

  // Coordinated entrance stagger via delay param
  function staggeredSlideFade(node, { index, baseDelay = 0 }) {
    return slideFade(node, {
      delay: baseDelay + index * 60,       // 60ms per-item stagger
      duration: 400,
      stiffness: 250,
      damping: 22,
    });
  }
</script>

{#each items as item, i (item.id)}
  <div transition:staggeredSlideFade={{ index: i, baseDelay: 300 }}>
    <!-- item content -->
  </div>
{/each}
```

#### 6.4.5 `{#key}` Block Transitions (Page-Level)

```svelte
<script lang="ts">
  import { pageTransition } from '@stryde/motion-svelte';

  const { pathname } = $props();
</script>

{#key pathname}
  <div in:pageTransition={{ type: 'spring', stiffness: 200, damping: 24 }} out:pageTransition={{ type: 'spring', stiffness: 350, damping: 28 }}>
    <!-- routed content -->
  </div>
{/key}
```

#### 6.4.6 `<SharedElement>` Component

```svelte
<!-- ProductList.svelte -->
<script lang="ts">
  import { SharedElement, SharedElementGroup } from '@stryde/motion-svelte';
</script>

<SharedElementGroup id="gallery">
  {#each products as p (p.id)}
    <a href="/product/{p.id}">
      <SharedElement id="product-{p.id}">
        <img src={p.thumb} alt={p.name} />
      </SharedElement>
    </a>
  {/each}
</SharedElementGroup>

<!-- ProductDetail.svelte -->
<script lang="ts">
  import { SharedElement } from '@stryde/motion-svelte';
</script>

<SharedElement id="product-{product.id}">
  <img src={product.fullImage} alt={product.name} />
</SharedElement>
```

#### 6.4.7 Motion Tokens (Svelte)

```ts
// Reduced motion store
import { reducedMotion } from '@stryde/motion-svelte';

const springConfig = $derived(
  $reducedMotion
    ? { stiffness: 800, damping: 50 }
    : { stiffness: 170, damping: 26 }
);

// Stagger utility
import { staggerDelays } from '@stryde/motion-svelte';

const delays = staggerDelays(items.length, { perItem: 60, base: 0 });
// delays = [0, 60, 120, 180, ...]
```

---

## 7. Framework-Agnostic Token API Reference

All framework implementations share a common core. The core is exposed as `@stryde/motion-core` and re-exported by each framework adapter.

```ts
// Core exports
export { spring, multiSpring, SpringPreset } from './spring';
export { createTimeline, createScrollTimeline } from './timeline';
export {
  captureElementRect,
  animateSharedElement,
  SharedElementRegistry,
} from './shared-element';
export { staggerChildren, createStagger, staggerDelays } from './stagger';
export { prefersReducedMotion, useReducedMotionQuery } from './accessibility';
export type {
  SpringConfig,
  SpringState,
  TimelineSegment,
  TimelineState,
  SharedElementDescriptor,
  StaggerConfig,
  EasingFunction,
} from './types';
```

---

## 8. Accessibility & Performance

### 8.1 `prefers-reduced-motion`

Every motion primitive MUST respect the user's OS-level `prefers-reduced-motion` media query.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

In JavaScript, the system provides a reactive flag:

```ts
const prefersReduced = useReducedMotion(); // boolean
```

When `true`:
- Spring simulations snap to target instantly (stiffness=800, damping=50).
- Timelines skip to end state.
- Entrance/exit sequences become instant opacity toggles.
- Shared element morphs become instant snaps.

### 8.2 Performance Budget

| Metric | Target |
|---|---|
| JS execution per spring frame | < 1ms |
| Total frame budget (16.67ms) | < 8ms for JS |
| Memory per active spring | < 1KB |
| Timeline segment overhead | < 500B per segment |
| Shared element clone DOM cost | 1 element per morph |

### 8.3 Optimisation Strategies

1. **Web Animations API (WAAPI)** for timeline segments where spring physics aren't needed — offloads to compositor thread.
2. **`will-change`** hints applied during animation, removed on complete.
3. **`contain: layout style paint`** on animated containers.
4. **Batch reads and writes** — all `getBoundingClientRect` calls before any style mutations.
5. **`requestAnimationFrame` throttling** — at most one spring tick per rAF.

---

## 9. Package Structure

```
@stryde/motion-core/          # Framework-agnostic engine
  src/
    spring.ts                 # Spring simulation
    timeline.ts               # Timeline DAG + execution
    shared-element.ts         # Morph capture/clone/animate
    stagger.ts                # Stagger delay generators
    accessibility.ts          # prefers-reduced-motion
    easing.ts                 # Easing functions
    waapi.ts                  # WAAPI bridge
    types.ts                  # Shared type definitions
    index.ts                  # Public API surface

@stryde/motion-react/         # React adapter
  src/
    hooks/
      useSpring.ts
      useMultiSpring.ts
      useTimeline.ts
      useReducedMotion.ts
      useStagger.ts
    components/
      AnimatePresence.tsx
      SharedElement.tsx
      SharedElementGroup.tsx
      motion.tsx              # motion.div, motion.span, etc.
    index.ts

@stryde/motion-vue/           # Vue 3 adapter
  src/
    composables/
      useSpring.ts
      useMultiSpring.ts
      useTimeline.ts
      useReducedMotion.ts
      useStagger.ts
    directives/
      vSpring.ts
      vMultiSpring.ts
    components/
      SharedElement.vue
      SharedElementGroup.vue
      TransitionGroupSpring.vue
    index.ts

@stryde/motion-svelte/        # Svelte 5 adapter
  src/
    runes/
      spring.svelte.ts
      multiSpring.svelte.ts
      timeline.svelte.ts
      reducedMotion.svelte.ts
    transitions/
      springTransition.ts
      pageTransition.ts
      staggeredTransition.ts
    components/
      SharedElement.svelte
      SharedElementGroup.svelte
    index.ts
```

---

## 10. Usage Examples (End-to-End)

### 10.1 React: Product Gallery → Detail Page

```tsx
// ProductGallery.tsx
function ProductGallery() {
  const timeline = useTimeline([
    { id: 'header', at: 0,    duration: 400, animate: ... },
    { id: 'grid',   at: 200,  duration: 600, animate: ..., stagger: { count: 12, delay: 50 } },
  ]);
  useEffect(() => { timeline.play(); }, []);

  return (
    <SharedElementGroup id="catalog">
      {products.map(p => (
        <SharedElement key={p.id} id={`product-${p.id}`}>
          <ProductCard product={p} />
        </SharedElement>
      ))}
    </SharedElementGroup>
  );
}

// ProductDetail.tsx
function ProductDetail() {
  const timeline = useTimeline([...]);
  useEffect(() => { timeline.play(); }, []);

  return (
    <AnimatePresence>
      <SharedElement id={`product-${product.id}`}>
        <ProductHero product={product} />
      </SharedElement>
      {/* other detail content with staggered entrance */}
    </AnimatePresence>
  );
}
```

### 10.2 Vue: Notification Stack with Spring

```vue
<template>
  <TransitionGroup name="notification" tag="div" class="notification-stack">
    <div
      v-for="(note, i) in notifications"
      :key="note.id"
      class="notification-item"
      :style="{ '--stagger-index': i }"
    >
      {{ note.message }}
    </div>
  </TransitionGroup>
</template>

<script setup lang="ts">
import { spring } from '@stryde/motion-vue';

function onEnter(el, done) {
  const i = Number(el.style.getPropertyValue('--stagger-index'));
  spring({
    from: 0, to: 1,
    stiffness: 500, damping: 15,  // bouncy
    delay: i * 80,
    onUpdate: (v) => {
      el.style.opacity = v;
      el.style.transform = `translateX(${(1 - v) * 60}px) scale(${0.8 + v * 0.2})`;
    },
    onComplete: done,
  });
}
</script>
```

### 10.3 Svelte: Drag-to-Dismiss with Spring Return

```svelte
<script lang="ts">
  import { spring } from '@stryde/motion-svelte';

  let offsetX = $state(0);
  let dismissed = $state(false);

  const x = spring(() => dismissed ? 400 : offsetX, {
    stiffness: 180,
    damping: 14,
  });

  function handleDrag(e: MouseEvent) {
    offsetX = e.movementX;
  }

  function handleRelease() {
    if (Math.abs(offsetX) > 100) {
      dismissed = true;
    } else {
      offsetX = 0;
    }
  }
</script>

<div
  style="transform: translateX({x.current}px)"
  onmousedown={...}
  onmousemove={handleDrag}
  onmouseup={handleRelease}
>
  Swipe to dismiss
</div>
```

---

## 11. Summary

| Pillar | Key Deliverable | Cross-Framework |
|---|---|---|
| **Spring Physics** | Damped harmonic oscillator with stiffness/damping/mass presets | `useSpring` / `v-spring` / `$spring` |
| **Timeline Orchestration** | DAG-based segment scheduling, stagger, scroll-link, reverse-on-exit | `useTimeline` / composable / `$timeline` |
| **Entrance/Exit Sequences** | Staged entrance with stagger direction, interruptible exit protocol | `<AnimatePresence>` / `<TransitionGroup>` / `transition:` + `{#key}` |
| **Shared Element Transitions** | Capture → clone → morph → reveal lifecycle, grouped transitions | `<SharedElement>` in all three frameworks |
| **Motion Tokens** | Idiomatic APIs per framework, all backed by `@stryde/motion-core` | React hooks, Vue composables + directives, Svelte runes + transitions |

All primitives are performance-budgeted, accessibility-aware, and designed to compose naturally with each framework's reactivity model.

---

*Generated by `motion-design-spec-writer` (c2) — Stryde Forge Refinery. Run `run-20260626-020000`.*
