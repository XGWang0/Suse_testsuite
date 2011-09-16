#!/bin/sh

. bind.rc

backup_config
install_config "forwarder"

if [ ! -e $PID_FILE ]; then
   $BINDCTRL start
fi
	
sleep 10

OLDPID=`cat $PID_FILE`

$BINDCTRL restart

sleep 10

if [ -e $PID_FILE ]; then
   NEWPID=`cat $PID_FILE`

   if [ $OLDPID != $NEWPID ]; then
       echo "PASSED: bind - Restart daemon"
       RC=0
   else
       echo "FAILED: bind - Restart daemon"
       RC=1
   fi
else
   echo "FAILED: bind - Restart daemon"
   RC=1
fi

restore_config

exit $RC
