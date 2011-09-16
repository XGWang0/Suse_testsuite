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
    sendmail -q 

    if ! delUser "$TESTUSER"; then
        printMessage $MSG_WARN "Unable to delete user"
    fi
 
    if ! removeConfig $ORIGINAL_CONFIG; then
        printMessage $MSG_WARN "Unable to remove the config file"
    fi

    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
    fi
}

function test01() {
    printMessage $MSG_INFO "Test #1: basic postcat(1) functionality"

    SUBJECT="Testing e-mail0011"
    TEXTMESSAGE="test email0011 yadda yadda yadda ######"
    sendmail -q
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTUSER@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while 
    sleep $SLEEP_TIME

    # there should be something in the deferred queue
    if ! postcat `find "$QUEUE_DIRECTORY/deferred" -type f` | 
      grep "^Subject: $SUBJECT"; then

        printMessage $MSG_FAILED "postcat failed"    
        return $FAILED
    fi
    
    sendmail -q
   
    printMessage $MSG_PASSED "postcat"    
    return $PASSED
}

function test02() {
    printMessage $MSG_INFO "Test #1: postcat(1) -q functionality"

    SUBJECT="Testing e-mail0011b"
    TEXTMESSAGE="test email0011b yadda yadda yadda ######"
    sendmail -q
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTUSER@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while 
    sleep $SLEEP_TIME

    for i in `find "$QUEUE_DIRECTORY/deferred" -type f | xargs basename`; do 
        if ! postcat -q $i > /dev/null; then
            printMessage $MSG_FAILED "postcat -q failed"    
            return $FAILED
        fi
    done

    sendmail -q
    printMessage $MSG_PASSED "postcat -q"    
    return $PASSED
}

function test03() {
    printMessage $MSG_INFO "Test #1: postcat(1) -o functionality"

    SUBJECT="Testing e-mail0011c"
    TEXTMESSAGE="test email0011c yadda yadda yadda ######"
    sendmail -q
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTUSER@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while 
    sleep $SLEEP_TIME

    # there should be something in the deferred queue
    if ! postcat -o `find "$QUEUE_DIRECTORY/deferred" -type f` | 
      egrep "^[[:space:]]{1,}[0-9]{1,}[[:space:]]{1,}Subject: $SUBJECT" > /dev/null; then

        printMessage $MSG_FAILED "postcat -o"    
        return $FAILED
    fi
    
    sendmail -q
   
    printMessage $MSG_PASSED "postcat"    
    return $PASSED
}

init
test01 || RESULT=$?
test02 || RESULT=$?
test03 || RESULT=$?

exit $RESULT
