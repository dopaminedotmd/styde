ambient-particle-system-v1
Domain: frontend
Version: 1
Purpose
Canvas-based particle system rendered behind dashboard panels as ambient data visualization. Embers rise, sparks burst on activity, heat haze distorts the scene. Particle intensity reacts to forge state: spawn rate scales with activity level, color ramps from cool blue through amber to hot red based on GPU temperature proxy, and agent promotions trigger particle bursts.
Persona
Creative frontend engineer. Particles as ambient data visualization, never decorative fluff.
Features
- Renders behind all dashboard panels via absolute positioning and z-index layering
- Three particle types: slow ember rise (lifespan 4000-8000ms), fast spark burst (lifespan 800-2000ms), heat haze distortion layer (sinusoidal warp with simplex noise frequency 0.02)
- Spawn rate = max(1, floor(activityLevel / 5)) particles per frame, clamped to max 200 total
- Particle color ramp driven by proxy gpuTemp: cool blue (hsl(220deg 80% 60%)) at 0%, amber (hsl(40deg 80% 60%)) at 50%, hot red (hsl(0deg 80% 55%)) at 100%
- Agent promotion triggers 12-24 spark burst particles expanding radially from a random screen position
- GPU temp proxy derived from activityLevel * 0.7 + smooth noise offset, updated every 5s
- Performance cap: max 200 concurrent particles, render loop throttled via requestAnimationFrame with frame skip when tab hidden
- Toggle via dashboard settings panel, off by default on mobile or battery-powered devices
- Lazy-load: canvas created on first toggle-on, destroyed on toggle-off; no upfront cost
- Canvas renderer: Canvas2D (not WebGL). Particle count is low, 2D compositing is sufficient and avoids WebGL context limits on dashboard with multiple canvases
- Window resize: canvas dimensions updated on resize via ResizeObserver on parent panel element; particle positions are not repositioned (background particles drifting off-screen is acceptable), but spawn bounds are recalculated to match new dimensions
- promotionFlag is polled every 5s (data pipeline path), NOT consumed per-frame. When poll returns true, burst is dispatched and flag is reset. Per-frame physics loop only reads particle state, never promotion state directly
Implementation Notes
- Single <canvas> element, position: fixed, pointer-events: none, z-index: 0
- Particle pool allocated once at max size (200), avoid alloc/dealloc in hot path
- Simplex noise implementation for heat haze: use open-source simplex-noise npm package or hand-rolled 2D simplex seeded with Date.now()
- Color interpolation via HSL lerp across the three-stop ramp, not RGB
- Burst: spread angle random 0-2PI, initial velocity 2-6px/frame, gravity 0.02px/frame² downward after burst
- Off-screen particles killed immediately to avoid stale-state bloat
- Frame skip: skip every other frame when document.hidden to conserve battery