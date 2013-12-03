#!/bin/sh
# ****************************************************************************
# Copyright © 2013 Unpublished Work of SUSE, Inc. All Rights Reserved.
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
        if ! delUser "$TESTUSER"; then
            printMessage $MSG_WARN "Unable to delete user"
        fi;

        # Stop postfix service 
        if checkService "postfix"; then
            if stopService "postfix"; then
                printMessage $MSG_PASSED "Postfix - stop the service"
            else
                printMessage $MSG_FAILED "Postfix - stop the service"
            fi
        else
            printMessage $MSG_WARN "Postfix - stop the service: Postfix is not running."
        fi

        # Delete mailbox of receiving user
        echo "setacl user.$RECEIVING_USER cyrus c" | cyradm --user cyrus --auth login --pass cyrus localhost
        echo ""
        echo "deletemailbox user.$RECEIVING_USER" | cyradm --user cyrus --auth login --pass cyrus localhost
        echo ""

        # Stop cyrus service 
        if checkService "cyrus"; then
            if stopService "cyrus"; then
                printMessage $MSG_PASSED "Cyrus - stop the service"
            else
                printMessage $MSG_FAILED "Cyrus - stop the service"
            fi
        else
            printMessage $MSG_WARN "Cyrus - stop the service: Cyrus is not running."
        fi

        [ -f /etc/sasldb2.old ] && mv /etc/sasldb2.old /etc/sasldb2
        [ -f /tmp/imapd.pem ] && rm /tmp/imapd.pem

        # Restore postfix & cyrus config files
        [ -f /etc/imapd.conf.old ] && mv /etc/imapd.conf.old /etc/imapd.conf
        [ -f /etc/cyrus.conf.old ] && mv /etc/cyrus.conf.old /etc/cyrus.conf
        [ -f /etc/postfix/main.cf.old ] && mv /etc/postfix/main.cf.old /etc/postfix/main.cf

    fi    
    return $PASSED
}

test01
exit $?

