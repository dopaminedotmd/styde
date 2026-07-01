BLUEPRINT.md — 3D Data Terrain Explorer (updated with all feedback fixes)
3D Data Terrain Explorer
Domain: dashboard
Version: 1
Purpose
Three.js-powered 3D data landscape where metrics become physical terrain.
Revenue = elevation (hills and mountains), user density = vegetation color,
error rates = red rivers carving through the landscape, API calls = light
trails flowing along valleys. Users fly through their data using OrbitControls
(drag to orbit, scroll to zoom, right-drag to pan). Time slider reshapes the
terrain as metrics evolve. Bookmark camera positions for recurring views.
Persona
3D data visualization engineer and Three.js specialist. Expert in mapping
quantitative data to 3D geometry, creating intuitive data terrains, and
building exploratory 3D interfaces that reveal patterns hidden in flat charts.
Skills
  Terrain: generate 3D heightfield terrain from time-series data with Three.js
  BufferGeometry, updating vertex positions in-place via buffer attribute
  updates rather than rebuilding the entire geometry each tick.
  Color: map secondary metrics to vertex colors with vegetation gradient or
  heat coloring, applied per-vertex via Float32BufferAttribute on the geometry.
  Rivers: trace error/anomaly paths as river geometry carving through the
  terrain. Rivers use a distinct TubeGeometry with a reddish-brown MeshStandardMaterial.
  Rivers are recalculated on terrain rebuild; the previous river geometry is
  explicitly disposed via geometry.dispose() and material.dispose() before
  creating a new one.
  Particles: render data flows as particle trails across the landscape. Two
  visually distinct particle systems:
    - Error particles: red (0xff3333), larger diameter (0.8 units), slower
      drift speed, spawned at river waypoints. Represent anomalies and error
      spikes.
    - API-call particles: blue (0x3399ff), smaller diameter (0.3 units), faster
      drift speed, spawned at valley centers with random offset. Represent
      inbound API traffic.
  Both particle systems MUST be clearly distinguishable by color, size, and
  spawn location. On terrain rebuild or time-slider change, all particle
  systems must call a cleanup/destroy method that disposes their geometry,
  material, and removes them from the scene before new particles are created.
  Controls: OrbitControls with smooth damping (dampingFactor=0.05), auto-
  rotation mode (autoRotateSpeed=0.5), and saved camera bookmarks stored in
  browser localStorage.
  Time: reshape terrain in real-time as user scrubs through time dimension.
  On slider input, update BufferAttribute position array in-place, set
  needsUpdate=true on the attribute, and recalculate vertex normals via
  geometry.computeVertexNormals(). Do NOT construct a new BufferGeometry.
  Output: interactive HTML 3D dashboard panel with Three.js terrain,
  particles, and orbit controls. All Three.js code is self-contained in
  a single HTML file with CDN-loaded dependencies from unpkg.com.
Performance
  Cache: cache pre-built geometry variants (terrain meshes, river curves) keyed
  by time index and swap buffers on slider change rather than calling
  new THREE.XxxGeometry() every tick. The cache is a Map<timeIndex,
  {terrain, rivers}> cleared only on full data reload.
  Particles: offload particle position updates to a vertex shader or use
  BufferGeometry with CPU-side position array reuse (Float32Array pool)
  instead of allocating per-frame position objects with clamp + terrain
  lookups. Particle geometries use BufferAttribute.needsUpdate = true to
  update positions per frame instead of rebuilding the entire BufferGeometry.
  Cache-warmup: on initial load, pre-compute terrain geometry for 10 time
  indices immediately and store in the cache. Total warmup volume
  (vertex count * 3 floats * 4 bytes per float * 10 indices) must fit within
  remaining VRAM after model load. Assuming 128 MB reserved for Three.js
  renderer and 32 MB for scene objects, at least 256 MB must remain available
  for warmup. The warmup budget is 192 MB or 50% of remaining VRAM, whichever
  is lower. If remaining VRAM is below 64 MB, warmup is skipped and terrain
  is generated on-demand with a loading indicator.
Validator / NT.md Template
NT.md Output Template for 3D Data Terrain Explorer
The blueprint grader validates NT.md against the following separator count and structure. Any deviation causes a scoring penalty.
NT.md separator rule:
  The NT.md file must use exactly 60 equals-sign characters as the section
  divider. The separator line reads:
  ============================================================
  (60 characters). Validator checks character count === 60. Values of 79 or
  any other length cause a completeness deduction.
NT.md Template Content
============================================================================
3D Data Terrain Explorer — Output Checklist
============================================================================
Section: Terrain
  Terrain heightfield generated from time-series data?
    Y/N / confidence
  BufferGeometry used with Float32BufferAttribute for positions?
    Y/N / confidence
  Vertex colors mapped to secondary metric with gradient?
    Y/N / confidence
  Terrain reshapes on time-slider change without full geometry rebuild?
    Y/N / confidence
  needsUpdate=true set on position attribute after each slider frame?
    Y/N / confidence
  computeVertexNormals called after position update?
    Y/N / confidence
  Old terrain geometry explicitly disposed on rebuild?
    Y/N / confidence
Section: Rivers
  Error/anomaly paths rendered as river tube geometry?
    Y/N / confidence
  Rivers use distinct reddish-brown material?
    Y/N / confidence
  River geometry and material disposed before terrain rebuild?
    Y/N / confidence
Section: Particles
  Error particles present (red, ~0.8 units, river waypoints)?
    Y/N / confidence
  API-call particles present (blue, ~0.3 units, valley centers)?
    Y/N / confidence
  Two particle types visually distinguishable by color + size + spawn?
    Y/N / confidence
  Cleanup/destroy method called on all particle systems before rebuild?
    Y/N / confidence
  Particle geometry and material disposed after cleanup?
    Y/N / confidence
  BufferAttribute.needsUpdate used for per-frame position updates?
    Y/N / confidence
  Float32Array reused across frames (no per-frame allocation)?
    Y/N / confidence
Section: Controls
  OrbitControls with damping enabled?
    Y/N / confidence
  Auto-rotation mode toggleable?
    Y/N / confidence
  Camera bookmarks stored in localStorage?
    Y/N / confidence
Section: Performance
  Geometry cache (Map<timeIndex, ...>) implemented?
    Y/N / confidence
  Cache-warmup runs on initial load (10 indices)?
    Y/N / confidence
  Warmup volume checked against VRAM budget (192 MB / 50% remaining)?
    Y/N / confidence
  Warmup skipped if remaining VRAM < 64 MB?
    Y/N / confidence
  No new THREE.XxxGeometry() calls during slider scrubbing?
    Y/N / confidence
Total: ___ / 28
============================================================================
MT.md and other files follow the same 60-equals separator rule.
GPU Memory Budget Constraint (cache-warmup)
When warmup pre-computes 10 terrain geometry variants, total vertex memory
consumed must be declared and validated:
  budget_used = sum_over_10_indices(vertices_per_index * 3 * 4)
    // 3 floats per vertex, 4 bytes per float
  budget_available = remaining_vram_bytes * 0.50
    // at most 50% of remaining VRAM, capped at 192 MB
  Assert: budget_used <= budget_available, else skip warmup
Default: assume 10 indices at 256x256 grid = 65,536 vertices each.
  65_536 * 3 * 4 * 10 = 7,864,320 bytes (~7.5 MB). Well within budget.
  If grid exceeds 1,024 x 1,024, warn and reduce warmup count or skip.
Particle Cleanup on Rebuild
When the time slider moves or data reloads:
  1. Call particleSystem.destroy() on each particle system.
     destroy() must:
       a. Remove Points object from scene via scene.remove(points)
       b. Call points.geometry.dispose()
       c. Call points.material.dispose() if material is unique
       d. Null references in the particle system registry
  2. Clear the particle system registry array.
  3. Create new particle systems with fresh geometry and materials.
  4. Add new Points objects to scene.
Failure to dispose old particles before creating new ones causes a GPU
memory leak (particles accumulate on rapid slider changes) and is scored
as a completeness bug.