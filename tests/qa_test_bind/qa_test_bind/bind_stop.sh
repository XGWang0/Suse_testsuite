#!/bin/sh

. bind.rc

backup_config
install_config "forwarder"

$BINDCTRL restart

sleep 10

if [ ! -e $PID_FILE ]; then
   echo "FAILED: bind - Stop daemon (could not start to stop)"
   RC=1
else
   PID=`cat $PID_FILE`
   $BINDCTRL stop
   
   sleep 10

   RESULT=$(ps ax | grep "$PID.*/usr/sbin/named" | grep -v grep)
   if [ -n "$RESULT" ]; then
      echo "FAILED: bind - Stop daemon (didn't stop)"
      RC=1
   else
      echo "PASSED: bind - Stop daemon"
   fi
fi

restore_config

exit $RC

