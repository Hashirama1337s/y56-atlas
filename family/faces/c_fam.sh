#!/bin/bash
export PATH=/usr/local/bin:/usr/bin:/bin
ulimit -v 8000000
cd "$(dirname "$0")"
timeout 600 "${SINGULAR:-Singular}" -q c_fam.sing > c_fam.log 2>&1; echo "exit $?" >> c_fam.log
