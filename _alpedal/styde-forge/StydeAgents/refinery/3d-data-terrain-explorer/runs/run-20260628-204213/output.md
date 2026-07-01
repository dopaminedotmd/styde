BLUEPRINT:
3D Data Terrain Explorer
Domain: dashboard Version: 2
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
Validation
  - 3D structure: verify correct depth ordering, layer rendering, parallax effect across viewport. Automated assertion: terrain faces render with z-sorting correct for at least 3 camera angles.
  - Visual correctness: no broken transforms (scale/rotation matrix determinant > 0), correct z-index stacking on overlay elements, no degenerate triangles (area > 0) in generated BufferGeometry.
  - Render performance: full frame render < 16ms (60 FPS threshold). Measured via performance.now() wrapper around render loop. Fail if 3 consecutive frames exceed 32ms.
  - Memory: no geometry/geometry-attributes allocation outside initial setup and slider change. Verify via heap snapshot diff before/after orbit interaction. Fail on leak > 5% per bookmark switch.
  - FPS constraint: animation loop target 30 FPS minimum. Measured over 5-second window. Fail if average < 25 FPS or any single frame > 100ms.
Code extraction rules
  - Extract code blocks using balanced-brace matching (track open/close count across newlines) instead of regex that stops at first EOL-brace.
  - Match tokens with word boundaries. Edge-case detection uses exact substring match '\bedge\b' not bare 'edge' which matches 'knowledge', 'edge-case', 'hedge'.
  - Parameter extraction from function signatures: use a simple tokenizer counting paren depth, not reg ex greedy capture.
Efficiency
  - Script consolidation: before adding a new verification or utility script, check if an existing script can be extended with a parameter (mode, input type, threshold). Two scripts differing only in constants or one regex pattern are one script with a parameter.
  - Verification checklist step: 'Before adding new scripts or files, check whether an existing one can be extended or parameterized. If the new version would share > 60% of lines with an existing script, extend the existing one instead.'
Quality standards
  - No duplicate or almost-duplicate scripts. Define duplicate as: same logic with different constants, same loop structure with different variable names, same verification steps with different thresholds. Consolidate into parameterized scripts.
Performance
  - Cache: cache pre-built geometry variants and swap buffers on slider change rather than calling new THREE.XxxGeometry() every tick. Use THREE.BufferGeometryUtils.mergeBufferGeometries for composite landscapes.
  - Particles: offload particle position updates to vertex shader with uniform time, or reuse Float32Array position buffer with CPU-side write and BufferGeometry.attributes.position.needsUpdate = true. No per-frame new allocations.
  - Raycaster: throttle raycast checks to every 3rd frame for hover/tooltip detection. Cache last hit object.
  - River geometry: build river mesh once from path spline, regenerate only when underlying error data changes. Store as BufferGeometry with pre-computed normals.
Implementation constraints
  - Single HTML file output. Three.js loaded from CDN (unpkg or cdnjs).
  - No external build step. No bundler. No npm install.
  - Synthetic demo data generator included inline. Default dataset: 30x30 grid, 4 time steps.
  - Controls panel: time slider, auto-rotate toggle, bookmark save/load (localStorage), reset camera button.
  - River paths: minimum 2 paths with at least 5 control points each.
  - Color scheme: terrain elevation viridis gradient, error rivers red-to-orange, particle trails cyan-to-white with opacity fade.