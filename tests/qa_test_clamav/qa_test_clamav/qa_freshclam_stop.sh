#!/bin/bash
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************
#

#===============================================================================
#
#           FILE: qa_freshclam_stop.sh
#        VERSION: 0.3
#         AUTHOR: Andrej Semen <asemen@suse.de>
#       REVIEWER:
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

