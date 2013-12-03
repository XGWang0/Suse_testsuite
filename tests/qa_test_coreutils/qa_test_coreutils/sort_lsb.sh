#!/bin/bash
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
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
#           FILE: sort_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#
#        CREATED: 2005-11-04
#        REVISED: 2005-11-04
#
#    DESCRIPTION: "test use of sort (test some sorting options)"
#   REQUIREMENTS: "needs coreutils, diffutils, mktemp"
#          USAGE: ./sort_lsb.sh
#
#===============================================================================

TMPDIR=`mktemp -d`
TESTDATADIR=/usr/share/qa/qa_test_coreutils/data
FAILED=0
. /usr/share/qa/qa_test_coreutils/detect.sh
export LC_ALL=C	

if sort --help &>/dev/null; then

	N=0
	for i in ignore-leading-blanks dictionary-order ignore-case general-numeric-sort ignore-nonprinting numeric-sort reverse; do
		N=`expr $N + 1`

               
                if [ $i = "general-numeric-sort" ];then
                        origin_file=$TESTDATADIR/origin.general-numeric-sort
                else
                        origin_file=$TESTDATADIR/origin
                fi 
                expect_file=$TESTDATADIR/sort_$i.chk
                
                
		cat $origin_file | sort --$i > $TMPDIR/$i

		if [ $? -eq 0 ]; then 
			if ! diff $TMPDIR/$i $expect_file >/dev/null; then
				echo "FAILED: Test #$N sorted file (sort --$i) is different from the reference "
				FAILED=$N
			fi
				
		else
			FAILED=$N
			echo "FAILED: Test #$N sort --$i returned non-zero exit code"
		fi
		
		
		if [ $FAILED -ne $N ]; then
			echo "PASSED: Test #$N (sort - $i ordering option) passed"
		fi
	done
	
	#cleanup
		rm -rf $TMPDIR
	
	#overall result
		if [ $FAILED -ne 0 ]; then
			echo "FAILED: Overall result of sort_lsb.sh is failed (last failed test was $FAILED)"
			exit 1
		else 
			echo "PASSED: Overall result of sort_lsb.sh is passed"
			exit 0
		fi

else 
	echo "FAILED: ERROR: sort cannot be called"
	exit 1
fi
	
	



