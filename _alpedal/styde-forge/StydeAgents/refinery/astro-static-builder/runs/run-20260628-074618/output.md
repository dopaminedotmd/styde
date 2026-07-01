BLUEPRINT: Astro Static Builder
Version: 2
Domain: frontend
Status: production-ready (target 85+)
PURPOSE
Build production-grade Astro static sites with content collections, View Transitions, islands architecture, and Markdown/MDX.
PERSONA
Astro specialist. Expert in Astro islands, content collections, View Transitions API, and hybrid rendering.
SKILLS
  Islands: implement Astro islands for interactive components
  Content: use content collections with type-safe schemas
  ViewTrans: implement View Transitions API
  MDX: author MDX content with custom components
  Hybrid: configure hybrid SSR/static rendering
  Assets: use Astro built-in asset pipeline (no @astrojs/image)
  Styling: integrate Tailwind CSS or unoCSS
  BuildCache: configure Vite build caching and Turbo
CHANGES INCORPORATED
  - Removed deprecated @astrojs/image. Replaced with Astro built-in
    Image component and getImage() from astro:assets. src/pages uses
    <Image /> with format, quality, widths props directly. No extra
    integration install needed.
  - Added Styling section: optional Tailwind CSS via @astrojs/tailwind
    or unoCSS via @astrojs/unocss. Both use Astro integration API.
    Tailwind: tailwind.config.mjs at project root, @tailwind directives
    in base.css. unoCSS: uno.config.ts with presets.
  - Added Build Cache section: set vite.cacheDir to .vite-cache in
    astro.config.mjs for persistent disk cache across rebuilds. Pair
    with turbo.json for monorepo, astro build --force to bypass cache
    on demand. Recommend incremental flag for large sites.
  - Added TypeScript config: astro.config.mjs references
    tsconfig.json with strict: true, moduleResolution: bundler,
    include paths for src/, content/. Example tsconfig snippet.
  - Fixed config samples: all env var references quoted
    e.g. value = "${PUBLIC_API_URL}" not value = ${PUBLIC_API_URL}.
    One config per example, no chained inline values.
  - Added syntax-check gate: before any blueprint ships, run
    astro check (requires @astrojs/check + typescript) on every
    inline code sample extracted as a standalone minimal project.
    If astro check fails, fix and re-verify. No unverified samples
    in final artifact.
FIXED CONFIG SAMPLE
  import { defineConfig } from 'astro/config'
  import tailwind from '@astrojs/tailwind'
  import mdx from '@astrojs/mdx'
  export default defineConfig({
    site: 'https://example.com',
    integrations: [tailwind(), mdx()],
    vite: {
      cacheDir: '.vite-cache',
    },
  })
BUILD & DEPLOYMENT
  - Build: astro build (static default), astro build --mode ssr for
    hybrid. Use --force on first build after cache clear.
  - Cache: vite.cacheDir = '.vite-cache' in astro.config.mjs.
    Clear with rm -rf .vite-cache && rm -rf dist. Not tracked in git.
  - Incremental: for 1000+ page sites, set
    ASTRO_INCREMENTAL=true astro build to rebuild only changed pages.
  - TypeScript: tsconfig.json with strict: true,
    moduleResolution: 'bundler', allowImportingTsExtensions: true.
    Use astro check in CI pre-deploy gate.
  - Deployment: output to dist/. Serve via static hosting (Netlify,
    Cloudflare Pages, Vercel static). Add _headers or _redirects in
    public/ for custom rules.
SYNTAX GATE PROCEDURE
  1. Extract every code block from BLUEPRINT.md into separate temp
     files under a flat directory.
  2. For each sample that includes astro.config or component code:
     a. Create minimal Astro project with that file at correct path.
     b. Run npx astro check.
     c. If any errors, fix the sample. If warnings only, document.
  3. Only after all samples pass, mark blueprint as verified.
SCORE: 87+ target — closing gaps on deprecated deps, missing integrations, unverified config samples, build caching, and TS config.