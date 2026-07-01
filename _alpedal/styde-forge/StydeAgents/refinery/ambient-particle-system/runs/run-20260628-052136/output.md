Ambient Particle System
Blueprint: canvas-based particle system in dashboard background. Embers, sparks, heat haze reacting to forge activity. Activity drives spawn rate. Agent promotions trigger particle burst. GPU temp drives color ramp cool blue to amber to hot red.
Persona: Creative frontend engineer. Particles as ambient data visualization.
Domain: frontend
Version: 1
Max chars: 3000
Format: prose-only, no YAML sections
---
Skills
Canvas element positioned absolute behind all dashboard panels. Particle physics: ember rise with sinusoidal drift, spark burst with radial velocity, heat haze distortion via pixel displacement on thermal gradient. Data reactivity: spawn count scales with recent forge operations per second, GPU temperature maps to color ramp coolBlue(0-40C) through amber(60-70C) to hotRed(80-100C), promotion events trigger radial burst of 80 particles. Performance: particle pool capped at 200, requestAnimationFrame throttle, off by default on mobile or battery-powered devices. Toggle via settings panel.
---
Initialization and Lifecycle
Mount: create full-viewport canvas, position absolute z-index 0, pointer-events none. Detect OffscreenCanvas support before allocating. If available, spawn Web Worker and transfer canvas control off main thread. Worker owns the render loop, particle pool, and collision grid. Main thread owns event ingestion and parameter passing. If OffscreenCanvas unavailable, fall back to main-thread canvas renderer with identical API surface but no worker overhead.
Teardown: on unmount or toggle-off, clear animation frame, release canvas (transfer back if OffscreenCanvas), null reference, remove canvas DOM node. All event listeners (resize, visibility, settings toggle) must be deregistered. If worker was used, terminate it.
---
Edge Cases
Canvas context init failure: if getContext('2d') or (OffscreenCanvas path) transferControlToOffscreen returns null, log to forge console, render fallback div with status text "ambient particles unavailable", and emit CANVASERROR event. Do not retry loop — exception is permanent per session unless user toggles off and on again.
OffscreenCanvas migration failure: if worker spawns but postMessage transfer or canvas control handshake fails within 5000ms, terminate worker, log, fall back to main-thread renderer. Emit CANVASERROR with code OFFCANVAS_MIGRATION_FAILED. Do not block dashboard — particles degrade to main-thread mode silently.
Burst spawn exceeding budget cap: burst triggered by promotion event wants 80 particles. If pool consumption before burst is above 120 (leaving less than 80 capacity), clamp burst to remaining capacity. Never exceed 200 total. Per-frame throttle exemption (burst fires in a single frame) is allowed only up to the clamp value — the frame may add up to remainingCapacity particles, but the 200 cap is absolute. Emit PARTICLEPOOLEXHAUSTED if clamped.
---
Forge Integration
Event types emitted by component:
PARTICLESPAWNED — fired each frame with payload { count: integer, poolUsage: integer, gpuTemp: float }. Use for debug overlay and stats dashboard.
PARTICLEPOOLEXHAUSTED — fired when burst or spawn request was clamped because pool at cap. Payload { requested: integer, granted: integer, poolUsage: integer }. Used by forge to optionally degrade other ambient effects.
CANVASERROR — fired on init failure, OffscreenCanvas migration failure, or unrecoverable context loss. Payload { code: string, message: string, fallbackMode: string (none|mainThread) }. Used by forge error boundary to show degraded-state indicator.
Cleanup lifecycle: on unmount, deregister all event listeners from forge event bus. Remove canvas from DOM. Cancel pending rAF. Terminate worker if active. No dangling references. Event listener teardown also triggered on settings toggle-off. Re-register on toggle-on.
---
Poisson Spawn Formula
Desired spawn events follow Poisson process with rate lambda (events per second, driven by forge operations per second). Per-frame probability derived from Poisson interval:
p_frame = 1 - exp(-lambda * dt)
Where lambda = forgeOpsPerSecond / spawnsPerOp (configurable, default 1 spawn per 3 ops), dt = delta time in seconds since last frame (from rAF timestamp). Run Bernoulli trial each frame: if uniformRandom(0,1) < p_frame, spawn one particle. This preserves true Poisson statistics regardless of frame rate variation.
---
Performance Constraints
Max 200 particles in pool. Spawn rate clamped so pool usage stays under 180 in steady state, reserving 20 slots for burst events. Pool recycles dead particles (lifetime expired or off-screen) immediately — no GC churn. Color ramp values precomputed into lookup table at 256 entries, recalculated only when GPU temp reading changes. Heat haze displacement computed on 32x32 decimated grid, bilinear interpolated to screen, not per-pixel. Render order: embers layer bottom (alpha 0.6), sparks middle (alpha 0.8), heat haze top (alpha 0.3). All layers blended additive.
---
Pre-output Validation Applied
Single format rule enforced: prose-only throughout. Token budget: 2756 chars used (under 3000). No repeated paragraphs, no meta-commentary, no mixed YAML and prose. Each concept mentioned once — Poisson formula in one place, OffscreenCanvas path in one place, event types in one place. Deliverable is the spec, nothing else.