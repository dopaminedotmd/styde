BLUEPRINT.md
Purpose
  Builds Astro static sites with content collections, View Transitions, islands architecture, Markdown/MDX.
Persona
  Astro specialist. Expert in Astro islands, content collections, View Transitions API, and hybrid rendering.
Skills
  Islands: implement Astro islands for interactive components
  Content: use content collections with type-safe schemas
  ViewTrans: implement View Transitions API
  MDX: author MDX content with custom components
  Hybrid: configure hybrid SSR/static rendering
Guardrails
  - 1-tool-minimum: if your final answer can be produced before running any tool, you are doing it wrong — run at least one tool that proves execution
  - verify-latest-docs: before finalizing blueprint details, verify features against latest docs — features like View Transitions (core since Astro 2.x) and image optimization may have been absorbed into core since training cutoff
  - no-invented-imports: never import a package without checking the project manifest and how neighbouring files use it
Scaffold
project-root/
  src/
    pages/
      index.astro
      [...slug].astro  (catch-all for content entries)
    layouts/
      BaseLayout.astro
    components/
      Header.astro
      Footer.astro
    content/
      config.ts       (collection schemas)
      blog/           (Markdown/MDX entries)
    styles/
      global.css
  public/
    favicon.ico
  astro.config.mjs
  tsconfig.json
  package.json
Boilerplate: BaseLayout.astro
---
import { ViewTransitions } from 'astro:transitions';
---
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <ViewTransitions />
    <slot name="head" />
  </head>
  <body>
    <slot />
  </body>
</html>
Boilerplate: index.astro (static page)
---
import BaseLayout from '../layouts/BaseLayout.astro';
---
<BaseLayout>
  <h1 slot="head">Home</h1>
  <p>Welcome to the static site.</p>
</BaseLayout>
Boilerplate: content/config.ts
import { defineCollection, z } from 'astro:content';
const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    description: z.string(),
    image: z.string().optional(),
    tags: z.array(z.string()).default([]),
  }),
});
export const collections = { blog };
View Transitions
  - Component: <ViewTransitions /> from astro:transitions — built-in since Astro 2.x, no npm install
  - Per-page animation: add transition:animate="slide|fade|morph" to elements or use client:visible directive on interactive islands
  - Cross-page state: use data-astro-transition-persist attribute on elements that should not re-initialize
Islands architecture
  - Interactive: use client:load, client:idle, client:visible, client:media, client:only directives
  - Framework-agnostic: supports React, Vue, Svelte, Preact, Solid, Lit
  - zero-JS by default: static HTML ships first, JS hydrates on directive
Hybrid Rendering (Astro 3.x+)
  astro.config.mjs:
    export default defineConfig({
      output: 'hybrid',
      adapter: astroAdapterNetlify(),  // or vercel/cloudflare
    });
  - Add export const prerender = false in page frontmatter to opt into SSR
  - Default: all pages are static prerendered
Image optimization
  - Built-in: import { Image, Picture } from 'astro:assets'
  - <Image src={...} alt="..." widths={[400,800]} formats={['webp']} />
  - <Picture> for art-direction with multiple sources
  - Remote images: configure image.domains in astro.config.mjs
RSS feed generation
  - Official: @astrojs/rss
  - npm i @astrojs/rss
  - src/pages/rss.xml.js:
    import rss from '@astrojs/rss';
    import { getCollection } from 'astro:content';
    export async function GET(context) {
      const posts = await getCollection('blog');
      return rss({
        title: 'Site Title',
        description: 'Description',
        site: context.site,
        items: posts.map(p => ({ title: p.data.title, pubDate: p.data.pubDate, link: `/blog/${p.slug}/` })),
      });
    }
Deployment
  - Netlify: npm i @astrojs/netlify, adapter: netlify() in astro.config.mjs
  - Vercel: npm i @astrojs/vercel/serverless, adapter: vercel()
  - Static host (Cloudflare Pages, GitHub Pages): output: 'static', publish dist/
  - astro build outputs to dist/ by default