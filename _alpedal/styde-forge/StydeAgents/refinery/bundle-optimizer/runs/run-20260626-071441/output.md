Bundle analysis for D:\styde\_alpedal\styde-forge\Dashboard\web
Baseline:
- Build tool: tsc only (no bundler)
- HTML delivery: single 46KB monolithic file with ~370 lines inline CSS + ~400 lines inline JS
- Fonts: external Google Fonts (Geist/Geist Mono) — render-blocking
- dist/ output: 4 separate ES module files + 4 source maps (27KB total, never loaded by HTML)
- Build config: sourceMap: true, removeComments: false, no minification
Findings:
1. Zero bundler usage
   The TypeScript src/*.ts files compile individually through tsc and produce independent ES modules. No bundler stitches them together. No tree shaking. No code splitting. No minification.
2. Dead TypeScript code
   The inline <script> block in mission_control_8765.html is the actual runtime — it's a ~400-line vanilla JS sphere with its own particle system, cascade rendering, gauge SVGs, keyboard handlers, API functions, and boot logic. The compiled TypeScript in dist/ is never loaded by any HTML page.
3. Inlined CSS cannot cache
   Every page load re-downlods the full ~370-line CSS block. Any CSS change invalidates the entire HTML cache.
4. Google Fonts is render-blocking
   The <link href=...> to fonts.googleapis.com blocks painting until the external CSS and font files load.
5. Source maps shipped to dist/
   19KB of .js.map files alongside 8KB of JS output. Minor since dist/ isn't served.
6. Timeline page replicate the pattern
   timeline.html is 75KB with its own full inline CSS + JS — same structural issue.
Effort estimates and expected score deltas:
dimension: efficiency | baseline: 0/100 (no bundler at all) | delta: +85
  effort: 90 min
  Vite setup with CSS/JS extraction, HTML shell, production build config
dimension: maintainability | baseline: 40/100 | delta: +40
  effort: 15 min
  Remove inline script and CSS from HTML, wire up Vite entry point
dimension: network_performance | baseline: 50/100 | delta: +30
  effort: 10 min
  Self-host or preconnect fonts with font-display swap
dimension: bundle_size | baseline: 30/100 | delta: +50
  effort: 5 min
  Enable minification + removeComments + sourceMap:false (Vite defaults)
Total effort: ~120 min
Composite score projection: 40/100 → 86/100
Klar att genomföra? Det innebär:
1. Skapa vite.config.ts + byt ut package.json scripts
2. Flytta inline CSS till en egen .css-fil i src/
3. Bygg HTML-skalet för Vite (liten index.html med <script type=module src=/src/main.ts>)
4. Ta bort den 400-radiga inline-scriptsen (ersätt med TS-modulerna)
5. Lägg till preconnect + font-display: swap för Geist
6. Lägg till timeline.html i samma pipeline med lazy load
Första steget är 90 min om du vill köra på.