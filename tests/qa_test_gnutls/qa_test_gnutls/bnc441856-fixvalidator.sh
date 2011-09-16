#!/bin/bash

# Testcase for bnc#441856 (gnutls vulnerability CVE-2008-4989)
#
# Documentation:
# https://wiki.innerweb.novell.com/index.php/RD-OPS_QA/HowTos/README.autotest-creation

# The ctcs2 exit codes as of 2010 (anything else is IntError)
RC_PASS=0
RC_FAIL=1
RC_IntErr_deprec=2
RC_IntErr=11
RC_SKIP=22

PRODUCT_INST="$(grep '^SUSE Linux' /etc/SuSE-release)"
case "$PRODUCT_INST" in
	SUSE\ Linux\ Enterprise*\ 11\ * )
		PKGS_UNDER_TEST="gnutls libgnutls26" ;;
	SUSE\ Linux\ Enterprise*\ 10\ * )
		PKGS_UNDER_TEST="gnutls" ;;
	* )
		PKGS_UNDER_TEST="gnutls" ;;
esac

export LANG=C
myname="$(basename "$0")"
timestamp="$(date '+%y%m%d.%H%M')"

function die() {
	local exitcode="$1" ; shift
	local reason="$1"
	echo -e "$myname: $reason\n\nAborting (exitcode: $exitcode)..." >&2
	exit "$exitcode"
}

# Check presence of package(s) to test
echo "Check: GNU TLS package(s) installed?"
rpm -q $PKGS_UNDER_TEST && echo || die $RC_IntErr "ERROR: Some NEEDED packages to test are not installed."


# Find my auxiliary data
#
DATAFILES="chain.pem server.key thawte.pem"
DATASUBD="data/bnc#441856"
DATAPARENTD="qa_test_gnutls"
DATAGRANDPAD="/usr/share/qa"
DATADIR_DFLT="$DATAGRANDPAD/$DATAPARENTD/$DATASUBD"

DATADIR_FOUND=""
# Look in some reasonable $PWD-dependent places...
for DATADIR in "$DATADIR_DFLT" "$DATASUBD" "../../share/qa/$DATAPARENTD/$DATASUBD" . ; do
	[ -d "$DATADIR" ] && { DATADIR_FOUND="yes" ; break ; }
done
# This never happens if "." is contained in the DATADIR candidates list, of course
[ -n "$DATADIR_FOUND" ] || die $RC_IntErr "Unable to find my data directory. Default location:\n\n   $DATADIR_DFLT"

for df in $DATAFILES; do
	# [ -f "$DATADIR"/"$df" ] || die $RC_IntErr "ERROR: Detected data dir: $DATADIR: File not found: $df"
	[ -f "$DATADIR"/"$df" ] || die $RC_IntErr "ERROR: Detected data dir: $DATADIR: File not found: $df\nDEBUG: $PWD"
done

# Temporarily prepare /etc/hosts
ETC_HOSTS_defines_server="$(grep  '^[^#]*\<server\>' /etc/hosts)"
if [ -n "$ETC_HOSTS_defines_server" ] ; then
	if echo "$ETC_HOSTS_defines_server" | \
	   grep -qv '^[[:space:]]*127\.0\.0\.1[[:space:]]*server[[:space:]]*$' ; then
		die $RC_IntErr "ERROR: /etc/hosts defines needed hostname \"server\" otherwise.\nNOT modifying it. Check"
	fi
	# OK, the "server" line(s) is as desired. Nothing to do.
	ETC_HOSTS_BAK=""	
else
	ETC_HOSTS_BAK="$(mktemp -q /etc/hosts.bak-$timestamp.XXXX)" || \
		die $RC_IntErr "ERROR: mktemp /etc/hosts.bak-* failed (missing access rights?)"
	cp -a /etc/hosts "$ETC_HOSTS_BAK"
	# Need to stick with name "server" since it must match the
	# 1st certificate of chain.pem
	echo "127.0.0.1       server" >> /etc/hosts
fi

# Launch server which features the broken "chain.pem" certificates chain.
# (penultimate cert. is _not_ signed with the last one, "thawte.pem").
#
echo "Launching gnutls server with broken x590certfile in the background. Cmd: 
gnutls-serv -q --http -p 4433 --x509keyfile $DATADIR/server.key --x509certfile $DATADIR/chain.pem &"
gnutls-serv -q --http -p 4433 --x509keyfile "$DATADIR"/server.key --x509certfile "$DATADIR"/chain.pem &
servpid="$!"
echo "Server's PID: $servpid"

sleep 1

EXITCODE=$RC_IntErr
killserver()
{
	echo
	if [ -n "$ETC_HOSTS_BAK" ] ; then
		echo "Restoring original /etc/hosts..."
		cp -af "$ETC_HOSTS_BAK" /etc/hosts && rm -f "$ETC_HOSTS_BAK"
	fi
	echo "Terminating the gnutls server..."
	kill "$servpid"
	echo "Terminating myself, too -- exiting"
	exit $EXITCODE

}

trap killserver EXIT

# Attempt to connect to malicious server
# (Client gets to know just the initial official thawte.pem certificate.)
#
echo "
Attempting to connect to gnutls server with bad x590certfile. Cmd: 
gnutls-cli --x509cafile $DATADIR/thawte.pem -p 4433 server"
GNUTLS_CLIENT_STDOUT="$(gnutls-cli --x509cafile "$DATADIR"/thawte.pem -p 4433 server < /dev/null)"
echo "
$GNUTLS_CLIENT_STDOUT"
if echo "$GNUTLS_CLIENT_STDOUT" | grep -q "Peer's certificate is NOT trusted"; then
	echo -e "\nBad server certificate properly refused: Testcase  passed"
	EXITCODE=$RC_PASS
else
	echo -e "\nBad server certificate accepted: gnutls vulnerable"
	echo "Testcase  FAILED"
	EXITCODE=$RC_FAIL
fi
# Actual exiting handled by trap handler killserver()
