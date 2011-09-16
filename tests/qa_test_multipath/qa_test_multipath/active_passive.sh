#!/bin/bash
. /usr/share/qa/qa_test_multipath/functions.sh

backup_conf

CONFIG=$DATA_DIR/active_passive
map="multipath-test"

reseterr

iscsi_connect
checkerror
prepare
checkerror

get_paths
PATHS_NUMBER=$[${#PATHS[*]}-1]
paths_status

copy_data

for n in `seq 1 $PATHS_NUMBER`;
	do
	fail_path $n
	sleep 30;
	paths_status
	check_failed $n
	checkerror

	check_data
	checkerror

	recover_path $n
	sleep 30;
	paths_status
	check_active $n
	checkerror

	check_data
	checkerror
done
createresult
