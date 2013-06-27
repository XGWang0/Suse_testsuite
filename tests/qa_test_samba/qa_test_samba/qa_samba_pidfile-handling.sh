#!/bin/bash
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE. All Rights Reserved.
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
# - verify pidfile handling
# (- Start daemon and check if it is running)
# (- Stop daemon and check that it stopped)
# 
#

export TEST_NAME="Pidfile handling test"
export TEST_DESCRIPTION="Tests whether samba init scripts handles pidfiles correctly."

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
	backup "/etc/samba" || return 1
	
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
		printError " Unable to create samba configuration."
		return 1
	fi

	return 0
}

#run the test itself
function test_action()
{
	# Stop all

	stop_service_and_check_status smb nmb winbind || return 1
	
	#Basic pidfile all functionality
	start_service_and_check_status smb nmb winbind || return 1

	check_pidfiles || return 1
	
	stop_service_and_check_status winbind || return 1

	check_pidfiles || return 1

	stop_service_and_check_status smb || return 1

	check_pidfiles || return 1

	stop_service_and_check_status nmb || return 1

	start_service_and_check_status smb || return 1

	check_pidfiles || return 1
	
	restart_service_and_check_status smb || return 1
	
	start_service_and_check_status nmb winbind || return 1

	check_pidfiles || return 1
	
	stop_service_and_check_status smb nmb winbind || return 1
	
	check_pidfiles || return 1

	#Passed
	return 0
}

#ifchanged something, make it into original state
function test_cleanup()
{
	result=0

	restore_from_backup || return 1
	
	return $result
}

function stop_service_and_check_status
{
	for i in $@ ; do
		if ! stopService $i ; then
			printFailed "Error while stopping service $i"
			return 1;
		fi
		sleep 10
		if checkService $i ; then
			printFailed "Error while stopping service $i - service didn't stop"
			return 1;
		fi
	done

	return 0
}

function start_service_and_check_status
{
	for i in $@ ; do
		# let other initialize
		sleep 2
		if ! startService $i ; then
			printFailed "Error while starting service $i"
			return 1;
		fi
		sleep 10
		if ! checkService $i ; then
			printFailed "Error while starting service $i - service didn't start"
			return 1;
		fi
	done

	return 0
}

function restart_service_and_check_status
{
	for i in $@ ; do
		# let other initialize
		sleep 2
		if ! restartService $i ; then
			printFailed "Error while restarting service $i"
			return 1;
		fi
		sleep 10
		if ! checkService $i ; then
			printFailed "Error while restarting service $i - service didn't start"
			return 1;
		fi
	done

	return 0
}


function check_pidfiles()
{
	#needed to ensure that all changes it's state correctly
	sleep 2

	for SERVICE in smbd nmbd winbindd
	do
		PIDFILE="/var/run/samba/${SERVICE}.pid"
		if [ -f $PIDFILE ] ; then
			PID=`cat $PIDFILE`
			if [ "`ps h --pid $PID -o comm=`" != "$SERVICE" ] ; then
	                        printError "$SERVICE - pidfile handling doesn't work"
	                        return 1
	                fi
	        else
	                if [ `ps h -C $SERVICE | wc -l` -gt 0 ] ; then
	                        # There SHOULD be a pidfile, error
	                        printError "$SERVICE - pidfile handling doesn't work"
	                        return 1
	               	fi
	        fi
	done


	return 0
}

#test itself
run_test

