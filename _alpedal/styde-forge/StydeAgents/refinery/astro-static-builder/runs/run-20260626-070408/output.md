Blueprint: Astro Static Builder
Domain: frontend
Version: 3
Purpose:
Production-ready Astro static site scaffolding. Content collections with type-safe schemas, View Transitions API, islands architecture, MDX authoring, image optimization, RSS, sitemaps, deployment config, and hybrid SSR/static rendering.
Persona:
Astro specialist. Expert in Astro islands, content collections, View Transitions API, image optimization pipelines, and hybrid rendering.
Skills:
  Islands: implement Astro islands for interactive client components
  Content: use content collections with type-safe Zod schemas, query entries in pages, filter by fields
  ViewTrans: implement View Transitions API with fade/slide animations and persist-able elements
  MDX: author MDX content with custom component injection via components prop
  Images: use @astrojs/image for optimized, responsive images with srcset and lazy loading
  RSS: generate RSS/Atom feeds from content collections
  Sitemap: auto-generate XML sitemaps via @astrojs/sitemap
  Deploy: configure adapters for Netlify, Vercel, Cloudflare Pages
  Env: manage environment variables with Astro's built-in VITE_ prefix and server-side Astro.env
  Hybrid: configure hybrid SSR/static rendering with output: 'hybrid' and per-route export
Dependencies:
  astro@^4.0.0
  @astrojs/mdx
  @astrojs/sitemap
  @astrojs/netlify or @astrojs/vercel or @astrojs/cloudflare
  astro-icon (optional, for SVG icons)
Structure:
src/
  content/
    config.ts          -- collection schemas
    blog/              -- MDX blog entries
    projects/          -- MDX project entries
  layouts/
    Base.astro         -- HTML shell, View Transitions, SEO meta
    BlogPost.astro     -- article layout with prose styling
  components/
    Interactive/
      LikeButton.astro -- client:load island
      Map.astro        -- client:visible island
    Content/
      Prose.astro      -- shared prose container
  pages/
    index.astro        -- hero + featured posts
    blog/
      index.astro      -- paginated list, RSS link
      [...slug].astro  -- dynamic routes from content collections
    rss.xml.ts         -- RSS feed endpoint
    projects/
      index.astro
      [...slug].astro
  styles/
    global.css         -- view transitions, prose, resets
Content Collections config (src/content/config.ts):
  import { z, defineCollection } from 'astro:content'
  const blog = defineCollection({
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
  const projects = defineCollection({
    type: 'content',
    schema: z.object({
      title: z.string(),
      description: z.string(),
      url: z.string().url().optional(),
      tech: z.array(z.string()),
      featured: z.boolean().default(false),
    })
  })
  export const collections = { blog, projects }
Query example in a page (src/pages/blog/[...slug].astro):
  ---
  import { getCollection } from 'astro:content'
  import BlogPost from '../../layouts/BlogPost.astro'
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
View Transitions (src/layouts/Base.astro):
  ---
  import { ViewTransitions } from 'astro:transitions'
  ---
  <!DOCTYPE html>
  <html lang="en">
    <head>
      <ViewTransitions />
      <meta name="viewport" content="width=device-width" />
      <slot name="head" />
    </head>
    <body>
      <slot />
    </body>
  </html>
Image Optimization (src/components/Content/Prose.astro):
  ---
  import { Image } from '@astrojs/image/components'
  ---
  <Image src={heroImage} alt={title} widths={[400, 800, 1200]} sizes="(max-width: 768px) 100vw, 800px" loading="lazy" />
RSS Feed (src/pages/rss.xml.ts):
  ---
  import rss from '@astrojs/rss'
  import { getCollection } from 'astro:content'
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
        link: `/blog/${post.slug}/`,
      })),
      customData: '<language>en-us</language>'
    })
  }
Sitemap (astro.config.mjs):
  import { defineConfig } from 'astro/config'
  import mdx from '@astrojs/mdx'
  import sitemap from '@astrojs/sitemap'
  import netlify from '@astrojs/netlify'
  export default defineConfig({
    site: 'https://example.com',
    integrations: [mdx(), sitemap()],
    output: 'static',
    adapter: netlify(),
    image: {
      service: { entrypoint: 'astro/assets/services/sharp' }
    }
  })
Env Vars:
  Public: VITE_API_URL=http://localhost:4321
  Server-only: SECRET_API_KEY stored in .env, accessed via Astro.env.SECRET_API_KEY
  .env file at project root, .env.example committed without secrets
Hybrid SSR (per-route opt-in):
  astro.config.mjs:
    output: 'hybrid'
    adapter: netlify()
  Mark pages with export const prerender = false for SSR
  Default is static (prerender = true)
Deploy configs:
  Netlify: netlify.toml with build command, publish dir, redirects
    [build]
      command = 'npm run build'
      publish = 'dist'
    [[redirects]]
      from = '/*'
      to = '/404'
      status = 404
  Vercel: vercel.json with framework preset
    { "framework": "astro", "buildCommand": "npm run build", "outputDirectory": "dist" }
Integrations checklist:
  @astrojs/mdx for MDX content with custom components
  @astrojs/sitemap for auto sitemap
  @astrojs/rss for RSS feeds
  @astrojs/image or built-in astro:assets for image optimization
  Adapter (netlify/vercel/cloudflare) for deployment
  astro-icon for SVG icon system
MDX Custom Components:
  In mdx files, import and use Astro components directly
  Or pass via components prop in MDX layout:
    const { Content } = await post.render()
    <Content components={{ h1: MyCustomH1, img: OptimizedImage }} />