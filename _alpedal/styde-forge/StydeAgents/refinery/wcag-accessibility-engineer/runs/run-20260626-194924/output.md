Audit: teacher feedback cross-run analysis
Subject: BLUEPRINT.md, persona.md, config.yaml version integrity
Source runs: 20260626-193320 (87.8), 20260626-194746 (91.4)
Findings:
1. Duplicate content between BLUEPRINT.md and persona.md
   - contrast methodology tables duplicated
   - step-by-step completion checklist duplicated
   - tool path descriptions duplicated
   - Fix: deduplicate BLUEPRINT.md, use cross-references to persona.md
2. YAML formatting inconsistency in BLUEPRINT.md
   - mixed styles: yaml fenced blocks, indented YAML, raw markdown headings inside value fields
   - Fix: normalize to single style per file
3. Missing references section in BLUEPRINT.md
   - no document map for linked files (persona.md, config.yaml)
   - Fix: add References section with one-line summaries
4. Version drift between persona.md (v1) and BLUEPRINT.md (v2)
   - persona.md contains v1 constraints that contradict current blueprint
   - Fix: bump persona.md to v2, strip conflicting v1 references
5. Config gaps in config.yaml
   - missing output directory configuration
   - missing retry logic
   - missing fallback model declaration
   - Fix: add maxretries: 3, backoff: 2.0, fallback model, output dir
6. No version sync mechanism
   - no version bumper comment in persona.md
   - Fix: add # Version: 2 at top of persona.md
Severity assessment:
  High: items 1, 4 (duplication and drift undermine trustworthiness)
  Medium: items 2, 5 (formatting waste, config gaps)
  Low: items 3, 6 (nice-to-have structural improvements)
Priority order for remediation:
  bump persona.md to v2 and strip v1 constraints
  deduplicate BLUEPRINT.md, replace with cross-references
  normalize YAML formatting in BLUEPRINT.md
  add retry logic and fallback model to config.yaml
  add version bumper to persona.md
  add References section to BLUEPRINT.md