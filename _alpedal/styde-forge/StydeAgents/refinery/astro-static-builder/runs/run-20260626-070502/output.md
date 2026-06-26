BLUEPRINT.md
Purpose
Builds production-ready Astro static sites. Content collections, View Transitions, islands architecture, Markdown/MDX, asset optimization, RSS, sitemaps, Tailwind CSS.
Project structure
src/
  content/
    config.ts          content collection schemas
    blog/              blog collection entries (.md/.mdx)
    pages/             page collection entries
  components/
    BaseHead.astro     SEO head with canonical, OG, sitemap link
    Navigation.astro   responsive nav with View Transitions
    Footer.astro       site footer
    Hero.astro         landing hero section
    BlogCard.astro     card for blog listing
    BlogGrid.astro     grid of BlogCards
    ThemeToggle.astro  client:visible island for dark/light toggle
    Search.astro       client:load island for full-text search
    MdxWrapper.astro   custom components provider for MDX
  layouts/
    BaseLayout.astro   HTML shell, SEO, fonts, View Transitions
    BlogLayout.astro   blog post layout with prose styling
    PageLayout.astro   generic page layout with sidebar
  pages/
    index.astro        landing page
    blog/
      index.astro      blog listing with pagination
      [...slug].astro  blog post route with getStaticPaths
    rss.xml.ts         RSS feed endpoint
  styles/
    global.css         Tailwind base + custom properties
  env.d.ts             env type declarations (PUBLIC_ prefix, runtime vars)
public/
  favicon.ico
  robots.txt           disallow nothing, sitemap: /sitemap-index.xml
astro.config.mjs
import { defineConfig } from astro/config
import mdx from '@astrojs/mdx'
import sitemap from '@astrojs/sitemap'
import tailwindcss from '@tailwindcss/vite'
import netlify from '@astrojs/netlify' // adapter: netlify() — not astroAdapterNetlify()
import react from '@astrojs/react'     // islands
import partytown from '@astrojs/partytown' // analytics offloading
import compressor from 'astro-compressor'  // brotli in build
export default defineConfig({
  site: 'https://example.com',
  trailingSlash: 'never',
  output: 'static',
  adapter: netlify(),
  integrations: [
    mdx({
      remarkPlugins: [],
      rehypePlugins: [],
      customComponentImports: true,
      gfm: true,
    }),
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
      filter: (page) => !page.includes('/404'),
    }),
    react(),
    partytown({
      config: { forward: ['dataLayer.push'] },
    }),
    compressor(),
  ],
  vite: {
    plugins: [tailwindcss()],
    envPrefix: ['PUBLIC_', 'ASTRO_'],
  },
  image: {
    service: { entrypoint: 'astro/assets/services/sharp' },
    domains: ['images.ctfassets.net'],
  },
  build: {
    format: 'file',
    assets: '_assets',
    inlineStylesheets: 'auto',
  },
  server: {
    port: 4321,
  },
  experimental: {
    contentLayer: true, // Astro 5 content layer
  },
})
Content collections: src/content/config.ts
import { defineCollection, z } from 'astro:content'
const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().max(160),
    pubDate: z.date(),
    updatedDate: z.date().optional(),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    canonicalURL: z.string().url().optional(),
  }),
})
const pages = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    navOrder: z.number().optional(),
    draft: z.boolean().default(false),
  }),
})
export const collections = { blog, pages }
Query example in a page (src/pages/blog/index.astro):
---
import { getCollection } from 'astro:content'
import BlogCard from '@/components/BlogCard.astro'
const posts = await getCollection('blog', ({ data }) => !data.draft)
  .then(ps => ps.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()))
---
MDX with custom components (src/components/MdxWrapper.astro):
---
import type { MDXComponents } from 'astro/components'
import CustomImage from './CustomImage.astro'
import YouTubeEmbed from './YouTubeEmbed.astro'
export const components: MDXComponents = {
  img: CustomImage,
  YouTube: YouTubeEmbed,
}
---
<slot />
Then in MDX frontmatter:
---
export const components = (await import('@/components/MdxWrapper.astro')).components
---
Tailwind CSS setup
1. pnpm add tailwindcss @tailwindcss/vite
2. Add @tailwindcss/vite in astro.config.mjs vite.plugins (shown above)
3. src/styles/global.css:
@import "tailwindcss";
@custom-variant dark (&:where(.dark, .dark *));
@theme {
  --font-sans: Inter, system-ui, sans-serif;
  --font-mono: JetBrains Mono, monospace;
  --color-brand: oklch(0.55 0.22 265);
}
Image optimization (current Astro asset API, not deprecated @astrojs/image)
- Built-in: Astro 3+ includes image optimization via astro/assets/services/sharp
- Import: import { Image, Picture } from 'astro:assets'
- Usage:
  <Image src={import('../assets/hero.png')} alt="hero" width={1200} height={630} formats={['avif','webp']} loading="eager" />
  <Picture src={import('../assets/banner.png')} formats={['avif','webp']} widths={[400,800,1200]} sizes="(max-width:768px) 100vw, 50vw" alt="banner" />
- Remote images: <Image src={new URL(remoteUrl)} ... /> with image.domains config
- Sharp must be installed: pnpm add sharp
RSS feed (src/pages/rss.xml.ts):
import rss from '@astrojs/rss'
import { getCollection } from 'astro:content'
import sanitizeHtml from 'sanitize-html'
import MarkdownIt from 'markdown-it'
const parser = new MarkdownIt()
export async function GET(context) {
  const posts = await getCollection('blog')
  return rss({
    title: 'Site Title',
    description: 'Site description',
    site: context.site,
    items: posts.map(post => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description,
      link: `/blog/${post.id}/`,
      content: sanitizeHtml(parser.render(post.body)),
    })),
    customData: '<language>en-us</language>',
    stylesheet: '/rss-style.xsl',
  })
}
Dependencies: pnpm add @astrojs/rss sanitize-html markdown-it
View Transitions API
- In BaseLayout.astro: import { ViewTransitions } from 'astro:transitions'
- Add <ViewTransitions /> to <head>
- Per-page transition directives:
  <a href="/blog" data-astro-transition-persist>Blog</a>
  Transition name via: transition:name="hero" on elements that should morph
  transition:animate="slide" | "fade" | "morph" on page wrapper
Environment variables
- Public: PUBLIC_ prefixed vars available client+server via import.meta.env.PUBLIC_API_URL
- Server-only: ASTRO_ prefixed vars, available server-side only via import.meta.env
- .env.example:
  PUBLIC_SITE_URL=https://example.com
  PUBLIC_GA_ID=G-XXXXXXXXXX
  ASTRO_CONTENTFUL_SPACE=xxx
- Type-safe env: src/env.d.ts
  /// <reference types="astro/client" />
  interface ImportMetaEnv {
    readonly PUBLIC_SITE_URL: string
    readonly ASTRO_CONTENTFUL_SPACE: string
  }
  interface ImportMeta {
    readonly env: ImportMetaEnv
  }
Deploy configuration
Netlify (recommended):
- netlify.toml:
  [build]
    command = "pnpm build"
    publish = "dist"
  [[redirects]]
    from = "/blog/*"
    to = "/blog/[...slug]"
    status = 200
- Environment variables set in Netlify dashboard, pulled at build time
Vercel:
- adapter: vercel() from @astrojs/vercel (serverless or static)
- vercel.json for rewrites/headers
Use adapter: edge for edge-rendered fallback on both platforms
Hybrid rendering (if SSR needed selectively)
astro.config.mjs:
  output: 'hybrid',
  adapter: netlify(),
In pages that need SSR:
  export const prerender = false
In static pages (default):
  export const prerender = true
Edge cases: write to KV/store in SSR page, serve cached static version for remaining routes
Implementation sequence
1. pnpm create astro@latest --template basics --install
2. pnpm add @astrojs/mdx @astrojs/sitemap @astrojs/netlify @astrojs/react @astrojs/rss @tailwindcss/vite tailwindcss astro-compressor @astrojs/partytown sharp sanitize-html markdown-it
3. Copy astro.config.mjs from above
4. Create src/content/config.ts with schemas
5. Create base layout with ViewTransitions, SEO, fonts
6. Create blog layout with prose, table of contents
7. Create pages: index, blog/index, blog/[...slug]
8. Create rss.xml.ts, sitemap auto-generated by integration
9. Add hero images, favicon, robots.txt
10. pnpm build && pnpm preview