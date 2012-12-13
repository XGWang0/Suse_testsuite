#!/bin/sh
#
# openposix testsuite has several return values:
#
# PTS_PASS        0
# PTS_FAIL        1
# PTS_UNRESOLVED  2 (some error has hapend while setting up testcase)
# PTS_UNSUPPORTED 4 (configuration not appropriate for testing)
# PTS_UNTESTED    5 (test not written at all or other internal error)
#
# Documented in ./testcases/open_posix_testsuit/Documentation/HOWTO_ResultCodes

LTPROOT=/opt/ltp/

echo "INFO: Exectuting '$@'"

eval "$@"
rc=$?

case "$rc" in
	"0") echo "INFO: Test PASSED"; exit 0;;
	"1") echo "INFO: Test FAILED"; exit 1;;
	"2") echo "INFO: Test UNRESOLVED"; exit 11;;
	"4") echo "INFO: Test UNSUPPORTED"; exit 22;;
	"5") echo "INFO: Test UNTESTED"; exit 11;;
	*) echo "INFO: Test returned $rc"; exit $rc;;
esac
