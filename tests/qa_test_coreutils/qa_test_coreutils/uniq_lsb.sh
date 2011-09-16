#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: uniq_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#        LICENSE: unknown
#
#        CREATED: 2005-11-07
#        REVISED: 2005-11-07
#
#    DESCRIPTION: "test use of uniq (test some switches)"
#   REQUIREMENTS: "needs coreutils, diffutils, mktemp"
#          USAGE: ./uniq_lsb.sh
#
#===============================================================================


TESTDATADIR="/usr/share/qa/qa_test_coreutils/data"
TMPDIR=`mktemp -d`
FAILED=0

if uniq --help &>/dev/null; then

#test base functionality
	uniq "$TESTDATADIR/uniq-test.data" > "$TMPDIR/uniq.res" 

	if [ $? -eq 0 ]; then 
		if ! diff "$TMPDIR/uniq.res" "$TESTDATADIR/uniq.res" > /dev/null; then
			FAILED=1
			echo "FAILED: Test #1: uniq - basic functionality - output file is different from the reference "
		else 
	    		echo "PASSED: Test #1 (uniq - basic functionality) passed"
		fi
	else
   		echo "FAILED: Test #1 (uniq - basic functionality) returned non-zero exit code"
		FAILED=1
	fi
#test prefixing lines with numbers
	uniq -c "$TESTDATADIR/uniq-test.data" > "$TMPDIR/uniq-c.res" 

	if [ $? -eq 0 ]; then 
		if ! diff "$TMPDIR/uniq-c.res" "$TESTDATADIR/uniq-c.res" > /dev/null; then
			FAILED=2
			echo "FAILED: Test #2: uniq -c output file is different from the reference "
		else 
	    		echo "PASSED: Test #2 (uniq - prefix lines with numbers) passed"
		fi
	else
   		echo "FAILED: Test #2 (uniq -c) returned non-zero exit code"
		FAILED=2
	fi

#test -D switch (have no clue what is this supposed to do)
	uniq -D "$TESTDATADIR/uniq-test.data" > "$TMPDIR/uniq-D.res" 

	if [ $? -eq 0 ]; then 
		if ! diff "$TMPDIR/uniq-D.res" "$TESTDATADIR/uniq-D.res" > /dev/null; then 
			FAILED=3
   			echo "FAILED: Test #3 (uniq -D output file is different from the reference" 
		else 
	    		echo "PASSED: Test #3 (uniq -D switch) passed"
		fi
	else
   		echo "FAILED: Test #3 (uniq -D) returned non-zero exit code"
		FAILED=3
	fi

#test printing unique lines only
	uniq -u "$TESTDATADIR/uniq-test.data" > "$TMPDIR/uniq-u.res"

	if [ $? -eq 0 ]; then 
		if ! diff "$TMPDIR/uniq-u.res" "$TESTDATADIR/uniq-u.res" > /dev/null; then
			FAILED=4
	   		echo "FAILED: Test #4 (uniq -u output file is different from the reference"
		else
	    		echo "PASSED: Test #4 (uniq - print unique lines only) passed"
		fi
	else
   		echo "FAILED: Test #4 (uniq -u) returned non-zero exit code"
		FAILED=4
	fi
#cleanup
	rm -rf $TMPDIR

#overall result
	if [ $FAILED -ne 0 ]; then
		echo "FAILED: Overall result of uniq_lsb.sh is failed (last failed test was $FAILED)"
		exit 1
	else 
		echo "PASSED: Overall result of uniq_lsb.sh is passed"
		exit 0
	fi

else    
	echo "FAILED: ERROR: uniq cannot be called"
	exit 1
fi


