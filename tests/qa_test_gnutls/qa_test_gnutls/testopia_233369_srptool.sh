#!/bin/bash
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

# Figure out where my stuff resides
QA_GNUTLS_PATH=`dirname "$0"`
if [ "$QA_GNUTLS_PATH" == "${QA_GNUTLS_PATH#/}" ] ; then
	QA_GNUTLS_PATH="$PWD/$QA_GNUTLS_PATH"
	MYSELF="$QA_GNUTLS_PATH/$myname"
fi
## increasingly desperate fallbacks if things go weirdly wrong
if ! [ -f "$MYSELF" -a -x "$MYSELF" ] ; then
	MY_RPM="$(rpm -q "$0")" 2>/dev/null
	MYSELF="$(rpm -ql "$MY_RPM" | grep "/$myname\$")"
	QA_GNUTLS_PATH=`dirname "$MYSELF"`
fi
if ! [ -f "$MYSELF" -a -x "$MYSELF" ] ; then
	MYSELF="$(type -p "$myname")"
	QA_GNUTLS_PATH=`dirname "$MYSELF"`
fi
if ! [ -f "$MYSELF" -a -x "$MYSELF" ] ; then
	QA_GNUTLS_PATH=/usr/share/qa/qa_test_gnutls
	MYSELF="$QA_GNUTLS_PATH/$myname"
fi
if ! [ -f "$MYSELF" -a -x "$MYSELF" ] ; then
	QA_GNUTLS_PATH=/usr/share/qa/qa_gnutls
	MYSELF="$QA_GNUTLS_PATH/$myname"
fi
if ! [ -f "$MYSELF" -a -x "$MYSELF" ] ; then
	echo "$myname: ERROR: unable to figure out the directory I'm residing in. Giving up..."
	exit "$RC_IntErr"
fi

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

