#!/bin/sh

cd /usr/share/qa/qa_test_findutils/orig_tests/find/testsuite

mkdir -p /tmp/qa_test_findutils/find_orig
runtest --outdir /tmp/qa_test_findutils/find_orig

exit $?
