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
#           FILE: qa_freshclam_update.sh 
#        VERSION: 0.2
#         AUTHOR: Andrej Semen <asemen@suse.de>
#       REVIEWER: 
#
#        CREATED: 2008-11-13
#        REVISED: 2008-12-12
#
#    DESCRIPTION: "clamscan - scan files and directories for viruses"
#   REQUIREMENTS: ""
#          USAGE: ./qa_freshclam_update.sh
#
#===============================================================================

#<Declarations>

TESTBASEDIR="/usr/share/qa/qa_test_clamav";
TESTDATADIR="/usr/share/qa/qa_test_clamav/data";
FAILED="0";

. $TESTBASEDIR/clamav.rc

backup_config
install_config "forwarder"


#</Declarations>

#<main>

# RETURN CODES
# 0 : Database successfully updated.
# 1 : Database is up-to-date.
# 40: Unknown option passed.
# 50: Can't change directory.
# 51: Can't check MD5 sum.
# 52: Connection (network) problem.
# 53: Can't unlink file.
# 54: MD5 or digital signature verification error.
# 55: Error reading file.
# 56: Config file error.
# 57: Can't create new file.
# 58: Can't read database from remote server.
# 59: Mirrors are not fully synchronized (try again later).
# 60: Can't get information about '' user from /etc/passwd.
# 61: Can't drop privileges.
# 62: Can't initialize logger.


#freshclam --quiet
freshclam
RET=$?
echo $RET

case "$RET" in

        0)
        echo -n "0 - Database successfully updated."
        ;;
        1)
        echo -n "1 - Database is up-to-date."
        ;;
        40)
        echo -n "40 - Unknown option passed."
        exit 1
        ;;
        50)
        echo -n "50 - Can't change directory."
        exit 1
        ;;
        51)
        echo -n "51 - Can't check MD5 sum."
        exit 1
        ;;
        52)
        echo -n "Connection (network) problem."
        exit 1
        ;;
        53)
        echo -n "Can't unlink file."
        exit 1
        ;;
        54)
        echo -n "Can't unlink file."
        exit 1
        ;;
        55)
        echo -n "Error reading file."
        exit 1
        ;;
        56)
        echo -n "Config file error."
        exit 1
        ;;
        57)
        echo -n "Can't create new file."
        exit 1
        ;;
        58)
        echo -n "Can't read database from remote server."
        exit 1
        ;;
        59)
        echo -n "Mirrors are not fully synchronized (try again later)."
        exit 1
        ;;
        60)
        echo -n "Can't get information about '' user from /etc/passwd."
        exit 1
        ;;
        61)
        echo -n "Can't drop privileges."
        exit 1
        ;;
        62)
        echo -n "Can't initialize logger."
        exit 1
        ;;
        *)
        echo "Usage: $0 {unkown Return coder $RET }"
        exit 1
        ;;
esac
sleep 5

#</main>
exit 0
