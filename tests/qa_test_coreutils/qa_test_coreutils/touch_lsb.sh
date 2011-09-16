#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: touch_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#        LICENSE: unknown
#
#        CREATED: 2005-11-02
#        REVISED: 2005-11-02
#
#    DESCRIPTION: "test use of touch (test all available switches)"
#   REQUIREMENTS: "needs coreutils, mktemp "
#          USAGE: ./touch_lsb.sh
#
#===============================================================================


TMPDIR=`mktemp -d`
FAILED=0

if touch --help &>/dev/null; then

#test specifying timestamp
	touch -t 196702170202 "$TMPDIR/touch1.test"
	
	if [ $? -eq 0 ]; then
		ls -l --time-style=long-iso "$TMPDIR/touch1.test" | grep " 1967-02-17 02:02 " > /dev/null || FAILED=1
	
		if [ $FAILED -eq 1 ]; then 
   			echo "FAILED: Test #1 (touch - modified timestamp) failed - search string not found in the result"
		else
	    		echo "PASSED: Test #1 (touch - modified timestamp) passed"
		fi
	else 
		echo "FAILED: Test #1: touch - modified timestamp returned non-zero exit code"
		FAILED=1
	fi
#test using timestamp of reference file
	touch -d  19670217 "$TMPDIR/special.date" 

	if [ $? -eq 0 ]; then 
		touch -r "$TMPDIR/special.date" "$TMPDIR/touch2.test"
	
		if [ $? -eq 0 ]; then 
			ls -l --time-style=long-iso "$TMPDIR/touch2.test" | grep " 1967-02-17 " >/dev/null || FAILED=2
 
			if [ $FAILED -eq 2 ]; then 
   				echo "FAILED: Test #2 (touch - timestamp of reference file) failed - search string not found in the result"
			else
			    	echo "PASSED: Test #2 (touch - timestamp of reference file) passed"
			fi
		else
			echo "FAILED: touch -r returned non-zero exit code"
			FAILED=2
		fi		
	else 
		echo "FAILED: touch -d returned non-zero exit code"
		FAILED=2
	fi 

#overall result
	if [ $FAILED -ne 0 ]; then
		echo "FAILED: Overall result of touch_lsb.sh is failed (last failed test was $FAILED)"
		exit 1
	else 
		echo "PASSED: Overall result of touch_lsb.sh is passed"
		exit 0
	fi

else

	echo "FAILED: ERROR: touch cannot be called"
	exit 1
fi

