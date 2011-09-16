#!/bin/sh

#this file is a simple wrapper for eval_onescript.sh, which must be
#executed in "testing" directory. This script can be executed from anywhere

pushd . > /dev/null
cd /usr/share/qa/qa_test_net-snmp/testing
./eval_onescript.sh $1
RESULT=$?
popd > /dev/null
exit $RESULT
