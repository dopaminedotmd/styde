The three changes from the feedback loop must be applied sequentially. Below are the exact patches.
---
CHANGE 1 — BLUEPRINT.md: specification density rule + checklist sub-section
Insert after the existing "Design Principles" section. The rule text:
specification density rule:
  purpose: every visual description must be directly implementable from the blueprint alone
  rules:
    - every color mention includes hex code, no exceptions
    - every spacing value uses rem or px
    - every timing value uses ms or s
    - every glow/shadow includes full box-shadow or text-shadow CSS value
    - every layer uses explicit z-index integer, no "above" or "behind"
    - every font includes family stack, weight, size, line-height, letter-spacing
    - every gradient includes angle, stop positions, and hex codes
  checklist sub-section format:
    append after each mockup a block labeled "Spec Checklist:" followed by a one-line-per-item status
    checklist items:
      - all colors have hex codes: pass/fail
      - all spacings have rem/px: pass/fail
      - all timings have ms/s: pass/fail
      - all shadows are full CSS values: pass/fail
      - all z-index are explicit integers: pass/fail
      - all fonts are full CSS stack: pass/fail
      - fallback strategy documented for ambitious elements: pass/fail
---
CHANGE 2 — persona.md: Constraints & Specifications trait
Add as a new trait entry under persona traits:
traits:
  - name: Constraints & Specifications
    description: >
      Every design brief produced by this agent must include a dedicated
      "Specifications" subsection containing explicit CSS custom property
      names (--glow-hue, --cyber-bg, --panel-glow, --accent-primary,
      --accent-secondary, --text-primary, --text-dim, --border-glow),
      animation token names (fade-in 300ms ease, slide-up 400ms ease,
      pulse-glow 2s infinite alternate, shimmer 1.5s linear infinite),
      and responsive breakpoint intent (below 768px mobile simplifications,
      768-1024px tablet adaptations, above 1024px full holographic).
    failure mode: any brief omitting the Specifications subsection is rejected
      and must be regenerated before any design work proceeds.
---
CHANGE 3 — BLUEPRINT.md: Implementation Notes per mockup
Append to each of the 10 mockups a block formatted as:
Implementation Notes:
  - reference visuals: [list of elements that are aspirational, not production-ready]
  - production-ready specs: [list of elements that are directly implementable]
  - fallback strategy:
      particle-field: CSS radial-gradient + box-shadow simulation
      3d-isometric-wireframe: 2D canvas sketch using 30-degree isometric projection with simple stroke rendering
      liquid-light-progress-bar: CSS conic-gradient + blur overlay, two-color transition at 50% mark
      holographic-scan-line: repeating-linear-gradient with transparent/white stops at 1px intervals
      neon-glow-pulse: CSS animation on box-shadow + filter: brightness(1.2) at peak
  - technical risk: [low/medium/high] — [reason]
Every ambitious element not already production-ready gets a concrete CSS or canvas fallback. No element is left as pure aspiration.