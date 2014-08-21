#! /bin/bash

# Install the test suites packages for validation testing.
/usr/share/qa/qa_testset_kernel/install.sh -v

echo -e "You can run stress validation tests now.\n"
# Set Env
echo $PATH | grep '/usr/share/qa/tools:/usr/lib/ctcs2/tools' > /dev/null || export PATH="/usr/share/qa/tools:/usr/lib/ctcs2/tools:$PATH"
# run the 3 stress testing.
for test_case in test_sched_stress-run test_fs_stress-run test_process_stress-run;do
        /bin/bash $test_case
done
# redirect the submission log to a file.
mkdir -p /root/submission_log
remote_qa_db_report.pl -b -T bwliu > /root/submission_log/3_stress 2>&1  
# get the submission url. 
url=`tail -n1 /root/submission_log/3_stress |awk '{print $7}'`
# send E-mail to tester. 
echo "The three stress tests(sched,fs,process) have been completed.\n The submission url is $url" | mail -s "Please review the stress tests result. "  bwliu@suse.com
