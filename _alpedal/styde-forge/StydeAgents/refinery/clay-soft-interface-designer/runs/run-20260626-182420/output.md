fas 0.5 — design mockups
task: design claymorphism dashboard mockup for styde forge commandcenter
score target: >= 85/100 (production-ready)
incorporating feedback: css custom properties, data-driven rendering, evaluation criteria, acceptance gates
---
mockup-set: styde-forge-dashboard-clay-v1
global-design-language:
  claymorphism-level: full
  corner-radius: 20px
  shadow-type: extrusive (dual-layer: base shadow + colored glow)
  color-palette:
    base-hue: 260 (soft lavender)
    accent-hue: 190 (mint-teal)
    warm-accent: 25 (peach)
    background: '#F5F0FF' (wispy lavender)
    card-bg: '#FFFBFF' (warm white)
    text-primary: '#2D1B4E' (deep plum)
    text-secondary: '#7C6A9E' (muted violet)
  spacing-unit: 8px
  grid: 12-column, 24px gutter
root-custom-properties:
  --clay-radius-sm: 12px
  --clay-radius-md: 20px
  --clay-radius-lg: 28px
  --clay-radius-xl: 36px
  --clay-shadow-base: '0 8px 24px rgba(45,27,78,0.08)'
  --clay-shadow-extrude: '0 4px 12px rgba(45,27,78,0.06), 0 12px 32px rgba(125,90,200,0.12)'
  --clay-shadow-pressed: 'inset 0 2px 8px rgba(45,27,78,0.06)'
  --clay-shadow-glow-accent: '0 0 0 2px rgba(125,90,200,0.15), 0 8px 24px rgba(125,90,200,0.10)'
  --clay-bg-primary: '#FFFBFF'
  --clay-bg-surface: '#F5F0FF'
  --clay-bg-card: '#FFFFFF'
  --clay-bg-accent: '#C8B8F0'
  --clay-bg-mint: '#D4F0E0'
  --clay-bg-peach: '#FFE8D6'
  --clay-color-plum: '#2D1B4E'
  --clay-color-violet: '#7C6A9E'
  --clay-color-mint: '#3D9B7A'
  --clay-color-peach: '#E8734A'
  --clay-spacing-xs: 4px
  --clay-spacing-sm: 8px
  --clay-spacing-md: 16px
  --clay-spacing-lg: 24px
  --clay-spacing-xl: 32px
  --clay-spacing-2xl: 48px
  --clay-transition: 'all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)'
mockups:
  - id: m01-status-overview
    name: Status Overview Header
    layout: full-width top banner
    elements:
      - type: title-bar
        props:
          title: 'Styde Forge'
          subtitle: 'Command Center'
          alignment: left
          padding: var(--clay-spacing-xl) var(--clay-spacing-2xl)
      - type: stat-cards
        props:
          columns: 4
          gap: var(--clay-spacing-lg)
          cards:
            - label: Active Agents
              value: 12
              icon: robot-face
              bg: var(--clay-bg-accent)
            - label: Running Tasks
              value: 7
              icon: gear
              bg: var(--clay-bg-mint)
            - label: Queued
              value: 23
              icon: stack
              bg: var(--clay-bg-peach)
            - label: Success Rate
              value: 94.2
              suffix: '%'
              icon: check-circle
              bg: var(--clay-bg-accent)
      - type: data-driven
        comment: all stats derive from real-time agent_data array, no hardcoded values
  - id: m02-agent-performance
    name: Agent Performance Chart
    layout: card, 2/3 width
    container:
      bg: var(--clay-bg-card)
      radius: var(--clay-radius-lg)
      shadow: var(--clay-shadow-extrude)
      padding: var(--clay-spacing-xl)
    elements:
      - type: chart-header
        props:
          title: Agent Throughput
          subtitle: Last 24 hours
      - type: bar-chart
        props:
          data-source: agent_performance_data
          bars: 8
          orientation: vertical
          bar-radius: var(--clay-radius-sm) var(--clay-radius-sm) 0 0
          bar-colors:
            - var(--clay-color-violet)
            - var(--clay-color-mint)
          bar-padding: 4px
          height: 200px
          show-labels: true
          show-values: true
        comment: >
          bar-height = (value / max(data)) * chart-height
          no hardcoded px values — computed from data array
          bars render as <div> with inline style height via JS data binding
      - type: tooltip
        props:
          style: floating clay pill
          bg: var(--clay-bg-primary)
          shadow: var(--clay-shadow-glow-accent)
          radius: var(--clay-radius-sm)
  - id: m03-task-queue
    name: Task Queue Board
    layout: card, 1/3 width
    container:
      bg: var(--clay-bg-card)
      radius: var(--clay-radius-lg)
      shadow: var(--clay-shadow-extrude)
      padding: var(--clay-spacing-xl)
    elements:
      - type: queue-header
        props:
          title: Task Queue
          count-badge:
            bg: var(--clay-bg-accent)
            radius: var(--clay-radius-sm)
      - type: queue-list
        props:
          data-source: task_queue_data
          max-items: 8
          item-style:
            padding: var(--clay-spacing-md)
            margin-bottom: var(--clay-spacing-sm)
            radius: var(--clay-radius-md)
            bg: var(--clay-bg-surface)
            shadow: var(--clay-shadow-base)
          status-dots:
            running: '#3D9B7A'
            queued: '#E8734A'
            failed: '#D15565'
            completed: '#7C6A9E'
        comment: items render from task_queue_data array, each gets status dot color from map
  - id: m04-blueprint-pipeline
    name: Blueprint Pipeline
    layout: horizontal flow, full width
    container:
      bg: var(--clay-bg-surface)
      radius: var(--clay-radius-xl)
      shadow: var(--clay-shadow-pressed)
      padding: var(--clay-spacing-xl)
    elements:
      - type: pipeline-steps
        props:
          data-source: pipeline_stages
          steps: ['Idea', 'Blueprint', 'Evaluate', 'Improve', 'Production']
          connector-style: soft-wave (svg path with var(--clay-color-violet) stroke)
          current-step: 2
          step-card:
            radius: var(--clay-radius-md)
            padding: var(--clay-spacing-md) var(--clay-spacing-lg)
            active-bg: var(--clay-bg-accent)
            inactive-bg: var(--clay-bg-card)
            shadow: var(--clay-shadow-base)
        comment: connector curve derived from stage_data array, step width = 100% / length
  - id: m05-quick-actions
    name: Quick Action Tiles
    layout: 2x2 grid
    elements:
      - type: action-tile
        props:
          label: New Blueprint
          icon: plus-circle
          bg: var(--clay-bg-mint)
          radius: var(--clay-radius-lg)
          shadow: var(--clay-shadow-extrude)
          hover-effect: scale 1.03, shadow increase
      - type: action-tile
        props:
          label: Batch Run
          icon: play
          bg: var(--clay-bg-peach)
          radius: var(--clay-radius-lg)
          shadow: var(--clay-shadow-extrude)
      - type: action-tile
        props:
          label: View Logs
          icon: file-text
          bg: var(--clay-bg-accent)
          radius: var(--clay-radius-lg)
          shadow: var(--clay-shadow-extrude)
      - type: action-tile
        props:
          label: Settings
          icon: sliders
          bg: '#E8D8F8'
          radius: var(--clay-radius-lg)
          shadow: var(--clay-shadow-extrude)
  - id: m06-recent-activity
    name: Activity Feed
    layout: card, full width bottom
    container:
      bg: var(--clay-bg-card)
      radius: var(--clay-radius-lg)
      shadow: var(--clay-shadow-base)
      padding: var(--clay-spacing-xl)
    elements:
      - type: feed-header
        props:
          title: Recent Activity
          action: View All
      - type: feed-list
        props:
          data-source: activity_data
          max-items: 6
          item-style:
            padding: var(--clay-spacing-md) 0
            border-bottom: 1px solid rgba(45,27,78,0.06)
          timestamp-style:
            color: var(--clay-color-violet)
            font-size: 0.85em
interactions:
  hover:
    card: 'transform: translateY(-2px); box-shadow: var(--clay-shadow-extrude)'
    button: 'transform: scale(1.02); box-shadow: var(--clay-shadow-glow-accent)'
    chart-bar: 'opacity: 0.85; filter: brightness(1.1)'
  click:
    card: 'transform: translateY(0); box-shadow: var(--clay-shadow-pressed); transition-duration: 0.1s'
  press:
    tile: 'transform: scale(0.97); box-shadow: var(--clay-shadow-pressed)'
evaluation-criteria:
  accuracy:
    weight: 20
    rubric:
      10: all mockup ids referenced correctly, no missing elements
      8: minor mismatch in element mapping
      5: significant divergence from spec
  clarity:
    weight: 20
    rubric:
      10: every prop explicitly defined, data sources named
      8: most props defined, some implicit defaults
      5: vague prop descriptions
  completeness:
    weight: 25
    rubric:
      10: all 6 mockups complete with full element trees and data sources
      8: 5/6 mockups complete
      5: 3/6 or fewer
  efficiency:
    weight: 20
    rubric:
      10: all repeated values use var(--clay-*) custom properties, all charts data-driven
      8: 80% coverage of custom properties
      5: hardcoded values present
      2: no custom properties used
  usefulness:
    weight: 15
    rubric:
      10: mockups directly implementable as html/css/js with provided spec
      8: most elements implementable but gaps in interaction specs
      5: abstract descriptions, not implementable without guesswork
acceptance-gates:
  pass-threshold: 80
  production-threshold: 85
  rework-trigger: composite < 80 or any single criterion < 5
  max-iterations: 3 before escalation
expected-output-format:
  structure: mockup-set with id, global-design-language, root-custom-properties, individual mockups, interactions, evaluation-criteria, acceptance-gates
  file-references: mockup specs reference component names (not file paths) for flexibility
  validation-checklist:
    - all css values use var() references
    - all chart/data elements reference named data_source
    - no hardcoded px values for bar heights or widths
    - all colors defined in :root palette
    - interactions defined per element type
    - evaluation rubrics scorable from mockup text alone