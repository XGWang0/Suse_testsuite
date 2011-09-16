#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: findutils_find.sh 
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#        LICENSE: unknown
#
#        CREATED: 2006-01-13
#        REVISED: 
#
#    DESCRIPTION: "test use of find (some of available switches)"
#   REQUIREMENTS: "needs findutils, coreutils, grep, mktemp"
#          USAGE: ./findutils_find.sh
#
#===============================================================================

checkscript () {
        if [ $? -ne 0 ]; then
                echo "FAILED: Test #$2: find -$1 returned non-zero exit-code"
			 FAILED=$2
			 return 1
        fi
}

FAILED=0
TMPDIR=`mktemp -d`
TESTFILE='testing_find'

if find --help &>/dev/null; then
#test 'name' switch functionality

	touch "$TMPDIR/$TESTFILE"
		
	RESULT=""
	RESULT=`find $TMPDIR -name "$TESTFILE"`
	if checkscript name 1; then
		if echo "$RESULT" | grep "$TESTFILE" > /dev/null; then
	    		echo "PASSED: Test #1: findutils - find -name switch"
		else
	    		echo "FAILED: Test #1: findutils - find -name switch - test file not found"
			FAILED=1
		fi
	fi

#test 'type' functionality (and mindepth)
	TESTDIR=`mktemp -d -p $TMPDIR`
	TESTDIR=`basename $TESTDIR`
	
	RESULT=`find $TMPDIR -mindepth 1 -type d`
	if checkscript type 2; then
		if echo "$RESULT" | grep -q "$TESTDIR" ; then
	    		echo "PASSED: Test #2: findutils - find -type switch"
		else
	    		echo "FAILED: Test #2: findutils -  find -type switch - test file not found"
			FAILED=2
		fi
	fi
#test 'perm' functionality
	chmod 777 "$TMPDIR/$TESTFILE"
	RESULT=`find $TMPDIR -perm 777`
	if checkscript perm 3; then
		if echo "$RESULT" | grep -q "$TESTFILE" ; then
	    		echo "PASSED: Test #3: findutils - find -perm switch"
		else
	    		echo "FAILED: Test #3: findutils -  find -perm switch - test file not found"
			FAILED=3
		fi
	fi

#test 'uid' switch and compound condition
	MY_UID=`id -u`
	RESULT=`find $TMPDIR -type f -a -uid $MY_UID`
	if checkscript uid 4; then
		if echo "$RESULT" | grep -q "$TESTFILE" ; then
	    		echo "PASSED: Test #4: findutils - find -uid switch "
		else
	    		echo "FAILED: Test #4: findutils -  find -uid switch - test file not found"
			FAILED=4
		fi
	fi
#test 'exec' switch 
	find $TMPDIR -name $TESTFILE -exec rm '{}' \;
	if checkscript exec 5; then
		RESULT=`ls $TMPDIR | grep $TESTFILE`
		if [ -z "$RESULT" ]; then
	    		echo "PASSED: Test #5: findutils - find -exec switch "
		else
	    		echo "FAILED: Test #5: findutils -  find -exec switch - test file not removed"
			FAILED=5
		fi
	fi
	
#cleanup
	rm -r $TMPDIR

#overall result
	if [ $FAILED -ne 0 ]; then
		echo "FAILED: Overall result of findutils_find.sh is failed (last failed test was $FAILED)"
		exit 1
	else 
		echo "PASSED: Overall result of findutils_find.sh is passed"
		exit 0
	fi



else 
		echo "FAILED: ERROR: find cannot be called"
		exit 1
fi


