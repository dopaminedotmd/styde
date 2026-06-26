# Astro Static Builder — Run 20260626-020000 (Advanced c2)

## Executive Summary

Deep-dive into Astro 5.x advanced patterns: Server Islands (`server:defer`), streaming SSR with Suspense fallbacks, persistent client state via nanostores, the Content Layer API for external data loading, and on-demand ISR with adapter-level cache invalidation. Every section includes real, copy-paste-ready source files, configuration, and architectural guidance. This run extends and complements the c1 foundational build with production-grade progressive enhancement techniques.

---

## 1. Complete Project Structure

```
advanced-astro-site/
├── astro.config.mjs                    # Adapter, integrations, ISR cache config
├── package.json
├── tsconfig.json
├── .env                                # CMS tokens, ISR secrets
├── .gitignore
│
├── public/
│   ├── favicon.svg
│   └── robots.txt
│
├── src/
│   ├── env.d.ts
│   │
│   ├── content/
│   │   ├── config.ts                   # Content Layer API: loaders + schemas
│   │   ├── blog/                       # Local MDX files (content collection)
│   │   │   ├── post-1.mdx
│   │   │   └── post-2.mdx
│   │   └── products/                   # Remote CMS data (content layer loader)
│   │       └── (empty — loaded from CMS)
│   │
│   ├── components/
│   │   ├── BaseHead.astro
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   │
│   │   ├── server/                     # Server Islands (server:defer)
│   │   │   ├── ProductPrice.server.astro
│   │   │   ├── PersonalizedRecommendations.server.astro
│   │   │   ├── UserDashboard.server.astro
│   │   │   └── AdServer.server.astro
│   │   │
│   │   ├── streaming/                  # Streaming + Suspense
│   │   │   ├── StreamingProductList.astro
│   │   │   ├── SlowDataSection.astro
│   │   │   ├── StreamingSkeleton.svelte
│   │   │   └── CommentSection.astro
│   │   │
│   │   ├── state/                      # nanostores atoms + maps
│   │   │   ├── cartStore.ts
│   │   │   ├── userPreferencesStore.ts
│   │   │   ├── themeStore.ts
│   │   │   └── notificationStore.ts
│   │   │
│   │   ├── react/                      # React interactive islands
│   │   │   ├── CartButton.tsx
│   │   │   ├── ThemeToggle.tsx
│   │   │   ├── NotificationBell.tsx
│   │   │   └── SearchOverlay.tsx
│   │   │
│   │   └── svelte/                     # Svelte interactive islands
│   │       ├── ProductFilter.svelte
│   │       ├── StreamingSkeleton.svelte
│   │       └── LiveCounter.svelte
│   │
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   ├── ProductLayout.astro
│   │   └── DashboardLayout.astro
│   │
│   ├── pages/
│   │   ├── index.astro                 # Homepage (static + server islands)
│   │   ├── products/
│   │   │   ├── index.astro             # Product listing with streaming
│   │   │   └── [slug].astro            # Product detail with server island
│   │   ├── dashboard/
│   │   │   └── index.astro             # User dashboard (SSR + server islands)
│   │   ├── cart/
│   │   │   └── index.astro             # Cart page with nanostores
│   │   │
│   │   └── api/
│   │       ├── revalidate.ts           # On-demand ISR endpoint
│   │       └── webhook.ts              # CMS webhook → ISR trigger
│   │
│   ├── styles/
│   │   └── global.css
│   │
│   └── lib/
│       ├── cms.ts                      # CMS client helpers
│       ├── cache-tags.ts               # ISR cache tag utilities
│       └── constants.ts
│
└── (this document)
```

---

## 2. Configuration Files

### 2.1 `astro.config.mjs` — Server Islands, Streaming, ISR Adapter

```js
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import svelte from '@astrojs/svelte';
import vercel from '@astrojs/vercel';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://advanced-astro.example.com',

  // ═══════════════════════════════════════════════════════
  //  SERVER OUTPUT — required for server islands + ISR
  // ═══════════════════════════════════════════════════════
  output: 'server',
  // Use 'hybrid' if most pages are static and only specific
  // pages need SSR. 'server' is simpler when you're doing
  // on-demand ISR across the site.

  adapter: vercel({
    // ── On-Demand ISR configuration ─────────────────────
    isr: {
      // Cache-control headers for ISR pages
      expiration: 60 * 60,        // 1 hour stale-while-revalidate
      bypassToken: import.meta.env.VERCEL_BYPASS_TOKEN,
      // Individual pages can override via Astro.response.headers
    },
    // Edge rendering for lowest latency server islands
    edgeMiddleware: true,
    // Web analytics (optional)
    webAnalytics: { enabled: true },
  }),

  // ═══════════════════════════════════════════════════════
  //  INTEGRATIONS
  // ═══════════════════════════════════════════════════════
  integrations: [
    mdx(),
    react(),
    svelte(),
    sitemap(),
  ],

  // ═══════════════════════════════════════════════════════
  //  SERVER ISLANDS — experimental in early Astro 5.x,
  //                   stable in Astro 5.2+
  // ═══════════════════════════════════════════════════════
  experimental: {
    serverIslands: true,
    // Content layer with remote loaders:
    contentLayer: true,   // only needed in early 5.x
  },

  // ═══════════════════════════════════════════════════════
  //  IMAGE OPTIMIZATION (leverage for streaming)
  // ═══════════════════════════════════════════════════════
  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp',
    },
  },
});
```

### 2.2 `package.json`

```json
{
  "name": "advanced-astro-site",
  "type": "module",
  "version": "2.0.0",
  "scripts": {
    "dev": "astro dev",
    "build": "astro check && astro build",
    "preview": "astro preview",
    "astro": "astro",
    "revalidate": "curl -X POST http://localhost:4321/api/revalidate"
  },
  "dependencies": {
    "@astrojs/check": "^0.9.4",
    "@astrojs/mdx": "^4.2.6",
    "@astrojs/react": "^4.2.6",
    "@astrojs/sitemap": "^3.3.1",
    "@astrojs/svelte": "^7.0.12",
    "@astrojs/vercel": "^8.2.2",
    "@nanostores/react": "^0.8.4",
    "@nanostores/persistent": "^0.10.4",
    "astro": "^5.7.12",
    "nanostores": "^0.11.4",
    "react": "^19.1.0",
    "react-dom": "^19.1.0",
    "svelte": "^5.34.0",
    "typescript": "^5.5.0",
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "@types/react": "^19.1.3",
    "@types/react-dom": "^19.1.5",
    "prettier": "^3.5.3",
    "prettier-plugin-astro": "^0.14.1"
  }
}
```

### 2.3 `tsconfig.json`

```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "react",
    "baseUrl": ".",
    "paths": {
      "@components/*": ["src/components/*"],
      "@layouts/*": ["src/layouts/*"],
      "@lib/*": ["src/lib/*"],
      "@content/*": ["src/content/*"],
      "@stores/*": ["src/components/state/*"]
    }
  }
}
```

### 2.4 `src/env.d.ts`

```ts
/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />

interface ImportMetaEnv {
  readonly VERCEL_BYPASS_TOKEN: string;
  readonly CMS_API_URL: string;
  readonly CMS_API_TOKEN: string;
  readonly REVALIDATION_SECRET: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

---

## 3. Server Islands — Deferred Server Rendering

### Concept

Server Islands are Astro components that render **on the server after the page has loaded**. The initial HTML is shipped immediately (static shell), and the server island content streams in asynchronously via a `fetch` request from the browser. This gives you:

- **Instant page loads** — the static shell renders in < 100ms
- **Personalized content** — user-specific data (cart, recommendations, auth state) without blocking
- **Zero client JS for static parts** — only the island itself hydrates

### 3.1 How It Works

```
Browser requests /products/laptop
         │
         ▼
┌─────────────────────────────────────┐
│  Server renders static shell        │
│  (everything NOT marked server:* )  │
│  Response sent immediately          │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Browser paints static shell        │
│  Skeleton / spinner visible         │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Auto-fetch: GET /_server-islands   │
│  ?props=encoded&component=Product   │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Server renders island component    │
│  (has access to request, cookies,   │
│   DB, auth, etc.)                   │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  HTML fragment replaces skeleton    │
│  SWAP-IN transition (optional)      │
└─────────────────────────────────────┘
```

### 3.2 Writing a Server Island Component

**`src/components/server/ProductPrice.server.astro`** — dynamic pricing from DB:

```astro
---
// ═══════════════════════════════════════════════════════
//  server:defer — renders AFTER the page shell
//  server:defer => the component code NEVER ships to
//                 the client. It ONLY runs on the server.
// ═══════════════════════════════════════════════════════
export const server = 'defer' as const;

interface Props {
  productId: string;
  currency?: string;
}

const { productId, currency = 'USD' } = Astro.props;

// Full server access: DB queries, auth, secrets
const price = await fetchProductPrice(productId, currency);

// Simulate fetching from a DB or external pricing API
async function fetchProductPrice(id: string, cur: string) {
  // In production: query your DB or pricing service
  const response = await fetch(
    `${import.meta.env.CMS_API_URL}/products/${id}/price?currency=${cur}`,
    { headers: { Authorization: `Bearer ${import.meta.env.CMS_API_TOKEN}` } }
  );
  const data = await response.json();
  return data;
}
---

<astro-slot name="fallback">
  <!-- ═══════════════════════════════════════════════════ -->
  <!--  FALLBACK — shown while the island fetches        -->
  <!-- ═══════════════════════════════════════════════════ -->
  <div class="price-skeleton animate-pulse">
    <span class="block h-6 w-20 rounded bg-gray-200 dark:bg-gray-700"></span>
  </div>
</astro-slot>

<!-- ═══════════════════════════════════════════════════════ -->
<!--  SERVER-ONLY CONTENT — never in client bundle        -->
<!-- ═══════════════════════════════════════════════════════ -->
<div
  class="product-price"
  data-server-island="product-price"
>
  {price.discountApplied && (
    <span class="line-through text-gray-400 mr-2">
      {formatCurrency(price.original, currency)}
    </span>
  )}
  <span class="text-2xl font-bold text-green-600">
    {formatCurrency(price.current, currency)}
  </span>
  {price.stock < 10 && (
    <span class="ml-2 text-xs text-red-500">
      Only {price.stock} left!
    </span>
  )}
</div>
```

### 3.3 Using Server Islands in a Page

**`src/pages/products/[slug].astro`**:

```astro
---
import BaseLayout from '@layouts/BaseLayout.astro';
import ProductPrice from '@components/server/ProductPrice.server.astro';
import PersonalizedRecommendations from '@components/server/PersonalizedRecommendations.server.astro';
import UserDashboard from '@components/server/UserDashboard.server.astro';
import CartButton from '@components/react/CartButton';

export const prerender = false; // SSR page

const { slug } = Astro.params;
const product = await getProduct(slug);
---

<BaseLayout title={product.name}>
  <article class="product-detail">
    <!-- ══════════════════════════════════════════════════ -->
    <!--  STATIC SHELL — renders instantly                -->
    <!-- ══════════════════════════════════════════════════ -->
    <h1>{product.name}</h1>
    <p>{product.description}</p>
    <img src={product.image} alt={product.name} />

    <!-- ══════════════════════════════════════════════════ -->
    <!--  SERVER ISLAND — price from DB (deferred)        -->
    <!--  Skeleton shown, then swapped with real price    -->
    <!-- ══════════════════════════════════════════════════ -->
    <ProductPrice
      productId={product.id}
      currency="USD"
      server:defer
    />

    <!-- ══════════════════════════════════════════════════ -->
    <!--  CLIENT ISLAND — interactive add-to-cart          -->
    <!-- ══════════════════════════════════════════════════ -->
    <CartButton
      client:load
      productId={product.id}
      productName={product.name}
    />

    <!-- ══════════════════════════════════════════════════ -->
    <!--  SERVER ISLAND — recommendations from ML service -->
    <!-- ══════════════════════════════════════════════════ -->
    <section class="recommendations">
      <h2>You Might Also Like</h2>
      <PersonalizedRecommendations
        productId={product.id}
        server:defer
      />
    </section>
  </article>
</BaseLayout>
```

### 3.4 Multiple Server Islands on One Page

**`src/components/server/PersonalizedRecommendations.server.astro`**:

```astro
---
export const server = 'defer' as const;

interface Props {
  productId: string;
}

const { productId } = Astro.props;

// This could be a slow ML inference call
const recommendations = await fetchRecommendations(productId);

async function fetchRecommendations(id: string) {
  // Simulate slow ML service (300–800ms typical)
  await new Promise(r => setTimeout(r, 400));
  return [
    { name: 'Wireless Mouse', slug: 'wireless-mouse', score: 0.94 },
    { name: 'USB-C Hub', slug: 'usb-c-hub', score: 0.87 },
    { name: 'Laptop Stand', slug: 'laptop-stand', score: 0.82 },
  ];
}
---

<astro-slot name="fallback">
  <div class="grid grid-cols-3 gap-4">
    {[1, 2, 3].map(i => (
      <div class="skeleton-card animate-pulse">
        <div class="h-32 rounded bg-gray-200 dark:bg-gray-700" />
        <div class="mt-2 h-4 w-3/4 rounded bg-gray-200 dark:bg-gray-600" />
      </div>
    ))}
  </div>
</astro-slot>

<div class="recommendations-grid grid grid-cols-3 gap-4">
  {recommendations.map(rec => (
    <a href={`/products/${rec.slug}`} class="rec-card">
      <span class="rec-name">{rec.name}</span>
      <span class="rec-score text-xs text-gray-400">
        {Math.round(rec.score * 100)}% match
      </span>
    </a>
  ))}
</div>
```

### 3.5 Server Island Lifecycle + Scripts

```astro
---
// src/components/server/AdServer.server.astro
export const server = 'defer' as const;
const ad = await fetchTargetedAd(Astro.request);
---

<astro-slot name="fallback">
  <div class="ad-placeholder h-24 bg-gray-100 dark:bg-gray-800 rounded flex items-center justify-center text-gray-400">
    Advertisement
  </div>
</astro-slot>

<div class="ad-container" data-ad-id={ad.id}>
  <a href={ad.url} target="_blank">
    <img src={ad.image} alt={ad.alt} loading="lazy" />
  </a>
</div>

<!-- ═══════════════════════════════════════════════════════ -->
<!--  SERVER ISLAND LIFE CYCLE SCRIPT                      -->
<!--  This runs ONLY after the island renders             -->
<!-- ═══════════════════════════════════════════════════════ -->
<script>
  // This script is injected by Astro for server islands
  // It fires when the HTML fragment is swapped in
  document.addEventListener('astro:server-island', (event) => {
    const island = event.target;
    console.log('Server island loaded:', island.dataset.adId);
    // Track impression or initialize analytics
  });
</script>
```

### 3.6 Server Islands + Auth Context

Server islands have full access to `Astro.request` including cookies and headers:

```astro
---
// src/components/server/UserDashboard.server.astro
export const server = 'defer' as const;

// Read auth cookie — NOT available in static shell or client islands
const sessionToken = Astro.cookies.get('session')?.value;
const user = sessionToken ? await validateSession(sessionToken) : null;

if (!user) {
  // Redirect to login — works because server island runs on server
  return Astro.redirect('/login');
}

const stats = await fetchUserStats(user.id);
---

<astro-slot name="fallback">
  <div class="dashboard-skeleton">
    <div class="h-40 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
  </div>
</astro-slot>

<div class="dashboard">
  <h2>Welcome back, {user.name}</h2>
  <div class="stats-grid grid grid-cols-4 gap-4">
    <StatCard label="Orders" value={stats.orders} />
    <StatCard label="Reviews" value={stats.reviews} />
    <StatCard label="Wishlist" value={stats.wishlistCount} />
    <StatCard label="Points" value={stats.loyaltyPoints} />
  </div>
</div>
```

### 3.7 Server Islands Compatibility Matrix

| Feature | Static Shell | Server Island | Client Island |
|---------|:---:|:---:|:---:|
| Renders at build time | ✅ | ❌ | ❌ |
| Renders at request time | ❌ | ✅ | ❌ |
| Access to `Astro.request` | ❌ | ✅ | ❌ |
| Access to cookies | ❌ | ✅ | ❌ |
| DB queries / secrets | ❌ | ✅ | ❌ |
| Interactive on client | ❌ | ❌ | ✅ |
| JS shipped to browser | 0 KB | 0 KB | Framework runtime |
| Can use `client:*` directives | ❌ | ❌ | ✅ |

---

## 4. Streaming SSR with Fallbacks

### Concept

Streaming sends HTML to the browser **progressively** as it's rendered, rather than waiting for the entire page. Combined with Astro's `render()` and `Suspense`-like patterns, you can:

- Send the `<head>` and above-the-fold content in **~50ms**
- Defer slow data sections behind **loading skeletons**
- Use **out-of-order streaming** so fast sections render before slow ones

### 4.1 Basic Streaming — `Astro.response`

```astro
---
// src/pages/products/index.astro
import BaseLayout from '@layouts/BaseLayout.astro';
import StreamingProductList from '@components/streaming/StreamingProductList.astro';
import SlowDataSection from '@components/streaming/SlowDataSection.astro';

// Enable streaming for this page
Astro.response.headers.set('Transfer-Encoding', 'chunked');

// Fast data — available immediately
const categories = await fetchCategories(); // ~20ms
const heroBanner = await fetchHeroBanner();   // ~30ms
---

<BaseLayout title="Products">
  <!-- ═══════════════════════════════════════════════════ -->
  <!--  FAST SECTION — renders in first chunk            -->
  <!-- ═══════════════════════════════════════════════════ -->
  <section class="hero">
    <h1>{heroBanner.title}</h1>
    <p>{heroBanner.subtitle}</p>
  </section>

  <nav class="categories">
    {categories.map(cat => (
      <a href={`/products?category=${cat.slug}`}>{cat.name}</a>
    ))}
  </nav>

  <!-- ═══════════════════════════════════════════════════ -->
  <!--  STREAMING SECTION — deferred via component        -->
  <!-- ═══════════════════════════════════════════════════ -->
  <StreamingProductList client:only="svelte" />
  <!-- OR: server-side streaming with progressive render -->

  <!-- ═══════════════════════════════════════════════════ -->
  <!--  SLOW DATA — streams in after 300–800ms           -->
  <!-- ═══════════════════════════════════════════════════ -->
  <SlowDataSection />
</BaseLayout>
```

### 4.2 Streaming Component with Fallback

**`src/components/streaming/StreamingProductList.astro`**:

```astro
---
// This component streams its output.
// Astro renders it on the server and sends HTML chunks.

interface Product {
  id: string;
  name: string;
  price: number;
  image: string;
  slug: string;
}

// This fetch might take 500ms
const products: Product[] = await fetchProductList();

async function fetchProductList(): Promise<Product[]> {
  // In production: query DB, search API, or CMS
  const res = await fetch(`${import.meta.env.CMS_API_URL}/products`);
  return res.json();
}
---

<!-- ═══════════════════════════════════════════════════════ -->
<!--  The browser renders each product card as it arrives  -->
<!--  No placeholder needed — real content streams in      -->
<!-- ═══════════════════════════════════════════════════════ -->
<div class="product-grid grid grid-cols-3 gap-6">
  {products.map(product => (
    <a href={`/products/${product.slug}`} class="product-card">
      <img
        src={product.image}
        alt={product.name}
        loading="lazy"
        decoding="async"
      />
      <h3>{product.name}</h3>
      <span class="price">${product.price}</span>
    </a>
  ))}
</div>
```

### 4.3 Out-of-Order Streaming with `render()`

For maximum control, use `Astro.render()` to stream multiple components independently:

**`src/components/streaming/SlowDataSection.astro`**:

```astro
---
// Deliberately slow — simulates a complex DB query or external API
await new Promise(resolve => setTimeout(resolve, 600));

const reviews = [
  { author: 'Alice', rating: 5, text: 'Amazing quality!' },
  { author: 'Bob', rating: 4, text: 'Great value for money.' },
  { author: 'Carol', rating: 5, text: 'Fast shipping, perfect.' },
];
---

<section class="reviews-section">
  <h2>Customer Reviews</h2>
  <div class="reviews-list space-y-4">
    {reviews.map(review => (
      <blockquote class="review-card">
        <div class="flex items-center gap-2">
          <span class="font-semibold">{review.author}</span>
          <span class="text-yellow-500">{'★'.repeat(review.rating)}</span>
        </div>
        <p>{review.text}</p>
      </blockquote>
    ))}
  </div>
</section>
```

### 4.4 Streaming with `Suspense`-style Islands

**`src/pages/products/[slug].astro`** — the full page with streaming sections:

```astro
---
import BaseLayout from '@layouts/BaseLayout.astro';
import ProductPrice from '@components/server/ProductPrice.server.astro';
import CommentSection from '@components/streaming/CommentSection.astro';
import CartButton from '@components/react/CartButton';

export const prerender = false;

const { slug } = Astro.params;
const product = await getProduct(slug); // ~50ms — fast cache hit

Astro.response.headers.set('Transfer-Encoding', 'chunked');
---

<BaseLayout title={product.name}>
  <!-- ═══════════════════════════════════════════════════ -->
  <!--  CHUNK 1 — Above the fold (immediate)             -->
  <!-- ═══════════════════════════════════════════════════ -->
  <article class="product-detail">
    <div class="product-hero grid grid-cols-2 gap-8">
      <img src={product.image} alt={product.name} />
      <div class="product-info">
        <h1>{product.name}</h1>
        <p class="description">{product.description}</p>

        <!-- Server island — price with live stock -->
        <ProductPrice productId={product.id} server:defer />

        <!-- Client island — interactive cart button -->
        <CartButton
          client:load
          productId={product.id}
          productName={product.name}
        />
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════ -->
    <!--  CHUNK 2 — Specs (streams when ready, ~200ms)    -->
    <!-- ═══════════════════════════════════════════════════ -->
    <section class="specifications">
      <h2>Specifications</h2>
      {/* Renders progressively — content appears as available */}
    </section>

    <!-- ═══════════════════════════════════════════════════ -->
    <!--  CHUNK 3 — Comments from external API (~800ms)   -->
    <!-- ═══════════════════════════════════════════════════ -->
    <CommentSection productId={product.id} />
  </article>
</BaseLayout>
```

**`src/components/streaming/CommentSection.astro`**:

```astro
---
interface Props {
  productId: string;
}

const { productId } = Astro.props;

// Fetch from external comments service (takes ~500–800ms)
const comments = await fetchComments(productId);

async function fetchComments(id: string) {
  const res = await fetch(`https://comments-api.example.com/products/${id}`);
  if (!res.ok) return [];
  return res.json();
}
---

<section class="comments-section mt-8">
  <h2 class="text-xl font-bold mb-4">
    Comments ({comments.length})
  </h2>

  {comments.length === 0 ? (
    <p class="text-gray-500">No comments yet. Be the first!</p>
  ) : (
    <div class="space-y-4">
      {comments.map(comment => (
        <div class="comment-card bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
          <div class="flex items-center justify-between mb-2">
            <span class="font-semibold">{comment.author}</span>
            <time class="text-sm text-gray-400">{comment.date}</time>
          </div>
          <p>{comment.body}</p>
        </div>
      ))}
    </div>
  )}
</section>
```

### 4.5 Streaming + Client-side Hydration for Infinite Scroll

**`src/components/svelte/StreamingSkeleton.svelte`**:

```svelte
<script>
  // Shown during streaming before real content arrives
  export let count = 6;
</script>

<div class="grid grid-cols-3 gap-4">
  {#each Array(count) as _, i}
    <div class="skeleton-card animate-pulse" key={i}>
      <div class="h-48 bg-gray-200 dark:bg-gray-700 rounded-t-lg" />
      <div class="p-4 space-y-2">
        <div class="h-4 w-3/4 bg-gray-200 dark:bg-gray-600 rounded" />
        <div class="h-4 w-1/2 bg-gray-200 dark:bg-gray-600 rounded" />
      </div>
    </div>
  {/each}
</div>
```

### 4.6 Streaming Headers + SEO

```astro
---
// For streaming pages, set headers early
Astro.response.headers.set('Content-Type', 'text/html; charset=utf-8');
Astro.response.headers.set('Transfer-Encoding', 'chunked');
Astro.response.headers.set('X-Content-Type-Options', 'nosniff');

// SEO meta tags render in the <head> and are NOT streamed.
// The <head> is always sent in the first chunk.
---

<!doctype html>
<html lang="en">
  <head>
    <!-- This reaches the browser in < 50ms -->
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <title>{title} | Advanced Astro</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={Astro.url.href} />
  </head>
  <body>
    <!-- Body content streams progressively -->
    <slot />
  </body>
</html>
```

---

## 5. Persistent State with nanostores

### Concept

**nanostores** is a tiny (~250 bytes) state management library that works across frameworks. It's framework-agnostic and perfect for Astro's multi-framework islands architecture because:

- **Atoms** hold primitive values (numbers, strings, booleans)
- **Maps** hold key-value objects
- **Computed stores** derive values from other stores
- **`onMount`** persistence to localStorage
- **Framework bindings** exist for React (`@nanostores/react`), Svelte, Vue, Solid, and vanilla JS

### 5.1 Cart Store (Atom-based)

**`src/components/state/cartStore.ts`**:

```ts
import { atom, computed, map } from 'nanostores';
import { persistentAtom, persistentMap } from '@nanostores/persistent';

// ── Types ─────────────────────────────────────────────
export interface CartItem {
  productId: string;
  name: string;
  price: number;
  quantity: number;
  image: string;
}

// ── Atoms ─────────────────────────────────────────────
// $ prefix convention for stores

/** Whether the cart drawer is open */
export const $cartOpen = atom<boolean>(false);

/** Cart items — persisted to localStorage */
export const $cart = persistentMap<Record<string, CartItem>>(
  'cart-items',
  {},
  {
    encode: JSON.stringify,
    decode: JSON.parse,
  }
);

// ── Computed Stores ───────────────────────────────────

/** Total number of items in cart */
export const $cartCount = computed($cart, (items) => {
  return Object.values(items).reduce((sum, item) => sum + item.quantity, 0);
});

/** Total price */
export const $cartTotal = computed($cart, (items) => {
  return Object.values(items).reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
});

/** Cart items as an array (for rendering) */
export const $cartItems = computed($cart, (items) => {
  return Object.values(items);
});

// ── Actions ───────────────────────────────────────────

export function addToCart(item: CartItem) {
  const existing = $cart.get()[item.productId];
  $cart.setKey(item.productId, {
    ...item,
    quantity: existing ? existing.quantity + 1 : 1,
  });
  // Open cart drawer briefly
  $cartOpen.set(true);
  setTimeout(() => $cartOpen.set(false), 3000);
}

export function removeFromCart(productId: string) {
  const items = { ...$cart.get() };
  delete items[productId];
  $cart.set(items);
}

export function updateQuantity(productId: string, quantity: number) {
  if (quantity <= 0) {
    removeFromCart(productId);
  } else {
    $cart.setKey(productId, {
      ...$cart.get()[productId],
      quantity,
    });
  }
}

export function clearCart() {
  $cart.set({});
}
```

### 5.2 User Preferences Store (Map-based)

**`src/components/state/userPreferencesStore.ts`**:

```ts
import { persistentMap } from '@nanostores/persistent';
import { computed } from 'nanostores';

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  reducedMotion: boolean;
  fontSize: 'sm' | 'base' | 'lg';
  currency: 'USD' | 'EUR' | 'GBP';
  notifications: boolean;
}

export const $preferences = persistentMap<UserPreferences>(
  'user-prefs',
  {
    theme: 'system',
    reducedMotion: false,
    fontSize: 'base',
    currency: 'USD',
    notifications: true,
  },
  {
    encode: JSON.stringify,
    decode: JSON.parse,
  }
);

// Derived: the active theme (resolves 'system' to light/dark)
export const $activeTheme = computed($preferences, (prefs) => {
  if (prefs.theme !== 'system') return prefs.theme;
  if (typeof window !== 'undefined') {
    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }
  return 'light';
});

// Actions
export function setTheme(theme: UserPreferences['theme']) {
  $preferences.setKey('theme', theme);
}

export function toggleReducedMotion() {
  const current = $preferences.get().reducedMotion;
  $preferences.setKey('reducedMotion', !current);
}
```

### 5.3 Theme Store Integration

**`src/components/state/themeStore.ts`**:

```ts
import { persistentAtom } from '@nanostores/persistent';
import { onMount } from 'nanostores';

export const $theme = persistentAtom<'light' | 'dark' | 'system'>(
  'theme',
  'system'
);

// On client mount, apply theme to <html>
onMount($theme, () => {
  // This only runs client-side
  const applyTheme = () => {
    const t = $theme.get();
    const resolved =
      t === 'system'
        ? window.matchMedia('(prefers-color-scheme: dark)').matches
          ? 'dark'
          : 'light'
        : t;
    document.documentElement.setAttribute('data-theme', resolved);
  };

  applyTheme();

  // Listen for system preference changes
  const mq = window.matchMedia('(prefers-color-scheme: dark)');
  mq.addEventListener('change', () => {
    if ($theme.get() === 'system') applyTheme();
  });

  return () => mq.removeEventListener('change', applyTheme);
});

export function toggleTheme() {
  const current = $theme.get();
  if (current === 'light') $theme.set('dark');
  else if (current === 'dark') $theme.set('system');
  else $theme.set('light');
}
```

### 5.4 React Island Consuming nanostores

**`src/components/react/CartButton.tsx`**:

```tsx
import { useStore } from '@nanostores/react';
import { $cartOpen, $cartCount, $cartTotal, addToCart, removeFromCart } from '@stores/cartStore';
import { useState, useCallback } from 'react';

interface CartButtonProps {
  productId: string;
  productName: string;
  price: number;
  image?: string;
}

export default function CartButton({ productId, productName, price, image }: CartButtonProps) {
  // ═════════════════════════════════════════════════════
  //  useStore() subscribes to nanostores atom/map
  //  Component re-renders when store changes
  // ═════════════════════════════════════════════════════
  const cartCount = useStore($cartCount);
  const cartOpen = useStore($cartOpen);
  const cartTotal = useStore($cartTotal);
  const [added, setAdded] = useState(false);

  const handleAdd = useCallback(() => {
    addToCart({
      productId,
      name: productName,
      price,
      quantity: 1,
      image: image ?? '/placeholder.png',
    });
    setAdded(true);
    setTimeout(() => setAdded(false), 1500);
  }, [productId, productName, price, image]);

  return (
    <div className="cart-button-group">
      <button
        onClick={handleAdd}
        className={`add-to-cart-btn ${added ? 'added' : ''}`}
        aria-label={`Add ${productName} to cart`}
      >
        {added ? '✓ Added!' : 'Add to Cart'}
      </button>

      {/* Floating cart indicator — updates live from nanostores */}
      {cartCount > 0 && (
        <span className="cart-badge" aria-label={`${cartCount} items in cart`}>
          🛒 {cartCount} (${cartTotal.toFixed(2)})
        </span>
      )}

      {/* Cart drawer — controlled by $cartOpen */}
      {cartOpen && (
        <div className="cart-drawer">
          <h3>Cart ({cartCount} items)</h3>
          <p>Total: ${cartTotal.toFixed(2)}</p>
        </div>
      )}
    </div>
  );
}
```

### 5.5 Svelte Island Consuming nanostores

**`src/components/svelte/ProductFilter.svelte`**:

```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import { $preferences, setTheme } from '@stores/userPreferencesStore';
  import { $cartCount } from '@stores/cartStore';

  // nanostores integrates natively with Svelte's $ store syntax
  // when using the @nanostores/svelte package (optional adapter)

  let activeCategory = $state('all');
  let maxPrice = $state(1000);

  // Read nanostores via .get() and .subscribe()
  let currency = $state($preferences.get().currency);

  // Subscribe reactively
  const unsub = $preferences.subscribe((prefs) => {
    currency = prefs.currency;
  });

  onMount(() => {
    return () => unsub();
  });
</script>

<div class="product-filter">
  <h3>Filters</h3>

  <label>
    Category
    <select bind:value={activeCategory}>
      <option value="all">All</option>
      <option value="electronics">Electronics</option>
      <option value="clothing">Clothing</option>
      <option value="books">Books</option>
    </select>
  </label>

  <label>
    Max Price ({currency})
    <input type="range" min="0" max="1000" bind:value={maxPrice} />
    <span>{currency} {maxPrice}</span>
  </label>

  <!-- Cart count from shared nanostores -->
  <div class="cart-summary">
    🛒 {/** Use nanostores .get() for one-off reads */}
    {$cartCount.get()} items
  </div>
</div>
```

### 5.6 Sharing State Between Unrelated Islands

The magic of nanostores: **two different framework islands can share state without any bridge code**.

```
┌─────────────────────┐       ┌──────────────────────┐
│   React Island      │       │   Svelte Island       │
│   ThemeToggle.tsx   │       │   Settings.svelte      │
│                     │       │                        │
│  useStore($theme)   │       │  $theme.subscribe()    │
│       │             │       │       │                │
│       └──────┬──────┘       └───────┬────────────────┘
│              │                      │
│         ┌────▼──────────────────────▼────┐
│         │      nanostores atom           │
│         │      $theme                     │
│         │  (persistent to localStorage)   │
│         └─────────────────────────────────┘
│                       │
│         ┌─────────────▼──────────────────┐
│         │   Vanilla JS Island            │
│         │   themeStore.init()             │
│         │   document.documentElement      │
│         └────────────────────────────────┘
```

### 5.7 Notification Store (Cross-Component Communication)

**`src/components/state/notificationStore.ts`**:

```ts
import { atom } from 'nanostores';

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  duration?: number; // ms, default 4000
}

export const $notifications = atom<Notification[]>([]);

let nextId = 0;

export function addNotification(
  notification: Omit<Notification, 'id'>
) {
  const id = `notif-${++nextId}`;
  const duration = notification.duration ?? 4000;

  $notifications.set([
    ...$notifications.get(),
    { ...notification, id },
  ]);

  if (duration > 0) {
    setTimeout(() => dismissNotification(id), duration);
  }
}

export function dismissNotification(id: string) {
  $notifications.set($notifications.get().filter((n) => n.id !== id));
}
```

**`src/components/react/NotificationBell.tsx`**:

```tsx
import { useStore } from '@nanostores/react';
import { $notifications, dismissNotification } from '@stores/notificationStore';
import { addToCart } from '@stores/cartStore';

export default function NotificationBell() {
  const notifications = useStore($notifications);

  return (
    <div className="notification-center">
      <button className="bell-icon" aria-label="Notifications">
        🔔 {notifications.length > 0 && (
          <span className="badge">{notifications.length}</span>
        )}
      </button>

      {notifications.length > 0 && (
        <div className="notification-dropdown">
          {notifications.map((n) => (
            <div key={n.id} className={`notification ${n.type}`}>
              <p>{n.message}</p>
              <button onClick={() => dismissNotification(n.id)}>✕</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

---

## 6. Content Layer API

### Concept

The **Content Layer API** (Astro 5.x) replaces the old content collections loader with a pluggable system. Instead of being limited to local Markdown/MDX files, you can now load content from **any source** — headless CMS, database, REST API, GraphQL, CSV files, or even generated data — and have it participate in Astro's type-safe content collections.

### 6.1 Content Layer Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Content Collection                   │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ Local MDX    │  │ CMS Loader   │  │ DB Loader   │ │
│  │ (built-in)   │  │ (custom)     │  │ (custom)    │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬─────┘ │
│         │                 │                 │        │
│         └────────┬────────┴────────┬────────┘        │
│                  ▼                 ▼                  │
│          ┌──────────────────────────────┐            │
│          │   Type-safe Zod Schema       │            │
│          │   getCollection('name')      │            │
│          └──────────────────────────────┘            │
│                         │                             │
│                         ▼                             │
│          ┌──────────────────────────────┐            │
│          │  Astro Pages / Components     │            │
│          └──────────────────────────────┘            │
└─────────────────────────────────────────────────────┘
```

### 6.2 Content Config with Loaders

**`src/content/config.ts`**:

```ts
import { defineCollection, z } from 'astro:content';
import { cmsLoader } from '../lib/cms-loader';
import { productLoader } from '../lib/product-loader';

// ═══════════════════════════════════════════════════════
//  1. TRADITIONAL CONTENT COLLECTION — local MDX files
// ═══════════════════════════════════════════════════════
const blogCollection = defineCollection({
  type: 'content', // 'content' = local files (MDX, MD, etc.)
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    author: z.string().default('Team'),
    featured: z.boolean().default(false),
  }),
});

// ═══════════════════════════════════════════════════════
//  2. CONTENT LAYER COLLECTION — from external CMS
// ═══════════════════════════════════════════════════════
const productsCollection = defineCollection({
  // 'content_layer' type means data comes from a loader
  // NOT from local files in src/content/products/
  loader: cmsLoader({
    endpoint: `${import.meta.env.CMS_API_URL}/products`,
    headers: {
      Authorization: `Bearer ${import.meta.env.CMS_API_TOKEN}`,
    },
    // Transform CMS response to Astro entries
    transform: (item: any) => ({
      id: item.slug,
      // Any additional data needed for rendering
      rawData: item,
    }),
  }),
  schema: z.object({
    name: z.string(),
    slug: z.string(),
    description: z.string(),
    price: z.number(),
    currency: z.string().default('USD'),
    images: z.array(z.string()).default([]),
    category: z.string(),
    tags: z.array(z.string()).default([]),
    stock: z.number().default(0),
    featured: z.boolean().default(false),
    rating: z.number().min(0).max(5).default(0),
    createdAt: z.coerce.date(),
    updatedAt: z.coerce.date(),
    metadata: z.object({
      seoTitle: z.string().optional(),
      seoDescription: z.string().optional(),
    }).optional(),
  }),
});

// ═══════════════════════════════════════════════════════
//  3. CONTENT LAYER — from external DB or generated
// ═══════════════════════════════════════════════════════
const reviewsCollection = defineCollection({
  loader: productLoader({
    // This could be a database query, GraphQL, anything
    source: 'database',
    query: 'SELECT * FROM reviews WHERE approved = true',
  }),
  schema: z.object({
    productSlug: z.string(),
    author: z.string(),
    rating: z.number().min(1).max(5),
    body: z.string(),
    createdAt: z.coerce.date(),
  }),
});

export const collections = {
  blog: blogCollection,
  products: productsCollection,
  reviews: reviewsCollection,
};
```

### 6.3 Custom Loader Implementation

**`src/lib/cms-loader.ts`**:

```ts
import type { Loader } from 'astro/loaders';

interface CmsLoaderOptions {
  endpoint: string;
  headers?: Record<string, string>;
  transform?: (item: any) => { id: string; rawData?: any };
}

/**
 * Creates an Astro Content Layer loader that fetches from a headless CMS.
 *
 * The loader runs at BUILD TIME (in static mode) or
 * ON REQUEST (in server mode with caching).
 */
export function cmsLoader(options: CmsLoaderOptions): Loader {
  return {
    name: 'cms-loader',

    async load({ store, logger, parseData, generateDigest }) {
      logger.info(`Fetching content from: ${options.endpoint}`);

      try {
        const response = await fetch(options.endpoint, {
          headers: {
            'Content-Type': 'application/json',
            ...options.headers,
          },
        });

        if (!response.ok) {
          throw new Error(
            `CMS returned ${response.status}: ${response.statusText}`
          );
        }

        const data = await response.json();
        const items = Array.isArray(data) ? data : data.items ?? data.data ?? [];

        logger.info(`Loaded ${items.length} entries from CMS`);

        for (const item of items) {
          const transformed = options.transform
            ? options.transform(item)
            : { id: item.slug ?? item.id };

          // Store the entry in Astro's content layer
          store.set({
            id: transformed.id,
            data: item,        // Raw data — will be validated against schema
            // Optional: digest for cache invalidation
            digest: generateDigest(JSON.stringify(item)),
            // Optional: rendered HTML if the CMS provides it
            // rendered: { html: item.body_html },
          });
        }
      } catch (error) {
        logger.error(`Failed to load from CMS: ${error}`);
        throw error;
      }
    },

    // Optional: schema for the raw data before collection schema is applied
    // schema: z.object({ ... }),
  };
}
```

### 6.4 Using Content Layer Data in Pages

**`src/pages/products/index.astro`**:

```astro
---
import BaseLayout from '@layouts/BaseLayout.astro';
import { getCollection } from 'astro:content';

// ═══════════════════════════════════════════════════════
//  getCollection() works THE SAME for both local MDX
//  and content-layer collections. Type-safe either way.
// ═══════════════════════════════════════════════════════
const products = await getCollection('products', ({ data }) => {
  // Filter / sort just like local collections
  return data.stock > 0;
});

// Sort by rating
const sorted = products.sort((a, b) => b.data.rating - a.data.rating);

// Also get local blog posts
const blogPosts = await getCollection('blog', ({ data }) => !data.draft);
---

<BaseLayout title="Products">
  <h1>Our Products</h1>
  <p>{sorted.length} products available</p>

  <div class="product-grid">
    {sorted.map(product => (
      <a href={`/products/${product.data.slug}`} class="product-card">
        <img
          src={product.data.images[0] ?? '/placeholder.png'}
          alt={product.data.name}
        />
        <h3>{product.data.name}</h3>
        <p class="price">${product.data.price} {product.data.currency}</p>
        <span class="rating">★ {product.data.rating}/5</span>
        {product.data.stock < 10 && (
          <span class="low-stock">Only {product.data.stock} left!</span>
        )}
      </a>
    ))}
  </div>
</BaseLayout>
```

### 6.5 Content Layer with Incremental Builds

The Content Layer API caches loader results, so subsequent builds only fetch changed entries:

```ts
// src/lib/cms-loader.ts (extended)
export function cmsLoader(options: CmsLoaderOptions): Loader {
  return {
    name: 'cms-loader',

    async load({ store, logger, parseData, generateDigest, meta }) {
      // meta contains previous build state for incremental fetching
      const lastBuild = meta.get('lastBuild');
      const endpoint = lastBuild
        ? `${options.endpoint}?updated_since=${lastBuild}`
        : options.endpoint;

      logger.info(`Fetching from: ${endpoint}`);
      const response = await fetch(endpoint, {
        headers: options.headers,
      });

      const data = await response.json();
      const items = Array.isArray(data) ? data : data.items ?? [];

      for (const item of items) {
        store.set({
          id: item.slug ?? item.id,
          data: item,
          digest: generateDigest(JSON.stringify(item)),
        });
      }

      // Store build timestamp for next incremental fetch
      meta.set('lastBuild', new Date().toISOString());
    },
  };
}
```

### 6.6 Content Layer + ISR (Cache Tags)

```astro
---
// src/pages/products/[slug].astro
import { getEntry } from 'astro:content';

const { slug } = Astro.params;
const product = await getEntry('products', slug!);

if (!product) {
  return Astro.redirect('/404');
}

// ═══════════════════════════════════════════════════════
//  Set cache tags for on-demand ISR
// ═══════════════════════════════════════════════════════
Astro.response.headers.set(
  'Cache-Control',
  'public, max-age=0, s-maxage=3600, stale-while-revalidate=86400'
);
// Tag this page so it can be purged by tag
Astro.response.headers.set('CDN-Cache-Control', 'public, max-age=3600');
Astro.response.headers.set(
  'Cache-Tag',
  `product:${slug},products,page:product`
);
---

<BaseLayout title={product.data.name}>
  <h1>{product.data.name}</h1>
  <!-- ... -->
</BaseLayout>
```

---

## 7. On-Demand ISR with Adapters

### Concept

**Incremental Static Regeneration (ISR)** lets you cache statically-rendered pages at the CDN/edge and revalidate them **on demand** — without rebuilding the entire site. Astro 5.x + adapters (Vercel, Netlify, Cloudflare) support:

- **Time-based ISR**: `s-maxage` / `stale-while-revalidate` headers
- **On-demand ISR**: API endpoint triggers revalidation via cache tags or paths
- **Cache tags**: Associate pages with tags (e.g., `product:laptop`) for surgical purging
- **Bypass tokens**: Regenerate stale content programmatically

### 7.1 Adapter Configuration for ISR

**Vercel** (`astro.config.mjs` excerpt):

```js
adapter: vercel({
  isr: {
    expiration: 60 * 60,         // 1 hour
    bypassToken: import.meta.env.VERCEL_BYPASS_TOKEN,
    // Optional: allow query params for bypass
    allowQuery: ['x-vercel-protection-bypass'],
  },
  edgeMiddleware: true,
}),
```

**Netlify** (`astro.config.mjs` excerpt):

```js
adapter: netlify({
  cacheOnDemandPages: true,
  // Pages with Cache-Control headers will be ISR'd automatically
}),
```

**Cloudflare** (`astro.config.mjs` excerpt):

```js
adapter: cloudflare({
  routes: {
    strategy: 'auto',
    // ISR via Cache API
  },
}),
```

### 7.2 Time-Based ISR (Automatic)

```astro
---
// src/pages/products/[slug].astro
export const prerender = false;

// ═══════════════════════════════════════════════════════
//  TIME-BASED ISR — revalidates every hour
// ═══════════════════════════════════════════════════════
Astro.response.headers.set(
  'Cache-Control',
  'public, max-age=0, s-maxage=3600, stale-while-revalidate=86400'
);
// s-maxage=3600      → CDN caches for 1 hour
// stale-while-revalidate=86400 → serve stale for 24h while
//                                  regenerating in background
---

<div>This page ISRs every hour automatically.</div>
```

### 7.3 On-Demand ISR Endpoint

**`src/pages/api/revalidate.ts`** — the revalidation API:

```ts
import type { APIRoute } from 'astro';

// ═══════════════════════════════════════════════════════
//  ON-DEMAND ISR ENDPOINT
//  POST /api/revalidate
//  Headers: Authorization: Bearer <REVALIDATION_SECRET>
//  Body: { tags?: string[], paths?: string[] }
// ═══════════════════════════════════════════════════════
export const POST: APIRoute = async ({ request }) => {
  // ── Auth check ──────────────────────────────────────
  const authHeader = request.headers.get('Authorization');
  const secret = import.meta.env.REVALIDATION_SECRET;

  if (!authHeader || authHeader !== `Bearer ${secret}`) {
    return new Response(JSON.stringify({ error: 'Unauthorized' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    const body = await request.json();
    const { tags = [], paths = [] } = body;

    const results: string[] = [];

    // ── Revalidate by cache tag ───────────────────────
    for (const tag of tags) {
      // This endpoint varies by adapter.
      // Vercel: use their API to purge by tag
      if (import.meta.env.VERCEL_URL) {
        await fetch(
          `https://api.vercel.com/v1/edge-config/${import.meta.env.VERCEL_EDGE_CONFIG}/items?tag=${tag}`,
          {
            method: 'PATCH',
            headers: { Authorization: `Bearer ${import.meta.env.VERCEL_TOKEN}` },
          }
        );
      }
      results.push(`tag:${tag}`);
    }

    // ── Revalidate by path ────────────────────────────
    for (const path of paths) {
      const url = new URL(path, Astro.url.origin);
      // Fetch with x-prerender-revalidate header
      await fetch(url.toString(), {
        headers: {
          'x-prerender-revalidate': import.meta.env.VERCEL_BYPASS_TOKEN,
        },
      });
      results.push(`path:${path}`);
    }

    return new Response(
      JSON.stringify({
        revalidated: true,
        items: results,
        timestamp: new Date().toISOString(),
      }),
      {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ revalidated: false, error: String(error) }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
};
```

### 7.4 CMS Webhook → ISR Trigger

**`src/pages/api/webhook.ts`**:

```ts
import type { APIRoute } from 'astro';

// ═══════════════════════════════════════════════════════
//  CMS WEBHOOK ENDPOINT
//  POST /api/webhook
//  Receives content change notifications from your CMS.
//  Extracts cache tags and triggers ISR revalidation.
// ═══════════════════════════════════════════════════════
export const POST: APIRoute = async ({ request }) => {
  const signature = request.headers.get('x-webhook-signature');

  // Verify webhook signature (implement per your CMS)
  if (!verifyWebhookSignature(signature, await request.clone().text())) {
    return new Response('Invalid signature', { status: 401 });
  }

  const body = await request.json();
  // Expected format: { event: 'product.updated', data: { slug: 'laptop' } }

  const tags: string[] = [];

  switch (body.event) {
    case 'product.created':
    case 'product.updated':
    case 'product.deleted':
      if (body.data?.slug) {
        tags.push(`product:${body.data.slug}`);
        tags.push('products');
        tags.push('page:product');
      }
      break;

    case 'category.updated':
      tags.push(`category:${body.data?.slug ?? 'all'}`);
      tags.push('products');
      break;

    case 'site.settings_updated':
      // Purge all pages
      tags.push('all');
      break;

    default:
      return new Response(JSON.stringify({ skipped: true }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
  }

  // Call revalidation endpoint
  const revalidateUrl = new URL('/api/revalidate', request.url);
  const revalidateResponse = await fetch(revalidateUrl.toString(), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${import.meta.env.REVALIDATION_SECRET}`,
    },
    body: JSON.stringify({ tags }),
  });

  const result = await revalidateResponse.json();

  return new Response(JSON.stringify(result), {
    status: revalidateResponse.status,
    headers: { 'Content-Type': 'application/json' },
  });
};

function verifyWebhookSignature(sig: string | null, body: string): boolean {
  if (!sig) return false;
  // Implement HMAC validation per your CMS
  // Example: crypto.createHmac('sha256', secret).update(body).digest('hex')
  return true; // placeholder
}
```

### 7.5 Cache Tag Utilities

**`src/lib/cache-tags.ts`**:

```ts
/**
 * Standardized cache tag generation.
 * Use these in Astro.response.headers.set('Cache-Tag', ...)
 */

export function productTag(slug: string): string {
  return `product:${slug}`;
}

export function categoryTag(slug: string): string {
  return `category:${slug}`;
}

export function pageTag(name: string): string {
  return `page:${name}`;
}

export function collectionTag(name: string): string {
  return `collection:${name}`;
}

/**
 * Build a Cache-Tag header value from an array of tags.
 */
export function cacheTagHeader(...tags: string[]): string {
  return tags.filter(Boolean).join(',');
}

/**
 * Pages that should be purged when a product changes.
 */
export function productInvalidationTags(slug: string): string {
  return cacheTagHeader(
    productTag(slug),
    collectionTag('products'),
    pageTag('product'),
    pageTag('home')
  );
}
```

### 7.6 Putting It All Together — ISR Product Page

```astro
---
// src/pages/products/[slug].astro
import BaseLayout from '@layouts/BaseLayout.astro';
import ProductPrice from '@components/server/ProductPrice.server.astro';
import { getEntry } from 'astro:content';
import { productInvalidationTags } from '@lib/cache-tags';

export const prerender = false;

const { slug } = Astro.params;
const product = await getEntry('products', slug!);

if (!product) {
  return new Response(null, { status: 404 });
}

// ═══════════════════════════════════════════════════════
//  ISR HEADERS — time-based + cache tags for on-demand
// ═══════════════════════════════════════════════════════
Astro.response.headers.set(
  'Cache-Control',
  'public, max-age=0, s-maxage=3600, stale-while-revalidate=86400'
);
Astro.response.headers.set(
  'Cache-Tag',
  productInvalidationTags(slug!)
);

// For Vercel specifically:
if (import.meta.env.VERCEL_URL) {
  Astro.response.headers.set(
    'CDN-Cache-Control',
    'public, max-age=3600, stale-while-revalidate=86400'
  );
}
---

<BaseLayout
  title={product.data.metadata?.seoTitle ?? product.data.name}
  description={product.data.metadata?.seoDescription ?? product.data.description}
>
  <!-- Static shell — cached at CDN -->
  <article class="product-detail">
    <div class="product-hero">
      <img src={product.data.images[0]} alt={product.data.name} />
      <div class="product-info">
        <h1>{product.data.name}</h1>
        <p>{product.data.description}</p>

        <!-- Server island — dynamic price, NOT cached -->
        <ProductPrice productId={product.data.slug} server:defer />

        <!-- Rating -->
        <div class="rating">
          {'★'.repeat(Math.round(product.data.rating))}
          {'☆'.repeat(5 - Math.round(product.data.rating))}
          <span class="text-sm text-gray-500">
            ({product.data.rating}/5)
          </span>
        </div>

        <!-- Stock badge -->
        {product.data.stock > 0 ? (
          <span class="in-stock">✓ In Stock ({product.data.stock})</span>
        ) : (
          <span class="out-of-stock">✕ Out of Stock</span>
        )}
      </div>
    </div>
  </article>
</BaseLayout>
```

### 7.7 ISR Flow Diagram

```
CMS Content Update
        │
        ▼
POST /api/webhook
  (verifies signature)
        │
        ▼
POST /api/revalidate
  { tags: ['product:laptop', 'products', 'page:product'] }
        │
        ▼
┌─────────────────────────────────────────────┐
│  Adapter (Vercel / Netlify / Cloudflare)    │
│  Purges CDN cache for matching cache tags   │
└─────────────────────────────────────────────┘
        │
        ▼
Next request to /products/laptop
        │
        ▼
┌─────────────────────────────────────────────┐
│  CDN cache MISS → origin server             │
│  Renders fresh page with latest content     │
│  Sets Cache-Tag + Cache-Control headers     │
│  CDN caches new version                     │
└─────────────────────────────────────────────┘
```

---

## 8. Integration: All Patterns Combined

### 8.1 The Complete Product Page

This page combines **all five** advanced patterns:

```astro
---
// src/pages/products/[slug].astro
import BaseLayout from '@layouts/BaseLayout.astro';
import { getEntry } from 'astro:content';
import { productInvalidationTags } from '@lib/cache-tags';

// Server Islands
import ProductPrice from '@components/server/ProductPrice.server.astro';
import PersonalizedRecommendations from '@components/server/PersonalizedRecommendations.server.astro';

// Streaming
import CommentSection from '@components/streaming/CommentSection.astro';

// Client Islands (consume nanostores)
import CartButton from '@components/react/CartButton';
import ProductFilter from '@components/svelte/ProductFilter.svelte';

export const prerender = false;

const { slug } = Astro.params;

// Content Layer — fetches from CMS via loader (section 6)
const product = await getEntry('products', slug!);
if (!product) return new Response(null, { status: 404 });

// ISR Headers (section 7)
Astro.response.headers.set(
  'Cache-Control',
  'public, max-age=0, s-maxage=3600, stale-while-revalidate=86400'
);
Astro.response.headers.set('Cache-Tag', productInvalidationTags(slug!));

// Streaming (section 4)
Astro.response.headers.set('Transfer-Encoding', 'chunked');
---

<BaseLayout title={product.data.name}>
  <!-- ================================================ -->
  <!--  STATIC SHELL — cached + instant                 -->
  <!-- ================================================ -->
  <article class="product-detail">
    <h1>{product.data.name}</h1>
    <div class="product-body">
      <img src={product.data.images[0]} alt={product.data.name} />
      <p>{product.data.description}</p>
    </div>

    <!-- ================================================ -->
    <!--  SERVER ISLAND — price from DB (section 3)       -->
    <!-- ================================================ -->
    <ProductPrice productId={slug!} server:defer />

    <!-- ================================================ -->
    <!--  CLIENT ISLAND — nanostores cart (section 5)     -->
    <!-- ================================================ -->
    <CartButton
      client:load
      productId={slug!}
      productName={product.data.name}
    />

    <!-- ================================================ -->
    <!--  CLIENT ISLAND — filtering with nanostores       -->
    <!-- ================================================ -->
    <ProductFilter client:visible />

    <!-- ================================================ -->
    <!--  SERVER ISLAND — ML recommendations (section 3)  -->
    <!-- ================================================ -->
    <PersonalizedRecommendations productId={slug!} server:defer />

    <!-- ================================================ -->
    <!--  STREAMING — comments load last (section 4)      -->
    <!-- ================================================ -->
    <CommentSection productId={slug!} />
  </article>
</BaseLayout>
```

### 8.2 Performance Budget

| Section | Render Time | Strategy |
|---------|:---:|----------|
| `<head>` + shell | ~40ms | Static, streamed first chunk |
| Product hero | ~80ms | Static, in shell |
| ProductPrice | 200–500ms | Server Island (deferred) |
| CartButton | ~50ms | Client Island (React) |
| Recommendations | 400–800ms | Server Island (deferred) |
| Comments | 500–1000ms | Streamed (last chunk) |
| **Time-to-Interactive** | **~150ms** | Shell + critical islands |
| **Full Page Load** | **~1200ms** | All sections complete |

---

## 9. Comparison: c1 (Basic) vs c2 (Advanced)

| Feature | c1 (Basic) | c2 (Advanced) |
|---------|-----------|---------------|
| **Rendering** | Static + Hybrid SSR | Full SSR + Streaming |
| **Interactive components** | Basic islands (`client:load`) | Islands + Server Islands |
| **State management** | Per-component | nanostores (cross-framework) |
| **Content source** | Local MDX only | Content Layer API (CMS, DB, API) |
| **Caching** | None | Time-based + On-demand ISR |
| **Server access** | Build-time only | `Astro.request`, cookies, auth |
| **Page load strategy** | All-or-nothing | Progressive (streaming + deferred) |
| **Cache invalidation** | Full rebuild | Surgical (cache tags) |
| **Complexity** | Low | High |

---

## 10. ADR: Architecture Decision Records

### ADR-002: Server Islands for Dynamic Content

**Decision**: Use Server Islands (`server:defer`) for any component that needs server-side data (pricing, recommendations, user-specific content).

**Rationale**:
- Static shell loads in < 100ms (great for SEO + UX)
- Server-only code never ships to the client (zero JS for these components)
- Personalized content without blocking the page
- Built-in fallback skeletons provide immediate visual feedback

### ADR-003: nanostores for Cross-Framework State

**Decision**: Use nanostores as the single shared state layer for all interactive islands.

**Rationale**:
- Framework-agnostic (works with React, Svelte, Vue, vanilla)
- Tiny (< 250 bytes) — doesn't bloat bundles
- Built-in localStorage persistence (`@nanostores/persistent`)
- Computed stores for derived values (cart total, count)
- Single source of truth prevents state inconsistencies

### ADR-004: Content Layer API for External Data

**Decision**: Use the Content Layer API with custom loaders for all external data sources (CMS, DB).

**Rationale**:
- Type-safe collections regardless of data source
- Incremental builds (only fetch changed content)
- Unified API (`getCollection`, `getEntry`) for local + remote content
- Loaders run at build time or request time depending on output mode
- Cache tag integration for ISR

### ADR-005: On-Demand ISR with Cache Tags

**Decision**: Implement on-demand ISR via `/api/revalidate` endpoint and cache tags, triggered by CMS webhooks.

**Rationale**:
- Immediate content updates without full rebuilds
- Surgical cache invalidation (only affected pages regenerate)
- CDN-edge caching with `stale-while-revalidate` for zero-downtime updates
- Webhook-driven automation (CMS change → ISR purge → fresh content)

---

## 11. Troubleshooting & Gotchas

### Server Islands

- **Symptom**: Server island never loads; skeleton persists.
  **Fix**: Ensure `output: 'server'` (or `'hybrid'` with `prerender = false`) in `astro.config.mjs`. Server islands require SSR.

- **Symptom**: `Astro.request` is undefined in server island.
  **Fix**: Only `server:defer` components have access. Check `export const server = 'defer' as const;`.

- **Symptom**: Server island content is stale.
  **Fix**: Lower the ISR `s-maxage` value, or use cache tags + on-demand revalidation.

### Streaming

- **Symptom**: No streaming; page loads all at once.
  **Fix**: Ensure `Transfer-Encoding: chunked` is set. Some adapters/CDNs buffer the response — check adapter docs for streaming support.

- **Symptom**: SEO meta tags missing.
  **Fix**: The `<head>` is always sent in the first chunk. Don't place meta tags inside streaming sections.

### nanostores

- **Symptom**: Stores reset on navigation.
  **Fix**: Use `@nanostores/persistent` (`persistentAtom`, `persistentMap`) for localStorage-backed persistence. Plain `atom`/`map` are in-memory only.

- **Symptom**: Store value is stale in React.
  **Fix**: Use `useStore()` from `@nanostores/react`, not `.get()` directly. `useStore` subscribes to changes.

### Content Layer

- **Symptom**: `getCollection` returns empty for content layer collection.
  **Fix**: Check that the loader's `store.set()` is called with the correct `id` and `data` fields. Enable debug logging: `logger.info(...)`.

- **Symptom**: Types not generated for content layer collections.
  **Fix**: Run `astro sync` after modifying `config.ts`. Types for content layer entries are inferred from Zod schemas.

### On-Demand ISR

- **Symptom**: Pages don't update after revalidation.
  **Fix**: Check that `Cache-Tag` headers match the tags sent to `/api/revalidate`. Verify the bypass token is correct for your adapter.

- **Symptom**: ISR but always getting stale content.
  **Fix**: Ensure `stale-while-revalidate` is set. Without it, the CDN returns stale content until `s-maxage` expires.

---

## 12. Quick-Start Script

```bash
# 1. Create the project
npm create astro@latest advanced-astro-site -- \
  --template minimal \
  --install \
  --typescript strict

cd advanced-astro-site

# 2. Install advanced dependencies
npm install \
  @astrojs/vercel \
  @astrojs/react @astrojs/svelte \
  @astrojs/mdx @astrojs/sitemap \
  nanostores @nanostores/react @nanostores/persistent \
  react react-dom svelte zod

# 3. Add adapter to astro.config.mjs (see section 2.1)

# 4. Create server island
mkdir -p src/components/server
# Copy ProductPrice.server.astro (section 3.2)

# 5. Create nanostores
mkdir -p src/components/state
# Copy cartStore.ts (section 5.1)

# 6. Create content layer loader
mkdir -p src/lib
# Copy cms-loader.ts (section 6.3)

# 7. Create ISR endpoint
mkdir -p src/pages/api
# Copy revalidate.ts (section 7.3)

# 8. Set environment variables
cat > .env << 'EOF'
CMS_API_URL=https://your-cms.example.com/api
CMS_API_TOKEN=your-token
REVALIDATION_SECRET=your-secret
VERCEL_BYPASS_TOKEN=your-bypass-token
EOF

# 9. Develop
npm run dev

# 10. Build & Deploy
npm run build
# Deploy to Vercel/Netlify/Cloudflare
```

---

## 13. References

- [Astro Server Islands Docs](https://docs.astro.build/en/guides/server-islands/)
- [Astro Streaming SSR Guide](https://docs.astro.build/en/guides/streaming/)
- [nanostores Documentation](https://github.com/nanostores/nanostores)
- [Astro Content Layer API](https://docs.astro.build/en/guides/content-collections/#the-content-layer)
- [Astro Content Loaders](https://docs.astro.build/en/reference/content-loader-reference/)
- [Vercel ISR with Astro](https://docs.astro.build/en/guides/integrations-guide/vercel/)
- [Netlify On-Demand Builders](https://docs.astro.build/en/guides/integrations-guide/netlify/)
- [Astro Adapter API](https://docs.astro.build/en/reference/adapter-reference/)
- [Web APIs: Transfer-Encoding](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Transfer-Encoding)
- [Cache-Control Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)
