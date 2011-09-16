#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: basename_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#        LICENSE: unknown
#
#        CREATED: 2005-11-09
#        REVISED: 2005-11-09
#
#    DESCRIPTION: "test use of basename"
#   REQUIREMENTS: "needs coreutils, grep, mktemp"
#          USAGE: ./basename_lsb.sh
#
#===============================================================================

if basename --help &>/dev/null; then 

	TMPDIR=`mktemp -d`
	TESTSTRING="$TMPDIR/you_know/some_testing_dirs/hello.world"

	rm -r $TMPDIR
	if basename "$TESTSTRING" .world | grep "^hello$" > /dev/null; then
	    echo "PASSED: basename - basic functions"
	    exit 0		
	else
	    echo "FAILED: basename - basic functions"
	    exit 1	
	fi

else 
	echo "FAILED: ERROR: basename cannot be called"
	exit 1
fi
