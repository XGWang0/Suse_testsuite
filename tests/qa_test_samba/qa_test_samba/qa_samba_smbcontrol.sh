#!/bin/bash

#
# This test covers PDB testcase:
# - test smbcontrol
#

export TEST_NAME="Smbcontrol test"
export TEST_DESCRIPTION="Tests smbcontrol utility."

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
		printError "Unable to create samba configuration."
		return 1
	fi

	restartService smb && checkService smb || return 1
	restartService nmb && checkService nmb || return 1
	restartService winbind && checkService winbind || return 1

	return 0
}
# 
#run the test itself
function test_action()
{	
	# ping services using smbcontrol
	for SERVICE in smbd nmbd winbindd ;  do
		PID=`cat /var/run/samba/$SERVICE.pid`
		if [ `smbcontrol -t 2 $SERVICE ping | grep "PONG from pid $PID" | wc -l` -ne 1 ] ; then
			printError "No responce [or too many responces?] for ping from service $SERVICE($PID)"
			return $FAILED
		fi
	done
	
	#Passed
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
