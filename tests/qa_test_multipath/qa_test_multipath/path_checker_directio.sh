#!/bin/bash
. /usr/share/qa/qa_test_multipath/functions.sh

backup_conf

CONFIG=$DATA_DIR/path_checker_dio
map="multipath-test"
reseterr

iscsi_connect
checkerror
prepare
checkerror

get_paths
PATHS_NUMBER=$[${#PATHS[*]}-1]

for n in `seq 1 $PATHS_NUMBER`; 
do
	fail_path $n
	sleep 30;
	paths_status
	check_failed $n
	checkerror

	recover_path $n
	sleep 30;
	paths_status
	check_active $n
	checkerror
done

createresult
