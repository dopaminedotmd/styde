scope:
  files:
    - E:\Stryde\_alpedal\styde-forge\Dashboard\web\timeline.html
    - E:\Stryde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html
  conformance: WCAG 2.2 AA [assumed: no level specified]
  target: [assumed: all .html files in Dashboard/web/]
violations:
- criterion: 1.1.1
  severity: critical
  file: timeline.html
  selector: SVG circles at line 615-624
  behavior: Interactive SVG nodes created via createElementNS with click handlers but zero text alternatives. Screen reader sees anonymous circles.
  expected: Each circle must have aria-label with blueprint name and run status. Or wrap in <g role="img" aria-label="...">.
  fix: Add aria-label attribute to each circle element: circle.setAttribute('aria-label', `${bp} run ${a.run_id} score ${score}`)
- criterion: 1.1.1
  severity: high
  file: mission_control_8765.html
  selector: gaugeSvg() at line 697-710
  behavior: SVG gauge circles have no aria-label. Temperature values rendered as <text> elements ignored by screen readers.
  expected: Add aria-label reading temperature and metric name.
  fix: Add role="img" and aria-label="GPU temperature: ${Math.round(temp)} degrees" to gauge SVG wrapper.
- criterion: 1.4.1
  severity: high
  file: timeline.html
  selector: getColor() at line 493-497 and popup-score at line 669
  behavior: Color alone distinguishes gold (85+), amber (70-84), cool (<70). No text labels or patterns supplement the color coding.
  expected: Add text labels, icons, or patterns alongside color differentiation.
  fix: Add a data-score-label attribute or text suffix like "Gold", "Amber", "Cool" to each colored element. In popup, prepend score tier text.
- criterion: 1.4.1
  severity: high
  file: mission_control_8765.html
  selector: .forge-beat.live at line 116-117, zone colors at line 184-197
  behavior: Forge beat indicator uses color-only change (amber vs grey). Zone bars use border-color alone (amber/emerald/grey) to distinguish refinery/production/archive.
  expected: Add text labels, icons, or additional visual cues beyond color.
  fix: Add shape or label change to forge-beat (e.g. pulse icon + text). Zone labels already present as text but the color distinction needs a non-color differentiator like an icon.
- criterion: 1.4.3
  severity: critical
  file: timeline.html
  selector: body background #0a0b0f with color #6b7b90 (lines 9, 73, etc.)
  behavior: Numerous text elements use color #6b7b90 on #0a0b0f background. Approximate contrast ratio ~3.8:1 — fails AA minimum of 4.5:1. Ticking labels #3a4a60 on #0a0b0f ~2.4:1.
  expected: Minimum 4.5:1 contrast ratio for body text, 3:1 for large text.
  fix: Lighten text colors: #6b7b90 to #8899b0 (4.5:1 on #0a0b0f), #3a4a60 to #5a7a90.
- criterion: 1.4.3
  severity: critical
  file: mission_control_8765.html
  selector: --text-faint:#3A3A5C on --void:#020208 (line 38, 53)
  behavior: --text-faint (#3A3A5C) on --void (#020208) yields ~2.8:1 contrast. --text-dim (#686898) yields ~4.0:1 on --void. Both fail or barely pass.
  expected: 4.5:1 minimum for body-size text.
  fix: --text-faint to #6A6A9A, --text-dim to #8888B8.
- criterion: 1.4.4
  severity: medium
  file: timeline.html
  selector: viewport content="width=1400" at line 5
  behavior: Fixed viewport at 1400px prevents responsive text scaling on mobile. Resize to 200% will clip content.
  expected: Viewport must allow user-scalable resizing up to 200%.
  fix: Change to <meta name="viewport" content="width=device-width, initial-scale=1.0"> and use responsive layout.
- criterion: 2.1.1
  severity: critical
  file: timeline.html
  selector: SVG node circles at line 615-624
  behavior: Circles added via SVG API with click events but no tabindex, no keyboard event listeners. Impossible to activate via keyboard alone.
  expected: Every interactive control must be keyboard operable.
  fix: Add tabindex="0" to each circle, add keydown('Enter'/'Space') listener calling same showPopup handler.
- criterion: 2.4.7
  severity: high
  file: timeline.html
  selector: .search-box:focus at line 56, all interactive elements
  behavior: Default browser focus outlines are removed via *{outline:none} at line 56 but only search-box has a custom focus indicator. Buttons, slider, popup have no visible focus.
  expected: Every interactive element must have a visible focus indicator.
  fix: Add :focus styles: .btn:focus{outline:2px solid #ffd700; outline-offset:2px}. Ensure slider thumb focus is visible.
- criterion: 2.4.7
  severity: high
  file: mission_control_8765.html
  selector: .fc-btn at line 209-218, .fc-input at line 220-226
  behavior: fc-btn has :hover but no :focus style. fc-input has :focus only on border-color with no outline ring. Tab buttons (line 462) have no focus style beyond hover. Toggle (line 228-233) has zero focus indicator.
  expected: Two or more visible focus indicators across interactive controls.
  fix: Add :focus-visible: outline styles to all interactive elements. Example: .fc-btn:focus-visible{outline:2px solid var(--cool-indigo); outline-offset:2px}
- criterion: 4.1.2
  severity: high
  file: timeline.html
  selector: popup-close button at line 53 and 720
  behavior: Button innerHTML contains &times; (Unicode multiplication sign) — no accessible name. Screen reader announces empty button.
  expected: Button must have programmatic label.
  fix: Add aria-label="Close popup" to the popup-close button element.
- criterion: 4.1.2
  severity: high
  file: mission_control_8765.html
  selector: .fc-toggle input at line 550, 554
  behavior: Toggle checkboxes lack role="switch" and aria-checked attribute. Screen reader announces as checkbox, not switch.
  expected: Custom toggle pattern must use role="switch" and aria-checked matching .checked.
  fix: Add role="switch" to each toggle input. Sync aria-checked with checked state via onchange handler: this.setAttribute('aria-checked', this.checked)
- criterion: 3.3.2
  severity: medium
  file: timeline.html
  selector: search-box at line 55
  behavior: Search input has placeholder only — no explicit <label> element. Placeholder disappears on input, leaving no visible label.
  expected: Every input must have a programmatically associated label.
  fix: Wrap input in <label> with text "Filter blueprints" or add aria-label="Filter blueprints" attribute.
- criterion: 3.3.2
  severity: medium
  file: mission_control_8765.html
  selector: spawn-input at line 547, skill-search at line 584, bp-search at line 609
  behavior: Three inputs with placeholders only, zero programmatic labels or aria-labels.
  expected: Each input must have associated label.
  fix: Add aria-label to each: spawn-input aria-label="Blueprint name to spawn", skill-search aria-label="Filter skills", bp-search aria-label="Filter blueprints".
summary:
  files_audited: 2
  violations_found: 14
  severity_breakdown:
    critical: 4 (1.1.1 SVG no text, 1.4.3 contrast x2, 2.1.1 keyboard)
    high: 7 (1.1.1 gauge, 1.4.1 color x2, 2.4.7 focus x2, 4.1.2 x2)
    medium: 3 (1.4.4 viewport, 3.3.2 labels x2)
refinement:
  "I assumed WCAG 2.2 AA and audited both .html files in Dashboard/web/. Run with AAA for stricter thresholds (7:1 contrast, 3:1 large text AAA), or specify a different target. I skipped popup overlay ESC handling (2.1.1) and focus-trap for modal (2.4.3) as nice-to-haves — address those too?"
expected_mutations (would apply if write_file permitted):
  - file: timeline.html
    criteria: [1.1.1, 2.1.1]
    description: Add aria-label to SVG circles, add tabindex+keydown handler
  - file: timeline.html
    criteria: [1.4.3]
    description: Lighten #6b7b90 to #8899b0, #3a4a60 to #5a7a90 in body text
  - file: timeline.html
    criteria: [4.1.2, 3.3.2]
    description: Add aria-label to popup-close button, add aria-label to search-box
  - file: mission_control_8765.html
    criteria: [1.4.3]
    description: Update --text-faint to #6A6A9A, --text-dim to #8888B8 in :root
  - file: mission_control_8765.html
    criteria: [4.1.2, 3.3.2]
    description: Add role=switch aria-checked to toggles, add aria-labels to three inputs
  - file: mission_control_8765.html
    criteria: [2.4.7]
    description: Add :focus-visible styles to .fc-btn, .fc-input, tab buttons, toggles