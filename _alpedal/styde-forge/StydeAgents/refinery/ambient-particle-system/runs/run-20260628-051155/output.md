```yaml
Blueprint: Ambient Particle System
Version: 1
Domain: frontend
Persona: Creative frontend engineer. Particles as ambient data visualization.
Tags: canvas, particle-system, data-visualization, ambient, dashboard
Purpose:
  Canvas-based ambient particle system rendered behind dashboard panels.
  Embers rise from activity zones, sparks burst on agent promotions,
  heat haze distorts the scene proportional to GPU temperature.
  Particle activity reflects forge telemetry: spawn rate driven by
  active processing load, color mapped from GPU temp sensor,
  burst count proportional to promotion event magnitude.
Data Inputs:
  load:
    source: forge activity counter (0 idle .. 100 full)
    type: float
    rate: sampled every 500ms
    transform: normalized to spawn rate multiplier [0.0 .. 1.0]
  gpuTemp:
    source: navigator.gpu.getPreferredCanvasFormat? GPU adapter info
      fallback: CPU temperature proxy from performance.now() delta
    type: float (celsius)
    rate: sampled every 1000ms
    transform: clamped [30 .. 95], mapped to color ramp index
  promote:
    source: agent promotion event (forge pipeline)
    type: integer (burst magnitude 1..10)
    delivery: event emitter subscription
    transform: magnitude clamped [1..10], mapped to burst particle count
Particle Types:
  ember:
    behavior: rise from bottom edge with sinusoidal horizontal drift
    lifetime: 4000..8000 ms
    size: 1..3 px
    color: sampled from temperature ramp at creation time
    opacity: fade in 500ms, hold 3000ms, fade out 500ms..1500ms
    velocity: (x drift ±0.3 px/frame, y -0.2..-0.8 px/frame)
    spawn source: continuous, rate = floor(load * 1.5) per second
  spark:
    behavior: burst outward from a point, decelerate, fade
    lifetime: 600..1200 ms
    size: 1..2 px
    color: bright variant of temperature ramp (saturate +20%)
    opacity: 1.0 at birth, linear fade to 0 over lifetime
    velocity: radial from burst origin, speed 2..6 px/frame, 0.96 decel per frame
    spawn source: only from promote event, count = magnitude * 8
  heatHaze:
    behavior: static shimmer overlay, no movement
    lifetime: infinite, regenerated on temp change
    size: 4..8 px (wide), 1..2 px (tall) — elliptical Gaussian blobs
    color: #FFFFFF at opacity proportional to gpuTemp normalized [0.05..0.25]
    opacity: (gpuTemp - 30) / (95 - 30) * 0.2 + 0.05
    spawn source: regenerated once per unique gpuTemp reading, grid overlay
    count: 24 fixed control points evenly distributed
Color Ramp (single authoritative definition):
  source: gpuTemp normalized [0.0 .. 1.0] where 0.0 = 30 C, 1.0 = 95 C
  stops:
    - 0.0:  #30A0FF (cool blue)
    - 0.3:  #70C0FF (light blue)
    - 0.5:  #FFB030 (amber)
    - 0.7:  #FF7030 (orange)
    - 1.0:  #FF2020 (hot red)
  interpolation: linear RGB between stops
  used_by: [ember.color, spark.color, heatHaze.colorTint, burstParticles.color]
Spawn System (single throttling mechanism):
  mechanism: spawn cap per frame
  cap: max new particles created in a single frame = floor(spawnBudget)
    where spawnBudget = 1.5 (base) + load * 0.5 (load bonus)
  rule: ember spawns claim from cap first. Spark spawns from promote
    events bypass cap BUT count against total particle limit.
  rationale: single point of spawn throttling — no second gate, no
    skipSpawnNextFrame toggle, no alternating-frame scheme.
  consistency: this is the ONLY spawn-limiting mechanism. All particle
    creation routes through a single SpawnManager.decide() method.
Particle Pool (single authoritative model):
  strategy: dynamic allocation with soft limit
  pool: particles held in a flat Float32Array (position x,y, velocity x,y,
    lifetime, maxLife, size, colorR, colorG, colorB, opacity, type)
  claim: createParticle() finds first dead slot (lifetime <= 0) and
    reinitializes it. If no dead slot and count < maxParticles, appends.
    If count >= maxParticles, drops the spawn silently.
  maxParticles: 150 (constant, never changed at runtime)
  no_preallocation: pool starts empty, fills on demand. No pre-allocated
    reserve. The phrase "pre-allocated" does not appear in this system.
  consistency: createParticle may push new slots when below limit.
    The claim-grab-recycle model is the only object lifecycle. No
    parallel allocation path exists.
Frame Loop (single render pathway):
  clock: requestAnimationFrame with delta normalization
  deltaTime: clamped [1 .. 33] ms (1..2 frames at 60fps)
    used for: lifetime decrement, velocity integration, opacity animation
    NOT used for: spawn rate (spawn rate uses real wall clock interval)
    consistency: deltaTime is applied identically to ALL particle types.
      No particle type uses raw frame count while another uses deltaTime.
  steps (executed in order, no overlap):
    1. deltaTime = min(Date.now() - lastFrame, 33)
       lastFrame = Date.now()
    2. iterate particles descending, for each:
       lifetime -= deltaTime
       if lifetime <= 0: mark slot dead, continue
       opacity = computeOpacity(lifetime, maxLife, type)
       if type == ember:
         x += velocityX * deltaTime/16.67
         y += velocityY * deltaTime/16.67
         velocityX += sin(time * emberWaveFreq) * 0.02 * deltaTime/16.67
       elif type == spark:
         x += velocityX * deltaTime/16.67
         y += velocityY * deltaTime/16.67
         velocityX *= 0.96
         velocityY *= 0.96
    3. computeSpawnBudget: spawnBudget = 1.5 + load * 0.5
    4. if promote event pending:
       burstParticles = promoteEventMagnitude * 8
       for i in burstParticles:
         createParticle(spark, origin=(promoteX, promoteY),
           angle=random(0..2PI), speed=random(2..6))
       promoteEvent = null
    5. emberSpawnThisFrame = floor(spawnBudget)
       for i in emberSpawnThisFrame:
         createParticle(ember,
           origin=(random(0..canvasWidth), canvasHeight+10),
           drift=random(-0.3..0.3), rise=random(0.2..0.8))
    6. if gpuTemp changed since last sample:
       regenerate heatHaze control points
    7. render: clear canvas, draw heatHaze blur pass, draw embers, draw sparks
       (z-order: heatHaze underneath, embers mid, sparks on top)
  consistency: spawnBudget, burst spawn, and ember spawn all route through
    createParticle() for the pool. No separate allocation path.
    deltaTime normalization factor (deltaTime/16.67) applied uniformly.
    No particle type positions using raw deltaTime while another uses
    a different normalization.
Performance:
  maxParticles: 150 (hard limit enforced in createParticle)
  rAF throttle: no extra throttle — rAF naturally pauses on inactive tab
  mobile/battery: settings toggle off by default on navigator.battery?
    (API deprecated) fallback: navigator.getBattery() promise, else
    'Reduce Motion' media query prefers-reduced-motion: reduce
  toggle: settings panel checkbox "Ambient Particles", default off
    on mobile detection (userAgent match or pointer: coarse)
  creation cost: Float32Array pool avoids GC pressure
  render cost: single canvas 2D context, composite operation
    'lighter' for additive glow effect
Consistency Verification (pre-finalization step):
  1. cross-reference every parameter: each appears in exactly one
     authoritative definition above. No parameter defined twice.
  2. verify spawn mechanism: only spawnBudget cap exists — no
     skipSpawnNextFrame, no alternating throttle, no dual gate.
  3. verify pool model: createParticle may push new slots, no
     pre-allocation claim exists, no conflicting pool semantics.
  4. verify deltaTime: applied uniformly to all particle types via
     normalization factor. No particle uses raw deltaTime, no particle
     uses frame count. Single formula: deltaTime/16.67 for all position
     and velocity integration.
  5. verify color ramp: single authoritative definition with stops.
     Each consumer references it by name. No inline color formulas.
  6. verify burst: promote event is single source for sparks.
     No alternate burst trigger path.
Edge Cases:
  load == 0: spawn budget = 1.5 floor = 1 ember per second, minimal
  load == 100: spawn budget = 1.5 + 1.0 * 0.5 = 2, capped at 2 per frame
  gpuTemp < 30: clamped to 30, color index 0.0 = cool blue
  gpuTemp > 95: clamped to 95, color index 1.0 = hot red
  promote magnitude 0: no burst (magnitude clamped min 1)
  promote while pool full: individual sparks silently dropped
  tab switch: rAF pauses, deltaTime clamp prevents time skip on resume
  canvas resize: re-center heatHaze control points, no particle invalidation
  multiple rapid promotes: bursts queued, processed one per frame
```