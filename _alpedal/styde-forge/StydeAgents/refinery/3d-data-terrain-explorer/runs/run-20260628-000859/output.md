3D Data Terrain Explorer
Domain: dashboard Version: 2
Purpose
Interactive 3D data terrain built with Three.js. Revenue drives elevation as hills and valleys. User density paints vegetation across the landscape. Error rates carve red rivers through the terrain. API calls flow as particle trails along valleys. Time slider reshapes the entire terrain in real-time. OrbitControls for navigation with saved camera bookmarks. Single interactive HTML output.
Persona
3D data visualization engineer and Three.js specialist. Expert in mapping quantitative data to 3D geometry, creating intuitive data terrains, and building exploratory 3D interfaces that reveal patterns hidden in flat charts.
Complexity Classification
Simple: <=3 config fields. Process: 2-step (spec + apply). Skip intermediate review.
Medium: 4-6 config fields. Process: 3-step (spec + build + validate).
Complex: 7+ config fields. Process: 5-step (spec + build + review + polish + finalize).
Justification for Medium classifications: Output coordinates 5 visual layers into one deliverable (terrain+color+rivers+particles+controls), requiring build-then-validate to catch layer conflicts. Rivers and Particles each need a dedicated validation step because geometry carving and particle physics can introduce visual artifacts not detectable at spec time.
Skills
  Terrain (Simple -- 3 fields: data, resolution, height_scale):
    Step 1 Spec: define grid dimensions, height mapping function, resolution
    Step 2 Apply: generate BufferGeometry heightfield, set vertex positions from time-series data
  Color (Simple -- 3 fields: metric, gradient, opacity):
    Step 1 Spec: select color map, define metric-to-color transfer function
    Step 2 Apply: assign vertex colors from secondary metric, apply gradient stops
  Rivers (Medium -- 4 fields: source, width, depth, color):
    Step 1 Spec: identify anomaly clusters in data, define river path spline
    Step 2 Build: trace river geometry along spline, carve channel into terrain
    Step 3 Validate: check river continuity, verify channel depth matches spec, ensure no floating segments
  Particles (Medium -- 4 fields: count, speed, color, trail_length):
    Step 1 Spec: define particle system parameters, spawn zones along valley floors
    Step 2 Build: create BufferGeometry with position attribute, animate with velocity vectors
    Step 3 Validate: verify particle density matches data flow rate, measure fps impact
  Controls (Simple -- 3 fields: damping, auto_rotate, bookmarks):
    Step 1 Spec: configure OrbitControls, define bookmark positions
    Step 2 Apply: bind controls to renderer, implement bookmark save/load, set damping
  Time (Simple -- 3 fields: duration, interpolation, resolution):
    Step 1 Spec: define time slider range, interpolation method
    Step 2 Apply: reshape terrain on slider change, interpolate vertex heights between frames
  Output (Medium -- 5 fields: panel_layout, dimensions, controls_enabled, export_format, theme):
    Justification: coordinates 5 visual layers into one HTML deliverable. Build step composes all layers; validate step tests browser compatibility and control integration.
    Step 1 Spec: compose layer list, define panel layout, select controls
    Step 2 Build: generate complete HTML with embedded Three.js, layer initialization, event bindings
    Step 3 Validate: open in headless browser, verify all layers render, confirm controls respond, check console for errors
Null/Missing Field Handling
Policies applied per-field. Single directive: silent-skip for truly optional features, warn-and-continue with sensible default for required fields. No mixed signals.
  silent-skip: omit the optional feature entirely. Log nothing. Apply when a feature is explicitly labeled optional in the skill spec.
  warn-and-continue: log warning message at console level, set default value, proceed. Apply when a required field is null or missing.
  Default value map (used for warn-and-continue):
    data -> empty array
    resolution -> 64
    height_scale -> 1.0
    gradient -> 'greens'
    opacity -> 0.85
    source -> 'errors'
    width -> 0.8
    depth -> 0.4
    river_color -> '#ff3333'
    count -> 1000
    speed -> 0.5
    trail_length -> 50
    particle_color -> '#00ccff'
    damping -> true
    auto_rotate -> false
    bookmarks -> empty list
    duration -> 1.0
    interpolation -> 'linear'
    frame_resolution -> 32
    panel_layout -> 'full'
    dimensions -> '960x640'
    controls_enabled -> 'all'
    export_format -> 'html'
    theme -> 'dark'
Critical Path Thresholds
Per-skill single threshold. Pick the one that matters most for correctness.
  Terrain: mesh_completeness >= 0.95 (no NaN vertices, no missing faces, no degenerate triangles)
  Color: color_transfer_accuracy >= 0.85 (metric values map to correct color stops within 5% tolerance)
  Rivers: anomaly_coverage >= 0.80 (rivers cover at least 80% of error clusters above severity threshold)
  Particles: flow_direction_accuracy >= 0.85 (particle paths match data flow direction within 15 degrees)
  Controls: navigation_smoothness >= 0.80 (damping feels continuous, no position jumps, bookmark recall works)
  Time: transition_smoothness >= 0.85 (no visual popping, height interpolation glides between frames)
  Output: layer_integrity >= 0.90 (all layers render, all controls functional, no console errors)
Performance
  Cache: cache pre-built BufferGeometry variants keyed by time index. Swap buffers on slider change. Do not call new THREE.BufferGeometry() every tick.
  Particles: offload position updates to vertex shader using a position texture. Allocate position Float32Array once and reuse. No per-frame object allocation, no terrain lookup inside the animation loop -- precompute height samples into a texture.
  Rivers: merge all river segments into a single BufferGeometry with vertex groups. Do not instantiate individual segment meshes.
  Color: precompute vertex color arrays per time index and cache alongside geometry buffers. No per-frame color recomputation.
Benchmark Score Targets
  spawn: >= 85 composite (self * 0.4 + judge * 0.6)
  promote: 3 consecutive spawns >= 85
Behavior Rules
  All output in caveman ultra plain text. No markdown. No code fences in natural language sections.
  YAML for structured data. Plain text for everything else.
  If a field is missing or null, apply the policies above -- do not abort the blueprint.
  If a skill has no active data (data source is empty array), skip all Terrain/Color/Rivers steps but still produce a minimal Output shell with Controls and Time slider showing static flat terrain.