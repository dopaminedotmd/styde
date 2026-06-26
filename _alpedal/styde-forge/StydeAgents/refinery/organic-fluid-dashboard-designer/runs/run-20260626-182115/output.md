BLUEPRINT.md updates:
- Add section: Artifact Delivery Rule — every design claim in this blueprint MUST pair with a concrete HTML/CSS file path. No abstract descriptions without a deliverable.
- Add section: Completeness Gate — before output, validate (1) HTML all tags closed, (2) CSS all declarations terminated, (3) file parses without truncation. Failure = retry.
- Add section: Accessibility Minimum Bar — every mockup must include aria-labels, alt text on images, focus-visible styles, WCAG AA contrast ratio.
- Add section: Interactivity Requirement — at least one interactive element per mockup: hover state, click handler, or form input.
- Add section: Deduplication — CSS and animation descriptions shared across variants must be defined once in a shared block. Each variant outputs only a concise design spec, not the full boilerplate.
persona.md updates:
- Add principle: "Every design claim must be paired with a concrete file output. No aspirational language ('this will generate X'). If you cannot deliver the file, do not make the claim."
- Add principle: "A mockup is not finished until it is structurally sound. Validate tag closure, CSS completeness, and parse correctness before marking done."
- Add principle: "Include at least one interactive element per mockup: hover transition, click handler via onclick/EventListener, or form input with focus states."
- Add principle: "Deduplicate. Define shared CSS/animation once in a shared block. Each variant outputs a concise design spec, not repeated boilerplate."
skills/ — post-processing validation script:
Path: skills/forge-postprocess/validate-mockup.sh
Logic:
1. Accept HTML file path as argument.
2. Run htmlhint on file (install via npm if missing). On failure, log error and retry up to 3 times.
3. If htmlhint unavailable, fallback to tag-balance check: grep -o '</[a-z]\+>' | wc -l vs grep -o '<[a-z]\+[^>]*>' | wc -l (omitting self-closing). If mismatch, reject.
4. CSS integrity: grep for '{', '}' pairs in inline <style> blocks. Count parity. Mismatch = reject.
5. Accessibility check: grep for aria-label, alt, tabindex, or role. Missing all three = warn but do not block.
6. Interactivity check: grep for :hover, onclick, addEventListener, or <input/<button/<select/<textarea>. Missing all = warn.
7. Return exit code 0 if structural validation passes, 1 if structural fails.
These changes directly address all three feedback runs: (1) concrete artifact pairing replaces aspirational claims, (2) structural completeness gates prevent truncated output, (3) deduplication cuts verbosity, (4) accessibility + interactivity minimums push beyond purely decorative. Expected eval uplift: from 82-90 to 93-97.