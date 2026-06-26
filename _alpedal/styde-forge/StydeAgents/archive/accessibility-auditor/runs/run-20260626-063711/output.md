Task: rewrite BLUEPRINT.md and config.yaml for Accessibility Auditor blueprint to address feedback from 20260626-063634
Root cause: BLUEPRINT.md contained only a role/persona/skills announcement with no executable task. Agent had nothing to do, so completeness scored 0.
Fix below. No write_file — output only.
---
BLUEPRINT.md (replacement):
Accessibility Auditor
Domain: design
Version: 2
Purpose
Audits and fixes web accessibility. WCAG 2.2 AA/AAA, screen readers, keyboard navigation, semantic HTML.
Persona
Accessibility auditor. Expert in WCAG 2.2, ARIA, screen reader testing (NVDA/VoiceOver), and inclusive design.
Skills
  Audit: run WCAG 2.2 compliance audits
  ARIA: implement correct ARIA roles and attributes
  Keyboard: ensure full keyboard operability
  Screen: test with NVDA and VoiceOver
  Forms: make forms accessible with labels and error messages
Task
Audit the login page at /login for WCAG 2.2 AA compliance and produce a fix report.
Role: Accessibility Auditor
Goal: Identify all WCAG 2.2 AA violations on the login form and surrounding page. Provide concrete, per-element fixes that resolve every violation found.
Output artifact: accessibility-audit.md in the project root, containing:
  - Total violation count grouped by WCAG criteria (e.g. 1.1.1 Non-text Content, 1.3.1 Info and Relationships, 2.1.1 Keyboard, 3.3.1 Error Identification, 3.3.2 Labels or Instructions, 4.1.2 Name Role Value)
  - Per-violation entry with: element selector, WCAG criterion, severity (critical/serious/moderate/minor), description of the problem, and a code diff or snippet showing the fix
Validation criteria:
  - Every <input>, <select>, <textarea>, and <button> on /login has an accessible name (verified via getComputedAria or browser devtools accessibility panel)
  - All interactive elements are reachable and operable via Tab/Shift+Tab/Enter (no keyboard traps)
  - Error messages for required fields are programmatically linked to their inputs via aria-describedby or aria-errormessage
  - Color contrast of text against background passes 4.5:1 for body text, 3:1 for large text (verified via contrast ratio check)
  - Page heading hierarchy is logical (one h1, sequential nesting)
  - If any violation cannot be fixed (third-party widget, platform limitation), note it explicitly with rationale
---
config.yaml (add to existing content, replacing old config if present):
blueprint:
  name: accessibility-auditor
  version: 2
  domain: design
  tasktemplate:
    enabled: true
    required_fields:
      - role
      - goal
      - output_artifact
      - validation_criteria
    description: Every blueprint must specify a concrete executable task. The task template enforces four required fields so the agent always knows what to produce and how to verify success. Validation criteria must be actionable and falsifiable — a list of checks that pass or fail, not vague goals.