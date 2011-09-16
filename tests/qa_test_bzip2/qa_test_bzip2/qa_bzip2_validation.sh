#!/bin/bash
#===============================================================================
#
#                 SUSE/Novell confidential Testscript
#           Only for internal use, no distribution allowed
#
#
#
#           FILE: qa_bzip2_validation.sh
#        VERSION: 0.1
#         AUTHOR: Frank Seidel <fseidel@suse.de>
#       REVIEWER: 
#        LICENSE: unknown
#
#        CREATED: 2005-10-04
#        REVISED: 2005-10-04
#
#    DESCRIPTION: "compresses, decompr. and compares files with various settings"
#   REQUIREMENTS: "needs bzip2,mktemp"
#          USAGE: ./qa_bzip2_validation.sh
#
#===============================================================================
 
#<Declarations>
TESTBASEDIR="/usr/share/qa/qa_test_bzip2";
TESTDATADIR="/usr/share/qa/qa_test_bzip2/data";
FILESDIR="${TESTDATADIR}/topack";
TMPDIR="$(mktemp -d)";
FAILED="0";
#</Declarations>


#<main>

#first check if bzip2 can be run at all
if bzip2 -h &>/dev/null 
then

	#1. Test: compress files with default settings, decompress and compare

	cp -r $FILESDIR ${TMPDIR}/default;
	( bzip2 ${TMPDIR}/default/* && ls  ${TMPDIR}/default/*.bz2 1>/dev/null ) || FAILED="1";
	bzip2 -d ${TMPDIR}/default/* || FAILED="1";
	diff -r $FILESDIR ${TMPDIR}/default || FAILED="1";
	rm -fr ${TMPDIR}/default
	if [ $FAILED -eq 1 ]
	then
		echo "FAILED: Test #1 (default-settings) failed :(" >&2
	else
		echo "PASSED: Test #1 (default-settings) passed :)" 
	fi
	#---


	#2. Test: compress files with different blocksizes, decompress, compare

	COUNTER="1";
	while [ $COUNTER -le 9 ]
	do
		cp -r $FILESDIR ${TMPDIR}/blocksize-${COUNTER}
		( bzip2 -${COUNTER} ${TMPDIR}/blocksize-${COUNTER}/* && ls ${TMPDIR}/blocksize-${COUNTER}/*.bz2 1>/dev/null) || FAILED="2";
		bzip2 -d ${TMPDIR}/blocksize-${COUNTER}/* || FAILED="2";
		diff -r $FILESDIR ${TMPDIR}/blocksize-${COUNTER} || FAILED="2";
		rm -fr ${TMPDIR}/blocksize-${COUNTER}
		if [ $FAILED -eq 2 ]
		then
			echo "FAILED: Test #2 failed at blocksize ${COUNTER}00k :(" >&2
			break;
		else
			echo "PASSED: Test #2 passed (for blocksize ${COUNTER}00k) :)"
		fi

		COUNTER=$[COUNTER+1];
	done
	#---


	#3. Test: uses bzip2's integrity check (bzip2 --test)

	cp -r $FILESDIR ${TMPDIR}/integrity;
	( bzip2 ${TMPDIR}/integrity/* && ls ${TMPDIR}/integrity/*.bz2 1>/dev/null) || FAILED="3";
	bzip2 --test ${TMPDIR}/integrity/* || FAILED="3";
	rm -fr ${TMPDIR}/integrity
	if [ $FAILED -eq 3 ]
	then
		echo "FAILED: Test #3 (bzip2-integritycheck) failed :(" >&2
	else
		echo "PASSED: Test #3 (bzip2-integritycheck) passed :)" 
	fi
	#---



	#4. Test: check bzip2's keep (old files) setting

	cp -r $FILESDIR ${TMPDIR}/keep;
	( bzip2 --keep ${TMPDIR}/keep/* && ls ${TMPDIR}/keep/*.bz2 1>/dev/null ) || FAILED="4";
	for NEWFILE in ${TMPDIR}/keep/*.bz2
	do
		ORIG="${NEWFILE%.bz2}";
		BASEN="$(basename $ORIG)";
		(ls $ORIG 1>/dev/null && diff $ORIG ${FILESDIR}/$BASEN ) || FAILED="4";
	done
	rm -fr ${TMPDIR}/keep
	if [ $FAILED -eq 4 ]
	then
		echo "FAILED: Test #4 (keep-setting) failed :(" >&2
	else
		echo "PASSED: Test #4 (keep-setting) passed :)"
	fi
	#---

	
	

	#CLEANUP
	rm -fr $TMPDIR

	#OVERALL-RESULT
	if [ $FAILED -ne 0 ]
	then
		echo "FAILED: Overall-result of qa_bzip2_validation.sh is failed (last failed test was $FAILED)" >&2
		exit 1;
	else
		echo "PASSED: Overall-result of qa_bzip2_validation.sh is passed :)"
		exit 0;
	fi


else
	echo "FAILED: ERROR: bzip2 could not be called." >&2 ;
	exit 1;
fi


#</main>
