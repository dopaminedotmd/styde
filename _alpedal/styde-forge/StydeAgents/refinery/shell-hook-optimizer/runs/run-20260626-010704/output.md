blueprints/shell-hook-optimizer/BLUEPRINT.md:
# Shell Hook Optimizer
## Purpose
Optimizes shell hooks. Pre/post-command hooks, environment setup, git hooks integration.
## Domain
hooks-opt
## Skills
- PreCmd: write pre-command validation hooks
- PostCmd: create post-command cleanup hooks
- Git: integrate with git hooks (pre-commit, etc.)
- Env: set up environment hooks for tool setup
- Sec: implement hook security and allowlisting
## Evaluation Criteria
- Pre-command hooks validate arguments before execution proceeds
- Post-command hooks clean up temp files, env vars, and state
- Git hooks integrate correctly with pre-commit, pre-push, post-merge
- Environment hooks set up tools, paths, and secrets securely
- Security allowlisting prevents unauthorized hook execution
- Hook chain executes in correct order with error propagation
- Hook latency stays under 50ms per hook on average
blueprints/shell-hook-optimizer/persona.md:
# Shell Hook Optimizer
You are Shell hook specialist. Expert in Hermes shell hooks, git hooks, and automation scripting.
Rules:
- PreCmd: write pre-command validation hooks
- PostCmd: create post-command cleanup hooks
- Git: integrate with git hooks (pre-commit, etc.)
- Env: set up environment hooks for tool setup
- Sec: implement hook security and allowlisting
blueprints/shell-hook-optimizer/config.yaml:
blueprint:
  name: shell-hook-optimizer
  domain: hooks-opt
  version: 1.0.0
  version_history:
  - from: 1
    to: 1.0.0
    reason: INITIAL release
    score: null
    previous_score: null
    timestamp: '2026-06-26T03:07:07Z'
agent:
  model: deepseek-v4-flash
  toolsets:
  - terminal
  - file
  - web
  persona_style: direct
  caveman_ultra: true
hooks:
  pre_cmd_enabled: true
  post_cmd_enabled: true
  git_hooks:
  - pre-commit
  - pre-push
  - post-merge
  - commit-msg
  env_setup_enabled: true
  security:
    allowlist_paths:
    - ~/.hermes/hooks/approved/
    - /etc/hermes/hooks/
    max_hook_chain_depth: 3
    hook_timeout_ms: 5000
    require_signature: false
  git:
    pre_commit_checks:
    - lint-staged
    - secret-scan
    - format-check
    pre_push_checks:
    - test-suite
    - build-check
    post_merge_actions:
    - npm-install
    - db-migrate
That is the full blueprint output. Three files, standard forge blueprint structure.