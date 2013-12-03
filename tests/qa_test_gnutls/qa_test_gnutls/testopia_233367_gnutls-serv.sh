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
#  TESTOPIA testcase 233367 for pkg: gnutls
#  https://bugzilla.novell.com/tr_show_case.cgi?case_id=233367
#
#  Testcase description
#  ====================
#
# (taken from http://www.gnu.org/software/gnutls/manual/gnutls.html#Invoking-gnutls_002dserv)
# 
# gnutls-serv -p 666
# 
# #  you should see an output like this:
# 
# Echo Server ready. Listening to port '666'.
# 
# #  use telnet to connect to the server and produce some protocol errors ;)

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

starttime="$(date '+%s')"
function record_runtime {
        local invoked_at="$(date '+%s')"
        echo "Started at: $(date -d "@$starttime"). Finished at: $(date -d "@$invoked_at")"
        echo "Consumed runtime: $((invoked_at - starttime)) s"
}

echo "
==========================================
TESTOPIA testcase 233367: gnutls-serv test
==========================================

The original testcase operates a server by means of \"gnutls-serv -p 666\"

Within this package, however, gnutls-serv functionality testing is also
covered by the bnc441856 and bnc457938 testcases. See

    $QA_GNUTLS_PATH/bnc441856-fixvalidator.sh
    $QA_GNUTLS_PATH/bnc457938-fixvalidator.sh

Therefore, doing nothing more here and SKIPPING this testcase.
"

record_runtime
exit $RC_SKIP

