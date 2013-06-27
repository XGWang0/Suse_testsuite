#/bin/bash
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
#           FILE: qa_clamscan_file_scan_bad-zip.sh
#        VERSION: 0.2
#         AUTHOR: Andrej Semen <asemen@suse.de>
#       REVIEWER: 
#
#        CREATED: 2008-11-19
#        REVISED: 2008-11-19
#
#    DESCRIPTION: "clamscan - scan bad-zip file for viruses"
#   REQUIREMENTS: ""
#          USAGE: ./qa_clamscan_file_scan_bad-zip.sh
#
#===============================================================================

#<Declarations>

TESTBASEDIR="/usr/share/qa/qa_test_clamav";
TESTDATADIR="/usr/share/qa/qa_test_clamav/data";
FAILED="0";

#</Declarations>

#<main>


# scan file using kommandline clamscan
# clamscan - scan files and directories for viruses
# RETURN CODES 
# 0 : No virus found.
# 1 : Virus(es) found.
# 40: Unknown option passed.
# 50: Database initialization error.
# 52: Not supported file type.
# 53: Can't open directory.
# 54: Can't open file. (ofm)
# 55: Error reading file. (ofm)
# 56: Can't stat input file / directory.
# 57: Can't get absolute path name of current working directory.
# 58: I/O error, please check your file system.
# 62: Can't initialize logger.
# 63: Can't create temporary files/directories (check permissions).
# 64: Can't write to temporary directory (please specify another one).
# 70: Can't allocate memory (calloc).
# 71: Can't allocate memory (malloc).


clamscan $TESTDATADIR/bad-zip	
RET2=$?
echo "Return code $RET2"
	if [ $RET2 -ne 0 ] 
        then
                echo "FAILED: clamscan $TESTDATADIR/bad-zip return code $RET2" >&2
                exit 1;
	fi

#</main>
exit 0
