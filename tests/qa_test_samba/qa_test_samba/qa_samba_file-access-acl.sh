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


#
# This test covers PDB testcase:
# - access ACL (partly - no windows client access)
#
#
# THIS TEST ISNOT FINISHED YET

export TEST_NAME="File access test"
export TEST_DESCRIPTION="Tests whether samba server allows correct file access."

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
TEST_SHARE="share.$$"
TEST_SHARE_DIR=/tmp/$TEST_SHARE
TESTUSER1="smb_test_user_1"
TESTUSER1_PASSWD="asdk2-8s211"
TESTUSER2="smb_test_user_2"
TESTUSER2_PASSWD="asdk2-8s212"
TESTUSER3="smb_test_user_3"
TESTUSER3_PASSWD="asdk2-8s213"
TESTGROUP1="smb_test_group_1"
TESTGROUP2="smb_test_group_2"
MOUNTPOINT="/tmp/smb_test_mountpoint.$$"

#initializes environmet, setup required services, etc.
function test_init()
{
	chmod 777 $TEST_ROOT/data/file-access-acl/simple

	backup "/etc/samba" "/var/lib/samba/group_mapping.tdb" || return 1

	rm -fr /etc/samba/* /var/lib/samba/group_mapping.tdb

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
[homes]
        comment = Home Directories
        valid users = %S
        browseable = No
        read only = No
        create mask = 0640
        directory mask = 0750
--END_SMBCONF--

	if [ $? -ne 0 ] ; then
		printError "Unable to create samba configuration."
		return 1
	fi

	#Add testing groups & users
	group_add $TESTGROUP1 || return 1
	group_add $TESTGROUP2 || return 1
	user_add $TESTUSER1 $TESTGROUP1 || return 1
	user_passwd $TESTUSER1 $TESTUSER1_PASSWD || return 1
	user_add $TESTUSER2 $TESTGROUP1 || return 1
	user_passwd $TESTUSER2 $TESTUSER2_PASSWD || return 1
	user_add $TESTUSER3 $TESTGROUP2 || return 1
	user_passwd $TESTUSER3 $TESTUSER3_PASSWD || return 1


	( echo "$TESTUSER1_PASSWD" ; echo "$TESTUSER1_PASSWD" ) | smbpasswd -s -a $TESTUSER1 > /dev/null
	if [ $? -ne 0 ] ; then
		printError "Unable to create samba user $TESTUSER1"
		return 1
	fi
	( echo "$TESTUSER2_PASSWD" ; echo "$TESTUSER2_PASSWD" ) | smbpasswd -s -a $TESTUSER2 > /dev/null
	if [ $? -ne 0 ] ; then
		printError "Unable to create samba user $TESTUSER2"
		return 1
	fi
	( echo "$TESTUSER3_PASSWD" ; echo "$TESTUSER3_PASSWD" ) | smbpasswd -s -a $TESTUSER3 > /dev/null
	if [ $? -ne 0 ] ; then
		printError "Unable to create samba user $TESTUSER3"
		return 1
	fi

	#add samba shares
	for((u = 0; u < 8; u++)) ; do
		for((g = 0; g < 8; g++)) ; do
			for ((o = 0; o < 8; o++)) ; do
				mkdir -p "${TEST_SHARE_DIR}-$u$g$o"
				chmod 777 "${TEST_SHARE_DIR}-$u$g$o"
				chown root:root "${TEST_SHARE_DIR}-$u$g$o"
				cat >> /etc/samba/smb.conf << --END_SMBCONF--
[${TEST_SHARE}-$u$g$o]
	path = ${TEST_SHARE_DIR}-$u$g$o
	read only = no
	inherit acls = Yes
--END_SMBCONF--

				if [ $? -ne 0 ] ; then
					printError "Unable to create samba configuration."
					return 1
				fi

				#setfacl -m user:$TESTUSER1:$u,group:$TESTGROUP1:$g,other::$o ${TEST_SHARE_DIR}-$u$g$o || return 1

				#default acl - so it will be used on all newly created
				setfacl -d -m user:$TESTUSER1:$u,group:$TESTGROUP1:$g,other::$o,user::7,group::0 ${TEST_SHARE_DIR}-$u$g$o || return 1

				cat $TEST_ROOT/data/file-access-acl/simple > "${TEST_SHARE_DIR}-$u$g$o/file_restricted_access" || return 1
				chown root:root "${TEST_SHARE_DIR}-$u$g$o/file_restricted_access" || return 1
				chmod 700 "${TEST_SHARE_DIR}-$u$g$o/file_restricted_access" || return 1
				setfacl -m user:$TESTUSER1:$u,group:$TESTGROUP1:$g,other::$o "${TEST_SHARE_DIR}-$u$g$o/file_restricted_access" || return 1
				cat $TEST_ROOT/data/file-access-acl/simple > "${TEST_SHARE_DIR}-$u$g$o/file_full_access" || return 1
				chown root:root "${TEST_SHARE_DIR}-$u$g$o/file_full_access" || return 1
				chmod 700 "${TEST_SHARE_DIR}-$u$g$o/file_full_access" || return 1
				setfacl -m user:$TESTUSER1:7,group:$TESTGROUP1:7,other::7 "${TEST_SHARE_DIR}-$u$g$o/file_full_access" || return 1
			done
		done
	done



	mkdir -p $MOUNTPOINT || return 1
	chmod 777 $MOUNTPOINT


	restart_service_and_check_status smb nmb winbind || return 1

	#export groups using samba
	net -d1 groupmap add unixgroup=$TESTGROUP1 || return 1
	net -d1 groupmap add unixgroup=$TESTGROUP2 || return 1

	#I'm not sure whether it's really necessary - but it shouldn't hurt
	restart_service_and_check_status nscd || return 1

	return 0

}

#run the test itself
function test_action()
{
	retval=0

	for((u = 0; u < 8; u++)) ; do
		for((g = 0; g < 8; g++)) ; do
			for ((o = 0; o < 8; o++)) ; do
				for mode in owner group other ; do
					echo -n "Share $u$g$o mode $mode: "

					result=0
					case "$mode" in
						owner)
							user=$TESTUSER1
							password=$TESTUSER1_PASSWD
							tested_access=$u
							;;
						group)
							user=$TESTUSER2
							password=$TESTUSER2_PASSWD
							tested_access=$g
							;;
						other)
							user=$TESTUSER3
							password=$TESTUSER3_PASSWD
							tested_access=$o
							;;
					esac
					echo $TEST_SHARE-$u$g$o
					mount -t cifs //$NETBIOS_NAME/$TEST_SHARE-$u$g$o $MOUNTPOINT -o user=$user,password=$password ||result=1
					if [ $? -ne 0 ] ; then
						printError "Unable to mount share using cifs."
						result=1
					fi

					if [ $mode == "owner" ] ; then
						#create a file - this should be ok - and the file should have correct
						#access rights set because 'simple' has 777
						#su $user --command="cp $TEST_ROOT/data/file-access-acl/simple $MOUNTPOINT/test_file"
						cat $TEST_ROOT/data/file-access-acl/simple > $MOUNTPOINT/test_file
						if ! [ -f $MOUNTPOINT/test_file ] ; then
							printError "Creation of test file failed."
							result=1
						fi
						#change owner to root:root - otherwise owner access right will be used even while specifis acl entry is set (SUCKS!)
						chown root:root $TEST_SHARE_DIR-$u$g$o/test_file
						#chmod u+rwx $TEST_SHARE_DIR-$u$g$o/test_file
						#chmod g-rwx $TEST_SHARE_DIR-$u$g$o/test_file
						getfacl $TEST_SHARE_DIR-$u$g$o/test_file
					fi

					su $user --command="cat $MOUNTPOINT/file_full_access > /dev/null 2> /dev/null"
					if [ $? -ne 0 ] ; then
						printError "Unable to read full access file using cifs."
						result=1
					fi

					su $user --command="$MOUNTPOINT/file_full_access > /dev/null 2> /dev/null"
					if [ $? -ne 0 ] ; then
						printError "Unable to execute full access file using cifs."
						result=1
					fi

					su $user --command="echo 'echo' >> $MOUNTPOINT/file_full_access 2> /dev/null"
					if [ $? -ne 0 ] ; then
						printError "Unable to write full access file using cifs."
						result=1
					fi




					for filename in test_file file_restricted_access ; do
						#write executable into that file - it migh not be succesful yet because of rights
						# this is done again because the file was crrupted
						#RIGHTS="`stat -c %a ${TEST_SHARE_DIR}-$u$g$o/$filename`"
						#chmod 666 ${TEST_SHARE_DIR}-$u$g$o/$filename
						cat $TEST_ROOT/data/file-access-acl/simple > ${TEST_SHARE_DIR}-$u$g$o/$filename
						#chmod $RIGHTS ${TEST_SHARE_DIR}-$u$g$o/$filename

						su $user --command="$MOUNTPOINT/$filename > /dev/null 2> /dev/null" ; resultx=$?
						su $user --command="cat $MOUNTPOINT/$filename > /dev/null 2> /dev/null" ; resultr=$?
						su $user --command="( echo 'echo' >> $MOUNTPOINT/$filename ) > /dev/null 2> /dev/null" ; resultw=$?

						#Ugly long case - just check whether failed what should fail and succeeded what should succeed ;-)
						case "$tested_access" in
							0)
								if [ $resultr -eq 0 ] ; then
									printError "Successfull read of file $filename."
									result=1
								fi
								if [ $resultw -eq 0 ] ; then
									printError "Successfull write of file $filename."
									result=1
								fi
								if [ $resultx -eq 0 ] ; then
									printError "Successfull execution of file $filename."
									result=1
								fi
								;;
							1)
								if [ $resultr -eq 0 ] ; then
									printError "Successfull read of file $filename."
									result=1
								fi
								if [ $resultw -eq 0 ] ; then
									printError "Successfull write of file $filename."
									result=1
								fi
								if [ $resultx -ne 0 ] ; then
									printError "Failed execution of file $filename."
									result=1
								fi
								;;
							2)
								if [ $resultr -eq 0 ] ; then
									printError "Successfull read of file $filename."
									result=1
								fi
								if [ $resultw -ne 0 ] ; then
									printError "Failed write of file $filename."
									result=1
								fi
								if [ $resultx -eq 0 ] ; then
									printError "Successfull execution of file $filename."
									result=1
								fi
								;;
							3)
								if [ $resultr -eq 0 ] ; then
									printError "Successfull read of file $filename."
									result=1
								fi
								if [ $resultw -ne 0 ] ; then
									printError "Failed write of file $filename."
									result=1
								fi
								if [ $resultx -eq 0 ] ; then
									printError "Successfull execution of file $filename. Strange, this shouldn't be possible."
									result=1
								fi
								;;
							4)
								if [ $resultr -ne 0 ] ; then
									printError "Failed read of file $filename."
									result=1
								fi
								if [ $resultw -eq 0 ] ; then
									printError "Successfull write of file $filename."
									result=1
								fi
								if [ $resultx -eq 0 ] ; then
									printError "Successfull execution of file $filename."
									result=1
								fi
								;;
							5)
								if [ $resultr -ne 0 ] ; then
									printError "Failed read of file $filename."
									result=1
								fi
								if [ $resultw -eq 0 ] ; then
									printError "Successfull write of file $filename."
									result=1
								fi
								if [ $resultx -ne 0 ] ; then
									printError "Failed execution of file $filename."
									result=1
								fi
								;;
							6)
								if [ $resultr -ne 0 ] ; then
									printError "Failed read of file $filename."
									result=1
								fi
								if [ $resultw -ne 0 ] ; then
									printError "Failed write of file $filename."
									result=1
								fi
								if [ $resultx -eq 0 ] ; then
									printError "Successfull execution of file $filename."
									result=1
								fi
								;;
							7)
								if [ $resultr -ne 0 ] ; then
									printError "Failed read of file $filename."
									result=1
								fi
								if [ $resultw -ne 0 ] ; then
									printError "Failed write of file $filename."
									result=1
								fi
								if [ $resultx -ne 0 ] ; then
									printError "Failed execution of file $filename."
									result=1
								fi
								;;
						esac
					done

					if [ $result -eq 0 ] ; then
						echo "OK"
					else
						echo "FAILED"
						retval=1
					fi

					umount $MOUNTPOINT
				done
			done
		done
	done

	return $retval
}

#ifchanged somthing, make it into original state
function test_cleanup()
{

	result=0

	umount $MOUNTPOINT > /dev/null 2> /dev/null
	rmdir $MOUNTPOINT

	# delete group mappings
	net -d1 groupmap delete ntgroup=$TESTGROUP1
	net -d1 groupmap delete ntgroup=$TESTGROUP2

	#delete samba users
	smbpasswd -x $TESTUSER1 > /dev/null
	if [ $? -ne 0 ] ; then
		printError "Unable to delete samba user $TESTUSER1"
		result=1
	fi

	smbpasswd -x $TESTUSER2 > /dev/null
	if [ $? -ne 0 ] ; then
		printError "Unable to delete samba user $TESTUSER2"
		result=1
	fi

	smbpasswd -x $TESTUSER3 > /dev/null
	if [ $? -ne 0 ] ; then
		printError "Unable to delete samba user $TESTUSER3"
		result=1
	fi

	user_del $TESTUSER1 || result=1
	user_del $TESTUSER2 || result=1
	user_del $TESTUSER3 || result=1
	group_del $TESTGROUP1 || result=1
	group_del $TESTGROUP2 || result=1

	for((u = 0; u < 8; u++)) ; do
		for((g = 0; g < 8; g++)) ; do
			for ((o = 0; o < 8; o++)) ; do
				rm -fr "${TEST_SHARE_DIR}-$u$g$o"
			done
		done
	done

	restore_from_backup || result=1


	return $result
}



#test itself
run_test

