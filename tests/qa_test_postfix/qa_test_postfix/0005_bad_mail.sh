#!/bin/bash

source libqainternal.lib.sh

TESTUSER=testmail01
RESULT=$ERROR
CONFIG="conf/0005.conf"
ORIGINAL_CONFIG="/etc/postfix/main.cf"
ALIASES="conf/0005.aliases"
ORIGINAL_ALIASES="/etc/aliases"

SLEEP_TIME=${SLEEP_TIME:-5}
trap "cleanup" 0

function init() {

    if ! copyConfig $CONFIG $ORIGINAL_CONFIG; then
        printMessage $MSG_ERROR "Unable to copy config file"
        exit $FAILED
    fi

    if ! copyConfig $ALIASES $ORIGINAL_ALIASES; then
        printMessage $MSG_ERROR "Unable to copy aliases file"
        exit $FAILED
    fi

    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
        exit $FAILED
    fi

    if ! newaliases; then
        printMessage $MSG_ERROR "Unable to execute newaliases"
        exit $FAILED
    fi

    rm -f /var/spool/mail/root
}

function cleanup() {
    if ! delUser "$TESTUSER"; then
        printMessage $MSG_WARN "Unable to delete user"
    fi
 
    if ! removeConfig $ORIGINAL_CONFIG; then
        printMessage $MSG_WARN "Unable to remove the config file"
    fi

    if ! removeConfig $ORIGINAL_ALIASES; then
        printMessage $MSG_ERROR "Unable to copy aliases file"
    fi

    if ! newaliases; then
         printMessage $MSG_ERROR "Unable to execute newaliases"
    fi

    rm -f /var/spool/mail/root

    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
    fi
}

function test01() {
    echo "Test #1: Sending e-mail to non-existent user"

    SUBJECT="Testing e-mail0005"
    TEXTMESSAGE="test email0005 yadda yadda yadda ######"
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTUSER@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while so the mail will be delivered
    sleep $SLEEP_TIME

    if grep "^Subject: Undelivered Mail Returned to Sender" /var/spool/mail/root > /dev/null &&
       grep "^Subject: $SUBJECT" /var/spool/mail/root > /dev/null &&
       grep "$TEXTMESSAGE" /var/spool/mail/root > /dev/null &&
       grep "unknown user: \"$TESTUSER\"" /var/log/mail > /dev/null
    then
    
        printMessage $MSG_PASSED "Sending mail"    
        return $PASSED
    else
         printMessage $MSG_FAILED "Sending mail"    
    fi

    return $FAILED
}

init
test01
exit $?
