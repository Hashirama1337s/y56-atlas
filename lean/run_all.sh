#!/bin/sh
# Re-check every Y56 Lean file, one at a time.
#   Positive files must compile with no error; for each, `#print axioms` is run on every theorem.
#   Negative controls (*_neg.lean) must FAIL; their error text is written to <name>.actual-error.txt
#   (compare with the shipped <name>.expected-error.txt).
#   A file is also rejected if it contains sorry, admit, an axiom declaration or native_decide.
#
# Setup once (from this folder):  lake exe cache get      (downloads the prebuilt Mathlib v4.36.0-rc2)
# Then:                           sh run_all.sh           (about 7 minutes; peak memory about 10 GB)
# To use another project that already has this Mathlib built, set LEAN_PROJECT to its folder.
HERE=$(cd "$(dirname "$0")" && pwd)
PROJ=${LEAN_PROJECT:-$HERE}
LOG="$HERE/run_all.log"
: > "$LOG"
fail=0
check_one() {  # $1 = file stem, $2 = pos|neg
  f="$HERE/$1.lean"
  if grep -nE '(^|[^A-Za-z_])(sorry|admit|native_decide)([^A-Za-z_]|$)|^[[:space:]]*axiom[[:space:]]' "$f" > /dev/null; then
    echo "REJECT $1: forbidden keyword" >> "$LOG"; fail=1; return
  fi
  if [ "$2" = pos ]; then
    tmp="$HERE/.tmp_axioms_$1.lean"
    cp "$f" "$tmp"
    grep -oE '^(theorem|lemma) [^ :({]+' "$f" | awk '{print "#print axioms Y56." $2}' >> "$tmp"
    start=$(date +%s)
    ( cd "$PROJ" && lake env lean "$tmp" ) > "$HERE/.tmp_out_$1.txt" 2>&1
    rc=$?
    secs=$(( $(date +%s) - start ))
    if [ $rc -eq 0 ] && ! grep -q "error" "$HERE/.tmp_out_$1.txt"; then
      echo "=== POS $1: PASS ($secs s)" >> "$LOG"
    else
      echo "=== POS $1: FAIL ($secs s)" >> "$LOG"; fail=1
    fi
    grep -E "depends on axioms|does not depend on any axioms|error" "$HERE/.tmp_out_$1.txt" >> "$LOG"
    rm -f "$tmp" "$HERE/.tmp_out_$1.txt"
  else
    ( cd "$PROJ" && lake env lean "$f" ) > "$HERE/.tmp_neg_$1.txt" 2>&1
    rc=$?
    sed "s#$HERE/##" "$HERE/.tmp_neg_$1.txt" > "$HERE/$1.actual-error.txt"; rm -f "$HERE/.tmp_neg_$1.txt"
    n=$(grep -c "error" "$HERE/$1.actual-error.txt")
    if [ $rc -ne 0 ] && [ "$n" -gt 0 ]; then
      echo "=== NEG $1: rejected by Lean as expected ($n error lines)" >> "$LOG"
    else
      echo "=== NEG $1: NOT rejected (control failed)" >> "$LOG"; fail=1
    fi
  fi
}
POS=${ONLY_POS-"Y56_L1 Y56_L7 Y56_Pencil Y56_L2 Y56_L3 Y56_L6 Y56_L5a Y56_L5b Y56_L5c Y56_L8"}
NEG=${ONLY_NEG-"Y56_L1_neg Y56_L7_neg Y56_Pencil_neg Y56_L2_neg Y56_L3_neg Y56_L6_neg Y56_L5c_neg Y56_L8_neg"}
for f in $POS; do check_one $f pos; done
for f in $NEG; do check_one $f neg; done
if [ $fail -eq 0 ]; then echo "=== ALL OK" >> "$LOG"; else echo "=== SOME CHECKS FAILED" >> "$LOG"; fi
cat "$LOG"
exit $fail
