#!/bin/sh

. bind.rc

backup_config
install_config "forwarder"

$BINDCTRL stop

sleep 10

$BINDCTRL start

sleep 10

if [ -e $PID_FILE ]; then
   PID=`cat $PID_FILE`

   RESULT=$(ps ax | grep "$PID.*/usr/sbin/named")

   if [ -z "$RESULT" ]; then
      echo "FAILED: bind - Start daemon"
      RC=1
   else 
      echo "PASSED: bind - Start daemon"
      RC=0
   fi
else
   echo "FAILED: bind - Start daemon"
   RC=1
fi

restore_config

exit $RC
