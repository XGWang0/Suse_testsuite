#!/bin/sh

#Simple wrapper program which can be executed from any location

TEST=$1
cd /usr/share/qa/qa_test_postfix
./$TEST
exit $?
