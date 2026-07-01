DETECTION heuristics per fix level:
fix_level_1 (format/instruction ignorance):
  heuristic: if assistant output starts with apology (sorry, apologies, my apologies) > 3 tokens AND contains no code/config output: flag format-ignorance
  heuristic: if assistant output contains markdown fences but caveman-mode disallows them: flag format-violation
  heuristic: if assistant output length > 2000 chars without structural breaks: flag verbosity
fix_level_2 (context/model boundary confusion):
  heuristic: if assistant references its own training data cutoff date: flag temporal-leak
  heuristic: if assistant says "I don't have access" or "I cannot see" about user-provided context: flag context-blindness
  heuristic: if assistant score dimension claims evidence not in prompt: flag hallucinated-evidence
fix_level_3 (hallucination/invention):
  heuristic: if assistant names a file or function that search_files shows does not exist: flag file-hallucination
  heuristic: if assistant describes API parameters not matching the tool's openapi spec: flag api-hallucination
  heuristic: if assistant claims output was produced but no terminal/process call confirms it: flag fake-execution
persona.md before/after:
before: "You are CLI tool specialist. Expert in clap/cobra/commander, terminal UX, and shell integration."
after: "You are a CLI tool builder. When a task involves argument parsing, use clap (Rust) or cobra (Go) or argparse (Python) -- select based on the project's existing language. Never describe a CLI interface verbally: produce the actual struct/command definition. Add --help output that includes usage examples. If output is long, pipe through less or add --paginate flag. Generate shell completions script as a separate deliverable file."
config.yaml VALIDATION block:
settings:
  language:
    description: "Target programming language for the CLI tool"
    enforcedby: cli_blueprint_validator.py ::check_language_supported()
    values: [rust, go, python, typescript]
    default: python
    validate: if unknown, fall back to project root's Cargo.toml/go.mod/pyproject.toml
  arg_parser:
    description: "Argument parsing library to use"
    enforcedby: cli_blueprint_validator.py ::check_arg_parser_compat()
    values: [clap, cobra, argparse, commander, yargs]
    validate: must match language -- clap only for rust, cobra for go, argparse for python
  progress_bars:
    description: "Whether to include progress bars"
    enforcedby: cli_blueprint_validator.py ::check_progress_deps()
    type: boolean
    default: true
    validate: if true, ensure dependency is added to requirements/build file
  shell_completions:
    description: "Generate shell completion scripts"
    enforcedby: cli_blueprint_validator.py ::check_completions_output()
    type: boolean
    default: false
    validate: if true, add --completions bash|zsh|fish flag AND generate script file
BLUEPRINT.md deduplicated three-level fix section:
Fix specifications for composite evaluator (authoritative version -- all other fix references in this file are overridden by this section):
DETECTION (common to all levels):
  Run detection heuristics (defined under each level) on the assistant's raw output before scoring.
  If any heuristic triggers at level 1, apply fix_level_1 first, then re-evaluate.
  If any heuristic triggers at level 2, apply fix_level_2 first, then re-evaluate.
  If any heuristic triggers at level 3, apply fix_level_3 first, then re-evaluate.
  Multiple levels may trigger simultaneously -- apply highest level first.
fix_level_1: Format/instruction ignorance
  DETECTION:
    heuristic_1: output starts with apology > 3 tokens and no code/config
    heuristic_2: markdown fences present when caveman-mode is on
    heuristic_3: output > 2000 chars without structural breaks
  FIX: Re-issue prompt with caveman-mode reminder. Strip all markdown. Rewrite with plain text + YAML only.
fix_level_2: Context/model boundary confusion
  DETECTION:
    heuristic_1: references training data cutoff date
    heuristic_2: claims inability to access user-provided context
    heuristic_3: scores dimensions without verifiable evidence in prompt
  FIX: Re-issue with all context prepended. Require evidence citation per dimension. Score unverifiable items as N/A.
fix_level_3: Hallucination/invention
  DETECTION:
    heuristic_1: names files that do not exist in repo
    heuristic_2: describes API params not matching tool spec
    heuristic_3: claims execution with no terminal/process call
  FIX: Halt scoring. Re-run with search_files verification. Only score dimensions backed by tool output.
context preflight step (added to scoring section):
  Before scoring any dimension, run preflight:
    1. list each rubric item
    2. for each item, state what evidence from the user prompt supports it
    3. if no evidence found, score as N/A (not assumed full marks)
    4. print preflight table before score table
confidence per dimension:
  For each rubric dimension, append one of [high|medium|low] with a one-sentence justification citing prompt evidence.
  Example: "accuracy: high (all file paths verified via search_files, output matches tool result)"
dependency & side-effect check:
  For each proposed fix, output:
    depends_on: [list of files, config keys, or tools the fix needs to work]
    might_break: [list of downstream processes that depend on changed behavior]
    rollback: [exact revert command or steps]