#!/bin/bash

source libqainternal.lib.sh

TESTUSER=testmail01
RESULT=$ERROR
CONFIG="conf/0004.conf"
ORIGINAL_CONFIG="/etc/postfix/main.cf"
SLEEP_TIME=${SLEEP_TIME:-5}
trap "cleanup" 0

function init() {
    if ! addUser "$TESTUSER"; then
        printMessage $MSG_ERROR "Unable to create user"
        exit $FAILED
    fi

    if ! copyConfig $CONFIG $ORIGINAL_CONFIG; then
        printMessage $MSG_ERROR "Unable to copy config file"
        exit $FAILED
    fi

    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
        exit $FAILED
    fi
}

function cleanup() {
    if ! delUser "$TESTUSER"; then
        printMessage $MSG_WARN "Unable to delete user"
    fi
 
    if ! removeConfig $ORIGINAL_CONFIG; then
        printMessage $MSG_WARN "Unable to remove the config file"
    fi

    rm -f /var/spool/mail/$TESTUSER
    
    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
    fi
}

function test01() {
    echo "Test #1: Testing the basic mailing functionality"

    SUBJECT="Testing e-mail0004"
    TEXTMESSAGE="test email0004 yadda yadda yadda ######"
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTUSER@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while so the mail will be delivered
    sleep $SLEEP_TIME

    if grep "^Subject: $SUBJECT" /var/spool/mail/$TESTUSER  &&
       grep "$TEXTMESSAGE" /var/spool/mail/$TESTUSER; then
    
        printMessage $MSG_PASSED "Sending mail"    
        return $PASSED
    else
         printMessage $MSG_FAILED "Sending mail"    
    fi

    return $FAILED
}


init
test01
RESULT=$?

exit $RESULT
