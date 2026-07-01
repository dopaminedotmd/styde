3D Data Terrain Explorer — applied teacher feedback from runs 87.4 and 86.6
Changes:
BLUEPRINT.md — added Renderer Setup subsection with WebGL2 config and terrain lookup texture specs; added reference to config.yaml keys for all budgets; deduplicated redundant skill descriptions and performance directives already implied by headers
config.yaml — added per-particle budget fields, variant-count caps, max_token_budget under new performance constraints section
Updated file contents below.
---
BLUEPRINT.md
3D Data Terrain Explorer
Domain: dashboard Version: 5.1.0
Purpose
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue = elevation, user density = vegetation color, error rates = red rivers, API calls = light trails along valleys. OrbitControls with time slider and camera bookmarks.
Persona
3D data visualization engineer and Three.js specialist.
Skills
Terrain: heightfield from time-series data via Three.js BufferGeometry
Color: secondary metrics to vertex colors (vegetation gradient, heat)
Rivers: error/anomaly paths as river geometry carving terrain
Particles: data flows as particle trails across landscape
Controls: OrbitControls with smooth damping, auto-rotation, camera bookmarks
Time: reshape terrain in real-time as user scrubs time
Output: interactive HTML 3D dashboard panel
Renderer Setup
WebGL2 renderer: antialias true, pixel ratio cap 2, toneMapping ACESFilmic, outputEncoding sRGB. Terrain lookup texture: 1024x1024 RGBA unsigned byte, updated per-frame via texSubImage2D on slider change — no full texture rebuild.
Performance
Frame budget: config.yaml performance.frame_budget_ms
Init budget: config.yaml performance.init_budget_ms
Particle vertex count: config.yaml performance.particle_vertex_count
Max draw calls: config.yaml performance.particle_draw_calls
Shader variant cap: config.yaml performance.max_shader_variants
Token budget: config.yaml performance.max_token_budget
Cache pre-built geometry variants and swap buffers (BufferAttribute.needsUpdate = true) instead of calling new THREE.XxxGeometry() per tick. Dispose old geometry and material references before creating new. Hard cap at 60 FPS via requestAnimationFrame delta gating. Offload particle position updates to vertex shader or reuse CPU-side Float32Array — no per-frame position object allocation with clamp + terrain lookups.
---
config.yaml
agent:
  max_iterations: 10
  retry_on_failure: true
  timeout_seconds: 300
  toolsets:
  - terminal
  - file
  - web
blueprint:
  dependencies: []
  domain: dashboard
  last_reviewed: '2026-06-28'
  name: 3d-data-terrain-explorer
  review_interval_days: 90
  schema_expectations: []
  priorities:
  - functionality
  - performance
  - polish
  version: 5.1.0
  version_history:
  - from: 1.0.0
    to: 2.0.0
    reason: 'MAJOR: quality gate passed (score=90.2)'
    score: 90.2
    previous_score: null
    timestamp: '2026-06-27T23:52:15Z'
  - from: 2.0.0
    to: 3.0.0
    reason: 'MAJOR: quality gate passed (score=87.2)'
    score: 87.2
    previous_score: 90.2
    timestamp: '2026-06-27T23:57:41Z'
  - from: 3.0.0
    to: 4.0.0
    reason: 'MAJOR: quality gate passed (score=87.4)'
    score: 87.4
    previous_score: 87.2
    timestamp: '2026-06-27T23:58:55Z'
  - from: 4.0.0
    to: 5.0.0
    reason: 'MAJOR: quality gate passed (score=86.6)'
    score: 86.6
    previous_score: 87.4
    timestamp: '2026-06-28T00:00:20Z'
  - from: 5.0.0
    to: 5.1.0
    reason: 'MINOR: added renderer setup, terrain texture, per-particle budgets, dedup'
    score: null
    previous_score: 86.6
    timestamp: '2026-06-28T02:00:27Z'
eval:
  benchmarks: []
  judge_model: deepseek-v4-pro
  min_pass_score: 70
performance:
  frame_budget_ms: 8
  init_budget_ms: 200
  particle_vertex_count: 64
  particle_draw_calls: 1
  max_shader_variants: 4
  max_token_budget: 280
hardware_profiles:
  pontus-main:
    eval_model: deepseek-v4-pro
    max_tokens: 8192
    model: deepseek-v4-flash
    provider: deepseek
    temperature: 0.3