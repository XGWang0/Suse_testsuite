#! /bin/bash


# Install the test suites packages



/usr/share/qa/qa_testset_kernel/install.sh

echo -e "You can run acceptance/kernel/regression tests now.\n"                             
                                                                                                        
#start all tests                                                                                        
                                                                                                        
echo -e "\nBEWARE: ALL TESTS are running, Please see screen -r tests\n" > /etc/motd                     
                                                                                                        
echo -e "All tests starts now, see screen -r tests for details\n"                                       
                                                                                                        
echo -e "========== Starting Testing ==========\n" 

kernel_run=`awk '{print $2}' kernel_test_packages`
regression_run=`awk '{print $2}' regression_test_packages`

for test_run in $kernel_run $regression_run;do
	run_path=`grep $test_run *test_packages | awk '{print $3}'`
	export test_run run_path
	screen -d -L -S $test_run -m /bin/bash -c '(
		echo -e "================================= Testing ${test_run} ================================\n"
		/bin/bash $run_path/$test_run
		)'
done

> /etc/motd

