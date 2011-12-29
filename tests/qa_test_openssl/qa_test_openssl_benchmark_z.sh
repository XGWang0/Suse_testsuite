#!/bin/bash
if [[ $(lsmod |grep z90crypt |wc -l) -gt 1 ]]; then
	openssl speed -engine ibmca
else
	exit 22
fi
