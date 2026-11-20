#!/bin/bash
export PATH=/usr/local/bin:/usr/bin:/bin
ulimit -v 8000000
M=${MSOLVE:-msolve}
cd "$(dirname "$0")"
for g in "$@"; do
  echo "=== $g ==="; date
  timeout 600 $M -t 8 -p 64 -f b_$g.ms -o b_$g.out; echo "exit $?"; date
done
