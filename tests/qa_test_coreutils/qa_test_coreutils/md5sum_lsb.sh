#!/bin/bash
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE. All Rights Reserved.
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
#           FILE: md5sum_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#
#        CREATED: 2005-11-07
#        REVISED: 2005-11-07
#
#    DESCRIPTION: "test use of md5sum (calculate md5sum of different types of files)"
#   REQUIREMENTS: "needs coreutils, gawk"
#          USAGE: ./md5sum_lsb.sh
#
#===============================================================================


TESTDATADIR=/usr/share/qa/qa_test_coreutils/data/md5sum
FAILED=0

if md5sum --help &>/dev/null; then

	N=0
	for i in $TESTDATADIR/*; do
		N=`expr $N + 1`
		FILETYPE=`file $i | gawk -F ":" '{print $2}' | gawk -F "," '{print $1}'`
		TOTEST=`md5sum $i`
		
		if [ $? -eq 0 ]; then
			FIR=$(echo $TOTEST | gawk '{print $1}')
			SEC=$(basename $i)
			if [ $FIR != $SEC ] ; then
				echo "FAILED: md5sum of testing $FILETYPE is different from the reference."
				FAILED=$N
			fi
		else
			FAILED=$N
			echo "FAILED: md5sum on $FILETYPE returned non-zero exit code"
		fi

		if [ $FAILED -ne $N ] ; then
			echo "PASSED: Test #$N (md5sum - compute md5 checksum of $FILETYPE) passed"
		fi 

	done
	
#overall result
	if [ $FAILED -ne 0 ]; then
		echo "FAILED: Overall result of md5sum_lsb.sh is failed (last failed test was $FAILED)"
		exit 1
	else 
		echo "PASSED: Overall result of md5sum_lsb.sh is passed"
		exit 0
	fi

else
	echo "FAILED: ERROR: md5sum cannot be called"
	exit 1
fi






