Nu har jag hela bilden. Här är analysen.
bundle_analysis:
  project: styde-forge/Dashboard/web
  breakdown:
    mission_control_8765.html:
      total: 43651 bytes
      inline_css: 18246 bytes (41.8%)
      inline_js: 19983 bytes (45.8%)
      html_markup: 5422 bytes (12.4%)
    timeline.html:
      total: 75235 bytes
      inline_css: 4781 bytes (6.4%)
      inline_js: 68406 bytes (90.9%)
      html_markup: 2048 bytes (2.7%)
    dist/:
      compiled_js: 20384 bytes (not served)
      source_maps: 19094 bytes (not served)
findings:
  - id: F01
    severity: high
    title: No bundler — raw tsc outputs 4 separate files, none served
    evidence: build script is `tsc -p tsconfig.json`, server has no /dist/ route
    impact: 20KB compiled JS + 19KB source maps = 38KB dead weight on disk
  - id: F02
    severity: high
    title: Inline-only deployment blocks caching
    evidence: server reads mission_control_8765.html as raw bytes, serves text/html. Every page load re-downloads all 43KB JS+CSS.
    impact: zero cache hit rate on JS/CSS. Browser can't cache inline content separately from HTML.
  - id: F03
    severity: medium
    title: Dual codebases — TS refactor compiled but unused
    evidence: src/main.ts, api.ts, render.ts, state.ts (v5 refactor) compile to dist/ but the HTML runs a separate inline JS version. The inline JS appears to be an older generation.
    impact: maintenance burden, bug fixes must be applied in two places, TS types unused in production
  - id: F04
    severity: medium
    title: No minification
    evidence: tsconfig has `removeComments: false`, no Terser/uglify in pipeline. Bytes saved: uncompressed ~20KB JS → minified ~11KB estimated
    impact: 45%+ size reduction left on table for zero config time
  - id: F05
    severity: low
    title: Shared code duplicated across HTML files
    evidence: both mission_control_8765.html (44KB) and timeline.html (75KB) have inline JS. Utilities like GPU gauge rendering, color helpers, API fetch logic appear in both independently.
    impact: no shared module, no tree shaking, each file carries its own copy of infrastructure code
  - id: F06
    severity: low
    title: Source maps shipped but unused
    evidence: dist/ contains 19KB .map files (95% of JS size). Not served, not referenced. No debugging benefit.
    impact: wasted disk space, risk of accidental serving in production
recommendations:
  - priority: 1
    action: Add Vite with TypeScript plugin
    details: replace tsc build with vite build. Vite handles TS transpilation, bundling, minification (esbuild for dev, Rollup+Terser for prod), and HMR for dev.
    files_to_change:
      - Dashboard/web/package.json: add vite, @vitejs/plugin-typescript
      - Dashboard/web/vite.config.ts: new file
      - Dashboard/web/tsconfig.json: add vite reference types
    expected_savings:
      js_bundle: 20KB → ~8KB (minified + tree-shaken)
      source_maps: 19KB → 0KB (disabled in prod)
      total_served: 44KB → ~30KB (if CSS stays inline) or ~14KB JS + 18KB CSS (externalized)
  - priority: 2
    action: Externalize CSS to separate file
    details: move 18KB inline CSS to styles.css. Server serves with Cache-Control: max-age=86400. HTML drops 18KB.
    files_to_change:
      - Dashboard/web/src/styles.css: new file (extract inline styles)
      - Dashboard/web/mission_control_8765.html: remove <style> block, add <link>
    expected_savings: first load 44KB, repeat load 26KB (18KB CSS cached)
  - priority: 3
    action: Serve JS as external modules via Vite output
    details: configure Vite to emit hashed chunk filenames. Server adds /dist/* static file route with Cache-Control headers. HTML loads <script type="module" src="/dist/assets/index.abc123.js">.
    files_to_change:
      - Dashboard/web/server_8765.py: add static file handler for /dist/
      - Dashboard/web/mission_control_8765.html: replace inline <script> with module script src
    expected_savings: repeat load for JS drops to zero (immutable cache), HTML shrinks from 44KB to permanent ~6KB
  - priority: 4
    action: Implement route-based code splitting
    details: timeline.html becomes a separate route in the Vite app. Shared code (GPU gauges, color helpers, API layer) goes into common chunk loaded once. Each page chunk loads its unique code.
    files_to_change:
      - Dashboard/web/src/: add router.ts, split timeline-specific renderers
      - Dashboard/web/timeline.html: replace with Vite entry or remove (serve from SPA)
    expected_savings: shared JS across pages loads once instead of twice
verification:
  - after each change, run: npx vite build and confirm output size reduction
  - check: dist/ contains only .js, no .map
  - check: server_8765.py serves /dist/* correctly
  - check: mission_control page loads and all features work (API calls, GPU gauges, activity feed, skill modal)
  - check: timeline page loads and timeline renders correctly
next_action: apply priority 1 — add Vite to Dashboard/web