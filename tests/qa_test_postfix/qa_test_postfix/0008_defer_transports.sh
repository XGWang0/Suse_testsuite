#!/bin/bash
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
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


source libqainternal.lib.sh

TESTUSER=testmail01
RESULT=$ERROR
CONFIG="conf/0008.conf"
ORIGINAL_CONFIG="/etc/postfix/main.cf"
QUEUE_DIRECTORY="/var/spool/postfix"

SPOOLDIR="/var/spool/mail"
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

	# send all deferred mails before sending the testing one.
	sendmail -q

    rm -f $SPOOLDIR/$TESTUSER
}

function cleanup() {
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
    echo "Test #1: Testing the defer_transports option and sendmail -q"

    SUBJECT="Testing e-mail0008"
    TEXTMESSAGE="test email0008 yadda yadda yadda ######"

    
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTUSER@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while 
    sleep $SLEEP_TIME
    # now look to the spool. the mail must not be there

    if grep "^Subject: $SUBJECT" $SPOOLDIR/$TESTUSER > /dev/null &&
       grep "$TEXTMESSAGE" $SPOOLDIR/$TESTUSER > /dev/null; then
    
        printMessage $MSG_FAILED "deferring e-mail, mail was delivered"    
        return $FAILED
    fi
	
    # there should be something in the deferred queue
    if ! find "$QUEUE_DIRECTORY/deferred" -type f | grep 'deferred' > /dev/null; then
        printMessage $MSG_FAILED "deferring e-mail, deferred queue is empty"    
        return $FAILED
    fi

    #okay so far nothing try to deliver the mail
    sendmail -q

    #sleep for a while
    sleep $SLEEP_TIME

    # and now check the mail
    if grep "^Subject: $SUBJECT" $SPOOLDIR/$TESTUSER  > /dev/null &&
       grep "$TEXTMESSAGE" $SPOOLDIR/$TESTUSER > /dev/null; then
        printMessage $MSG_PASSED "deferring e-mail, mail was delivered after sendmail -q"    
        return $PASSED
    else
        printMessage $MSG_FAILED "deferring e-mail, mail was not delivered after sendmail -q"    
        return $FAILED
    fi
}


init
test01
exit $?

