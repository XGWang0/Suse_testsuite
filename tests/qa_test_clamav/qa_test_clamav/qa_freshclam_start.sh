#!/bin/bash

#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: qa_freshclam_start.sh
#        VERSION: 0.3
#         AUTHOR: Andrej Semen <asemen@suse.de>
#       REVIEWER:
#        LICENSE: GPL
#
#        CREATED: 2008-11-19
#        REVISED: 2008-12-12
#
#    DESCRIPTION: "start the freshclam"
#   REQUIREMENTS: ""
#          USAGE: ./qa_freshclam_start.sh
#
#===============================================================================



source libqainternal.lib.sh


function freshclam_start {
    if startService "freshclam"; then
        printMessage $MSG_PASSED "freshclam - start the service"
        return $PASSED
    else
        printMessage $MSG_FAILED "freshclam - start the service"
        return $FAILED
    fi
}


# check if freshclamd is stoped.
rcfreshclam status
RET=$?
#echo $RET
        if [ $RET -eq 0 ]
        then
                echo "freshclamd is running ... stopping freshclamd ..." >&2
	rcfreshclam stop
	sleep 5
        fi

sleep 2
# 2nd check if clamd is stoped. 
rcfreshclam status
RET=$?
#echo $RET
        if [ $RET -eq 0 ]
        then
                echo "freshclamd is running ... FAILED to stop clamd - internel ERROR -" >&2
		exit 2
        fi

freshclam_start
sleep 5
exit 0
