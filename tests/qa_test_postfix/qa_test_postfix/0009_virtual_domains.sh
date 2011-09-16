#!/bin/bash

source libqainternal.lib.sh

TESTUSER=testmail01
TESTALIAS="test@test-host.site"
RESULT=$ERROR
CONFIG="conf/0009.conf"
ORIGINAL_CONFIG="/etc/postfix/main.cf"
VIRTUAL="conf/0009.virtual"
ORIGINAL_VIRTUAL="/etc/postfix/virtual"
SLEEP_TIME=${SLEEP_TIME:-5}


SPOOLDIR="/var/spool/mail"

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

    if ! copyConfig $VIRTUAL $ORIGINAL_VIRTUAL; then
        printMessage $MSG_ERROR "Unable to copy aliases file"
        exit $FAILED
    fi

    if ! postmap "$ORIGINAL_VIRTUAL"; then
        printMessage $MSG_ERROR "Unable to execute postmap \"$ORIGINAL_VIRTUAL\""
        exit $FAILED
    fi

    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
        exit $FAILED
    fi

    rm -f $SPOOLDIR/$TESTUSER
}

function cleanup() {
    if ! delUser "$TESTUSER"; then
        printMessage $MSG_WARN "Unable to delete user"
    fi
 
    if ! removeConfig $ORIGINAL_CONFIG; then
        printMessage $MSG_WARN "Unable to remove the config file"
    fi

    if ! removeConfig $ORIGINAL_VIRTUAL; then
        printMessage $MSG_ERROR "Unable to copy aliases file"
    fi

    if ! postmap "$ORIGINAL_VIRTUAL"; then
         printMessage $MSG_ERROR "Unable to execute newaliases"
    fi

    rm -f $SPOOLDIR/$TESTUSER
    
    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
    fi
}

function test01() {
    echo "Test #1: Testing the virtual alias domains mechanism (/etc/postfix/virtual)"

    SUBJECT="Testing e-mail0009"
    TEXTMESSAGE="test email0009 yadda yadda yadda ######"
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTALIAS"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while so the mail will be delivered
    sleep $SLEEP_TIME

    if grep "^Subject: $SUBJECT" $SPOOLDIR/$TESTUSER > /dev/null &&
       grep "$TEXTMESSAGE" $SPOOLDIR/$TESTUSER > /dev/null; then
    
        printMessage $MSG_PASSED "Sending mail (to virtual domain alias)"    
        return $PASSED
    else
         printMessage $MSG_FAILED "Sending mail (to virtual domain alias)"    
    fi

    return $FAILED
}


init
test01
RESULT=$?

exit $RESULT
