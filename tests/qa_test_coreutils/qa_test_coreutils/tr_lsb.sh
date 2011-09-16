#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: tr_lsb.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#        LICENSE: unknown
#
#        CREATED: 2005-11-09
#        REVISED: 2005-11-09
#
#    DESCRIPTION: "test use of tr"
#   REQUIREMENTS: "needs coreutils"
#          USAGE: ./tr_lsb.sh
#
#===============================================================================

if tr --help &>/dev/null; then
	RESULT=`echo 'edcba' | tr abcde xunil`
	
	if [ "$RESULT" = "linux" ]; then
	    echo "PASSED: tr base functionality"
	    exit 0
	else
	    echo "FAILED: tr base functionality"
	    exit 1
	fi
else
	echo "FAILED: ERROR: tr cannot be called"
	exit 1	
fi
