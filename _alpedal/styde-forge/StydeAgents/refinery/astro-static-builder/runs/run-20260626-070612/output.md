BLUEPRINT.md
Purpose
Builds Astro static sites. Content collections, View Transitions, islands architecture, Markdown/MDX.
Persona
Astro specialist. Expert in Astro islands, content collections, View Transitions API, and hybrid rendering.
Skills
  Islands: implement Astro islands for interactive components
  Content: use content collections with type-safe schemas
  ViewTrans: implement View Transitions API
  MDX: author MDX content with custom components
  Hybrid: configure hybrid SSR/static rendering
Init
  npx create-astro@latest project --template basics
  cd project
  npx astro add mdx tailwind netlify sitemap
Dependencies
  Required:
    astro@5
    @astrojs/mdx
    @astrojs/netlify
    @astrojs/sitemap
    @astrojs/tailwind
    @astrojs/check
    typescript@5
    tailwindcss@3
  Optional:
    @astrojs/alpinejs (light islands)
    @astrojs/vue    (Vue islands)
    @astrojs/react  (React islands)
    @astrojs/solid  (Solid islands)
    @astrojs/preact (Preact islands)
    unocss          (alternative to Tailwind)
    @unocss/astro   (UnoCSS integration)
Config: astro.config.mjs
  import { defineConfig } from astro/config
  import mdx from @astrojs/mdx
  import tailwind from @astrojs/tailwind
  import netlify from @astrojs/netlify
  import sitemap from @astrojs/sitemap
  import alpinejs from @astrojs/alpinejs  // optional
  export default defineConfig({
    site: 'https://example.com',
    output: 'static',
    adapter: netlify(),
    integrations: [
      mdx({
        remarkPlugins: [],
        rehypePlugins: [],
        gfm: true,
        optimize: true,
      }),
      tailwind(),
      sitemap({
        filter: (page) => !page.includes('/draft/'),
        changefreq: 'weekly',
        priority: 0.7,
        lastmod: new Date(),
      }),
      alpinejs(),
    ],
    // View Transitions — enabled per-page via <ViewTransitions />
    // Or globally in Layout.astro: import { ViewTransitions } from astro:transitions
    experimental: {
      clientPrerender: true,
    },
    // Image optimization — Astro 5 built-in
    image: {
      service: {
        entrypoint: 'astro/assets/services/sharp',
        config: {
          quality: 80,
        },
      },
    },
    // Build caching
    vite: {
      cacheDir: '.vite-cache',
      build: {
        rollupOptions: {
          output: {
            manualChunks: (id) => {
              if (id.includes('node_modules')) {
                if (id.includes('alpinejs')) return 'vendor-alpine'
                if (id.includes('marked') || id.includes('shiki')) return 'vendor-content'
                return 'vendor'
              }
            },
          },
        },
        cssMinify: 'esbuild',
        sourcemap: false,
      },
      ssr: {
        noExternal: ['@astrojs/*'],
      },
    },
    // TypeScript strict
    typescript: {
      strict: true,
      allowJs: false,
    },
  })
TypeScript: tsconfig.json
  {
    "extends": "astro/tsconfigs/strict",
    "include": [".astro/types.d.ts", "**/*"],
    "exclude": ["dist"],
    "compilerOptions": {
      "strict": true,
      "noUncheckedIndexedAccess": true,
      "exactOptionalPropertyTypes": false,
      "baseUrl": ".",
      "paths": {
        "@/*": ["src/*"],
        "@components/*": ["src/components/*"],
        "@layouts/*": ["src/layouts/*"],
        "@content/*": ["src/content/*"]
      }
    }
  }
Content Collections: src/content/config.ts
  import { defineCollection, z } from astro:content
  const blog = defineCollection({
    type: 'content', // loads Markdown/MDX
    schema: z.object({
      title: z.string(),
      description: z.string().max(160),
      pubDate: z.coerce.date(),
      updatedDate: z.coerce.date().optional(),
      heroImage: z.string().optional(),
      tags: z.array(z.string()).default([]),
      draft: z.boolean().default(false),
      author: z.string().default('Staff'),
    }),
  })
  const pages = defineCollection({
    type: 'content',
    schema: z.object({
      title: z.string(),
      order: z.number().optional(),
      draft: z.boolean().default(false),
    }),
  })
  export const collections = { blog, pages }
MDX custom components: src/components/mdx/index.astro (re-export as jsx/tsx)
  Use Astro components inside MDX via Astro.glob or import in MDX layout:
  // src/layouts/BlogPost.astro
  ---
  import { Content } from astro:content
  import CodeBlock from '@components/mdx/CodeBlock.astro'
  import Image from '@components/mdx/MdxImage.astro'
  import Callout from '@components/mdx/Callout.astro'
  export const components = { pre: CodeBlock, img: Image, blockquote: Callout }
  ---
  <Content components={components} />
Content query example: src/pages/blog/[slug].astro
  ---
  import { getCollection } from astro:content
  import BlogPost from '@layouts/BlogPost.astro'
  export async function getStaticPaths() {
    const posts = await getCollection('blog', ({ data }) => !data.draft)
    return posts.map(post => ({
      params: { slug: post.slug },
      props: { post },
    }))
  }
  const { post } = Astro.props
  const { Content } = await post.render()
  ---
  <BlogPost post={post}>
    <Content />
  </BlogPost>
Hybrid rendering (pages needing SSR)
  // src/pages/api/contact.ts
  export const prerender = false
  // or in astro.config: output: 'hybrid', adapter: netlify()
View Transitions: enabled via <ViewTransitions /> in Layout.astro
  ---
  import { ViewTransitions } from astro:transitions
  ---
  <!doctype html>
  <html lang="en">
    <head>
      <ViewTransitions />
    </head>
    <body>
      <slot />
    </body>
  </html>
  Per-page transitions via transition:name and transition:animate directives on elements.
  Supported animations: fade, slide, initial, custom CSS keyframes.
Image optimization — Astro 5 built-in (NOT @astrojs/image)
  // src/components/ResponsiveImage.astro
  ---
  import { Image, Picture } from astro:assets
  export interface Props {
    src: ImageMetadata | Promise<{ default: ImageMetadata }>
    alt: string
    sizes?: string
    widths?: number[]
    formats?: ('webp' | 'avif')[]
  }
  const { src, alt, sizes = '100vw', widths = [640, 960, 1280], formats } = Astro.props
  ---
  <Picture
    src={src}
    alt={alt}
    sizes={sizes}
    widths={widths}
    formats={formats}
    loading="lazy"
    decoding="async"
  />
  // Usage in MDX or Astro pages:
  // import hero from '@images/hero.jpg'
  // <Image src={hero} alt="Hero" />
Styling: Tailwind CSS (or UnoCSS)
  Tailwind setup via @astrojs/tailwind integration (already in astro.config).
  Add custom theme in tailwind.config.mjs:
    export default {
      content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
      theme: {
        extend: {
          fontFamily: {
            display: ['Inter', 'system-ui', 'sans-serif'],
            mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
          },
        },
      },
    }
  Alternative: UnoCSS via @unocss/astro — lighter build time, JIT by default.
    // uno.config.ts
    import { defineConfig, presetUno, presetAttributify, presetIcons } from unocss
    export default defineConfig({
      presets: [presetUno(), presetAttributify(), presetIcons()],
    })
Environment variables
  Prefix with PUBLIC_ for client-side access: PUBLIC_API_URL
  Server-side only: SECRET_API_KEY (not exposed to client)
  .env file at project root:
    PUBLIC_SITE_URL=https://example.com
    PUBLIC_API_URL=https://api.example.com
    SECRET_API_KEY=sk-xxx
  Access in Astro: import.meta.env.PUBLIC_SITE_URL
  Access in adapter server context: Astro.locals (set via middleware)
Build & Deployment
  Caching (significant speedup):
    astro.config.mjs sets vite.cacheDir to .vite-cache
    Persist .vite-cache between builds on CI (GitHub Actions: actions/cache)
    Use `turbo` for monorepo: pnpm dlx turbo run build --cache-dir=.turbo-cache
  Commands:
    dev:     npx astro dev
    build:   npx astro build
    preview: npx astro preview
    check:   npx astro check (type-check .astro files)
  Incremental builds (Astro 5):
    Content changes only rebuild affected pages.
    No config needed — built-in with static output.
  Netlify deploy:
    Build command: npx astro build
    Publish directory: dist
    Environment variables set in Netlify UI / netlify.toml
    netlify.toml:
      [build]
        command = "npx astro build"
        publish = "dist"
      [[redirects]]
        from = "/api/*"
        to = "/.netlify/functions/:splat"
        status = 200
Production checklist
  Verify sitemap at /sitemap-index.xml
  Verify RSS if configured
  Test View Transitions across browsers (Chrome, Safari 18+, Firefox)
  Run npx astro check for type errors
  Run lighthouse audit
  Set PUBLIC_SITE_URL in deployment environment
  Enable CDN caching for /_astro/* assets (fingerprinted, long cache)
  Disable drafts: all frontmatter draft: true or filter in getStaticPaths