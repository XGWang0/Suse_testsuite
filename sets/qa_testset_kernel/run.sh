#! /bin/bash

export PATH="/usr/share/qa/tools:/usr/lib/ctcs2/tools:$PATH"

kernel_run=`awk '{print $2}' /usr/share/qa/qa_testset_kernel/kernel_test_packages`
regression_run=`awk '{print $2}' /usr/share/qa/qa_testset_kernel/regression_test_packages`

mkdir -p /root/submission_log
for test_case in test_sched_stress-run test_fs_stress-run test_process_stress-run;do
	/bin/bash $test_case
done
remote_qa_db_report.pl -T lzheng > /root/submission_log/3_stress 2>&1	

url=`tail -n1 /root/submission_log/3_stress |awk '{print $7}'`


echo "The three stress tests(sched,fs,process) have been completed.The submission url is $url" | mail -s "Please review the stress tests result. " lzheng@suse.com jli@suse.com


i=1
for test_name in $kernel_run $regression_run;do
        echo -e "========================================= Testing ${test_name} [$i] ======================================\n"
#        run_path=`grep $test_name /usr/share/qa/qa_testset_kernel/*test_packages | awk '{print $3}'`
#        /bin/bash $run_path/$test_name
	/bin/bash $test_name

        let i=i+1
done
