#!/bin/sh

#
# There are runtest files that utilize either LTPROOT or TMPDIR which I
# consider wrong, but we must stick with this until this is fixed.
#
export LTPROOT="/opt/ltp/";
export TMPDIR="/tmp"

#
# The testcases bin directory must be in PATH so that
# testcases could executed binaries from there
#
export PATH="${PATH}:${LTPROOT}/testcases/bin/"

#
# native ltp testsuite has serveral return values (ltp manpage: tst_res(3))
#
# TPASS 0   The test case produced expected results.
# TFAIL 1   The test case produced unexpected results.
# TBROK 2   A resource needed to execute the test case was not available  (e.g.  a  temporary  file  could  not  be
#           opened).
#

eval "$@"
rc=$?

if [ $rc -eq 0 ]; then
	echo "INFO: Test PASSED"
	exit 0
fi
  
if [ "$(( $rc & 1 ))" -eq 1 ]; then
	echo "INFO: Test FAILED"
	exit 1
fi

if [ "$(( $rc & 2))" -eq 2 ]; then
	echo "INFO: Test INTERNAL ERROR"
	exit 11
fi

# Test was killed, signaled etc..
echo "INFO: Test returned $rc"
exit $rc
