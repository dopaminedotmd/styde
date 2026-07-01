name: Ambient Particle System
version: 1
domain: frontend
purpose: Canvas-based particle system in dashboard background. Embers, sparks, and heat haze reactive to forge activity. More activity = more particles. Agent promotions trigger particle burst. GPU temp drives particle color ramp cool blue to amber to hot red.
persona: Creative frontend engineer. Particles as ambient data visualization.
skills:
  - Canvas  behind dashboard panels, absolute positioned
  - Particle physics: ember rise, spark burst, heat haze distortion
  - Data reactivity: spawns = spark rate, GPU temp = color ramp, promote = burst
  - Performance: limit 100-200 particles, requestAnimationFrame throttle
  - Toggle via settings panel, off by default on mobile or battery
implementation:
  core loop:
    init: createCanvas(dashboardContainer)
      edge: container null -> return noop renderer
      edge: WebGL context missing -> fallback to 2d context, log warning
    loop: requestAnimationFrame(tick)
      tick:
        1. updateParticles(deltaTime)
        2. applySpawns(activityLevel, promoteFlag)
        3. applyPhysics(deltaTime)
        4. render(ctx)
        5. schedule next frame
  particle state:
    pool: Float32Array(particles * 5) for x, y, vx, vy, life
      rationale: avoid GC pressure, 200 particles x 5 floats = 4KB
    spawns: new particles at rate proportional to activityLevel (0..1)
      spawnRate = clamp(Math.round(activityLevel * 3), 0, 6) per tick
    promotion burst: activityLevel spike >= 0.85 -> burst 20 particles
      burstOrigin: random (x, y) within canvas bounds
    color ramp:
      temp (0..100):
        0-33: cool blue hsl(210, 80%, 60%)
        34-66: amber hsl(30, 90%, 55%)
        67-100: hot red hsl(0, 85%, 55%)
      interpolation: lerp between anchors per temp value
  physics:
    ember rise: vy -= gravity * dt, slight horizontal drift sin(phase)
    spark burst: radial velocity from origin, rapid fade (life 0.3s)
    heat haze: sin wave offset on particle draw, distort radius ~2px
    bounds: particle out of canvas or life <= 0 -> recycle to pool tail
  performance:
    maxParticles: 100 idle, 200 during burst
    pooling: Float32Array preallocated, index pointer for active count
    throttle: skip render if tab hidden (document.hidden check)
    deprecation: will-change hint on canvas parent for GPU composition
  toggle:
    default: on for desktop, off for mobile and battery saver
    detection: navigator.getBattery? battery.charging === false
    setting: settings panel -> ambient particles toggle
    localStorage: persist pref
  edge cases:
    canvas null: return noop renderer, set active false
    WebGL missing: fallback 2d context, silent degrade
    temp out of range (NaN, <0, >100): clamp to 0-100, default color blue
    activityLevel NaN: treat as 0, no spawns
    window resize: debounce 200ms, resize canvas, reset burst positions
    visibility change: pause loop on hidden, resume on visible
    rapid toggle (on/off within 100ms): debounce, flush pool on each off
  concision gate:
    after drafting, prune any sentence restating platform default
    collapse 3+ bullet edge lists to 1 line when stdlib handles gracefully
    target: output under 2KB raw spec text