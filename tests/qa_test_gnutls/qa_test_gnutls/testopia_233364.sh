#!/bin/bash
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
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


#  TESTOPIA testcase 233364 for pkg: gnutls
#  https://bugzilla.novell.com/tr_show_case.cgi?case_id=233364
#
#  Adapted from the original testcase script "http://w3.suse.de/~hvogel/gnutls.test"
#  by Hendrik Vogelsang <hvogel@suse.de>
#
#  $Id: testopia_233364.sh,v 2.5 2010/10/07 10:55:42 kgw Exp kgw $
#
# QA testcase documentation:
# https://wiki.innerweb.novell.com/index.php/RD-OPS_QA/HowTos/README.autotest-creation

# For use within the ctcs2 wrapper framework:
# The ctcs2 exit codes as of 2010 (anything else is IntError)
RC_PASS=0
RC_FAIL=1
RC_IntErr=11
RC_SKIP=22

source qa_test_gnutls-config

export LC_ALL=C
VERSION="2.5"
SCRIPTNAME=`basename $0`
USAGE="$SCRIPTNAME $VERSION

Usage: $SCRIPTNAME [OPTIONS]

This scripts implements TESTOPIA testcase #233364 for the gnutls package.
Options:

-h      display this help text
-q	quiet   [not implemented yet]
-c	certtool test               (TESTOPIA testcase #233368)
-g	gnutls-cli test             (TESTOPIA testcases #233365/#233366)
-s	srptool test [interactive]
        (only for SLE-10 and older;  TESTOPIA testcase #233369)
-a	test all
"

#defaults
QUIET=no
CERT=no
CLI=no
SRP=no

while getopts ":hqcgsa" Option
do
case "$Option" in
        h )
        echo -e "$USAGE"
        exit 0
        ;;
        q )
        QUIET=no
	echo "quiet not implemented yet" 
        ;;
        c )
        CERT=yes
        ;;
        g )
        CLI=yes
        ;;
        s )
        SRP=yes
        ;;
	a )
        SRP=yes; CLI=yes; CERT=yes
        ;;
        * )
        echo -e "$SCRIPTNAME : invalid option\nTry $SCRIPTNAME -h for more information."
        exit 1
esac
done
shift $(($OPTIND - 1))

starttime="$(date '+%s')"
function record_runtime {
	local invoked_at="$(date '+%s')"
	echo "Started at: $(date -d "@$starttime"). Finished at: $(date -d "@$invoked_at")"
	echo "Consumed runtime: $((invoked_at - starttime)) s"
}
# Handlers for ctcs2-typical signaled abortions (SIGINT in case of timeouts)
# Global variable $where_am_i is being maintained throughout the script
function SIGINThandler {
	echo -e "\nCaught SIGINT (ctcs2 timeout?) during $where_am_i"
	record_runtime
	exit $RC_IntErr
}
trap SIGINThandler INT

function SIGQUIThandler {
	echo -e "\nCaught SIGQUIT (from ctcs2?) during $where_am_i"
	record_runtime
	exit $RC_IntErr
}
trap SIGQUIThandler QUIT

function SIGTERMhandler {
	echo -e "\nCaught SIGTERM (from ctcs2?) during $where_am_i"
	record_runtime
	exit $RC_IntErr
}
trap SIGTERMhandler TERM

# not really supposed to be triggered
function SIGSEGVhandler {
	echo -e "\nAiee -- caught SIGSEGV during $where_am_i"
	record_runtime
	exit $RC_IntErr
}
trap SIGSEGVhandler SEGV

# output version
echo -n "GNUTLS: "
if ! rpm -q gnutls ; then
	echo "ERROR: Not installed: NEEDED package gnutls. Aborting..." >&2
	exit $RC_IntErr
fi

# Needed because of the varying names and (widely!) versions
# of the utilities under test
#
function detect_product {
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
[ x$QUIET != xyes ] && echo "Detected product: $product"
}
function tempdir_create {
if ! TEMPDIR=`mktemp -d -p /tmp gnutls-testXXXX` ; then
	echo "$SCRIPTNAME: unable to create TEMPDIR during $where_am_i. Aborting (IntErr)..."
	exit $RC_IntErr
fi
cd $TEMPDIR
export TEMPDIR
}

function tempdir_destroy {
rm $TEMPDIR/*
rmdir $TEMPDIR
}

function certtool_test_die {
	local what="$1"
	echo -e "\n\t$what failed. This should not happen!
	You find logs and used files in $TEMPDIR
        TESTOPIA Testcase 233368 (certtool) FAILED.\n"
	record_runtime
	exit $RC_FAIL
}

function certtool_test {
if [ "x$QUIET" != "xyes" ]; then
echo "
=================================================================
TESTOPIA testcase 233368: certtool test in $TEMPDIR
=================================================================
"
if [ "$product" == "SLES-9 family" ] ; then
	if ! rpm -q expect ; then
		echo "ERROR: Not installed: NEEDED package expect. Aborting..." >&2
		exit $RC_IntErr
	fi
	if [ "$(uname -m)" == x86_64 ] ; then
	echo -e "WARNING: the certtool test is known to FAIL on SLES-9 x86_64 (bnc#97443)\n"
		# exit $RC_IntErr
	fi
fi

echo "Testcase 233368: 1)  Trying to generate parameters for Diffie Hellman key exchange

certtool --generate-dh-params --outfile dh.pem"
fi
where_am_i="certtool test: step 1: generate Diffie Hellman params"
certtool --generate-dh-params --outfile dh.pem || certtool_test_die "Generation"

if [ x$QUIET != xyes ]; then
echo -e "\nTestcase 233368: 2)  Trying to generate parameters for the RSA-EXPORT key exchange
                 WARNING: command draws on /dev/random and may spend lots of waiting time

certtool --generate-privkey --bits 512 --outfile rsa.pem"
fi
where_am_i="certtool test: step 2: generate private RSA key"
certtool --generate-privkey --bits 512 --outfile rsa.pem || certtool_test_die "Generation"

if [ x$QUIET != xyes ]; then
echo -e "
Testcase 233368: 3)   Trying to create a self signed certificate
                      (non-interactively, from a template or via expect).
                 3a)  Preparation: trying to create a private key for signing purposes

certtool --generate-privkey --outfile ca-key.pem"
fi
where_am_i="certtool test: step 3: generate self signed certificate"
certtool --generate-privkey --outfile ca-key.pem || certtool_test_die "Creation"

# Notice: certtool v1.0.8 or older (SLES-9) does not feature the useful
#         --template option: one must proceed interactively instead
#         (i.e., utilize expect scripts).
#
certtool_version="$(certtool -v 2>&1)"
case "$certtool_version" in
	"certtool, version 1.0."* )
		certtool_is_old="y"
	;;
	* )	certtool_is_old=""
	;;
esac	# case "certtool version old"

if [ -n "$certtool_is_old" ] ; then
if [ "x$QUIET" != "xyes" ]; then
		echo -n "
                 3b)  Preparation: Detected OLD $certtool_version 
                      Creating expect script ca-cert.expect for interaction with old certtools... "
fi
cat << EOF >ca-cert.expect
#!/usr/bin/expect -f

spawn certtool --generate-self-signed --load-privkey ca-key.pem --outfile ca-cert.pem

expect {
	"Country name (2 chars): "						{ send "$country\n"
		exp_continue
	}
	"Organization name: "							{ send "$ca_organization\n"
		exp_continue
	}
	"Organizational unit name: "						{ send "$organizational_unit\n"
		exp_continue
	}
	"Locality name: "							{ send "$locality\n"
		exp_continue
	}
	"State or province name: "						{ send "$province_name\n"
		exp_continue
	}
	"Common name: "								{ send "TEST-CERT\n"
		exp_continue
	}
	"UID: "									{ send "nobody\n"
		exp_continue
	}
	"E-mail: "								{ send "none@none.org\n"
		exp_continue
	}
	"Enter the certificate's serial number (decimal): "			{ send "107\n"
		exp_continue
	}
	"certificate will expire in (days): "					{ send "60\n"
		exp_continue
	}
	"Does the certificate belong to an authority? (Y/N): "			{ send "N\n"
		exp_continue
	}
	"web server certificate? (Y/N): "					{ send "N\n"
		exp_continue
	}
	"Is this a TLS web client certificate? (Y/N): "				{ send "N\n"
		exp_continue
	}
	"Enter the e-mail of the subject of the certificate: "				{ send "subject@none.org\n"
		exp_continue
	}
	"Will the certificate be used for signing (required for TLS)? (Y/N):"		{ send "Y\n"
		exp_continue
	}
	"Will the certificate be used for encryption (not required for TLS)? (Y/N): "	{ send "N\n"
		exp_continue
	}
	"Enter the URI of the CRL distribution point: "				{ send "\n"
		exp_continue
	}
	"Is the above information ok? (Y/N): "					{ send "Y\n"
		exp_continue
	}
}
send_user "\ncerttool run finished -- check generated ca-cert.pem\n"
EOF
chmod +x ./ca-cert.expect
if [ x$QUIET != xyes ]; then
echo -e "done.
                 3c)  Now trying to create the self signed certificate\n"
fi
./ca-cert.expect || certtool_test_die "Creation"

else	# ! [ -n "$certtool_is_old" ]

if [ "x$QUIET" != "xyes" ]; then
echo -ne "\n                 3b)  Preparation: creating certificate template... "
fi
echo "#
## X.509 Certificate options
#
# DN options

# The organization of the subject.
organization = \"$ca_organization\"

# The organizational unit of the subject.
unit = \"$organizational_unit\"

# The locality of the subject.
locality = \"$locality\"

# The state of the certificate owner.
state = \"$province_name\"

# The country of the subject. Two letter code.
country = \"$country\"

# The common name of the certificate owner.
cn = \"TEST-CERT\"

# A user id of the certificate owner.
uid = \"nobody\"

# If the supported DN OIDs are not adequate you can set
# any OID here.
# For example set the X.520 Title and the X.520 Pseudonym
# by using OID and string pairs.
#dn_oid = \"2.5.4.12\" \"Dr.\" \"2.5.4.65\" \"jackal\"

# This is deprecated and should not be used in new
# certificates.
# pkcs9_email = \"none@none.org\"

# The serial number of the certificate
serial = \"007\"
     
# In how many days, counting from today, this certificate will expire.
expiration_days = \"60\"
     
# X.509 v3 extensions
     
# A dnsname in case of a WWW server.
#dns_name = \"www.none.org\"
     
# An IP address in case of a server.
#ip_address = \"192.168.1.1\"
     
# An email in case of a person
email = \"none@none.org\"
     
# An URL that has CRLs (certificate revocation lists)
# available. Needed in CA certificates.
#crl_dist_points = \"http://www.getcrl.crl/getcrl/\"
     
# Whether this is a CA certificate or not
#ca
     
# Whether this certificate will be used for a TLS client
#tls_www_client
     
# Whether this certificate will be used for a TLS server
#tls_www_server
     
# Whether this certificate will be used to sign data (needed
# in TLS DHE ciphersuites).
signing_key
     
# Whether this certificate will be used to encrypt data (needed
# in TLS RSA ciphersuites). Note that it is prefered to use different
# keys for encryption and signing.
#encryption_key
     
# Whether this key will be used to sign other certificates.
#cert_signing_key
     
# Whether this key will be used to sign CRLs.
#crl_signing_key
     
# Whether this key will be used to sign code.
#code_signing_key
     
# Whether this key will be used to sign OCSP data.
#ocsp_signing_key
     
# Whether this key will be used for time stamping.
#time_stamping_key" > template.cfg

if [ x$QUIET != xyes ]; then
echo "done.
                 3c)  Now trying to create the self signed certificate

certtool --generate-self-signed --load-privkey ca-key.pem \\
         --template template.cfg --outfile ca-cert.pem"
fi
certtool --generate-self-signed --load-privkey ca-key.pem \
         --template template.cfg --outfile ca-cert.pem \
     || certtool_test_die "Creation"

fi 	#  if [ -n "$certtool_is_old" ]
# Yes, old certtools would create zero-length certificates successfully (SLES-9 x86_64)
[ -s "ca-cert.pem" ] || certtool_test_die 'ca-cert.pem empty! Creation'

if [ x$QUIET != xyes ]; then
echo -e "
Testcase 233368: 4)   Trying to generate a PKCS #10 certificate request
                      (non-interactively, from a template or via expect).
                 4a)  Preparation:  trying to create another private key for signing purposes

certtool --generate-privkey --outfile request-key.pem"
fi
where_am_i="certtool test: step 4: generate PKCS #10 certificate request"
certtool --generate-privkey --outfile request-key.pem || certtool_test_die "Creation"

if [ -n "$certtool_is_old" ] ; then
if [ "x$QUIET" != "xyes" ]; then
echo -n "
                 4b)  Preparation: Creating expect script request.expect for interaction with old certtools... "
fi
cat << EOF >request.expect
#!/usr/bin/expect -f

spawn certtool --generate-request --load-privkey request-key.pem --outfile request.pem 

expect {
	"Country name (2 chars): "						{ send "$country\n"
		exp_continue
	}
	"Organization name: "							{ send "$request_organization\n"
		exp_continue
	}
	"Organizational unit name: "						{ send "QA\n"
		exp_continue
	}
	"Locality name: "							{ send "$locality\n"
		exp_continue
	}
	"State or province name: "						{ send "$province_name\n"
		exp_continue
	}
	"Common name: "								{ send "$request_common_name\n"
		exp_continue
	}
	"UID: "									{ send "qa_tester\n"
		exp_continue
	}
	"Enter a challenge password: "						{ send "$challenge_password\n"
		exp_continue
	}
	"Is the above information ok? (Y/N): "					{ send "Y\n"
		exp_continue
	}
}
send_user "\ncerttool run finished -- check generated request.pem\n"
EOF
chmod +x ./request.expect
if [ x$QUIET != xyes ]; then
echo -e "done.
                 4c)  Now trying to generate the signed PKCS #10 certificate request\n"
fi
./request.expect || certtool_test_die "Creation"

else	# ! [ -n "$certtool_is_old" ]

if [ "x$QUIET" != "xyes" ]; then
echo -ne "\n                 4b)  Preparation: Creating request template... "
fi
echo "#
## PKCS #10 certificate request options
#

# The country of the subject. Two letter code.
country = \"$country\"

# The organization of the subject.
organization = \"$request_organization\"

# The organizational unit of the subject.
unit = \"QA\"

# The locality of the subject.
locality = \"$locality\"

# The state of the certificate owner.
state = \"$province_name\"

# The common name of the certificate owner.
cn = \"$request_common_name\"

# A user id of the certificate owner.
#uid = "qa_tester"

# A challenge password for the request.
challenge_password = \"$challenge_password\"" > requesttempl.cfg

if [ x$QUIET != xyes ]; then
echo -e "done.
                 4c)  Now trying to generate the signed PKCS #10 certificate request:

certtool --generate-request --load-privkey request-key.pem \\
         --template requesttempl.cfg --outfile request.pem"
fi
certtool --generate-request --load-privkey request-key.pem \
         --template requesttempl.cfg --outfile request.pem \
    || certtool_test_die "Generation"

fi	# [ -n "$certtool_is_old" ]

if [ "x$QUIET" != "xyes" ]; then
echo -e "\nTestcase 233368: 5)   Trying to create a certificate for the just-generated request"
fi
where_am_i="certtool test: step 5: generate certificate upon request of step 4"
if [ -n "$certtool_is_old" ] ; then
if [ "x$QUIET" != "xyes" ]; then
echo -n "\
                 5a)  Preparation: Creating expect script reply_w_cert.expect
                      for interaction with old certtools... "
fi
cat << EOF >reply_w_cert.expect
#!/usr/bin/expect -f

spawn certtool --generate-certificate --load-request request.pem --outfile cert.pem --load-ca-certificate ca-cert.pem --load-ca-privkey ca-key.pem 

expect {
	"E-mail: "								{ send "none@none.org\n"
		exp_continue
	}
	"Enter the certificate's serial number (decimal): "			{ send "7\n"
		exp_continue
	}
	"certificate will expire in (days): "					{ send "365\n"
		exp_continue
	}
	"Does the certificate belong to an authority? (Y/N): "			{ send "N\n"
		exp_continue
	}
	"Is this a TLS web client certificate? (Y/N): "				{ send "N\n"
		exp_continue
	}
	"web server certificate? (Y/N): "					{ send "Y\n"
		exp_continue
	}
	"Enter the dnsName of the subject of the certificate: "			{ send "$ca_subject_dnsname\n"
		exp_continue
	}
	"Will the certificate be used for signing (DHE and RSA-EXPORT ciphersuites)? (Y/N): " { send "N\n"
		exp_continue
	}
	"Will the certificate be used for encryption (RSA ciphersuites)? (Y/N): "	{ send "Y\n"
		exp_continue
	}
	"Is the above information ok? (Y/N): "					{ send "Y\n"
		exp_continue
	}
}
send_user "\ncerttool run finished -- check generated cert.pem\n"
EOF
chmod +x ./reply_w_cert.expect
if [ x$QUIET != xyes ]; then
echo -e "done.
                 5b)  Now trying to create the requested certificate:\n"
fi
./reply_w_cert.expect || certtool_test_die "Creation"

else	# ! [ -n "$certtool_is_old" ]

if [ "x$QUIET" != "xyes" ]; then
echo -en  "                 5a)  Preparation: Creating certificate template for answer to request... "
fi
echo "#
## certificate options for PKCS #10 request reply
#

# Serial number of the certificate
serial = 7

# Validity period:
# In how many days, counting from today, this certificate will expire.
expiration_days = 365

# Does the certificate belong to an authority? (Y/N): N
# Whether this is a CA certificate or not
#ca

# Whether this certificate will be used for a TLS client
#tls_www_client

# Is this a web server certificate? (Y/N): Y
# Whether this certificate will be used for a TLS server
tls_www_server

# Will the certificate be used for signing (DHE and RSA-EXPORT ciphersuites)? (Y/N): N
# Whether this certificate will be used to sign data (needed
# in TLS DHE ciphersuites).
# signing_key

# Will the certificate be used for encryption (RSA ciphersuites)? (Y/N): Y
# Whether this certificate will be used to encrypt data (needed
# in TLS RSA ciphersuites). Note that it is prefered to use different
# keys for encryption and signing.
encryption_key

# Enter the dnsName of the subject of the certificate: gemini.suse.de
# A dnsname in case of a WWW server.
dns_name = \"$ca_subject_dnsname\"" >replytempl.cfg

if [ x$QUIET != xyes ]; then
echo -e "done.
                 5b)  Now trying to create the requested certificate

certtool --generate-certificate --load-request request.pem --outfile cert.pem \\
         --load-ca-certificate ca-cert.pem --load-ca-privkey ca-key.pem"
fi
certtool --generate-certificate --load-request request.pem --outfile cert.pem \
         --template replytempl.cfg --load-ca-certificate ca-cert.pem --load-ca-privkey ca-key.pem \
    || certtool_test_die "Creation"

fi 	# [ -n "$certtool_is_old" ]
# Yes, old certtools would create zero-length certificates successfully (SLES-9 x86_64)
[ -s "cert.pem" ] || certtool_test_die 'cert.pem empty! Creation'

if [ x$QUIET != xyes ]; then
echo -e "
Testcase 233368: 6)   Reporting certificate info about the just-generated new certificate

certtool --certificate-info --infile cert.pem"
fi
where_am_i="certtool test: step 6: report about certificate of step 5"
certtool --certificate-info --infile cert.pem || certtool_test_die "Report"

echo "
=========================================
certtool test successful
=========================================
"
}

function cli_test_die {
	local what="$1"
	echo -e "\n\t$what This should not happen!
	You find logs and used files in $TEMPDIR
        TESTOPIA Testcase 233365 (gnutls-cli) FAILED.\n"
	record_runtime
	exit $RC_FAIL
}

function cli_test {
# Reference: http://www.gnu.org/software/gnutls/manual/gnutls.html#Invoking-gnutls_002dcli
if [ x$QUIET != xyes ]; then
echo "
===================================================================
TESTOPIA testcase 233365: gnutls-cli test in $TEMPDIR
===================================================================
"
## Connection gnutls-cli www.gnutls.org -p 5555 does not work anymore
## as of Sep 2010
## DISABLED ##echo -e "Testcase 233365: Trying gnutls-cli on www.gnutls.org port 5555\n"
fi
## DISABLED ##{ echo "gnutls-cli www.gnutls.org -p 5555"
## DISABLED ##  gnutls-cli www.gnutls.org -p 5555
## DISABLED ##} | tee gnutls-cli.log1
## DISABLED ##grep -q "Got a certificate list of 0 certificates." gnutls-cli.log1 \
## DISABLED ##    || cli_test_die "No certificate found. "

if [ x$QUIET != xyes ]; then
echo -e "Testcase 233365: Trying gnutls-cli on TLS server $TLS_server\n"
fi
where_am_i="gnutls-cli test: step 1: gnutls-cli $TLS_server"
{ 
  echo "gnutls-cli $TLS_servere"
  ## FIXME: hopefully these waiting times are enough
  { sleep 6 ; echo "GET /" ; sleep 6 ; }  | gnutls-cli $TLS_server
} > gnutls-cli.log2 2>&1
cat gnutls-cli.log2
if grep -q "Got a certificate list of 1 certificates." gnutls-cli.log2
then
	echo "
=========================================
gnutls-cli test successful
=========================================
"
else
	cli_test_die "gnutls-cli FAILED on $TLS_server. "
fi


# Reference: http://www.gnu.org/software/gnutls/manual/gnutls.html#Invoking-gnutls_002dcli_002ddebug
if [ x$QUIET != xyes ]; then
echo "
=========================================================================
TESTOPIA testcase 233366: gnutls-cli-debug test in $TEMPDIR
=========================================================================
"
echo -e "Testcase 233366: Trying gnutls-cli-debug on TLS server $TLS_server\n"
fi
echo "gnutls-cli-debug $TLS_server"
where_am_i="gnutls-cli test: step 2: gnutls-cli-debug $TLS_server"
gnutls-cli-debug $TLS_server \
    || cli_test_die "gnutls-cli-debug FAILED on $TLS_server. "
echo "
=========================================
gnutls-cli-debug test successful
=========================================
"
}

function srptool_test_die {
	local what="$1"
	echo -e "\n\t$what failed. This should not happen!
	You find logs and used files in $TEMPDIR
        TESTOPIA Testcase 233369 (srptool) FAILED.\n"
	record_runtime
	exit $RC_FAIL
}

function srp_test {
if [ x$QUIET != xyes ]; then
echo "
===================================================================
TESTOPIA testcase 233369: (SLE-10)  srptool test 
                          (SLES-9)  gnutls-srpcrypt test
===================================================================

WARNING: this testcase is for __interactive__ use only.
         Reason: /dev/tty is utilized for the password dialogues.
         Trying to run it from within a wrapper will hang indefinitely
         and eventually fail.
"
fi
if [ "$SRPTOOL" ] ; then
	[ x$QUIET != xyes ] && echo "Testing:          $SRPTOOL"
else
	echo "Product does not contain a srptool equivalent. SKIPPING test."
	record_runtime
	exit $RC_SKIP
fi
if ! type -p "$SRPTOOL" >/dev/null 2>&1 ; then
	echo "$SCRIPTNAME: $SRPTOOL: command not found. Aborting (INTERNAL ERROR)..."
	record_runtime
	exit $RC_IntErr
fi

if [ x$QUIET != xyes ]; then	
	echo -e "Creating SRP password config file\n
$SRPTOOL --create-conf ./tpasswd.conf"
fi
where_am_i="srptool test: step 1: create SRP password config file tpasswd.conf"
"$SRPTOOL" --create-conf ./tpasswd.conf || srptool_test_die "Creation"
if [ x$QUIET != xyes ]; then	
	echo -e "\ncat ./tpasswd.conf"
	cat ./tpasswd.conf
fi

if [ x$QUIET != xyes ]; then	
	echo -e "Trying to set a password for user qa_tester (TTY INPUT NEEDED)\n
$SRPTOOL --passwd ./tpasswd --passwd-conf ./tpasswd.conf -u qa_tester"
fi
where_am_i="srptool test: step 2: create SRP password for user \"qa_tester\""
"$SRPTOOL" --passwd ./tpasswd --passwd-conf ./tpasswd.conf -u qa_tester \
    || srptool_test_die "Setting the password"

if [ x$QUIET != xyes ]; then
echo -e "Trying to verify the password of user qa_tester (TTY INPUT NEEDED)\n
$SRPTOOL --passwd ./tpasswd --passwd-conf ./tpasswd.conf --verify -u qa_tester"
fi
where_am_i="srptool test: step 3: verify SRP password for user \"qa_tester\""
"$SRPTOOL" --passwd ./tpasswd --passwd-conf ./tpasswd.conf --verify -u qa_tester \
    || srptool_test_die "Verifying the password"

echo "
=========================================
srptool test successful
=========================================
"
}

# do stuff

detect_product

do_some=""
if [ x$CERT == xyes ]; then
where_am_i="certtool test (start)"
starttime="$(date '+%s')"
do_some="yes"
tempdir_create
certtool_test
tempdir_destroy
record_runtime
fi

if [ x$CLI == xyes ]; then
where_am_i="gnutls-cli test (start)"
starttime="$(date '+%s')"
do_some="yes"
tempdir_create
cli_test
tempdir_destroy
record_runtime
fi

if [ x$SRP == xyes ]; then
where_am_i="srptool test (start)"
starttime="$(date '+%s')"
do_some="yes"
tempdir_create
srp_test
tempdir_destroy
record_runtime
fi

if [ -z "$do_some" ] ; then
	if [ "x$QUIET" != "xyes" ]; then
		echo "
======================================
TESTOPIA testcase 233364: gnutls tests
======================================

No action options provided: doing nothing.
$USAGE"
	fi
	record_runtime
	exit $RC_PASS
fi

