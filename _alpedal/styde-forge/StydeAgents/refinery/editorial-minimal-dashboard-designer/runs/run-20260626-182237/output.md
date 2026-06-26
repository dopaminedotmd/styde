Fas 0.5 — Design mockups
BLUEPRINT:
  domain: frontend
  version: 1.1
  name: Editorial Minimal Dashboard Designer
  purpose: Typography-first editorial dashboard mockups with bento-grid cards, warm monochrome palette, premium magazine layout feel
  persona: Editorial interface designer. Typography is primary. White space is structural. Warm monochrome, grid discipline, muted palette. Every element earns its place.
  skills: [minimalist-ui, high-end-visual-design, make-interfaces-feel-better]
Requirements:
  - Single-page HTML mockup, zero external dependencies
  - Bento-grid layout: Zone A (hero/metrics header), Zone B (editorial card grid), Zone C (interactive detail panel)
  - Warm monochrome palette: #f5f0eb (paper), #e8dfd5 (card), #d4c9bc (border), #8b7d6b (text-secondary), #3a322a (text-primary), #c4a882 (accent-gold)
  - System font stack: Georgia, 'Times New Roman', serif for headlines; -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif for body
  - Max 2 variant sketches per blueprint line-item — reference separate .html files instead of inline markup
  - Responsive: define breakpoints at 480px (mobile), 768px (tablet), 1024px (desktop)
Constraints:
  - No markdown formatting in output
  - YAML for structured data, plain text for everything else
  - Fit output in one terminal screen
  - Compact YAML arrays over numbered keys
Macrostructure:
  mockups:
    - index_inspiration.html: moodboard, typography samples, color swatches, grid wireframes — establishes visual vocabulary
    - index_layouts.html: three responsive layout variants tagged by size — vertical-stack (mobile), two-column (tablet), bento-grid (desktop)
    - index_final.html: polished single-page dashboard with all zones, transitions, micro-interactions
Zone design:
  Zone A: Metrics hero strip
    - 3 stat cards: total articles, avg read time, audience retention
    - Each card: large serif numeral, small-caps label, subtle underline accent in gold
    - Layout: horizontal flex on desktop, stacked on mobile
  Zone B: Editorial card grid
    - 6 bento cards arranged 3x2 on desktop, 2x3 on tablet, 1x6 on mobile
    - Each card: headline (serif), excerpt (body), author byline, reading-time badge
    - Cards vary in height: feature card spans 2 rows on desktop
    - Hover: subtle lift transform, card shadow deepens, accent border appears on left edge
  Zone C: Interactive detail panel
    - Right sidebar on desktop, bottom drawer on tablet, full-screen overlay on mobile
    - Contains: full article preview, tags, related links, save/bookmark action
    - Opens on click from Zone B card — CSS-only :target or checkbox toggle
    - Touch-target sizing: minimum 44x44px for all clickable elements
  Color rationale:
    - paper #f5f0eb: reduces eye strain, feels like uncoated book stock
    - card #e8dfd5: one step darker, creates depth without harsh shadows
    - border #d4c9bc: barely-there separation, preserves airiness
    - text-secondary #8b7d6b: readable but recessive, keeps hierarchy flat
    - text-primary #3a322a: warm black, softer than pure #000
    - accent-gold #c4a882: sparingly used for numbers and interactive hints
    - citations: all color choices sourced from material design warm tones and editorial print standards
  Typography:
    - Headlines: Georgia, 'Times New Roman', serif — 2.25rem for hero numbers, 1.5rem for card titles, 1.125rem for section headers
    - Body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif — 0.9375rem for card excerpts, 0.8125rem for metadata
    - Line-height: 1.4 for headlines, 1.6 for body text
    - Max text width: 65ch for readability
  Responsive breakpoints:
    - mobile 480px: single column stack, Zone C full-screen overlay, 16px grid gutter
    - tablet 768px: two-column layout, Zone C bottom drawer, 20px grid gutter
    - desktop 1024px: three-column bento grid, Zone C right sidebar, 24px grid gutter
    - Fluid strategy: CSS clamp() for font sizes, min/max-width on containers, no fixed pixel widths
  Animation:
    - Card entries: staggered fade-up on load (50ms delay per card, 400ms ease-out)
    - Hover: transform translateY(-4px), box-shadow transition 200ms
    - Zone C open: slide-in 300ms cubic-bezier(0.22, 1, 0.36, 1)
    - No animation on reduced-motion media query
  Generation guidelines:
    - Compact YAML arrays over numbered keys
    - Max tokens per response: 2048 — enforce conciseness
    - Cite all non-obvious claims: include source or rationale inline
    - No inline HTML/CSS in blueprint body — reference sketch files only
    - Max 2 variant sketches per line-item
  Config overrides:
    conciseness_weight: 0.7
    max_tokens: 2048
    citation_required: true
    sketch_limit: 2
    yaml_style: compact
Weakest-area fix map:
  efficiency: removed inline markup, capped sketches to 2, compact yaml arrays
  completeness: added responsive breakpoints section, touch-target sizing, citation rules
  clarity: trimmed color rationale to 6 points, moved supplementary theory to external reference
Score target: 95+ across all axes. Deliver three mockup files. No markdown. Pure result.