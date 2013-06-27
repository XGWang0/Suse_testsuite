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
TESTALIAS2=testmail01_alias2
RESULT=$PASSED
SLEEP_TIME=${SLEEP_TIME:-5}
CONFIG="conf/5001.conf"
ORIGINAL_CONFIG="/etc/postfix/main.cf"
MYSQLCONFIG="conf/5001.mysql.conf"
ORIGINAL_MYSQLCONFIG="/etc/postfix/mysql-aliases.cf"
MYSQL="conf/5001.mysql"
ORIGINAL_ALIASES="/etc/aliases"

SPOOLDIR="/var/spool/mail"
DATABASE="postfix_test_db"
MYSQL_USER="postfix_test"
MYSQL_PASSWORD="postfix_test"

trap "cleanup" 0

function enableMySQL() {
    
    checkService "mysql" || startService "mysql" || return $FAILED
    echo "CREATE DATABASE $DATABASE;" | mysql -uroot || return $FAILED
    echo "GRANT ALL PRIVILEGES on *.* to '$MYSQL_USER'@'localhost' \
          IDENTIFIED by '$MYSQL_PASSWORD'" | mysql -uroot || return $FAILED

    cat $MYSQL | mysql -u$MYSQL_USER -p$MYSQL_PASSWORD $DATABASE || return $FAILED
    return $PASSED
}

function cleanMySQL() {
    echo "drop database $DATABASE" | mysql -uroot || return $FAILED
    return $PASSED
}

function init() {
    if ! addUser "$TESTUSER"; then
        printMessage $MSG_ERROR "Unable to create user"
        exit $FAILED
    fi

    if ! copyConfig $CONFIG $ORIGINAL_CONFIG; then
        printMessage $MSG_ERROR "Unable to copy config file"
        exit $FAILED
    fi

    if ! cp $MYSQLCONFIG $ORIGINAL_MYSQLCONFIG; then
        printMessage $MSG_ERROR "Unable to copy mysql config"
        exit $FAILED
    fi

    if ! enableMySQL; then
        printMessage $MSG_ERROR "mysql initialization failed"
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


}

function cleanup() {
    if ! delUser "$TESTUSER"; then
        printMessage $MSG_WARN "Unable to delete user"
    fi
 
    if ! removeConfig $ORIGINAL_CONFIG; then
        printMessage $MSG_WARN "Unable to remove the config file"
    fi

    if ! rm -f $ORIGINAL_MYSQLCONFIG; then
        printMessage $MSG_ERROR "Unable to copy aliases file"
    fi

    if ! newaliases; then
         printMessage $MSG_ERROR "Unable to execute newaliases"
    fi

    if ! cleanMySQL; then
         printMessage $MSG_ERROR "Unable to execute newaliases"
    fi


    rm -f $SPOOLDIR/$TESTUSER

    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
    fi
}

function test01() {
    printMessage $MSG_INFO "Test #1: Testing aliases from mysql db"

    SUBJECT="Testing e-mail5001"
    TEXTMESSAGE="test email5001 yadda yadda yadda ######"
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTALIAS@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while so the mail will be delivered
    sleep $SLEEP_TIME

    if grep "^Subject: $SUBJECT" $SPOOLDIR/$TESTUSER > /dev/null &&
       grep "$TEXTMESSAGE" $SPOOLDIR/$TESTUSER > /dev/null; then
    
        printMessage $MSG_PASSED "Sending mail (mysql-alias)"    
        return $PASSED
    else
         printMessage $MSG_FAILED "Sending mail (mysql-alias)"    
    fi

    return $FAILED
}

function test02() {
    printMessage $MSG_INFO "Test #2: Testing aliases from mysql db (unpaid alias)"

    SUBJECT="Testing e-mail5001b"
    TEXTMESSAGE="test email5001b yadda yadda yadda ######"
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTALIAS2@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while so the mail will be delivered
    sleep $SLEEP_TIME

    if grep "^Subject: $SUBJECT" $SPOOLDIR/$TESTUSER > /dev/null 2> /dev/null ||
       grep "$TEXTMESSAGE" $SPOOLDIR/$TESTUSER > /dev/null 2>/dev/null; then
    
        printMessage $MSG_FAILED "Sending mail (bad mysql-alias)"    
    else
        printMessage $MSG_PASSED "Sending mail (bad mysql-alias)"    
        return $PASSED
    fi

    return $FAILED
}


init
test01 || RESULT=$?
test02 || RESULT=$?
exit $RESULT

