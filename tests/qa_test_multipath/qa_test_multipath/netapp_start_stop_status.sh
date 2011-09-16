#!/bin/bash
HW=1
. /usr/share/qa/qa_test_multipath/functions.sh

backup_conf

config_prepare NETAPP 
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
