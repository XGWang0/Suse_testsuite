#!/bin/bash
. /usr/share/qa/qa_test_multipath/functions.sh

backup_conf

HW=1

config_prepare EMC 
if [ $? -eq 50 ];then
exit 22
fi 

reseterr
prepare
checkerror

/etc/init.d/multipathd stop
checkerror

/etc/init.d/multipathd start
checkerror

/etc/init.d/multipathd restart
checkerror

/etc/init.d/multipathd status
checkerror

createresult
