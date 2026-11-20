#!/bin/bash
export PATH=/usr/local/bin:/usr/bin:/bin:$PATH
cd "$(dirname "$0")"
ulimit -v 4000000
"${GAP:-gap}" -q sd16b.g < /dev/null > sd16.out 2>&1
echo exit $? >> sd16.out
