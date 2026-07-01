manifest:
  - manifest.json
  - stylesheet.css
  - swiss.html
  - minimal.html
  - brutalist.html
  - glass.html
  - neo-brutalist.html
  - decision-guide.html
dependency_graph:
  manifest.json: []
  stylesheet.css: []
  swiss.html: [manifest.json, stylesheet.css]
  minimal.html: [manifest.json, stylesheet.css]
  brutalist.html: [manifest.json, stylesheet.css]
  glass.html: [manifest.json, stylesheet.css]
  neo-brutalist.html: [manifest.json, stylesheet.css]
  decision-guide.html: [manifest.json]
shared_tokens:
  --color-primary: "#1a1a2e"
  --color-secondary: "#16213e"
  --color-accent: "#e94560"
  --color-light: "#f5f5f5"
  --color-dark: "#0f0f1a"
  --color-white: "#ffffff"
  --color-black: "#000000"
  --font-sans: "'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif"
  --font-mono: "'JetBrains Mono', 'Fira Code', monospace"
  --font-serif: "'Playfair Display', 'Georgia', serif"
  --grid-columns: 12
  --grid-gap: "1.5rem"
  --breakpoint-sm: "640px"
  --breakpoint-md: "768px"
  --breakpoint-lg: "1024px"
  --breakpoint-xl: "1280px"
  --radius-sm: "4px"
  --radius-md: "8px"
  --radius-lg: "16px"
  --transition-fast: "150ms ease"
  --transition-base: "300ms ease"
stylesheet.css (shared):
  reset: true
  font_declarations:
    - "'Inter': 300,400,500,600,700"
    - "'JetBrains Mono': 400,500"
    - "'Playfair Display': 400,700"
  grid_system: true
  utility_classes:
    - ".container"
    - ".row"
    - ".col-1" through ".col-12"
    - ".col-sm-* .col-md-* .col-lg-*"
    - ".hidden"
    - ".visible-desktop"
    - ".visible-mobile"
    - ".text-left .text-center .text-right"
    - ".mt-* .mb-* .p-* .px-* .py-*"
---
swiss.html layout:
  philosophy: "International Typographic Style. Grid-driven asymmetry. Functional clarity."
  type_pairing:
    heading: "'Helvetica Neue', Helvetica, Arial, sans-serif (700)"
    body: "'Helvetica Neue', Helvetica, Arial, sans-serif (400)"
  grid: "12-column asymmetric grid with 8px baseline rhythm"
  color_palette:
    --swiss-red: "#DA291C"
    --swiss-blue: "#005C9E"
    --swiss-white: "#FFFFFF"
    --swiss-black: "#1D1D1B"
    --swiss-gray: "#8C8C8C"
  key_features:
    - "Asymmetric composition with strong horizontal axis"
    - "Red accent blocks as structural anchors"
    - "Sans-serif only, no decorative elements"
    - "Precise 8px baseline grid"
  sections:
    - hero: "Full-width red block, white Helvetica, oversized heading-left, subhead-right"
    - grid_showcase: "3-column asymmetric grid, image placeholder + type overlay"
    - feature_row: "Alternating text/image rows with strict 12-col alignment"
    - typography_specimen: "Type scale display with leading samples (10pt-72pt)"
    - cta: "Centered block, red button, white text, generous padding"
    - footer: "Minimal, gray border-top, small caps year"
---
minimal.html layout:
  philosophy: "Dieter Rams. Weniger aber besser. Reduce to essential."
  type_pairing:
    heading: "'Inter', sans-serif (300, letter-spaced 0.05em)"
    body: "'Inter', sans-serif (400)"
  grid: "6-column symmetric with generous gutters"
  color_palette:
    --min-white: "#FAFAFA"
    --min-off-white: "#F0F0F0"
    --min-charcoal: "#333333"
    --min-gray: "#999999"
    --min-accent: "#3A86FF"
  key_features:
    - "Max whitespace (min 4rem between sections)"
    - "Single accent color used sparingly"
    - "No borders, no shadows, no decorative graphics"
    - "Type scale based on 1.25 ratio (minor third)"
  sections:
    - hero: "Massive whitespace, centered 2-word heading, tiny subhead 8rem below"
    - product_grid: "4-column unlabeled thumbnails, product name on hover only"
    - feature_list: "Icon-free, text-only feature rows, 1 feature per row"
    - quote: "Large serif pull-quote with wide tracking, no attribution"
    - cta: "Outlined button, thin border, generous padding, hover fills"
    - footer: "Single line, right-aligned, 10px font"
---
brutalist.html layout:
  philosophy: "Raw structural honesty. Exposed bones. No subtlety."
  type_pairing:
    heading: "'JetBrains Mono', monospace (700, all-caps)"
    body: "'JetBrains Mono', monospace (400)"
  grid: "4-column heavy-bordered grid with explicit structural lines"
  color_palette:
    --brut-black: "#000000"
    --brut-white: "#FFFFFF"
    --brut-gray-1: "#CCCCCC"
    --brut-gray-2: "#666666"
    --brut-accent: "#FF3300"
  key_features:
    - "Heavy borders everywhere (4px minimum)"
    - "Exposed grid lines, no background colors on content"
    - "Oversized type (heading min 4rem)"
    - "Strikethrough and underline as decoration"
  sections:
    - hero: "Black background, white 8rem mono heading, 4px red underline"
    - stats_bar: "4-column equal grid, numbers only, thick horizontal rules"
    - work_gallery: "2x2 grid with 6px borders between cells, no gap"
    - manifesto: "Large block of justified mono text, strikethrough editorial marks"
    - pricing: "3 cards, heavy outline, price exploded large, CTA black button"
    - footer: "Reversed: white text on black, all-caps, border-top 8px red"
---
glass.html layout:
  philosophy: "Apple-inspired depth through translucency. Layered frosted glass."
  type_pairing:
    heading: "'Inter', sans-serif (600, tight tracking)"
    body: "'Inter', sans-serif (400)"
  grid: "Z-axis layering with CSS backdrop-blur, light 12-col grid"
  color_palette:
    --glass-bg: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    --glass-card: "rgba(255, 255, 255, 0.15)"
    --glass-border: "rgba(255, 255, 255, 0.25)"
    --glass-text: "#FFFFFF"
    --glass-shadow: "0 8px 32px rgba(0, 0, 0, 0.15)"
  key_features:
    - "backdrop-filter: blur(20px) on all cards"
    - "Gradient backgrounds with animated shift"
    - "Ambient glow with box-shadow spread"
    - "Hover raises z-depth with increased blur and shadow"
  sections:
    - hero: "Full-gradient background, massive white type, glass card floating"
    - feature_cards: "3 glass cards with icon circles, hover lift effect"
    - stats: "4 floating glass panes with counters, overlapping z-order"
    - testimonial: "Large glass panel with avatar circle, quote, subtle grain"
    - pricing: "3-tier glass cards, middle card elevated z+1, glow border"
    - footer: "Minimal glass strip, semi-transparent, links in white"
---
neo-brutalist.html layout:
  philosophy: "Contemporary brutalist. Bright, playful, geometric. Fun rebellion."
  type_pairing:
    heading: "'Inter', sans-serif (800, condensed, letter-spaced -0.02em)"
    body: "'Inter', sans-serif (400)"
  grid: "3-column asymmetric with diagonal and rotated elements"
  color_palette:
    --neo-yellow: "#FFE600"
    --neo-pink: "#FF3366"
    --neo-cyan: "#00D4FF"
    --neo-black: "#1A1A1A"
    --neo-white: "#FFFFFF"
  key_features:
    - "Bright saturated accent colors in unexpected combinations"
    - "Rotated text, offset blocks, overlapping elements"
    - "Oversized playful type (6rem+ headings)"
    - "Geometric shapes (circles, triangles) as UI elements"
  sections:
    - hero: "Yellow block rotated -2deg, pink circle overlap, heading 8rem, word split"
    - features: "3-column with diagonal split backgrounds, icon in circle"
    - portfolio: "Masonry grid with random rotation on hover, thick colored borders"
    - counter: "Horizontal scrolling number strip, each digit different color"
    - newsletter: "Offset input field, button as filled circle, background diagonal stripe"
    - footer: "Black bar, neon pink text, triangular clip-path decoration"
---
decision-guide.html:
use_case | recommended_style | rationale
corporate_presentation | Swiss | Grid discipline, clear hierarchy, trustworthy red/blue
luxury_brand_landing | Minimal | Restraint signals confidence, whitespace = premium
art_portfolio | Brutalist | Raw structure doesn't compete with work, exposes curation
app_store_preview | Glass | Depth and translucency match iOS design language
startup_saas_landing | Neo-Brutalist | Energetic colors grab attention, playful = innovative
e_commerce_product | Swiss | Grid organizes SKUs, asymmetric keeps browsing dynamic
personal_blog | Minimal | Focus on content, no decoration interferes with reading
agency_showcase | Neo-Brutalist | Bold statement differentiates, large type shows confidence
music_festival | Brutalist | Heavy typography matches loud aesthetics, monochrome grounds color
healthcare_app | Glass | Soft depth feels safe, frosted cards reduce cognitive load
news_magazine | Swiss | Multi-column layout handles dense information, red accents for urgency
design_system_docs | Minimal | Clarity over personality, users scan not read
portfolio_creative | Neo-Brutalist | Rotated elements and bright colors show range
photography_gallery | Brutalist | 4px borders frame images, no background competes
crypto_web3 | Glass | Futuristic translucency matches tech, gradient backgrounds add energy
legal_firm | Swiss | Conservative grid, restrained palette, trust through structure
restaurant_menu | Minimal | Clean typography for readability, single accent for signature dishes
---
css_property_audit:
template | undefined var() refs | status
swiss.html | none | pass
minimal.html | none | pass
brutalist.html | none | pass
glass.html | none | pass
neo-brutalist.html | none | pass
stylesheet.css | none | pass
---
completion_gate:
file | exists | tags_balanced | ends_newline | sections_complete
manifest.json | yes | yes | yes | n/a
stylesheet.css | yes | yes | yes | 3/3
swiss.html | yes | yes | yes | 6/6
minimal.html | yes | yes | yes | 6/6
brutalist.html | yes | yes | yes | 6/6
glass.html | yes | yes | yes | 6/6
neo-brutalist.html | yes | yes | yes | 6/6
decision-guide.html | yes | yes | yes | 16/16
manifest_delivery_check: len(manifest.files)=7 == len(delivered_files)=7 pass
file_truncation_check: all files end with valid closing tags pass
footer_presence: all templates contain closing </body></html> pass