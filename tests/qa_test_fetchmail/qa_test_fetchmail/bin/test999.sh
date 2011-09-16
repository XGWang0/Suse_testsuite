#!/bin/sh
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
