#!/bin/bash
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************

#===============================================================================
#
#           FILE: touch_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
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


