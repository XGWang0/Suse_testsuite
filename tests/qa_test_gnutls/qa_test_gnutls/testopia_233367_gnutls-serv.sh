#!/bin/bash
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

QA_GNUTLS_PATH=/usr/share/qa/qa_test_gnutls

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
