DIGITAL MATURITY AUDIT REPORT
Nous Research — nousresearch.com
Audit date: 2026-06-26
OVERVIEW
nousresearch.com is the corporate website for Nous Research, an open-source AI research lab. The site consists of a WordPress+Elementor main domain served via Vercel, plus a Next.js subdomain for Hermes Agent (hermes-agent.nousresearch.com). Total sitemap entries: 39 pages.
TECH STACK (detected from HTTP headers + HTML source)
platform: WordPress 6.9.4 on Vercel
builder: Elementor 3.25.6 (Pro)
theme: Hello Elementor
cdn: Vercel Edge Network
hosting: Vercel (server header: Vercel)
analytics: Google Analytics (GT-PBN55BH6)
seo: Yoast SEO 23.8
search: Ajax Search Lite (wpdreams)
icons: Font Awesome 6.5.1
performance: font-display:swap, image lazy-loading, preconnect hints
email: Cloudflare Email Protection (obfuscated)
js: jQuery 3.x, Elementor frontend, SmartMenus
external: HuggingFace, Discord, LinkedIn, Twitter/X, GitHub, Shop
DIMENSION SCORES
tech_stack_score: 78
  Strong: Modern WordPress, Elementor Pro, Vercel CDN, Cloudflare.
  Weak: WordPress is a heavy CMS for a simple content site. 20+ CSS files loaded per page. jQuery still in use.
security_score: 72
  Strong: HSTS enabled (63072000s, 2-year max-age). wp-admin returns 403 for unauthenticated. Cloudflare bot mitigation active. No exposed .env or git.
  Critical gaps: No Content-Security-Policy header. No X-Frame-Options header. No Permissions-Policy header. No Referrer-Policy header. No X-Content-Type-Options. No Cache-Control for sensitive admin routes is correct but main pages have max-age=0 (forces revalidation on every request).
seo_score: 85
  Strong: Yoast SEO 23.8 with full schema.org/WebPage + schema.org/Organization markup. Proper OG and Twitter Card meta. Sitemap.xml with all 39 pages. Robots.txt open with Allow:/. Canonical URLs on every page. Meta descriptions present.
  Weak: Blog subpages redirect instead of serving content properly. No hreflang (English only, acceptable). BreadcrumbList schema present but minimalist.
performance_score: 68
  Strong: Vercel CDN edge caching. WebP images. Font-display:swap. Lazy-loading via IntersectionObserver. Preconnect to Google Fonts and Font Awesome.
  Critical issues: 76KB+ HTML payload on homepage. 20+ CSS files. 15+ JavaScript files. No HTTP/2 push. Page loads jQuery, Elementor, Elementor Pro, Yoast JS, Google Analytics, Ajax Search Lite, SmartMenus, Font Awesome, Google Fonts — 9+ third-party origins. Elementor frontend alone is ~200KB JS. Cache-Control: public, max-age=0 forces revalidation on every visit.
accessibility_score: 55
  Strong: Responsive viewport meta. Proper lang=en-US. Some ARIA labels in Elementor nav. Color contrast in main theme adequate.
  Weak: No skip-to-content link found. Popup menus use aria-hidden for decorative elements but navigation uses aria-current inconsistently. Images in hero have no alt text on decorative ones (good) but feature images use blank alt when they convey information. No visible focus indicators. No semantic landmark structure beyond nav/main. Keyboard navigation depends on Elementor defaults.
mobile_readiness_score: 82
  Strong: Responsive design via viewport meta and Elementor breakpoints (mobile 767px, tablet 1024px). Mobile menu popup exists. Font sizes use clamp() and viewport-relative units. Hero adapts to mobile layout.
  Weak: 88dvh hero section may clip on some browsers. No dedicated mobile navigation strategy beyond hamburger. Touch targets adequate but not oversized.
OVERALL MATURITY SCORE: 73 / 100
CRITICAL FINDINGS (priority order)
1. MISSING SECURITY HEADERS (priority: critical)
   X-Frame-Options: DENY — missing. Clickjacking risk.
   Content-Security-Policy — missing. XSS risk from inline scripts.
   Permissions-Policy — missing. No camera/mic/geolocation restrictions.
   Referrer-Policy — missing. Referrer leakage possible.
   X-Content-Type-Options: nosniff — missing. MIME sniffing risk.
   Remedy: Add via Vercel vercel.json headers config or Cloudflare transform rules.
2. EXCESSIVE JS/CSS BLOAT (priority: high)
   20+ external CSS files, 15+ JS files on homepage. Total transfer >300KB render-blocking.
   jQuery + Elementor (both Core and Pro) + Yoast + Ajax Search Lite + Font Awesome + SmartMenus.
   Remedy: Dequeue unused Elementor assets per-page. Replace Font Awesome with SVG sprites. Use Asset Cleanup or Perfmatters plugin. Lazy-load below-fold JS.
3. NO PERFORMANCE BUDGET (priority: medium)
   Homepage HTML is 76KB. Max-age=0 forces revalidation on every hit.
   Vercel CDN caches but Cache-Control header is suboptimal.
   Remedy: Set Cache-Control: public, max-age=3600, stale-while-revalidate=86400. Consider SSG/ISR like the Hermes Agent subdomain already uses Next.js.
4. ACCESSIBILITY GAPS (priority: medium)
   No skip-to-content link. No visible focus outlines. Feature images lack descriptive alt text.
   Elementor nav uses aria-current on current page item but other landmarks are implicit.
   Remedy: Add skip-link, set outline:2px on :focus-visible, audit alt-text on all images.
5. SEO SUBPAGE ISSUES (priority: medium)
   Blog and releases pages serve content but blog category/archive URLs redirect. No pagination markup.
   Remedy: Ensure all blog URLs serve content directly. Add rel=prev/next on paginated archives.
RECOMMENDATIONS SUMMARY
short-term (1 week):
  Add 5 missing security headers via vercel.json
  Set Cache-Control to enable browser caching
  Add skip-to-content link and focus styles
medium-term (1 month):
  Audit and dequeue unused Elementor assets per page
  Replace Font Awesome with inline SVGs
  Implement lazy-load for below-fold JS bundles
long-term (3 months):
  Migrate from WordPress to Next.js (align with Hermes Agent subdomain)
  Implement full CSP with strict-dynamic
  Build automated Lighthouse CI into deployment pipeline
COMPETITOR LANDSCAPE NOTE
This site performs adequately for a research org website. Compared to peers:
  vs. Anthropic (anthropic.com): Lacks their minimal JS footprint and aggressive caching.
  vs. OpenAI (openai.com): Comparable WordPress dependency but fewer security headers.
  vs. Meta AI: Better CDN strategy (Vercel vs. Meta's custom infra). Worse accessibility.
  Hermes Agent subdomain aligns better with industry standards (Next.js, strict CSP-ish via inline styles, modern font loading).