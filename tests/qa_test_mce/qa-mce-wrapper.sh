#!/bin/bash
#
# Wrapper for simple mce-tests that doesn't return their result as return
# number.
#

MCEDIR=/usr/share/qa/qa_test_mce/

#
# Run the test
#
$MCEDIR/drivers/simple/driver.sh $1

#
# Return the result
#
# The tests are writing lines starting with "Failed:" and "Passed:" into log,
# testrun is considered to be succesfull if there were some lines in log that
# contains "Passed" and doesn't contain "Failed".
#
if grep -q "Failed" $MCEDIR/results/simple/result; then
	exit 1
else
	if grep -q "Passed" $MCEDIR/results/simple/result; then
		exit 0
	else
		exit 1
	fi
fi
