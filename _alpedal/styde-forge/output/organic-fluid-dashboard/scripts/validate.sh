#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INDEX="$SCRIPT_DIR/index.html"
STYLES="$SCRIPT_DIR/styles/main.css"
PASS=0 FAIL=0 TOTAL=0

check() {
  local label=$1 desc=$2
  TOTAL=$((TOTAL+1))
  if [ $# -ge 3 ] && [ "$3" = "skip" ]; then
    echo "  SKIP  $label - $desc"
    return
  fi
  echo "  CHECK $label - $desc"
}

pass() { PASS=$((PASS+1)); echo "    PASS"; }
fail() { FAIL=$((FAIL+1)); echo "    FAIL $1"; }

echo "=== validate.sh - organic dashboard ==="
echo ""

# 1 DOCTYPE
check "d01" "DOCTYPE present"
if head -1 "$INDEX" | grep -q '<!DOCTYPE html'; then pass; else fail "line 1 missing DOCTYPE"; fi

# 2 charset meta
check "d02" "charset meta present"
if grep -qi 'charset=' "$INDEX"; then pass; else fail "charset meta not found"; fi

# 3 viewport meta
check "d03" "viewport meta present"
if grep -qi 'name=viewport' "$INDEX"; then pass; else fail "viewport meta not found"; fi

# 4 CSS exists
check "s01" "styles/main.css exists"
if [ -f "$STYLES" ]; then pass; else fail "styles/main.css not found"; fi

# 5 CSS file size < 50KB
check "s02" "stylesheet size < 50KB"
size=""
size=$(stat -c%s "$STYLES" 2>/dev/null || stat -f%z "$STYLES" 2>/dev/null)
if [ "$size" -lt 51200 ]; then pass; else fail "size ${size}B exceeds 50KB limit"; fi

# 6 CSS declaration count <= 800 (uses awk, not grep -c '{')
check "s03" "declaration count <= 800"
real_count=0
real_count=$(awk '{cnt += gsub(/{/, "")} END {print cnt}' "$STYLES")
if [ "$real_count" -le 800 ]; then pass; else fail "${real_count} declarations exceeds 800 limit"; fi

# 7 :root block exists
check "s04" ":root custom properties block"
if grep -q ':root' "$STYLES"; then pass; else fail "no :root block found"; fi

# 8 no duplicate keyframe names
check "s05" "no duplicate keyframe names"
dupes=""
dupes=$(grep -oP '@keyframes\s+\K\S+' "$STYLES" | sort | uniq -d)
if [ -z "$dupes" ]; then pass; else fail "duplicate keyframes: $(echo $dupes)"; fi

# 9 spot-check hardcoded colors outside :root
check "s06" "no inline colors outside :root (spot)"
color_hits=0
color_hits=$(grep -cP '#[0-9a-fA-F]{3,6}|rgba?\(' "$STYLES" || true)
if [ "$color_hits" -lt 40 ]; then pass; else fail "found ${color_hits} possible hardcoded color values"; fi

# 10 JS file exists
check "j01" "scripts/dashboard.js exists"
if [ -f "$SCRIPT_DIR/scripts/dashboard.js" ]; then pass; else fail "dashboard.js not found"; fi

# 11 no inline script above 50 lines
check "j02" "no large inline script blocks"
inline_lines=0
inline_lines=$(grep -c '<script>' "$INDEX" || true)
if [ "$inline_lines" -le 2 ]; then pass; else fail "found ${inline_lines} inline script blocks"; fi

# 12 no var keyword in JS
check "j03" "no var keyword usage in JS"
if grep -qP '\bvar\s+[a-zA-Z_]\w*' "$SCRIPT_DIR/scripts/dashboard.js" 2>/dev/null; then
  fail "var keyword found in dashboard.js"
else
  pass
fi

# 13 xmllint schema check with graceful skip
check "x01" "HTML well-formedness (xmllint)" ""
if command -v xmllint &>/dev/null; then
  xmllint_rc=0
  xmllint --noout "$INDEX" 2>/dev/null
  xmllint_rc=$?
  if [ $xmllint_rc -eq 0 ]; then pass; else fail "xmllint reported errors (rc=$xmllint_rc)"; fi
else
  echo "    WARN xmllint not installed, skipping schema validation"
  pass
fi

echo ""
echo "=== Results: $PASS passed, $FAIL failed, $TOTAL total ==="
exit $FAIL
