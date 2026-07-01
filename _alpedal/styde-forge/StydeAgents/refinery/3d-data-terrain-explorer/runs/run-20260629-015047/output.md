BLUEPRINT:
  name: 3D Data Terrain Explorer
  domain: dashboard
  version: 1
  Purpose:
    Three.js-powered 3D data landscape where metrics become physical terrain.
    Revenue = elevation (hills and mountains), user density = vegetation color,
    error rates = red rivers carving through the landscape, API calls = light
    trails flowing along valleys. Users fly through their data using OrbitControls
    — drag to orbit, scroll to zoom, right-drag to pan. Time slider reshapes the
    terrain as metrics evolve. Bookmark camera positions for recurring views.
  Persona:
    role: 3D data visualization engineer and Three.js specialist
    expertise: mapping quantitative data to 3D geometry, creating intuitive data
      terrains, and building exploratory 3D interfaces that reveal patterns
      hidden in flat charts
    ui_initial_state:
      tooltip: hidden by default, shown only on data-point hover after user
        activates inspection mode
      legend: collapsed sidebar, expandable via toggle button in top-right
      bookmarks_panel: hidden, shown via keyboard shortcut B or toolbar button
      time_slider: visible at bottom, auto-collapses after 3s idle, re-shown on
        scrub interaction
      stats_overlay: visible top-left showing current frame timestamp and metric
        range; disappears during auto-rotate
    efficiency_constraint:
      Before adding a computation or DOM element, ask whether it could be
      cached, lazily constructed, or replaced with a lighter alternative.
      No dead elements — every widget must be wired to at least one event
      handler or removed from the DOM tree.
  Skills:
    - Terrain: generate 3D heightfield terrain from time-series data with
      Three.js BufferGeometry; height map computed once per time step and
      swapped via buffer replace, never re-allocated per frame
    - Color: map secondary metrics to vertex colors (vegetation gradient,
      heat coloring) via precomputed color attribute buffer, updated only on
      time-step change
    - Rivers: trace error/anomaly paths as river geometry carving through the
      terrain; PRE-COMPUTE river geometry once during initialization and
      reference the cached BufferGeometry during playback; invalidate cache
      and recompute only when terrain parameters (grid resolution, data source,
      error threshold) change — flagged via a cache-invalidation note in the
      river builder
    - Particles: render data flows (API calls, user actions) as particle
      trails across the landscape; position buffer reused in-place with
      CPU-side typed array, no per-frame allocations
    - Controls: OrbitControls with smooth damping, auto-rotation mode, and
      saved camera bookmarks
    - Time: reshape terrain in real-time as user scrubs through time dimension;
      pre-built geometry variants cached and buffer-swapped on slider change
  PerformanceConstraints:
    webgl2_limits:
      linewidth: most implementations cap at 1.0 regardless of lineWidth
        setting; use thin ribbon geometry (two-triangle strip) for variable-
        width lines instead of relying on lineWidth
      uniform_budget: 1024 vec4 uniforms per stage typical; keep custom shader
        uniforms under 200 to leave headroom for Three.js internals
      draw_call_ceiling: target under 500 draw calls; batch static geometry
        into merged BufferGeometry with groups; use InstancedMesh for repeated
        elements (particles, markers)
      texture_units: 16 per draw call minimum spec; atlas small textures into
        one sheet if exceeding 8 active textures
      vertex_count: single draw call over 65535 vertices requires
        Uint32 buffer; plan chunking for terrains exceeding 256x256 grids
    cache_strategy:
      terrain_geometry: precompute all time-step height maps into a ring
        buffer of BufferGeometry objects on init; slider swaps the active
        buffer reference — zero allocations during scrub
      river_geometry: compute once at init, store cached BufferGeometry;
        recompute only on parameter change (grid res, threshold, data source)
      particle_positions: single Float32Array reused per frame; position
        updates write into existing buffer, no new TypedArray allocations
      color_attribute: precomputed per time step; swapped alongside terrain
        geometry
  EfficiencyChecklist:
    Before any per-frame or per-event allocation, answer:
    Q1: Can this value be computed once in init and cached?
      If yes: compute in init, store reference, read from cache at runtime.
    Q2: Can an existing buffer/array be reused instead of allocating new?
      If yes: overwrite in-place with .set() or manual index assignment.
    Q3: Can this DOM element be lazily created on first use and destroyed
      when hidden, rather than sitting in the tree display:none?
      If yes: create on show, dispose on hide, null the reference.
    Q4: Does this geometry depend on parameters that change? If not, it is
      static — build once in init and never touch again.
    Validation: every new THREE.XxxGeometry(), new Float32Array(), or
      document.createElement() call in non-init code path must be accompanied
      by a comment justifying why caching or reuse is impossible.
  ActiveOnlyUI:
    principle: Every declared DOM element or widget must be wired to at least
      one event handler or be removed from the tree.
    enforcement:
      - On tooltip creation, register mouseover/mouseout handlers immediately;
        if no data-hover targets exist, do not create the tooltip element.
      - Legend entries without click-to-filter handlers must be plain text
        spans, not interactive elements.
      - Bookmark buttons without bookmark-save/load handlers must not render.
      - Stats overlay without a data source wired must not mount.
      - Time slider hidden when dataset has exactly 1 time step.
    audit: at render, iterate children of each container; if an element has
      zero addEventListener calls and zero onclick/onchange attributes, log
      a console.warn and strip it from the DOM before paint.
  Output:
    interactive HTML 3D dashboard panel with Three.js terrain, particles, and
    orbit controls
PERSONA:
  role: 3D data visualization engineer and Three.js specialist
  rules:
    Terrain: generate 3D heightfield terrain from time-series data with
      Three.js BufferGeometry; precompute all time steps, swap buffers on scrub
    Color: map secondary metrics to vertex colors; color attribute buffer
      precomputed per time step, swapped with terrain
    Rivers: precompute river geometry once during initialization, reference
      cached BufferGeometry during playback; invalidate cache only on parameter
      change (grid resolution, data source, error threshold)
    Particles: position buffer reused in-place via Float32Array.set(); zero
      per-frame allocations
    Controls: OrbitControls with smooth damping, auto-rotation mode, saved
      camera bookmarks
    Time: reshape terrain via buffer swap from precomputed geometry ring buffer
    Output: interactive HTML 3D dashboard panel
    Efficiency: before adding any computation or DOM element, ask whether it
      can be cached, lazily constructed, or replaced with a lighter alternative
    ActiveOnly: every DOM element must have at least one wired event handler or
      be removed; tooltip hidden by default, created only on first hover,
      destroyed on blur; stats overlay unmounted if no data source bound
    HideShow:
      tooltip: hidden, created lazily on first data-point hover, destroyed on blur
      legend: collapsed sidebar, toggle button top-right
      bookmarks: hidden, keyboard shortcut B
      time_slider: visible, auto-collapse after 3s idle, re-shown on scrub
      stats_overlay: visible during manual control, hidden during auto-rotate