#!/bin/sh

#this file is a simple test wrapper since subdomain regression tests must
#be executed within the subdomain directory. This script can be executed
#from anywhere

pushd . > /dev/null
cd /usr/share/qa/qa_test_apparmor/tests
sh $1
RESULT=$?
popd > /dev/null
exit $RESULT
