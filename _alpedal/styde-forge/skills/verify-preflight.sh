#!/usr/bin/env bash
set -o pipefail

# verify-preflight.sh
# Dry-run encoding validator for forge verification scripts.
# Pipeline stage: Gate — catches unicode encoding mismatches before real check.
# Usage:
#   ./skills/verify-preflight.sh <verification-script> [args...]
#
# Does:
#   1. Scan the verification script for unicode characters outside ASCII range.
#   2. Run the script in dry-run mode (envar VERIFY_PREFLIGHT=1) and capture
#      any lines containing non-ASCII output that would cause match failures.
#   3. Exit 0 if clean, 1 if encoding issues found with a report.

SCRIPT="$1"
if [ -z "$SCRIPT" ] || [ ! -f "$SCRIPT" ]; then
  echo "Usage: $0 <verification-script> [args...]"
  echo "Error: script not found or not specified"
  exit 1
fi
shift

has_issues=0
issues=()

# --- Check 1: Static scan of the script source for non-ASCII patterns ---
echo ":: PREFLIGHT :: Static scan of $SCRIPT for non-ASCII characters..."
while IFS= read -r line; do
  linenum=$(echo "$line" | cut -d: -f1)
  content=$(echo "$line" | cut -d: -f2-)
  if echo "$content" | grep -Pn '[\x80-\xFF]' >/dev/null 2>&1; then
    echo "  WARN  line $linenum  non-ASCII character detected"
    has_issues=1
  fi
done < <(grep -n '.' "$SCRIPT" | grep -v '^[0-9]*:#')

# --- Check 2: Dry-run execution, trap non-ASCII output ---
echo ":: PREFLIGHT :: Dry-run mode: VERIFY_PREFLIGHT=1 $SCRIPT $*"
output=$(VERIFY_PREFLIGHT=1 "$SCRIPT" "$@" 2>&1)
dry_exit=$?

while IFS= read -r line; do
  if echo "$line" | grep -Pn '[\x80-\xFF]' >/dev/null 2>&1; then
    echo "  NON-ASCII OUTPUT: $line"
    has_issues=1
  fi
done < <(echo "$output")

# --- Check 3: Common unicode punctuation patterns ---
echo ":: PREFLIGHT :: Scanning for known unicode pitfalls..."
while IFS= read -r line; do
  linenum=$(echo "$line" | cut -d: -f1)
  content=$(echo "$line" | cut -d: -f2-)
  if echo "$content" | grep -q '—'; then
    echo "  WARN  line $linenum  em-dash (—) should be replaced with regular dash (-)"
    has_issues=1
  fi
  if echo "$content" | grep -q '[“”]'; then
    echo "  WARN  line $linenum  smart double quotes should be replaced with straight quotes"
    has_issues=1
  fi
  if echo "$content" | grep -q '[‘’]'; then
    echo "  WARN  line $linenum  smart single quotes should be replaced with straight quotes"
    has_issues=1
  fi
  if echo "$content" | grep -q '…'; then
    echo "  WARN  line $linenum  ellipsis (…) should be replaced with three periods (...)"
    has_issues=1
  fi
  if echo "$content" | grep -q '•'; then
    echo "  WARN  line $linenum  bullet (•) should be replaced with ASCII asterisk or dash"
    has_issues=1
  fi
done < <(grep -n '.' "$SCRIPT" | grep -v '^[0-9]*:#' | grep -v '^[0-9]*:$')

# --- Summary ---
if [ "$has_issues" -eq 1 ]; then
  echo ":: PREFLIGHT :: FAIL — encoding issues found. Fix before running real verification."
  echo ":: HINT :: Use: sed -i 's/—/-/g; s/\xe2\x80\x9c/\\"/g; s/\xe2\x80\x9d/\\"/g' \"$SCRIPT\""
  exit 1
else
  echo ":: PREFLIGHT :: PASS — all ASCII-safe."
  exit "$dry_exit"
fi
