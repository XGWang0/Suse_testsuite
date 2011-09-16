#!/bin/bash
if [ ! -d /abuild/ftpload_test ] ; then
	mkdir -p /abuild/ftpload_test
fi 

ftpload -d /abuild/ftpload_test -c 20 ftp://10.11.136.9/400MB
