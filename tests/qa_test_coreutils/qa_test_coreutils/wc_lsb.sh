#!/bin/sh
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
#        CREATED: 2005-11-03
#        REVISED: 2005-11-03
#
#    DESCRIPTION: "test use of wc (count lines, words and characters, find longest line)"
#   REQUIREMENTS: "needs coreutils, gawk"
#          USAGE: ./wc.sh
#
#===============================================================================


FAILED=0;
TESTDATAFILE=/usr/share/qa/qa_test_coreutils/data/44_290_1936_65

if wc --help &>/dev/null; then
	
	LINES=$(basename $TESTDATAFILE | gawk -F_ '{print $1}')
	WORDS=$(basename $TESTDATAFILE | gawk -F_ '{print $2}')
	CHARS=$(basename $TESTDATAFILE | gawk -F_ '{print $3}')
	LLINE=$(basename $TESTDATAFILE | gawk -F_ '{print $4}')

	TLINES=$(wc -l $TESTDATAFILE ) 
	
	if [ $? -eq 0 ]; then
		TLINES=`echo $TLINES | gawk '{print $1}'`
	
		if [ "$LINES" != "$TLINES" ]; then
			FAILED=1
			echo "FAILED: Test #1: wc -l line count is different from the reference"
		else 
			echo "PASSED: Test #1 (wc - display line count) passed"
		fi

	else
		echo "FAILED: Test #1 wc -l returned non-zero exit code"
		FAILED=1
	fi 


	TWORDS=$(wc -w $TESTDATAFILE )

	if [ $? -eq 0 ]; then
		TWORDS=`echo $TWORDS | gawk '{print $1}'`
	
		if [ "$WORDS" != "$TWORDS" ]; then
			FAILED=2
			echo "FAILED: Test #2: wc -w word count is different from the reference"
		else
			echo "PASSED: Test #2 (wc - display word count) passed"
		fi
	else
		echo "FAILED: Test #2 wc -w returned non-zero exit code"
		FAILED=2
	fi 

 
	TCHARS=$(wc -c $TESTDATAFILE ) 

	if [ $? -eq 0 ]; then 
		TCHARS=`echo $TCHARS | gawk '{print $1}'`

		if [ "$CHARS" != "$TCHARS" ]; then
			FAILED=3
			echo "FAILED: Test #3: wc -c character count different from the reference"
		else
			echo "PASSED: Test #3 (wc - display character count) passed"
		fi
	else
		echo "FAILED: Test #3 (wc - display character count) failed"
	fi 

	TLLINE=$(wc -L $TESTDATAFILE ) 
	
	if [ $? -eq 0 ]; then
		TLLINE=`echo $TLLINE | gawk '{print $1}'`

		if [ "$LLINE" != "$TLLINE" ]; then
			FAILED=4
			echo "FAILED: Test #4: wc -L longest line length is different from the reference"
		else
			echo "PASSED: Test #4 (wc - display longest line length) passed"			
		fi
	else
		echo "FAILED: Test #4 (wc - display longest line length) failed"
	fi 

#	echo tested lines: $TLINES
#	echo trooth lines: $LINES
#	echo
#	echo tested lines: $TWORDS
#	echo trooth lines: $WORDS
#	echo
#	echo tested lines: $TWORDS
#	echo trooth lines: $WORDS
#	echo
#	echo tested longest line: $TLLINE
#	echo trooth longest line: $LLINE

#overall result
	if [ $FAILED -ne 0 ]; then
		echo "FAILED: Overall result of wc_lsb.sh is failed (last failed test was $FAILED)"
		exit 1
	else 
		echo "PASSED: Overall result of wc_lsb.sh is passed"
		exit 0
	fi


else 

	echo "FAILED: ERROR: wc cannot be called"
	exit 1
fi

