#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: comm_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#        LICENSE: unknown
#
#        CREATED: 2005-10-21
#        REVISED: 2005-10-21
#
#    DESCRIPTION: "test use of comm (test all available switches)"
#   REQUIREMENTS: "needs coreutils, diffutils, mktemp"
#          USAGE: ./comm_lsb.sh
#
#===============================================================================


TESTDATADIR="/usr/share/qa/qa_test_coreutils/data"
TMPDIR=`mktemp -d`
FAILED=0

if comm --help &>/dev/null; then
	
#basic function
	comm "$TESTDATADIR/hello" "$TESTDATADIR/goodbye" > "$TMPDIR/comm.0"
	diff  "$TMPDIR/comm.0" "$TESTDATADIR/comm.0" > /dev/null || FAILED=1
   
	if [ $FAILED -eq 1 ]; then
	    	echo "FAILED: Test #1 (comm - basic function) failed"
	else
	 	echo "PASSED: Test #1 (comm - basic function) passed"
	fi

#omit first column
	comm -1 "$TESTDATADIR/hello" "$TESTDATADIR/goodbye" > "$TMPDIR/comm.1"
	diff  "$TMPDIR/comm.1" "$TESTDATADIR/comm.1" > /dev/null || FAILED=2
   
	if [ $FAILED -eq 2 ]; then
	    	echo "FAILED: Test #2 (comm - omit first file stuff) failed"
	else
	 	echo "PASSED: Test #2 (comm - omit first file stuff) passed"
	fi

#omit second column
	comm -2 "$TESTDATADIR/hello" "$TESTDATADIR/goodbye" > "$TMPDIR/comm.2"
	diff  "$TMPDIR/comm.2" "$TESTDATADIR/comm.2" > /dev/null || FAILED=3
   
	if [ $FAILED -eq 3 ]; then
	    	echo "FAILED: Test #3 (comm - omit second file stuff) failed"
	else
	 	echo "PASSED: Test #3 (comm - omit second file stuff) passed"
	fi

#omit third column
	comm -3 "$TESTDATADIR/hello" "$TESTDATADIR/goodbye" > "$TMPDIR/comm.3"
	diff  "$TMPDIR/comm.3" "$TESTDATADIR/comm.3" > /dev/null || FAILED=4
   
	if [ $FAILED -eq 4 ]; then
	    	echo "FAILED: Test #4 (comm - omit common stuff) failed"
	else
	 	echo "PASSED: Test #4 (comm - omit common stuff) passed"
	fi

#cleanup
    rm -rf "$TMPDIR"

#overall result
	if [ $FAILED -ne 0 ]; then
		echo "FAILED: Overall result of comm_lsb.sh is failed (last failed test was $FAILED)"
		exit 1
	else 
		echo "PASSED: Overall result of comm_lsb.sh is passed"
		exit 0
	fi

else
	echo "FAILED: ERROR: comm cannot be called"
	exit 1
fi

