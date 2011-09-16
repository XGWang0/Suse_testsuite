#!/bin/sh

TMPDIR=/tmp/topack

DIR=/usr/share/qa/qa_test_gzip
DATA=$DIR/data


if ! [ -e $TMPDIR ]; then
	mkdir $TMPDIR
fi

cp $DATA/topack/file* $TMPDIR 
gzip -n $TMPDIR/*

if ! diff -s $TMPDIR $DATA/archive > /dev/null ; then 
	echo "FAILED: gzip - Create archive"
	rm -rf $TMPDIR 
	exit 1

else
	
	echo "PASSED: gzip - Create archive"
	rm -rf $TMPDIR 
	exit 0

fi



