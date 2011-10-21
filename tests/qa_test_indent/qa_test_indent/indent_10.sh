#!/bin/sh

DATADIR=/usr/share/qa/qa_test_indent/data

cp $DATADIR/testing_indent* /tmp

indent -i10 /tmp/testing_indent.in

if  diff -s /tmp/testing_indent.in /tmp/testing_indent.10 >/dev/null; then

	echo "PASSED: indent - format 10"
	rm -f /tmp/testing_indent*
	exit 0

else 

	echo "FAILED: indent - format 10"
	rm -f /tmp/testing_indent*
	exit 1

fi



