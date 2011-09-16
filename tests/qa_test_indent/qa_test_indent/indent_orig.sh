#!/bin/sh

DATADIR=/usr/share/qa/qa_test_indent/data

cp $DATADIR/testing_indent* /tmp

indent -orig /tmp/testing_indent.in

if diff -s /tmp/testing_indent.in /tmp/testing_indent.berkley >/dev/null; then

	echo "PASSED: indent - format orig"
	rm -f /tmp/testing_indent*
	exit 0

else 

	echo "FAILED: indent - format orig"
	rm -f /tmp/testing_indent*
	exit 1

fi

