#!/bin/bash
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
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

