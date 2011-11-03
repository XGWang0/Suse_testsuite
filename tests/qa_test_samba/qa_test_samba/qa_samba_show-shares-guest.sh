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
# - show shares
# - private file shares (partly)
#
# (homes share shouldn't be on the list)

export TEST_NAME="List of samba shares test"
export TEST_DESCRIPTION="Tests whether samba server publishes correct list of shares."

# the first param is the optional path to the root directory of tests
if [ "$1x" == "x" ]; then
    TEST_ROOT="/usr/share/qa/qa_test_samba"
else
    TEST_ROOT=$1
fi

source $TEST_ROOT/config
source $TEST_ROOT/shared/qa_samba_shared.sh


NETBIOS_NAME="`hostname --short`"
WORKGROUP="TEST_WORKGRP"
TEST_SHARE1="sh-1.$$"
TEST_SHARE1_DIR=/tmp/$TEST_SHARE1
TEST_SHARE2="sh-2.$$"
TEST_SHARE2_DIR=/tmp/$TEST_SHARE2
TEST_SHARE3="sh-3.$$"
TEST_SHARE3_DIR=/tmp/$TEST_SHARE3
TMP_FILE="/tmp/samba_test.$$"



#initializes environmet, setup required services, etc.
function test_init()
{
	#create file with list of shares - sorted
	#there used to be ADMIN$ share as well
	cat << --END_TMPFILE-- | sort > $TMP_FILE
netlogon
profiles
$TEST_SHARE1
$TEST_SHARE2
$TEST_SHARE3
--END_TMPFILE--

	if [ $? -ne 0 ] ; then
		printError "Unable to create temporary file."
		return 1
	fi
	backup "/etc/samba" || return 1

	rm -fr /etc/samba/*
	mkdir $TEST_SHARE1_DIR
	mkdir $TEST_SHARE2_DIR
	mkdir $TEST_SHARE3_DIR

	cat > /etc/samba/smb.conf << --END_SMBCONF--
[global]
	netbios name = $NETBIOS_NAME
	workgroup = $WORKGROUP
	passdb backend = smbpasswd
	os level = 33
	preferred master = auto
	map to guest = Bad User
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
[homes]
        comment = Home Directories
        valid users = %S
        browseable = No
        read only = No
        create mask = 0640
        directory mask = 0750
[$TEST_SHARE1]
	path = $TEST_SHARE1_DIR
	read only = no
	create mask = 0600
	guest ok = no
[$TEST_SHARE2]
	path = $TEST_SHARE2_DIR
	read only = no
	create mask = 0600
	guest ok = no
[$TEST_SHARE3]
	path = $TEST_SHARE3_DIR
	read only = no
	create mask = 0600
	guest ok = no

--END_SMBCONF--

	if [ $? -ne 0 ] ; then
		printError "Unable to create samba configuration."
		return 1
	fi

	restartService smb && checkService smb || return 1
	restartService nmb && checkService nmb || return 1

	return 0

}

#run the test itself
function test_action()
{

	# use net share to test	- since root should not be know - guest
	net share -S localhost -U 'root%' | grep -v 'ADMIN\$\|IPC\$' | sort | cmp -s $TMP_FILE
	if [ $? -ne 0 ] ; then
		printError "net share retured incorrect list of shares."
		return $FAILED
	fi

	printInfo "'net' test passed"

	# Use rpcclient call to test
	rpcclient -N -c netshareenum localhost | grep -v 'ADMIN\$\|IPC\$' | grep '^netname: ' \
	| sed 's/^netname: \([^ \t]\+\).*/\1/' | sort | cmp -s $TMP_FILE
	if [ $? -ne 0 ] ; then
		printError "rpcclient retured incorrect list of shares."
		return $FAILED
	fi

	printInfo "'rpcclient' test passed"

	# Use smbclient to test
	# We need to parse that ugly output ;-) - use subshell so we can read lines and parse them
	smbclient -N -L $NETBIOS_NAME 2> /dev/null \
	| (
		LINE="xxx"
		until [ "$LINE" == "" ] ; do
			LINE="`line | sed 's/^[ \t]*$//'`"
			#if [ $? -ne 0 ] ; then
			#	echo "Error: smbclient retured incorrect list of shares."
			#	return $FAILED
			#fi
		done


		#after  empty line - two headers
		line > /dev/null
		line > /dev/null

		# so, the lines we're interested in
		LINE="`line`"

		while [ "`echo $LINE | sed 's/^[ \t]*$//'`" != "" ] ; do
			echo "$LINE" | sed 's/^[ \t]\+\([^ \t]\+\)[ \t]\+.*/\1/'
			#next line
			LINE="`line`"
		done

	) | grep -v 'ADMIN\$\|IPC\$' | sort | cmp -s $TMP_FILE

	if [ $? -ne 0 ] ; then
		printError "smbclient retured incorrect list of shares."
		return $FAILED
	fi

	printInfo "'smbclient' test passed"

	#Passed
	return $PASSED
}

#ifchanged somthing, make it into original state
function test_cleanup()
{
	result=0


	rm $TMP_FILE

	rmdir $TEST_SHARE1_DIR
	rmdir $TEST_SHARE2_DIR
	rmdir $TEST_SHARE3_DIR

	restore_from_backup || result=1

	return $result
}



#test itself
run_test

