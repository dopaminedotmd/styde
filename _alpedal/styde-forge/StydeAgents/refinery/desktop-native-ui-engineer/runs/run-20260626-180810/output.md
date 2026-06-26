Warning: Unknown toolsets: patch, read_file, search_files
teacher feedback identifies two scoring sessions with overlapping root causes:
session 20260626-180638 score 77.0 — weakest: efficiency. verbose metrics/training sections, system warning banners in output, broken frontmatter, missing dependency.
session 20260626-181508 score 84.0 — weakest: efficiency. tool warnings in output, duplicate cleanliness instructions across sections.
common failure pattern: output hygiene. both sessions penalized for leaking non-content lines (system banners, tool warnings, debug output) and redundant rules that inflate token count.
changes to apply to BLUEPRINT.md:
1. add final-step instruction under task execution pipeline — before deliver: scan and strip all non-content lines. output must start with requested content, zero prefix lines.
2. deduplicate output-cleanliness rules. currently spread across output standards, output completeness gate, side-effect error detection. merge into a single delivery section with output standards subsection. remove redundant copies.
3. add explicit output constraints: max 8 lines per code block, max 2 paragraphs per non-code section, ban system banner/warning leakage via output filter.
4. add pre-submit verification step: validate yaml frontmatter parses, confirm all crates referenced in code exist in cargo.toml, strip any non-content diagnostic lines.
5. for config.yaml — add conciseness penalty or lower maxtokens to enforce tighter output targets.
no changes to evaluation metrics, training data, or domain content — those scored well (completeness 92). the gate issue is strictly output formatting and rule organization.
delivery output after changes would produce a blueprint that scores 86-90 by eliminating the two high-severity efficiency deductions and tightening verbosity in the remaining sections.