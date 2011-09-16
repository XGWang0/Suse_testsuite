#!/bin/bash

source libqainternal.lib.sh

# message_size_limit = 20480
# mailbox_size_limit = 40900
# mail_spool_directory = /tmp

MAILBOX_SIZE_LIMIT=40900

TESTUSER=testmail01
RESULT=$ERROR
CONFIG="conf/0006.conf"
ORIGINAL_CONFIG="/etc/postfix/main.cf"
ATTACHMENT=`mktemp`
SPOOLDIR=/tmp/qa
SLEEP_TIME=${SLEEP_TIME:-10}


trap "cleanup" 0

function init() {

    if ! test -d $SPOOLDIR; then
        if ! mkdir -p $SPOOLDIR; then 
            printMessage $MSG_ERROR "Unable to create spool directory $SPOOLDIR"
            exit $FAILED
        fi
    fi
    
    if ! addUser "$TESTUSER"; then
        printMessage $MSG_ERROR "Unable to create user"
        exit $FAILED
    fi

    if ! copyConfig $CONFIG $ORIGINAL_CONFIG; then
        printMessage $MSG_ERROR "Unable to copy config file"
        exit $FAILED
    fi

    if ! reloadService "postfix" > /dev/null; then
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

    rm -rf $SPOOLDIR
    rm -f "$ATTACHMENT"
    
    if ! reloadService "postfix" > /dev/null; then
        printMessage $MSG_ERROR "Reload of postfix failed."
    fi
}

function test01() {
    echo "Test #1: Send mail with attachment"
    
    SUBJECT="Testing e-mail0006 with attachment"
    TEXTMESSAGE="Attached the testing e-mail0006"
    dd bs=1024 count=10 if=/dev/urandom of=$ATTACHMENT 2> /dev/null
    ATTACHMENT_BASE=`basename $ATTACHMENT`
    md5sum $ATTACHMENT | sed "s,$ATTACHMENT,$ATTACHMENT_BASE," > $ATTACHMENT.md5
    if ! echo "$TEXTMESSAGE" | mail -a $ATTACHMENT -s "$SUBJECT" "$TESTUSER@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while so the mail will be delivered
    sleep $SLEEP_TIME

    RESULT=$PASSED
    if ! grep "^Subject: $SUBJECT" $SPOOLDIR/$TESTUSER > /dev/null; then
        RESULT=$FAILED
        printMessage $MSG_ERROR "testing subject not found in the message"
    fi
    
    if ! grep "$TEXTMESSAGE" $SPOOLDIR/$TESTUSER > /dev/null ; then
        RESULT=$FAILED
        printMessage $MSG_ERROR "testing message not found in the message"
    fi
    
    if ! echo w 1 | mail -f $SPOOLDIR/$TESTUSER > /dev/null; then
        RESULT=$FAILED
        printMessage $MSG_ERROR "Unable to save the attachment"
    fi
    
    if ! md5sum --status -c $ATTACHMENT.md5  ; then
        RESULT=$FAILED
        printMessage $MSG_ERROR "md5sum of the attachment is incorrect"
    fi
    rm -f $ATTACHMENT_BASE 1

   
    if [ "$RESULT" = "$FAILED" ]; then
        printMessage $MSG_FAILED "Sending mail with attachment"    
    else
        printMessage $MSG_PASSED "Sending mail with attachment"    
    fi

    return $RESULT
}



function test02() 
{
    echo "Test #2: Send mail with attachment too big to fit into message_size_limit"
    
    SUBJECT="Testing e-mail0006b with attachment"
    TEXTMESSAGE="Attached the testing e-mail0006b"
    dd bs=1024 count=30 if=/dev/urandom of=$ATTACHMENT 2> /dev/null

    rm -f $SPOOLDIR/$TESTUSER
    
    if ! echo "$TEXTMESSAGE" | mail -a $ATTACHMENT -s "$SUBJECT" "$TESTUSER@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while so the mail will be delivered
    sleep $SLEEP_TIME

    if [ -f $SPOOLDIR/$TESTUSER ]; then
        printMessage $MSG_FAILED "Sending with attachment exceeding the message_size_limit"
        return $FAILED
    fi

    if ! ( ( tail /var/log/mail.err | grep -i 'file too big' ) ||
           ( tail /var/log/mail | grep -i 'file too big' ) ); then
        printMessage $MSG_FAILED "Sending with attachment exceeding the message_size_limit"
        return $FAILED
    fi

    printMessage $MSG_PASSED "Sending with attachment exceeding the message_size_limit"
    return $PASSED
}


function test03() 
{
    echo "Test #3: Send e-mails up to mailbox_size_limit"
    
    SUBJECT="Testing e-mail with attachment0006c"
    TEXTMESSAGE="Attached the testing e-mail0006c"
    dd bs=1024 count=10 if=/dev/urandom of=$ATTACHMENT 2> /dev/null

    rm -f $SPOOLDIR/$TESTUSER
    NUMBER_OF_MAILS=6
    for i in seq 1 NUMBER_OF_MAILS; do
        if ! echo "$TEXTMESSAGE" | mail -a $ATTACHMENT -s "$SUBJECT.$i" "$TESTUSER@localhost"; then
            printMessage $MSG_FAILED "Sending mail"
            return $FAILED
        fi
    done
    
    #sleep for a while so the mail will be delivered
    sleep $SLEEP_TIME

    MAILS=`grep '$SUBJECT' $SPOOLDIR/$TESTUSER | wc -l`

    if ! expr $MAILS '<' $NUMBER_OF_MAILS > /dev/null; then
        printMessage $MSG_FAILED "Send e-mails up to mailbox_size_limit: all e-mails were delivered"
        return $FAILED
    fi

    SIZE=`stat -c '%s' $SPOOLDIR/$TESTUSER`
    
    if ! expr $SIZE '<' $MAILBOX_SIZE_LIMIT > /dev/null; then
        printMessage $MSG_FAILED "Send e-mails up to mailbox_size_limit: mailbox larger than expected"
        return $FAILED
    fi

    printMessage $MSG_PASSED "Send e-mails up to mailbox_size_limit"
    return $PASSED
}

init
test01 || RESULT=$?
test02 || RESULT=$?
test03 || RESULT=$?

exit $RESULT
