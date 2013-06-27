#!/bin/bash
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE. All Rights Reserved.
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
#           FILE: qa_clamd_start.sh
#        VERSION: 0.3
#         AUTHOR: Andrej Semen <asemen@suse.de>
#       REVIEWER:
#
#        CREATED: 2008-11-10
#        REVISED: 2008-12-12
#
#    DESCRIPTION: "start the clamd"
#   REQUIREMENTS: ""
#          USAGE: ./qa_clamd_start.sh
#
#===============================================================================



source libqainternal.lib.sh


function clamd_start {
    if startService "clamd"; then
        printMessage $MSG_PASSED "clamd - start the service"
        return $PASSED
    else
        printMessage $MSG_FAILED "clamd - start the service"
        return $FAILED
    fi
}

# check if clamd is stoped.
rcclamd status
RET=$?
#echo $RET
        if [ $RET -eq 0 ]
        then
                echo "clamd is running ... stopping clamd ..." >&2
	rcclamd stop
	sleep 5
        fi

sleep 5
# 2nd check if clamd is stoped. 
rcclamd status
RET=$?
#echo $RET
        if [ $RET -eq 0 ]
        then
                echo "clamd is running ... FAILED to stop clamd - internel ERROR -" >&2
		exit 2
        fi

        # Return value is slightly different for the status command:
        # 0 - service up and running
        # 1 - service dead, but /var/run/  pid  file exists
        # 2 - service dead, but /var/lock/ lock file exists
        # 3 - service not running (unused)
        # 4 - service status unknown :-(
        # 5--199 reserved (5--99 LSB, 100--149 distro, 150--199 appl.)

# scan file using clamd
# clamdscan - scan files and directories for viruses using Clam AntiVirus Daemon (man clamdscan)
# RETURN CODES
# 0 : No virus found.
# 1 : Virus(es) found.
# 2 : An error occured.


clamd_start
sleep 5
exit 0

