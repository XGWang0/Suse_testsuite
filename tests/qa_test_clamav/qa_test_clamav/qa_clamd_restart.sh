#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: qa_clamd_restart.sh
#        VERSION: 0.2
#         AUTHOR: Andrej Semen <asemen@suse.de>
#       REVIEWER: 
#        LICENSE: GPL
#
#        CREATED: 2008-11-10
#        REVISED: 2008-12-12
#
#    DESCRIPTION: "clamd scan some files malware and clean file"
#   REQUIREMENTS: ""
#          USAGE: ./qa_clamd_restart.sh
#
#===============================================================================

#<Declarations>

TESTBASEDIR="/usr/share/qa/qa_test_clamav";
TESTDATADIR="/usr/share/qa/qa_test_clamav/data";
FAILED="0";
CLAMD_BIN=/usr/sbin/clamd
CLAMD_PIDFILE=/var/lib/clamav/clamd.pid

#</Declarations>

#<main>

# stop clamd if not already stoped:

# check if clamd is started, and stop clamd.
rcclamd status
RET=$?
#echo $RET
        if [ $RET -eq 0 ]
        then
                echo "clamd is running ... stopping clamd ..." >&2
	rcclamd stop
	sleep 5
        fi

rcclamd restart
# 1st check if cladm is running after restart
rcclamd status 
RET=$?
#echo $RET

case "$RET" in
	
	0)
        echo -n "0 - service up and running "
	EX1=0
        ;;
	1)
        echo -n "1 - service dead, but /var/run/  pid  file exists "
	EX1=1
        ;;
	2)
        echo -n "2 - service dead, but /var/lock/ lock file exists "
	EX1=1
        ;;
	3)
        echo -n "3 - service not running (unused) "
	EX1=1
        ;;
	4)
        echo -n "4 - service status unknown :-( "
	EX1=1
        ;;
	5)
        echo -n "5--199 reserved (5--99 LSB, 100--149 distro, 150--199 appl.) "
	EX1=1
        ;;
    	*)
        echo "Usage: $0 {Return not between 0 and 5 }"
	EX1=1
        ;;
esac

sleep 5

# check if clamd is started.
rcclamd status
RET=$?
#echo $RET
        if [ $RET -ne 0 ]
        then
                echo "clamd is not running ... -Internal Error exit 2-" >&2
	exit 2
        fi


rcclamd restart
sleep 5
# 2nd check if cladm is running after restart
rcclamd status 
RET=$?
#echo $RET

case "$RET" in
	
	0)
        echo -n "0 - service up and running "
	EX2=0
        ;;
	1)
        echo -n "1 - service dead, but /var/run/  pid  file exists "
	EX2=1
        ;;
	2)
        echo -n "2 - service dead, but /var/lock/ lock file exists "
	EX2=1
        ;;
	3)
        echo -n "3 - service not running (unused) "
	EX2=1
        ;;
	4)
        echo -n "4 - service status unknown :-( "
	EX2=1
        ;;
	5)
        echo -n "5--199 reserved (5--99 LSB, 100--149 distro, 150--199 appl.) "
	EX2=1
        ;;
    	*)
        echo "Usage: $0 {Return not between 0 and 5 }"
	EX2=1
        ;;
esac

	# exit codes 
	if [ $EX1 -eq 1 ] || [ $EX2 -eq 1 ]
        then
                echo "FAILED: to restart clamd 1st run $EX1 2nd run $EX2" >&2
                exit 1;
        fi


#</main>
sleep 5
exit 0
