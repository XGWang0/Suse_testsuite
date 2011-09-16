#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: cat_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#        LICENSE: unknown
#
#        CREATED: 2005-10-19
#        REVISED: 2005-10-19
#
#    DESCRIPTION: "test use of cat (test all available switches)"
#   REQUIREMENTS: "needs coreutils, diffutils"
#          USAGE: ./cat_lsb.sh
#
#===============================================================================

TMPDIR=`mktemp -d`
TESTDATADIR="/usr/share/qa/qa_test_coreutils/data"
FAILED=0

if cat --help &>/dev/null; then

#test displaying of endlines and tabs
	cat -A "$TESTDATADIR/source" > "$TMPDIR/cat.A" 
	
	if [ $? -eq 0 ]; then
		if ! diff "$TESTDATADIR/cat.A" "$TMPDIR/cat.A" > /dev/null; then
	   		echo "FAILED: Test #1 (cat - showall switch) failed - resulting file different from the reference"
			FAILED=1 
		else
	    		echo "PASSED: Test #1 (cat - showall switch) passed"
		fi
	else
		echo "FAILED: Test #1: cat - showall switch returned non-zero exit code"
		FAILED=1
	fi


#test displaying of endlines
	cat -E "$TESTDATADIR/source" > "$TMPDIR/cat.E" 

	if [ $? -eq 0 ]; then
		if ! diff "$TESTDATADIR/cat.E" "$TMPDIR/cat.E" > /dev/null; then 
	   		echo "FAILED: Test #2 (cat - show end lines switch) failed - resulting file different from the reference"
		else		
	    		echo "PASSED: Test #2 (cat - show end lines switch) passed"
		fi
	else
   		echo "FAILED: Test #2 cat - show end lines switch returned non-zero exit code"
		FAILED=2
	fi

#test displaying tabs
	cat -T "$TESTDATADIR/source" > "$TMPDIR/cat.T" 

	if [ $? -eq 0 ]; then
		if ! diff "$TESTDATADIR/cat.T" "$TMPDIR/cat.T" > /dev/null; then
   			echo "FAILED: Test #3 (cat - show tabs switch) failed - resulting file different from the reference"
			FAILED=3 
		else
	    		echo "PASSED: Test #3 (cat - show tabs switch) passed"
		fi
	else
   		echo "FAILED: Test #3 (cat - show tabs switch) returned non-zero exit code"
		FAILED=3 
	fi
#test numbering non-blank lines 
	cat -b "$TESTDATADIR/source" > "$TMPDIR/cat.b" 

	if [ $? -eq 0 ]; then
		if ! diff "$TESTDATADIR/cat.b" "$TMPDIR/cat.b" > /dev/null; then
	   		echo "FAILED: Test #4 (cat - number non-blank lines) failed - resulting file different from the reference"
			FAILED=4
		else
		    	echo "PASSED: Test #4 (cat - number non-blank lines) passed"
		fi
	else
   		echo "FAILED: Test #4 (cat - number non-blank lines) returned non-zero exit code"
	fi
#test -vE switch 
	cat -e "$TESTDATADIR/source" > "$TMPDIR/cat.e" 

	if [ $? -eq 0 ]; then
		if ! diff "$TESTDATADIR/cat.e" "$TMPDIR/cat.e" > /dev/null; then
   			echo "FAILED: Test #5 (cat -vE switch) failed - resulting file different from the reference"
			FAILED=5
		else
	    		echo "PASSED: Test #5 (cat -vE switch) passed"
		fi
	else
   		echo "FAILED: Test #5 (cat -vE switch) returned non-zero exit code"
	fi
#test numbering all lines  
	cat -n "$TESTDATADIR/source" > "$TMPDIR/cat.n" 

	if [ $? -eq 0 ]; then
		if ! diff "$TESTDATADIR/cat.n" "$TMPDIR/cat.n" > /dev/null; then
   			echo "FAILED: Test #6 (cat - number all lines) failed - resulting file different from the reference"
			FAILED=6
		else
	    		echo "PASSED: Test #6 (cat - number all lines) passed"
		fi
	else
   		echo "FAILED: Test #6 (cat - number all lines) returned non-zero exit code"
		FAILED=6
	fi 
#test squeezing blank lines 
	cat -s "$TESTDATADIR/source" > "$TMPDIR/cat.s" 

	if [ $? -eq 0 ]; then
		if ! diff "$TESTDATADIR/cat.s" "$TMPDIR/cat.s" > /dev/null; then 
   			echo "FAILED: Test #7 (cat - squeeze blank lines) failed - resulting file different from the reference"
			FAILED=7
		else
	    		echo "PASSED: Test #7 (cat - squeeze blank lines) passed"
		fi
	else
   		echo "FAILED: Test #7 (cat - squeeze blank lines) returned non-zero exit code"
		FAILED=7
	fi
#test -vT switch 
	cat -t "$TESTDATADIR/source" > "$TMPDIR/cat.t" 

	if [ $? -eq 0 ]; then
		if ! diff "$TESTDATADIR/cat.t" "$TMPDIR/cat.t" > /dev/null; then 
   			echo "FAILED: Test #8 (cat -vT switch) failed - resulting file different from the reference"
			FAILED=8
		else 	
		    	echo "PASSED: Test #8 (cat -vT switch) passed"
		fi
	else
   		echo "FAILED: Test #8 (cat -vT switch) returned non-zero exit code"
		FAILED=8
	fi
#test displaying non-printing characters  
	cat -v "$TESTDATADIR/source" > "$TMPDIR/cat.v" 

	if [ $? -eq 0 ]; then
		if ! diff "$TESTDATADIR/cat.v" "$TMPDIR/cat.v" > /dev/null; then
   			echo "FAILED: Test #9 (cat - display non-printing characters) failed - resulting file different from the reference"
			FAILED=9
		else
	    		echo "PASSED: Test #9 (cat - display non-printing characters) passed"
		fi
	else
   		echo "FAILED: Test #9 (cat - display non-printing characters) returned non-zero exit code"
		FAILED=9
	fi
#test concatenation of multiple files
	cat "$TESTDATADIR/source" "$TESTDATADIR/source2" "$TESTDATADIR/source3" > $TMPDIR/cat.multiple || FAILED=10
	
	if [ $? -eq 0 ]; then
		if ! diff "$TESTDATADIR/cat.multiple" "$TMPDIR/cat.multiple" >/dev/null; then
	   		echo "FAILED: Test #10 (cat - concatenate multiple files) failed - resulting file different from the reference"
			FAILED=10
		else
		    	echo "PASSED: Test #10 (cat - concatenate multiple files) passed"
		fi 
	else
   		echo "FAILED: Test #10 (cat - concatenate multiple files) returned non-zero exit code"
		FAILED=10
	fi


#cleanup
	rm -rf $TMPDIR

#overall result
	if [ $FAILED -ne 0 ]; then
		echo "FAILED: Overall result of cat_lsb.sh is failed (last failed test was $FAILED)"
		exit 1
	else 
		echo "PASSED: Overall result of cat_lsb.sh is passed"
		exit 0
	fi

else

	echo "FAILED: ERROR: cat cannot be called"
	exit 1
fi

