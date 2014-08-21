#! /bin/bash

echo $PATH | grep '/usr/share/qa/tools:/usr/lib/ctcs2/tools' > /dev/null || export PATH="/usr/share/qa/tools:/usr/lib/ctcs2/tools:$PATH"
kernel_run=`awk -F "\t+" '{print $2}' /usr/share/qa/qa_testset_kernel/kernel_test_packages`
regression_run=`awk -F "\t+" '{print $2}' /usr/share/qa/qa_testset_kernel/regression_test_packages`

i=1
#Change $IFS for Loop File Names With Spaces
SAVE_IFS=$IFS
IFS=$'\n'
for test_name in $regression_run $kernel_run;do
        echo -e "============ Testing ${test_name} [$i] =============\n"
	echo "$test_name"|sh
        let i=i+1
done
#Restore $IFS
IFS=$SAVE_IFS
