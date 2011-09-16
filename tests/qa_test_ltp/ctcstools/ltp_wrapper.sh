#!/bin/bash

OPENPOSIX_MODE=0
LTP_MODE=0

if [ -z "$LTPROOT" ]; then
	if [ -d "/usr/lib64/ltp" ]; then
		LTPROOT="/usr/lib64/ltp";
	elif [ -d "/usr/lib/ltp" ]; then
		LTPROOT="/usr/lib/ltp";
	else
		echo "$0: couldn't find LTP installation!";
		exit 1;
	fi
fi

export LTPROOT;
export PATH="${PATH}:${LTPROOT}/testcases/bin"

if [ -z "$1" ]; then
	echo "usage: $0 <command file>";
	exit 1;
fi

export TMP=`mktemp -d /tmp/ltp-XXXXXXXXXX`
cd $TMP

# Keep the order! First check for openposix!
if [ `basename $0` == "openposix_wrapper.sh" ]; then
  # openposix testsuite has several return values:
  #
  # PTS_PASS        0
  # PTS_FAIL        1
  # PTS_UNRESOLVED  2 X (mapped anyway to internal error)
  # PTS_UNSUPPORTED 4
  # PTS_UNTESTED    5 X
  #
  # Those marked with X get mapped to CTCS2 internal error
  #
  # Documented in ./testcases/open_posix_testsuit/Documentation/HOWTO_ResultCodes

  OPENPOSIX_MODE=1
elif [ `basename $0` == "ltp_wrapper.sh" ]; then
  # native ltp testsuite has serveral return values (ltp manpage: tst_res(3))
  # TPASS 0   The test case produced expected results.
  # TFAIL 1   The test case produced unexpected results.
  # TBROK 2 X A resource needed to execute the test case was not available  (e.g.  a  temporary  file  could  not  be
  #           opened).
  # TCONF 4   The  test case was not appropriate for the current hardware or software configuration (e.g. MLS was not
  #           enabled).
  # TRETR 8   The test case was no longer valid and has been "retired."
  # TWARN 16X The testing procedure caused undesirable side effects that did not affect test results (e.g.  a  tempo‐
  #           rary file could not be removed after all test results were recorded).
  # TINFO 32  An  informative  message about the execution of the test that does not correspond to a test case result
  #           and does not indicate a problem.
  #
  # NOTE: TPASS, TRETR, TINFO, and TCONF do not have an effect on the test program exit status
  LTP_MODE=1
fi;

#eval $@
eval pan -n $$ -a $$ -e -S -L -f $@ 
rc=$?
 
if [ $rc -eq 0 ]; then
  echo "INFO: pan reported all tests PASS"
  VALUE=0
# LTP_MODE map unsuitable/unsupported tests to PASS. Check if _only_ TCONF is set!
elif [ $LTP_MODE -eq 1 ] && [[ "$rc" -eq 4 ]]; then
  echo "INFO: pan reported this test is unsuitable/unsupported (LTP_MODE)"
  VALUE=0
# LTP_MODE uses bit fields - TFAIL is 0x1
elif [ $LTP_MODE -eq 1 ]  && [ "$(( $rc & 1 ))" -eq 0 ] ; then
  echo "INFO: pan reported this test had INTERNAL ERRORS (LTP_MODE)"
  VALUE=2
# OPENPOSIX_MODE map internal errors
elif [ $OPENPOSIX_MODE -eq 1 ] && [[ "$rc" -eq 5 || "$rc" -eq "2" ]]; then
  echo "INFO: pan reported this test had INTERNAL ERRORS (OPENPOSIX_MODE)"
  VALUE=2
# OPENPOSIX_MODE map unsuitable/unsupported tests to PASS
elif [ $OPENPOSIX_MODE -eq 1 ] && [[ "$rc" -eq 4 ]]; then
  echo "INFO: pan reported this test is unsuitable/unsupported (OPENPOSIX_MODE)"
  VALUE=0
else
  echo "INFO: pan reported some tests FAIL"
  VALUE=1
fi

rm -rf $TMP

exit $VALUE
