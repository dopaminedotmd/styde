3D Data Terrain Explorer
Domain: dashboard
Version: 2
Purpose
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue = elevation (hills and mountains), user density = vegetation color, error rates = red rivers carving through the landscape, API calls = light trails flowing along valleys. Users fly through their data using OrbitControls — drag to orbit, scroll to zoom, right-drag to pan. Time slider reshapes the terrain as metrics evolve.
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
Performance Checklist
  Throttle: skip particle position updates when time index unchanged between frames
  Geometry reuse: cache pre-built BufferGeometry variants, swap buffers on slider change
  Shader offload: vertex shader handles particle position interpolation, CPU only feeds uniforms
  Attribute cleanup: strip unused geometry attributes before upload to GPU
Performance Budget
  max_draw_calls: 200
  max_vertices_total: 500000
  max_particles: 10000
  terrain_update_frequency: on time-slider change only
  particle_update_frequency: once per time index, no per-frame recalc
  target_fps: 60
  target_gpu_memory_mb: 256
Accessibility
  keyboard_navigation: WASD pan, Q/E roll, R/F altitude, 1-9 bookmark slots
  colorblind_mode: deuteranopia/protanopia/tritanopia palette toggle
  labels: hover tooltips on terrain peaks and river nodes with aria-live region for screen readers
  reduced_motion: disable auto-rotation, set damping to instant jump
Time Slider UI
  type: HTML range input overlaid on canvas
  range: full dataset time span, step = one time slice
  display: timestamp label adjacent to slider
  bookmarks: num keys 1-9 save/restore camera position + time index
Controls UI
  orbit: left-drag rotate, scroll zoom, right-drag pan
  damping: 0.1 default, 0.0 in reduced-motion mode
  auto_rotate: checkbox toggle, speed 0.5 rad/s
  bookmarks: save with Ctrl+[1-9], restore with [1-9]
Output Spec
  A single self-contained HTML file loading Three.js + OrbitControls from CDN
  Inline CSS, no external dependencies beyond CDN scripts
  Terrain rendered as BufferGeometry with vertex colors
  Particle system using Points with BufferGeometry, shader-updated positions
  River geometry as TubeGeometry following anomaly paths
  Time slider as HTML range input, terrain rebuilds on slider change via buffer swap
  Performance budget section documenting draw calls, vertex counts, update frequency