#!/bin/bash

timer=6000

cd qa_test_virtualization/
type="$1"

[ "$type" == "" ] && type=standalone

for i in install_* ; do
	cat << EOF
timer $timer
fg 1 $i /usr/share/qa/qa_test_virtualization/$i $type
wait

EOF
done

