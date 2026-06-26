PERFORMANCE AUDIT: Styde Forge
---
1. state.yaml — CRITICAL BOTTLENECK
106KB YAML parsed fresh on every dashboard poll. 3565 lines loaded into memory then sliced to last 50.
state.yaml contains every agent, evaluation, improvement since genesis. No tail-only fast path. YAML is the slowest serialization format available — Python's yaml.safe_load takes 40-80ms on a file this size, blocking the single-threaded HTTPServer.
Fix: maintain a separate small stats cache file (stats.json, 2KB) updated only when state changes. Send that to the dashboard. Full state.yaml only on explicit request. Or use the already-existing smart_cache.py SQLite for index queries instead of parsing YAML.
2. /api/state NO COMPRESSION — WASTES BANDWIDTH
150KB JSON payload sent uncompressed every poll (1-5s interval). Python http.server has no gzip. Tauri/Vite deployment has no CDN or reverse proxy.
Fix: add gzip via gzip module to do_GET. Reduces payload to 15-25KB. Or run behind nginx/Cloudflare.
3. nvidia-smi SUBPROCESS ON EVERY REQUEST
server_8765.py get_hardware() spawns nvidia-smi subprocess (200-300ms) plus psutil.cpu_percent(interval=0.5) on every /api/state call. The 0.5s interval alone doubles response time.
Fix: cache hardware metrics with 5-10s TTL. Move psutil.cpu_percent to 0.1s interval or use /proc/stat directly.
4. DASHBOARD IS A 35KB MONOLITHIC HTML FILE
mission-control.html has all CSS inline, all JS inline. No code splitting. No lazy loading of panels. The Agent, Benchmark, Chat panels all render simultaneously even when tabs hide them.
Fix: split panels into lazy modules. Import on tab switch. Defer Chat panel — it loads highlight.js + marked on page start but user may never use chat.
5. VITE CONFIG IS STUB
vite.config.ts has zero build optimization. No rollupOptions, no manualChunks, no minify config, no CSS code splitting. The Tauri src/main.ts is 1 line placeholder — the real dashboard bypasses Vite entirely.
Fix: wire the dashboard through Vite build pipeline. Enable rollupOptions.output.manualChunks to split vendor (marked, highlight.js) from app code.
6. SINGLE-THREADED HTTP BLOCKING
HTTPServer (threadingless) serves one request at a time. YAML parse + nvidia-smi + psutil all block the same thread. One slow request delays all others.
Fix: switch to ThreadingHTTPServer or aiohttp. Or at minimum move YAML parse to background thread with cached result.
7. SMART CACHE EXISTS BUT UNUSED BY DASHBOARD
Core/smart_cache.py has a full SQLite cache with WAL mode, TTL, blueprint-aware invalidation. It's not wired into the dashboard server at all. The YAML re-parse on every request is completely unnecessary with this available.
8. NO CDN FOR STATIC ASSETS
mission-control.html has no content-hashed URLs, no CDN, no cache headers for the dashboard HTML itself (Cache-Control: no-cache on the HTML too). Every reload fetches the same 35KB.
Scores by area:
LCP (state.yaml loading): FAIL - 106KB YAML parsed per request, 80-200ms blocking
INP (dashboard interactivity): FAIL - no lazy rendering, all panels active
Bundle (dashboard size): FAIL - 35KB monolithic, no code splitting, gzip disabled
Caching: FAIL - no-cache on everything, smart_cache.py sits unused
Data Efficiency: FAIL - loads full history, uses last 50 items
Priority fixes (in order):
1. Replace full YAML parse with incremental stats cache
2. Add gzip compression to dashboard server
3. Cache hardware metrics with 10s TTL
4. Wire smart_cache into dashboard endpoint
5. Split monolithic HTML into lazy-loaded panels