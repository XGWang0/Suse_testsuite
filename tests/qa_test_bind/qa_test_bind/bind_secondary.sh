#!/bin/sh

. bind.rc

backup_config
install_config "secondary"

$BINDCTRL restart
sleep 10 # end of transfer

QUERY="felix.suse.cz"
MATCH="10.20.1.89"
RESULT=$(dig @127.0.0.1 $QUERY | grep -E "(^$QUERY.*$MATCH)")

echo "query for '$QUERY' resulted in '$RESULT'"

if [ -n "$RESULT" ]; then
   echo "PASSED: bind - Slave DNS"
   RC=0
else
   echo "FAILED: bind - Slave DNS"
   RC=1
fi

restore_config

exit $RC
