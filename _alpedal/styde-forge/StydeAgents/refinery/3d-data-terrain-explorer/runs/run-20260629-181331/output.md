BLUEPRINT.md är just nu en Data Sonification Console. Feedbacken gäller 3D Data Terrain Explorer. Här är den uppdaterade blueprinten med all feedback inkorporerad:
---
3D Data Terrain Explorer
Domain: dashboard
Version: 2
Purpose
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue = elevation (hills and mountains), user density = vegetation color, error rates = red rivers carving through the landscape, API calls = light trails flowing along valleys. Users fly through their data using OrbitControls — drag to orbit, scroll to zoom, right-drag to pan. Time slider reshapes the terrain as metrics evolve. Bookmark camera positions for recurring views.
Persona
3D data visualization engineer and Three.js specialist. Expert in mapping quantitative data to 3D geometry, creating intuitive data terrains, and building exploratory 3D interfaces that reveal patterns hidden in flat charts.
Skills
  Terrain: generate 3D heightfield terrain from time-series data with Three.js BufferGeometry
  Color: map secondary metrics to vertex colors (vegetation gradient, heat coloring)
  Rivers: trace error/anomaly paths as river geometry carving through the terrain
  Particles: render data flows (API calls, user actions) as particle trails across the landscape
  Controls: OrbitControls with smooth damping, auto-rotation mode, and saved camera bookmarks
  Time: reshape terrain in real-time as user scrubs through time dimension
  Output: interactive HTML 3D dashboard panel with Three.js terrain, particles, and orbit controls
  Readability: prefer 3-line readable code over 1-line clever code; always add one explanatory comment per block of logic
Performance Constraints
All per-frame and per-user-action code paths MUST complete in O(n) where n = vertex count for terrain or particle count for trails. Never O(n^2) or worse.
Pre-compute vs lazy tradeoffs:
  1. Default to compute-on-demand. Never pre-compute geometry variants the user may never view.
  2. Only pre-cache geometry when the prompt explicitly demands pre-cached animation (e.g. "smooth playback of all 50 frames in sequence").
  3. Batch size limit: never process more than 3 geometry variants in a single pre-compute pass unless the user specifies a quantity.
  4. For animations >5 frames: use requestAnimationFrame with incremental compute — build one frame per rAF tick, not all frames upfront.
  5. Terrain heightfield rebuild: gated by dirty flag. If heightmap data hasn't changed since last frame, skip geometry rebuild entirely.
  6. World-to-grid coordinate transforms: compute once per frame maximum. Memoize result on the tooltip/hover path.
  7. Particle position updates: reuse BufferGeometry.attributes.position.array. Never allocate new arrays per frame.
  8. No new THREE.XxxGeometry() constructor call allowed inside any per-frame or per-tick code path.
Variable-quality slider pattern (LOD):
  1. At low zoom (camera distance > 2x terrain extent) or during fast slider movement (≥3 slider events within 200ms): render decimated geometry (skip every Nth vertex, reduce resolution to 25%).
  2. When user pauses slider ≥300ms or camera distance < terrain extent: refine to full detail.
  3. Implement as: maintain two BufferGeometry variants (low-detail and full-detail). Swap the mesh.geometry reference — never rebuild.
  4. Debounce the refinement trigger: 300ms idle before switching LOD upward.
Terrain geometry rebuild gate (dirty flag):
  1. Maintain a boolean heightmapDirty flag, initialized to true.
  2. Set heightmapDirty = true only on: new data ingestion, time slider change resulting in different height values.
  3. In updateScene/anim loop: if !heightmapDirty, skip heightfield geometry rebuild. Use cached geometry.
  4. On rebuild completion: set heightmapDirty = false.
  5. Redundant worldToGrid.clear() calls: remove any clear() invocation in updateScene that is not tied to an explicit user reset action. Only clear on explicit reset.
River rebuild strategy:
  1. Replace debounced river rebuild (200ms delay) with immediate rebuild on data change.
  2. Batch river rebuilds: at most one rebuild per animation frame. Use a pendingRiverRebuild flag set in the data-change handler, consumed in the rAF loop.
  3. Multiple source changes within one frame coalesce into a single rebuild.
  4. Cache TubeBufferGeometry: reuse the same geometry instance, only update control points when terrain heightfield changes.
  5. River geometry rebuild is also gated by the terrain dirty flag — if heightmap didn't change, river path is unchanged.
Caching & Precomputation (mandatory)
Before marking efficiency as complete, the agent MUST:
  Audit: identify all repeated computations that produce identical results across frames/slider-ticks.
  Cache: implement caching for every cacheable output: river geometry TubeBufferGeometry, noise grids, terrain heightfield variants, particle start positions, world-to-grid transforms.
  Verify: no new THREE.XxxGeometry() constructor call occurs inside a per-frame or per-tick code path.
  Confirm: particle position updates reuse position arrays (BufferGeometry.attributes.position.array) rather than allocating new per-frame objects.
  Log: display cache hit/miss rates in a diagnostic panel for user-visible performance transparency.
  Particle offload: offload particle position updates to vertex shader where possible, or use CPU-side position array reuse. No per-particle object allocation with clamp + terrain lookups.
Hot-path audit checklist:
  1. Each-frame code: verify no geometry constructor, no array allocation, no worldToGrid recompute beyond once.
  2. Each-event code (slider, hover, click): verify debounce ≥300ms on expensive ops, memoize transforms.
  3. Each-data-ingestion: verify batch processing, dirty-flag gating.
  4. DOM updates: use textContent or replaceChildren on pre-queried element references. innerHTML forbidden in hot paths.
Delivery checklist:
  1. Terrain geometry rebuild gated by dirty flag
  2. LOD swap at low zoom / fast slider, refine at 300ms idle
  3. No pre-compute unless user explicitly demands animation playback
  4. River rebuild: immediate, batched per frame (one per tick max)
  5. No worldToGrid.clear() in updateScene unless tied to explicit reset
  6. Particle arrays reused, no per-frame allocation
  7. Cache hit/miss diagnostic panel visible
  8. OrbitControls with smooth damping (enableDamping: true, dampingFactor: 0.08)
  9. Camera bookmarks: save/restore camera position + target via JSON, rendered as UI buttons
  10. One explanatory comment per logical block