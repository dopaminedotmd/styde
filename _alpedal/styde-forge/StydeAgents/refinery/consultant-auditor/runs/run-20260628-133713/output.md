target: nousresearch.com
company: Nous Research
url: https://nousresearch.com/
timestamp: 2026-06-28T13:42:00Z
tech_stack:
  cms: wordpress 6.9.4
  page_builder: elementor 3.25.6
  elementor_pro: true
  hosting: vercel (cdn edge)
  dns: cloudflare
  ssl_issuer: lets_encrypt (valid thru 2026-08-29)
  seo_plugin: yoast 23.8
  analytics: google analytics via site kit 1.139.0
  fonts: google fonts (courier prime, geist, geist mono, open sans)
  icons: fontawesome 6.5.1
  search: ajax search lite
  math_rendering: mathjax
  code_highlighting: prism.js
  tables: tablepress
  pdf_viewer: embed pdf viewer
  javascript: jquery 3.x
security: 45/100
  findings:
    - strict-transport-security: present, max-age=63072000 (good)
    - x-frame-options: MISSING (risk: clickjacking)
    - x-content-type-options: MISSING (risk: mime sniffing)
    - content-security-policy: MISSING (risk: xss)
    - referrer-policy: MISSING (risk: referrer leakage)
    - permissions-policy: MISSING (risk: browser features unobstructed)
    - server_header: vercel (acceptable, does not leak version)
  severity: critical
  recommendation: add x-frame-options, x-content-type-options, and csp headers via vercel.json or _headers
performance: 72/100
  findings:
    - ttfb: 89ms (excellent, edge caching via vercel)
    - total_load: 102ms from cache
    - page_size: 76kb html
    - total_external_resources: 26 css + js files (heavy; elementor bloat)
    - external_domains: 21 unique third-party domains
    - image_formats: 9 png, 8 webp, 2 svg (good mix but png should be webp/avif)
    - html_size_raw: 76131 bytes
    - inline_css_volume: extremely heavy (wordpress block styles + elementor inline)
  severity: major
  recommendation: reduce css bundle count via elementor asset optimization, convert remaining png to webp, defer third-party scripts
seo: 85/100
  findings:
    - title_tag: present, descriptive "NOUS RESEARCH - Open Source AI"
    - meta_description: present, well-crafted
    - canonical_url: present on all pages
    - opengraph: complete (title, description, image, url, type)
    - twitter_cards: present (summary_large_image)
    - sitemap: present, 38 urls, well-structured
    - robots.txt: present, allows all crawlers
    - schema_markup: yoast json-ld with organization, webpage, website types
    - breadcrumbs: schema-level breadcrumbs present
    - blog: 17+ posts, recent content
    - hreflang: absent (single-language site, acceptable for english-only)
    - broken_links_check: not performed (would require deeper crawl)
  severity: minor
  recommendation: add article schema to blog posts, consider faq schema for product pages
mobile_readiness: 78/100
  findings:
    - viewport_meta: present (width=device-width, initial-scale=1)
    - responsive_framework: elementor with breakpoints for desktop, laptop, tablet, mobile
    - mobile_navigation: hamburger/ellipsis menu for mobile + tablet
    - popup_mobile_menu: separate elementor popup for mobile/tablet
    - touch_targets: not measured but elementor default targets are adequate
    - font_size: uses rem/em where possible
    - image_responsiveness: not confirmed (elementor likely handles via srcset)
    - parallax_motion_effects: present on hero sections, may degrade mobile performance
  severity: major
  recommendation: disable parallax and motion effects on mobile, verify touch target sizes >= 48px
accessibility: 58/100
  findings:
    - skip_to_content: present (good)
    - aria_labels: present on navigation menu (good)
    - role_attributes: present on interactive elements (button, navigation)
    - alt_text_on_images: some images present, not comprehensively verified
    - heading_structure: homepage uses styled divs instead of semantic h1-h6 tags (critical gap)
    - color_contrast: custom css may fail wcag aa (white on blue hero sections)
    - aria_hidden_extensive: multiple aria-hidden="true" on decorative icons (good practice)
    - form_labels: no forms found on homepage (no issue)
    - tab_index: not verified programmatically
  severity: critical
  recommendation: restore semantic heading hierarchy on homepage, run axe-core audit, ensure 4.5:1 contrast ratio across all text
overall_score: 68/100
maturity_level: emerging (3/5)
priority_map:
  critical:
    - missing content-security-policy header
    - missing x-frame-options header
    - homepage lacks semantic heading structure (accessibility)
    - no x-content-type-options (mime sniffing risk)
  major:
    - 26 external css/js resources (elementor bloat)
    - 21 third-party domains loaded
    - parallax motion effects on mobile degrade UX
    - png images not converted to next-gen formats
  minor:
    - missing article schema on blog posts
    - referrer-policy header absent
    - permissions-policy header absent
    - standalone blog subpage is redirect-only (no direct content)