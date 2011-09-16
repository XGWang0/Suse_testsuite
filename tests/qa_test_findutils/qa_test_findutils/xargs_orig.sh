#!/bin/sh

cd /usr/share/qa/qa_test_findutils/orig_tests/xargs/testsuite

mkdir -p /tmp/qa_test_findutils/xargs_orig
runtest --outdir /tmp/qa_test_findutils/xargs_orig

exit $?
