app/
├── (marketing)/
│   ├── page.tsx                    # RSC — static landing, ISR revalidate=3600
│   ├── loading.tsx                 # Suspense fallback for page shell
│   └── blog/
│       ├── [slug]/
│       │   ├── page.tsx            # generateStaticParams + revalidate=60
│       │   └── loading.tsx
│       └── page.tsx                # stream latest posts via <Suspense>
│           └── posts-list.tsx      # async RSC — fetches, streams in
├── (dashboard)/
│   ├── layout.tsx                  # checks session — RSC reads cookie
│   ├── page.tsx                    # guarded — redirects if no session
│   └── settings/
│       └── page.tsx                # form — client component boundary
├── api/
│   ├── revalidate/
│   │   └── route.ts               # POST route handler — on-demand ISR
│   └── webhook/
│       └── route.ts               # Edge runtime — stripe/webhook
├── middleware.ts                   # Edge — reads cookie, rewrites /app to /dashboard
└── layout.tsx                      # root layout — wraps <Suspense><Shell />
middleware.ts:
export { default } from 'next-auth/middleware'
export const config = { matcher: ['/dashboard/:path*'] }
blog/[slug]/page.tsx:
export const revalidate = 60                        # ISR — stale-while-revalidate
export async function generateStaticParams() { ... }  # build-time paths
export default async function Page({ params }) {      # RSC
  const post = await db.post.findUnique(params.slug)  # direct DB — no API layer
  return <PostBody html={post.content} />              # streams via Suspense parent
}
blog/page.tsx:
export default function Page() {
  return (
    <Suspense fallback={<Skeleton />}>
      <PostsList />
    </Suspense>
  )                                                  # streaming SSR — shell renders
}                                                     # immediately, PostsList streams in
api/revalidate/route.ts:
import { revalidatePath } from 'next/cache'
export async function POST(req) {
  const body = await req.json()
  revalidatePath(`/blog/${body.slug}`)
  return Response.json({ revalidated: true })
}
Key decisions:
- RSC by default — only sprinkle 'use client' when interactive (forms, clicks, state)
- Suspense boundaries at page layout level — not inside every component
- ISR over SSR for read-heavy public routes — stale-while-revalidate pattern
- Middleware runs at edge — keep it thin (cookie check + rewrite), no DB calls
- Route handlers in app dir — file-based, no separate pages/api directory
- Data fetching in RSC — direct DB/ORM calls, not fetch wrappers that add N+1