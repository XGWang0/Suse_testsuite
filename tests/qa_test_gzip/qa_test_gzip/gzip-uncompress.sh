#!/bin/sh

TMPDIR=/tmp/archive 
DIR=/usr/share/qa/qa_test_gzip
DATA=$DIR/data

if ! [ -e $TMPDIR ]; then
	mkdir $TMPDIR
fi

cp  $DATA/archive/file*.gz $TMPDIR

gunzip $TMPDIR/*


if ! diff -s $DATA/topack $TMPDIR > /dev/null; then

	echo "FAILED: gzip - Uncompress archive"
	rm -rf $TMPDIR
	exit 1

else
	
	echo "PASSED: gzip - Uncompress archive"
	rm -rf $TMPDIR
	exit 0

fi


