agent-status-panel-v1:
  concept:
    composition:
      - header-bar: [forge-brand, run-controls, time-range-filter]
      - status-banner: [overall-health-ring, live-counts, throughput-gauge]
      - agent-grid: [agent-cards in responsive flow layout]
    grid-columns: [1 on mobile, 2 on tablet, 3 on desktop, 4 on wide]
    card-height: fixed 240px
  agent-card:
    layout:
      row-1: [avatar-initials, agent-name, status-dot, score-pill]
      row-2: [health-bar (filled)]
      row-3: [current-task-label (truncated)]
      row-4: [counts-row: running | pending | completed]
      row-5: [mini-timeline (last 5 status transitions)]
    avatar-initials:
      size: 32px
      bg: hsl from agent-name hash
      text: first-two-chars uppercase
      weight: 600
    status-dot:
      states:
        idle:
          color: '#9CA3AF'
          pulse: false
          label: idle
        running:
          color: '#10B981'
          pulse: true (3s ease-in-out)
          label: active
        paused:
          color: '#F59E0B'
          pulse: false
          label: paused
        error:
          color: '#EF4444'
          pulse: false
          label: faulted
        completed:
          color: '#3B82F6'
          pulse: false (static checkmark)
          label: done
      size: 10px
      border: 1.5px solid rgba(255,255,255,0.4)
    health-bar:
      height: 6px
      radius: 3px
      track-bg: '#1F2937'
      fill-gradient: linear-gradient(90deg, #EF4444, #F59E0B, #10B981)
      fill-width: agent.health_score + '%' (0-100)
      overlay-edge-guard: if total_evaluations == 0, fill-width = '50%' with gray color, label 'insufficient data'
    score-pill:
      position: card row-1 right-aligned
      height: 22px
      min-width: 40px
      padding: 0 8px
      radius: 11px
      bg: score-to-color(score)
      text: score + '%' or 'N/A' if unrated
      size: 11px
      weight: 700
      color: white
    score-to-color:
      90-100: '#10B981' (green)
      70-89: '#F59E0B' (amber)
      0-69: '#EF4444' (red)
      null: '#6B7280' (gray, unrated)
    counts-row:
      layout: [icon-running:count, icon-pending:count, icon-completed:count]
      separator: vertical bar '|' with opacity 0.3
      icon-running:
        glyph: play-circle
        color: '#10B981'
      icon-pending:
        glyph: clock
        color: '#F59E0B'
      icon-completed:
        glyph: check-circle
        color: '#9CA3AF'
      all-counts: font-mono 14px weight 600
    mini-timeline:
      height: 20px
      nodes: 5 dots in horizontal line
      dot-radius: 3px
      connectors: 1px solid rgba(255,255,255,0.15)
      dot-colors: mapped from status-dot states
      interaction: tooltip on hover shows event-type + timestamp
    current-task-label:
      font-size: 12px
      color: rgba(255,255,255,0.6)
      line-clamp: 1
      placeholder-if-empty: 'awaiting instruction'
  overall-health-ring:
    type: circular-progress
    size: 80px
    stroke-width: 6
    value: avg(agent.health_score for all agents)
    color: score-to-color(value)
    center-text:
      line-1: value + '%'
      line-2: 'overall'
    empty-state: if no agents registered, show '0 agents' with dashed ring
  live-counts:
    layout: row of 3 count-blocks
    count-block:
      label: ['running', 'pending', 'failed']
      value: count
      icon: respective glyph
      color: respective status color
    edge-case: if count > 999 format as '999+'
  throughput-gauge:
    type: horizontal-bar
    label: 'throughput'
    value: completed_tasks / time_window
    unit: 'tasks/min'
    sparkline: 20px high inline chart of last 30 datapoints
    fallback-if-no-data: show '-- tasks/min' with empty sparkline
  empty-state:
    banner-on-empty:
      icon: grid-3x3 icon
      headline: 'No agents deployed'
      subtext: 'Configure your first blueprint run to populate the dashboard'
      action-button: 'Create Agent' -> navigates to forge-run config
  interactions:
    card-click: navigates to /forge/agents/{agent-id}/detail
    card-hover:
      border: 1px solid rgba(255,255,255,0.2) -> glow effect rgba(16,185,129,0.15)
      transform: translateY(-2px)
      transition: 200ms ease
    status-dot-hover: tooltip shows last-status-change + uptime duration
    health-bar-click: expands to full health breakdown modal
    sort-controls:
      options: [score desc, score asc, name a-z, running first, recently active]
      default: running first + score desc secondary
  accessibility:
    status-dot:
      aria-role: status
      aria-label: 'Agent {name} is {state}. Health score {score} percent.'
    health-bar:
      aria-role: progressbar
      aria-valuenow: health_score
      aria-valuemin: 0
      aria-valuemax: 100
      aria-valuetext: '{score} percent health'
    agent-card:
      aria-role: region
      aria-label: 'Agent summary for {name}'
      tabindex: 0
    color-blind-safe:
      status-dot uses shape+icon in addition to color
      red-green confusion handled by shape overlay (circle=idle, diamond=running, triangle=paused, X=error, check=completed)
    contrast-ratios:
      text-on-dark: min 4.5:1 for body, 3:1 for large text
      score-pill-text: always white over high-saturation bg
  responsive-breakpoints:
    mobile: < 640px (1 column, compact counts, no mini-timeline)
    tablet: 640-1024px (2 columns, mini-timeline hidden)
    desktop: 1024-1440px (3 columns, full)
    wide: > 1440px (4 columns, full + throughput visible)