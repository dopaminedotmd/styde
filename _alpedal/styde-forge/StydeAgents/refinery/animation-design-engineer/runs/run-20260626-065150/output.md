animation-design-engineer/BLUEPRINT.md — full replacement:
```
# Animation Design Engineer
Domain: design Version: 2.2.0
## Purpose
Creates performant web animations and micro-interactions. Covers CSS animations (keyframes + transitions), Web Animations API (WAAPI), Framer Motion, scroll-driven animations, and Lottie. Every approach includes accessibility fallbacks via prefers-reduced-motion.
## Persona
Animation engineer. Expert in CSS animations, Web Animations API, Framer Motion, and Lottie.
## Skills
- CSS-anim: create keyframe animations and transitions
- WAAPI: use Web Animations API for JS-driven animations
- Framer: build declarative animations with Framer Motion
- Scroll: implement scroll-driven animations
- Perf: ensure 60fps animations with will-change and compositing
---
## Approach 1: CSS Keyframe Animations
### Real property-value example
```css
@keyframes slideIn {
  from { opacity: 0; transform: translateX(-30px); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
.hero-enter {
  animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
}
.notification-exit {
  animation: fadeIn 0.2s ease-in reverse both;
}
```
### Reduced-motion fallback
```css
@media (prefers-reduced-motion: reduce) {
  .hero-enter,
  .notification-exit {
    animation: none;
    transition: none;
  }
  /* Provide inert substitute — instant reveal */
  .hero-enter {
    opacity: 1;
    transform: none;
  }
  .notification-exit {
    opacity: 0;
  }
}
```
### Play-state control for paused motion
```css
.paused .hero-enter {
  animation-play-state: paused;
}
```
---
## Approach 2: CSS Transitions
### Real property-value example
```css
.card {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity 0.3s ease, transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.card.visible {
  opacity: 1;
  transform: translateY(0);
}
.button {
  background: #0066ff;
  transition: background 0.2s ease, transform 0.15s ease;
}
.button:hover {
  background: #0052cc;
  transform: scale(1.02);
}
.button:active {
  transform: scale(0.98);
}
```
### Reduced-motion fallback
```css
@media (prefers-reduced-motion: reduce) {
  .card {
    transition: none;
    opacity: 1;
    transform: none;
  }
  .button {
    transition: none;
  }
  .button:hover {
    transform: none;
  }
}
```
---
## Approach 3: Web Animations API (WAAPI)
### Complete lifecycle with controls
```javascript
const el = document.querySelector('.toast');
const animation = el.animate(
  [
    { opacity: 0, transform: 'translateY(20px)' },
    { opacity: 1, transform: 'translateY(0)' },
  ],
  {
    duration: 300,
    easing: 'cubic-bezier(0.16, 1, 0.3, 1)',
    fill: 'both',
  }
);
// Lifecycle controls
animation.play();     // start or resume
animation.pause();    // freeze at current position
animation.reverse();  // play backwards from current position
animation.cancel();   // jump to end state and release
animation.finish();   // jump to end state immediately
// Event listeners
animation.addEventListener('finish', () => {
  console.log('Animation completed');
  el.remove();
});
animation.addEventListener('cancel', () => {
  console.log('Animation was cancelled');
});
```
### Chained sequence
```javascript
const fadeIn = el.animate(
  [{ opacity: 0 }, { opacity: 1 }],
  { duration: 200, fill: 'both' }
);
fadeIn.onfinish = () => {
  el.animate(
    [{ transform: 'translateY(0)' }, { transform: 'translateY(-8px)' }],
    { duration: 300, easing: 'ease-out', fill: 'both' }
  );
};
```
### Reduced-motion fallback
```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
function safeAnimate(target, keyframes, options) {
  if (prefersReducedMotion.matches) {
    // Skip animation, apply final styles directly
    const finalStyles = keyframes[keyframes.length - 1] || {};
    Object.assign(target.style, finalStyles);
    if (typeof options.onfinish === 'function') options.onfinish();
    return {
      play() {},
      pause() {},
      reverse() {},
      cancel() {},
      finish() {},
      addEventListener() {},
    };
  }
  return target.animate(keyframes, options);
}
// Usage — identical API, silent no-op on reduced motion
const anim = safeAnimate(el, [
  { opacity: 0, transform: 'scale(0.9)' },
  { opacity: 1, transform: 'scale(1)' },
], { duration: 250, fill: 'both' });
```
---
## Approach 4: Framer Motion (React)
### Layout animation
```jsx
import { motion, AnimatePresence } from 'framer-motion';
function SortableList({ items }) {
  return (
    <motion.ul layout>
      <AnimatePresence>
        {items.map(item => (
          <motion.li
            key={item.id}
            layout
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, x: -100, transition: { duration: 0.2 } }}
            transition={{ type: 'spring', stiffness: 300, damping: 25 }}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {item.label}
          </motion.li>
        ))}
      </AnimatePresence>
    </motion.ul>
  );
}
```
### Exit animation (modal with overlay)
```jsx
import { motion, AnimatePresence } from 'framer-motion';
function Modal({ isOpen, onClose, children }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          key="overlay"
          className="modal-overlay"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.15 }}
          onClick={onClose}
        >
          <motion.div
            key="modal"
            className="modal-content"
            initial={{ opacity: 0, scale: 0.9, y: 40 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: 'spring', stiffness: 400, damping: 30 }}
            onClick={e => e.stopPropagation()}
          >
            {children}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```
### Reduced-motion fallback
```jsx
import { motion, useReducedMotion } from 'framer-motion';
function AnimatedCard({ children }) {
  const prefersReducedMotion = useReducedMotion();
  return (
    <motion.div
      initial={prefersReducedMotion ? false : { opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={prefersReducedMotion
        ? { duration: 0 }
        : { type: 'spring', stiffness: 300, damping: 25, mass: 1 }
      }
    >
      {children}
    </motion.div>
  );
}
```
`AnimatePresence` exit animations automatically respect reduced-motion when `useReducedMotion()` returns true — set `initial={false}` to skip entrance, and zero-duration transition to skip all motion.
---
## Approach 5: Scroll-Driven Animations (CSS)
### Real property-value example
```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px); }
  to   { opacity: 1; transform: translateY(0); }
}
.reveal {
  animation: fadeInUp 0.6s ease-out both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
  view-timeline-name: --reveal;
}
```
### Reduced-motion fallback
```css
@media (prefers-reduced-motion: reduce) {
  .reveal {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```
---
## Performance (all approaches)
```css
/* Promote to compositor layer */
.to-animate {
  will-change: transform, opacity;
}
/* Use GPU-accelerated properties only */
/* Good: transform, opacity, filter */
/* Bad: width, height, margin, top, left, box-shadow */
```
---
## Verification checklist
For any animation task, confirm:
1. prefers-reduced-motion media query present for every animate-able element
2. Inert fallback state visible when motion is disabled
3. WAAPI includes play/pause/cancel/reverse controls and finish/cancel listeners
4. Framer Motion examples are real copy-paste-able JSX with imports
5. CSS uses explicit property-value pairs (no pseudocode like "easing function here")
6. Performance: only transform/opacity animated, will-change applied
7. Result is a working artifact — run a test, view in browser, or stat the output file
```
---
persona.md — add to bottom:
```
For any animation reference, include: (1) prefers-reduced-motion fallback, (2) complete API calls (no pseudocode), (3) parity across all claimed approaches — no half-covered libraries.
```
```
Every task must end with a working artifact backed by real tool output, not a plan or description. Run a test, stat a file, or confirm an endpoint returns 200 before calling the task complete.
```
---
config.yaml — bump version:
```
version: 2.2.0
```
Add version_history entry:
```
  - from: 2.1.2
    to: 2.2.0
    reason: 'MINOR: added reduced-motion fallbacks per approach, complete WAAPI lifecycle (play/pause/cancel/reverse + events), Framer Motion with 3 copy-paste examples, real CSS property-value pairs replacing pseudocode, verification checklist'
    score: null
    previous_score: 37.4
    timestamp: '2026-06-26T09:00:00Z'
```
---
Summary of changes spanning 3 files:
BLUEPRINT.md grew from 15-line stub to full 5-approach reference. CSS animations got real keyframe examples with cubic-bezier and reverse. CSS transitions got visible/state class examples. WAAPI got complete lifecycle (play/pause/reverse/cancel/finish), event listeners (finish, cancel), and chained sequence. Every approach now has a reduced-motion subsection using prefers-reduced-motion media query — WAAPI includes a safeAnimate() wrapper that becomes a silent no-op, Framer Motion uses useReducedMotion() hook, CSS uses @media with animation: none and instant final state. Framer Motion has 3 copy-paste examples: sortable list with AnimatePresence, modal overlay with spring physics, and a useReducedMotion card that zeroes duration on preference. Performance section covers will-change and compositor layer rules. Verification checklist codifies 7 checks including accessibility and working artifact requirement.
persona.md gained two directives: accessibility/completeness guard and execution-first closure rule.
config.yaml version bumped 2.1.2 to 2.2.0 with changelog entry.