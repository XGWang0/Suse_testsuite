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

/etc/init.d/multipathd stop
checkerror

/etc/init.d/multipathd start
checkerror

/etc/init.d/multipathd restart
checkerror

/etc/init.d/multipathd status
checkerror

createresult
