#!/bin/sh

TMPDIR=/tmp/archive 
DIR=/usr/share/qa/qa_test_unace
DATA=$DIR/data

if ! [ -e $TMPDIR ]; then
	mkdir $TMPDIR
fi

( cd  $TMPDIR && unace e -y $DATA/compressed/testarchive.ace ) || return 1




if ! diff -s $DATA/uncompressed/flat $TMPDIR > /dev/null; then

	echo "FAILED: unace - Uncompress archive flat"
	rm -rf $TMPDIR
	exit 1

else
	
	echo "PASSED: unace - Uncompress archive flat"
	rm -rf $TMPDIR
	exit 0

fi


