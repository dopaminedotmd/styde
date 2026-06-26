app/ layout.tsx (root layout with html/body, fonts, metadata)
app/ (segment-name)/ page.tsx (RSC — fetch + render)
app/ (segment-name)/ loading.tsx (Suspense fallback)
app/ (segment-name)/ error.tsx (error boundary, client component)
app/ (segment-name)/ layout.tsx (nested layout when needed)
app/ (segment-name)/ not-found.tsx (404 boundary)
app/ api/ (route)/ route.ts (route handlers, no RSC)
app/ (auth)/ login/ page.tsx (grouped routes, no path prefix)
Middleware at src/middleware.ts — runs on every matched route. Export config.matcher to narrow. Use NextResponse.rewrite/redirect. Check cookies/tokens before layout renders. Cannot read local state — only request/response primitives.
Streaming pattern: parent page fetches slow data, wraps children in <Suspense fallback={<Loading />}>. Children are async RSC components doing individual fetches. Each Suspense boundary yields independently. loading.tsx is the automatic boundary for a segment.
ISR: export const revalidate = 3600 (seconds). Or fetch(url, { next: { revalidate: 3600 } }). fetch caching is default-on in App Router. Revalidation is time-based, not webhook-driven unless you call revalidatePath/revalidateTag in a route handler.
RSC rule: only Server Components fetch data. Client components (marked with 'use client') render on client — don't pass server data through them unless serialised. Props from RSC to client are serialised JSON at build/request time.
Route handlers (app/api/ route.ts) replace pages/api. Use NextRequest/NextResponse. Edge runtime: export const runtime = 'edge'. Edge supports fewer Node APIs but lower latency.