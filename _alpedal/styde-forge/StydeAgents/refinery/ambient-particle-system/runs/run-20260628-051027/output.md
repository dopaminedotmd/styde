BLUEPRINT.md
Domain: frontend  Version: 1
Purpose
Canvas-based particle system layered behind dashboard panels. Embers drift upward, sparks burst on promotion events, heat haze distorts background content. Particle activity mirrors forge pipeline state: spawn rate driven by pipeline activity, color mapped to GPU temperature, burst triggered on agent promotions. Togglable via settings panel, off by default on mobile and battery-constrained devices. Max 200 particles, single requestAnimationFrame loop, no allocations per frame.
Persona
Creative frontend engineer. Particles as ambient data visualization.
Data Pipeline (activityLevel sourcing)
Source: forge-pipeline heartbeat event piped through a shared EventBus. Each completed iteration emits { timestamp, status }. Status values: idle, running, promoting. Aggregation window: 1000ms sliding window. Smoothing: exponential moving average with alpha = 0.15, initialized to 0. Decay: when no events arrive for 5000ms, target value decays toward 0 at rate 0.05 per frame. Update cadence: per rAF tick, sample EventBus accumulator, apply EMA, store in global activityLevel (float 0.0–1.0). Single source of truth — activityLevel is read-only and referenced by name everywhere; never redefined in a second location.
Render-loop structure (one complete frame)
  function tick(timestamp) {
    deltaTime = (timestamp - lastTimestamp) / 1000;
    deltaTime = min(deltaTime, 0.05);   // clamp to 50ms to avoid spiral of death
    lastTimestamp = timestamp;
    // 1. Input sampling — gather system state
    activity = sampleActivityEventBus();
    currentTemp = sampleGpuTemperature();
    promotions = consumePromotionQueue();
    // 2. State update — physics + reactivity
    activityLevel = ema(activityLevel, activity, 0.15);
    targetSpawnRate = lerp(5, 40, activityLevel);
    activeColorRamp = temperatureToColorRamp(currentTemp);   // single definition per temp → color
    pendingBursts = pendingBursts + promotions;
    // 3. Particle lifecycle — spawn, update, cull
    spawnCount = floor(targetSpawnRate * deltaTime);
    spawnCount = min(spawnCount, 200 - particles.length);
    for i in 0..spawnCount:
      p = createParticle(colorRampMid(activeColorRamp));
      applyBurstVelocity(p, popBurst(pendingBursts));
      particles.push(p);
    for p in particles:
      frameHeatHaze(p, deltaTime);   // single heat-haze function, referenced by name
      frameEmberRise(p, deltaTime);
      p.lifetime -= deltaTime;
      if p.lifetime <= 0: markDead(p);
    particles = filterAlive(particles);   // single cull path
    // 4. Output dispatch — draw on canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for p in particles:
      drawParticle(ctx, p);
    // 5. Backpressure check
    if particles.length > 180:
      skipSpawnNextFrame = true;
    if skipSpawnNextFrame:
      skipSpawnNextFrame = false;
    else
      scheduleNextFrame(tick);
  }
Particle physics
ember rise: y -= baseSpeed * (1 + personalVariance) * deltaTime * 60. x += sin(age * 2) * 0.3 * deltaTime * 60. alpha fades from 0.7 to 0 over lifetime.
spark burst: on promotion, emit 8–15 particles from a random x position at y = canvasHeight. Initial velocity randomized: vx in [-3, 3], vy in [-6, -2]. Spark particles have shorter lifetime (1.5s) and white-to-orange color.
heat haze distortion: each particle applies a subtle radial displacement to background content drawn behind it. displacementRadius = particle.size * 2, displacementStrength = sin(age * 4) * 1.5 (pixels). Drawn as a globalCompositeOperation = 'lighter' overlay with low alpha. Single heat-haze function used everywhere — not duplicated or reimplemented in another section.
Data reactivity (parameter definitions — each defined exactly once, referenced by name)
spawns (spark rate): spawnsPerFrame = lerp(5, 40, activityLevel). activityLevel is the EMA-smoothed pipeline activity float defined under Data Pipeline above. Single definition at render-loop step 3.
GPU temp (color ramp): color mapped via temperatureToColorRamp(temp). temp below 50°C → cool blue ramp (#4488ff→#88bbff). 50–70°C → amber ramp (#ffaa44→#ffcc66). Above 70°C → hot red ramp (#ff3300→#ff6644). Interpolated linearly between ranges. Single definition referenced by name in step 2 and 3 — never redefined.
promote (burst): burst count per event = 10 (base) + floor(activityLevel * 5). Consumed from pendingBursts FIFO queue in step 3. burstVelocity applied on spawn. Single definition.
Performance
particle limit: hard cap at 200. New spawns skipped when count >= 180 (backpressure in step 5). Dead particles culled at end of each frame.
allocation: particle objects pre-allocated in an object pool of 200 slots. tick() reuses dead slots via marking, never calls new. No garbage per frame.
rAF throttle: single requestAnimationFrame loop. No setInterval or setTimeout fallback. Canvas redraw skipped when page is backgrounded (document.hidden check).
draw call: all particles batched into single fillRect call per draw pass — no per-particle stroke or radial gradient in hot loop. Heat haze drawn as single low-alpha overlay.
Toggle
Default: off. Detected via (navigator.battery?.level !== undefined || 'ontouchstart' in window) -> initially off. Settings panel checkbox: "Ambient particles" -> writes to localStorage key styde_particles_enabled. Tick() early-returns if disabled. Particle pool preserved across toggles (no dispose/recreate).
Consistency verification (required step before finalizing)
1. Scan every parameter, formula, and transform that appears in more than one section. Confirm each has a single definition and is referenced by name in all other locations. Reject any duplicate definition.
2. Cross-reference color ramp definitions: verify temperatureToColorRamp is the sole mapping from temperature to color. No other section should define an independent temperature→color formula.
3. Cross-reference deltaTime usage: verify clamp to 50ms is applied exactly once (step 1) and that every per-frame calculation uses deltaTime, not a fixed timestep. No other section should redefine or override deltaTime normalization.
4. Cross-reference heat-haze function: verify frameHeatHaze is the only displacement function. No second heat-haze or alternative distortion in another section.
5. Verify all spawn/decay rates reference activityLevel (the single EMA-smoothed value from Data Pipeline), not an independent activity metric.