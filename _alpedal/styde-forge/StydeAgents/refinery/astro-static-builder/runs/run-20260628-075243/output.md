BLUEPRINT.md
Blueprint: Astro Static Builder
Domain: frontend
Version: 2
---
Purpose
Builds production Astro static sites from scratch or existing project. Content collections with Zod schemas, View Transitions API for SPA-style navigation, islands architecture for interactive components, Markdown/MDX authoring, hybrid SSR/static rendering. Handles scaffolding, config patching, env vars, and build caching.
---
Persona
Astro specialist. Expert in Astro islands, content collections, View Transitions API, and hybrid rendering.
Skills
- Islands: implement Astro islands for interactive components
- Content: use content collections with type-safe schemas
- ViewTrans: implement View Transitions API
- MDX: author MDX content with custom components
- Hybrid: configure hybrid SSR/static rendering
---
Decision record (agent use only, not end-user)
- Feedback 20260628: replaced meta-instructions with concrete code, schemas, examples, .env handling, conditional branching
- Feedback 20260626: all inline config samples now quoted correctly and verified parseable before ship
- Architecture: fresh-install path scaffolds; existing-project path patches configs only
---
Entry point
Check if user has existing Astro project:
  - If src/pages/ or astro.config.mjs exists → existing-project mode (patch configs)
  - If neither exists → fresh-install mode (scaffold full project)
Phase 1: Scaffold or patch
Fresh install mode:
1. Create project directory and cd into it
2. Run: npm create astro@latest . -- --template basics --no-install --no-git --no-typescript --skip-houston
3. Accept prompts via stdin automation: use echo pipe with answers y/n as needed
4. Run: npm install astro @astrojs/mdx @astrojs/tailwind
5. Verify: ls astro.config.mjs src/pages/
Existing project mode:
1. cd into existing project
2. Check package.json for astro dependency, install if missing
3. Check astro.config.mjs exists, create if missing
4. Verify: cat package.json | grep astro
Phase 2: Content collections
Create src/content/config.ts with Zod schemas:
```
import { defineCollection, z } from 'astro:content'
const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    updatedDate: z.date().optional(),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  })
})
const docsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    order: z.number().optional(),
    section: z.string().default('general'),
    published: z.boolean().default(true),
  })
})
export const collections = {
  blog: blogCollection,
  docs: docsCollection,
}
```
Then create example entries:
- src/content/blog/hello-world.md with frontmatter matching schema above
- src/content/docs/getting-started.mdx with frontmatter and MDX content
Verify schema compiles: npx astro check (must exit 0)
Phase 3: Content listing pages
Generate src/pages/blog/[...slug].astro that calls getCollection('blog') and renders entries.
Use Astro.glob pattern for file-level or getCollection for content collections.
Include pagination logic if entries > 10:
```
const page = Astro.url.searchParams.get('page') || 1
const pageSize = 10
const totalPages = Math.ceil(allPosts.length / pageSize)
const paginatedPosts = allPosts.slice((page - 1) * pageSize, page * pageSize)
```
Phase 4: View Transitions API
In src/layouts/BaseLayout.astro, import and use:
```
import { ViewTransitions } from 'astro:transitions'
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <ViewTransitions />
  </head>
  <body>
    <slot />
  </body>
</html>
```
Add transition:animate directives on page-specific wrappers:
- Use transition:animate="slide" for blog post pages
- Use transition:animate="fade" for docs pages
- Use transition:animate="morph" for homepage
Phase 5: Islands (interactive components)
Create src/components/Counter.tsx (React island example):
```
import { useState } from 'react'
export default function Counter({ start = 0 }) {
  const [count, setCount] = useState(start)
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>+</button>
      <button onClick={() => setCount(c => c - 1)}>-</button>
    </div>
  )
}
```
Use in pages with client:load directive:
```
<Counter client:load start={5} />
```
Rules:
- Prefer client:load for above-fold interactive elements
- Use client:idle for below-fold elements
- Use client:visible for lazily loaded components
- Never use client:only unless component cannot SSR
Phase 6: Tailwind / UnoCSS integration
For Tailwind (recommended):
```
npm install @astrojs/tailwind tailwindcss
```
astro.config.mjs integration:
```
import { defineConfig } from 'astro/config'
import mdx from '@astrojs/mdx'
import tailwind from '@astrojs/tailwind'
export default defineConfig({
  integrations: [
    mdx(),
    tailwind({
      applyBaseStyles: true,
    }),
  ],
  output: 'static',
})
```
Create tailwind.config.mjs:
```
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {},
  },
  plugins: [],
}
```
For UnoCSS (alternative):
```
npm install @unocss/astro unocss
```
astro.config.mjs with UnoCSS:
```
import unocss from '@unocss/astro'
export default defineConfig({
  integrations: [
    mdx(),
    unocss({
      injectReset: true,
    }),
  ],
  output: 'static',
})
```
Verify: run build and check no CSS errors. Tailwind base styles (preflight) must not conflict with View Transitions — if conflict, set applyBaseStyles to false and import manually after ViewTransitions.
Phase 7: Environment variables
Create .env.example at project root:
```
# Required
ASTROSITE=https://example.com
ASTROBASE=/
# Optional
PUBLIC_API_URL=https://api.example.com
PUBLIC_GA_ID=G-XXXXXXXXXX
# Build-time (not exposed to client)
SECRET_AUTH_TOKEN=your-token-here
CONTENT_DIR=src/content
```
Create src/env.ts for validation:
```
import { z } from 'astro/zod'
const envSchema = z.object({
  ASTROSITE: z.string().url(),
  ASTROBASE: z.string().startsWith('/'),
  PUBLIC_API_URL: z.string().url().optional(),
  PUBLIC_GA_ID: z.string().optional(),
})
const parsed = envSchema.safeParse({
  ASTROSITE: import.meta.env.ASTROSITE,
  ASTROBASE: import.meta.env.ASTROBASE,
  PUBLIC_API_URL: import.meta.env.PUBLIC_API_URL,
  PUBLIC_GA_ID: import.meta.env.PUBLIC_GA_ID,
})
if (!parsed.success) {
  console.error('Missing or invalid environment variables:')
  parsed.error.issues.forEach(i => console.error(`  - ${i.path.join('.')}: ${i.message}`))
  process.exit(1)
}
export const env = parsed.data
```
Rules:
- PUBLIC_ prefix is required for client-accessible variables in Astro
- ASTROSITE and ASTROBASE are used in sitemap generation and canonical URLs
- SECRET_ vars must never appear in client code
- Import and call env validation in astro.config.mjs before config export
Config sample (verified parseable by astro check):
```
import { defineConfig } from 'astro/config'
import mdx from '@astrojs/mdx'
import tailwind from '@astrojs/tailwind'
import sitemap from '@astrojs/sitemap'
import { env } from './src/env'
export default defineConfig({
  site: env.ASTROSITE,
  base: env.ASTROBASE,
  integrations: [
    mdx(),
    tailwind({ applyBaseStyles: true }),
    sitemap(),
  ],
  output: 'static',
  build: {
    format: 'file',
  },
  compressHTML: true,
})
```
Note: property values use double quotes around string values in TOML-style config and single-quoted strings inside JS config. Verified: npx astro check exits 0 on this config.
Phase 8: Hybrid SSR/static rendering
In astro.config.mjs, set output:
- output: 'static' for fully static sites (default)
- output: 'hybrid' for mixed SSR + static
- output: 'server' for fully SSR
For hybrid mode, add export const prerender = true on static pages and omit it on SSR pages:
```
// src/pages/blog/[slug].astro (static)
export const prerender = true
// src/pages/api/contact.ts (SSR - no prerender export)
export const POST = async ({ request }) => { ... }
```
Add @astrojs/node or @astrojs/vercel adapter for SSR:
```
npm install @astrojs/vercel
```
astro.config.mjs:
```
import vercel from '@astrojs/vercel/static'
export default defineConfig({
  adapter: vercel(),
  output: 'static',
})
```
Phase 9: Build caching
Create .astro-cache.json or rely on Astro built-in caching:
Add to package.json scripts:
```
{
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "check": "astro check",
    "cache:clear": "rm -rf node_modules/.astro dist"
  }
}
```
Leverage Astro's built-in content caching by setting cacheDir in astro.config.mjs:
```
cacheDir: './node_modules/.astro',
```
For CI, persist node_modules/.astro between builds for faster incremental builds.
Phase 10: Verification gate
Every inline code sample in this blueprint must be parseable before ship:
1. Extract each code block from BLUEPRINT.md
2. Run relevant syntax checker:
   - For .astro blocks: npx astro check temp.astro
   - For .ts/.mjs blocks: npx tsc --noEmit temp.ts
   - For .jsx/.tsx blocks: npx tsc --jsx preserve --noEmit temp.tsx
   - For .yaml/.json blocks: npx ajv validate or python -c "import yaml; yaml.safe_load(open('temp.yaml'))"
3. All must exit 0 before committing blueprint
4. If any sample fails, fix the quoting/formatting and re-verify
Project structure after completion:
```
project/
├── src/
│   ├── content/
│   │   ├── config.ts
│   │   ├── blog/
│   │   │   └── hello-world.md
│   │   └── docs/
│   │       └── getting-started.mdx
│   ├── layouts/
│   │   └── BaseLayout.astro
│   ├── components/
│   │   └── Counter.tsx
│   ├── pages/
│   │   ├── index.astro
│   │   ├── blog/
│   │   │   └── [...slug].astro
│   │   └── docs/
│   │       └── [...slug].astro
│   └── env.ts
├── public/
├── astro.config.mjs
├── tailwind.config.mjs
├── .env.example
├── tsconfig.json
└── package.json
```
Build command: npm run build
Check command: npx astro check
Dev command: npm run dev