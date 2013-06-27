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


#
# This test covers PDB testcase:
# - Start daemon and check if it is running
# - Stop daemon and check that it stopped
# 
#

export TEST_NAME="Start-stop test"
export TEST_DESCRIPTION="Tests samba whether samba starts & stops correctly. Uses rcXXX commands and YaST to start-stop the daemon."

# the first param is the optional path to the root directory of tests
if [ "$1x" == "x" ]; then
    TEST_ROOT="/usr/share/qa/qa_test_samba"
else
    TEST_ROOT=$1
fi

source $TEST_ROOT/config
source $TEST_ROOT/shared/qa_samba_shared.sh


NETBIOS_NAME="`hostname --short`"
WORKGROUP="TEST_DOMAIN"

#initializes environmet, setup required services, etc.
function test_init()
{
	backup "/etc/samba" || return $ERROR
	
	#samba config
	rm -fr /etc/samba/*

	cat > /etc/samba/smb.conf << --END_SMBCONF--
[global]
	netbios name = $NETBIOS_NAME
	workgroup = $WORKGROUP
	passdb backend = smbpasswd
	os level = 33
	preferred master = auto
	domain master = yes
	local master = yes
	security = user
	domain logons = yes
	logon path = \\%N\profiles\%U
	logon drive = H:
	logon home = \\%N\%U\.9xprofile
[netlogon]
	path = /var/lib/samba/netlogon
	read only = yes
	write list = root
[profiles]
	path = %H
	read only = no
	create mask = 0600
	directory mask = 0700
--END_SMBCONF--
	
	if [ $? -ne 0 ] ; then
		printError "Unable to create samba configuration."
		return $ERROR
	fi

	return 0
}

#run the test itself
function test_action()
{
	# Stop all
	for SERVICE in smb nmb winbind ; do 
		stopService $SERVICE || return $FAILED
		sleep 10
		checkService $SERVICE && return $FAILED
		check_process_exists ${SERVICE}d
		if [ $? -ne 1 ] ; then
			printFailed "Unable to stop $SERVICE service."
			return $FAILED
		fi
	done
	
	
	#Start all
	for SERVICE in smb nmb winbind ; do 
		# wait for prev. services to start/stop
		sleep 2
		startService $SERVICE || return $FAILED
		sleep 10
		checkService $SERVICE || return $FAILED
		check_process_exists ${SERVICE}d
		if [ $? -ne 0 ] ; then
			printFailed "Unable to start $SERVICE service."
			return $FAILED 
		fi
	done
	
	
	return $PASSED
}

#ifchanged somthing, make it into original state
function test_cleanup()
{
	result=0
	
	restore_from_backup || result=1
	

	return $result
}



#test itself
run_test

