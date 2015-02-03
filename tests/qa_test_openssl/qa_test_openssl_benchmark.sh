#!/bin/bash
COUNT=5

TEMPDIR=$(mktemp -d)
DIR=$(cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)

for i in $(seq ${COUNT}); do
	echo "Running temporary run number ${i}, storing into bench${i}.out"
	if [[ $(lsmod |grep z90crypt |wc -l) -gt 1 ]]; then
		echo "Running tests using HW cryptography modules"
		openssl speed -engine ibmca &> "${TEMPDIR}/bench${i}.out"
	else
		echo "Running tests without HW cryptography modules"
		[[ $(uname -m) == s390* ]] && rcz90crypt stop &> /dev/null
		openssl speed &> "${TEMPDIR}/bench${i}.out"
		[[ $(uname -m) == s390* ]] && rcz90crypt start &> /dev/null
	fi
done
perl "${DIR}/process_benchmarks.pl" $(for i in $(seq ${COUNT}); do echo "${TEMPDIR}/bench${i}.out" |tr '\n' ' '; done)
exit 0
