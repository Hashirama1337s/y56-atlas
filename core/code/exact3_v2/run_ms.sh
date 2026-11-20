#!/bin/bash
ulimit -v 8000000
M=${MSOLVE:-msolve}
cd "$(dirname "$0")"
{
$M -h | head -5
echo "=== chart 01: GB (degree) ==="
timeout 600 $M -t 12 -g 2 -f fano_01.ms -o gb_01.out; echo "exit $?"
echo "=== chart 01: param + real roots ==="
timeout 600 $M -t 12 -P 2 -p 64 -f fano_01.ms -o par_01.out; echo "exit $?"
for ij in 02 03 12 13 23; do
 echo "=== chart $ij + p01: expect empty ==="
 timeout 600 $M -t 12 -g 2 -f fano_${ij}_p01.ms -o gb_${ij}_p01.out; echo "exit $?"
 head -c 300 gb_${ij}_p01.out; echo
done
} > msolve_run.log 2>&1
