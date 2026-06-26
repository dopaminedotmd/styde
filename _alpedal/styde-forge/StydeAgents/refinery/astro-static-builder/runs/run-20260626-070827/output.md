Blueprint: Astro Static Builder
Domain: frontend
Version: 2
Purpose
Builds production-grade Astro static sites with content collections, View Transitions, islands architecture, and MDX. Targets 85+ evaluation score.
Persona
Astro specialist. Expert in Astro 5 islands, Content Collections, View Transitions API, hybrid rendering, and build optimisation.
Skills
  Islands: implement Astro islands for interactive components using client:* directives
  Content: use Content Collections with Zod schemas and type-safe queries
  ViewTrans: implement View Transitions API with named transitions and fallbacks
  MDX: author MDX content with custom components and layouts
  Hybrid: configure hybrid SSR/static rendering per route
  BuildOpt: configure build caching, incremental builds, and TypeScript strict mode
  Assets: use Astro built-in image service and getImage() for optimised assets
  Styling: integrate Tailwind CSS or unoCSS via Astro integrations
Architecture
Project layout:
  src/
    content/
      blog/         -- Content collection with schema validation
      projects/     -- Second collection, cross-referenced via slug
    layouts/
      base.astro    -- HTML shell, View Transitions, global styles
      markdown.astro -- Content layout with prose styling
    pages/
      index.astro   -- Landing page, statically generated
      blog/[...slug].astro -- Dynamic routes from content
      projects/[...slug].astro
    components/
      island/       -- Interactive components with client:load, client:idle, client:visible
      ui/           -- Pure presentational (no client directive)
      mdx/          -- Custom MDX component overrides
    lib/
      collections.ts -- Collection access helpers with error boundaries
      images.ts     -- Image optimisation using Astro built-in API
    styles/
      global.css    -- Tailwind base or unoCSS layers
    env.d.ts       -- TypeScript ambient declarations
  public/           -- Static assets, robots.txt, favicon
  astro.config.ts   -- Astro configuration
  tsconfig.json     -- Strict-mode TypeScript config
  tailwind.config.ts -- (if Tailwind) or unocss.config.ts
Content Collections
Define in src/content/config.ts using Zod:
  import { defineCollection, z } from 'astro:content'
  const blogCollection = defineCollection({
    type: 'content',
    schema: z.object({
      title: z.string(),
      pubDate: z.date(),
      description: z.string(),
      author: z.string().default('Team'),
      image: z.object({ url: z.string(), alt: z.string() }).optional(),
      tags: z.array(z.string()).default([]),
      draft: z.boolean().default(false),
    }),
  })
  export const collections = { blog: blogCollection }
Query with type-safe helpers in src/lib/collections.ts -- use getCollection('blog') and filter with array methods. Wrap in try/catch. Re-export a getPosts() that returns sorted, non-draft posts.
Asset Handling (replacing deprecated @astrojs/image)
Use Astro 5 built-in image service exclusively. Do NOT install @astrojs/image -- it is deprecated.
For optimised images in templates:
  import { Image, Picture } from 'astro:assets'
  import heroImage from '../images/hero.png'
  <Image src={heroImage} alt="Hero" width={1200} height={630} format="webp" />
For remote images:
  import { getImage } from 'astro:assets'
  const optimised = await getImage({ src: 'https://example.com/photo.jpg', width: 800 })
For responsive picture sets with art direction, use the <Picture> component with sources array.
Store source images in src/images/ (not public/) so Astro processes them. Public/ is for unprocessed files (robots.txt, PDFs, etc.).
Styling Integration (Tailwind or unoCSS)
Add via Astro integration, not manual PostCSS setup.
Tailwind (option A):
  npx astro add tailwind
  Configure in tailwind.config.ts with content paths pointing to src/
  Use @tailwind base/components/utilities in src/styles/global.css
unoCSS (option B):
  npx astro add unocss
  Configure in unocss.config.ts with presets (presetUno, presetIcons, presetAttributify)
  Use @unocss directives in global CSS
Do NOT use both in the same project. Pick one based on team preference -- Tailwind for ecosystem familiarity, unoCSS for faster HMR and atomic CSS flexibility.
View Transitions API
Enable globally in src/layouts/base.astro:
  import { ViewTransitions } from 'astro:transitions'
  <html>
    <head>
      <ViewTransitions />
    </head>
    <body>
      <slot />
    </body>
  </html>
Use named transitions on elements that persist across routes:
  <nav transition:name="nav">...</nav>
For custom animations, use transition:animate with CSS:
  <main transition:animate="slide">...</main>
Fallback: if the ViewTransitions script does not load (rare), pages render fully without animation -- no content loss.
MDX Content Authoring
Install: npx astro add mdx
Place .mdx files in src/content/blog/ with frontmatter matching the collection schema.
Custom MDX components defined in src/components/mdx/ and wired in astro.config.ts:
  import { defineConfig } from 'astro/config'
  import mdx from '@astrojs/mdx'
  export default defineConfig({
    integrations: [mdx({
      customComponentImports: ['./src/components/mdx/index.ts'],
    })],
  })
The mdx/index.ts re-exports all custom components (CodeBlock, Note, Figure, Video, etc.).
Hybrid Rendering
In astro.config.ts:
  import { defineConfig } from 'astro/config'
  export default defineConfig({
    output: 'hybrid',
    adapter: ... // only if SSR routes needed
  })
Mark routes in src/pages/ with export const prerender = false for SSR, or true (default for hybrid mode) for static.
For fully static sites (no server routes), output: 'static' is the correct choice -- do NOT add an adapter.
Build and Deployment
  astro.config.ts caching optimisations:
  export default defineConfig({
    vite: {
      cacheDir: 'node_modules/.vite',               // default, explicit for clarity
      build: {
        rollupOptions: {
          output: {
            manualChunks: (id) => id.includes('node_modules') ? 'vendor' : undefined,
          },
        },
        target: 'esnext',                           // modern browsers only
      },
    },
    build: {
      inlineStylesheets: 'auto',                    // inline small CSS for fewer requests
    },
  })
  Turbo build with pre-bundled cache:
  ASTRO_TELEMETRY_DISABLED=1 astro build         # disable telemetry during CI
  Use --preserve-output for incremental builds:
  astro build --preserve-output                    # keep existing dist/ assets
  For monorepos, add to package.json scripts:
    "build": "astro build && astro check",
    "build:cached": "astro build --preserve-output",
    "check": "astro check"
  CI pipeline recommendation:
  - Cache node_modules/ and .astro/ between runs
  - Cache .vite/ (vite.cacheDir) for astro build
  - Run astro check before deploy to catch type/config errors
TypeScript Configuration
  tsconfig.json -- strict mode:
  {
    "extends": "astro/tsconfigs/strict",
    "compilerOptions": {
      "baseUrl": ".",
      "paths": {
        "@components/*": ["src/components/*"],
        "@layouts/*": ["src/layouts/*"],
        "@lib/*": ["src/lib/*"],
        "@assets/*": ["src/assets/*"]
      },
      "jsx": "preserve",
      "strictNullChecks": true,
      "noUncheckedIndexedAccess": true,
      "exactOptionalPropertyTypes": false
    },
    "include": ["src/**/*", "astro.config.ts"],
    "exclude": ["dist", "node_modules"]
  }
Syntax Verification Gate
Every code sample in this blueprint MUST pass astro check before release.
Process:
1. Extract all code blocks from this document into a temporary Astro project
2. Run `npx astro check` against that project
3. Fix any errors found (quoting, imports, config key names)
4. Only then mark the blueprint as ready for evaluation
Known syntax pitfalls:
- astro.config.ts property names are unquoted unless the value is a string with special chars
  CORRECT: site: 'https://example.com'
  CORRECT: vite: { cacheDir: 'node_modules/.vite' }
  INCORRECT: site: https://example.com
  INCORRECT: value: ${VAR}
  INCORRECT: value = "${VAR}"
- All string values must be quoted in JavaScript/TypeScript config files (single or double quotes)
- Zod schema keys are unquoted JS identifiers, not YAML keys
- Environment variable interpolation uses process.env.VAR, not ${VAR}
Deploy Targets
  Cloudflare Pages (recommended for static + edge):
  - npx astro add @astrojs/cloudflare
  - output: 'hybrid' or 'static'
  - Build command: astro build
  - Output directory: dist/
  Netlify (simplest for static):
  - npx astro add @astrojs/netlify
  - No config needed for static output
  GitHub Pages:
  - npx astro add @astrojs/node  (or no adapter for static-only)
  - Set base in astro.config.ts to match repo name
  - Use GitHub Actions to deploy
  Vercel:
  - npx astro add @astrojs/vercel
  - output: 'static' for pure static, 'hybrid' for serverless
Package.json minimum
  {
    "name": "astro-static-site",
    "type": "module",
    "version": "1.0.0",
    "scripts": {
      "dev": "astro dev",
      "build": "astro build && astro check",
      "preview": "astro preview",
      "check": "astro check",
      "lint": "eslint src/",
      "typecheck": "tsc --noEmit"
    },
    "dependencies": {
      "astro": "^5.0.0",
      "@astrojs/mdx": "^4.0.0",
      "@astrojs/tailwind": "^6.0.0"
    },
    "devDependencies": {
      "@astrojs/check": "^0.9.0",
      "typescript": "^5.6.0"
    }
  }
Do NOT include @astrojs/image -- use Astro built-in image service. Add @astrojs/unocss if choosing unoCSS over Tailwind.
Evaluation checklist (score target: 85+)
  Islands: each interactive component uses correct client:* directive
  Content: every content collection has a Zod schema; query helpers are type-safe
  ViewTrans: ViewTransitions component present in base layout
  MDX: MDX configured with custom component imports
  Hybrid: output mode explicitly set (static or hybrid)
  Assets: no @astrojs/image dependency; uses astro:assets Image/getImage
  Styling: Tailwind or unoCSS via integration, not manual PostCSS
  BuildCache: vite.cacheDir explicit, rollup manualChunks set, --preserve-output available
  TSconfig: strict mode enabled, path aliases configured
  VerifyGate: every code sample has been astro check verified
  ConfigSyntax: all config samples use correct quoting and no shell-style interpolation