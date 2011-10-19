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
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: qa_bzip2_bigfilerun.sh
#        VERSION: 0.1
#         AUTHOR: Frank Seidel <fseidel@suse.de>
#       REVIEWER: 
#        LICENSE: unknown
#
#        CREATED: 2005-10-06
#        REVISED: 2005-10-06
#
#    DESCRIPTION: "simple use of bzip2 on a somewhat bigger amount of data"
#   REQUIREMENTS: "needs bzip2"
#          USAGE: ./qa_bzip2_bigfilerun.sh
#
#===============================================================================
 
#<Declarations>
TEST_MBYTES="10"; #<= CHANGE THIS IF YOU WANT TO TEST EVEN BIGGER SIZES

TESTBASEDIR="/usr/share/qa/qa_test_bzip2";
TESTDATADIR="/usr/share/qa/qa_test_bzip2/data";
FAILED="0";
#</Declarations>


#<main>

#first check if bzip2 can be run at all
if bzip2 -h &>/dev/null 
then

	#1. Test: compress datastream of defined size
	echo "Starting compression of $TEST_MBYTES MBytes .."
	( dd if=/dev/urandom bs=1024 count=${TEST_MBYTES}k | bzip2 -z >/dev/null ) || FAILED="1"

	
	#OVERALL-RESULT
	if [ $FAILED -ne 0 ]
	then
		echo "FAILED: qa_bzip2_bigfilerun.sh failed" >&2
		exit 1;
	else
		echo "PASSED: qa_bzip2_bigfilerun.sh passed :)"
		exit 0;
	fi


else
	echo "FAILED: ERROR: bzip2 could not be called." >&2 ;
	exit 1;
fi


#</main>

