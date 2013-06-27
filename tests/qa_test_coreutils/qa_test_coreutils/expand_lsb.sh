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
#           FILE: expand_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#
#        CREATED: 2005-10-26
#        REVISED: 2005-10-26
#
#    DESCRIPTION: "test use of expand (test all available switches)"
#   REQUIREMENTS: "needs coreutils, diffutils, mktemp"
#          USAGE: ./expand_lsb.sh
#
#===============================================================================

TMPDIR=`mktemp -d`
TESTDATADIR="/usr/share/qa/qa_test_coreutils/data"
FAILED=0

if expand --help &>/dev/null; then

#test not converting tabs after non-blanks
	expand -i $TESTDATADIR/file > $TMPDIR/file_i

	if [ $? -eq 0 ]; then
		if ! diff $TESTDATADIR/file_i.ref $TMPDIR/file_i; then
			echo "FAILED: Test #1: output file (expand -i) is different from the reference"	
			FAILED=1
		fi
	else
		echo "FAILED: Test #1: expand -i returned non-zero exit code"
	fi

	if [ $FAILED -ne 1 ]; then 
   		echo "PASSED: Test #1 (expand - do not convert after non-blanks) passed"
	fi
#test standard expand
	expand  $TESTDATADIR/file > $TMPDIR/file_noop

	if [ $? -eq 0 ]; then
		if ! diff $TESTDATADIR/file_noop.ref $TMPDIR/file_noop; then
			echo "FAILED: Test #2: output file (expand - standard output) is different from the reference"	
			FAILED=2
		fi
	else
		echo "FAILED: Test #2: expand returned non-zero exit code"
	fi

	if [ $FAILED -ne 2 ]; then 
   		echo "PASSED: Test #2 (expand - standard output) passed"
	fi

#test comma separated list of of tabs position
	expand -t 1,2,3  $TESTDATADIR/file > $TMPDIR/file_i2
	if [ $? -eq 0 ]; then	
		if ! diff $TESTDATADIR/file_i2.ref $TMPDIR/file_i2; then 
			echo "FAILED: Test #3: output file (expand -t list_of_tabs_positions ) is different from the reference"	
			FAILED=3
		fi
	else
		echo "FAILED: Test #3: expand -t list_of_tabs_positions returned non-zero exit code"
	fi

	if [ $FAILED -ne 3 ]; then 
   		echo "PASSED: Test #3 (expand - list of tabs positions) passed"
	fi

#test using fixed number of spaces	
	expand -t 12  $TESTDATADIR/file > $TMPDIR/file_t
	if [ $? -eq 0 ]; then	
		if ! diff $TESTDATADIR/file_t.ref $TMPDIR/file_t; then 
			echo "FAILED: Test #4: output file (expand -t fixed_tab_position ) is different from the reference"	
			FAILED=4
		fi
	else
		echo "FAILED: Test #4: expand -t fixed_tab_positions returned non-zero exit code"
	fi
			
	if [ $FAILED -ne 4 ]; then 
   		echo "PASSED: Test #4 (expand - fixed number of spaces) passed"
	fi

#cleanup
    rm -rf "$TMPDIR"

#overall result
	if [ $FAILED -ne 0 ]; then
		echo "FAILED: Overall result of expand_lsb.sh is failed (last failed test was $FAILED)"
		exit 1
	else 
		echo "PASSED: Overall result of expand_lsb.sh is passed"
		exit 0
	fi

else
	echo "FAILED: ERROR: expand cannot be called"
	exit 1
fi



