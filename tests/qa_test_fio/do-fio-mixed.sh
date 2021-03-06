#!/bin/sh

CONFIG=/usr/share/qa/fio/fio-mixed.job
NEEDED_MB=1600

# config
if [ ! -r $CONFIG ]
then
	echo "Config file $CONFIG missing"
	exit 11
fi

DIR=`grep '^directory=' $CONFIG | cut -d= -f2-`
if [ -z "$DIR" ]
then
	echo "Directory not found in $CONFIG"
	exit 11
fi

DF=`df $DIR | grep -v Filesystem | sed 's/\s\+/ /g' | cut -d\  -f4`
if [ -z "$DF" ]
then
	echo "Could not free disk space in $DIR"
	exit 11
fi
MB=`expr $DF / 1024`
if [ ! -z "$MB" ]
then
	if [ $MB -lt $NEEDED_MB ]
	then
		echo "Not enough disk space in $DIR : $MB free, $NEEDED_MB needed"
		exit 11
	fi
fi

# run
fio $CONFIG

# cleanup
rm $DIR/file*.*.*
