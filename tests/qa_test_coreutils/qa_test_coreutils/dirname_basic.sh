#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: dirname_basic.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#        LICENSE: unknown
#
#        CREATED: 2005-10-26
#        REVISED: 2005-10-26
#
#    DESCRIPTION: "test use of dirname" 
#   REQUIREMENTS: "needs coreutils, mktemp"
#          USAGE: ./dirname_basic.sh
#
#===============================================================================


if dirname --help &>/dev/null; then
 
	TMPDIR=`mktemp -d`
	TESTSTRING="$TMPDIR/auto_test/yaddayadda"
	
	rm -r $TMPDIR
	if dirname "$TESTSTRING" | grep -q "^$TMPDIR/auto_test$";  then
    		echo "PASSED: dirname - basic functionality"
	     exit 0
	else
	    echo "FAILED: dirname - basic functionality"
    		exit 1
	fi
else 
	echo "FAILED: ERROR: dirname cannot be called"
	exit 1
fi


