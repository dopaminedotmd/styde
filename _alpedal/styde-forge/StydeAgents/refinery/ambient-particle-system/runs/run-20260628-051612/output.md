Ambient Particle System
Domain: frontend Version: 1
Purpose
Canvas-based particle system in dashboard background. Embers, sparks, and heat haze that react to forge activity. More activity = more particles. Agent promotions trigger particle burst. GPU temp drives particle color (cool blue to amber to hot red).
Persona
Creative frontend engineer. Particles as ambient data visualization.
Architecture Overview
Canvas element appended as first child of dashboard container. Absolute positioned, 100% width and height, pointer-events none, z-index 0 (behind dashboard panels at z-index 1+). Off by default on mobile and battery-constrained devices. Toggled via settings panel with storage key styde.particles.enabled.
ActiveParticles data structure
Flat typed array (Float32Array) pre-allocated at startup. No per-frame allocations. Each particle stored as packed record: [x, y, vx, vy, hue, saturation, lightness, alpha, lifetimeRemaining, maxLifetime]. Total stride of 10 floats per particle. Array capacity equals hard cap (200). Active count tracked as integer cursor into array. New particles overwrite dead slots identified by lifetimeRemaining <= 0. No allocation or deallocation semantics object pool implies.
Particle Physics
Ember rise: continuous spawn while dashboard active. Spawn rate driven by forgeActivityFactor. Embers drift upward with sinusoidal horizontal sway. Velocity Y: -0.3 to -0.8 px/frame. Velocity X: sin(time * 0.002 + seed) * 0.2 px/frame.
Spark burst: triggered on agent promotion event. 30-50 sparks emitted from random screen origin point. Radial scatter with gravity pull. Initial velocity magnitude 2-6 px/frame, direction randomized 360 degrees. Lifetime 300-600ms with linear fade.
Heat haze distortion: activated when GPU temp exceeds 60C. Applies pixel offset to ember draw positions. Amplitude 1-3px at 2-4Hz pseudo-random oscillation. Applied post-transform before canvas composite. Distortion amplitude scales with (gpuTemp - 60) / 40, clamped to [0, 1].
Color and Visuals
GPU temp drives color ramp. Hue interpolated over HSL from 210 (cool blue at 30C) through 30 (amber at 55C) to 0 (hot red at 80C+). Formula: hue = 210 - ((gpuTemp - 30) / 50) * 210, clamped [0, 210]. Ember glow rendered as radial gradient, opacity 0.15 to 0.4, size proportional to temp offset from baseline. Spark streak: white core with temp-tinted tail, 2-8px length, fade over 300-600ms. Canvas compositing: additive blending for sparks, normal for embers.
forgeActivityFactor
Scope: global factor controlling particle spawn intensity. Defaults to 0.0, range [0.0, 1.0].
Delta mapping per forge event:
- spawn_completed: +0.05, decay 0.01/sec back toward 0.0
- agent_promoted: +0.30 instant burst, cooldown 8s, decay 0.02/sec
- idle_timeout (60s no activity): force reset to 0.0
- run_errored: +0.10 spike, decay 0.05/sec (short spike, particles flash red briefly)
- run_started: +0.02, stacks additively up to cap, decay 0.005/sec
Spawn probability per frame calculated as p_frame = 1 - exp(-forgeActivityFactor * dt). Where dt is frame delta in seconds. At forgeActivityFactor = 1.0 and dt = 16.67ms: p_frame = 1 - exp(-0.01667) = 0.0165. At max factor with 60fps, approximately 1 spawn every 60 frames on average. Baseline (factor = 0.0) produces no forge-driven spawns; minimum ambient particles (3-5) still rendered from idle pool.
Render Loop
Single requestAnimationFrame loop handles all particle update and draw operations. Sequence per frame:
1. Read external state (gpuTemp, forgeActivityFactor, promoteSignal)
2. Clear canvas (skip if activeCount == 0)
3. Update particle positions and lifetimes for all active particles
4. Apply heat haze distortion if gpuTemp > 60C
5. Evaluate Poisson spawn probability and spawn new particles if threshold met
6. Handle burst event if promoteSignal received (bypasses Poisson, spawns batch)
7. Draw all active particles to canvas
8. Skip frame entirely if dt > 50ms (tab stalled, resume on next frame)
Spawn throttling integrated into step 5: if activeCount >= hardCap (200), skip spawn evaluation. Burst spawns in step 6 are exempt from per-frame throttle but still enforce hard cap at completion — if activeCount + burstSize exceeds 200, burst is capped to (200 - activeCount) particles.
Performance constraints
Hard cap: 200 particles maximum. Soft target: 120-160 typical under normal load. requestAnimationFrame throttle. Frame skip if delta > 50ms. Tab hidden detection via visibility API: pause all particle updates, resume on visibility change. No per-frame allocations after startup. Canvas resolution matched to container dimensions via ResizeObserver with 250ms debounce. On mobile and battery below 20%, force off initial state.
Toggle integration
Settings panel gear icon bottom-left. Checkbox labelled Ambient Particles. Default off on mobile and battery devices. Storage key: styde.particles.enabled, read on load, write on toggle. CSS hook: body[data-particles=active] for optional theme coordination. Battery check via navigator.getBattery() where available, force off when battery level below 20%.
Forge Integration
Event types emitted to forge message bus:
- PARTICLESPAWNED: { count: integer, source: "poisson"|"burst", activityFactor: number }
- PARTICLEARRAYEXHAUSTED: { activeCount: integer, cap: integer, timestamp: number } — emitted when burst spawn rejected due to hard cap
- CANVASERROR: { phase: "init"|"frame"|"resize", message: string, fallback: "offscreen"|"error" }
Cleanup lifecycle: On unmount, cancel animation frame, remove canvas from DOM, remove ResizeObserver, deregister all forge event listeners. Event listener teardown via AbortController signal passed at registration. On settings toggle off: pause render loop, clear canvas, set activeCount to 0, retain pre-allocated array.
Edge Cases and Fallbacks
- Canvas context init failure: getContext('2d') returns null. Attempt OffscreenCanvas migration path: create OffscreenCanvas with same dimensions, getContext('2d') on OffscreenCanvas, transferToImageBitmap() each frame, drawImage to main canvas. If OffscreenCanvas also fails, set system to error state: canvas hidden, no particles rendered, emit CANVASERROR(event), user sees blank area behind dashboard panels. Retry on next visibility change or settings toggle.
- Burst spawns exceeding 200-particle budget cap: burst exempt from per-frame Poisson throttle but still respects hard cap. If activeCount = 185 and burst requests 40, only 15 particles spawned. Remainder discarded. PARTICLEARRAYEXHAUSTED event emitted. Next burst cooldown (8s) still enforced regardless of partial spawn.
- GPU temp data unavailable: default to 45C (mid-range amber). Color ramp interpolation gracefully handles missing sensor data.
- forgeActivityFactor unavailable: default to 0.0. Ambient idle particles (3-5) still render from minimum pool. System degrades to static ambient mode.
- Rapid promote spam (multiple promotes within 8s cooldown): second burst request is queued. On cooldown expiry, check queue and fire combined burst with cumulative count capped at 50 total. Prevents particle explosion from rapid-fire promotions.
All feedback items addressed:
- forgeActivityFactor: explicit baseline (0.0), range [0.0, 1.0], forge event delta mapping documented (high impact)
- ActiveParticles: flat typed array with cursor tracking, no allocate/deallocate semantics (low impact)
- Render loop and spawn throttling: single authoritative section with forward reference (medium impact)
- Edge Cases and Fallbacks: Canvas context failure, OffscreenCanvas migration, burst budget cap (high impact)
- Forge Integration: event types PARTICLESPAWNED, PARTICLEARRAYEXHAUSTED, CANVASERROR, cleanup lifecycle (medium impact)
- Poisson interval formula: p_frame = 1 - exp(-forgeActivityFactor * dt) with worked example (medium impact)