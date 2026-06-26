Pipeline stage: Generation + Evaluation gate
Teacher feedback applied across three files. Changes address two root causes:
1. clarity — unified-diff format for config changes
2. efficiency — CSS deduplication standards + persona pre-submit grep check
==========
BLUEPRINT.md
Section 4 (Change Planning Protocol):
All change plans for config or code files MUST use strict unified-diff format (---/+++) with three-line context blocks. Commentary precedes or follows the diff block — never interleaved. For YAML config changes, each diff block covers exactly one file; linked files appear in sequential diff blocks separated by a blank line.
Wrong:
  Set `weight: 1.2` in config.yaml:
    evaluationcriteria:
      efficiency:
        weight: 1.2
  Also change persona.md to add...
Right (unified-diff blocks):
  --- a/config.yaml
  +++ b/config.yaml
  @@ evaluationcriteria +2,7 @@
     efficiency:
  -    weight: 1.0
  +    weight: 1.2
  --- a/persona.md
  +++ b/persona.md
  @@ +83,4 @@
  +qualitygate: before marking complete, grep for ::before duplicates and .space dimension constants; refactor into shared layer or CSS custom property.
3. Efficiency Standards (new section, placed before "Spatial Quality Requirements"):
  Efficiency Standards
  All CSS output across multiple mockups or dashboard variants must satisfy:
  a) Shared glass-surface, edge-glow, depth-plane, and frosted-texture styles reside in a single base utility layer or stylesheet.
  b) Per-mockup files contain only unique overrides — never re-declare shared properties.
  c) All repeatable values (colors, sizes, blurs, z-indices, animation durations) use CSS custom properties defined in :root.
  d) Before verification, grep for ::before pseudo-element duplicates and .space dimension constants appearing identically in more than one file; refactor matching blocks into a shared layer or custom property.
  e) CSS file size budget: each per-mockup stylesheet must not exceed 10KB or 40% of the shared layer, whichever is larger. Flag oversized files at the Gate stage.
==========
persona.md
Append to the end of the behavioral checklist:
qualitygate pre-submit check (Gate stage)
Before marking any mockup task complete:
  grep -rn '::before' mockups/ | sort | uniq -d  > /tmp/dup_before.txt
  grep -rn '\.space' mockups/ | sort | uniq -d   > /tmp/dup_space.txt
  if [ -s /tmp/dup_before.txt ] || [ -s /tmp/dup_space.txt ]; then
    echo "FAIL: Duplicate CSS blocks found. Refactor into shared layer."
    exit 1
  fi
  echo "PASS: No duplicate ::before or .space constants found."
Also: ASCII-normalize all file content before verification. Replace em-dash (U+2014) with regular dash, smart quotes ("") with straight quotes (""). Run verify-preflight.sh in dry-run mode to catch encoding mismatches before real check.
==========
config.yaml (target: evaluationcriteria section)
evaluationcriteria:
  clarity:
    weight: 1.0
  accuracy:
    weight: 1.0
  efficiency:
    weight: 1.2
  completeness:
    weight: 1.0
  design_quality:
    weight: 1.0
==========
Feedback-to-pipeline mapping
clarity changes protect Evaluation stage — unified diffs prevent the judge from scoring down on presentation noise.
efficiency changes protect Gate stage — CSS dedup grep runs before promotion, catching bloat early.
efficiency.weight=1.2 protects Generation stage — forces the agent to allocate attention proportionally during creation, since its self-assessment overrates efficiency.
qualitygate grep in persona protects Gate stage — enforces the pre-submit mechanical check.
ASCII-normalization step protects Gate stage — em-dash mismatches previously caused false negatives in verification.
==========
Design artifacts not requested in the parent task — the above is a targeted feedback-incorporation pass only. If mockup generation is needed, that is a separate task that will produce 3+ spatial glass dashboard mockups.