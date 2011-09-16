#!/bin/sh

export current_dir=/usr/share/qa/qa_test_sharutils/upstream_tests 
export PACKAGE_STRING='sharutils 4.6' 
export top_srcdir='/usr/share/qa/qa_test_sharutils/upstream_tests'
export top_builddir='/usr/share/qa/qa_test_sharutils/upstream_tests'


/usr/share/qa/qa_test_sharutils/upstream_tests/tests/$1
