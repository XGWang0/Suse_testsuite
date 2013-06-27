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
#           FILE: csplit_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#
#        CREATED: 2005-10-24
#        REVISED: 2005-10-24
#
#    DESCRIPTION: "test use of csplit (test all available switches)"
#   REQUIREMENTS: "needs coreutils, diffutils, mktemp"
#          USAGE: ./csplit_lsb.sh
#
#===============================================================================

TESTDATADIR="/usr/share/qa/qa_test_coreutils/data"
TMPDIR=`mktemp -d`
FAILED=0

if csplit --help &>/dev/null; then

#test suffix format
	mkdir $TMPDIR/b
	cd $TMPDIR/b && csplit -b yadda%dyadda $TESTDATADIR/splitme 10 > /dev/null 

	if [ $? -eq 0 ]; then
		if ! diff "$TMPDIR/b/" "$TESTDATADIR/INTEGER/b/" >/dev/null; then 
			echo "FAILED: Test #1: splitted file (csplit - change suffix format) is different from the reference" 
			FAILED=1
		fi
	else 
		echo "FAILED: Test #1: csplit -b returned non-zero exit code"
		FAILED=1
	fi
	
	if [ $FAILED -ne 1 ]; then 
	    	echo "PASSED: Test #1 (csplit - change suffix format) passed"
	fi
#test prefix format
	mkdir $TMPDIR/f
	cd $TMPDIR/f && csplit -f yaddayadda $TESTDATADIR/splitme 10 > /dev/null

	if [ $? -eq 0 ]; then
		if ! diff "$TMPDIR/f/" "$TESTDATADIR/INTEGER/f/" >/dev/null; then 
			echo "FAILED: Test #2: splitted file (csplit - change prefix format) is different from the reference" 
			FAILED=2
		fi
	else 
		echo "FAILED: Test #2: csplit -f returned non-zero exit code"
		FAILED=2
	fi

	if [ $FAILED -ne 2 ]; then 
	    	echo "PASSED: Test #2 (csplit - change prefix format) passed"
	fi
#test no.of digits switch
	mkdir $TMPDIR/n
	cd $TMPDIR/n && csplit -n 4 $TESTDATADIR/splitme 10 > /dev/null

	if [ $? -eq 0 ]; then
		if ! diff "$TMPDIR/n/" "$TESTDATADIR/INTEGER/n/" >/dev/null; then
			echo "FAILED: Test #3: splitted file (csplit - change no of digits) is different from the reference" 
			FAILED=3
		fi
	else 
		echo "FAILED: Test #3: csplit -n returned non-zero exit code"
		FAILED=3
	fi
	
	if [ $FAILED -ne 3 ]; then 
	    	echo "PASSED: Test #3 (csplit - change no of digits) passed"
	fi

#test regexp matching with offset
	mkdir $TMPDIR/regexp_offset
	cd $TMPDIR/regexp_offset && csplit $TESTDATADIR/splitme "/yes.it.is/+5" > /dev/null

	if [ $? -eq 0 ]; then
		if ! diff "$TMPDIR/regexp_offset/" "$TESTDATADIR/REGEXP/regexp_offset/" >/dev/null; then
			echo "FAILED: Test #4: splitted file (csplit - basic regexp matching with offset) is different from the reference" 
			FAILED=4
		fi
	else 
		echo "FAILED: Test #4: csplit - basic regexp matching with offset returned non-zero exit code"
		FAILED=4
	fi

	if [ $FAILED -ne 4 ]; then 
	    	echo "PASSED: Test #4 (csplit - basic regexp matching with offset) passed"
	fi

#test basic regexp matching
	mkdir $TMPDIR/regexp_upto
	cd $TMPDIR/regexp_upto && csplit $TESTDATADIR/splitme "/yes.it.is/" > /dev/null

	if [ $? -eq 0 ]; then
		if ! diff "$TMPDIR/regexp_upto/" "$TESTDATADIR/REGEXP/regexp_upto/" >/dev/null; then
			echo "FAILED: Test #5: splitted file (csplit - basic regexp matching) is different from the reference"  
			FAILED=5
		fi
	else 
		echo "FAILED: Test #5: csplit - basic regexp matching returned non-zero exit code"
		FAILED=5
	fi
	
	if [ $FAILED -ne 5 ]; then 
	    	echo "PASSED: Test #5 (csplit - basic regexp matching) passed"
	fi

#test regexp matching - skipto
	mkdir $TMPDIR/regexp_skipto
	cd $TMPDIR/regexp_skipto && csplit $TESTDATADIR/splitme "%yes.it.is%" > /dev/null

	if [ $? -eq 0 ]; then
		if ! diff "$TMPDIR/regexp_skipto/" "$TESTDATADIR/REGEXP/regexp_skipto/" >/dev/null; then
			echo "FAILED: Test #6: splitted file (csplit - skip-to regexp matching) is different from the reference"  
			FAILED=6
		fi
	else 
		echo "FAILED: Test #6: csplit - skip-to regexp matching returned non-zero exit code"
		FAILED=6
	fi
	
	if [ $FAILED -ne 6 ]; then 
	    	echo "PASSED: Test #6 (csplit - skip-to regexp matching) passed"
	fi

#test silent switch
	mkdir $TMPDIR/s
	cd $TMPDIR/s && TESTSTRING=`csplit -s $TESTDATADIR/splitme 10` 

	if [ $? -eq 0 ]; then 
		if [ ! -z "$TESTSTRING" ]; then
			echo "FAILED: Test #7: Output of csplit --silent is not empty"
			FAILED=7
		fi
	else
		echo "FAILED: Test #7: csplit -s returned non-zero exit code"
		FAILED=6
	fi
	if [ $FAILED -ne 7 ]; then 
	    	echo "PASSED: Test #7 (csplit - silent switch) passed"
	fi


#cleanup
	rm -rf $TMPDIR

#overall result
	if [ $FAILED -ne 0 ]; then
		echo "FAILED: Overall result of csplit_lsb.sh is failed (last failed test was $FAILED)"
		exit 1
	else 
		echo "PASSED: Overall result of csplit_lsb.sh is passed"
		exit 0
	fi

else 

	echo "FAILED: ERROR: csplit cannot be called"
	exit 1
fi





