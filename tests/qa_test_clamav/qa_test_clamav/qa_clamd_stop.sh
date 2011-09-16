#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: qa_clamd_stop.sh
#        VERSION: 0.3
#         AUTHOR: Andrej Semen <asemen@suse.de>
#       REVIEWER:
#        LICENSE: GPL
#
#        CREATED: 2008-11-19
#        REVISED: 2008-12-12
#
#    DESCRIPTION: "start the clamd"
#   REQUIREMENTS: ""
#          USAGE: ./qa_clamd_stop.sh
#
#===============================================================================


source libqainternal.lib.sh

function clamd_stop() {
    if checkService "clamd"; then
        if stopService "clamd"; then
            printMessage $MSG_PASSED "clamd - stop the service"
            return $PASSED
        else
            printMessage $MSG_FAILED "clamd - stop the service"
            return $FAILED
        fi
    else
        printMessage $MSG_FAILED "clamd - stop the service: clamd is not running."
        return $FAILED
    fi
}


# check if clamd is started.
rcclamd status
RET=$?
#echo $RET
        if [ $RET -ne 0 ]
        then
                echo "clamd is not running ... starting clamd ..." >&2
	rcclamd start
	sleep 5
        fi

sleep 2

# 2nd check if clamd is started. 
rcclamd status
RET=$?
#echo $RET
        if [ $RET -ne 0 ]
        then
                echo "clamd is not running ... FAILED to startclamd - internel ERROR -" >&2
		exit 2
        fi

        # Return value is slightly different for the status command:
        # 0 - service up and running
        # 1 - service dead, but /var/run/  pid  file exists
        # 2 - service dead, but /var/lock/ lock file exists
        # 3 - service not running (unused)
        # 4 - service status unknown :-(
        # 5--199 reserved (5--99 LSB, 100--149 distro, 150--199 appl.)


clamd_stop
sleep 5
exit 0
