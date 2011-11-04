#!/bin/bash
if [[ $(lsmod |grep -q z90crypt) -eq 0 ]]; then
	openssl speed -engine ibmca
else
	exit 22
fi
