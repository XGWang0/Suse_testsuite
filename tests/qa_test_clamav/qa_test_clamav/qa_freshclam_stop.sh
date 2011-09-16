#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: qa_freshclam_stop.sh
#        VERSION: 0.3
#         AUTHOR: Andrej Semen <asemen@suse.de>
#       REVIEWER:
#        LICENSE: GPL
#
#        CREATED: 2008-11-19
#        REVISED: 2008-12-12
#
#    DESCRIPTION: "stop the freshclam"
#   REQUIREMENTS: ""
#          USAGE: ./qa_freshclam_stop.sh
#
#===============================================================================


source libqainternal.lib.sh

function freshclam_stop() {
    if checkService "freshclam"; then
        if stopService "freshclam"; then
            printMessage $MSG_PASSED "freshclam - stop the service"
            return $PASSED
        else
            printMessage $MSG_FAILED "freshclam - stop the service"
            return $FAILED
        fi
    else
        printMessage $MSG_FAILED "freshclam - stop the service: freshclam is not running."
        return $FAILED
    fi
}



# check if clamd is started.
rcfreshclam status
RET=$?
#echo $RET
        if [ $RET -ne 0 ]
        then
                echo "freshclamd is not running ... starting freshclamd ..." >&2
	rcfreshclam start
	sleep 5
        fi

sleep 1
# 2nd check if clamd is started. 
rcfreshclam status
RET=$?
#echo $RET
        if [ $RET -ne 0 ]
        then
                echo "freshclamd is not running ... FAILED to start freshclamd - internel ERROR -" >&2
		exit 2
        fi

freshclam_stop
sleep 5
exit 0
