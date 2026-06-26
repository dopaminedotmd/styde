app router directory structure:
/ (app)
  layout.tsx           root layout, html/body, providers
  page.tsx             entry /
  loading.tsx          root suspense fallback
  error.tsx            root error boundary
  not-found.tsx        404
  /(auth)
    login/page.tsx
    register/page.tsx
    layout.tsx          auth-specific layout, no sidebar
  /(dashboard)
    layout.tsx          sidebar, header, session check
    page.tsx            dashboard overview
    /settings/page.tsx
    /teams
      page.tsx          team list
      [teamId]/page.tsx team detail, generateStaticParams for ISR
  /api
    /trpc/[trpc]/route.ts  tRPC or REST handlers
    /revalidate/route.ts   on-demand ISR webhook
  /blog
    page.tsx            static generation
    [slug]/page.tsx     dynamic paths, generateStaticParams, revalidate: 3600
react server components:
default all components are RSC. 'use client' only for interactivity.
server components fetch directly, no useEffect.
server component pattern:
  async function Page({ params }) {
    const data = await fetch(url, { next: { revalidate: 60 } })
    return <Suspense fallback={<Skeleton />}>
      <ClientWrapper data={data} />
    </Suspense>
  }
keep data fetching in RSC. pass serializable props to client.
avoid 'use client' on layout — children stay server-renderable.
streaming with suspense:
wrap slow async children in Suspense boundaries.
layout.tsx defines loading.tsx as root Suspense fallback.
inner components get granular Suspense.
pattern:
  <Suspense fallback={<Spinner />}>
    <SlowComponent /> // this is an async RSC
  </Suspense>
each Suspense boundary is an independent stream chunk.
use loading.tsx for route-level, Suspense for component-level.
incremental static regeneration (ISR):
export const revalidate = 3600 // time-based, seconds
or individual fetch:
  fetch(url, { next: { revalidate: 3600 } })
on-demand ISR (from webhook or admin action):
  import { revalidatePath, revalidateTag } from 'next/cache'
  revalidatePath('/blog/[slug]')
  revalidateTag('posts')
trigger from api/revalidate/route.ts with a secret token.
edge middleware:
file: middleware.ts at app root (or src/)
export { auth as middleware } from '@/lib/auth'
or custom:
  import { NextResponse } from 'next/server'
  import type { NextRequest } from 'next/server'
  export function middleware(request: NextRequest) {
    const token = request.cookies.get('session')
    if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
    return NextResponse.next()
  }
  export const config = {
    matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
  }
match array for performance. avoid running middleware on static assets.
route handlers:
app/api/route.ts
  export async function GET(request: NextRequest) {
    return Response.json({ ok: true })
  }
access searchParams via request.nextUrl.searchParams.
streaming response:
  const stream = new ReadableStream(...)
  return new Response(stream)
cache strategy:
static render default for pages. dynamic = 'force-dynamic' for per-request.
fetch cache: 'force-cache' (default), 'no-store' for dynamic.
revalidateTag for granular cache busting.
stale-while-revalidate via revalidate export.
performance rules:
move all data fetching to RSC. never fetch in client components.
co-locate queries with the page that needs them.
use React.cache() to deduplicate same fetch across parent/child RSC.
keep client bundle small: import heavy libs only in RSC.
Streaming means first paint is not blocked by slow backend calls.