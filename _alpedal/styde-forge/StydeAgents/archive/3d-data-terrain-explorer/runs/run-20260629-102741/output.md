3D Data Terrain Explorer
Domain: dashboard
Version: 1
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
  Cache: before declaring a feature complete, audit the implementation for repeated computations and confirm every cacheable output is stored (geometries, noise grids, particles, textures)
  Readability: prefer 3-line readable code over 1-line clever code; always add one explanatory comment per block of logic
  Hot-path: identify hot-path allocations (each-frame or each-event) and add debounce/memoize/cache where geometry or data is rebuilt on repeated calls
REQUIREDFEATURES
All UI interactions listed below are pass/fail acceptance criteria. Each MUST be wired with real event handlers — not just rendered in the DOM. Verification: open browser DevTools, enable Event Listener Breakpoints for mouse/keyboard events, and confirm each interaction triggers a handler call.
  Tooltip-Hover: hovering the mouse over any terrain vertex or particle MUST display a tooltip with the underlying data values (metric name, value, timestamp). Implementation: raycasting via THREE.Raycaster on pointermove, intersect BufferGeometry, read vertex attribute data at the intersected index. Verification: move mouse slowly across terrain surface — tooltip must appear within 100ms of pointer stopping over a vertex, must update as pointer moves to adjacent vertices, and must disappear when pointer leaves all geometry. Tooltip must show correct data values matching the raw dataset at that (x,z) coordinate.
  Click-to-Select: clicking a terrain vertex or river segment MUST select it (highlight with outline or emission color change) and display a detail panel with all metrics at that point. Verification: click 5 random points on terrain and river — each must highlight the clicked element and populate the detail panel with non-null values.
  Time-Slider Terrain Morph: dragging the time slider MUST reshape terrain geometry in real-time. Verification: scrub slider from min to max at 30fps — terrain heightfield must visibly morph, vertex colors must update, and river paths must recompute within 200ms of slider release.
  OrbitControls: MUST support drag-to-rotate (left mouse), scroll-to-zoom, right-drag-to-pan. Verification: perform each interaction — camera must respond with <50ms latency.
  Camera Bookmarks: clicking a saved bookmark button MUST restore camera position, target, and zoom level within 200ms. Verification: save 3 bookmarks at distinct positions, verify each restores exactly.
  Auto-Rotation: toggling auto-rotate MUST smoothly rotate camera around terrain at configurable speed. Verification: toggle on — camera orbits continuously without jank at 60fps.
  Diagnostic Panel: MUST display cache hit/miss rates, frame time, and worker message count. Verification: panel visible and updates at least 1 Hz during interaction.
Worker Offloading
MANDATORY: terrain mutation, path tracing, and river flood-fill MUST run in a Web Worker. The main thread handles only rendering, OrbitControls, and UI events.
Architecture:
  1. Create a dedicated Web Worker (new Worker('terrain-worker.js')) on dashboard init
  2. Transfer raw dataset (Float32Array) to worker via postMessage with transferable ArrayBuffer handoff: worker.postMessage({ type: 'load', buffer: dataBuffer }, [dataBuffer])
  3. Worker computes: heightfield vertices, vertex colors, river control points, particle paths, noise grids
  4. Worker returns results via postMessage as Float32Array of vertex positions, Uint8Array of colors, Float32Array of river curve points
  5. Main thread receives results into pre-allocated BufferGeometry attributes (NEVER allocate new Float32Array on receive — write into existing attribute.array via .set())
  6. Worker recompute triggers only when terrain parameters change (dirty-flag), not on render-loop idle ticks
Per-frame Budget
All per-time-step computation MUST fit within 8 ms on mid-range hardware (integrated GPU, 4-core CPU) to maintain 60 fps.
  Main-thread budget: 5 ms for render call (renderer.render), 2 ms for OrbitControls update, 1 ms for UI callbacks and raycaster
  Worker budget: terrain recompute < 16 ms (one 60fps frame of headroom, single invocation)
  River mesh recompute: debounced at 200ms, execute < 8 ms
  Particle position update: vertex shader or BufferGeometry reuse, execute < 2 ms on main thread
  Raycaster (tooltip hover): intersectObjects budget < 2 ms per pointermove event; debounce raycaster to fire max every 16ms (once per frame)
Dirty-Flag Mechanism
River mesh and particle paths MUST only recompute when terrain parameters actually change, not on every render loop iteration.
Implementation:
  1. terrainDirty flag: set to true when time-slider value changes, false after worker recompute completes
  2. riverDirty flag: set to true when terrainDirty transitions from true to false (terrain changed, rivers need update), false after river rebuild
  3. particleDirty flag: set to true when terrainDirty transitions, false after particle path recalculation
  4. Render loop checks: if (!terrainDirty && !riverDirty && !particleDirty) skip all recompute; only call renderer.render(scene, camera)
  5. Slider input handler: on slider input event, set terrainDirty = true. On slider change (release), post message to worker. Do NOT post on every input event — input updates terrain preview via vertex shader displacement, not full geometry rebuild
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
Implementation Guidance
Deliver: produce exact artifact type stated; verify against every acceptance criteria in REQUIREDFEATURES; only then mark done.