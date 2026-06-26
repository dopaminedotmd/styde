Blueprint: Styde Se Site Integrator
Version: 1
Domain: frontend
Phase: 0.5
Design deliverable:
---
integration_spec:
  problem:
    current_dashboard_has:
    - standalone dark sidebar with no styde.se branding
    - no parent site navigation present
    - feels like separate app, not sub-site
    - mockup-v3 has breadcrumb link to styde.se but no shared chrome
  guiding_principle:
    Forge is /forge on styde.se. Not a separate origin. Not an iframe. Not a different visual language. The user should feel they navigated from styde.se into Forge, not left styde.se entirely.
  chrome_layers:
    layer_1_styde_se_global_nav:
      position: fixed top, full width, z-index 2000
      height: 48px
      background: white or near-white (#fafafa or #ffffff)
      border_bottom: 1px solid #e5e7eb
      content:
      - left: styde.se wordmark / logotype in sans-serif, medium weight, #111827
      - left: subtle divider, then "Forge" in the same weight but at 0.8 opacity if not on Forge page
      - right: user menu (avatar + dropdown), notification bell with dot, global search icon
      - the styde.se wordmark is always clickable -> styde.se home
      - no Forge-specific controls in this bar
      transitions:
      - on scroll down on forge page, this bar can shrink to 40px or get a slightly stronger backdrop blur
      - never hides entirely — it is the parent site persistent chrome
    layer_2_forge_app_header:
      position: below global nav, sticky, z-index 1500
      height: 56px
      background: rgba(255,255,255,0.85) with backdrop-filter blur(12px)
      border_bottom: 1px solid #e5e7eb
      content:
      - left: breadcrumb trail "styde.se / Forge / Dashboard"
      - left: the breadcrumb "styde.se" is a nav link to parent site
      - left: "Forge" in the trail is the app root
      - right: action buttons (New Pipeline, Refresh, view toggle)
      - right: status indicator dot + "All Systems Nominal" in green
    layer_3_forge_page_body:
      starts below the two header layers
      sidebar or tab navigation depends on page variant
  header_variant_matrix:
    scenario_global_nav_alone:
      pages: styde.se marketing pages, blog, docs (non-forge)
      layer_1: visible
      layer_2: hidden
    scenario_forge_full:
      pages: /forge/dashboard, /forge/pipelines, /forge/agents
      layer_1: visible (thin, 48px, parent chrome)
      layer_2: visible (56px, app-specific chrome)
      layer_3: visible (page content)
    scenario_forge_embedded_tool:
      pages: /forge/blueprint/NNN, /forge/eval/run/NNN (deep tools)
      layer_1: visible
      layer_2: visible (with deeper breadcrumb: styde.se / Forge / Blueprints / "Dashboard Mockup v3")
      layer_3: visible with minimal chrome, max content area
    scenario_forge_fullscreen:
      pages: /forge/terminal, /forge/vnc, /forge/logs (fullscreen tools)
      layer_1: collapsed to 40px minimal bar with just styde.se wordmark + close button
      layer_2: hidden
      layer_3: full viewport beneath the minimal bar
  visual_language_bridge:
    colors:
      parent_palette: any inferred styde.se brand colors
      forge_palette: derives from parent but shifts toward tech/ops feel
      - accent: same primary brand color as styde.se used for CTAs
      - forge retains its own accent indigo/purple only for agent-specific states
      - background: same white/off-white base as parent site
      - cards and surfaces stay white with subtle border, matching parent card style
    typography:
      family: Inter (or whatever styde.se uses), not a separate font
      scale: matches parent site scale
      forge uses same sizes and weights as parent documentation
    spacing:
      grid: multiples of 4px matching parent site
      page padding: same 24px gutters as parent
      max-width: same container width as parent content pages
    component_crossover:
      shared_components:
      - styde.se button styles used in forge action buttons
      - styde.se form elements in forge settings/config
      - styde.se data table styling in forge pipeline list
      - parent site loading spinner and toast system
      forge_specific_components:
      - agent status dots and timeline feed
      - GPU bars and resource meters
      - pipeline DAG visualization
      these maintain the parent visual language but extend it with new purposes
  navigation_model:
    primary_nav:
      position: layer_1 (global nav)
      items:
      - "Styde" or brand home
      - "Forge" (current section, highlighted)
      - maybe "Docs", "Blog", "Community" — whatever styde.se top nav has
      active_state: underline + bold for current section
    secondary_nav:
      position: below breadcrumb in layer_2, or as tab bar
      items:
      - Dashboard (overview)
      - Agents (agent list/status)
      - Pipelines (run history)
      - Blueprints (BP library)
      - Settings
      active_state: underlined tab with accent color
    tertiary_nav:
      position: left sidebar within page body (only for deep pages)
      items: per-section sub-navigation
      example: Blueprints > All BPs, Priority Tier, Drafts, Templates
  breadcrumb_system:
    always_visible: true
    location: layer_2, left side
    format: "styde.se / Forge / [Section] / [Sub-section]"
    each segment is clickable except the last
    first segment always links to styde.se home
    second segment always links to /forge
    handles 4 levels without truncation on desktop
    mobile: truncates to last 2 segments with "..." for overflow
    icon: simple chevron or slash separator, consistent with parent site
  responsive_behavior:
    mobile:
    - layer_1 global nav collapses to hamburger with drawer
    - layer_2 app header stacks breadcrumb on one row, actions move into overflow menu
    - forge sidebar becomes overlay drawer triggered by hamburger
    - breadcrumb truncates to 2 segments
    tablet:
    - both header layers visible at full width
    - forge sidebar can collapse to icon-only
    - breadcrumb at full width
    desktop:
    - full chrome, all layers visible
    - sidebar persistent, 240px
    - breadcrumb at full width
  footer:
    shared styde.se footer, not a forge-specific footer
    includes: copyright, links to styde.se pages, version info tucked into small text
    forge version number in lower-right secondary position
  page_transition:
    navigating between styde.se pages and forge should feel same-origin
    no full-page flash/white blink
    SPA-style transitions if feasible
    route transitions: subtle fade (150ms) + content slide-up (200ms)
  success_metrics:
  - user cannot tell where styde.se ends and forge begins
  - breadcrumb trail always anchors to parent site
  - forge dashboard accessible via /forge on styde.se
  - same visual DNA: fonts, spacing, border radii, shadows
  - forge-specific UI (agent dots, GPU bars) is an extension, not a break
  action_items:
  - determine actual styde.se brand colors, typography, spacing values from parent site
  - rebuild dashboard.html to use two-header-layer architecture
  - replace current standalone sidebar with proper secondary nav in layer_2
  - inject breadcrumb that anchors to styde.se
  - confirm parent site footer and inject it into forge pages
  - test responsive behavior across all breakpoints