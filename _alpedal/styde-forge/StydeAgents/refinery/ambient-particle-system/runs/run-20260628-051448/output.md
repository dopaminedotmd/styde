BLUEPRINT: Ambient Particle System
Domain: frontend
Version: 3
Purpose
Canvas-based particle system rendered behind dashboard panels. Embers, sparks, and heat haze that visualize forge activity in real time. More forge events = higher particle density and livelier motion. Agent promotions trigger a directional burst. GPU temperature maps to particle color ramp (cool blue, amber, hot red). Mobile and battery-sensitive environments default to off.
Particle Types and Behaviors
Ember:
  Source: spawns at random bottom-edge positions
  Motion: slow upward drift with horizontal sway (Perlin noise)
  Lifetime: 6000-12000 ms
  Size: 1.5-3 px
  Color: maps to gpuTemp via HSL — 0-40 C = blue (210deg), 40-60 C = amber (30deg), 60-85+ C = red (0deg), interpolated linearly between thresholds
  Decay: alpha fades in over 400 ms, holds, then fades out over last 2000 ms
Spark:
  Source: spawns near forge event positions (random 30 px jitter)
  Motion: fast diagonal burst, decelerates, then gentle drift
  Lifetime: 400-1200 ms
  Size: 1-2.5 px
  Color: white-to-yellow with gpuTemp tint
  Decay: alpha fades out over entire lifetime
Heat Haze:
  Source: emitted continuously from hot regions (gpuTemp > 50 C)
  Motion: vertical rise with strong horizontal distortion, sinusoidal
  Lifetime: 2000-4000 ms
  Size: 8-20 px semi-transparent ellipse
  Color: matches gpuTemp at emission time, alpha 0.03-0.08
  Decay: alpha fade entire lifetime, slight scale growth
Data Reactivity
forgeActivityFactor:
  range: [0.0, 1.0], default: 0.0
  Deltas: each completed run event = +0.1 (decays 0.02 per second), each agent promotion = +0.15 (decays 0.03 per second), each error/retry = -0.05 (decays 0.01 per second). Clamped to [0.0, 1.0] after every update.
  Effect: scales max particle budget linearly. budget = floor(50 + forgeActivityFactor * 150). At 0.0 = 50 particles minimum, at 1.0 = 200 particles maximum.
gpuTemp:
  range: [0, 100], unit: Celsius
  Effect: color ramp as described in Ember color mapping above
  Note: when gpuTemp is unavailable or NaN, default to 45 C (mid-amber)
promote event:
  Effect: instant burst of 15-25 sparks from a random screen position. Burst spawns are exempt from per-frame spawn cap (throttle rules below). Burst sparks have 1.5x speed multiplier and their color shifts +30deg toward red.
Architecture
Data structure: ActiveParticles
  A flat array of particle objects. No pool alloc/dealloc semantics. Dead particles are marked with alive: false. Every render frame, the update pass filters dead particles with a single splice sweep (index-reversed loop) to compact the array. This avoids allocation churn while keeping the API surface at push/pop.
Render loop and spawn throttling (single authoritative section):
  Loop: requestAnimationFrame drives a single update+render tick per frame.
  Per-frame steps:
    1. Compute forgeActivityFactor delta decay and re-clamp.
    2. Compute budget = floor(50 + forgeActivityFactor * 150).
    3. Spawn new particles: if ActiveParticles.length < budget, sample Poisson-distributed interval (mean 100 ms converted to per-frame probability). Cap spawns at floor(budget * 0.1) per frame to avoid visual spikes.
    4. Update each particle position, velocity, alpha, age.
    5. Remove dead particles (alive === false) via index-reversed splice.
    6. Render all alive particles to canvas in a single draw pass.
  Throttle: spawn rate is governed entirely by the Poisson interval and per-frame cap above. No additional spawn cooldown is needed — duplicating throttle logic here would be redundant because the per-frame cap already prevents burst frames. See spawn cap above as the single constraint.
Canvas layer:
  - Position: absolute, inset 0, z-index 0 behind dashboard panels
  - Pointer-events: none so interactions pass through
  - Size: full viewport, resized on window resize (debounced 200 ms)
  - DPI: devicePixelRatio scaling via canvas width/height attributes, CSS size unchanged
Settings toggle:
  - Schema key: ambientParticles
  - Default: true on desktop (window.innerWidth > 768 and not 'reduce-motion' prefers-reduced-motion), false on mobile or battery (navigator.getBattery API if available)
  - Location: Settings panel, visual category, toggle labeled "Ambient particles"
  - Toggle off kills the rAF loop immediately and clears canvas
  - Toggle on starts a fresh rAF loop (particles start from zero, no reservoir)
Performance constraints:
  - Max 200 particles alive at any time (budget-clamped)
  - No allocation in hot path — particle objects are reused in place, only dead removal splices the array
  - rAF loop pauses when tab is hidden (Page Visibility API)
  - Canvas composite operation: 'lighter' for sparks (additive blend), 'source-over' for embers and haze
  - OffscreenCanvas considered if per-frame draw time exceeds 8 ms on 3 consecutive frames — feature-detect and migrate transparently
Cross-references (constraints stated at point of use; no separate consistency block):
  - Budget clamp and per-frame spawn cap are defined above in Render loop and spawn throttling — refer to those values wherever spawn logic is evaluated.
  - Particle color ramp is defined under Ember color mapping — all particle types that reference gpuTemp defer to that single definition.
  - Mobile/battery default-off is defined under Settings toggle — no separate accessibility section needed.