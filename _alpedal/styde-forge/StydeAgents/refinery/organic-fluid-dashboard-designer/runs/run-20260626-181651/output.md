3 dashboard mockups generated. Each mockup is a standalone HTML file concept. Outputting mockup specs in YAML.
---
mockup: dashboard_home
concept: living organism dashboard
viewport: 1440x900
vibe: dawn over a still lake
layout:
  navigation: left rail, 64px wide, fully rounded corners, frosted glass. 5 icons floating with 8px vertical gaps. active icon pulses with a soft glow.
  header: 80px tall, no hard edges. page title in a pill-shaped badge. date/time in a floating chip. profile avatar with a gentle halo.
  main_grid: 3-column responsive. cards have border-radius: 24px. card backgrounds use subtle radial gradients. cards cast soft shadows with 40% opacity. no straight lines anywhere.
card_types:
  - name: welcome_card
    shape: wide pill, width span 2 columns. background: warm peach-to-cream gradient (radial). contains greeting text, a decorative biomorphic blob illustration, and an action button that looks like a water droplet.
  - name: metric_tile
    shape: rounded square. background: soft blue-teal radial gradient. value displayed in a large soft number, label beneath in thin weight. a subtle curved progress indicator wraps the bottom edge like a wave.
  - name: activity_chart
    shape: rounded rectangle. background: lavender-to-rose radial gradient. inline chart rendered as smooth bezier curves, no axis lines, just floating data points connected by flowing ribbons.
  - name: status_card
    shape: organic blob (clip-path with bezier curves). background: warm amber radial. status items as horizontal pills with dot indicators. dots pulse gently.
color_palette:
  primary: '#f7d4b5' (warm peach)
  secondary: '#c9e4de' (mint cream)
  accent: '#e8a87c' (terracotta)
  bg: '#faf3ea' (warm ivory)
  surface: 'rgba(255, 252, 248, 0.75)' (frosted)
  text_primary: '#2d2a26'
  text_secondary: '#7a736c'
  glow: 'rgba(232, 168, 124, 0.2)'
animations:
  - page load: cards rise gently from below with 600ms ease-out. stagger: 80ms.
  - hover: card raises 4px, shadow deepens, a subtle scale(1.01).
  - breathing: background gradient shifts 3px over 8s infinite loop.
  - ripple: clicking a button creates a circular ripple that fades outward.
typography:
  font: 'Inter', system-ui, sans-serif
  weight_light: 300
  weight_regular: 400
  weight_medium: 500
  scale: 14px body, 18px card title, 36px metric value, 12px label
---
mockup: analytics_view
concept: flowing river of data
vibe: afternoon sun through leaves
layout:
  header: collapsed into a floating chip bar that follows scroll. semi-transparent.
  main_area: single column with organic dividers — not lines, but 4px tall gradient bands that fade in and out.
  right_panel: detachable floating panel, slides in from right with 300ms ease-out. border-radius: 32px on all corners. backdrop-filter: blur(20px).
sections:
  - name: trend_river
    description: >
      A horizontal scrolling timeline. Each data point is a droplet-shaped node.
      Lines between nodes are thick (3px) and use bezier curves.
      The entire river has a soft glow beneath it. Nodes change color based on sentiment (green/amber/rose).
      No X/Y axis. Time flows left to right like a stream.
  - name: metric_circles
    description: >
      Three concentric rings. Innermost ring = current value. Middle ring = comparison period. Outer ring = target.
      Rings are not perfect circles — they wobble slightly like a cell membrane.
      Values appear inside the center as floating text. Ring colors: inner warm peach, middle soft teal, outer lavender.
  - name: breakdown_fan
    description: >
      A radial fan-out chart. Categories are segments that spread from a center point.
      Segments have rounded tips (border-radius on the arc). Gaps between segments are 2px.
      Hovering a segment pulls it outward 8px and shows a floating tooltip card.
      Center circle shows total with a gentle pulsing animation.
colors:
  gradient_base: linear-gradient(135deg, #f7d4b5 0%, #e8a87c 50%, #c9e4de 100%)
  node_positive: '#9fd8cb'
  node_neutral: '#f0d5b6'
  node_negative: '#e8a87c'
  ring_peach: 'rgba(247, 212, 181, 0.6)'
  ring_teal: 'rgba(201, 228, 222, 0.6)'
  ring_lavender: 'rgba(211, 210, 240, 0.6)'
---
mockup: settings_panel
concept: tactile clay interface
vibe: warm lamp in a cozy room
layout:
  page: single column, max-width 640px centered. background shifts from warm ivory to a very subtle radial glow behind the active section.
  sections: stacked vertically, each section is a pill-shaped container (border-radius: 28px). between sections, 24px gap created by organic spacing — not divider lines.
  no tabs, no toggle buttons with hard edges.
controls:
  - type: switch
    shape: pill track, 48px wide, 28px tall. knob is a circle with a soft shadow. track fills with gradient when active. transition: 400ms ease.
    states:
      off: '#d4ccc4' track, '#ffffff' knob
      on: '#c9e4de' track -> '#9fd8cb' fill, knob slides right
  - type: slider
    shape: full width track, 6px tall, fully rounded. knob is 24px circle with inner gradient. track gradient transitions smoothly.
    track_bg: '#e8e0d8'
    track_fill: linear-gradient(90deg, #f7d4b5, #e8a87c)
    behavior: value shown as a floating chip above knob while dragging. chip has a small tail pointing down.
  - type: select
    shape: pill-shaped button that expands into a dropdown panel. dropdown has border-radius: 20px and backdrop-filter: blur.
    option_rows: 40px tall, rounded corners on hover. selected option has a blob-shaped checkmark.
  - type: action_button
    shape: water droplet silhouette. click creates a ripple that radiates outward in a wave pattern. background uses the warm peach gradient. text is centered, slightly inset.
    hover: droplet fills with a slightly deeper gradient, a 1px highlight appears on the upper curve.
card_section_example:
  header: 'Display Settings'
  items:
    - label: 'Dark Mode'
      control: switch (off)
      description: 'Softer on the eyes at night'
    - label: 'Font Size'
      control: slider (value: 16px)
      description: 'Drag to adjust readability'
    - label: 'Theme Color'
      control: select (value: 'Dawn')
      options: ['Dawn', 'Mist', 'Sunset', 'Forest']
animations:
  - controls fade in on scroll with 40px upward drift, 500ms ease-out, staggered 60ms
  - switch knob has a slight bounce at the end of transition
  - slider shows a subtle ripple under the knob on drag start
  - section containers breathe: box-shadow oscillates between two warm tones over 6s loop