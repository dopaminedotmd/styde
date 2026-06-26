Blueprint: astro-static-builder v1
Domain: frontend
Target: static-site generation with islands, content collections, View Transitions, MDX
Dir structure:
  src/
    pages/
      index.astro
      blog/
        [...slug].astro
    content/
      config.ts
      blog/
        first-post.md
      _schema.ts
    components/
      Header.astro
      Footer.astro
    layouts/
      Base.astro
      BlogPost.astro
    styles/
      global.css
  public/
    favicon.ico
  astro.config.mjs
  package.json
  tsconfig.json
Dependencies:
  astro@latest
  @astrojs/mdx
  @astrojs/sitemap
  No astro-view-transitions package -- View Transitions built into astro core since 2.x
Astro config:
  import { defineConfig } from astro
  import mdx from @astrojs/mdx
  import sitemap from @astrojs/sitemap
  export default defineConfig({
    site: https://example.com,
    integrations: [mdx(), sitemap()],
    output: static,
    viewTransitions: true
  })
Content collections schema:
  src/content/config.ts
    defineCollection for blog
      schema: z.object({
        title: z.string(),
        pubDate: z.date(),
        description: z.string(),
        author: z.string().default('Anonymous'),
        tags: z.array(z.string()).default([]),
        draft: z.boolean().default(false)
      })
View Transitions implementation:
  import { ViewTransitions } from astro:transitions
  Place in Base.astro <head>
  Use client:visible directive on interactive islands
  No separate npm package -- core feature since Astro 2.x
Islands architecture:
  Interactive components get client:visible or client:load directive
  Static content remains server-rendered
  All .astro components without client directive are zero JS
MDX setup:
  @astrojs/mdx integration
  Custom components via export const components in MDX files
  Layout applied via frontmatter layout property
Page scaffold:
  src/pages/index.astro
    import Base from ../layouts/Base.astro
    import Header from ../components/Header.astro
    <Base title=Home>
      <Header />
      <main>slot content</main>
    </Base>
  src/pages/blog/[...slug].astro
    import { getCollection } from astro:content
    export async function getStaticPaths() {
      const posts = await getCollection('blog')
      return posts.filter(p => !p.data.draft).map(p => ({
        params: { slug: p.slug },
        props: { post: p }
      }))
    }
    ---
    const { post } = Astro.props
    const { Content } = await post.render()
    ---
    <BlogPost title={post.data.title}>
      <Content />
    </BlogPost>
Verification: this blueprint reflects Astro features as of June 2026. View Transitions API is built-in since Astro 2.x. No external view-transitions package required.