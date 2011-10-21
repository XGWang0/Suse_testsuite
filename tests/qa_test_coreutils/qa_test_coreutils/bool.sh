#!/bin/bash

#===============================================================================
#
#           FILE: bool.sh
#        VERSION: 0.1
#         AUTHOR: Katarina Machalkova <kmachalkova@suse.de>
#       REVIEWER:
#
#        CREATED: 2005-11-09
#        REVISED: 2005-11-09
#
#    DESCRIPTION: "test simple use of bool"
#   REQUIREMENTS: "needs coreutils"
#          USAGE: ./bool.sh
#
#===============================================================================

FAILED=0

/bin/true 
RESULT1=$?

if [ $RESULT1 -eq 0 ]; then
    echo "PASSED: Test #1 (bool - true) passed"
else
    echo "FAILED: Test #1 (bool - true) failed"
    FAILED=1
fi


/bin/false 
RESULT2=$?

if [ $RESULT2 -eq 1 ]; then
    echo "PASSED: Test #2 (bool - false) passed"
else
    echo "FAILED: Test #2 (bool - false) failed"
    FAILED=2
fi

#overall result
if [ $FAILED -ne 0 ]; then
	echo "FAILED: Overall result of bool.sh is failed (last failed test was $FAILED)"
	exit 1
else 
	echo "PASSED: Overall result of bool.sh is passed"
	exit 0
fi





