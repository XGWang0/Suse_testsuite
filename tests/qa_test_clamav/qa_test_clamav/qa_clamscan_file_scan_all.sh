#/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: qa_clamav_file_scan_clamscan.sh
#        VERSION: 0.1
#         AUTHOR: Andrej Semen <asemen@suse.de>
#       REVIEWER: 
#        LICENSE: GPL
#
#        CREATED: 2008-11-13
#        REVISED: 2008-11-13
#
#    DESCRIPTION: "clamscan - scan files and directories for viruses"
#   REQUIREMENTS: ""
#          USAGE: ./qa_clamav_file_scan_clamscan.sh
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


clamscan $TESTDATADIR/MIME-test
RET1=$?
echo "Return code $RET1"
	if [ $RET1 -ne 0 ] 
        then
                echo "FAILED: clamscan $TESTDATADIR/MIME-test return code $RET1" >&2
                exit 1;
	fi

clamscan $TESTDATADIR/bad-zip	
RET2=$?
echo "Return code $RET2"
	if [ $RET2 -ne 0 ] 
        then
                echo "FAILED: clamscan $TESTDATADIR/bad-zip return code $RET2" >&2
                exit 1;
	fi

clamdscan $TESTDATADIR/eicarcom2.zip
RET3=$?
echo "Return code $RET3"
	if [ $RET3 -ne 1 ] 
        then
                echo "FAILED: clamscan $TESTDATADIR/eicarcom2.zip return code $RET3" >&2
                exit 1;
	fi


#</main>
exit 0
