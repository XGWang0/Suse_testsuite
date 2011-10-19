#!/bin/bash
# ****************************************************************************
# Copyright © 2011 Unpublished Work of SUSE. All Rights Reserved.
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
CONFIG="conf/5101.conf"
ORIGINAL_CONFIG="/etc/postfix/main.cf"
PGSQLCONFIG="conf/5101.pgsql.conf"
ORIGINAL_PGSQLCONFIG="/etc/postfix/pgsql-aliases.cf"
PGSQL="conf/5101.pgsql"
ORIGINAL_ALIASES="/etc/aliases"
PGHBA="conf/5101.pg_hba.conf"
ORIGINAL_PGHBA="/var/lib/pgsql/data/pg_hba.conf"



SPOOLDIR="/var/spool/mail"
DATABASE="postfix_test_db"
PGSQL_USER="postfix_test"
PGSQL_PASSWORD="postfix_test"
POSTGRES_USER="postgres"

trap "cleanup" 0

function enablePGSQL() {
    
    checkService "postgresql" || startService "postgresql" || return $FAILED
    
    echo "CREATE DATABASE $DATABASE;" | su "$POSTGRES_USER" -c "psql" > /dev/null || return $FAILED
    echo "CREATE USER $PGSQL_USER WITH UNENCRYPTED PASSWORD '$PGSQL_PASSWORD'" | 
         su "$POSTGRES_USER" -c "psql" > /dev/null || return $FAILED

    cat $PGSQL | su "$POSTGRES_USER" -c "psql $DATABASE" > /dev/null || return $FAILED
    echo "ALTER TABLE aliases owner to $PGSQL_USER;" | 
         su "$POSTGRES_USER" -c "psql $DATABASE" > /dev/null || return $FAILED
    return $PASSED
}

function cleanPGSQL() {

    echo "drop database $DATABASE" | su "$POSTGRES_USER" -c "psql" > /dev/null || return $FAILED
    echo "drop user $PGSQL_USER" | su "$POSTGRES_USER" -c "psql" > /dev/null || return $FAILED
    return $PASSED
}

function init() {
    if ! addUser "$TESTUSER"; then
        printMessage $MSG_ERROR "Unable to create user"
        exit $FAILED
    fi

    if ! ( copyConfig $CONFIG $ORIGINAL_CONFIG && copyConfig $PGHBA $ORIGINAL_PGHBA ); then
        printMessage $MSG_ERROR "Unable to copy config file"
        exit $FAILED
    fi

    if ! cp $PGSQLCONFIG $ORIGINAL_PGSQLCONFIG; then
        printMessage $MSG_ERROR "Unable to copy postgresql config"
        exit $FAILED
    fi

    if ! enablePGSQL; then
        printMessage $MSG_ERROR "postgresql initialization failed"
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

    if ! rm -f $ORIGINAL_PGSQLCONFIG; then
        printMessage $MSG_ERROR "Unable to copy aliases file"
    fi

    if ! newaliases; then
         printMessage $MSG_ERROR "Unable to execute newaliases"
    fi

    rm -f $SPOOLDIR/$TESTUSER

    if ! reloadService "postfix"; then
        printMessage $MSG_ERROR "Reload of postfix failed."
    fi

    if ! cleanPGSQL; then
         printMessage $MSG_ERROR "Unable to execute newaliases"
    fi
}

function test01() {
    printMessage $MSG_INFO "Test #1: Testing aliases from postgresql db"

    SUBJECT="Testing e-mail5101"
    TEXTMESSAGE="test email5101 yadda yadda yadda ######"
    if ! echo "$TEXTMESSAGE" | mail -s "$SUBJECT" "$TESTALIAS@localhost"; then
        printMessage $MSG_FAILED "Sending mail"
        return $FAILED
    fi
    
    #sleep for a while so the mail will be delivered
    sleep $SLEEP_TIME

    if grep "^Subject: $SUBJECT" $SPOOLDIR/$TESTUSER > /dev/null &&
       grep "$TEXTMESSAGE" $SPOOLDIR/$TESTUSER > /dev/null; then
    
        printMessage $MSG_PASSED "Sending mail (postgresql-alias)"    
        return $PASSED
    else
         printMessage $MSG_FAILED "Sending mail (postgresql-alias)"    
    fi

    return $FAILED
}

function test02() {
    printMessage $MSG_INFO "Test #2: Testing aliases from postgresql db (unpaid alias)"

    SUBJECT="Testing e-mail5101b"
    TEXTMESSAGE="test email5101b yadda yadda yadda ######"
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

