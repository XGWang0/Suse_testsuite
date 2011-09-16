#!/bin/bash
#
# Testcase for bnc#457938 (gnutls vulnerability CVE-2008-4989)
#

# Documentation:
# https://wiki.innerweb.novell.com/index.php/RD-OPS_QA/HowTos/README.autotest-creation

# The ctcs2 exit codes as of 2010 (anything else is IntError)
RC_PASS=0
RC_FAIL=1
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
DATAFILES="selfsigned.pem server.key"
DATASUBD="data/bnc#457938"
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
	[ -f "$DATADIR"/"$df" ] || die $RC_IntErr "ERROR: Detected data dir: $DATADIR: File not found: $df"
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
		die $RC_IntErr "ERROR: mktemp /etc/hosts.bak-* failed (missing rights?)"
	cp -a /etc/hosts "$ETC_HOSTS_BAK"
	# Need to stick with name "server" since it must match the
	# certificate of selfsigned.pem
	echo "127.0.0.1       server" >> /etc/hosts
fi

# certificate chain for the server: here just one self-signed certificate
#
echo "Launching gnutls server with just an unreliable self-signed x590 certificate in the background. Cmd: 
gnutls-serv -q --http -p 4433 --x509keyfile $DATADIR/server.key --x509certfile $DATADIR/selfsigned.pem &"
gnutls-serv -q --http -p 4433 --x509keyfile "$DATADIR"/server.key --x509certfile "$DATADIR"/selfsigned.pem &
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

# Attempt to connect to server w/ self-signed unreliable certificate
# 
# Before the update (SLE-11: gnutls-2.4.1-24.15, SLE-10: gnutls-1.2.10-13.13),
# this should cause the client to SIGSEGV
#
# After the update, nothing bad should happen. See below
#
echo "
Attempting to connect to server w/ self-signed unreliable certificate. 
If affected by bnc#457938, the client may catch a SIGSEGV. Cmd:

gnutls-cli --x509cafile $DATADIR/selfsigned.pem -p 4433 server < /dev/null
"

gnutls-cli --x509cafile "$DATADIR"/selfsigned.pem -p 4433 server < /dev/null

exitcode_gnutlscli="$?"
if [ "$exitcode_gnutlscli" -eq 0 ] ; then
	echo -e "\nTestcase  PASSED:  gnutls-cli exit code: 0; nothing bad happened."
	EXITCODE=$RC_PASS
elif [ "$exitcode_gnutlscli" -eq 139 ] ; then
	echo -e "\nTestcase  FAILED:  gnutls-cli client caught SIGSEGV (bnc#457938?)"
	EXITCODE=$RC_FAIL
else
	echo -e "\nTestcase  FAILED:  gnutls-cli exit code: $exitcode_gnutlscli"
	EXITCODE=$RC_FAIL
fi
# Actual exiting handled by trap handler killserver()


##  Expected outputs
##  ================

##  Before update (gnutls-1.2.10-13.139): segfault
##  ----------------------------------------------

##  Resolving 'server'...
##  Connecting to '127.0.0.1:4433'...
##  - Successfully sent 0 certificate(s) to server.
##  - Certificate type: X.509
##   - Got a certificate list of 1 certificates.

##   - Certificate[0] info:
##   # The hostname in the certificate matches 'server'.
##   # valid since: Fri Apr 17 15:29:32 CEST 2009
##   # expires at: Wed Oct 14 15:29:36 CEST 2009
##   # fingerprint: 76:71:59:F6:20:02:D6:67:76:DC:92:87:E6:49:6A:53
##   # Subject's DN: C=DE,O=SUSE LINUX Products GmbH,OU=QA-Maintenance,L=NUE,ST=BY,CN=server,UID=bead2880-c299-4e94-8d16-fe7bd13a5a68,EMAIL=kgw@suse.de
##   # Issuer's DN: C=DE,O=SUSE LINUX Products GmbH,OU=QA-Maintenance,L=NUE,ST=BY,CN=server,UID=bead2880-c299-4e94-8d16-fe7bd13a5a68,EMAIL=kgw@suse.de

##  Segmentation fault


##  After update (gnutls-1.2.10-13.139): success
##  --------------------------------------------

##  Resolving 'server'...
##  Connecting to '127.0.0.1:4433'...
##  - Successfully sent 0 certificate(s) to server.
##  - Certificate type: X.509
##   - Got a certificate list of 1 certificates.

##   - Certificate[0] info:
##   # The hostname in the certificate matches 'server'.
##   # valid since: Fri Apr 17 15:29:32 CEST 2009
##   # expires at: Wed Oct 14 15:29:36 CEST 2009
##   # fingerprint: 76:71:59:F6:20:02:D6:67:76:DC:92:87:E6:49:6A:53
##   # Subject's DN: C=DE,O=SUSE LINUX Products GmbH,OU=QA-Maintenance,L=NUE,ST=BY,CN=server,UID=bead2880-c299-4e94-8d16-fe7bd13a5a68,EMAIL=kgw@suse.de
##   # Issuer's DN: C=DE,O=SUSE LINUX Products GmbH,OU=QA-Maintenance,L=NUE,ST=BY,CN=server,UID=bead2880-c299-4e94-8d16-fe7bd13a5a68,EMAIL=kgw@suse.de


##  - Peer's certificate is trusted
##  - Version: TLS 1.1
##  - Key Exchange: RSA
##  - Cipher: AES 128 CBC
##  - MAC: SHA
##  - Compression: DEFLATE
##  - Handshake was completed

##  - Simple Client Mode:
