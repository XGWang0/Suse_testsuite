#!/bin/bash

#===============================================================================
#
#           FILE: expr_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#
#        CREATED: 2005-10-26
#        REVISED: 2005-10-26
#
#    DESCRIPTION: "test use of expr (test all available switches)"
#   REQUIREMENTS: "needs coreutils"
#          USAGE: ./expr_lsb.sh
#
#===============================================================================

FAILED=0

if expr --help &>/dev/null; then

	RESULT1=`expr 1 \& 6` 

	if [ $? -ne 3 ]; then 
		if [ "$RESULT1" -ne 1 ]; then
			echo "FAILED: Test #1 (expr - ARG1 & ARG2 part 1) - wrong result "
			FAILED=1
		else
    			echo "PASSED: Test #1 (expr - ARG1 & ARG2 part 1) passed "
		fi
	else
		echo "FAILED: Test #1 (expr - ARG1 & ARG2 part 1) - error calling expr "
		FAILED=1
	fi

	RESULT2=`expr 1 \& 0` 

	if [ $? -ne 3 ]; then  
		if [ "$RESULT2" -ne 0 ]; then
    			echo "FAILED: Test #2 (expr - ARG1 & ARG2 part 2) - wrong result"
			FAILED=2
		else
    			echo "PASSED: Test #2 (expr - ARG1 & ARG2 part 2) passed "
		fi
	else
    		echo "FAILED: Test #2 (expr - ARG1 & ARG2 part 2) - error calling expr "
		FAILED=2
	fi

	RESULT3=`expr 18 \/ 6` 

	if [ $? -ne 3 ]; then 
		if [ "$RESULT3" -ne 3 ]; then
	    		echo "FAILED: Test #3 (expr - ARG1 / ARG2 ) failed - wrong result"
			FAILED=3
		else
    			echo "PASSED: Test #3 (expr - ARG1 / ARG2 ) passed "
		fi
	else
    		echo "FAILED: Test #3 (expr - ARG1 / ARG2 ) failed - error calling expr"
		FAILED=3
	fi

	RESULT4=`expr 0 \= 6` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT4" -ne 0 ]; then
	    		echo "FAILED: Test #4 (expr - ARG1 = ARG2 part 1) failed - wrong result"
			FAILED=4
		else
    			echo "PASSED: Test #4 (expr - ARG1 = ARG2 part 1) passed "
		fi
	else
    		echo "FAILED: Test #4 (expr - ARG1 = ARG2 part 1) failed - error calling expr"
		FAILED=4
	fi

	RESULT5=`expr 1 \= 1` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT5" -ne 1 ]; then
			echo "FAILED: Test #5 (expr - ARG1 = ARG2 part 2) failed - wrong result"
			FAILED=5
		else 
			echo "PASSED: Test #5 (expr - ARG1 = ARG2 part 2) passed "
		fi
	else
    		echo "FAILED: Test #5 (expr - ARG1 = ARG2 part 2) failed - error calling expr"
		FAILED=5
	fi


	RESULT6=`expr \( 11 + 31 \)` 

   	if [ $? -ne 3 ] ; then 
		if [ "$RESULT6" -ne 42 ]; then
   			echo "FAILED: Test #6 (expr - more complex expression) failed - wrong result"
   			FAILED=6
		else
   			echo "PASSED: Test #6 (expr - more complex expression) passed "
  		fi
	else
		echo "FAILED: Test #6 (expr - more complex expression) failed - error calling expr"
		FAILED=6
	fi

	RESULT7=`expr 0 \> 6` 

	if [ $? -ne 3 ]; then 
		if [ "$RESULT7" -ne 0 ]; then
    			echo "FAILED: Test #7 (expr - ARG1 > ARG2 part 1) failed - wrong result"
			FAILED=7
		else
    			echo "PASSED: Test #7 (expr - ARG1 > ARG2 part 1) passed "
		fi
	else
    		echo "FAILED: Test #7 (expr - ARG1 > ARG2 part 1) failed - error calling expr"
		FAILED=7
	fi

	RESULT8=`expr 6 \> 0` 

	if [ $? -ne 3 ]; then 
		if [ "$RESULT8" -ne 1 ]; then
    			echo "FAILED: Test #8 (expr - ARG1 > ARG2 part 2) failed - wrong result"
			FAILED=8
		else
    			echo "PASSED: Test #8 (expr - ARG1 > ARG2 part 2) passed "
		fi
	else
    		echo "FAILED: Test #8 (expr - ARG1 > ARG2 part 2) failed - error calling expr"
		FAILED=8
	fi

	RESULT9=`expr 1 \> 1` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT9" -ne 0 ]; then
    			echo "FAILED: Test #9 (expr - ARG1 > ARG2 part 3) failed - wrong result"
			FAILED=9
		else
    			echo "PASSED: Test #9 (expr - ARG1 > ARG2 part 3) passed "
		fi
	
	else
    		echo "FAILED: Test #9 (expr - ARG1 > ARG2 part 3) failed - error calling expr"
		FAILED=9
	fi

	RESULT10=`expr 0 \>= 6` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT10" -ne 0 ]; then
    			echo "FAILED: Test #10 (expr - ARG1 >= ARG2 part 1) failed - wrong result "
			FAILED=10
		else 
    			echo "PASSED: Test #10 (expr - ARG1 >= ARG2 part 1) passed "
		fi
	else
    		echo "FAILED: Test #10 (expr - ARG1 >= ARG2 part 1) failed - error calling expr"
		FAILED=10
	fi

RESULT11=`expr 1 \>= 1` 

	if [ $? -ne 3 ] ; then 
 		if [ "$RESULT11" -ne 1 ]; then
 			echo "FAILED: Test #11 (expr - ARG1 >= ARG2 part 2) failed - wrong result"
			FAILED=11
		else
 			echo "PASSED: Test #11 (expr - ARG1 >= ARG2 part 2) passed "
		fi
	else
 		echo "FAILED: Test #11 (expr - ARG1 >= ARG2 part 2) failed - error calling expr"
	 	FAILED=11
	fi

	RESULT12=`expr 6 \>= 0` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT12" -ne 1 ]; then
    			echo "FAILED: Test #12 (expr - ARG1 >= ARG2 part 3) failed - wrong result"
			FAILED=12
		else
    			echo "PASSED: Test #12 (expr - ARG1 >= ARG2 part 3) passed "
		fi
	else
    		echo "FAILED: Test #12 (expr - ARG1 >= ARG2 part 3) failed "
		FAILED=12
	fi

	RESULT13=`expr index yaddayadda add` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT13" -ne 2 ]; then
    			echo "FAILED: Test #13 (expr - return index) failed - wrong result"
			FAILED=13
		else
    			echo "PASSED: Test #13 (expr - return index) passed "
		fi
	else
    		echo "FAILED: Test #13 (expr - return index) failed - error calling expr"
		FAILED=13
	fi
	
	RESULT14=`expr length yaddayadda` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT14" -ne 10 ]; then
    			echo "FAILED: Test #14 (expr - return strlen()) failed - wrong result "
			FAILED=14
		else
    			echo "PASSED: Test #14 (expr - return strlen()) passed "
		fi
	
	else
    		echo "FAILED: Test #14 (expr - return strlen()) failed - error calling expr"
		FAILED=14
	fi
	
	RESULT15=`expr 10 \- 6` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT15" -ne 4 ]; then
    			echo "FAILED: Test #15 (expr - ARG1 minus ARG2) failed - wrong result"
			FAILED=15
		else
    			echo "PASSED: Test #15 (expr - ARG1 minus ARG2) passed "
		fi
	else
    		echo "FAILED: Test #15 (expr - ARG1 minus ARG2) failed - error calling expr"
		FAILED=15
	fi

	RESULT16=`expr 3 \* 6` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT16" -ne 18 ]; then
    			echo "FAILED: Test #16 (expr - ARG1 times ARG2) failed - wrong result"
			FAILED=16
		else
    			echo "PASSED: Test #16 (expr - ARG1 times ARG2) passed "
		fi
	else
    		echo "FAILED: Test #16 (expr - ARG1 times ARG2) failed - error calling expr"
		FAILED=16
	fi

	RESULT17=`expr 0 \| 6` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT17" -ne 6 ]; then
    			echo "FAILED: Test #17 (expr - ARG1 | ARG2 part 1) failed - wrong result "
			FAILED=17
		else
    			echo "PASSED: Test #17 (expr - ARG1 | ARG2 part 1) passed "
		fi
	else
    		echo "FAILED: Test #17 (expr - ARG1 | ARG2 part 1) failed - error calling expr"
		FAILED=17
	fi

	RESULT18=`expr 5 \| 6` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT18" -ne 5 ]; then
    			echo "FAILED: Test #18 (expr - ARG1 | ARG2 part 2) failed - wrong result "
			FAILED=18
		else
    			echo "PASSED: Test #18 (expr - ARG1 | ARG2 part 2) passed "
		fi
	else
    		echo "FAILED: Test #18 (expr - ARG1 | ARG2 part 2) failed - error calling expr "
		FAILED=18
	fi


	RESULT19=`expr 4 \+ 6` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT19" -ne 10 ]; then
    			echo "FAILED: Test #19 (expr - ARG1 plus ARG2) failed - wrong result "
			FAILED=19
		else
	    		echo "PASSED: Test #19 (expr - ARG1 plus ARG2) passed "
		fi
	else
    		echo "FAILED: Test #19 (expr - ARG1 plus ARG2) failed - error calling expr "
		FAILED=19
	fi

	RESULT20=`expr yaddayadda : \.\*ad` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT20" -ne 8 ]; then
   			echo "FAILED: Test #20 (expr - match regexp in string) failed - wrong result "
			FAILED=20
		else
    			echo "PASSED: Test #20 (expr - match regexp in string) passed "
		fi
	else
   		echo "FAILED: Test #20 (expr - match regexp in string) failed - error calling expr "
		FAILED=20
	fi

	RESULT21=`expr 20 \% 6` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT21" -ne 2 ]; then
    			echo "FAILED: Test #21 (expr - ARG1 % ARG2) failed - wrong result"
			FAILED=21
		else
    			echo "PASSED: Test #21 (expr - ARG1 % ARG2) passed "
		fi
	else
    		echo "FAILED: Test #21 (expr - ARG1 % ARG2) failed "
		FAILED=21
	fi

	RESULT22=`expr 0 \< 6` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT22" -ne 1 ]; then
    			echo "FAILED: Test #22 (expr - ARG1 < ARG2 part 1) failed - wrong result  "
			FAILED=22
		else
    			echo "PASSED: Test #22 (expr - ARG1 < ARG2 part 1) passed "
		fi
	else
    		echo "FAILED: Test #22 (expr - ARG1 < ARG2 part 1) failed - error calling expr "
		FAILED=22
	fi

	RESULT23=`expr 6 \< 0` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT23" -ne 0 ]; then
    			echo "FAILED: Test #23 (expr - ARG1 < ARG2 part 2) failed - wrong result "
			FAILED=23
    		else		
			echo "PASSED: Test #23 (expr - ARG1 < ARG2 part 2) passed "
		fi
	else
    		echo "FAILED: Test #23 (expr - ARG1 < ARG2 part 2) failed - error calling expr "
		FAILED=23
	fi

	RESULT24=`expr 0 \<= 6` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT24" -ne 1 ]; then
	    		echo "FAILED: Test #24 (expr - ARG1 <= ARG2 part 1) failed - wrong result "
			FAILED=24
		else
    			echo "PASSED: Test #24 (expr - ARG1 <= ARG2 part 1) passed "
		fi
	else
    		echo "FAILED: Test #24 (expr - ARG1 <= ARG2 part 1) failed - error calling expr "
		FAILED=24
	fi

	RESULT25=`expr 1 \<= 1` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT25" -ne 1 ]; then
	    		echo "FAILED: Test #25 (expr - ARG1 <= ARG2 part 2) failed - wrong result "
			FAILED=25
		else
    			echo "PASSED: Test #25 (expr - ARG1 <= ARG2 part 2) passed "
		fi
	else
    		echo "FAILED: Test #25 (expr - ARG1 <= ARG2 part 2) failed - error calling expr "
		FAILED=25
	fi
 
	RESULT26=`expr 6 \<= 0` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT26" -ne 0 ]; then
    			echo "FAILED: Test #26 (expr - ARG1 <= ARG2 part 3) failed - wrong result "
			FAILED=26
		else
    			echo "PASSED: Test #26 (expr - ARG1 <= ARG2 part 3) passed "
		fi
	else
    		echo "FAILED: Test #26 (expr - ARG1 <= ARG2 part 3) failed - error calling expr "
		FAILED=26
	fi
	
	RESULT27=`expr substr yaddayadda 4 3` 

	if [ $? -ne 3 ] ; then 
		if [ "$RESULT27" != "day" ]; then
    			echo "FAILED: Test #27 (expr - return substring) failed - wrong result"
			FAILED=27
		else
	    		echo "PASSED: Test #27 (expr - return substring) passed - error calling expr "
		fi
	else
    		echo "FAILED: Test #27 (expr - return substring) failed "
		FAILED=27
	fi

#overall result
	if [ $FAILED -ne 0 ]; then
		echo "FAILED: Overall result of expr_lsb.sh is failed (last failed test was $FAILED)"
		exit 1
	else 
		echo "PASSED: Overall result of expr_lsb.sh is passed"
		exit 0
	fi
else
	echo "FAILED: ERROR: expr cannot be called"
	exit 1
fi	


