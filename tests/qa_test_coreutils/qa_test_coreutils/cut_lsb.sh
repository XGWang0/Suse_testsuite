#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: cut_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#        LICENSE: unknown
#
#        CREATED: 2005-10-26
#        REVISED: 2005-10-26
#
#    DESCRIPTION: "test use of cut (test all available switches)"
#   REQUIREMENTS: "needs coreutils"
#          USAGE: ./cut_lsb.sh
#
#===============================================================================


TESTDATAFILE="/usr/share/qa/qa_test_coreutils/data/test"
TESTDATAFILE_DELIM="/usr/share/qa/qa_test_coreutils/data/test_delim"
FAILED=0

if cut --help &>/dev/null; then

#test selecting block of bytes,
	RESULT1=`cut -b 1-8 "$TESTDATAFILE"`

	if [ $? -eq 0 ]; then
		if [ "$RESULT1" = "01234567" ]; then
    			echo "PASSED: Test #1 (cut - selecting block of bytes) passed" 
		else
    			FAILED=1	
	    		echo "FAILED: Test #1 (cut - selecting block of bytes) failed - search string not found in the result" 
		fi
	else
		echo "FAILED: Test #1: cut -b returned non-zero exit code"
		FAILED=1
	fi

#test selecting single bytes
	RESULT2=`cut -b 2,4,6 "$TESTDATAFILE"`

	if [ $? -eq 0 ]; then
		if [ "$RESULT2" = "135" ]; then
 			echo "PASSED: Test #2 (cut - selecting single bytes) passed" 
		else
    			FAILED=2	
    			echo "FAILED: Test #2 (cut - selecting single bytes) failed - search string not found in the result" 
		fi
	else
		echo "FAILED: Test #2: cut -b returned non-zero exit code"
		FAILED=2
	fi

#test selecting bytes up to limit
	RESULT3=`cut -b -5 "$TESTDATAFILE"`

	if [ $? -eq 0 ]; then
		if [ "$RESULT3" = "01234" ]; then
 			echo "PASSED: Test #3 (cut - selecting bytes up to limit) passed" 
		else
    			FAILED=3	
	    		echo "FAILED: Test #3 (cut - selecting bytes up to limit) failed - search string not found in the result" 
		fi
	else
		echo "FAILED: Test #3: cut -b returned non-zero exit code"
		FAILED=3
	fi

#test selecting single byte
	RESULT4=`cut -b 5 "$TESTDATAFILE"`

	if [ $? -eq 0 ]; then
		if [ "$RESULT4" = "4" ]; then
 			echo "PASSED: Test #4 (cut - selecting single byte) passed" 
		else
    			FAILED=4	
    			echo "FAILED: Test #4 (cut - selecting single byte) failed - search string not found in the result" 
		fi
	else
		echo "FAILED: Test #4: cut -b returned non-zero exit code"
		FAILED=4
	fi

#test selecting block of characters,
	RESULT5=`cut -c 1-8 "$TESTDATAFILE"`

	if [ $? -eq 0 ]; then
		if [ "$RESULT5" = "01234567" ]; then
    			echo "PASSED: Test #5 (cut - selecting block of chars) passed" 
		else
    			FAILED=5	
    			echo "FAILED: Test #5 (cut - selecting block of chars) failed" 
		fi
	else 
		echo "FAILED: Test #5: cut -c returned non-zero exit code"
		FAILED=5
	fi
	
#test selecting single characters
	RESULT6=`cut -c 3,6,8 "$TESTDATAFILE"`

	if [ $? -eq 0 ]; then
		if [ "$RESULT6" = "257" ]; then
	    		echo "PASSED: Test #6 (cut - selecting single chars) passed" 
		else
	    		FAILED=6	
	    		echo "FAILED: Test #6 (cut - selecting single chars) failed - search string not found in the result"
		fi
	else
		echo "FAILED: Test #6: cut -c returned non-zero exit code"
		FAILED=6
	fi
#test selecting chars up to limit
	RESULT7=`cut -c -5 "$TESTDATAFILE"`

	if [ $? -eq 0 ]; then
		if [ "$RESULT7" = "01234" ]; then
 			echo "PASSED: Test #7 (cut - selecting chars up to limit) passed" 
		else
	    		FAILED=7	
	   		echo "FAILED: Test #7 (cut - selecting chars up to limit) failed - search string not found in the result" 
		fi
	else
		echo "FAILED: Test #7: cut -c returned non-zero exit code"
		FAILED=7
	fi

#test input delimiter
	RESULT8=`cut -d, -f2-4 $TESTDATAFILE_DELIM`

	if [ $? -eq 0 ]; then
		if [ "$RESULT8" = "1,2,3" ]; then
	 		echo "PASSED: Test #8 (cut - use different input field delimiter) passed" 
		else
	    		FAILED=8	
	   		echo "FAILED: Test #8 (cut - use different input field delimiter) failed - search string not found in the result" 
		fi
	else
		echo "FAILED: Test #8: cut -d, -f returned non-zero exit code" 
		FAILED=8
	fi
	

#test output delimiter
	RESULT9=`cut -d, -f2- --output-delimiter=x $TESTDATAFILE_DELIM`
	
	if [ $? -eq 0 ]; then
		if [ "$RESULT9" = "1x2x3x4x5x6x7x8x9" ]; then
	 		echo "PASSED: Test #9 (cut - use different output field delimiter) passed" 
		else
	    		FAILED=9	
	   		echo "FAILED: Test #9 (cut - use different output field delimiter) failed - search string not found in the result" 
		fi
	else
		echo "FAILED: Test #8: cut -d, -f, --output delimiter returned non-zero exit code" 
		FAILED=9
	fi

#overall result
	if [ $FAILED -ne 0 ]; then
		echo "FAILED: Overall result of cut_lsb.sh is failed (last failed test was $FAILED)"
		exit 1
	else 
		echo "PASSED: Overall result of cut_lsb.sh is passed"
		exit 0
	fi


else
	echo "FAILED: ERROR: cut cannot be called"
	exit 1
fi		
