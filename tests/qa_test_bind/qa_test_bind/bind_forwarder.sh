#!/bin/bash

. bind.rc

backup_config
install_config "forwarder"

$BINDCTRL restart

sleep 10

QUERY="www.web.de"
RESULT=$(dig @127.0.0.1 $QUERY | grep -E "^$QUERY")

echo "query for '$QUERY' resulted in '$RESULT'"

if [ -n "$RESULT" ]; then
   echo "PASSED: bind - Test forward config"
   RC=0

else
   echo "FAILED: bind - Test forward config"
   RC=1
fi

restore_config

exit $RC
