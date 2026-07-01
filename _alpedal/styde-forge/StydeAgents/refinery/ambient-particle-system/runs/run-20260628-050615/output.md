Ambient Particle System
Domain: frontend
Version: 2
Purpose
Canvas-based particle system rendering behind dashboard panels as ambient data visualization. Embers, sparks, and heat haze react to forge activity level and agent promotion events. More forge activity = higher spawn rate. Promotions trigger directional particle bursts. GPU temperature drives particle color ramp from cool blue through amber to hot red. System is toggleable via settings panel and off by default on mobile or battery-constrained devices.
Features
  Canvas renderer: Canvas2D with devicePixelRatio-aware backing store. WebGL is not required for particle counts under 200 and introduces unnecessary GPU context overhead for background rendering.
  Lazy loading: Instantiate canvas and animation loop on first user interaction with the dashboard panel. No allocation on page load. Destroy on panel close.
  Window resize: Debounced resize handler (150 ms) resets canvas dimensions to panel client rect. Particles reflow relative to new bounds — no burst or cull on resize.
  Particle physics: Ember rise (slow upward drift with sinusoidal lateral sway). Spark burst (fast radial ejection from a point, decelerating toward rest). Heat haze distortion (low-frequency noise applied to nearby particle positions creating shimmer).
  Data reactivity: spawnRate = min(2, floor(activityLevel / 10)). GPU temp maps 30 C–90 C to HSL hue 240 → 0. Promotion events inject 40 sparks from the center of the active panel. Fallback color when temp is unavailable: HSL 40, 80%, 60% (amber default).
  Performance: Hard cap at 200 particles. requestAnimationFrame with frame delta normalization. Cull particles below alpha 0.02 or beyond 5 s lifetime. Skip render when document.hidden is true.
  Toggle: On by default on desktop with AC power. Off by default on mobile or battery. Toggle stored in localStorage key: ambient_particles_enabled. Settings panel checkbox reads/writes same key and dispatches a custom event 'particle:toggle' with detail.bool.
Data pipeline
  activityLevel: Ingested from forge engine via window.__FORGE_STATE__.activityLevel (integer 0–100). Polled every 2 s inside the animation loop. Fallback value: 0.
  gpuTemp: Ingested from performance monitor via window.__FORGE_STATE__.gpuTemp (float, Celsius). Polled every 5 s. Fallback value: null (triggers default amber color).
  promotionFlag: Boolean from window.__FORGE_STATE__.promoted. Consumed once per frame; after burst emission the flag resets to false. No fallback — absence means no burst.
  All three keys are optional in __FORGE_STATE__. Missing keys use fallbacks silently. No error thrown.
Bundle-size budget
  Total module (ESM): max 6 kB gzipped. With zero runtime dependencies.
  Canvas layer creation and particle update loop: 3 kB.
  Color math and temp ramp lookup: 1 kB.
  Toggle logic, localStorage, event dispatch, mobile/battery detection: 1 kB.
  Comments and whitespace stripped in production build. No tree-shaking boundary violations.
  CI gate: PRs exceeding budget fail build step. Check runs on `npm run build -- --analyze` via bundlesize or size-limit tool.
Deliverable guardrail
  This blueprint is the final deliverable artifact. No summary, diff log, or excerpt shall be produced in its place. The complete artifact is written and presented in full. Consumers read this file, not a report about it.
Canvas renderer
  Context: Canvas2D. createElement('canvas') appended to panel container. CSS position: absolute; inset: 0; pointer-events: none; z-index: 0. Backing store size = panel.clientWidth * devicePixelRatio, panel.clientHeight * devicePixelRatio. CSS size = panel.clientWidth x panel.clientHeight px. Clear entire canvas each frame via clearRect. No WebGL — overhead unjustified for sub-200 particles.
Lazy loading strategy
  Init hook: Event listener on dashboard panel for 'mouseenter'. First mouseenter calls initParticleSystem() which creates canvas, reads __FORGE_STATE__, starts rAF loop, then removes the listener. If toggled off, listener never fires.
  Destroy: On panel 'remove' event or custom 'velocity-sidebar:close', cancel rAF, remove canvas from DOM, null refs.
  Re-init on re-open follows same mouseenter pattern. Canvas instance is ephemeral.
Window resize handling
  Listener on window 'resize' debounced at 150 ms via requestAnimationFrame coalescing. On fire: read panel.getBoundingClientRect(), resize canvas backing store, resize CSS dimensions. No particle repositioning — they continue physics from current positions within new bounds. Particles outside new bounds are culled on next frame bounds check.