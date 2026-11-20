#!/bin/bash
export PATH=/usr/local/bin:/usr/bin:/bin
ulimit -v 8000000
cd "$(dirname "$0")"
for f in "$@"; do timeout ${TMO:-600} "${SINGULAR:-Singular}" -q $f.sing > $f.log 2>&1; echo "exit $?" >> $f.log; done
