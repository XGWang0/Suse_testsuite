#! /bin/bash

# Set log level
echo 8 >/proc/sys/kernel/printk

# Install the test suites packages for validation testing.
/usr/share/qa/qa_testset_kernel/install.sh -v

echo -e "You can run stress validation tests now.\n"
# Set Env
echo $PATH | grep '/usr/share/qa/tools:/usr/lib/ctcs2/tools' > /dev/null || export PATH="/usr/share/qa/tools:/usr/lib/ctcs2/tools:$PATH"
# Run the validation testing.
validation_run=`awk -F "\t+" '{print $2}' /usr/share/qa/qa_testset_kernel/validation_test_packages`
i=1
#Change $IFS for Loop Command Names With Spaces
SAVE_IFS=$IFS
IFS=$'\n'
for test_name in $validation_run ;do
        echo -e "============ Testing ${test_name} [$i] =============\n"
	logger "Run#[$i] $test_name"
	echo "$test_name"|sh
        let i=i+1
done
#Restore $IFS
IFS=$SAVE_IFS

# redirect the submission log to a file.
mkdir -p /root/submission_log
remote_qa_db_report.pl -b -T bwliu > /root/submission_log/3_stress 2>&1  
# get the submission url. 
url=`tail -n1 /root/submission_log/3_stress |awk '{print $7}'`
# send E-mail to tester. 
logger "Send E-mail, the submission url is $url"
echo "The three stress tests(sched,fs,process) have been completed.\n The submission url is $url" | mail -s "Please review the stress tests result. "  bwliu@suse.com
