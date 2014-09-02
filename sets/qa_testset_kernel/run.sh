#! /bin/bash

# Set log level
echo 8 >/proc/sys/kernel/printk

# Install the test suites packages for validation testing.
/usr/share/qa/qa_testset_kernel/install.sh -r -k
echo -e "You can run kernel and regression tests now.\n"
# Set Env
echo $PATH | grep '/usr/share/qa/tools:/usr/lib/ctcs2/tools' > /dev/null || export PATH="/usr/share/qa/tools:/usr/lib/ctcs2/tools:$PATH"
kernel_run=`awk -F "\t+" '{print $2}' /usr/share/qa/qa_testset_kernel/kernel_test_packages`
regression_run=`awk -F "\t+" '{print $2}' /usr/share/qa/qa_testset_kernel/regression_test_packages`

i=1
#Change $IFS for Loop Command Names With Spaces
SAVE_IFS=$IFS
IFS=$'\n'
for test_name in $regression_run $kernel_run;do
        echo -e "============ Testing ${test_name} [$i] =============\n"
	logger "Run#[$i] $test_name"
	echo "$test_name"|sh
        let i=i+1
done
#Restore $IFS
IFS=$SAVE_IFS
