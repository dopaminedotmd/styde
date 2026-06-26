Audit complete. Report below.
violations:
  file: landing.html
  issues:
    - line: 7
      wcag: 1.1.1
      severity: A
      description: Missing <main> landmark element. Page uses only <section> elements with no semantic document structure.
    - line: 1
      wcag: 2.4.1
      severity: A
      description: No skip-to-content link provided. Users cannot bypass repetitive navigation.
    - line: 43-46
      wcag: 1.4.3
      severity: AA
      description: .btn-primary has white text (#fff) on gradient background (#00d4ff to #7b2ff7). Light blue segments fail 4.5:1 contrast against white. Estimated ratio ~2.8:1.
    - line: 45
      wcag: 2.1.1
      severity: A
      description: .btn-secondary and .btn-primary use :hover-only effects. No :focus-visible style defined.
    - line: 14-24
      wcag: 2.3.1
      severity: A
      description: Particle animation (#particles span) with @keyframes float runs continuously. No @media (prefers-reduced-motion: reduce) override.
    - line: 60-68
      wcag: 2.3.1
      severity: A
      description: .mockup-bar animation barRise has no prefers-reduced-motion override.
    - line: 30-31
      wcag: 4.1.2
      severity: A
      description: .nav-links a have no aria-current="page" for active state differentiation.
    - line: 152-155
      wcag: 1.1.1
      severity: A
      description: Decorative particle <span> elements have no aria-hidden="true".
    - line: 112
      wcag: 1.4.1
      severity: A
      description: .urgency pseudo-content uses ::before {content:'hourglass'} to convey meaning. Screen readers may not announce this.
  file: styde-forge-dashboard.html
  issues:
    - line: 1
      wcag: 2.4.1
      severity: A
      description: No skip-to-content link.
    - line: 503-579
      wcag: 1.3.1
      severity: A
      description: Navigation items use <a> tags without href attribute (lines 503,514,524,534,543,554,563,571). These are not keyboard focusable and have no role="button". Screen readers may interpret them as placeholder links.
    - line: 652,675,693,712
      wcag: 2.1.1
      severity: A
      description: .panel-header <div> elements have click handlers (togglePanel) but no role="button", no tabindex="0", and no keyboard event listeners for Enter/Space.
    - line: 101
      wcag: 1.4.3
      severity: AA
      description: .nav-item color #94a3b8 on sidebar background #0f1419. Estimated ratio ~4.0:1. Below 4.5:1 for normal text (14px).
    - line: 99
      wcag: 1.4.3
      severity: AA
      description: .nav-section-label color rgba(255,255,255,0.25) on #0f1419. Estimated ratio ~2.5:1. Below 4.5:1, and text is 11px (below 18px large-text threshold).
    - line: 197-198
      wcag: 1.4.1
      severity: A
      description: .header-breadcrumb a color #64748b. Hover changes to accent only. No underline or other non-color indicator.
    - line: 286
      wcag: 1.4.3
      severity: AA
      description: .metric-change color #64748b on metric-card background #ffffff. Ratio ~4.0:1. Below 4.5:1 for 12px text.
    - line: 150
      wcag: 2.3.1
      severity: A
      description: .status-dot animation pulse-dot. No prefers-reduced-motion override.
    - line: 391
      wcag: 2.3.1
      severity: A
      description: .gpu-bar-fill has transition:width 600ms ease. No prefers-reduced-motion override.
    - line: 963-964
      wcag: 2.2.2
      severity: A
      description: @keyframes spin injected dynamically on refresh. No prefers-reduced-motion.
    - line: 151
      wcag: 2.4.7
      severity: AA
      description: No visible :focus-visible style defined for any interactive element. Default browser outline suppressed? Not explicitly but also not reinforced.
    - line: 665-671
      wcag: 1.1.1
      severity: A
      description: Chart legend uses inline colored <span> blocks with no text equivalents. Screen readers see only inline text.
    - line: 727-738
      wcag: 1.3.1
      severity: A
      description: Data table headers (th) use no scope attribute. Screen readers may not associate columns correctly.
  file: mission_control_8765.html
  issues:
    - line: 1
      wcag: 2.4.1
      severity: A
      description: No skip-to-content link.
    - line: 120-127
      wcag: 1.3.2
      severity: A
      description: #workshop uses CSS grid with no logical DOM order fallback for linearized reading. Source order (furnace, cascade, instruments, terminal, skills) differs from visual presentation for screen readers.
    - line: 209-218
      wcag: 2.1.1
      severity: A
      description: .fc-btn buttons have onclick but no keyboard handling beyond native button defaults. No Enter/Space fallback documented.
    - line: 310-325
      wcag: 2.1.1
      severity: A
      description: .skill-node <div> elements have onclick="openSkill(name)" but no role="button", no tabindex, and no keyboard listener. Inaccessible to keyboard-only users.
    - line: 311-314
      wcag: 1.4.1
      severity: A
      description: .skill-node hover border-color changes from subtle to cool-indigo. No non-color indicator for focus/hover.
    - line: 336-337
      wcag: 1.3.1
      severity: A
      description: #skill-modal uses display:none/block toggling. No aria-hidden management when closed, no focus trap when open.
    - line: 338
      wcag: 2.4.3
      severity: A
      description: .modal-close button is positioned absolutely. Tab order may be unexpected. No focus management on modal open/close.
    - line: 548-551
      wcag: 1.3.1
      severity: A
      description: Toggle labels (Caveman Ultra, Auto-Refresh) are <span> elements adjacent to <label> wrapping input. No explicit for/id association.
    - line: 221
      wcag: 1.4.3
      severity: AA
      description: #spawn-input placeholder "Blueprint name..." uses color var(--text-faint) #3A3A5C on background rgba(5,5,15,0.9) (~#05050f). Ratio ~2.0:1. Fails WCAG SC 1.4.3 for placeholder text.
    - line: 63-64
      wcag: 2.3.1
      severity: A
      description: Particle canvas runs continuous requestAnimationFrame loop. No prefers-reduced-motion check.
    - line: 243
      wcag: 2.3.1
      severity: A
      description: .cascade-entry animation cascadeIn has no prefers-reduced-motion override.
    - line: 262
      wcag: 2.3.1
      severity: A
      description: @keyframes shimmer runs continuously for running entries. No prefers-reduced-motion.
    - line: 117
      wcag: 2.3.1
      severity: A
      description: @keyframes beat animation for #forge-beat.live. No prefers-reduced-motion.
    - line: 701
      wcag: 1.4.1
      severity: A
      description: GPU gauges convey temperature via color only (green/amber/red). No text labels or patterns supplement the color coding.
    - line: 102
      wcag: 1.4.3
      severity: AA
      description: .metric .m-label color var(--text-faint) #3A3A5C on rgba(10,10,22,0.98) background. Text is 8px. Ratio ~2.5:1. Fails 4.5:1.
    - line: 462
      wcag: 1.4.3
      severity: AA
      description: #tab-bar button color var(--text-faint) #3A3A5C on background rgba(10,10,22,0.7). 12px text. Ratio ~2.5:1. Fails.
    - line: 584
      wcag: 1.3.1
      severity: A
      description: #skill-search input has placeholder "Filter..." but no programmatically associated label element.
    - line: 636-643
      wcag: 4.1.2
      severity: A
      description: #skill-modal uses onclick on the backdrop div to close. No role="dialog" or aria-modal="true" on the modal container.
  file: desktop-mockup.html
  issues:
    - line: 1
      wcag: 2.4.1
      severity: A
      description: No skip-to-content link.
    - line: 33
      wcag: 1.3.1
      severity: A
      description: No <main> element. Window content is wrapped in a single <div class="content">.
    - line: 107
      wcag: 1.4.3
      severity: AA
      description: .agent-role color var(--text-dim) #5c6bc0 on var(--bg-card) #1e2746. Estimated ratio ~3.5:1 for 10px text. Fails.
    - line: 121
      wcag: 1.4.3
      severity: AA
      description: .agent-role color var(--text-dim) on rgba(255,255,255,0.02) tint on #1e2746. Same ratio issue.
    - line: 177-179
      wcag: 4.1.2
      severity: A
      description: Titlebar buttons (minimize, maximize, close) use HTML entities (---, #x25A1, #x2715) as content. No aria-label. Screen readers read entity characters.
    - line: 293-303
      wcag: 1.3.1
      severity: A
      description: Agent list rendered via innerHTML with no role="list" or aria-live="polite" for dynamic content updates.
    - line: 356-358
      wcag: 2.2.2
      severity: A
      description: setInterval(addActivity, 3000) continuously adds activity items. No pause mechanism, no aria-live region announced.
    - line: 384-386
      wcag: 2.3.1
      severity: A
      description: Metrics update via setInterval(updateMetrics, 800). No prefers-reduced-motion check. Visual updates at 800ms may cause distraction.
    - line: 190-196
      wcag: 1.1.1
      severity: A
      description: SVG gauge uses stroke-dasharray for data representation with no accessible text alternative. #cpuArc, #memArc paths convey percentage data to sighted users only.
    - line: 407-416
      wcag: 2.3.1
      severity: A
      description: minimize() function animates window transform with no prefers-reduced-motion support.
  file: live-collab-canvas.html
  issues:
    - line: 1
      wcag: 2.4.1
      severity: A
      description: No skip-to-content link.
    - line: 15-16
      wcag: 1.3.1
      severity: A
      description: #topbar contains <h1> but no <main> or <header> landmark. Navigation structure is implicit.
    - line: 244-246
      wcag: 1.3.1
      severity: A
      description: Filter group labels (<label>Search</label>) have no for attribute, and corresponding <input> has no id. No programmatic label association.
    - line: 54-56
      wcag: 2.1.1
      severity: A
      description: .panel.locked state conveyed via visual border color (orange) plus box-shadow. No accessible state announcement (aria-pressed/aria-selected).
    - line: 256-257
      wcag: 4.1.2
      severity: A
      description: .lock-btn and .comment-btn have no aria-label. Screen readers read Unicode lock/chat emoji characters.
    - line: 259
      wcag: 1.1.1
      severity: A
      description: <canvas> elements inside chart panels have no role="img" with aria-label or fallback text. Chart data invisible to screen readers.
    - line: 80-81
      wcag: 2.3.1
      severity: A
      description: @keyframes fadeIn on .chat-msg. No prefers-reduced-motion override.
    - line: 136-139
      wcag: 2.3.1
      severity: A
      description: @keyframes toastIn with translateX animation. No prefers-reduced-motion.
    - line: 65-66
      wcag: 1.4.1
      severity: A
      description: .annotation-marker uses background color (accent2) only to distinguish from other elements. No icon or text differentiation.
    - line: 302-303
      wcag: 1.3.1
      severity: A
      description: Chat input and send button have no association. #chat-input has placeholder but no label element.
    - line: 315-317
      wcag: 1.3.1
      severity: A
      description: Comment input and Post button have no label association. #comment-input has placeholder only.
    - line: 38-39
      wcag: 1.4.3
      severity: AA
      description: #connection-status .dot uses color-only indicator (green/red/orange) for connection state. No text supplement.
    - line: 140-148
      wcag: 2.4.7
      severity: AA
      description: No visible :focus-visible style defined. Custom scrollbar styles may hide default focus outlines.
  file: anomaly-panel.html
  issues:
    - line: 1
      wcag: 2.4.1
      severity: A
      description: No skip-to-content link.
    - line: 9
      wcag: 1.3.1
      severity: A
      description: No <main> element. All content is inside a single <div class="panel">.
    - line: 73-74
      wcag: 1.1.1
      severity: A
      description: #streamCanvas has no role="img" or aria-label. All chart data (anomaly points, thresholds, trends) is visual-only.
    - line: 92-93
      wcag: 1.1.1
      severity: A
      description: #driftCanvas same issue. No text alternative for drift visualization.
    - line: 37-41
      wcag: 2.1.1
      severity: A
      description: .heatmap-cell hover shows tooltip. No keyboard equivalent for focus. Tab cannot reach individual cells.
    - line: 28-36
      wcag: 2.3.1
      severity: A
      description: @keyframes pulse-glow animation on .pulse-dot. No prefers-reduced-motion.
    - line: 288-319
      wcag: 2.3.1
      severity: A
      description: spawnPulse() creates animated SVG circle overlay with requestAnimationFrame. No prefers-reduced-motion check.
    - line: 18
      wcag: 1.4.3
      severity: AA
      description: .card-title .badge color #3a6a8a on background #1a2a3a. Estimated ratio ~2.8:1 for 9px text. Fails 4.5:1.
    - line: 29
      wcag: 2.2.2
      severity: A
      description: .pulse-dot.red animation pulse-glow runs continuously. No pause mechanism.
    - line: 47
      wcag: 1.4.1
      severity: A
      description: .threshold-legend .swatch uses color-only swatches (red=upper, green=mean, blue=lower, amber=band). No text labels or pattern fills.
summary:
  total_files_audited: 6
  total_violations: 66
  by_severity:
    A: 58
    AA: 8
  by_wcag:
    1.1.1: 7
    1.3.1: 12
    1.3.2: 1
    1.4.1: 4
    1.4.3: 9
    2.1.1: 5
    2.2.2: 3
    2.3.1: 12
    2.4.1: 6
    2.4.3: 1
    2.4.7: 2
    4.1.2: 4
  worst_file: mission_control_8765.html (19 violations)
  best_file: anomaly-panel.html (9 violations)