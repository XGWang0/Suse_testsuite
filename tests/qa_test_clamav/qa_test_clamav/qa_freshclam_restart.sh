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
#           FILE: qa_freshclam_restart.sh
#        VERSION: 0.3
#         AUTHOR: Andrej Semen <asemen@suse.de>
#       REVIEWER: 
#
#        CREATED: 2008-11-19
#        REVISED: 2008-12-12
#
#    DESCRIPTION: "freshclam - update virus databases"
#   REQUIREMENTS: ""
#          USAGE: ./qa_freshclam_restart.sh
#
#===============================================================================

#<Declarations>

TESTBASEDIR="/usr/share/qa/qa_test_clamav";
TESTDATADIR="/usr/share/qa/qa_test_clamav/data";
FAILED="0";
FRESHCLAM_BIN=/usr/bin/freshclam
FRESHCLAM_PIDFILE=/var/lib/clamav/freshclam.pid

#</Declarations>

#<main>

# check if freshclamd is started, and stop freshclamd.
rcfreshclam status
RET=$?
#echo $RET
        if [ $RET -eq 0 ]
        then
                echo "clamd is running ... stopping clamd ..." >&2
	rcfreshclam stop
	sleep 5
        fi


rcfreshclam restart
# 1st check if freshclamd is running after restart
rcfreshclam status
RET=$?
#echo $RET

case "$RET" in
	
	0)
        echo -n "0 - service up and running "
        ;;
	1)
        echo -n "1 - service dead, but /var/run/  pid  file exists "
	exit 1
        ;;
	2)
        echo -n "2 - service dead, but /var/lock/ lock file exists "
	exit 1
        ;;
	3)
        echo -n "3 - service not running (unused) "
	exit 1
        ;;
	4)
        echo -n "4 - service status unknown :-( "
	exit 1
        ;;
	5)
        echo -n "5--199 reserved (5--99 LSB, 100--149 distro, 150--199 appl.) "
	exit 1
        ;;
    	*)
        echo "Usage: $0 {Return not between 0 and 5 }"
	exit 1
        ;;
esac

        # Return value is slightly different for the status command:
        # 0 - service up and running
        # 1 - service dead, but /var/run/  pid  file exists
        # 2 - service dead, but /var/lock/ lock file exists
        # 3 - service not running (unused)
        # 4 - service status unknown :-(
        # 5--199 reserved (5--99 LSB, 100--149 distro, 150--199 appl.)

sleep 5



# check if freshclamd is started.
rcfreshclam status
RET=$?
#echo $RET
        if [ $RET -ne 0 ]
        then
                echo "freshclamd is not running ... -Internal Error exit 2-" >&2
	exit 2
        fi

rcfreshclam restart
# 2nd check if freshclamd is running after restart
rcfreshclam status
RET=$?
#echo $RET
case "$RET" in
	
	0)
        echo -n "0 - service up and running "
        ;;
	1)
        echo -n "1 - service dead, but /var/run/  pid  file exists "
	exit 1
        ;;
	2)
        echo -n "2 - service dead, but /var/lock/ lock file exists "
	exit 1
        ;;
	3)
        echo -n "3 - service not running (unused) "
	exit 1
        ;;
	4)
        echo -n "4 - service status unknown :-( "
	exit 1
        ;;
	5)
        echo -n "5--199 reserved (5--99 LSB, 100--149 distro, 150--199 appl.) "
	exit 1
        ;;
    	*)
        echo "Usage: $0 {Return not between 0 and 5 }"
	exit 1
        ;;
esac

sleep 5
#</main>
sleep 5
exit 0


