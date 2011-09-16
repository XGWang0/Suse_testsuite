#!/bin/bash

#
# This test covers PDB testcase:
# - create user
# - delete user
# 
#

export TEST_NAME="User-management test"
export TEST_DESCRIPTION="Tests whether samba user management works correctly."

# the first param is the optional path to the root directory of tests
if [ "$1x" == "x" ]; then
    TEST_ROOT="/usr/share/qa/qa_test_samba"
else
    TEST_ROOT=$1
fi

source $TEST_ROOT/config
source $TEST_ROOT/shared/qa_samba_shared.sh

TESTUSER="smb_test_user"
TESTUSER_PASSWD1="asdk2-8s21"
TESTUSER_PASSWD2="as468d9#-1"
NETBIOS_NAME="`hostname --short`"
WORKGROUP="TEST_DOMAIN"



#initializes environmet, setup required services, etc.
function test_init()
{	

	#Add testing user
	addUser $TESTUSER || return 1

	changePassword $TESTUSER $TESTUSER_PASSWD1 || return 1
	
	backup "/etc/samba" || return 1
	

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

#run the test itself
function test_action()
{
	# Use rpcclient call to test user/passwd - use any simple command ;-)
	rpcclient -U "$TESTUSER%$TESTUSER_PASSWD1" -c srvinfo localhost > /dev/null 2> /dev/null || \
	rpcclient -U "$TESTUSER%$TESTUSER_PASSWD1" -c srvinfo $NETBIOS_NAME > /dev/null 2> /dev/null
	if [ $? -eq 0 ] ; then
		printFailed "Non-existing user authenticated with rpcclient"
		return $FAILED
	fi 

	#Add testing samba user
	( echo "$TESTUSER_PASSWD1" ; echo "$TESTUSER_PASSWD1" ) | smbpasswd -s -a $TESTUSER > /dev/null
	if [ $? -ne 0 ] ; then
		printFailed "Unable to create samba user $TESTUSER"
		return $FAILED
	fi

	# Use rpcclient call to test user/passwd - use any simple command ;-)
	rpcclient -U "$TESTUSER%$TESTUSER_PASSWD1" -c srvinfo localhost > /dev/null 2> /dev/null && \
	rpcclient -U "$TESTUSER%$TESTUSER_PASSWD1" -c srvinfo $NETBIOS_NAME > /dev/null 2> /dev/null
	if [ $? -ne 0 ] ; then
		printFailed "Unable to authenticate with rpcclient"
		return $FAILED
	fi 
	
	#try to authenticate with incorrect password and without password
	rpcclient -U "$TESTUSER%$TESTUSER_PASSWD2" -c srvinfo localhost > /dev/null 2> /dev/null || \
	rpcclient -U "$TESTUSER%$TESTUSER_PASSWD2" -c srvinfo $NETBIOS_NAME > /dev/null 2> /dev/null || \
	rpcclient -U "$TESTUSER%" -c srvinfo localhost > /dev/null 2> /dev/null || \
	rpcclient -U "$TESTUSER%" -c srvinfo $NETBIOS_NAME > /dev/null 2> /dev/null || \
	if [ $? -eq 0 ] ; then
		printFailed "User authenticated with incorrect/empty password with rpcclient"
		return $FAILED
	fi 

	#change password for samba user
	( echo "$TESTUSER_PASSWD2" ; echo "$TESTUSER_PASSWD2" ) | smbpasswd -s $TESTUSER
	if [ $? -ne 0 ] ; then
		printFailed "Unable to change password for samba user $TESTUSER"
		return $FAILED
	fi

	# Use rpcclient call to test user/passwd - use any simple command ;-)
	rpcclient -U "$TESTUSER%$TESTUSER_PASSWD2" -c srvinfo localhost > /dev/null 2> /dev/null && \
	rpcclient -U "$TESTUSER%$TESTUSER_PASSWD2" -c srvinfo $NETBIOS_NAME > /dev/null 2> /dev/null
	if [ $? -ne 0 ] ; then
		printFailed "Unable to authenticate with rpcclient"
		return $FAILED
	fi 
	
	#try to authenticate with incorrect password and without password
	rpcclient -U "$TESTUSER%$TESTUSER_PASSWD1" -c srvinfo localhost > /dev/null 2> /dev/null || \
	rpcclient -U "$TESTUSER%$TESTUSER_PASSWD1" -c srvinfo $NETBIOS_NAME > /dev/null 2> /dev/null || \
	rpcclient -U "$TESTUSER%" -c srvinfo localhost > /dev/null 2> /dev/null || \
	rpcclient -U "$TESTUSER%" -c srvinfo $NETBIOS_NAME > /dev/null 2> /dev/null || \
	if [ $? -eq 0 ] ; then
		printFailed "User authenticated with incorrect/empty password with rpcclient"
		return $FAILED
	fi 

	#delete samba user
	smbpasswd -x $TESTUSER > /dev/null
	if [ $? -ne 0 ] ; then
		printFailed "Unable to delete samba user $TESTUSER"
		return $FAILED
	fi
	
	# Use rpcclient call to test user/passwd - use any simple command ;-)
	rpcclient -U "$TESTUSER%$TESTUSER_PASSWD2" -c srvinfo localhost > /dev/null 2> /dev/null || \
	rpcclient -U "$TESTUSER%$TESTUSER_PASSWD2" -c srvinfo $NETBIOS_NAME > /dev/null 2> /dev/null
	if [ $? -eq 0 ] ; then
		printFailed "Non-existing user authenticated with rpcclient"
		return $FAILED
	fi 

	#Passed
	return $PASSED
}

#ifchanged somthing, make it into original state
function test_cleanup()
{
	result=0

	smbpasswd -x $TESTUSER > /dev/null

	delUser $TESTUSER || result=1

	restore_from_backup || result=1
	

	return $result	
}



#test itself
run_test
