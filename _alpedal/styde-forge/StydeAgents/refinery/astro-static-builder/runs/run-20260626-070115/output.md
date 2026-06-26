project: create astro-static-site
location: /tmp/astro-demo
tech-stack:
  framework: astro 5.x
  rendering: static (SSG)
  ui: astro islands
  content: content collections
  transitions: view transitions api
  mdx: yes
steps:
  - init: npm create astro@latest /tmp/astro-demo -- --template basics --install --no-git
  - add mdx: npx astro add mdx --yes
  - add integrations: npx astro add view-transitions --yes
content-collection:
  path: src/content/blog/
  schema:
    title: string
    date: date
    description: string
    draft: boolean (optional)
    tags: string[] (optional)
  body: MDX
islands:
  component: src/components/Counter.tsx
  pattern: client:load for critical interactivity
  pattern: client:idle for non-critical interactivity
view-transitions:
  enabled: true (via integration)
  usage: <a data-astro-transition="slide" /> for page transitions
  persist: keep persistent elements with transition:persist directive
build-output: dist/
  static: true
  all pages pre-rendered at build time
  zero client JS for non-interactive pages
key-configs:
  astro.config.mjs:
    - site: https://example.com
    - integrations: [mdx(), viewTransitions()]
    - output: static (default)
  content-collection-schema:
    - src/content/config.ts with defineCollection and z.object
    - type-safe frontmatter validation at build time
deliverable: fully static Astro site with content collections, View Transitions, MDX authoring, and interactive islands where needed