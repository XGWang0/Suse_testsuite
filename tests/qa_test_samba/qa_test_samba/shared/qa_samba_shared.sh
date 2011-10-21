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


export LANG=C

source /usr/share/qa/qa_internalapi/sh/libqainternal.lib.sh

source /usr/share/qa/qa_test_samba/config

BACKUP_FILE="/tmp/backup_conf.$$.tar.bz2"



# 0 = process exists
# 1 = dosn't exixt
# param - process name
function check_process_exists()
{
	if [ `ps h -C "$1" | wc -l` -gt 0 ] ; then
		return 0
	else
		return 1
	fi	
}

#create a new group
#param - groupname
function group_add()
{
	getent group $1 > /dev/null 2> /dev/null
	if [ $? -eq 0 ] ; then
		printError "Group $1 already exists. Unble to add. Terminating"
		return 1
	fi

	groupadd $1 > /dev/null 2> /dev/null
	
	if [ $? -ne 0 ] ; then
		printError "Unable to add group $1. Terminating"
		return 1
	fi

	return 0
}

#delete group
#param - groupname
function group_del()
{
	getent group $1 > /dev/null 2> /dev/null
	if [ $? -ne 0 ] ; then
		printError "Group $1 doesn't exist. Unble to delete. Terminating"
		return 1
	fi

	groupdel $1 > /dev/null 2> /dev/null
	
	if [ $? -ne 0 ] ; then
		printError "Unable to delete group $1. Terminating"
		return 1
	fi

	return 0
}


#creates a backup of files/dirs specified as params - to some temp file - one backup per process can exist
function backup
{
	if [ -e $BACKUP_FILE ] ; then
		printError "Backup file $BACKUP_FILE already exists. Terminating"
		return 1
	fi
	list=""
	for i in  $@ ; do
		[ -x "$i" ] && list="$list $i"
	done

	tar cjPpf $BACKUP_FILE $list
	if [ $? -ne 0 ] ; then
		printError "Error during backup creation."
		return 1
	fi

	return 0
}

#restores files/dirs from backup - one backup per process can exist - and DELETES the backup
function restore_from_backup
{
	if [ ! -e $BACKUP_FILE ] ; then
		printError "Backup file $BACKUP_FILE does not exist. Terminating"
		return 1
	fi
	tar xjPpf $BACKUP_FILE $@
	result=$?
	stopService smb && stopService nmb && stopService winbind
	if [ $? -ne 0 ] ; then
		printError "Error Restart samba after test failed! Please restart it manually"
	fi
	if [ $result -ne 0 ] ; then
		printError "Error during backup restoration/extraction."
		return 1
	fi

	#restored - so remove the backup
	rm $BACKUP_FILE

	return 0
}

#run test itself
function run_test
{
	stopService smb 
	stopService nmb 
	stopService winbind
	for p in smbd nmbd winbindd ; do 
		check_process_exists $p && printInfo "Process $p is running, doing kill" && killall $p
	done

	if [ "$HARDKILL_RUNNING_INSTANCES_AT_START" == "yes" ] ; then 
		for p in smbd nmbd winbindd ; do 
			check_process_exists $p && printInfo "Process $p is does not react to kill, doing kill -9" && killall -9 $p
		done
		
		rm -fr /var/run/samba/*
	fi

	test_init
	if [ $? -ne 0 ] ; then
		printError "Initialization failed, running cleanup - some errors might occur due to improper initialization."
		test_cleanup
		exit $ERROR
	fi

	if ! testparm -s > /dev/null ; then
		printError "Testparm says that the config is invalid!!!"
		testparm -s
		exit $ERROR
	fi

	#give services time to successfully load
	sleep 5

	test_action
	test_result=$?

	test_cleanup
	if [ $? -ne 0 ] ; then
		printWarning "Cleanup failed - this might (but shouldn't) cause failure of next tests."
	fi

	[ $test_result -eq $PASSED ] && printPassed "Test passed"

	exit $test_result
}

