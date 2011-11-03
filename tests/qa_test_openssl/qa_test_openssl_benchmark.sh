#!/bin/bash
[[ $(uname -m) == s390* ]] && rcz90crypt stop &> /dev/null

openssl speed

[[ $(uname -m) == s390* ]] && rcz90crypt start &> /dev/null

exit 0
