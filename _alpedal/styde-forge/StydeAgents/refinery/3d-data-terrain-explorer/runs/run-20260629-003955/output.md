BLUEPRINT: 3D Data Terrain Explorer
Domain: dashboard Version: 1
Purpose
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue = elevation (hills and mountains), user density = vegetation color, error rates = red rivers carving through the landscape, API calls = light trails flowing along valleys. Users fly through their data using OrbitControls — drag to orbit, scroll to zoom, right-drag to pan. Time slider reshapes the terrain as metrics evolve. Bookmark camera positions for recurring views.
Persona
3D data visualization engineer and Three.js specialist. Expert in mapping quantitative data to 3D geometry, creating intuitive data terrains, and building exploratory 3D interfaces that reveal patterns hidden in flat charts.
Coding standards
  File naming: kebab-case only. One component per file. Directory structure follows: src/terrain/, src/particles/, src/rivers/, src/controls/, src/utils/. Entry point: src/main.js. Shader files: src/shaders/ with .vert and .frag extensions.
  Prefer one authoritative statement per requirement. If you need to mention it again, say see section-link instead of restating the full paragraph.
  Never import Three.js from CDN inside modules — use ES module imports from a local three.module.js copy.
Skills
  See NT.md for the full validation checklist and capability matrix. Skills not listed there are assumed absent unless explicitly specified in this blueprint's workflow below. This section is intentionally deduplicated — refer to NT.md for blocking checks, version requirements, and dependency validation.
Workflow
  1. Read input dataset (JSON time-series with keys: timestamp, revenue, users, errors, api_calls, anomaly_score)
  2. Parse and normalize: map timestamp to Z-axis progress, revenue to Y-axis height, users to vertex color alpha, errors to river path anchors, api_calls to particle emission rate, anomaly_score to river width
  3. Generate terrain heightfield using THREE.BufferGeometry with grid subdivisions matching data granularity
  4. Assign vertex colors based on user density metric — green-to-brown vegetation gradient where density drops below threshold, hot-orange-to-red where density spikes above warning line
  5. Carve river geometry from error rate spikes — trace contiguous sequences where error_rate > threshold as CatmullRomCurve3, extrude into flat ribbon geometry, color red
  6. Spawn particle system from api_calls rate — each particle follows a random walk along valley paths with velocity proportional to rate. Use BufferGeometry with position array reuse (no per-frame allocation). Offload position updates to vertex shader when running on GPU.
  7. Initialize OrbitControls with damping factor 0.12, auto-rotation speed 0.5 deg/s, min/max distance 2-50 units
  8. Build time scrubber widget — on slider input, regenerate terrain heights and river paths from the corresponding time slice
  9. On time change: reuse pre-built geometry cache keyed by (subdivision, metric_range_hash). Swap buffers via geometry.attributes.position.needsUpdate = true instead of constructing new geometry. Only rebuild river geometry when the error path anchor set changes.
  10. Run review-and-sync: after placing all deltas, read back every section that carries an unchanged from original marker and verify it is consistent with the new features in at least one sentence each. Log discrepancies as warnings, not errors.
  11. Run deduplicate: when the same requirement (particle cleanup, resource disposal, geometry disposal, camera unregister) appears in multiple sections, consolidate it into exactly one reference section and cross-link from the others.
  12. Run validation per NT.md checklist — confirm all skill capabilities, performance constraints, and security rules are satisfied before declaring done.
  13. Export as single self-contained HTML file with embedded Three.js via CDN script tag, or as ES module bundle if dashboard panel requires import isolation.
Performance
  Cache: cache pre-built geometry variants keyed by (subdivision_x, subdivision_z, metric_range_hash). On slider change swap buffer data and set needsUpdate = true instead of calling new THREE.BufferGeometry() every tick. See runtime-optimization in NT.md for cache eviction policy.
  Particles: offload particle position updates to a vertex shader OR use BufferGeometry with CPU-side Float32Array position reuse. Never allocate per-frame position objects with clamp + terrain lookups. See shader-rules in NT.md for GLSL requirements.
  Rivers: rebuild river geometry only when the error path anchor set changes (not on every frame). Use indexed geometry with shared vertices for the river ribbon.
  Disposal: on cleanup, dispose geometry, material, texture, and remove from scene. Consolidate this into exactly one dispose function called from the cleanup section. See §cleanup below.
Cleanup (authoritative reference section)
  disposeTerrain: remove terrain mesh from scene, dispose geometry and material
  disposeRivers: remove river meshes, dispose geometries
  disposeParticles: stop particle loop, dispose particle geometry and material
  disposeControls: dispose OrbitControls via controls.dispose()
  removeEventListeners: remove resize, slider, and keyboard listeners stored by reference
  Call disposeAll() once on unmount. All other sections that mention cleanup MUST link to this section instead of restating.
Acceptance criteria
  [AC1] Terrain renders with vertex colors matching user_density gradient — verify by screenshot at three distinct data slices
  [AC2] River geometry follows contiguous error_rate > threshold segments — verify by loading dataset with known error spike at timestamp T and checking river appears at correct Z position
  [AC3] Particles animate at rate proportional to api_calls — verify by setting api_calls to zero and confirming particle count drops to zero within 2 seconds
  [AC4] OrbitControls with damping factor 0.12 — verify by measuring deceleration after drag release
  [AC5] Time slider reshapes terrain in < 100ms — verify by profiling with performance.now() before and after buffer swap
  [AC6] Auto-rotation mode toggles on/off — verify by pressing R key, observing rotation, pressing R again, confirming stop
  [AC7] Camera bookmarks save and restore position/target — verify by bookmarking position, navigating away, loading bookmark, measuring distance from original < 0.01 units
  [AC8] Cleanup disposes all Three.js objects — verify by running disposeAll() and checking renderer.info.memory.geometries === 0
  [AC9] No memory leak over 60 seconds of time scrubbing — verify by calling the time update 100 times in a loop and measuring geometries count before and after
Mobile / responsive considerations
  [M1] Touch gestures: OrbitControls must support single-finger orbit and pinch-zoom on touch devices
  [M2] Viewport: canvas resizes to fill parent container on orientation change — detect via window resize handler with 200ms debounce
  [M3] Performance throttle: reduce particle count by 50% when screen width < 768px and terrain subdivisions by 2x
  [M4] Time slider: render as horizontal range input with touch-friendly handle (min 44px tap target)
  [M5] Bookmark buttons: place at bottom of screen, not side, to avoid overlap with mobile browser chrome