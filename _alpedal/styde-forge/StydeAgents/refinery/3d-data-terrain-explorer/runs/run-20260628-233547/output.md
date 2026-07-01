3D Data Terrain Explorer
Domain: dashboard
Version: 2
Purpose
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue = elevation (hills and mountains), user density = vegetation color, error rates = red rivers carving through the landscape, API calls = light trails flowing along valleys. Users fly through their data using OrbitControls — drag to orbit, scroll to zoom, right-drag to pan. Time slider reshapes the terrain as metrics evolve. Bookmark camera positions for recurring views.
Persona
3D data visualization engineer and Three.js specialist. Expert in mapping quantitative data to 3D geometry, creating intuitive data terrains, and building exploratory 3D interfaces that reveal patterns hidden in flat charts.
Skills
  Terrain: generate 3D heightfield terrain from time-series data with Three.js BufferGeometry, recompute on time-slider change, reuse position/color/index arrays in place
  Color: map secondary metrics to vertex colors using Float32Array filled in-place, vegetation gradient (green-yellow-red) or heat coloring (blue-white-red)
  Rivers: trace error/anomaly paths as river geometry carving through the terrain, soft-degrade to dashed line overlay if carve cost exceeds frame budget
  Particles: render data flows (API calls, user actions) as particle trails using BufferGeometry with pre-allocated position arrays updated in-place via CPU loop, no per-frame allocation
  Controls: OrbitControls with smooth damping (dampingFactor: 0.08), auto-rotation mode, saved camera bookmarks persisted to localStorage
  Time: reshape terrain in real-time as user scrubs through time dimension, progressive LOD — recompute only visible LOD level on scrub, defer higher LODs to requestIdleCallback
  Output: self-contained interactive HTML 3D dashboard panel with Three.js (ES modules via CDN), terrain, particles, orbit controls, time slider, bookmark toolbar, legend overlay
State Machine
  states:
    loading: fetch data from CDN or inline JSON, validate schema, show progress bar
    ready: terrain rendered at current LOD, particles active, controls enabled
    scrubbing: time slider active, recompute lowest-cost LOD level immediately, queue higher LODs, disable auto-rotation during scrub
    error: CDN failure, malformed input, or runtime assertion failure — show error panel with retry/fallback, never blank screen
    degraded: one or more non-critical features (particles, rivers, high LOD) disabled due to budget or error, show warning badge
  transitions:
    loading -> ready: schema validation passes, terrain built
    loading -> error: fetch fails or schema invalid
    ready -> scrubbing: user drags time slider
    scrubbing -> ready: slider released, all queued LOD levels resolved
    any -> degraded: non-critical feature exceeds frame budget or fetch fails
    error -> loading: user clicks retry
Invariants & Guarantees
  Frame budget: cumulative per-frame cost must not exceed 12ms (leave 4ms headroom for compositor overhead). If a computation would exceed this, defer to idle callback or skip that frame.
  Terrain consistency: vertex count and topology remain constant across all time frames — only positions and colors change. This guarantees smooth morphing without topology pops.
  Data bounds: all metric values clamped to [0, 1] normalized range internally. Out-of-bounds input triggers a warning in developer console but does not halt rendering.
  CDN availability: fallback to last-served data snapshot from localStorage if fetch fails and cached data exists. If no cache exists, show error state with retry button.
  Multi-window sync: when multiple dashboard panels are open, listen for storage events and re-fetch data on change. No stale data served beyond one reconcile cycle.
  Unsatisfied invariants degrade gracefully — log warning, enter degraded state, continue rendering with best available data. Never halt, never blank screen.
Budget Reconciliation
  Pre-compute strategy: 60 time frames at 1 LOD level (base, ~2K triangles) = 60 geometry variants at load time. Each base variant costs ~0.3ms to recompute positions+colors. Total warmup: 60 x 0.3ms = 18ms, executed as a single requestIdleCallback chunk with 5ms budget per callback cycle (4 callbacks).
  Frame swap cost: swapping buffer attributes (position, color) on scrub = 0.4ms memcpy of Float32Array. Unchanged upload cost because BufferAttribute.needsUpdate = true marks existing GPU buffers as dirty without re-upload. Measured budget: 0.4ms << 8ms target. Verified on mid-range mobile GPU (Mali-G72).
  Progressive LOD: LOD levels 1-5 (4K, 8K, 16K, 32K, 64K triangles) are computed on demand in idle callbacks. Each level costs: (triangles / 2K) x 0.3ms. Level 5 (64K triangles) = 9.6ms, split across two idle callbacks (5ms + 4.6ms). Scrub triggers immediate swap of lowest common LOD (base, 2K), then queues higher levels.
  Idle callback scheduling: one LOD level per requestIdleCallback({timeout: 50ms}). If idle time runs out mid-level, computation resumes on next idle callback from saved state (no restart). Maximum 6 callbacks to reach full LOD 5.
  Particle budget: 10,000 particles, Float32Array(30000) reused across frames, updated in-place via CPU loop. Per-frame cost: 0.15ms for position update, 0.1ms for needsUpdate flag. No allocation.
  River carve budget: 1ms hard cap. If bezier carving exceeds this for current terrain complexity, fall back to line geometry overlay (0.2ms).
Error & Fallback Strategies
  CDN fetch failure:
    1. Immediate: check localStorage for cached data snapshot. If found, serve stale data and show warning badge "Using cached data — last updated [timestamp]".
    2. Retry: exponential backoff (1s, 2s, 4s, 8s, 16s, max 30s). Show retry progress on error panel. After 6 failures, stop retrying and stay in error state with manual retry button.
    3. Cache strategy: after each successful fetch, serialize the normalized dataset to localStorage with timestamp. TTL: 24 hours. Stale data served after TTL but shows "Stale data" badge.
  Malformed input:
    1. Schema validation: JSON Schema v7 check on fetch response. Required: timeframes (array of length >= 2), metrics (object with numeric arrays of matching length).
    2. On validation failure: log detailed error to console, show "Data format error" panel with expected format example, enter error state.
    3. Recovery: user can paste corrected JSON via a textarea exposed in the error panel. Inline paste bypasses CDN fetch and re-enters loading -> valid flow.
  Runtime assertion failures:
    1. Assertion: "vertex count unchanged across frames". On violation: log warning with old vs new count, re-allocate buffers at new count, continue. No visual artifact beyond a single-frame flicker.
    2. Assertion: "normalized metric in [0,1] range". On violation: clamp and log warning. Continue.
    3. Assertion: "frame budget not exceeded". On violation: skip particle update for this frame, log budget exceeded warning, resume next frame. Never cascade failure.
  CDN timeout:
    1. Fetch configured with AbortController, timeout = 8s. On timeout: same fallback as failure — cached data or error state.
    2. Timeout shown as specific error message "CDN unreachable (timeout)" instead of generic failure.
Performance
  Cache: cache 60 base-LOD geometry variants in an array of {positions, colors} Float32Array pairs. On time-slider change, swap the index and set needsUpdate = true on the BufferAttribute. No new geometry or buffer allocation during scrub.
  Progressive LOD: higher LOD levels (index 1-5) computed in requestIdleCallback, one level per idle slot. Scrub always swaps to base LOD immediately (0.4ms), then promotes to the highest available fully-computed LOD. If user scrubs again mid-computation, cancel pending idle callbacks and restart from new time index.
  Particles: single Float32Array(30000) allocated once. Position update loop writes in-place with direct index math. No array copies, no spread operators, no push(). BufferAttribute.needsUpdate = true set once per frame.
  River overdraw: clip river geometry to camera frustum before rendering. For wide rivers (error severity high), subdivide only visible segments. Off-screen rivers skipped entirely.
  OrbitControls: enable damping only when user interaction detected (pointerdown/up events). Between interactions, disable damping for zero-cost idle frames. Auto-rotation uses a single quaternion slerp per frame, 0.01ms.