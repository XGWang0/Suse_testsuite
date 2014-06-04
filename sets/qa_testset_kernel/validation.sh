#! /bin/bash
mkdir -p /root/submission_log
for test_case in test_sched_stress-run test_fs_stress-run test_process_stress-run;do
        /bin/bash $test_case
done
remote_qa_db_report.pl -T lzheng > /root/submission_log/3_stress 2>&1  

url=`tail -n1 /root/submission_log/3_stress |awk '{print $7}'`


echo "The three stress tests(sched,fs,process) have been completed.\n The submission url is $url" | mail -s "Please review the stress test
s result. " bwliu@suse.com
