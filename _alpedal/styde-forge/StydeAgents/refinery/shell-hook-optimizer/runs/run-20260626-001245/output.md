SHELL HOOK OPTIMIZER v1
Domain: hooks-opt
Target: E:\Stryde\_alpedal\styde-forge
---
PRE-COMMAND VALIDATION HOOKS
File: hooks/pre-cmd/validate.sh
```bash
#!/usr/bin/env bash
# PreCmd: validate command safety before execution
PRE_CMD_ALLOWLIST="$HOME/.hermes/hooks/allowlist.txt"
PRE_CMD_BLOCKLIST="$HOME/.hermes/hooks/blocklist.txt"
PRE_CMD_HASH_DB="$HOME/.hermes/hooks/hash_db.json"
hook_pre_cmd_validate() {
  local cmd_raw="$*"
  local cmd_bin
  cmd_bin=$(echo "$cmd_raw" | awk '{print $1}' | xargs which 2>/dev/null)
  # Blocklist check
  if [[ -f "$PRE_CMD_BLOCKLIST" ]]; then
    while IFS= read -r blockpat; do
      [[ -z "$blockpat" || "$blockpat" =~ ^# ]] && continue
      if echo "$cmd_raw" | grep -qiE "$blockpat"; then
        echo "[HOOK:BLOCK] Command blocked: $cmd_raw (pattern: $blockpat)"
        return 1
      fi
    done < "$PRE_CMD_BLOCKLIST"
  fi
  # Allowlist check for destructive ops
  local destructive_patterns="rm -rf|dd if=|mkfs|:(){:|:};:|chmod -R 000|chown -R"
  if echo "$cmd_raw" | grep -qiE "$destructive_patterns"; then
    if [[ -f "$PRE_CMD_ALLOWLIST" ]]; then
      local cmd_hash
      cmd_hash=$(echo "$cmd_raw" | sha256sum | cut -d' ' -f1)
      if ! grep -qF "$cmd_hash" "$PRE_CMD_ALLOWLIST"; then
        echo "[HOOK:WARN] Destructive command not allowlisted: $cmd_raw"
        echo "         Hash: $cmd_hash"
        echo "         Add to $PRE_CMD_ALLOWLIST to allow"
        return 1
      fi
    else
      echo "[HOOK:CONFIRM] Run destructive command? (y/N): $cmd_raw"
      read -r confirm
      [[ "$confirm" != "y" && "$confirm" != "Y" ]] && return 1
    fi
  fi
  # Working directory guard
  if [[ "$cmd_raw" =~ ^rm\ -rf\ \. && "$PWD" == "/" ]]; then
    echo "[HOOK:BLOCK] rm -rf . in root. Aborting."
    return 1
  fi
  return 0
}
export -f hook_pre_cmd_validate
```
File: hooks/pre-cmd/syntax-check.sh
```bash
#!/usr/bin/env bash
# PreCmd: check file syntax before destructive edits
hook_pre_cmd_syntax() {
  local target_files=()
  # Detect files about to be modified (from git or last command)
  if [[ -n "$HERMES_MODIFY_FILES" ]]; then
    IFS=':' read -ra target_files <<< "$HERMES_MODIFY_FILES"
  fi
  for f in "${target_files[@]}"; do
    if [[ -f "$f" ]]; then
      case "$f" in
        *.py)
          python -m py_compile "$f" 2>/dev/null || {
            echo "[HOOK:SYNTAX] Python syntax error in $f"
            python -m py_compile "$f" 2>&1
            return 1
          }
          ;;
        *.json)
          python -m json.tool "$f" >/dev/null 2>&1 || {
            echo "[HOOK:SYNTAX] Invalid JSON in $f"
            return 1
          }
          ;;
        *.yaml|*.yml)
          python -c "import yaml; yaml.safe_load(open('$f'))" 2>/dev/null || {
            echo "[HOOK:SYNTAX] Invalid YAML in $f"
            return 1
          }
          ;;
        *.sh)
          bash -n "$f" 2>/dev/null || {
            echo "[HOOK:SYNTAX] Bash syntax error in $f"
            bash -n "$f" 2>&1
            return 1
          }
          ;;
      esac
    fi
  done
  return 0
}
export -f hook_pre_cmd_syntax
```
---
POST-COMMAND CLEANUP HOOKS
File: hooks/post-cmd/cleanup.sh
```bash
#!/usr/bin/env bash
# PostCmd: cleanup after command execution
POST_CMD_TEMP_DIR="$HOME/.hermes/hooks/tmp"
POST_CMD_LOG_DIR="$HOME/.hermes/hooks/logs"
hook_post_cmd_cleanup() {
  local exit_code=$1
  local cmd_raw="$2"
  local duration=$3
  mkdir -p "$POST_CMD_TEMP_DIR" "$POST_CMD_LOG_DIR"
  # Rotate logs - keep last 100
  local logfile="$POST_CMD_LOG_DIR/cmd_$(date +%Y%m%d_%H%M%S).log"
  {
    echo "TIMESTAMP: $(date -Iseconds)"
    echo "EXIT_CODE: $exit_code"
    echo "COMMAND: $cmd_raw"
    echo "DURATION: ${duration}s"
    echo "PWD: $PWD"
  } > "$logfile"
  # Prune old logs (>100)
  local log_count
  log_count=$(ls -1 "$POST_CMD_LOG_DIR"/*.log 2>/dev/null | wc -l)
  if (( log_count > 100 )); then
    ls -1t "$POST_CMD_LOG_DIR"/*.log | tail -n +101 | xargs rm -f 2>/dev/null
  fi
  # Clean temp files older than 1h
  find "$POST_CMD_TEMP_DIR" -type f -mmin +60 -delete 2>/dev/null
  # Auto-commit small changes if in git repo and exit 0
  if [[ $exit_code -eq 0 ]] && git rev-parse --git-dir >/dev/null 2>&1; then
    if [[ -n "$HERMES_AUTO_COMMIT" && "$HERMES_AUTO_COMMIT" == "1" ]]; then
      local changed
      changed=$(git status --porcelain | wc -l)
      if (( changed > 0 && changed < 10 )); then
        git add -A 2>/dev/null
        git commit -m "auto: $(echo "$cmd_raw" | head -c 80)" --no-verify 2>/dev/null
      fi
    fi
  fi
  return 0
}
export -f hook_post_cmd_cleanup
```
File: hooks/post-cmd/state-save.sh
```bash
#!/usr/bin/env bash
# PostCmd: save state snapshot for rollback
hook_post_cmd_save_state() {
  local exit_code=$1
  local state_dir="$HOME/.hermes/hooks/state"
  local snapshot_id
  snapshot_id="snap_$(date +%Y%m%d_%H%M%S)"
  mkdir -p "$state_dir"
  # Only save on failure for debugging
  if [[ $exit_code -ne 0 ]]; then
    local snap_file="$state_dir/$snapshot_id.json"
    {
      echo "{"
      echo "  \"timestamp\": \"$(date -Iseconds)\","
      echo "  \"exit_code\": $exit_code,"
      echo "  \"pwd\": \"$PWD\","
      if git rev-parse --git-dir >/dev/null 2>&1; then
        echo "  \"git_branch\": \"$(git branch --show-current 2>/dev/null)\","
        echo "  \"git_status\": $(git status --porcelain 2>/dev/null | head -20 | jq -R -s -c 'split(\"\n\")[:-1]' 2>/dev/null || echo '[]'),"
        echo "  \"git_diff\": $(git diff --no-color 2>/dev/null | head -50 | jq -R -s -c '.' 2>/dev/null || echo '\"\"')"
      else
        echo "  \"git_branch\": null,"
        echo "  \"git_status\": [],"
        echo "  \"git_diff\": \"\""
      fi
      echo "}"
    } > "$snap_file"
    # Keep last 20 failure snapshots
    local snap_count
    snap_count=$(ls -1 "$state_dir"/snap_*.json 2>/dev/null | wc -l)
    if (( snap_count > 20 )); then
      ls -1t "$state_dir"/snap_*.json | tail -n +21 | xargs rm -f 2>/dev/null
    fi
  fi
  return 0
}
export -f hook_post_cmd_save_state
```
---
GIT HOOKS INTEGRATION
File: hooks/git/pre-commit
```bash
#!/usr/bin/env bash
# Git: pre-commit hook - validate before commit
HOOKS_GIT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "[HOOK:GIT] Pre-commit validation..."
# Load pre-cmd validators
source "$HOOKS_GIT_DIR/pre-cmd/validate.sh" 2>/dev/null
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)
# 1. Syntax check all staged files
for f in $STAGED_FILES; do
  case "$f" in
    *.py)
      python -m py_compile "$f" 2>/dev/null || {
        echo "[HOOK:FAIL] Python syntax error in $f"
        git diff --cached -- "$f" | head -30
        exit 1
      }
      # Run ruff if available
      if command -v ruff &>/dev/null; then
        ruff check "$f" --quiet 2>/dev/null || {
          echo "[HOOK:WARN] Ruff issues in $f (not blocking)"
        }
      fi
      ;;
    *.sh)
      bash -n "$f" 2>/dev/null || {
        echo "[HOOK:FAIL] Bash syntax error in $f"
        exit 1
      }
      ;;
    *.json)
      python -m json.tool "$f" >/dev/null 2>&1 || {
        echo "[HOOK:FAIL] Invalid JSON in $f"
        exit 1
      }
      ;;
    *.yaml|*.yml)
      python -c "import yaml; yaml.safe_load(open('$f'))" 2>/dev/null || {
        echo "[HOOK:FAIL] Invalid YAML in $f"
        exit 1
      }
      ;;
    *.ts|*.tsx)
      if command -v npx &>/dev/null; then
        npx tsc --noEmit --pretty "$f" 2>/dev/null || {
          echo "[HOOK:WARN] TypeScript issues in $f (not blocking)"
        }
      fi
      ;;
    Cargo.toml)
      if command -v cargo &>/dev/null; then
        cargo verify-project 2>/dev/null || {
          echo "[HOOK:FAIL] Invalid Cargo.toml"
          exit 1
        }
      fi
      ;;
  esac
done
# 2. Check for merge conflicts
if git diff --cached | grep -qE '^\+<<<<<<< |^\+=======$|^\+>>>>>>> '; then
  echo "[HOOK:FAIL] Merge conflict markers detected in staged files"
  git diff --cached | grep -nE '^\+<<<<<<< |^\+=======$|^\+>>>>>>> '
  exit 1
fi
# 3. Check for debug artifacts
if git diff --cached | grep -qE '^\+.*\b(console\.log|debugger|print\(|pdb\.set_trace)\b'; then
  echo "[HOOK:WARN] Debug statements in staged files:"
  git diff --cached | grep -nE '^\+.*\b(console\.log|debugger|print\(|pdb\.set_trace)\b'
  echo "         Commit anyway? (y/N)"
  read -r confirm
  [[ "$confirm" != "y" && "$confirm" != "Y" ]] && exit 1
fi
# 4. Large file check (>1MB)
for f in $STAGED_FILES; fi
  local size
  size=$(git show :"$f" | wc -c 2>/dev/null || echo 0)
  if (( size > 1048576 )); then
    echo "[HOOK:BLOCK] File too large: $f (${size} bytes, max 1MB)"
    echo "         Use git-lfs or exclude this file"
    exit 1
  fi
done
echo "[HOOK:GIT] Pre-commit checks passed."
exit 0
```
File: hooks/git/pre-push
```bash
#!/usr/bin/env bash
# Git: pre-push hook - validate before push
echo "[HOOK:GIT] Pre-push validation..."
CURRENT_BRANCH=$(git branch --show-current)
PROTECTED_BRANCHES="master|main|develop|production"
# 1. Block force-push to protected branches
if [[ "$CURRENT_BRANCH" =~ ^($PROTECTED_BRANCHES)$ ]]; then
  echo "[HOOK:GIT] Protected branch: $CURRENT_BRANCH"
  echo "         Force push blocked. Use PR workflow instead."
  exit 1
fi
# 2. Block if branch has uncommitted changes
if [[ -n "$(git status --porcelain)" ]]; then
  echo "[HOOK:GIT] Uncommitted changes on $CURRENT_BRANCH"
  echo "         Commit or stash before push."
  exit 1
fi
# 3. Check CI status if configured
if [[ -f ".github/workflows/ci.yml" || -f ".gitlab-ci.yml" ]]; then
  # Local check: run tests
  if [[ -f "pyproject.toml" ]] && command -v pytest &>/dev/null; then
    echo "[HOOK:GIT] Running tests before push..."
    pytest -x --tb=short -q 2>/dev/null || {
      echo "[HOOK:FAIL] Tests failed. Fix before push."
      exit 1
    }
  fi
fi
echo "[HOOK:GIT] Pre-push checks passed."
exit 0
```
File: hooks/git/post-commit
```bash
#!/usr/bin/env bash
# Git: post-commit hook - post-commit actions
echo "[HOOK:GIT] Post-commit actions..."
COMMIT_MSG=$(git log -1 --pretty=%B)
COMMIT_HASH=$(git log -1 --pretty=%H)
# Log commit
echo "$(date -Iseconds) | $COMMIT_HASH | $(echo "$COMMIT_MSG" | head -1)" >> "$HOME/.hermes/hooks/logs/commits.log"
# Auto-tag based on commit type
if echo "$COMMIT_MSG" | grep -qiE '^feat(\(.+\))?:'; then
  echo "[HOOK:GIT] Feature commit detected. Consider tag: git tag -a v$(date +%Y%m%d)-feat -m \"$COMMIT_MSG\""
elif echo "$COMMIT_MSG" | grep -qiE '^fix(\(.+\))?:'; then
  echo "[HOOK:GIT] Fix commit detected."
elif echo "$COMMIT_MSG" | grep -qiE '^breaking|BREAKING'; then
  echo "[HOOK:GIT] BREAKING CHANGE. Tag major version."
fi
# Check for branch deletion candidates (already merged branches)
if git branch --merged | grep -vE '^\*|master|main|develop'; then
  local stale
  stale=$(git branch --merged | grep -vE '^\*|master|main|develop' | head -5)
  if [[ -n "$stale" ]]; then
    echo "[HOOK:GIT] Merged branches ready for cleanup:"
    echo "$stale"
  fi
fi
exit 0
```
---
ENVIRONMENT SETUP HOOKS
File: hooks/env/hermes-env.sh
```bash
#!/usr/bin/env bash
# Env: Hermes environment setup hooks
# Activate on shell start
if [[ -n "$HERMES_HOOKS_ENABLED" && "$HERMES_HOOKS_ENABLED" == "1" ]]; then
  # Pre-command hook via DEBUG trap
  hook_env_pre_cmd() {
    local last_cmd="$BASH_COMMAND"
    [[ -z "$last_cmd" || "$last_cmd" == "hook_"* ]] && return
    hook_pre_cmd_validate "$last_cmd" 2>&1 || {
      kill -INT $$
      return 1
    }
  }
  # Post-command hook via PROMPT_COMMAND
  hook_env_post_cmd() {
    local exit_code=$?
    local last_cmd
    last_cmd=$(history 1 | sed 's/^ *[0-9]* *//')
    [[ -z "$last_cmd" ]] && return
    local duration=$SECONDS
    hook_post_cmd_cleanup "$exit_code" "$last_cmd" "$duration" 2>/dev/null
    hook_post_cmd_save_state "$exit_code" 2>/dev/null
  }
  # Install hooks
  if [[ ! " ${PROMPT_COMMAND[*]} " =~ "hook_env_post_cmd" ]]; then
    PROMPT_COMMAND="hook_env_post_cmd;${PROMPT_COMMAND}"
  fi
  # DEBUG trap for pre-cmd
  trap 'hook_env_pre_cmd' DEBUG
  export HERMES_HOOKS_ACTIVE=1
fi
# Tool-specific path setup
hook_env_setup_tools() {
  # uv compatibility
  if command -v uv &>/dev/null; then
    export UV_COMPILE_BYTECODE=1
    eval "$(uv generate-shell-completion bash 2>/dev/null)"
  fi
  # Rust/Cargo
  if [[ -f "$HOME/.cargo/env" ]]; then
    source "$HOME/.cargo/env" 2>/dev/null
  fi
  # Node/nvm
  if [[ -f "$HOME/.nvm/nvm.sh" ]]; then
    source "$HOME/.nvm/nvm.sh" 2>/dev/null
  fi
}
hook_env_setup_tools
# Forge-specific env
if [[ -d "E:/Stryde/_alpedal/styde-forge" ]]; then
  export STYDE_FORGE_ROOT="E:/Stryde/_alpedal/styde-forge"
  export HERMES_DEFAULT_MODEL="deepseek-v4-flash"
fi
```
File: hooks/env/forge-env.sh
```bash
#!/usr/bin/env bash
# Env: Styde Forge environment setup
FORGE_ROOT="E:/Stryde/_alpedal/styde-forge"
hook_env_forge() {
  if [[ -d "$FORGE_ROOT" ]]; then
    export FORGE_ROOT
    export FORGE_BLUEPRINTS="$FORGE_ROOT/blueprints"
    export FORGE_AGENTS="$FORGE_ROOT/agents"
    export FORGE_KNOWLEDGE="$FORGE_ROOT/knowledge"
    # Forge prompt — show active blueprint count
    if [[ -d "$FORGE_BLUEPRINTS" ]]; then
      local bp_count
      bp_count=$(find "$FORGE_BLUEPRINTS" -name '*.yaml' 2>/dev/null | wc -l)
      export FORGE_BLUEPRINT_COUNT=$bp_count
    fi
  fi
}
hook_env_forge
# Forge custom prompt
if [[ -n "$HERMES_HOOKS_CUSTOM_PS1" && "$HERMES_HOOKS_CUSTOM_PS1" == "1" ]]; then
  PS1='\[\033[38;5;202m\]⚡\u@\h:\[\033[38;5;39m\]\w\[\033[0m\] $(git branch 2>/dev/null | grep "^*" | tr -d "* " | xargs -I{} echo "\[\033[38;5;214m\]({})\[\033[0m\]") \$ '
fi
```
---
HOOK SECURITY AND ALLOWLISTING
File: hooks/security/allowlist.txt
```
# Hermes Shell Hook Allowlist
# Format: one sha256 hash per line, or regex patterns with ^#
# Lines starting with # are comments
#
# Generated: $(date -Iseconds)
#
# To allowlist a command:
#   echo -n "your command here" | sha256sum >> ~/.hermes/hooks/allowlist.txt
#
# To allowlist a pattern:
#   echo "^git push origin.*" >> ~/.hermes/hooks/allowlist.txt
```
File: hooks/security/blocklist.txt
```
# Hermes Shell Hook Blocklist
# Regex patterns. One per line.
# Lines starting with # are comments.
# Destructive system operations
^rm -rf /$
^dd if=/dev/zero of=/dev/sd
^mkfs\.ext[234] /
^mkfs\.btrfs /
^mkfs\.xfs /
^dd if=/dev/random
^:\(\)\s*\{.*\}:\s*;.*\:
# Crypto/ransomware patterns
^curl.*\||^wget.*\|bash$
^\s*eval\s*"\$\(curl
^\s*bash\s*<\s*\(curl
# Remote execution without allowlist
^ssh .* "rm
^ssh .* "dd
# Process killer
^killall -9
# Permission nuking
^chmod -R 000 /
^chown -R .*:\s*/
```
File: hooks/security/manager.sh
```bash
#!/usr/bin/env bash
# Sec: hook security manager — allowlist/blocklist management
SEC_ALLOWLIST="$HOME/.hermes/hooks/allowlist.txt"
SEC_BLOCKLIST="$HOME/.hermes/hooks/blocklist.txt"
SEC_LOGS="$HOME/.hermes/hooks/logs/security.log"
hook_sec_init() {
  mkdir -p "$HOME/.hermes/hooks" "$HOME/.hermes/hooks/logs"
  [[ ! -f "$SEC_ALLOWLIST" ]] && touch "$SEC_ALLOWLIST"
  [[ ! -f "$SEC_BLOCKLIST" ]] && touch "$SEC_BLOCKLIST"
  echo "$(date -Iseconds) | INIT | Security hooks initialized" >> "$SEC_LOGS"
}
hook_sec_allow() {
  local cmd="$*"
  [[ -z "$cmd" ]] && { echo "Usage: hook_sec_allow <command>"; return 1; }
  local hash
  hash=$(echo -n "$cmd" | sha256sum | cut -d' ' -f1)
  if grep -qF "$hash" "$SEC_ALLOWLIST" 2>/dev/null; then
    echo "[SEC] Command already allowlisted: $cmd"
  else
    echo "$hash  # $cmd" >> "$SEC_ALLOWLIST"
    echo "$(date -Iseconds) | ALLOW | $cmd | $hash" >> "$SEC_LOGS"
    echo "[SEC] Allowlisted: $cmd (hash: ${hash:0:12}...)"
  fi
}
hook_sec_block() {
  local pattern="$*"
  [[ -z "$pattern" ]] && { echo "Usage: hook_sec_block <regex_pattern>"; return 1; }
  if grep -qF "$pattern" "$SEC_BLOCKLIST" 2>/dev/null; then
    echo "[SEC] Pattern already blocked: $pattern"
  else
    echo "$pattern" >> "$SEC_BLOCKLIST"
    echo "$(date -Iseconds) | BLOCK | $pattern" >> "$SEC_LOGS"
    echo "[SEC] Blocked pattern: $pattern"
  fi
}
hook_sec_status() {
  echo "=== Allowlist ($(wc -l < "$SEC_ALLOWLIST" 2>/dev/null || echo 0) entries) ==="
  head -20 "$SEC_ALLOWLIST" 2>/dev/null || echo "(empty)"
  echo ""
  echo "=== Blocklist ($(wc -l < "$SEC_BLOCKLIST" 2>/dev/null || echo 0) entries) ==="
  head -20 "$SEC_BLOCKLIST" 2>/dev/null || echo "(empty)"
  echo ""
  echo "=== Recent events ==="
  tail -10 "$SEC_LOGS" 2>/dev/null || echo "(no events)"
}
hook_sec_verify_integrity() {
  # Verify hook files haven't been tampered with
  local hook_dir="$HOME/.hermes/hooks"
  local manifest="$hook_dir/manifest.sha256"
  if [[ ! -f "$manifest" ]]; then
    echo "[SEC] No manifest found. Generating..."
    find "$hook_dir" -type f -not -name 'manifest.sha256' -not -path '*/logs/*' -exec sha256sum {} \; > "$manifest"
    echo "[SEC] Manifest generated. Verify manually for trust."
    return 0
  fi
  echo "[SEC] Verifying hook integrity..."
  sha256sum -c "$manifest" --quiet 2>/dev/null || {
    echo "[SEC:ALERT] Hook file integrity check FAILED!"
    echo "         Possible tampering detected."
    sha256sum -c "$manifest" 2>&1 | grep -v ': OK$'
    return 1
  }
  echo "[SEC] All hook files intact."
  return 0
}
export -f hook_sec_init hook_sec_allow hook_sec_block hook_sec_status hook_sec_verify_integrity
# Auto-init
hook_sec_init
```
File: hooks/security/audit.sh
```bash
#!/usr/bin/env bash
# Sec: periodic audit and reporting
hook_sec_audit() {
  local report="$HOME/.hermes/hooks/logs/audit_$(date +%Y%m%d).log"
  {
    echo "=== Security Audit $(date -Iseconds) ==="
    echo ""
    echo "Allowlist entries: $(wc -l < "$HOME/.hermes/hooks/allowlist.txt" 2>/dev/null || echo 0)"
    echo "Blocklist entries: $(wc -l < "$HOME/.hermes/hooks/blocklist.txt" 2>/dev/null || echo 0)"
    echo ""
    # Check for weak patterns
    echo "=== Weak allowlist entries ==="
    grep -v '^#' "$HOME/.hermes/hooks/allowlist.txt" 2>/dev/null | while IFS= read -r line; do
      if echo "$line" | grep -qE '^\s*#'; then
        continue
      fi
      echo "Review: $line"
    done
    echo ""
    echo "=== Recent blocked commands ==="
    grep 'BLOCK' "$HOME/.hermes/hooks/logs/security.log" 2>/dev/null | tail -10
  } > "$report"
  echo "[SEC] Audit written to $report"
}
# Cron hook: run audit daily
if [[ -n "$HERMES_HOOKS_AUDIT_CRON" && "$HERMES_HOOKS_AUDIT_CRON" == "1" ]]; then
  hook_sec_audit
fi
export -f hook_sec_audit
```
---
INSTALLATION SCRIPT
File: hooks/setup.sh
```bash
#!/usr/bin/env bash
# Shell Hook Optimizer — Installer
set -euo pipefail
INSTALL_DIR="$HOME/.hermes/hooks"
FORGE_ROOT="E:/Stryde/_alpedal/styde-forge"
GIT_HOOKS_DIR="$FORGE_ROOT/.git/hooks"
echo "=== Shell Hook Optimizer v1 ==="
echo "Installing to: $INSTALL_DIR"
echo ""
# Create directory structure
mkdir -p "$INSTALL_DIR"/{pre-cmd,post-cmd,git,env,security,logs,state,tmp}
# Copy all hook files
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp -r "$SCRIPT_DIR"/pre-cmd/*.sh "$INSTALL_DIR/pre-cmd/" 2>/dev/null || true
cp -r "$SCRIPT_DIR"/post-cmd/*.sh "$INSTALL_DIR/post-cmd/" 2>/dev/null || true
cp -r "$SCRIPT_DIR"/env/*.sh "$INSTALL_DIR/env/" 2>/dev/null || true
cp -r "$SCRIPT_DIR"/security/*.txt "$INSTALL_DIR/security/" 2>/dev/null || true
cp -r "$SCRIPT_DIR"/security/*.sh "$INSTALL_DIR/security/" 2>/dev/null || true
# Make executable
find "$INSTALL_DIR" -name '*.sh' -exec chmod +x {} \;
# Install git hooks
echo ""
echo "=== Installing git hooks ==="
if [[ -d "$GIT_HOOKS_DIR" ]]; then
  cp "$SCRIPT_DIR/git/pre-commit" "$GIT_HOOKS_DIR/pre-commit"
  cp "$SCRIPT_DIR/git/pre-push" "$GIT_HOOKS_DIR/pre-push"
  cp "$SCRIPT_DIR/git/post-commit" "$GIT_HOOKS_DIR/post-commit"
  chmod +x "$GIT_HOOKS_DIR/pre-commit"
  chmod +x "$GIT_HOOKS_DIR/pre-push"
  chmod +x "$GIT_HOOKS_DIR/post-commit"
  echo "Git hooks installed to $GIT_HOOKS_DIR"
else
  echo "WARNING: No .git/hooks directory found at $GIT_HOOKS_DIR"
  echo "         Git hooks not installed."
fi
# Source env hooks in bashrc
BASHRC="$HOME/.bashrc"
ENV_SOURCE_LINE="source $INSTALL_DIR/env/hermes-env.sh"
if ! grep -qF "$ENV_SOURCE_LINE" "$BASHRC" 2>/dev/null; then
  echo "" >> "$BASHRC"
  echo "# Hermes Shell Hook Optimizer" >> "$BASHRC"
  echo "export HERMES_HOOKS_ENABLED=1" >> "$BASHRC"
  echo "$ENV_SOURCE_LINE" >> "$BASHRC"
  echo "Env hooks added to $BASHRC"
fi
# Generate manifest for integrity checking
echo ""
echo "=== Generating integrity manifest ==="
find "$INSTALL_DIR" -type f -not -path '*/logs/*' -not -name 'manifest.sha256' -exec sha256sum {} \; > "$INSTALL_DIR/manifest.sha256"
echo "Manifest: $INSTALL_DIR/manifest.sha256"
echo ""
echo "=== Installation complete ==="
echo "Source $BASHRC or restart shell to activate."
echo "Commands:"
echo "  hook_sec_status          - View allowlist/blocklist"
echo "  hook_sec_allow 'cmd'     - Allowlist a command"
echo "  hook_sec_block 'pattern' - Block a command pattern"
echo "  hook_sec_verify_integrity - Check hook file integrity"
echo "  hook_sec_audit           - Run security audit"
```
---
USAGE
Setup: run hooks/setup.sh from project root. Sources into bashrc. Three activation modes:
1. FULL: HERMES_HOOKS_ENABLED=1 — DEBUG trap + PROMPT_COMMAND active. Every command validated pre-run and logged post-run.
2. GIT-ONLY: Only git hooks active (pre-commit, pre-push, post-commit). No shell overhead.
3. MANUAL: Source individual hooks on demand. `source ~/.hermes/hooks/security/manager.sh` then call hook_sec_allow 'git push origin master'.
Integration points:
- PreCmd validates every shell command against blocklist/allowlist before execution
- PostCmd logs exit codes, duration, autoclears temp files
- Git hooks block bad commits (syntax errors, merge conflicts, debug code, large files)
- Security manager maintains allowlist hash database and blocklist regex patterns
- Integrity manifest detects hook file tampering
For Styde Forge specifically: pre-commit validates Python .py files via py_compile, checks for stray debug print() calls, blocks files >1MB. Pre-push blocks direct pushes to master/main. Post-commit logs commit activity to ~/.hermes/hooks/logs/commits.log.