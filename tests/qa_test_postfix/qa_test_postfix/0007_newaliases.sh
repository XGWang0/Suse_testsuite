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
TESTALIAS=testmail01_alias
RESULT=$PASSED
SLEEP_TIME=${SLEEP_TIME:-10}
CONFIG="conf/0007.conf"
ORIGINAL_CONFIG="/etc/postfix/main.cf"
ALIASES="conf/0007.aliases"
ORIGINAL_ALIASES="/etc/aliases"

ALIASES2="conf/0007.aliases2"
ORIGINAL_ALIASES2="/tmp/aliases2"
COPY_FILE01="/tmp/copy01"
COPY_FILE02="/tmp/copy02"
COPY_FILE03="/tmp/copy03"
COPY_FILE04="/tmp/copy04"
TESTALIAS_FILE="file_alias"
TESTALIAS_PIPE="pipe_alias"
TESTALIAS_INCLUDE="include_alias"

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

    if ! copyConfig $ALIASES $ORIGINAL_ALIASES; then
        printMessage $MSG_ERROR "Unable to copy aliases file"
        exit $FAILED
    fi

    if ! cp "$ALIASES2" "$ORIGINAL_ALIASES2"; then
        printMessage $MSG_ERROR "Unable to copy aliases file"
        exit $FAILED
    fi

    rm -f $COPY_FILE01 $COPY_FILE02 $COPY_FILE03 $COPY_FILE04

    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
        exit $FAILED
    fi

    if ! newaliases; then
        printMessage $MSG_ERROR "Unable to execute newaliases"
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

    if ! removeConfig $ORIGINAL_ALIASES; then
        printMessage $MSG_ERROR "Unable to copy aliases file"
    fi

    if ! newaliases; then
         printMessage $MSG_ERROR "Unable to execute newaliases"
    fi

    rm -f $SPOOLDIR/$TESTUSER

    rm -f $COPY_FILE01 $COPY_FILE02 $COPY_FILE03 $COPY_FILE04 $ORIGINAL_ALIASES2
   
    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
    fi
}

function test01() {
    printMessage $MSG_INFO "Test #1: Testing the newaliases command and sending mail to the alias"

    SUBJECT="Testing e-mail0007"
    TEXTMESSAGE="test email0007 yadda yadda yadda ######"
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTALIAS@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while so the mail will be delivered
    sleep $SLEEP_TIME

    if grep "^Subject: $SUBJECT" $SPOOLDIR/$TESTUSER > /dev/null &&
       grep "$TEXTMESSAGE" $SPOOLDIR/$TESTUSER > /dev/null; then
    
        printMessage $MSG_PASSED "Sending mail (alias)"    
        return $PASSED
    else
         printMessage $MSG_FAILED "Sending mail (alias)"    
    fi

    return $FAILED
}

function test02() {
    printMessage $MSG_INFO "Test #2: alias to file"

    SUBJECT="Testing e-mail0007b"
    TEXTMESSAGE="test email0007b yadda yadda yadda ######"
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTALIAS_FILE@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while so the mail will be delivered
    sleep $SLEEP_TIME

    if grep "^Subject: $SUBJECT" $COPY_FILE01 > /dev/null &&
       grep "$TEXTMESSAGE" $COPY_FILE01 > /dev/null &&
       grep "^Subject: $SUBJECT" $COPY_FILE02 > /dev/null &&
       grep "$TEXTMESSAGE" $COPY_FILE02 > /dev/null; then
    
        printMessage $MSG_PASSED "Sending mail (alias to file)"    
        return $PASSED
    else
        printMessage $MSG_FAILED "Sending mail (alias to file)"    
    fi

    return $FAILED
}

function test03() {
    printMessage $MSG_INFO "Test #3: alias to pipe"

    SUBJECT="Testing e-mail0007c"
    TEXTMESSAGE="test email0007c yadda yadda yadda ######"
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTALIAS_PIPE@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while so the mail will be delivered
    sleep $SLEEP_TIME

    if grep "^Subject: $SUBJECT" $COPY_FILE03 > /dev/null &&
       grep "$TEXTMESSAGE" $COPY_FILE03 > /dev/null; then
    
        printMessage $MSG_PASSED "Sending mail (alias to pipe)"    
        return $PASSED
    else
        printMessage $MSG_FAILED "Sending mail (alias to pipe)"    
    fi

    return $FAILED
}

function test04() {
    printMessage $MSG_INFO "Test #4: include alias"

    SUBJECT="Testing e-mail0007d"
    TEXTMESSAGE="test email0007d yadda yadda yadda ######"
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTALIAS_INCLUDE@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while so the mail will be delivered
    sleep $SLEEP_TIME

    if grep "^Subject: $SUBJECT" $COPY_FILE04 > /dev/null &&
       grep "$TEXTMESSAGE" $COPY_FILE04 > /dev/null &&
       grep "^Subject: $SUBJECT" $SPOOLDIR/$TESTUSER > /dev/null &&
       grep "$TEXTMESSAGE" $SPOOLDIR/$TESTUSER > /dev/null; then
      
        printMessage $MSG_PASSED "Sending mail (alias from included file)"    
        return $PASSED
    else
        printMessage $MSG_FAILED "Sending mail (alias from included file)"    
    fi

    return $FAILED
}

init
test01 || RESULT=$?
test02 || RESULT=$?
test03 || RESULT=$?
test04 || RESULT=$?
exit $RESULT

