#!/bin/bash
if [[ $(lsmod |grep -q z90crypt) -eq 0 ]]; then
	openssl speed -e ibmca 
else
	exit 22
fi
