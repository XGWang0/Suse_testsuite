#!/bin/bash
HW=1
. /usr/share/qa/qa_test_multipath/functions.sh

backup_conf

config_prepare NETAPP 
if [ $? -eq 50 ];then
exit 22
fi

for map_alias in ${MAPS[@]};
do
map="$map_alias"

reseterr
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
done

createresult
