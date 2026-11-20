#!/bin/bash
ulimit -v 8000000
M=${MSOLVE:-msolve}
cd "$(dirname "$0")"
timeout 600 $M -t 12 -p 128 -f fano_01.ms -o real_01.out > msolve_real.log 2>&1; echo "exit $?" >> msolve_real.log
