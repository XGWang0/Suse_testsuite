#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: qa_bzip2_bznew.sh
#        VERSION: 0.1
#         AUTHOR: Frank Seidel <fseidel@suse.de>
#       REVIEWER: 
#        LICENSE: unknown
#
#        CREATED: 2005-10-06
#        REVISED: 2005-10-06
#
#    DESCRIPTION: "simple use of bznew to recompress a .gz-file to .bz2"
#   REQUIREMENTS: "needs bzip2"
#          USAGE: ./qa_bzip2_bznew.sh
#
#===============================================================================
 
#<Declarations>
TESTBASEDIR="/usr/share/qa/qa_test_bzip2";
TESTDATADIR="/usr/share/qa/qa_test_bzip2/data";
TESTFILE="${TESTDATADIR}/torepack/testfile.gz";
TMPDIR="$(mktemp -d)";
VERSION="$(rpm -q bzip2 | cut -d\- -f 2)";
FAILED="0";
#</Declarations>


#<main>

#first check if bzip2 can be run at all
if [ -x /usr/bin/bznew ]
then

	#1. Test: recompress testfile to bzip2-format
	cp $TESTFILE ${TMPDIR}/
	echo "Starting re-compression of testfile .."
	( bznew ${TMPDIR}/* && ls -l ${TMPDIR}/*.bz2 1>/dev/null ) || FAILED="1"
	test -e ${TMPDIR}/*.gz && echo "WARNING: old .gz-file was not removed" >&2
	rm -fr $TMPDIR
	
	#OVERALL-RESULT
	if [ $FAILED -ne 0 ]
	then
		echo "FAILED: qa_bzip2_bznew.sh failed" >&2
		exit 1;
	else
		echo "PASSED: qa_bzip2_bznew.sh passed :)"
		exit 0;
	fi


else
	if [ "${VERSION//\.}" -ge 103 ]
	then 
		echo "FAILED: ERROR: bznew could not be found." >&2 ;
		exit 1;
	else
		echo "NOTE: qa_bzip2_bznew.sh cannot be run as bznew is not included in versions older than 1.0.3";
		exit 0;
	fi
fi


#</main>
