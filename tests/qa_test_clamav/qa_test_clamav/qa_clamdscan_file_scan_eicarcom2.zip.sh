#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: qa_clamdscan_file_scan_eicarcom2.zip.sh
#        VERSION: 0.3
#         AUTHOR: Andrej Semen <asemen@suse.de>
#       REVIEWER: 
#        LICENSE: GPL
#
#        CREATED: 2008-11-19
#        REVISED: 2008-11-19
#
#    DESCRIPTION: "clamdscan eicarcom2.zip testfile"
#   REQUIREMENTS: ""
#          USAGE: ./qa_clamdscan_file_scan_eicarcom2.zip.sh
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

#first check if cladm is running
rcclamd status 
RET=$?
#echo $RET
        if [ $RET -ne 0 ]
        then
                echo "FAILED: clamd is not running -Internal Error-" >&2
                exit 2;
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

clamdscan $TESTDATADIR/eicarcom2.zip
RET3=$?
echo $RET3
        if [ $RET3 -ne 1 ]
        then
                echo "FAILED: clamdscan $TESTDATADIR/eicarcom2.zip" >&2
                exit 1;
        fi


#</main>
exit 0
