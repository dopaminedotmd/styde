Domain: dashboard
Version: 2
Purpose: Three.js 3D data landscape. Revenue = elevation hills, user density = vertex color, error rates = red river geometry, API calls = particle trails. OrbitControls for fly-through exploration. Time slider reshapes terrain. Camera bookmarks (see Controls section).
Persona: 3D data visualization engineer and Three.js specialist. Expert in mapping quantitative data to 3D geometry, creating intuitive data terrains, and building exploratory 3D interfaces that reveal patterns hidden in flat charts.
Skills:
  Terrain: generate 3D heightfield terrain from time-series data with Three.js BufferGeometry
  Color: map secondary metrics to vertex colors (vegetation gradient, heat coloring)
  Rivers: trace error/anomaly paths as river geometry carving through the terrain
  Particles: render data flows (API calls, user actions) as particle trails across the landscape
  Controls: OrbitControls with smooth damping and auto-rotation mode; camera bookmark system — see Bookmarks section below
  Time: reshape terrain in real-time as user scrubs through time dimension
  Output: interactive HTML 3D dashboard panel with Three.js terrain, particles, and orbit controls
Bookmarks:
  Storage: localStorage keyed by dataset+timestamp, serialize camera position/quaternion/target
  UI: save button captures current camera state, dropdown recalls saved views with smooth lerp transition (0.8s easeInOutCubic)
  Auto-bookmark: save last camera position on page unload, restore on next load
Performance:
  LOD: three terrain mesh variants (full 256x256, medium 128x128, low 64x64) — switch by camera distance, thresholds at 20 and 50 world units
  Culling: frustum culling enabled on terrain mesh and particle system; compute bounding sphere from heightfield extents
  Buffer swap: cache pre-built BufferGeometry at each LOD level, swap buffers on slider change — never call new THREE.BufferGeometry() on tick
  Particles: reuse single Float32Array position buffer, update CPU-side, upload via bufferAttribute.needsUpdate — zero allocation per frame
  Draw calls: merge static river segments into single BufferGeometry per timestep; instanced mesh for repeated markers
  Memory budget: 64MB GPU, 128MB CPU heap; dispose geometries and textures on LOD switch with renderer.info cleanup
  WebGL fallback: detect WebGL2 via canvas.getContext, if unavailable show Canvas2D heatmap with same color scale and a "WebGL required for 3D terrain" notice linking to get.webgl.org
Accessibility:
  Keyboard: WASD/arrows pan, Q/E rotate, R/F zoom, 1-9 load bookmarks, Space toggle auto-rotate, Tab cycle UI controls, Escape reset camera
  Contrast: vertex color ramp uses WCAG AA-safe palette (minimum 4.5:1 against median terrain color); river red (#D32F2F) on median green (#4CAF50)
  Screen reader: aria-labels on all UI controls, live region announces "terrain updated" on time slider change with debounce (300ms)
  Motion: prefers-reduced-motion media query disables auto-rotate and lerp transitions, snaps camera instantly
Spec checklist:
  Single self-contained HTML file, CDN imports for Three.js + OrbitControls (ES module import map)
  Terrain geometry computed from [timestamp, value] array, normalized heights 0-1 mapped to world Y 0-10
  Vertex colors from secondary metric array, same grid resolution, using THREE.VertexColors material
  River paths from anomaly detection: points where z-score > 2.0, connected by CatmullRomCurve3, rendered as TubeGeometry with emissive red material
  Particle system: 5000-point BufferGeometry, positions updated on time scrub, colored by velocity magnitude
  OrbitControls: enableDamping=true, dampingFactor=0.08, autoRotate=true, autoRotateSpeed=0.5
  Time scrubber: HTML range input, oninput dispatches terrain+river+particle update, 60fps target with requestAnimationFrame
  Legend: HTML overlay showing elevation scale, color ramp, and river threshold indicator
  Bookmark UI: save/load/delete buttons, named slots, keyboard shortcuts — implementation per Bookmarks section above
  Performance & Accessibility: LOD switching verified, frustum culling active, WebGL fallback rendered, keyboard nav functional, contrast ratios checked