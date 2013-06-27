#!/bin/sh
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

#
# this test is just a simple wrapper. It needs to be run before all other
# tests are executed, because they expect that the users 

source libqainternal.lib.sh

# the first param is the optional path to the root directory of tests
if [ "$1x" == "x" ]; then
    TEST_ROOT="."
else
    TEST_ROOT=$1
fi

. $TEST_ROOT/config

function test01() {
    if [ "$LOCAL_MODE" = "yes" ]; then
        if id "$TESTUSER" > /dev/null; then
            delUser "$TESTUSER"
        fi;

        if ! addUser "$TESTUSER"; then
            printMessage $MSG_ERROR "Unable to create testuser"
            return $FAILED
        fi;

        if stopService "postfix"; then
            printMessage $MSG_PASSED "Postfix - stop the service"
        else
            printMessage $MSG_FAILED "Postfix - stop the service"
            return $FAILED
        fi;

        # Stop cyrus daemon
        if stopService "cyrus"; then
            printMessage $MSG_PASSED "Cyrus - stop the service"
        else
            printMessage $MSG_FAILED "Cyrus - stop the service"
            return $FAILED
        fi

        # Cyrus and postfix configuration
        [ -f /etc/imapd.conf ] && mv /etc/imapd.conf /etc/imapd.conf.old
        [ -f /etc/cyrus.conf ] && mv /etc/cyrus.conf /etc/cyrus.conf.old
        [ -f /etc/postfix/main.cf ] && mv /etc/postfix/main.cf /etc/postfix/main.cf.old

        cp $TEST_ROOT/imapd.conf /etc/imapd.conf
        cp $TEST_ROOT/cyrus.conf /etc/cyrus.conf
        cp $TEST_ROOT/main.cf /etc/postfix/main.cf

        # Copy server SSL certificate to temporary location
        cp $TEST_ROOT/certs/imapd.pem /tmp/imapd.pem
        chown cyrus /tmp/imapd.pem
        chmod 600 /tmp/imapd.pem
        
        # Backup /etc/sasldb2 (if exists)
        [ -f /etc/sasldb2 ] && mv /etc/sasldb2 /etc/sasldb2.old

        # create password for cyrus administrator
        echo "cyrus" | saslpasswd2 cyrus

        # /etc/sasldb2 must be readable by cyrus server
        chown cyrus /etc/sasldb2

        if startService "cyrus"; then
            printMessage $MSG_PASSED "Cyrus - start the service"
        else
            printMessage $MSG_FAILED "Cyrus - start the service"
            return $FAILED
        fi

        # create mailbox for user 'receiver' with passwd 'receiver' (this needs cyrus to be running, so give cyrus some time to start)
        sleep 3
        echo $RECEIVER_PASSWORD | saslpasswd2 receiver
        echo "createmailbox user.$RECEIVING_USER" | cyradm --user cyrus --auth login --pass cyrus localhost
        echo ""

        if startService "postfix"; then
            printMessage $MSG_PASSED "Postfix - start the service"
        else
            printMessage $MSG_FAILED "Postfix - start the service"
            return $FAILED
        fi
    fi
    return $PASSED
}

test01
exit $?

