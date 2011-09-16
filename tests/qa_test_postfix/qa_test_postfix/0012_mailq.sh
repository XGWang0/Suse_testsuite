#!/bin/bash

source libqainternal.lib.sh

RESULT=$PASSED
CONFIG="conf/0011.conf"
ORIGINAL_CONFIG="/etc/postfix/main.cf"
TESTUSER=testmail01
SPOOLDIR="/tmp/spool/mail"
QUEUE_DIRECTORY="/var/spool/postfix"

SLEEP_TIME=${SLEEP_TIME:-10}

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

    rm -f $SPOOLDIR/$TESTUSER
}

function cleanup() {

    if ! delUser "$TESTUSER"; then
        printMessage $MSG_WARN "Unable to delete user"
    fi
 
    if ! removeConfig $ORIGINAL_CONFIG; then
        printMessage $MSG_WARN "Unable to remove the config file"
    fi

    rm -f $SPOOLDIR/$TESTUSER
    
    sendmail -q 

    sleep $SLEEP_TIME

    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
    fi

}

function test01() {
    printMessage $MSG_INFO "Test #1: basic mailq(1) functionality"

    SUBJECT="Testing e-mail0012"
    TEXTMESSAGE="test email0012 yadda yadda yadda ######"
    sendmail -q
    for i in {a..z}; do 
        if ! echo "${TEXTMESSAGE}$i" | mail -s "${SUBJECT}$i" "$TESTUSER@localhost"; then
            printMessage $MSG_FAILED "Sending mail"
            return $FAILED
        fi
    done

    #sleep for a while 
    sleep $SLEEP_TIME

    # there should be something in the deferred queue. Get the IDs and check
    # with mailq
    find "$QUEUE_DIRECTORY/deferred" -type f | while read ID; do
        ID=`basename $ID`
        if ! mailq | grep $ID > /dev/null; then
            printMessage $MSG_FAILED "mailq (ID: $ID not found)"    
            return $FAILED
        fi
    done

    printMessage $MSG_PASSED "mailq"    
    return $PASSED
}

init
test01 || RESULT=$?

exit $RESULT
