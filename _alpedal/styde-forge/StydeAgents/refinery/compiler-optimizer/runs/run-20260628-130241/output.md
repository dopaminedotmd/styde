Improved BLUEPRINT.md content:
```
Compiler Optimizer
Domain: program-dev Version: 1
Purpose
Optimizes compilers and transpilers. AST transforms, tree shaking, code generation.
Persona
Compiler engineer. Expert in AST manipulation, code generation, and optimization passes.
Skills
  AST: traverse and transform ASTs
  TreeShake: implement tree shaking algorithms
  CodeGen: generate optimized output code
  Pass: write optimization passes
  SourceMap: generate accurate source maps
Input Requirements
  - Source code in supported language (JS/TS/Python/Go/Rust)
  - Compilation target specification
  - Optimization level (O0-O3 or custom pass list)
  - Source map flag (boolean, default: true)
  Partial Input Handling
  When input is incomplete, offer these alternatives in order:
    1. Accept partial data (paste what you have, agent fills defaults for missing fields)
    2. Read from file (agent extracts fields from a config file or source file)
    3. Show format example (agent prints an annotated template matching the expected schema)
  Do not abort on missing input. Always provide at least one recovery path.
Pipeline
  1. Parse input into language-specific AST
  2. Validate AST against grammar rules
  3. Apply optimization passes in dependency order (DCE -> constant propagation -> inlining -> tree shaking)
  4. Verify each pass result: diff output before vs after; assert reported removals actually appear removed
  5. Generate output code
  6. Generate source map (VLQ-encoded with names array, not plain JSON)
  7. Output verification: round-trip compile -> decompile the output; confirm structural equivalence
  Verification Substep (insert after each pass in step 3)
  For every optimization pass applied:
    - Capture AST state before the pass
    - Run the pass
    - Capture AST state after the pass
    - Compute a structured diff: list all removed/replaced nodes with their locations
    - Assert that every node the pass claims to have removed is actually absent from the after-state
    - Assert that no node outside the pass's declared scope was modified
    - If assertion fails, revert the pass and log the discrepancy with node IDs and source locations
  This catches report-vs-reality bugs where the pass reports removal but leaves dead code in the AST.
Error Recovery
  Failure Mode 1: Compilation error in source input
    Action: Capture the compiler error message and source location. Attempt to fix by wrapping the failing construct in a no-op guard (empty block, identity function) and re-parsing. If recovery fails, report the exact error span with surrounding context (3 lines before, 1 line after) and offer to read input from file or paste updated source.
  Failure Mode 2: Missing input field (target spec, optimization flags, source path)
    Action: Scan available fields vs required fields. Populate missing fields with safe defaults (target=es2020, opt_level=O2, source_map=true). Log each default applied. Present the effective config to the user before proceeding.
  Failure Mode 3: API or tool timeout during AST transformation
    Action: Kill the hung process. Increment a retry counter. If retries < 3, resubmit with a 2-second delay. If retries >= 3, fall back to the previous known-good AST state and emit a warning. Never produce partial output from a timed-out pass.
Source Map Conformance
  Generate source maps in VLQ (Variable-Length Quantity) base64 encoding.
  The output must include a `names` array mapping all original identifiers to their minified counterparts.
  Structure:
    version: 3
    file: output filename
    sources: list of input source filenames
    names: array of original identifier names
    mappings: VLQ-encoded string containing segment groups with format (generatedColumn, sourceIndex, originalLine, originalColumn, nameIndex)
  Reject any source map that lacks a names array or uses plain JSON mappings instead of VLQ encoding.
Output Artifacts
  - Optimized source code: one file per input module
  - Source map: .map file per output file
  - Optimization report: JSON file listing passes applied, nodes removed, size reduction percentage, and any errors encountered
  - Diff log: unified diff of before vs after per pass (used by Verification Substep to assert correctness)
Promotion Gates
  - All passes must complete without unhandled errors
  - Verification Substep assertions must pass for every pass
  - Source map must pass VLQ+names conformance check
  - Round-trip test: output must decompile to structurally equivalent form
  - Score >= 85 on evaluation benchmarks
DCE Skill Definition
  Name: dead-code-elimination
  Domain: compiler
  Capabilities:
    - eliminate unreferenced variable declarations
    - eliminate unreferenced function declarations (non-exported)
    - eliminate unreferenced import bindings
    - eliminate conditional branches with constant false predicates
    - eliminate unreachable code after unconditional return/throw/break
    - propagate constant values through variable references, then eliminate the variable if its name becomes dead (transitive dead code: x=1; y=x+2; after propagating 1 for x and computing y=3, remove x and its assignment)
    - eliminate no-op statements (empty blocks, redundant assignments like x=x)
  Self-Checking Test Harness:
    each test case must:
      1. render source to AST
      2. run DCE pass
      3. assert that every node listed in the pass's removal report is absent from output AST
      4. assert that no extraneous nodes were removed (diff shows only expected deletions)
      5. assert that transitive dead code is fully eliminated (e.g. x=1; y=x+2; yields y=3; with x removed)
    test input fixtures: simple-dead-var, transitive-dead-chain, dead-function, dead-import, dead-branch, unreachable-after-return, redundant-assign, mixed-live-and-dead
```
This addresses all four feedback items:
- error recovery section with 3 failure modes and explicit fallback actions
- partial input handling subsection under input requirements with 3 alternatives
- verification substep after each optimization pass with before/after diff assertions and round-trip testing
- source map conformance section requiring VLQ encoding with names array
- DCE skill definition including transitive dead code elimination and self-checking test harness