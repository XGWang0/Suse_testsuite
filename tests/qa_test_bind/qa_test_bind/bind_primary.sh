#!/bin/bash

. bind.rc

backup_config
install_config "primary"

$BINDCTRL restart

sleep 10

QUERY_1="probe1.testing.foo"
MATCH_1="192.168.42.250"
RESULT_1=$(dig @127.0.0.1 $QUERY_1 | grep -E "(^$QUERY_1.*$MATCH_1)")

echo "query for '$QUERY_1' resulted in '$RESULT_1'"

QUERY_2="192.168.42.251"
MATCH_2="251.42.168.192.in-addr.arpa"
RESULT_2=$(dig @127.0.0.1 -x $QUERY_2 | grep -E "^$MATCH_2")

echo "query for '$QUERY_2' resulted in '$RESULT_2'"

if [ -n "$RESULT_1" -a -n "$RESULT_2" ]; then
   echo "PASSED: bind - Primary DNS"
   RC=0
else 
   echo "FAILED: bind - Primary DNS"
   RC=1
fi
   
restore_config

exit $RC
