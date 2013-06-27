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
#    DESCRIPTION: "trivial compile-test against included bzlib.h"
#   REQUIREMENTS: "needs bzip2 and gcc"
#          USAGE: ./qa_bzip2_compile.sh
#
#===============================================================================
 
#<Declarations>
TESTBASEDIR="/usr/share/qa/qa_test_bzip2";
TESTDATADIR="/usr/share/qa/qa_test_bzip2/data";
TESTFILE="${TESTDATADIR}/tocompile/trivial.c";
TMPDIR="$(mktemp -d)";
FAILED="0";
#</Declarations>


#<main>

#first check if bzip2 can be run at all
if ( bzip2 -h &>/dev/null && gcc --help &>/dev/null )
then

	#1. Test: try to compile trivial.c and run it
	cp $TESTFILE ${TMPDIR}/
	echo "Start compiling.."
	( gcc -o ${TMPDIR}/trivial -lbz2 ${TMPDIR}/trivial.c && ls -l ${TMPDIR}/trivial 1>/dev/null ) || FAILED="1"
	${TMPDIR}/trivial || FAILED="1"
	rm -fr $TMPDIR
	
	#OVERALL-RESULT
	if [ $FAILED -ne 0 ]
	then
		echo "FAILED: qa_bzip2_compile.sh failed" >&2
		exit 1;
	else
		echo "PASSED: qa_bzip2_compile.sh passed :)"
		exit 0;
	fi


else
	echo "FAILED: ERROR: bzip2 and gcc need to be installed." >&2 ;
	exit 1;
fi


#</main>

