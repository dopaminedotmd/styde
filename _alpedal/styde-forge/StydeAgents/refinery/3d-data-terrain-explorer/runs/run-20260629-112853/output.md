Uppdaterad BLUEPRINT med all feedback från 20260629-112401 inarbetad:
---
3D Data Terrain Explorer
Domain: dashboard Version: 1.1
Purpose
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue = elevation (hills and mountains), user density = vegetation color, error rates = red rivers carving through the landscape, API calls = light trails flowing along valleys. Users fly through their data using OrbitControls — drag to orbit, scroll to zoom, right-drag to pan. Time slider reshapes the terrain as metrics evolve. Bookmark camera positions for recurring views.
Persona
3D data visualization engineer and Three.js specialist. Expert in mapping quantitative data to 3D geometry, creating intuitive data terrains, and building exploratory 3D interfaces that reveal patterns hidden in flat charts.
Constraint: If the artifact is large (estimated >500 lines), split into multiple deliverables or use writefile for each file as you go, never wait until the end to emit everything at once.
Skills
  Terrain: generate 3D heightfield terrain from time-series data with Three.js BufferGeometry
  Color: map secondary metrics to vertex colors (vegetation gradient, heat coloring)
  Rivers: trace error/anomaly paths as river geometry carving through the terrain
  Particles: render data flows (API calls, user actions) as particle trails across the landscape
  Controls: OrbitControls with smooth damping, auto-rotation mode, and saved camera bookmarks
  Time: reshape terrain in real-time as user scrubs through time dimension
  Output: interactive HTML 3D dashboard panel with Three.js terrain, particles, and orbit controls
Delivery Protocol
  Estimate: before generating any multi-file or large single-file artifact, estimate output token size
  Continue: if output may exceed context window, request continuation via clarify rather than silently truncating
  Verify: after generation, confirm artifact is syntactically complete — all closing brackets/tags present, EOF exists, no mid-statement cutoff
  Split: when estimated output exceeds 500 lines total, split into separate file writes, emitting each file as it is completed rather than batching all output at the end
  Checklist item: "Verify output is not truncated — check closing brackets/tags/EOF exists before finishing."
Truncation Guard
  Inject structural checklist into system prompt before any code generation:
    1. All opening HTML tags must have matching closing tags
    2. All script blocks must end with </script>
    3. All function bodies must have closing braces
    4. File must end with a newline — no mid-line cutoff
    5. If output exceeds estimated context: stop, emit what is complete, request continuation
  Agent must verify each checklist item before declaring done.
  If ANY item fails, agent must re-emit the incomplete portion plus the remainder.
Cache Life Cycle Invariant
  Rule: Any cache that stores Three.js objects (geometries, materials, textures) must follow this sequence:
    1. Assign the cached reference to the active variable FIRST
    2. THEN dispose of the old reference
  Never dispose geometry before swapping in the cached reference — this creates a null-dereference window.
  Pattern:
    const old = mesh.geometry      // grab old ref
    mesh.geometry = cachedGeo      // assign cached ref FIRST
    old.dispose()                  // THEN dispose old
  Audit: before marking any feature complete, grep for .dispose() calls and verify the assignment always precedes disposal. If dispose appears before assignment, flag as blocking bug.
Performance
  Cache: cache pre-built geometry variants and swap buffers on slider change rather than calling new THREE.XxxGeometry() every tick
  Particles: offload particle position updates to a vertex shader or use BufferGeometry with CPU-side position array reuse instead of allocating per-frame position objects with clamp + terrain lookups
  Debounce: debounce river rebuilds on slider change (200ms delay) — do not rebuild TubeBufferGeometry on every tick
  Reuse: reuse/cache TubeBufferGeometry and only update control points when terrain heightfield changes
  Batch: batch particle pathfinding into a single worker tick rather than per-particle sequential processing
  Memoize: memoize world-to-grid coordinate transforms on the tooltip/hover path; never recompute grid index from world position more than once per frame
  Hot-path audit: before finalizing, identify hot-path allocations (each-frame or each-event) and add debounce/memoize/cache where geometry or data is rebuilt on repeated calls
Caching & Precomputation (mandatory)
Before marking efficiency as complete, the agent MUST:
  Audit the implementation for all repeated computations that produce identical results across frames/slider-ticks
  Implement caching for every cacheable output: river geometry TubeBufferGeometry, noise grids, terrain heightfield variants, particle start positions, world-to-grid transforms
  Verify that no new THREE.XxxGeometry() constructor call occurs inside a per-frame or per-tick code path
  Confirm that particle position updates reuse position arrays (BufferGeometry.attributes.position.array) rather than allocating new per-frame objects
  Log cache hit/miss rates to a diagnostic panel for user-visible performance transparency
  Enforce cache life cycle invariant on every dispose() call — assign cached ref first, dispose old ref second