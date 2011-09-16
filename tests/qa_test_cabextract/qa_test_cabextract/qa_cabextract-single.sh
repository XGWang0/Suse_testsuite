#!/bin/sh

TMPDIR=/tmp/archive 
DIR=/usr/share/qa/qa_test_cabextract
DATA=$DIR/data

if ! [ -e $TMPDIR ]; then
	mkdir $TMPDIR
fi

cabextract -d $TMPDIR $DATA/compressed/testarchive.cab || return 1




if ! diff -s $DATA/uncompressed $TMPDIR > /dev/null; then

	echo "FAILED: cabextract - Uncompress archive"
	rm -rf $TMPDIR
	exit 1

else
	
	echo "PASSED: cabextract - Uncompress archive"
	rm -rf $TMPDIR
	exit 0

fi


