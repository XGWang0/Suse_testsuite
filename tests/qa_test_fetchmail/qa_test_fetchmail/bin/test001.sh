#!/bin/bash
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
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

function usage() {
cat <<EOF
usage: $1 [options]
    Options are as follows:
    -t      test root directory
    -p      protocols to test (pop3/imap/...)
    -h      help 
    -s      use ssl
    -w      host to send the e-mail to/flush the e-mail from
    -r      user to send the e-mail to/flush the e-mail from
    -l      limit for the message (in octets)
EOF

exit 2 
}

PROTO="POP3"
TEST_ROOT="."
USE_SSL=""
LIMIT=""
FAILED=0
EXPECT_FAILURE=0

while getopts "t:hp:sl:w:r:f" Option
do
  case $Option in
    #ROOT DIRECTORY OF THE TEST
    t     ) TEST_ROOT="$OPTARG";;
    #PROTOCOL TO TEST (pop3 by default)
    p     ) PROTO="$OPTARG";;
    #help
    h     ) usage;;
    #use ssl for fetching the mail
    s     ) USE_SSL="ssl";;
    #limit for the message
    l     ) LIMIT="limit $OPTARG";;
    #host to flush/send message from
    w     ) HOST="$OPTARG";;
    #user I will send e-mail to/fetch e-mail from
    r     ) RECEIVING_USER=$OPTARG;;
    #expect that the message will not be flushed by fetchmail
    f     ) EXPECT_FAILURE=1;;
    *     ) usage;;
  esac
done

. $TEST_ROOT/config

# just get the e-mail of the receiver
RECEIVER="$RECEIVING_USER@$HOST"
FETCHMAILRC="/tmp/fetchmailrc001"

# where to store downloaded mail
TESTUSERMAIL="/tmp/testusermail"

# prepare fetchmailrc
cat > "$FETCHMAILRC" <<EOF
poll $HOST with proto $PROTO and options 
    user "$RECEIVING_USER" with password "$RECEIVER_PASSWORD" is
    "$TESTUSER" here $USE_SSL $LIMIT
    mda cat
EOF
#disable TLS negotiation (fetchmail(1), --sslproto)
[ -z $USE_SSL ] && echo "    sslproto ''" >> "$FETCHMAILRC"
#fetchmail requires fetchmailrc to have 0710 at most
chmod 0710 "$FETCHMAILRC"


if [ "$LOCAL_MODE" = "yes" ]; then
    #first delete all e-mail in $RECEIVERs mailbox (on the server)
    #the simplest way to do this is to fetch all mails with fetchmail
    #and send them directly to /dev/null
    echo "Deleting e-mails from mailbox $RECEIVING_USER@$HOST: "
    $FETCHMAIL -as -f $FETCHMAILRC > /dev/null
    echo "Done"
fi

if [ "$EXPECT_FAILURE" = "1" ]; then
    echo "NOTE: the fetchmail is expected NOT to flush the message";
fi


echo "using the following fetchmailrc: "
echo "-----------------cut here---------------"
cat $FETCHMAILRC
echo "-----------------cut here---------------"

#send test e-mail
SUBJECT="test001.$PROTO.$$.$USE_SSL.$LIMIT"
echo -n "Sending e-mail to $RECEIVER: "
echo "$SUBJECT" | mail -s "$SUBJECT" -r "$TESTUSER" "$RECEIVER"

# let give the MTA some time to process the e-mail
sleep $SLEEPTIME
echo "Done"

#fetch the e-mail using protocol
echo -n "Fetching mail from $RECEIVER ($PROTO $USE_SSL): "

CORRECT_EXIT=0
rm -rf "$TESTUSERMAIL"
$FETCHMAIL -s -f "$FETCHMAILRC" > "$TESTUSERMAIL" && CORRECT_EXIT=1

if [ "$EXPECT_FAILURE" = "0" ] && [ $CORRECT_EXIT = "0" ]; then
    FAILED=1
    echo "FAILED: fetchmail expected to return 0 exit code"
elif [ "$EXPECT_FAILURE" = "1" ] && [ $CORRECT_EXIT = "1" ]; then
    FAILED=1
    echo "FAILED: fetchmail expected to return non-zero exit code"
fi   

echo "Done"

#check if the mail was fetched
MAIL_FETCHED=0
if grep -i "^Subject: $SUBJECT" "$TESTUSERMAIL"; then
    MAIL_FETCHED=1
fi

if [ "$EXPECT_FAILURE" = "0" ] && [ $MAIL_FETCHED = "1" ]; then
    echo $PROTO $USE_SSL PASSED 
elif [ "$EXPECT_FAILURE" = "1" ] && [ $MAIL_FETCHED = "0" ]; then
    echo $PROTO $USE_SSL PASSED 
else
    echo $PROTO $USE_SSL FAILED
    FAILED=1
fi


if [ "$FAILED" = "1" ]; then
    exit 1
else
    exit 0
fi


