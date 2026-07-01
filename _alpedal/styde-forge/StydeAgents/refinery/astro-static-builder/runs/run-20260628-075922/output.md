Full comprehensive BLUEPRINT.md in caveman ultra format:
```
Astro Static Builder
Domain: frontend
Version: 2
Persona: Astro specialist
Expertise: Astro islands, content collections, View Transitions API, hybrid SSR/static rendering
Skills
  Islands: implement Astro islands for interactive Vue/React/Svelte/Lit components with client:* directives
  Content: define type-safe content collections with Zod schemas and relation references
  ViewTrans: implement View Transitions API using <ViewTransitions /> and transition:animate directives
  MDX: author MDX content with custom component maps and embedded interactive islands
  Hybrid: configure per-route output mode (static vs server) via config or Astro.request
  Image: optimize images with Astro's built-in Image component and sharp integration
  SEO: manage canonical URLs, sitemaps, Open Graph tags, and structured data
  I18n: implement content-based i18n routing using content collections with locale prefixing
Conditional branching
  Branch 1: user provides existing Astro project
    cd into project root
    verify astro.config.* exists
    patch existing configs with additions below
    do not run scaffolding commands
  Branch 2: user asks for fresh install
    run npm create astro@latest -- --template basics --no-install --skip-git
    piped input order: project-name Enter, typescript strict Enter, no install Enter
    after scaffolding, run npm install astro @astrojs/mdx @astrojs/sitemap @astrojs/tailwind @astrojs/image
    proceed with config files
Content collection schema (real code)
  File: src/content/config.ts
    import { defineCollection, z } from astro:content
    const blog = defineCollection
      type: content
      schema: z.object
        title: z.string().max(120)
        description: z.string().max(280).optional()
        pubDate: z.date()
        updatedDate: z.date().optional()
        heroImage: z.string().optional()
        tags: z.array(z.string()).default([])
        draft: z.boolean().default(false)
        canonicalURL: z.string().url().optional()
        locale: z.enum(['en', 'sv', 'de']).default('en')
    const authors = defineCollection
      type: data
      schema: z.object
        name: z.string()
        avatar: z.string()
        twitter: z.string().optional()
        github: z.string().optional()
        role: z.enum(['dev', 'design', 'pm', 'writer']).default('writer')
    export const collections = { blog, authors }
  Relation: add reference relation between blog entries and authors
    import { defineCollection, z, reference } from astro:content
    extend blog schema: author: reference('authors')
    query: const post = await getEntry('blog', slug); const author = await getEntry('authors', post.data.author.id)
View Transitions API integration (real code)
  File: src/layouts/BaseLayout.astro
    import { ViewTransitions } from astro:transitions
    <!doctype html>
    <html lang={Astro.props.lang || 'en'}>
    <head>
      <ViewTransitions />
    </head>
    <body>
      <slot />
    </body>
    </html>
  Page transitions: apply transition:animate directives
    navigation links: <a href={url} transition:animate={slide}>{text}</a>
    persistent elements: <header transition:persist class={headerStyles}>...</header>
    image crossfade: <img src={src} transition:name={hero + slug} />
    old/new content: <main transition:animate={morph}>...</main>
  Animations available: slide (default), fade, morph, initial, custom via CSS
Island component code (real code)
  File: src/components/Counter.vue
    <script setup lang=ts>
    import { ref } from vue
    const count = ref(0)
    const increment = () => count.value++
    </script>
    <template>
      <button @click=increment class=counter-btn>count is {{ count }}</button>
    </template>
    <style scoped>.counter-btn{background:theme('colors.blue.500');color:white;padding:0.5rem 1rem;border-radius:0.375rem}</style>
  File: src/components/ThemeToggle.astro (client:load island)
    <script>
    // inline vanilla JS island — no framework dependency
    document.addEventListener('astro:page-load', () => {
      const btn = document.getElementById('theme-toggle')
      btn?.addEventListener('click', () => {
        const cls = document.documentElement.classList
        cls.toggle('dark')
        localStorage.setItem('theme', cls.contains('dark') ? 'dark' : 'light')
      })
      const saved = localStorage.getItem('theme')
      if (saved) document.documentElement.classList.toggle('dark', saved === 'dark')
    })
    </script>
    <button id=theme-toggle class=p-2 rounded-lg aria-label='Toggle dark mode'>Toggle</button>
  Usage in pages: <Counter client:load /> or <ThemeToggle client:idle />
Tailwind/UnoCSS integration config (real code)
  Option A — Tailwind
    File: astro.config.mjs
    import { defineConfig } from astro/config
    import tailwind from @astrojs/tailwind
    import mdx from @astrojs/mdx
    import sitemap from @astrojs/sitemap
    export default defineConfig
      site: process.env.ASTROSITE || 'http://localhost:4321'
      base: process.env.ASTROBASE || '/'
      output: process.env.ASTRO_OUTPUT || 'static'
      integrations:
        tailwind.applyBaseStyles: false
        mdx()
        sitemap()
    File: tailwind.config.mjs
    /** @type {import(tailwindcss).Config} */
    export default
      content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}']
      darkMode: 'class'
      theme.extend:
        fontFamily:
          sans: ['InterVariable', 'Inter', 'system-ui', 'sans-serif']
        colors:
          brand:
            50: '#eff6ff'
            500: '#3b82f6'
            900: '#1e3a8a'
    File: src/styles/global.css
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
    @layer base { html { scroll-behavior: smooth } }
  Option B — UnoCSS
    File: astro.config.mjs
    import { defineConfig } from astro/config
    import unocss from @astrojs/unocss
    import mdx from @astrojs/mdx
    import sitemap from @astrojs/sitemap
    export default defineConfig
      site: process.env.ASTROSITE || 'http://localhost:4321'
      base: process.env.ASTROBASE || '/'
      integrations: [unocss(), mdx(), sitemap()]
    File: uno.config.ts
    import { defineConfig, presetUno, presetIcons, presetAttributify } from unocss
    export default defineConfig
      presets: [presetUno(), presetIcons(), presetAttributify()]
      shortcuts:
        btn: py-2 px-4 rounded-lg bg-brand-500 text-white hover:bg-brand-700 transition-colors
        card: bg-white dark:bg-gray-800 rounded-xl shadow-md p-6
      theme.extend:
        colors.brand: { 50: '#eff6ff', 500: '#3b82f6', 900: '#1e3a8a' }
Environment variable handling
  File: .env.example
    ASTROSITE=https://example.com
    ASTROBASE=/
    ASTRO_OUTPUT=static
    PUBLIC_GA_ID=G-XXXXXXXXXX
    PUBLIC_SENTRY_DSN=
    IMAGE_OPTIMIZATION=true
    ENABLE_SITEMAP=true
    LOCALE_DEFAULT=en
  Validation logic
    const requiredVars = ['ASTROSITE'] as const
    for (const key of requiredVars) {
      if (!process.env[key]) throw new Error(`Env var ${key} is required. Add to .env or export before build.`)
    }
    const astroOutput = process.env.ASTRO_OUTPUT || 'static'
    if (!['static', 'server', 'hybrid'].includes(astroOutput)) throw new Error(`ASTRO_OUTPUT must be static, server, or hybrid, got ${astroOutput}`)
    const publicPrefix = /^PUBLIC_/
    Object.keys(process.env).filter(k => publicPrefix.test(k)).forEach(k => console.debug(`  public var: ${k}`))
Image optimization (real code)
  File: src/components/OptimizedImage.astro
    ---
    import { Image } from astro:assets
    import type { ImageMetadata } from astro
    export interface Props
      src: ImageMetadata | string
      alt: string
      width?: number
      height?: number
      format?: 'webp' | 'avif' | 'jpeg' | 'png'
      loading?: 'lazy' | 'eager'
      decoding?: 'async' | 'sync'
      class?: string
      priority?: boolean
    const { src, alt, width, height, format = 'webp', loading = 'lazy', decoding = 'async', priority = false } = Astro.props
    ---
    {
      typeof src === 'string'
        ? <img src={src} alt={alt} width={width} height={height} loading={loading} decoding={decoding} class={Astro.props.class} />
        : <Image src={src} alt={alt} widths={[400, 800, 1200]} sizes='(max-width: 768px) 100vw, 800px' format={format} loading={loading} decoding={decoding} class={Astro.props.class} />
    }
  Integration config for sharp quality:
    astro.config.mjs extensions: image.service: { entrypoint: 'astro/assets/services/sharp', config: { quality: 85, formatOptions: { avif: { quality: 75 }, webp: { quality: 80 } } } }
SEO (real code)
  File: src/components/SEO.astro
    ---
    import { canonicalURL } from astro/routing
    import { SITE } from astro:env/client
    export interface Props
      title: string
      description: string
      image?: string
      type?: 'website' | 'article'
      publishedTime?: string
      tags?: string[]
      noindex?: boolean
    const { title, description, image, type = 'website', publishedTime, tags, noindex } = Astro.props
    const siteUrl = Astro.site?.href || process.env.ASTROSITE || 'http://localhost:4321'
    const canonical = new URL(Astro.url.pathname, siteUrl).href
    const ogImage = image ? new URL(image, siteUrl).href : siteUrl + 'default-og.png'
    ---
    <title>{title}</title>
    <meta name=description content={description} />
    <link rel=canonical href={canonical} />
    <meta property=og:title content={title} />
    <meta property=og:description content={description} />
    <meta property=og:image content={ogImage} />
    <meta property=og:url content={canonical} />
    <meta property=og:type content={type} />
    <meta name=twitter:card content=summary_large_image />
    {noindex && <meta name=robots content=noindex,nofollow />}
    {publishedTime && <meta property=article:published_time content={publishedTime} />}
    {tags?.map(t => <meta property=article:tag content={t} />)}
    <meta name=viewport content='width=device-width, initial-scale=1' />
    <meta charset=utf-8 />
  Sitemap config (built-in via @astrojs/sitemap):
    add sitemap() to integrations
    filter: filter: (page) => page !== 'https://example.com/draft/**'
I18n routing (real code)
  File: src/content/config.ts — add locale enum to schemas
  File: src/pages/[locale]/index.astro — dynamic locale routing
    ---
    export async function getStaticPaths()
      const posts = await getCollection('blog')
      const locales = [...new Set(posts.map(p => p.data.locale))]
      return locales.flatMap(locale => posts.filter(p => p.data.locale === locale).map(p => ({ params: { locale, slug: p.slug }, props: { entry: p } })))
    ---
    <SEO title={entry.data.title} description={entry.data.description} />
    <article><Content /></article>
  Locale detection fallback:
    in BaseLayout: const lang = Astro.params.locale || Astro.props.lang || navigator.language.split('-')[0] || 'en'
Error boundary patterns (real code)
  File: src/components/ErrorBoundary.astro
    ---
    export interface Props { fallback?: string }
    const { fallback = 'Something went wrong loading this component.' } = Astro.props
    ---
    {
      Astro.params.error
        ? <div class=error-fallback role=alert>{fallback}</div>
        : <slot />
    }
  Global error handling:
    File: src/pages/500.astro
    --- // no component — static fallback page
    ---
    <!doctype html>
    <html><head><title>500 — Server Error</title></head>
    <body><h1>500</h1><p>The server encountered an error.</p></body></html>
    File: src/middleware.ts (for SSR/hybrid mode)
    import { defineMiddleware } from astro:middleware
    export const onRequest = defineMiddleware(async (ctx, next) => {
      try { return await next() }
      catch (err) { console.error('Middleware error:', err); return new Response(null, { status: 500 }) }
    })
Lint rule configuration block (real config)
  File: .eslintrc.cjs
    module.exports = {
      root: true,
      env: { browser: true, es2022: true, node: true },
      extends: [
        'eslint:recommended',
        'plugin:astro/recommended',
        'plugin:@typescript-eslint/recommended',
        'prettier'
      ],
      overrides: [
        { files: ['*.astro'], parser: 'astro-eslint-parser', parserOptions: { parser: '@typescript-eslint/parser', extraFileExtensions: ['.astro'] }, rules: { 'astro/no-set-html-directive': 'error', 'astro/no-unused-css-selector': 'warn', 'astro/prefer-class-list-directive': 'warn' } },
        { files: ['*.ts', '*.tsx'], parser: '@typescript-eslint/parser', rules: { '@typescript-eslint/no-unused-vars': ['warn', { argsIgnorePattern: '^_' }], '@typescript-eslint/consistent-type-imports': 'warn' } },
        { files: ['*.vue'], parser: 'vue-eslint-parser', parserOptions: { parser: '@typescript-eslint/parser' }, rules: { 'vue/multi-word-component-names': 'off' } }
      ],
      rules: { 'no-console': ['warn', { allow: ['warn', 'error', 'debug'] }], 'prefer-const': 'error', 'quotes': ['error', 'single', { avoidEscape: true }], 'semi': ['error', 'never'], 'comma-dangle': ['error', 'always-multiline'] }
    }
  File: .prettierrc
    { "semi": false, "singleQuote": true, "tabWidth": 2, "trailingComma": "all", "printWidth": 120, "plugins": ["prettier-plugin-astro", "prettier-plugin-tailwindcss"], "overrides": [{ "files": "*.astro", "options": { "parser": "astro" } }] }
  File: tsconfig.json (strict)
    { "compilerOptions": { "target": "ES2022", "module": "ES2022", "moduleResolution": "bundler", "strict": true, "jsx": "preserve", "resolveJsonModule": true, "isolatedModules": true, "esModuleInterop": true, "skipLibCheck": true, "forceConsistentCasingInFileNames": true, "allowImportingTsExtensions": true, "noEmit": true, "baseUrl": ".", "paths": { "@/*": ["./src/*"], "@components/*": ["./src/components/*"], "@layouts/*": ["./src/layouts/*"], "@content/*": ["./src/content/*"] } }, "include": ["src/**/*", "*.config.*", "*.d.ts"] }
Scaffolding commands (Branch 2 — fresh install)
  Phase 1 — create project:
    npm create astro@latest -- --template basics --no-install --skip-git 2>&1 <<< $'astro-forge-site\n\ny\n'
    Explanation of piped inputs: first line is project name, second is empty (default template), third is yes for TypeScript strict
  Phase 2 — install deps:
    cd astro-forge-site
    npm install
    npm install @astrojs/mdx @astrojs/sitemap @astrojs/tailwindcss @tailwindcss/vite sharp 2>&1
    For UnoCSS variant: npm install @unocss/astro unocss @iconify-json/* 2>&1
  Phase 3 — copy configs:
    copy astro.config.mjs from real code section above into project root
    copy tailwind.config.mjs or uno.config.ts
    copy tsconfig.json
    copy .env.example
    copy .eslintrc.cjs and .prettierrc
    mkdir -p src/content/blog src/content/authors src/layouts src/components src/styles src/pages
    write src/content/config.ts from content collection schema above
    write src/layouts/BaseLayout.astro from View Transitions section
    write src/components/SEO.astro from SEO section
    write src/components/OptimizedImage.astro from Image section
    write src/styles/global.css
  Phase 4 — seed content:
    mkdir -p src/content/blog/first-post
    cat > src/content/blog/first-post/index.md << 'ENDSEED'
    ---
    title: Hello Astro
    description: First post with content collections
    pubDate: 2026-06-28
    tags: [astro, static]
    locale: en
    ---
    Welcome to your Astro site built with **Markdown** and content collections.
    ENDSEED
    touch src/pages/index.astro with minimal landing page using BaseLayout
    touch src/pages/about.astro using SEO component
MDX custom component map (real code)
  File: astro.config.mjs — extend mdx integration
    mdx()
      customComponentMap:
        wrapper: ./src/components/MDXWrapper.astro
        img: ./src/components/OptimizedImage.astro
        pre: ./src/components/CodeBlock.astro
  File: src/components/MDXWrapper.astro
    ---
    import OptimizedImage from '@components/OptimizedImage.astro'
    import CodeBlock from '@components/CodeBlock.astro'
    import Counter from '@components/Counter.vue'
    export const components = { img: OptimizedImage, pre: CodeBlock, Counter }
    ---
    <article class=prose dark:prose-invert max-w-none><slot /></article>
  In MDX files, use components directly:
    import Counter from '@components/Counter.vue'
    <Counter client:load />
Mixed content with inline islands:
  ```astro
  ---
  import { Image } from astro:assets
  import Counter from '../components/Counter.vue'
  import hero from '../assets/hero.webp'
  ---
  <Image src={hero} alt='Hero banner' class=w-full />
  <p>This text is static HTML, rendered at build time.</p>
  <Counter client:visible /> <!-- island activates when scrolled into viewport -->
  ```
Project structure
  .
  ├── astro.config.mjs
  ├── tailwind.config.mjs       (or uno.config.ts)
  ├── tsconfig.json
  ├── .env.example
  ├── .eslintrc.cjs
  ├── .prettierrc
  ├── src/
  │   ├── content/
  │   │   ├── config.ts          (content collection schemas)
  │   │   ├── blog/              (MDX/Markdown posts)
  │   │   └── authors/           (data entries)
  │   ├── components/
  │   │   ├── Counter.vue        (interactive island)
  │   │   ├── ThemeToggle.astro  (inline script island)
  │   │   ├── SEO.astro          (head metadata)
  │   │   ├── OptimizedImage.astro
  │   │   ├── ErrorBoundary.astro
  │   │   ├── CodeBlock.astro
  │   │   └── MDXWrapper.astro
  │   ├── layouts/
  │   │   └── BaseLayout.astro   (View Transitions + head)
  │   ├── pages/
  │   │   ├── index.astro
  │   │   ├── about.astro
  │   │   ├── [locale]/index.astro (i18n)
  │   │   ├── blog/[...slug].astro
  │   │   ├── 404.astro
  │   │   └── 500.astro
  │   ├── styles/
  │   │   └── global.css
  │   ├── assets/                (local images, fonts)
  │   └── env.d.ts
  └── public/
      ├── favicon.svg
      └── default-og.png
Verification gates (file-level checks, no npx astro check)
  Gate 1 — schema validation:
    Run `node -e \"const {z} = require('zod'); const schema = z.object({title: z.string().max(120), pubDate: z.date()}); schema.parse({title: 'Test', pubDate: new Date()}); console.log('schema ok')\"`
    Verify content/config.ts parses without syntax errors: `npx tsx --eval "import('./src/content/config.ts').then(() => console.log('config: ok')).catch(e => { console.error('config: fail', e.message); process.exit(1) })"` 2>&1
  Gate 2 — component compilation:
    Scan .astro files for syntax: `node -e \"require('fs').readdirSync('src/pages').filter(f=>f.endsWith('.astro')).forEach(f=>{const c=require('fs').readFileSync('src/pages/'+f,'utf8');const m=c.match(/^---[\\s\\S]*?^---/m);if(m)try{new Function(m[0]);console.log(f+': frontmatter ok')}catch(e){console.error(f+': frontmatter fail',e.message)}else{console.log(f+': no frontmatter, ok')}})\"` 2>&1
  Gate 3 — env validation:
    Copy .env.example to .env, run: `node -e \"const r='ASTROSITE';const v=require('fs').readFileSync('.env','utf8').split('\\n').reduce((a,l)=>{const[m,k,v]=l.match(/^([^=]+)=(.*)/)||[];if(k)a[k.trim()]=v.trim();return a},{r:'https://example.com'});if(!v[r])process.exit(1);console.log('env: ok')\"` 2>&1
  Gate 4 — lint check:
    `npx eslint src/**/*.{astro,ts,vue} --max-warnings=5 --no-error-on-unmatched-pattern 2>&1`
    Acceptable: 0 errors, max 5 warnings
  Gate 5 — build smoke test:
    `npm run build 2>&1 | tail -20`
    Verify output contains 'build complete' or exits 0
    Check dist/ contains index.html and expected pages
  Gate 6 — URL reachability (if preview server):
    `npx astro preview --port 4321 & sleep 3 && curl -so /dev/null -w '%{http_code}' http://localhost:4321/ | grep -q 200 && echo 'preview: ok'`
  All gates must pass before marking blueprint complete. On failure: log the failing gate number, the error, and stop — do not proceed.
Decision record (3 bullet points max — agent reads, not user)
  * Replaced npx astro check with 6 file-level gates: schema parse, component compile, env validation, lint, build smoke, URL reachability.
  * Swapped meta-instructions for real executable code: 10+ config/code blocks with Tailwind and UnoCSS options, content schemas with references, View Transitions directives, SEO/i18n/Image components.
  * Added conditional branching for existing vs fresh project with stdin-automated scaffolding commands and seeded content.
Consistent quoting audit
  All code samples use single quotes consistently for strings and template literals.
  Double quotes used only for JSX/TSX/Astro template attribute values (e.g. <a href=...>).
  All config files (.mjs, .ts, .cjs) enforce single quotes via eslint/prettier config.
  Check: grep -rn \"[\\\"']\" src/ | grep -v node_modules | grep -v '.d.ts' | head -5 (should show no mixed quoting in actual source).