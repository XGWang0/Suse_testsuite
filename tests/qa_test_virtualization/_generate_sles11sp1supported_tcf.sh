#!/bin/bash

timer=6000

cd qa_test_virtualization/
type="$1"

[ "$type" == "" ] && type=standalone

for i in install_* ; do
	# This is intentionally in for of blacklist, so that all newer are tested as well (maybe should be changed in the future?"
	echo $i | grep -q 'nw-65-sp7\|oes-2-fcs\|oes-2-sp1\|rhel-3\|rhel-4-u6\|rhel-4-u7\|rhel-5-fcs\|rhel-5-u1\|rhel-5-u2\|rhel-5-u3\|rhel-5-u4\|sle[ds]-10-sp1\|sle[ds]-10-sp2\|sled-10-sp3\|sle[ds]-10-fcs\|win-vista-fcs\|win-vista-sp1\|win-xp-sp1\|win-xp-sp2\|win-xp-fcs\|win-2k8-' && continue
	cat << EOF
timer $timer
fg 1 $i /usr/share/qa/qa_test_virtualization/$i $type
wait

EOF
done

