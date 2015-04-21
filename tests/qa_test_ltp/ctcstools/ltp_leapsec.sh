#!/bin/bash
#
# Runs LTP testcase while system inserts leap second
#
# The $1 select action to be done, either add or rem
# LTP Testcase to run is stored in $2
#

# LTP needs these
export LTPROOT="/opt/ltp/";
export TMPDIR="/tmp"
export PATH="${PATH}:${LTPROOT}/testcases/bin/"

# Test runtime in seconds
RUNTIME=10

adjtimex -S0
# Kernel has to reset state automat in second_owerflow() function
sleep 1

SAVED_TIME=$(date)
date -s "23:59:55 UTC"

case "$1" in
	add) adjtimex -S16;;
	rem) adjtimex -S32;;
	*) echo "wrong operation %1"; exit 1;;
esac

$2 -I $RUNTIME 2>&1 |tail -n 10000
rc="${PIPESTATUS[0]}"

date -s "$SAVED_TIME"
date -s "+ $RUNTIME seconds"

# Map exitcode to CTCS2
if [ $rc -eq 0 ]; then
	echo "INFO: Test PASSED"
	exit 0
fi

if [ "$(( $rc & 1 ))" -eq 1 ]; then
	echo "INFO: Test FAILED"
	exit 1
fi

if [ "$(( $rc & 2 ))" -eq 2 ]; then
	echo "INFO: Test INTERNAL ERROR"
	exit 11
fi

if [ "$(( $rc & 32 ))" -eq 32 ]; then
	echo "INFO: Test SKIPPED"
	exit 22
fi

# Test was killed, signaled etc..
echo "INFO: Test returned $rc"
exit $rc
