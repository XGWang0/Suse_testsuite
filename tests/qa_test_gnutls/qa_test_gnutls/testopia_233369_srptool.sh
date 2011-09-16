#!/bin/bash
#
#  TESTOPIA testcase 233369 for pkg: gnutls
#  https://bugzilla.novell.com/tr_show_case.cgi?case_id=233369
#  Covered by the "-s" option of the testcase 233364 script
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

# product detection
product="not SLES-9 or SLE-10 family"
product_txt=""
SRPTOOL=""
if type -p SPident >/dev/null 2>&1 ; then
	[ x$QUIET != xyes ] && echo "Checking installed product (SPident...)"
	product_txt="$(SPident | grep '\<found\>')"
	case "$product_txt" in
		*SLES-9*)
			product="SLES-9 family" ; SRPTOOL="gnutls-srpcrypt"	;;
		*SLE-10*)
			product="SLE-10 family" ; SRPTOOL="srptool"		;;
	esac
else
	[ x$QUIET != xyes ] && echo "Checking installed product (/etc/SuSE-release...)"
	product_txt="$(head -n 1 /etc/SuSE-release)"
	case "$product_txt" in
		SUSE\ LINUX\ Enterprise\ *\ 9*)
			product="SLES-9 family" ; SRPTOOL="gnutls-srpcrypt"	;;
		SUSE\ Linux\ Enterprise\ *\ 10*)
			product="SLE-10 family" ; SRPTOOL="srptool"		;;
	esac
fi
echo "Detected product: $product"
# END product detection
if [ -z "$SRPTOOL" ] ; then
	echo "Product does not contain an srptool equivalent. SKIPPING test."
	exit $RC_SKIP
fi

if [ -f "$MASTERSCRIPT" -a -x "$MASTERSCRIPT" ] ; then
	echo "\
===================================================================
TESTOPIA testcase 233369: (SLE-10)  srptool test 
                          (SLES-9)  gnutls-srpcrypt test
===================================================================

WARNING: this testcase is for __interactive__ use only.
         Reason: /dev/tty is utilized for the password dialogues.
         Do not try to run it from within ctcs2: it will hang indefinitely
         and eventually fail.
         Instead, execute the following command interactively:

    $MASTERSCRIPT -s

         SKIPPING this testcase now.
" 
	exit $RC_SKIP
else
	echo "$myname: $MASTERSCRIPT: needed executable not found. Aborting..."
	exit $RC_IntErr
fi
