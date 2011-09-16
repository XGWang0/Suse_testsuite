#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: sort_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#        LICENSE: unknown
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

export LC_ALL=C	

if sort --help &>/dev/null; then

	N=0
	for i in ignore-leading-blanks dictionary-order ignore-case general-numeric-sort ignore-nonprinting numeric-sort reverse; do
		N=`expr $N + 1`

		cat $TESTDATADIR/origin | sort --$i > $TMPDIR/$i
		
		if [ $? -eq 0 ]; then 
			if ! diff $TMPDIR/$i $TESTDATADIR/sort_$i.chk >/dev/null; then
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
	
	
