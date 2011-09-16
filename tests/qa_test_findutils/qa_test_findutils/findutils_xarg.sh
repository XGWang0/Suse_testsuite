#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: findutils_xargs.sh 
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#        LICENSE: unknown
#
#        CREATED: 2006-01-17
#        REVISED: 
#
#    DESCRIPTION: "test use of xargs (some of available switches)"
#   REQUIREMENTS: "needs findutils, coreutils, diffutils, grep, mktemp"
#          USAGE: ./findutils_xargs.sh
#
#===============================================================================

checkscript () {
        if [ $? -ne 0 ]; then
                echo "FAILED: Test #$2: xargs -$1 - error executing command invoked by xargs or xargs error"
			 FAILED=$2
			 return 1
        fi
}

FAILED=0
TMPDIR=`mktemp -d`
TESTFILE='testing_find'

if xargs --help &>/dev/null; then
#test basic functionality
	touch "$TMPDIR/$TESTFILE"
	chmod 777 "$TMPDIR/$TESTFILE"
	
	RESULT=''
	RESULT=`find $TMPDIR -name "$TESTFILE" | xargs ls -l`
	
	if checkscript "basic functionality" 1; then
		if echo "$RESULT" | grep ".rwxrwxrwx.*$TMPDIR/$TESTFILE" ; then
	    		echo "PASSED: Test #1: findutils - xargs basic functionality"
		else 
			echo "FAILED: Test #1: findutils - xargs basic functionality - outputs do not match"
			FAILED=1
		fi
	fi

#test 'replace strings' switch
	TESTDIR1=`mktemp -d -p $TMPDIR`
	TESTDIR1=`basename $TESTDIR1`
	TESTDIR2=`mktemp -d -p $TMPDIR`
	TESTDIR2=`basename $TESTDIR2`
	
	for ((i=0; i<=9; i++)); do
		touch $TMPDIR/$TESTDIR1/file$i
	done	
	ls $TMPDIR/$TESTDIR1 | xargs -i  cp $TMPDIR/$TESTDIR1/{} $TMPDIR/$TESTDIR2

	if checkscript "replace strings" 2; then
		if diff -r $TMPDIR/$TESTDIR1 $TMPDIR/$TESTDIR2; then
			echo "PASSED: Test #2: findutils - xargs replace-strings switch "
		else
			echo "FAILED: Test #2: findutils - xargs replace-strings switch - outputs do not match"
			FAILED=2
		fi
	fi

#test 'null' switch
	touch "$TMPDIR/file with spaces"
	find $TMPDIR -name "file*" -print0 | xargs -0 rm
	if checkscript "null switch" 3; then
		RESULT=`ls $TMPDIR | grep "file with spaces"`
		if [ -z "$RESULT" ]; then
			echo "PASSED: Test #3: findutils - xargs null switch"
		else
			echo "FAILED: Test #3: findutils - xargs null switch - target file not removed"
			FAILED=3
		fi
	fi
#cleanup
	rm -r $TMPDIR

#overall result
	if [ $FAILED -ne 0 ]; then
		echo "FAILED: Overall result of findutils_xargs.sh is failed (last failed test was $FAILED)"
		exit 1
	else 
		echo "PASSED: Overall result of findutils_xargs.sh is passed"
		exit 0
	fi
else 
		echo "FAILED: ERROR: xargs cannot be called"
		exit 1
fi
