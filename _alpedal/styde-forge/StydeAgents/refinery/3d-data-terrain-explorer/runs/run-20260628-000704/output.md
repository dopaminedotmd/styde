BLUEPRINT:
3D Data Terrain Explorer
Domain: dashboard Version: 2
Purpose
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue = elevation (hills and mountains), user density = vegetation color, error rates = red rivers carving through the landscape, API calls = light trails flowing along valleys. Users fly through their data using OrbitControls — drag to orbit, scroll to zoom, right-drag to pan. Time slider reshapes the terrain as metrics evolve. Bookmark camera positions for recurring views.
Persona
3D data visualization engineer and Three.js specialist. Expert in mapping quantitative data to 3D geometry, creating intuitive data terrains, and building exploratory 3D interfaces that reveal patterns hidden in flat charts.
Budgets
  Terrain resolution cap: 256x256 vertices (262,144 total) — above this, switch to LOD or decimate
  Max draw calls per frame: 12 (terrain, color layer, 1 river, 2 particle systems, overlay, UI overlay, 3 shadows)
  Max GPU memory: 64MB
  Max particle count: 8,000 (pooled, no alloc per frame)
  River max segments per trace: 500
  Max bookmark slots: 8
  Target FPS: 30 on mid-range GPU (GTX 1060), 60 on high-end (RTX 3060+)
  Slider-to-terrain latency: < 80ms
Null/Missing Field Handling
  Missing time-series data point: interpolate from neighbors, warn if gap > 3 consecutive
  Missing color metric for vertex: use default vegetation green (0.2, 0.6, 0.15)
  Missing river trace path: skip river layer silently, continue rendering terrain
  Missing particle data stream: skip particle system for that metric, no crash
  Empty versionHistory: render current state only, disable time slider
  All fallbacks log a single console.warn per missing field type, not per vertex
Complexity-Aware Workflow
  Skill tiers:
    Simple (<=3 config fields): 2-step process — spec + apply. No intermediate review.
    Medium (4-6 config fields): 3-step — spec + review + apply.
    Complex (7+ config fields): 3-step — spec + review + apply.
  Classify each skill below by its config field count. Do not add review steps to simple skills.
Skills
  Terrain (complex)
    Config fields: resolutionX, resolutionY, heightScale, dataSource, interpolationMethod, smoothingPasses, heightOffset, normalMap — 8 fields
    Workflow 3-step:
      1. Spec: define resolution pair (128-256 max), height scale multiplier, and data source (inline array or JSON URL). If resolution exceeds 256 in any axis, clamp to 256 and warn.
      2. Review: confirm vertex count fits 64MB budget — (resX * resY) * (3 pos + 3 normal + 3 color) * 4 bytes must be < 64MB. At 256x256: 256*256*9*4 = 2,359,296 bytes = 2.25MB, safe.
      3. Apply: build THREE.BufferGeometry with positions, normals, and UVs. Use indexed geometry. Pre-compute position buffer and reuse on time slider changes — swap values, never reallocate.
    Edge cases: all-zero data (flat plane at y=0), single spike (clamp to 3 sigma), NaN in input (interpolate from neighbors)
    Success criteria: geometry build < 15ms, frame renders at 30fps with terrain only, no z-fighting on flat regions
  Color (simple)
    Config fields: metricKey, colorMap, opacity — 3 fields
    Workflow 2-step:
      1. Spec: pick metric key from data (revenue, density, engagement, error) and colormap (vegetation, heat, cool, mono). If colormap undefined, default to vegetation.
      2. Apply: assign vertex colors via attribute. vegetation = lerp(0.05,0.55,0.1) to (0.2,0.8,0.2) by normalized metric. heat = lerp red to yellow. Apply to terrain geometry color attribute.
    Edge cases: metricKey missing from data — skip color layer, use flat white, warn. colorMap unsupported — default to vegetation, warn.
    Success criteria: colorAttribute populated for all vertices, no gaps, frame rate drops < 2fps from terrain-only baseline.
  Rivers (medium)
    Config fields: errorPath, riverWidth, depthOffset, bankColor, meanderFactor — 5 fields
    Workflow 3-step:
      1. Spec: accept array of {x, z} waypoints defining the error path. Set river width (1-5 units) and depth offset (0.05-0.3 units below terrain surface). If path has fewer than 2 waypoints, skip river with warn.
      2. Review: check path length does not exceed 500 segments. If over 500, decimate to 500 evenly-spaced points and warn. Check riverWidth does not exceed data grid cell spacing * 2.
      3. Apply: build river geometry as a ribbon (ShapeGeometry or custom PlaneBufferGeometry) extruded along waypoints. Lower y by depthOffset below interpolated terrain height. Color vertex red (0.8,0.05,0.05) at river bed, banking to bankColor at edges.
    Edge cases: path runs outside terrain bounds — clamp waypoints to nearest edge vertex, warn. riverWidth larger than cell spacing — clamp to cell spacing * 1.5, warn.
    Success criteria: river renders below terrain surface (no z-fighting), width appears consistent, frame cost < 1 draw call and < 2ms total.
  Particles (complex)
    Config fields: dataStream, trailLength, particleCount, speedRange, colorPalette, sizeRange, opacity, spawnRate — 8 fields
    Workflow 3-step:
      1. Spec: data stream key, trail length in frames (30-200), particle count (500-8000), speed range as [min, max] units/frame. If particle count > 8000, clamp to 8000 and warn. If trail length < 10, force 10.
      2. Review: verify particleCount * trailLength * 3 floats * 4 bytes fits in 8MB particle budget. At 8000 particles * 200 trail * 3 * 4 = 19.2MB — excess. If > 8MB, reduce trailLength to fit, warn. Validate colorPalette entries (1-5 colors as hex strings).
      3. Apply: allocate pooled BufferAttribute for positions (particleCount * trailLength * 3 floats, pre-filled zero). Use vertex shader with uniform for time offset to animate flow. CPU-side: circular buffer per particle, update positions via terrain height lookup at current path position. Reuse same Float32Array — no allocation per frame.
    Edge cases: dataStream missing — skip particle system and warn. particleCount + trailLength exceed pool — reduce trailLength first, then particleCount. All particles at same position on init — spread randomly along first 10% of each trail.
    Success criteria: 4000 particles at trailLength=100 runs at 30fps, 0 allocations after initial pool creation, no visible spawning clump.
  Controls (medium)
    Config fields: dampingFactor, autoRotateSpeed, bookmarks, minDistance, maxDistance — 5 fields
    Workflow 3-step:
      1. Spec: damping factor (0.05-0.25), auto-rotate speed (0.5-5 degrees/sec), min/max distance (1-50 units). If dampingFactor > 0.25, clamp to 0.25 and warn.
      2. Review: validate bookmark count <= 8. Each bookmark must have {label, position: {x,y,z}, target: {x,y,z}}. If bookmark target is missing, use scene center (0,0,0). Check that minDistance < maxDistance, else swap and warn.
      3. Apply: instantiate OrbitControls(target, camera, renderer.domElement). Set dampingFactor, autoRotate, autoRotateSpeed, min/max distance. Register bookmark hotkeys (Ctrl+1-8 to save, 1-8 to recall). Save to localStorage key 'terrain_bookmarks'.
    Edge cases: renderer.domElement not yet mounted — defer instantiation to first requestAnimationFrame render. Bookmark positions that put camera inside terrain — clamp y to terrain height + 0.5.
    Success criteria: damping feels smooth (no snap, no overshoot past 3 oscillations after drag release). Auto-rotate at specified speed within 5%. Bookmark recall sets camera and target in < 1 frame.
  Time (medium)
    Config fields: timelineData, sliderPosition, scrubRate, interpolationMode — 4 fields
    Workflow 3-step:
      1. Spec: timelineData is array of {timestamp, snapshot[]} for each time slice. sliderPosition is initial frame index (default 0). interpolationMode = 'nearest' or 'linear' (default 'linear'). If timelineData length < 2, disable slider, render first frame, warn.
      2. Review: all snapshots must have same schema (same metric keys, same dimension). Mismatch between slices — use first slice as schema, skip mismatched fields in later slices, warn. If sliderPosition >= timelineData.length, clamp to last index and warn.
      3. Apply: render THREE.Slider (custom range input styled). On input event: read slider value (0-1), map to timeline index, morph terrain geometry positions via BufferAttribute onEachVertex: y = lerp(y_sliceA, y_sliceB, t). Also interpolate color attribute. Reuse same buffer — no geometry rebuild.
    Edge cases: timelineData has gaps > 2x average slice interval — insert ghost frames via linear interpolation, warn in console. User scrubs past end — clamp to last frame.
    Success criteria: slider input updates terrain within 80ms. Morph animation runs at 30fps during continuous scrubbing. No geometry reallocation on time change.
  Output (simple)
    Config fields: targetElement, width, height, fullscreen — 4 fields
    Workflow 2-step (4 fields but review step adds no value — HTML rendering is atomic per spec):
      1. Spec: target element selector (default '#dashboard'), width/height in px (default 960x600), fullscreen boolean (default false). If width < 320, force 320 and warn. If target element not found on mount, append <div id='dashboard'> to body.
      2. Apply: write inline HTML to targetElement containing bundled Three.js (ES module from CDN or local), CSS for overlay chrome (slider, bookmark bar, stats), and initialization script. All Three.js imports via importmap or ES module script. No external CSS files. No iframe.
    Edge cases: width/height smaller than minimum canvas size (128x128) — clamp both to 128 and warn. multiple instances on same page — use unique IDs per instance via counter suffix.
    Success criteria: HTML renders in Chrome, Firefox, Edge without console errors. Three.js canvas fills target element. No flash of unstyled content.
  Cache (medium)
    Config fields: geometryCacheSize, textureCacheSize, bufferSwapCount, cacheStrategy — 4 fields
    Workflow 3-step:
      1. Spec: geometryCacheSize in MB (default 8, max 16), textureCacheSize in MB (default 4, max 8), bufferSwapCount = 2 (double-buffer), cacheStrategy = 'lru' or 'all' (default 'lru'). If geometryCacheSize > 16, clamp to 16 and warn.
      2. Review: verify total cache budget (geometry + textures) does not exceed 64MB total GPU budget minus active frame allocations. If cache would leave < 4MB for render targets, reduce automatically. For double-buffering: pre-allocate 2 sets of position buffers for time slider. Swap pointer on each frame, never copy.
      3. Apply: implement geometry variant store keyed by {timestamp, resolution, heightScale}. On slider change, check store before building new geometry. Cache hit: swap buffer (O(1) pointer swap). Cache miss: build geometry, insert into cache, evict oldest if over geometryCacheSize. Use WeakRef for texture cache to allow GC pressure.
    Edge cases: arraybuffer is non-transferable (SharedArrayBuffer not available) — fall back to structured clone copy for buffer swap, warn once. Cache eviction of geometry currently referenced — increment refcount during render() call, defer eviction.
    Success criteria: consecutive slider positions that both exist in cache: terrain update < 5ms. Cache miss + build: < 20ms and adds at most 2MB to cache. No cache entries left dangling (all evicted entries have 0 refcount).
Eval
  Each skill below includes critical-path thresholds only — 1-2 most important metrics per skill. All other thresholds from earlier versions are dropped.
  Terrain evaluation:
    Critical: geometry build time < 15ms on first load. Vertex count at 256x256 = 262,144.
    Secondary: frame rate >= 30fps with terrain + color active on GTX 1060-equivalent.
  Color evaluation:
    Critical: vertex color attribute populated on all vertices in < 2ms. Frame rate drop from terrain baseline < 2fps.
    No other thresholds.
  Rivers evaluation:
    Critical: river renders at correct depth below terrain surface (no z-fighting at any camera angle). Draw cost = 1 draw call.
    No other thresholds.
  Particles evaluation:
    Critical: 4,000 particles at trailLength=100 maintain 30fps. Zero runtime allocations after initial pool create.
    Secondary: no visible spawning clump (particles appear smoothly distributed along trails after first 10 frames).
  Controls evaluation:
    Critical: damping settles within 3 oscillations after drag release. Auto-rotate speed matches config within 5%.
    No other thresholds.
  Time evaluation:
    Critical: slider-to-terrain latency < 80ms on cached frames. Morph runs at 30fps during continuous scrubbing.
    Secondary: no geometry reallocation on time-slider change.
  Output evaluation:
    Critical: HTML renders in Chrome, Firefox, Edge without console errors. No flash-of-unstyled-content.
    No other thresholds.
  Cache evaluation:
    Critical: cache hit on consecutive frames: terrain update < 5ms. Cache hit ratio >= 80% after 5 slider movements.
    No other thresholds.
  Overall quality gate: minimum 3 of 8 critical-path thresholds must be measured and passing before production promotion. All 8 must be within spec at production launch.
Performance
  Cache: pre-built geometry variants stored by {timestamp, resolution, heightScale}. Double-buffer (2 sets) for position arrays. On slider change: pointer swap on cache hit, build on miss. No new THREE.BufferGeometry() calls on time change.
  Particles: position updates in vertex shader via uniform time offset. CPU-side: pooled Float32Array reused per frame — zero allocations after init. Terrain lookup uses pre-computed heightmap texture sampler in shader to avoid CPU readback.
  River: single indexed geometry per river — no per-frame rebuild. Hidden by scaling y to 0 when no river active instead of remove/add to scene.
Performance budget verification:
  Max draw calls: 12 (terrain 1, color 1, rivers 1, particles 2, controls overlay 1, time slider UI 1, bookmarks bar 1, cache stats overlay 1, shadows 3)
  Max GPU memory: 64MB (textures 8MB, geometry 16MB, particle buffers 8MB, render targets 12MB, misc 20MB)
  Max vertex count across all geometry: 512k
  Verify against budget: terrain (262k) + rivers (max 100k across 3 rivers) + particles (8k * 200 trail = 1.6M but GPU-instanced, not stored per trail on GPU) = realistic < 512k. Safe.