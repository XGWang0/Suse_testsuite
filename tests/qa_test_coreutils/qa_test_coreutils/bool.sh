#!/bin/bash
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
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
#


#===============================================================================
#
#           FILE: bool.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#
#        CREATED: 2005-11-09
#        REVISED: 2005-11-09
#
#    DESCRIPTION: "test simple use of bool"
#   REQUIREMENTS: "needs coreutils"
#          USAGE: ./bool.sh
#
#===============================================================================

FAILED=0

/bin/true 
RESULT1=$?

if [ $RESULT1 -eq 0 ]; then
    echo "PASSED: Test #1 (bool - true) passed"
else
    echo "FAILED: Test #1 (bool - true) failed"
    FAILED=1
fi


/bin/false 
RESULT2=$?

if [ $RESULT2 -eq 1 ]; then
    echo "PASSED: Test #2 (bool - false) passed"
else
    echo "FAILED: Test #2 (bool - false) failed"
    FAILED=2
fi

#overall result
if [ $FAILED -ne 0 ]; then
	echo "FAILED: Overall result of bool.sh is failed (last failed test was $FAILED)"
	exit 1
else 
	echo "PASSED: Overall result of bool.sh is passed"
	exit 0
fi






