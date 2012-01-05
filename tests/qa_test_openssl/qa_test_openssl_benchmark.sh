#!/bin/bash
COUNT=5

for i in $(seq ${COUNT}); do
	echo "Running temporary run number ${i}, storing into bench${i}.out"
	if [[ $(lsmod |grep z90crypt |wc -l) -gt 1 ]]; then
		echo "Running tests using HW cryptography modules"
		openssl speed -engine ibmca > "bench${i}.out"
	else
		echo "Running tests without HW cryptography modules"
		[[ $(uname -m) == s390* ]] && rcz90crypt stop &> /dev/null
		openssl speed > "bench${i}.out"
		[[ $(uname -m) == s390* ]] && rcz90crypt start &> /dev/null
	fi
done
perl process_benchmarks.pl $(for i in $(seq ${COUNT}); do echo bench${i}.out |tr '\n' ' '; done)
exit 0
