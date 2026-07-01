Ambient Particle System
Domain: frontend Version: 2
Purpose
Canvas-based particle system rendered behind dashboard panels, absolute positioned. Embers, sparks, and heat haze react to forge activity. More activity = more particles. Agent promotions trigger particle burst. GPU temp drives particle color ramp: cool blue through amber to hot red. Performance capped at 100-200 particles, requestAnimationFrame throttled. Toggle via settings panel, off by default on mobile/battery.
Persona
Creative frontend engineer. Particles as ambient data visualization.
activityLevel
  Definition:
    Normalized forge load metric. Range: 0 (idle) to 100 (peak burn).
  Data Pipeline:
    Source: WebSocket message forge.occupancy — integer 0..100, received every 2 seconds.
    Aggregation window: sliding window of the last 5 readings (10 seconds).
    Smoothing: exponential moving average, alpha=0.3. Updated on each new reading.
    Output: smoothed occupancy value rounded to integer, written to shared state every 2 seconds.
    Initial value: 0.
spawnRate
  Formula:
    floor(activityLevel / 5) + 1
  Clamp:
    maxParticles = 200. If currentParticleCount + spawnCount > maxParticles, spawn none.
  Minimum: 1 particle per frame even at idle (single ambient ember).
  Maximum: 21 particles per frame at activityLevel=100.
particleTypes
  ember:
    Lifetime: 3000-6000ms
    Rise speed: 0.2 + activityLevel/500 px/frame
    Width: 2-4px
    Opacity: 0.3-0.7, fades out in last 1000ms
    Color: hsl(40deg 80% 60%) at emission, shifts toward hsl(20deg 90% 70%) as lifetime progresses
  spark:
    Lifetime: 800-1500ms
    Burst trajectory: random angle, speed 2-5 px/frame, deceleration 0.97 per frame
    Width: 1-2px, shrinks 0.02 per frame after peak
    Opacity: 0.6-1.0 at birth, linear fade to 0
    Color: hsl(50deg 100% 80%) at birth, shifts to hsl(0deg 100% 60%) over lifetime
    Trigger: promotion events only. Burst of 12-20 sparks at random angles from promotion origin.
heatHaze
  Amplitude: 1.5 + activityLevel * 0.02 px
  Frequency: 0.02 (simplex noise)
  Update: every frame via simplex noise sample at continuous time, applied as y-offset to all particle positions (distortion layer)
  Applied: after main particle position update, before render
promotionFlag
  Source: WebSocket message agent.promoted — dispatched by data pipeline on receipt.
  Lifecycle: consumed per-frame in the render loop. Set true on WebSocket receipt. After trigger, rendered as one burst of 12-20 sparks on the next frame. Flag is then cleared immediately after the burst render. Never polled on a 5s interval — the physics layer consumes it frame-synchronously.
  Rationale: Promotion is a visual event; frame-level response prevents perceptible delay. The data pipeline (5s cadence) handles occupancy only.
  Cache invalidation: clearing the flag IS the invalidation. No stale bursts.
renderLoopPseudocode
  function frame(timestamp):
    deltaTime = timestamp - lastTimestamp
    lastTimestamp = timestamp
    // Input sampling
    currentActivity = readSharedState(forge.occupancy.smoothed)
    newPromotion = readSharedState(agent.promoted)
    // State update
    updateActivitySmooth(currentActivity, deltaTime)
    if newPromotion:
      spawnSparkBurst(12 + (currentActivity / 10), centerX, centerY)
      clearSharedState(agent.promoted)
    // Spawn embers from spawnRate
    spawnCount = floor(currentActivity / 5) + 1
    clampParticles(200)
    if particleCount + spawnCount <= 200:
      for i in 0..spawnCount:
        spawnEmber(random(width), height + 10)
    // Physics tick — ALL particles
    for p in particles:
      if p.type == ember:
        p.y -= (0.2 + currentActivity / 500) * deltaTime.speed
        p.x += sin(noise(p.x, p.y, time * 0.02)) * heatHazeAmplitude
        p.age += deltaTime
        if p.age > p.lifetime: kill(p)
      if p.type == spark:
        p.x += p.vx
        p.y += p.vy
        p.vx *= 0.97
        p.vy *= 0.97
        p.age += deltaTime
        p.width -= 0.02
        if p.age > p.lifetime or p.width <= 0: kill(p)
      p.color = colorRamp(p.temp or gpuTemp)
    // Heat haze distortion (post-physics)
    for p in particles:
      p.y += simplexNoise(p.x * 0.01, p.y * 0.01, time * 0.02) * heatHazeAmplitude
    // Output dispatch
    clearCanvas()
    for p in particles:
      drawCircle(p.x, p.y, p.width, p.color, p.opacity)
    // Backpressure check
    if fps < 20:
      reduceMaxParticles(20)
    if fps < 30 and particleCount > 150:
      killOldest(particleCount - 150)
    requestAnimationDraw(frame)
colorRamp
  Input: gpuTemp in degrees Celsius (range 30-90).
  Mapping:
    30-45C: hsl(220deg 80% 60%) to hsl(40deg 80% 60%) — cool blue to warm amber
    45-70C: hsl(40deg 80% 60%) to hsl(20deg 90% 65%) — amber to orange
    70-90C: hsl(20deg 90% 65%) to hsl(0deg 100% 55%) — orange to hot red
  Implementation: linear interpolation of hue between breakpoints.
performance
  maxParticles: 200 hard cap, dynamic throttle down to 80 if fps below 30 for 3 consecutive frames
  requestAnimationFrame: single loop, no setInterval
  OffscreenCanvas: used in Web Worker if available, fallback to main thread Canvas2D
  Battery-aware: if navigator.getBattery().level < 0.2, set renderScale = 0 and particleCount = 0 (system off)
  Mobile: default off in settings, user must toggle on
settingsPanel
  Path: /settings/appearance
  Toggle label: Ambient Particles
  Default: off on mobile and battery < 20%, on otherwise
  Controls:
    Particle density: slider 0-100 (maps to scalar on spawnRate)
    Heat haze intensity: slider 0-200% (maps to heatHazeAmplitude multiplier)
css
  Canvas element: position absolute, inset 0, pointer-events none, z-index 0
  Parent container: position relative, overflow hidden