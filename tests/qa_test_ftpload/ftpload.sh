#!/bin/bash
if [ ! -d /abuild/ftpload_test ] ; then
	mkdir -p /abuild/ftpload_test
fi 

FREE_SPACE=`df -m / | grep -e "/$" | awk '{print $4}'`
if [ $FREE_SPACE -le 400 ]; then
	echo "no enough space for this test! At least 400MB free space is required!"
	exit 1
fi

ftpload -d /abuild/ftpload_test -c 20 ftp://10.11.136.9/400MB
