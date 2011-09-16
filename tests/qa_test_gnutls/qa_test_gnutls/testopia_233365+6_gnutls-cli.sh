#!/bin/bash
#
#  TESTOPIA testcases 233365, 233366 for pkg: gnutls
#  https://bugzilla.novell.com/tr_show_case.cgi?case_id=233365 etc.
#  Covered by the "-g" option of the testcase 233364 script
#

# The ctcs2 exit codes as of 2010 (anything else is IntError)
RC_PASS=0
RC_FAIL=1
RC_IntErr=11
RC_SKIP=22

export LC_ALL=C

myname="$(basename "$0")"

QA_GNUTLS_PATH=/usr/share/qa/qa_test_gnutls
MASTERSCRIPT="$QA_GNUTLS_PATH"/testopia_233364.sh

if [ -f "$MASTERSCRIPT" -a -x "$MASTERSCRIPT" ] ; then
	exec "$MASTERSCRIPT" -g
else
	echo "$myname: $MASTERSCRIPT: needed executable not found. Aborting..."
	exit $RC_IntErr
fi
