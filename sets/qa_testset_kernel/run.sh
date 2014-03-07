kernel_run=`awk '{print $2}' /usr/share/qa/qa_testset_kernel/kernel_test_packages`
regression_run=`awk '{print $2}' /usr/share/qa/qa_testset_kernel/regression_test_packages`

i=1
for test_name in $kernel_run $regression_run;do
        echo -e "========================================= Testing ${test_name} [$i] ======================================\n"
        run_path=`grep $test_run /usr/share/qa/qa_testset_kernel/*test_packages | awk '{print $3}'`
        /bin/bash $run_path/$test_name
        let i=i+1
done
