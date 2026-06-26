The current state is clear. Here is the full analysis:
---
BUNDLE AUDIT: D:\styde\_alpedal\styde-forge\Dashboard\web
---
current setup
build: tsc only. No bundler. 381 lines of inline JS inside mission_control_8765.html.
deployment: Python HTTPServer (server_8765.py) serves the HTML file verbatim.
src/ contains a TypeScript refactor with 4 modules:
  main.ts (entry, 69 lines) — fetchState, keyboard handlers, dynamic imports
  render.ts (277 lines) — DOM rendering, SVG gauges, smart-diff
  api.ts (146 lines) — fetch wrappers, skill modal, controls
  state.ts (84 lines) — types + state variables
tsc compiles these to dist/ individually (5 .js + .js.map pairs).
The HTML does NOT load them — it runs the old inline JS instead.
---
problems found
problem 1: zero bundling
Each tsc output file is a separate HTTP request. No minification, no tree shaking, no scope hoisting. The inline JS in the HTML is one giant 22KB blob with no module boundaries.
problem 2: dead TS pipeline
The TypeScript refactor compiled on every `npm run build` but never reaches the browser. 576 lines of TS produce zero runtime benefit.
problem 3: no code splitting
main.ts already uses `import()` for lazy loading (api.ts module, state.ts on timeout). But with tsc these are separate network requests. No bundler to optimize chunk boundaries.
problem 4: no analysis tooling
No `rollup-plugin-visualizer`, no `vite-bundle-visualizer`, no `webpack-bundle-analyzer`. Impossible to measure bundle sizes.
problem 5: no production optimizations
- tsc doesn't remove dead code
- tsc doesn't minify
- tsc doesn't inline constants
- tsc doesn't compress CSS (300+ lines inline in HTML)
- CSS lives inside HTML <style>, can't be code-split
---
recommendations
1. ADD VITE AS BUNDLER (highest impact)
   `npm install -D vite @rollup/plugin-visualizer rollup-plugin-visualizer`
   vite.config.ts:
   ```
   import { defineConfig } from "vite";
   import { visualizer } from "rollup-plugin-visualizer";
   export default defineConfig({
     build: {
       outDir: "dist",
       sourcemap: false,
       minify: "esbuild",
       rollupOptions: {
         output: {
           manualChunks: {
             render: ["./src/render.ts"],
             api: ["./src/api.ts"],
             state: ["./src/state.ts"],
           },
         },
       },
     },
     plugins: [
       visualizer({
         filename: "dist/bundle-analysis.html",
         open: true,
         gzipSize: true,
       }),
     ],
   });
   ```
2. CREATE index.html AS VITE ENTRY
   Copy mission_control_8765.html -> index.html.
   Replace the inline <script> block with:
   `<script type="module" src="./src/main.ts"></script>`
   This connects the TS modules to the page.
3. UPDATE package.json SCRIPTS
   ```
   "scripts": {
     "dev": "vite",
     "build": "vite build",
     "preview": "vite preview",
     "analyze": "vite build && start dist/bundle-analysis.html",
     "clean": "rm -rf dist"
   }
   ```
4. ALIGN server_8765.py
   In dev: `python server_8765.py` serves API on :8765, Vite dev server on :5173 proxies /api to :8765.
   In prod: the Python server serves the Vite-built dist/index.html + assets.
5. EXTRACT CSS
   Move the 300+ lines from index.html <style> to src/style.css.
   Import in main.ts: `import "./style.css"`.
   Vite extracts and minifies it automatically.
---
estimated impact
metric                     before            after
JS payload                22KB inline       ~4KB gzipped bundled
HTTP requests per load    1 (inline)       1 (bundled) + 2-3 chunks
tree shaking              none              esbuild removes unused exports
minification              none              esbuild minify (50-60% reduction)
code splitting            none              3 modules auto-split
bundle analysis           none              visualizer HTML report
CSS size                  ~10KB inline      ~5KB minified extracted
---
recommended build command
npm install -D vite @rollup/plugin-visualizer
npx vite build
Then open dist/bundle-analysis.html to see the chunk sizes visualized.