Blueprint: Astro Static Builder
Domain: frontend
Version: 3
---
Purpose
Builds production Astro static sites from scratch or existing project. Content collections with Zod schemas, View Transitions API for SPA-style navigation, islands architecture for interactive components, Markdown/MDX authoring, hybrid SSR/static rendering, image optimization, SEO canonical/sitemap, i18n routing, error boundaries. Handles scaffolding, config patching, env vars, lint tooling, and build caching.
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
- v3: added image optimization (Astro:<Image>/<Picture>), SEO (Head/canonical/sitemap), i18n routing, AstroErrorBoundary patterns, prettier+eslint-astro lint config, file-level verification gate replacing npx astro check
- v2 (20260628): replaced meta-instructions with concrete schemas, ViewTrans examples, island code, tailwind/unoCSS config, .env handling, conditional branching (fresh vs existing project)
- v1: initial skeleton scaffold with domain/skills/persona only
---
Entry point
Check if user has existing Astro project:
  - If src/pages/ or astro.config.mjs exists -> existing-project mode (patch configs only)
  - If neither exists -> fresh-install mode (scaffold full project)
Phase 1: Scaffold or patch
Fresh install mode:
1. Create project directory and cd into it
2. Run: npm create astro@latest . -- --template basics --no-install --no-git --no-typescript --skip-houston
3. Accept prompts via stdin automation: use echo pipe with answers y/n as needed
4. Run: npm install astro @astrojs/mdx @astrojs/tailwind @astrojs/sitemap @astrojs/image
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
Verify schema compiles: npx astro check src/content/config.ts (must exit 0)
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
<html lang='en'>
  <head>
    <meta charset='utf-8' />
    <meta name='viewport' content='width=device-width, initial-scale=1' />
    <ViewTransitions />
  </head>
  <body>
    <slot />
  </body>
</html>
```
Add transition:animate directives on page-specific wrappers:
- Use transition:animate='slide' for blog post pages
- Use transition:animate='fade' for docs pages
- Use transition:animate='morph' for homepage
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
Phase 7: Image optimization
Install:
```
npm install @astrojs/image
```
In astro.config.mjs:
```
import image from '@astrojs/image'
export default defineConfig({
  integrations: [
    image({
      serviceEntryPoint: '@astrojs/image/sharp',
      cacheDir: './node_modules/.astro/image',
    }),
  ],
})
```
Use the Astro <Image /> component for optimized images:
```
---
import { Image } from '@astrojs/image/components'
import hero from '../assets/hero.jpg'
---
<Image src={hero} alt='Hero image' width={1200} height={630} format='webp' />
```
Use <Picture /> for responsive images with multiple formats:
```
---
import { Picture } from '@astrojs/image/components'
import banner from '../assets/banner.png'
---
<Picture src={banner} widths={[400, 800, 1200]} sizes='(max-width: 800px) 100vw, 800px' formats={['avif', 'webp']} alt='Banner' />
```
Rules:
- Always specify explicit width and height to prevent CLS
- Prefer webp or avif format for modern browsers
- Use <Picture> for responsive breakpoints
- Place images in src/assets/ for build-time processing, public/ for passthrough
Phase 8: SEO / Sitemap
Install sitemap integration:
```
npm install @astrojs/sitemap
```
astro.config.mjs with sitemap:
```
import sitemap from '@astrojs/sitemap'
export default defineConfig({
  site: 'https://example.com',
  integrations: [sitemap()],
})
```
Create src/components/SEO.astro for per-page head management:
```
---
export interface Props {
  title: string
  description: string
  canonical?: string
  ogImage?: string
  ogType?: string
  noindex?: boolean
}
const { title, description, canonical, ogImage, ogType, noindex } = Astro.props
---
<title>{title}</title>
<meta name='description' content={description} />
<meta name='robots' content={noindex ? 'noindex, nofollow' : 'index, follow'} />
<link rel='canonical' href={canonical || Astro.url.href} />
<meta property='og:title' content={title} />
<meta property='og:description' content={description} />
<meta property='og:type' content={ogType || 'website'} />
<meta property='og:url' content={canonical || Astro.url.href} />
{ogImage && <meta property='og:image' content={ogImage} />}
```
Use in page layouts:
```
<SEO title='Home | My Site' description='Welcome to my Astro site' canonical='https://example.com/' ogImage='https://example.com/og.png' />
```
Rules:
- site config in astro.config.mjs is required for sitemap generation
- sitemap integration auto-generates /sitemap-index.xml from all routes
- Exclude draft or noindex pages by adding noindex prop to SEO component
Phase 9: i18n routing  
Create src/i18n/index.ts for locale utilities:
```
export const defaultLocale = 'en'
export const locales = ['en', 'sv', 'de'] as const
export type Locale = (typeof locales)[number]
export const labels: Record<Locale, string> = {
  en: 'English',
  sv: 'Svenska',
  de: 'Deutsch',
}
export function getLocaleFromUrl(url: URL): Locale {
  const seg = url.pathname.split('/')[1]
  return (locales as readonly string[]).includes(seg) ? (seg as Locale) : defaultLocale
}
```
Create src/layouts/I18nLayout.astro for locale-aware base layout:
```
---
import { ViewTransitions } from 'astro:transitions'
import { getLocaleFromUrl, locales, labels, defaultLocale } from '../i18n'
const locale = getLocaleFromUrl(Astro.url)
const altLocales = locales.filter(l => l !== locale)
---
<html lang={locale}>
  <head>
    <meta charset='utf-8' />
    <meta name='viewport' content='width=device-width, initial-scale=1' />
    <ViewTransitions />
    <link rel='alternate' hreflang='x-default' href={`/${defaultLocale}`} />
    {locales.map(l => (
      <link rel='alternate' hreflang={l} href={`/${l}${Astro.url.pathname.replace(/^\/[a-z]{2}/, '')}`} />
    ))}
  </head>
  <body>
    <nav>
      {locales.map(l => (
        <a href={l === defaultLocale ? '/' : `/${l}`} hreflang={l}>{labels[l]}</a>
      ))}
    </nav>
    <slot />
  </body>
</html>
```
Rules:
- Default locale URLs have no prefix; non-default locales get /sv/, /de/ prefixes
- Use hreflang and alternates for SEO on multilingual sites
- Content collections can use locale subdirectories: src/content/blog/en/, src/content/blog/sv/
Phase 10: Error boundaries
Create src/components/AstroErrorBoundary.astro to catch render errors gracefully:
```
---
export interface Props {
  fallbackTitle?: string
  fallbackMessage?: string
}
const { fallbackTitle = 'Something went wrong', fallbackMessage = 'An unexpected error occurred while rendering this section.' } = Astro.props
---
<div class='error-boundary' role='alert'>
  <h2>{fallbackTitle}</h2>
  <p>{fallbackMessage}</p>
  <slot name='actions'>
    <a href='/' class='error-link'>Return to home page</a>
  </slot>
</div>
<style>
  .error-boundary {
    padding: 2rem;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    background: #fff5f5;
    text-align: center;
  }
  .error-link {
    color: #3182ce;
    text-decoration: underline;
  }
</style>
```
Wrap island components in error boundaries within layout:
```
<AstroErrorBoundary>
  <Counter client:load start={5} />
</AstroErrorBoundary>
```
For SSR error pages, create src/pages/500.astro:
```
---
export const prerender = false
---
<BaseLayout>
  <main>
    <h1>500 — Server Error</h1>
    <p>An unexpected error occurred. Our team has been notified.</p>
    <a href='/'>Go home</a>
  </main>
</BaseLayout>
```
Rules:
- Error boundaries catch rendering errors in island components
- Always provide fallback UI so partial page content still renders
- For SSR: create 500.astro and 404.astro error pages
- Log errors to console in dev; use AstroError utility for structured error data
Phase 11: Environment variables
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
Full astro.config.mjs with env + sitemap + image + tailwind:
```
import { defineConfig } from 'astro/config'
import mdx from '@astrojs/mdx'
import tailwind from '@astrojs/tailwind'
import sitemap from '@astrojs/sitemap'
import image from '@astrojs/image'
import { env } from './src/env'
export default defineConfig({
  site: env.ASTROSITE,
  base: env.ASTROBASE,
  integrations: [
    mdx(),
    tailwind({ applyBaseStyles: true }),
    sitemap(),
    image({
      serviceEntryPoint: '@astrojs/image/sharp',
      cacheDir: './node_modules/.astro/image',
    }),
  ],
  output: 'static',
  build: {
    format: 'file',
  },
  compressHTML: true,
})
```
Phase 12: Lint and formatting config
Install tooling:
```
npm install -D prettier eslint eslint-plugin-astro @typescript-eslint/parser prettier-plugin-astro
```
Create .prettierrc:
```
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "all",
  "plugins": ["prettier-plugin-astro"],
  "overrides": [
    {
      "files": "*.astro",
      "options": {
        "parser": "astro"
      }
    }
  ]
}
```
Create eslint.config.mjs:
```
import pluginAstro from 'eslint-plugin-astro'
export default [
  ...pluginAstro.configs.recommended,
  {
    rules: {
      'astro/no-set-html-directive': 'error',
      'astro/no-unused-define-vars-in-style': 'warn',
      'quotes': ['error', 'single', { avoidEscape: true }],
      'semi': ['error', 'never'],
    },
  },
]
```
Add to package.json scripts:
```
"format": "prettier --write .",
"lint": "eslint src/ --ext .astro,.ts,.tsx,.js,.jsx,.mjs",
"lint:fix": "eslint src/ --ext .astro,.ts,.tsx,.js,.jsx,.mjs --fix"
```
Rules:
- Use single quotes consistently across all JS/TS/Astro files
- Prettier runs on save in editor; eslint in CI
- eslint-plugin-astro catches common Astro-specific issues (missing props, invalid directives)
- Ignore .astro in prettier-trailing-comma (Astro parser doesn't support it)
Phase 13: Hybrid SSR/static rendering
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
Phase 14: Build caching
Create .astro-cache.json or rely on Astro built-in caching:
Add to package.json scripts:
```
{
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "check": "astro check",
    "cache:clear": "rm -rf node_modules/.astro dist",
    "format": "prettier --write .",
    "lint": "eslint src/ --ext .astro,.ts,.tsx,.js,.jsx,.mjs"
  }
}
```
Leverage Astro's built-in content caching by setting cacheDir in astro.config.mjs:
```
cacheDir: './node_modules/.astro',
```
For CI, persist node_modules/.astro between builds for faster incremental builds.
Phase 15: Verification gate  
Every inline code sample in this blueprint must be parseable before ship.
Do NOT use npx astro check (requires full project setup, not single-file validation).
Use file-level checks instead:
1. Extract each code block from BLUEPRINT.md
2. Run relevant syntax checkers on individual files:
   - For .astro blocks: eslint with eslint-plugin-astro (eslint --no-eslintrc --config eslint-verify.config.mjs --ext .astro temp.astro)
   - For .ts/.mjs blocks: npx tsc --noEmit --strict --esModuleInterop temp.ts 2>/dev/null
   - For .jsx/.tsx blocks: npx tsc --jsx react-jsx --noEmit --strict temp.tsx 2>/dev/null
   - For .yaml/.json blocks: python3 -c 'import yaml, sys; yaml.safe_load(open(sys.argv[1]))' temp.yaml
   - For Markdown/MDX frontmatter: npx tsx -e 'import { z } from "zod"; z.object({title: z.string()}).parse({title: "test"})'
3. All must exit 0 before committing blueprint
4. If any sample fails, fix quoting/formatting and re-verify
5. Manual checklist for code samples:
   [ ] All Astro template expressions have matching braces
   [ ] All import paths reference real packages
   [ ] All JSX/TSX components close properly
   [ ] All Zod schema fields use correct types
   [ ] All config objects use valid Astro/MDX/Tailwind API keys
   [ ] Single quotes on all JS strings (no double quotes except in JSX attributes)
   [ ] No trailing commas in .astro files (Astro parser limitation)
Project structure after completion:
```
project/
├── src/
│   ├── content/
│   │   ├── config.ts
│   │   ├── blog/
│   │   │   ├── en/
│   │   │   │   └── hello-world.md
│   │   │   └── sv/
│   │   │       └── hej-varlden.md
│   │   └── docs/
│   │       └── getting-started.mdx
│   ├── components/
│   │   ├── Counter.tsx
│   │   ├── SEO.astro
│   │   └── AstroErrorBoundary.astro
│   ├── i18n/
│   │   └── index.ts
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   └── I18nLayout.astro
│   ├── pages/
│   │   ├── index.astro
│   │   ├── 404.astro
│   │   ├── 500.astro
│   │   ├── blog/
│   │   │   └── [...slug].astro
│   │   └── docs/
│   │       └── [...slug].astro
│   ├── assets/
│   │   └── hero.jpg
│   └── env.ts
├── public/
├── astro.config.mjs
├── tailwind.config.mjs
├── .env.example
├── .prettierrc
├── eslint.config.mjs
├── tsconfig.json
└── package.json
```
Build command: npm run build
Lint command: npm run lint
Format command: npm run format
Dev command: npm run dev
